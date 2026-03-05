---
name: spacelift-terraform
description: >-
  Spacelift infrastructure management platform for GitHub + Terraform GitOps
  workflows. Use when working with Spacelift stacks, runs, policies, contexts,
  worker pools, drift detection, or the spacectl CLI. Covers PR previews,
  merge deploys, push/plan/trigger/approval policies, private worker pools,
  and agent automation via spacectl.
---

# Spacelift

Spacelift orchestrates Terraform via GitOps: GitHub pushes trigger runs,
policies govern behavior, contexts inject config, workers execute runs.

- **API**: `https://<account>.app.spacelift.io/graphql`
- **Terraform provider**: `spacelift-io/spacelift`
- **spacectl**: `brew install spacelift-io/spacelift/spacectl`

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Stack** | Terraform project unit: repo + branch + settings + state |
| **Run** | Execution of `terraform plan` (proposed) or `plan+apply` (tracked) |
| **Policy** | OPA Rego rule set governing stack behavior (9 types) |
| **Context** | Reusable bundle of env vars + mounted files + hooks |
| **Worker Pool** | Set of runners executing runs (public Spacelift-hosted or private) |
| **Space** | Organizational boundary for access control and resource scoping |

---

## GitOps Workflow

```
feature branch push
  → push policy → propose
  → proposed run: terraform plan
  → commit status reported to PR

PR merged to tracked branch (e.g., main)
  → push policy → track
  → tracked run: terraform plan
  → if autodeploy: auto-apply
  → else: unconfirmed state → human confirms → apply
```

### Run States

| State | Meaning |
|-------|---------|
| QUEUED | Waiting for worker; approval policies evaluated here |
| INITIALIZING | Worker starting, downloading source |
| PLANNING | `terraform plan` running |
| UNCONFIRMED | Plan done, awaiting human confirm (or autodeploy blocked) |
| CONFIRMED | Human confirmed, apply will start |
| APPLYING | `terraform apply` running |
| FINISHED | Completed successfully |
| FAILED | Run failed at some phase |
| DISCARDED | Manually abandoned |

---

## spacectl Quick Reference

### Auth (CI/Agent — non-interactive)

```bash
export SPACELIFT_API_KEY_ENDPOINT=https://myorg.app.spacelift.io
export SPACELIFT_API_KEY_ID=$SECRET_KEY_ID
export SPACELIFT_API_KEY_SECRET=$SECRET_KEY_SECRET
```

### GitHub Actions

```yaml
- uses: spacelift-io/setup-spacectl@main
- run: spacectl stack deploy --id my-stack --auto-confirm --tail
  env:
    SPACELIFT_API_KEY_ENDPOINT: https://myorg.app.spacelift.io
    SPACELIFT_API_KEY_ID: ${{ secrets.SPACELIFT_API_KEY_ID }}
    SPACELIFT_API_KEY_SECRET: ${{ secrets.SPACELIFT_API_KEY_SECRET }}
```

### Key Commands

```bash
spacectl stack list
spacectl stack deploy --id <stack> --auto-confirm --tail
spacectl stack task --id <stack> --tail 'terraform output -json'
spacectl run list --stack <stack>
spacectl run logs --stack <stack> --run <run-id>
spacectl run confirm --stack <stack> --run <run-id>
spacectl workerpool list
spacectl profile export-token          # get bearer token for API calls
```

---

## Stack Settings Quick Reference

| Field | Key Values |
|-------|-----------|
| Branch | Tracked branch — pushes here trigger tracked runs |
| Project root | Subdirectory for Terraform root (monorepo) |
| Project globs | Sparse checkout paths (requires git checkout mode) |
| Autodeploy | `true` = auto-apply on clean plan |
| Autoretry | `true` = retry proposed runs when state changes (private worker only) |
| Worker pool | Assign private pool; required for drift detection |
| Runner image | Custom Docker image (default: `public.ecr.aws/spacelift/runner-terraform:latest`) |
| Labels | Used by policies for auto-attach and filtering |
| Deletion protection | Prevent accidental stack deletion |

---

## Policy Types Quick Reference

| Type | Fires when | Key outputs |
|------|-----------|-------------|
| **Push** | Git push or PR event | `track`, `propose`, `ignore`, `cancel` |
| **Plan** | After `terraform plan` | `deny` (fail), `warn` (require review) |
| **Trigger** | Tracked run reaches terminal state | `trigger` (stack IDs to cascade) |
| **Approval** | Run enters queued/unconfirmed | `approve`, `reject` |
| **Login** | User login attempt | `allow`, `deny`, `admin` |
| **Stack Access** | Stack access check | `read`, `write`, `admin`, `deny` |
| **Notification** | Any run state change | notification targets |
| **Task** | Before task runs | `allow`, `deny` |
| **Run Init** | Before run starts (deprecated) | `allow`, `deny` |

All policies use **Rego v1** (`package spacelift`). Auto-attach via label `autoattach:<label>`.

### Most Common Patterns

```opa
# Push: standard GitOps
track if input.push.branch == input.stack.branch
propose if not is_null(input.pull_request)
ignore if { not track; not propose }

# Plan: block deletions
deny contains sprintf("Deletion not allowed: %s", [c.entity.address]) if {
  some c in input.spacelift.run.changes; c.action == "deleted"
}

# Plan: manual review for drift
warn contains "Drift reconciliation requires manual approval" if {
  input.spacelift.run.drift_detection
}

# Approval: require 1 reviewer
approve if count(input.reviews.current.approvals) >= 1
```

---

## Reference Files

| File | Read when |
|------|-----------|
| `references/github-terraform-workflow.md` | Setting up GitHub App, branch tracking, PR status checks, push policy patterns, monorepo sparse checkout |
| `references/stack-configuration.md` | Stack creation fields, VCS settings, Terraform settings, hooks, scheduling, stack dependencies |
| `references/policies.md` | All 9 policy types with full input schemas, Rego v1 examples, workbench testing |
| `references/spacectl.md` | CLI installation, auth methods, stack/run/worker commands, CI agent patterns, GraphQL API |
| `references/contexts-and-config.md` | Context creation, auto-attach labels, priority/conflict resolution, `.spacelift/config.yml`, env var precedence |
| `references/worker-pools.md` | Private worker setup (CSR → pool → launch), config vars, network requirements, sizing |
| `references/drift-detection.md` | Scheduling, reconciliation, plan/trigger policy integration, drift run limits |
| `references/gcp-integration.md` | Setting up GCP OIDC (WIF), native GCP integration, credential config JSON, Terraform provider auth, hierarchical space access, direct resource access |
| `references/terraform-provider.md` | Terraform provider config, resource+data source inventory, HCL schemas for all core resources, AWS integration setup, import IDs |
