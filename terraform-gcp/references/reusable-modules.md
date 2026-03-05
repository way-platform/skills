# Best practices for reusable modules

This document provides guidelines and recommendations to consider when using reusable Terraform modules.

This guide is not an introduction to Terraform. For an introduction to using Terraform with Google Cloud, see [Get started with Terraform](https://docs.cloud.google.com/docs/terraform/get-started-with-terraform).

## Activate required APIs in modules

Terraform modules can activate any required services by using the `google_project_service` resource or the [`project_services`](https://github.com/terraform-google-modules/terraform-google-project-factory/tree/master/modules/project_services) module. Including API activation makes demonstrations easier.

- If API activation is included in a module, then the API activation _must_ be disableable by exposing an `enable_apis` variable that defaults to `true`.
- If API activation is included in a module, then the API activation _must_ set `disable_services_on_destroy` to `false`, because this attribute can cause issues when working with multiple instances of the module.
    
    For example:
    
    ```hcl
    module "project-services" {
      source  = "terraform-google-modules/project-factory/google//modules/project_services"
      version = "~> 12.0"
    
      project_id  = var.project_id
      enable_apis = var.enable_apis
    
      activate_apis = [
        "compute.googleapis.com",
        "pubsub.googleapis.com",
      ]
      disable_services_on_destroy = false
    }
    ```

## Include an owners file

For all shared modules, include an [`OWNERS`](https://github.com/bkeepers/OWNERS) file (or [`CODEOWNERS`](https://blog.github.com/2017-07-06-introducing-code-owners/) on GitHub), documenting who is responsible for the module. Before any pull request is merged, an owner should approve it.

### Release tagged versions

Sometimes modules require breaking changes and you need to communicate the effects to users so that they can pin their configurations to a specific version.

Make sure that shared modules follow [SemVer v2.0.0](https://semver.org/spec/v2.0.0.html) when new versions are tagged or released.

When referencing a module, use a [version constraint](https://www.terraform.io/language/expressions/version-constraints) to pin to the _major_ version. For example:

```hcl
module "gke" {
  source  = "terraform-google-modules/kubernetes-engine/google"
  version = "~> 20.0"
}
```

## Don't configure providers or backends

Shared modules [must not configure providers or backends](https://developer.hashicorp.com/terraform/language/providers/configuration#provider-configuration-1). Instead, configure providers and backends in root modules.

For shared modules, define the minimum required provider versions in a [`required_providers`](https://www.terraform.io/language/modules/develop/providers#provider-version-constraints-in-modules) block, as follows:

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

Unless proven otherwise, assume that new provider versions will work.

## Expose labels as a variable

Allow flexibility in the labeling of resources through the module's interface. Consider providing a `labels` variable with a default value of an empty map, as follows:

```hcl
variable "labels" {
  description = "A map of labels to apply to contained resources."
  default     = {}
  type        = "map"
}
```

## Expose outputs for all resources

Variables and outputs let you infer dependencies between modules and resources. Without any outputs, users cannot properly order your module in relation to their Terraform configurations.

For every resource defined in a shared module, include at least one output that references the resource.

## Use inline submodules for complex logic

- Inline modules let you organize complex Terraform modules into smaller units and de-duplicate common resources.
- Place inline modules in `modules/$modulename`.
- Treat inline modules as private, not to be used by outside modules, unless the shared module's documentation specifically states otherwise.
- Terraform doesn't track refactored resources. If you start with several resources in the top-level module and then push them into submodules, Terraform tries to recreate all refactored resources. To mitigate this behavior, use [`moved`](https://www.terraform.io/language/modules/develop/refactoring#moved-block-syntax) blocks when refactoring.
- Outputs defined by internal modules aren't automatically exposed. To share outputs from internal modules, re-export them.