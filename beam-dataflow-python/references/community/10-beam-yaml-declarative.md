# Dataflow Python: Beam YAML and Declarative Pipelines

Introduced to improve developer velocity, **Beam YAML** is a declarative syntax for building pipelines. It is a major focus for standard ETL tasks in 2025.

## Why YAML?
*   **No Code Required:** Data analysts and operators can author complex pipelines without knowing Python or Java.
*   **Built-in Best Practices:** The underlying engine automatically applies optimizations (like proper runner selection and schema inference).
*   **Polyglot by Default:** A YAML pipeline can seamlessly mix Python transforms and Java transforms (via Xlang) without complex setup.

## Best Practices
1.  **Use for Standard ETL:** Use YAML for straightforward Extract-Transform-Load tasks (e.g., reading from Kafka, mapping fields, writing to BigQuery).
2.  **Fallback to Python:** For complex, custom business logic or stateful processing, write a custom Python transform and call it from your YAML pipeline.
3.  **Version Control:** Treat your `pipeline.yaml` files as code. Store them in Git and deploy them via automated pipelines.

## Example YAML Pipeline
```yaml
pipeline:
  type: chain
  transforms:
    - type: ReadFromPubSub
      topic: projects/my-project/topics/input-topic
      format: json
    
    - type: MapToFields
      language: python
      fields:
        user_id: user.id
        event_time: timestamp
        status: '"ACTIVE"'
        
    - type: WriteToBigQuery
      table: my-project:dataset.events
      method: STORAGE_WRITE_API
```

## References & Further Reading
*   [Apache Beam YAML Overview](https://beam.apache.org/documentation/sdks/yaml/)
*   [Apache Beam YAML Transform Reference](https://beam.apache.org/documentation/sdks/yaml-reference/)
