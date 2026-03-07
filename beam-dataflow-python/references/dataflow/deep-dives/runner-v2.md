---
source_url: https://docs.cloud.google.com/dataflow/docs/runner-v2
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Use Dataflow Runner v2 \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

When you use Dataflow to run your pipeline, the
Dataflow runner uploads your pipeline code and dependencies to a
Cloud Storage bucket and creates a Dataflow job. This
Dataflow job runs your pipeline on managed resources in
Google Cloud Platform.

- For batch pipelines that use the Apache Beam Java SDK versions
  2.54.0 or later, Runner v2 is enabled by default.
- For pipelines that use the Apache Beam Java SDK, Runner v2 is required
  when running multi-language pipelines, using custom containers,
  or using Spanner or Bigtable change stream pipelines. In other
  cases, use the default runner.
- For pipelines that use the Apache Beam Python SDK versions
  2.21.0 or later, Runner v2 is enabled by default. For pipelines that use the
  Apache Beam Python SDK versions 2.45.0 and later, Dataflow
  Runner v2 is the only Dataflow runner available.
- For the Apache Beam SDK for Go, Dataflow Runner v2 is the
  only Dataflow runner available.

Runner v2 uses a services-based architecture that benefits
many pipelines:

- Dataflow Runner v2 lets you pre-build your Python
  container, which can improve VM startup times and Horizontal Autoscaling
  performance. For more information, see
  [Pre-build Python dependencies](/dataflow/docs/guides/build-container-image#prebuild).
- Dataflow Runner v2 supports
  [multi-language pipelines](https://beam.apache.org/documentation/programming-guide/#multi-language-pipelines),
  a feature that enables your Apache Beam pipeline to use transforms defined in
  other Apache Beam SDKs. Dataflow Runner v2 supports
  [using Java transforms from a Python SDK pipeline](https://beam.apache.org/documentation/sdks/python-multi-language-pipelines/)
  and
  [using Python transforms from a Java SDK pipeline](https://beam.apache.org/documentation/sdks/java-multi-language-pipelines/).
  When you run Apache Beam pipelines without Runner v2, the
  Dataflow runner uses language-specific workers.

## Limitations and restrictions

Dataflow Runner v2 has the following requirements and limitations:

- Dataflow Runner v2 requires [Streaming Engine](/dataflow/docs/streaming-engine)
  for streaming jobs.
- Because Dataflow Runner v2 requires Streaming Engine for
  streaming jobs, any Apache Beam transform that requires
  Dataflow Runner v2 also requires the use of Streaming Engine
  for streaming jobs. For example, the [Pub/Sub Lite I/O
  connector](https://beam.apache.org/releases/pydoc/current/apache_beam.io.gcp.pubsublite.html)
  for the Apache Beam SDK for Python is a cross-language transform that
  requires Dataflow Runner v2. If you try to disable Streaming
  Engine for a job or template that uses this transform, the job fails.
- For streaming pipelines that use the Apache Beam Java SDK, the classes
  [`MapState`](https://beam.apache.org/releases/javadoc/current/index.html?org/apache/beam/sdk/state/MapState.html)
  and
  [`SetState`](https://beam.apache.org/releases/javadoc/current/index.html?org/apache/beam/sdk/state/SetState.html)
  are not supported with Runner v2. To use the `MapState` and `SetState`
  classes with Java pipelines, enable Streaming Engine, disable Runner v2, and
  use the Apache Beam SDK version 2.58.0 or later.
- For batch and streaming pipelines that use the Apache Beam Java SDK, the
  class
  [`AfterSynchronizedProcessingTime`](https://beam.apache.org/releases/javadoc/current/org/apache/beam/sdk/transforms/windowing/AfterSynchronizedProcessingTime.html)
  isn't supported.
- While Runner v2 scales better than Runner v1 in many cases, the memory usage
  might be higher for fixed sharding.
- Dataflow [classic
  templates](/dataflow/docs/guides/templates/running-templates) can't be run
  with a different version of the Dataflow runner than they were
  built with. This means that Google-provided classic templates can't enable
  Runner v2. To enable Runner v2 for custom templates, set the
  `--experiments=use_runner_v2` flag when you build the template.
- Due to a known autoscaling issue, Runner v2 is disabled by default for batch
  Java pipelines that require [stateful processing](https://beam.apache.org/documentation/programming-guide/#state-and-timers).
  You can still enable Runner v2 for those pipelines (see
  [Enable Runner v2](/dataflow/docs/runner-v2#enable)), but pipeline
  performance might be severely bottlenecked.
- In some pipelines, Runner v2 can increase the frequency of consistency
  failures. You might see the following error in the log files: "Internal
  consistency check failed, the output is likely incorrect. Please retry the
  job". A possible mitigation is to add a `Reshuffle` transform after the
  `Join`/`GrouByKey` step. If the failure rate is not tolerable and the
  mitigation does not solve the issue, try
  [disabling Runner v2](/dataflow/docs/runner-v2#disable).

## Enable Runner v2

To enable Dataflow Runner v2, follow the configuration
instructions for your Apache Beam SDK.

### Java

Dataflow Runner v2 requires the Apache Beam Java SDK
versions 2.30.0 or later, with version 2.44.0 or later being recommended.

For batch pipelines that use the Apache Beam Java SDK versions
2.54.0 or later, Runner v2 is enabled by default.

To enable Runner v2, run your job with the `use_runner_v2` experiment. For
more information, see
[Set experimental pipeline options](/dataflow/docs/guides/setting-pipeline-options#experimental).

### Python

For pipelines that use the Apache Beam Python SDK versions
2.21.0 or later, Runner v2 is enabled by default.

Dataflow Runner v2 isn't supported with the Apache Beam
Python SDK versions 2.20.0 and earlier.

In some cases, your pipeline might not use Runner v2 even though
the pipeline runs on a supported SDK version. To run the job with Runner v2,
set the `use_runner_v2` experiment. For more information, see
[Set experimental pipeline options](/dataflow/docs/guides/setting-pipeline-options#experimental).

### Go

Dataflow Runner v2 is the only Dataflow runner
available for the Apache Beam SDK for Go. Runner v2 is enabled by default.

## Disable Runner v2

To disable Dataflow Runner v2, follow the configuration
instructions for your Apache Beam SDK.

### Java

To disable Runner v2, set the `disable_runner_v2` experiment. For more
information, see
[Set experimental pipeline options](/dataflow/docs/guides/setting-pipeline-options#experimental).

### Python

Disabling Runner v2 is not supported with the Apache Beam Python SDK
versions 2.45.0 and later.

For earlier versions of the Python SDK, if your job is identified as using the
`auto_runner_v2` experiment, you can disable Runner v2 by setting the
`disable_runner_v2` experiment. For more information, see
[Set experimental pipeline options](/dataflow/docs/guides/setting-pipeline-options#experimental).

### Go

Dataflow Runner v2 can't be disabled in Go. Runner v2 is the
only Dataflow runner available for the Apache Beam SDK for
Go.

## Monitor your job

Use the monitoring interface to view
[Dataflow job metrics](/dataflow/docs/guides/using-monitoring-intf),
such as memory utilization, CPU utilization, and more.

Worker VM logs are available through the
[Logs Explorer](/logging/docs/view/logs-explorer-interface) and the
[Dataflow monitoring interface](/dataflow/docs/guides/monitoring-overview).
Worker VM logs include logs from the runner harness process and logs from the SDK
processes. You can use the VM logs to troubleshoot your job.

## Troubleshoot Runner v2

To troubleshoot jobs using Dataflow Runner v2, follow
[standard pipeline troubleshooting steps](/dataflow/docs/guides/troubleshooting-your-pipeline).
The following list provides additional information about how
Dataflow Runner v2 works:

- Dataflow Runner v2 jobs run two types of processes on the
  worker VM: SDK process and the runner harness process. Depending on the
  pipeline and VM type, there might be one or more SDK processes, but there is
  only one runner harness process per VM.
- SDK processes run user code and other language-specific functions. The
  runner harness process manages everything else.
- The runner harness process waits for all SDK processes to connect to it before
  starting to request work from Dataflow.
- Jobs might be delayed if the worker VM downloads and installs dependencies
  during the SDK process startup. If issues occur during an SDK process, such as
  when starting up or installing libraries, the worker reports its status as
  unhealthy. If the startup times increase, enable the Cloud Build API on your
  project and submit your pipeline with the following parameter:
  `--prebuild_sdk_container_engine=cloud_build`.
- Because Dataflow Runner v2 uses checkpointing, each worker might
  wait for up to five seconds while buffering changes before sending the
  changes for further processing. As a result, latency of approximately six
  seconds is expected.

**Note:** The pre-build feature requires the Apache Beam SDK for Python, version
2.25.0 or later.

- To diagnose problems in your user code, examine the worker logs from the SDK
  processes. If you find any errors in the runner harness logs,
  [contact Support](https://console.cloud.google.com/support) to file a bug.
- To debug common errors related to Dataflow multi-language
  pipelines, see the [Multi-language Pipelines Tips](https://cwiki.apache.org/confluence/display/BEAM/Multi-language+Pipelines+Tips) guide.
