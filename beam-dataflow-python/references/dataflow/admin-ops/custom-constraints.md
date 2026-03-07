---
source_url: https://docs.cloud.google.com/dataflow/docs/custom-constraints
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Manage Dataflow resources using custom constraints \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2025-11-24 UTC."
---

Google Cloud Organization Policy gives you centralized, programmatic
control over your organization's resources. As the
[organization policy administrator](/resource-manager/docs/organization-policy/using-constraints#add-org-policy-admin), you can define an organization policy,
which is a set of restrictions called _constraints_ that apply to
Google Cloud resources and descendants of those resources in the
[Google Cloud Platform resource hierarchy](/resource-manager/docs/cloud-platform-resource-hierarchy). You can enforce organization policies at
the organization, folder, or project level.

Organization Policy provides [predefined constraints](/resource-manager/docs/organization-policy/org-policy-constraints) for various
Google Cloud services. However, if you want more granular, customizable
control over the specific fields that are restricted in your organization
policies, you can also create custom organization policies.

## Benefits

You can use a custom organization policy to allow or deny creation of Dataflow jobs with conditions based on
supported resource attributes, such as job name, type, and service options.

## Policy inheritance

By default, organization policies are inherited by the descendants of the
resources on which you enforce the policy. For example, if you enforce a policy
on a folder, Google Cloud enforces the policy on all projects in the
folder. To learn more about this behavior and how to change it, see
[Hierarchy evaluation rules](/resource-manager/docs/organization-policy/understanding-hierarchy#disallow_inheritance).

## Pricing

The Organization Policy Service, including predefined and custom organization policies, is
offered at no charge.

## Limitations

- Custom constraints for Dataflow `Job` resources can only be set up by using the Google Cloud console or Google Cloud CLI.
- Custom constraints can only be enforced on the `CREATE` method for Dataflow `Job` resources.
- Newly enforced custom constraints don't apply to existing resources.

## Before you begin

For more information about what organization policies and constraints are and
how they work, see the
[Introduction to the Organization Policy Service](/resource-manager/docs/organization-policy/org-policy-constraints).

### Required roles

To get the permissions that
you need to manage organization policies,
ask your administrator to grant you the
[Organization policy administrator](/iam/docs/roles-permissions/orgpolicy#orgpolicy.policyAdmin) (`roles/orgpolicy.policyAdmin`)
IAM role on the organization.
For more information about granting roles, see [Manage access to projects, folders, and organizations](/iam/docs/granting-changing-revoking-access).

This predefined role contains
the permissions required to manage organization policies. To see the exact permissions that are
required, expand the **Required permissions** section:

#### Required permissions

The following permissions are required to manage organization policies:

- `orgpolicy.constraints.list`
- `orgpolicy.policies.create`
- `orgpolicy.policies.delete`
- `orgpolicy.policies.list`
- `orgpolicy.policies.update`
- `orgpolicy.policy.get`
- `orgpolicy.policy.set`

You might also be able to get
these permissions
with [custom roles](/iam/docs/creating-custom-roles) or
other [predefined roles](/iam/docs/roles-overview#predefined).

## Create a custom constraint

A custom constraint is defined in a YAML file by the resources, methods,
conditions, and actions that are supported by the service on which you are
enforcing the organization policy. Conditions for your custom constraints are
defined using
[Common Expression Language (CEL)](https://github.com/google/cel-spec/blob/master/doc/intro.md). For more information about how to build
conditions in custom constraints using CEL, see the CEL section of
[Creating and managing custom constraints](/resource-manager/docs/organization-policy/creating-managing-custom-constraints#common_expression_language).

To create a YAML file for a custom constraint:

Replace the following:

- `ORGANIZATION_ID`: your organization ID, such as
  `123456789`.
- `CONSTRAINT_NAME`: the name you want for your new
  custom constraint. A custom constraint must start with `custom.`, and can
  only include uppercase letters, lowercase letters, or numbers—for
  example, custom.denyPrimeJobs. The maximum length of this field is 70
  characters, not counting the prefix—for example,
  `organizations/123456789/customConstraints/custom`.
- `RESOURCE_NAME`: the name (not the URI) of the
  Dataflow API REST resource containing the object and field
  you want to restrict. For example, `Job`.
- `CONDITION`: a [CEL condition](/resource-manager/docs/organization-policy/creating-managing-custom-constraints#common_expression_language) that is written against
  a representation of a supported service resource. This
  field has a maximum length of 1000 characters. See
  [Supported resources](#supported_resources) for more information about the
  resources available to write conditions against. For example,
  `"resource.environment.serviceOptions.exists(value, value=='enable_prime')"`.
- `ACTION`: the action to take if the `condition` is
  met. Supported values are `ALLOW` and `DENY`.
- `DISPLAY_NAME`: a human-friendly name for the
  constraint. This field has a maximum length of 200 characters.
- `DESCRIPTION`: a human-friendly description of the
  constraint to display as an error message when the policy is violated. This
  field has a maximum length of 2000 characters.

For more information about how to create a custom constraint, see
[Defining custom constraints](/resource-manager/docs/organization-policy/creating-managing-custom-constraints#defining_custom_constraints).

## Set up a custom constraint

After you have created the YAML file for a new custom constraint, you must set it up to make
it available for organization policies in your organization. To set up a custom constraint, use
the `gcloud org-policies set-custom-constraint` command:

```
gcloud org-policies set-custom-constraint CONSTRAINT_PATH
```

Replace `CONSTRAINT_PATH` with the full path to your
custom constraint file. For example, `/home/user/customconstraint.yaml`.
Once completed, your custom constraints are available as organization policies
in your list of Google Cloud Platform organization policies.
To verify that the custom constraint exists, use the
`gcloud org-policies list-custom-constraints` command:

```
gcloud org-policies list-custom-constraints --organization=ORGANIZATION_ID
```

Replace `ORGANIZATION_ID` with the ID of your organization resource.
For more information, see
[Viewing organization policies](/resource-manager/docs/organization-policy/creating-managing-policies#viewing_organization_policies).

## Enforce a custom organization policy

You can enforce a constraint by creating an organization policy that references it, and then
applying that organization policy to a Google Cloud Platform resource.

### Console

1. In the Google Cloud console, go to the **Organization policies** page.

   [Go to Organization policies](https://console.cloud.google.com/iam-admin/orgpolicies)

2. From the project picker, select the project for which you want to set the
   organization policy.
3. From the list on the **Organization policies** page, select your constraint to view
   the **Policy details** page for that constraint.
4. To configure the organization policy for this resource, click **Manage policy**.
5. On the **Edit policy** page, select **Override parent's policy**.
6. Click **Add a rule**.
7. In the **Enforcement** section, select whether enforcement of this organization policy
   is on or off.
8. Optional: To make the organization policy conditional on a tag, click
   **Add condition**. Note that if you add a conditional rule to an organization
   policy, you must add at least one unconditional rule or the policy cannot be saved. For more
   information, see
   [Setting an organization policy with tags](/resource-manager/docs/organization-policy/tags-organization-policy).
9. Click **Test changes** to simulate the effect of the organization policy. Policy
   simulation isn't available for legacy managed constraints. For more information, see
   [Test organization policy changes with Policy Simulator](/policy-intelligence/docs/test-organization-policies).
10. To finish and apply the organization policy, click **Set policy**. The policy
    requires up to 15 minutes to take effect.

### gcloud

To create an organization policy with boolean rules, create a policy YAML file that
references the constraint:

Replace the following:

- `PROJECT_ID`: the project on which you want to enforce your
  constraint.
- `CONSTRAINT_NAME`: the name you defined for your custom constraint. For
  example, `custom.denyPrimeJobs`.

To enforce the organization policy containing the constraint, run the following command:

```
    gcloud org-policies set-policy POLICY_PATH
```

Replace `POLICY_PATH` with the full path to your organization policy
YAML file. The policy requires up to 15 minutes to take effect.

## Example: Create a constraint to deny creation of a job with prime enabled

### gcloud

1. Create a `denyPrimeJobs.yaml` constraint file with the following
   information. Replace `ORGANIZATION_ID` with your
   organization ID.
2. Set the custom constraint.

   ```
   gcloud org-policies set-custom-constraint denyPrimeJobs.yaml
   ```

3. Create an `enforce-policy-denyPrimeJobs.yaml` policy file with the following
   information. In this example, the constraint is enforced at the project
   level. You might also set this constraint at the organization or folder level.
   Replace `PROJECT_ID` with your project ID.
4. [Enforce the policy](/resource-manager/docs/organization-policy/creating-managing-custom-constraints#enforcing_custom_constraints) by running following command.

   ```
   gcloud org-policies set-policy enforce-policy-denyPrimeJobs.yaml
   ```

5. To test the constraint, try to create a Dataflow job with the
   `enable_prime` option. Follow the
   [Create a Dataflow pipeline using Java](/dataflow/docs/quickstarts/create-pipeline-java)
   quickstart to create a WordCount job.

   ```
   mvn -Pdataflow-runner compile \
   exec:java \
   -Dexec.mainClass=org.apache.beam.examples.WordCount \
   -Dexec.args="--project=PROJECT_ID \
   --gcpTempLocation=gs://BUCKET_NAME/temp/ \
   --output=gs://BUCKET_NAME/output \
   --runner=DataflowRunner \
   --region=us-central1 \
   --dataflowServiceOptions=enable_prime" \
   -Pdataflow-runner
   ```

   The output is similar to the following example:

   The audit log should show violation details like following:

## Expression fields for conditions

The following table contains the expression fields that you can use to create
conditions. Conditions are written in [Common Expression Language (CEL)](/resource-manager/docs/organization-policy/creating-managing-custom-constraints#common_expression_language).
The value of the expression fields is case-sensitive.

For descriptions of the following expression fields and which values you can specify, see the [Dataflow `Job` JSON representation](/dataflow/docs/reference/rest/v1b3/projects.jobs#Job).

| **Expression field**                           | **Value type**   |
| ---------------------------------------------- | ---------------- |
| `name`                                         | `string`         |
| `type`                                         | `string`         |
| `transformNameMapping`                         | `map`            |
| `location`                                     | `string`         |
| `environment`                                  | `message`        |
| `environment.serviceOptions`                   | `list of string` |
| `environment.serviceKmsKeyName`                | `string`         |
| `environment.serviceAccountEmail`              | `string`         |
| `environment.workerRegion`                     | `string`         |
| `environment.workerZone`                       | `string`         |
| `environment.streamingMode`                    | `string`         |
| `environment.debugOptions`                     | `message`        |
| `environment.debugOptions.enableHotKeyLogging` | `bool`           |

## Example use cases

Some example use cases are listed in the following table.

| **Use Case**                                                                | **Action** | **Custom Constraint**                                                                                         |
| --------------------------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------- |
| Disallow use of prime job                                                   | DENY       | `resource.environment.serviceOptions.exists(value, value=='enable_prime')`                                    |
| Prevents VMs from accepting SSH keys that are stored in project metadata.   | DENY       | `!resource.environment.serviceOptions.exists(value, value=='block_project_ssh_keys')`                         |
| Disallow jobs without setting the maximum number of seconds the job can run | DENY       | `!resource.environment.serviceOptions.exists(value, value.contains('max_workflow_runtime_walltime_seconds=')` |

## What's next

- See [Introduction to the Organization Policy Service](/resource-manager/docs/organization-policy/overview) to learn more about organization policies.
- Learn more about how to [create and manage organization policies](/resource-manager/docs/organization-policy/using-constraints).
- See the full list of predefined [Organization policy constraints](/resource-manager/docs/organization-policy/org-policy-constraints).
