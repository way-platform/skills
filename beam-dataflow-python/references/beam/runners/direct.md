---
source_url: https://beam.apache.org/documentation/runners/direct/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Direct Runner"
beam_last_updated: "Last updated on 2026/03/06"
---

# Using the Direct Runner

The Direct Runner executes pipelines on your machine and is designed to validate that pipelines adhere to the Apache Beam model as closely as possible. Instead of focusing on efficient pipeline execution, the Direct Runner performs additional checks to ensure that users do not rely on semantics that are not guaranteed by the model. Some of these checks include:

- enforcing immutability of elements
- enforcing encodability of elements
- elements are processed in an arbitrary order at all points
- serialization of user functions (`DoFn`, `CombineFn`, etc.)

Using the Direct Runner for testing and development helps ensure that pipelines are robust across different Beam runners. In addition, debugging failed runs can be a non-trivial task when a pipeline executes on a remote cluster. Instead, it is often faster and simpler to perform local unit testing on your pipeline code. Unit testing your pipeline locally also allows you to use your preferred local debugging tools.

Here are some resources with information about how to test your pipelines.

- [Test Your Pipeline](/documentation/pipelines/test-your-pipeline/)
- The [Apache Beam WordCount Walkthrough](/get-started/wordcount-example/#testing-your-pipeline-with-asserts) contains an example of logging and testing a pipeline with `assert_that`.

The Direct Runner is not designed for production pipelines, because it’s optimized for correctness rather than performance. The Direct Runner must fit all user data in memory, whereas the Flink and Spark runners can spill data to disk if it doesn’t fit in memory. Consequently, Flink and Spark runners are able to run larger pipelines and are better suited to production workloads.

## Direct Runner prerequisites and setup

### Specify your dependency

This section is not applicable to the Beam SDK for Python.

## Pipeline options for the Direct Runner

For general instructions on how to set pipeline options, see the [programming guide](/documentation/programming-guide/#configuring-pipeline-options).

When executing your pipeline from the command-line, set `runner` to `direct` or `DirectRunner`. The default values for the other pipeline options are generally sufficient.

See the reference documentation for the
[`DirectOptions`](https://beam.apache.org/releases/pydoc/2.71.0/apache_beam.options.pipeline_options.html#apache_beam.options.pipeline_options.DirectOptions)
interface for defaults and additional pipeline configuration options.

## Additional information and caveats

### Memory considerations

Local execution is limited by the memory available in your local environment. It is highly recommended that you run your pipeline with data sets small enough to fit in local memory. You can create a small in-memory data set using a [`Create`](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/transforms/core.py) transform, or you can use a [`Read`](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/io/iobase.py) transform to work with small local or remote files.

### Streaming execution

Streaming support for Python DirectRunner is limited. For known issues, see: <https://github.com/apache/beam/issues/24528>.

If your pipeline uses an unbounded data source or sink, you must set the `streaming` option to `true`.

### Parallel execution

Python [FnApiRunner](/contribute/runner-guide/#the-fn-api) supports multi-threading and multi-processing mode.

#### Setting parallelism

Number of threads or subprocesses is defined by setting the `direct_num_workers` pipeline option.
From 2.22.0, `direct_num_workers = 0` is supported. When `direct_num_workers` is set to 0, it will set the number of threads/subprocess to the number of cores of the machine where the pipeline is running.

**Setting running mode**

In Beam 2.19.0 and newer, you can use the `direct_running_mode` pipeline option to set the running mode.
`direct_running_mode` can be one of [`'in_memory'`, `'multi_threading'`, `'multi_processing'`].

**in_memory**: Runner and workers’ communication happens in memory (not through gRPC). This is a default mode.

**multi_threading**: Runner and workers communicate through gRPC and each worker runs in a thread.

**multi_processing**: Runner and workers communicate through gRPC and each worker runs in a subprocess.

### Before deploying pipeline to remote runner

While testing on the direct runner is convenient, it can still behave differently from remote runners beyond Beam model semantics, especially for runtime environment related issues. In general, it is recommended to test your pipeline on targeted remote runner in small scale before fully deploying into production.
