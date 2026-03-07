---
source_url: https://docs.cloud.google.com/dataflow/docs/vertical-autoscaling
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Vertical Autoscaling \u00a0|\u00a0 Cloud Dataflow \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

Vertical Autoscaling is a feature that enables
[Dataflow Prime](/dataflow/docs/guides/enable-dataflow-prime) to dynamically
scale up or scale down the memory available to workers to fit the requirements
of the job. The feature is designed to make jobs resilient to out-of-memory
(OOM) errors and to maximize pipeline efficiency. Dataflow Prime monitors
your pipeline, detects situations where the workers lack or exceed available
memory, and then replaces those workers with new workers with more or less
memory.

**Important:** Because Vertical Autoscaling replaces existing workers with new
workers, we strongly recommend [using custom
containers](/dataflow/docs/guides/using-custom-containers) to improve the
latency that might arise from resizing the workers.

## Streaming

Vertical Autoscaling is enabled by default for all new streaming jobs that [use
Dataflow Prime](/dataflow/docs/guides/enable-dataflow-prime#enable-prime).

If you are launching a job from a template through the command line interface,
you can disable Vertical Autoscaling by passing the
`--additional_experiments=disable_vertical_memory_autoscaling` flag.

All Dataflow Prime streaming Java and Python pipelines support Vertical
Autoscaling. You can use Dataflow Prime streaming Java pipelines without
Streaming Engine. However, for the best experience with Vertical Autoscaling,
enabling Streaming Engine is recommended.

## Batch

For Dataflow Prime batch jobs, Vertical Autoscaling only scales up after four
out-of-memory errors occur.

- Vertical Autoscaling scales up to prevent job failures and does not scale
  down.
- The entire pool scales up for the remainder of the job.
- If resource hints are used and multiple pools are created, each pool scales
  up separately.

For batch jobs, Vertical Autoscaling is not enabled by default. To enable
Vertical Autoscaling for batch jobs, set the following pipeline options:

- `--experiments=enable_batch_vmr`
- `--experiments=enable_vertical_memory_autoscaling`

To disable Vertical Autoscaling for batch jobs, do one of the following:

- Do not set the `--experiments=enable_batch_vmr` pipeline option.
- Set the `--experiments=disable_vertical_memory_autoscaling` pipeline option.

## Limitations

- Only the memory of the workers scales vertically.
- By default, memory scaling has an upper limit of 16 GiB and a lower limit of
  6 GiB. When you [use GPUs](/dataflow/docs/gpu), memory scaling has an upper
  limit of 26 GiB and a lower limit of 12 GiB. You can change both the upper
  and lower limits by providing a resource hint.
- Vertical Autoscaling is not supported for pools using A100 GPUs.
- For batch jobs, bundles that include a failing item might be retried more
  than 4 times before the pipeline fails completely.
- Vertical Autoscaling isn't supported with
  [VPC Service Controls](/vpc-service-controls/docs/overview). If you enable
  Dataflow Prime and launch a new job within a VPC Service Controls
  perimeter, the job uses [Dataflow Prime without Vertical
  Autoscaling](/dataflow/docs/guides/enable-dataflow-prime#features).
- When you use right fitting with Vertical Autoscaling, only batch pipelines
  are supported.

## Monitor Vertical Autoscaling

Vertical Autoscaling operations are published to the job and worker logs. To
view these logs, see [Dataflow job
metrics](/dataflow/docs/guides/using-monitoring-intf).

## Effect on Horizontal Autoscaling

In [Dataflow Prime](/dataflow/docs/guides/enable-dataflow-prime), Vertical
Autoscaling works alongside [Horizontal
Autoscaling](/dataflow/docs/horizontal-autoscaling). This combination enables
Dataflow Prime to seamlessly scale workers up or down to best fit the needs
of your pipeline and maximize the utilization of the compute capacity.

By design, Vertical Autoscaling (which adjusts the worker memory) occurs at a
lower frequency than Horizontal Autoscaling (which adjusts the number of
workers). Horizontal Autoscaling is deactivated during and up to 10 minutes
after an update is triggered by Vertical Autoscaling. If there exists a
significant backlog of input data after this 10-minute mark, Horizontal
Autoscaling is likely to occur to clear that backlog. To learn about Horizontal
Autoscaling for streaming pipelines, see [Streaming
autoscaling](#streaming).

## Troubleshooting

This section provides instructions for troubleshooting common issues related to
vertical autoscaling.

### Vertical Autoscaling does not seem to work

If Vertical Autoscaling isn't working, check the following job details.

- Check for the following job message to verify that Vertical Autoscaling is
  active:
  `Vertical Autoscaling is enabled. This pipeline is receiving recommendations
for resources allocated per worker.`

  The absence of this message indicates that Vertical Autoscaling is not
  running.

- For streaming pipelines, verify that the
  `enable_vertical_memory_autoscaling` flag is set. For batch pipelines,
  verify that the `enable_vertical_memory_autoscaling` and the
  `enable_batch_vmr` flags are set.
- Verify that you enabled the Cloud Autoscaling API for your Google Cloud project.
  [Enable the API](https://console.cloud.google.com/flows/enableapi?apiid=autoscaling.googleapis.com)
- Verify that your job is running Dataflow Prime. For more information, see
  [Enabling
  Dataflow Prime](/dataflow/docs/guides/enable-dataflow-prime#enable-prime).

### Job observes high backlog and high watermark

These instructions only apply to streaming jobs. If the vertical reshaping of
workers takes longer than a few minutes, your
job might exhibit a high backlog of the input data and a high watermark. To
address this issue in Python pipelines, we strongly recommend that you
[use custom containers](/dataflow/docs/guides/using-custom-containers), because
they can improve the latency that might arise from reshaping the workers. To
address this issue in Java pipelines, we strongly recommend that you enable
[Streaming Engine](/dataflow/docs/streaming-engine)
and [Runner v2](/dataflow/docs/runner-v2).
If the issue persists after enabling these features, contact
[Customer Care](https://cloud.google.com/support-hub).

### Vertical Autoscaling has reached the memory capacity.

By default, if no resource hints are provided, Vertical Autoscaling does not
scale memory beyond 16 GiB per worker (26 GiB when using GPUs) or less
than 6  GiB per worker (12 GiB when using GPUs). When these limits are
reached, one of the following log messages is generated in Cloud Logging.

Streaming jobs:

`Vertical Autoscaling has a desire to upscale memory, but we have hit the memory
scaling limit of X GiB. This is only a problem if the pipeline continues to see
memory throttling and/or OOMs.`

Batch jobs:

`Vertical Autoscaling has a desire to upscale memory, but we have hit the memory
scaling limit of 16.0 GiB. Job will fail because we have upsized to maximum
size, and the pipeline is still OOMing.`

If your pipeline continues to see out-of-memory errors, you can use [right
fitting](/dataflow/docs/guides/right-fitting) (resource hints) to define memory
requirements for your transform by specifying `min_ram="numberXB"`. This setting
allows Dataflow to select an initial configuration for your
workers that can support a higher memory capacity. However, changing this
initial configuration can increase the latent parallelism available to your
pipeline. If you have a memory-hungry transform, this might result in your
pipeline using more memory than before due to the increased available
parallelism. In such cases, it might be necessary to optimize your transform to
reduce its memory footprint.

**Note:** Vertical Autoscaling does not prevent OOM errors from appearing in the
worker logs. If an OOM error occurs, it is visible in the worker logs, because
Vertical Autoscaling finds and tracks the OOM events.

### Worker memory limit doesn't stabilize and goes up and down over time despite constant memory use

These instructions only apply to streaming jobs.
For Java pipelines, enable [Streaming Engine](/dataflow/docs/streaming-engine)
and [Runner v2](/dataflow/docs/runner-v2).
If the issue persists or if you observe this behavior in Python pipelines,
contact [Customer Care](https://cloud.google.com/support-hub).

## Common log messages

This section describes the common log messages generated when you enable
Vertical Autoscaling.

### Vertical Autoscaling is enabled. This pipeline is receiving recommendations for resources allocated per worker.

This message indicates that Vertical Autoscaling is active. The absence of this
message indicates that Vertical Autoscaling is not operating on the worker pool.

If Vertical Autoscaling is not active, see [Vertical Autoscaling does not seem
to work. What should I
check?](/dataflow/docs/vertical-autoscaling#vertical_autoscaling_does_not_seem_to_work_what_should_i_check)
for troubleshooting instructions.

### Vertical Autoscaling update triggered to change per worker memory limit for pool from X GiB to Y GiB.

This message indicates that Vertical Autoscaling has triggered a resize of the
worker pool memory.
