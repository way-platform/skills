---
source_url: https://beam.apache.org/documentation/runners/spark/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Apache Spark Runner"
beam_last_updated: "Last updated on 2026/03/06"
---

# Using the Apache Spark Runner

The Apache Spark Runner can be used to execute Beam pipelines using [Apache Spark](https://spark.apache.org/).
The Spark Runner can execute Spark pipelines just like a native Spark application; deploying a self-contained application for local mode, running on Spark’s Standalone RM, or using YARN or Mesos.

The Spark Runner executes Beam pipelines on top of Apache Spark, providing:

- Batch and streaming (and combined) pipelines.
- The same fault-tolerance [guarantees](https://spark.apache.org/docs/latest/streaming-programming-guide.html#fault-tolerance-semantics) as provided by RDDs and DStreams.
- The same [security](https://spark.apache.org/docs/latest/security.html) features Spark provides.
- Built-in metrics reporting using Spark’s metrics system, which reports Beam Aggregators as well.
- Native support for Beam side-inputs via spark’s Broadcast variables.

The [Beam Capability Matrix](/documentation/runners/capability-matrix/) documents the currently supported capabilities of the Spark Runner.

## Three flavors of the Spark runner

The Spark runner comes in three flavors:

1. A _legacy Runner_ which supports only Java (and other JVM-based languages) and that is based on Spark RDD/DStream
2. An _Structured Streaming Spark Runner_ which supports only Java (and other JVM-based languages) and that is based on Spark Datasets and the [Apache Spark Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html) framework.

> **Note:** It is still experimental, its coverage of the Beam model is partial. As for now it only supports batch mode.

3. A _portable Runner_ which supports Java, Python, and Go

This guide is split into two parts to document the non-portable and
the portable functionality of the Spark Runner. Please use the switcher below to
select the appropriate Runner:

## Which runner to use: portable or non portable runner?

Beam and its Runners originally only supported JVM-based languages
(e.g. Java/Scala/Kotlin). Python and Go SDKs were added later on. The
architecture of the Runners had to be changed significantly to support executing
pipelines written in other languages.

If your applications only use Java, then you should currently go with one of the java based runners.
If you want to run Python or Go pipelines with Beam on Spark, you need to use
the portable Runner. For more information on portability, please visit the
[Portability page](/roadmap/portability/).

## Spark Runner prerequisites and setup

The Spark runner currently supports Spark’s 3.2.x branch.

> **Note:** Support for Spark 2.4.x was dropped with Beam 2.46.0.

### Deploying Spark with your application

You will need Docker to be installed in your execution environment. To develop
Apache Beam with Python you have to install the Apache Beam Python SDK: `pip install apache_beam`. Please refer to the [Python documentation](/documentation/sdks/python/)
on how to create a Python pipeline.

![](/images/copy-icon.svg)

```
pip install apache_beam
```

Starting from Beam 2.20.0, pre-built Spark Job Service Docker images are available at
[Docker Hub](https://hub.docker.com/r/apache/beam_spark_job_server).

For older Beam versions, you will need a copy of Apache Beam’s source code. You can
download it on the [Downloads page](/get-started/downloads/).

1. Start the JobService endpoint:
   - with Docker (preferred): `docker run --net=host apache/beam_spark_job_server:latest`
   - or from Beam source code: `./gradlew :runners:spark:3:job-server:runShadow`

The JobService is the central instance where you submit your Beam pipeline.
The JobService will create a Spark job for the pipeline and execute the
job. To execute the job on a Spark cluster, the Beam JobService needs to be
provided with the Spark master address.

2. Submit the Python pipeline to the above endpoint by using the `PortableRunner`, `job_endpoint` set to `localhost:8099` (this is the default address of the JobService), and `environment_type` set to `LOOPBACK`. For example:

![](/images/copy-icon.svg)

```
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

options = PipelineOptions([
    "--runner=PortableRunner",
    "--job_endpoint=localhost:8099",
    "--environment_type=LOOPBACK"
])
with beam.Pipeline(options) as p:
    ...
```

### Running on a pre-deployed Spark cluster

Deploying your Beam pipeline on a cluster that already has a Spark deployment (Spark classes are available in container classpath) does not require any additional dependencies.
For more details on the different deployment modes see: [Standalone](https://spark.apache.org/docs/latest/spark-standalone.html), [YARN](https://spark.apache.org/docs/latest/running-on-yarn.html), or [Mesos](https://spark.apache.org/docs/latest/running-on-mesos.html).

1. Start a Spark cluster which exposes the master on port 7077 by default.

2. Start JobService that will connect with the Spark master:
   - with Docker (preferred): `docker run --net=host apache/beam_spark_job_server:latest --spark-master-url=spark://localhost:7077`
   - or from Beam source code: `./gradlew :runners:spark:3:job-server:runShadow -PsparkMasterUrl=spark://localhost:7077`

3. Submit the pipeline as above.
   Note however that `environment_type=LOOPBACK` is only intended for local testing.
   See [here](/roadmap/portability/#sdk-harness-config) for details.

(Note that, depending on your cluster setup, you may need to change the `environment_type` option.
See [here](/roadmap/portability/#sdk-harness-config) for details.)

### Running on Dataproc cluster (YARN backed)

To run Beam jobs written in Python, Go, and other supported languages, you can use the `SparkRunner` and `PortableRunner` as described on the Beam’s [Spark Runner](https://beam.apache.org/documentation/runners/spark/) page (also see [Portability Framework Roadmap](https://beam.apache.org/roadmap/portability/)).

The following example runs a portable Beam job in Python from the Dataproc cluster’s master node with Yarn backed.

> Note: This example executes successfully with Dataproc 2.0, Spark 3.1.2 and Beam 2.37.0.

1. Create a Dataproc cluster with [Docker](https://cloud.google.com/dataproc/docs/concepts/components/docker) component enabled.

```
gcloud dataproc clusters create CLUSTER_NAME \
    --optional-components=DOCKER \
    --image-version=DATAPROC_IMAGE_VERSION \
    --region=REGION \
    --enable-component-gateway \
    --scopes=https://www.googleapis.com/auth/cloud-platform \
    --properties spark:spark.master.rest.enabled=true
```

- `--optional-components`: Docker.
- `--image-version`: the [cluster’s image version](https://cloud.google.com/dataproc/docs/concepts/versioning/dataproc-versions#supported_cloud_dataproc_versions), which determines the Spark version installed on the cluster (for example, see the Apache Spark component versions listed for the latest and previous four [2.0.x image release versions](https://cloud.google.com/dataproc/docs/concepts/versioning/dataproc-release-2.0)).
- `--region`: a supported Dataproc [region](https://cloud.google.com/dataproc/docs/concepts/regional-endpoints#regional_endpoint_semantics).
- `--enable-component-gateway`: enable access to [web interfaces](https://cloud.google.com/dataproc/docs/concepts/accessing/dataproc-gateways).
- `--scopes`: enable API access to GCP services in the same project.
- `--properties`: add specific configuration for some component, here spark.master.rest is enabled to use job submit to the cluster.

2. Create a Cloud Storage bucket.

```
gsutil mb BUCKET_NAME
```

3. Install the necessary Python libraries for the job in your local environment.

```
python -m pip install apache-beam[gcp]==BEAM_VERSION
```

4. Bundle the word count example pipeline along with all dependencies, artifacts, etc. required to run the pipeline into a jar that can be executed later.

```
python -m apache_beam.examples.wordcount \
    --runner=SparkRunner \
    --output_executable_path=OUTPUT_JAR_PATH \
    --output=gs://BUCKET_NAME/python-wordcount-out \
    --spark_version=3
```

- `--runner`(required): `SparkRunner`.
- `--output_executable_path`(required): path for the bundle jar to be created.
- `--output`(required): where output shall be written.
- `--spark_version`(optional): select spark version 3 (default) or 2 (deprecated!).

5. Submit spark job to Dataproc cluster’s master node.

```
gcloud dataproc jobs submit spark \
        --cluster=CLUSTER_NAME \
        --region=REGION \
        --class=org.apache.beam.runners.spark.SparkPipelineRunner \
        --jars=OUTPUT_JAR_PATH
```

- `--cluster`: name of created Dataproc cluster.
- `--region`: a supported Dataproc [region](https://cloud.google.com/dataproc/docs/concepts/regional-endpoints#regional_endpoint_semantics).
- `--class`: the entry point for your application.
- `--jars`: path to the bundled jar including your application and all dependencies.

6. Check that the results were written to your bucket.

```
gsutil cat gs://BUCKET_NAME/python-wordcount-out-SHARD_ID
```

## Pipeline options for the Spark Runner

When executing your pipeline with the Spark Runner, you should consider the following pipeline options.

| Field            | Description                                                                                     | Value                                                              |
| ---------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `--runner`       | The pipeline runner to use. This option allows you to determine the pipeline runner at runtime. | Set to `PortableRunner` to run using Spark.                        |
| `--job_endpoint` | Job service endpoint to use. Should be in the form hostname:port, e.g. localhost:3000           | Set to match your job service endpoint (localhost:8099 by default) |

## Additional notes

### Using spark-submit

When submitting a Spark application to cluster, it is common (and recommended) to use the `spark-submit` script that is provided with the spark installation.
The `PipelineOptions` described above are not to replace `spark-submit`, but to complement it.
Passing any of the above mentioned options could be done as one of the `application-arguments`, and setting `–master` takes precedence.
For more on how to generally use `spark-submit` checkout Spark [documentation](https://spark.apache.org/docs/latest/submitting-applications.html#launching-applications-with-spark-submit).

### Monitoring your job

You can monitor a running Spark job using the Spark [Web Interfaces](https://spark.apache.org/docs/latest/monitoring.html#web-interfaces). By default, this is available at port `4040` on the driver node. If you run Spark on your local machine that would be `http://localhost:4040`.
Spark also has a history server to [view after the fact](https://spark.apache.org/docs/latest/monitoring.html#viewing-after-the-fact).

Spark metrics are not yet supported on the portable runner.

### Streaming Execution

Streaming is not yet supported on the Spark portable runner.

### Using a provided SparkContext and StreamingListeners

Provided SparkContext and StreamingListeners are not supported on the Spark portable runner.

### Kubernetes

#### Submit beam job without job server

To submit a beam job directly on spark kubernetes cluster without spinning up an extra job server, you can do:

```
spark-submit --master MASTER_URL \
  --conf spark.kubernetes.driver.podTemplateFile=driver_pod_template.yaml \
  --conf spark.kubernetes.executor.podTemplateFile=executor_pod_template.yaml \
  --class org.apache.beam.runners.spark.SparkPipelineRunner \
  --conf spark.kubernetes.container.image=apache/spark:v3.3.2 \
  ./wc_job.jar
```

Similar to run the beam job on Dataproc, you can bundle the job jar like below. The example use the `PROCESS` type of [SDK harness](https://beam.apache.org/documentation/runtime/sdk-harness-config/) to execute the job by processes.

```
python -m beam_example_wc \
    --runner=SparkRunner \
    --output_executable_path=./wc_job.jar \
    --environment_type=PROCESS \
    --environment_config='{\"command\": \"/opt/apache/beam/boot\"}' \
    --spark_version=3
```

And below is an example of kubernetes executor pod template, the `initContainer` is required to download the beam SDK harness to run the beam pipelines.

```
spec:
  containers:
    - name: spark-kubernetes-executor
      volumeMounts:
      - name: beam-data
        mountPath: /opt/apache/beam/
  initContainers:
  - name: init-beam
    image: apache/beam_python3.7_sdk
    command:
    - cp
    - /opt/apache/beam/boot
    - /init-container/data/boot
    volumeMounts:
    - name: beam-data
      mountPath: /init-container/data
  volumes:
  - name: beam-data
    emptyDir: {}
```

#### Submit beam job with job server

An [example](https://github.com/cometta/python-apache-beam-spark) of configuring Spark to run Apache beam job with a job server.
