# GitHub + Terraform Workflow

## Table of Contents
- [GitHub App Setup](#github-app-setup)
- [Branch Tracking and Run Types](#branch-tracking-and-run-types)
- [PR Workflow and Status Checks](#pr-workflow-and-status-checks)
- [Push Events and Push Policies](#push-events-and-push-policies)
- [Multi-Stack GitFlow Patterns](#multi-stack-gitflow-patterns)
- [Monorepo: Project Root and Sparse Checkout](#monorepo-project-root-and-sparse-checkout)

---

## GitHub App Setup

### Wizard (recommended)

1. _Integrate Services > Discover all integrations_ → GitHub → **Set up via wizard**
2. Integration name (immutable — used in webhook URL), type (default or Space-scoped), VCS checks mode
3. GitHub redirects back; install app on org/repo

### Manual App Creation

Create GitHub App with:

**Repository permissions:**

| Permission      | Access       |
|-----------------|--------------|
| Checks          | Read & write |
| Commit statuses | Read & write |
| Contents        | Read-only    |
| Deployments     | Read & write |
| Metadata        | Read-only    |
| Pull requests   | Read & write |
| Webhooks        | Read & write |

**Organization permissions:** Check run, Issue comment, Organization, Pull request, Pull request review, Push, Repository

**Key fields back in Spacelift:**
- API host URL: `https://api.github.com`
- App ID (from GitHub App's About section)
- Private key (generate in GitHub App → Private keys section)
- **Use Git checkout**: required for sparse checkout

### VCS Check Modes

- **Individual checks** — one check per stack (default)
- **Aggregated checks** — grouped as `spacelift/tracked`, `spacelift/proposed`, `spacelift/modules`

### Webhook Events Spacelift Subscribes To

| Event | Purpose |
|-------|---------|
| Push | Create/cancel runs; match against tracked stacks |
| Pull request (open/sync/close) | Show in stack PRs tab; deduplicate with push events |
| Pull request review | Re-evaluate push policies (enables review-based gating) |
| App installation | Create Spacelift account |
| Repository renamed | Update stack references |

---

## Branch Tracking and Run Types

Each stack has one **tracked branch** (e.g., `main`).

| Push target | Default behavior |
|-------------|-----------------|
| Tracked branch | **Tracked run** → can be applied |
| Any other branch (with open PR) | **Proposed run** → plan-only, reports to PR |

The tracked branch is always available in push policy input as `input.stack.branch`.

### GitHub Deployment Status

Tracked runs create GitHub deployment records:
- Planning with changes detected → `Pending`
- Discarded or failed apply → `Failure`
- Successful apply → `Active`

Deployment environment name = stack name. Override with label `ghenv:my-env-name`. Disable with `ghenv:-`.

---

## PR Workflow and Status Checks

### Typical PR Flow

```
feature branch push
  → push event received
  → push policy evaluates → propose
  → proposed run: terraform plan
  → commit status reported to PR (in-progress → success/failure)

PR merged to main
  → push event received
  → push policy evaluates → track
  → tracked run: terraform plan
  → if autodeploy: auto-apply
  → else: unconfirmed state, await confirmation
```

### PR Status Check States

1. Initializing → yellow (in progress)
2. Succeeded without changes → green
3. Succeeded with changes → green (with resource diff)
4. Failed → red

### Branch Protection Setup

In GitHub branch settings, require status check from your stack before merge:
- Check name matches stack name (or `spacelift/proposed` for aggregated mode)
- Optionally: require branches be up-to-date before merging (triggers fresh run on stale PRs)

### Prevent Direct GitHub Deploys (Plan Policy)

```opa
package spacelift

deny contains "Do not deploy from GitHub" if {
  input.spacelift.run.type == "TRACKED"
  startswith(input.spacelift.run.triggered_by, "github/")
}
```

### Event Deduplication

When a PR push arrives, Spacelift receives both a _push_ event and a _pull_request (synchronized)_ event. These are deduplicated by `(commit SHA, run type)` — only one run is created. The push event (without `pull_request` data) is typically retained.

To ensure `pull_request_id` is available downstream (e.g., notification policies), ignore pure push events:

```opa
package spacelift

is_pr if not is_null(input.pull_request)
track if input.push.branch == input.stack.branch
propose if is_pr
ignore if { not track; not is_pr }
```

Note: this ignores direct pushes to tracked branch without a PR.

---

## Push Events and Push Policies

### Policy Outcomes

| Output | Effect |
|--------|--------|
| `track` | Set head commit, create tracked run |
| `propose` | Create proposed run (plan only) |
| `ignore` | No run created |
| `notify` | Send notification (without creating run) |
| `cancel` | Cancel in-progress runs |

### Default Behavior (No Push Policy)

- Push to tracked branch + files changed in project root → tracked run
- Push to other branch → proposed run if PR exists

### Common Patterns

**Standard GitOps (track main, propose on PRs):**
```opa
package spacelift

track if input.push.branch == input.stack.branch
propose if not is_null(input.pull_request)
ignore if { not track; not propose }
```

**PR-only workflow (no direct push deploys):**
```opa
package spacelift

is_pr if not is_null(input.pull_request)
track if { is_pr; input.push.branch == input.stack.branch }
propose if is_pr
ignore if not is_pr
```

**PR label gating (require "deploy" label):**
```opa
package spacelift

track if {
  not is_null(input.pull_request)
  some label in input.pull_request.labels
  label == "deploy"
}
propose if true
```

**Cancel queued proposed runs on new push:**
```opa
package spacelift

cancel contains run.id if {
  some run in input.in_progress
  run.type == "PROPOSED"
  run.state == "QUEUED"
}
```

**Path-based filtering (monorepo):**
```opa
package spacelift

track if {
  input.push.branch == input.stack.branch
  some file in input.push.affected_files
  startswith(file, "infra/networking/")
}
propose if {
  not is_null(input.pull_request)
  some file in input.push.affected_files
  startswith(file, "infra/networking/")
}
ignore if { not track; not propose }
```

### Key Push Policy Input Fields

```json
{
  "push": {
    "branch": "string",
    "affected_files": ["string"],
    "tag": "string or null",
    "message": "string"
  },
  "pull_request": {
    "action": "opened | synchronized | closed | labeled",
    "draft": "boolean",
    "labels": ["string"],
    "head": { "branch": "string", "sha": "string" },
    "base": { "branch": "string" },
    "id": "number"
  },
  "stack": {
    "id": "string",
    "branch": "string",
    "project_root": "string or null",
    "labels": ["string"]
  },
  "in_progress": [{ "id": "string", "type": "string", "state": "string" }]
}
```

---

## Multi-Stack GitFlow Patterns

### Single Stack (simple)

- One stack → `main` branch
- Feature branches → PRs → proposed runs
- Merge → tracked run → (auto)deploy

### Staging + Production GitFlow

```
feature/* → staging branch → staging stack (proposed → tracked)
staging branch → PR to production branch → production stack (proposed)
Merge → production stack (tracked → apply)
```

- Protect both branches in GitHub
- Staging: require green status check, optional manual review
- Production: require **both** green status check AND manual approval

### Multi-Directory Monorepo

- Multiple stacks, same repo, different `project_root` settings
- Push policies filter by `input.push.affected_files`
- Each stack only triggers when its directory changes

### Stack Dependencies (prefer over trigger policies)

Use Spacelift stack dependencies for ordered deployment chains:
- Networking → Platform → Applications
- Dependencies run after parent finishes successfully
- See `references/stack-configuration.md` for dependency config

---

## Monorepo: Project Root and Sparse Checkout

### Project Root

Set on stack: `project_root = "infra/networking"`. All Terraform commands run from this subdirectory.

Can also be set per-run via `.spacelift/config.yml`:
```yaml
version: "1"
stack_defaults:
  project_root: infra/networking
```

### Sparse Checkout

Requires **Use Git checkout** enabled on GitHub integration.

Limits which paths are downloaded for each run. Set via `project_globs` on stack:
- `infra/networking/**` — only download the networking module
- `modules/shared/**` — include shared modules

Reduces clone time for large monorepos. Requires git checkout mode (not API tarball download).
