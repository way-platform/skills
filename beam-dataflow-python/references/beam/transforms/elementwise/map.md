---
source_url: https://beam.apache.org/documentation/transforms/python/elementwise/map/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Map"
beam_last_updated: "Last updated on 2026/03/06"
---

# Map

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.Map) |

Applies a simple 1-to-1 mapping function over each element in the collection.

## Examples

In the following examples, we create a pipeline with a `PCollection` of produce with their icon, name, and duration.
Then, we apply `Map` in multiple ways to transform every element in the `PCollection`.

`Map` accepts a function that returns a single element for every input element in the `PCollection`.

### Example 1: Map with a predefined function

We use the function `str.strip` which takes a single `str` element and outputs a `str`.
It strips the input element’s whitespaces, including newlines and tabs.

### Example 2: Map with a function

We define a function `strip_header_and_newline` which strips any `'#'`, `' '`, and `'\n'` characters from each element.

### Example 3: Map with a lambda function

We can also use lambda functions to simplify **Example 2**.

### Example 4: Map with multiple arguments

You can pass functions with multiple arguments to `Map`.
They are passed as additional positional arguments or keyword arguments to the function.

In this example, `strip` takes `text` and `chars` as arguments.

### Example 5: MapTuple for key-value pairs

If your `PCollection` consists of `(key, value)` pairs,
you can use `MapTuple` to unpack them into different function arguments.

### Example 6: Map with side inputs as singletons

If the `PCollection` has a single value, such as the average from another computation,
passing the `PCollection` as a _singleton_ accesses that value.

In this example, we pass a `PCollection` the value `'# \n'` as a singleton.
We then use that value as the characters for the `str.strip` method.

### Example 7: Map with side inputs as iterators

If the `PCollection` has multiple values, pass the `PCollection` as an _iterator_.
This accesses elements lazily as they are needed,
so it is possible to iterate over large `PCollection`s that won’t fit into memory.

> **Note**: You can pass the `PCollection` as a _list_ with `beam.pvalue.AsList(pcollection)`,
> but this requires that all the elements fit into memory.

### Example 8: Map with side inputs as dictionaries

If a `PCollection` is small enough to fit into memory, then that `PCollection` can be passed as a _dictionary_.
Each element must be a `(key, value)` pair.
Note that all the elements of the `PCollection` must fit into memory for this.
If the `PCollection` won’t fit into memory, use `beam.pvalue.AsIter(pcollection)` instead.

### Example 9: Map with setup and bundle contexts.

If an expensive shared object, such as a database connection, is required, this can be passed
as a bundle or setup context which is invoked like a Python context manager.
For example

## Related transforms

- [FlatMap](/documentation/transforms/python/elementwise/flatmap) behaves the same as `Map`, but for
  each input it may produce zero or more outputs.
- [Filter](/documentation/transforms/python/elementwise/filter) is useful if the function is just
  deciding whether to output an element or not.
- [ParDo](/documentation/transforms/python/elementwise/pardo) is the most general elementwise mapping
  operation, and includes other abilities such as multiple output collections and side-inputs.

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.Map) |
