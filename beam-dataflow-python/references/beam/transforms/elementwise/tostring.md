---
source_url: https://beam.apache.org/documentation/transforms/python/elementwise/tostring/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "ToString"
beam_last_updated: "Last updated on 2026/03/06"
---

# ToString

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html#apache_beam.transforms.util.ToString) |

Transforms every element in an input collection to a string.

## Examples

Any non-string element can be converted to a string using standard Python functions and methods.
Many I/O transforms, such as
[`textio.WriteToText`](https://beam.apache.org/releases/pydoc/current/apache_beam.io.textio.html#apache_beam.io.textio.WriteToText),
expect their input elements to be strings.

### Example 1: Key-value pairs to string

The following example converts a `(key, value)` pair into a string delimited by `','`.
You can specify a different delimiter using the `delimiter` argument.

### Example 2: Elements to string

The following example converts a dictionary into a string.
The string output will be equivalent to `str(element)`.

### Example 3: Iterables to string

The following example converts an iterable, in this case a list of strings,
into a string delimited by `','`.
You can specify a different delimiter using the `delimiter` argument.
The string output will be equivalent to `iterable.join(delimiter)`.

## Related transforms

- [Map](/documentation/transforms/python/elementwise/map) applies a simple 1-to-1 mapping function over each element in the collection

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html#apache_beam.transforms.util.ToString) |
