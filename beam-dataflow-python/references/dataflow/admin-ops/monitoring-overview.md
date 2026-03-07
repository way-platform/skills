---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/monitoring-overview
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Use the Dataflow job monitoring interface \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

When you run your pipeline by using Dataflow,
you can view that job and any others by using the Dataflow monitoring
interface. The monitoring interface lets you see and
interact with your Dataflow jobs.

You can access the Dataflow monitoring interface in the
[Google Cloud console](https://console.cloud.google.com/).

Tasks that you can perform by using the monitoring interface include the
following:

- See a list of running, completed, and failed jobs.
- View a graphical representation of a job's stages and the progress of each
  stage
- View graphs of job metrics, such as data freshness, resource utilization, and
  I/O requests.
- Monitor the estimated cost of a job.
- View pipeline logs.
- Identify which steps might cause pipeline lag.
- Identify causes of latency in your sources and sinks.
- Understand pipeline errors.

**Note:** Sometimes job data is intermittently unavailable. When data is missing, gaps appear in
the job monitoring charts.

## Monitoring interface components

The monitoring interface contains the following visualizers and charts:

[Project monitoring dashboard](/dataflow/docs/guides/project-monitoring)
: A dashboard that monitors your Dataflow jobs at the project
level.

[Jobs list](/dataflow/docs/guides/jobs-list)
: A list of all running Dataflow jobs and all jobs run within the
last 30 days, along with their status, region, elapsed time, and other
information.

[Job graph](/dataflow/docs/guides/job-graph)
: A graphical representation of a pipeline. The job graph also provides a job
summary, a job log, and information about each step in the pipeline.

[Execution details](/dataflow/docs/concepts/execution-details)
: Shows the execution stages of a job, data freshness for streaming jobs, and
worker progress for batch jobs.

[Job metrics](/dataflow/docs/guides/using-monitoring-intf)
: Charts that display metrics over the duration of a job.

[Estimated cost](/dataflow/docs/guides/estimated-cost)
: The estimated cost of your Dataflow job, based on resource
usage metrics.

[Recommendations](/dataflow/docs/guides/recommendations)
: Recommendations for improving job performance, reducing cost, and
troubleshooting errors.

[Autoscaling](/dataflow/docs/guides/autoscaling-metrics)
: A set of charts that help you to understand the autoscaling behavior of
streaming jobs.

[Pipeline logs](/dataflow/docs/guides/logging)
: Logs emitted by your pipeline and by the Dataflow service.

[Data sampling](/dataflow/docs/guides/data-sampling)
: A tool that lets you observe sampled data at each step of a pipeline.

## What's next

- Use [Cloud Monitoring](/dataflow/docs/guides/using-cloud-monitoring) to create alerts and view Dataflow metrics, including custom metrics
- Learn more about [building production-ready data pipelines](/architecture/building-production-ready-data-pipelines-using-dataflow-monitoring)
- Learn how to [troubleshoot your pipeline](/dataflow/docs/guides/troubleshooting-your-pipeline?)
