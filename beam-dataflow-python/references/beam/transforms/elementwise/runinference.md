---
source_url: https://beam.apache.org/documentation/transforms/python/elementwise/runinference/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "RunInference"
beam_last_updated: "Last updated on 2026/03/06"
---

# RunInference

|                                                                                                                                             |     |
| ------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| [Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.ml.inference.base.html#apache_beam.ml.inference.base.RunInference) |     |

Uses models to do local and remote inference. A `RunInference` transform performs inference on a `PCollection` of examples using a machine learning (ML) model. The transform outputs a `PCollection` that contains the input examples and output predictions. Avaliable in Apache Beam 2.40.0 and later versions.

For more information about Beam RunInference APIs, see the [About Beam ML](https://beam.apache.org/documentation/ml/about-ml) page and the [RunInference API pipeline](https://github.com/apache/beam/tree/master/sdks/python/apache_beam/examples/inference) examples.

## Examples

The following examples show how to create pipelines that use the Beam RunInference API to make predictions based on models.

| Framework | Example                                                                                                                     |
| --------- | --------------------------------------------------------------------------------------------------------------------------- |
| PyTorch   | [PyTorch unkeyed model](/documentation/transforms/python/elementwise/runinference-pytorch/#example-1-pytorch-unkeyed-model) |
| PyTorch   | [PyTorch keyed model](/documentation/transforms/python/elementwise/runinference-pytorch/#example-2-pytorch-keyed-model)     |
| Sklearn   | [Sklearn unkeyed model](/documentation/transforms/python/elementwise/runinference-sklearn/#example-1-sklearn-unkeyed-model) |
| Sklearn   | [Sklearn keyed model](/documentation/transforms/python/elementwise/runinference-sklearn/#example-2-sklearn-keyed-model)     |

## Related transforms

Not applicable.

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.ml.inference.html#apache_beam.ml.inference.RunInference) |
