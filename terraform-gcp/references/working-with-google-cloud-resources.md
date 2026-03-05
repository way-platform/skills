# Best practices when working with Google Cloud resources

Best practices for provisioning Google Cloud resources with Terraform, are integrated into the [Cloud Foundation Toolkit](https://docs.cloud.google.com/foundation-toolkit) modules that Google maintains. This document reiterates some of these best practices.

This guide is not an introduction to Terraform. For an introduction to using Terraform with Google Cloud, see [Get started with Terraform](https://docs.cloud.google.com/docs/terraform/get-started-with-terraform).

## Bake virtual machine images

In general, we recommend that you _bake_ virtual machine images [using a tool like Packer](https://docs.cloud.google.com/compute/docs/images/image-management-best-practices#automated_baking). Terraform then only needs to launch machines using the pre-baked images.

If pre-baked images are not available, Terraform can hand off new virtual machines to a configuration management tool with a `provisioner` block. We recommend that you avoid this method and only use it as a [last resort](https://www.terraform.io/language/resources/provisioners/syntax#provisioners-are-a-last-resort). To clean up old state associated with the instance, provisioners that require teardown logic should use a `provisioner` block with `when = destroy`.

Terraform should provide VM configuration information to configuration management with [instance metadata](https://docs.cloud.google.com/compute/docs/metadata/overview).

## Manage Identity and Access Management

When provisioning IAM associations with Terraform, several different resources are available:

- `google_*_iam_policy` (for example, `google_project_iam_policy`)
- `google_*_iam_binding` (for example, `google_project_iam_binding`)
- `google_*_iam_member` (for example, `google_project_iam_member`)

`google_*_iam_policy` and `google_*_iam_binding` create _authoritative_ IAM associations, where the Terraform resources serve as the only source of truth for what permissions can be assigned to the relevant resource.

If the permissions change outside of Terraform, Terraform on its next execution overwrites all permissions to represent the policy as defined in your configuration. This might make sense for resources that are wholly managed by a particular Terraform configuration, but it means that roles that are automatically managed by Google Cloud are removed—potentially disrupting the functionality of some services.

To prevent this, we recommend using either `google_*_iam_member` resources directly or the [IAM module from Google](https://github.com/terraform-google-modules/terraform-google-iam).

