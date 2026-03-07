---
source_url: https://beam.apache.org/documentation/io/built-in/hadoop/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Apache Hadoop Input/Output Format IO"
beam_last_updated: "Last updated on 2026/03/06"
---

# Hadoop Input/Output Format IO

> **IMPORTANT!** Previous implementation of Hadoop Input Format IO, called `HadoopInputFormatIO`, is deprecated starting from _Apache Beam 2.10_. Please, use current `HadoopFormatIO` which supports both `InputFormat` and `OutputFormat`.

A `HadoopFormatIO` is a transform for reading data from any source or writing data to any sink that implements Hadoop’s `InputFormat` or `OutputFormat` accordingly. For example, Cassandra, Elasticsearch, HBase, Redis, Postgres, etc.

`HadoopFormatIO` allows you to connect to many data sources/sinks that do not yet have a Beam IO transform. However, `HadoopFormatIO` has to make several performance trade-offs in connecting to `InputFormat` or `OutputFormat`. So, if there is another Beam IO transform for connecting specifically to your data source/sink of choice, we recommend you use that one.

### Reading using HadoopFormatIO

You will need to pass a Hadoop `Configuration` with parameters specifying how the read will occur. Many properties of the `Configuration` are optional and some are required for certain `InputFormat` classes, but the following properties must be set for all `InputFormat` classes:

- `mapreduce.job.inputformat.class` - The `InputFormat` class used to connect to your data source of choice.
- `key.class` - The `Key` class returned by the `InputFormat` in `mapreduce.job.inputformat.class`.
- `value.class` - The `Value` class returned by the `InputFormat` in `mapreduce.job.inputformat.class`.

For example:

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

You will need to check if the `Key` and `Value` classes output by the `InputFormat` have a Beam `Coder` available. If not, you can use `withKeyTranslation` or `withValueTranslation` to specify a method transforming instances of those classes into another class that is supported by a Beam `Coder`. These settings are optional and you don’t need to specify translation for both key and value.

For example:

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

#### Read data only with Hadoop configuration.

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

#### Read data with configuration and key translation

For example, a Beam `Coder` is not available for `Key` class, so key translation is required.

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

#### Read data with configuration and value translation

For example, a Beam `Coder` is not available for `Value` class, so value translation is required.

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

#### Read data with configuration, value translation and key translation

For example, Beam Coders are not available for both `Key` class and `Value` classes of `InputFormat`, so key and value translation are required.

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

# Examples for specific InputFormats

### Cassandra - CqlInputFormat

To read data from Cassandra, use `org.apache.cassandra.hadoop.cql3.CqlInputFormat`, which needs the following properties to be set:

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

Call Read transform as follows:

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

The `CqlInputFormat` key class is `java.lang.Long` `Long`, which has a Beam `Coder`. The `CqlInputFormat` value class is `com.datastax.driver.core.Row` `Row`, which does not have a Beam `Coder`. Rather than write a new coder, you can provide your own translation method, as follows:

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

### Elasticsearch - EsInputFormat

To read data from Elasticsearch, use `EsInputFormat`, which needs following properties to be set:

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

Call Read transform as follows:

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

The `org.elasticsearch.hadoop.mr.EsInputFormat`’s `EsInputFormat` key class is `org.apache.hadoop.io.Text` `Text`, and its value class is `org.elasticsearch.hadoop.mr.LinkedMapWritable` `LinkedMapWritable`. Both key and value classes have Beam Coders.

### HCatalog - HCatInputFormat

To read data using HCatalog, use `org.apache.hive.hcatalog.mapreduce.HCatInputFormat`, which needs the following properties to be set:

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

Call Read transform as follows:

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

### Amazon DynamoDB - DynamoDBInputFormat

To read data from Amazon DynamoDB, use `org.apache.hadoop.dynamodb.read.DynamoDBInputFormat`.
DynamoDBInputFormat implements the older `org.apache.hadoop.mapred.InputFormat` interface and to make it compatible with HadoopFormatIO which uses the newer abstract class `org.apache.hadoop.mapreduce.InputFormat`,
a wrapper API is required which acts as an adapter between HadoopFormatIO and DynamoDBInputFormat (or in general any InputFormat implementing `org.apache.hadoop.mapred.InputFormat`)
The below example uses one such available wrapper API - <https://github.com/twitter/elephant-bird/blob/master/core/src/main/java/com/twitter/elephantbird/mapreduce/input/MapReduceInputFormatWrapper.java>

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

Call Read transform as follows:

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

### Apache HBase - TableSnapshotInputFormat

To read data from an HBase table snapshot, use `org.apache.hadoop.hbase.mapreduce.TableSnapshotInputFormat`.
Reading from a table snapshot bypasses the HBase region servers, instead reading HBase data files directly from the filesystem.
This is useful for cases such as reading historical data or offloading of work from the HBase cluster.
There are scenarios when this may prove faster than accessing content through the region servers using the `HBaseIO`.

A table snapshot can be taken using the HBase shell or programmatically:

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

A `TableSnapshotInputFormat` is configured as follows:

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

Call Read transform as follows:

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

### Writing using HadoopFormatIO

You will need to pass a Hadoop `Configuration` with parameters specifying how the write will occur. Many properties of the `Configuration` are optional, and some are required for certain `OutputFormat` classes, but the following properties must be set for all `OutputFormat`s:

- `mapreduce.job.id` - The identifier of the write job. E.g.: end timestamp of window.
- `mapreduce.job.outputformat.class` - The `OutputFormat` class used to connect to your data sink of choice.
- `mapreduce.job.output.key.class` - The key class passed to the `OutputFormat` in `mapreduce.job.outputformat.class`.
- `mapreduce.job.output.value.class` - The value class passed to the `OutputFormat` in `mapreduce.job.outputformat.class`.
- `mapreduce.job.reduces` - Number of reduce tasks. Value is equal to number of write tasks which will be generated. This property is not required for `Write.PartitionedWriterBuilder#withoutPartitioning()` write.
- `mapreduce.job.partitioner.class` - Hadoop partitioner class which will be used for distributing of records among partitions. This property is not required for `Write.PartitionedWriterBuilder#withoutPartitioning()` write.

_Note_: All mentioned values have appropriate constants. E.g.: `HadoopFormatIO.OUTPUT_FORMAT_CLASS_ATTR`.

For example:

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

You will need to set `OutputFormat` key and value class (i.e. “mapreduce.job.output.key.class” and “mapreduce.job.output.value.class”) in Hadoop `Configuration` which are equal to `KeyT` and `ValueT`. If you set different `OutputFormat` key or value class than `OutputFormat`’s actual key or value class then, it will throw `IllegalArgumentException`.

#### Batch writing

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```

#### Stream writing

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support Hadoop Input/Output Format IO.
```
