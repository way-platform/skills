---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/troubleshoot-networking
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Troubleshoot Dataflow networking issues \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

This page shows you how to resolve issues with Dataflow networking.

For more information about configuring networking for your Dataflow
jobs, see [Configure internet access and firewall
rules](/dataflow/docs/guides/routes-firewall) and [Specify a network and
subnetwork](/dataflow/docs/guides/specifying-networks).

## Cannot create PoolableConnectionFactory

The following error occurs when your Dataflow job needs to connect
to an external database:

```
java.sql.SQLException: Cannot create PoolableConnectionFactory
(The connection attempt failed.)
```

This issue occurs when the Dataflow worker
can't establish a connection with the database server, often due to an
egress rule or a firewall.

To identify the root cause of this issue, [create and run
Connectivity Tests](/network-intelligence-center/docs/connectivity-tests/how-to/running-connectivity-tests).
The Connectivity Tests can help you identify where the traffic is
blocked.

To update your egress rules, see [Example firewall egress
rule](/dataflow/docs/guides/routes-firewall#example_firewall_egress_rule).

## Connection times out when using Cloud NAT

The following error can occur when your Dataflow job tries to
connect to an external service through a Cloud NAT gateway:

```
java.net.ConnectTimeoutException: Connection timed out
```

This issue can occur if your Dataflow job is configured to use external
IP addresses when your network is also set up to use Cloud NAT for egress
traffic. When Dataflow workers have external IP addresses, they
attempt to route traffic to the internet directly instead of through the
Cloud NAT gateway, which can lead to connection timeouts if firewall
rules prevent this direct access.

To resolve this issue, configure your Dataflow workers to not use
external IP addresses. This configuration helps to make sure that egress traffic
is routed through the configured Cloud NAT gateway. For more
information, see the [Cloud NAT documentation](/nat/docs/overview).

For information about how to disable external IP addresses, see [Configure
internet access and firewall
rules](/dataflow/docs/guides/routes-firewall#turn_off_external_ip_address).

## Cross-project references for this resource are not allowed

The following error occurs when you run a Dataflow job on a
Shared VPC network:

```
Invalid value for field 'resource.properties.networkInterfaces[0].subnetwork':
'https://www.googleapis.com/compute/v1/projects/PROJECT/regions/REGION/subnetworks/SUBNETWORK'.
Cross-project references for this resource are not allowed.
```

This issue occurs if you specify a subnetwork in a Shared VPC network,
but the service project isn't attached to the Shared VPC host project.

To resolve this issue, a Shared VPC Admin must [attach the service
project to the host project](/vpc/docs/provisioning-shared-vpc#create-shared).

## Instance must be in the same region as the subnetwork

The following error occurs when you run a Dataflow job with a
subnetwork specified:

```
Failed to start the VM, launcher-ID, used for launching because of status code: INVALID_ARGUMENT, reason: Invalid Error:
Message: Invalid value for field 'resource.networkInterfaces[0].subnetwork': 'https://www.googleapis.com/compute/v1/projects/PROJECT/regions/REGION/subnetworks/SUBNETWORK'. Instance must be in the same region as the subnetwork.
HTTP Code: 400.
```

This issue occurs when your job and the subnetwork specified in your job are
in different regions.

To resolve this issue, run your job in the region that your subnetwork is in.
For example, if your subnetwork is in `us-central1`, run your job in the region
`us-central1`.

## IP space is exhausted

When you create a Dataflow job or trigger an autoscaling
operation, these operations might fail with the following message:

```
IP_SPACE_EXHAUSTED: Instance 'INSTANCE_NAME' creation failed: IP space of 'projects/PROJECT/regions/REGION/subnetworks/SUBNETWORK' is exhausted.
```

You can try any of the following strategies to resolve this error:

1. Reduce the number of worker requests for the Dataflow job.
   You provide a specific number of workers by setting the `num_workers`
   pipeline option, or you can set an upper bound on the number of workers
   using the `max_num_workers` pipeline option. For more information, see
   [Pipeline
   options](/dataflow/docs/reference/pipeline-options#resource_utilization).
2. If possible, increase the size of the Dataflow job's subnet.
   For information on expanding an existing subnet, see the [Virtual Private
   Cloud](/vpc/docs/create-modify-vpc-networks#expand-subnet) documentation.
3. Use a different subnet with enough available IP addresses for the
   Dataflow job.
4. If feasible, create a dedicated subnet with a sufficient number of IP
   addresses for Dataflow jobs.

## Network interface must specify a subnet if the network resource is in custom subnet mode

The following error occurs when you run a Dataflow job:

```
Workflow failed. Causes: Invalid Error: Message: Invalid value for field
'resource.properties.networkInterfaces[0].subnetwork': ''. Network interface
must specify a subnet if the network resource is in custom subnet mode. HTTP
Code: 400
```

This issue occurs if the VPC network named `default` was
converted from an auto mode VPC network to a custom mode
VPC network.

To resolve this issue, specify the subnetwork parameter when using a custom
mode VPC network. For more information, see
[Specify a network and subnetwork](/dataflow/docs/guides/specifying-networks).

## Network is unreachable

The following error occurs when you have external IP addresses disabled and try
to run a Dataflow job:

```
NewConnectionError(''<pip._vendor.urllib3.connection.HTTPSConnection  object at ID>:
Failed to establish a new connection: [Errno 101] Network is unreachable
```

This issue occurs because your pipeline configuration doesn't allow connections
to external IP addresses, but your pipeline needs to connect to an external IP
to run. The following pipeline options disable external IP connections:

### Java

`--usePublicIps=false`

### Python

`--no_use_public_ips=true`

### Go

`--no_use_public_ips=true`

### API

`options = PipelineOptions(use_public_ips=False)`

To identify where traffic is blocked, [create and run
Connectivity Tests](/network-intelligence-center/docs/connectivity-tests/how-to/running-connectivity-tests).

To resolve this issue without allowing connections to external IP addresses,
make one or more of the following changes.

- Configure a NAT solution, such as [Cloud NAT](/nat/docs/overview).
- [Configure Private Google Access](/vpc/docs/configure-private-google-access).
- If you can't configure a NAT solution, you can
  [use custom containers](/dataflow/docs/guides/using-custom-containers)
  to supply Python pipeline dependencies.

For more information about configuring internet access for
Dataflow, see [Internet access for
Dataflow](/dataflow/docs/guides/routes-firewall#internet_access_for).

## Network or subnetwork is not accessible to Dataflow service account or does not exist

One of the following errors occurs when you try to run a Dataflow
job. The job fails.

```
Workflow failed. Causes: Network default is not accessible to Dataflow Service
account or does not exist
```

```
Workflow failed. Causes: Subnetwork SUBNETWORK is not
accessible to Dataflow Service account or does not exist
```

This issue can occur for the following reasons:

- You omit both the subnetwork and network parameters when you create the
  Dataflow job, but an auto mode VPC network
  named `default` doesn't exist in your project. You might not have a
  default network if the default network was deleted or if an organization
  policy constraint prevents you from creating a default network.
- The subnetwork is missing.
- The subnetwork parameter is specified incorrectly.
- The required permissions for the Dataflow service account are
  missing.
- If you're using a Shared VPC, the value for the host
  project must be the project that the VPC is hosted in.
  To learn more about Shared VPC, see
  [Shared VPC overview](/vpc/docs/shared-vpc).

To resolve this issue, follow the [guidelines for specifying a network and
subnetwork](/dataflow/docs/guides/specifying-networks#specifying_a_network_and_a_subnetwork).

## RPC timed out or failed to connect on ports 12345 or 12346

One of the following errors occurs when you run a Dataflow job
that doesn't use Streaming Engine or Dataflow Shuffle. The job
gets stuck or fails.

For streaming jobs:

```
Rpc to WORKER_HARNESS:12345 completed with error
UNAVAILABLE: failed to connect to all addresses; last error : UNKNOWN:
ipv4:WORKER_IP_ADDRESS:12345: Failed to connect to remote
host: FD Shutdown
```

For batch jobs:

```
(g)RPC timed out when SOURCE_WORKER_HARNESS talking to
DESTINATION_WORKER_HARNESS:12346.
```

This issue occurs if a firewall rule that allows network traffic on TCP ports
`12345` and `12346` is missing. When the job uses multiple workers, the workers
aren't able to communicate with each other.

To resolve this issue, see the troubleshooting steps in [DEADLINE_EXCEEDED or
Server Unresponsive](/dataflow/docs/guides/common-errors#tsg-rpc-timeout).

## Single worker is repeatedly started and stopped

The following issue occurs when you launch a Dataflow job. On
the Dataflow job's **Job metrics** page, the
**CPU utilization (All Workers)** chart shows that a worker is repeatedly
started and then stopped after a few minutes. Only one worker is available at a
given time.

![CPU utilization chart showing that one worker at a time is repeatedly created and then stopped.](/static/dataflow/images/cpu-utilization-one-worker.png)

The following error occurs:

```
The Dataflow job appears to be stuck because no worker activity has been seen
in the last 1h. Please check the worker logs in Stackdriver Logging.
```

**Note:** If you see a `Dataflow job appears to be stuck` error and you also see an
`Error syncing pod` error, the issue is likely a container failure. For more
information, see [Error syncing pod ... failed to
"StartContainer"](/dataflow/docs/guides/common-errors#error-syncing-pod).

No worker logs are created.

In the job logs, multiple messages similar to the following might appear:

```
Autoscaling: Raised the number of workers to 1 based on the rate of progress in
the currently running stage(s).
```

This issue occurs if the VPC network doesn't have a default
route to the internet and a default route to the subnetwork.

To resolve this issue,
[add default routes](/vpc/docs/using-routes#adding_and_removing_routes)
to your VPC network. For more information, see
[Internet access for Dataflow](/dataflow/docs/guides/routes-firewall#internet_access_for).

This issue can also occur if the user-managed worker service account and the
Dataflow job are in different projects. For more information about
avoiding this issue when using cross-project service accounts, see the guidance
offered in step 3 and step 4 of [Specify a user-managed worker service
account](/dataflow/docs/concepts/security-and-permissions#user-managed).

If your VPC network has default routes, and the user-managed
worker service account and the Dataflow job are in the same
project, sign in to the Dataflow job's worker VM and check the
logs in the `/var/log/dataflow` directory to identify the issue.

## Subnetwork does not have Private Google Access

The following error occurs when you launch a Dataflow job in which
external IP addresses are disabled:

```
Workflow failed. Causes: Subnetwork SUBNETWORK on project
PROJECT_ID network NETWORK in
region REGION does not have Private Google Access, which
is required for usage of private IP addresses by the Dataflow workers.
```

This issue occurs if you [turn off external IP
addresses](/dataflow/docs/guides/routes-firewall#turn_off_external_ip_address)
without enabling Private Google Access.

To resolve this issue,
[enable Private Google Access](/vpc/docs/configure-private-google-access) for
the subnetwork that the Dataflow job uses.

## Unable to create Dataflow with a specified IP range

Dataflow doesn't support assigning a static IP range to the
worker VMs. As a workaround, you can create a subnetwork with a specific
IP address range and deploy the Dataflow job in that
subnetwork.

For more information about using subnetworks with Dataflow, see
[Specify a network and subnetwork](/dataflow/docs/guides/specifying-networks).

For information about configuring IP ranges in subnetworks, see
[Configure alias IP ranges](/vpc/docs/configure-alias-ip-ranges).

To run your pipeline in the subnetwork, see [Run your pipeline with the
subnetwork specified](/dataflow/docs/guides/specifying-networks#specify-subnet).

You might also need to create a NAT rule and a router. For more information,
see [Cloud NAT](/nat/docs/overview).

## What's next

For additional networking troubleshooting steps, see
[Troubleshoot internal connectivity between VMs](/vpc/docs/ts-vm-vm-internal).
