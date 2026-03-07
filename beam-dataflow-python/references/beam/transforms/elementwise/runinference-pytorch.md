---
source_url: https://beam.apache.org/documentation/transforms/python/elementwise/runinference-pytorch/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "RunInference with PyTorch"
beam_last_updated: "Last updated on 2026/03/06"
---

# Use RunInference with PyTorch

|                                                                                                                                   |     |
| --------------------------------------------------------------------------------------------------------------------------------- | --- |
| [Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.ml.inference.html#apache_beam.ml.inference.RunInference) |     |

The following examples demonstrate how to create pipelines that use the Beam RunInference API and PyTorch.

## Example 1: PyTorch unkeyed model

In this example, we create a pipeline that uses a PyTorch RunInference transform on unkeyed data.

[![](/images/code-icon.svg)](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/snippets/transforms/elementwise/runinference.py "View source code")
![](/images/copy-icon.svg)

```
import apache_beam as beam
import numpy
import torch
from apache_beam.ml.inference.base import RunInference
from apache_beam.ml.inference.pytorch_inference import PytorchModelHandlerTensor

model_state_dict_path = 'gs://apache-beam-samples/run_inference/five_times_table_torch.pt'  # pylint: disable=line-too-long
model_class = LinearRegression
model_params = {'input_dim': 1, 'output_dim': 1}
model_handler = PytorchModelHandlerTensor(
    model_class=model_class,
    model_params=model_params,
    state_dict_path=model_state_dict_path)

unkeyed_data = numpy.array([10, 40, 60, 90],
                           dtype=numpy.float32).reshape(-1, 1)

with beam.Pipeline() as p:
  predictions = (
      p
      | 'InputData' >> beam.Create(unkeyed_data)
      | 'ConvertNumpyToTensor' >> beam.Map(torch.Tensor)
      | 'PytorchRunInference' >> RunInference(model_handler=model_handler)
      | beam.Map(print))
```

Output:

![](/images/copy-icon.svg)

```
PredictionResult(example=tensor([10.]), inference=tensor([52.2325]), model_id='gs://apache-beam-samples/run_inference/five_times_table_torch.pt')
PredictionResult(example=tensor([40.]), inference=tensor([201.1165]), model_id='gs://apache-beam-samples/run_inference/five_times_table_torch.pt')
PredictionResult(example=tensor([60.]), inference=tensor([300.3724]), model_id='gs://apache-beam-samples/run_inference/five_times_table_torch.pt')
PredictionResult(example=tensor([90.]), inference=tensor([449.2563]), model_id='gs://apache-beam-samples/run_inference/five_times_table_torch.pt')
```

## Example 2: PyTorch keyed model

In this example, we create a pipeline that uses a PyTorch RunInference transform on keyed data.

[![](/images/code-icon.svg)](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/snippets/transforms/elementwise/runinference.py "View source code")
![](/images/copy-icon.svg)

```
import apache_beam as beam
import torch
from apache_beam.ml.inference.base import KeyedModelHandler
from apache_beam.ml.inference.base import RunInference
from apache_beam.ml.inference.pytorch_inference import PytorchModelHandlerTensor

model_state_dict_path = 'gs://apache-beam-samples/run_inference/five_times_table_torch.pt'  # pylint: disable=line-too-long
model_class = LinearRegression
model_params = {'input_dim': 1, 'output_dim': 1}
keyed_model_handler = KeyedModelHandler(
    PytorchModelHandlerTensor(
        model_class=model_class,
        model_params=model_params,
        state_dict_path=model_state_dict_path))

keyed_data = [("first_question", 105.00), ("second_question", 108.00),
              ("third_question", 1000.00), ("fourth_question", 1013.00)]

with beam.Pipeline() as p:
  predictions = (
      p
      | 'KeyedInputData' >> beam.Create(keyed_data)
      | "ConvertIntToTensor" >>
      beam.Map(lambda x: (x[0], torch.Tensor([x[1]])))
      | 'PytorchRunInference' >>
      RunInference(model_handler=keyed_model_handler)
      | beam.Map(print))
```

Output:

![](/images/copy-icon.svg)

```
('first_question', PredictionResult(example=tensor([105.]), inference=tensor([523.6982]), model_id='gs://apache-beam-samples/run_inference/five_times_table_torch.pt'))
('second_question', PredictionResult(example=tensor([108.]), inference=tensor([538.5867]), model_id='gs://apache-beam-samples/run_inference/five_times_table_torch.pt'))
('third_question', PredictionResult(example=tensor([1000.]), inference=tensor([4965.4019]), model_id='gs://apache-beam-samples/run_inference/five_times_table_torch.pt'))
('fourth_question', PredictionResult(example=tensor([1013.]), inference=tensor([5029.9180]), model_id='gs://apache-beam-samples/run_inference/five_times_table_torch.pt'))
```
