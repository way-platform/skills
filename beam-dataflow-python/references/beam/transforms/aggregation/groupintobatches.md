---
source_url: https://beam.apache.org/documentation/transforms/python/aggregation/groupintobatches/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "GroupIntoBatches"
beam_last_updated: "Last updated on 2026/03/06"
---

# GroupIntoBatches

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html#apache_beam.transforms.util.GroupIntoBatches) |

Batches the input into desired batch size.

## Examples

In the following example, we create a pipeline with a `PCollection` of produce by season.

We use `GroupIntoBatches` to get fixed-sized batches for every key, which outputs a list of elements for every key.

## Related transforms

For unkeyed data and dynamic batch sizes, one may want to use
[BatchElements](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html#apache_beam.transforms.util.BatchElements).

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html#apache_beam.transforms.util.GroupIntoBatches) |
