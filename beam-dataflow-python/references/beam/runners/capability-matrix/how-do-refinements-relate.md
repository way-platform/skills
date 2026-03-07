---
source_url: https://beam.apache.org/documentation/runners/capability-matrix/how-do-refinements-relate/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "How do refinements relate?"
beam_last_updated: "Last updated on 2026/03/06"
---

[back to collapsed details](/documentation/runners/capability-matrix)

#### How do refinements relate?

|              |
| ------------ |
| Discarding   |
| Accumulating |

| Google Cloud Dataflow | Prism Local Runner | Apache Flink | Apache Spark (RDD/DStream based) | Apache Spark Structured Streaming (Dataset based) | Apache Samza | Apache Nemo | Hazelcast Jet | Twister2 | Python Direct FnRunner | Go Direct Runner |
| --------------------- | ------------------ | ------------ | -------------------------------- | ------------------------------------------------- | ------------ | ----------- | ------------- | -------- | ---------------------- | ---------------- |

|                                                                                                                                |                       |                       |                                                                                |                                           |                       |                       |                       |                       |
| ------------------------------------------------------------------------------------------------------------------------------ | --------------------- | --------------------- | ------------------------------------------------------------------------------ | ----------------------------------------- | --------------------- | --------------------- | --------------------- | --------------------- |
| Yes : fully supported                                                                                                          | Yes : fully supported | Yes : fully supported | Yes : fully supported Spark streaming natively discards elements after firing. | Partially : fully supported in batch mode | Yes : fully supported | Yes : fully supported | Yes : fully supported | Yes : fully supported |
| Yes : fully supported Requires that the accumulated pane fits in memory, after being passed through the combiner (if relevant) | Yes : fully supported | Yes : fully supported | No                                                                             | No                                        | Yes : fully supported | Yes : fully supported | Yes : fully supported | Yes : fully supported |
