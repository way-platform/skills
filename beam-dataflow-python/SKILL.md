---
name: beam-dataflow-python
description: Expertise in Apache Beam (Python SDK) and Google Cloud Dataflow. Use when creating, debugging, optimizing, or reviewing Python-based data pipelines. Critical for tasks involving unified batch/streaming architectures, Protobuf serialization, windowing/triggers, testing Beam logic, or operational reliability on Google Cloud.
---

# Apache Beam & Dataflow (Python) Best Practices

Implement Way's specific architectural patterns and modern (2024+) community best practices when building and editing Dataflow Python pipelines. Follow these core workflows to ensure high-performance, cost-efficient, and maintainable data systems.

## 1. Unified Pipeline Architecture
Design pipelines to handle both streaming and batch data processing using the same core logic structure. Treat batch as a bounded stream.

*   **Implement Mode-Driven Routing**: Parameterize pipeline construction with a `mode` flag (e.g., `--mode streaming` vs. `--mode batch`). Use this flag to conditionally inject the appropriate I/O connectors (Pub/Sub vs. BigQuery/GCS) and windowing configurations while keeping the transform logic identical.
*   **Enforce Layered Architecture**: Strictly separate files by concern:
    *   `pipeline.py`: High-level `PTransform` chain composition (wiring sources, transforms, sinks).
    *   `transforms.py`: Custom `DoFn` and `PTransform` implementations.
    *   `state_machine.py` / Domain Logic: Pure Python state tracking and aggregations.
*   **Prioritize Event-Time**: Always develop logic around event time, rather than processing time, ensuring backfills produce consistent state.

