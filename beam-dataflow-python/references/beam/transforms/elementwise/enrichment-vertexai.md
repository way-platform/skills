---
source_url: https://beam.apache.org/documentation/transforms/python/elementwise/enrichment-vertexai/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Enrichment with Vertex AI Feature Store"
beam_last_updated: "Last updated on 2026/03/06"
---

# Enrichment with Google Cloud Vertex AI Feature Store

|                                                                                                                                                                                                                                                |     |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| [Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.enrichment_handlers.vertex_ai_feature_store.html#apache_beam.transforms.enrichment_handlers.vertex_ai_feature_store.VertexAIFeatureStoreEnrichmentHandler) |     |

In Apache Beam 2.55.0 and later versions, the enrichment transform includes a built-in enrichment handler for [Vertex AI Feature Store](https://cloud.google.com/vertex-ai/docs/featurestore).
The following example demonstrates how to create a pipeline that use the enrichment transform with the [`VertexAIFeatureStoreEnrichmentHandler`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.enrichment_handlers.vertex_ai_feature_store.html#apache_beam.transforms.enrichment_handlers.vertex_ai_feature_store.VertexAIFeatureStoreEnrichmentHandler) handler and the [`VertexAIFeatureStoreLegacyEnrichmentHandler`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.enrichment_handlers.vertex_ai_feature_store.html#apache_beam.transforms.enrichment_handlers.vertex_ai_feature_store.VertexAIFeatureStoreLegacyEnrichmentHandler) handler.

## Example 1: Enrichment with Vertex AI Feature Store

The precomputed feature values stored in Vertex AI Feature Store uses the following format:

| user_id | age | gender | state | country |
| ------- | --- | ------ | ----- | ------- |
| 21422   | 12  | 0      | 0     | 0       |
| 2963    | 12  | 1      | 1     | 1       |
| 20592   | 12  | 1      | 2     | 2       |
| 76538   | 12  | 1      | 3     | 0       |

![](/images/copy-icon.svg)

```
import apache_beam as beam
from apache_beam.transforms.enrichment import Enrichment
from apache_beam.transforms.enrichment_handlers.vertex_ai_feature_store \
  import VertexAIFeatureStoreEnrichmentHandler

project_id = 'apache-beam-testing'
location = 'us-central1'
api_endpoint = f"{location}-aiplatform.googleapis.com"
data = [
    beam.Row(user_id='2963', product_id=14235, sale_price=15.0),
    beam.Row(user_id='21422', product_id=11203, sale_price=12.0),
    beam.Row(user_id='20592', product_id=8579, sale_price=9.0),
]

vertex_ai_handler = VertexAIFeatureStoreEnrichmentHandler(
    project=project_id,
    location=location,
    api_endpoint=api_endpoint,
    feature_store_name="vertexai_enrichment_example",
    feature_view_name="users",
    row_key="user_id",
)
with beam.Pipeline() as p:
  _ = (
      p
      | "Create" >> beam.Create(data)
      | "Enrich W/ Vertex AI" >> Enrichment(vertex_ai_handler)
      | "Print" >> beam.Map(print))
```

Output:

![](/images/copy-icon.svg)

```
Row(user_id='2963', product_id=14235, sale_price=15.0, age=12.0, state='1', gender='1', country='1')
Row(user_id='21422', product_id=11203, sale_price=12.0, age=12.0, state='0', gender='0', country='0')
Row(user_id='20592', product_id=8579, sale_price=9.0, age=12.0, state='2', gender='1', country='2')
```

## Example 2: Enrichment with Vertex AI Feature Store (legacy)

The precomputed feature values stored in Vertex AI Feature Store (Legacy) use the following format:

| entity_id | title                    | genres |
| --------- | ------------------------ | ------ |
| movie_01  | The Shawshank Redemption | Drama  |
| movie_02  | The Shining              | Horror |
| movie_04  | The Dark Knight          | Action |

![](/images/copy-icon.svg)

```
import apache_beam as beam
from apache_beam.transforms.enrichment import Enrichment
from apache_beam.transforms.enrichment_handlers.vertex_ai_feature_store \
  import VertexAIFeatureStoreLegacyEnrichmentHandler

project_id = 'apache-beam-testing'
location = 'us-central1'
api_endpoint = f"{location}-aiplatform.googleapis.com"
data = [
    beam.Row(entity_id="movie_01", title='The Shawshank Redemption'),
    beam.Row(entity_id="movie_02", title="The Shining"),
    beam.Row(entity_id="movie_04", title='The Dark Knight'),
]

vertex_ai_handler = VertexAIFeatureStoreLegacyEnrichmentHandler(
    project=project_id,
    location=location,
    api_endpoint=api_endpoint,
    entity_type_id='movies',
    feature_store_id="movie_prediction_unique",
    feature_ids=["title", "genres"],
    row_key="entity_id",
)
with beam.Pipeline() as p:
  _ = (
      p
      | "Create" >> beam.Create(data)
      | "Enrich W/ Vertex AI" >> Enrichment(vertex_ai_handler)
      | "Print" >> beam.Map(print))
```

Output:

![](/images/copy-icon.svg)

```
Row(entity_id='movie_01', title='The Shawshank Redemption', genres='Drama')
Row(entity_id='movie_02', title='The Shining', genres='Horror')
Row(entity_id='movie_04', title='The Dark Knight', genres='Action')
```

## Related transforms

Not applicable.

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.enrichment_handlers.vertex_ai_feature_store.html#apache_beam.transforms.enrichment_handlers.vertex_ai_feature_store.VertexAIFeatureStoreEnrichmentHandler) |
