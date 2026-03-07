---
source_url: https://docs.cloud.google.com/dataflow/docs/streaming-engine
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Use Streaming Engine for streaming jobs \u00a0|\u00a0 Cloud Dataflow \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

Dataflow's Streaming Engine
moves pipeline execution out of the worker virtual machines (VMs) and into the
Dataflow service backend. When you don't use Streaming Engine
for streaming jobs, the Dataflow runner executes the steps of your
streaming pipeline entirely on worker VMs, consuming worker CPU,
memory, and Persistent Disk storage.

Streaming Engine is enabled by default for the following pipelines:

- Streaming pipelines that use the Apache Beam Python SDK version 2.21.0 or later
  and Python 3.
- Streaming pipelines that use the Apache Beam Go SDK version 2.33.0 or later.

To learn more about the implementation of Streaming Engine, see
[Streaming Engine: Execution Model for Highly-Scalable, Low-Latency Data Processing](https://medium.com/google-cloud/streaming-engine-execution-model-1eb2eef69a8e).

## Benefits

The Streaming Engine model has the following benefits:

- Reduced CPU, memory, and Persistent Disk storage resource usage
  on the worker VMs. Streaming Engine works best with smaller worker machine
  types (`n1-standard-2` instead of `n1-standard-4`). It doesn't require
  Persistent Disk beyond a small worker boot disk, leading to less resource
  and quota consumption.
- More responsive [Horizontal Autoscaling](/dataflow/docs/horizontal-autoscaling)
  in response to variations in incoming data volume. Streaming Engine offers
  smoother, more granular scaling of workers.
- Improved supportability, because you don't need to redeploy your pipelines to
  apply service updates.

Most of the reduction in worker resources comes from offloading the work to the
Dataflow service. For that reason, there is a
[charge](https://cloud.google.com/dataflow/pricing) associated with the use of
Streaming Engine.

## Support and limitations

- For the Java SDK, Streaming Engine requires the Apache Beam SDK version 2.10.0
  or later.
- For the Python SDK, Streaming Engine requires the Apache Beam SDK version
  2.16.0 or later.
- For the Go SDK, Streaming Engine requires the Apache Beam SDK version
  2.33.0 or later.
- You can't [update pipelines](/dataflow/docs/guides/updating-a-pipeline)
  that are already running to use Streaming Engine.
  If your pipeline is running in production without Streaming Engine and you want to use
  Streaming Engine, stop your pipeline by using the Dataflow
  [Drain](/dataflow/docs/guides/stopping-a-pipeline#drain) option. Then, specify
  the Streaming Engine parameter, and rerun your pipeline.
- For jobs that use Streaming Engine, the aggregated input data
  for the open windows has a limit of 60 GB per key.
  Aggregated input data includes both
  [buffered elements](https://beam.apache.org/documentation/programming-guide/#window-accumulation-modes)
  and [custom state](https://beam.apache.org/documentation/programming-guide/#state-and-timers).
  When a pipeline exceeds this limit, the pipeline becomes stuck
  with high system lag, and a message in the job log indicates that the limit has been exceeded.
  As a best practice, avoid pipeline designs that result in large keys. For
  more information, see
  [Writing Dataflow pipelines with scalability in mind](https://cloud.google.com/blog/products/gcp/writing-dataflow-pipelines-with-scalability-in-mind).
- Supports [customer-managed encryption keys (CMEK)](/dataflow/docs/guides/customer-managed-encryption-keys)

## Use Streaming Engine

This feature is available in all regions where Dataflow is supported. To see available locations, read [Dataflow locations](/dataflow/docs/resources/locations).

### Java

Streaming Engine requires the Apache Beam Java SDK version 2.10.0
or later.

To use Streaming Engine for your streaming pipelines, specify the following
parameter:

- `--enableStreamingEngine` if you're using Apache Beam SDK for Java
  versions 2.11.0 or later.
- `--experiments=enable_streaming_engine` if you're using Apache Beam SDK
  for Java version 2.10.0.

If you use Dataflow Streaming Engine for your pipeline, don't
specify the `--zone` parameter. Instead, specify the `--region` parameter and
set the value to a [supported region](/dataflow/docs/resources/locations).
Dataflow auto-selects the zone in the region you
specified. If you do specify the `--zone` parameter and set it to a zone
outside of the available regions, Dataflow reports an error.

Streaming Engine works best with smaller core worker machine types. Use the
job type to determine whether to use a high memory worker machine type.
Example machine types that we recommend include `--workerMachineType=n1-standard-2`
and `--workerMachineType=n1-highmem-2`. You can also set `--diskSizeGb=30`
because Streaming Engine only needs space for the worker boot image and local
logs. These values are the default values.

### Python

Streaming Engine requires the Apache Beam Python SDK version
2.16.0 or later.

Streaming Engine is enabled by default for new Dataflow streaming
pipelines when the following conditions are met:

- Pipelines use the Apache Beam Python SDK version 2.21.0
  or later and Python 3.
- [Customer-managed encryption keys](/dataflow/docs/guides/customer-managed-encryption-keys)
  are not used.
- Dataflow workers are in the same
  [region](/dataflow/docs/concepts/regional-endpoints) as your
  Dataflow job.

In Python SDK version 2.45.0 or later, you cannot disable Streaming Engine
for streaming pipelines. In Python SDK version 2.44.0 or earlier, to disable
Streaming Engine, specify the following parameter:

`--experiments=disable_streaming_engine`

If you use Python 2, to enable Streaming Engine, specify the
following parameter:

`--enable_streaming_engine`

**Caution:** As of October 7, 2020, Dataflow no longer supports
pipelines that use Python 2. Read more information about
[Python 2 support on Google Cloud Platform](https://cloud.google.com/python/docs/python2-sunset#dataflow).

If you use Dataflow Streaming Engine in your pipeline, don't
specify the `--zone` parameter. Instead, specify the `--region` parameter and
set the value to a [supported region](/dataflow/docs/resources/locations).
Dataflow auto-selects the zone in the region you
specified. If you specify the `--zone` parameter and set it to a zone
outside of the available regions, Dataflow reports an error.

Streaming Engine works best with smaller core worker machine types. Use the
job type to determine whether to use a high memory worker machine type.
Example machine types that we recommend include `--workerMachineType=n1-standard-2`
and `--workerMachineType=n1-highmem-2`. You can also set `--disk_size_gb=30`
because Streaming Engine only needs space for the worker boot image and local
logs. These values are the default values.

### Go

Streaming Engine requires the Apache Beam Go SDK version
2.33.0 or later.

Streaming Engine is enabled by default for new Dataflow streaming
pipelines that use the Apache Beam Go SDK.

If you want to disable Streaming Engine in your Go streaming pipeline,
specify the following parameter. This parameter must be specified everytime
you want to disable Streaming Engine.

`--experiments=disable_streaming_engine`

If you use Dataflow Streaming Engine in your pipeline, don't
specify the `--zone` parameter. Instead, specify the `--region` parameter and
set the value to a [supported region](/dataflow/docs/resources/locations).
Dataflow auto-selects the zone in the region you
specified. If you specify the `--zone` parameter and set it to a zone
outside of the available regions, Dataflow reports an error.

Streaming Engine works best with smaller core worker machine types. Use the
job type to determine whether to use a high memory worker machine type.
Example machine types that we recommend include `--workerMachineType=n1-standard-2`
and `--workerMachineType=n1-highmem-2`. You can also set `--disk_size_gb=30`
because Streaming Engine only needs space for the worker boot image and local
logs. These values are the default values.

### gcloud CLI

When you run your pipeline by using the
[`gcloud dataflow jobs run`](https://cloud.google.com/sdk/gcloud/reference/dataflow/jobs/run)
command or the
[`gcloud dataflow flex-template run`](https://cloud.google.com/sdk/gcloud/reference/dataflow/flex-template/run)
command, to enable Streaming Engine, use the following flag:

`--enable-streaming-engine`

To disable streaming engine, use the following flag:

`--additional-experiments=disable_streaming_engine`

### REST

When you run your pipeline by using the
[`projects.locations.jobs.create`](/dataflow/docs/reference/rest/v1b3/projects.locations.jobs/create)
method in the REST API, use the
[`Job` resource](/dataflow/docs/reference/rest/v1b3/projects.jobs) to enable
or disable Streaming Engine. To enable Streaming Engine,
under `environment`, set the `experiments` field to `enable_streaming_engine`:

To disable Streaming Engine,
under `environment`, set the `experiments` field to `disable_streaming_engine`:

## Pricing

Dataflow Streaming Engine offers a resource-based billing model
where you're billed for the total resources that are consumed by your job.
With resource-based billing, the Streaming Engine resources
consumed by your job are metered and measured in
[Streaming Engine Compute Units](https://cloud.google.com/dataflow/pricing#streaming-compute-units).
You're billed for worker CPU, worker memory, and Streaming Engine Compute Units.

### Use resource-based billing

To use resource-based billing, when you
start or update your job, include the following
[Dataflow service option](/dataflow/docs/reference/service-options).

### Java

```
--dataflowServiceOptions=enable_streaming_engine_resource_based_billing
```

### Python

```
--dataflow_service_options=enable_streaming_engine_resource_based_billing
```

### Go

```
--dataflow_service_options=enable_streaming_engine_resource_based_billing
```

### Data-processed billing (legacy)

Unless you [enable resource-based billing](/dataflow/docs/streaming-engine#compute-unit-pricing),
your jobs are billed by using the legacy [data-processed billing](https://cloud.google.com/dataflow/pricing#streaming-data).

### Verify the billing model

Unless you're using Dataflow Prime, when you have jobs that use resource-based billing, the bill
includes the SKU `Streaming Engine Compute Unit`. When you have jobs that use
data-processed billing, the bill includes the SKU `Streaming Engine data processed`.
If you have some jobs that use resource-based billing and
other jobs that use data-processed billing,
the bill includes both SKUs.

When you use Dataflow Prime with resource-based billing, the
[Data Compute Unit (DCU)](https://cloud.google.com/dataflow/pricing#prime-compute-resources) SKU is used.

To see which pricing model your job uses, in the
[Dataflow monitoring interface](/dataflow/docs/guides/jobs-list),
select your job. If your job uses resource-based billing, the
**Job info** side panel includes a **Streaming Engine Compute Units** field.

If you have questions about your billing, contact
[Cloud Customer Care](/support).
