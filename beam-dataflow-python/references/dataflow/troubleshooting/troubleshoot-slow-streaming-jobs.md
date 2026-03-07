---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/troubleshoot-slow-streaming-jobs
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Troubleshoot slow or stuck streaming jobs \u00a0|\u00a0 Cloud Dataflow \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

This page explains how to troubleshoot common causes of slow or stuck
Dataflow streaming jobs.

If you notice the following symptoms, your Dataflow streaming job
might be running slowly or stuck:

- The pipeline isn't reading data from the source. For example, Pub/Sub has a growing backlog.
- The pipeline isn't writing data to the sink.
- The [data freshness metric](/dataflow/docs/guides/using-monitoring-intf#data_freshness_streaming) is increasing.
- The [system latency metric](/dataflow/docs/guides/using-monitoring-intf#system_latency_streaming) is increasing.

Use the information in the following sections to identify and diagnose the problem.

## Identify the root cause

1. Check the
   [data freshness](/dataflow/docs/guides/using-monitoring-intf#data_freshness_streaming)
   and [backlog bytes](/dataflow/docs/guides/using-monitoring-intf#backlog)
   metrics.
   - If both metrics are monotonically increasing, it means the pipeline is stuck
     and not progressing.
   - If data freshness is increasing, but backlog bytes remains normal, it means
     that one or more work items are stuck in the pipeline.

   Look for the stages where these metrics are increasing, to identify any stage
   with problems and the operations performed in that stage.

2. Check the
   [Parallel processing chart](/dataflow/docs/guides/using-monitoring-intf#parallelism)
   to see if any stage is stuck due to excessive or insufficient parallelism. See
   [Troubleshoot parallelism](#insufficient-parallelism).
3. Check the [job logs](/dataflow/docs/guides/logging#log-types) for issues
   such as quota limits, stockout issues, or IP address exhaustion.
4. Check the worker logs for warnings and errors.
   - If worker logs contain errors, view the stack trace. Investigate whether
     the error is caused by a bug in your code.
   - Look for Dataflow errors. See
     [Troubleshoot Dataflow errors](/dataflow/docs/guides/common-errors).
   - Look for errors that show the job exceeded a limit, such as the maximum
     Pub/Sub message size.
   - Look for out-of-memory errors, which can cause a stuck pipeline. If you
     see out-of-memory errors, follow the steps in
     [Troubleshoot Dataflow out of memory errors](/dataflow/docs/guides/troubleshoot-oom).
   - To identify a slow or stuck step, check the worker logs for
     `Operation ongoing` messages. View the stack trace to see where the step is
     spending time. For more information, see
     [Processing stuck or operation ongoing](/dataflow/docs/guides/common-errors#processing-stuck).

5. If a work item is stuck on a specific worker, restart that worker VM.
6. If you aren't using Streaming Engine, check the
   [shuffler logs](/dataflow/docs/guides/logging#log-types) for warnings and
   errors. If you see an
   [RPC timeout error](/dataflow/docs/guides/troubleshoot-networking#worker-communicate-firewall-ports)
   on port 12345 or 12346, your job might be missing a firewall rule. See
   [Firewall rules for Dataflow](/dataflow/docs/guides/routes-firewall#firewall_rules).
7. [Check for hot keys](#hot-keys).
8. If Runner v2 is enabled, check the
   [harness logs](/dataflow/docs/guides/logging#log-types) for errors. For more
   information, see
   [Troubleshoot Runner v2](/dataflow/docs/runner-v2#debugging).

## Investigate repeated failures

In a streaming job, some failures are retried indefinitely. These retries
prevent the pipeline from progressing. To identify repeated failures, check
the worker logs for exceptions.

- If the exception is with user code, debug and fix the issue in the code or
  in the data.
- To prevent unexpected failures from stalling your pipeline,
  implement a dead-letter queue. For an example implementation, see
  [BigQuery patterns](https://beam.apache.org/documentation/patterns/bigqueryio/)
  in the Apache Beam documentation.
- If the exception is an out of memory (OOM) error, see
  [Troubleshoot Dataflow out of memory errors](/dataflow/docs/guides/troubleshoot-oom).
- For other exceptions, see
  [Troubleshoot Dataflow errors](/dataflow/docs/guides/common-errors).

## Identify unhealthy workers

If the workers processing the streaming job are unhealthy, the job might be slow or appear stuck. To identify unhealthy workers:

- Check for memory pressure by using the
  [memory utilization metrics](/dataflow/docs/guides/using-monitoring-intf#memory-use)
  and by looking for out of memory errors in the worker logs. For more information, see
  [Troubleshoot Dataflow out of memory errors](/dataflow/docs/guides/troubleshoot-oom).
- If you're using Streaming Engine, use the
  [persistence metrics](/dataflow/docs/guides/using-monitoring-intf#persistence_streaming)
  to identify bottlenecks with the disk input/output operations (IOPS).
- Check the worker logs for other errors. For more information, see
  [Work with pipeline logs](/dataflow/docs/guides/logging) and
  [Troubleshoot Dataflow errors](/dataflow/docs/guides/common-errors).

## Identify stragglers

A straggler is a work item that is slow relative to other work items in the
stage. For information about identifying and fixing stragglers, see
[Troubleshoot stragglers in streaming jobs](/dataflow/docs/guides/troubleshoot-streaming-stragglers).

## Troubleshoot parallelism

For scalability and efficiency, Dataflow runs the stages of your
pipeline in parallel across multiple workers. The smallest unit of parallel
processing in Dataflow is a key. Incoming messages for each fused
stage are associated with a key. The key is defined in one of the following ways:

- The key is implicitly defined by the properties of the source, such as Kafka partitions.
- The key is explicitly defined by aggregation logic in the pipeline, such as `GroupByKey`.

In Dataflow, worker threads are responsible for handling the processing of
bundles of work (messages) for a key. The number of available threads to process the job's keys is
equal to `num_of_workers * threads_per_worker`. The per worker [thread count](/dataflow/docs/guides/troubleshoot-oom#dofn)
is determined based on the SDK (Java, Python, or Go) and the job type (batch or streaming).

If the pipeline doesn't have enough keys for a given stage, it limits parallel
processing. That stage might become a bottleneck.

If the pipeline uses a very large number of keys for a given stage, it can limit
the throughput of the stage and accumulate backlog in the upstream stages,
because there is some overhead per key. Overhead might include the backend
communicating to workers, externals RPCs to a sink such as BigQuery,
and other processing. For example, if processing a key with one message takes
100ms, it might also take about 100ms to process 1000 messages in that key
bundle.

### Identify stages with low parallelism

To identify if pipeline slowness is caused by low parallelism, view the
[CPU utilization metrics](/dataflow/docs/guides/using-monitoring-intf#cpu-use).
If CPU is low but evenly distributed across workers, your job might have
insufficient parallelism. If your job is using Streaming Engine, to see if a
stage has low parallelism, in the **Job Metrics** tab, view the
[parallelism metrics](/dataflow/docs/guides/using-monitoring-intf#parallelism).
To mitigate this issue:

- In the Google Cloud console, on the **Job info** page, use the
  [Autoscaling tab](/dataflow/docs/guides/autoscaling-metrics) to
  see if the job is having problems scaling up. If autoscaling is the
  problem, see
  [Troubleshoot Dataflow autoscaling](/dataflow/docs/guides/troubleshoot-autoscaling).
- Use the [job graph](/dataflow/docs/guides/job-graph) to check the steps in
  the stage. If the stage is reading from a source or
  writing to a sink, review the documentation for the service of the source or
  sink. Use the documentation to determine if that service is
  configured for sufficient scalability.
  - To gather more information, use the
    [input and output metrics](/dataflow/docs/guides/using-monitoring-intf#input-output)
    provided by Dataflow.
  - If you're using Kafka, check the number of Kafka partitions. For more
    information, see the [Apache Kafka](https://kafka.apache.org/)
    documentation.
  - If you're using a BigQuery sink, enable automatic sharding to improve
    parallelism. For more information, see
    [3x Dataflow Throughput with Auto Sharding for BigQuery](https://cloud.google.com/blog/products/data-analytics/3x-dataflow-throughput-auto-sharding-bigquery).

### Identify stages with high parallelism

A combination of low system latency, growing data freshness, and increasing
backlog and underutilized worker CPUs suggests that the pipeline is being
throttled due to a large number of keys. Check the
[parallel processing](/dataflow/docs/guides/using-monitoring-intf#parallelism)
chart to identify stages with a large number of keys.

Transforms such as [`Reshuffle`](https://beam.apache.org/releases/javadoc/current/org/apache/beam/sdk/transforms/Reshuffle.html)
can generate millions of keys if you don't explicitly specify
[`withNumBuckets`](<https://javadoc.io/doc/org.apache.beam/beam-sdks-java-core/latest/org/apache/beam/sdk/transforms/Reshuffle.ViaRandomKey.html#withNumBuckets(java.lang.Integer)>).
Large numbers of keys can lead to the creation of numerous smaller work bundles,
each of which requires a dedicated worker thread to process. Because the
available worker threads are limited, it can lead to a significant backlog of
processing keys, causing delays as they wait for resources. As a result, the
worker threads are not efficiently used.

We recommend limiting the number of keys by setting the `withNumBuckets` option
in the `Reshuffle` transform. The value shouldn't exceed the total number of
threads across all the workers. Targeting `(threads_per_worker * max_workers)`
keys in the pipeline might not be optimal. Sometimes fewer keys and larger
bundles are possible, and are processed more efficiently by Dataflow
due to using fewer workers. A smaller number of keys creates larger work
bundles, which efficiently uses the worker threads and increases the throughput
of the stage.

If there are multiple `Reshuffle` steps in the pipeline, divide the total number
of threads by the count of `Reshuffle` steps to calculate `withNumBuckets`.

### Check for hot keys

If tasks are unevenly distributed across workers and worker utilization is
very uneven, your pipeline might have a hot key. A hot key is a key that is
overrepresented in the data.

Check to see if your pipeline has hot-keys by looking at the Bottleneck status
for the slow step. You might have hot keys if the bottleneck reason is "Hot keys
or insufficient key parallelism." For general information about bottlenecks, see
[Troubleshoot bottlenecks](/dataflow/docs/guides/troubleshoot-bottlenecks)

You can print the specific key by running your pipeline with
`--hotKeyLoggingEnabled=true`.

Then, check for hot keys by using the following log filter:

```
  resource.type="dataflow_step"
  resource.labels.job_id=JOB_ID
  jsonPayload.logger="org.apache.beam.runners.dataflow.worker.HotKeyLogger"
```

Replace JOB_ID with the ID of your job.

To resolve this issue, take one or more of the following steps:

- Rekey your data. To output new key-value pairs, apply a `ParDo` transform.
  For more information, see the
  [Java `ParDo` transform page](https://beam.apache.org/documentation/transforms/java/elementwise/pardo/)
  or the
  [Python `ParDo` transform page](https://beam.apache.org/documentation/transforms/python/elementwise/pardo/)
  in the Apache Beam documentation.
- Use `.withFanout` in your combine transforms. For more information, see the
  [`Combine.PerKey`](https://beam.apache.org/releases/javadoc/current/org/apache/beam/sdk/transforms/Combine.PerKey.html)
  class in the Java SDK or the
  [`with_hot_key_fanout`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.CombinePerKey.with_hot_key_fanout)
  operation in the Python SDK.
- If you have a Java pipeline that processes
  high-volume unbounded `PCollections`, we recommend that you do the following:
  - Use `Combine.Globally.withFanout` instead of `Combine.Globally`.
  - Use `Combine.PerKey.withHotKeyFanout` instead of `Count.PerKey`.

## Check for insufficient quota

Make sure you have sufficient quota for your source and sink. For example, if
your pipeline reads input from Pub/Sub or BigQuery, your Google Cloud Platform project
might have insufficient quota. For more information about quota limits for these
services, see
[Pub/Sub quota](/pubsub/quotas) or [BigQuery quota](/bigquery/quotas).

If your job is generating a high number of `429 (Rate Limit Exceeded)` errors, it
might have insufficient quota. To check for errors, try the
following steps:

1. Go to the [Google Cloud console](https://console.cloud.google.com/).
2. In the navigation pane, click **APIs & services**.
3. In the menu, click **Library**.
4. Use the search box to search for **Pub/Sub**.
5. Click **Cloud Pub/Sub API**.
6. Click **Manage**.
7. In the **Traffic by response code** chart, look for `(4xx)` client error codes.

You can also use [Metrics Explorer](/monitoring/charts/metrics-explorer) to
check quota usage. If your pipeline uses a BigQuery source or sink, to
troubleshoot quota issues, use the
[BigQuery Storage API metrics](/monitoring/api/metrics_gcp_a_b#gcp-bigquerystorage).
For example, to create a chart showing the BigQuery concurrent connection count,
follow these steps:

1. In the Google Cloud console, select **Monitoring**:

   [Go to Monitoring](https://console.cloud.google.com/monitoring)

2. In the navigation pane, select **Metrics explorer**.
3. In the **Select a metric** pane, for **Metric**, filter to
   **BigQuery Project** > **Write** > **concurrent connection count**.

For instructions about viewing Pub/Sub metrics, see
[Monitor quota usage](/pubsub/docs/monitoring#quota) in "Monitor Pub/Sub in
Cloud Monitoring." For instructions about viewing BigQuery metrics, see
[View quota usage and limits](/bigquery/docs/monitoring-dashboard#view_quota_usage_and_limits)
in "Create dashboards, charts, and alerts."

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
