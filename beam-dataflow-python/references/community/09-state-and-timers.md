# Dataflow Python: State and Timers

For advanced streaming use cases where standard windowing isn't enough, Beam provides a low-level API: **State and Timers**.

## Concepts
*   **State:** Allows a `DoFn` to store data across multiple elements for a specific key (e.g., keeping a running total, or buffering elements).
*   **Timers:** Allows a `DoFn` to schedule a callback at a specific time (Processing Time or Event Time) to take action (e.g., flushing a buffer).

## Best Practices
1.  **Always Key Your Data:** State and Timers operate *strictly on a per-key and per-window basis*. You must have a `KV` (Key-Value) PCollection before applying a stateful `DoFn`.
2.  **Manage State Size:** Do not store unbounded amounts of data in State. Use Timers to periodically clear or output state, preventing memory exhaustion on the worker nodes.
3.  **Enable Streaming Engine:** Stateful processing is heavily optimized when using the Dataflow Streaming Engine, as it moves state storage off the worker VMs to a managed backend.

```python
from apache_beam.transforms.userstate import BagStateSpec, TimerSpec
from apache_beam.transforms.timeutil import TimeDomain

class BufferAndFlush(beam.DoFn):
    # Define State and Timer
    BUFFER = BagStateSpec('buffer', beam.coders.PickleCoder())
    FLUSH_TIMER = TimerSpec('flush_timer', TimeDomain.PROCESSING_TIME)

    def process(self, element, buffer=beam.DoFn.StateParam(BUFFER), timer=beam.DoFn.TimerParam(FLUSH_TIMER)):
        buffer.add(element)
        # Set timer to flush in 1 minute
        timer.set(beam.window.Timestamp.now() + 60)

    @beam.on_timer(FLUSH_TIMER)
    def on_flush(self, buffer=beam.DoFn.StateParam(BUFFER)):
        items = list(buffer.read())
        buffer.clear()
        yield items
```

## References & Further Reading
*   [Apache Beam: State and Timers Guide](https://beam.apache.org/documentation/programming-guide/#state-and-timers)
*   [Beam Blog: Stateful processing with Apache Beam](https://beam.apache.org/blog/stateful-processing/)
