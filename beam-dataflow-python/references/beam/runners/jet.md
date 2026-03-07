---
source_url: https://beam.apache.org/documentation/runners/jet/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Hazelcast Jet Runner"
beam_last_updated: "Last updated on 2026/03/06"
---

## Overview

The Hazelcast Jet Runner can be used to execute Beam pipelines using [Hazelcast
Jet](https://jet-start.sh/).

The Jet Runner and Jet are suitable for large scale continuous jobs and provide:

- Support for both batch (bounded) and streaming (unbounded) data sets
- A runtime that supports very high throughput and low event latency at the same time
- Natural back-pressure in streaming programs
- Distributed massively parallel data processing engine with in memory storage

It’s important to note that the Jet Runner is currently in an _EXPERIMENTAL_ state and can not make use of many of
the capabilities present in Jet:

- Jet has full Fault Tolerance support, the Jet Runner does not; if a job fails it must be restarted
- Internal performance of Jet is extremely high.
  The Runner can’t match it as of now because Beam pipeline optimization/surgery has not been fully implemented.

The [Beam Capability Matrix](/documentation/runners/capability-matrix/) documents the
supported capabilities of the Jet Runner.

## Running WordCount with the Hazelcast Jet Runner

### Generating the Beam examples project

Just follow the instruction from the [Java Quickstart page](/get-started/quickstart-java/#get-the-wordcount-code)

### Running WordCount on a Local Jet Cluster

Issue following command in the Beam examples project to start new Jet cluster and run the WordCount example on it.

```
    $ mvn package exec:java \
        -DskipTests \
        -Dexec.mainClass=org.apache.beam.examples.WordCount \
        -Dexec.args="\
            --runner=JetRunner \
            --jetLocalMode=3 \
            --inputFile=pom.xml \
            --output=counts" \
        -Pjet-runner
```

### Running WordCount on a Remote Jet Cluster

The Beam examples project, when generated from an archetype, comes from a particular released Beam version (that’s what
the `archetypeVersion` property is about). Each Beam version that contains the Jet Runner (ie. from 2.14.0 onwards)
uses a certain version of Jet. Because of this, when we start a stand-alone Jet cluster and try to run Beam examples on
it we need to make sure the two are compatible. See following table for which Jet version is recommended for various
Beam versions.

| Beam Version    | Compatible Jet Versions |
| --------------- | ----------------------- |
| 2.20.0 or newer | 4.x                     |
| 2.14.0 - 2.19.0 | 3.x                     |
| 2.13.0 or older | N/A                     |

Download latest Hazelcast Jet version compatible with the Beam you are using from
[Hazelcast Jet Website](https://jet-start.sh/download).

**Adapt for:**

- Hazelcast Jet 3.x
- Hazelcast Jet 4.x

Once the download has finished you need to start a Jet cluster. The simplest way to do so is to start Jet cluster
members using the `jet-start` script that comes with the downloaded Jet distribution. The members use the
[auto discovery feature](https://docs.hazelcast.org/docs/3.12/manual/html-single/index.html#setting-up-clusters)
[auto discovery feature](https://docs.hazelcast.org/docs/4.0/manual/html-single/#setting-up-clusters)
to form a cluster. Let’s start up a cluster formed by two members:

![](/images/copy-icon.svg)

![](/images/copy-icon.svg)

Check the cluster is up and running:

![](/images/copy-icon.svg)

![](/images/copy-icon.svg)

You should see something like:

![](/images/copy-icon.svg)

![](/images/copy-icon.svg)

Change directory to the Beam Examples project and issue following command to submit and execute your
Pipeline on the remote Jet cluster.
Make sure to distribute the input file (file with the words to be counted) to all machines where the
cluster runs. The word count job won’t be able to read the data otherwise.

```
    $ mvn package exec:java \
        -DskipTests \
        -Dexec.mainClass=org.apache.beam.examples.WordCount \
        -Dexec.args="\
            --runner=JetRunner \
            --jetServers=192.168.0.117:5701,192.168.0.117:5702 \
            --codeJarPathname=target/word-count-beam-bundled-0.1.jar \
            --inputFile=<INPUT_FILE_AVAILABLE_ON_ALL_CLUSTER_MEMBERS> \
            --output=/tmp/counts" \
        -Pjet-runner
```

## Pipeline Options for the Jet Runner

| Field                        | Description                                                                                                                                                                                                                                                                                                             | Default Value                        |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `runner`                     | The pipeline runner to use. This option allows you to determine the pipeline runner at runtime.                                                                                                                                                                                                                         | Set to `JetRunner` to run using Jet. |
| `jetGroupNamejetClusterName` | The name of the Hazelcast Group to join, in essence an ID of the Jet Cluster that will be used by the Runner. With groups it is possible to create multiple clusters where each cluster has its own group and doesn't interfere with other clusters. The name of the Hazelcast Cluster that will be used by the Runner. | `jet`                                |
| `jetServers`                 | List of the addresses of Jet Cluster members, needed when the Runner doesn't start its own Jet Cluster, but makes use of an external, independently started one. Takes the form of a comma separated list of ip/hostname-port pairs, like this: `192.168.0.117:5701,192.168.0.117:5702`                                 | `127.0.0.1:5701`                     |
| `codeJarPathname`            | Also a property needed only when using external Jet Clusters, specifies the location of a fat jar containing all the code that needs to run on the cluster (so at least the pipeline and the runner code). The value is any string that is accepted by `new java.io.File()` as a parameter.                             | Has no default value.                |
| `jetLocalMode`               | The number of Jet Cluster members that should be started locally by the Runner. If it's `0` then the Runner will be using an external cluster. If greater, then the Runner will be using a cluster started by itself.                                                                                                   | `0`                                  |
| `jetDefaultParallelism`      | Local parallelism of Jet members, the number of processors of each vertex of the DAG that will be created on each Jet Cluster member.                                                                                                                                                                                   | `2`                                  |
| `jetProcessorsCooperative`   | Boolean flag specifying if Jet Processors for DoFns are allowed to be cooperative (ie. use green threads instead of dedicated OS ones). If set to true than all such Processors will be cooperative, except when they have no outputs (so they are assumed to be syncs).                                                | `false`                              |
