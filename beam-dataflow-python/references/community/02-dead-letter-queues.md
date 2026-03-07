# Dataflow Python: Error Handling & Dead Letter Queues (DLQ)

A resilient Dataflow pipeline must never drop data silently or crash entirely due to a single malformed record (a "poison pill"). In 2025, the standard pattern for this is the **Dead Letter Queue (DLQ)**.

## Two-Layered DLQ Architecture
1.  **Delivery Layer (Pub/Sub):** Catch persistent delivery failures at the Pub/Sub level before they reach the pipeline.
2.  **Application Layer (Beam):** Catch parsing, schema, and enrichment errors inside your Python code using side outputs.

## Implementing Side Outputs with `TupleTag`
Use `beam.pvalue.TaggedOutput` to route errors to a separate `PCollection`.

```python
import apache_beam as beam

class ParseEventFn(beam.DoFn):
    def process(self, element):
        try:
            # Attempt parsing
            parsed = json.loads(element)
            yield parsed
        except Exception as e:
            # Yield to the DLQ branch
            yield beam.pvalue.TaggedOutput('dlq', (element, str(e)))

# Pipeline construction
results = (p 
    | 'Read' >> beam.io.ReadFromPubSub(...)
    | 'Parse' >> beam.ParDo(ParseEventFn()).with_outputs('dlq', main='main')
)

main_output = results.main
dlq_output = results.dlq

# Write DLQ to BigQuery or GCS for debugging
dlq_output | 'Write DLQ' >> beam.io.WriteToBigQuery('project:dataset.dlq_table')
```

## DLQ Best Practices
*   **Preserve the Raw Payload:** Always store the original, unparsed message alongside the error so it can be replayed.
*   **Include Error Context:** Attach the timestamp, the transform name, and the stack trace.
*   **Alerting:** Set up Cloud Monitoring to trigger alerts if the DLQ volume spikes.

## References & Further Reading
*   [Google Cloud: Handling Invalid Inputs in Dataflow](https://cloud.google.com/dataflow/docs/guides/common-errors#handling-invalid-inputs)
*   [Apache Beam: Multiple Outputs](https://beam.apache.org/documentation/programming-guide/#multiple-outputs)
