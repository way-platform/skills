---
source_url: https://docs.cloud.google.com/dataflow/docs/optimize-costs
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Best practices for Dataflow cost optimization \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

This document explains best practices for optimizing your
Dataflow jobs with the goal of minimizing costs. It explains
factors that impact costs and provides techniques for monitoring and managing
those costs.

For more information about how costs are calculated for Dataflow
jobs, see [Dataflow pricing](https://cloud.google.com/dataflow/pricing).

Several factors can have a large impact on job cost:

- Runtime settings
- Pipeline performance
- Pipeline throughput requirements

The following sections provide details about how to monitor your jobs, factors
that impact job cost, and suggestions for how to improve pipeline efficiency.

## Define SLOs

Before you start to optimize, define your pipeline's service level objectives
(SLOs), especially for throughput and latency. These requirements will help you
to reason about tradeoffs between cost and other factors.

- If your pipeline requires low end-to-end ingest latency, pipeline costs might
  be higher.
- If you need to process late arriving data, the overall pipeline cost might be
  higher.
- If your streaming pipeline has data spikes that need to be processed, the
  pipeline might need extra capacity, which can increase costs.

## Monitor jobs

To determine how to optimize your job, you first need to understand its
behavior. Use the Dataflow monitoring tools to observe your
pipeline as it runs. Then use this information to improve performance and
efficiency.

### Cost monitoring

Use the following techniques to predict and monitor costs.

- Before running the pipeline in production, run one or more smaller jobs on a
  subset of your data. For many pipelines, this technique can provide a cost
  estimate.
- Use the **Cost** page in the Dataflow monitoring interface to
  monitor the estimated cost of your jobs. The estimated cost might not reflect
  the actual job cost for various reasons, such as contractual discounts, but it
  can provide a good baseline for cost optimization. For more information, see
  [Cost monitoring](/dataflow/docs/guides/monitoring-overview#cost).
- [Export Cloud Billing data to BigQuery](/billing/docs/how-to/export-data-bigquery)
  and perform a cost analysis on the billing export tables. Cloud Billing
  export lets you export detailed Google Cloud Platform billing data automatically
  throughout the day to a BigQuery dataset. Billing data includes
  usage, cost estimates, and pricing data.
- To avoid unexpected costs, create monitoring alerts when your
  Dataflow job exceeds a threshold that you define. For more
  information, see
  [Use Cloud Monitoring for Dataflow pipelines](/dataflow/docs/guides/using-cloud-monitoring).

### Job monitoring

Monitor your jobs and identify areas where you might be able to improve pipeline
efficiency.

- Use the Dataflow
  [job monitoring interface](/dataflow/docs/guides/monitoring-overview) to
  identify problems in your pipelines. The monitoring interface shows a
  [job graph](/dataflow/docs/guides/job-graph) and
  [execution details](/dataflow/docs/concepts/execution-details) for each
  pipeline. Both of these tools can help you to understand your pipeline and
  identify slow stages, stuck stages, or steps with too much
  [wall time](/dataflow/docs/guides/step-info-panel#wall-time).
- Use [Metrics Explorer](/dataflow/docs/guides/using-cloud-monitoring#metrics-explorer)
  to see detailed Dataflow job metrics. You can use custom
  metrics to capture performance data. The `Distribution` metric is
  particularly useful for gathering performance data.
- For CPU-intensive pipelines, use
  [Cloud Profiler](/dataflow/docs/guides/profiling-a-pipeline) to identify
  the parts of the pipeline code consuming the most resources.
- Use [data sampling](/dataflow/docs/guides/data-sampling) to identify problems
  with your data. Data sampling lets you observe the data at each step of a
  Dataflow pipeline. By showing the actual inputs and outputs in
  a running or completed job, this information can help you to debug problems
  with your pipeline.
- Customize the
  [project monitoring dashboard](/dataflow/docs/guides/project-monitoring) to
  show potentially expensive jobs. For more information, see
  [Customize the Dataflow monitoring dashboard](/dataflow/docs/guides/customize-monitoring-dashboard).

It's not recommended to log per-element processing metrics in high-volume
pipelines, because logging is subject to
[limits](/dataflow/docs/guides/logging#LogLimits), and excessive logging can
degrade job performance.

## Optimize runtime settings

The following runtime settings can affect cost:

- Whether you run a streaming job or a batch job
- What service you use to run the job, such as Streaming Engine or FlexRS
- The machine type, disk size, and number of GPUs in the worker VMs
- The autoscaling mode
- The initial number of workers and the maximum number of workers
- The streaming mode (exactly-once mode or at-least-once mode)

This section describes potential changes that you can make to optimize your job.
To determine whether these suggestions are appropriate for your workload,
consider your pipeline design and requirements. Not all suggestions are
appropriate or helpful for all pipelines.

Before making any large-scale changes, test changes on small pipelines that use
a subset of your data. For more information, see
[Run small experiments for large jobs](/dataflow/docs/guides/large-pipeline-best-practices#small-experiments)
in "Best practices for large batch pipelines."

### Job location

Most Dataflow jobs interact with other services such as data
stores and messaging systems. Consider where these are located.

- Run your job in the same region as the resources that your job uses.
- Create your Cloud Storage bucket for storing staging and temporary job
  files in the same region as your job. For more information, see the
  `gcpTempLocation` and `temp_location`
  [pipeline options](/dataflow/docs/reference/pipeline-options#basic_options).

### Adjust machine types

The following adjustments to worker VMs might improve cost efficiency.

- Run your job with the smallest machine type required. Adjust the machine type
  as needed based on the pipeline requirements. For example, streaming jobs with
  CPU-intensive pipelines sometimes benefit from changing the machine type from
  the default. For more information, see
  [Machine type](/dataflow/docs/guides/configure-worker-vm#machine-type).
- For memory-intensive or compute-intensive workloads, use appropriate machine
  types. For more information, see
  [CoreMark scores of VMs by family](/compute/docs/coremark-scores-of-vm-instances).
- Set the initial number of workers. When a job scales up, work has to be
  redistributed to the new VMs. If you know how many workers your jobs needs,
  you might avoid this cost by setting the initial number of workers. To set
  the initial number of workers, use the `numWorkers` or `num_workers`
  [pipeline option](/dataflow/docs/reference/pipeline-options#resource_utilization).
- Set the maximum number of workers. By setting a value for this
  parameter, you can potentially limit the total cost of your job. When you
  first test the pipeline, start with a relatively low maximum. Then increase
  the value until it's high enough to run a production workload. Consider your
  pipeline SLOs before setting a maximum. For more information, see
  [Horizontal Autoscaling](/dataflow/docs/horizontal-autoscaling).
- Use [right fitting](/dataflow/docs/guides/right-fitting) to customize the
  resource requirements for specific pipeline steps.
- Some pipelines benefit from using GPUs. For more information, see
  [GPUs with Dataflow](/dataflow/docs/gpu). By using right
  fitting, you can configure GPUs for specific steps of the pipeline.
- Make sure you have enough [network bandwidth](/compute/docs/network-bandwidth)
  to access data from your worker VMs, particularly when you need to access
  on-premise data.

### Optimize settings for batch jobs

This section provides suggestions for optimizing runtime settings for batch
jobs. For batch jobs, the job stages execute sequentially, which can affect
performance and cost.

#### Use Flexible Resource Scheduling

If your batch job is not time sensitive, consider using
[Flexible Resource Scheduling](/dataflow/docs/guides/flexrs) (FlexRS). FlexRS
reduces batch processing costs by finding the best time to start the job, and
then using a combination of
[preemptible VM](/compute/docs/instances/preemptible) instances and standard
VMs. Preemptible VMs are available at much lower price compared to standard VMs,
which can lower the total cost. By using a combination of preemptable and
standard VMs, FlexRS helps to ensure that your pipeline makes progress even if
Compute Engine preempts the preemptible VMs.

#### Avoid running very small jobs

When feasible, avoid running jobs that process very small amounts of data. If
possible, run fewer jobs on larger datasets. Starting and stopping worker VMs
incurs a cost, so running fewer jobs on more data can improve efficiency.

Make sure that
[Dataflow Shuffle](/dataflow/docs/shuffle-for-batch) is enabled.
Batch jobs use Dataflow shuffle by default.

#### Adjust autoscaling settings

By default, batch jobs use autoscaling. For some jobs, such as short-running
jobs, autoscaling isn't needed. If you think that your pipeline doesn't benefit
from autoscaling, turn it off. For more information, see
[Horizontal Autoscaling](/dataflow/docs/horizontal-autoscaling).

You can also use
[dynamic thread scaling](/dataflow/docs/guides/thread-scaling) to let
Dataflow tune the thread count based on CPU utilization.
Alternately, if you know the optimal number of threads for the job, explicitly
set the number of threads per worker by using the
`numberOfWorkerHarnessThreads` or `number_of_worker_harness_threads`
[pipeline option](/dataflow/docs/reference/pipeline-options#resource_utilization).

#### Stop long-running jobs

Set your jobs to automatically stop if they exceed a predetermined run time. If
you know approximately how long your job takes to run, use the
`max_workflow_runtime_walltime_seconds`
[service option](/dataflow/docs/reference/pipeline-options#resource_utilization)
to automatically stop the job if it runs longer than expected.

### Optimize settings for streaming jobs

This section provides suggestions for optimizing runtime settings for streaming
jobs.

#### Use Streaming Engine

[Streaming Engine](/dataflow/docs/streaming-engine) moves pipeline execution
from the worker VMs and into the Dataflow service backend for
greater efficiency. It's recommended to use Streaming Engine for your streaming
jobs.

#### Consider at-least-once mode

Dataflow supports two modes for streaming jobs: exactly-once
mode and at-least-once mode. If your workload can tolerate duplicate records,
then at-least-once mode can significantly reduce the cost of your job. Before
you enable at-least-once mode, evaluate whether your pipeline requires
[exactly-once processing](/dataflow/docs/concepts/exactly-once) of records.
For more information, see
[Set the pipeline streaming mode](/dataflow/docs/guides/streaming-modes).

#### Choose your pricing model

[Committed use discounts](/dataflow/docs/cuds) (CUDs) for
Dataflow streaming jobs provide discounted prices in exchange
for your commitment to continuously use a certain amount of
Dataflow compute resources for a year or longer.
Dataflow CUDs are useful when your spending on
Dataflow compute capacity for streaming jobs involves a
predictable minimum that you can commit to for at least a year. By using CUDs,
you can potentially reduce the cost of your Dataflow jobs.

Also consider using
[resource-based billing](/dataflow/docs/streaming-engine#compute-unit-pricing).
With resource-based billing, the Streaming Engine resources consumed by your
job are metered and measured in
[Streaming Engine Compute Units](https://cloud.google.com/dataflow/pricing#streaming-compute-units).
You're billed for worker CPU, worker memory, and Streaming Engine Compute Units.

#### Adjust autoscaling settings

Use autoscaling hints to tune your autoscaling settings. For more information,
see [Tune Horizontal Autoscaling for streaming pipelines](/dataflow/docs/guides/tune-horizontal-autoscaling).
For streaming jobs that use Streaming Engine, you can update the autotuning
settings without stopping or replacing the job. For more information, see
[In-flight job option update](/dataflow/docs/guides/updating-a-pipeline#in-flight-updates).

If you think that your pipeline doesn't benefit from autoscaling, turn it off.
For more information, see
[Horizontal Autoscaling](/dataflow/docs/horizontal-autoscaling).

If you know the optimal number of threads for the job, explicitly set the
number of threads per worker by using the `numberOfWorkerHarnessThreads` or
`number_of_worker_harness_threads`
[pipeline option](/dataflow/docs/reference/pipeline-options#resource_utilization).

#### Stop long-running jobs

For streaming jobs, Dataflow retries failed work items
indefinitely. The job is not terminated. However, the job might stall until the
issue is resolved. Create
[monitoring policies](/dataflow/docs/guides/using-cloud-monitoring) to detect
signs of a stalled pipeline, such as an increase in system latency and a
decrease in
[data freshness](/dataflow/docs/guides/using-monitoring-intf#data_freshness_streaming).
Implement error logging in your pipeline code to help identify work items that
fail repeatedly.

- To monitor pipeline errors, see [Worker error log count](/dataflow/docs/guides/using-monitoring-intf#worker-error-logs).
- To troubleshoot errors, see [Troubleshoot Dataflow errors](/dataflow/docs/guides/common-errors).

## Pipeline performance

Pipelines that run faster might cost less. The following factors can affect
pipeline performance:

- The parallelism available to your job
- The efficiency of the transforms, I/O connectors, and coders used in the
  pipeline
- The data location

The first step to improving pipeline performance is to understand the processing
model:

- Learn about the
  [Apache Beam model](https://beam.apache.org/documentation/basics/) and the
  [Apache Beam execution model](https://beam.apache.org/documentation/runtime/model/).
- Learn more about the [pipeline lifecycle](/dataflow/docs/pipeline-lifecycle),
  including how Dataflow manages parallelization and the
  optimization strategies it uses. Dataflow jobs use multiple
  worker VMs, and each worker runs multiple threads. Element bundles from a
  `PCollection` are distributed to each worker thread.

Use these best practices when you write your pipeline code:

- When possible, use the latest supported
  [Apache Beam SDK version](/dataflow/docs/support/sdk-version-support-status).
  Follow the [release notes](/dataflow/docs/resources/release-notes-apache-beam)
  to understand the changes in different versions.
- Follow [best practices for writing pipeline code](/dataflow/docs/guides/pipeline-best-practices#write-beam-code).
- Follow [I/O connector best practices](/dataflow/docs/guides/io-connector-best-practices).
- For Python pipelines, consider using
  [custom containers](/dataflow/docs/guides/using-custom-containers).
  Pre-packaging dependencies decreases worker start-up time.

### Logging

Follow these best practices when logging:

- Excessive logging can hurt performance.
- To reduce the volume of logs, consider changing the
  [pipeline log level](/dataflow/docs/guides/logging#SettingLevels). For more
  information, see
  [Control log volume](/dataflow/docs/guides/logging#LogControls).
- Don't log individual elements. Enable
  [data sampling](/dataflow/docs/guides/data-sampling) instead.
- Use a
  [dead letter pattern](/dataflow/docs/guides/pipeline-best-practices#dead-letter-queues)
  for per-element errors, instead of logging each error.

### Testing

Testing your pipeline has many benefits, including helping with SDK upgrades,
pipeline refactoring, and code reviews. Many optimizations, such as reworking
custom CPU-intensive transforms, can be tested locally without needing to run a
job on Dataflow.

Test large scale pipelines with realistic test data for your workload, including
the total number of elements for batch pipelines, the number of elements per
second for streaming pipelines, the element size, and the number of keys. Test
your pipelines in two modes: in a steady state, and processing a large backlog
to simulate a crash recovery.

For more information about creating unit tests, integration tests, and
end-to-end tests, see
[Test your pipeline](/dataflow/docs/guides/develop-and-test-pipelines#test-your-pipeline).
For examples of tests, see the
[`dataflow-ordered-processing`](https://github.com/GoogleCloudPlatform/dataflow-ordered-processing)
GitHub repository.

## What's next

- [Plan your Dataflow pipeline](/dataflow/docs/guides/plan-pipelines)
- [Develop and test Dataflow pipelines](/dataflow/docs/guides/develop-and-test-pipelines)
- [Troubleshoot pipelines](/dataflow/docs/guides/troubleshooting-your-pipeline)
