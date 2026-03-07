---
source_url: https://beam.apache.org/documentation/runners/capability-matrix/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Apache Beam Capability Matrix"
beam_last_updated: "Last updated on 2026/03/06"
---

# Beam Capability Matrix

Apache Beam provides a portable API layer for building sophisticated data-parallel processing pipelines that may be executed across a diversity of execution engines, or _runners_. The core concepts of this layer are based upon the Beam Model (formerly referred to as the [Dataflow Model](https://www.vldb.org/pvldb/vol8/p1792-Akidau.pdf)), and implemented to varying degrees in each Beam runner. To help clarify the capabilities of individual runners, we’ve created the capability matrix below.

Individual capabilities have been grouped by their corresponding What / Where / When / How question:

- What results are being calculated?
- Where in event time?
- When in processing time?
- How do refinements of results relate?

For more details on the What / Where / When / How breakdown of concepts, we recommend reading through the [Streaming 102](https://oreilly.com/ideas/the-world-beyond-batch-streaming-102) post on O’Reilly Radar.

Note that in the future, we intend to add additional tables beyond the current set, for things like runtime characteristics (e.g. at-least-once vs exactly-once), performance, etc.

##### How to read the tables

|            | Tools we are comparing                                        |
| ---------- | ------------------------------------------------------------- |
| Properties | Does this tool have this property?Yes/Partially/No/Unverified |

##### What do those signs mean?

✓

Yes

~

Partially

?

Unverified

✕

No

#### What is being computed?

|                      |
| -------------------- |
| ParDo                |
| GroupByKey           |
| Flatten              |
| Combine              |
| Composite Transforms |
| Side Inputs          |
| Source API           |
| Metrics              |
| Stateful Processing  |

| Google Cloud Dataflow | Prism Local Runner | Apache Flink | Apache Spark (RDD/DStream based) | Apache Spark Structured Streaming (Dataset based) | Apache Samza | Apache Nemo | Hazelcast Jet | Twister2 | Python Direct FnRunner | Go Direct Runner |
| --------------------- | ------------------ | ------------ | -------------------------------- | ------------------------------------------------- | ------------ | ----------- | ------------- | -------- | ---------------------- | ---------------- |

|       |       |       |       |       |       |       |       |       |       |       |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **✓** | **✓** | **✓** | **✓** | **~** | **✓** | **✓** | **✓** | **✓** | **✕** | **✕** |
| **✓** | **✓** | **✓** | **~** | **~** | **✓** | **✓** | **✓** | **✓** | **✕** | **✕** |
| **✓** | **✓** | **✓** | **✓** | **~** | **✓** | **✓** | **✓** | **✓** | **✕** | **✕** |
| **✓** | **✓** | **✓** | **✓** | **~** | **✓** | **✓** | **✓** | **✓** | **✕** | **✕** |
| **~** | **✓** | **~** | **~** | **~** | **~** | **✓** | **~** | **~** | **✕** | **✕** |
| **✓** | **✓** | **✓** | **✓** | **~** | **✓** | **✓** | **~** | **✓** | **✕** | **✕** |
| **✓** | **✓** | **✓** | **✓** | **~** | **✓** | **✓** | **✓** | **✓** | **✕** | **✕** |
| **~** | **~** | **~** | **~** | **~** | **~** | **✕** | **~** | **✕** | **✕** | **✕** |
| **~** | **✓** | **~** | **~** | **✕** | **~** | **✕** | **~** | **✕** | **✕** | **✕** |

[SEE DETAILS AND FULL VERSION HERE.](/documentation/runners/capability-matrix/what-is-being-computed/)

#### Bounded Splittable DoFn Support Status

|                                         |
| --------------------------------------- |
| Base                                    |
| Side Inputs                             |
| Splittable DoFn Initiated Checkpointing |
| Dynamic Splitting                       |
| Bundle Finalization                     |

| Google Cloud Dataflow | Prism Local Runner | Apache Flink | Apache Spark (RDD/DStream based) | Apache Spark Structured Streaming (Dataset based) | Apache Samza | Apache Nemo | Hazelcast Jet | Twister2 | Python Direct FnRunner | Go Direct Runner |
| --------------------- | ------------------ | ------------ | -------------------------------- | ------------------------------------------------- | ------------ | ----------- | ------------- | -------- | ---------------------- | ---------------- |

|       |       |       |       |       |       |       |       |       |       |       |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **~** | **✓** | **~** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✓** | **✓** |
| **~** | **✓** | **~** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✓** |
| **~** | **✓** | **~** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✓** | **✕** |
| **~** | **✓** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✓** | **✕** |
| **~** | **✓** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✓** | **✕** |

[SEE DETAILS AND FULL VERSION HERE.](/documentation/runners/capability-matrix/bounded-splittable-dofn-support-status/)

#### Unbounded Splittable DoFn Support Status

|                                         |
| --------------------------------------- |
| Base                                    |
| Side Inputs                             |
| Splittable DoFn Initiated Checkpointing |
| Dynamic Splitting                       |
| Bundle Finalization                     |

| Google Cloud Dataflow | Prism Local Runner | Apache Flink | Apache Spark (RDD/DStream based) | Apache Spark Structured Streaming (Dataset based) | Apache Samza | Apache Nemo | Hazelcast Jet | Twister2 | Python Direct FnRunner | Go Direct Runner |
| --------------------- | ------------------ | ------------ | -------------------------------- | ------------------------------------------------- | ------------ | ----------- | ------------- | -------- | ---------------------- | ---------------- |

|       |       |       |       |       |       |       |       |       |       |       |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **✓** | **✓** | **~** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✓** | **✕** |
| **✓** | **✓** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✓** |
| **✓** | **✓** | **~** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✓** | **✕** |
| **✕** | **✓** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** |
| **~** | **✓** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** | **✓** | **✕** |

[SEE DETAILS AND FULL VERSION HERE.](/documentation/runners/capability-matrix/unbounded-splittable-dofn-support-status/)

#### Where in event time?

|                        |
| ---------------------- |
| Global windows         |
| Fixed windows          |
| Sliding windows        |
| Session windows        |
| Custom windows         |
| Custom merging windows |
| Timestamp control      |

| Google Cloud Dataflow | Prism Local Runner | Apache Flink | Apache Spark (RDD/DStream based) | Apache Spark Structured Streaming (Dataset based) | Apache Samza | Apache Nemo | Hazelcast Jet | Twister2 | Python Direct FnRunner | Go Direct Runner |
| --------------------- | ------------------ | ------------ | -------------------------------- | ------------------------------------------------- | ------------ | ----------- | ------------- | -------- | ---------------------- | ---------------- |

|       |       |       |       |       |       |       |       |       |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **✓** | **✓** | **✓** | **✓** | **~** | **✓** | **✓** | **✓** | **✓** |
| **✓** | **✓** | **✓** | **✓** | **~** | **✓** | **✓** | **✓** | **✓** |
| **✓** | **✓** | **✓** | **✓** | **~** | **✓** | **✓** | **✓** | **✓** |
| **✓** | **✕** | **✓** | **✓** | **~** | **✓** | **✓** | **✓** | **✓** |
| **✓** | **✕** | **✓** | **✓** | **~** | **✓** | **✓** | **✓** | **✓** |
| **✓** | **✕** | **✓** | **✓** | **~** | **✓** | **✓** | **✓** | **✓** |
| **✓** | **✕** | **✓** | **✓** | **~** | **✓** | **✓** | **✓** | **✓** |

[SEE DETAILS AND FULL VERSION HERE.](/documentation/runners/capability-matrix/where-in-event-time/)

#### When in processing time?

|                          |
| ------------------------ |
| Configurable triggering  |
| Event-time triggers      |
| Processing-time triggers |
| Count triggers           |
| Composite triggers       |
| Allowed lateness         |
| Timers                   |

| Google Cloud Dataflow | Prism Local Runner | Apache Flink | Apache Spark (RDD/DStream based) | Apache Spark Structured Streaming (Dataset based) | Apache Samza | Apache Nemo | Hazelcast Jet | Twister2 | Python Direct FnRunner | Go Direct Runner |
| --------------------- | ------------------ | ------------ | -------------------------------- | ------------------------------------------------- | ------------ | ----------- | ------------- | -------- | ---------------------- | ---------------- |

|       |       |       |       |       |       |       |       |       |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **✓** | **✓** | **✓** | **✓** | **~** | **✓** | **✓** | **✓** | **✓** |
| **✓** | **✓** | **✓** | **✓** | **~** | **✓** | **✓** | **✓** | **✓** |
| **✓** | **✓** | **✓** | **✓** | **~** | **✓** | **✓** | **✓** | **✓** |
| **✓** | **✕** | **✓** | **✓** | **~** | **✓** | **✓** | **✓** | **✓** |
| **✓** | **✓** | **✓** | **✓** | **~** | **✓** | **✓** | **✓** | **~** |
| **✓** | **✓** | **✓** | **✕** | **✕** | **✓** | **✓** | **✓** | **~** |
| **~** | **✓** | **~** | **~** | **✕** | **~** | **✕** | **~** | **~** |

[SEE DETAILS AND FULL VERSION HERE.](/documentation/runners/capability-matrix/when-in-processing-time/)

#### How do refinements relate?

|              |
| ------------ |
| Discarding   |
| Accumulating |

| Google Cloud Dataflow | Prism Local Runner | Apache Flink | Apache Spark (RDD/DStream based) | Apache Spark Structured Streaming (Dataset based) | Apache Samza | Apache Nemo | Hazelcast Jet | Twister2 | Python Direct FnRunner | Go Direct Runner |
| --------------------- | ------------------ | ------------ | -------------------------------- | ------------------------------------------------- | ------------ | ----------- | ------------- | -------- | ---------------------- | ---------------- |

|       |       |       |       |       |       |       |       |       |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **✓** | **✓** | **✓** | **✓** | **~** | **✓** | **✓** | **✓** | **✓** |
| **✓** | **✓** | **✓** | **✕** | **✕** | **✓** | **✓** | **✓** | **✓** |

[SEE DETAILS AND FULL VERSION HERE.](/documentation/runners/capability-matrix/how-do-refinements-relate/)

#### Additional common features not yet part of the Beam model

|                      |
| -------------------- |
| Drain                |
| Checkpoint           |
| Key-ordered delivery |

| Google Cloud Dataflow | Prism Local Runner | Apache Flink | Apache Spark (RDD/DStream based) | Apache Spark Structured Streaming (Dataset based) | Apache Samza | Apache Nemo | Hazelcast Jet | Twister2 | Python Direct FnRunner | Go Direct Runner |
| --------------------- | ------------------ | ------------ | -------------------------------- | ------------------------------------------------- | ------------ | ----------- | ------------- | -------- | ---------------------- | ---------------- |

|       |       |       |       |       |       |       |       |       |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **~** | **✕** | **~** | **✕** | **✕** | **✕** | **✕** | **✕** | **✕** |
| **✕** | **✕** | **~** | **~** | **✕** | **~** | **✕** | **✕** | **✕** |
| **~** | **✓** | **?** | **~** | **?** | **?** | **?** | **~** | **?** | **?** | **?** |

[SEE DETAILS AND FULL VERSION HERE.](/documentation/runners/capability-matrix/additional-common-features-not-yet-part-of-the-beam-model/)
