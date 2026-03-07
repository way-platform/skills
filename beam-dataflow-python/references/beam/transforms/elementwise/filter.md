---
source_url: https://beam.apache.org/documentation/transforms/python/elementwise/filter/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Filter"
beam_last_updated: "Last updated on 2026/03/06"
---

# Filter

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.Filter) |

Given a predicate, filter out all elements that don’t satisfy that predicate.
May also be used to filter based on an inequality with a given value based
on the comparison ordering of the element.

## Examples

In the following examples, we create a pipeline with a `PCollection` of produce with their icon, name, and duration.
Then, we apply `Filter` in multiple ways to filter out produce by their duration value.

`Filter` accepts a function that keeps elements that return `True`, and filters out the remaining elements.

### Example 1: Filtering with a function

We define a function `is_perennial` which returns `True` if the element’s duration equals `'perennial'`, and `False` otherwise.

### Example 2: Filtering with a lambda function

We can also use lambda functions to simplify **Example 1**.

### Example 3: Filtering with multiple arguments

You can pass functions with multiple arguments to `Filter`.
They are passed as additional positional arguments or keyword arguments to the function.

In this example, `has_duration` takes `plant` and `duration` as arguments.

### Example 4: Filtering with side inputs as singletons

If the `PCollection` has a single value, such as the average from another computation,
passing the `PCollection` as a _singleton_ accesses that value.

In this example, we pass a `PCollection` the value `'perennial'` as a singleton.
We then use that value to filter out perennials.

### Example 5: Filtering with side inputs as iterators

If the `PCollection` has multiple values, pass the `PCollection` as an _iterator_.
This accesses elements lazily as they are needed,
so it is possible to iterate over large `PCollection`s that won’t fit into memory.

> **Note**: You can pass the `PCollection` as a _list_ with `beam.pvalue.AsList(pcollection)`,
> but this requires that all the elements fit into memory.

### Example 6: Filtering with side inputs as dictionaries

If a `PCollection` is small enough to fit into memory, then that `PCollection` can be passed as a _dictionary_.
Each element must be a `(key, value)` pair.
Note that all the elements of the `PCollection` must fit into memory for this.
If the `PCollection` won’t fit into memory, use `beam.pvalue.AsIter(pcollection)` instead.

## Related transforms

- [FlatMap](/documentation/transforms/python/elementwise/flatmap) behaves the same as `Map`, but for
  each input it might produce zero or more outputs.
- [ParDo](/documentation/transforms/python/elementwise/pardo) is the most general elementwise mapping
  operation, and includes other abilities such as multiple output collections and side-inputs.

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.Filter) |
