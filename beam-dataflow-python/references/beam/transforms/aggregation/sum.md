---
source_url: https://beam.apache.org/documentation/transforms/python/aggregation/sum/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Sum"
beam_last_updated: "Last updated on 2026/03/06"
---

# Sum

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.CombineGlobally) |

Sums all the elements within each aggregation.

## Examples

In the following example, we create a pipeline with a `PCollection`.
Then, we get the sum of all the element values in different ways.

### Example 1: Sum of the elements in a PCollection

We use `Combine.Globally()` to get sum of all the element values from the _entire_ `PCollection`.

### Example 2: Sum of the elements for each key

We use `Combine.PerKey()` to get the sum of all the element values for each unique key in a `PCollection` of key-values.

## Related transforms

- [CombineGlobally](/documentation/transforms/python/aggregation/combineglobally)
- [CombinePerKey](/documentation/transforms/python/aggregation/combineperkey)
- [Max](/documentation/transforms/python/aggregation/max)
- [Mean](/documentation/transforms/python/aggregation/mean)
- [Min](/documentation/transforms/python/aggregation/min)

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.CombineGlobally) |
