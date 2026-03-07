# Community Best Practices: Apache Beam (Python) 2024+

This document synthesizes current (2024-2025) community advice, architectural patterns, and best practices for developing Apache Beam Python pipelines. It maps closely to our specific data processing patterns (such as Protobuf, unified architectures, and domain decoupling).

## 1. Unified Streaming & Batch Architecture

The community emphasizes a "unified-first" architecture where the distinction between batch and streaming is minimized. Batch is treated simply as a bounded stream.

*   **Layered Architecture:** The standard for robust projects is to cleanly separate layers:
    *   **Domain Layer:** Pure business logic and decoupled transformations.
    *   **Infrastructure Layer:** Handles I/O bounds (e.g., Pub/Sub vs. GCS vs. BigQuery).
    *   **Application Layer:** The `pipeline.py` script that glues components based on CLI arguments (e.g., `--mode streaming`).
*   **Event-Time First:** Always develop logic against *event time*, rather than processing time, guaranteeing that bounded backfills produce the exact same data states as live streams. ([Source: Unified Batch and Streaming Data Processing with Apache Beam](https://plainenglish.io/blog/unified-batch-and-streaming-data-processing-with-apache-beam-a-hands-on-guide))
*   **Routing and Error Handling:** The standard pattern is to use the `with_exception_handling` method to route bad inputs (e.g., invalid JSON payloads or unexpected schemas) into a Dead-Letter Queue (DLQ). This ensures one bad event doesn't stall a streaming job indefinitely or crash a batch run.

## 2. Protobuf & BigQuery Integration

When working with complex serialization requirements like Protobuf in Python:

*   **`ProtoCoder` Reigns Supreme:** For custom Python operations, explicitly registering `coders.registry.register_coder(MyProto, coders.ProtoCoder)` is still the most performant and reliable approach to handling Protobuf across the shuffle phase.
*   **BigQuery Storage Write API:** The community recommends moving away from the old `insertAll` (streaming inserts) API towards the `STORAGE_WRITE_API` for streaming ingestion. It offers lower latency, higher throughput, and native Protobuf support under the hood. ([Source: Beam Programming Guide - BigQuery](https://beam.apache.org/documentation/io/built-in/google-bigquery/))
*   **Type Management Nuances:**
    *   *Enums*: A common recommendation is to cast Protobuf `Enums` to Strings before sinking them into BigQuery to ensure downstream analytics don't break if the integer values change over time.
    *   *Dynamic fields*: If dealing with `google.protobuf.Struct` or arbitrary nested data, write to a BigQuery `JSON` column rather than flattening it.

## 3. Advanced Windowing & PaneInfo Handling

When utilizing streaming windows with `AfterWatermark` triggers and allowed lateness, tracking pane state (`PaneInfo`) is crucial.

*   **Pane Timings (`Timing.EARLY`, `ON_TIME`, `LATE`):** Inside a `DoFn` via `pane_info=beam.DoFn.PaneInfoParam`, checking `pane_info.timing` lets you differentiate:
    *   `EARLY`: Speculative results (useful to feed fast, incomplete dashboards).
    *   `ON_TIME`: The watermark has passed the window end.
    *   `LATE`: Corrections arriving after the window closed.
*   **Avoiding Pane Explosions:** A common pitfall in production pipelines is emitting a pane on every single arriving element. Always throttle early firings (e.g., `Repeatedly(AfterProcessingTime(delay=...))`). ([Source: Windowing and Triggers in Dataflow](https://medium.com/@kiran.d.anvekar/dataflow-concept-windowing-and-triggers-e8df99178bf7))
*   **Downstream Idempotency:** Because `LATE` panes arrive asynchronously long after the `ON_TIME` pane, your sinks must be capable of idempotency. Use the window boundary alongside `pane_info.index` as a unique primary key to upsert results in your target datastore.

## 4. Testing & Domain Logic Decoupling

The modern Beam testing philosophy is **"Logic-First Decoupling."** Testing a full `TestPipeline` is inherently slow, so the community stresses abstracting complex logic outside of Beam entirely.

*   **Pure Python State Machines & Functions:** Extract complex rules (like session chunking, state tracking, and mathematical aggregations) into plain Python classes or functions. *These files should contain no `import apache_beam` statements.* ([Source: Decoupling Data Processing from Apache Beam](https://whiteowleducation.com/apache-beam-decoupling-data-processing/))
*   **Multi-Tiered Testing Strategy:**
    1.  **Unit Tests (Pure Python):** Use `pytest` on the plain Python logic. These should make up 80-90% of your tests, catching edge cases instantly without Beam overhead.
    2.  **Transform Tests (DoFn):** Use `TestPipeline` and `assert_that` solely to verify that your `DoFn` yields the correct outputs from the decoupled logic or correctly manages `State` and `Timer` APIs.
    3.  **Integration Tests:** End-to-end testing with mock IOs.
*   **Mocking API Calls:** Never embed direct API calls inside a `process()` loop without wrapping them in an injected or mockable client to ensure clean transform tests.
*   **Prism Runner:** When executing local tests that rely heavily on streaming features (like timers, state, or complex windowing triggers), the new *Prism Runner* provides much higher fidelity than the older DirectRunner.