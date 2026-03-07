---
source_url: https://beam.apache.org/documentation/runners/capability-matrix/where-in-event-time/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Where in event time?"
beam_last_updated: "Last updated on 2026/03/06"
---

[back to collapsed details](/documentation/runners/capability-matrix)

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

|                 |                       |                 |                 |                                           |                 |                 |                 |                 |
| --------------- | --------------------- | --------------- | --------------- | ----------------------------------------- | --------------- | --------------- | --------------- | --------------- |
| Yes : default   | Yes : default         | Yes : supported | Yes : supported | Partially : fully supported in batch mode | Yes : supported | Yes : supported | Yes : supported | Yes : supported |
| Yes : built-in  | Yes : fully supported | Yes : supported | Yes : supported | Partially : fully supported in batch mode | Yes : supported | Yes : supported | Yes : supported | Yes : supported |
| Yes : built-in  | Yes : fully supported | Yes : supported | Yes : supported | Partially : fully supported in batch mode | Yes : supported | Yes : supported | Yes : supported | Yes : supported |
| Yes : built-in  | No :                  | Yes : supported | Yes : supported | Partially : fully supported in batch mode | Yes : supported | Yes : supported | Yes : supported | Yes : supported |
| Yes : supported | No :                  | Yes : supported | Yes : supported | Partially : fully supported in batch mode | Yes : supported | Yes : supported | Yes : supported | Yes : supported |
| Yes : supported | No :                  | Yes : supported | Yes : supported | Partially : fully supported in batch mode | Yes : supported | Yes : supported | Yes : supported | Yes : supported |
| Yes : supported | No : Not supported    | Yes : supported | Yes : supported | Partially : fully supported in batch mode | Yes : supported | Yes : supported | Yes : supported | Yes : supported |
