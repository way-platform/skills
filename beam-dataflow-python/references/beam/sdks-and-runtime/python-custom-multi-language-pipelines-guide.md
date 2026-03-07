---
source_url: https://beam.apache.org/documentation/sdks/python-custom-multi-language-pipelines-guide/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Python custom multi-language pipelines guide"
beam_last_updated: ""
---

# Python custom multi-language pipelines guide

Apache Beam’s powerful model enables the development of scalable, resilient, and production-ready transforms, but the process often requires significant time and effort.

With SDKs available in multiple languages (Java, Python, Golang, YAML, etc.), creating and maintaining transforms for each language becomes a challenge, particularly for IOs. Developers must navigate different APIs, address unique quirks, and manage ongoing maintenanceâsuch as updates, new features, and documentationâwhile ensuring consistent behavior across SDKs. This results in redundant work, as the same functionality is implemented repeatedly for each language (M x N effort, where M is the number of SDKs and N is the number of transforms).

To streamline this process, Beamâs portability framework enables the use of portable transforms that can be shared across languages. This reduces duplication, allowing developers to focus on maintaining only N transforms. Pipelines combining [portable transforms](#portable-transform) from other SDK(s) are known as [âmulti-languageâ pipelines](../../programming-guide/#13-multi-language-pipelines-multi-language-pipelines).

The SchemaTransform framework represents the latest advancement in enhancing this multi-language capability.

The following jumps straight into the guide. Check out the [appendix](#appendix) section below for some of the terminology used here. For a runnable example, check out this [page](python-multi-language-pipelines-2.md).

## Create a Java SchemaTransform

For better readability, use [**TypedSchemaTransformProvider**](https://beam.apache.org/releases/javadoc/current/index.html?org/apache/beam/sdk/schemas/transforms/TypedSchemaTransformProvider.html), a [SchemaTransformProvider](#schematransformprovider) parameterized on a custom configuration type `T`. TypedSchemaTransformProvider will take care of converting the custom type definition to a Beam [Schema](../../basics/#schema), and converting an instance to a Beam Row.

### Implement a configuration

First, set up a Beam Schema-compatible configuration. This will be used to construct the transform. AutoValue types are encouraged for readability. Adding the appropriate `@DefaultSchema` annotation will help Beam do the conversions mentioned above.

This configuration is surfaced to foreign SDKs. For example, when using this transform in Python, use the following format:

```
with beam.Pipeline() as p:
  (p
   | Create([...])
   | MySchemaTransform(foo="abc", bar=123)
```

When using this transform in YAML, use the following format:

### Implement a TypedSchemaTransformProvider

Next, implement the `TypedSchemaTransformProvider`. The following two methods are required:

- `identifier`: Returns a unique identifier for this transform. The [Beam standard](../../programming-guide/#1314-defining-a-urn) follows this structure: `<namespace>:<org>:<functionality>:<version>`.
- `from`: Builds the transform using a provided configuration.

An [expansion service](#expansion-service) uses these methods to find and build the transform. The `@AutoService(SchemaTransformProvider.class)` annotation is also required to ensure this provider is recognized by the expansion service.

#### Additional metadata (optional)

The following optional methods can help provide relevant metadata:

- `description`: Provide a human-readable description for the transform. Remote SDKs can use this text to generate documentation.
- `inputCollectionNames`: Provide PCollection tags that this transform expects to take in.
- `outputCollectionNames`: Provide PCollection tags this transform expects to produce.

## Build an expansion service that contains the transform

Use an expansion service to make the transform available to foreign SDKs.

First, build a shaded JAR file that includes:

1. the transform,
2. the [**ExpansionService artifact**](https://central.sonatype.com/artifact/org.apache.beam/beam-sdks-java-expansion-service),
3. and some additional dependencies.

### Gradle build file

Next, run the shaded JAR file, and provide a port to host the service. A list of available SchemaTransformProviders will be displayed.

```
$ java -jar path/to/my-expansion-service.jar 12345

Starting expansion service at localhost:12345

Registered transforms:
        ...
Registered SchemaTransformProviders:
        beam:schematransform:org.apache.beam:my_transform:v1
```

The transform is discoverable at `localhost:12345`. Foreign SDKs can now discover and add it to their pipelines. The next section demonstrates how to do this with a Python pipeline.

## Use the portable transform in a Python pipeline

The Python SDKâs [**ExternalTransformProvider**](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.external_transform_provider.html#apache_beam.transforms.external_transform_provider.ExternalTransformProvider)
can dynamically generate wrappers for portable transforms.

```
from apache_beam.transforms.external_transform_provider import ExternalTransformProvider
```

### Connect to an expansion service

First, connect to an expansion service that contains the transform. This section demonstrates two methods of connecting to the expansion service.

#### Connect to an already running service

If your expansion service JAR file is already running, pass in the address:

```
provider = ExternalTransformProvider("localhost:12345")
```

#### Start a service based on a Java JAR file

If the service lives in a JAR file but isnât currently running, use Beam utilities to run the service in a subprocess:

```
from apache_beam.transforms.external import JavaJarExpansionService

provider = ExternalTransformProvider(
    JavaJarExpansionService("path/to/my-expansion-service.jar"))
```

You can also provide a list of services:

```
provider = ExternalTransformProvider([
    "localhost:12345",
    JavaJarExpansionService("path/to/my-expansion-service.jar"),
    JavaJarExpansionService("path/to/another-expansion-service.jar")])
```

When initialized, the `ExternalTransformProvider` connects to the expansion service(s), retrieves all portable transforms, and generates a Pythonic wrapper for each one.

### Retrieve and use the transform

Retrieve the transform using its unique identifier and use it in your multi-language pipeline:

```
identifier = "beam:schematransform:org.apache.beam:my_transform:v1"
MyTransform = provider.get_urn(identifier)

with beam.Pipeline() as p:
  p | beam.Create(...) | MyTransform(foo="abc", bar=123)
```

### Inspect the transform’s metadata

You can learn more about a portable transformâs configuration by inspecting its metadata:

```
import inspect

inspect.getdoc(MyTransform)
# Output: "This transform does this and that..."

inspect.signature(MyTransform)
# Output: (foo: "str: Description of what foo does...",
#	     bar: "int: Description of what bar does....")
```

This metadata is generated directly from the provider’s implementation. The class documentation is generated from the [optional **description** method](#additional-metadata-optional). The signature information is generated from the `@SchemaFieldDescription` annotations in the [configuration object](#implement-a-configuration).

### Using Beam native Java SchemaTransforms

If there’s an existing Beam native Java SchemaTransform you’d like to use, and you know which expansion service module it’s in, you can connect to it using `BeamJarExpansionService`:

```
from apache_beam.transforms.external_transform_provider import ExternalTransformProvider
from apache_beam.transforms.external import BeamJarExpansionService

identifier = "beam:schematransform:org.apache.beam:bigquery_fileloads:v1"
expansion_service = "sdks:java:io:google-cloud-platform:expansion-service:shadowJar"

provider = ExternalTransformProvider(BeamJarExpansionService(expansion_service))
BqFileLoads = provider.get_urn(identifier)

with beam.Pipeline(argv=args) as p:
  p | beam.Create(...) | BqFileLoads(table="project.dataset.table")
```

## Appendix

### Portable transform

Also known as a [cross-language transform](../../glossary/#cross-language-transforms): a transform that is made available to other SDKs (i.e. other languages) via an expansion service. Such a transform must offer a way to be constructed using language-agnostic parameter types.

### Expansion Service

A container that can hold multiple portable transforms. During pipeline expansion, this service will

- Look up the transform in its internal registry
- Build the transform in its native language using the provided configuration
- Expand the transform â i.e. construct the transformâs sub-graph to be inserted in the pipeline
- Establish a gRPC communication channel with the runner to exchange data and signals during pipeline execution.

### SchemaTransform

A transform that takes and produces PCollections of Beam Rows with a predefined Schema, i.e.:

### SchemaTransformProvider

Produces a SchemaTransform using a provided configuration. An expansion service uses this interface to identify and build the transform for foreign SDKs.
