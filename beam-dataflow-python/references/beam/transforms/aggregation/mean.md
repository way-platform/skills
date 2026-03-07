---
source_url: https://beam.apache.org/documentation/transforms/python/aggregation/mean/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Mean"
beam_last_updated: "Last updated on 2026/03/06"
---

# Mean

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.combiners.html#apache_beam.transforms.combiners.Mean) |

Transforms for computing the arithmetic mean of the elements in a collection,
or the mean of the values associated with each key in a collection of
key-value pairs.

## Examples

In the following example, we create a pipeline with a `PCollection`.
Then, we get the element with the average value in different ways.

### Example 1: Mean of element in a PCollection

We use `Mean.Globally()` to get the average of the elements from the _entire_ `PCollection`.

### Example 2: Mean of elements for each key

We use `Mean.PerKey()` to get the average of the elements for each unique key in a `PCollection` of key-values.

## Related transforms

- [CombineGlobally](/documentation/transforms/python/aggregation/combineglobally)
- [CombinePerKey](/documentation/transforms/python/aggregation/combineperkey)
- [Max](/documentation/transforms/python/aggregation/max)
- [Min](/documentation/transforms/python/aggregation/min)
- [Sum](/documentation/transforms/python/aggregation/sum)

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.combiners.html#apache_beam.transforms.combiners.Mean) |
