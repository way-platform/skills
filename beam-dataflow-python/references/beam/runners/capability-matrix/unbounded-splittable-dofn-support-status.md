---
source_url: https://beam.apache.org/documentation/runners/capability-matrix/unbounded-splittable-dofn-support-status/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Unbounded Splittable DoFn Support Status"
beam_last_updated: "Last updated on 2026/03/06"
---

[back to collapsed details](/documentation/runners/capability-matrix)

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

|                                                    |                       |                                                                                      |     |     |     |     |     |     |       |       |
| -------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------ | --- | --- | --- | --- | --- | --- | ----- | ----- |
| Yes :                                              | Yes : fully supported | Partially : Support is either incomplete or broken on portable Flink Runner (#19637) | :   | :   | :   | :   | :   | :   | Yes : | No :  |
| Yes : fully supported                              | Yes : fully supported | No :                                                                                 | :   | :   | :   | :   | :   | :   | :     | Yes : |
| Yes :                                              | Yes : fully supported | Partially :                                                                          | :   | :   | :   | :   | :   | :   | Yes : | No :  |
| No :                                               | Yes : fully supported | No :                                                                                 | :   | :   | :   | :   | :   | :   | No :  | No :  |
| Partially : Only Dataflow Runner V2 supports this. | Yes : fully supported | No :                                                                                 | :   | :   | :   | :   | :   | :   | Yes : | No :  |
