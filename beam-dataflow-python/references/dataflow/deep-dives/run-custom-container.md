---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/run-custom-container
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Run a Dataflow job in a custom container \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

This document describes how to run a Dataflow pipeline using a
custom container.

For information about creating the container image, see
[Build custom container images for Dataflow](/dataflow/docs/guides/build-container-image).

When you run your pipeline, launch the pipeline using the Apache Beam SDK
with the same version and language version as the SDK on your custom container
image. This step avoids unexpected errors from incompatible dependencies or
SDKs.

## Test locally

Before you run your pipeline in Dataflow, it's a good idea to test
the container image locally, which allows for more rapid testing and debugging.

To learn more about Apache Beam-specific usage, see the Apache Beam guide for
[Running pipelines with custom container images](https://beam.apache.org/documentation/runtime/environments/#running-pipelines).

### Basic testing with `PortableRunner`

To verify that remote container images can be pulled and can run a simple
pipeline, use the Apache Beam `PortableRunner`. When you use the
`PortableRunner`, job submission occurs in the local environment, and the
`DoFn` execution happens in the Docker environment.

When you use GPUs, the Docker container might not have access to the GPUs. To
test your container with GPUs, use the [direct runner](#direct-runner) and
follow the steps for testing a container image on a standalone VM with GPUs in the
[Debug with a standalone VM](/dataflow/docs/gpu/troubleshoot-gpus#debug-vm)
section of the "Use GPUs" page.

The following runs an example pipeline:

### Java

```
mvn compile exec:java -Dexec.mainClass=com.example.package.MyClassWithMain \
    -Dexec.args="--runner=PortableRunner \
    --jobEndpoint=REGION \
    --defaultEnvironmentType=DOCKER \
    --defaultEnvironmentConfig=IMAGE_URI \
    --inputFile=INPUT_FILE \
    --output=OUTPUT_FILE"
```

### Python

```
python path/to/my/pipeline.py \
  --runner=PortableRunner \
  --job_endpoint=REGION \
  --environment_type=DOCKER \
  --environment_config=IMAGE_URI \
  --input=INPUT_FILE \
  --output=OUTPUT_FILE
```

### Go

```
go path/to/my/pipeline.go \
  --runner=PortableRunner \
  --job_endpoint=REGION \
  --environment_type=DOCKER \
  --environment_config=IMAGE_URI \
  --input=INPUT_FILE \
  --output=OUTPUT_FILE
```

Replace the following:

- `REGION`: the job service region to use,
  in the form of address and port. For example: `localhost:3000`. Use `embed` to
  run an in-process job service.
- `IMAGE_URI`: the custom container image URI.
- `INPUT_FILE`: an input file that can be read as a
  text file. This file must be accessible by the SDK harness  
  container image, either preloaded on the container image or a remote
  file.
- `OUTPUT_FILE`: a path to write output to. This
  path is either a remote path or a local path on the container.

When the pipeline successfully completes, review the console logs to verify that
the pipeline completed successfully and that the **remote image**, specified by
`IMAGE_URI`, is used.

After running the pipeline, files saved to the container are not in your local
file system, and the container is stopped. You can copy files from
the stopped container file system by using
[`docker cp`](https://docs.docker.com/engine/reference/commandline/cp/).

Alternatively:

- Provide outputs to a remote file system like Cloud Storage.
  You might need to manually configure access for testing purposes,
  including for credential files or
  [Application Default Credentials](/docs/authentication/provide-credentials-adc).
- For quick debugging, add temporary [logging](/dataflow/docs/guides/logging).

### Use the Direct Runner

For more in-depth local testing of the container image and your pipeline, use the
Apache Beam [Direct Runner](https://beam.apache.org/documentation/runners/direct/).

You can verify your pipeline separately from the container by testing in a
local environment matching the container image, or by launching the pipeline
on a running container.

### Java

```
docker run -it --entrypoint "/bin/bash" IMAGE_URI
...
# On docker container:
root@4f041a451ef3:/#  mvn compile exec:java -Dexec.mainClass=com.example.package.MyClassWithMain ...
```

### Python

```
docker run -it --entrypoint "/bin/bash" IMAGE_URI
...
# On docker container:
root@4f041a451ef3:/#  python path/to/my/pipeline.py ...
```

### Go

```
docker run -it --entrypoint "/bin/bash" IMAGE_URI
...
# On docker container:
root@4f041a451ef3:/#  go path/to/my/pipeline.go ...
```

Replace `IMAGE_URI` with the custom container image URI.

The examples assume any pipeline files, including the pipeline itself, are on
the custom container, have been mounted from a local file system, or are
remote and accessible by Apache Beam and the container. For example, to use
Maven (`mvn`) to run the previous Java example, Maven and its
dependencies must be staged on the container. For more information, see
[Storage](https://docs.docker.com/storage/) and
[`docker run`](https://docs.docker.com/engine/reference/run/)
in the Docker documentation.

The goal for testing on the Direct Runner is to test your pipeline
in the custom container environment, not to test running your container
with its default `ENTRYPOINT`. Modify the `ENTRYPOINT` (for example,
`docker run --entrypoint ...`) to either directly run your pipeline or to allow
manually running commands on the container.

If you rely on a specific configuration that is based on running the container
on Compute Engine, you can run the container directly on a Compute Engine
VM. For more information, see
[Containers on Compute Engine](/compute/docs/containers).

## Launch the Dataflow job

When launching the Apache Beam pipeline on Dataflow, specify
the path to the container image. Don't use the `:latest` tag with your custom
images. Tag your builds with a date or a unique identifier. If something goes
wrong, using this type of tag might make it possible to revert the pipeline
execution to a previously known working configuration and allow for an
inspection of changes.

### Java

Use `--sdkContainerImage` to specify an SDK container image for your Java runtime.

Use `--experiments=use_runner_v2` to enable Runner v2.

### Python

If using SDK version **2.30.0 or later**, use the pipeline option `--sdk_container_image` to specify an SDK container image.

For earlier versions of the SDK, use the pipeline option `--worker_harness_container_image` to specify the location of container image to use for the worker harness.

Custom containers are only supported for Dataflow Runner v2. If
you're launching a batch Python pipeline, set the `--experiments=use_runner_v2` flag.
If you're launching a streaming Python pipeline, specifying the experiment isn't
necessary, because streaming Python pipelines use Runner v2 by default.

### Go

If using SDK version **2.40.0 or later**, use the pipeline option `--sdk_container_image` to specify an SDK container image.

For earlier versions of the SDK, use the pipeline option `--worker_harness_container_image` to specify the location of container image to use for the worker harness.

Custom containers are supported on all versions of the Go SDK because they
use Dataflow Runner v2 by default.

The following example demonstrates how to launch the batch
[`WordCount` example](https://beam.apache.org/get-started/wordcount-example/)
with a custom container.

### Java

```
mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.WordCount \
   -Dexec.args="--runner=DataflowRunner \
                --inputFile=INPUT_FILE \
                --output=OUTPUT_FILE \
                --project=PROJECT_ID \
                --region=REGION \
                --gcpTempLocation=TEMP_LOCATION \
                --diskSizeGb=DISK_SIZE_GB \
                --experiments=use_runner_v2 \
                --sdkContainerImage=IMAGE_URI"
```

### Python

Using the Apache Beam SDK for Python version 2.30.0 or later:

```
python -m apache_beam.examples.wordcount \
  --input=INPUT_FILE \
  --output=OUTPUT_FILE \
  --project=PROJECT_ID \
  --region=REGION \
  --temp_location=TEMP_LOCATION \
  --runner=DataflowRunner \
  --disk_size_gb=DISK_SIZE_GB \
  --experiments=use_runner_v2 \
  --sdk_container_image=IMAGE_URI
```

### Go

```
wordcount --input gs://dataflow-samples/shakespeare/kinglear.txt \
          --output gs://<your-gcs-bucket>/counts \
          --runner dataflow \
          --project your-gcp-project \
          --region your-gcp-region \
          --temp_location gs://<your-gcs-bucket>/tmp/ \
          --staging_location gs://<your-gcs-bucket>/binaries/ \
          --sdk_container_image=IMAGE_URI
```

Replace the following:

- `INPUT_FILE`: the Cloud Storage input path
  read by Dataflow when running the example.
- `OUTPUT_FILE`: the Cloud Storage output path
  written to by the example pipeline. This file contains the word counts.
- `PROJECT_ID`: the ID of your Google Cloud
  project.
- `REGION`: the region to deploy your
  Dataflow job in.
- `TEMP_LOCATION`: the Cloud Storage path for
  Dataflow to stage temporary job files created during the
  execution of the pipeline.
- `DISK_SIZE_GB`: Optional. If your container is
  large, consider increasing default [boot disk size](/dataflow/docs/reference/pipeline-options#worker-level_options)
  to avoid [running out of disk space](/dataflow/docs/guides/common-errors#no-space-left).
- `IMAGE_URI`: the SDK custom container image URI.
  Always use a versioned container SHA or tag. Don't use the `:latest` tag or
  a mutable tag.

### Container image streaming

You can improve your Dataflow pipeline's startup and autoscaling
latency by enabling image streaming. This feature is useful if your custom
container contains extraneous content or doesn't use all of its content at each
step. For example, your container might contain incidental content such as
CPU-based library code for GPU-based inference. Similarly, you might have a
container that runs ML pipelines with multiple models that use only one model at
each step, so its contents aren't needed all at once. Enabling image streaming
would help to improve latency in these cases.

### Java

`--dataflowServiceOptions=enable_image_streaming`

### Python

`--dataflow_service_options=enable_image_streaming`

### Go

`--dataflow_service_options=enable_image_streaming`

Image streaming will fetch parts of your custom container as your pipeline code
needs them instead of downloading your entire container up-front. Parts of your
container that aren't used never have to be downloaded.

You must have the
[Container File System API](https://console.cloud.google.com/marketplace/product/google/containerfilesystem.googleapis.com) enabled to benefit from image streaming.
