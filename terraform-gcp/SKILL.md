---
name: terraform-gcp
description: >-
  Write, review, and refactor Terraform HCL for Google Cloud Platform. Use
  when creating or editing any .tf files targeting GCP resources, structuring
  root modules or reusable modules for GCP, managing IAM with the Google
  provider, writing terraform tests for GCP infrastructure, importing or
  exporting GCP resources, or organizing Terraform project directories for
  GCP deployments.
---

# Terraform + GCP

## File Organization

Per `references/terraform-style-guide.md` (HashiCorp):

| File | Purpose |
|------|---------|
| `terraform.tf` | Terraform and provider version requirements |
| `providers.tf` | Provider configurations |
| `main.tf` | Primary resources and data sources |
| `variables.tf` | Input variable declarations (alphabetical) |
| `outputs.tf` | Output value declarations (alphabetical) |
| `locals.tf` | Local value declarations |

For larger modules, split `main.tf` into purpose-grouped files (`references/general-style-and-structure.md`, Google):

```hcl
# dns.tf — google_dns_managed_zone + google_dns_record_set together
# network.tf — VPC, subnets, firewall rules together
```

---

## Formatting

- 2 spaces per nesting level, no tabs — always run `terraform fmt -recursive`
- Align `=` for consecutive arguments in the same block
- Block order within a resource:
  1. Meta-arguments (`count`, `for_each`, `provider`, `depends_on`)
  2. Arguments
  3. Nested blocks
  4. `lifecycle` last

---

## Naming Conventions

- `lowercase_underscores` for all resource/variable/output names
- Descriptive nouns — **no resource type in the name**
- Singular, not plural
- Use `main` when there is only one of a type

```hcl
# Bad
resource "google_compute_global_address" "main_global_address" {}
resource "google_storage_bucket" "buckets" {}

# Good
resource "google_compute_global_address" "main" {}
resource "google_storage_bucket" "artifacts" {}
```

---

## Variables

Every variable needs `type` + `description`. Add `validation` for constrained inputs.
Mark `sensitive = true` for secrets. Don't provide defaults for environment-specific
values like `project_id` — force the caller to provide them.

**GCP-specific naming:**
- Numeric values: include units — `ram_size_gb`, `disk_size_gib`
- Storage: binary prefixes (`kibi`, `mebi`, `gibi`); all other measurements: decimal
- Booleans: positive names — `enable_external_access`, not `disable_internal`

```hcl
variable "ram_size_gb" {
  description = "RAM per instance in gibibytes"
  type        = number
}

variable "environment" {
  description = "Deployment environment"
  type        = string

  validation {
    condition     = contains(["dev", "qa", "prod"], var.environment)
    error_message = "Must be dev, qa, or prod."
  }
}
```

---

## Outputs

Every output needs `description`. Mark `sensitive = true` where appropriate.

**Never pass an input variable directly as an output** — always reference a resource
attribute to preserve the dependency graph:

```hcl
# Bad — breaks implicit dependencies
output "bucket_name" {
  value = var.bucket_name
}

# Good — reference the resource attribute
output "bucket_name" {
  description = "Name of the storage bucket"
  value       = google_storage_bucket.main.name
}
```

---

## `for_each` vs `count`

- `for_each` — multiple named resources (stable identity, survives reordering)
- `count` — conditional creation only
- Use a separate `enable_x` boolean for conditional logic; don't drive `count`
  directly from resource attributes that may be unknown at plan time

```hcl
# Multiple resources — use for_each
resource "google_storage_bucket" "regional" {
  for_each = toset(var.regions)
  name     = "data-${each.key}"
  location = each.key
}

# Conditional — use count
resource "google_monitoring_alert_policy" "latency" {
  count        = var.enable_alerts ? 1 : 0
  display_name = "High Latency Alert"
}
```

---

## Dependency Management (CRITICAL)

**Prefer implicit over explicit.** Reference output attributes — not input args — to
create real ordering. Input args are known at plan time and create no dependency;
output attrs are only known after creation.

```hcl
# Bad — .name is an input arg, Terraform sees no dependency
bucket = google_storage_bucket.main.name

# Good — .id is an output attr, creates real implicit dependency
bucket = google_storage_bucket.main.id
```

Module dependency — implicit via output reference:

```hcl
# Bad — depends_on is a blunt instrument, slows planning
module "bigquery" {
  project_id = var.project_id
  depends_on = [module.project_services]
}

# Good — implicit dependency, Terraform tracks exactly what changed
module "bigquery" {
  project_id = module.project_services.project_id
}
```

Use `depends_on` only as a last resort. Always add a comment explaining why.

Cross-config dependencies: use `terraform_remote_state` (GCS backend). Don't use
data sources to reference resources managed by another Terraform config.

---

## IAM — Authoritative vs Additive (CRITICAL)

| Resource pattern | Behavior | Use? |
|-----------------|----------|------|
| `google_*_iam_policy` | **Authoritative** — overwrites ALL roles, removes Google-managed accounts | AVOID |
| `google_*_iam_binding` | **Authoritative** — overwrites that specific role's bindings | Avoid unless owning the entire role |
| `google_*_iam_member` | **Additive** — adds one member, leaves all others untouched | PREFERRED |

