---
title: Data Publication
id: pub-sql
---

# Data Publication

## Create Publication

The `CREATE PUBLICATION` statement is used to create a new publication in the current database. The publication name must be unique among all existing publications in the database.

### Privileges

- The user must have the SELECT privilege on the target time-series tables.

### Syntax

![](../../../static/sql-reference/create_pub.png)

### Syntax

| Parameter | Description |
| --- | --- |
| `name`                  | The name of the publication. It must be unique within the current database. |
| `table_name`            | Specifies the table to add to the publication.<br >**Note**<br >Currently, KWDB only supports publishing time-series tables. Relational tables, temporary tables, internal views and regular views are not supported. |
| `column_name`           | The columns of the time-series table to publish. Supports publishing all columns or specified columns.<br >- *: Publish all columns.<br >- Selected columns: Publish only specified columns. All primary key columns and NOT NULL columns must be included. |
| `WHERE expr`            | `WHERE` clause for row filtering. Rows evaluated as `FALSE` or `NULL` will not be published. |
| `table_name_list`       | List of time-series tables for publication. Multiple table names are separated by commas (`,`).<br >**Note**<br >Row filtering and column selection are not supported. |
| `database_name`         | Specifies the time-series database for publication. All tables in the database will be published.<br >**Note**<br >- Row filtering and column selection are not supported.<br >- Currently, only time-series databases are supported. Relational databases are excluded.|
| `publication_parameter` | Publication configuration parameters:<br >- `buffer_size`: Buffer size in MiB. Set to 0 for immediate delivery. Default value: `1`.<br >- `retrieve_tags`: Enables or disables ordinary Tag supplementation and validation. Valid values: `on` / `off`.`on`: Supplement or validate ordinary Tags. If ordinary Tags are required in output or filter columns but missing during data ingestion, or their mapping to Primary Tags differs from the initial record, the system uses the first recorded ordinary Tag values before publishing.`off`: Disable Tag supplementation. Missing ordinary Tags are treated as NULL. Mismatched Tag values will be published as written. Default value: `off`.
- `publish`: Specifies types of operations to publish. Supported values: `insert`, `update`, `delete`, `all`. Default value: `insert`. |
| `value`                 | The value of the corresponding Publication parameter. |

### Examples

The following examples assume the time-series databas（`benchmark`）and table（`cpu`、`sensor_data`）have been created and populated with data.

```sql
-- create ts database.
CREATE TS DATABASE benchmark;

-- create ts table benchmark.cpu。
CREATE TABLE benchmark.cpu (k_timestamp TIMESTAMPTZ NOT NULL, usage_user INT8 NOT NULL, usage_system INT8 NOT NULL, usage_idle INT8 NOT NULL) TAGS (id INT8 NOT NULL, hostname VARCHAR NOT NULL, region VARCHAR NOT NULL, datacenter VARCHAR NOT NULL) PRIMARY TAGS (id);

-- insert into data to benchmark.cpu.
INSERT INTO benchmark.cpu (k_timestamp, usage_user, usage_system, usage_idle, id, hostname, region, datacenter) VALUES ('2024-01-22 22:22:22.224',2,3,4,647470401348904606,'locahost','nanjing','center');

-- create ts table benchmark.sensor_data.
CREATE TABLE benchmark.sensor_data (k_timestamp TIMESTAMP NOT NULL, temperature FLOAT NOT NULL, humidity FLOAT, pressure FLOAT) TAGS (sensor_id INT NOT NULL,sensor_type VARCHAR(30) NOT NULL) PRIMARY TAGS (sensor_id);

-- insert into data to benchmark.sensor_data.
INSERT INTO benchmark.sensor_data (k_timestamp, temperature, humidity, sensor_id, sensor_type) VALUES ('2023-10-01 08:00:00', 25.5, 60.0, 101, 'a'), ('2023-10-01 09:00:00', 26.0, 58.5, 101, 'b')；
```

- Create a publication and publicate real-time data from table `cpu`，including only columns `usage_user` and `usage_system`.

    ```sql
    CREATE PUBLICATION cpu_filtered FOR TABLE benchmark.cpu (usage_user, usage_system);
    ```

- Create a publication that only publishes `INSERT` operations from table `cpu` .

    ```sql
    CREATE PUBLICATION insert_only FOR TABLE benchmark.cpu WITH OPTIONS (publish = 'insert');
    ```

- Create a publication for tables `cpu` and `sensor_data` with ordinary Tag supplementation enabled.

    ```sql
    CREATE PUBLICATION mypub FOR TABLE benchmark.cpu, benchmark.sensor_data WITH OPTIONS (retrieve_tags = 'on');
    ```

- Create a publication to publish all tables in the `benchmark` database. 

    ```sql
    CREATE PUBLICATION alltables FOR DATABASE benchmark;
    ```

## Show Publication

Use `SHOW PUBLICATIONS` or `SHOW PUBLICATION` to view details of all or specified publications, including name, target objects, configurations, creation time, creator and subscriptions.

### Privileges

None

### Syntax

![](../../../static/sql-reference/show_pub.png)

### Parameters

