---
source_url: https://beam.apache.org/documentation/transforms/python/aggregation/latest/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Latest"
beam_last_updated: "Last updated on 2026/03/06"
---

# Latest

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.combiners.html#apache_beam.transforms.combiners.Latest) |

Gets the element with the latest timestamp.

## Examples

In the following examples, we create a pipeline with a `PCollection` of produce with a timestamp for their harvest date.

We use `Latest` to get the element with the latest timestamp from the `PCollection`.

### Example 1: Latest element globally

We use `Latest.Globally()` to get the element with the latest timestamp in the entire `PCollection`.

### Example 2: Latest elements for each key

We use `Latest.PerKey()` to get the elements with the latest timestamp for each key in a `PCollection` of key-values.

## Related transforms

- [Sample](/documentation/transforms/python/aggregation/sample) randomly takes some number of elements in a collection.

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.combiners.html#apache_beam.transforms.combiners.Latest) |
