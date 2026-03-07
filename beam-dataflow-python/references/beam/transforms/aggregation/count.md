---
source_url: https://beam.apache.org/documentation/transforms/python/aggregation/count/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Count"
beam_last_updated: "Last updated on 2026/03/06"
---

# Count

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.combiners.html#apache_beam.transforms.combiners.Count) |

Counts the number of elements within each aggregation.

## Examples

In the following example, we create a pipeline with two `PCollection`s of produce.
Then, we apply `Count` to get the total number of elements in different ways.

### Example 1: Counting all elements in a PCollection

We use `Count.Globally()` to count _all_ elements in a `PCollection`, even if there are duplicate elements.

### Example 2: Counting elements for each key

We use `Count.PerKey()` to count the elements for each unique key in a `PCollection` of key-values.

### Example 3: Counting all unique elements

We use `Count.PerElement()` to count only the unique elements in a `PCollection`.

## Related transforms

N/A

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.combiners.html#apache_beam.transforms.combiners.Count) |
