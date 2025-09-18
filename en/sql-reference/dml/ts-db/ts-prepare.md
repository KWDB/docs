---
title: PREPARE
id: ts-prepare
---

# PREPARE

The `PREPARE` statement ​preprocesses SQL statements, allowing the system to prepare SQL statements for subsequent execution. Once prepared, the SQL statement can be executed using the `EXECUTE` command.

KWDB supports writing data to, ​query data from, or ​delete data from specified tables​ using the `PREPARE` and `EXECUTE` statements.

::: tip

If the table's metadata (e.g., metadata changes caused by ​adding columns, ​modifying column types) changes between `PREPARE` and `EXECUTE` in KWDB, the prepared SQL statement ​may be invalid, leading to execution errors.

:::

## Privileges

- Insert data: the user must have granted the `INSERT` privilege on the specified table(s).
- Query data: the user must have granted the `SELECT` privilege on the specified table(s).
- Delete data: the user must have granted the `SELECT` and `DELETE` privileges on the specified table(s).

## Syntax

- `PREPARE`

    ![](../../../../static/sql-reference/JFsvb0ZvHo5YgZxpOMscCuUjnpe.png)

- `EXECUTE`

    ![](../../../../static/sql-reference/HYCcb1byKoCfyFxqhJ3c3c93nwb.png)

## Parameters

| Parameter | Description |
| --- | --- |
| `statement_name` | The SQL statement to preprocess. |
| `statement_sql` | The `INSERT`, `QUERY`, or `DROP` statement, in which `$<number>` is used as the placeholer, such as `$1`, `$2`. |
| `parameter_value` | The values of parameters to insert, query or delete. These values should correspond to placeholders in the `INSERT`, `QUERY`, or `DROP` statement. |

## Examples

- Insert a single row without specifiying column names.

    ```sql
    CREATE TABLE vehicle_gps_track (TIME timestamp not NULL, LATITUDE float, LONGITUDE float, ALTITUDE float, SPEED float, DIRECTION varchar) TAGS (IMEI int not null) PRIMARY TAGS (IMEI);        
    CREATE TABLE

    PREPARE p1 AS INSERT INTO vehicle_gps_track VALUES ($1,$2,$3,$4,$5,$6,$7);
    PREPARE

    EXECUTE p1 ('2024-02-06 12:00:00', 34.0522, -118.2437, 100, 60, 'North', 12345678);
    INSERT 1

    SELECT * FROM vehicle_gps_track;
                time            | latitude | longitude | altitude | speed | direction |   imei
    ----------------------------+----------+-----------+----------+-------+-----------+-----------
      2024-02-06 12:00:00+00:00 |  34.0522 | -118.2437 |      100 |    60 | North     | 12345678
    ```

- Insert multiple rows without specifiying column names.

    ```sql
    PREPARE p2 AS INSERT INTO vehicle_gps_track VALUES ($1,$2,$3,$4,$5,$6,$7),($8,$9,$10,$11,$12,$13,$14);
    PREPARE

    EXECUTE p2 ('2024-02-06 12:15:00', 40.7128, -74.0060, 150, 55, 'East', 23456789,'2024-02-06 12:30:00', 51.5074, -0.1278, 80, 70, 'West', 34567890);
    INSERT 2

    SELECT * FROM vehicle_gps_track;
                time            | latitude | longitude | altitude | speed | direction |   imei
    ----------------------------+----------+-----------+----------+-------+-----------+-----------
      2024-02-06 12:00:00+00:00 |  34.0522 | -118.2437 |      100 |    60 | North     | 12345678
      2024-02-06 12:15:00+00:00 |  40.7128 |   -74.006 |      150 |    55 | East      | 23456789
      2024-02-06 12:30:00+00:00 |  51.5074 |   -0.1278 |       80 |    70 | West      | 34567890
    (3 rows)
    ```

- Query data.

    ```sql
    PREPARE p3 AS SELECT * FROM vehicle_gps_track WHERE imei=$1;
    PREPARE

    EXECUTE p3(12345678);
                time            | latitude | longitude | altitude | speed | direction |   imei
    ----------------------------+----------+-----------+----------+-------+-----------+-----------
      2024-02-06 12:00:00+00:00 |  34.0522 | -118.2437 |      100 |    60 | North     | 12345678
    ```

- Delete data.

    ```sql
    PREPARE p4 AS DELETE FROM vehicle_gps_track WHERE imei=$1;
    PREPARE

    EXECUTE p4(12345678);
    DELETE 1

    SELECT * FROM vehicle_gps_track;
                time            | latitude | longitude | altitude | speed | direction |   imei
    ----------------------------+----------+-----------+----------+-------+-----------+-----------
      2024-02-06 12:15:00+00:00 |  40.7128 |   -74.006 |      150 |    55 | East      | 23456789
      2024-02-06 12:30:00+00:00 |  51.5074 |   -0.1278 |       80 |    70 | West      | 34567890
    (2 rows)
    ```
