---
source_url: https://beam.apache.org/documentation/runners/capability-matrix/bounded-splittable-dofn-support-status/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Bounded Splittable DoFn Support Status"
beam_last_updated: "Last updated on 2026/03/06"
---

[back to collapsed details](/documentation/runners/capability-matrix)

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

|                                                    |                       |                                                       |     |     |     |     |     |     |                            |       |
| -------------------------------------------------- | --------------------- | ----------------------------------------------------- | --- | --- | --- | --- | --- | --- | -------------------------- | ----- |
| Partially : Only Dataflow Runner V2 supports this. | Yes : fully supported | Partially : Only portable Flink Runner supports this. | :   | :   | :   | :   | :   | :   | Yes :                      | Yes : |
| Partially : Only Dataflow Runner V2 supports this. | Yes : fully supported | Partially : Only portable Flink Runner supports this. | :   | :   | :   | :   | :   | :   | :                          | Yes : |
| Partially : Only Dataflow Runner v2 supports this. | Yes : fully supported | Partially : Only portable Flink Runner supports this. | :   | :   | :   | :   | :   | :   | Yes :                      | No :  |
| Partially : Only Dataflow Runner V2 supports this. | Yes : fully supported | No :                                                  | :   | :   | :   | :   | :   | :   | Yes : Only with Python SDK | No :  |
| Partially : Only Dataflow Runner V2 supports this. | Yes : fully supported | No :                                                  | :   | :   | :   | :   | :   | :   | Yes :                      | No :  |
