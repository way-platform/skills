---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/troubleshoot-permissions
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Troubleshoot Dataflow permissions \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

This page shows you how to investigate and resolve issues with
[Dataflow permissions](/dataflow/docs/concepts/security-and-permissions).

To successfully run Dataflow jobs, your user account and the
Dataflow service accounts must have the necessary access to resources.
For a list of required roles and steps for granting these roles, see
[Security and permissions for pipelines on Google Cloud](/dataflow/docs/concepts/security-and-permissions#permissions)
on the Dataflow security and permissions page.

In addition, when your Apache Beam pipelines access Google Cloud resources,
your Dataflow project worker service account needs access to the resources.
For a list of roles that your worker service account might need, see
[Example role assignment](/dataflow/docs/concepts/access-control#example).

When one or more roles required for running a job is missing, an error might appear in the job logs or in the worker logs.
For instructions explaining how to find errors when a job fails, see
[Find information about pipeline failures](/dataflow/docs/guides/troubleshooting-your-pipeline#Workflow).

To resolve permissions issues, you need to understand which
permission is missing and which account needs to have that permission.
To understand which permission is missing, look at the permission
listed in the error message and find the role that contains that permission.
Often, but not always, you need to assign the relevant
role to the [Dataflow worker service account](/dataflow/docs/concepts/security-and-permissions#worker-service-account).

To add permissions, your user account needs to be allowed to manage access. For more
information, see [Manage access to service accounts](/iam/docs/manage-access-service-accounts)
and [Manage access to other resources](/iam/docs/manage-access-other-resources).

## User does not have write access to project

When you try to run a Dataflow job, the job fails and you see an error
similar to the following:

```
PERMISSION_DENIED: (Could not create workflow; user does not have write access to project: $PROJECT_ID Causes: (...): Permission 'dataflow.jobs.create' denied on project: '$PROJECT_ID'
```

This error occurs when your user account doesn't have the `roles/dataflow.developer`
role.

To resolve this issue, grant your user account the `roles/dataflow.developer`
role. In addition, make sure that your user account has the `roles/iam.serviceAccountUser` role.
For more information, see [Grant a single role](/iam/docs/manage-access-service-accounts#grant-single-role)
in the Identity and Access Management documentation.

## User does not have sufficient permissions on project

When you try to cancel a Dataflow job, you see an error
similar to the following:

```
Could not cancel workflow; user does not have sufficient permissions on project:PROJECT_ID, or the job does not exist in the project. Causes: (...): Permission 'dataflow.jobs.cancel' denied on project: 'PROJECT_ID' Please ensure you have permission to access the job
```

Similar errors might occur when trying to drain or update a job.

This error occurs for one of the following reasons:

- Your user account doesn't have the `roles/dataflow.developer` role.
  To resolve this issue, grant your user account the `roles/dataflow.developer`
  role. In addition, make sure that your user account has the `roles/iam.serviceAccountUser` role.
  For more information, see [Grant a single role](/iam/docs/manage-access-service-accounts#grant-single-role)
  in the Identity and Access Management documentation.
- The job ID is incorrect. It might contain a typo, or you might
  be using the job name to
  [cancel the job](https://cloud.google.com/sdk/gcloud/reference/dataflow/jobs/cancel)
  instead of the job ID.

## Permissions verification for worker service account failed

When you try to run a Dataflow job, you see an error
similar to the following:

```
Workflow failed. Causes: Permissions verification for controller service account failed. All permissions in IAM role roles/dataflow.worker should be granted to controller service account PROJECT_NUMBER-compute@developer.gserviceaccount.com.
```

This error occurs when the worker service account doesn't have the `roles/dataflow.worker`
role.

To resolve this issue, grant the worker service account the `roles/dataflow.worker`
role.
For more information, see [Grant a single role](/iam/docs/manage-access-service-accounts#grant-single-role)
in the Identity and Access Management documentation.

## Pipeline validation failed

Before a new Dataflow job launches,
Dataflow performs validation checks on the pipeline. When the
validation checks find problems with the pipeline, to save time and compute resources,
Dataflow fails the job submission early. In the
[job logs](/dataflow/docs/guides/logging#MonitoringLogs), Dataflow
includes log messages that contain the validation findings and instructions for
resolving the issues.

When the pipeline validation check finds permission issues, you might see the
following error in the job logs:

```
[The preflight pipeline validation failed for job JOB_ID.] Missing permissions
PERMISSION when accessing RESOURCE_PATH as Dataflow worker service account WORKER_SERVICE_ACCOUNT.
```

If permissions are missing for more than one resource, the job logs contain
multiple permission error messages.

Before attempting to resubmit your Dataflow job, fix
the permission issues. The following resources provide information about
modifying roles and permissions.

- If you need to find a role that gives a specific permission, refer to the
  [IAM permissions reference](/iam/docs/permissions-reference).
- To grant a role to a principal for a project, see
  [Grant an IAM role by using the Google Cloud console](/iam/docs/grant-role-console).
- To add a missing permission for a project, IAM administrators
  can use the [`gcloud projects add-iam-policy-binding` command](/sdk/gcloud/reference/projects/add-iam-policy-binding):

  ```
  gcloud projects add-iam-policy-binding PROJECT_ID \
      --member=PRINCIPAL --role=ROLE
  ```

- To grant or change specific roles, see
  [Grant or revoke roles](/iam/docs/granting-changing-revoking-access#single-role).
- For information about required roles and permissions for the
  Dataflow worker service account, see
  [Worker service account](/dataflow/docs/concepts/security-and-permissions#worker-service-account)
  in the Dataflow security and permissions page.

If you want to override the pipeline validation and launch your job with
validation errors, use the following pipeline option:

```
--experiment=enable_ppv_effect=false
```

## There was a problem refreshing your credentials

When you try to run a Dataflow job, you see an error
similar to the following:

```
Workflow failed. Causes: There was a problem refreshing your credentials.
Please check: 1. The Dataflow API is enabled for your project.
2. Make sure both the Dataflow service account and the controller service account have sufficient permissions.
If you are not specifying a controller service account, ensure the default Compute Engine service account PROJECT_NUMBER-compute@developer.gserviceaccount.com exists and has sufficient permissions.
If you have deleted the default Compute Engine service account, you must specify a controller service account
```

This error occurs when the worker service account doesn't have the `roles/dataflow.worker`
role or when the Dataflow API isn't enabled.

First verify that the worker service account the `roles/dataflow.worker`
role. If needed, grant the `roles/dataflow.worker` to the worker service account.
For more information, see [Grant a single role](/iam/docs/manage-access-service-accounts#grant-single-role)
in the Identity and Access Management documentation.

To enable the Dataflow API, see
[Enabling an API in your Google Cloud Platform project](/endpoints/docs/openapi/enable-api).

## Required 'compute.subnetworks.get' permission

When you try to run a Dataflow job on a Shared VPC
network, you see an error similar to one of the following:

```
Required 'compute.subnetworks.get' permission for 'projects/project-id/regions/region/subnetworks/subnet-name' HTTP Code: 403
```

```
Required 'compute.subnetworks.use' permission for 'projects/project-id/regions/region/subnetworks/subnet-name' HTTP Code: 403
```

Shared VPC lets you export subnets from a [VPC network](/vpc/docs/vpc)
in a _host project_ to other _service projects_ in the same
[organization](/resource-manager/docs/creating-managing-organization). Instances
in the service projects can have network connections in the shared subnets of
the host project. For more information, see [Shared VPC
overview](/vpc/docs/shared-vpc).

To resolve this issue, first verify that the service project is attached to the
host project. For more information, see [Attach service
projects](/vpc/docs/provisioning-shared-vpc).

Next, ensure the [Dataflow Service
Account](/dataflow/docs/concepts/security-and-permissions#df-service-account) of
the service project (the project where the job runs) has the following roles:

- `roles/dataflow.serviceAgent`
- [`roles/compute.networkUser`](/compute/docs/access/iam#compute.networkUser)
  on the subnetwork

The Dataflow Service Account has the following name pattern:
`service-PROJECT_NUMBER@dataflow-service-producer-prod.iam.gserviceaccount.com`.

For more information, see [Guidelines for specifying a subnetwork parameter for
Shared VPC](/dataflow/docs/guides/specifying-networks#shared) and [Grant
a single role](/iam/docs/manage-access-service-accounts#grant-single-role) in
the Identity and Access Management documentation.

## Dataflow runner does not have access to bucket

When you try to list objects in a Cloud Storage bucket, the
Dataflow job fails, and you see an error similar to the following:

```
"dataflow-runner@project-id.iam.gserviceaccount.com" does not have `storage.objects.list` access to the Google Cloud Storage Bucket
```

This error occurs when the worker service account doesn't have the
`roles/storage.objectViewer` role.

To resolve this issue, grant your user account account the
`roles/storage.objectViewer` role. For more information, see [Grant a single
role](/iam/docs/manage-access-service-accounts#grant-single-role) in the
Identity and Access Management documentation.

## Cloud KMS key permission denied on resource

When you're [using customer-managed encryption keys](/dataflow/docs/guides/customer-managed-encryption-keys)
and try to create a Dataflow job, the job fails, and you see an error similar to the following:

```
Cloud KMS key permission 'cloudkms.cryptoKeyVersions.useToEncrypt' denied on resource
'projects/project-id/locations/location/keyRings/keyRingName/cryptoKeys/keyname' (or it may not exist). cannot be validated.
Please confirm the full key path is used (starts with projects) and that there are no typos.
```

This error occurs when the worker service account and the Dataflow
service account don't have the `roles/cloudkms.cryptoKeyEncrypterDecrypter`
[role](/kms/docs/reference/permissions-and-roles#predefined_roles).

To resolve this issue, grant the `roles/cloudkms.cryptoKeyEncrypterDecrypter` role
to the worker service account and to the Dataflow service account.
For more information, see [Granting Encrypter/Decrypter permissions](/dataflow/docs/guides/customer-managed-encryption-keys#granting_encrypterdecrypter_permissions)
in the Using customer-managed encryption keys page.

## Permission denied on resource

When you try to create a pipeline, the pipeline fails with the following error:

```
Permission 'datapipelines.pipelines.create' denied on resource '//datapipelines.googleapis.com/projects/PROJECT_ID/locations/REGION' (or it may not exist).
```

This error occurs if the worker service account of your project doesn't have
access to the files and other resources associated with the pipeline.

To resolve this issue, assign the following roles to the worker service account:

- `roles/dataflow.admin`
- `roles/dataflow.worker`

For more information, see
[Worker service account](/dataflow/docs/concepts/security-and-permissions#worker-service-account)
in "Dataflow security and permissions."

## Workflow failed

When you're [using customer-managed encryption keys](/dataflow/docs/guides/customer-managed-encryption-keys)
and try to create a Dataflow job, the job fails with the following error:

```
Workflow failed
```

This error can occur for the following reasons:

- The key and the Dataflow job aren't in the same region, or a multi-regional
  key is used. Global and multi-regional keys are not supported.
  The region for your CMEK and the [region](/dataflow/docs/resources/locations)
  for your Dataflow job must be the same.
- The key name is not specified correctly. The key might not exist, or the name might have a typo.

## Cloud KMS key can't protect resources for this job

When you're running a Dataflow job and trying to enable a
[customer-managed encryption key](/dataflow/docs/guides/customer-managed-encryption-keys),
the job fails, and you see an error similar to the following:

```
Cloud KMS key can't protect resources for this job. Please make sure the KMS key's region matches the Dataflow region
```

This error can occur for the following reasons:

- The key and the Dataflow job aren't in the same region, or a multi-regional
  key is used. Global and multi-regional keys are not supported.
  The region for your CMEK and the [region](/dataflow/docs/resources/locations)
  for your Dataflow job must be the same.
- The [`dataflowKMSKey`](/dataflow/docs/reference/pipeline-options#security_and_networking)
  parameter is not specified correctly.

## Vertical Autoscaling not working

When you're using [Vertical Autoscaling](/dataflow/docs/vertical-autoscaling),
the job doesn't automatically scale vertically,
and the following error appears in the job logs:

```
{"level":"error","ts":1708815877.1246133,"caller":"exporter/exporter.go:232","msg":"failed to get response from UAS: %v","error":"rpc error: code = PermissionDenied desc = The caller does not have permission","stacktrace":"google3/autoscaler/vitor/external/go/exporter/exporter.receiver\n\tautoscaler/vitor/external/go/exporter/exporter.go:232"}
```

This error occurs when the worker service account doesn't have the
Dataflow Worker (`roles/dataflow.worker`) role.

To resolve this issue, grant the worker service account the `roles/dataflow.worker`
role. For more information, see
[Grant a single role](/iam/docs/manage-access-service-accounts#grant-single-role)
in the Identity and Access Management documentation.

If you're using a custom role for the worker service account,
add the following permissions to the custom role:

- `autoscaling.sites.readRecommendations`
- `autoscaling.sites.writeMetrics`
- `autoscaling.sites.writeState`

## Not authorized to create Pub/Sub tracking subscription

When a Dataflow job reads from Pub/Sub using custom
event timestamps, the following error appears in the job logs:

```
Creating watermark tracking pubsub subscription projects/PROJECT_ID/subscriptions/SUBSCRIPTION __df_internal[16 HEX CHARACTERS] to topic projects/PROJECT_ID/topics/TOPIC failed with error: User not authorized to perform this action
```

You can configure Dataflow to read event timestamps from an
attribute on the Pub/Sub message. In that case,
Dataflow creates a second Pub/Sub subscription,
called the _tracking subscription_.

This error occurs when Dataflow doesn't have permission to create
the tracking subscription. For more information, see
[Timestamps and watermarks](/dataflow/docs/concepts/streaming-with-cloud-pubsub#low_latency_watermarks).
