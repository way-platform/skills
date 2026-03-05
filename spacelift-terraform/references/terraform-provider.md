# Spacelift Terraform Provider

- **Source**: `spacelift-io/spacelift`
- **Docs**: `docs/resources/` and `docs/data-sources/` in the provider repo

---

## Provider Configuration

### Inside Spacelift (recommended)

```hcl
terraform {
  required_providers {
    spacelift = {
      source = "spacelift-io/spacelift"
    }
  }
}

provider "spacelift" {}
# Zero config — uses SPACELIFT_API_TOKEN auto-injected by the run environment
# Stack must be marked administrative (or have admin role attachment)
```

### Outside Spacelift (API key)

```hcl
provider "spacelift" {
  api_key_endpoint = "https://myorg.app.spacelift.io"
  api_key_id       = var.spacelift_api_key_id
  api_key_secret   = var.spacelift_api_key_secret
}
```

Env vars (used when provider block is empty):
- `SPACELIFT_API_KEY_ENDPOINT`
- `SPACELIFT_API_KEY_ID`
- `SPACELIFT_API_KEY_SECRET`

### Multi-account (aliases)

```hcl
provider "spacelift" {
  alias            = "prod"
  api_key_endpoint = "https://prod.app.spacelift.io"
  api_key_id       = var.prod_key_id
  api_key_secret   = var.prod_key_secret
}

resource "spacelift_stack" "example" {
  provider = spacelift.prod
  # ...
}
```

---

## Resource Inventory

### Core

| Resource | Description |
|----------|-------------|
| `spacelift_stack` | Terraform/Pulumi/K8s/Ansible project: repo + branch + config + state |
| `spacelift_space` | Organizational namespace for access control and resource scoping |
| `spacelift_context` | Reusable bundle of env vars + mounted files + lifecycle hooks |
| `spacelift_policy` | OPA Rego rule set for a decision point (push, plan, approval, etc.) |
| `spacelift_worker_pool` | Private worker pool registration (generates CSR + config) |
| `spacelift_drift_detection` | Scheduled drift check for a stack |

### Attachments

| Resource | Description |
|----------|-------------|
| `spacelift_context_attachment` | Attach a context to a stack or module with priority |
| `spacelift_policy_attachment` | Attach a policy to a stack or module |
| `spacelift_aws_integration_attachment` | Attach an AWS integration to a stack or module |
| `spacelift_azure_integration_attachment` | Attach an Azure integration to a stack or module |
| `spacelift_role_attachment` | Grant a role (admin/write/read) to a stack or user |

### Stack Config

| Resource | Description |
|----------|-------------|
| `spacelift_environment_variable` | Env var on a context, stack, or module |
| `spacelift_mounted_file` | File mounted into run workspace (base64 content) |
| `spacelift_stack_dependency` | Declare that one stack's tracked runs wait on another |
| `spacelift_stack_dependency_reference` | Expose stack outputs as env vars in dependent stacks |

### Stack Lifecycle

| Resource | Description |
|----------|-------------|
| `spacelift_run` | Trigger a run; recreate on `keepers` change |
| `spacelift_stack_destructor` | Safe teardown: runs `terraform destroy` before stack deletion |
| `spacelift_stack_activator` | Control stack activation state |

### Scheduling

| Resource | Description |
|----------|-------------|
| `spacelift_scheduled_run` | Cron or one-time scheduled tracked run |
| `spacelift_scheduled_task` | Cron or one-time task (arbitrary command) |
| `spacelift_scheduled_delete_stack` | Schedule future stack deletion |

### Cloud Integrations

| Resource | Description |
|----------|-------------|
| `spacelift_aws_integration` | Account-level AWS integration via role assumption |
| `spacelift_gcp_service_account` | GCP service account attachment (account-level, legacy OAuth) |
| `spacelift_stack_gcp_service_account` | GCP service account for a specific stack (legacy OAuth) |
| `spacelift_aws_role` | Deprecated: per-stack AWS role assumption |
| `spacelift_stack_aws_role` | Deprecated: per-stack AWS role assumption |
| `spacelift_azure_integration` | Azure integration (see Azure docs) |
| `spacelift_gitlab_integration` | GitLab VCS integration |
| `spacelift_bitbucket_datacenter_integration` | Bitbucket Data Center VCS integration |

