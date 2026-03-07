---
source_url: https://docs.cloud.google.com/dataflow/docs/use-cases
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Use cases for Dataflow \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2025-06-05 UTC."
---

## Dataflow use cases

![](https://docs.cloud.google.com/static/dataflow/images/ml-landing01.png)

Dataflow is designed to support streaming and batch pipelines at large scale. Dataflow is built on the open-source Apache Beam framework.

This page links to tutorials and example use cases to help you get started.

[About Dataflow](https://docs.cloud.google.com/dataflow/docs/overview)
[About Apache Beam](https://docs.cloud.google.com/dataflow/docs/concepts/beam-programming-model)

## Data movement

### [Process data from Kafka to BigQuery](https://docs.cloud.google.com/dataflow/docs/kafka-dataflow)

This tutorial shows how to run a Dataflow template that reads from Managed Service for Apache Kafka and writes the records to a BigQuery table.

### [Process data from Pub/Sub to BigQuery](https://docs.cloud.google.com/dataflow/docs/tutorials/dataflow-stream-to-bigquery)

This tutorial shows how to run a Dataflow template that reads JSON-encoded messages from Pub/Sub and writes them to a BigQuery table.

## Dataflow ML

### [Use RunInference and Embeddings](https://docs.cloud.google.com/dataflow/docs/notebooks/run_inference_huggingface)

This notebook shows how to use ML models in Apache Beam pipelines that use the RunInference transform.

### [Use GPUs in your pipeline](https://docs.cloud.google.com/dataflow/docs/notebooks/run_inference_vllm)

This notebook shows how to run machine learning inference by using vLLM and GPUs. vLLM is a library for LLM inference and serving.

## Other resources

### [Reference patterns](https://docs.cloud.google.com/dataflow/docs/tutorials/reference-patterns)

Links to sample code and technical reference guides for common Dataflow use cases.

### [Ecommerce streaming pipeline](https://docs.cloud.google.com/dataflow/docs/tutorials/ecommerce-retail-pipeline)

In this tutorial, you create a pipeline that transforms ecommerce data from Pub/Sub and outputs the data to BigQuery and Bigtable.

### [HPC highly parallel workloads](https://docs.cloud.google.com/dataflow/docs/hpc-ep)

With Dataflow, you can run highly parallel workloads in a single pipeline, improving efficiency and making your workflow easier to manage.
