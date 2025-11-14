---
title: Time-Series Data Query
id: ts-data-query
---

# Time-Series Data Query

The time-series database supports executing various query types using SQL statements, including simple queries, nested queries, join queries, UNION queries, and interpolation queries.

## Simple Query

### Privileges

The user must be a member of the `admin` role or have been granted the `SELECT` privilege on the specified table(s). By default, the `root` user belongs to the `admin` role.

### Syntax

For details about the syntax used to query time-series data, see [SQL Reference](../../../en/sql-reference/dml/ts-db/ts-select.md#syntax).

### Parameters

For details about the parameters used to query time-series data, see [SQL Reference](../../../en/sql-reference/dml/ts-db/ts-select.md#parameters).

### Examples

- Retrieve data from a time-series table.

    ```sql
    -- 1. Create a table named t1.

    CREATE TABLE ts_db.t1(ts timestamp not null,a int, b int) tags(tag1 int not null, tag2 int) primary tags(tag1);
    CREATE TABLE

    -- 2. Insert data into the table.

    INSERT INTO ts_db.t1 VALUES(now(),11,11,33,44);
    INSERT INTO ts_db.t1 VALUES(now(),22,22,33,44);
    INSERT INTO ts_db.t1 VALUES(now(),11,33,33,44);
    INSERT INTO ts_db.t1 VALUES(now(),22,44,33,44);
    INSERT INTO ts_db.t1 VALUES(now(),33,55,44,44);
    INSERT INTO ts_db.t1 VALUES(now(),22,44,44,44);
    INSERT INTO ts_db.t1 VALUES(now(),33,44,55,44);
    INSERT INTO ts_db.t1 VALUES(now(),null,null,66,66);
    INSERT INTO ts_db.t1 VALUES(now(),null,null,66,77);

    -- 3. Query data from the table.

    SELECT * FROM t1;
                  ts               |  a   |  b   | tag1 | tag2
    --------------------------------+------+------+------+-------
      2024-02-26 01:28:28.867+00:00 |   11 |   11 |   33 |   44
      2024-02-26 01:28:28.874+00:00 |   22 |   22 |   33 |   44
      2024-02-26 01:28:28.877+00:00 |   11 |   33 |   33 |   44
      2024-02-26 01:28:28.88+00:00  |   22 |   44 |   33 |   44
      2024-02-26 01:28:28.883+00:00 |   33 |   55 |   44 |   44
      2024-02-26 01:28:28.885+00:00 |   22 |   44 |   44 |   44
      2024-02-26 01:28:28.888+00:00 |   33 |   44 |   55 |   44
      2024-02-26 01:28:28.89+00:00  | NULL | NULL |   66 |   66
      2024-02-26 01:28:28.893+00:00 | NULL | NULL |   66 |   66
    (9 rows)
    ```

- Retrieve specific columns.

    ```sql
    SELECT sum(a) FROM ts_db.t1;
      sum
    -------
      154
    (1 row)
    ```

- Use the `DISTINCT` keyword to remove duplicate values, retaining only one instance of each unique value.

    ```sql
    SELECT DISTINCT a FROM ts_db.t1;
      a
    --------
        11
        22
        33
      NULL
    (4 rows)
    ```

- Use the `WHERE` clause to filter tag columns.

    ```sql
    SELECT tag1 FROM ts_db.t1 WHERE a = 11;
      tag1
    --------
        33
        33
    (2 rows)
    ```

- Use the `GROUP BY` and `ORDER BY` clauses to group and sort data columns.

    ```sql
    SELECT a, max(b) FROM ts_db.t1 GROUP BY a ORDER BY a;
      a   | max
    -------+-------
      NULL | NULL
        11 |   33
        22 |   44
        33 |   55
    (4 rows)
    ```

## Interpolation Query

In some cases, time-series data may be missing or contain gaps, which can affect the usage and analysis of subsequent data. KWDB provides the `time_bucket_gapfill()` and `interpolate()` functions to address this issue. These functions support aligning timestamps based on specified intervals and filling missing TIMESTAMP-typed column values.

The interpolation functions can work with the following:

- `LIMIT`: Specifies the maximum number of rows to return after interpolating and filling values.
- `LIMIT...OFFSET`: Specifies the maximum number of rows to return after interpolating and filling values, as well as the number of rows to skip.
- Subquery: Includes non-correlated `FROM` subqueries, and correlated and non-correlated `WHERE` subqueries. Tables in subqueries can be either time-series tables or relational tables.
- `JOIN`: Includes `JOIN`, `FULL JOIN`, `LEFT JOIN`, and `RIGHT JOIN`. When the interpolation query works with `JOIN`, KWDB performs the `JOIN` operation first and then applies interpolation to the result.
- `UNION`: Includes `UNION` and `UNION ALL`. When the interpolation query works with `UNION`, each subquery or dataset applies interpolation first, and then the system combines the result sets.

::: warning Note

The `time_bucket_gapfill()` function must be used with the `GROUP BY` clause. To query columns that are not specified in the `GROUP BY` clause, you must use aggregate functions. For example, KWDB does not support the following query:

```sql
SELECT time_bucket_gapfill (time, 86400) AS a, c1 FROM t1 GROUP BY a;
```

In this case, you must use an aggregate function to query the data:

```sql
SELECT time_bucket_gapfill (time, 86400) AS a, max(c1) FROM t1 GROUP BY a;
```

:::

### Privileges

The user must be a member of the `admin` role or have been granted the `SELECT` privilege on the specified table(s). By default, the `root` user belongs to the `admin` role.

### Syntax

- Perform interpolation queries without filling missing values:

    ```sql
    SELECT time_bucket_gapfill(<timestamp_column>, <interval>) AS <alias_1> 
    FROM <table_name> 
    GROUP BY <column_list_1> 
    [ORDER BY <column_list_2>] 
    [LIMIT <n>] 
    [OFFSET <m>];
    ```

- Perform interpolation queries and fill missing values:

    ```sql
    SELECT time_bucket_gapfill(<timestamp_column>, <interval>) AS <alias_1>, 
          interpolate(<expression_1>, <expression_2>) [AS <alias_2>] 
    FROM <table_name> 
    GROUP BY <column_list_1> 
    [ORDER BY <column_list_2>] 
    [LIMIT <n>] 
    [OFFSET <m>];
    ```

### Parameters

| Parameter | Description |
| --- | --- |
| `timestamp_column` | The TIMESTAMP-typed column. |
| `interval` | The interval, in units of nanosecond, microsecond, millisecond, second, minute, hour, day, week, month, and year. KWDB does not support composite time formats, such as `1d1h`. <br> The following lists the accepted input forms for each unit: <br> - nanosecond: `ns`, `nsec`, `nsecs`, `nanosecond`, `nanoseconds` <br> - microsecond: `us`, `usec`, `usecs`, `microsecond`, `microseconds` <br> - millisecond: `ms`, `msec`, `msecs`, `millisecond`, `milliseconds` <br> - second: `s`, `sec`, `secs`, `second`, `seconds` <br> - minute: `m`, `min`, `mins`, `minute`, `minutes` <br> - hour: `h`, `hr`, `hrs`, `hour`, `hours`<br> - day: `d`, `day`, `days` <br> - week: `w`, `week`, `weeks` <br> - month: `mon`, `mons`, `month`, `months` <br> - year: `y`, `yr`, `yrs`, `year`, `years`|
| `alias_1` | An alias for the generated time bucket results, which makes queries more readable and understandable.|
| `table_name` | The name of the table to query. |
| `column_list_1` | A comma-separated list of columns to group by. KWDB treats all columns except the timestamp-typed column as a group and fills values within the group. Groups are independent. |
| `column_list_2` | A comma-separated list of columns to sort by. You can use the `ASC` or `DESC` keyword to sort the column in ascending (ASC) or descending (DESC) order. The default is `ASC`.|
| `n` | Optional. Specifies the maximum number of rows to return. |
| `m` | Optional. Specifies the number of rows to skip. Use `LIMIT` and `OFFSET` to paginate through retrieved rows. |
| `expression_1` | Interpolation algorithm, supporting only aggregate functions and numeric data types. |
| `expression_2` | Interpolation mode, supporting constant, prev, next, linear, and null. The data type of the filled values must be consistent with that of the original data. |
| `alias_2` | Optional. An alias for the interpolation results, which makes queries more readable and understandable.|

### Examples

These examples assume that you have created two time-series tables and inserted data into them.

```sql
-- Create a table named t1 and insert data into the table.
create table t1(time timestamp not null, temperature DOUBLE, humidity DOUBLE) tags(device_id int not null) primary tags(device_id);
INSERT INTO t1 (time, device_id, temperature, humidity) VALUES ('2024-08-01 12:00:00', 1, 25.3, 60.2);
INSERT INTO t1 (time, device_id, temperature, humidity) VALUES ('2024-09-01 12:00:00', 2, 25.6, 60.3);

-- Create a table named t2 and insert data into the table.
create table t2(time timestamp not null, temperature DOUBLE, humidity DOUBLE) tags(device_id int not null) primary tags(device_id);
INSERT INTO t2 (time, device_id, temperature, humidity) VALUES ('2024-08-01 12:00:00', 1, 25.3, 60.2);
INSERT INTO t2 (time, device_id, temperature, humidity) VALUES ('2024-09-01 12:00:00', 2, 25.6, 60.3);
```

- Perform interpolation queries without filling missing values.

    ```sql
    SELECT time_bucket_gapfill (time, 86400) AS tt FROM t1 GROUP BY tt ORDER BY tt;
                tt
    -----------------------------
      2024-08-01 00:00:00+00:00
      2024-08-02 00:00:00+00:00
      2024-08-03 00:00:00+00:00
      2024-08-04 00:00:00+00:00
      2024-08-05 00:00:00+00:00
      2024-08-06 00:00:00+00:00
      2024-08-07 00:00:00+00:00
      2024-08-08 00:00:00+00:00
      ...
    (32 rows)
    ```

- Perform interpolation queries and fill missing values using PREV.

    ```sql
     SELECT time_bucket_gapfill(time, 86400) AS tt, interpolate(avg(temperature), PREV) FROM t1 GROUP BY tt ORDER BY tt;
                tt             | interpolate
    ----------------------------+--------------
      2024-08-01 00:00:00+00:00 |        25.3
      2024-08-02 00:00:00+00:00 |        25.3
      2024-08-03 00:00:00+00:00 |        25.3
      2024-08-04 00:00:00+00:00 |        25.3
      2024-08-05 00:00:00+00:00 |        25.3
      2024-08-06 00:00:00+00:00 |        25.3
      2024-08-07 00:00:00+00:00 |        25.3
      2024-08-08 00:00:00+00:00 |        25.3
      ...
    (32 rows)
    ```

- Perform interpolation queries, fill missing values using constants, and limit the result set size using the `LIMIT` and `OFFSET` clauses.

    ```sql
    SELECT time_bucket_gapfill(time, 86400) AS tt, interpolate(avg(temperature), '25') FROM t1 GROUP BY tt ORDER BY tt limit 8 offset 2;
              tt             | interpolate
  ----------------------------+--------------
    2024-08-03 00:00:00+00:00 |          25
    2024-08-04 00:00:00+00:00 |          25
    2024-08-05 00:00:00+00:00 |          25
    2024-08-06 00:00:00+00:00 |          25
    2024-08-07 00:00:00+00:00 |          25
    2024-08-08 00:00:00+00:00 |          25
    2024-08-09 00:00:00+00:00 |          25
    2024-08-10 00:00:00+00:00 |          25
  (8 rows)
  ```

- Perform interpolation queries with a `FROM` subquery.

    In this example, the system first groups and performs interpolation queries on the original data daily, and then groups and performs interpolation queries on the interpolation results every 2 days.

    ```sql
    select time_bucket_gapfill(tt, 2 * 86400) as c,interpolate(count(b), null) from (select time_bucket_gapfill(time,86400) as tt,interpolate(max(device_id),linear) as b from t1 group by tt order by tt ) group by c order by c;
                  c             | interpolate
    ----------------------------+--------------
      2024-08-01 00:00:00+00:00 |           2
      2024-08-03 00:00:00+00:00 |           2
      2024-08-05 00:00:00+00:00 |           2
      2024-08-07 00:00:00+00:00 |           2
      2024-08-09 00:00:00+00:00 |           2
      2024-08-11 00:00:00+00:00 |           2
    ...
    (16 rows)
    ```

- Perform interpolation queries with a `WHERE` subquery.

    In this example, the system first retrieves the largest timestamp from the `t1` table and then filters records whose timestamps are greater than that value.

    ```sql
    select * from t1 where time > (select time_bucket_gapfill(time,86400) as tb from t1 group by tb order by tb desc limit 1) order by time;
    time                   |temperature|humidity|device_id|
    -----------------------|-----------|--------|---------|
    2024-09-01 12:00:00.000|       25.6|    60.3|        2|
    (1 row)
    ```

- Perform interpolation queries with a `UNION` query.

    In this example, each subquery applies interpolation first, and then the system combines the result sets.

    ```sql
    SELECT time_bucket_gapfill(time, 86400) AS a, interpolate(avg(temperature), 'linear') FROM t1 GROUP BY a UNION ALL SELECT time_bucket_gapfill(time, 86400) AS a, interpolate(avg(temperature), 'linear') FROM t2 GROUP BY a limit 8;
        a                  |interpolate       |
    -----------------------|------------------|
    2024-08-01 00:00:00.000|              25.3|
    2024-08-02 00:00:00.000|25.309677419354838|
    2024-08-03 00:00:00.000| 25.31935483870968|
    2024-08-04 00:00:00.000|25.329032258064515|
    2024-08-05 00:00:00.000|25.338709677419356|
    2024-08-06 00:00:00.000|25.348387096774193|
    2024-08-07 00:00:00.000|25.358064516129033|
    2024-08-08 00:00:00.000| 25.36774193548387|
    (8 rows)
    ```

## Contextual Min/Max Query

The contextual min/max query feature in KWDB allows you to retrieve the complete row context when using `min` or `max` functions. This feature extends beyond standard SQL syntax limitations, enabling you to obtain complete contextual information about extreme values in a single query.

**Notes:**

- This feature currently supports queries on **a single time-series table** only.
- Only **one** `min` or `max` function can be used per query.
- Only the following aggregate functions are supported: `min`, `max`, `first`, `last`, where:
  - `min` and `max` do not support tag columns.
  - `first` and `last` only support timestamp columns.
- The `SELECT` clause must include at least one **non-aggregated column**, and these non-aggregated columns cannot all be included in the `GROUP BY` clause.

### Privileges

The user must be a member of the `admin` role or have been granted the `SELECT` privilege on the specified table(s). By default, the `root` user belongs to the `admin` role.

### Syntax

```sql
SELECT <non_agg_column_list>, [<min_function> | <max_function>] [, <first_function>] [, <last_function>]
FROM <table_name>
[WHERE <condition>]
[GROUP BY <grouping_columns>]
[ORDER BY <ordering_columns>];
```

::: warning Note

Columns in the `SELECT` clause can be arranged in any order, but must include:

- At least one non-aggregated column
- One `min_function` or `max_function`

:::

### Parameters

| Parameter | Description |
| --- | --- |
| `non_agg_column_list` | (Required) List of non-aggregated columns. Supports multiple columns, each of which can be a column name, function expression, or combination of column name and function. For example: `voltage`, `round(voltage)`, etc. Supports all time-series data types, mathematical functions, string functions, and expression calculations.|
| `min_function` | Supports nested functions, such as `min(voltage)`, `min(abs(voltage))`.|
| `max_function` | Supports nested functions, such as `max(temperature)`, `max(sqrt(power))`.|
| `first_function` | Retrieves the data with the smallest timestamp within the specified range (excluding NULL values).|
| `last_function` | Retrieves the data with the largest timestamp within the specified range (excluding NULL values).|
| `table_name` | The name of the time-series table to query.|
| `grouping_columns` | Column names for grouping, which can be regular columns, expressions, time bucket functions, or grouping window functions such as time windows, event windows, count windows, or session windows.|
| `ordering_columns` | Column names for sorting. Supports multiple fields separated by commas (`,`). You can specify `ASC` (ascending) or `DESC` (descending); the default is ascending.|

### Examples

The following examples assume that you have created a time-series database (`sensor_db`), a time-series table (`sensors`), and inserted the corresponding data into the table.

```sql
-- Create time-series database
CREATE TS DATABASE sensor_db;

-- Switch to time-series database
USE sensor_db;

-- Create sensor data table
CREATE TABLE sensors (
    k_timestamp TIMESTAMP NOT NULL,
    voltage FLOAT,
    temperature FLOAT
) TAGS (
    device_id INT NOT NULL,
    location VARCHAR(100)
) PRIMARY TAGS (device_id);

-- Insert data to device 1 (2024-01-01)
INSERT INTO sensors (k_timestamp, voltage, temperature, device_id, location) VALUES
('2024-01-01 00:00:00', 220.5, 25.3, 1, 'Beijing Server Room A'),
('2024-01-01 00:10:00', 219.8, 25.5, 1, 'Beijing Server Room A'),
('2024-01-01 00:20:00', 221.2, 25.8, 1, 'Beijing Server Room A'),
('2024-01-01 00:30:00', 218.5, 26.1, 1, 'Beijing Server Room A'),  -- Minimum voltage
('2024-01-01 00:40:00', 220.0, 26.3, 1, 'Beijing Server Room A'),
('2024-01-01 00:50:00', 222.3, 26.5, 1, 'Beijing Server Room A'),  -- Maximum voltage
('2024-01-01 01:00:00', 220.8, 26.2, 1, 'Beijing Server Room A'),

-- Insert data to device 2 (2024-01-01)
('2024-01-01 00:00:00', 219.2, 24.8, 2, 'Shanghai Server Room B'),
('2024-01-01 00:10:00', 217.5, 24.9, 2, 'Shanghai Server Room B'),  -- Minimum voltage
('2024-01-01 00:20:00', 220.8, 25.2, 2, 'Shanghai Server Room B'),
('2024-01-01 00:30:00', 221.5, 25.5, 2, 'Shanghai Server Room B'),
('2024-01-01 00:40:00', 223.0, 25.8, 2, 'Shanghai Server Room B'),  -- Maximum voltage
('2024-01-01 00:50:00', 220.3, 25.6, 2, 'Shanghai Server Room B'),
('2024-01-01 01:00:00', 219.8, 25.3, 2, 'Shanghai Server Room B'),

-- Insert data to device 3 (2024-01-01)
('2024-01-01 00:00:00', 221.0, 26.0, 3, 'Guangzhou Server Room C'),
('2024-01-01 00:10:00', 220.5, 26.2, 3, 'Guangzhou Server Room C'),
('2024-01-01 00:20:00', 219.0, 26.5, 3, 'Guangzhou Server Room C'),  -- Minimum voltage
('2024-01-01 00:30:00', 221.8, 26.8, 3, 'Guangzhou Server Room C'),
('2024-01-01 00:40:00', 224.2, 27.0, 3, 'Guangzhou Server Room C'),  -- Maximum voltage
('2024-01-01 00:50:00', 222.5, 26.7, 3, 'Guangzhou Server Room C'),
('2024-01-01 01:00:00', 221.3, 26.4, 3, 'Guangzhou Server Room C'),

-- Cross-day data (2024-01-02, for conditional query testing)
('2024-01-02 00:00:00', 220.0, 25.0, 1, 'Beijing Server Room A'),
('2024-01-02 00:10:00', 219.5, 25.2, 1, 'Beijing Server Room A'),
('2024-01-02 00:00:00', 218.0, 24.5, 2, 'Shanghai Server Room B'),
('2024-01-02 00:10:00', 218.5, 24.7, 2, 'Shanghai Server Room B');
```

- **Full table query**

  The following example queries the minimum voltage value in the entire table along with its corresponding timestamp, temperature, and device ID.

  ```sql
  SELECT k_timestamp, temperature, device_id, min(voltage) FROM sensors;
  ```

  Expected result:

  ```sql
          k_timestamp        | temperature | device_id |  min
  ----------------------------+-------------+-----------+--------
    2024-01-01 00:10:00+00:00 |        24.9 |         2 | 217.5
  (1 row) 
  ```

- **Conditional query**

  The following example queries data for January 1, 2024, returning the minimum voltage value and its corresponding information.

  ```sql
  SELECT k_timestamp, temperature, device_id, min(voltage) 
  FROM sensors 
  WHERE k_timestamp >= '2024-01-01' AND k_timestamp < '2024-01-02';
  ```

  Expected result:

  ```sql
          k_timestamp        | temperature | device_id |  min
  ----------------------------+-------------+-----------+--------
    2024-01-01 00:10:00+00:00 |        24.9 |         2 | 217.5
  (1 row)
  ```

- **Grouped query**

  The following example groups data by device and queries the minimum voltage and corresponding information for each device.

  ```sql
  SELECT device_id, k_timestamp, temperature, min(voltage) 
  FROM sensors 
  GROUP BY device_id
  ORDER BY device_id;
  ```

  Expected result:

  ```sql
    device_id |        k_timestamp        | temperature |  min
  ------------+---------------------------+-------------+--------
            1 | 2024-01-01 00:30:00+00:00 |        26.1 | 218.5
            2 | 2024-01-01 00:10:00+00:00 |        24.9 | 217.5
            3 | 2024-01-01 00:20:00+00:00 |        26.5 |   219
  (3 rows)  
  ```

- **Time window grouped query**

  The following example groups data by 10-minute time windows and queries the minimum voltage value and its corresponding context data for each time window.

  ```sql
  SELECT first(k_timestamp) as window_start,
         last(k_timestamp) as window_end,
         k_timestamp,
         voltage,
         device_id,
         min(voltage)
  FROM sensors 
  GROUP BY time_window(k_timestamp, '10min')
  ORDER BY window_start DESC;
  ```

  Expected result:

  ```sql
          window_start        |        window_end         |        k_timestamp        | voltage | device_id |  min
  ----------------------------+---------------------------+---------------------------+---------+-----------+--------
    2024-01-02 00:10:00+00:00 | 2024-01-02 00:20:00+00:00 | 2024-01-02 00:10:00+00:00 |   218.5 |         2 | 218.5
    2024-01-02 00:00:00+00:00 | 2024-01-02 00:10:00+00:00 | 2024-01-02 00:00:00+00:00 |     218 |         2 |   218
    2024-01-01 01:00:00+00:00 | 2024-01-01 01:10:00+00:00 | 2024-01-01 01:00:00+00:00 |   219.8 |         2 | 219.8
    2024-01-01 00:50:00+00:00 | 2024-01-01 01:00:00+00:00 | 2024-01-01 00:50:00+00:00 |   220.3 |         2 | 220.3
    2024-01-01 00:40:00+00:00 | 2024-01-01 00:50:00+00:00 | 2024-01-01 00:40:00+00:00 |     220 |         1 |   220
    2024-01-01 00:30:00+00:00 | 2024-01-01 00:40:00+00:00 | 2024-01-01 00:30:00+00:00 |   218.5 |         1 | 218.5
    2024-01-01 00:20:00+00:00 | 2024-01-01 00:30:00+00:00 | 2024-01-01 00:20:00+00:00 |     219 |         3 |   219
    2024-01-01 00:10:00+00:00 | 2024-01-01 00:20:00+00:00 | 2024-01-01 00:10:00+00:00 |   217.5 |         2 | 217.5
    2024-01-01 00:00:00+00:00 | 2024-01-01 00:10:00+00:00 | 2024-01-01 00:00:00+00:00 |   219.2 |         2 | 219.2
  (9 rows)
  ```