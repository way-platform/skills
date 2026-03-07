---
source_url: https://docs.cloud.google.com/dataflow/docs/gpu/troubleshoot-gpus
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Troubleshoot your Dataflow GPU job \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

**Note:** The following
considerations apply to this GA offering:

- Jobs that use GPUs incur charges as specified in the
  Dataflow [pricing page](https://cloud.google.com/dataflow/pricing).
- To use GPUs, your Dataflow job must use [Dataflow Runner v2](/dataflow/docs/runner-v2).

If you encounter problems running your Dataflow job with GPUs,
follow these steps:

1. Follow the workflow in
   [Best practices for working with Dataflow GPUs](/dataflow/docs/gpu/develop-with-gpus)
   to ensure that your pipeline is configured correctly.
2. Confirm that your Dataflow job is using GPUs. See
   [Verify your Dataflow job](/dataflow/docs/gpu/use-gpus#verify) in
   "Run a pipeline with GPUs."
3. [Debug your job](#debug-job), either with a standalone VM or
   by using Dataflow.
4. If the problem persists, follow the rest of the troubleshooting steps on this page.

## Debug your job

If possible, [debug your job with a standalone VM](#debug-vm), because debugging
with a standalone VM is usually faster. However, if organizational policies
prevent you from debugging with a standalone VM, you can
[debug by using Dataflow](#debug-df).

### Debug with a standalone VM

While you're designing and iterating on a container image that works for you,
it can be faster to reduce the feedback loop by trying out your container image
on a standalone VM.

You can debug your custom container on a standalone VM with GPUs by creating a
Compute Engine VM running GPUs on Container-Optimized OS,
installing drivers, and starting your container as follows.

1. Create a VM instance.

   ```
   gcloud compute instances create INSTANCE_NAME \
     --project "PROJECT" \
     --image-family cos-stable \
     --image-project=cos-cloud  \
     --zone=us-central1-f \
     --accelerator type=nvidia-tesla-t4,count=1 \
     --maintenance-policy TERMINATE \
     --restart-on-failure  \
     --boot-disk-size=200G \
     --scopes=cloud-platform
   ```

2. Use `ssh` to connect to the VM.

   ```
   gcloud compute ssh INSTANCE_NAME --project "PROJECT"
   ```

3. Install the GPU drivers. After connecting to the VM by using `ssh`, run the
   following commands on the VM:

   ```
   # Run these commands on the virtual machine
   cos-extensions install gpu
   sudo mount --bind /var/lib/nvidia /var/lib/nvidia
   sudo mount -o remount,exec /var/lib/nvidia
   /var/lib/nvidia/bin/nvidia-smi
   ```

4. Launch your custom container.

   Apache Beam SDK containers use the `/opt/apache/beam/boot` entrypoint. For
   debugging purposes you can launch your container manually with a different
   entrypoint:

   ```
   docker-credential-gcr configure-docker
   docker run --rm \
     -it \
     --entrypoint=/bin/bash \
     --volume /var/lib/nvidia/lib64:/usr/local/nvidia/lib64 \
     --volume /var/lib/nvidia/bin:/usr/local/nvidia/bin \
     --privileged \
     IMAGE
   ```

   Replace IMAGE with the Artifact Registry path for your Docker image.

5. Verify that the GPU libraries installed in your container can access the
   GPU devices.

   If you're using TensorFlow, you can
   print available devices in Python interpreter with the following:

   ```
   >>> import tensorflow as tf
   >>> print(tf.config.list_physical_devices("GPU"))
   ```

   If you're using PyTorch, you can
   inspect available devices in Python interpreter with the following:

   ```
   >>> import torch
   >>> print(torch.cuda.is_available())
   >>> print(torch.cuda.device_count())
   >>> print(torch.cuda.get_device_name(0))
   ```

To iterate on your pipeline, you can launch your pipeline on Direct Runner. You
can also launch pipelines on Dataflow Runner from this environment.

### Debug by using Dataflow

If organizational constraints prevent you from debugging on a standalone VM,
you can debug by using Dataflow.

Simplify your pipeline so that all it does is detect whether GPUs are
present, and then run the pipeline on Dataflow. The following
example demonstrates what the code for this pipeline might look like:

```
def check_if_gpus_present(element):
  import torch
  import tensorflow as tf

  tensorflow_detects_gpus = tf.config.list_physical_devices("GPU")
  torch_detects_gpus = torch.cuda.is_available()
  if tensorflow_detects_gpus and torch_detects_gpus:
    return element

  if tensorflow_detects_gpus:
    raise Exception('PyTorch failed to detect GPUs with your setup')
  if torch_detects_gpus:
    raise Exception('Tensorflow failed to detect GPUs with your setup')
  raise Exception('Both Tensorflow and PyTorch failed to detect GPUs with your setup')

with beam.Pipeline() as p:
  _ = (p | beam.Create([1,2,3]) # Create a PCollection of the prompts.
         | beam.Map(check_if_gpus_present)
  )
```

If your pipeline succeeds, your code is able to access GPUs. To identify the
problem code, gradually insert progressively larger examples into your pipeline
code, running your pipeline after each change.

If your pipeline fails to detect GPUs, follow the steps in the
[No GPU usage](#no-gpu-usage) section of this document.

## Workers don't start

If your job is stuck and the Dataflow workers never start
processing data, it's likely that you have a problem related to using a custom
container with Dataflow. For more details, read
the [custom containers troubleshooting guide](/dataflow/docs/guides/troubleshoot-custom-container).

If you're a Python user, verify that the following conditions are met:

- The Python interpreter minor version
  in your container image is the same version as you use when launching your
  pipeline. If there's a mismatch, you might see errors like
  [`SystemError: unknown opcode`](/dataflow/docs/guides/common-errors#custom-container-python-version)
  with a stack trace involving `apache_beam/internal/pickler.py`.
- If you're using the Apache Beam SDK 2.29.0 or earlier,
  `pip` must be accessible on the image in `/usr/local/bin/pip`.

We recommend that you reduce the customizations to a minimal working
configuration the first time you use a custom image. Use the sample custom
container images provided in the examples on this page. Make sure you
can run a straightforward Dataflow pipeline with this container
image without requesting GPUs. Then, iterate on the solution.

Verify that workers have sufficient disk space to download your container
image. Adjust disk size if necessary. Large images take longer to
download, which increases worker startup time.

## Job fails immediately at startup

If you encounter the
[`ZONE_RESOURCE_POOL_EXHAUSTED`](/compute/docs/troubleshooting/troubleshooting-vm-creation#resource_availability)
or [`ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS`](/compute/docs/troubleshooting/troubleshooting-vm-creation#resource_availability) errors, you can take the following steps:

- Don't specify the worker zone so that Dataflow selects the
  optimal zone for you.
- Launch the pipeline in a different zone or with a different accelerator type.
- Configure a provisioning model, such as Flex-start. For more information, read [Configure a provisioning model](/dataflow/docs/gpu/use-gpus#optional_configure_a_provisioning_model).

## Job fails at runtime

If the job fails at runtime, check for out of memory (OOM) errors on the worker
machine and on the GPU. GPU OOM errors may manifest as
`cudaErrorMemoryAllocation out of memory` errors in worker logs. If you're
using TensorFlow, verify that you use only one
TensorFlow process to access one GPU device.
For more information, read [GPUs and worker parallelism](/dataflow/docs/concepts/gpu-support#gpus_and_worker_parallelism).

## No GPU usage

If your job doesn't appear to be using GPUs, follow the steps in the
[Debug your job](#debug-job) section of this document to verify whether GPUs are
available with your Docker image.

If GPUs are available but not used, the problem is likely with the pipeline code.
To debug the pipeline code, start with a straightforward pipeline that successfully
uses GPUs, and then gradually add code to the pipeline, testing the pipeline
with each new addition. For more information, see the
[Debug on Dataflow](#debug-df) section of this document.

If your pipeline fails to detect GPUs, verify the following:

- NVIDIA libraries installed in the container image match the requirements of
  pipeline user code and libraries that it uses.
- Installed NVIDIA libraries in container images are accessible as shared
  libraries.

If the devices are not available, you might be using an incompatible software
configuration. To verify the image configuration, run a straightforward pipeline
that just checks that GPUs are available and accessible to the workers.

## Troubleshoot TensorFlow issues

If PyTorch detects GPUs in your pipeline but TensorFlow doesn't,
try the following troubleshooting steps:

- Verify that you have a compatible combination of TensorFlow,
  cuDNN version, and CUDA Toolkit version. For more information, see
  [Tested build configurations](https://www.tensorflow.org/install/source#gpu)
  in the TensorFlow documentation.
- If possible, upgrade to the latest compatible TensorFlow and
  CUDA versions.
- Review the known issues for TensorFlow and CUDA to verify whether
  a known is causing problems in your pipeline. For example, the following known
  issue could prevent TensorFlow from detecting GPUs:
  [TF 2.17.0 RC0 Fails to work with GPUs](https://github.com/tensorflow/tensorflow/issues/63362).

## What's next

- [Getting started: Running GPUs on Container-Optimized
  OS](/container-optimized-os/docs/how-to/run-gpus#getting_started_running_gpus_on).
- [Container-Optimized OS toolbox](/container-optimized-os/docs/how-to/toolbox).
- [Service account access scopes](/compute/docs/access/service-accounts#accesscopesiam).