### Notifications

| Resource | Description |
|----------|-------------|
| `spacelift_webhook` | POST webhook on run state changes |
| `spacelift_named_webhook` | Named webhook (reusable across notification policies) |
| `spacelift_named_webhook_secret_header` | Secret header for named webhooks |

### Identity / Access

| Resource | Description |
|----------|-------------|
| `spacelift_api_key` | API key for automation; `secret` output stored in state |
| `spacelift_role` | Custom role definition |
| `spacelift_user` | Manage user access |
| `spacelift_idp_group_mapping` | Map IdP groups to Spacelift roles |

### Miscellaneous

| Resource | Description |
|----------|-------------|
| `spacelift_module` | Terraform module registry entry |
| `spacelift_blueprint` | Stack blueprint template |
| `spacelift_template` | Stack template |
| `spacelift_template_version` | Version of a stack template |
| `spacelift_template_deployment` | Deploy a stack template |
| `spacelift_plugin` | Custom plugin |
| `spacelift_plugin_template` | Custom plugin template |
| `spacelift_vcs_agent_pool` | VCS agent pool (for private VCS) |
| `spacelift_terraform_provider` | Register a private Terraform provider |
| `spacelift_version` | Pin Spacelift account version |
| `spacelift_default_runner_image` | Set the default runner image |
| `spacelift_security_email` | Security notification email |
| `spacelift_audit_trail_webhook` | Audit trail webhook endpoint |
| `spacelift_saved_filter` | Saved stack filter |
| `spacelift_worker_pool_recycle` | Trigger worker pool recycling |

---

## Data Source Inventory

| Data Source | Description |
|-------------|-------------|
| `spacelift_current_stack` | Current stack's own ID (use inside a Spacelift run) |
| `spacelift_current_space` | Current space context |
| `spacelift_stack` | Look up a stack by ID |
| `spacelift_stacks` | All stacks in the account |
| `spacelift_stack_outputs` | Outputs of a stack |
| `spacelift_space` | Look up a space by ID |
| `spacelift_space_by_path` | Look up a space by path (e.g. `/root/production`) |
| `spacelift_spaces` | All spaces |
| `spacelift_context` | Look up a context by ID |
| `spacelift_contexts` | All contexts |
| `spacelift_policy` | Look up a policy by ID |
| `spacelift_policies` | All policies |
| `spacelift_worker_pool` | Look up a worker pool by ID |
| `spacelift_worker_pools` | All worker pools |
| `spacelift_aws_integration` | Look up an AWS integration |
| `spacelift_aws_integrations` | All AWS integrations |
| `spacelift_aws_integration_attachment_external_id` | Generate external ID for IAM trust policy |
| `spacelift_aws_integration_attachment` | Look up an AWS integration attachment |
| `spacelift_account` | Account-level metadata |
| `spacelift_ips` | Spacelift egress IP ranges |
| `spacelift_environment_variable` | Look up an env var on context/stack/module |
| `spacelift_mounted_file` | Look up a mounted file |
| `spacelift_module` | Look up a module |
| `spacelift_modules` | All modules |
| `spacelift_vcs_agent_pool` | Look up a VCS agent pool |
| `spacelift_vcs_agent_pools` | All VCS agent pools |
| `spacelift_role` | Look up a role |
| `spacelift_role_actions` | Available role actions |
| `spacelift_tool_versions` | Available tool versions |

---

## Core Resource Schemas

### `spacelift_stack`

