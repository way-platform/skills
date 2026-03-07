# Dataflow Python: Resource Management & Autoscaling

Cost efficiency and performance in Dataflow rely heavily on proper resource management and taking advantage of Google Cloud's managed autoscaling features.

## Right-Sizing Workers & Hardware (2026 Update)
*   **Arm-Based Workers (C4A Series):** In early 2026, Google Cloud made the C4A Arm-based worker series generally available for Dataflow. These provide significantly better price-performance than the N2 series for most Python-based workloads.
*   **Vertical Autoscaling:** Enable Vertical Autoscaling to allow Dataflow to automatically adjust memory and CPU allocations for workers dynamically without restarting the pipeline.
*   **Speculative Execution:** For batch pipelines, enable speculative execution to mitigate "stragglers" (slow workers). Dataflow will detect lagging tasks and launch redundant copies on other workers to ensure the fastest overall completion time.

## Off-Worker Services
Always enable these managed services to offload work from your VMs:
*   **Streaming Engine (`--enable_streaming_engine`):** Moves state, timers, and windowing logic off the worker VMs to a Google-managed backend. Drastically improves autoscaling responsiveness.
*   **Dataflow Shuffle (`--experiments=shuffle_mode=service`):** For batch pipelines, moves the `GroupByKey` shuffle operations to a managed service, reducing the need for large worker disks and speeding up execution.

## FlexRS for Batch
For non-time-critical batch jobs, use **Flexible Resource Scheduling (FlexRS)** (`--flexrs_goal=COST_OPTIMIZED`). This delays execution up to 6 hours to find cheaper preemptible VMs, reducing costs by up to 40%.

## References & Further Reading
*   [Google Cloud: Dataflow Autoscaling](https://cloud.google.com/dataflow/docs/guides/deploying-a-pipeline#autoscaling)
*   [Google Cloud: Using Flexible Resource Scheduling (FlexRS)](https://cloud.google.com/dataflow/docs/guides/flexrs)
