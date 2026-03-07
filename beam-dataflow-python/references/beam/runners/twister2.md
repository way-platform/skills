---
source_url: https://beam.apache.org/documentation/runners/twister2/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Twister2 Runner"
beam_last_updated: "Last updated on 2026/03/06"
---

## Overview

**Note** Twister2 runner is deprecated and the support is planned to be removed in Beam 3.0 ([Issue](https://github.com/apache/beam/issues/35905)).

Twister2 Runner can be used to execute Apache Beam pipelines on top of a Twister2
cluster. Twister2 Runner runs Beam pipelines as Twister2 jobs, which can be executed on
a Twister2 cluster either as a local deployment or distributed deployment using, Nomad,
Kubernetes, Slurm, etc.

The Twister2 runner is suitable for large scale batch jobs, specially jobs that
require high performance, and provide.

- Batch pipeline support.
- Support for HPC environments, supports propriety interconnects such as Infiniband.
- Distributed massively parallel data processing engine with high performance using
  Bulk Synchronous Parallel (BSP) style execution.
- Native support for Beam side-inputs.

The [Beam Capability Matrix](/documentation/runners/capability-matrix/) documents the
supported capabilities of the Twister2 Runner.

## Running WordCount with the Twister2 Runner

### Generating the Beam examples project

Just follow the instruction from the [Java Quickstart page](/get-started/quickstart-java/#get-the-wordcount-code)

### Running WordCount on a Twister2 Local Deployment

Issue following command in the Beam examples project to start new Twister2 Local cluster and run the WordCount example on it.

```
    $ mvn package exec:java \
        -DskipTests \
        -Dexec.mainClass=org.apache.beam.examples.WordCount \
        -Dexec.args="\
            --runner=Twister2Runner \
            --inputFile=pom.xml \
            --output=counts" \
        -Ptwister2-runner
```

### Running WordCount on a Twister2 Deployment

The Beam examples project, when generated from an archetype, comes from a particular released Beam version (that’s what
the `archetypeVersion` property is about). Each Beam version that contains the Twister2 Runner (i.e. from 2.23.0 onwards)
uses a certain version of Twister2. Because of this, when we start a stand-alone Twister2 cluster and try to run Beam examples on
it we need to make sure the two are compatible. See following table for which Twister2 version is recommended for various
Beam versions.

| Beam Version    | Compatible Twister2 Versions |
| --------------- | ---------------------------- |
| 2.23.0 or newer | 0.6.0                        |
| 2.22.0 or older | N/A                          |

Download latest Twister2 version compatible with the Beam you are using from
[Twister2 Website](https://twister2.org/docs/download). Twister2 currently supports
several deployment options, such as standalone, Slurm, Mesos, Nomad, etc. To learn more about the Twister2
deployments and how to get them setup visit [Twister2 Docs](https://twister2.org/docs/deployment/job-submit).

**Adapt for:**

- Twister2 0.6.0

Issue following command in the Beam examples project to start new Twister2 job,
The “twister2Home” should point to the home directory of the Twister2 standalone
deployment.

Note: Currently file paths need to be absolute paths.

```
    $ mvn package exec:java \
        -DskipTests \
        -Dexec.mainClass=org.apache.beam.examples.WordCount \
        -Dexec.args="\
            --runner=Twister2Runner \
            --twister2Home=<PATH_TO_TWISTER2_HOME>
            --parallelism=2
            --inputFile=<PATH_TO_FILE>/pom.xml \
            --output=<PATH_TO_FILE>/counts" \
        -Ptwister2-runner
```

## Pipeline Options for the Twister2 Runner

| Field          | Description                                                                                                        | Default Value                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| `runner`       | The pipeline runner to use. This option allows you to determine the pipeline runner at runtime.                    | Set to `Twister2Runner` to run using Twister2.                                                     |
| `twister2Home` | Location of the Twister2 home directory of the deployment being used.                                              | Has no default value. Twister2 Runner will use the Local Deployment mode for execution if not set. |
| `parallelism`  | Set the parallelism of the job                                                                                     | 1                                                                                                  |
| `clusterType`  | Set the type of Twister deployment being used. Valid values are `standalone, slurm, nomad, mesos`.                 | standalone                                                                                         |
| `workerCPUs`   | Number of CPU's assigned to a single worker. The total number of CPU's utilized would be `parallelism*workerCPUs`. | 2                                                                                                  |
| `ramMegaBytes` | Memory allocated to a single worker in MegaBytes. The total allocated memory would be `parallelism*ramMegaBytes`.  | 2048                                                                                               |
