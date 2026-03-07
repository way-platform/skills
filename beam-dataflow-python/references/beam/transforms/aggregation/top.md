---
source_url: https://beam.apache.org/documentation/transforms/python/aggregation/top/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Top"
beam_last_updated: "Last updated on 2026/03/06"
---

# Top

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.combiners.html#apache_beam.transforms.combiners.Top) |

Transforms for finding the largest (or smallest) set of elements in
a collection, or the largest (or smallest) set of values associated
with each key in a collection of key-value pairs.

## Examples

In the following example, we create a pipeline with a `PCollection`.
Then, we get the largest or smallest elements in different ways.

### Example 1: Largest elements from a PCollection

We use `Top.Largest()` to get the largest elements from the _entire_ `PCollection`.

### Example 2: Largest elements for each key

We use `Top.LargestPerKey()` to get the largest elements for each unique key in a `PCollection` of key-values.

### Example 3: Smallest elements from a PCollection

We use `Top.Smallest()` to get the smallest elements from the _entire_ `PCollection`.

### Example 4: Smallest elements for each key

We use `Top.SmallestPerKey()` to get the smallest elements for each unique key in a `PCollection` of key-values.

### Example 5: Custom elements from a PCollection

We use `Top.Of()` to get elements with customized rules from the _entire_ `PCollection`.

You can change how the elements are compared with `key`.
By default you get the largest elements, but you can get the smallest by setting `reverse=True`.

### Example 6: Custom elements for each key

We use `Top.PerKey()` to get elements with customized rules for each unique key in a `PCollection` of key-values.

You can change how the elements are compared with `key`.
By default you get the largest elements, but you can get the smallest by setting `reverse=True`.

## Related transforms

- [Sample](/documentation/transforms/python/aggregation/sample) to combine elements. Takes samples of the elements in a collection.

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.combiners.html#apache_beam.transforms.combiners.Top) |
