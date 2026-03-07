---
source_url: https://beam.apache.org/documentation/io/built-in/cdap/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Cdap IO"
beam_last_updated: "Last updated on 2026/03/06"
---

# Cdap IO

A `CdapIO` is a transform for reading data from source or writing data to sink CDAP plugin.

## Batch plugins support

`CdapIO` currently supports the following CDAP Batch plugins by referencing `CDAP plugin` class name:

- [Hubspot Batch Source](https://github.com/data-integrations/hubspot/blob/develop/src/main/java/io/cdap/plugin/hubspot/source/batch/HubspotBatchSource.java)
- [Hubspot Batch Sink](https://github.com/data-integrations/hubspot/blob/develop/src/main/java/io/cdap/plugin/hubspot/sink/batch/HubspotBatchSink.java)
- [Salesforce Batch Source](https://github.com/data-integrations/salesforce/blob/develop/src/main/java/io/cdap/plugin/salesforce/plugin/source/batch/SalesforceBatchSource.java)
- [Salesforce Batch Sink](https://github.com/data-integrations/salesforce/blob/develop/src/main/java/io/cdap/plugin/salesforce/plugin/sink/batch/SalesforceBatchSink.java)
- [ServiceNow Batch Source](https://github.com/data-integrations/servicenow-plugins/blob/develop/src/main/java/io/cdap/plugin/servicenow/source/ServiceNowSource.java)
- [Zendesk Batch Source](https://github.com/data-integrations/zendesk/blob/develop/src/main/java/io/cdap/plugin/zendesk/source/batch/ZendeskBatchSource.java)

Also, any other CDAP Batch plugin based on Hadoop’s `InputFormat` or `OutputFormat` can be used. They can be easily added to the list of supported by class name plugins, for more details please see [CdapIO readme](https://github.com/apache/beam/blob/master/sdks/java/io/cdap/README.md).

## Streaming plugins support

`CdapIO` currently supports CDAP Streaming plugins based on [Apache Spark Receiver](https://spark.apache.org/docs/2.4.0/streaming-custom-receivers.html).

Requirements for CDAP Streaming plugins:

- CDAP Streaming plugin should be based on `Spark Receiver` (Spark 2.4).
- CDAP Streaming plugin should support work with offsets.
- Corresponding Spark Receiver should implement [HasOffset](https://github.com/apache/beam/blob/master/sdks/java/io/sparkreceiver/2/src/main/java/org/apache/beam/sdk/io/sparkreceiver/HasOffset.java) interface.
- Records should have the numeric field that represents record offset.

## Batch reading using CdapIO

In order to read from CDAP plugin you will need to pass:

- `Key` and `Value` classes. You will need to check if these classes have a Beam Coder available.
- `PluginConfig` object with parameters for certain CDAP plugin.

You can easily build `PluginConfig` object using `ConfigWrapper` class by specifying:

- Class of the needed `PluginConfig`.
- `Map<String, Object>` parameters map for corresponding CDAP plugin.

For example:

### Read data by plugin class name

Some CDAP plugins are already supported and can be used just by plugin class name.

For example:

### Read data with building Batch Plugin

If CDAP plugin is not supported by plugin class name, you can easily build `Plugin` object by passing the following parameters:

- Class of CDAP Batch plugin.
- The `InputFormat` class used to connect to your CDAP plugin of choice.
- The `InputFormatProvider` class used to provide `InputFormat`.

Then you will be able to pass this `Plugin` object to `CdapIO`.

For example:

### Examples for specific CDAP plugins

#### CDAP Hubspot Batch Source plugin

#### CDAP Salesforce Batch Source plugin

#### CDAP ServiceNow Batch Source plugin

#### CDAP Zendesk Batch Source plugin

To learn more please check out [complete examples](https://github.com/apache/beam/tree/master/examples/java/cdap).

## Batch writing using CdapIO

In order to write to CDAP plugin you will need to pass:

- `Key` and `Value` classes. You will need to check if these classes have a Beam Coder available.
- `locksDirPath`, which is locks directory path where locks will be stored. This parameter is needed for Hadoop External Synchronization (mechanism for acquiring locks related to the write job).
- `PluginConfig` object with parameters for certain CDAP plugin.

You can easily build `PluginConfig` object using `ConfigWrapper` class by specifying:

- Class of the needed `PluginConfig`.
- `Map<String, Object>` parameters map for corresponding CDAP plugin.

For example:

### Write data by plugin class name

Some CDAP plugins are already supported and can be used just by plugin class name.

For example:

### Write data with building Batch Plugin

If CDAP plugin is not supported by plugin class name, you can easily build `Plugin` object by passing the following parameters:

- Class of CDAP plugin.
- The `OutputFormat` class used to connect to your CDAP plugin of choice.
- The `OutputFormatProvider` class used to provide `OutputFormat`.

Then you will be able to pass this `Plugin` object to `CdapIO`.

For example:

### Examples for specific CDAP plugins

#### CDAP Hubspot Batch Sink plugin

#### CDAP Salesforce Batch Sink plugin

To learn more please check out [complete examples](https://github.com/apache/beam/tree/master/examples/java/cdap/src/main/java/org/apache/beam/examples/complete/cdap).

## Streaming reading using CdapIO

In order to read from CDAP plugin you will need to pass:

- `Key` and `Value` classes. You will need to check if these classes have a Beam Coder available.
- `PluginConfig` object with parameters for certain CDAP plugin.

You can easily build `PluginConfig` object using `ConfigWrapper` class by specifying:

- Class of the needed `PluginConfig`.
- `Map<String, Object>` parameters map for corresponding CDAP plugin.

For example:

### Read data by plugin class name

Some CDAP plugins are already supported and can be used just by plugin class name.

For example:

### Read data with building Streaming Plugin

If CDAP plugin is not supported by plugin class name, you can easily build `Plugin` object by passing the following parameters:

- Class of CDAP Streaming plugin.
- `getOffsetFn`, which is `SerializableFunction` that defines how to get `Long` record offset from a record.
- `receiverClass`, which is Spark (v 2.4) `Receiver` class associated with CDAP plugin.
- (Optionally) `getReceiverArgsFromConfigFn`, which is `SerializableFunction` that defines how to get constructor arguments for Spark `Receiver` using `PluginConfig` object.

Then you will be able to pass this `Plugin` object to `CdapIO`.

For example:

### Read data with optional parameters

Optionally you can pass the following optional parameters:

- `pullFrequencySec`, which is delay in seconds between polling for new records updates.
- `startOffset`, which is inclusive start offset from which the reading should be started.

For example:

### Examples for specific CDAP plugins

#### CDAP Hubspot Streaming Source plugin

#### CDAP Salesforce Streaming Source plugin

To learn more please check out [complete examples](https://github.com/apache/beam/tree/master/examples/java/cdap/src/main/java/org/apache/beam/examples/complete/cdap).
