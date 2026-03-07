---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/estimated-cost
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Dataflow estimated cost \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

The **Estimated Cost** page in the Google Cloud console shows the estimated cost of your current Dataflow
job. Estimated costs are calculated by multiplying the resource usage metrics
as shown in Cloud Monitoring by
the [price of those resources in the job region](https://cloud.google.com/dataflow/pricing).

To view the estimated cost for a job, perform the following steps:

1. In the Google Cloud console, go to the **Dataflow** >
   **Jobs** page.

   [Go to Jobs](https://console.cloud.google.com/dataflow/jobs)

2. Select a job.
3. Click the **Cost** tab.

**Warning:** The estimated cost might not reflect the actual job cost for a variety
of reasons, such as contractual discounts or temporary billing adjustments.
To view the actual cost of your Dataflow jobs, view the
[Cloud Billing reports for your Cloud Billing account](/billing/docs/how-to/reports#getting_started)
in the Google Cloud console.

## Use cost monitoring

Job cost estimates are available for both batch and streaming jobs. The
**Estimated Cost** page in the Google Cloud console provides the following
information:

- Details about which resources contribute to the job cost and by how much.
  Resources include vCPUs, memory, Dataflow Shuffle data processed
  or Streaming Engine data processed, and SSD and HDD disk usage.
- Costs over specific time windows, such as: time since the job started, the previous
  hour, the last 24 hours, the preceding seven days, and a user-specified time range.

You can use monitoring alerts to get notifications when your job costs cross a specified threshold.
You can also use alerts to make changes to your jobs, such as stopping or canceling jobs,
based on the thresholds that you set.

To create a Cloud Monitoring alert rule, click **Create alert**.
For instructions about how to configure these alerts, see
[Use Cloud Monitoring for Dataflow pipelines](/dataflow/docs/guides/using-cloud-monitoring).

## Limitations

Dataflow cost monitoring does not support
Dataflow Prime jobs and does not reflect additional GPU accelerator cost.

Dataflow cost monitoring approximates the TPU accelerator costs
using the vCPU and memory costs, even though TPU workers don't incur vCPU and
memory charges.
