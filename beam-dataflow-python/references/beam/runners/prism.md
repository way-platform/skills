---
source_url: https://beam.apache.org/documentation/runners/prism/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Prism Runner"
beam_last_updated: "Last updated on 2026/03/06"
---

# Overview

The Apache Beam Prism Runner can be used to execute Beam pipelines locally using [Beam Portability](/roadmap/portability/).

The Prism runner is suitable for small scale local testing and provides:

- A statically compiled, single binary for simple deployment without additional configuration.
- A web UI when executing in stand alone mode.
- A direct implementation of Beam execution semantics.
- A streaming-first runtime that supports batch processing and data streaming programs.
- Fast, in-memory execution for to simplify SDK, Transform, and Pipeline development.
- Cross Language Transform support.

Written in [Go](https://go.dev), it is the default runner for the [Go SDK](/roadmap/go-sdk/), but can be used in other SDKs as well (see below).

# Capabilities

While Prism already supports a great deal of Beam features, it doesn’t yet support everything.
Prism is under active development to close these gaps.

With the exception of timer issues, use of unsupported features should fail the pipeline at job submission time.

In the [2.59.0 release](/blog/beam-2.59.0/), Prism passes most runner validations tests with the exceptions of pipelines using the following features:

OrderedListState, OnWindowExpiry (eg. GroupIntoBatches), CustomWindows, MergingWindowFns, Trigger and WindowingStrategy associated features, Bundle Finalization, Looping Timers, and some Coder related issues such as with Python combiner packing, and Java Schema transforms, and heterogenous flatten coders.
Processing Time timers do not yet have real time support.

See the [Roadmap](/roadmap/prism-runner/) for how to find current progress.
Specific feature support information will soon migrate to the [Runner Capability Matrix](/documentation/runners/capability-matrix/).

# Using the Prism Runner

Set the runner to `PrismRunner`.

For other SDKs, Prism is included as an asset on [Beam Github Releases](https://github.com/apache/beam/releases/tag/v2.71.0) for download and stand alone use.

Here are some resources with information about how to test your pipelines.

- [Test Your Pipeline](/documentation/pipelines/test-your-pipeline/)
- The [Apache Beam WordCount Walkthrough](/get-started/wordcount-example/#testing-your-pipeline-with-asserts) contains an example of logging and testing a pipeline with asserts.

### Specify your dependency

This section is not applicable to the Beam SDK for Python. Prism is built in.

Except for the Go SDK, Prism is included as an asset on [Beam Github Releases](https://github.com/apache/beam/releases/tag/v2.71.0) for automatic download, startup, and shutdown on SDKs.
The binary is cached locally for subsequent executions.

## Pipeline options for the Prism Runner

Prism aims to have minimal configuration required, and does not currently present user pipeline options.

## Running Prism Standalone

Prism can be executed as a stand alone binary and will present a basic UI for listing jobs, and job status.
This is an optional mode for Prism that is useful for demos or rapid iteration.
It is not a requirement for using Prism in the Java or Python SDKs.

This can be done in two ways, downloading an asset from the github release, or building the binary locally with Go installed.

In either case, Prism serves a JobManagement API endpoint, and a Webpage UI locally.
Jobs can be submitted using `--runner=PortableRunner --endpoint=<endpoint address>` and monitored using the webpage UI.

Example output from the Prism binary:

```
2024/09/30 09:56:42 INFO Serving JobManagement endpoint=localhost:8073
2024/09/30 09:56:42 INFO Serving WebUI endpoint=http://localhost:8074
```

The binary has the following optional flags:

- `--job_port` sets the port for the Job management server (defaults to 8073)
- `--web_port` sets the port for the web ui (defaults to 8074)
- `--serve_http` enables or disables the web ui (defaults to true)
- `---idle_shutdown_timeout` sets a duration that Prism will wait for a new job before automatically shutting itself down. Uses duration format like `10s`, `5m`,`2h`. Defaults to not shutting down.

### Download a release asset

This approach doesn’t require other dependencies or runtimes installed.
This is recommended if you want to deploy Prism on some other machine.

Navigate to the latest [Beam Release Github page](https://github.com/apache/beam/releases/tag/v2.71.0), scroll to the bottom, and download the correct asset for where you want to run Prism.

For example, if you want to execute Prism on a newer MacBook, you’d download the `darwin-arm64` asset. For executing on many cloud machines, you’d download the `linux-amd64` asset.

This requires downloading the right asset for the machine Prism will run on, such as your development machine.

Simply unzip, and execute.

### Build from the release with Go.

This approach requires a [recent version of Go installed](https://go.dev/dl/).
This is recommended if you only want to run Prism on your local machine.

You can insall Prism with `go install`:

```
go install github.com/apache/beam/sdks/v2/go/cmd/prism@latest
prism
```

Or simply build and execute the binary immeadiately using `go run`:

```
go run github.com/apache/beam/sdks/v2/go/cmd/prism@latest
```
