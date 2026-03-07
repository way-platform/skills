---
name: beam-dataflow-python
description: Expertise in Apache Beam (Python SDK) and Google Cloud Dataflow. Use when creating, debugging, optimizing, or reviewing Python-based data pipelines. Critical for tasks involving unified batch/streaming architectures, Protobuf serialization, Docker/Flex Templates, windowing/triggers, stateful processing, or operational reliability on Google Cloud.
---

# Apache Beam & Dataflow (Python) Best Practices

Implement Way's architectural patterns and modern (2025+) best practices when building
Dataflow Python pipelines.

## 1. Unified Pipeline Architecture

- **Mode-driven routing**: `--mode streaming` vs `--mode batch` flag conditionally
  injects I/O connectors (Pub/Sub vs. BigQuery/GCS) and windowing; transform logic
  is identical across modes
- **Layered files**: `pipeline.py` (PTransform wiring) → `transforms.py` (DoFn impls)
  → `state_machine.py` / domain logic (pure Python, zero Beam imports)
- **Event-time first**: always develop around event time so backfills produce consistent
  state

**Reference**: [Way's Pipeline Patterns](references/key-topics.md),
[Community Best Practices](references/community/key-topics.md)

## 2. Runner v2 + Streaming Engine

Runner v2 is mandatory for Python SDK 2.45.0+; Streaming Engine is required for
Runner v2 streaming jobs.

- **Always set these flags** for streaming:
  ```
  --experiments=use_runner_v2
  --enable_streaming_engine
  ```
- Streaming Engine offloads state/timer storage to Google-managed backend → reduces
  worker memory pressure and enables finer-grained autoscaling
- Runner v2 also unlocks vertical autoscaling, C4A (ARM) workers, and cross-language
  transforms

**Reference**: [runner-v2.md](references/dataflow/deep-dives/runner-v2.md),
[streaming-engine.md](references/dataflow/deep-dives/streaming-engine.md)

## 3. Deployment: Docker + Flex Templates

`setup.py` is deprecated as of 2025. Docker is the only supported production
deployment pattern.

- **Flex Template Dockerfile is two-stage** — the launcher base and SDK are separate
  images; copy the SDK into the launcher base:
  ```dockerfile
  FROM apache/beam_python3.12_sdk:VERSION AS beam-sdk
  FROM gcr.io/dataflow-templates-base/python312-template-launcher-base AS final
  COPY --from=beam-sdk /opt/apache/beam /opt/apache/beam
  RUN uv pip install --system -r requirements.txt
  ENV FLEX_TEMPLATE_PYTHON_PY_FILE="/app/main.py"
  ```
- **Use `uv pip install`** in Dockerfiles for faster dependency resolution
- **Tag with git commit SHA** — never `:latest`; enables reproducible rollbacks
- **Flex Template** = `metadata.json` in GCS pointing to the container image +
  runtime parameter definitions; launch via `gcloud dataflow flex-template run`
- Pre-baked deps → faster cold-start autoscaling (no pip install on worker boot)
- The `ENTRYPOINT` is set by the launcher base image — do not override it

**Reference**: [build-container-image.md](references/dataflow/deep-dives/build-container-image.md),
[run-custom-container.md](references/dataflow/deep-dives/run-custom-container.md),
[using-custom-containers.md](references/dataflow/deep-dives/using-custom-containers.md),
[08-docker-custom-containers-flex-templates.md](references/community/08-docker-custom-containers-flex-templates.md),
[GCP Flex Template examples](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/dataflow/flex-templates)

## 4. Data Serialization (Protobuf-first)

Protobuf is Way's canonical schema across all environments (Pub/Sub, Beam shuffles,
BigQuery, cross-language). Maximize leverage from protos in every pipeline stage.

- **Register coders explicitly** — prevents Pickle fallback, which is slow and fragile:
  ```python
  coders.registry.register_coder(MyMessage, coders.ProtoCoder)
  ```
- **Use upb C-backend** (protobuf v3.24+): `pip install protobuf>=3.24.0`; verify
  `google.protobuf.runtime_version` is `"upb"` — 3-5x faster than pure Python
- **Pub/Sub JSON ↔ proto**: use integer enums for compact wire format:
  - Decode: `json_format.Parse(json_bytes, MyMessage())`
  - Encode: `json_format.MessageToJson(msg, use_integers_for_enums=True)`
- **BigQuery mapping**: use string enums for queryability:
  - Sink: `MessageToDict(msg, preserving_proto_field_name=True, including_default_value_fields=True, use_integers_for_enums=False)`
  - Source: `ParseDict(row, MyMessage(), ignore_unknown_fields=True)`
