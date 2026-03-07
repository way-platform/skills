---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/troubleshoot-autoscaling
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Troubleshoot Dataflow autoscaling \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

This page shows you how to resolve issues with the
[Dataflow autoscaling features](/dataflow/docs/guides/deploying-a-pipeline#autotuning-features)
and provides information about how to manage autoscaling.

## Job doesn't scale up or down

This section provides information about scenarios that might prevent workers from
scaling up or down.

### Streaming job doesn't scale up

When your streaming pipeline has a backlog, the workers don't scale up.

This issue occurs when the backlog lasts less than a few minutes or when parallelism is limited.

Sometimes, backlog is elevated but parallelism is low. In that case,
Dataflow doesn't scale up, because the work can't be distributed
across more workers, so adding more workers won't help with processing.
For more information, see [Streaming autoscaling](/dataflow/docs/horizontal-autoscaling#streaming).

### Batch and streaming jobs don't scale up

Your batch or streaming job runs as expected, but when more workers are needed,
the job doesn't scale up.

This issue might occur for one of the following reasons:

- The staging or temp files are inaccessible. If your job uses a Cloud Storage bucket, the bucket might have a
  [lifecycle configuration](/storage/docs/lifecycle) that deletes objects in the bucket.
  The deleted objects include staging and temp folders and files.
  To verify whether files have been deleted, [check the lifecycle configuration for the bucket](/storage/docs/managing-lifecycles#check).
  If the staging or temp folders or files were deleted after the job started, the packages required to create new workers might not exist.
  To resolve this issue, recreate the folders and files in the bucket.
- [Firewall rules](/vpc/docs/using-firewalls) prevent workers from sending and receiving traffic on the necessary TCP ports.
  Firewall rules might prevent workers from starting.
  Dataflow workers need to be able to send and receive traffic on TCP ports 12345 and 12346.
  For more information, including steps to resolve this issue, see
  [Firewall rules for Dataflow](/dataflow/docs/guides/routes-firewall#firewall_rules).
- A custom source has a `getProgress()` method that returns a NULL value.
  When you use a custom source, the [backlog metrics](/dataflow/docs/guides/using-monitoring-intf#backlog) rely on
  the return value of your custom source's `getProgress()` method to start collecting data. The default
  implementation for `getProgress()` returns a NULL value. To resolve this issue,
  ensure that your custom source overrides the default `getProgress()` method to return a non-NULL value.
- An update triggered by Vertical Autoscaling temporarily deactivates Horizontal
  Autoscaling. For more information, see
  [Effect on Horizontal Autoscaling](/dataflow/docs/vertical-autoscaling#horizontal-autoscaling).
- If you're using a `map` operation in a Python pipeline and your job doesn't
  scale up, you might need to add a
  [`Reshuffle` transform](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html?highlight=reshuffle#apache_beam.transforms.util.Reshuffle)
  to your pipeline code. For more information, see
  [Reshuffle](https://beam.apache.org/documentation/transforms/python/other/reshuffle/)
  in the Apache Beam documentation.

### Streaming job doesn't scale down

When your streaming job has a low backlog and low CPU utilization,
the workers don't scale down. This issue can occur for various reasons.

- When jobs don't use Streaming Engine, Dataflow balances the number of persistent
  disks between the workers. As a result, each worker must have an equal number of
  persistent disks. For example, if there are 100 disks and 100 workers, each worker has one disk.
  When the job scales down, the job can have 50 workers with two persistent disks per worker.
  The job doesn't scale down again until it can have 25 workers with four persistent disks per worker.
  In addition, the minimum number of workers is the value assigned to `maxNumWorkers` divided by 15.
  For more information, see [Scaling range for streaming autoscaling pipelines](#scaling-range).
- When jobs use Streaming Engine, the downscaling target is based on a target CPU utilization of 75%.
  When this CPU utilization can't be achieved, downscaling is disabled.
- The backlog time estimate needs to stay below ten seconds for at least two minutes before workers scale down.
  Fluctuations in backlog time might disable scaling down. In addition, low throughput can skew the time estimate.
- [`PeriodicImpulse`](https://beam.apache.org/releases/javadoc/current/org/apache/beam/sdk/transforms/PeriodicImpulse.html)
  is supported in the Apache Beam SDK versions 2.60.0 and later.
  When your pipeline uses `PeriodicImpulse` with the Apache Beam
  SDK versions 2.59.0 and earlier,
  Dataflow workers don't scale down as expected.

### Scaling up stops

Your batch or streaming job starts scaling up, but the workers stop scaling up even though a backlog remains.

This issue occurs when quota limits are reached.

- **Compute Engine quotas:** Dataflow jobs are subject to
  the [Compute Engine quota](/compute/quotas) of the project. If multiple jobs are running,
  the project might be at the limit of its Compute Engine quota. In that case,
  Dataflow can't increase the number of workers.
- **CPU quotas:** Dataflow jobs are also subject to
  the [CPU quota](/compute/quotas#cpu_quota) of the project. If the worker type uses
  more than one CPU, the project might be at the limit of the CPU quota.
- **External IP address quotas**: When your job uses [external IP addresses](/compute/quotas#external_ip_addresses) to
  communicate with resources, you need as many external IPs addresses as workers.
  When the number of workers scales up, the number of external IP addresses also increases.
  When you reach the [IP address limit](/vpc/docs/quota#ip_address_limits), the workers stop scaling up.

In addition, if the region you choose is out of a resource, you can't create new resources of that type, even if you have remaining quota in your region or project. For example, you might still have quota to create external IP addresses in `us-central1`, but that region might not
have available IP addresses. For more information, see [Quotas and resource availability](/compute/quotas#quotas_and_resource_availability).

To resolve this issue, [request a quota increase](/compute/quotas#requesting_additional_quota)
or run the job in a different region.

## The worker utilization hint has no effect

You set the
[worker utilization hint](/dataflow/docs/guides/tune-horizontal-autoscaling#utilization-hint)
but the autoscaling behavior does not change.

To understand this issue, go to the
[Worker CPU utilization chart](/dataflow/docs/guides/autoscaling-metrics#cpu-use)
and check whether the worker utilization hint is actively used. If the hint is
being used, the chart shows
`CPU utilization hint (actively used by autoscaler)`. Otherwise, it shows
`CPU utilization hint (not actively used by autoscaler)`.

The utilization hint is only one factor that affects autoscaling. The following
table lists some reasons why the autoscaler might not actively use the hint:

| Observed scaling behavior | Causes                                                                                                                                                                                                                                                                                                                                                                                            | Metrics to check                                                                                                                                                                                                             |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| No change                 | - You have reached the minimum or maximum number of workers. - The number of workers is limited by the number of keys processed in parallel. - Jobs are throttled by external RPCs. - The downscaling adjustment is too small or Dataflow is _dampening_ downscaling. For more information, see [Streaming autoscaling heuristics](/dataflow/docs/guides/tune-horizontal-autoscaling#heuristics). | - `job/aggregated_worker_utilization` - `job/max_worker_instances_limit` - `job/min_worker_instances_limit` - `job/processing_parallelism_keys` - RPC errors reported in worker error logs - Crashes reported in worker logs |
| Scale up                  | - High backlog or latency goal is overriding the hint. - The minimum number of workers was updated to a higher value than the current number of workers.                                                                                                                                                                                                                                          | - `job/aggregated_worker_utilization` - `job/backlog_bytes` - `job/backlog_elements` - `job/estimated_timer_backlog_processing_time` - `job/min_worker_instances_limit`                                                      |
| Scale down                | - The maximum number of workers was updated to a lower value than the current number of workers.                                                                                                                                                                                                                                                                                                  | - `job/aggregated_worker_utilization` - `job/max_worker_instances_limit`                                                                                                                                                     |

For more information, see
[Streaming autoscaling heuristics](/dataflow/docs/guides/tune-horizontal-autoscaling#heuristics).

## Gaps in autoscaling metrics

There are short, temporary gaps in autoscaling metrics.

This issue can occur if backend tasks are restarted. These gaps in the metrics
don't indicate a problem with autoscaling or the health of your streaming job.

## CPU is unevenly distributed

When the job is autoscaling, CPU utilization is unevenly distributed among workers.
Some workers have higher CPU utilization, system latency, or data freshness than others.

This issue can occur if your data contains a hot key. A hot key is a key with
enough elements to negatively affect pipeline performance. Each key must be
processed by a single worker, so the work can't be split between workers.

For more information, see the
[hot key error guidance](/dataflow/docs/guides/common-errors#hot-key-detected).

## The work item requesting state read is no longer valid on the backend

During communication between worker VM instances and Streaming Engine tasks in a
streaming pipeline, the following error occurs:

```
The work item requesting state read is no longer valid on the backend.
The work has already completed or will be retried.
This is expected during autoscaling events.
```

During autoscaling, worker VM instances communicate with multiple
Streaming Engine tasks, and each task serves multiple worker VM instances.
Item keys are used to distribute the work. Each task and worker VM instance have a
collection of key ranges, and the distribution of these ranges can change
dynamically. For example, during autoscaling, job resizing can cause the key
range distribution to change. When a key range changes, this error can occur.
The error is expected, and unless you see a correlation between these messages
and an underperforming pipeline, you can ignore it.

## Insufficient Streaming Engine resources

If Streaming Engine cannot allocate the minimum number of workers that you
request, the following error is returned:

```
Streaming Engine does not currently have enough resources available to fulfill
the request.
```

To resolve this issue, try setting a smaller minimum number of workers. See
[Set the autoscaling range](/dataflow/docs/guides/tune-horizontal-autoscaling#set-range).

## Scaling range for streaming autoscaling pipelines

This section provides details about the scaling range for streaming
autoscaling pipelines.

### Java

For streaming autoscaling jobs that don't use
[Streaming Engine](/dataflow/docs/streaming-engine), the
Dataflow service allocates between 1 to 15 Persistent Disks to
each worker. This allocation means that the minimum number of
workers used for a streaming autoscaling pipeline is N/15, where N is the value
of `--maxNumWorkers`.

For streaming autoscaling jobs that use
[Streaming Engine](/dataflow/docs/streaming-engine),
the minimum number of workers is 1.

Dataflow balances the number of Persistent Disks between the
workers. For example, if your pipeline needs three or four workers in steady
state, you could set `--maxNumWorkers=15`. The pipeline automatically
scales between 1 and 15 workers, using 1, 3, 5, or 15 workers, which
correspond to 15, 5, 3, or 1 Persistent Disks per worker, respectively.

`--maxNumWorkers` can be 1000 at most.

### Python

For streaming autoscaling jobs that don't use
[Streaming Engine](/dataflow/docs/streaming-engine), the
Dataflow service allocates between 1 to 15 Persistent Disks to
each worker. This allocation means that the minimum number of
workers used for a streaming autoscaling pipeline is N/15, where N is the value
of `--max_num_workers`.

For streaming autoscaling jobs that use
[Streaming Engine](/dataflow/docs/streaming-engine),
the minimum number of workers is 1.

Dataflow balances the number of Persistent Disks between the
workers. For example, if your pipeline needs three or four workers in steady
state, you could set `--max_num_workers=15`. The pipeline automatically
scales between 1 and 15 workers, using 1, 2, 3, 4, 5, 8, or 15 workers, which
correspond to 15, 8, 5, 4, 3, 2, or 1 Persistent Disks per worker,
respectively.

`--max_num_workers` can be 1000 at most.

### Go

For streaming autoscaling jobs that don't use
[Streaming Engine](/dataflow/docs/streaming-engine), the
Dataflow service allocates between 1 to 15 Persistent Disks to
each worker. This allocation means that the minimum number of
workers used for a streaming autoscaling pipeline is N/15, where N is the value
of `--max_num_workers`.

For streaming autoscaling jobs that use
[Streaming Engine](/dataflow/docs/streaming-engine),
the minimum number of workers is 1.

Dataflow balances the number of Persistent Disks between the
workers. For example, if your pipeline needs three or four workers in steady
state, you could set `--max_num_workers=15`. The pipeline automatically
scales between 1 and 15 workers, using 1, 2, 3, 4, 5, 8, or 15 workers, which
correspond to 15, 8, 5, 4, 3, 2, or 1 Persistent Disks per worker,
respectively.

`--max_num_workers` can be 1000 at most.

## Maximum number of workers streaming autoscaling might use

### Java

Dataflow operates within the limits of the
Compute Engine instance count quota of your project or `maxNumWorkers`, whichever is
lower.

### Python

Dataflow operates within the limits of the
Compute Engine instance count quota of your project or `max_num_workers`, whichever is
lower.

### Go

Dataflow operates within the limits of the
Compute Engine instance count quota of your project or `max_num_workers`, whichever is
lower.

## Limit autoscaling to reduce the impact on billing

If you don't want autoscaling to increase your bill, you can limit the maximum
number of workers that your streaming job can use.

### Java

By specifying `--maxNumWorkers`, you limit the scaling range used to process
your job.

### Python

By specifying `--max_num_workers`, you limit the scaling range used to process
your job.

### Go

By specifying `--max_num_workers`, you limit the scaling range used to process
your job.

## Change the scaling range

For information about changing the scaling range on a streaming pipeline, see
[Set the autoscaling range](/dataflow/docs/guides/tune-horizontal-autoscaling#set-range).

## Turn off autoscaling on streaming pipelines

To turn off autoscaling on streaming pipeline, follow these steps.

### Java

Set `--autoscalingAlgorithm=NONE`. For more information, see
[Disable Horizontal Autoscaling](/dataflow/docs/horizontal-autoscaling#disable).

### Python

Set `--autoscaling_algorithm=NONE`. For more information, see
[Disable Horizontal Autoscaling](/dataflow/docs/horizontal-autoscaling#disable).

### Go

Set `--autoscaling_algorithm=NONE`. For more information, see
[Disable Horizontal Autoscaling](/dataflow/docs/horizontal-autoscaling#disable).

## Use a fixed number of workers

For streaming jobs that don't use
[Streaming Engine](/dataflow/docs/streaming-engine), the default behavior is
to use a fixed number of workers. To use streaming autoscaling with these
pipelines, you must explicitly opt in as it's not on by default.
