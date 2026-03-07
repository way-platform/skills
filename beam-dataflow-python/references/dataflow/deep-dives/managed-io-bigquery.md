---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/managed-io-bigquery
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Dataflow managed I/O for BigQuery \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

Managed I/O supports the following capabilities for BigQuery:

- Dynamic table creation
- [Dynamic destinations](/dataflow/docs/guides/write-to-iceberg#dynamic-destinations%22)
- For reads, the connector uses the
  [BigQuery Storage Read API](/bigquery/docs/reference/storage).
- For writes, the connector uses the following BigQuery methods:
  - If the source is unbounded and Dataflow is using
    [streaming exactly-once processing](/dataflow/docs/guides/streaming-modes),
    the connector performs writes to BigQuery, by using the
    [BigQuery Storage Write API](/bigquery/docs/write-api) with exactly-once
    delivery semantics.
  - If the source is unbounded and Dataflow is using
    [streaming at-least-once processing](/dataflow/docs/guides/streaming-modes),
    the connector performs writes to BigQuery, by using the
    [BigQuery Storage Write API](/bigquery/docs/write-api) with at-least-once
    delivery semantics.
  - If the source is bounded, the connector uses
    [BigQuery file loads](/bigquery/docs/batch-loading-data).

## Requirements

The following SDKs support managed I/O for BigQuery:

- Apache Beam SDK for Java version 2.61.0 or later
- Apache Beam SDK for Python version 2.61.0 or later

## Configuration

Managed I/O for BigQuery supports the following configuration
parameters:

### `BIGQUERY` Read

| Configuration   | Type        | Description                                                                                                                                                                                            |
| --------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| kms_key         | `str`       | Use this Cloud KMS key to encrypt your data                                                                                                                                                            |
| query           | `str`       | The SQL query to be executed to read from the BigQuery table.                                                                                                                                          |
| row_restriction | `str`       | Read only rows that match this filter, which must be compatible with Google standard SQL. This is not supported when reading via query.                                                                |
| fields          | `list[str]` | Read only the specified fields (columns) from a BigQuery table. Fields may not be returned in the order specified. If no value is specified, then all fields are returned. Example: "col1, col2, col3" |
| table           | `str`       | The fully-qualified name of the BigQuery table to read from. Format: [${PROJECT}:]${DATASET}.${TABLE}                                                                                                  |

### `BIGQUERY` Write

| Configuration                | Type        | Description                                                                                                                                   |
| ---------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **table**                    | `str`       | The bigquery table to write to. Format: [${PROJECT}:]${DATASET}.${TABLE}                                                                      |
| drop                         | `list[str]` | A list of field names to drop from the input record before writing. Is mutually exclusive with 'keep' and 'only'.                             |
| keep                         | `list[str]` | A list of field names to keep in the input record. All other fields are dropped before writing. Is mutually exclusive with 'drop' and 'only'. |
| kms_key                      | `str`       | Use this Cloud KMS key to encrypt your data                                                                                                   |
| only                         | `str`       | The name of a single record field that should be written. Is mutually exclusive with 'keep' and 'drop'.                                       |
| triggering_frequency_seconds | `int64`     | Determines how often to 'commit' progress into BigQuery. Default is every 5 seconds.                                                          |

## What's next

For more information and code examples, see the following topics:

- [Read from BigQuery](/dataflow/docs/guides/read-from-bigquery)
- [Write to BigQuery](/dataflow/docs/guides/write-to-bigquery)
