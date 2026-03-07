---
source_url: https://beam.apache.org/documentation/transforms/python/elementwise/values/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Values"
beam_last_updated: "Last updated on 2026/03/06"
---

# Values

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html#apache_beam.transforms.util.Values) |

Takes a collection of key-value pairs, and returns the value of each element.

## Example

In the following example, we create a pipeline with a `PCollection` of key-value pairs.
Then, we apply `Values` to extract the values and discard the keys.

## Related transforms

- [Keys](/documentation/transforms/python/elementwise/keys) for extracting the key of each component.
- [KvSwap](/documentation/transforms/python/elementwise/kvswap) swaps the key and value of each element.

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html#apache_beam.transforms.util.Values) |
