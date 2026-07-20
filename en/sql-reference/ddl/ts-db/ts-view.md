---
title: Views
id: ts-view
---

# Views

## CREATE VIEW

The `CREATE VIEW` statement creates a new view, which is a stored query represented as a virtual table.

### Privileges

The user must be a member of the `admin` role or have been granted the `CREATE` privilege on the parent database and the `SELECT` privilege on any table(s) referenced by the view. By default, the `root` user belongs to the `admin` role.

### Syntax

![](../../../../static/sql-reference/create_ts_view.png)

### Parameters

| Parameter | Description |
| --- | --- |
| `IF NOT EXISTS` | Optional. <br>- When the `IF NOT EXISTS` keyword is used, the system creates a new view only if a view of the same name does not already exist. Otherwise, the system fails to create a view table without returning an error. <br>- When the `IF NOT EXISTS` keyword is not used, the system creates a new view only if a view of the same name does not already exist. Otherwise, the system fails to create a new view and returns an error.  |
| `view_name` | The name of the view to create. The view name must be unique within the database and must follow these [Identifier Rules](../../../sql-reference/sql-identifiers.md). When the parent database is not set as the default, the name must be formatted as `database.view_name`. |
| `opt_column_list` | An optional, comma-separated list of column names for the view. If specified, these names will be used in the response instead of the columns specified in the `select_stmt` statement. |
| `select_stmt` | The selection query to execute when the view is requested. Currently, it is possible to use `*` to select all columns from a referenced table. <br >- Where there are duplicate columns in the result set, the system returns the `duplicate column name: "a"` error. <br >- When new columns are added to the original table, the view structure is not changed. <br >- When deleting a column referenced by the view from the original table, the system returns the `cannot drop column "b" because view "v" depends on it` error. |

### Examples

The following example demonstrates creating a table named `sensor_data` which contains columns for timestamp, temperature, humidity and device ID. It also creates a view named `v_sensor_min_agg` for the `sensor_data` table to calculate the average temperature and humidity of each device every minute.

```sql
-- 1. Create sensor_data.

create table sensor_data ( 
-- Time series timestamp (primary key)
 ts timestamp not null,
-- Metric: Temperature
 temperature double ,
-- Metric: Humidity
 humidity double
)tags(device_ID varchar(50) not null
) primary tags(device_ID);

--2. Bulk writing sensor time series data

INSERT INTO sensor_data (ts, temperature, humidity, device_id)
VALUES
('2026-07-14 08:00:01', 25.3, 48.2, 'dev_001'),
('2026-07-14 08:00:02', 25.5, 48.1, 'dev_001'),
('2026-07-14 08:00:03', 25.4, 48.0, 'dev_001'),
('2026-07-14 08:01:01', 25.3, 48.2, 'dev_001'),
('2026-07-14 08:01:02', 25.6, 48.0, 'dev_001'),
('2026-07-14 08:01:03', 25.2, 48.3, 'dev_001'),
('2026-07-14 08:00:01', 26.3, 47.9, 'dev_002'),
('2026-07-14 08:00:02', 26.1, 47.8, 'dev_002'),
('2026-07-14 08:00:03', 26.2, 47.9, 'dev_002'),
('2026-07-14 08:01:01', 26.3, 47.7, 'dev_002'),
('2026-07-14 08:01:02', 26.4, 47.6, 'dev_002'),
('2026-07-14 08:01:03', 26.5, 47.8, 'dev_002');

-- 3. Create a view named v_sensor_min_agg for the sensor_data table to calculate the average temperature and humidity of each device every minute. 

create view v_sensor_min_agg as
select
	date_trunc('minute', ts) as collect_time,
	device_id,
	avg(temperature) as avg_temp,
	avg(humidity) as avg_humi
from
	sensor_data
group by
	collect_time,
	device_id;

-- 4. Check what views are available.

show tables;
     table_name    |    table_type
-------------------+--------------------
  sensor_data      | TIME SERIES TABLE
  v_sensor_min_agg | VIEW
(2 rows)

--5. View the creation statement of the view

 show create view v_sensor_min_agg;
     table_name    |                                                                                                                        create_statement
-------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  v_sensor_min_agg | CREATE VIEW v_sensor_min_agg (collect_time, device_id, avg_temp, avg_humi) AS SELECT date_trunc('minute', ts) AS collect_time, device_id, avg(temperature) AS avg_temp, avg(humidity) AS avg_humi FROM tsdb.public.sensor_data GROUP BY collect_time, device_id
(1 row)

--6. View view information.

SELECT * FROM v_sensor_min_agg;
        collect_time        |      avg_temp      |      avg_humi      | device_id
----------------------------+--------------------+--------------------+------------
  2026-07-14 08:00:00+00:00 | 26.200000000000003 |  47.86666666666667 | dev_002
  2026-07-14 08:01:00+00:00 | 26.400000000000002 |  47.70000000000001 | dev_002
  2026-07-14 08:00:00+00:00 | 25.399999999999995 |               48.1 | dev_001
  2026-07-14 08:01:00+00:00 |  25.36666666666667 | 48.166666666666664 | dev_001
(4 rows)
```

