---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/common-errors
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Troubleshoot Dataflow errors \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

If you run into problems with your Dataflow pipeline or job, this
page lists error messages that you might see and provides suggestions for how to
fix each error.

Errors in the log types `dataflow.googleapis.com/worker-startup`,
`dataflow.googleapis.com/harness-startup`, and `dataflow.googleapis.com/kubelet`
indicate configuration problems with a job. They can also indicate conditions
that prevent the normal logging path from functioning.

Your pipeline might throw exceptions while processing data. Some of these errors
are transient, for example when temporary difficulty accessing an external
service occurs. Some of these errors are permanent, such as errors caused by
corrupt or unparseable input data, or null pointers during computation.

Dataflow processes elements in arbitrary bundles and retries the
complete bundle when an error is thrown for any element in that bundle. When
running in batch mode, bundles including a failing item are retried four times.
The pipeline fails completely when a single bundle fails four times. When
running in streaming mode, a bundle including a failing item is retried
indefinitely, which might cause your pipeline to permanently stall.

Exceptions in user code, for example, your `DoFn` instances, are
reported in the [Dataflow monitoring
interface](/dataflow/pipelines/dataflow-monitoring-intf). If you run your
pipeline with `BlockingDataflowPipelineRunner`, you also see error messages
printed in your console or terminal window.

