---
source_url: https://beam.apache.org/documentation/transforms/python/other/tee/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Tee"
beam_last_updated: "Last updated on 2026/03/06"
---

# Tee

[![Pydoc](/images/logos/sdks/python.png)
Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html?highwebsite/www/site/content/en/documentation/transforms/python/otherlight=flattenwith#apache_beam.transforms.util.Tee)

The `Tee` transform allows for splitting the pipeline flow into multiple branches,
enabling the application of side transformations while preserving the main pipeline.
This is similar to the Unix `tee` command, which duplicates input and sends it to
multiple outputs without interrupting the main flow.

See more information in the [Beam Programming Guide](/documentation/programming-guide/#tee).

## Examples
