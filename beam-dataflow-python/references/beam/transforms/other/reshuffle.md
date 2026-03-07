---
source_url: https://beam.apache.org/documentation/transforms/python/other/reshuffle/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Reshuffle"
beam_last_updated: "Last updated on 2026/03/06"
---

# Reshuffle

[![Pydoc](/images/logos/sdks/python.png)
Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html?highlight=reshuffle#apache_beam.transforms.util.Reshuffle)

Adds a temporary random key to each element in a collection, reshuffles
these keys, and removes the temporary key. This redistributes the
elements between workers and returns a collection equivalent to its
input collection. This is most useful for adjusting parallelism or
preventing coupled failures.

## Examples

See [Issue 19498](https://github.com/apache/beam/issues/19498) for updates.

## Related transforms

N/A