**Reference**: See [Way's Pipeline Patterns](references/key-topics.md) and [Community Best Practices](references/community/key-topics.md).

## 2. Testing & Logic Decoupling
Adopt the "Logic-First Decoupling" method to speed up testing and ensure accuracy.

*   **Extract Domain Logic**: Remove complex business logic (e.g., session sequencing, state chunking) from `DoFn`s. Place them into pure Python classes or functions that contain zero `apache_beam` imports.
*   **Test in Three Tiers**:
    1.  **Pure Python (80-90%)**: Test the decoupled domain logic using standard `pytest`. This executes instantly and avoids Beam runner overhead.
    2.  **Transform Logic**: Use `TestPipeline` and `assert_that` strictly to verify boundary behavior: verifying that `DoFn`s route the pure logic correctly, manage Beam `State` and `Timer` APIs, and emit the right side-outputs.
    3.  **Integration**: Run local end-to-end tests using mock I/O, leveraging the modern **Prism Runner** for high-fidelity stateful execution.

**Reference**: See [Community Testing Patterns](references/community/key-topics.md#4-testing--domain-logic-decoupling).

## 3. Data Serialization & BigQuery Integration
Google Protocol Buffers (Protobuf) is our canonical data schema across all streaming and batch environments.

*   **Register ProtoCoders**: Use `coders.registry.register_coder(MyMessage, coders.ProtoCoder)` to seamlessly shuffle and serialize objects in Python.
*   **BigQuery Sinks**: Prefer the **Storage Write API** (`method='STORAGE_WRITE_API'`) over legacy streaming inserts for low latency and high throughput. 
*   **Protobuf Mappings**: When mapping Protobuf to dictionaries for external sinks, use `google.protobuf.json_format.MessageToDict` (or `ParseDict` for sources) with arguments like `preserving_proto_field_name=True`. Convert Protobuf Enums to Strings to avoid breakage.

**Reference**: See [Protobuf & BigQuery Integration](references/community/key-topics.md#2-protobuf--bigquery-integration) and [03-bigquery-io-optimization](references/community/03-bigquery-io-optimization.md).

## 4. Advanced Windowing, Triggers & PaneInfo
Handle out-of-order streams correctly by applying proper event-time bounding.

*   **Abstract Windowing**: Extract window logic into configuration objects (e.g., `StreamingSessionWindowConfig`). Use triggers (e.g., `AfterWatermark`) and explicitly define `allowed_lateness`.
*   **Track Pane State**: Within a `DoFn`, inject `pane_info=beam.DoFn.PaneInfoParam`. Evaluate `pane_info.timing` to differentiate outputs:
    *   `EARLY`: Speculative / running aggregates. Throttle these (e.g., `Repeatedly(AfterProcessingTime(delay=...))`) to avoid "pane explosion".
    *   `ON_TIME`: The watermark has passed the window end.
    *   `LATE`: Corrections arriving after the window closes.
*   **Ensure Downstream Idempotency**: Since `LATE` panes arrive asynchronously, ensure external sinks handle overwrites properly by using the window boundaries and `pane_info.index` as a primary key.

**Reference**: See [Advanced Windowing & PaneInfo Handling](references/community/key-topics.md#3-advanced-windowing--paneinfo-handling).

## 5. Resilience & Operational Excellence
*   **Dead-Letter Queues (DLQ)**: Do not allow pipelines to crash on "poison pill" records. Use side outputs or the 2025 preferred `with_exception_handling` wrapper to route failed records to a dead-letter queue.
*   **Idempotency**: Dataflow guarantees exactly-once *delivery*, but not exactly-once *execution*. Ensure all API calls and external writes are idempotent.
*   **Autoscaling**: Deploy using **Vertical Autoscaling** and **C4A (ARM)** workers to minimize bottlenecks and reduce costs on Google Cloud.

## Agent Reference Index (Progressive Disclosure)

Do not guess syntax or patterns. When you encounter specific challenges, use `read_file` or `grep_search` on the following reference documents to load exact procedures into your context.

### 🏗️ Architecture & Core Strategy
*   **[Way's Internal Patterns](references/key-topics.md)**: Read for the baseline architectural expectations (Unified pipelines, Pure Python State Machines, Mode routing).
*   **[2024+ Community Best Practices](references/community/key-topics.md)**: Read for the industry consensus on these same topics (Logic-First Decoupling, DLQs).

### 🛠️ Detailed Community Guides (2025+)
*   **Testing & Mocking**: Read [01-testing-and-ci-cd.md](references/community/01-testing-and-ci-cd.md) when setting up `TestStream`, `PrismRunner`, or CI/CD pipelines.
*   **Error Handling**: Read [02-dead-letter-queues.md](references/community/02-dead-letter-queues.md) when implementing `with_exception_handling` or side-outputs for bad records.
*   **BigQuery I/O**: Read [03-bigquery-io-optimization.md](references/community/03-bigquery-io-optimization.md) for the exact syntax of the `STORAGE_WRITE_API` and mapping schemas.
*   **Cloud Resources**: Read [04-autoscaling-resource-management.md](references/community/04-autoscaling-resource-management.md) when configuring worker types (C4A), vertical autoscaling, or FlexRS.
*   **Streaming & Late Data**: Read [05-windowing-and-triggers.md](references/community/05-windowing-and-triggers.md) when defining complex event-time windows and `allowed_lateness`.
*   **Java Interop**: Read [06-cross-language-transforms.md](references/community/06-cross-language-transforms.md) when you need to use Java connectors (like KafkaIO) inside Python.
*   **Pandas in Beam**: Read [07-dataframe-api.md](references/community/07-dataframe-api.md) when performing scalar/tabular operations that benefit from a DataFrame approach.
*   **Deployment**: Read [08-docker-custom-containers-flex-templates.md](references/community/08-docker-custom-containers-flex-templates.md) when packaging pipelines for Dataflow runtime.
*   **Complex Stateful Logic**: Read [09-state-and-timers.md](references/community/09-state-and-timers.md) when session windows aren't enough and you need per-key state management.
*   **No-Code Pipelines**: Read [10-beam-yaml-declarative.md](references/community/10-beam-yaml-declarative.md) if tasked with simple ingestion routing without writing Python.
*   **High-Scale Optimization**: Read [11-frontline-lessons-learned.md](references/community/11-frontline-lessons-learned.md) for debugging "stuck" pipelines, breaking fusion, or fixing hot keys.
*   **Python Typings**: Read [12-modern-pythonic-patterns.md](references/community/12-modern-pythonic-patterns.md) when implementing Pydantic validation and Structural Pattern Matching.
*   **Protobuf Deep Dive**: Read [13-protobuf-best-practices.md](references/community/13-protobuf-best-practices.md) for advanced schema evolution and serialization rules.
*   **Future Proofing**: Read [14-trends-and-strategic-direction.md](references/community/14-trends-and-strategic-direction.md) to understand where Beam and Dataflow are heading in 2026.

### 🐍 Core SDK & Infrastructure Docs
If the community guides don't cover it, fallback to the core documentation:
*   **Apache Beam**: Search in [references/beam/](references/beam/) for the raw programming guides, transform catalogs, and runner specifics.
*   **Google Cloud Dataflow**: Search in [references/dataflow/](references/dataflow/) for cloud-specific ops, IAM, billing, and troubleshooting.
