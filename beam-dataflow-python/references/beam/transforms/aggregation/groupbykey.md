---
source_url: https://beam.apache.org/documentation/transforms/python/aggregation/groupbykey/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "GroupByKey"
beam_last_updated: "Last updated on 2026/03/06"
---

# GroupByKey

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.GroupByKey) |

Takes a keyed collection of elements and produces a collection
where each element consists of a key and all values associated with that key.

See more information in the [Beam Programming Guide](/documentation/programming-guide/#groupbykey).

## Examples

**Example 1**: In the following example, we create a pipeline with a `PCollection` of produce keyed by season.

We use `GroupByKey` to group all the produce for each season.

**Example 2**:

## Related transforms

- [GroupBy](/documentation/transforms/python/aggregation/groupby) for grouping by arbitrary properties of the elements.
- [CombinePerKey](/documentation/transforms/python/aggregation/combineperkey) for combining all values associated with a key to a single result.
- [CoGroupByKey](/documentation/transforms/python/aggregation/cogroupbykey) for multiple input collections.

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.GroupByKey) |