| 参数 | 说明 |
| --- | --- |
| `name` | The name of the publication. |

### Response Fields

| Field | Description |
| --- | --- |
| `name`         | The name of the publication. |
| `pub_objects`  | The object of the publication. |
| `parameter`    | Configured parameters of the publication. |
| `create_at`    | Creation time of the publication. |
| `create_by`    | Creator of the publication. |
| `subscription` | Subscription information. Only active and connected subscriptions are displayed.|

### Examples

View details of the publication `pub1`.

```sql
SHOW PUBLICATION mypub;
```

Sample output:

```sql
  name  |                    pub_objects                    |                                                                                                                                                                                                                                                                                                                                                                                                                                                                    parameter                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |            create_at             | create_by | subscription
--------+---------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+-----------+---------------
  mypub | benchmark.public.cpu,benchmark.public.sensor_data | {"options": {"buffer_size": 1, "publish": "insert", "retrieve_tags": "on", "sub_timeout": 2}, "table_list": [{"column_ids": [1, 2, 3, 4, 5, 6, 7, 8], "column_names": ["k_timestamp", "usage_user", "usage_system", "usage_idle", "id", "hostname", "region", "datacenter"], "column_types": ["TIMESTAMPTZ(3)", "INT8", "INT8", "INT8", "INT8", "VARCHAR(254)", "VARCHAR(254)", "VARCHAR(254)"], "database": "benchmark", "id": 96, "is_star": true, "need_normal_tag": true, "schema": "public", "table": "cpu", "ts_column_name": "k_timestamp"}, {"column_ids": [1, 2, 3, 4, 5, 6], "column_names": ["k_timestamp", "temperature", "humidity", "pressure", "sensor_id", "sensor_type"], "column_types": ["TIMESTAMPTZ(3)", "FLOAT8", "FLOAT8", "FLOAT8", "INT4", "VARCHAR(30)"], "database": "benchmark", "id": 97, "is_star": true, "need_normal_tag": true, "schema": "public", "table": "sensor_data", "ts_column_name": "k_timestamp"}]} | 2025-10-11 06:49:46.238842+00:00 | root      | null
(1 row)
```

## Alter Publication

The `ALTER PUBLICATION` statement modifies existing publications. It contains two subcommands: 

- `ALTER PUBLICATION SET TABLE`：Modifies target time-series tables, output columns and filter conditions.
- `ALTER PUBLICATION SET OPTIONS`：Modifies publication parameters.

::: warning Notes

- The two subcommands must be executed separately. Modifying target objects and parameters in one statement is not supported.
- Target objects cannot be modified if the publication covers an entire database or multiple tables.
- Online modification is only allowed when no active subscriptions exist for the publication.
:::

### Privileges

- The user must be a member of the `admin` role or the creator of the publication.

### Syntax

![](../../../static/sql-reference/alter_pub.png)

### Parameters

| Parameter | Description |
| --- | --- |
| `name`         | The name of the publication to modify. |
| `table_name`   | The name of the time-series table.<br >*Note** <br >Currently, KWDB only supports publishing time-series tables. Relational tables, temporary tables, internal views and regular views are not supported. |
| `column_name`  |  The columns of the time-series table to publish. Supports publishing all columns or specified columns.<br >- *: Publish all columns.<br >- Selected columns: Publish only specified columns. All primary key columns and NOT NULL columns must be included. |
| `WHERE expr`   | `WHERE` clause for row filtering. Rows evaluated as `FALSE` or `NULL` will not be published. |
| `publication_parameter` | Publication configuration parameters:<br >- `buffer_size`: Buffer size in MiB. Set to 0 for immediate delivery. Default value: `1`.<br >- `retrieve_tags`: Enables or disables ordinary Tag supplementation and validation. Valid values: `on` / `off`.`on`: Supplement or validate ordinary Tags. If ordinary Tags are required in output or filter columns but missing during data ingestion, or their mapping to Primary Tags differs from the initial record, the system uses the first recorded ordinary Tag values before publishing.`off`: Disable Tag supplementation. Missing ordinary Tags are treated as NULL. Mismatched Tag values will be published as written. Default value: `off`.
- `publish`: Specifies types of operations to publish. Supported values: `insert`, `update`, `delete`, `all`. Default value: `insert`. |
| `value`       | The value of the corresponding Publication parameter. |

### Example

Disable ordinary Tag supplementation for the publication  `mypub`.

```sql
ALTER PUBLICATION mypub SET OPTIONS (retrieve_tags = 'off');
ALTER PUBLICATION
```

## Drop Publication

The `DROP PUBLICATION` statement deletes a specified publication.

### Privileges

- The user must be a member of the admin role or the creator of the publication.

### Syntax

![](../../../static/sql-reference/drop_pub.png)

### Parameters

| Parameter | Description |
| --- | --- |
| `IF EXISTS` | Optional keyword. If specified, no error is returned when the target publication does not exist. Without this keyword, an error will be thrown if the publication cannot be found. |
| `name`      | The name of the publication. |


### Syntax

Drop the publication named `mypub`.

```sql
DROP PUBLICATION mypub;
```
