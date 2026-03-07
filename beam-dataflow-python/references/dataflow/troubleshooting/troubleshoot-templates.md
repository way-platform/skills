---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/troubleshoot-templates
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Troubleshoot Flex Templates \u00a0|\u00a0 Cloud Dataflow \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-04 UTC."
---

This page provides troubleshooting tips and debugging strategies that you might find helpful if you're
using Dataflow Flex Templates.
This information can help you detect a polling timeout, determine the reason behind the timeout, and correct the problem.

## Polling timeout errors

Your job might return one of the following error messages:

```
Timeout in polling result file: FILE_PATH. Possible causes are:
1. Your launch takes too long time to finish. Please check the logs on stackdriver.
2. Service account SERVICE_ACCOUNT may not have enough permissions to pull
container image IMAGE_PATH or create new objects in FILE_PATH.
3. Transient errors occurred, please try again.
```

```
Timeout in polling result file: FILE_PATH.
Service account: SERVICE_ACCOUNT
Image URL: IMAGE_PATH
Troubleshooting guide at https://cloud.google.com/dataflow/docs/guides/common-errors#timeout-polling
```

This error can occur for the following reasons:

1. [The base Docker image was overridden.](#docker-entrypoint)
2. [The service account that fills in SERVICE_ACCOUNT does not
   have some necessary permissions.](#service-account)
3. [External IP addresses are disabled, and VMs can't connect to the set of
   external IP addresses used by Google APIs and services.](#private-access)
4. [The launcher VM cannot resolve or access gcr.io.](#gcr-io-access)
5. [The program that creates the graph takes too long to finish.](#launcher)
6. [Code running in the launcher VM takes too long to finish.](#long-running-code)
7. [Intermittent network or Cloud Storage errors.](#intermittent-errors)
8. [Pipeline options are being overwritten.](#required-options)
9. [Python users: Installing or staging dependencies takes too long.](#python-requirements)
10. There was a transient error.

To resolve this issue, first check for transient errors by checking the job logs
and retrying.

Follow the guidance in the [Early startup issues](#serial-port-logging) section
to enable serial port logging, which might reveal additional information.

If those steps don't resolve the issue, try the following troubleshooting steps.

### Optional: Run templates to further diagnose your issue

To further identify which of the previous reasons might be causing this error,
use the following strategies:

1. Run the [WordCount](/dataflow/docs/sample-template) Google-provided
   template. Be sure to provide parameters unique to your use case, such as the
   subnetwork from a Shared VPC project, private IP for worker VMs, and
   Dataflow worker service account you want to use. For more
   information on how to provide these parameters, see the [gcloud
   Reference](/sdk/gcloud/reference/dataflow/jobs/run) and [API
   Reference](/dataflow/docs/reference/rest/v1b3/projects.templates/launch).

   If you're able to complete this job successfully, that indicates that
   Networking, IAM Permissions, and [Private Google Access](/vpc/docs/private-google-access) are likely
   configured correctly.

2. Complete the [Run a pipeline by using the job
   builder](/dataflow/docs/quickstarts/create-pipeline-job-builder) quickstart,
   which runs the job as a Flex Template. If your job fails before launching
   the worker VM, [access the launcher VM](/compute/docs/connect/standard-ssh)
   and try to download a sample Docker image using a command similar to the
   following:

   ```
   docker run --entrypoint /bin/bash -it gcr.io/dataflow-templates/2025-03-11-00_rc02/yaml-template
   ```

   If this command fails, there may be a networking issue with
   downloading images. In this case, work with your internal networking team.

3. Run a [Google-provided Flex
   Template](/dataflow/docs/guides/templates/provided-templates) and check
   the result. If the Google-provided template job completes successfully, this
   indicates that the problem is likely related to your specific custom
   template code files. In this case you need to continue troubleshooting your
   specific code to resolve the issue.

### Verify Docker entrypoint

Try this step if you're running a template from a custom Docker image rather
than using one of the provided templates.

Check for the container entrypoint using the following command:

```
docker inspect $TEMPLATE_IMAGE
```

The following output is expected:

### Java

`/opt/google/dataflow/java_template_launcher`

### Python

`/opt/google/dataflow/python_template_launcher`

If you get a different output, then the entrypoint of your Docker container is
overridden. Restore `$TEMPLATE_IMAGE` to the default.

### Check service account permissions

Check that the service account mentioned in the message has the following
permissions:

- It must be able read and write the Cloud Storage path that fills in
  `${file_path}` in the message.
- It must be able to read the Docker image that fills in `${image_url}` in the
  message.

### Configure Private Google Access

If external IP addresses are disabled, you need to allow Compute Engine
VMs to connect to the set of external IP addresses used by
[Google APIs and services](https://developers.google.com/apis-explorer/). Enable
Private Google Access on the subnet used by the network interface of the VM.

For configuration details, see
[Configuring Private Google Access](/vpc/docs/configure-private-google-access).

By default, when a Compute Engine VM lacks an external IP address
assigned to its network interface, it can only send packets to other internal
IP address destinations.

### GCR.io access issues

Flex Template launcher VMs require access to `gcr.io` to pull a logging agent
container
(`gcr.io/dataflow-templates-base/template-launcher-logger-distroless`). This
agent is responsible for streaming launcher logs to Cloud Logging. If the
launcher VM cannot resolve or connect to `gcr.io`, the startup process might
stop responding, leading to a polling timeout.

This issue can occur even if your custom template image is stored in
Artifact Registry, because the logging agent is always pulled from `gcr.io`.

To diagnose and resolve this issue:

1. **Enable serial port logging**: Follow the steps in the [Early startup
   issues](#serial-port-logging) section. If you see that the `cloud-init`
   process is stuck or if there are errors related to
   `gcr-wait-online.service`, a DNS or networking issue is likely.
2. **SSH into the launcher VM**: Use the `gcloud compute ssh` command to
   connect to the launcher VM while it is still running:

   ```
   gcloud compute ssh launcher-JOB_ID --tunnel-through-iap
   ```

   Replace `JOB_ID` with the ID of your Dataflow job.

3. **Verify DNS resolution**: Run the following commands inside the launcher
   VM:

   ```
   curl -I https://gcr.io
   ```

   If the command fails with a
   `"Could not resolve host"` error, your DNS configuration is missing an entry
   for `gcr.io`.

4. **Check for stuck startup services**: Examine the `cloud-init` output log:

   ```
   sudo cat /var/log/cloud-init-output.log
   ```

   Look for messages
   indicating that the process is waiting for the network or for `gcr.io` to
   become accessible.

Additionally, make sure that your VPC's DNS settings allow for the resolution of
`gcr.io`. In some private network configurations, you might need to add a
specific DNS `A` record for `gcr.io` pointing to the [Restricted Google APIs or
Private Google APIs](/vpc/docs/configure-private-google-access#config-options)
IP ranges.

### Check if the launcher program fails to exit

The program that constructs the pipeline must finish before the pipeline can
be launched. The polling error could indicate that it took too long to do so.

Some things you can do to locate the cause in code are:

- Make sure no threads are blocking the program from exiting. Some clients
  might create their own threads, and if these clients are not shut down, the
  program waits forever for these threads to be joined.
- In the code that defines your pipeline, don't use `waitUntilFinish` (for
  Java) or `wait_until_finish` (for Python). These functions block the program
  from exiting, which prevents the Flex Template from launching the pipeline.

Pipelines launched directly that don't use a template don't have these
limitations. Therefore, if the pipeline worked directly but not as a
template, then the use of a template might be the root cause. Finding the issue
in the template and fixing the template might resolve the issue.

### Long-running code in the launcher VM

If the code in your main program takes too long to execute, the Flex Template
might time out before the pipeline launches. This can happen if the code
performs complex computations or makes synchronous calls to external resources
during initialization.

To diagnose this issue, [check the job
logs](/dataflow/docs/guides/logging#MonitoringLogs) for any operation that takes
a long time to complete. Examples include requests for external resources, large
data lookups, or heavy initialization logic that you can move to the pipeline
execution phase.

### Intermittent network or Cloud Storage errors

Intermittent "Timeout in polling result file" or "Failed to read the result
file" errors can occur due to high network latency or transient issues with the
Cloud Storage API. Chronic network contention in your VPC, specifically within the
Private Google Access path, often causes latencies of 400–500 ms.

A "Timeout in polling result file" is typically a slow failure, while a "Failed
to read the result file" is a fast failure, but both often indicate the same
underlying connectivity issue.

To diagnose these intermittent failures:

1. **Check for network latency**: Monitor the network latency within your VPC.
   Sustained high latency can cause timeouts when the launcher VM attempts to
   write or read the job result file from Cloud Storage.
2. **Monitor Cloud Storage API metrics**:
   1. In the Google Cloud console, navigate to the **APIs & Services** dashboard.

      [Go to Enabled APIs & services](https://console.cloud.google.com/project/_/apis/dashboard)

   2. Filter and select the **Cloud Storage API**.
   3. Review the charts for **Traffic** (sent and received bytes) and **Error
      rate**.
   4. Look for spikes in **5xx errors** (such as 503 errors) that align with
      the exact time of the job failures.

If you identify spikes in errors or high latency, investigate your VPC's network
performance or [contactCloud Customer Care](/dataflow/docs/support/getting-support)
for assistance with potential service disruptions.

### Verify whether required pipeline options are suppressed

When using Flex Templates, you can configure some but not all pipeline options during
pipeline initialization. For
more information, see the [Failed to read the job file](#read-job-file)
section in this document.

### Python users: Dependency management

If you're running a Python Flex Template job that supplies extra dependencies in
a `requirements.txt` file, your job might fail to launch. This failure happens
when downloading or installing the dependencies specified in the requirements
file takes longer than the time allocated for launching the Flex template.

To optimize your job's performance, prepackage the dependencies when building
your template to avoid the necessity to download or install the dependencies
during template launch. For more information, see the
[Package dependencies for Python](/dataflow/docs/guides/templates/configuring-flex-templates#dependencies-python)
section in "Configure Flex Templates."

## Job launch failures

The following section contains common errors that lead to job launch failures
and steps for resolving or troubleshooting the errors.

### Early startup issues

When the template launching process fails in an early stage, regular Flex
Template logs might not be available. To investigate startup issues, enable
[serial port logging](/compute/docs/troubleshooting/viewing-serial-port-output)
for the templates launcher VM.

To enable logging for Java templates, set the
`enableLauncherVmSerialPortLogging` option to `true`. To enable logging for Python and Go templates, set the
`enable_launcher_vm_serial_port_logging` option to `true`. In the Google Cloud console, the parameter is
listed in **Optional parameters** as **Enable Launcher VM Serial Port Logging**.

You can view the serial port output logs of the templates launcher VM in
Cloud Logging. To find the logs for a particular launcher VM, use the query
`resource.type="gce_instance" "launcher-number"` where number starts
with the current date in the format `YYYMMDD`.

[Your organization policy](/compute/docs/troubleshooting/viewing-serial-port-output#setting_an_organization_policy)
might prohibit you from enabling serial port outputs logging.

### Failed to read the job file

When you try to run a job from a Flex Template, your
job might fail with the following error:

```
Failed to read the job file : gs://dataflow-staging-REGION-PROJECT_ID/staging/template_launches/TIMESTAMP/job_object...
```

This error occurs when the necessary pipeline initialization options are overwritten. When
using Flex Templates, you can configure some but not all pipeline options during pipeline
initialization.
If the command line arguments required by the Flex Template are overwritten,
the job might ignore, override, or discard the pipeline options
passed by the template launcher. The job might fail to launch, or a job that
doesn't use the Flex Template might launch.

To avoid this issue, during pipeline initialization, don't change the following
[pipeline options](/dataflow/docs/reference/pipeline-options)
in user code or in the `metadata.json` file:

### Java

- `runner`
- `project`
- `jobName`
- `templateLocation`
- `region`

### Python

- `runner`
- `project`
- `job_name`
- `template_location`
- `region`

### Go

- `runner`
- `project`
- `job_name`
- `template_location`
- `region`

### Failed to read the result file

When you try to run a job from a Flex Template, your
job might fail with the following error:

```
Failed to read the result file : gs://BUCKET_NAME...
```

This error occurs when the [Compute Engine default service
account](/compute/docs/access/service-accounts#default_service_account) doesn't
have all the permissions that it needs to run a Flex Template.

For the list of required permissions, see [Permissions to run a Flex
Template](/dataflow/docs/guides/templates/configuring-flex-templates#permissions_to_run_a_flex_template).

This error can also be caused by intermittent network latency or Cloud Storage API
issues. For more information, see [Intermittent network or Cloud Storage
errors](#intermittent-errors).

### Permission denied on resource

When you try to run a job from a Flex Template, your
job might fail with the following error:

```
Permission "MISSING_PERMISSION" denied on resource "projects/PROJECT_ID/locations/REGION/repositories/REPOSITORY_NAME" (or it may not exist).
```

This error occurs when the used service account does not have
permissions to access necessary resources to run a Flex Template.

To avoid this issue, verify that the service account has the
[required permissions](/dataflow/docs/guides/templates/configuring-flex-templates#permissions_to_run_a_flex_template).
Adjust the service account permissions as needed.

### Flag provided but not defined

When you try to run a Go Flex Template with the `worker_machine_type` pipeline
option, the pipeline fails with the following error:

```
flag provided but not defined: -machine_type
```

This error is caused by a known issue in the Apache Beam Go SDK versions
2.47.0 and earlier. To resolve this issue, upgrade to Apache Beam Go version
2.48.0 or later.

### Unable to fetch remote job server jar

If you try to run a job from a Flex Template when you're not connected to the
internet, your job might fail with the following error:

```
Unable to fetch remote job server jar at
https://repo.maven.apache.org/maven2/org/apache/beam/beam-sdks-java-io-expansion-service/VERSION/beam-sdks-java-io-expansion-service-VERSION.jar:
\u003curlopen error [Errno 101] Network is unreachable\u003e
```

This error occurs because the VM is unable to download the Apache Beam
Java package from the internet. This package is required when you run a
multi-language job by using a Flex Template.

To resolve this issue, make one of the following changes:

- Connect to the internet. When connected to the internet, your job can access
  the required file.
- Include the Apache Beam Java package in your local directory so that your
  job can access it locally. Put the file in the following directory:
  `/root/.apache_beam/cache/jars/`. For example,
  `/root/.apache_beam/cache/jars/beam-sdks-java-io-expansion-service-SDK_VERSION.jar`.

### Unable to get filesystem from specified path

When you try to run a job from a Flex Template, your
job might fail with the following error:

```
ValueError: Unable to get filesystem from specified path, please use
the correct path or ensure the required dependency is installed, e.g., pip
install apache-beam[gcp]. Path specified: PATH
```

This error occurs when the job uses a Flex Template container image, and the
container image doesn't contain a Java installation.

To resolve this issue, add the following line to your Dockerfile:

`sh
RUN apt-get update && apt-get install -y openjdk-17-jdk`

This command installs Java in your container environment.

### Launcher VM resource exhaustion

When you try to run a job from a Flex Template, your job might fail with the
following error:

```
Failed to start the VM, launcher-ID, used for launching because of status code: INTERNAL, reason: Unknown error in operation 'OPERATION_ID': [ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS] 'The zone 'projects/PROJECT_ID/zones/ZONE_ID' does not have enough resources available to fulfill the request.
```

The VM name `launcher-ID` represents the launcher VM name. The launcher VM is
responsible for gathering job resources, such as the template code and image,
before building and submitting the job graph to the Dataflow
service to start work.

By default, the `launcherMachineType` is `n1-standard-1` regardless of the
worker `machineType` selected.

To resolve this issue, use one of the following strategies:

- Update the launcher machine type to a different [machine
  type](/dataflow/docs/guides/configure-worker-vm) and retry the job.
  - REST API: Set
    [`launchParameter.environment.launcherMachineType`](/dataflow/docs/reference/rest/v1b3/projects.locations.flexTemplates/launch#flextemplateruntimeenvironment)
    in the `flexTemplates.launch` method.
  - gcloud CLI: Set the [`--launcher-machine-type`](/sdk/gcloud/reference/dataflow/flex-template/run#--launcher-machine-type)
    flag in the `gcloud dataflow flex-template run` command.
- Launch your Flex Template from a different
  [region](/dataflow/docs/resources/locations).

## Flex Template launcher delay

When you submit a Flex Template job, the job request goes into
a Spanner queue. The template launcher picks up the job from the
Spanner queue and then runs the template. When Spanner has a
message backlog, a significant delay might occur between the time you submit
the job and the time the job launches.

To work around this issue, launch your Flex Template from a different region.

## The template parameters are invalid

When you try to use the gcloud CLI to run a job that uses a
[Google-provided template](/dataflow/docs/guides/templates/provided-templates),
the following error occurs:

```
ERROR: (gcloud.beta.dataflow.flex-template.run) INVALID_ARGUMENT: The template
parameters are invalid. Details: defaultSdkHarnessLogLevel: Unrecognized
parameter defaultWorkerLogLevel: Unrecognized parameter
```

This error occurs because some Google-provided templates don't support the
`defaultSdkHarnessLog` and `defaultWorkerLog` options.

As a workaround, copy the template specification file to a Cloud Storage bucket. Add
the following additional parameters to the file.

After you make this change to the template file, use the following command to
run the template.

```
--template-file-gcs-location=gs://BUCKET_NAME/FILENAME
```

Replace the following values:

- `BUCKET_NAME`: the name of your Cloud Storage bucket
- `FILENAME`: the name of your template specification file

## Flex Template launcher logs show wrong severity

When a [custom Flex Template](/dataflow/docs/guides/templates/using-flex-templates)
launch fails, the following message appears in the log files with the severity
`ERROR`:

```
ERROR: Error occurred in the launcher container: Template launch failed. See console logs.
```

The root cause of the launch failure usually appears in the logs prior to this
message with the severity `INFO`. Although this log level may be incorrect, it
is expected, because the Flex template launcher has no way to extract severity
details from the log messages produced by the Apache Beam application.

If you want to see the correct severity for every message in the launcher log,
configure your template to generate logs in the JSON format instead of in plain
text. This configuration allows the template launcher to extract the correct log
message severity. Use the following message structure:

In Java, you can use
[Logback logger](https://logback.qos.ch/documentation.html)
with a custom JSON [appender](https://logback.qos.ch/manual/appenders.html)
implementation. For more information, see the
[Logback example configuration](https://github.com/GoogleCloudPlatform/DataflowTemplates/blob/f0029e203fbcfd3ea32b1632c70add1d6088ed38/structured-logging/src/main/resources/logback.xml)
and the
[JSON appender example code](https://github.com/GoogleCloudPlatform/DataflowTemplates/blob/ae826040fe19c3d1cb4c80763403dd4f257711db/structured-logging/src/main/java/com/google/cloud/teleport/v2/logging/JsonAppender.java#L28)
in GitHub.

This issue only impacts the logs generated by the Flex Template launcher
when the pipeline is launching. When the launch succeeds
and the pipeline is running, the logs produced by
Dataflow workers have the proper severity.

[Google-provided templates](/dataflow/docs/guides/templates/provided-templates)
show the correct severity during job launch, because the Google-provided
templates use this JSON logging approach.
