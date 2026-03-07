---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/thread-scaling
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Dynamic thread scaling \u00a0|\u00a0 Cloud Dataflow \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

Dynamic thread scaling is a part of Dataflow's suite of vertical
scaling features. It complements Dataflow's [horizontal
autoscaling](/dataflow/docs/horizontal-autoscaling) feature by adjusting the
number of parallel tasks, also known as
[bundles](https://beam.apache.org/documentation/runtime/model/#bundling-and-persistence),
that each Dataflow worker runs. The goal is to increase the
overall efficiency of your Dataflow pipeline.

When Dataflow runs a pipeline, the processing is distributed
across multiple Compute Engine virtual machines (VMs), also known as
workers. A thread is a single executable task running within a larger process.
Dataflow launches several threads on each worker.

With dynamic thread scaling enabled, the Dataflow service
automatically chooses the appropriate number of threads to run on each
Dataflow worker. Because each thread runs a task, increasing the
number of threads allows more tasks to run in parallel on a worker. When you use
this feature with the horizontal autoscaling feature, the total number of
threads used by the pipeline remains the same, but fewer workers are used.

Dynamic thread scaling uses an algorithm to determine how many
threads each worker needs based on resource utilization signals generated
during pipeline execution. For more information, see the
[How it works](#how-it-works) section on this page.

## Benefits

Dynamic thread scaling has the following potential benefits.

- Allows Dataflow workers to process data more efficiently by
  improving per-worker CPU and memory utilization.
- Improves parallel processing by adjusting the number of worker threads
  available to run tasks in parallel during pipeline execution.
- Reduces the number of workers required to process large datasets, which
  might reduce your costs.

## Support and limitations

- Dynamic thread scaling is available for pipelines that use the Java, Python,
  and Go SDKs.
- The Dataflow job must use [Runner v2](/dataflow/docs/runner-v2).
- Only batch pipelines are supported.
- Pipelines that are CPU or memory intensive might not benefit from dynamic
  thread scaling.
- Dynamic thread scaling doesn't reduce the amount of time it takes a
  Dataflow job to complete.
- Dynamic thread scaling is primarily intended for data-related memory
  issues. If you are running out of memory due to the size of an ML model,
  see [Memory Management](/dataflow/docs/machine-learning/runinference-best-practices#memory-management).
- For high-memory use cases, you might still need to manually
  tune `num_worker_harness_threads` or switch to a high-memory machine
  type.

## How it works

Dynamic thread scaling uses autotuning principles to dynamically
scale the thread count up or down on each worker in the Dataflow worker
pool. The thread count is scaled independently on each worker. Each thread
runs a task. Increasing the number of threads allows more tasks to run in
parallel on a worker. As tasks complete and the threads are no longer needed,
the thread count scales down. An algorithm determines how many threads each worker needs.

The thread count on a worker scales up to a maximum of two threads per vCPU when
both of the following conditions are met:

- Memory utilization on the worker is less than 50%.
- CPU utilization on the worker is less than 65%.

The thread count on a worker scales down to a minimum of one thread per vCPU when
the following condition is met:

- Memory utilization on the worker is more than 70%.

To view memory and CPU utilization for your job, use the
[**Job metrics**](/dataflow/docs/guides/using-monitoring-intf)
tab of the Dataflow web interface.

To ensure that the recommendations are valid, Dataflow waits for resource
utilization to stabilize before sending recommendations to workers. For example,
memory and CPU utilization might be in the range for scaling, but because
resource utilization is still growing, Dataflow doesn't send
a recommendation. After
resource utilization stabilizes, Dataflow sends a recommendation.

If an out of memory (OOM) error occurs, thread scaling is automatically
disabled, and the pipeline runs with one thread per vCPU.

## Enable dynamic thread scaling

To enable dynamic thread scaling, use the
following
[Dataflow service option](/dataflow/docs/reference/service-options).

### Java

```
--dataflowServiceOptions=enable_dynamic_thread_scaling
```

### Python

```
--dataflow_service_options=enable_dynamic_thread_scaling
```

### Go

```
--dataflow_service_options=enable_dynamic_thread_scaling
```

When dynamic thread scaling is enabled, you can also set the initial and
maximum number of workers available to your pipeline during execution. For more
information, see
[Pipeline options](/dataflow/docs/reference/pipeline-options).

### Verify that dynamic thread scaling is enabled

When dynamic thread scaling is enabled, the following message appears in your
[worker log files](/dataflow/docs/guides/logging#MonitoringLogs):

```
Enabling thread vertical scaling feature in worker.
```

To see your worker log files, in the
[Logs Explorer](/logging/docs/view/logs-explorer-interface),
use the
[**Query** pane](/logging/docs/view/building-queries#query-builder-menus)
to filter the logs by **Log name**. Use the following log name in your filter:

```
projects/PROJECT_ID/logs/dataflow.googleapis.com%2Fharness
```

You can see the recommended number of threads in the worker log files. The
following message includes the recommended number of threads:

```
worker_thread_scaling_report_response { recommended_thread_count: NUMBER }
```

If resource utilization isn't in the [range for scaling](#how-it-works), the
value displayed equals the number of vCPUs on the worker.

You can also use the Google Cloud console to see whether dynamic thread scaling is
enabled. When it's enabled, on the Dataflow **Job info** panel,
in the **dataflowServiceOptions** row of the
**Pipeline options** section, `enable_dynamic_thread_scaling` displays.

## Troubleshooting

This section provides instructions for troubleshooting common issues related to
dynamic thread scaling.

### Performance degrades with dynamic thread scaling enabled

Increasing the thread count might cause performance issues in the following
cases:

- When multiple processes are trying to use the same resource, one
  process is able to use the resource while others must wait. This situation
  is known as _resource contention_. When resource contention occurs,
  pipeline performance might decline.
- When out of memory errors occur, dynamic thread scaling is disabled. In
  some cases, out of memory errors might cause the pipeline to fail.

Verify whether thread count has increased. For information about how to
verify the recommended thread count, see
[Verify that thread scaling is enabled](#verify) on this page.

If thread scaling is enabled, to resolve this issue, when you run your
pipeline, don't include the dynamic thread scaling service option.

### Unified worker … both enabled and disabled

After you enable dynamic thread scaling, your job might fail with the following
error:

```
The workflow could not be created. Causes: (ID): Unified worker misconfigured by user and was both enabled and disabled.
```

This error occurs when Runner v2 is explicitly disabled.

To resolve this issue, enable Runner v2. For more information, see the
[Enable Dataflow Runner v2](/dataflow/docs/runner-v2#enable)
section in the "Use Dataflow Runner V2" page.

### Upgrade your SDK

After you enable dynamic thread scaling, your job might fail with the following
error:

### Java

```
Dataflow Runner v2 requires the Apache Beam Java SDK version 2.29.0 or higher. Please upgrade your SDK and resubmit your job.
```

### Python

```
Dataflow Runner v2 requires the Apache Beam SDK, version 2.21.0 or higher. Please upgrade your SDK and resubmit your job.
```

This error occurs when Runner v2 can't be enabled because the SDK version
doesn't support it.

To resolve this issue, use an SDK version that supports Runner v2.

### Thread vertical scaling feature can not be enabled

After you enable dynamic thread scaling, your job might fail with the following
error:

```
The workflow could not be created. Causes: (ID): Thread vertical scaling feature can not be enabled while number_of_worker_harness_threads is specified.
```

This error occurs when the pipeline explicitly sets the number of threads per
worker by using the `numberOfWorkerHarnessThreads` or
`number_of_worker_harness_threads`
[pipeline option](/dataflow/docs/reference/pipeline-options#resource_utilization).

To resolve this issue, remove the `numberOfWorkerHarnessThreads` or
`number_of_worker_harness_threads` pipeline option from your pipeline.