Consider guarding against errors in your code by adding exception handlers. For
example, if you want to drop elements that fail some custom input validation
done in a `ParDo`, use a try/catch block within
your `ParDo` to handle the exception and log and drop the element. For
production workloads, implement an unprocessed message pattern. To track the
error count, you use [aggregation
transforms](https://beam.apache.org/documentation/transforms/java/overview/#aggregation).

## Missing log files

If you don't see any logs for your jobs, remove any exclusion filters containing
`resource.type="dataflow_step"` from all of your Cloud Logging **Log Router**
sinks.

[Go to Log Router](https://console.cloud.google.com/logs/router)

For more details about removing your logs exclusions, refer to the [Removing
exclusions](/logging/docs/exclusions#stopping-resource) guide.

## Duplicates in output

When you run a Dataflow job, the output contains duplicate
records.

This issue can occur when your Dataflow job uses the at-least-once
pipeline streaming mode. This mode guarantees
that records are processed at least once. However, duplicate records are
possible in this mode.

If your workflow can't tolerate duplicate records, use the exactly-once
streaming mode. This mode helps to ensure that records are not dropped or
duplicated as the data moves through the pipeline.

To verify which streaming mode your job is using, see [View a job's streaming
mode](/dataflow/docs/guides/streaming-modes#view-streaming-mode).

For more information about streaming modes, see [Set the pipeline streaming
mode](/dataflow/docs/guides/streaming-modes).

## Pipeline errors

The following sections contain common pipeline errors that you might encounter
and steps for resolving or troubleshooting the errors.

### Some Cloud APIs need to be enabled

When you try to run a Dataflow job, the following error occurs:

```
Some Cloud APIs need to be enabled for your project in order for Cloud Dataflow to run this job.
```

This issue occurs because some required APIs are not enabled in your project.

To resolve this issue and run a Dataflow job, enable the following
Google Cloud APIs in your project:

- Compute Engine API (Compute Engine)
- Cloud Logging API
- Cloud Storage
- Cloud Storage JSON API
- BigQuery API
- Pub/Sub
- Datastore API

For detailed instructions, see the [Getting Started section on enabling
Google Cloud APIs](/dataflow/getting-started#APIs) .

### "@\*" and "@N" are reserved sharding specs

When you try to run a job, the following error appears in the log files, and the
job fails:

```
Workflow failed. Causes: "@*" and "@N" are reserved sharding specs. Filepattern must not contain any of them.
```

This error occurs if the filename for your Cloud Storage path for
temporary files (`tempLocation` or `temp_location`) has an at sign (@) followed
by a number or by an asterisk (\*).

To resolve this issue, change the filename so that the at sign is followed by a
supported character.

### Bad request

When you run a Dataflow job,
[Cloud Monitoring](/dataflow/docs/guides/using-cloud-monitoring) logs display
a series of warnings similar to the following:

```
Unable to update setup work item STEP_ID error: generic::invalid_argument: Http(400) Bad Request
Update range task returned 'invalid argument'. Assuming lost lease for work with id LEASE_ID
with expiration time: TIMESTAMP, now: TIMESTAMP. Full status: generic::invalid_argument: Http(400) Bad Request
```

Bad request warnings occur if worker state information is stale or out of sync
due to processing delays. Often, your Dataflow job succeeds
despite the bad request warnings. If that is the case, ignore the warnings.

### Cannot read and write in different locations

When you run a Dataflow job, you might see the following error in
the log files:

```
message:Cannot read and write in different locations: source: SOURCE_REGION, destination: DESTINATION_REGION,reason:invalid
```

This error occurs when the source and destination are in different regions. It
can also occur when the staging location and destination are in different
regions. For example, if the job reads from Pub/Sub and then writes to a
Cloud Storage `temp` bucket before writing to a BigQuery table, the
Cloud Storage `temp` bucket and the BigQuery table must be in the
same region.

Multi-region locations are considered different than single-region locations,
even if the single region falls within the scope of the multi-region location.
For example, `us (multiple regions in the United States)` and `us-central1` are
different regions.

To resolve this issue, have your destination, source, and staging locations in
the same region. Cloud Storage bucket locations can't be changed, so you
might need to create a new Cloud Storage bucket in the correct region.

### Connection timed out

When you run a Dataflow job, you might see the following error in
the log files:

```
org.springframework.web.client.ResourceAccessException: I/O error on GET request for CONNECTION_PATH: Connection timed out (Connection timed out); nested exception is java.net.ConnectException: Connection timed out (Connection timed out)
```

This issue occurs when the Dataflow workers fail to establish or
maintain a connection with the data source or destination.

To resolve the issue, follow these troubleshooting steps:

- Verify that the data source is running.
- Verify that the destination is running.
- Review the [connection parameters](https://beam.apache.org/documentation/pipelines/create-your-pipeline/#reading-data-into-your-pipeline)
  used in the Dataflow pipeline configuration.
- Verify that performance issues aren't affecting the source or destination.
- Make sure that [firewall rules](/dataflow/docs/guides/routes-firewall)
  aren't blocking the connection.

### No such object

When you run your Dataflow jobs, you might see the following error in
the log files:

```
..., 'server': 'UploadServer', 'status': '404'}>, <content <No such object:...
```

These errors typically occur when some of your running Dataflow jobs
use the same `temp_location` to stage temporary job files created when the
pipeline runs. When multiple concurrent jobs share the same `temp_location`,
these jobs might step on the temporary data of each other, and a race condition
might occur. To avoid this issue, it's recommended that you use a unique
`temp_location` for each job.

### Dataflow is unable to determine backlog

When running a streaming pipeline from Pub/Sub, the following
warning occurs:

```
Dataflow is unable to determine the backlog for Pub/Sub subscription
```

When a Dataflow pipeline pulls data from Pub/Sub,
Dataflow needs to repeatedly request information from
Pub/Sub. This information includes the amount of backlog on the
subscription and the age of the oldest unacknowledged message. Occasionally,
Dataflow is unable to retrieve this information from
Pub/Sub because of internal system issues, which may cause a
transient accumulation of backlog.

For more information, see [Streaming With Cloud
Pub/Sub](/dataflow/docs/concepts/streaming-with-cloud-pubsub).

### DEADLINE_EXCEEDED or Server Unresponsive

When you run your jobs, you might encounter RPC timeout exceptions or one of the
following errors:

```
DEADLINE_EXCEEDED
```

Or:

```
Server Unresponsive
```

These errors typically occur for one of the following reasons:

- **The Virtual Private Cloud (VPC) network used for your job might be missing
  a [firewall rule](/vpc/docs/firewalls)**. The firewall rule needs to enable
  all TCP traffic among VMs in the VPC network you specified in
  your pipeline options. For more information, see [Firewall rules for
  Dataflow](/dataflow/docs/guides/routes-firewall#firewall_rules).

  In some cases, the workers aren't able to communicate with each other. When
  you run a Dataflow job that doesn't use Dataflow
  Shuffle or Streaming Engine, workers need to communicate with each other
  using TCP ports `12345` and `12346` within the VPC network.
  In this scenario, the error includes the worker harness name and the TCP
  port that's blocked. The error looks like one of the following examples:

  ```
  DEADLINE_EXCEEDED: (g)RPC timed out when SOURCE_WORKER_HARNESS
  talking to DESTINATION_WORKER_HARNESS:12346.
  ```

  ```
  Rpc to WORKER_HARNESS:12345 completed with error UNAVAILABLE: failed to connect to all addresses
  Server unresponsive (ping error: Deadline Exceeded, UNKNOWN: Deadline Exceeded...)
  ```

  To resolve this issue, use the `gcloud compute firewall-rules create`
  [rules](/sdk/gcloud/reference/compute/firewall-rules/create#--rules) flag to
  allow network traffic to ports `12345` and `12346`. The following example
  demonstrates the Google Cloud CLI command:

  ```
  gcloud compute firewall-rules create FIREWALL_RULE_NAME \
    --network NETWORK \
    --action allow \
    --direction IN \
    --target-tags dataflow \
    --source-tags dataflow \
    --priority 0 \
    --rules tcp:12345-12346
  ```

  Replace the following:
  - `FIREWALL_RULE_NAME`: the name of your firewall
    rule
  - `NETWORK`: the name of your network

- **Your job is shuffle-bound**.

  To resolve this issue, make one or more of the following changes.

  ### Java
  - If the job is not using the service-based shuffle, switch to using the
    service-based Dataflow Shuffle by setting
    `--experiments=shuffle_mode=service`. For details and availability, see
    [Dataflow Shuffle](/dataflow/docs/shuffle-for-batch).
  - _Add more workers_. Try setting `--numWorkers` with a higher value when
    you run your pipeline.
  - _Increase the size of the attached disk for workers._ Try setting
    `--diskSizeGb` with a higher value when you run your pipeline.
  - _Use an SSD-backed persistent disk_. Try setting
    `--workerDiskType="compute.googleapis.com/projects/PROJECT_ID/zones/ZONE/diskTypes/pd-ssd"`
    when you run your pipeline.

  ### Python
  - If the job is not using the service-based shuffle, switch to using the
    service-based Dataflow Shuffle by setting
    `--experiments=shuffle_mode=service`.
    For details and availability, see
    [Dataflow Shuffle](/dataflow/docs/shuffle-for-batch).
  - _Add more workers_. Try setting `--num_workers` with a
    higher value when you run your pipeline.
  - _Increase the size of the attached disk for workers._ Try setting
    `--disk_size_gb` with a higher value when you run your pipeline.
  - _Use an SSD-backed persistent disk_. Try setting
    `--worker_disk_type="compute.googleapis.com/projects/PROJECT_ID/zones/ZONE/diskTypes/pd-ssd"`
    when you run your pipeline.

  ### Go
  - If the job is not using the service-based shuffle, switch to using the
    service-based Dataflow Shuffle by setting
    `--experiments=shuffle_mode=service`.
    For details and availability, see
    [Dataflow Shuffle](/dataflow/docs/shuffle-for-batch).
  - _Add more workers_. Try setting `--num_workers` with a
    higher value when you run your pipeline.
  - _Increase the size of the attached disk for workers._ Try setting
    `--disk_size_gb` with a higher value when you run your pipeline.
  - _Use an SSD-backed persistent disk_. Try setting
    `--disk_type="compute.googleapis.com/projects/PROJECT_ID/zones/ZONE/diskTypes/pd-ssd"`
    when you run your pipeline.

### Empty split returned

When running a Dataflow job, the following message might appear in
the worker logs:

```
Continuing to process work-id WORK_ID without splitting. Reader split status was: INTERNAL: Empty split returned and SDK split status was: ...
```

If your job runs correctly, this message is benign, and you can ignore it. This
message can occur due to a race condition where the service attempts to split
work that has already been completed.

### Encoding errors, IOExceptions, or unexpected behavior in user code

The Apache Beam SDKs and the Dataflow workers depend on common
third-party components. These components import additional dependencies. Version
collisions can result in unexpected behavior in the service. Also, some
libraries aren't forward-compatible. You might need to pin to the listed
versions that are in scope during execution. [SDK and Worker
Dependencies](/dataflow/docs/concepts/sdk-worker-dependencies) contains a list
of dependencies and their required versions.

### Error running LookupEffectiveGuestPolicies

When you run a Dataflow job, you might see the following error in
the log files:

```
OSConfigAgent Error policies.go:49: Error running LookupEffectiveGuestPolicies:
error calling LookupEffectiveGuestPolicies: code: "Unauthenticated",
message: "Request is missing required authentication credential.
Expected OAuth 2 access token, login cookie or other valid authentication credential.
```

This error occurs if [OS configuration
management](/compute/docs/os-configuration-management) is enabled for the entire
project.

To resolve this issue, disable [VM Manager](/compute/docs/vm-manager)
policies that apply to the entire project. If disabling VM Manager
policies for the entire project isn't possible, you can safely ignore this error
and filter it out of log monitoring tools.

### A fatal error has been detected by the Java Runtime Environment

The following error occurs during worker startup:

```
A fatal error has been detected by the Java Runtime Environment
```

This error occurs if the pipeline is using Java Native Interface (JNI) to run
non-Java code and that code or the JNI bindings contain an error.

### googclient_deliveryattempt attribute key error

Your Dataflow job fails with one of the following errors:

```
The request contains an attribute key that is not valid (key=googclient_deliveryattempt). Attribute keys must be non-empty and must not begin with 'goog' (case-insensitive).
```

Or:

```
Invalid extensions name: googclient_deliveryattempt
```

This error occurs when your Dataflow job has the following
characteristics:

- The Dataflow job uses Streaming Engine.
- The pipeline has a Pub/Sub sink.
- The pipeline uses a [pull subscription](/pubsub/docs/pull).
- The pipeline uses one of the [Pub/Sub service
  APIs](/pubsub/docs/pull#service_apis) to publish messages instead of using
  the built-in Pub/Sub I/O sink.
- Pub/Sub is using the Java or C# [client
  library](/pubsub/docs/pull#client_libraries).
- The Pub/Sub subscription has a [dead-letter
  topic](/pubsub/docs/handling-failures#dead_letter_topic).

This error occurs because when you use the Pub/Sub Java or C#
client library and a dead-letter topic for a subscription is enabled, the
delivery attempts are in the `googclient_deliveryattempt` message attribute
instead of the `delivery_attempt` field. For more information, see [Track
delivery attempts](/pubsub/docs/dead-letter-topics#track-delivery-attempts) in
the "Handle message failures" page.

To workaround this issue, make one or more of the following changes.

- [Disable Streaming Engine](/dataflow/docs/streaming-engine#use).
- Use the built-in [Apache Beam `PubSubIO` connector](https://beam.apache.org/documentation/io/connectors/)
  instead of the Pub/Sub service API.
- Use a different [type of Pub/Sub
  subscription](/pubsub/docs/subscription-overview#push_pull).
- [Remove the dead-letter
  topic](/pubsub/docs/dead-letter-topics#removing_a_dead_letter_topic).
- Don't use the Java or C# client library with your Pub/Sub pull
  subscription. For other options, see [Client library code
  samples](/pubsub/docs/pull#client_library_code_samples).
- In your pipeline code, when attribute keys start with `goog`, erase the
  message attributes before publishing the messages.

### A hot key ... was detected

**Note:** Hot key detection and logging is disabled for streaming pipelines as of
March 2022.

The following error occurs:

```
A hot key HOT_KEY_NAME was detected in...
```

These errors occur if your data contains a hot key. A hot key is a key with
enough elements to negatively affect pipeline performance. These keys limit the
ability of Dataflow to process elements in parallel, which
increases execution time.

To print the human-readable key to the logs when a hot key is detected in the
pipeline, use the [hot key pipeline
option](/dataflow/docs/reference/pipeline-options#debugging).

To resolve this issue, check that your data is evenly distributed. If a key has
disproportionately many values, consider the following courses of action:

- Rekey your data. Apply a
  [`ParDo`](https://beam.apache.org/documentation/programming-guide/#pardo)
  transform to output new key-value pairs.
- For Java jobs, use the [`Combine.PerKey.withHotKeyFanout`](https://beam.apache.org/releases/javadoc/current/org/apache/beam/sdk/transforms/Combine.PerKey.html)
  transform.
- For Python jobs, use the [`CombinePerKey.with_hot_key_fanout`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.CombinePerKey.with_hot_key_fanout)
  transform.
- Enable [Dataflow Shuffle](/dataflow/docs/shuffle-for-batch).

To view hot keys in the Dataflow monitoring interface, see
[Troubleshoot stragglers in batch
jobs](/dataflow/docs/guides/troubleshoot-batch-stragglers).

### Invalid table specification in Data Catalog

When you use Dataflow SQL to create Dataflow SQL jobs, your job might fail
with the following error in the log files:

```
Invalid table specification in Data Catalog: Could not resolve table in Data Catalog
```

This error occurs if the Dataflow service account doesn't have
access to the Data Catalog API.

To resolve this issue, [enable the Data Catalog
API](/dataplex/docs/transition-to-dataplex-catalog) in the Google Cloud
[project](/resource-manager/docs/cloud-platform-resource-hierarchy#projects)
that you're using to write and run queries.

Alternately, assign the `roles/datacatalog.viewer` role to the [Dataflow service
account](/dataflow/docs/concepts/security-and-permissions#security_and_permissions_for_pipelines_on).

### The job graph is too large

Your job might fail with the following error:

```
The job graph is too large. Please try again with a smaller job graph,
or split your job into two or more smaller jobs.
```

This error occurs if the graph size of your job exceeds 10 MB. Certain
conditions in your pipeline can cause the job graph to exceed the limit. Common
conditions include:

- A `Create` transform that includes a large amount of in-memory data.
- A large `DoFn` instance that is serialized for transmission to remote
  workers.
- A `DoFn` as an anonymous inner class instance that (possibly inadvertently)
  pulls in a large amount of data to be serialized.
- A directed acyclic graph (DAG) is being used as part of a programmatic loop
  that is enumerating a large list.

To avoid these conditions, consider restructuring your pipeline.

### Key Commit Too Large

When running a streaming job, the following error appears in the worker log
files:

```
KeyCommitTooLargeException
```

This error occurs in streaming scenarios if a very large amount of data is
grouped without using a `Combine` transform, or if a large amount of data is
produced from a single input element.

To reduce the possibility of encountering this error, use the following
strategies:

- Make sure that processing a single element cannot result in outputs or state
  modifications exceeding the limit.
- If multiple elements were grouped by a key, consider increasing the key
  space to reduce the elements grouped per key.
- If elements for a key are emitted at a high frequency over a short time,
  that might result in many GB of events for that key in windows. Rewrite the
  pipeline to detect keys like this and only emit an output indicating the key
  was frequently present in that window.
- Use sublinear space `Combine` transforms for commutative and associate
  operations. Don't use a combiner if it doesn't reduce space. For example,
  combiner for strings that just appends strings together is worse than not
  using combiner.

### Rejecting message over 7168K

When you run a Dataflow job created from a template, the job might fail
with the following error:

```
Error: CommitWork failed: status: APPLICATION_ERROR(3): Pubsub publish requests are limited to 10MB, rejecting message over 7168K (size MESSAGE_SIZE) to avoid exceeding limit with byte64 request encoding.
```

This error occurs when messages written to a dead-letter queue exceed the size
limit of 7168 K. As a workaround, enable [Streaming
Engine](/dataflow/docs/streaming-engine), which has a higher size limit. To
enable Streaming Engine, use the following [pipeline
option](/dataflow/docs/reference/pipeline-options#streaming_pipeline_management).

### Java

`--enableStreamingEngine=true`

### Python

`--enable_streaming_engine=true`

### Request Entity Too Large

When you submit your job, one of the following errors appears in your console or
terminal window:

```
413 Request Entity Too Large
The size of serialized JSON representation of the pipeline exceeds the allowable limit
Failed to create a workflow job: Invalid JSON payload received
Failed to create a workflow job: Request payload exceeds the allowable limit
```

When you encounter an error about the JSON payload when submitting your job, the
JSON representation of your pipeline exceeds the maximum 20 MB request
size.

The size of your job is tied to the JSON representation of the pipeline. A
larger pipeline means a larger request. Dataflow
has a limitation that caps requests at 20 MB.

To estimate the size of the JSON request of your pipeline, run your pipeline
with the following option:

### Java

`--dataflowJobFile=PATH_TO_OUTPUT_FILE`

### Python

`--dataflow_job_file=PATH_TO_OUTPUT_FILE`

### Go

Outputting your job as JSON is not supported in Go.

This command writes a JSON representation of your job to a file. The size of the
serialized file is a good estimate of the size of the request. The actual size
is slightly larger due to some additional information included the request.

Certain conditions in your pipeline can cause the JSON representation to exceed
the limit. Common conditions include:

- A `Create` transform that includes a large amount of in-memory data.
- A large `DoFn` instance that is serialized for transmission to remote
  workers.
- A `DoFn` as an anonymous inner class instance that (possibly inadvertently)
  pulls in a large amount of data to be serialized.

To avoid these conditions, consider restructuring your pipeline.

### SDK pipeline options or staging file list exceeds size limit

When running a pipeline, one of the following errors occurs:

```
SDK pipeline options or staging file list exceeds size limit.
Please keep their length under 256K Bytes each and 512K Bytes in total.
```

Or:

```
Value for field 'resource.properties.metadata' is too large: maximum size
```

These errors occur if the pipeline couldn't be started due to Compute Engine
metadata limits being exceeded. These limits can't be changed.
Dataflow uses Compute Engine metadata for pipeline options. The
limit is documented in the Compute Engine custom metadata
[limitations](/compute/docs/metadata/setting-custom-metadata#limitations).

The following scenarios can cause the JSON representation to exceed the limit:

- There are too many JAR files to stage.
- The `sdkPipelineOptions` request field is too large.

To estimate the size of the JSON request of your pipeline, run your pipeline
with the following option:

### Java

`--dataflowJobFile=PATH_TO_OUTPUT_FILE`

### Python

`--dataflow_job_file=PATH_TO_OUTPUT_FILE`

### Go

Outputting your job as JSON is not supported in Go.

The size of the output file from this command must be less than 256 KB. The
512 KB in the error message refers to the total size of the output file and
the custom metadata options for the Compute Engine VM instance.

You can get a rough estimate of the custom metadata option for VM instance from
running Dataflow jobs in the project. Choose any running
Dataflow job. Take a VM instance, and then navigate to the
Compute Engine VM instance details page for that VM to check for the custom
metadata section. The total length of the custom metadata and the file should be
less than 512 KB. An accurate estimate for the failed job is not possible,
because the VMs are not spun up for failed jobs.

If your JAR list is hitting the 256-KB limit, review it and reduce any
unnecessary JAR files. If it's still too large, try running the
Dataflow job by using an uber JAR. For an example that
demonstrates how to create and use uber JAR, see [Build and deploy an Uber
JAR](/functions/docs/concepts/java-deploy#build_and_deploy_an_uber_jar).

If the `sdkPipelineOptions` request field is too large, include the following
option when you run your pipeline. The pipeline option is the same for Java,
Python, and Go.

```
--experiments=no_display_data_on_gce_metadata
```

### Shuffle key too large

The following error appears in the worker log files:

```
Shuffle key too large
```

This error occurs if the serialized key emitted to a particular (Co-)GroupByKey
is too large after the corresponding coder is applied. Dataflow
has a limit for serialized shuffle keys.

To resolve this issue, reduce the size of the keys or use more space-efficient
coders.

For more information, see [production limits for
Dataflow](/dataflow/quotas#limits).

### Side input stale caching in global window

When running a streaming pipeline using the Apache Beam SDK for Python, side
inputs in the global window might experience unpredictable delays in updates.
Workers might retain old side input values for extended periods, especially when
processing continuous main input data. This issue typically affects pipelines
using Pub/Sub as both main and side inputs.

To resolve this issue, if you use Apache Beam SDK version 2.56.0 or later,
enable the `disable_global_windowed_args_caching` experiment flag:

```
--experiments=disable_global_windowed_args_caching
```

### Total number of BoundedSource objects ... is larger than the allowable limit

One of the following errors might occur when running jobs with Java:

```
Total number of BoundedSource objects generated by splitIntoBundles() operation is larger than the allowable limit
```

Or:

```
Total size of the BoundedSource objects generated by splitIntoBundles() operation is larger than the allowable limit
```

### Java

This error might occur if you're reading from a very large number of files
by using `TextIO`, `AvroIO`, `BigQueryIO` through EXPORT, or some other
file-based source. The particular limit depends on the details of your
source, but it is on the order of tens of thousands of files in one
pipeline. For example, embedding schema in `AvroIO.Read` allows fewer files.

This error might also occur if you created a custom data source for your
pipeline and the `splitIntoBundles` method of your source returned a list of
`BoundedSource` objects which takes up more than 20 MB when serialized.

The allowable limit for the total size of the `BoundedSource` objects
generated by the `splitIntoBundles()` operation of your custom source is
20 MB.

To work around this limitation, make one of the following changes:

1. Enable [Runner V2](/dataflow/docs/runner-v2). Runner v2 converts sources
   into splittable DoFns that don't have this source split limit.
2. Modify your custom `BoundedSource` subclass so that the total size of
   the generated `BoundedSource` objects is smaller han the 20-MB limit.
   For example, your source might generate fewer splits initially, and rely
   on [Dynamic Work Rebalancing](/dataflow/docs/dynamic-work-rebalancing)
   to further split inputs on demand.

### Request payload size exceeds the limit: 20971520 bytes

When you run a pipeline, the job might fail with the following error:

```
com.google.api.client.googleapis.json.GoogleJsonResponseException: 400 Bad Request
POST https://dataflow.googleapis.com/v1b3/projects/PROJECT_ID/locations/REGION/jobs/JOB_ID/workItems:reportStatus
{
  "code": 400,
  "errors": [
    {
      "domain": "global",
      "message": "Request payload size exceeds the limit: 20971520 bytes.",
      "reason": "badRequest"
    }
  ],
  "message": "Request payload size exceeds the limit: 20971520 bytes.",
  "status": "INVALID_ARGUMENT"
}
```

This error can occur when a job using the Dataflow runner has a
very large job graph. A large job graph can generate a large number of metrics
that need to be reported back to the Dataflow service. If the size of
these metrics exceeds the 20 MB API request limit, the job fails.

To resolve this issue, migrate your pipeline to use [Dataflow Runner
v2](/dataflow/docs/runner-v2). Runner v2 uses a more efficient method for
reporting metrics and does not have this 20 MB limitation.

### ModuleNotFoundError: No module named 'pkg_resources'

When you run a Dataflow job, the following error occurs during
worker startup or dependency installation:

```
ModuleNotFoundError: No module named 'pkg_resources'
```

This issue occurs because as of `setuptools` version 82.0.0 (released on
February 8, 2026), the `pkg_resources` module has been removed. This module was
previously deprecated and has been replaced by `importlib.resources` and
`importlib.metadata`.

To resolve this issue, use one of the following methods:

- **Pin `setuptools`**: If your dependencies require a backward-compatible
  version of `setuptools` to build successfully, force a specific version
  requirement using the `setup_requires` argument in your `setup.py` file. For
  example:

  ```
  import setuptools

  setuptools.setup(
      name='PACKAGE-NAME',
      version='PACKAGE-VERSION',
      # Pin to a version prior to 82.0.0
      setup_requires=['setuptools<82.0.0'],
      install_requires=['incompatible-package', ...],
      packages=setuptools.find_packages()
  )
  ```

- **Update dependencies**: Review your library and dependency requirements to
  update to newer versions that are compatible with the latest version of
  `setuptools` and don't rely on `pkg_resources`.
- **Remove unnecessary libraries**: Remove any libraries from your
  requirements or setup file that aren't required by your job. For example,
  some earlier versions of `cx_Oracle` have been identified as triggering this
  issue during the build process.

### NameError

When you execute your pipeline using the Dataflow service, the
following error occurs:

```
NameError
```

This error does not occur when you execute locally, such as when you execute
using the `DirectRunner`.

This error occurs if your `DoFn`s are using values in the global namespace that
are not available on the Dataflow worker.

By default, global imports, functions, and variables defined in the main session
are not saved during the serialization of a Dataflow job.

To resolve this issue, use one of the following methods. If your `DoFn`s are
defined in the main file and reference imports and functions in the global
namespace, set the `--save_main_session` pipeline option to `True`. This change
pickles the state of the global namespace to and loads it on the
Dataflow worker.

If you have objects in your global namespace that can't be pickled, a pickling
error occurs. If the error is regarding a module that should be available in the
Python distribution, import the module locally, where it's used.

For example, instead of:

```
import re
…
def myfunc():
  # use re module
```

use:

```
def myfunc():
  import re
  # use re module
```

Alternatively, if your `DoFn`s span multiple files, use a different
approach to packaging your workflow and [managing
dependencies](https://beam.apache.org/documentation/sdks/python-pipeline-dependencies/).

### Object is subject to bucket's retention policy

When you have a Dataflow job that writes to a Cloud Storage
bucket, the job fails with the following error:

```
Object 'OBJECT_NAME' is subject to bucket's retention policy or object retention and cannot be deleted or overwritten
```

You might also see the following error:

```
Unable to rename "gs://BUCKET"
```

The first error occurs when object retention is enabled on the Cloud Storage
bucket that the Dataflow job is writing to. For more information,
see [Enable and use object retention
configurations](/storage/docs/using-object-lock).

To resolve this issue, use one of the following workarounds:

- Write to a Cloud Storage bucket that doesn't have a retention policy on
  the `temp` folder.
- Remove the retention policy from the bucket that the job writes to. For more
  information, see [Set an object's retention
  configuration](/storage/docs/using-object-lock#set-object-config).

The second error can indicate that the object retention is enabled on the
Cloud Storage bucket, or it can indicate that the Dataflow
worker service account doesn't have permission to write to the Cloud Storage
bucket.

If you see the second error and object retention is enabled on the
Cloud Storage bucket, try the workarounds described previously. If object
retention isn't enabled on the Cloud Storage bucket, verify whether the
Dataflow worker service account has write permission on the
Cloud Storage bucket. For more information, see [Access Cloud Storage
buckets](/dataflow/docs/concepts/security-and-permissions#accessing_gcs).

### Processing stuck or operation ongoing

If Dataflow spends more time executing a `DoFn` than the time
specified in TIME_INTERVAL without returning, the
following message is displayed.

### Java

Either of the two following log messages, depending on the version:

`Processing stuck in step STEP_NAME for at least TIME_INTERVAL`

`Operation ongoing in bundle BUNDLE_ID for at least TIME_INTERVAL without outputting or completing: at STACK_TRACE`

### Python

`Operation ongoing for over TIME_INTERVAL in state STATE in step STEP_ID without returning. Current Traceback: TRACEBACK`

### Go

`Operation ongoing in transform TRANSFORM_ID for at least TIME_INTERVAL without outputting or completing in state STATE`

This behavior has two possible causes:

- Your `DoFn` code is slow, or waiting for some slow external operation to
  complete.
- Your `DoFn` code might be stuck, deadlocked, or abnormally slow to finish
  processing.

To determine which is the case, expand the
[Cloud Monitoring](/dataflow/docs/guides/using-cloud-monitoring) log entry to
see a stack trace. Look for messages that indicate that the `DoFn` code is stuck
or otherwise encountering issues. If no messages are present, the issue might be
the execution speed of the `DoFn` code. Consider using
[Cloud Profiler](/dataflow/docs/guides/profiling-a-pipeline) or other tool to
investigate the performance of your code.

If your pipeline is built on the Java VM (using either Java or Scala), you can
investigate the cause of your stuck code. Take a full thread dump of the whole
JVM (not just the stuck thread) by following these steps:

1. Make note of the worker name from the log entry.
2. In the Compute Engine section of the Google Cloud console, find
   the Compute Engine instance with the worker name you noted.
3. Use SSH to connect to the instance with that name.
4. Run the following command:

   ```
   curl http://localhost:8081/threadz
   ```

### Operation ongoing in bundle

When you run a pipeline reading from
[`JdbcIO`](https://beam.apache.org/releases/javadoc/current/org/apache/beam/sdk/io/jdbc/JdbcIO.html),
the partitioned reads from `JdbcIO` are slow, and the following message appears
in the worker log files:

```
Operation ongoing in bundle process_bundle-[0-9-]* for PTransform{id=Read from JDBC with Partitions\/JdbcIO.Read\/JdbcIO.ReadAll\/ParDo\(Read\)\/ParMultiDo\(Read\).*, state=process} for at least (0[1-9]h[0-5][0-9]m[0-5][0-9]s) without outputting or completing:
```

To resolve this issue, make one or more of the following changes to your
pipeline:

- Use partitions to increase the job parallelism. Read with more and smaller
  partitions for better scaling.
- Check if the partitioning column is an index column or a true partitioning
  column in the source. Activate indexing and partitioning on this column in
  the source database for the best performance.
- Use `lowerBound` and `upperBound` parameters to skip finding the bounds.

### Pub/Sub quota errors

When running a streaming pipeline from Pub/Sub, the following
errors occur:

```
429 (rateLimitExceeded)
```

Or:

```
Request was throttled due to user QPS limit being reached
```

These errors occur if your project has insufficient [Pub/Sub
quota](/pubsub/quotas).

To find out if your project has insufficient quota, follow these steps to check
for client errors:

1. Go to the [Google Cloud console](https://console.cloud.google.com/).
2. In the menu on the left, select **APIs & services**.
3. In the **Search Box**, search for **Cloud Pub/Sub**.
4. Click the **Usage** tab.
5. Check **Response Codes** and look for `(4xx)` client error codes.

### Request is prohibited by organization's policy

When running a pipeline, the following error occurs:

```
Error trying to get gs://BUCKET_NAME/FOLDER/FILE:
{"code":403,"errors":[{"domain":"global","message":"Request is prohibited by organization's policy","reason":"forbidden"}],
"message":"Request is prohibited by organization's policy"}
```

This error occurs if the Cloud Storage bucket is outside of your [service
perimeter](/vpc-service-controls/docs/overview).

To resolve this issue, create an [egress
rule](/vpc-service-controls/docs/ingress-egress-rules) that allows access to the
bucket outside of the service perimeter.

### Staged package...is inaccessible

Jobs that used to succeed might fail with the following error:

```
Staged package...is inaccessible
```

To resolve this issue:

- Verify that the Cloud Storage bucket used for staging does not have
  [TTL settings](/storage/docs/lifecycle) that cause staged packages to be
  deleted.
- Verify that the worker service account of your Dataflow
  project has the permission to access the Cloud Storage bucket used
  for staging. Gaps in permission can be due to any of the following reasons:
  - The Cloud Storage bucket used for staging is present in a
    different project.
  - The Cloud Storage bucket used for staging was migrated from
    fine-grained access to [uniform bucket-level
    access](/storage/docs/uniform-bucket-level-access). Due to the
    inconsistency between IAM and ACL policies, migrating the
    staging bucket to uniform bucket-level access disallows ACLs for
    Cloud Storage resources. ACLs include the permissions held by
    the worker service account of your Dataflow project over
    the staging bucket.

For more information, see [Accessing Cloud Storage buckets across
Google Cloud Platform
projects](/dataflow/docs/concepts/security-and-permissions#accessing_buckets_across_projects).

### A work item has failed 4 times

The following error occurs when a batch job fails:

```
The job failed because a work item has failed 4 times.
```

This error occurs if a single operation in a batch job causes the worker code to
fail four times. Dataflow fails the job, and this message is
displayed.

When running in streaming mode, a bundle including a failing item is retried
indefinitely, which might cause your pipeline to permanently stall.

You can't configure this failure threshold. For more details, refer to [pipeline
error and exception
handling](/dataflow/docs/pipeline-lifecycle#error_and_exception_handling).

To resolve this issue, look in the
[Cloud Monitoring](/dataflow/docs/guides/using-cloud-monitoring) logs of the
job for the four individual failures. In the worker logs, look for
**Error-level** or **Fatal-level** log entries that show exceptions or errors.
The exception or error should appear at least four times. If the logs only
contain generic timeout errors related to accessing external resources, such as
MongoDB, verify that the worker service account has permission to access the
subnetwork of the resource.

### Timeout in Polling Result File

For full information about troubleshooting a "Timeout in polling result file"
error, see [Troubleshoot Flex
Templates](/dataflow/docs/guides/troubleshoot-templates).

### Write Correct File/Write/WriteImpl/PreFinalize failed

When running a job, the job fails intermittently, and the following error
occurs:

```
Workflow failed. Causes: S27:Write Correct File/Write/WriteImpl/PreFinalize failed., Internal Issue (ID): ID:ID, Unable to expand file pattern gs://BUCKET_NAME/temp/FILE
```

This error occurs when the same subfolder is used as the temporary storage
location for multiple jobs that run concurrently.

To resolve this issue, don't use the same subfolder as the temporary storage
location for multiple pipelines. For each pipeline, provide a unique subfolder
to use as the temporary storage location.

### Element exceeds maximum protobuf message size

When you run Dataflow jobs and your pipeline has large elements, you
might see errors similar to the following examples:

```
Exception serializing message!
ValueError: Message org.apache.beam.model.fn_execution.v1.Elements exceeds maximum protobuf size of 2GB
```

Or:

```
Buffer size ... exceeds GRPC limit 2147483548. This is likely due to a single element that is too large.
```

Or:

```
Output element size exceeds the allowed limit. (... > 83886080) See https://cloud.google.com/dataflow/quotas#limits for more details.
```

You might also see a warning similar to the following example:

```
Data output stream buffer size ... exceeds 536870912 bytes. This is likely due to a large element in a PCollection.
```

These errors occur when your pipeline contains large elements.

To resolve this issue, if you use the Python SDK, upgrade to Apache Beam
version 2.57.0 or later. The Python SDK versions 2.57.0 and later [improve the
processing of large elements](https://github.com/apache/beam/issues/31607) and
add relevant logging.

If the errors persist after upgrading or if you're not using the Python SDK,
identify the step in the job where the error happens, and try to reduce the size
of the elements in that step.

When `PCollection` objects in your pipeline have large elements, the RAM
requirements for the pipeline increase. Large elements can also cause runtime
errors, especially when they cross the boundaries of fused stages.

Large elements can occur when a pipeline inadvertently materializes a large
iterable. For example, a pipeline that passes the output of a `GroupByKey`
operation into an unnecessary `Reshuffle` operation materializes lists as single
elements. These lists potentially contain a large number of values for each key.

If the error happens in a step that uses a side input, be aware that using side
inputs can introduce a fusion barrier. Check whether the transform that produces
a large element and the transform that consumes it belong to the same stage.

When constructing your pipeline, follow these best practices:

- In `PCollections` use multiple small elements instead of a single large
  element.
- Store large blobs in external storage systems. Either use `PCollections` to
  pass their metadata, or use a custom coder that reduces the size of the
  element.
- If you must pass a PCollection that can exceed 2 GB as a side input, use
  iterable views, such as `AsIterable` and `AsMultiMap`.

The maximum size for a single element in a Dataflow job is limited
to 2 GB (or 80 MB for Streaming Engine). For more information, see
[Quotas and limits](/dataflow/quotas#limits).

### Dataflow is unable to process managed transform(s)...

Pipelines that use [Managed I/O](/dataflow/docs/guides/managed-io) might fail
with this error if Dataflow can't [automatically
upgrade](/dataflow/docs/guides/managed-io#upgrades) the I/O transforms to the
latest supported version. The URN and the step names provided in the error
should specify which exact transforms Dataflow
failed to upgrade.

You might find additional details regarding this error in
[Logs Explorer](/logging/docs/view/logs-explorer-interface) under
Dataflow log names `managed-transforms-worker` and
`managed-transforms-worker-startup`.

If Logs Explorer does not provide adequate information to troubleshoot the
error, please contact [Cloud Customer Care](/support).

## Archive job errors

The following sections contain common errors that you might encounter when you
try to [archive a Dataflow
job](/dataflow/docs/guides/stopping-a-pipeline#archive) by using the API.

### No value is provided

When you try to archive a Dataflow job by using the API, the following
error might occur:

```
The field mask specifies an update for the field job_metadata.user_display_properties.archived in job JOB_ID, but no value is provided. To update a field, please provide a field for the respective value.
```

This error occurs for one of the following reasons:

- The path specified for the `updateMask` field doesn't follow the correct
  format. This issue can occur due to typos.
- The [`JobMetadata`](/dataflow/docs/reference/rest/v1b3/projects.jobs#jobmetadata)
  isn't correctly specified. In the `JobMetadata` field, for
  `userDisplayProperties`, use the key-value pair `"archived":"true"`.

To resolve this error, verify that the command that you pass to the API matches
the required format. For more details, see [Archive a
job](/dataflow/docs/guides/stopping-a-pipeline#archive-jobs).

### The API does not recognize the value

When you try to archive a Dataflow job by using the API, the following
error might occur:

```
The API does not recognize the value VALUE for the field job_metadata.user_display_properties.archived for job JOB_ID. REASON: Archived display property can only be set to 'true' or 'false'
```

This error occurs when the value provided in the archive jobs key-value pair
isn't a supported value. The supported values for the archive jobs key-value
pair are `"archived":"true"` and `"archived":"false"`.

To resolve this error, verify that the command that you pass to the API matches
the required format. For more details, see [Archive a
job](/dataflow/docs/guides/stopping-a-pipeline#archive-jobs).

### Cannot update both state and mask

When you try to archive a Dataflow job by using the API, the following
error might occur:

```
Cannot update both state and mask.
```

This error occurs when you try to update both the [job
state](/dataflow/docs/reference/rpc/google.dataflow.v1beta3#google.dataflow.v1beta3.JobState)
and the archive status in the same API call. You can't make updates to both the
job state and the
[updateMask](/dataflow/docs/reference/rest/v1b3/projects.jobs/update#query-parameters)
query parameter in the same API call.

To resolve this error, update the job state in a separate API call. Make updates
to the job state before updating the job archive status.

### Workflow modification failed

When you try to archive a Dataflow job by using the API, the following
error might occur:

```
Workflow modification failed.
```

This error usually occurs when you try to archive a job that is running.

To resolve this error, wait until the job completes before archiving it.
Completed jobs have one of the following [job
states](/dataflow/docs/reference/rpc/google.dataflow.v1beta3#google.dataflow.v1beta3.JobState):

- `JOB_STATE_CANCELLED`
- `JOB_STATE_DRAINED`
- `JOB_STATE_DONE`
- `JOB_STATE_FAILED`
- `JOB_STATE_UPDATED`

For more information, see [Detect Dataflow job
completion](/dataflow/docs/guides/stopping-a-pipeline#job-completion).

## Container image errors

The following sections contain common errors that you might encounter when using
custom containers and steps for resolving or troubleshooting the errors. The
errors are typically prefixed with the following message:

```
Unable to pull container image due to error: DETAILED_ERROR_MESSAGE
```

### Permission "containeranalysis.occurrences.list" denied

The following error appears in your log files:

```
Error getting old patchz discovery occurrences: generic::permission_denied: permission "containeranalysis.occurrences.list" denied for project "PROJECT_ID", entity ID "" [region="REGION" projectNum=PROJECT_NUMBER projectID="PROJECT_ID"]
```

Container Analysis API isn't enabled. In some cases, the Container Analysis API
is required for vulnerability scanning.

API.

**Note:** This API is automatically enabled by the [Container
Scanning](/artifact-analysis/docs/enable-container-scanning) API.

For more information, see [OS scanning
overview](/artifact-analysis/docs/os-overview) and [Configuring access
control](/artifact-analysis/docs/ca-access-control) in the
Artifact Analysis documentation.

### Error syncing pod ... failed to "StartContainer"

The following error occurs during worker startup:

```
Error syncing pod POD_ID, skipping: [failed to "StartContainer" for CONTAINER_NAME with CrashLoopBackOff: "back-off 5m0s restarting failed container=CONTAINER_NAME pod=POD_NAME].
```

A pod is a colocated group of Docker containers running on a
Dataflow worker. This error occurs when one of the Docker
containers in the pod fails to start. If the failure is not recoverable, the
Dataflow worker isn't able to start, and Dataflow
batch jobs eventually fail with errors like the following:

```
The Dataflow job appears to be stuck because no worker activity has been seen in the last 1h.
```

This error typically occurs when one of the containers is continuously crashing
during startup.

**Note:** If you see a `Dataflow job appears to be stuck` error when a single worker
is repeatedly started and then stopped after a few minutes, the issue is likely
a networking issue. For more information, see [Single worker is repeatedly
started and
stopped](/dataflow/docs/guides/troubleshoot-networking#one-worker-repeatedly-stopped).

To understand the root cause, look for the logs captured immediately prior to
the failure. To analyze the logs, use the
[Logs Explorer](/logging/docs/view/logs-explorer-interface). In the
Logs Explorer, limit the log files to log entries emitted from the worker
with container startup errors. To limit the log entries, complete the following
steps:

1. In the Logs Explorer, find the `Error syncing pod` log entry.
2. To see the labels associated with the log entry, expand the log entry.
3. Click the label associated with the `resource_name`, and then click **Show
   matching entries**.

![The Logs Explorer page with the steps for limiting log files
highlighted.](/static/dataflow/images/log-explorer-pod-error.png)

In the Logs Explorer, the Dataflow logs are organized into
several log streams. The `Error syncing pod` message is emitted in the log named
`kubelet`. However, the logs from the failing container could be in a different
log stream. Each container has a name. Use the following table to determine
which log stream might contain logs relevant to the failing container.

| Container name                        | Log names                |
| ------------------------------------- | ------------------------ |
| sdk, sdk0, sdk1, sdk-0-0, and similar | docker                   |
| harness                               | harness, harness-startup |
| python, java-batch, java-streaming    | worker-startup, worker   |
| artifact                              | artifact                 |

When you query the Logs Explorer, make sure that the query either includes
the relevant log names [in the query builder
interface](/logging/docs/view/building-queries#query-builder-menus) or does not
have restrictions on the log name.

![A Logs Explorer query that includes the relevant log
names.](/static/dataflow/images/logs-explorer-query.png)

After you select the relevant logs, the query result might look like the
following example:

```
resource.type="dataflow_step"
resource.labels.job_id="2022-06-29_08_02_54-JOB_ID"
labels."compute.googleapis.com/resource_name"="testpipeline-jenkins-0629-DATE-cyhg-harness-8crw"
logName=("projects/apache-beam-testing/logs/dataflow.googleapis.com%2Fdocker"
OR
"projects/apache-beam-testing/logs/dataflow.googleapis.com%2Fworker-startup"
OR
"projects/apache-beam-testing/logs/dataflow.googleapis.com%2Fworker")
```

Because the logs reporting the symptom of the container failure are sometimes
reported as `INFO`, include `INFO` logs in your analysis.

Typical causes of container failures include the following:

1. Your Python pipeline has additional dependencies that are installed at
   runtime, and the installation is unsuccessful. You might see errors like
   `pip install failed with error`. This issue might occur due to conflicting
   requirements, or due to a restricted networking configuration that prevents
   a Dataflow worker from pulling an external dependency from a
   public repository over the internet.
2. A worker fails in the middle of the pipeline run due to an out of memory
   error. You might see an error like one of the following:
   - `java.lang.OutOfMemoryError: Java heap space`
   - `Shutting down JVM after 8 consecutive periods of measured GC thrashing.
Memory is used/total/max = 24453/42043/42043 MB, GC last/max =
58.97/99.89 %, #pushbacks=82, gc thrashing=true. Heap dump not written.`

   To debug an out of memory issue, see [Troubleshoot Dataflow
   out of memory errors](/dataflow/docs/guides/troubleshoot-oom).

3. Dataflow is unable to pull the container image. For more
   information, see [Image pull request failed with
   error](#error-pulling-container-image).
4. The container used is not compatible with the worker VM's CPU architecture.
   In the harness startup logs, you might see an error like the following: `exec
/opt/apache/beam/boot: exec format error`. To check the container image's
   architecture, run `docker image inspect $IMAGE:$TAG` and look for the
   `Architecture` key word. If it says `Error: No such image: $IMAGE:$TAG`, you
   might need to pull the image first by running `docker pull $IMAGE:$TAG`. For
   information on building multi-architecture images, see [Build a
   multi-architecture container
   image](/dataflow/docs/guides/multi-architecture-container).

After you identify the error causing the container to fail, try to address the
error, and then resubmit the pipeline.

### Template launch failed with error

During flex template startup, following error appears in job logs:

```
Error: Template launch failed: exit status 13
Error occurred in the launcher container: Template launch failed. See console logs.
```

Worker logs contain stacktrace similar to following trace logs:

```
TypeError: canonicalize_version() got an unexpected keyword argument 'strip_trailing_zero'
ERROR:absl:Internal Error Type : RuntimeError
ERROR:absl:Error Message : Full trace: Traceback (most recent call last):
File "/usr/local/lib/python3.9/site-packages/apache_beam/utils/processes.py", line 89, in check_output
out = subprocess.check_output(*args, **kwargs)
IFile "/usr/local/lib/python3.9/subprocess.py", line 424, in check_output
return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,
File "/usr/local/lib/python3.9/subprocess.py", line 528, in run
raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command '['/usr/local/bin/python', 'setup.py', 'sdist', '--dist-dir', '/tmp/tmp196n6g8d']' returned non-zero exit status 1.
```

These errors occur if a template launcher finds conflicting dependencies [during
setup](https://github.com/pypa/setuptools/issues/4496), specifically when the
`setuptools` package is updated to a version higher or equal to `71.0`. Review
your pipeline's dependencies and make sure the packaging dependency is higher or
equal to `25.0`.

### Image pull request failed with error

During worker startup, one of the following errors appears in the worker or job
logs:

```
Image pull request failed with error
```

```
pull access denied for IMAGE_NAME
```

```
manifest for IMAGE_NAME not found: manifest unknown: Failed to fetch
```

```
Get IMAGE_NAME: Service Unavailable
```

These errors occur if a worker is unable to start up because the worker can't
pull a Docker container image. This issue happens in the following scenarios:

- The custom SDK container image URL is incorrect
- The worker lacks credential or network access to the remote image

To resolve this issue:

- If you're using a custom container image with your job, verify that your
  image URL is correct and has a valid tag or digest. The
  Dataflow workers also need access to the image.
- Verify that public images can be pulled locally by running `docker pull
$image` from an unauthenticated machine.

For private images or private workers:

- If you're using Container Registry to host your container image, it is
  recommended that you use Artifact Registry instead. Effective May 15, 2023,
  Container Registry is deprecated. If you use Container Registry, you can
  [transition to
  Artifact Registry](/artifact-registry/docs/transition/transition-from-gcr). If
  your images are in a different project than the one used to run your
  Google Cloud Platform job, [configure access
  control](/container-registry/docs/access-control) for the default
  Google Cloud Platform service account.
- If using shared Virtual Private Cloud (VPC), make sure that workers [can
  access](/dataflow/docs/guides/routes-firewall) the custom container
  repository host.
- Use `ssh` to connect with a running job worker VM and run `docker pull
$image` to directly confirm that the worker is configured properly.

If workers fail several times in a row due to this error and work has started on
a job, the job can fail with an error similar to the following message:

```
Job appears to be stuck.
```

If you remove access to the image while the job is running, either by removing
the image itself or revoking the Dataflow worker
Service Account Credentials or internet access to access images,
Dataflow only logs errors. Dataflow doesn't fail the
job. Dataflow also avoids failing long-running streaming pipelines
to avoid losing pipeline state.

Other possible errors can arise from repository quota issues or outages. If you
experience issues exceeding the [Docker Hub
quota](https://docs.docker.com/docker-hub/download-rate-limit/) for pulling
public images or general third-party repository outages, consider using [Artifact Registry](/artifact-registry/docs/overview) as the image repository.

### SystemError: unknown opcode

Your Python custom container pipeline might fail with the following error
immediately after job submission:

```
SystemError: unknown opcode
```

In addition, the stack trace might include

```
apache_beam/internal/pickler.py
```

To resolve this issue, verify that the Python version that you're using locally
matches the version in the container image up to the major and minor version.
The difference in the patch version, such as 3.6.7 versus 3.6.8, does not create
compatibility issues. The difference in minor version, such as 3.6.8 versus
3.8.2, can cause pipeline failures.

## Upgrade streaming pipeline errors

For information on how to resolve errors when you upgrade a streaming pipeline
using features such as running a parallel replace job, see [Troubleshoot
Streaming pipeline
upgrades](/dataflow/docs/guides/troubleshoot-streaming-upgrade).

### Runner v2 harness update

The following info message appears in the job logs of a Runner v2 job

```
The Dataflow RunnerV2 container image of this job's workers will be ready for update in 7 days.
```

This means that the version of the runner harness process will be automatically
updated at some point 7 days after the initial delivery of the message,
resulting in a brief pause in processing. If you want to control when this pause
occurs, see [Update an existing
pipeline](/dataflow/docs/guides/updating-a-pipeline) to start a replacement job
which will have the most recent version of the runner harness.

## Worker errors

The following sections contain common worker errors that you might encounter and
steps for resolving or troubleshooting the errors.

### Call from Java worker harness to Python DoFn fails with error

If a call from the Java worker harness to a Python `DoFn` fails, a relevant
error message is displayed.

To investigate the error, expand the
[Cloud Monitoring](/dataflow/docs/guides/using-cloud-monitoring) error log
entry and look at the error message and traceback. It shows you which code
failed so you can correct it if necessary. If you believe that the error is a
bug in Apache Beam or Dataflow, [report the
bug](/dataflow/docs/support/getting-support).

### EOFError: marshal data too short

The following error appears in the worker logs:

```
EOFError: marshal data too short
```

This error sometimes occurs when Python pipeline workers run out of disk space.

To resolve this issue, see [No space left on device](#no-space-left).

### Failed to attach disk

When you try to launch a Dataflow job that uses [C3
VMs](/compute/docs/general-purpose-machines#c3_series) with Persistent Disk, the job
fails with one or both of the following errors:

```
Failed to attach disk(s), status: generic::invalid_argument: One or more operations had an error
```

```
Can not allocate sha384 (reason: -2), Spectre V2 : WARNING: Unprivileged eBPF is enabled with eIBRS on...
```

These errors occur when you use C3 VMs with an unsupported Persistent Disk type. For
more information, see [Supported disk types for
C3](/compute/docs/general-purpose-machines#c3_disks).

To use C3 VMs with your Dataflow job, choose the `pd-ssd` worker
disk type. For more information, see [Worker-level
options](/dataflow/docs/reference/pipeline-options#worker-level_options).

### Java

`--workerDiskType=pd-ssd`

### Python

`--worker_disk_type=pd-ssd`

### Go

`disk_type=pd-ssd`

### No space left on device

When a job runs out of disk space, the following error might appear in the
worker logs:

```
No space left on device
```

This error can occur for one of the following reasons:

- The worker persistent storage runs out of free space, which can occur for
  one of the following reasons:
  - A job downloads large dependencies at runtime
  - A job uses large custom containers
  - A job writes many temporary data to local disk
- When using [Dataflow
  Shuffle](/dataflow/docs/shuffle-for-batch), Dataflow sets
  [lower default disk
  size](/dataflow/docs/guides/deploying-a-pipeline#disk-considerations). As a
  result, this error might occur with jobs moving from worker-based shuffle.
- The worker boot disk fills up because it's logging more than 50 entries per
  second.

To resolve this issue, follow these troubleshooting steps:

To see disk resources associated with a single worker, look up VM instance
details for worker VMs associated with your job. Part of the disk space is
consumed by the operating system, binaries, logs, and containers.

To increase persistent disk or boot disk space, adjust the [disk size pipeline
option](/dataflow/docs/reference/pipeline-options#worker-level_options).

Track disk space usage on the worker VM instances by using Cloud Monitoring.
See [Receive worker VM metrics from the Monitoring
agent](/dataflow/docs/guides/using-cloud-monitoring#receive_worker_vm_metrics_from_the_agent)
for instructions explaining how to set this up.

Look for boot disk space issues by [Viewing serial port
output](/compute/docs/instances/viewing-serial-port-output#viewing_serial_port_output)
on the worker VM instances and looking for messages like:

```
Failed to open system journal: No space left on device
```

If you have many worker VM instances, you can create a script to run `gcloud
compute instances get-serial-port-output` on all of them at once. You can review
that output instead.

### Python pipeline fails after one hour of worker inactivity

When using the Apache Beam SDK for Python with Dataflow Runner
V2 on worker machines with many CPU cores, use Apache Beam SDK 2.35.0 or
later. If your job uses a custom container, use Apache Beam SDK 2.46.0 or
later.

Consider pre-building your Python container. This step can improve VM startup
times and horizontal autoscaling performance. To use this feature, enable the
Cloud Build API on your project and submit your pipeline with the following
parameter:

`‑‑prebuild_sdk_container_engine=cloud_build`.

For more information, see [Dataflow Runner
V2](/dataflow/docs/runner-v2).

You can also [use a custom container
image](/dataflow/docs/guides/using-custom-containers) with all dependencies
preinstalled.

### RESOURCE_POOL_EXHAUSTED

When you create a Google Cloud Platform resource, the following error occurs:

```
Startup of the worker pool in zone ZONE_NAME failed to bring up any of the desired NUMBER workers.
ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS: Instance 'INSTANCE_NAME' creation failed: The zone 'projects/PROJECT_ID/zones/ZONE_NAME' does not have enough resources available to fulfill the request. '(resource type:RESOURCE_TYPE)'.
```

This error occurs due to a temporary lack of availability for a specific
resource in a specific zone.

To resolve the issue, you can either wait, or you can create the same resource
in another zone.

As a workaround, implement a retry loop for your jobs, so that when a stock out
error occurs, the job automatically retries until resources are available. To
create a retry loop, implement the following workflow:

1. Create a Dataflow job, and get the job ID.
2. Poll the job status until the job status is `RUNNING` or `FAILED`.
   - If the job status is `RUNNING`, exit the retry loop.
   - If the job status is `FAILED`, use the Cloud Logging API to query the job
     logs for the string `ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS`. For more
     information, see [Work with pipeline
     logs](/dataflow/docs/guides/logging).
     - If the logs don't contain the string, exit the retry loop.
     - If the logs contain the string, create a Dataflow
       job, get the job ID, and restart the retry loop.

As a best practice, distribute your resources across [multiple zones and
regions](/compute/docs/regions-zones#choosing_a_region_and_zone) to tolerate
outages.

### Runtime dependency errors

When you run a Dataflow job that uses the Apache Beam SDK for
Python with cross-language transforms, the job might fail with an `HTTP Error
403: Forbidden` error when downloading JAR files from Maven Central.

This issue is caused by a change in Maven Central's CDN provider, which blocks
requests from the Python `urllib` library used by the Apache Beam SDK.

To resolve this issue, upgrade to Apache Beam version 2.69.0 or later. If
you can't upgrade, see the workarounds in this section.

#### Fixes in Apache Beam 2.69.0 and later

Apache Beam 2.69.0 and later includes the following fixes:

- **Custom Maven Repository URL**: You can specify a custom Maven repository
  by using the `--maven_repository_url` pipeline option. For example:

  ```
  --maven_repository_url https://maven-central.storage-download.googleapis.com/maven2/
  ```

- **User-Agent Identification**: The Apache Beam SDK sends a specific
  `User-Agent` header to prevent requests from being blocked.

#### Workarounds for older SDKs

If you can't upgrade to Apache Beam 2.69.0 or later, use one of the
following workarounds:

- **Pre-package JARs in a custom container (Recommended)**: Pre-package the
  required JAR files in your [custom container
  image](/dataflow/docs/guides/using-custom-containers). Place the JARs in the
  Apache Beam cache directory (`/root/.apache_beam/cache/jars/`) to
  prevent the SDK from downloading them at runtime.
- **Use Google's Maven mirror**: Use the `--expansion_service` pipeline option
  to instruct the Apache Beam SDK to download the necessary JARs from
  Google's mirror of Maven Central. For example:

  ```
  --expansion_service https://maven-central.storage-download.googleapis.com/maven2/org/apache/beam/beam-sdks-java-extensions-schemaio-expansion-service/BEAM_VERSION/beam-sdks-java-extensions-schemaio-expansion-service-BEAM_VERSION.jar
  ```

- **Stage JARs in Cloud Storage**: Download the required JARs, stage them in a
  Cloud Storage bucket, and then provide the Cloud Storage path of the
  JAR to the `--expansion_service` pipeline option.

### Instances with guest accelerators do not support live migration

A Dataflow pipeline fails at job submission with the following
error:

```
UNSUPPORTED_OPERATION: Instance <worker_instance_name> creation failed:
Instances with guest accelerators do not support live migration
```

This error might occur when you have requested a worker machine type that has
hardware accelerators, but you have not configured Dataflow to use
accelerators.

Use the `--worker_accelerator` Dataflow
[service option](/dataflow/docs/reference/service-options) or the `accelerator`
[resource hint](/dataflow/docs/guides/right-fitting#use_resource_hints) to
request hardware accelerators.

If you use Flex templates, you can use the `--additionalExperiments` option to
supply Dataflow service options. If done correctly, the
`worker_accelerator` option can be found in the job's **Job info panel** in the
Google Cloud console.

### Project quota ... or access control policies preventing the operation

The following error occurs:

```
Startup of the worker pool in zone ZONE_NAME failed to bring up any of the desired NUMBER workers. The project quota may have been exceeded or access control policies may be preventing the operation; review the Cloud Logging 'VM Instance' log for diagnostics.
```

This error occurs for one of the following reasons:

- You have exceeded one of the Compute Engine quotas that Dataflow
  worker creation relies on.
- Your organization has [constraints](/resource-manager/docs/organization-policy/using-constraints)
  in place that prohibit some aspect of the VM instance creation process, like
  the account being used, or the zone being targeted.

To resolve this issue, follow these troubleshooting steps:

**Review the VM Instance log**

1. Go to the [Cloud Logging viewer](https://console.cloud.google.com/logs/viewer)
2. In the **Audited Resource** drop-down list, select **VM Instance**.
3. In the **All logs** drop-down list, select
   **compute.googleapis.com/activity_log**.
4. Scan the log for any entries related to VM instance creation failure.

**Check your usage of Compute Engine quotas**

1. To view Compute Engine resource usage compared to [Dataflow
   quotas](/dataflow/quotas#compute-engine-quotas) for the zone you're
   targeting, run the following command:

   `gcloud compute regions describe [REGION]`

2. Review the results for the following resources to see if any are exceeding
   quota:
   - CPUS
   - DISKS_TOTAL_GB
   - IN_USE_ADDRESSES
   - INSTANCE_GROUPS
   - INSTANCES
   - REGIONAL_INSTANCE_GROUP_MANAGERS

3. If needed, [request a quota change](/compute/quotas#request_quotas).

**Review your organization policy constraints**

1. Go to the [Organization policies page](https://console.cloud.google.com/iam-admin/orgpolicies/list)
2. Review the constraints for any that might limit VM instance creation for
   either the account you're using (by default, the [Dataflow service
   account](/dataflow/docs/concepts/security-and-permissions#cloud_dataflow_service_account))
   or in the zone that you're targeting.
3. If you have a policy that restricts the use of external IP addresses, turn
   off external IP addresses for this job. For more information about turning
   off external IP addresses, see [Configure internet access and firewall
   rules](/dataflow/docs/guides/routes-firewall#turn_off_external_ip_address).

### Timed out waiting for an update from the worker

When a Dataflow job fails, the following error occurs:

```
Root cause: Timed out waiting for an update from the worker. For more information, see https://cloud.google.com/dataflow/docs/guides/common-errors#worker-lost-contact.
```

Several causes can lead to this error, including the following:

- [Worker overload](#worker-overload)
- [Holding the Global Interpreter Lock](#python-gil)
- [Long-running DoFn setup](#dofn-setup)

#### Worker overload

Sometimes, a time-out error occurs when the worker runs out of memory or swap
space. To resolve this issue, as a first step, try running the job again. If the
job still fails and the same error occurs, try using a worker with more memory
and disk space. For example, add the following pipeline startup option:

`--worker_machine_type=m1-ultramem-40 --disk_size_gb=500`

Changing the worker type could affect billed cost. For more information, see
[Troubleshoot Dataflow out of memory
errors](/dataflow/docs/guides/troubleshoot-oom).

This error can also occur when your data contains a hot key. In this scenario,
CPU utilization is high on some workers during most of the duration of the job.
However, the number of workers does not reach the maximum allowed. For more
information about hot keys and possible solutions, see [Writing
Dataflow pipelines with scalability in
mind](https://cloud.google.com/blog/products/gcp/writing-dataflow-pipelines-with-scalability-in-mind).

For additional solutions to this issue, see [A hot key ... was
detected](#hot-key-detected).

#### Python: Global Interpreter Lock (GIL)

If your Python code calls C/C++ code by using the [Python extension
mechanism](https://docs.python.org/3/extending/extending.html), check whether
the extension code releases the Python Global Interpreter Lock (GIL) in
computationally intensive parts of code that don't access Python state. If the
GIL is not released for a prolonged period of time, you might see error messages
like: `Unable to retrieve status info from SDK harness <...> within allowed time`
and `SDK worker appears to be permanently unresponsive. Aborting the SDK`.

The libraries that facilitate interactions with extensions like
[Cython](https://cython.readthedocs.io/en/latest/src/userguide/external_C_code.html#nogil),
and
[PyBind](https://pybind11.readthedocs.io/en/stable/advanced/misc.html#global-interpreter-lock-gil)
have primitives to control GIL status. You can also manually release the GIL and
reacquire it before returning control to the Python interpreter by using the
`Py_BEGIN_ALLOW_THREADS` and `Py_END_ALLOW_THREADS` macros. For more
information, see [Thread State and the Global Interpreter
Lock](https://docs.python.org/3/c-api/init.html#thread-state-and-the-global-interpreter-lock)
in the Python documentation.

It might be possible to retrieve stacktraces of a thread that is holding the GIL
on a running Dataflow worker as follows:

```
# SSH into a running Dataflow worker VM that is currently a straggler, for example:
gcloud compute ssh --zone "us-central1-a" "worker-that-emits-unable-to-retrieve-status-messages" --project "project-id"

# Install nerdctl to inspect a running container with ptrace privileges.
wget https://github.com/containerd/nerdctl/releases/download/v2.0.2/nerdctl-2.0.2-linux-amd64.tar.gz
sudo tar Cxzvvf /var/lib/toolbox  nerdctl-2.0.2-linux-amd64.tar.gz
alias nerdctl="sudo /var/lib/toolbox/nerdctl -n k8s.io"

# Find a container running the Python SDK harness.
CONTAINER_ID=`nerdctl ps | grep sdk-0-0 | awk '{print $1}'`

# Start a shell in the running container.
nerdctl exec --privileged -it $CONTAINER_ID /bin/bash

# Inspect python processes in the running container.
ps -A | grep python
PYTHON_PID=$(ps -A | grep python | head -1 | awk '{print $1}')

# Use pystack to retrieve stacktraces from the python process.
pip install pystack

pystack remote --native $PYTHON_PID

# Find which thread holds the GIL and inspect the stacktrace.
pystack remote --native $PYTHON_PID | grep -iF "Has the GIL" -A 100

# Alternately, use inspect with gdb.
apt update && apt install -y gdb
gdb --quiet \
  --eval-command="set pagination off" \
  --eval-command="thread apply all bt" \
  --eval-command "set confirm off" \
  --eval-command="quit"  -p $PYTHON_PID
```

In Python pipelines, in the default configuration, Dataflow
assumes that each Python process running on the workers efficiently uses one
vCPU core. If the pipeline code bypasses the GIL limitations, such as by using
libraries that are implemented in C++, processing elements might use resources
from more than one vCPU core, and the workers might not get enough CPU
resources. To work around this issue, [reduce the number of
threads](/dataflow/docs/guides/troubleshoot-oom#reduce-threads) on the workers.

#### Long-running DoFn setup

If you are not using Runner v2, then a long-running call to `DoFn.Setup` can
lead to the following error:

```
Timed out waiting for an update from the worker
```

In general, avoid time-consuming operations inside `DoFn.Setup`.

### Transient errors publishing to topic

When your streaming job uses the at-least-once streaming mode and publishes to a
Pub/Sub sink, the following error appears in the job logs:

```
There were transient errors publishing to topic
```

If your job runs correctly, this error is benign, and you can ignore it.
Dataflow automatically retries sending the Pub/Sub
messages with a backoff delay.

### Unable to fetch data due to token mismatch for key

The following error means the work item being processed has been reallocated to
another worker:

`Unable to fetch data due to token mismatch for key`

This most commonly occurs during autoscaling, but can happen at any time. Any
work impacted will be retried. You can ignore this error.

### Java dependency issues

Incompatible classes and libraries can cause Java dependency issues. When your
pipeline has Java dependency issues, one of the following errors might occur:

- `NoClassDefFoundError`: This error occurs when an entire class is not
  available during runtime. It can be caused either by general configuration
  issues or by incompatibilities between Beam's protobuf version and a
  client's generated protos (for example, [this
  issue](https://github.com/GoogleCloudPlatform/DataflowTemplates/issues/2191)).
  - `NoSuchMethodError`: This error occurs when the class in the classpath
    uses a version that doesn't contain the correct method or when the
    method signature changed.
- `NoSuchFieldError`: This error occurs when the class in the classpath uses a
  version that doesn't have a field required during runtime.
- `FATAL ERROR in native method`: This error occurs when a built-in dependency
  can't be loaded properly. When using uber JAR (shaded), don't include
  libraries that use signatures (such as Conscrypt) in the same JAR.

If your pipeline contains user-specific code and settings, the code can't
contain mixed versions of libraries. If you're using a dependency management
library, we recommend that you use [Google Cloud Platform Libraries BOM](/java/docs/bom).

If you're using the Apache Beam SDK, to import the correct libraries BOM,
use `beam-sdks-java-io-google-cloud-platform-bom`:

### Maven

### Gradle

For more information, see [Manage pipeline dependencies in
Dataflow](/dataflow/docs/guides/manage-dependencies#java).

### InaccessibleObjectException in JDK 17 and later

When you run pipelines with the Java Platform, Standard Edition Development Kit
(JDK) versions 17 and later, the following error might appear in the worker log
files:

```
Unable to make protected METHOD accessible:
    module java.MODULE does not "opens java.MODULE" to ...
```

This issue occurs because starting in Java version 9, open module Java virtual
machine (JVM) options are needed to access JDK internals. In Java 16 and later
versions, open module JVM options are always required to access JDK internals.

To resolve this issue, when you pass modules to your Dataflow
pipeline to open, use the format
`MODULE/PACKAGE=TARGET_MODULE(,TARGET_MODULE)*`
with the `jdkAddOpenModules` pipeline option. This format allows access to the
necessary library.

For example, if the error is `module java.base does not "opens java.lang" to
unnamed module @...`, then include the following pipeline option when you run
your pipeline:

```
--jdkAddOpenModules=java.base/java.lang=ALL-UNNAMED
```

For more information, see the
[`DataflowPipelineOptions`](https://beam.apache.org/documentation/sdks/javadoc/current/index.html?org/apache/beam/runners/dataflow/options/DataflowPipelineOptions.html)
class documentation.

### Error reporting workitem progress

For Java pipelines, if you are not using Runner V2, you might see the following
error:

```
Error reporting workitem progress update to Dataflow service: ...
```

This error is caused by an unhandled exception during a work item progress
update, such as during splitting of a source. In most cases, if Apache Beam
user code throws an unhandled exception, the work item fails, causing the
pipeline to fail.l However, exceptions in `Source.split` are suppressed, because
that part of the code is outside of a work item. As a result, only an error log
is recorded.

This error is usually harmless if it occurs only intermittently. However,
consider gracefully handling exceptions inside of your `Source.split` code.

## BigQuery connector errors

The following sections contain common BigQuery connector errors that
you might encounter and steps for resolving or troubleshooting the errors.

### quotaExceeded

When using the BigQuery connector to write to BigQuery using
streaming inserts, write throughput is lower than expected, and the following
error might occur:

```
quotaExceeded
```

Slow throughput might be due to your pipeline exceeding the available
BigQuery streaming insert quota. If so, quota related error messages
from BigQuery appear in the Dataflow
worker logs (look for `quotaExceeded` errors).

If you see `quotaExceeded` errors, to resolve this issue:

- When using the Apache Beam SDK for Java, set the BigQuery sink
  option `ignoreInsertIds()`.
- When using the Apache Beam SDK for Python, use the `ignore_insert_ids`
  option.

These settings make you eligible for a one GB per sec, per-project
BigQuery streaming insert throughput. For more information on caveats
related to automatic message deduplication, see the [BigQuery
documentation](/bigquery/streaming-data-into-bigquery#disabling_best_effort_de-duplication).
To increase the BigQuery streaming insert quota higher than one
GBps, [submit a request through the
Google Cloud console](https://console.cloud.google.com/iam-admin/quotas).

If you don't see quota related errors in worker logs, the issue might be that
default bundling or batching related parameters don't provide adequate
parallelism for your pipeline to scale. You can adjust several
Dataflow BigQuery connector related configurations to
achieve the expected performance when writing to BigQuery using
streaming inserts. For example, for Apache Beam SDK for Java, adjust
`numStreamingKeys` to match the maximum number of workers and consider
increasing `insertBundleParallelism` to configure BigQuery connector to
write to BigQuery using more parallel threads.

For configurations available in the Apache Beam SDK for Java, see
[BigQueryPipelineOptions](https://github.com/apache/beam/blob/master/sdks/java/io/google-cloud-platform/src/main/java/org/apache/beam/sdk/io/gcp/bigquery/BigQueryOptions.java),
and for configurations available in the Apache Beam SDK for Python, see the
[WriteToBigQuery
transform](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/io/gcp/bigquery.py).

### rateLimitExceeded

When using the BigQuery connector, the following error occurs:

```
rateLimitExceeded
```

This error occurs if too many BigQuery [API
requests](https://console.cloud.google.com/apis/api/bigquery.googleapis.com/quotas)
are sent during a short duration. BigQuery has short term quota
limits. It's possible for your Dataflow pipeline to temporarily
exceed such a quota. In this scenario, [API
requests](https://console.cloud.google.com/apis/api/bigquery.googleapis.com/quotas)
from your Dataflow pipeline to BigQuery might fail, which
could result in `rateLimitExceeded` errors in worker logs.

Dataflow retries such failures, so you can safely ignore these
errors. If you believe that your pipeline is affected by `rateLimitExceeded`
errors, contact [Cloud Customer Care](/support).

## Miscellaneous errors

The following sections contain miscellaneous errors that you might encounter and
steps for resolving or troubleshooting the errors.

### Can not allocate sha384

Your job runs correctly, but you see the following error in the job logs:

```
ima: Can not allocate sha384 (reason: -2)
```

If your job runs correctly, this error is benign, and you can ignore it. The
worker VM base images sometimes produce this message. Dataflow
automatically responds to and addresses the underlying issue.

A feature request exists to change the level of this message from `WARN` to
`INFO`. For more information, see [Lowering the Dataflow system
launch error log level to WARN or
INFO](https://issuetracker.google.com/262361831).

### Error initializing dynamic plugin prober

Your job runs correctly, but you see the following error in the job logs:

```
Error initializing dynamic plugin prober" err="error (re-)creating driver directory: mkdir /usr/libexec/kubernetes: read-only file system
```

If your job runs correctly, this error is benign, and you can ignore it. This
error occurs when the Dataflow job tries to create a directory
without the necessary write permissions, and the task fails. If your job
succeeds, the directory either wasn't needed, or Dataflow
addressed the underlying issue.

A feature request exists to change the level of this message from `WARN` to
`INFO`. For more information, see [Lowering the Dataflow system
launch error log level to WARN or
INFO](https://issuetracker.google.com/262361831).

### No such object: `pipeline.pb`

When listing jobs using the
[`JOB_VIEW_ALL`](/dataflow/docs/reference/rest/v1b3/JobView) option, the
following error occurs:

```
No such object: BUCKET_NAME/PATH/pipeline.pb
```

This error can occur if you delete the `pipeline.pb` file from the staging files
for the job.

### Skipping pod synchronization

Your job runs correctly, but you see one of the following errors in the job
logs:

```
Skipping pod synchronization" err="container runtime status check may not have completed yet"
```

Or:

```
Skipping pod synchronization" err="[container runtime status check may not have completed yet, PLEG is not healthy: pleg has yet to be successful]"
```

If your job runs correctly, these errors are benign, and you can ignore them.
The message `container runtime status check may not have completed yet` occurs
when the Kubernetes kubelet is skipping the synchronization of pods because it's
waiting for the container runtime to initialize. This scenario occurs for a
variety of reasons, such as when the container runtime has recently started or
is restarting.

The when the message includes `PLEG is not healthy: pleg has yet to be
successful`, the kubelet is waiting for the pod lifecycle event generator (PLEG)
to become healthy before synchronizing pods. The PLEG is responsible for
generating events that are used by the kubelet to track the state of pods.

A feature request exists to change the level of this message from `WARN` to
`INFO`. For more information, see [Lowering the Dataflow system
launch error log level to WARN or
INFO](https://issuetracker.google.com/262361831).

## Recommendations

For guidance on recommendations generated by Dataflow Insights,
see [Insights](/dataflow/docs/guides/using-dataflow-insights#insights).
