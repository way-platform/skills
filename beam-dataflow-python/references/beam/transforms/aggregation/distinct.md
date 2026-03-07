---
source_url: https://beam.apache.org/documentation/transforms/python/aggregation/distinct/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Distinct"
beam_last_updated: "Last updated on 2026/03/06"
---

# Distinct

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html#apache_beam.transforms.util.Distinct) |

Produces a collection containing distinct elements of the input collection.

## Examples

In the following example, we create a pipeline with two `PCollection`s of produce.

We use `Distinct` to get rid of duplicate elements, which outputs a `PCollection` of all the unique elements.

## Related transforms

- [Count](/documentation/transforms/python/aggregation/count) counts the number of elements within each aggregation.

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html#apache_beam.transforms.util.Distinct) |
