---
source_url: https://docs.cloud.google.com/dataflow/docs/tpu/troubleshoot-tpus
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Troubleshoot your Dataflow TPU job \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

If you run into problems running your Dataflow job with TPUs, use
the following troubleshooting steps to resolve your issue.

## Troubleshoot your container image

It can be helpful to debug your container and TPU software on a standalone VM.
You can debug with a VM created by a GKE nodepool, or you can
debug on a running Dataflow worker VM.

### Debug with a standalone VM

To debug your container on a standalone VM, you can create a GKE
node pool that uses the same [TPU
VM](/dataflow/docs/tpu/use-tpus#configure-container) for local experimentation.
For example, creating a GKE node pool with one TPU V5 Lite device
in `us-west1-c` would look like the following:

1. Create a GKE cluster.

   ```
   gcloud container clusters create TPU_CLUSTER_NAME \
     --project PROJECT_ID \
     --release-channel=stable \
     --scopes=cloud-platform \
     --enable-ip-alias \
     --location us-west1-c
   ```

2. Create a GKE node pool.

   ```
   gcloud container node-pools create TPU_NODE_POOL_NAME \
     --project PROJECT_ID \
     --location=us-west1-c \
     --cluster=TPU_CLUSTER_NAME \
     --node-locations=us-west1-c \
     --machine-type=ct5lp-hightpu-1t \
     --num-nodes=1 \
     [ --reservation RESERVATION_NAME \
     --reservation-affinity=specific ]
   ```

3. Find the VM name of the TPU node in the nodepool in the GKE UI or with the following command.

   ```
   gcloud compute instances list --filter='metadata.kube-labels:"cloud.google.com/gke-nodepool=TPU_NODEPOOL_NAME"'
   ```

4. Connect to a VM created by the GKE node pool using
   [SSH](/compute/docs/connect/standard-ssh):

   ```
   gcloud compute ssh --zone "us-west1-c" "VM_NAME" --project PROJECT_ID
   ```

5. After connecting to a VM using SSH, configure Docker for the Artifact Registry you
   are using.

   ```
   docker-credential-gcr configure-docker --registries=us-west1-docker.pkg.dev
   ```

6. Then, start a container from the image that you use.

   ```
   docker run --privileged --network=host -it --rm --entrypoint=/bin/bash IMAGE_NAME
   ```

7. Inside the container, test that TPUs are accessible.

   For example, if you have an image that uses PyTorch to utilize TPUs,
   open a Python interpreter:

   ```
   python3
   ```

   Then, perform a computation on a TPU device:

   ```
   import torch
   import torch_xla.core.xla_model as xm
   dev = xm.xla_device()
   t1 = torch.randn(3,3,device=dev)
   t2 = torch.randn(3,3,device=dev)
   print(t1 + t2)
   ```

   Sample output:

   ```
   >>> tensor([[ 0.3355, -1.4628, -3.2610],
   >>>        [-1.4656,  0.3196, -2.8766],
   >>>        [ 0.8667, -1.5060,  0.7125]], device='xla:0')
   ```

8. If the computation fails, your image might not be properly configured.

   For example, you might need to set the required environment
   variables in the image Dockerfile. To confirm, retry the computation
   after setting the environment variables manually as follows:

   ```
   export TPU_SKIP_MDS_QUERY=1 # Don't query metadata
   export TPU_HOST_BOUNDS=1,1,1 # There's only one host
   export TPU_CHIPS_PER_HOST_BOUNDS=1,1,1 # 1 chips per host
   export TPU_WORKER_HOSTNAMES=localhost
   export TPU_WORKER_ID=0 # Always 0 for single-host TPUs
   export TPU_ACCELERATOR_TYPE=v5litepod-1 # Since we use v5e 1x1 accelerator.
   ```

   If PyTorch or LibTPU dependencies are missing, you could retry the
   computation after installing them using the following command:

   ```
   # Install PyTorch with TPU support
   pip install torch torch_xla[tpu] torchvision -f https://storage.googleapis.com/libtpu-releases/index.html
   ```

### Debug by using a Dataflow VM

As an alternative, you can connect to the Dataflow worker VM
instance using SSH while a job is running. Because Dataflow worker
VMs shut down after pipeline completion, you might need to artificially increase
the runtime by doing a computation that waits for a prolonged period of time.

Because a TPU device cannot be shared between multiple processes, you might need
to run a pipeline that doesn't make any computations on a TPU.

1. Find a VM for the running TPU job by searching for the
   Dataflow job ID in the Google Cloud console search bar or by
   using the following `gcloud` command:

   ```
   gcloud compute instances list --project PROJECT_ID --filter "STATUS='RUNNING' AND description ~ 'Created for Dataflow job: JOB_ID'"
   ```

2. After connecting to a VM with TPUs using SSH, start a container from the
   image that you use. For an example, see [Debug with a standalone VM](#debug-vm).
3. Inside the container, reconfigure the TPU settings and install necessary
   libraries to test your setup. For an example, see [Debug with a standalone
   VM](#debug-vm).

## Workers don't start

Before troubleshooting, verify the following pipeline options are set correctly:

- the `--dataflow_service_option=worker_accelerator` option
- the `--worker_zone` option
- the `--machine_type` option

Check if the console logs show that workers are starting, but the job fails with
a message similar to the following:

```
  Workflow failed. Causes: The Dataflow job appears to be stuck because no worker
  activity has been seen in the last 25m.
```

The cause of these issues might be related to capacity or worker
startup issues.

- **Capacity**: If you use on-demand TPU capacity, or a reservation that is
  exhausted, new pipelines might not start until capacity is available. If you
  use a reservation, check its remaining capacity on the [Compute Reservations
  page](https://console.cloud.google.com/compute/reservations) in the
  Google Cloud console or with the following command:

  ```
  gcloud compute reservations describe RESERVATION_NAME --zone ZONE
  ```

  Check whether your job has started any worker VMs. When your job starts a
  worker, loggers such as `worker`, `worker_startup`, `kubelet`, and others
  generally provide output. Additionally, on the [**Job
  metrics**](/dataflow/docs/guides/using-monitoring-intf#access-metrics) page in
  the Google Cloud console, the number of current workers should be greater than
  zero.

- **Worker startup**: Check the `job-message` and `launcher` logs. If your
  pipeline starts workers but they can't boot, you might have [errors in your
  custom container](/dataflow/docs/guides/troubleshoot-custom-container).
- **Disk space**: Verify that sufficient disk space is available for your job.
  To increase disk space, use the `--disk_size_gb` option.

## Job fails with an error

Use the following troubleshooting advice when your job fails with an error.

### Startup of worker pool failed

If you see the following error, verify that your pipeline specifies
`--worker_zone` and that the zone matches the zone for your reservation.

```
JOB_MESSAGE_ERROR: Startup of the worker pool in zone ZONE failed to
bring up any of the desired 1 workers. [...] INVALID_FIELD_VALUE:
Instance 'INSTANCE_NAME' creation failed: Invalid value for field
'resource.reservationAffinity': '{ "consumeReservationType":
"SPECIFIC_ALLOCATION", "key":
"compute.googleapis.com/RESERVATION_NAME...'. Specified reservations
[RESERVATION_NAME] do not exist.
```

### Managed instance groups don't support Cloud TPUs

If you see the following error, contact your [account
team](/dataflow/docs/support/getting-support) to verify whether your project has
been enrolled to use TPUs, or file a bug using the [Google Issue
Tracker](https://issuetracker.google.com/issues/new?component=187168&template=0).

```
apache_beam.runners.dataflow.dataflow_runner.DataflowRuntimeException: Dataflow
pipeline failed. State: FAILED, Error: Workflow failed. Causes: One or more
operations had an error [...]: [INVALID_FIELD_VALUE] 'Invalid value
for field 'resource.instanceTemplate': Managed Instance Groups do not support
Cloud TPUs. '.
```

### Invalid value for field

If you see the following error, verify that your pipeline invocation sets the
`worker_accelerator` Dataflow service option.

```
JOB_MESSAGE_ERROR: Workflow failed. Causes: One or more operations had an error:
'operation-[...]': [INVALID_FIELD_VALUE] 'Invalid value for field
'resource.instanceTemplate': 'projects/[...]-harness'. Regional
Managed Instance Groups do not support Cloud TPUs.'
```

### Device or resource busy

If you see the following error, then a Dataflow worker processing
your pipeline likely is running more than one process that is accessing the TPU
at the same time. This is not supported. For more information, see [TPUs and
worker parallelism](/dataflow/docs/tpu/use-tpus#tpus_and_worker_parallelism).

```
RuntimeError: TPU initialization failed: open(/dev/vfio/0): Device or resource
busy: Device or resource busy; Couldn't open iommu group /dev/vfio/0
```

If you see the preceding error while debugging your pipeline on a VM, you can
inspect and terminate the process that is holding up the TPU by using the
following commands:

```
apt update ; apt install lsof
lsof -w /dev/vfio/0
kill -9 PROCESS_ID    # to terminate the process.
```

### Instances with guest accelerators do not support live migration

If you see the following error, the pipeline was likely launched with an
explicitly-set machine type that has accelerators, but didn't specify
accelerator configuration correctly. Verify that your pipeline invocation sets
the `worker_accelerator` Dataflow service option, and make sure
the option name doesn't contain typos.

```
JOB_MESSAGE_ERROR: Startup of the worker pool in zone ZONE failed to
bring up any of the desired 1 workers. [...] UNSUPPORTED_OPERATION:
Instance INSTANCE_ID creation failed: Instances with guest
accelerators do not support live migration.
```

### The workflow was automatically rejected by the service

The following errors might also appear if some of the required pipeline options
are missing or incorrect:

```
The workflow was automatically rejected by the service. The requested
accelerator type tpu-v5-lite-podslice;topology:1x1 requires setting
the worker machine type to ct5lp-hightpu-1t. Learn more at:
https://cloud.google.com/dataflow/docs/guides/configure-worker-vm
```

### Timed out waiting for an update from the worker

When you launch pipelines on TPU VMs with a lot of vCPU, the job might encounter
errors like the following:

```
Workflow failed. Causes WORK_ITEM failed.
The job failed because a work item has failed 4 times.
Root cause: Timed out waiting for an update from the worker.
```

If you see this error, try reducing the number of threads.
For example, you could set: `--number_of_worker_harness_threads=50`.

## No TPU usage

If your pipeline runs successfully but TPU devices aren't used or aren't
accessible, verify that the frameworks you are using, such as JAX or PyTorch,
can access the attached devices. To troubleshoot your container image on a
single VM, see [Debug with a standalone VM](#debug-vm).
