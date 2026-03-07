---
source_url: https://beam.apache.org/documentation/transforms/python/aggregation/groupby/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "GroupBy"
beam_last_updated: "Last updated on 2026/03/06"
---

# GroupBy

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.GroupBy) |

Takes a collection of elements and produces a collection grouped,
by properties of those elements.

Unlike `GroupByKey`, the key is dynamically created from the elements themselves.

## Grouping Examples

In the following example, we create a pipeline with a `PCollection` of fruits.

We use `GroupBy` to group all fruits by the first letter of their name.

We can group by a composite key consisting of multiple properties if desired.

The resulting key is a named tuple with the two requested attributes, and the
values are grouped accordingly.

In the case that the property one wishes to group by is an attribute, a string
may be passed to `GroupBy` in the place of a callable expression.

It is possible to mix and match attributes and expressions, for example

## Aggregation

Grouping is often used in conjunction with aggregation, and the
`aggregate_field` method of the `GroupBy` transform can be used to accomplish
this easily.
This method takes three parameters: the field (or expression) which to
aggregate, the `CombineFn` (or associative `callable`) with which to aggregate
by, and finally a field name in which to store the result.
For example, suppose one wanted to compute the amount of each fruit to buy.
One could write

Similar to the parameters in `GroupBy`, one can also aggregate multiple fields
and by expressions.

One can, of course, aggregate the same field multiple times as well.
This example also illustrates a global grouping, as the grouping key is empty.

## Related transforms

- [CombinePerKey](/documentation/transforms/python/aggregation/combineperkey) for combining with a single CombineFn.
- [GroupByKey](/documentation/transforms/python/aggregation/groupbykey) for grouping with a known key.
- [CoGroupByKey](/documentation/transforms/python/aggregation/cogroupbykey) for multiple input collections.

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.GroupByKey) |
