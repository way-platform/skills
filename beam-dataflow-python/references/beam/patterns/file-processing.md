---
source_url: https://beam.apache.org/documentation/patterns/file-processing/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "File processing patterns"
beam_last_updated: "Last updated on 2026/03/06"
---

# File processing patterns

This page describes common file processing tasks. For more information on file-based I/O, see [Pipeline I/O](/documentation/programming-guide/#pipeline-io) and [File-based input and output data](/documentation/programming-guide/#file-based-data).

## Processing files as they arrive

This section shows you how to process files as they arrive in your file system or object store (like Google Cloud Storage). You can continuously read files or trigger stream and processing pipelines when a file arrives.

### Continuous read mode

- Storing processed filenames in an external file and deduplicating the lists at the next transform
- Adding timestamps to filenames, writing a glob pattern to pull in only new files, and matching the pattern when the pipeline restarts

The continuous-read option is not available for Python.

### Stream processing triggered from external source

A streaming pipeline can process data from an unbounded source. For example, to trigger stream processing with Google Cloud Pub/Sub:

1. Use an external process to detect when new files arrive.
2. Send a Google Cloud Pub/Sub message with a URI to the file.
3. Access the URI from a `DoFn` that follows the Google Cloud Pub/Sub source.
4. Process the file.

### Batch processing triggered from external source

To start or schedule a batch pipeline job when a file arrives, write the triggering event in the source file itself. This has the most latency because the pipeline must initialize before processing. Itâs best suited for low-frequency, large, file-size updates.

## Accessing filenames

1. Create a `ReadableFile` instance with `FileIO`. `FileIO` returns a `PCollection<ReadableFile>` object. The `ReadableFile` class contains the filename.
2. Call the `readFullyAsUTF8String()` method to read the file into memory and return the filename as a `String` object. If memory is limited, you can use utility classes like [`FileSystems`](https://beam.apache.org/releases/javadoc/current/org/apache/beam/sdk/io/FileSystems.html) to work directly with the file.

To read filenames in a pipeline job:

1. Collect the list of file URIs. You can use the [`FileSystems`](https://beam.apache.org/releases/pydoc/current/apache_beam.io.filesystems.html?highlight=filesystems#module-apache_beam.io.filesystems) module to get a list of files that match a glob pattern.
2. Pass the file URIs to a `PCollection`.

![](/images/copy-icon.svg)

```
with beam.Pipeline() as pipeline:
  readable_files = (
      pipeline
      | fileio.MatchFiles('hdfs://path/to/*.txt')
      | fileio.ReadMatches()
      | beam.Reshuffle())
  files_and_contents = (
      readable_files
      | beam.Map(lambda x: (x.metadata.path, x.read_utf8())))
```