- **TimestampedValue from proto timestamp**: inject event time from a proto
  `google.protobuf.Timestamp` field using `beam.window.TimestampedValue` +
  `Timestamp.from_rfc3339(ts.ToJsonString())`
- **2 GB per-element hard limit**: never pass large binary blobs as Beam elements;
  pass GCS URIs and load inside `DoFn.process()`
- **Avro for batch temp files**: set `temp_file_format='AVRO'` on BigQuery writes
  to save ~20% CPU vs JSON during shuffle
- **Protobuf Editions** (2023/2024 syntax): requires `protobuf>=5.27.0` on workers;
  pin this in your Dockerfile
- **Cross-language**: keep `.proto` files accessible to both Python and Java runtimes
  when using cross-language transforms

**Reference**: [13-protobuf-best-practices.md](references/community/13-protobuf-best-practices.md),
[03-bigquery-io-optimization.md](references/community/03-bigquery-io-optimization.md)

## 5. BigQuery & I/O

- **Write method depends on the pipeline mode**:
  - **Streaming / low-latency appends**: use `method='STORAGE_WRITE_API'` with
    `num_storage_api_streams=0` (auto-shard); never use legacy streaming inserts
  - **Batch / full partition replace**: use standard `WriteToBigQuery` with
    `write_disposition=WRITE_TRUNCATE` and a date-partition suffix `table$YYYYMMDD`;
    simpler, cheaper, and idempotent for full-partition overwrites
- **Managed I/O** (SDK 2.61.0+): use `beam.managed.Read` / `beam.managed.Write`
  for BigQuery, Kafka, and Iceberg — auto-upgrades connector versions without
  pipeline code changes:
  ```python
  pcoll | beam.managed.Write(beam.managed.BIGQUERY, config={...})
  ```

**Reference**: [managed-io.md](references/dataflow/deep-dives/managed-io.md),
[managed-io-bigquery.md](references/dataflow/deep-dives/managed-io-bigquery.md),
[managed-io-kafka.md](references/dataflow/deep-dives/managed-io-kafka.md),
[managed-io-iceberg.md](references/dataflow/deep-dives/managed-io-iceberg.md),
[03-bigquery-io-optimization.md](references/community/03-bigquery-io-optimization.md)

## 6. Testing & Logic Decoupling

- **Extract domain logic**: remove business logic from `DoFn`s into pure Python
  classes with zero `apache_beam` imports
- **Three-tier testing**:
  1. **Pure Python (80–90%)**: `pytest` on domain logic — instant, no runner overhead
  2. **Transform logic**: `TestPipeline` + `assert_that` for DoFn routing, State/Timer
     APIs, and side-output correctness
  3. **Integration**: local end-to-end with mock I/O using **Prism Runner** (current
     standard for high-fidelity stateful execution)

