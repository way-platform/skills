# Contexts and Configuration

## Table of Contents
- [What is a Context](#what-is-a-context)
- [Creating and Managing Contexts](#creating-and-managing-contexts)
- [Attaching Contexts](#attaching-contexts)
- [Auto-Attach via Labels](#auto-attach-via-labels)
- [Priority and Conflict Resolution](#priority-and-conflict-resolution)
- [Secret Masking](#secret-masking)
- [Runtime Config: `.spacelift/config.yml`](#runtime-config-spaceliftconfigyml)
- [Environment Variable Precedence](#environment-variable-precedence)

---

## What is a Context

A context is a reusable bundle of:
- **Environment variables** (plain or secret)
- **Mounted files** (content injected into runner filesystem at run time)
- **Hooks** (commands injected before/after lifecycle phases)

Contexts are created independently and attached to multiple stacks. Changes to a context affect all attached stacks immediately.

Use contexts to share:
- Cloud provider credentials (AWS role ARNs, GCP service account keys)
- Shared Terraform backend config files
- Common validation scripts (as mounted files + hooks)
- Organization-wide environment settings

---

## Creating and Managing Contexts

### UI

1. _Share code & config_ → _Contexts_ → **Create context**
2. Fill: Name, Space, Description, Labels
3. Add variables, mounted files, hooks
4. Attach to stacks

### Terraform Provider

```hcl
resource "spacelift_context" "aws_prod" {
  name        = "aws-production"
  description = "Production AWS credentials and config"
  space_id    = "root"
  labels      = ["autoattach:production"]
}

resource "spacelift_environment_variable" "aws_region" {
  context_id = spacelift_context.aws_prod.id
  name       = "AWS_DEFAULT_REGION"
  value      = "us-east-1"
}

resource "spacelift_environment_variable" "aws_role" {
  context_id = spacelift_context.aws_prod.id
  name       = "AWS_ROLE_ARN"
  value      = "arn:aws:iam::123456789:role/spacelift-prod"
  write_only = true  # secret
}

resource "spacelift_mounted_file" "backend_config" {
  context_id    = spacelift_context.aws_prod.id
  relative_path = "backend.hcl"
  content       = base64encode(file("backend.hcl"))
}

resource "spacelift_context_attachment" "attach" {
  context_id = spacelift_context.aws_prod.id
  stack_id   = spacelift_stack.my_stack.id
  priority   = 0
}
```

---

## Attaching Contexts

### Manual Attachment

Stack → Settings → Contexts → select context → **Attach**

Set priority (lower number = higher priority, evaluated first for conflicts).

### Detaching

Stack → Settings → Contexts → three dots → Detach

---

## Auto-Attach via Labels

Add label `autoattach:<label>` to a context. Any stack with that label automatically gets the context attached.

```
Context label: autoattach:production
Stack labels:  production, networking

→ Context is auto-attached to this stack
```

Auto-attached contexts are ordered alphabetically (or reverse) within hook execution. See hook ordering in `references/stack-configuration.md`.

**Common pattern:** org-wide policies context auto-attached to all stacks:
```
Context label: autoattach:all-stacks
Stack labels: all-stacks  (add to every stack)
```

---

## Priority and Conflict Resolution

When multiple contexts define the same variable/file, the one with **lowest priority number wins**.

| Priority | Source |
|----------|--------|
| 0 (highest) | Context with priority 0 |
| 1 | Context with priority 1 |
| ... | ... |
| Stack | Stack's own environment |

Stack-level variables always override context variables of the same name, regardless of context priority.

**Set priority on attachment:**
```hcl
resource "spacelift_context_attachment" "attach" {
  context_id = spacelift_context.base.id
  stack_id   = spacelift_stack.my_stack.id
  priority   = 10  # lower priority than other contexts
}
```

---

## Secret Masking

Mark variables or mounted files as **secret** (write-only):
- Value is never returned via API or shown in UI after creation
- Value is masked (`*****`) in run logs
- Still passed to the runner process as environment variable

```hcl
resource "spacelift_environment_variable" "db_password" {
  context_id = spacelift_context.app.id
  name       = "DB_PASSWORD"
  value      = var.db_password
  write_only = true
}
```

Additional masking in logs via runtime command:
```bash
# In a hook, mask dynamically computed values
echo "::add-mask $(aws sts get-caller-identity | jq -r .Account)"
```

---

## Runtime Config: `.spacelift/config.yml`

Per-repository runtime configuration file. Overrides stack settings on a per-run basis.

Location: `.spacelift/config.yml` in the repository root.

```yaml
version: "1"

stack_defaults:
  project_root: infra
  runner_image: my-registry/custom-runner:v1.2.0
  before_init:
    - aws sts get-caller-identity

stacks:
  networking:
    project_root: infra/networking
    before_plan:
      - tflint --init && tflint
  platform:
    project_root: infra/platform
```

### Config Precedence

Stack settings → overridden by → `.spacelift/config.yml` stack entry → falls back to → `stack_defaults`

### Common Uses

- Pin runner image per stack in monorepo
- Set different `project_root` for each stack in monorepo
- Inject validation commands before plan

---

## Environment Variable Precedence

From highest to lowest priority:

1. **Stack environment variables** (set directly on stack)
2. **Context variables** (lowest context priority number wins)
3. **Computed variables** (e.g., Spacelift-injected vars like `SPACELIFT_STACK_ID`)

### Spacelift-Injected Variables

Always available in runs:

| Variable | Value |
|----------|-------|
| `SPACELIFT_STACK_ID` | Stack slug |
| `SPACELIFT_RUN_ID` | Current run ID |
| `SPACELIFT_RUN_TYPE` | `TRACKED`, `PROPOSED`, `TASK` |
| `SPACELIFT_COMMIT_SHA` | Current commit hash |
| `SPACELIFT_COMMIT_BRANCH` | Branch of current commit |
| `TF_VAR_spacelift_stack_id` | Same as above, as TF variable |
| `TF_VAR_spacelift_run_id` | Run ID as TF variable |
| `TF_VAR_spacelift_final_run_state` | Available in `after_run` hook |
