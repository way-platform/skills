---
source_url: https://beam.apache.org/documentation/runners/dataflow/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Cloud Dataflow Runner"
beam_last_updated: "Last updated on 2026/03/06"
---

# Using the Google Cloud Dataflow Runner

The Google Cloud Dataflow Runner uses the [Cloud Dataflow managed service](https://cloud.google.com/dataflow/service/dataflow-service-desc). When you run your pipeline with the Cloud Dataflow service, the runner uploads your executable code and dependencies to a Google Cloud Storage bucket and creates a Cloud Dataflow job, which executes your pipeline on managed resources in Google Cloud Platform.

The Cloud Dataflow Runner and service are suitable for large scale, continuous jobs, and provide:

- a fully managed service
- [autoscaling](https://cloud.google.com/dataflow/service/dataflow-service-desc#autoscaling) of the number of workers throughout the lifetime of the job
- [dynamic work rebalancing](https://cloud.google.com/blog/products/gcp/no-shard-left-behind-dynamic-work-rebalancing-in-google-cloud-dataflow)

The [Beam Capability Matrix](/documentation/runners/capability-matrix/) documents the supported capabilities of the Cloud Dataflow Runner.

## Cloud Dataflow Runner prerequisites and setup

To use the Cloud Dataflow Runner, you must complete the setup in the _Before you
begin_ section of the [Cloud Dataflow quickstart](https://cloud.google.com/dataflow/docs/quickstarts)
for your chosen language.

1. Select or create a Google Cloud Platform Console project.
2. Enable billing for your project.
3. Enable the required Google Cloud APIs: Cloud Dataflow, Compute Engine,
   Stackdriver Logging, Cloud Storage, Cloud Storage JSON, and Cloud Resource
   Manager. You may need to enable additional APIs (such as BigQuery, Cloud
   Pub/Sub, or Cloud Datastore) if you use them in your pipeline code.
4. Authenticate with Google Cloud Platform.
5. Install the Google Cloud SDK.
6. Create a Cloud Storage bucket.

### Specify your dependency

This section is not applicable to the Beam SDK for Python.

### Self executing JAR

This section is not applicable to the Beam SDK for Python.

## Pipeline options for the Cloud Dataflow Runner

When executing your pipeline with the Cloud Dataflow Runner (Python), consider these common pipeline options.

| Field               | Description                                                                                                                                                                                                                                                                                                                        | Default Value                                                                                                    |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `runner`            | The pipeline runner to use. This option allows you to determine the pipeline runner at runtime.                                                                                                                                                                                                                                    | Set to `dataflow` or `DataflowRunner` to run on the Cloud Dataflow Service.                                      |
| `project`           | The project ID for your Google Cloud Project.                                                                                                                                                                                                                                                                                      | If not set, defaults to the default project in the current environment. The default project is set via `gcloud`. |
| `region`            | The Google Compute Engine region to create the job.                                                                                                                                                                                                                                                                                | If not set, defaults to the default region in the current environment. The default region is set via `gcloud`.   |
| `streaming`         | Whether streaming mode is enabled or disabled; `true` if enabled. Set to `true` if running pipelines with unbounded `PCollection`s.                                                                                                                                                                                                | `false`                                                                                                          |
| `temp_location`     | Required. Path for temporary files. Must be a valid Google Cloud Storage URL that begins with `gs://`.                                                                                                                                                                                                                             | No default value.                                                                                                |
| `staging_location`  | Optional. Cloud Storage bucket path for staging your binary and any temporary files. Must be a valid Cloud Storage URL that begins with `gs://`.                                                                                                                                                                                   | If not set, defaults to a staging directory within `temp_location`.                                              |
| `save_main_session` | Save the main session state so that pickled functions and classes defined in `__main__` (e.g. interactive session) can be unpickled. Some workflows do not need the session state if, for instance, all of their functions/classes are defined in proper modules (not `__main__`) and the modules are importable in the worker.    | `false`                                                                                                          |
| `sdk_location`      | Override the default location from where the Beam SDK is downloaded. This value can be a URL, a Cloud Storage path, or a local path to an SDK tarball. Workflow submissions will download or copy the SDK tarball from this location. If set to the string `default`, a standard SDK location is used. If empty, no SDK is copied. | `default`                                                                                                        |

See the reference documentation for the
[`PipelineOptions`](https://beam.apache.org/releases/pydoc/2.71.0/apache_beam.options.pipeline_options.html#apache_beam.options.pipeline_options.PipelineOptions)
interface (and any subinterfaces) for additional pipeline configuration options.

## Additional information and caveats

### Monitoring your job

While your pipeline executes, you can monitor the job’s progress, view details on execution, and receive updates on the pipeline’s results by using the [Dataflow Monitoring Interface](https://cloud.google.com/dataflow/pipelines/dataflow-monitoring-intf) or the [Dataflow Command-line Interface](https://cloud.google.com/dataflow/pipelines/dataflow-command-line-intf).

### Blocking Execution

To block until your job completes, call `wait_until_finish` on the `PipelineResult` returned from `pipeline.run()`. The Cloud Dataflow Runner prints job status updates and console messages while it waits. While the result is connected to the active job, note that pressing **Ctrl+C** from the command line does not cancel your job. To cancel the job, you can use the [Dataflow Monitoring Interface](https://cloud.google.com/dataflow/pipelines/dataflow-monitoring-intf) or the [Dataflow Command-line Interface](https://cloud.google.com/dataflow/pipelines/dataflow-command-line-intf).

### Streaming Execution

If your pipeline uses an unbounded data source or sink, you must set the `streaming` option to `true`.

When using streaming execution, keep the following considerations in mind.

1. Streaming pipelines do not terminate unless explicitly cancelled by the user.
   You can cancel your streaming job from the [Dataflow Monitoring Interface](https://cloud.google.com/dataflow/pipelines/stopping-a-pipeline)
   or with the [Dataflow Command-line Interface](https://cloud.google.com/dataflow/pipelines/dataflow-command-line-intf)
   ([gcloud dataflow jobs cancel](https://cloud.google.com/sdk/gcloud/reference/dataflow/jobs/cancel)
   command).
2. Streaming jobs use a Google Compute Engine [machine type](https://cloud.google.com/compute/docs/machine-types)
   of `n1-standard-2` or higher by default. You must not override this, as
   `n1-standard-2` is the minimum required machine type for running streaming
   jobs.
3. Streaming execution [pricing](https://cloud.google.com/dataflow/pricing)
   differs from batch execution.
