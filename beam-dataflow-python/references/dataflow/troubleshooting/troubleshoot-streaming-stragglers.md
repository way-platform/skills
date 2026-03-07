---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/troubleshoot-streaming-stragglers
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Troubleshoot stragglers in streaming jobs \u00a0|\u00a0 Cloud Dataflow \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

For streaming pipelines, a _straggler_ is defined as a work item with the
following characteristics:

- It prevents the
  [watermark](/dataflow/docs/concepts/beam-programming-model#advanced_concepts)
  from advancing for a significant length of time (on the order of minutes).
- It processes for a long time relative to other work items in the same stage.

Stragglers hold back the watermark and add latency to the job. If the lag is
acceptable for your use case, then you don't need to take any action. If you
want to reduce a job's latency, start by addressing any stragglers.

**Note:** For information about troubleshooting stragglers in batch jobs, see
[Troubleshoot stragglers in batch
jobs](/dataflow/docs/guides/troubleshoot-batch-stragglers).

## View streaming stragglers in the Google Cloud console

After you start a Dataflow job, you can use the Google Cloud console
to view any detected stragglers.

You can view streaming stragglers in the [stage progress
view](/dataflow/docs/concepts/execution-details#stage_progress_for_streaming_jobs)
or the [stage workflow
view](/dataflow/docs/concepts/execution-details#stage_workflow).

### View stragglers by stage progress

To view stragglers by stage progress:

1. In the Google Cloud console, go to the Dataflow **Jobs**
   page.

   [Go to Jobs](https://console.cloud.google.com/dataflow/jobs)

2. Click the name of the job.
3. In the **Job details** page, click the **Execution details** tab.
4. In the **Graph view** list, select **Stage progress**. The progress graph
   shows aggregated counts of all stragglers detected within each stage.

   ![A screenshot of the stage progress view.](/static/dataflow/images/streaming-straggler-stage-progress.png)

5. To see details for a stage, hold the pointer over the bar for the stage. The
   details pane includes a link to the worker logs. Clicking this link opens
   Cloud Logging scoped to the worker and the time range when the straggler
   was detected.

   ![A screenshot of the straggler details card.](/static/dataflow/images/streaming-straggler-details.png)

### View stragglers by stage workflow

To view stragglers by stage workflow:

1. In the Google Cloud console, go to the Dataflow **Jobs**
   page.

   Go to [Jobs](https://console.cloud.google.com/dataflow/jobs)

2. Click the name of the job.
3. In the job details page, click the **Execution details** tab.
4. In the **Graph view** list, select **Stage workflow**. The stage workflow
   shows the execution stages of the job, represented as a workflow graph.

   ![A screenshot of the stage workflow view.](/static/dataflow/images/streaming-straggler-stage-workflow.png)

## Troubleshoot streaming stragglers

If a straggler is detected, it means that an operation in your pipeline has
been running for an unusually long time.

To troubleshoot the issue, first check whether
[Dataflow insights](/dataflow/docs/guides/using-dataflow-insights)
pinpoints any issues.

If you still can't determine the cause, check the worker logs for the stage that
reported the straggler. To see the relevant worker logs, view the
[straggler details](#view_stragglers_by_stage_progress) in the stage progress.
Then click the link for the worker. This link opens Cloud Logging, scoped to
the worker and the time range when the straggler was detected. Look for problems
that might be slowing down the stage, such as:

- Bugs in `DoFn` code or
  [stuck `DoFns`](/dataflow/docs/guides/common-errors#processing-stuck). Look
  for stack traces in the logs, near the timestamp when the straggler was
  detected.
- Calls to external services that take a long time to complete. To mitigate this
  issue,
  [batch calls to external services](/dataflow/docs/tutorials/ecommerce-java#micro-batch-calls)
  and set timeouts on RPCs.
- Quota limits in sinks. If your pipeline outputs to a Google Cloud
  service, you might be able to raise the quota. For more information, see
  the [Cloud Quotas documentation](/docs/quotas/overview). Also, consult the documentation for the
  particular service for optimization strategies, as well as the documentation
  for the
  [I/O Connector](https://beam.apache.org/documentation/io/connectors/).
- `DoFns` that perform large read or write operations on persistent state.
  Consider refactoring your code to perform smaller reads or writes on
  persistent state.

You can also use the
[**Side info**](/dataflow/docs/concepts/execution-details#stage-info)
panel to find the slowest steps in the stage. One of these steps might be
causing the straggler. Click on the step name to view the worker logs for that
step.

After you determine the cause,
[update your pipeline](/dataflow/docs/guides/updating-a-pipeline) with new
code and monitor the result.

## What's next

- Learn to use the
  [Dataflow monitoring interface](/dataflow/docs/guides/using-monitoring-intf).
- Understand the
  [**Execution details**](/dataflow/docs/concepts/execution-details) tab in the
  monitoring interface.
