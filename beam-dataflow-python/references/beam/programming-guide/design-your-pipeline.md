---
source_url: https://beam.apache.org/documentation/pipelines/design-your-pipeline/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Design Your Pipeline"
beam_last_updated: "Last updated on 2026/03/06"
---

# Design Your Pipeline

- [What to consider when designing your pipeline](#what-to-consider-when-designing-your-pipeline)
- [A basic pipeline](#a-basic-pipeline)
- [Branching PCollections](#branching-pcollections)
  - [Multiple transforms process the same PCollection](#multiple-transforms-process-the-same-pcollection)
  - [A single transform that produces multiple outputs](#a-single-transform-that-produces-multiple-outputs)
- [Merging PCollections](#merging-pcollections)
- [Multiple sources](#multiple-sources)
- [What’s next](#whats-next)

This page helps you design your Apache Beam pipeline. It includes information about how to determine your pipeline’s structure, how to choose which transforms to apply to your data, and how to determine your input and output methods.

Before reading this section, it is recommended that you become familiar with the information in the [Beam programming guide](/documentation/programming-guide).

## What to consider when designing your pipeline

When designing your Beam pipeline, consider a few basic questions:

- **Where is your input data stored?** How many sets of input data do you have? This will determine what kinds of `Read` transforms you’ll need to apply at the start of your pipeline.
- **What does your data look like?** It might be plaintext, formatted log files, or rows in a database table. Some Beam transforms work exclusively on `PCollection`s of key/value pairs; you’ll need to determine if and how your data is keyed and how to best represent that in your pipeline’s `PCollection`(s).
- **What do you want to do with your data?** The core transforms in the Beam SDKs are general purpose. Knowing how you need to change or manipulate your data will determine how you build core transforms like [ParDo](/documentation/programming-guide/#pardo), or when you use pre-written transforms included with the Beam SDKs.
- **What does your output data look like, and where should it go?** This will determine what kinds of `Write` transforms you’ll need to apply at the end of your pipeline.

## A basic pipeline

The simplest pipelines represent a linear flow of operations, as shown in figure 1.

![A linear pipeline starts with one input collection, sequentially appliesthree transforms, and ends with one output collection.](/images/design-your-pipeline-linear.svg)

_Figure 1: A linear pipeline._

However, your pipeline can be significantly more complex. A pipeline represents a [Directed Acyclic Graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph) of steps. It can have multiple input sources, multiple output sinks, and its operations (`PTransform`s) can both read and output multiple `PCollection`s. The following examples show some of the different shapes your pipeline can take.

## Branching PCollections

It’s important to understand that transforms do not consume `PCollection`s; instead, they consider each individual element of a `PCollection` and create a new `PCollection` as output. This way, you can do different things to different elements in the same `PCollection`.

### Multiple transforms process the same PCollection

You can use the same `PCollection` as input for multiple transforms without consuming the input or altering it.

The pipeline in figure 2 is a branching pipeline. The pipeline reads its input (first names represented as strings) from a database table and creates a `PCollection` of table rows. Then, the pipeline applies multiple transforms to the **same** `PCollection`. Transform A extracts all the names in that `PCollection` that start with the letter ‘A’, and Transform B extracts all the names in that `PCollection` that start with the letter ‘B’. Both transforms A and B have the same input `PCollection`.

![The pipeline applies two transforms to a single input collection. Eachtransform produces an output collection.](/images/design-your-pipeline-multiple-pcollections.svg)

_Figure 2: A branching pipeline. Two transforms are applied to a single
PCollection of database table rows._

The following example code applies two transforms to a single input collection.

### A single transform that produces multiple outputs

Another way to branch a pipeline is to have a **single** transform output to multiple `PCollection`s by using [tagged outputs](/documentation/programming-guide/#additional-outputs). Transforms that produce more than one output process each element of the input once, and output to zero or more `PCollection`s.

Figure 3 illustrates the same example described above, but with one transform that produces multiple outputs. Names that start with ‘A’ are added to the main output `PCollection`, and names that start with ‘B’ are added to an additional output `PCollection`.

![The pipeline applies one transform that produces multiple output collections.](/images/design-your-pipeline-additional-outputs.svg)

_Figure 3: A pipeline with a transform that outputs multiple PCollections._

If we compare the pipelines in figure 2 and figure 3, you can see they perform
the same operation in different ways. The pipeline in figure 2 contains two
transforms that process the elements in the same input `PCollection`. One
transform uses the following logic:

```
if (starts with 'A') { outputToPCollectionA }
```

while the other transform uses:

```
if (starts with 'B') { outputToPCollectionB }
```

Because each transform reads the entire input `PCollection`, each element in the input `PCollection` is processed twice.

The pipeline in figure 3 performs the same operation in a different way - with only one transform that uses the following logic:

```
if (starts with 'A') { outputToPCollectionA } else if (starts with 'B') { outputToPCollectionB }
```

where each element in the input `PCollection` is processed once.

The following example code applies one transform that processes each element
once and outputs two collections.

You can use either mechanism to produce multiple output `PCollection`s. The first option is recommended if it logically does not make sense to combine the processing logic into one `ParDo`. However, using the second option (a single transform that produces multiple outputs) makes more sense if the transform’s computation per element is time-consuming, and is more scalable if you plan to add more output types in the future.

## Merging PCollections

Often, after you’ve branched your `PCollection` into multiple `PCollection`s via multiple transforms, you’ll want to merge some or all of those resulting `PCollection`s back together. You can do so by using one of the following:

- **Flatten** - You can use the `Flatten` transform in the Beam SDKs to merge multiple `PCollection`s of the **same type**.
- **Join** - You can use the `CoGroupByKey` transform in the Beam SDK to perform a relational join between two `PCollection`s. The `PCollection`s must be keyed (i.e. they must be collections of key/value pairs) and they must use the same key type.

The example in figure 4 is a continuation of the example in figure 2 in [the
section above](#multiple-transforms-process-the-same-pcollection). After
branching into two `PCollection`s, one with names that begin with ‘A’ and one
with names that begin with ‘B’, the pipeline merges the two together into a
single `PCollection` that now contains all names that begin with either ‘A’ or
‘B’. Here, it makes sense to use `Flatten` because the `PCollection`s being
merged both contain the same type.

![The pipeline merges two collections into one collection with the Flatten transform.](/images/design-your-pipeline-flatten.svg)

_Figure 4: A pipeline that merges two collections into one collection with the Flatten transform._

The following example code applies `Flatten` to merge two collections.

## Multiple sources

Your pipeline can read its input from one or more sources. If your pipeline reads from multiple sources and the data from those sources is related, it can be useful to join the inputs together. In the example illustrated in figure 5 below, the pipeline reads names and addresses from a database table, and names and order numbers from a Kafka topic. The pipeline then uses `CoGroupByKey` to join this information, where the key is the name; the resulting `PCollection` contains all the combinations of names, addresses, and orders.

![The pipeline joins two input collections into one collection with the Join transform.](/images/design-your-pipeline-join.svg)

_Figure 5: A pipeline that does a relational join of two input collections._

The following example code applies `Join` to join two input collections.

## What’s next

- [Create your own pipeline](/documentation/pipelines/create-your-pipeline).
- [Test your pipeline](/documentation/pipelines/test-your-pipeline).
