---
source_url: https://beam.apache.org/documentation/runners/samza/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Apache Samza Runner"
beam_last_updated: "Last updated on 2026/03/06"
---

# Using the Apache Samza Runner

**Note** Samza runner is deprecated and the support is planned to be removed in Beam 3.0 ([Issue](https://github.com/apache/beam/issues/35448)).

The Apache Samza Runner can be used to execute Beam pipelines using [Apache Samza](https://samza.apache.org/). The Samza Runner executes Beam pipeline in a Samza application and can run locally. The application can further be built into a .tgz file, and deployed to a YARN cluster or Samza standalone cluster with Zookeeper.

The Samza Runner and Samza are suitable for large scale, stateful streaming jobs, and provide:

- First class support for local state (with RocksDB store). This allows fast state access for high frequency streaming jobs.
- Fault-tolerance with support for incremental checkpointing of state instead of full snapshots. This enables Samza to scale to applications with very large state.
- A fully asynchronous processing engine that makes remote calls efficient.
- Flexible deployment model for running the applications in any hosting environment with Zookeeper.
- Features like canaries, upgrades and rollbacks that support extremely large deployments with minimal downtime.

The [Beam Capability Matrix](/documentation/runners/capability-matrix/) documents the currently supported capabilities of the Samza Runner.

## Samza Runner prerequisites and setup

The Samza Runner is built on Samza version greater than 1.0.

### Specify your dependency

## Executing a pipeline with Samza Runner

If you run your pipeline locally or deploy it to a standalone cluster with all the jars and resource files, no packaging is required. For example, the following command runs the WordCount example:

```
$ mvn exec:java -Dexec.mainClass=org.apache.beam.examples.WordCount \
    -Psamza-runner \
    -Dexec.args="--runner=SamzaRunner \
      --inputFile=/path/to/input \
      --output=/path/to/counts"
```

To deploy your pipeline to a YARN cluster, here is the [instructions](https://samza.apache.org/startup/hello-samza/latest/) of deploying a sample Samza job. First you need to package your application jars and resource files into a `.tgz` archive file, and make it available to download for Yarn containers. In your config, you need to specify the URI of this TGZ file location:

```
yarn.package.path=${your_job_tgz_URI}

job.name=${your_job_name}
job.factory.class=org.apache.samza.job.yarn.YarnJobFactory
job.coordinator.system=${job_coordinator_system}
job.default.system=${job_default_system}
```

For more details on the configuration, see [Samza Configuration Reference](https://samza.apache.org/learn/documentation/latest/jobs/configuration-table.html).

The config file will be passed in by setting the command line arg `--configFilePath=/path/to/config.properties`. With that, you can run your main class of Beam pipeline in a Yarn Resource Manager, and the Samza Runner will submit a Yarn job under the hood.

Check out our [Samza Beam example from Github](https://github.com/apache/samza-beam-examples)

## Pipeline options for the Samza Runner

When executing your pipeline with the Samza Runner, you can use the following pipeline options.

| Field                       | Description                                                                                     | Default Value                                                  |
| --------------------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `runner`                    | The pipeline runner to use. This option allows you to determine the pipeline runner at runtime. | Set to `SamzaRunner` to run using Samza.                       |
| `configFilePath`            | The config for Samza using a properties file.                                                   | `empty`, i.e. use local execution.                             |
| `configFactory`             | The factory to read config file from config file path.                                          | `PropertiesConfigFactory`, reading configs as a property file. |
| `configOverride`            | The config override to set programmatically.                                                    | `empty`, i.e. use config file or local execution.              |
| `jobInstance`               | The instance name of the job.                                                                   | `1`                                                            |
| `samzaExecutionEnvironment` | Samza application execution environment. See `SamzaExecutionEnvironment` for more details.      | `LOCAL`                                                        |
| `watermarkInterval`         | The interval to check for watermarks in milliseconds.                                           | `1000`                                                         |
| `systemBufferSize`          | The maximum number of messages to buffer for a given system.                                    | `5000`                                                         |
| `eventTimerBufferSize`      | The maximum number of event-time timers to buffer in memory for a PTransform                    | `5000`                                                         |
| `maxSourceParallelism`      | The maximum parallelism allowed for any data source.                                            | `1`                                                            |
| `storeBatchGetSize`         | The batch get size limit for the state store.                                                   | `10000`                                                        |
| `enableMetrics`             | Enable/disable Beam metrics in Samza Runner.                                                    | `true`                                                         |
| `stateDurable`              | The config for state to be durable.                                                             | `false`                                                        |
| `maxBundleSize`             | The maximum number of elements in a bundle.                                                     | `1` (by default the auto bundling is disabled)                 |
| `maxBundleTimeMs`           | The maximum time to wait before finalising a bundle (in milliseconds)..                         | `1000`                                                         |

## Monitoring your job

You can monitor your pipeline job using metrics emitted from both Beam and Samza, e.g. Beam source metrics such as `elements_read` and `backlog_elements`, and Samza job metrics such as `job-healthy` and `process-envelopes`. A complete list of Samza metrics is in [Samza Metrics Reference](https://samza.apache.org/learn/documentation/latest/container/metrics-table.html). You can view your job’s metrics via JMX in development, and send the metrics to graphing system such as [Graphite](https://graphiteapp.org/). For more details, please see [Samza Metrics](https://samza.apache.org/learn/documentation/latest/container/metrics.html).

For a running Samza YARN job, you can use YARN web UI to monitor the job status and check logs.
