---
source_url: https://docs.cloud.google.com/dataflow/docs/concepts/beam-programming-model
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Programming model for Apache Beam \u00a0|\u00a0 Cloud Dataflow \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

Dataflow is based on the open-source Apache Beam project. This
document describes the Apache Beam programming model, providing an overview
of its architecture and serving as a guide to its core concepts.

## Apache Beam data processing overview

This section provides an overview of the Apache Beam architecture, detailing
how its components work together for efficient data processing. Apache Beam
is an open-source, unified model for defining both batch and streaming
pipelines. The Apache Beam programming model simplifies the mechanics of
large-scale data processing. Using one of the Apache Beam SDKs, you build a
program that defines the pipeline. Then, you execute the pipeline on a specific
platform such as Dataflow. This model lets you concentrate on the
logical composition of your data processing job, rather than managing the
orchestration of parallel processing.

Apache Beam insulates you from the low-level details of distributed
processing, such as coordinating individual workers, sharding datasets, and
other such tasks. Dataflow fully manages these low-level details.

A _pipeline_ is a graph of transformations that are applied to collections of
data. In Apache Beam, a collection is called a `PCollection`, and a
transform is called a `PTransform`. A `PCollection` can be bounded or unbounded.
A _bounded_ `PCollection` has a known, fixed size, and can be processed using a
batch pipeline. Unbounded `PCollections` must use a streaming pipeline, because
the data is processed as it arrives.

Apache Beam provides connectors to read from and write to different systems,
including Google Cloud services and third-party technologies such as
Apache Kafka.

The following diagram shows an Apache Beam pipeline.

![An Apache Beam pipeline.](/static/dataflow/images/beam-pipeline.png)

You can write `PTransforms` that perform arbitrary logic. The Apache Beam
SDKs also provide a library of useful `PTransforms` out of the box, including
the following:

- Filter out all elements that don't satisfy a predicate.
- Apply a 1-to-1 mapping function over each element.
- Group elements by key.
- Count the elements in a collection
- Count the elements associated with each key in a key-value collection.

To run an Apache Beam pipeline using Dataflow, perform the
following steps:

1. Use the Apache Beam SDK to define and build the pipeline. Alternatively,
   you can deploy a prebuilt pipeline by using a Dataflow
   template.
2. Use Dataflow to run the pipeline. Dataflow
   allocates a pool of VMs to run the job, deploys the code to the VMs, and
   orchestrates running the job.
3. Dataflow performs optimizations on the backend to make your
   pipeline run efficiently and take advantage of parallelization.
4. While a job is running and after it completes, use Dataflow
   management capabilities to monitor progress and troubleshoot.

## Apache Beam programming concepts

This section contains summaries of fundamental concepts.

### Basic batch and streaming processing concepts

Pipelines
: A pipeline encapsulates the entire series of computations that are involved in
reading input data, transforming that data, and writing output data. The input
source and output sink can be the same type or of different types, letting you
convert data from one format to another. Apache Beam programs start by
constructing a `Pipeline` object, and then using that object as the basis for
creating the pipeline's datasets. Each pipeline represents a single, repeatable
job.

PCollection
: A `PCollection` represents a potentially distributed, multi-element dataset that
acts as the pipeline's data. Apache Beam transforms use
`PCollection` objects as inputs and outputs for each step in your pipeline. A
`PCollection` can hold a dataset of a fixed size or an unbounded dataset from a
continuously updating data source.

Transforms
: A transform represents a processing operation that transforms data. A
transform takes one or more `PCollection`s as input, performs an operation that
you specify on each element in that collection, and produces one or more
`PCollection`s as output. A transform can perform nearly any kind of processing
operation, including performing mathematical computations on data, converting
data from one format to another, grouping data together, reading and writing
data, filtering data to output only the elements you want, or combining data
elements into single values.

ParDo
: `ParDo` is the core parallel processing operation in the Apache Beam SDKs,
invoking a user-specified function on each of the elements of the input
`PCollection`. `ParDo` collects the zero or more output elements into an output
`PCollection`. The `ParDo` transform processes elements independently and
possibly in parallel. The user-defined function for a `ParDo` is called a
`DoFn`.

Pipeline I/O
: Apache Beam I/O connectors let you read data into your pipeline and
write output data from your pipeline. An I/O connector consists of a source and
a sink. All Apache Beam sources and sinks are transforms that let your
pipeline work with data from several different data storage formats. You can
also write a custom I/O connector.

Aggregation
: Aggregation is the process of computing some value from multiple input
elements. The primary computational pattern for aggregation in Apache Beam
is to group all elements with a common key and window. Then, it combines each
group of elements using an associative and commutative operation.

User-defined functions (UDFs)
: Some operations within Apache Beam let you execute user-defined code as a
way of configuring the transform. For `ParDo`, user-defined code specifies the
operation to apply to every element, and for `Combine`, it specifies how values
should be combined. A pipeline might contain UDFs written in a different
language than the language of your runner. A pipeline might also contain UDFs
written in multiple languages.

Runner
: Runners are the software that accepts a pipeline and executes it. Most runners
are translators or adapters to massively parallel big-data processing systems.
Other runners exist for local testing and debugging.

Source
: A transform that reads from an external storage system. A pipeline typically
reads input data from a source. The source has a type, which may be different
from the sink type, so you can change the format of data as it moves through the
pipeline.

Sink
: A transform that writes to an external data storage system, such as a file or a
database.

TextIO
: A `PTransform` for reading and writing text files. The `TextIO` source and
sink support files compressed with `gzip` and `bzip2`. The `TextIO` input source
supports JSON. However, for the Dataflow service to be able to
parallelize input and output, your source data must be delimited with a line
feed. You can use a regular expression to target specific files with the
`TextIO` source. Dataflow supports general wildcard patterns. Your
glob expression can appear anywhere in the path. However, Dataflow
does not support recursive wildcards (`**`).

### Advanced batch and streaming processing concepts

Event time
: The time a data event occurs, determined by the timestamp on the data
element itself. This contrasts with the time the actual data element
gets processed at any stage in the pipeline.

Windowing
: Windowing lets you group operations over unbounded collections by dividing
the collection into windows of finite collections according to the timestamps of
the individual elements. A windowing function tells the runner how to assign
elements to an initial window, and how to merge windows of grouped elements.
Apache Beam lets you define different kinds of windows or use the
predefined windowing functions.

Watermarks
: Apache Beam tracks a watermark, which is the system's notion of when all
data in a certain window can be expected to have arrived in the pipeline.
Apache Beam tracks a watermark because data is not guaranteed to arrive
in a pipeline in time order or at predictable intervals. In addition, it's not
guaranteed that data events will appear in the pipeline in the same order
that they were generated.

Trigger
: Triggers determine when to emit aggregated results as data arrives. For
bounded data, results are emitted after all of the input has been processed. For
unbounded data, results are emitted when the watermark passes the end of the
window, indicating that the system believes all input data for that window has
been processed. Apache Beam provides several predefined triggers and lets
you combine them.

## What's next

- To learn more about the basic concepts of building pipelines using the
  Apache Beam SDKs, see the
  [Apache Beam Programming Guide](https://beam.apache.org/documentation/programming-guide/)
  in the Apache Beam documentation.
- For more details about the Apache Beam capabilities supported by
  Dataflow, see the
  [Apache Beam capability matrix](https://beam.apache.org/documentation/runners/capability-matrix/).

_Apache Beam® is a registered trademark of The Apache Software Foundation
or its affiliates in the United States and/or
other countries._
