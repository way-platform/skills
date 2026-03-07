---
source_url: https://beam.apache.org/documentation/runners/flink/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Apache Flink Runner"
beam_last_updated: "Last updated on 2026/03/06"
---

# Overview

The Apache Flink Runner can be used to execute Beam pipelines using [Apache
Flink](https://flink.apache.org). For execution you can choose between a cluster
execution mode (e.g. Yarn/Kubernetes/Mesos) or a local embedded execution mode
which is useful for testing pipelines.

The Flink Runner and Flink are suitable for large scale, continuous jobs, and provide:

- A streaming-first runtime that supports both batch processing and data streaming programs
- A runtime that supports very high throughput and low event latency at the same time
- Fault-tolerance with _exactly-once_ processing guarantees
- Natural back-pressure in streaming programs
- Custom memory management for efficient and robust switching between in-memory and out-of-core data processing algorithms
- Integration with YARN and other components of the Apache Hadoop ecosystem

# Using the Apache Flink Runner

It is important to understand that the Flink Runner comes in two flavors:

1. The original _classic Runner_ which supports only Java (and other JVM-based languages)
2. The newer _portable Runner_ which supports Java/Python/Go

You may ask why there are two Runners?

Beam and its Runners originally only supported JVM-based languages
(e.g. Java/Scala/Kotlin). Python and Go SDKs were added later on. The
architecture of the Runners had to be changed significantly to support executing
pipelines written in other languages.

If your applications only use Java, then you should currently go with the classic
Runner. Eventually, the portable Runner will replace the classic Runner because
it contains the generalized framework for executing Java, Python, Go, and more
languages in the future.

If you want to run Python pipelines with Beam on Flink you want to use the
portable Runner. For more information on
portability, please visit the [Portability page](/roadmap/portability/).

Consequently, this guide is split into parts to document the classic and
the portable functionality of the Flink Runner.
In addition, Python provides convenience wrappers to handle the full lifecycle of the runner,
and so is further split depending on whether to manage the portability
components automatically (recommended) or manually.
Please use the switcher below to select the appropriate mode for the Runner:

## Prerequisites and Setup

If you want to use the local execution mode with the Flink Runner you don’t have
to complete any cluster setup. You can simply run your Beam pipeline. Be sure to
set the Runner to `FlinkRunner`.

To use the Flink Runner for executing on a cluster, you have to setup a Flink cluster by following the
Flink [Setup Quickstart](https://ci.apache.org/projects/flink/flink-docs-stable/quickstart/setup_quickstart.html#setup-download-and-start-flink).

### Dependencies

You will need Docker to be installed in your execution environment.
To run an embedded flink cluster or use the Flink runner for Python < 3.6
you will also need to have java available in your execution environment.

### Executing a Beam pipeline on a Flink Cluster

To run a pipeline on Flink, set the runner to `FlinkRunner`
and `flink_master` to the master URL of a Flink cluster.
In addition, optionally set `environment_type` set to `LOOPBACK`. For example,
after starting up a [local flink cluster](https://ci.apache.org/projects/flink/flink-docs-release-1.18/getting-started/tutorials/local_setup.html),
one could run:

![](/images/copy-icon.svg)

```
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

options = PipelineOptions([
    "--runner=FlinkRunner",
    "--flink_master=localhost:8081",
    "--environment_type=LOOPBACK"
])
with beam.Pipeline(options) as p:
    ...
```

To run on an embedded Flink cluster, simply omit the `flink_master` option
and an embedded Flink cluster will be automatically started and shut down for the job.

The optional `flink_version` option may be required as well for older versions of Python.

Note that `environment_type=LOOPBACK` is only intended for local testing,
and will not work on remote clusters.
See [here](/documentation/runtime/sdk-harness-config/) for details.

## Additional information and caveats

### Monitoring your job

You can monitor a running Flink job using the Flink JobManager Dashboard or its Rest interfaces. By default, this is available at port `8081` of the JobManager node. If you have a Flink installation on your local machine that would be `http://localhost:8081`. Note: When you use the `[local]` mode an embedded Flink cluster will be started which does not make a dashboard available.

### Streaming Execution

If your pipeline uses an unbounded data source or sink, the Flink Runner will automatically switch to streaming mode. You can enforce streaming mode by using the `--streaming` flag.

Note: The Runner will print a warning message when unbounded sources are used and checkpointing is not enabled.
Many sources like `PubSubIO` rely on their checkpoints to be acknowledged which can only be done when checkpointing is enabled for the `FlinkRunner`. To enable checkpointing, please set `checkpointing_interval` to the desired checkpointing interval in milliseconds.

## Pipeline options for the Flink Runner

When executing your pipeline with the Flink Runner, you can set these pipeline options.

The following list of Flink-specific pipeline options is generated automatically from the
[FlinkPipelineOptions](https://beam.apache.org/releases/javadoc/2.71.0/index.html?org/apache/beam/runners/flink/FlinkPipelineOptions.html)
reference class:

|                                                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                                 |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| `allow_non_restored_state`                        | Flag indicating whether non restored state is allowed if the savepoint contains state for an operator that is no longer part of the pipeline.                                                                                                                                                                                                                                                                                                                                                                                                                                   | Default: `false`                |
| `attached_mode`                                   | Specifies if the pipeline is submitted in attached or detached mode                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Default: `true`                 |
| `auto_balance_write_files_sharding_enabled`       | Flag indicating whether auto-balance sharding for WriteFiles transform should be enabled. This might prove useful in streaming use-case, where pipeline needs to write quite many events into files, typically divided into N shards. Default behavior on Flink would be, that some workers will receive more shards to take care of than others. This cause workers to go out of balance in terms of processing backlog and memory usage. Enabling this feature will make shards to be spread evenly among available workers in improve throughput and memory usage stability. | Default: `false`                |
| `auto_watermark_interval`                         | The interval in milliseconds for automatic watermark emission.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |                                 |
| `checkpoint_timeout_millis`                       | The maximum time in milliseconds that a checkpoint may take before being discarded.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Default: `-1`                   |
| `checkpointing_interval`                          | The interval in milliseconds at which to trigger checkpoints of the running pipeline. Default: No checkpointing.                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Default: `-1`                   |
| `checkpointing_mode`                              | The checkpointing mode that defines consistency guarantee.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Default: `EXACTLY_ONCE`         |
| `disable_metrics`                                 | Disable Beam metrics in Flink Runner                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Default: `false`                |
| `enable_stable_input_drain`                       | Allow drain operation for flink pipelines that contain RequiresStableInput operator. Note that at time of draining,the RequiresStableInput contract might be violated if there any processing related failures in the DoFn operator.                                                                                                                                                                                                                                                                                                                                            | Default: `false`                |
| `execution_mode_for_batch`                        | Flink mode for data exchange of batch pipelines. Reference {@link org.apache.flink.api.common.ExecutionMode}. Set this to BATCH_FORCED if pipelines get blocked, see https://issues.apache.org/jira/browse/FLINK-10672.                                                                                                                                                                                                                                                                                                                                                         | Default: `PIPELINED`            |
| `execution_retry_delay`                           | Sets the delay in milliseconds between executions. A value of {@code -1} indicates that the default value should be used.                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Default: `-1`                   |
| `externalized_checkpoints_enabled`                | Enables or disables externalized checkpoints. Works in conjunction with CheckpointingInterval                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Default: `false`                |
| `faster_copy`                                     | Remove unneeded deep copy between operators. See https://issues.apache.org/jira/browse/BEAM-11146                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Default: `false`                |
| `file_input_split_max_size_m_b`                   | Set the maximum size of input split when data is read from a filesystem. 0 implies no max size.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Default: `0`                    |
| `finish_bundle_before_checkpointing`              | If set, finishes the current bundle and flushes all output before checkpointing the state of the operators. By default, starts checkpointing immediately and buffers any remaining bundle output as part of the checkpoint. The setting may affect the checkpoint alignment.                                                                                                                                                                                                                                                                                                    | Default: `false`                |
| `flink_conf_dir`                                  | Directory containing Flink YAML configuration files. These properties will be set to all jobs submitted to Flink and take precedence over configurations in FLINK_CONF_DIR.                                                                                                                                                                                                                                                                                                                                                                                                     |                                 |
| `flink_master`                                    | Address of the Flink Master where the Pipeline should be executed. Can either be of the form "host:port" or one of the special values [local], [collection] or [auto].                                                                                                                                                                                                                                                                                                                                                                                                          | Default: `[auto]`               |
| `force_slot_sharing_group`                        | Set a slot sharing group for all bounded sources. This is required when using Datastream to have the same scheduling behaviour as the Dataset API.                                                                                                                                                                                                                                                                                                                                                                                                                              | Default: `true`                 |
| `force_unaligned_checkpoint_enabled`              | Forces unaligned checkpoints, particularly allowing them for iterative jobs.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Default: `false`                |
| `job_check_interval_in_secs`                      | Set job check interval in seconds under detached mode in method waitUntilFinish, by default it is 5 seconds                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Default: `5`                    |
| `latency_tracking_interval`                       | Interval in milliseconds for sending latency tracking marks from the sources to the sinks. Interval value <= 0 disables the feature.                                                                                                                                                                                                                                                                                                                                                                                                                                            | Default: `0`                    |
| `max_bundle_size`                                 | The maximum number of elements in a bundle. Default values are 1000 for a streaming job and 1,000,000 for batch                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Default: `MaxBundleSizeFactory` |
| `max_bundle_time_mills`                           | The maximum time to wait before finalising a bundle (in milliseconds). Default values are 1000 for streaming and 10,000 for batch.                                                                                                                                                                                                                                                                                                                                                                                                                                              | Default: `MaxBundleTimeFactory` |
| `max_parallelism`                                 | The pipeline wide maximum degree of parallelism to be used. The maximum parallelism specifies the upper limit for dynamic scaling and the number of key groups used for partitioned state.                                                                                                                                                                                                                                                                                                                                                                                      | Default: `-1`                   |
| `min_pause_between_checkpoints`                   | The minimal pause in milliseconds before the next checkpoint is triggered.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Default: `-1`                   |
| `num_concurrent_checkpoints`                      | The maximum number of concurrent checkpoints. Defaults to 1 (=no concurrent checkpoints).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Default: `1`                    |
| `number_of_execution_retries`                     | Sets the number of times that failed tasks are re-executed. A value of zero effectively disables fault tolerance. A value of -1 indicates that the system default value (as defined in the configuration) should be used.                                                                                                                                                                                                                                                                                                                                                       | Default: `-1`                   |
| `object_reuse`                                    | Sets the behavior of reusing objects.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Default: `false`                |
| `operator_chaining`                               | Sets the behavior of operator chaining.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Default: `true`                 |
| `parallelism`                                     | The degree of parallelism to be used when distributing operations onto workers. If the parallelism is not set, the configured Flink default is used, or 1 if none can be found.                                                                                                                                                                                                                                                                                                                                                                                                 | Default: `-1`                   |
| `report_checkpoint_duration`                      | If not null, reports the checkpoint duration of each ParDo stage in the provided metric namespace.                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                 |
| `retain_externalized_checkpoints_on_cancellation` | Sets the behavior of externalized checkpoints on cancellation.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Default: `false`                |
| `savepoint_path`                                  | Savepoint restore path. If specified, restores the streaming pipeline from the provided path.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                 |
| `shutdown_sources_after_idle_ms`                  | Shuts down sources which have been idle for the configured time of milliseconds. Once a source has been shut down, checkpointing is not possible anymore. Shutting down the sources eventually leads to pipeline shutdown (=Flink job finishes) once all input has been processed. Unless explicitly set, this will default to Long.MAX_VALUE when checkpointing is enabled and to 0 when checkpointing is disabled. See https://issues.apache.org/jira/browse/FLINK-2491 for progress on this issue.                                                                           | Default: `-1`                   |
| `state_backend`                                   | State backend to store Beam's state. Use 'rocksdb' or 'hashmap' (same as 'filesystem').                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                                 |
| `state_backend_factory`                           | Sets the state backend factory to use in streaming mode. Defaults to the flink cluster's state.backend configuration.                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                                 |
| `state_backend_storage_path`                      | State backend path to persist state backend data. Used to initialize state backend.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                 |
| `tolerable_checkpoint_failure_number`             | Sets the expected behaviour for tasks in case that they encounter an error in their checkpointing procedure. To tolerate a specific number of failures, set it to a positive number.                                                                                                                                                                                                                                                                                                                                                                                            | Default: `0`                    |
| `unaligned_checkpoint_enabled`                    | If set, Unaligned checkpoints contain in-flight data (i.e., data stored in buffers) as part of the checkpoint state, allowing checkpoint barriers to overtake these buffers. Thus, the checkpoint duration becomes independent of the current throughput as checkpoint barriers are effectively not embedded into the stream of data anymore                                                                                                                                                                                                                                    | Default: `false`                |

For general Beam pipeline options see the
[PipelineOptions](https://beam.apache.org/releases/javadoc/2.71.0/index.html?org/apache/beam/sdk/options/PipelineOptions.html)
reference.

## Flink Version Compatibility

The Flink cluster version has to match the minor version used by the FlinkRunner.
The minor version is the first two numbers in the version string, e.g. in `1.18.0` the
minor version is `1.18`.

We try to track the latest version of Apache Flink at the time of the Beam release.
A Flink version is supported by Beam for the time it is supported by the Flink community.
The Flink community supports the last two minor versions. When support for a Flink version is dropped, it may be deprecated and removed also from Beam.
To find out which version of Flink is compatible with Beam please see the table below:

| Flink Version         | Artifact Id             | Supported Beam Versions |
| --------------------- | ----------------------- | ----------------------- |
| 1.19.x                | beam-runners-flink-1.19 | ≥ 2.61.0                |
| 1.18.x                | beam-runners-flink-1.18 | ≥ 2.57.0                |
| 1.17.x                | beam-runners-flink-1.17 | ≥ 2.56.0                |
| 1.16.x                | beam-runners-flink-1.16 | 2.47.0 - 2.60.0         |
| 1.15.x                | beam-runners-flink-1.15 | 2.40.0 - 2.60.0         |
| 1.14.x                | beam-runners-flink-1.14 | 2.38.0 - 2.56.0         |
| 1.13.x                | beam-runners-flink-1.13 | 2.31.0 - 2.55.0         |
| 1.12.x                | beam-runners-flink-1.12 | 2.27.0 - 2.55.0         |
| 1.11.x                | beam-runners-flink-1.11 | 2.25.0 - 2.38.0         |
| 1.10.x                | beam-runners-flink-1.10 | 2.21.0 - 2.30.0         |
| 1.9.x                 | beam-runners-flink-1.9  | 2.17.0 - 2.29.0         |
| 1.8.x                 | beam-runners-flink-1.8  | 2.13.0 - 2.29.0         |
| 1.7.x                 | beam-runners-flink-1.7  | 2.10.0 - 2.20.0         |
| 1.6.x                 | beam-runners-flink-1.6  | 2.10.0 - 2.16.0         |
| 1.5.x                 | beam-runners-flink_2.11 | 2.6.0 - 2.16.0          |
| 1.4.x with Scala 2.11 | beam-runners-flink_2.11 | 2.3.0 - 2.5.0           |
| 1.3.x with Scala 2.10 | beam-runners-flink_2.10 | 2.1.x - 2.2.0           |
| 1.2.x with Scala 2.10 | beam-runners-flink_2.10 | 2.0.0                   |

For retrieving the right Flink version, see the [Flink downloads page](https://flink.apache.org/downloads.html).

For more information, the [Flink Documentation](https://ci.apache.org/projects/flink/flink-docs-stable/) can be helpful.

## Beam Capability

The [Beam Capability Matrix](/documentation/runners/capability-matrix/) documents the
capabilities of the classic Flink Runner.

The [Portable Capability
Matrix](https://s.apache.org/apache-beam-portability-support-table) documents
the capabilities of the portable Flink Runner.