```hcl
resource "spacelift_stack" "this" {
  # Required
  name       = "my-stack"
  repository = "my-repo"   # repo name only, no owner
  branch     = "main"

  # Common optional
  space_id         = spacelift_space.prod.id
  worker_pool_id   = spacelift_worker_pool.private.id
  project_root     = "terraform/my-service"  # relative to repo root
  description      = "Manages production network"
  autodeploy       = true
  autoretry        = false  # requires private worker
  runner_image     = "public.ecr.aws/spacelift/runner-terraform:latest"
  terraform_version         = "1.6.0"
  terraform_workflow_tool   = "TERRAFORM_FOSS"  # or OPEN_TOFU, CUSTOM
  protect_from_deletion     = true

  labels = ["autoattach:production", "team:platform"]

  # Lifecycle hooks (all List of String)
  before_init    = ["aws configure set region us-east-1"]
  before_plan    = []
  before_apply   = []
  after_apply    = ["slack-notify applied"]
  before_destroy = []
  after_destroy  = []

  # Sparse checkout (monorepos)
  git_sparse_checkout_paths    = ["shared/", "services/my-service/"]
  additional_project_globs     = ["shared/**"]
}
```

**Key arguments:**

| Argument | Type | Default | Notes |
|----------|------|---------|-------|
| `name` | String | required | Unique in account |
| `repository` | String | required | Repo name without owner |
| `branch` | String | required | Tracked branch |
| `space_id` | String | `legacy`/`root` | Space slug |
| `worker_pool_id` | String | — | Required for drift detection |
| `autodeploy` | Boolean | `false` | Auto-apply on clean plan |
| `autoretry` | Boolean | `false` | Retry proposed runs; private worker only |
| `project_root` | String | — | Subdir for monorepo |
| `labels` | Set of String | — | Used for auto-attach policies |
| `protect_from_deletion` | Boolean | `false` | Prevent accidental deletion |

**Read-only outputs:**
- `id` — stack slug used in all attachment resources
- `aws_assume_role_policy_statement` — IAM trust policy JSON

---

### `spacelift_space`

```hcl
resource "spacelift_space" "production" {
  name            = "production"
  parent_space_id = "root"
  inherit_entities = true   # read access to parent entities
  description     = "Production infrastructure"
  labels          = ["env:prod"]
}
```

| Argument | Type | Default | Notes |
|----------|------|---------|-------|
| `name` | String | required | |
| `parent_space_id` | String | `root` | Immutable after creation |
| `inherit_entities` | Boolean | `false` | Read access to parent resources |
| `labels` | Set of String | — | |

**Note:** Requires root Admin permissions. Use only from an administrative stack in the root space.

---

### `spacelift_context`

```hcl
resource "spacelift_context" "prod-gcp" {
  name        = "Production GCP"
  description = "GCP credentials for production"
  space_id    = spacelift_space.production.id
  labels      = ["autoattach:production"]  # auto-attaches to stacks with matching label

  # Lifecycle hooks (same set as spacelift_stack)
  before_init = ["gcloud auth activate-service-account"]
}
```

| Argument | Type | Default | Notes |
|----------|------|---------|-------|
| `name` | String | required | |
| `space_id` | String | — | |
| `labels` | Set of String | — | `autoattach:<label>` for auto-attachment |

---

### `spacelift_policy`

```hcl
resource "spacelift_policy" "no-deletions" {
  name        = "Block resource deletions"
  body        = file("${path.module}/policies/no-deletions.rego")
  type        = "PLAN"
  engine_type = "REGO_V1"  # recommended
  space_id    = spacelift_space.production.id
  labels      = ["autoattach:production"]
}
```

| Argument | Type | Notes |
|----------|------|-------|
| `name` | String | required |
| `body` | String | required — Rego source |
| `type` | String | required — see types below |
| `engine_type` | String | `REGO_V0` or `REGO_V1`; default `REGO_V0` |
| `labels` | Set of String | `autoattach:<label>` for auto-attachment |
| `space_id` | String | |

**Policy types:**

