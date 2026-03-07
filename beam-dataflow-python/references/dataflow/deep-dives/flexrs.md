---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/flexrs
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Use Flexible Resource Scheduling in Cloud Dataflow \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

This page explains how to enable Flexible Resource Scheduling (FlexRS) for
autoscaled batch pipelines in Dataflow.

FlexRS reduces batch processing costs by using advanced
[scheduling techniques](/dataflow/docs/guides/flexrs#delayed_scheduling), the
[Dataflow Shuffle](/dataflow/docs/shuffle-for-batch)
service, and a combination of
[preemptible virtual machine (VM) instances](/compute/docs/instances/preemptible)
and regular VMs. By running preemptible VMs and regular VMs in parallel,
Dataflow improves the user experience when Compute Engine stops
preemptible VM instances during a system event. FlexRS helps to ensure that
the pipeline continues to make progress and that you don't lose previous work
when [Compute Engine
preempts](/compute/docs/instances/preemptible#what_is_a_preemptible_instance)
your preemptible VMs.

Jobs with FlexRS use the service-based [Dataflow
Shuffle](/dataflow/docs/shuffle-for-batch) for
joining and grouping. As a result, FlexRS jobs don't use Persistent Disk resources
for storing temporary calculation results. Using Dataflow Shuffle
allows FlexRS to handle the preemption of a worker VM better, because the
Dataflow service doesn't have to redistribute data to the remaining
workers. Each Dataflow worker still needs a small 25 GB
Persistent Disk volume to store the machine image and temporary logs.

## Support and limitations

- Supports batch pipelines.
- Requires the Apache Beam SDK for Java 2.12.0 or later, the Apache Beam SDK
  for Python 2.12.0 or later, or the Apache Beam SDK for Go.
- Uses [Dataflow Shuffle](/dataflow/docs/shuffle-for-batch).
  Turning on FlexRS automatically enables Dataflow
  Shuffle.
- Doesn't support GPUs.
- Doesn't support Compute Engine reservations.
- FlexRS jobs have a scheduling delay. Therefore, FlexRS is most suitable for
  workloads that are not time-critical, such as daily or weekly jobs that can
  complete within a certain time window.

## Delayed scheduling

When you submit a FlexRS job, the Dataflow service
places the job into a queue and submits it for execution within six hours of
job creation. Dataflow finds the best time to start the job
within that time window, based on the available capacity and other factors.

When you submit a FlexRS job, the Dataflow service executes the
following steps:

1. Returns a job ID immediately after job submission.
2. Performs an [early validation](/dataflow/docs/guides/flexrs#early_validation)
   run.
3. Uses the early validation result to determine the next step.
   1. On success, queues the job to wait for the delay launch.
   2. In all other cases, the job fails and the Dataflow service
      reports the errors.

If validation succeeds, in the Dataflow
[monitoring interface](/dataflow/docs/guides/using-monitoring-intf#accessing_the_cloud_dataflow_monitoring_interface),
your job displays an ID and the
[status](/dataflow/docs/guides/troubleshooting-your-pipeline#Status)
`Queued`. If validation fails, your job displays the status `Failed`.

### Early validation

FlexRS jobs do not immediately launch upon submission. During early
validation, the Dataflow service verifies the execution parameters and
Google Cloud Platform environment settings, such as
[IAM roles](/dataflow/docs/concepts/access-control) and network configurations.
Dataflow validates the job as much as possible at job
submission time and reports potential errors. You are not billed for this early
validation process.

The early validation step does not execute user code. You must verify your code
to check for issues using the Apache Beam
[Direct Runner](https://beam.apache.org/documentation/runners/direct/) or
non-FlexRS jobs. If there are Google Cloud environment changes between
job creation and the job's delayed scheduling, the job might succeed during early
validation but still fail at launch time.

## Enable FlexRS

When you create a FlexRS job, a concurrent job quota is taken, even when the job is in the
**Queued** status. The early validation process does not verify or reserve any other quotas. Therefore, before you enable FlexRS, verify that you have
enough Google Cloud project resource [quotas](/dataflow/quotas) to launch
your job. This includes additional quota for preemptible CPUs,
regular CPUs, and IP addresses, unless you turn off the
[Public IP parameter](/dataflow/docs/guides/specifying-networks#public_ip_parameter).

If you do not have enough quota, your account might not have enough resources
when your FlexRS job deploys. Dataflow selects preemptible VMs for 90%
of workers in the worker pool by default. When planning for CPU quota, make sure
that you have sufficient
[preemptible VM quota](/compute/resource-usage#allocation_quotas_for_preemptible_resources). You can explicitly [request preemptible VM
quota](/compute/quotas#requesting_additional_quota); otherwise, your FlexRS job
will lack the resources to execute in a timely manner.

### Pricing

FlexRS jobs are billed for the following resources:

- Regular and preemptible CPUs
- Memory resources
- Dataflow Shuffle resources
- 25 GB per worker of Persistent Disk resources

While Dataflow uses both preemptible and regular workers to
execute your FlexRS job, you are billed a uniform discounted rate compared to
regular Dataflow prices regardless of the worker type.
Dataflow Shuffle and Persistent Disk resources are not discounted.

For more information, read the [Dataflow pricing
details](https://cloud.google.com/dataflow/pricing#pricing_details) page.

### Pipeline options

### Java

To enable a FlexRS job, use the following pipeline option:

- `--flexRSGoal=COST_OPTIMIZED`, where the cost-optimized goal means that the
  Dataflow service chooses any available discounted resources.
- `--flexRSGoal=SPEED_OPTIMIZED`, where it optimizes for lower execution time.
  If unspecified, the field `--flexRSGoal` defaults to `SPEED_OPTIMIZED`, which
  is the same as omitting this flag.

FlexRS jobs affect the following
[execution parameters](/dataflow/docs/guides/specifying-exec-params):

- `numWorkers` only sets the initial number of workers. However, you can
  set `maxNumWorkers` for cost control reasons.
- You cannot use the `autoscalingAlgorithm` option with FlexRS jobs.
- You cannot specify the `zone` flag for FlexRS jobs. The
  Dataflow service selects the zone for all FlexRS jobs in the
  region that you specified with the `region` parameter.
- You must select a
  [Dataflow location](/dataflow/docs/resources/locations)
  as your `region`.
- You cannot use the M2, M3, or H3 machine series for your `workerMachineType`.

The following example shows how to add parameters to your regular
pipeline parameters in order to use FlexRS:

```
--flexRSGoal=COST_OPTIMIZED \
--region=europe-west1 \
--maxNumWorkers=10 \
--workerMachineType=n1-highmem-16
```

If you omit `region`, `maxNumWorkers`, and `workerMachineType`, the
Dataflow service determines the default value.

### Python

To enable a FlexRS job, use the following pipeline option:

- `--flexrs_goal=COST_OPTIMIZED`, where the cost-optimized goal means that the
  Dataflow service chooses any available discounted resources.
- `--flexrs_goal=SPEED_OPTIMIZED`, where it optimizes for lower execution time.
  If unspecified, the field `--flexrs_goal` defaults to `SPEED_OPTIMIZED`, which
  is the same as omitting this flag.

FlexRS jobs affect the following
[execution parameters](/dataflow/docs/guides/specifying-exec-params):

- `num_workers` only sets the initial number of workers. However, you can
  set `max_num_workers` for cost control reasons.
- You cannot use the `autoscalingAlgorithm` option with FlexRS jobs.
- You cannot specify the `zone` flag for FlexRS jobs. The
  Dataflow service selects the zone for all FlexRS jobs in the
  region that you specified with the `region` parameter.
- You must select a
  [Dataflow location](/dataflow/docs/resources/locations)
  as your `region`.
- You cannot use the M2, M3, or H3 machine series for your `machine_type`.

The following example shows how to add parameters to your regular
pipeline parameters in order to use FlexRS:

```
--flexrs_goal=COST_OPTIMIZED \
--region=europe-west1 \
--max_num_workers=10 \
--machine_type=n1-highmem-16
```

If you omit `region`, `max_num_workers`, and `machine_type`, the
Dataflow service determines the default value.

### Go

To enable a FlexRS job, use the following pipeline option:

- `--flexrs_goal=COST_OPTIMIZED`, where the cost-optimized goal means that the
  Dataflow service chooses any available discounted resources.
- `--flexrs_goal=SPEED_OPTIMIZED`, where it optimizes for lower execution time.
  If unspecified, the field `--flexrs_goal` defaults to `SPEED_OPTIMIZED`, which
  is the same as omitting this flag.

FlexRS jobs affect the following
[execution parameters](/dataflow/docs/guides/specifying-exec-params):

- `num_workers` only sets the initial number of workers. However, you can
  set `max_num_workers` for cost control reasons.
- You cannot use the `autoscalingAlgorithm` option with FlexRS jobs.
- You cannot specify the `zone` flag for FlexRS jobs. The
  Dataflow service selects the zone for all FlexRS jobs in the
  region that you specified with the `region` parameter.
- You must select a
  [Dataflow location](/dataflow/docs/resources/locations)
  as your `region`.
- You cannot use the M2, M3, or H3 machine series for your `worker_machine_type`.

The following example shows how to add parameters to your regular
pipeline parameters in order to use FlexRS:

```
--flexrs_goal=COST_OPTIMIZED \
--region=europe-west1 \
--max_num_workers=10 \
--machine_type=n1-highmem-16
```

If you omit `region`, `max_num_workers`, and `machine_type`, the
Dataflow service determines the default value.

### Dataflow templates

Some [Dataflow templates](/dataflow/docs/concepts/dataflow-templates)
don't support the the FlexRS pipeline option.
As an alternative, use the following
[pipeline option](/dataflow/docs/guides/setting-pipeline-options#experimental).

```
--additional-experiments=flexible_resource_scheduling,shuffle_mode=service,delayed_launch
```

## Monitor FlexRS jobs

You can monitor the status of your FlexRS job on the Google Cloud console in two
places:

1. The [**Jobs** page](/dataflow/docs/guides/using-monitoring-intf#accessing_the_cloud_dataflow_monitoring_interface)
   that shows all your jobs.
2. The [**Monitoring interface** page](/dataflow/docs/guides/using-monitoring-intf#viewing_a_pipeline)
   of the job you submitted.

On the **Jobs** page, jobs that have not started show the status **Queued**.

![A list of Dataflow
    jobs in the Google Cloud console containing a job with Queued status.](/static/dataflow/images/flexrs_jobsummarycleared.png)

Figure 1: A list of Dataflow
jobs in the Google Cloud console containing a job with **Queued** status.

On the **Monitoring interface** page, jobs that are waiting in the queue display
the message "Graph will appear after a job starts" in the **Job graph** tab.

![A queued individual pipeline job in the Cloud Dataflow monitoring
              interface.](/static/dataflow/images/flexrs_jobdetails2.png)

Figure 2: A queued individual pipeline job shown in the
Dataflow monitoring interface.
