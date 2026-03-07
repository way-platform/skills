---
source_url: https://beam.apache.org/documentation/transforms/python/aggregation/sample/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Sample"
beam_last_updated: "Last updated on 2026/03/06"
---

# Sample

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.combiners.html#apache_beam.transforms.combiners.Sample) |

Transforms for taking samples of the elements in a collection, or
samples of the values associated with each key in a collection of
key-value pairs.

## Examples

In the following example, we create a pipeline with a `PCollection`.
Then, we get a random sample of elements in different ways.

### Example 1: Sample elements from a PCollection

We use `Sample.FixedSizeGlobally()` to get a fixed-size random sample of elements from the _entire_ `PCollection`.

### Example 2: Sample elements for each key

We use `Sample.FixedSizePerKey()` to get fixed-size random samples for each unique key in a `PCollection` of key-values.

## Related transforms

- [Top](/documentation/transforms/python/aggregation/top) finds the largest or smallest element.

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.combiners.html#apache_beam.transforms.combiners.Sample) |
