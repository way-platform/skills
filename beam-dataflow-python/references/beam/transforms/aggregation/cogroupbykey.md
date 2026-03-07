---
source_url: https://beam.apache.org/documentation/transforms/python/aggregation/cogroupbykey/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "CoGroupByKey"
beam_last_updated: "Last updated on 2026/03/06"
---

# CoGroupByKey

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html#apache_beam.transforms.util.CoGroupByKey) |

Aggregates all input elements by their key and allows downstream processing
to consume all values associated with the key. While `GroupByKey` performs
this operation over a single input collection and thus a single type of input
values, `CoGroupByKey` operates over multiple input collections. As a result,
the result for each key is a tuple of the values associated with that key in
each input collection.

See more information in the [Beam Programming Guide](/documentation/programming-guide/#cogroupbykey).

## Examples

In the following example, we create a pipeline with two `PCollection`s of produce, one with icons and one with durations, both with a common key of the produce name.
Then, we apply `CoGroupByKey` to join both `PCollection`s using their keys.

`CoGroupByKey` expects a dictionary of named keyed `PCollection`s, and produces elements joined by their keys.
The values of each output element are dictionaries where the names correspond to the input dictionary, with lists of all the values found for that key.

## Related transforms

- [CombineGlobally](/documentation/transforms/python/aggregation/combineglobally) to combine elements.
- [GroupByKey](/documentation/transforms/python/aggregation/groupbykey) takes one input collection.

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html#apache_beam.transforms.util.CoGroupByKey) |
