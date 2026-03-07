# Dataflow Python: BigQuery I/O Optimization

Writing high volumes of data to BigQuery from Dataflow requires modern APIs to ensure high throughput and low costs.

## Use the Storage Write API
The legacy `streaming_inserts` method is outdated and expensive. The modern standard (2025+) is the **BigQuery Storage Write API**. It offers exact-once semantics, higher throughput, and significantly lower costs.

```python
# Modern BigQuery Write Example
(p | beam.io.WriteToBigQuery(
    table='my_project:my_dataset.my_table',
    method=beam.io.WriteToBigQuery.Method.STORAGE_WRITE_API,
    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
))
```

## Optimizing Writes
1.  **Enable Autosharding:** For streaming pipelines, Dataflow can automatically adjust the number of shards writing to BigQuery based on throughput. Ensure `with_auto_sharding=True` is set (or let it default to True for the Storage API).
2.  **Use Avro Format:** If loading batch data, use `temp_file_format='AVRO'`. It is faster and handles nested schemas better than JSON.
3.  **Schema Enforcement:** Validate data against your BigQuery schema *before* the write step to prevent expensive partial failures. Use `beam.Row` for strict typing in Python.

## References & Further Reading
*   [Apache Beam: BigQuery I/O (Python)](https://beam.apache.org/documentation/io/built-in/google-bigquery/)
*   [Google Cloud: BigQuery Storage Write API](https://cloud.google.com/bigquery/docs/write-api)
