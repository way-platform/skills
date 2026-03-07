---
source_url: https://beam.apache.org/documentation/transforms/python/aggregation/combineglobally/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "CombineGlobally"
beam_last_updated: "Last updated on 2026/03/06"
---

# CombineGlobally

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.CombineGlobally) |

Combines all elements in a collection.

See more information in the [Beam Programming Guide](/documentation/programming-guide/#combine).

## Examples

In the following examples, we create a pipeline with a `PCollection` of produce.
Then, we apply `CombineGlobally` in multiple ways to combine all the elements in the `PCollection`.

`CombineGlobally` accepts a function that takes an `iterable` of elements as an input, and combines them to return a single element.

### Example 1: Combining with a function

We define a function `get_common_items` which takes an `iterable` of sets as an input, and calculates the intersection (common items) of those sets.

### Example 2: Combining with a lambda function

We can also use lambda functions to simplify **Example 1**.

### Example 3: Combining with multiple arguments

You can pass functions with multiple arguments to `CombineGlobally`.
They are passed as additional positional arguments or keyword arguments to the function.

In this example, the lambda function takes `sets` and `exclude` as arguments.

### Example 4: Combining with a `CombineFn`

The more general way to combine elements, and the most flexible, is with a class that inherits from `CombineFn`.

- [`CombineFn.create_accumulator()`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.CombineFn.create_accumulator):
  This creates an empty accumulator.
  For example, an empty accumulator for a sum would be `0`, while an empty accumulator for a product (multiplication) would be `1`.
- [`CombineFn.add_input()`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.CombineFn.add_input):
  Called _once per element_.
  Takes an accumulator and an input element, combines them and returns the updated accumulator.
- [`CombineFn.merge_accumulators()`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.CombineFn.merge_accumulators):
  Multiple accumulators could be processed in parallel, so this function helps merging them into a single accumulator.
- [`CombineFn.extract_output()`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.CombineFn.extract_output):
  It allows to do additional calculations before extracting a result.

## Related transforms

You can use the following combiner transforms:

- [CombinePerKey](/documentation/transforms/python/aggregation/combineperkey)
- [CombineValues](/documentation/transforms/python/aggregation/combinevalues)
- [Mean](/documentation/transforms/python/aggregation/mean)
- [Count](/documentation/transforms/python/aggregation/count)
- [Top](/documentation/transforms/python/aggregation/top)
- [Sample](/documentation/transforms/python/aggregation/sample)

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.CombineGlobally) |