**Reference**: [01-testing-and-ci-cd.md](references/community/01-testing-and-ci-cd.md),
[Community Testing Patterns](references/community/key-topics.md#4-testing--domain-logic-decoupling)

## 7. Advanced Windowing, Triggers & PaneInfo

- **Abstract window config**: extract into configuration objects (e.g.,
  `StreamingSessionWindowConfig`) to keep pipeline code readable
- **Triggers + lateness**: pair `AfterWatermark` with explicit `allowed_lateness`;
  throttle EARLY panes with `Repeatedly(AfterProcessingTime(delay=...))` to avoid
  pane explosion
- **PaneInfo injection**: `pane_info=beam.DoFn.PaneInfoParam` in `process()` signature
  - `EARLY`: speculative aggregate — throttle output rate
  - `ON_TIME`: watermark has passed window end
  - `LATE`: correction after close — sinks must be idempotent using window bounds +
    `pane_info.index` as primary key

**Reference**: [05-windowing-and-triggers.md](references/community/05-windowing-and-triggers.md)

## 8. Stateful Processing & Thread Safety

- **State + Timer APIs**: use `ReadModifyWriteState`, `BagState`, and `TimerSpec`
  for complex per-key session logic that session windows cannot express
- **Thread safety**: streaming workers run ~12 threads per process; objects
  initialized in `__init__` are shared — initialize non-thread-safe objects
  (clients, parsers, connections) in `setup()`, not `__init__`
- **Singleton pattern for expensive clients**: use `setup()` / `teardown()` lifecycle
  hooks to manage connection pools and ML model loading

**Reference**: [09-state-and-timers.md](references/community/09-state-and-timers.md),
[thread-scaling.md](references/dataflow/deep-dives/thread-scaling.md)

## 9. Resilience & Production Gotchas

- **DLQ**: wrap transforms with `.with_exception_handling()` to route failed records
  to a dead-letter sink; never let poison pills crash the pipeline
- **Fusion trap**: Dataflow fuses adjacent steps to reduce serialization overhead,
  but fusing a CPU-heavy step with a fast step causes 3–5x throughput loss; break
  fusion with `beam.Reshuffle()` or a no-op `GroupByKey` between the steps
- **Hot key sharding**: distribute work across keys by appending a random shard
  suffix before `GroupByKey`, then strip it after aggregation
- **Exactly-once misconception**: `DoFn.process()` may execute multiple times for
  the same element (retries, speculative execution); only sinks get exactly-once
  delivery guarantees — all API calls and external writes must be idempotent
- **ML inference**: use `RunInference` transform — never load models inside
  `process()`; models must be loaded in `setup()` and shared safely

**Reference**: [02-dead-letter-queues.md](references/community/02-dead-letter-queues.md),
[11-frontline-lessons-learned.md](references/community/11-frontline-lessons-learned.md),
[machine-learning.md](references/dataflow/deep-dives/machine-learning.md)

## 10. Cost Optimization

- **Streaming Engine**: reduces per-vCPU cost by offloading state to managed backend
- **FlexRS** (batch): mix preemptible VMs with on-demand; typically 40% cost
  reduction for non-latency-sensitive batch
- **C4A (ARM) workers**: `--worker_machine_type=c4a-standard-8`; 20–30% better
  price/performance for CPU-bound transforms
- **Vertical autoscaling**: `--enable_vertical_memory_scaling`; prevents OOM without
  over-provisioning RAM across the fleet
- **Shuffle Service** (batch): `--experiments=shuffle_mode=service`; offloads
  GroupByKey shuffle to managed backend
- **`worker_utilization_hint`**: `--experiments=worker_utilization_hint=0.8`; sets
  the target CPU utilization for autoscaling decisions (0.0–1.0); tune down for
  latency-sensitive streaming, up for throughput-bound batch

**Reference**: [flexrs.md](references/dataflow/deep-dives/flexrs.md),
[use-arm-vms.md](references/dataflow/deep-dives/use-arm-vms.md),
[vertical-autoscaling.md](references/dataflow/deep-dives/vertical-autoscaling.md),
[shuffle-for-batch.md](references/dataflow/deep-dives/shuffle-for-batch.md),
[right-fitting.md](references/dataflow/deep-dives/right-fitting.md),
[optimize-costs.md](references/dataflow/admin-ops/optimize-costs.md)

---

## Agent Reference Index

Do not guess syntax or patterns. Load exact procedures from these references.

### Architecture & Core Strategy

- **[Way's Internal Patterns](references/key-topics.md)**: baseline architectural
  expectations (unified pipelines, pure-Python state machines, mode routing)
- **[2024+ Community Best Practices](references/community/key-topics.md)**: industry
  consensus (logic-first decoupling, DLQs, Managed I/O)

### Community Guides (2025+)

- **Testing & CI**: [01-testing-and-ci-cd.md](references/community/01-testing-and-ci-cd.md)
  — `TestStream`, PrismRunner, CI/CD setup
- **Error Handling**: [02-dead-letter-queues.md](references/community/02-dead-letter-queues.md)
  — `with_exception_handling`, side-output DLQ patterns
- **BigQuery I/O**: [03-bigquery-io-optimization.md](references/community/03-bigquery-io-optimization.md)
  — Storage Write API syntax, schema mapping
- **Autoscaling**: [04-autoscaling-resource-management.md](references/community/04-autoscaling-resource-management.md)
  — C4A workers, vertical autoscaling, FlexRS config
- **Windowing**: [05-windowing-and-triggers.md](references/community/05-windowing-and-triggers.md)
  — event-time windows, triggers, `allowed_lateness`
- **Cross-language**: [06-cross-language-transforms.md](references/community/06-cross-language-transforms.md)
  — Java connectors (KafkaIO) from Python
- **DataFrames**: [07-dataframe-api.md](references/community/07-dataframe-api.md)
  — scalar/tabular operations with DataFrame API
- **Docker/Flex Templates**: [08-docker-custom-containers-flex-templates.md](references/community/08-docker-custom-containers-flex-templates.md)
  — Dockerfile patterns, metadata.json, launch commands
- **Stateful Logic**: [09-state-and-timers.md](references/community/09-state-and-timers.md)
  — State + Timer APIs, session management
- **Beam YAML**: [10-beam-yaml-declarative.md](references/community/10-beam-yaml-declarative.md)
  — no-code ingestion routing
- **Scale Debugging**: [11-frontline-lessons-learned.md](references/community/11-frontline-lessons-learned.md)
  — stuck pipelines, fusion breaking, hot keys
- **Pythonic Patterns**: [12-modern-pythonic-patterns.md](references/community/12-modern-pythonic-patterns.md)
  — Pydantic validation, structural pattern matching
- **Protobuf Deep Dive**: [13-protobuf-best-practices.md](references/community/13-protobuf-best-practices.md)
  — schema evolution, upb backend, coder registration, Editions
- **Strategic Direction**: [14-trends-and-strategic-direction.md](references/community/14-trends-and-strategic-direction.md)
  — Beam/Dataflow roadmap for 2026

### Dataflow Deep-Dives

- **Runner v2**: [runner-v2.md](references/dataflow/deep-dives/runner-v2.md)
- **Streaming Engine**: [streaming-engine.md](references/dataflow/deep-dives/streaming-engine.md)
- **Vertical Autoscaling**: [vertical-autoscaling.md](references/dataflow/deep-dives/vertical-autoscaling.md)
- **Horizontal Autoscaling**: [horizontal-autoscaling.md](references/dataflow/deep-dives/horizontal-autoscaling.md)
- **Build Container Image**: [build-container-image.md](references/dataflow/deep-dives/build-container-image.md)
- **Run Custom Container**: [run-custom-container.md](references/dataflow/deep-dives/run-custom-container.md)
- **Using Custom Containers**: [using-custom-containers.md](references/dataflow/deep-dives/using-custom-containers.md)
- **Managed I/O**: [managed-io.md](references/dataflow/deep-dives/managed-io.md)
- **Managed I/O — BigQuery**: [managed-io-bigquery.md](references/dataflow/deep-dives/managed-io-bigquery.md)
- **Managed I/O — Kafka**: [managed-io-kafka.md](references/dataflow/deep-dives/managed-io-kafka.md)
- **Managed I/O — Iceberg**: [managed-io-iceberg.md](references/dataflow/deep-dives/managed-io-iceberg.md)
- **Shuffle for Batch**: [shuffle-for-batch.md](references/dataflow/deep-dives/shuffle-for-batch.md)
- **Thread Scaling**: [thread-scaling.md](references/dataflow/deep-dives/thread-scaling.md)
- **FlexRS**: [flexrs.md](references/dataflow/deep-dives/flexrs.md)
- **ARM VMs**: [use-arm-vms.md](references/dataflow/deep-dives/use-arm-vms.md)
- **Right-Fitting**: [right-fitting.md](references/dataflow/deep-dives/right-fitting.md)
- **ML / RunInference**: [machine-learning.md](references/dataflow/deep-dives/machine-learning.md)

### Dataflow Operations & Troubleshooting

- **Monitoring**: [monitoring-overview.md](references/dataflow/admin-ops/monitoring-overview.md)
- **Cost Optimization**: [optimize-costs.md](references/dataflow/admin-ops/optimize-costs.md)
- **Logging**: [logging.md](references/dataflow/admin-ops/logging.md)
- **Common Errors**: [common-errors.md](references/dataflow/troubleshooting/common-errors.md)
- **Slow Jobs**: [troubleshoot-slow-jobs.md](references/dataflow/troubleshooting/troubleshoot-slow-jobs.md)
- **Bottlenecks**: [troubleshoot-bottlenecks.md](references/dataflow/troubleshooting/troubleshoot-bottlenecks.md)
- **OOM**: [troubleshoot-oom.md](references/dataflow/troubleshooting/troubleshoot-oom.md)
- **Streaming Stragglers**: [troubleshoot-streaming-stragglers.md](references/dataflow/troubleshooting/troubleshoot-streaming-stragglers.md)
- **Custom Container Issues**: [troubleshoot-custom-container.md](references/dataflow/troubleshooting/troubleshoot-custom-container.md)
- **Autoscaling Issues**: [troubleshoot-autoscaling.md](references/dataflow/troubleshooting/troubleshoot-autoscaling.md)

### Core SDK Fallback References

- **Apache Beam SDK**: [references/beam/](references/beam/) — programming guides,
  transform catalogs, runner specifics
- **Google Cloud Dataflow**: [references/dataflow/](references/dataflow/) — cloud ops,
  IAM, billing, troubleshooting
