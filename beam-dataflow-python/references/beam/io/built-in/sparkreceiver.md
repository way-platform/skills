---
source_url: https://beam.apache.org/documentation/io/built-in/sparkreceiver/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "SparkReceiver IO"
beam_last_updated: "Last updated on 2026/03/06"
---

# SparkReceiver IO

SparkReceiverIO is a transform for reading data from an Apache Spark Receiver as an unbounded source.

## Spark Receivers support

`SparkReceiverIO` currently supports [Apache Spark Receiver](https://spark.apache.org/docs/2.4.0/streaming-custom-receivers.html).

Requirements for `Spark Receiver`:

- Version of Spark should be 2.4.\*.
- `Spark Receiver` should support work with offsets.
- `Spark Receiver` should implement [HasOffset](https://github.com/apache/beam/blob/master/sdks/java/io/sparkreceiver/2/src/main/java/org/apache/beam/sdk/io/sparkreceiver/HasOffset.java) interface.
- Records should have the numeric field that represents record offset.

For more details please see [SparkReceiverIO readme](https://github.com/apache/beam/blob/master/sdks/java/io/sparkreceiver/2/README.md).

## Streaming reading using SparkReceiverIO

In order to read from `Spark Receiver` you will need to pass:

- `getOffsetFn`, which is `SerializableFunction` that defines how to get `Long` record offset from a record.
- `receiverBuilder`, which is needed for building instances of `Spark Receiver` that use Apache Beam mechanisms instead of Spark environment.

You can easily create `receiverBuilder` object by passing the following parameters:

- Class of your `Spark Receiver`.
- Constructor arguments needed to create an instance of your `Spark Receiver`.

For example:

Then you will be able to pass this `receiverBuilder` object to `SparkReceiverIO`.

For example:

### Read data with optional parameters

Optionally you can pass the following optional parameters:

- `pullFrequencySec`, which is delay in seconds between polling for new records updates.
- `startOffset`, which is inclusive start offset from which the reading should be started.
- `timestampFn`, which is a `SerializableFunction` that defines how to get an `Instant timestamp` from a record.

For example:

### Examples for specific Spark Receiver

#### CDAP Hubspot Receiver
