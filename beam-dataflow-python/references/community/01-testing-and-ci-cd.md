# Dataflow Python: Testing & CI/CD Best Practices (2025+)

Testing Apache Beam pipelines requires a multi-layered approach to ensure reliability before deploying to Google Cloud Dataflow. Modern best practices emphasize shifting left, using high-fidelity local runners, and modularizing transformations.

## Core Principles
1.  **Do Not Test Standard I/O:** Trust that built-in connectors (e.g., `ReadFromBigQuery`, `WriteToPubSub`) work. Focus tests on your custom business logic.
2.  **Modularize `DoFn`s:** Keep your transformations small, focused, and free of inline lambda functions. This makes unit testing straightforward.

## The Testing Pyramid
*   **Unit Tests (Prism Runner):** As of early 2026, the **Prism Runner** has replaced the legacy DirectRunner as the default local execution engine for Python. It offers high-fidelity emulation of distributed runners, including better support for cross-language transforms.
*   **Integration Tests (`TestStream`):** For streaming logic, use `TestStream` to simulate event time, advance watermarks manually, and test windowing/triggers without needing a real message broker.
*   **End-to-End (E2E) Smoke Tests (`DataflowRunner`):** Run a small subset of real data through the actual Dataflow infrastructure as part of your CI/CD pipeline.

## Example: Using `assert_that`
Always use `apache_beam.testing.util.assert_that` to verify pipeline outputs.
```python
import unittest
import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to

class ProcessDataTest(unittest.TestCase):
    def test_processing_logic(self):
        with TestPipeline() as p:
            input_data = [1, 2, 3]
            expected = [2, 4, 6]
            
            output = p | beam.Create(input_data) | beam.Map(lambda x: x * 2)
            assert_that(output, equal_to(expected))
```

## References & Further Reading
*   [Apache Beam Testing Guide](https://beam.apache.org/documentation/pipelines/test-your-pipeline/)
*   [Google Cloud: Building CI/CD pipelines for Dataflow](https://cloud.google.com/architecture/cicd-pipeline-for-data-processing)