| Type | Trigger |
|------|---------|
| `GIT_PUSH` | Git push or PR event |
| `PLAN` | After `terraform plan` |
| `TRIGGER` | Tracked run reaches terminal state |
| `APPROVAL` | Run enters queued or unconfirmed state |
| `ACCESS` | Stack access check |
| `LOGIN` | User login (global, not stack-attached) |
| `NOTIFICATION` | Any run state change |
| `TASK` | Before task runs |
| `INITIALIZATION` | Before run starts |

---

### `spacelift_worker_pool`

```hcl
resource "spacelift_worker_pool" "private" {
  name                      = "Private Workers"
  csr                       = filebase64("/path/to/worker.csr")
  description               = "EC2-based private workers"
  space_id                  = spacelift_space.production.id
  drift_detection_run_limit = 10
}

# Use config and private_key outputs to launch workers
# config: base64 credentials for SPACELIFT_TOKEN
# private_key: base64 private key matching the CSR
```

| Argument | Type | Notes |
|----------|------|-------|
| `name` | String | required |
| `csr` | String (Sensitive) | base64-encoded CSR; changing triggers token reset |
| `drift_detection_run_limit` | Number | Max concurrent drift detection runs |

**Sensitive outputs:** `config` (worker credentials), `private_key`

See `references/worker-pools.md` for full launch workflow.

---

### `spacelift_drift_detection`

```hcl
resource "spacelift_drift_detection" "this" {
  stack_id  = spacelift_stack.this.id
  schedule  = ["0 */6 * * *"]  # every 6 hours
  reconcile = true              # trigger tracked run when drift found
  timezone  = "UTC"
  ignore_state = false          # only check stacks in Finished state
}
```

| Argument | Type | Default | Notes |
|----------|------|---------|-------|
| `stack_id` | String | required | |
| `schedule` | List of String | required | Cron expressions |
| `reconcile` | Boolean | `false` | Auto-apply to fix drift |
| `timezone` | String | `UTC` | |
| `ignore_state` | Boolean | `false` | Check regardless of stack state |

**Note:** Stack must use a private worker pool. See `references/drift-detection.md`.

---

## Attachment Resources

### `spacelift_context_attachment`

```hcl
resource "spacelift_context_attachment" "this" {
  context_id = spacelift_context.prod-gcp.id
  stack_id   = spacelift_stack.this.id   # or module_id
  priority   = 0  # lower = higher precedence for conflict resolution
}
```

Import: `$CONTEXT_ID/$STACK_ID`

### `spacelift_policy_attachment`

```hcl
resource "spacelift_policy_attachment" "this" {
  policy_id = spacelift_policy.no-deletions.id
  stack_id  = spacelift_stack.this.id   # or module_id
  # LOGIN policies cannot be attached to stacks
}
```

Import: `$POLICY_ID/$STACK_ID`

---

## Stack Config Resources

### `spacelift_environment_variable`

```hcl
# Plain (visible) variable
resource "spacelift_environment_variable" "region" {
  context_id = spacelift_context.this.id  # or stack_id / module_id
  name       = "AWS_DEFAULT_REGION"
  value      = "us-east-1"
  write_only = false
}

# Secret (recommended for Terraform 1.11+)
resource "spacelift_environment_variable" "api-token" {
  context_id       = spacelift_context.this.id
  name             = "API_TOKEN"
  value_wo         = var.api_token   # never stored in state
  value_wo_version = 1               # increment to rotate
  write_only       = true
}
```

| Argument | Notes |
|----------|-------|
| `name` | required |
| `context_id` / `stack_id` / `module_id` | exactly one required |
| `value` | stored in state (sensitive) |
| `value_wo` + `value_wo_version` | not stored in state; requires TF 1.11+ |
| `write_only` | default `true` — hides value in UI |

Import: `context/$CONTEXT_ID/$VAR_NAME` or `stack/$STACK_ID/$VAR_NAME`

### `spacelift_mounted_file`