## ALTER VIEW

The `ALTER VIEW` statement changes the name of a view.

### Privileges

The user must be a member of the `admin` role or have been granted the `DROP` privilege on the current view and the `CREATE` privilege on the parent database of the renamed view. By default, the `root` user belongs to the `admin` role.


### Syntax

![](../../../../static/sql-reference/QVdqbp6BaocGw4xnbaYcLlYFnFd.png)

### Parameters

| Parameter | Description |
| --- | --- |
| `IF EXISTS` | Optional. <br>- When the `IF EXISTS` keyword is used, the system updates the view only if the target view has already existed. Otherwise, the system fails to update the view without returning an error. <br>- When the `IF EXISTS` keyword is not used, the system updates the view only if the target view has already existed. Otherwise, the system fails to update the view and returns an error. |
| `view_name` | The current name of the view to rename. You can use the `SELECT * FROM information_schema.tables WHERE table_type = 'VIEW'` statement to get existing view names. |
| `name` | The new name of the view. The view name must be unique within the database and must follow these [Identifier Rules](../../sql-identifiers.md). |

### Examples

This example renames the `test_view` view to `names`.

```sql
-- 1. Check all views. 

SELECT * FROM information_schema.tables WHERE table_type = 'VIEW';
  table_catalog | table_schema |    table_name    | table_type | is_insertable_into | version | namespace_oid
----------------+--------------+------------------+------------+--------------------+---------+----------------
  tsdb          | public       | v_sensor_min_agg | VIEW       | NO                 |       1 |    3015832540
(1 row)

-- 2. Rename the v_sensor_min_agg view to v_sensor_avg_agg.

ALTER VIEW v_sensor_min_agg rename to v_sensor_avg_agg;
RENAME VIEW

-- 3. Check all views.

SELECT * FROM information_schema.tables WHERE table_type = 'VIEW';
  table_catalog | table_schema |    table_name    | table_type | is_insertable_into | version | namespace_oid
----------------+--------------+------------------+------------+--------------------+---------+----------------
  tsdb          | public       | v_sensor_avg_agg | VIEW       | NO                 |       3 |    3015832540
(1 row)
```

## DROP VIEW

The `DROP VIEW` statement removes a view from a database.

### Privileges

- Remove a view with no dependency: the user must be a member of the `admin` role or have been granted the `DROP` privilege on the specified view(s).
- Remove a view with dependencies: the user must be a member of the `admin` role or have been granted the `DROP` privilege on the specified view(s) and its dependent objects.

### Syntax

![](../../../../static/sql-reference/ItRwb2ZvioB5H1xm1TgcvmXjnNd.png)

### Parameters

| Parameter | Description |
| --- | --- |
| `IF EXISTS` | Optional. <br>- When the `IF EXISTS` keyword is used, the system removes the view only if the target view has already existed. Otherwise, the system fails to remove the view without returning an error. <br>- When the `IF EXISTS` keyword is not used, the system removes the view only if the target view has already existed. Otherwise, the system fails to remove the view and returns an error. |
| `view_name_list` | A comma-separated list of view names. You can use the `SELECT * FROM information_schema.tables WHERE table_type = 'VIEW'` statement to get existing view names. |
| `CASCADE` | Optional. Remove the target view and its dependent objects. The `CASCADE` keyword does not list objects it removes, so it should be used cautiously. |
| `RESTRICT` | (Default) Optional. Do not remove the view if any objects depend on it. |

### Examples

This example removes the `names` view.

```sql
-- 1. Check all views. 

SELECT * FROM information_schema.tables WHERE table_type = 'VIEW';
  table_catalog | table_schema |    table_name    | table_type | is_insertable_into | version | namespace_oid
----------------+--------------+------------------+------------+--------------------+---------+----------------
  tsdb          | public       | v_sensor_avg_agg | VIEW       | NO                 |       3 |    3015832540
(1 row)

-- 2. Drop the v_sensor_avg_agg view。

DROP VIEW v_sensor_avg_agg;
DROP VIEW

-- 3. Check all views.

SELECT * FROM information_schema.tables WHERE table_type = 'VIEW';
  table_catalog | table_schema | table_name | table_type | is_insertable_into | version | namespace_oid
----------------+--------------+------------+------------+--------------------+---------+----------------
(0 rows)
```
