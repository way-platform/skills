---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/using-custom-containers
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Use custom containers in Dataflow \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

You can customize the runtime environment of user code in Dataflow
pipelines by supplying a custom container image. Custom containers are
supported for pipelines that use Dataflow
[Runner v2](/dataflow/docs/runner-v2).

When Dataflow starts up worker VMs, it uses Docker container
images to launch containerized SDK processes on the workers. By default, a
pipeline uses a prebuilt
[Apache Beam image](https://hub.docker.com/search?q=apache%2Fbeam&type=image).
However, you can provide a custom container image for your Dataflow job.
When you specify a custom container image, Dataflow launches workers
that pull the specified image.

You might use a custom container for the following reasons:

- Preinstall pipeline dependencies to reduce worker start time.
- Preinstall pipeline dependencies that are not available in
  public repositories.
- Preinstall pipeline dependencies when access to public repositories is
  turned off. Access might be turned off for security reasons.
- Prestage large files to reduce worker start time.
- Launch third-party software in the background.
- Customize the execution environment.

For more information about custom containers in Apache Beam, see the
[Apache Beam custom container guide](https://beam.apache.org/documentation/runtime/environments/).
For examples of Python pipelines that use custom containers, see
[Dataflow custom containers](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/dataflow/custom-containers).

## Next steps

- [Build custom container images](/dataflow/docs/guides/build-container-image)
- [Build multi-architecture container images](/dataflow/docs/guides/multi-architecture-container)
- [Run a Dataflow job in a custom container](/dataflow/docs/guides/run-custom-container)
- [Troubleshoot custom containers](/dataflow/docs/guides/troubleshoot-custom-container)
