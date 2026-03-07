---
source_url: https://docs.cloud.google.com/dataflow/docs/request-quotas
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Request quotas \u00a0|\u00a0 Cloud Dataflow \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

The Dataflow service fully manages resources in Google Cloud
on a per-job basis. This includes spinning up and shutting down
[Compute Engine](/compute) instances (occasionally referred to as
`workers` or `VMs`) and accessing your project's
[Cloud Storage](/storage) buckets for both I/O and temporary file
staging. However, if your pipeline interacts with Google Cloud data
storage technologies like [BigQuery](/bigquery) and
[Pub/Sub](/pubsub), you must manage the resources and quota for those
services.

Dataflow uses a user provided location in
[Cloud Storage](/storage) specifically for staging files. This location
is under your control, and you should ensure that the location's lifetime is
maintained as long as any job is reading from it. You can re-use the same
staging location for multiple job runs, as the SDK's built-in caching can speed
up the start time for your jobs.

**Caution:** Manually altering Dataflow-managed
Compute Engine resources associated with a Dataflow job is
an unsupported operation. You should not attempt to manually stop, delete, or
otherwise control the Compute Engine instances that
Dataflow has created to run your job. In addition, you should not
alter any persistent disk resources associated with your Dataflow
job.

## Jobs

You may run up to 25 concurrent
Dataflow jobs per Google Cloud project; however, this
limit can be increased by contacting [Google Cloud Platform Support](/support). For more
information, see [Quotas](/dataflow/quotas#quota-increase).

The Dataflow service is currently limited to processing JSON job
requests that are 20 MB in size or smaller. The size of the job request is
specifically tied to the JSON representation of your pipeline; a larger pipeline
means a larger request.

To estimate the size of your pipeline's JSON request, run your pipeline with the
following option:

### Java

`--dataflowJobFile=<path to output file>`

### Python

`--dataflow_job_file=<path to output file>`

### Go

Estimating the size of a job's JSON payload with a flag is not currently
supported in Go.

This command writes a JSON representation of your job to a file. The size of the
serialized file is a good estimate of the size of the request; the actual size
will be slightly larger due to some additional information included in the
request.

For more information, see the troubleshooting page for
["413 Request Entity Too Large" / "The size of serialized JSON representation of the pipeline exceeds the allowable limit"](/dataflow/docs/guides/common-errors#json-request-too-large).

In addition, your job's graph size must not exceed 10 MB. For more information,
see the troubleshooting page for ["The job graph is too large. Please try again with a smaller job graph, or split your job into two or more smaller jobs."](/dataflow/docs/guides/common-errors#job-graph-too-large).

## Workers

The Dataflow service currently allows a maximum of **1000
Compute Engine instances per job**. For batch jobs, the default machine
type is `n1-standard-1`. For streaming jobs, the default machine type for
**Streaming Engine-enabled** jobs is `n1-standard-2` and the default machine
type for **non-Streaming Engine** jobs is `n1-standard-4`. When using the
default machine types, the Dataflow service can therefore allocate
up to 4000 cores per job. If you need more cores for your job, you can select a
larger machine type.

**Note:** The Dataflow managed service now deploys
Compute Engine virtual machines associated with Dataflow
jobs using [Managed Instance Groups](/compute/docs/instance-groups). A Managed
Instance Group creates multiple Compute Engine instances from a common
template and allows you to control and manage them as a group. That way, you
don't have to individually control each instance associated with your pipeline.

You should not attempt to manage or otherwise interact directly with your
Compute Engine Managed Instance Group; the Dataflow
service will take care of that for you. Manually altering any
Compute Engine resources associated with your Dataflow
job is an unsupported operation.

You can use any of the available Compute Engine machine type families as well
as custom machine types. For best results, use `n1` machine types. Shared core
machine types, such as `f1` and `g1` series workers, are not supported under the
Dataflow [Service Level Agreement](https://cloud.google.com/dataflow/sla).

To allocate additional memory per worker thread, use a custom machine type with
extended memory. For example, `custom-2-15360-ext` is an `n1` machine type with
2 CPUs and 15 GB of memory. Dataflow considers the number of CPUs
in a machine to determine the number of worker threads per worker VM. If your
pipeline processes memory-intensive work, a custom machine type with extended
memory can give more memory per worker thread. For more information, see
[Creating a custom VM instance](/compute/docs/instances/creating-instance-with-custom-machine-type).

Dataflow bills by the number of vCPUs and GB of memory in workers.
Billing is independent of the machine type family. You can specify a machine
type for your pipeline by [setting the appropriate execution parameter](/dataflow/pipelines/specifying-exec-params) at pipeline creation time.

**Caution:** Shared core machine types such as `f1` and `g1` series workers are
not supported under Dataflow's [Service Level Agreement](https://cloud.google.com/dataflow/sla).

### Java

To change the machine type, set the `--workerMachineType` option.

### Python

To change the machine type, set the `--worker_machine_type` option.

### Go

To change the machine type, set the `‑‑worker_machine_type` option.

**Note:** The Dataflow service currently does not support jobs
with only [preemptible virtual machines](/compute/docs/instances/preemptible).
Instead, if you would like to save processing costs, consider using the [FlexRS batch processing mode](/dataflow/docs/guides/flexrs) that uses a combination of preemptible and
non-preemptible resources.

### Resource quota

The Dataflow service checks to ensure that your Google Cloud
project has the Compute Engine resource quota required to run your job,
both to start the job and scale to the maximum number of worker instances. Your
job will fail to start if there is not enough resource quota available.

If your Dataflow job deploys Compute Engine virtual
machines as a Managed Instance Group, you'll need to ensure your project
satisfies some additional quota requirements. Specifically, your project will
need one of the following types of quota for each concurrent
Dataflow job that you want to run:

- One Instance Group per job
- One Managed Instance Group per job
- One Instance Template per job

**Caution:** Manually changing your Dataflow job's Instance
Template or Managed Instance Group is **not** recommended or supported. Use
Dataflow's [pipeline configuration options](/dataflow/pipelines/specifying-exec-params) instead.

Dataflow's [Horizontal Autoscaling](#autoscaling) feature is
limited by your project's available Compute Engine quota. If your job
has sufficient quota when it starts, but another job uses the remainder of your
project's available quota, the first job will run but not be able to fully scale.

However, the Dataflow service **does not** manage quota increases
for jobs that exceed the resource quotas in your project. You are responsible
for making any necessary requests for additional resource quota, for which you
can use the [Google Cloud console](https://console.cloud.google.com/).

### IP addresses

By default, Dataflow assigns both public and private IP addresses
to worker VMs. A public IP address satisfies one of the [criteria for internet access](/vpc/docs/vpc#internet_access_reqs), but a public IP address also counts
against your [quota of external IP addresses](/compute/quotas#external_ip_addresses).

If your worker VMs don't need access to the public internet, consider using only
internal IP addresses, which don't count against your external quota. For more
information on configuring IP addresses, see the following resources:

- [Public IP parameter](/dataflow/docs/guides/specifying-networks#public_ip_parameter)
- [Internet access for Dataflow](/dataflow/docs/guides/routes-firewall#internet_access_for)

### Inactive workers

If the workers for a given job don't exhibit sufficient activity over a one-hour
period, the job fails. Worker inactivity can result from dependency management
problems. For example, if a worker encounters an issue while installing
dependencies for a [custom container image](/dataflow/docs/guides/using-custom-containers),
the worker might fail to start or fail to make progress. The lack of progress
could then cause the job to fail. To learn more, see:

- [Troubleshoot custom containers in Dataflow](/dataflow/docs/guides/troubleshoot-custom-container)
- [Error syncing pod ... failed to "StartContainer"](/dataflow/docs/guides/common-errors#error-syncing-pod)

## Persistent disk resources

The Dataflow service is limited to **15 persistent disks
per worker instance** when running a streaming job. Each persistent disk is
local to an individual Compute Engine virtual machine. Your job may not
have more workers than persistent disks; a 1:1 ratio between workers and disks
is the minimum resource allotment.

Jobs using Streaming Engine use **30 GB** boot disks. Jobs
using Dataflow Shuffle use **25 GB**
boot disks. For jobs that are not using these offerings, the default size of
each persistent disk is **250 GB in batch mode** and **400 GB in streaming
mode**.

## Locations

By default, the Dataflow service deploys Compute Engine
resources in the `us-central1-f` zone of the `us-central1` region. You can
override this setting by [specifying](/dataflow/pipelines/specifying-exec-params)
the `--region` parameter. If you need to use a specific zone for your resources,
use the `--zone` parameter when you create your pipeline. However, we recommend
that you only specify the region, and leave the zone unspecified. This allows
the Dataflow service to automatically select the best zone within
the region based on the available zone capacity at the time of the job creation
request. For more information, see the
[Dataflow regions](/dataflow/docs/concepts/regional-endpoints)
documentation.
