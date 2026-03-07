---
source_url: https://docs.cloud.google.com/dataflow/docs/audit-logging
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Dataflow audit logging \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

This document describes audit logging for Dataflow. Google Cloud Platform services
generate audit logs that record administrative and access activities within your Google Cloud Platform resources.
For more information about Cloud Audit Logs, see the following:

- [Types of audit logs](/logging/docs/audit#types)
- [Audit log entry structure](/logging/docs/audit#audit_log_entry_structure)
- [Storing and routing audit logs](/logging/docs/audit#storing_and_routing_audit_logs)
- [Cloud Logging pricing summary](/stackdriver/pricing#logs-pricing-summary)
- [Enable Data Access audit logs](/logging/docs/audit/configure-data-access)

## Service name

Dataflow audit logs use the service name `dataflow.googleapis.com`.
Filter for this service:

## Methods by permission type

Each IAM permission has a `type` property, whose value is an enum
that can be one of four values: `ADMIN_READ`, `ADMIN_WRITE`,
`DATA_READ`, or `DATA_WRITE`. When you call a method,
Dataflow generates an audit log whose category is dependent on the
`type` property of the permission required to perform the method.
Methods that require an IAM permission with the `type` property value
of `DATA_READ`, `DATA_WRITE`, or `ADMIN_READ` generate
[Data Access](/logging/docs/audit#data-access) audit logs.
Methods that require an IAM permission with the `type` property value
of `ADMIN_WRITE` generate
[Admin Activity](/logging/docs/audit#admin-activity) audit logs.

API methods in the following list that are marked with (LRO) are long-running operations (LROs).
These methods usually generate two audit log entries: one when the operation starts and
another when it ends. For more information see [Audit logs for long-running operations](/logging/docs/audit/understanding-audit-logs#lro).

| Permission type | Methods                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ADMIN_WRITE`   | `dataflow.jobs.create` `dataflow.jobs.updateContents`                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `OTHER`         | `resourcemanager.projects.get`: To enable this log, enable `ADMIN_READ` under the service `cloudresourcemanager.googleapis.com`. `resourcemanager.projects.get`: To enable this log, enable `ADMIN_READ` under the service `cloudresourcemanager.googleapis.com`. `resourcemanager.projects.get`: To enable this log, enable `ADMIN_READ` under the service `cloudresourcemanager.googleapis.com`. `resourcemanager.projects.get`: To enable this log, enable `ADMIN_READ` under the service `cloudresourcemanager.googleapis.com`. |

## API interface audit logs

For information about how and which permissions are evaluated for each method,
see the Identity and Access Management documentation for Dataflow.

### `google.dataflow.v1beta3.FlexTemplatesService`

The following audit logs are associated with methods belonging to
`google.dataflow.v1beta3.FlexTemplatesService`.

#### `get`

- **Method**: `resourcemanager.projects.get`
- **Audit log type**: [Data access](/logging/docs/audit#data-access)
- **Permissions**:
  - `resourcemanager.projects.get - ADMIN_READ`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `protoPayload.methodName="resourcemanager.projects.get"`

### `google.dataflow.v1beta3.JobsV1Beta3`

The following audit logs are associated with methods belonging to
`google.dataflow.v1beta3.JobsV1Beta3`.

#### `create`

- **Method**: `dataflow.jobs.create`
- **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
- **Permissions**:
  - `dataflow.jobs.create - ADMIN_WRITE`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `protoPayload.methodName="dataflow.jobs.create"`

#### `updateContents`

- **Method**: `dataflow.jobs.updateContents`
- **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
- **Permissions**:
  - `dataflow.jobs.cancel - ADMIN_WRITE`
  - `dataflow.jobs.updateContents - ADMIN_WRITE`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `protoPayload.methodName="dataflow.jobs.updateContents"`

### `google.dataflow.v1beta3.TemplatesService`

The following audit logs are associated with methods belonging to
`google.dataflow.v1beta3.TemplatesService`.

#### `get`

- **Method**: `resourcemanager.projects.get`
- **Audit log type**: [Data access](/logging/docs/audit#data-access)
- **Permissions**:
  - `resourcemanager.projects.get - ADMIN_READ`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `protoPayload.methodName="resourcemanager.projects.get"`

#### `get`

- **Method**: `resourcemanager.projects.get`
- **Audit log type**: [Data access](/logging/docs/audit#data-access)
- **Permissions**:
  - `resourcemanager.projects.get - ADMIN_READ`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `protoPayload.methodName="resourcemanager.projects.get"`

#### `get`

- **Method**: `resourcemanager.projects.get`
- **Audit log type**: [Data access](/logging/docs/audit#data-access)
- **Permissions**:
  - `resourcemanager.projects.get - ADMIN_READ`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `protoPayload.methodName="resourcemanager.projects.get"`

## Methods that don't produce audit logs

A method might not produce audit logs for one or more of the following
reasons:

- It is a high volume method involving significant log generation and storage
  costs.
- It has low auditing value.
- Another audit or platform log already provides method coverage.

The following methods don't produce audit logs:

- `google.dataflow.v1beta3.DebugCaptureV1Beta3.GetConfig`
- `google.dataflow.v1beta3.DebugCaptureV1Beta3.SendCapture`
- `google.dataflow.v1beta3.JobsV1Beta3.AggregatedListJobs`
- `google.dataflow.v1beta3.JobsV1Beta3.CheckActiveJobs`
- `google.dataflow.v1beta3.JobsV1Beta3.GetJob`
- `google.dataflow.v1beta3.JobsV1Beta3.ListJobs`
- `google.dataflow.v1beta3.JobsV1Beta3.SnapshotJob`
- `google.dataflow.v1beta3.MessagesV1Beta3.ListJobMessages`
- `google.dataflow.v1beta3.MetricsV1Beta3.GetJobExecutionDetails`
- `google.dataflow.v1beta3.MetricsV1Beta3.GetJobMetrics`
- `google.dataflow.v1beta3.MetricsV1Beta3.GetStageExecutionDetails`
- `google.dataflow.v1beta3.SnapshotsV1Beta3.DeleteSnapshot`
- `google.dataflow.v1beta3.SnapshotsV1Beta3.GetSnapshot`
- `google.dataflow.v1beta3.SnapshotsV1Beta3.ListSnapshots`
- `google.dataflow.v1beta3.WorkItemsV1Beta3.LeaseWorkItem`
- `google.dataflow.v1beta3.WorkItemsV1Beta3.ReportWorkItemStatus`
- `google.dataflow.v1beta3.WorkerMessagesV1Beta3.SendWorkerMessages`
