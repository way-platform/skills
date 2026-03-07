---
source_url: https://beam.apache.org/documentation/transforms/python/elementwise/runinference-sklearn/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "RunInference with Sklearn"
beam_last_updated: "Last updated on 2026/03/06"
---

# Use RunInference with Sklearn

|                                                                                                                                   |     |
| --------------------------------------------------------------------------------------------------------------------------------- | --- |
| [Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.ml.inference.html#apache_beam.ml.inference.RunInference) |     |

The following examples demonstrate how to to create pipelines that use the Beam RunInference API and Sklearn.

## Example 1: Sklearn unkeyed model

In this example, we create a pipeline that uses an SKlearn RunInference transform on unkeyed data.

[![](/images/code-icon.svg)](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/snippets/transforms/elementwise/runinference_sklearn_unkeyed_model_handler.py "View source code")
![](/images/copy-icon.svg)

```
import apache_beam as beam
import numpy
from apache_beam.ml.inference.base import RunInference
from apache_beam.ml.inference.sklearn_inference import ModelFileType
from apache_beam.ml.inference.sklearn_inference import SklearnModelHandlerNumpy

sklearn_model_filename = 'gs://apache-beam-samples/run_inference/five_times_table_sklearn.pkl'  # pylint: disable=line-too-long
sklearn_model_handler = SklearnModelHandlerNumpy(
    model_uri=sklearn_model_filename, model_file_type=ModelFileType.PICKLE)

unkeyed_data = numpy.array([20, 40, 60, 90],
                           dtype=numpy.float32).reshape(-1, 1)
with beam.Pipeline() as p:
  predictions = (
      p
      | "ReadInputs" >> beam.Create(unkeyed_data)
      | "RunInferenceSklearn" >>
      RunInference(model_handler=sklearn_model_handler)
      | beam.Map(print))
```

Output:

![](/images/copy-icon.svg)

```
PredictionResult(example=array([20.], dtype=float32), inference=array([100.], dtype=float32), model_id='gs://apache-beam-samples/run_inference/five_times_table_sklearn.pkl')
PredictionResult(example=array([40.], dtype=float32), inference=array([200.], dtype=float32), model_id='gs://apache-beam-samples/run_inference/five_times_table_sklearn.pkl')
PredictionResult(example=array([60.], dtype=float32), inference=array([300.], dtype=float32), model_id='gs://apache-beam-samples/run_inference/five_times_table_sklearn.pkl')
PredictionResult(example=array([90.], dtype=float32), inference=array([450.], dtype=float32), model_id='gs://apache-beam-samples/run_inference/five_times_table_sklearn.pkl')
```

## Example 2: Sklearn keyed model

In this example, we create a pipeline that uses an SKlearn RunInference transform on keyed data.

[![](/images/code-icon.svg)](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/snippets/transforms/elementwise/runinference_sklearn_keyed_model_handler.py "View source code")
![](/images/copy-icon.svg)

```
import apache_beam as beam
from apache_beam.ml.inference.base import KeyedModelHandler
from apache_beam.ml.inference.base import RunInference
from apache_beam.ml.inference.sklearn_inference import ModelFileType
from apache_beam.ml.inference.sklearn_inference import SklearnModelHandlerNumpy

sklearn_model_filename = 'gs://apache-beam-samples/run_inference/five_times_table_sklearn.pkl'  # pylint: disable=line-too-long
sklearn_model_handler = KeyedModelHandler(
    SklearnModelHandlerNumpy(
        model_uri=sklearn_model_filename,
        model_file_type=ModelFileType.PICKLE))

keyed_data = [("first_question", 105.00), ("second_question", 108.00),
              ("third_question", 1000.00), ("fourth_question", 1013.00)]

with beam.Pipeline() as p:
  predictions = (
      p
      | "ReadInputs" >> beam.Create(keyed_data)
      | "ConvertDataToList" >> beam.Map(lambda x: (x[0], [x[1]]))
      | "RunInferenceSklearn" >>
      RunInference(model_handler=sklearn_model_handler)
      | beam.Map(print))
```

Output:

![](/images/copy-icon.svg)

```
('first_question', PredictionResult(example=[105.0], inference=array([525.]), model_id='gs://apache-beam-samples/run_inference/five_times_table_sklearn.pkl'))
('second_question', PredictionResult(example=[108.0], inference=array([540.]), model_id='gs://apache-beam-samples/run_inference/five_times_table_sklearn.pkl'))
('third_question', PredictionResult(example=[1000.0], inference=array([5000.]), model_id='gs://apache-beam-samples/run_inference/five_times_table_sklearn.pkl'))
('fourth_question', PredictionResult(example=[1013.0], inference=array([5065.]), model_id='gs://apache-beam-samples/run_inference/five_times_table_sklearn.pkl'))
```
