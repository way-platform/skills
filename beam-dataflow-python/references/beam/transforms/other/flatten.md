---
source_url: https://beam.apache.org/documentation/transforms/python/other/flatten/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Flatten"
beam_last_updated: "Last updated on 2026/03/06"
---

# Flatten

[![Pydoc](/images/logos/sdks/python.png)
Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html?highlight=flatten#apache_beam.transforms.core.Flatten)

Merges multiple `PCollection` objects into a single logical
`PCollection`. A transform for `PCollection` objects
that store the same data type.

See more information in the [Beam Programming Guide](/documentation/programming-guide/#flatten).

## Examples

## Related transforms

- [FlatMap](/documentation/transforms/python/elementwise/flatmap) applies a simple 1-to-many mapping
  function over each element in the collection. This transform might produce zero
  or more outputs.