```hcl
resource "spacelift_mounted_file" "kubeconfig" {
  context_id    = spacelift_context.this.id  # or stack_id / module_id
  relative_path = "kubeconfig"  # accessible at /mnt/workspace/kubeconfig
  content       = filebase64("${path.module}/kubeconfig.json")
  write_only    = false
}

# Write-only (TF 1.11+)
resource "spacelift_mounted_file" "secret-file" {
  stack_id         = spacelift_stack.this.id
  relative_path    = "secrets/token"
  content_wo         = base64encode(var.secret_content)
  content_wo_version = 1
  write_only         = true
}
```

Import: `context/$CONTEXT_ID/$RELATIVE_PATH` or `stack/$STACK_ID/$RELATIVE_PATH`

---

## Cloud Integrations

### GCP — OIDC/WIF (recommended)

See `references/gcp-integration.md` for full Workload Identity Federation setup.

The preferred pattern uses native GCP integration (no service account key files):
- `spacelift_gcp_service_account` / `spacelift_stack_gcp_service_account` are the legacy OAuth token approach — avoid for new setups.

### AWS

```hcl
# 1. Create integration first (needed to get external ID)
resource "spacelift_aws_integration" "this" {
  name                           = "production"
  role_arn                       = "arn:aws:iam::123456789:role/spacelift"
  generate_credentials_in_worker = false  # true for private workers
  space_id                       = spacelift_space.production.id
}

# 2. Get external ID for trust policy
data "spacelift_aws_integration_attachment_external_id" "this" {
  integration_id = spacelift_aws_integration.this.id
  stack_id       = "my-stack-id"
  read           = true
  write          = true
}

# 3. Create IAM role using the external ID
resource "aws_iam_role" "spacelift" {
  name = "spacelift"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [jsondecode(data.spacelift_aws_integration_attachment_external_id.this.assume_role_policy_statement)]
  })
}

# 4. Attach integration to stack
resource "spacelift_aws_integration_attachment" "this" {
  integration_id = spacelift_aws_integration.this.id
  stack_id       = spacelift_stack.this.id
  read           = true
  write          = true
  depends_on     = [aws_iam_role.spacelift]
}
```

**`spacelift_aws_integration` key arguments:**

| Argument | Notes |
|----------|-------|
| `name` | required |
| `role_arn` | required |
| `generate_credentials_in_worker` | `true` for private workers (uses instance role) |
| `autoattach_enabled` | enables `autoattach:` label functionality |
| `external_id` | custom external ID (private workers only) |

**Deprecated:** `spacelift_aws_role` and `spacelift_stack_aws_role` — use `spacelift_aws_integration` + `spacelift_aws_integration_attachment` instead.

**Azure/other:** Resources exist (`spacelift_azure_integration`, `spacelift_azure_integration_attachment`) — not detailed here.

---

## Stack Lifecycle Resources

### `spacelift_run`

```hcl
resource "spacelift_run" "deploy" {
  stack_id = spacelift_stack.this.id

  # Recreate (trigger new run) when any keeper changes
  keepers = {
    config_hash = sha256(jsonencode(local.config))
    image_tag   = var.image_tag
  }

  wait {
    disabled          = false
    continue_on_state = ["finished"]
    continue_on_timeout = false
  }
}
```

### `spacelift_stack_destructor`

```hcl
resource "spacelift_stack_destructor" "this" {
  stack_id    = spacelift_stack.this.id
  deactivated = false  # set true to skip actual destroy on deletion

  # Ensure credentials are available during destroy
  depends_on = [
    spacelift_aws_integration_attachment.this,
    spacelift_environment_variable.credentials,
  ]
}
```

**Warning:** Destroying this resource runs `terraform destroy` on the stack. Set `deactivated = true` to remove the destructor without destroying infrastructure.

### `spacelift_stack_dependency`

```hcl
resource "spacelift_stack_dependency" "app-needs-infra" {
  stack_id            = spacelift_stack.app.id
  depends_on_stack_id = spacelift_stack.infra.id
  # app's tracked runs are blocked until infra finishes
}
```

---

## Scheduling Resources

### `spacelift_scheduled_run`

