---
source_url: https://beam.apache.org/documentation/transforms/python/elementwise/enrichment-cloudsql/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Enrichment with CloudSQL"
beam_last_updated: "Last updated on 2026/03/06"
---

# Use CloudSQL to enrich data

|                                                                                                                                                                                                      |     |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| [Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.enrichment_handlers.cloudsql.html#apache_beam.transforms.enrichment_handlers.cloudsql.CloudSQLEnrichmentHandler) |     |

Starting with Apache Beam 2.69.0, the enrichment transform includes
built-in enrichment handler support for the
[Google CloudSQL](https://cloud.google.com/sql/docs). This handler allows your
Beam pipeline to enrich data using SQL databases, with built-in support for:

- Managed PostgreSQL, MySQL, and Microsoft SQL Server instances on CloudSQL
- Unmanaged SQL database instances not hosted on CloudSQL (e.g., self-hosted or
  on-premises databases)

The following example demonstrates how to create a pipeline that use the
enrichment transform with the
[`CloudSQLEnrichmentHandler`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.enrichment_handlers.cloudsql.html#apache_beam.transforms.enrichment_handlers.cloudsql.CloudSQLEnrichmentHandler) handler.

## Example 1: Enrichment with Google CloudSQL (Managed PostgreSQL)

The data in the CloudSQL PostgreSQL table `products` follows this format:

| product_id | name | quantity | region_id |
| ---------- | ---- | -------- | --------- |
| 1          | A    | 2        | 3         |
| 2          | B    | 3        | 1         |
| 3          | C    | 10       | 4         |

![](/images/copy-icon.svg)

```
import apache_beam as beam
from apache_beam.transforms.enrichment import Enrichment
from apache_beam.transforms.enrichment_handlers.cloudsql import (
    CloudSQLEnrichmentHandler,
    DatabaseTypeAdapter,
    TableFieldsQueryConfig,
    CloudSQLConnectionConfig)
import os

database_adapter = DatabaseTypeAdapter.POSTGRESQL
database_uri = os.environ.get("GOOGLE_CLOUD_SQL_DB_URI")
database_user = os.environ.get("GOOGLE_CLOUD_SQL_DB_USER")
database_password = os.environ.get("GOOGLE_CLOUD_SQL_DB_PASSWORD")
database_id = os.environ.get("GOOGLE_CLOUD_SQL_DB_ID")
table_id = os.environ.get("GOOGLE_CLOUD_SQL_DB_TABLE_ID")
where_clause_template = "product_id = :pid"
where_clause_fields = ["product_id"]

data = [
    beam.Row(product_id=1, name='A'),
    beam.Row(product_id=2, name='B'),
    beam.Row(product_id=3, name='C'),
]

connection_config = CloudSQLConnectionConfig(
    db_adapter=database_adapter,
    instance_connection_uri=database_uri,
    user=database_user,
    password=database_password,
    db_id=database_id)

query_config = TableFieldsQueryConfig(
    table_id=table_id,
    where_clause_template=where_clause_template,
    where_clause_fields=where_clause_fields)

handler = CloudSQLEnrichmentHandler(
    connection_config=connection_config,
    table_id=table_id,
    query_config=query_config)
with beam.Pipeline() as p:
  _ = (
      p
      | "Create" >> beam.Create(data)
      | "Enrich W/ Google CloudSQL PostgreSQL" >> Enrichment(handler)
      | "Print" >> beam.Map(print))
```

Output:

![](/images/copy-icon.svg)

```
Row(product_id=1, name='A', quantity=2, region_id=3)
Row(product_id=2, name='B', quantity=3, region_id=1)
Row(product_id=3, name='C', quantity=10, region_id=4)
```

## Example 2: Enrichment with Unmanaged PostgreSQL

The data in the Unmanaged PostgreSQL table `products` follows this format:

| product_id | name | quantity | region_id |
| ---------- | ---- | -------- | --------- |
| 1          | A    | 2        | 3         |
| 2          | B    | 3        | 1         |
| 3          | C    | 10       | 4         |

![](/images/copy-icon.svg)

```
import apache_beam as beam
from apache_beam.transforms.enrichment import Enrichment
from apache_beam.transforms.enrichment_handlers.cloudsql import (
    CloudSQLEnrichmentHandler,
    DatabaseTypeAdapter,
    TableFieldsQueryConfig,
    ExternalSQLDBConnectionConfig)
import os

database_adapter = DatabaseTypeAdapter.POSTGRESQL
database_host = os.environ.get("EXTERNAL_SQL_DB_HOST")
database_port = int(os.environ.get("EXTERNAL_SQL_DB_PORT"))
database_user = os.environ.get("EXTERNAL_SQL_DB_USER")
database_password = os.environ.get("EXTERNAL_SQL_DB_PASSWORD")
database_id = os.environ.get("EXTERNAL_SQL_DB_ID")
table_id = os.environ.get("EXTERNAL_SQL_DB_TABLE_ID")
where_clause_template = "product_id = :pid"
where_clause_fields = ["product_id"]

data = [
    beam.Row(product_id=1, name='A'),
    beam.Row(product_id=2, name='B'),
    beam.Row(product_id=3, name='C'),
]

connection_config = ExternalSQLDBConnectionConfig(
    db_adapter=database_adapter,
    host=database_host,
    port=database_port,
    user=database_user,
    password=database_password,
    db_id=database_id)

query_config = TableFieldsQueryConfig(
    table_id=table_id,
    where_clause_template=where_clause_template,
    where_clause_fields=where_clause_fields)

cloudsql_handler = CloudSQLEnrichmentHandler(
    connection_config=connection_config,
    table_id=table_id,
    query_config=query_config)
with beam.Pipeline() as p:
  _ = (
      p
      | "Create" >> beam.Create(data)
      | "Enrich W/ Unmanaged PostgreSQL" >> Enrichment(cloudsql_handler)
      | "Print" >> beam.Map(print))
```

Output:

![](/images/copy-icon.svg)

```
Row(product_id=1, name='A', quantity=2, region_id=3)
Row(product_id=2, name='B', quantity=3, region_id=1)
Row(product_id=3, name='C', quantity=10, region_id=4)
```

## Example 3: Enrichment with Unmanaged MySQL

The data in the Unmanaged MySQL table `products` follows this format:

| product_id | name | quantity | region_id |
| ---------- | ---- | -------- | --------- |
| 1          | A    | 2        | 3         |
| 2          | B    | 3        | 1         |
| 3          | C    | 10       | 4         |

![](/images/copy-icon.svg)

```
import apache_beam as beam
from apache_beam.transforms.enrichment import Enrichment
from apache_beam.transforms.enrichment_handlers.cloudsql import (
    CloudSQLEnrichmentHandler,
    DatabaseTypeAdapter,
    TableFieldsQueryConfig,
    ExternalSQLDBConnectionConfig)
import os

database_adapter = DatabaseTypeAdapter.MYSQL
database_host = os.environ.get("EXTERNAL_SQL_DB_HOST")
database_port = int(os.environ.get("EXTERNAL_SQL_DB_PORT"))
database_user = os.environ.get("EXTERNAL_SQL_DB_USER")
database_password = os.environ.get("EXTERNAL_SQL_DB_PASSWORD")
database_id = os.environ.get("EXTERNAL_SQL_DB_ID")
table_id = os.environ.get("EXTERNAL_SQL_DB_TABLE_ID")
where_clause_template = "product_id = :pid"
where_clause_fields = ["product_id"]

data = [
    beam.Row(product_id=1, name='A'),
    beam.Row(product_id=2, name='B'),
    beam.Row(product_id=3, name='C'),
]

connection_config = ExternalSQLDBConnectionConfig(
    db_adapter=database_adapter,
    host=database_host,
    port=database_port,
    user=database_user,
    password=database_password,
    db_id=database_id)

query_config = TableFieldsQueryConfig(
    table_id=table_id,
    where_clause_template=where_clause_template,
    where_clause_fields=where_clause_fields)

cloudsql_handler = CloudSQLEnrichmentHandler(
    connection_config=connection_config,
    table_id=table_id,
    query_config=query_config)
with beam.Pipeline() as p:
  _ = (
      p
      | "Create" >> beam.Create(data)
      | "Enrich W/ Unmanaged MySQL" >> Enrichment(cloudsql_handler)
      | "Print" >> beam.Map(print))
```

Output:

![](/images/copy-icon.svg)

```
Row(product_id=1, name='A', quantity=2, region_id=3)
Row(product_id=2, name='B', quantity=3, region_id=1)
Row(product_id=3, name='C', quantity=10, region_id=4)
```

## Example 4: Enrichment with Unmanaged Microsoft SQL Server

The data in the Unmanaged Microsoft SQL Server table `products` follows this
format:

| product_id | name | quantity | region_id |
| ---------- | ---- | -------- | --------- |
| 1          | A    | 2        | 3         |
| 2          | B    | 3        | 1         |
| 3          | C    | 10       | 4         |

![](/images/copy-icon.svg)

```
import apache_beam as beam
from apache_beam.transforms.enrichment import Enrichment
from apache_beam.transforms.enrichment_handlers.cloudsql import (
    CloudSQLEnrichmentHandler,
    DatabaseTypeAdapter,
    TableFieldsQueryConfig,
    ExternalSQLDBConnectionConfig)
import os

database_adapter = DatabaseTypeAdapter.SQLSERVER
database_host = os.environ.get("EXTERNAL_SQL_DB_HOST")
database_port = int(os.environ.get("EXTERNAL_SQL_DB_PORT"))
database_user = os.environ.get("EXTERNAL_SQL_DB_USER")
database_password = os.environ.get("EXTERNAL_SQL_DB_PASSWORD")
database_id = os.environ.get("EXTERNAL_SQL_DB_ID")
table_id = os.environ.get("EXTERNAL_SQL_DB_TABLE_ID")
where_clause_template = "product_id = :pid"
where_clause_fields = ["product_id"]

data = [
    beam.Row(product_id=1, name='A'),
    beam.Row(product_id=2, name='B'),
    beam.Row(product_id=3, name='C'),
]

connection_config = ExternalSQLDBConnectionConfig(
    db_adapter=database_adapter,
    host=database_host,
    port=database_port,
    user=database_user,
    password=database_password,
    db_id=database_id)

query_config = TableFieldsQueryConfig(
    table_id=table_id,
    where_clause_template=where_clause_template,
    where_clause_fields=where_clause_fields)

cloudsql_handler = CloudSQLEnrichmentHandler(
    connection_config=connection_config,
    table_id=table_id,
    query_config=query_config)
with beam.Pipeline() as p:
  _ = (
      p
      | "Create" >> beam.Create(data)
      | "Enrich W/ Unmanaged SQL Server" >> Enrichment(cloudsql_handler)
      | "Print" >> beam.Map(print))
```

Output:

![](/images/copy-icon.svg)

```
Row(product_id=1, name='A', quantity=2, region_id=3)
Row(product_id=2, name='B', quantity=3, region_id=1)
Row(product_id=3, name='C', quantity=10, region_id=4)
```

## API documentation

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.enrichment_handlers.cloudsql.html#apache_beam.transforms.enrichment_handlers.cloudsql.CloudSQLEnrichmentHandler) |
