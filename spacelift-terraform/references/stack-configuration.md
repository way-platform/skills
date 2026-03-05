# Stack Configuration

## Table of Contents
- [Stack Creation Fields](#stack-creation-fields)
- [VCS Settings](#vcs-settings)
- [Terraform-Specific Settings](#terraform-specific-settings)
- [Behavior Settings](#behavior-settings)
- [Scheduling](#scheduling)
- [Stack Hooks](#stack-hooks)
- [Stack Dependencies](#stack-dependencies)

---

## Stack Creation Fields

| Field | Description |
|-------|-------------|
| Name | Unique stack identifier (slug-ified, immutable) |
| Space | Organizational space (default: `root`) |
| Labels | Arbitrary key or `key:value` tags; used by push/trigger policies and auto-attach |
| Description | Markdown free-text |
| Administrative | Grants stack a Space Admin API token (deprecated — use stack role attachments) |

---

## VCS Settings

| Field | Description |
|-------|-------------|
| Integration | Which GitHub App integration to use |
| Repository | `org/repo` |
| Branch | Tracked branch (pushes here → tracked runs) |
| Project root | Subdirectory for Terraform root; all commands run here |
| Project globs | Sparse checkout paths (requires git checkout mode on integration) |

### Branch Behavior

- Push to **tracked branch** → tracked run (can apply)
- Push to **any other branch** + open PR → proposed run (plan only)
- Override entirely with a push policy (see `references/github-terraform-workflow.md`)

---

## Terraform-Specific Settings

| Field | Description |
|-------|-------------|
| Terraform version | Pin version (e.g., `1.9.0`); `latest` tracks latest stable |
| Workspace | Terraform workspace name (default: `default`) |
| State backend | Managed by Spacelift by default; can point to external backend |
| Lock file | Enforce `.terraform.lock.hcl` existence and consistency |
| Runner image | Custom Docker image for runs (default: `public.ecr.aws/spacelift/runner-terraform:latest`) |

### Runtime Config Override (`.spacelift/config.yml`)

Per-run settings that override stack defaults:

```yaml
version: "1"
stack_defaults:
  project_root: infra/networking
  runner_image: my-registry/custom-runner:v1.2
  before_init:
    - aws sts get-caller-identity
```

---

## Behavior Settings

| Setting | Default | Description |
|---------|---------|-------------|
| Autodeploy | `false` | Auto-apply when plan succeeds with no policy warnings |
| Autoretry | `false` | Re-run proposed runs when state changes under them (private workers only) |
| Worker pool | public | Assign private worker pool |
| Deletion protection | `false` | Prevent accidental stack deletion |
| Enable local preview | `false` | Allow `spacectl stack local-preview` uploads |

### Autodeploy Behavior Detail

- Plan succeeds + no `warn` rules from plan policies → auto-apply
- Any plan policy `warn` → run pauses at **unconfirmed**, requires manual confirm
- Any plan policy `deny` → run fails
- Approval policies still evaluated at **queued** state even with autodeploy

---

## Scheduling

### Drift Detection

Schedule periodic proposed runs to detect infrastructure drift:

- Configure at: Stack → Scheduling → Drift Detection
- One or more cron expressions (e.g., `0 */6 * * *` = every 6h)
- **Reconciliation**: optionally trigger tracked run if drift found
- Requires **private worker pool** (public workers don't support drift detection)
- `drift_detection` flag set to `true` in policy input for drift runs

### Periodic Runs

Schedule tracked runs at fixed intervals (e.g., nightly applies):
- Stack → Scheduling → Periodic Runs
- Cron expression + optional timezone

---

## Stack Hooks

Commands injected at lifecycle phases. Managed on stack Settings → Behavior tab or via contexts.

### Phases

| Phase | Before hook | After hook |
|-------|-------------|------------|
| Init | `before_init` | `after_init` |
| Plan | `before_plan` | `after_plan` |
| Apply | `before_apply` | `after_apply` |
| Destroy | `before_destroy` | `after_destroy` |
| Task (perform) | `before_perform` | `after_perform` |
| Run cleanup | — | `after_run` |

### `after_run` Notes

- Runs regardless of run outcome (success, failure, discard)
- Has access to `TF_VAR_spacelift_final_run_state`
- Executes on worker (not run if canceled before worker starts)

### Hook Ordering (Stack + Contexts)

**Before phase:**
1. Context hooks (by priority, lowest first)
2. Context auto-attached hooks (reverse alphabetical)
3. Stack hooks

**After phase:**
1. Stack hooks
2. Context auto-attached hooks (alphabetical)
3. Context hooks (reverse priority)

### Common Hook Patterns

```bash
# Before init: install tools
brew install tflint && tflint --init

# Before plan: validate
terraform validate

# After run: notify
curl -X POST $SLACK_WEBHOOK -d "{\"text\":\"Run finished: $TF_VAR_spacelift_final_run_state\"}"
```

### Runtime Commands in Hooks

```bash
# Mask a value in logs
echo "::add-mask $(aws sts get-caller-identity | jq -r .Account)"
```

### Multi-Command Best Practice

Use `&&` chains or mounted scripts — avoid `\n`. If a hook uses `;`, subsequent commands run even on failure.

```bash
# GOOD: fails fast
./scripts/validate.sh && ./scripts/lint.sh

# BAD: second command runs even if first fails
./scripts/validate.sh; ./scripts/lint.sh
```

---

## Stack Dependencies

Define ordered execution chains without trigger policies.

### Configuration

On dependent stack: Settings → Dependencies → add parent stack(s).

- Dependent stack auto-triggers after parent's tracked run succeeds
- Optional: wait for specific outputs from parent

### Ordered Creation/Deletion

Use `stack_destructor_resource` in Spacelift Terraform provider for ordered teardown (runs `before_destroy` / `after_destroy` hooks).

### Alternative: Trigger Policies

For complex conditional logic not expressible in dependencies, use trigger policies (see `references/policies.md`).
