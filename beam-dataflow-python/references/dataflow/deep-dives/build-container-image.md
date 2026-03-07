---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/build-container-image
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Build custom container images for Dataflow \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

This document describes how to create a custom container image for
Dataflow jobs.

## Requirements

A custom container image for Dataflow must meet the following
requirements:

- The Apache Beam SDK and necessary dependencies are installed. We recommend
  starting with a default Apache Beam SDK image. For more information, see
  [Select a base image](#base-images) in this document.
- The `/opt/apache/beam/boot` script must run as the last step during container
  startup. This script initializes the worker environment and starts the SDK
  worker process. This script is the default `ENTRYPOINT` in the Apache Beam
  SDK images. However, if you use a different base image, or if you override the
  default `ENTRYPOINT`, then you must run the script explicitly. For more
  information, see [Modify the container entrypoint](#custom-entrypoint) in this
  document.
- Your container image must support the architecture of the worker VMs for your
  Dataflow job. If you plan to use the custom container on ARM
  VMs, we recommend building a multi-architecture image. For more information,
  see
  [Build a multi-architecture container image](/dataflow/docs/guides/multi-architecture-container).

## Before you begin

1. Verify that the version of the Apache Beam SDK installed supports
   [Runner v2](/dataflow/docs/runner-v2) and your language version. For more
   information, see
   [Install the Apache Beam SDK](/dataflow/docs/guides/installing-beam-sdk).
2. To test your container image locally, you must have Docker installed.
   For more information, see
   [Get Docker](https://docs.docker.com/get-docker/).
3. Create an [Artifact Registry](/artifact-registry/docs/repositories) repository.
   Specify Docker image format. You must have at least
   [Artifact Registry Writer access](/artifact-registry/docs/access-control#permissions)
   to the repository.

   To create a new repository, run the
   [`gcloud artifacts repositories create` command](/sdk/gcloud/reference/artifacts/repositories/create):

   ```
   gcloud artifacts repositories create REPOSITORY \
     --repository-format=docker \
     --location=REGION \
     --async
   ```

   Replace the following:
   - REPOSITORY: a name for your repository. Repository names must be
     unique for each location in a project.
   - REGION: the region to
     deploy your Dataflow job in. Select a Dataflow
     region close to where you run
     the commands. The value must be a valid region name. For more information
     about regions and locations, see
     [Dataflow locations](/dataflow/docs/resources/locations).

   This example uses the `--async` flag. The command returns immediately, without
   waiting for the operation to complete.

4. To configure Docker to authenticate requests for Artifact Registry, run the
   [`gcloud auth configure-docker` command](/sdk/gcloud/reference/auth/configure-docker):

   ```
   gcloud auth configure-docker REGION-docker.pkg.dev
   ```

   The command updates your Docker configuration. You can now connect with
   Artifact Registry in your Google Cloud project to push images.

## Select a base image

We recommend starting with an Apache Beam SDK image as the base container
image. These images are released as part of Apache Beam releases to
[Docker Hub](https://hub.docker.com/search?q=apache%2Fbeam&type=image).

### Use an Apache Beam base image

To use an Apache Beam SDK image as the base image, specify the container
image in the `FROM` instruction and then add your own customizations.

### Java

This example uses Java 8 with the Apache Beam SDK version 2.69.0.

```
FROM apache/beam_java8_sdk:2.69.0

# Make your customizations here, for example:
ENV FOO=/bar
COPY path/to/myfile ./
```

The runtime version of the custom container must match the runtime that you will
use to start the pipeline. For example, if you will start the pipeline from a
local Java 11 environment, the `FROM` line must specify a Java 11 environment:
`apache/beam_java11_sdk:...`.

### Python

This example uses Python 3.10 with the Apache Beam SDK version 2.69.0.

```
FROM apache/beam_python3.10_sdk:2.69.0

# Make your customizations here, for example:
ENV FOO=/bar
COPY path/to/myfile ./
```

The runtime version of the custom container must match the runtime that you will
use to start the pipeline. For example, if you will start the pipeline from a
local Python 3.10 environment, the `FROM` line must specify a Python 3.10 environment:
`apache/beam_python3.10_sdk:...`.

### Go

This example uses Go with the Apache Beam SDK version 2.69.0.

```
FROM apache/beam_go_sdk:2.69.0

# Make your customizations here, for example:
ENV FOO=/bar
COPY path/to/myfile ./
```

### Use a custom base image

If you want to use a different base image, or need to modify some aspect of the
default Apache Beam images (such as OS version or patches), use a
[multistage build](https://docs.docker.com/develop/develop-images/multistage-build/)
process. Copy the necessary artifacts from a default Apache Beam base image.

**Note:** Apache Beam and Dataflow are routinely tested using
[Debian](https://hub.docker.com/_/debian)-based images.
[Alpine](https://hub.docker.com/_/alpine) based images are not supported at this
time.

Set the `ENTRYPOINT` to run the `/opt/apache/beam/boot` script, which
initializes the worker environment and starts the SDK worker process. If you
don't set this entrypoint, the Dataflow workers don't start
properly.

The following example shows a Dockerfile that copies files from the
Apache Beam SDK:

### Java

```
FROM openjdk:8

# Copy files from official SDK image, including script/dependencies.
COPY --from=apache/beam_java8_sdk:2.69.0 /opt/apache/beam /opt/apache/beam

# Set the entrypoint to Apache Beam SDK launcher.
ENTRYPOINT ["/opt/apache/beam/boot"]
```

### Python

```
FROM python:3.10-slim

# Install SDK.
RUN pip install --no-cache-dir apache-beam[gcp]==2.69.0

# Verify that the image does not have conflicting dependencies.
RUN pip check

# Copy files from official SDK image, including script/dependencies.
COPY --from=apache/beam_python3.10_sdk:2.69.0 /opt/apache/beam /opt/apache/beam

# Set the entrypoint to Apache Beam SDK launcher.
ENTRYPOINT ["/opt/apache/beam/boot"]
```

This example assumes necessary dependencies (in this case, Python 3.10 and `pip`)
have been installed on the existing base image. Installing the Apache Beam
SDK into the image ensures that the image has the necessary SDK dependencies
and reduces the worker startup time.

**Important:** The SDK version specified in
the `RUN` and `COPY` instructions must match the version used to launch the pipeline.

### Go

```
FROM golang:latest

# Copy files from official SDK image, including script/dependencies.
COPY --from=apache/beam_go_sdk:2.69.0 /opt/apache/beam /opt/apache/beam

# Set the entrypoint to Apache Beam SDK launcher.
ENTRYPOINT ["/opt/apache/beam/boot"]
```

## Modify the container entrypoint

If your container runs a custom script during container startup, the script must
end with running `/opt/apache/beam/boot`. Arguments passed by
Dataflow during container startup must be passed to the default
boot script. The following example shows a custom startup script that calls the
default boot script:

```
#!/bin/bash

echo "This is my custom script"
# ...

# Pass command arguments to the default boot script.
/opt/apache/beam/boot "$@"
```

In your Dockerfile, set the `ENTRYPOINT` to call your script:

### Java

```
FROM apache/beam_java8_sdk:2.69.0

COPY script.sh path/to/my/script.sh
ENTRYPOINT [ "path/to/my/script.sh" ]
```

### Python

```
FROM apache/beam_python3.10_sdk:2.69.0

COPY script.sh path/to/my/script.sh
ENTRYPOINT [ "path/to/my/script.sh" ]
```

### Go

```
FROM apache/beam_go_sdk:2.69.0

COPY script.sh path/to/my/script.sh
ENTRYPOINT [ "path/to/my/script.sh" ]
```

## Build and push the image

You can use Cloud Build or Docker to build your container image and push it
to an Artifact Registry repository.

### Cloud Build

To build the file and push it to your Artifact Registry repository, run the
[`gcloud builds submit` command](/sdk/gcloud/reference/builds/submit):

```
  gcloud builds submit --tag REGION-docker.pkg.dev/PROJECT_ID/REPOSITORY/dataflow/IMAGE:TAG .
```

### Docker

```
docker build . --tag REGION-docker.pkg.dev/PROJECT_ID/REPOSITORY/dataflow/IMAGE:TAG
docker push REGION-docker.pkg.dev/PROJECT_ID/REPOSITORY/dataflow/IMAGE:TAG
```

Replace the following:

- `REGION`: the
  [region](/dataflow/docs/resources/locations)
  to deploy your Dataflow job in. The value of the `REGION`
  variable must be a valid region name.
- `PROJECT_ID`: the project name or username.
- `REPOSITORY`: the image repository name.
- `IMAGE`: the image's name.
- `TAG`: the image tag. Always specify a versioned
  container SHA or tag. Don't use the `:latest` tag or a mutable tag.

## Pre-install Python dependencies

This section applies to Python pipelines.

When you launch a Python Dataflow job, you can specify additional
dependencies by using the `--requirements_file` or the `--extra_packages` option at
runtime. For more information, see
[Managing Python Pipeline Dependencies](https://beam.apache.org/documentation/sdks/python-pipeline-dependencies/).
Additional dependencies are installed in each Dataflow worker
container. When the job first starts and during autoscaling, the dependency
installation often leads to high CPU usage and a long warm-up period on all
newly started Dataflow workers.

To avoid repetitive dependency installations, you can pre-build a custom Python
SDK container image with the dependencies pre-installed. You can perform this
step at build time by using a Dockerfile, or at run time when you submit the
job.

Workers create a new virtual Python environment when they start the container.
For this reason, install dependencies into the default (global) Python
environment instead of creating a virtual environment. If you activate a
virtual environment in your container image, this environment might not be
activate when the job starts. For more information, see
[Common issues](#common_issues).

### Pre-install using a Dockerfile

To add extra dependencies directly to your Python custom container, use the
following commands:

```
FROM apache/beam_python3.10_sdk:2.69.0

COPY requirements.txt .

# Pre-install Python dependencies. For reproducibile builds,
# supply all of the dependencies and their versions in a requirements.txt file.
RUN pip install -r requirements.txt

# You can also install individual dependencies.
RUN pip install lxml
# Pre-install other dependencies.
RUN apt-get update \
  && apt-get dist-upgrade \
  && apt-get install -y --no-install-recommends ffmpeg
```

Submit your job with the `--sdk_container_image` and the `--sdk_location` pipeline options.
The `--sdk_location` option prevents the SDK from downloading when your job launches.
The SDK is retrieved directly from the container image.

The following example runs the
[`wordcount` example pipeline](/dataflow/docs/guides/create-pipeline-python):

```
python -m apache_beam.examples.wordcount \
  --input=INPUT_FILE \
  --output=OUTPUT_FILE \
  --project=PROJECT_ID \
  --region=REGION \
  --temp_location=TEMP_LOCATION \
  --runner=DataflowRunner \
  --experiments=use_runner_v2 \
  --sdk_container_image=IMAGE_URI
  --sdk_location=container
```

Replace the following:

- INPUT_FILE: an input file for the pipeline
- OUTPUT_FILE: a path to write output to
- PROJECT_ID: the Google Cloud Platform project ID
- REGION: the
  [region](/dataflow/docs/resources/locations) to deploy
  your Dataflow job in
- TEMP_LOCATION: the Cloud Storage path for
  Dataflow to stage temporary job files
- IMAGE_URI: the custom container image URI

### Pre-build a container image when submitting the job

Pre-building a container image lets you to pre-install the pipeline dependencies
before job startup. You don't need to build a custom container image.

To pre-build a container with additional Python dependencies when you submit a
job, use the following pipeline options:

- `--prebuild_sdk_container_engine=[cloud_build | local_docker]`. When this flag
  is set, Apache Beam generates a custom container and installs all of the
  dependencies specified by the `--requirements_file` and the `--extra_packages`
  options. This flag supports the following values:
  - `cloud_build`. Use [Cloud Build](/build/docs/overview) to build the
    container. The Cloud Build API must be enabled in your project.
  - `local_docker`. Use your local Docker installation to build the container.

- `--docker_registry_push_url=IMAGE_PATH`.
  Replace `IMAGE_PATH` with an Artifact Registry folder.
- `--sdk_location=container`. This option prevents the workers from downloading
  the SDK when your job launches. Instead, the SDK is retrieved directly from
  the container image.

The following example uses Cloud Build to pre-build the image:

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
  --requirements_file=./requirements.txt \
  --prebuild_sdk_container_engine=cloud_build \
  --docker_registry_push_url=IMAGE_PATH \
  --sdk_location=container
```

The pre-build feature requires the Apache Beam SDK for Python version
2.25.0 or later.

The SDK container image pre-building workflow uses the image passed using the
`--sdk_container_image` pipeline option as the base image. If the option is not
set, by default an Apache Beam image is used as the base image.

**Note:** With Apache Beam SDK versions 2.38.0 and earlier, to specify the base image,
use `--prebuild_sdk_container_base_image`.

You can reuse a prebuilt Python SDK container image in another job with the same dependencies and SDK version.
To reuse the image, pass the prebuilt container image URL to the other job
by using the `--sdk_container_image` pipeline option. Remove the dependency
options `--requirements_file`, `--extra_packages`, and `--setup_file`.

If you don't plan to reuse the image, delete it after the job completes.
You can delete the image with the gcloud CLI
or in the Artifact Registry pages in the Google Cloud console.

If the image is stored in Artifact Registry, use the
[`artifacts docker images delete`](/sdk/gcloud/reference/artifacts/docker/images/delete) command:

```
   gcloud artifacts docker images delete IMAGE --delete-tags
```

### Common issues

- If your job has extra Python dependencies from a private PyPi mirror and can't be pulled
  by a remote Cloud Build job, try using the local docker option or
  try building your container using a Dockerfile.
- If the Cloud Build job fails with `docker exit code 137`, the build job ran out of memory,
  potentially due to the size of the dependencies being installed. Use a larger Cloud Build
  worker machine type by passing `--cloud_build_machine_type=machine_type`,
  where machine_type is one of the following options:
  - `n1-highcpu-8`
  - `n1-highcpu-32`
  - `e2-highcpu-8`
  - `e2-highcpu-32`

  By default, Cloud Build uses the machine type `e2-medium`.

- In Apache Beam 2.44.0 and later, workers create a virtual environment when
  starting a custom container. If the container creates its own virtual
  environment to install dependencies, those dependencies are discarded. This
  behavior can cause errors such as the following:

  `ModuleNotFoundError: No module named '<dependency name>'`

  To avoid this issue, install dependencies into the default (global) Python
  environment. As a workaround, disable this behavior in Beam 2.48.0 and
  later by setting the following environment variable in your container image:

  `ENV RUN_PYTHON_SDK_IN_DEFAULT_ENVIRONMENT=1`

## What's next

- For more information about writing Dockerfiles, see
  [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/).
- Learn how to [Run a Dataflow job in a custom container](/dataflow/docs/guides/run-custom-container).
