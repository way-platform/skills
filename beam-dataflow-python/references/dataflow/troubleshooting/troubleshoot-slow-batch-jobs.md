---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/troubleshoot-slow-batch-jobs
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Troubleshoot slow or stuck batch jobs \u00a0|\u00a0 Cloud Dataflow \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

This page explains how to troubleshoot common causes of slow or stuck
Dataflow batch jobs.

If your batch job is slow or stuck, use the
[Execution details](/dataflow/docs/concepts/execution-details) tab to find more
information about the job and to identify the stage or worker that's causing a bottleneck.

## Identify the root cause

1. Check whether the job is running into issues during worker startup. For more
   information, see
   [Error syncing pod](/dataflow/docs/guides/common-errors#error-syncing-pod).

   To verify the job has started processing data, look in the
   [job-message](/dataflow/docs/guides/logging#log-types) log for the following
   log entry:

   ```
   All workers have finished the startup processes and began to receive work requests
   ```

2. To compare job performance between different jobs, make sure the volume of
   input data, worker configuration, autoscaling behavior, and
   [Dataflow Shuffle](/dataflow/docs/shuffle-for-batch) settings
   are the same.
3. Check the [job-message](/dataflow/docs/guides/logging#log-types) logs for
   issues such as quota limits, stockout issues, or IP address exhaustion.
4. In the [**Execution details**](/dataflow/docs/concepts/execution-details)
   tab, compare the
   [stage progress](/dataflow/docs/concepts/execution-details#progress-batch)
   to identify stages that took longer.
5. Look for any stragglers in the job. For more information, see
   [Troubleshooting stragglers in batch jobs](/dataflow/docs/guides/troubleshoot-batch-stragglers).
6. Check the throughput, CPU, and memory utilization metrics.
7. Check the [worker logs](/dataflow/docs/guides/logging#log-types) for warnings
   and errors.
   - If the worker logs contain errors, view the stack trace. Investigate
     whether the error is caused by a bug in your code.
   - Look for Dataflow errors. See
     [Troubleshoot Dataflow errors](/dataflow/docs/guides/common-errors).
   - Look for
     [out-of-memory errors](/dataflow/docs/guides/troubleshoot-oom#find-errors),
     which can cause a stuck pipeline. If you see out-of-memory errors, follow
     the steps in
     [Troubleshoot Dataflow out of memory errors](/dataflow/docs/guides/troubleshoot-oom).
   - To identify a slow or stuck step, check the worker logs for
     `Operation ongoing` messages. View the stack trace to see where the step is
     spending time. For more information, see
     [Processing stuck or operation ongoing](/dataflow/docs/guides/common-errors#processing-stuck).

8. [Check for hot keys](#hot-keys).
9. If you aren't using
   [Dataflow Shuffle](/dataflow/docs/shuffle-for-batch), check the
   [shuffler logs](/dataflow/docs/guides/logging#log-types) for warnings and
   errors during shuffle operation. If you see an
   [RPC timeout error](/dataflow/docs/guides/troubleshoot-networking#worker-communicate-firewall-ports)
   on port 12345 or 12346, your job might be missing a firewall rule. See
   [Firewall rules for Dataflow](/dataflow/docs/guides/routes-firewall#firewall_rules).
10. If Runner v2 is enabled, check the
    [harness](/dataflow/docs/guides/logging#log-types) logs for errors. For more
    information, see [Troubleshoot Runner v2](/dataflow/docs/runner-v2#debugging).

## Identify stragglers

A straggler is a work item that is slow relative to other work items in the
stage. For information about identifying and fixing stragglers, see
[Troubleshoot stragglers in batch jobs](/dataflow/docs/guides/troubleshoot-batch-stragglers).

## Identify slow or stuck stages

To identify slow or stuck stages, use the
[**Stage progress**](/dataflow/docs/concepts/execution-details#progress-batch) view.
Longer bars indicate that the stage takes more time. Use this view to
identify the slowest stages in your pipeline.

After you find the bottleneck stage, you can take the following steps:

- Identify the
  [lagging worker](#lagging-worker) within that stage.
- If there are no lagging workers, identify the slowest step by using the
  [**Stage info**](/dataflow/docs/concepts/execution-details#stage-info)
  panel. Use this information to identify candidates for user code optimization.
- To find parallelism bottlenecks, use
  [Dataflow monitoring metrics](#debug-tools).

## Identify a lagging worker

To identify a lagging worker for a specific stage, use the
[**Worker progress**](/dataflow/docs/concepts/execution-details#worker-progress)
view. This view shows whether all workers are processing work until the end of the stage,
or if a single worker is stuck on a lagging task. If you find a lagging worker,
take the following steps:

- View the log files for that worker. For more information, see
  [Monitor and view pipeline logs](/dataflow/docs/guides/logging#MonitoringLogs).
- View the
  [CPU utilization metrics](/dataflow/docs/guides/using-monitoring-intf#cpu-use)
  and the [worker progress](/dataflow/docs/concepts/execution-details#worker-progress)
  details for lagging workers. If you see unusually high or low CPU utilization,
  in the log files for that worker, look for the following issues:
  - [`A hot key ... was detected`](/dataflow/docs/guides/common-errors#hot-key-detected)
  - [`Processing stuck ... Operation ongoing`](/dataflow/docs/guides/common-errors#processing-stuck)

## Tools for debugging

When you have a slow or stuck pipeline, the following tools can help you
diagnose the problem.

- To correlate incidents and identify bottlenecks, use
  [Cloud Monitoring for Dataflow](/dataflow/docs/guides/using-cloud-monitoring).
- To monitor pipeline performance, use
  [Cloud Profiler](/dataflow/docs/guides/profiling-a-pipeline).
- Some transforms are better suited to high-volume pipelines than others. Log
  messages can
  [identify a stuck user transform](/dataflow/docs/guides/common-errors#processing-stuck)
  in either batch or streaming pipelines.
- To learn more about a stuck job, use
  [Dataflow job metrics](/dataflow/docs/guides/using-monitoring-intf).
  The following list includes useful metrics:
  - The [Backlog bytes](/dataflow/docs/guides/using-monitoring-intf#backlog)
    metric (`backlog_bytes`) measures the amount of unprocessed input in bytes by
    stage. Use this metric to find a fused step that has no throughput.
    Similarly, the backlog elements metric (`backlog_elements`) measures the number of
    unprocessed input elements for a stage.
  - The [Processing parallelism keys](/dataflow/docs/guides/using-monitoring-intf#parallelism)
    (`processing_parallelism_keys`) metric measures the number of parallel processing
    keys for a particular stage of the pipeline over the last five minutes.
    Use this metric to investigate in the following ways:
    - Narrow the issue down to specific stages and confirm hot key warnings, such as
      [`A hot key ... was detected`](/dataflow/docs/guides/common-errors#hot-key-detected).
    - Find throughput bottlenecks caused by insufficient parallelism.
      These bottlenecks can result in slow or stuck pipelines.
  - The [System lag](/dataflow/docs/guides/using-monitoring-intf#system_latency_streaming)
    metric (`system_lag`) and the per-stage system lag metric (`per_stage_system_lag`) measure
    the maximum amount of time an item of data has been processing or awaiting
    processing. Use these metrics to identify inefficient stages and
    bottlenecks from data sources.

For additional metrics that aren't included in the Dataflow
monitoring web interface, see the complete list of Dataflow metrics in
[Google Cloud Platform metrics](/monitoring/api/metrics_gcp_d_h#gcp-dataflow).
