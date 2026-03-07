---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/troubleshoot-stragglers
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Troubleshoot stragglers in batch jobs \u00a0|\u00a0 Cloud Dataflow \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

_Stragglers_ are work items that slow down your Dataflow jobs by
preventing work from being done in parallel.

For batch pipelines, a straggler is defined as a work item with the
following characteristics:

- It takes significantly longer to complete than other work items in the same
  stage.
- It reduces parallelism within the stage.
- It blocks new work from starting.

In the worst case, a straggler blocks a stage from completion because a small
percentage of the work is in progress, causing overall delays in a job.

Dataflow detects stragglers that occur during batch jobs. If
Dataflow detects a straggler, it also tries to determine the cause
of the straggler.

**Note:** For information about troubleshooting stragglers in streaming jobs, see
[Troubleshoot stragglers in streaming jobs](/dataflow/docs/guides/troubleshoot-streaming-stragglers).

## View stragglers in the Google Cloud console

After you start a Dataflow job, you can use the Google Cloud console
to view any detected stragglers.

You can view stragglers either by stage or by worker. Use these views to find
which stages have stragglers, and then pinpoint the workers where stragglers
occurred within each stage.

### View stragglers by stage

To view stragglers by stage:

1. In the Google Cloud console, go to the Dataflow **Jobs**
   page.

   Go to [Jobs](https://console.cloud.google.com/dataflow/jobs)

2. Click the name of the job.
3. In the job details page, click the **Execution details** tab.
4. In the **Graph view** list, select **Stage progress**. The progress graph
   shows aggregated counts of all stragglers detected within each stage.

   ![](/static/dataflow/images/stragglers-by-stage.png)

5. To see details for a stage, hold the pointer over the bar for a stage. To
   view the workers for the stage, click **View workers** in the details panel.

### View stragglers by worker

To view stragglers by worker:

1. In the Google Cloud console, go to the Dataflow **Jobs**
   page.

   Go to [Jobs](https://console.cloud.google.com/dataflow/jobs)

2. Click the name of the job.
3. In the job details page, click the **Execution details** tab.
4. In the **Graph view** list, select **Worker progress**.
5. In the **Filter workers by stage** list, select the stage. The progress graph
   shows any stragglers detected for that stage. The bar has darker shading at
   the point where the straggler was first detected.

   ![](/static/dataflow/images/stragglers-by-worker.png)

6. To see details for a worker, hold the pointer over the bar for that worker.

In the **Stage info** panel, the **Straggler details** section lists the
stragglers for all workers shown on the page, with the following information:

- The start time when the straggler was detected.
- The worker that experienced the straggler.
- The cause, if known.

## Troubleshoot batch stragglers

Dataflow detects the following causes of stragglers in batch
pipelines:

- **Hot key**. A _hot key_ is a key that represents significantly more elements
  than other keys in the same `PCollection`. For more information, see
  [Troubleshoot stragglers caused by hot keys](#troubleshoot_stragglers_caused_by_hot_keys)
  in this document.
- **Slow Worker**. On a _slow worker_, work items run
  more slowly than usual. Often, the processing speed of a slow worker is
  less than the processing speed of workers doing similar work at the same stage.
  Many factors can cause worker slowness, including CPU starvation, thrashing,
  machine architecture, and stuck worker processes.
  When slowness occurs, Dataflow attempts to mitigate the issue
  automatically. For more information, see
  [Automatically mitigate stragglers caused by slow workers](#slow-workers) in this
  document.
- **Undetermined cause**. For stragglers with undetermined cause, see the
  general troubleshooting steps for
  [slow batch jobs](/dataflow/docs/guides/troubleshoot-slow-batch-jobs)
  in "Troubleshoot slow or stuck jobs."

### Troubleshoot stragglers caused by hot keys

Various factors can cause stragglers, but one common cause is the existence of
a _hot key_. A hot key is a key that represents significantly more elements than
other keys in the same `PCollection`. Hot keys can create stragglers because
they limit Dataflow's ability to process elements in parallel.

If Dataflow detects a straggler caused by a hot key, the
**Straggler Details** panel lists `Hot Key` as the cause.

By default, Dataflow does not display the key value of the
hot key. To display the key value, set the
[`hotKeyLoggingEnabled`](/dataflow/docs/reference/pipeline-options#debugging)
pipeline option to `true` when you run the job.

To resolve this issue, check that your data is evenly distributed. If a key has
disproportionately many values, consider the following courses of action:

- Rekey your data. Apply a
  [`ParDo`](https://beam.apache.org/documentation/programming-guide/#pardo)
  transform to output new key-value pairs.
- For Java jobs, use the [`Combine.PerKey.withHotKeyFanout`](https://beam.apache.org/releases/javadoc/current/org/apache/beam/sdk/transforms/Combine.PerKey.html)
  transform.
- For Python jobs, use the [`CombinePerKey.with_hot_key_fanout`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.CombinePerKey.with_hot_key_fanout)
  transform.
- Enable [Dataflow Shuffle](/dataflow/docs/shuffle-for-batch).

**Note:** Apache Beam SQL cannot reshuffle data that contains hotkeys during
sub-transforms.

For example, if a pipeline performs a `JOIN` operation as part of a SQL
transform, then a given key is likely to contain a disproportionate amount of
data when it is fed into the `GroupByKey` that is performed as part of the
expanded `JOIN` operation.

For more information, see the following feature request:
[beam-issue/28186](https://github.com/apache/beam/issues/28186).

### Automatically mitigate stragglers caused by slow workers

Slow workers are uncommon on Dataflow but can impact
job performance. To prevent performance issues, when Dataflow detects
slow workers, it tries to mitigate the problem before the workers cause
stragglers.

The automatic mitigation
[simulates a host maintenance event](/compute/docs/instances/simulating-host-maintenance).
The event is a Compute Engine maintenance mechanism that happens regularly.
Depending on the worker's
[host maintenance policy](/compute/docs/instances/host-maintenance-overview#schedulingoptions),
the worker is either live migrated or restarted. If a live migration occurs, the workload isn't interrupted.
If the worker is restarted, the ongoing work from the slow worker is lost,
and processing restarts.

If a slow worker is detected and successfully mitigated,
the following message displays in the **job-message** logs:

```
Slow worker ... detected and automatically remediated ...
```

Because slow workers are not stragglers, you don't need to take further action.

If mitigation is unsuccessful, the slow worker causes a straggler that
displays in the Dataflow monitoring interface.

Automatic mitigation might fail if your project runs out of quota for requests
to simulate a maintenance event on instances. For more information about the
default quota, see [API rate limits for regional
metrics](/compute/resource-usage#api-rate-limits-regional) in "Resource usage
quotas and permission management." To request a higher quota limit, see
[Requesting a quota adjustment](/docs/quotas/help/request_increase) in "View and
manage quotas."

### Use speculative execution to avoid stragglers

For batch pipelines, you can enable speculative execution to mitigate the impact
of stragglers. For more information, see [Best practices for large batch
pipelines](/dataflow/docs/guides/large-pipeline-best-practices#backup-tasks).

## What's next

- Learn to use the
  [Dataflow monitoring interface](/dataflow/docs/guides/using-monitoring-intf).
- Understand the
  [**Execution details**](/dataflow/docs/concepts/execution-details) tab in the
  monitoring interface.
