---
source_url: https://beam.apache.org/documentation/patterns/custom-io/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Custom I/O patterns"
beam_last_updated: "Last updated on 2026/03/06"
---

# Custom I/O patterns

This page describes common patterns in pipelines with [custom I/O connectors](/documentation/io/developing-io-overview/). Custom I/O connectors connect pipelines to databases that aren’t supported by Beam’s [built-in I/O transforms](/documentation/io/connectors/).

## Choosing between built-in and custom connectors

[Built-in I/O connectors](/documentation/io/connectors/) are tested and hardened, so use them whenever possible. Only use custom I/O connectors when:

- No built-in options exist
- Your pipeline pulls in a small subset of source data

For instance, use a custom I/O connector to enrich pipeline elements with a small subset of source data. If youâre processing a sales order and adding information to each purchase, you can use a custom I/O connector to pull the small subset of data into your pipeline (instead of processing the entire source).

Beam distributes work across many threads, so custom I/O connectors can increase your data sourceâs load average. You can reduce the load with the [start](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html?highlight=bundle#apache_beam.transforms.core.DoFn.start_bundle) and [finish](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html?highlight=bundle#apache_beam.transforms.core.DoFn.finish_bundle) bundle annotations.
