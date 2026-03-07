---
source_url: https://beam.apache.org/documentation/patterns/grouping-elements-for-efficient-external-service-calls/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Pattern for grouping elements for efficient external service calls"
beam_last_updated: "Last updated on 2026/03/06"
---

# Grouping elements for efficient external service calls using the `GroupIntoBatches`-transform

Usually, authoring an Apache Beam pipeline can be done with out-of-the-box tools and transforms like _ParDo_’s, _Window_’s and _GroupByKey_’s. However, when you want more tight control, you can keep state in an otherwise stateless _DoFn_.

State is kept on a per-key and per-windows basis, and as such, the input to your stateful DoFn needs to be keyed (e.g. by the customer identifier if you’re tracking clicks from an e-commerce website).

Examples of use cases are: assigning a unique ID to each element, joining streams of data in ‘more exotic’ ways, or batching up API calls to external services. In this section we’ll go over the last one in particular.

Make sure to check the [docs](/documentation/programming-guide/#state-and-timers) for deeper understanding on state and timers.

The `GroupIntoBatches`-transform uses state and timers under the hood to allow the user to exercise tight control over the following parameters:

- `maxBufferDuration`: limits the amount of waitingtime for a batch to be emitted.
- `batchSize`: limits the number of elements in one batch.
- `batchSizeBytes`: (in Java only) limits the bytesize of one batch (using input coder to determine elementsize).
- `elementByteSize`: (in Java only) limits the bytesize of one batch (using a user defined function to determine elementsize).

while abstracting away the implementation details from users.

The `withShardedKey()` functionality increases parallelism by spreading one key over multiple threads.

The transforms are used in the following way in Java & Python:

![](/images/copy-icon.svg)

```
input | GroupIntoBatches.WithShardedKey(batchSize, maxBufferingDuration)
```

Applying these transforms will output groups of elements in a batch on a per-key basis, which you can then use to call an external API in bulk rather than on a per-element basis, resulting in a lower overhead in your pipeline.
