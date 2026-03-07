# Dataflow Python: Windowing and Triggers

Streaming data is infinite, but aggregations (like sums or averages) require finite boundaries. This is where Windowing and Triggers come in.

## Best Practices for Windowing
1.  **Understand Your Data Profile:**
    *   *Fixed Windows:* Good for predictable, regular aggregations (e.g., "sales per hour").
    *   *Sliding Windows:* Good for moving averages (e.g., "server load over the last 5 minutes, updated every minute").
    *   *Session Windows:* Ideal for user behavior tracking (e.g., "group clicks until 30 minutes of inactivity").
2.  **Always Set Allowed Lateness:** By default, data arriving after the watermark passes the window boundary is discarded. Explicitly configure `allowed_lateness` to handle delayed events.

## Triggers
Triggers dictate *when* to emit results for a window.
*   **Early Firings:** Emit speculative results before the window closes. Useful for live dashboards.
*   **Late Firings:** Emit updated results when late data arrives.

```python
import apache_beam.window as window

# Example: Hourly window, updating every 5 minutes (early), 
# and updating when late data arrives up to 2 days later.
events | beam.WindowInto(
    window.FixedWindows(60 * 60),  # 1 hour
    trigger=window.AfterWatermark(
        early=window.AfterProcessingTime(5 * 60), # 5 mins
        late=window.AfterCount(1)),               # Every late element
    accumulation_mode=window.AccumulationMode.ACCUMULATING,
    allowed_lateness=window.Duration(2 * 24 * 60 * 60) # 2 days
)
```

## References & Further Reading
*   [Apache Beam: Windowing](https://beam.apache.org/documentation/programming-guide/#windowing)
*   [Apache Beam: Triggers](https://beam.apache.org/documentation/programming-guide/#triggers)