Authoritative resources silently remove Google's auto-managed service account roles,
breaking Cloud services. Default to `google_*_iam_member`.

```hcl
# Bad — removes all other IAM, including Google-managed bindings
resource "google_project_iam_policy" "main" {
  project     = var.project_id
  policy_data = data.google_iam_policy.admin.policy_data
}

# Good — additive, safe
resource "google_project_iam_member" "invoker" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.worker.email}"
}
```

---

## Stateful Resource Protection

Add `lifecycle { prevent_destroy = true }` to databases, buckets, and other
stateful resources:

```hcl
resource "google_sql_database_instance" "main" {
  name             = "primary"
  database_version = "POSTGRES_15"

  lifecycle {
    prevent_destroy = true
  }
}
```

---

## Compute / VM

- Bake images with Packer — do NOT use provisioners for configuration
- Pass runtime config via instance metadata, not provisioner scripts

---

## Version Pinning

**Root modules** — pin to minor, allow patch updates:

```hcl
terraform {
  required_version = ">= 1.7"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0.0"
    }
  }
}
```

**Reusable modules** — permissive `>=`, let callers decide:

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0.0"
    }
  }
}
```

---

## Root Module Structure

```
service/
├── OWNERS
├── modules/
│   └── <service-name>/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── README.md
└── environments/
    ├── dev/
    │   ├── backend.tf        # GCS backend
    │   ├── main.tf           # Instantiates service module
    │   └── terraform.tfvars
    ├── qa/
    └── prod/
```

- Max ~100 resources per state (ideally a few dozen) — per `references/root-modules.md` (Google)
- One directory per application/service; nest all code under it
- **Default workspace only** — no multiple CLI workspaces
- Variables in `terraform.tfvars`; check in `.terraform.lock.hcl`
- Never commit: `.terraform/`, `*.tfstate`, `*.tfstate.backup`, `*.tfplan`

---

## Reusable Module Rules

- **No `provider` or `backend` config** — root modules own these
- Expose `labels = {}` variable for every module
- Every resource defined in the module must have at least one output
- Enable APIs via `google_project_service`; expose `enable_apis = true`
  variable; always set `disable_services_on_destroy = false`
- Inline submodules in `modules/<name>/`
- Use `moved` blocks when refactoring to prevent destroy/recreate
- Release with SemVer; callers reference with `~> major.0`

---

## Testing

Two categories of `.tftest.hcl` tests:

| Type | Naming | Mode | Creates resources? |
|------|--------|------|-------------------|
| Unit | `*_unit_test.tftest.hcl` | `plan` | No — fast, safe |
| Integration | `*_integration_test.tftest.hcl` | `apply` | Yes — real infra |

```hcl
run "bucket_name_follows_convention" {
  command = plan

  assert {
    condition     = google_storage_bucket.main.name == "myproject-artifacts"
    error_message = "Bucket name does not match expected pattern."
  }
}
```

Key practices:
- Randomize resource names/project IDs to avoid collisions
- Use a dedicated test project isolated from dev/prod
- Always destroy after tests: `terraform destroy` or `project_cleanup` module
- Run independent tests in parallel: `test { parallel = true }`
- Order: `terraform validate` → unit tests → integration tests → e2e

See `references/terraform-test.md` for full `.tftest.hcl` syntax, mock
providers, `expect_failures`, and parallel execution rules.

---

## Import / Export

**Export existing GCP resources:**

```bash
gcloud beta resource-config bulk-export \
  --project=MY_PROJECT \
  --resource-format=terraform \
  --path=./exported/
```

**Import one resource:**

```bash
terraform import google_storage_bucket.main my-project/my-bucket
```

**Bulk import with generated config (Terraform 1.5+):**

```hcl
import {
  id = "projects/MY_PROJECT/global/networks/my-network"
  to = google_compute_network.main
}
```

```bash
terraform plan -generate-config-out=generated.tf
```

See `references/import-google-cloud-resources.md` and
`references/export-google-cloud-resources.md` for full workflows.

---

## Reference Files

| File | Read when |
|------|-----------|
| `references/terraform-style-guide.md` | Full HashiCorp style guide: formatting, block order, naming, security patterns |
| `references/terraform-test.md` | Complete `.tftest.hcl` syntax: run/assert/mock blocks, parallel execution, expect_failures |
| `references/general-style-and-structure.md` | Module structure, data source placement, static files, helper scripts, expression complexity |
| `references/root-modules.md` | Root module patterns, remote state, environment dirs, workspace rules |
| `references/reusable-modules.md` | API activation, OWNERS file, SemVer releases, submodule patterns, `moved` blocks |
| `references/dependency-management.md` | Implicit vs explicit deps with full examples, cross-config remote state |
| `references/working-with-google-cloud-resources.md` | IAM authoritative vs additive detail, VM baking |
| `references/testing.md` | GCP testing strategies, parallel execution, test environment isolation, cleanup |
| `references/import-google-cloud-resources.md` | Step-by-step import workflows, `import` block + `generate-config-out` |
| `references/export-google-cloud-resources.md` | Bulk export with `gcloud beta resource-config`, supported resource types |
| `references/blueprints.md` | Cloud Foundation Toolkit blueprint patterns |
