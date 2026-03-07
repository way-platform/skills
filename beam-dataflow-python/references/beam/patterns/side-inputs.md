---
source_url: https://beam.apache.org/documentation/patterns/side-inputs/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Side input patterns"
beam_last_updated: "Last updated on 2026/03/06"
---

# Side input patterns

The samples on this page show you common Beam side input patterns. A side input is an additional input that your `DoFn` can access each time it processes an element in the input `PCollection`. For more information, see the [programming guide section on side inputs](/documentation/programming-guide/#side-inputs).

If you are trying to enrich your data by doing a key-value lookup to a remote service, you may first want to consider the [Enrichment transform](https://beam.apache.org/documentation/transforms/python/elementwise/enrichment/) which can abstract away some of the details of side inputs and provide additional benefits like client-side throttling.

## Slowly updating global window side inputs

You can retrieve side inputs from global windows to use them in a pipeline job with non-global windows, like a `FixedWindow`.

To slowly update global window side inputs in pipelines with non-global windows:

1. Write a `DoFn` that periodically pulls data from a bounded source into a global window.

   a. Use the `GenerateSequence` source transform to periodically emit a value.

   b. Instantiate a data-driven trigger that activates on each element and pulls data from a bounded source.

   c. Fire the trigger to pass the data into the global window.

2. Create the side input for downstream transforms. The side input should fit into memory.

The global window side input triggers on processing time, so the main pipeline non-deterministically matches the side input to elements in event time.

For instance, the following code sample uses a `Map` to create a `DoFn`. The `Map` becomes a `View.asSingleton` side input thatâs rebuilt on each counter tick. The side input updates every 5 seconds in order to demonstrate the workflow. In a real-world scenario, the side input would typically update every few hours or once per day.

![](/images/copy-icon.svg)

```
No sample present.
```

## Slowly updating side input using windowing

You can read side input data periodically into distinct PCollection windows.
When you apply the side input to your main input, each main input
window is automatically matched to a single side input window.
This guarantees consistency on the duration of the single window,
meaning that each window on the main input will be matched to a single
version of side input data.

To read side input data periodically into distinct PCollection windows:

1. Use the PeriodicImpulse or PeriodicSequence PTransform to:
   - Generate an infinite sequence of elements at required processing time
     intervals
   - Assign them to separate windows.
2. Fetch data using SDF Read or ReadAll PTransform triggered by arrival of
   PCollection element.
3. Apply the side input.

![](/images/copy-icon.svg)

```
from apache_beam.transforms.periodicsequence import PeriodicImpulse
from apache_beam.transforms.window import TimestampedValue
from apache_beam.transforms import window

# from apache_beam.utils.timestamp import MAX_TIMESTAMP
# last_timestamp = MAX_TIMESTAMP to go on indefninitely

# Any user-defined function.
# cross join is used as an example.
def cross_join(left, rights):
  for x in rights:
    yield (left, x)

# Create pipeline.
pipeline = beam.Pipeline()
side_input = (
    pipeline
    | 'PeriodicImpulse' >> PeriodicImpulse(
        first_timestamp, last_timestamp, interval, True)
    | 'MapToFileName' >> beam.Map(lambda x: src_file_pattern + str(x))
    | 'ReadFromFile' >> beam.io.ReadAllFromText())

main_input = (
    pipeline
    | 'MpImpulse' >> beam.Create(sample_main_input_elements)
    |
    'MapMpToTimestamped' >> beam.Map(lambda src: TimestampedValue(src, src))
    | 'WindowMpInto' >> beam.WindowInto(
        window.FixedWindows(main_input_windowing_interval)))

result = (
    main_input
    | 'ApplyCrossJoin' >> beam.FlatMap(
        cross_join, rights=beam.pvalue.AsIter(side_input)))
```
