---
source_url: https://docs.cloud.google.com/dataflow/docs/horizontal-autoscaling
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Horizontal Autoscaling \u00a0|\u00a0 Cloud Dataflow \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

Horizontal Autoscaling enables Dataflow to choose the appropriate
number of worker instances for your job, adding or removing workers as needed.
Dataflow scales based on the average CPU utilization of the
workers and on the parallelism of a pipeline. The parallelism of a pipeline is
an estimate of the number of threads needed to most efficiently process data at
any given time.

Horizontal Autoscaling is supported in both batch and streaming pipelines.

## Batch autoscaling

Horizontal Autoscaling is enabled by default on all batch pipelines.
Dataflow automatically chooses the number of workers based on the
estimated total amount of work in each stage of your pipeline. This estimate
depends on the input size and the current throughput. Every 30 seconds,
Dataflow re-evaluates the amount of work according to the
execution progress. As the estimated total amount of work increases or
decreases, Dataflow dynamically scales the number of workers up or
down.

The number of workers is sublinear to the amount of work. For example, a job
with twice the work has fewer than twice the workers.

If any of the following conditions occur, Dataflow either
maintains or decreases the number of workers, in order to save idle resources:

- The average worker CPU usage is lower than 5%.
- Parallelism is limited due to unparallelizable work, such as un-splittable
  data caused by compressed files or I/O modules that don't split.
- The degree of parallelism is fixed, for example when writing to existing
  files in Cloud Storage.

To set an upper bound on the number of workers, set the
[`--maxNumWorkers` pipeline option](/dataflow/docs/reference/pipeline-options).
The default value is `2,000`.
To set a lower bound on the number of workers, set the
[`--dataflow-service-options=min_num_workers` service option](/dataflow/docs/reference/service-options).
These flags are optional.

## Streaming autoscaling

For streaming jobs, Horizontal Autoscaling allows Dataflow to
adaptively change the number of workers in response to changes in load and
resource utilization.

Horizontal Autoscaling is enabled by default for streaming jobs that use
[Streaming Engine](/dataflow/docs/streaming-engine).
To enable Horizontal Autoscaling for streaming jobs that don't use
Streaming Engine, set the following
[pipeline options](/dataflow/docs/reference/pipeline-options) when you start
your pipeline:

### Java

```
--autoscalingAlgorithm=THROUGHPUT_BASED
--maxNumWorkers=MAX_WORKERS
```

Replace MAX_WORKERS with the maximum number of worker
instances.

### Python

```
--autoscaling_algorithm=THROUGHPUT_BASED
--max_num_workers=MAX_WORKERS
```

Replace MAX_WORKERS with the maximum number of worker
instances.

### Go

```
--autoscaling_algorithm=THROUGHPUT_BASED
--max_num_workers=MAX_WORKERS
```

Replace MAX_WORKERS with the maximum number of worker
instances.

To set a lower bound on the number of workers, set the
[`--dataflow-service-options=min_num_workers` service option](/dataflow/docs/reference/service-options).
When you set this value, horizontal autoscaling doesn't scale below the number
of workers specified. This flag is optional.

While a streaming job is running, you can update the minimum and maximum workers
by using an
[in-flight job update](/dataflow/docs/guides/updating-a-pipeline#in-flight-updates).
To adjust the settings, set the `min-num-workers` and `max-num-workers` flags.
For more information, see
[Update the autoscaling range](/dataflow/docs/guides/tune-horizontal-autoscaling#update-range).

## Disable Horizontal Autoscaling

To disable Horizontal Autoscaling, set the following
[pipeline option](/dataflow/docs/reference/pipeline-options) when you run
the job.

### Java

```
--autoscalingAlgorithm=NONE
```

If you disable Horizontal Autoscaling, then Dataflow sets
the number of workers based on the `--numWorkers` option.

### Python

```
--autoscaling_algorithm=NONE
```

If you disable Horizontal Autoscaling, then Dataflow sets
the number of workers based on the `--num_workers` option.

### Go

```
--autoscaling_algorithm=NONE
```

If you disable Horizontal Autoscaling, then Dataflow sets
the number of workers based on the `--num_workers` option.

## Custom sources

If you create a custom data source, you can potentially improve performance by
implementing methods that provide more information to the Horizontal Autoscaling
algorithm:

### Java

#### Bounded sources

- In your `BoundedSource` subclass, implement the method `getEstimatedSizeBytes`.
  The Dataflow service uses `getEstimatedSizeBytes` when calculating
  the initial number of workers to use for your pipeline.
- In your `BoundedReader` subclass, implement the method `getFractionConsumed`.
  The Dataflow service uses `getFractionConsumed` to track read
  progress and converge on the correct number of workers to use during a read.

#### Unbounded sources

The source must inform the Dataflow service about backlog.
Backlog is an estimate of the input in bytes that has not yet been processed
by the source. To inform the service about backlog, implement either one of
the following methods in your `UnboundedReader` class.

- `getSplitBacklogBytes()` - Backlog for the current split of the source. The
  service aggregates backlog across all the splits.
- `getTotalBacklogBytes()` - The global backlog across all the splits. In
  some cases the backlog is not available for each split and can only be
  calculated across all the splits. Only the first split (split ID '0') needs
  to provide total backlog.

The Apache Beam repository contains several
[examples](https://github.com/apache/beam/blob/master/sdks/java/io/kafka/src/main/java/org/apache/beam/sdk/io/kafka/KafkaUnboundedReader.java)
of custom sources that implement the `UnboundedReader` class.

### Python

#### Bounded sources

- In your `BoundedSource` subclass, implement the method `estimate_size`. The
  Dataflow service uses `estimate_size` when calculating the
  initial number of workers to use for your pipeline.
- In your `RangeTracker` subclass, implement the method `fraction_consumed`.
  The Dataflow service uses `fraction_consumed` to track read
  progress and converge on the correct number of workers to use during a read.

### Go

#### Bounded sources

- In your `RangeTracker`, implement the method `GetProgress()`. The
  Dataflow service uses `GetProgress` to track read progress and
  converge on the correct number of workers to use during a read.

## Limitations

- In jobs running Dataflow Prime, Horizontal Autoscaling is deactivated
  during and up to 10 minutes after Vertical Autoscaling. For more information,
  see [Effect on Horizontal Autoscaling](/dataflow/docs/vertical-autoscaling#horizontal-autoscaling).
- For pipelines not using
  [Dataflow Shuffle](/dataflow/docs/shuffle-for-batch),
  Dataflow might not be able to scale down the workers effectively
  because the workers might have shuffled data stored in local disks.
- The
  [PeriodicImpulse](https://beam.apache.org/releases/javadoc/current/org/apache/beam/sdk/transforms/PeriodicImpulse.html)
  transform is supported with streaming autoscaling in the Apache Beam SDK versions 2.60.0 and later. If your pipeline uses
  `PeriodicImpulse` with an earlier SDK version, then Dataflow workers don't scale down as
  expected.

## What's next

- [Tune Horizontal Autoscaling for streaming pipelines](/dataflow/docs/guides/tune-horizontal-autoscaling)
- [Monitor Dataflow autoscaling](/dataflow/docs/guides/autoscaling-metrics)
- [Troubleshoot Dataflow autoscaling](/dataflow/docs/guides/troubleshoot-autoscaling)
