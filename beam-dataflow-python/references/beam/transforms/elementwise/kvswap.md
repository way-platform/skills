---
source_url: https://beam.apache.org/documentation/transforms/python/elementwise/kvswap/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "KvSwap"
beam_last_updated: "Last updated on 2026/03/06"
---

# Kvswap

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html#apache_beam.transforms.util.KvSwap) |

Takes a collection of key-value pairs and returns a collection of key-value pairs
which has each key and value swapped.

## Examples

In the following example, we create a pipeline with a `PCollection` of key-value pairs.
Then, we apply `KvSwap` to swap the keys and values.

## Related transforms

- [Keys](/documentation/transforms/python/elementwise/keys) for extracting the key of each component.
- [Values](/documentation/transforms/python/elementwise/values) for extracting the value of each element.

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html#apache_beam.transforms.util.KvSwap) |
