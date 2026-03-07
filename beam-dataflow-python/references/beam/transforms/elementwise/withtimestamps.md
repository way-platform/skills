---
source_url: https://beam.apache.org/documentation/transforms/python/elementwise/withtimestamps/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "WithTimestamps"
beam_last_updated: "Last updated on 2026/03/06"
---

# WithTimestamps

Assigns timestamps to all the elements of a collection.

## Examples

In the following examples, we create a pipeline with a `PCollection` and attach a timestamp value to each of its elements.
When windowing and late data play an important role in streaming pipelines, timestamps are especially useful.

### Example 1: Timestamp by event time

The elements themselves often already contain a timestamp field.
`beam.window.TimestampedValue` takes a value and a
[Unix timestamp](https://en.wikipedia.org/wiki/Unix_time)
in the form of seconds.

To convert from a
[`time.struct_time`](https://docs.python.org/3/library/time.html#time.struct_time)
to `unix_time` you can use
[`time.mktime`](https://docs.python.org/3/library/time.html#time.mktime).
For more information on time formatting options, see
[`time.strftime`](https://docs.python.org/3/library/time.html#time.strftime).

![](/images/copy-icon.svg)

```
import time

time_tuple = time.strptime('2020-03-19 20:50:00', '%Y-%m-%d %H:%M:%S')
unix_time = time.mktime(time_tuple)
```

To convert from a
[`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime)
to `unix_time` you can use convert it to a `time.struct_time` first with
[`datetime.timetuple`](https://docs.python.org/3/library/datetime.html#datetime.datetime.timetuple).

![](/images/copy-icon.svg)

```
import time
import datetime

now = datetime.datetime.now()
time_tuple = now.timetuple()
unix_time = time.mktime(time_tuple)
```

### Example 2: Timestamp by logical clock

If each element has a chronological number, these numbers can be used as a
[logical clock](https://en.wikipedia.org/wiki/Logical_clock).
These numbers have to be converted to a _“seconds”_ equivalent, which can be especially important depending on your windowing and late data rules.

### Example 3: Timestamp by processing time

If the elements do not have any time data available, you can also use the current processing time for each element.
Note that this grabs the local time of the _worker_ that is processing each element.
Workers might have time deltas, so using this method is not a reliable way to do precise ordering.

By using processing time, there is no way of knowing if data is arriving late because the timestamp is attached when the element _enters_ into the pipeline.

## Related transforms

- [Reify](/documentation/transforms/python/elementwise/reify) converts between explicit and implicit forms of Beam values.
