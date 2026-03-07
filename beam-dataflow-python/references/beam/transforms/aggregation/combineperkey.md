---
source_url: https://beam.apache.org/documentation/transforms/python/aggregation/combineperkey/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "CombinePerKey"
beam_last_updated: "Last updated on 2026/03/06"
---

# CombinePerKey

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.CombinePerKey) |

Combines all elements for each key in a collection.

See more information in the [Beam Programming Guide](/documentation/programming-guide/#combine).

## Examples

In the following examples, we create a pipeline with a `PCollection` of produce.
Then, we apply `CombinePerKey` in multiple ways to combine all the elements in the `PCollection`.

`CombinePerKey` accepts a function that takes a list of values as an input, and combines them for each key.

### Example 1: Combining with a predefined function

We use the function
[`sum`](https://docs.python.org/3/library/functions.html#sum)
which takes an `iterable` of numbers and adds them together.

### Example 2: Combining with a function

We define a function `saturated_sum` which takes an `iterable` of numbers and adds them together, up to a predefined maximum number.

### Example 3: Combining with a lambda function

We can also use lambda functions to simplify **Example 2**.

### Example 4: Combining with multiple arguments

You can pass functions with multiple arguments to `CombinePerKey`.
They are passed as additional positional arguments or keyword arguments to the function.

In this example, the lambda function takes `values` and `max_value` as arguments.

### Example 5: Combining with a `CombineFn`

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

- [CombineGlobally](/documentation/transforms/python/aggregation/combineglobally)
- [CombineValues](/documentation/transforms/python/aggregation/combinevalues)
- [Mean](/documentation/transforms/python/aggregation/mean)
- [Count](/documentation/transforms/python/aggregation/count)
- [Top](/documentation/transforms/python/aggregation/top)
- [Sample](/documentation/transforms/python/aggregation/sample)

See also [GroupBy](/documentation/transforms/python/aggregation/groupby) which allows you to combine more than one field at once.

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.CombinePerKey) |
