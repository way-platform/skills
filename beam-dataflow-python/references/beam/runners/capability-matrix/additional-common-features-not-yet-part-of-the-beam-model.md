---
source_url: https://beam.apache.org/documentation/runners/capability-matrix/additional-common-features-not-yet-part-of-the-beam-model/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Additional common features not yet part of the Beam model"
beam_last_updated: "Last updated on 2026/03/06"
---

[back to collapsed details](/documentation/runners/capability-matrix)

#### Additional common features not yet part of the Beam model

|                      |
| -------------------- |
| Drain                |
| Checkpoint           |
| Key-ordered delivery |

| Google Cloud Dataflow | Prism Local Runner | Apache Flink | Apache Spark (RDD/DStream based) | Apache Spark Structured Streaming (Dataset based) | Apache Samza | Apache Nemo | Hazelcast Jet | Twister2 | Python Direct FnRunner | Go Direct Runner |
| --------------------- | ------------------ | ------------ | -------------------------------- | ------------------------------------------------- | ------------ | ----------- | ------------- | -------- | ---------------------- | ---------------- |

|                                                                                                                                                                   |                       |                                                                                                                      |                                                                                                                                                                |                      |                                                       |              |                                                                                                                                                                |              |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- | ----------------------------------------------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ | ------------ | ------------ |
| Partially : Dataflow has a native drain operation, but it does not work in the presence of event time timer loops. Final implemention pending model support.      | No :                  | Partially : Flink supports taking a "savepoint" of the pipeline and shutting the pipeline down after its completion. | :                                                                                                                                                              | :                    | :                                                     | :            | :                                                                                                                                                              | :            |
| No :                                                                                                                                                              | No :                  | Partially : Flink has a native savepoint capability.                                                                 | Partially : Spark has a native savepoint capability.                                                                                                           | No : not implemented | Partially : Samza has a native checkpoint capability. | :            | :                                                                                                                                                              | :            |
| Partially : Dataflow performs different shuffling algorithms for batch and streaming. Dataflow guarantees key-ordered delivery in streaming, though not in batch. | Yes : fully supported | Unverified :                                                                                                         | Partially : Flink may perform different shuffling algorithms for batch and streaming. Flink guarantees key-ordered delivery in streaming, though not in batch. | Unverified :         | Unverified :                                          | Unverified : | Partially : Samza may perform different shuffling algorithms for batch and streaming. Samza guarantees key-ordered delivery in streaming, though not in batch. | Unverified : | Unverified : | Unverified : |
