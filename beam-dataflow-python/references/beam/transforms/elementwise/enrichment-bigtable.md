---
source_url: https://beam.apache.org/documentation/transforms/python/elementwise/enrichment-bigtable/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Enrichment with Bigtable"
beam_last_updated: "Last updated on 2026/03/06"
---

# Use Bigtable to enrich data

|                                                                                                                                                                                                      |     |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| [Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.enrichment_handlers.bigtable.html#apache_beam.transforms.enrichment_handlers.bigtable.BigTableEnrichmentHandler) |     |

In Apache Beam 2.54.0 and later versions, the enrichment transform includes a built-in enrichment handler for [Bigtable](https://cloud.google.com/bigtable/docs/overview).
The following example demonstrates how to create a pipeline that use the enrichment transform with the [`BigTableEnrichmentHandler`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.enrichment_handlers.bigtable.html#apache_beam.transforms.enrichment_handlers.bigtable.BigTableEnrichmentHandler) handler.

The data stored in the Bigtable cluster uses the following format:

| Row key | product:product_id | product:product_name | product:product_stock |
| ------- | ------------------ | -------------------- | --------------------- |
| 1       | 1                  | pixel 5              | 2                     |
| 2       | 2                  | pixel 6              | 4                     |
| 3       | 3                  | pixel 7              | 20                    |
| 4       | 4                  | pixel 8              | 10                    |

![](/images/copy-icon.svg)

```
import apache_beam as beam
from apache_beam.transforms.enrichment import Enrichment
from apache_beam.transforms.enrichment_handlers.bigtable import BigTableEnrichmentHandler

project_id = 'apache-beam-testing'
instance_id = 'beam-test'
table_id = 'bigtable-enrichment-test'
row_key = 'product_id'

data = [
    beam.Row(sale_id=1, customer_id=1, product_id=1, quantity=1),
    beam.Row(sale_id=3, customer_id=3, product_id=2, quantity=3),
    beam.Row(sale_id=5, customer_id=5, product_id=4, quantity=2)
]

bigtable_handler = BigTableEnrichmentHandler(
    project_id=project_id,
    instance_id=instance_id,
    table_id=table_id,
    row_key=row_key)
with beam.Pipeline() as p:
  _ = (
      p
      | "Create" >> beam.Create(data)
      | "Enrich W/ BigTable" >> Enrichment(bigtable_handler)
      | "Print" >> beam.Map(print))
```

Output:

![](/images/copy-icon.svg)

```
Row(sale_id=1, customer_id=1, product_id=1, quantity=1, product={'product_id': '1', 'product_name': 'pixel 5', 'product_stock': '2'})
Row(sale_id=3, customer_id=3, product_id=2, quantity=3, product={'product_id': '2', 'product_name': 'pixel 6', 'product_stock': '4'})
Row(sale_id=5, customer_id=5, product_id=4, quantity=2, product={'product_id': '4', 'product_name': 'pixel 8', 'product_stock': '10'})
```

## Related transforms

Not applicable.

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.enrichment_handlers.bigtable.html#apache_beam.transforms.enrichment_handlers.bigtable.BigTableEnrichmentHandler) |
