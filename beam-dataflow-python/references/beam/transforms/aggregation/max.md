---
source_url: https://beam.apache.org/documentation/transforms/python/aggregation/max/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Max"
beam_last_updated: "Last updated on 2026/03/06"
---

# Max

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.CombineGlobally) |

Gets the element with the maximum value within each aggregation.

## Examples

In the following example, we create a pipeline with a `PCollection`.
Then, we get the element with the maximum value in different ways.

### Example 1: Maximum element in a PCollection

We use `Combine.Globally()` to get the maximum element from the _entire_ `PCollection`.

### Example 2: Maximum elements for each key

We use `Combine.PerKey()` to get the maximum element for each unique key in a `PCollection` of key-values.

## Related transforms

- [CombineGlobally](/documentation/transforms/python/aggregation/combineglobally)
- [CombinePerKey](/documentation/transforms/python/aggregation/combineperkey)
- [Mean](/documentation/transforms/python/aggregation/mean)
- [Min](/documentation/transforms/python/aggregation/min)
- [Sum](/documentation/transforms/python/aggregation/sum)

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.CombineGlobally) |
