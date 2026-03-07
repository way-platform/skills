---
source_url: https://beam.apache.org/documentation/transforms/python/elementwise/keys/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Keys"
beam_last_updated: "Last updated on 2026/03/06"
---

# Keys

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html#apache_beam.transforms.util.Keys) |

Takes a collection of key-value pairs and returns the key of each element.

## Example

In the following example, we create a pipeline with a `PCollection` of key-value pairs.
Then, we apply `Keys` to extract the keys and discard the values.

## Related transforms

- [KvSwap](/documentation/transforms/python/elementwise/kvswap) swaps the key and value of each element.
- [Values](/documentation/transforms/python/elementwise/values) for extracting the value of each element.

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html#apache_beam.transforms.util.Keys) |
