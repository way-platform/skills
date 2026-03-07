---
source_url: https://beam.apache.org/documentation/patterns/pipeline-options/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Pipeline option patterns"
beam_last_updated: "Last updated on 2026/03/06"
---

# Pipeline option patterns

The samples on this page show you common pipeline configurations. For more information about pipeline configuration options, see [Creating a pipeline](/documentation/programming-guide/#creating-a-pipeline) and [Configuring pipeline options](/documentation/programming-guide/#configuring-pipeline-options).

## Retroactively logging runtime parameters

Use the `ValueProvider` interface to access runtime parameters after completing a pipeline job.

You can use the `ValueProvider` interface to pass runtime parameters to your pipeline, but you can only log the parameters from within the Beam DAG. A solution is to add a pipeline [branch](/documentation/programming-guide/#applying-transforms) with a `DoFn` that processes a placeholder value and then logs the runtime parameters:

![](/images/copy-icon.svg)

```
import logging

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.value_provider import RuntimeValueProvider

class MyOptions(PipelineOptions):
  @classmethod
  def _add_argparse_args(cls, parser):
    parser.add_value_provider_argument('--string_value', type=str)

class LogValueProvidersFn(beam.DoFn):
  def __init__(self, string_vp):
    self.string_vp = string_vp

  # Define the DoFn that logs the ValueProvider value.
  # The DoFn is called when creating the pipeline branch.
  # This example logs the ValueProvider value, but
  # you could store it by pushing it to an external database.
  def process(self, an_int):
    logging.info('The string_value is %s' % self.string_vp.get())
    # Another option (where you don't need to pass the value at all) is:
    logging.info(
        'The string value is %s' %
        RuntimeValueProvider.get_value('string_value', str, ''))

beam_options = PipelineOptions()
args = beam_options.view_as(MyOptions)

# Create pipeline.
with beam.Pipeline(options=beam_options) as pipeline:

  # Add a branch for logging the ValueProvider value.
  _ = (
      pipeline
      | beam.Create([None])
      | 'LogValueProvs' >> beam.ParDo(LogValueProvidersFn(args.string_value)))

  # The main pipeline.
  result_pc = (
      pipeline
      | "main_pc" >> beam.Create([1, 2, 3])
      | beam.CombineGlobally(sum))
```
