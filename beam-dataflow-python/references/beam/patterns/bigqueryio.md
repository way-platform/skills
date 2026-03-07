---
source_url: https://beam.apache.org/documentation/patterns/bigqueryio/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "BigQuery patterns"
beam_last_updated: "Last updated on 2026/03/06"
---

# Google BigQuery patterns

The samples on this page show you common patterns for use with BigQueryIO.

## BigQueryIO deadletter pattern

In production systems, it is useful to implement the deadletter pattern with BigQueryIO outputting any elements which had errors during processing by BigQueryIO into another PCollection for further processing.
The samples below print the errors, but in a production system they can be sent to a deadletter table for later correction.

In the result tuple you can access `FailedRows` to access the failed inserts.

![](/images/copy-icon.svg)

```
  # Create pipeline.
  schema = ({'fields': [{'name': 'a', 'type': 'STRING', 'mode': 'REQUIRED'}]})

  pipeline = beam.Pipeline()

  errors = (
      pipeline | 'Data' >> beam.Create([1, 2])
      | 'CreateBrokenData' >>
      beam.Map(lambda src: {'a': src} if src == 2 else {'a': None})
      | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
          "<Your Project:Test.dummy_a_table",
          schema=schema,
          insert_retry_strategy='RETRY_ON_TRANSIENT_ERROR',
          create_disposition='CREATE_IF_NEEDED',
          write_disposition='WRITE_APPEND'))
  result = (
      errors['FailedRows']
      | 'PrintErrors' >>
      beam.FlatMap(lambda err: print("Error Found {}".format(err))))
```