```hcl
# Cron-based
resource "spacelift_scheduled_run" "nightly" {
  stack_id = spacelift_stack.this.id
  name     = "nightly-apply"
  every    = ["0 2 * * *"]
  timezone = "UTC"
}

# One-time
resource "spacelift_scheduled_run" "one-off" {
  stack_id = spacelift_stack.this.id
  name     = "one-off-apply"
  at       = "1700000000"  # unix timestamp
}
```

### `spacelift_scheduled_task`

```hcl
resource "spacelift_scheduled_task" "cleanup" {
  stack_id = spacelift_stack.this.id
  name     = "weekly-cleanup"
  every    = ["0 3 * * 0"]  # Sundays 3am
  timezone = "UTC"
  command  = "terraform state list | xargs -n1 terraform state rm"
}
```

### `spacelift_scheduled_delete_stack`

```hcl
resource "spacelift_scheduled_delete_stack" "ephemeral" {
  stack_id        = spacelift_stack.ephemeral-env.id
  at              = "1700000000"   # unix timestamp
  delete_resources = true          # run destroy before deleting stack
}
```

---

## Notifications

### `spacelift_webhook`

```hcl
resource "spacelift_webhook" "alerts" {
  endpoint         = "https://hooks.example.com/spacelift"
  stack_id         = spacelift_stack.this.id  # or module_id
  enabled          = true
  secret_wo        = var.webhook_secret        # TF 1.11+
  secret_wo_version = 1
  retry_on_failure = true
}
```

Import: `stack/$STACK_ID/$WEBHOOK_ID`

---

## API Key Management

### `spacelift_api_key`

```hcl
resource "spacelift_api_key" "automation" {
  name = "CI automation"
  # secret output is sensitive and stored in state — secure your state backend
}

output "api_key_secret" {
  value     = spacelift_api_key.automation.secret
  sensitive = true
}
```

OIDC-based key (no static secret):

```hcl
resource "spacelift_api_key" "github-actions" {
  name = "GitHub Actions"
  oidc {
    issuer             = "https://token.actions.githubusercontent.com"
    client_id          = "https://github.com/my-org"
    subject_expression = "repo:my-org/my-repo:ref:refs/heads/main"
  }
}
```

---

## Data Source Patterns

```hcl
# Inside a Spacelift run — get own stack ID
data "spacelift_current_stack" "this" {}

# Look up space by path
data "spacelift_space_by_path" "prod" {
  space_path = "/root/production"
}

# All stacks (returns list)
data "spacelift_stacks" "all" {}

# All worker pools
data "spacelift_worker_pools" "all" {}

# Egress IPs (for firewall rules)
data "spacelift_ips" "this" {}
```

---

## Import Reference

| Resource | Import ID format |
|----------|-----------------|
| `spacelift_stack` | `$STACK_ID` |
| `spacelift_space` | `$SPACE_ID` |
| `spacelift_context` | `$CONTEXT_ID` |
| `spacelift_policy` | `$POLICY_ID` |
| `spacelift_worker_pool` | `$WORKER_POOL_ID` |
| `spacelift_context_attachment` | `$CONTEXT_ID/$STACK_ID` |
| `spacelift_policy_attachment` | `$POLICY_ID/$STACK_ID` |
| `spacelift_aws_integration` | `$INTEGRATION_ID` |
| `spacelift_aws_integration_attachment` | `$INTEGRATION_ID/$STACK_ID` |
| `spacelift_drift_detection` | `stack/$STACK_ID` |
| `spacelift_environment_variable` | `context/$CONTEXT_ID/$VAR_NAME` or `stack/$STACK_ID/$VAR_NAME` |
| `spacelift_mounted_file` | `context/$CONTEXT_ID/$RELATIVE_PATH` or `stack/$STACK_ID/$RELATIVE_PATH` |
| `spacelift_stack_dependency` | `$STACK_ID/$DEPENDS_ON_STACK_ID` |
| `spacelift_scheduled_run` | `$STACK_ID/$SCHEDULED_RUN_ID` |
| `spacelift_webhook` | `stack/$STACK_ID/$WEBHOOK_ID` |
