---
source_url: https://beam.apache.org/documentation/transforms/python/other/flattenwith/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "FlattenWith"
beam_last_updated: "Last updated on 2026/03/06"
---

# FlattenWith

[![Pydoc](/images/logos/sdks/python.png)
Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html?highwebsite/www/site/content/en/documentation/transforms/python/otherlight=flattenwith#apache_beam.transforms.core.FlattenWith)

Merges multiple `PCollection` objects into a single logical
`PCollection`. It allows for the combination of both root
`PCollection`-producing transforms (like `Create` and `Read`) and existing
PCollections.

See more information in the [Beam Programming Guide](/documentation/programming-guide/#flattenwith).

## Examples

## Related transforms

- [Flatten](/documentation/transforms/python/other/flatten) merges multiple
  `PCollection` objects into a single logical `PCollection`. This is useful when
  dealing with multiple collections of the same data type.
- [FlatMap](/documentation/transforms/python/elementwise/flatmap) applies a
  simple 1-to-many mapping function over each element in the collection. This
  transform might produce zero or more outputs.
