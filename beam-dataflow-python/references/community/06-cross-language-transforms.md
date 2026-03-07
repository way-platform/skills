# Dataflow Python: Cross-Language Transforms

The Python SDK does not have native connectors for every possible system. Modern Apache Beam (2025+) heavily utilizes **Cross-Language Transforms (Xlang)** to borrow robust Java connectors directly into Python pipelines.

## How It Works
Xlang uses an expansion service (often a Docker container running Java) that takes a Python definition, expands it into the underlying Java graph, and executes it seamlessly on Dataflow.

## Primary Use Cases
*   **Kafka I/O:** The Java Kafka connector is significantly more mature than Python alternatives. Use `ReadFromKafka` via Xlang.
*   **Spanner I/O:** High-performance writes to Cloud Spanner.
*   **Beam SQL:** Execute standard SQL queries on `PCollection`s within your Python code using the Java SQL execution engine.

## Best Practices
1.  **Manage Dependencies:** You must have Java installed in your environment to run the Expansion Service during pipeline construction.
2.  **Use `beam.Row`:** Xlang relies heavily on Beam Schemas. Convert your Python dictionaries or objects to `beam.Row` before passing them to a Java transform.
3.  **Monitor Expansion Service:** If pipeline submission is slow, check the expansion service logs; it may be downloading large JAR files on the first run.

## References & Further Reading
*   [Apache Beam: Multi-language Pipelines](https://beam.apache.org/documentation/programming-guide/#multi-language-pipelines)
*   [Google Cloud: Building Multi-language Pipelines on Dataflow](https://cloud.google.com/dataflow/docs/guides/multi-language-pipelines)
