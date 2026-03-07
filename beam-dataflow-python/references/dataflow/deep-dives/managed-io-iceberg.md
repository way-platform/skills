---
source_url: https://docs.cloud.google.com/dataflow/docs/guides/managed-io-iceberg
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Dataflow managed I/O for Apache Iceberg \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

[Managed I/O](/dataflow/docs/guides/managed-io) supports the following
capabilities for Apache Iceberg:

|                    |                                                                                                                                                           |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Catalogs           | - Hadoop - Hive - REST-based catalogs - [BigQuery metastore](/bigquery/docs/about-bqms) (requires Apache Beam SDK 2.62.0 or later if not using Runner v2) |
| Read capabilities  | Batch read                                                                                                                                                |
| Write capabilities | - Batch write - Streaming write - [Dynamic destinations](/dataflow/docs/guides/write-to-iceberg#dynamic-destinations) - Dynamic table creation            |

For [BigQuery tables for Apache Iceberg](/bigquery/docs/iceberg-tables),
use the
[`BigQueryIO` connector](https://beam.apache.org/documentation/io/built-in/google-bigquery/)
with BigQuery Storage API. The table must already exist; dynamic table creation is
not supported.

## Requirements

The following SDKs support managed I/O for Apache Iceberg:

- Apache Beam SDK for Java version 2.58.0 or later
- Apache Beam SDK for Python version 2.61.0 or later

## Configuration

Managed I/O for Apache Iceberg supports the following configuration
parameters:

### `ICEBERG` Read

| Configuration      | Type            | Description                                                                                                                                                         |
| ------------------ | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **table**          | `str`           | Identifier of the Iceberg table.                                                                                                                                    |
| catalog_name       | `str`           | Name of the catalog containing the table.                                                                                                                           |
| catalog_properties | `map[str, str]` | Properties used to set up the Iceberg catalog.                                                                                                                      |
| config_properties  | `map[str, str]` | Properties passed to the Hadoop Configuration.                                                                                                                      |
| drop               | `list[str]`     | A subset of column names to exclude from reading. If null or empty, all columns will be read.                                                                       |
| filter             | `str`           | SQL-like predicate to filter data at scan time. Example: "id > 5 AND status = 'ACTIVE'". Uses Apache Calcite syntax: https://calcite.apache.org/docs/reference.html |
| keep               | `list[str]`     | A subset of column names to read exclusively. If null or empty, all columns will be read.                                                                           |

### `ICEBERG` Write

| Configuration                | Type            | Description                                                                                                                                                                                                                                                                                                                                                                          |
| ---------------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **table**                    | `str`           | A fully-qualified table identifier. You may also provide a template to write to multiple dynamic destinations, for example: `dataset.my\_{col1}\_{col2.nested}\_table`.                                                                                                                                                                                                              |
| catalog_name                 | `str`           | Name of the catalog containing the table.                                                                                                                                                                                                                                                                                                                                            |
| catalog_properties           | `map[str, str]` | Properties used to set up the Iceberg catalog.                                                                                                                                                                                                                                                                                                                                       |
| config_properties            | `map[str, str]` | Properties passed to the Hadoop Configuration.                                                                                                                                                                                                                                                                                                                                       |
| direct_write_byte_limit      | `int32`         | For a streaming pipeline, sets the limit for lifting bundles into the direct write path.                                                                                                                                                                                                                                                                                             |
| drop                         | `list[str]`     | A list of field names to drop from the input record before writing. Is mutually exclusive with 'keep' and 'only'.                                                                                                                                                                                                                                                                    |
| keep                         | `list[str]`     | A list of field names to keep in the input record. All other fields are dropped before writing. Is mutually exclusive with 'drop' and 'only'.                                                                                                                                                                                                                                        |
| only                         | `str`           | The name of a single record field that should be written. Is mutually exclusive with 'keep' and 'drop'.                                                                                                                                                                                                                                                                              |
| partition_fields             | `list[str]`     | Fields used to create a partition spec that is applied when tables are created. For a field 'foo', the available partition transforms are: - `foo` - `truncate(foo, N)` - `bucket(foo, N)` - `hour(foo)` - `day(foo)` - `month(foo)` - `year(foo)` - `void(foo)` For more information on partition transforms, please visit <https://iceberg.apache.org/spec/#partition-transforms>. |
| table_properties             | `map[str, str]` | Iceberg table properties to be set on the table when it is created. For more information on table properties, please visit <https://iceberg.apache.org/docs/latest/configuration/#table-properties>.                                                                                                                                                                                 |
| triggering_frequency_seconds | `int32`         | For a streaming pipeline, sets the frequency at which snapshots are produced.                                                                                                                                                                                                                                                                                                        |

## What's next

For more information and code examples, see the following topics:

- [Read from Apache Iceberg](/dataflow/docs/guides/read-from-iceberg)
- [Write to Apache Iceberg](/dataflow/docs/guides/write-to-iceberg)
