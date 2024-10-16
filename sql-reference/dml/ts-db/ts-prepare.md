---
title: PREPARE
id: ts-prepare
---

# PREPARE

`PREPARE` 语句用于预处理 SQL 语句的 SQL 命令，允许系统将 SQL 语句准备好以供后续的执行。SQL 语句准备好后，可以使用 `EXECUTE` 命令执行 SQL 语句。

KWDB 支持用户使用 `PREARE` 和 `EXECUTE` 语句向指定表写入数据、查询指定表的数据或删除指定表的数据。

::: warning 提示

在 KWDB 执行 `PREPARE` 和 `EXECUTE` 之间，如果表的元数据发生变更，如添加列、修改列类型等，准备好的 SQL 语句可能失效，导致执行时出现报错。

:::

## 所需权限

- 写入数据：用户拥有目标表的  INSERT 权限。
- 查询数据：用户拥有目标表的 SELECT 权限。
- 删除数据：用户拥有目标表的 SELECT 和 DELETE 权限。

## 语法格式

- `PREPARE`

    ![](../../../static/sql-reference/JFsvb0ZvHo5YgZxpOMscCuUjnpe.png)

- `EXECUTE`

    ![](../../../static/sql-reference/HYCcb1byKoCfyFxqhJ3c3c93nwb.png)

## 参数说明

| 参数 | 说明 |
| --- | --- |
| `statement_name` | 预处理的 SQL 语句名称。|
| `statement_sql` | `INSERT`、`QUERY` 或 `DROP` 语句，语句中使用 `$<number>` 做占位符，例如 `$1`, `$2`|
| `parameter_value` | 待写入、查询或删除的参数值。参数值需要对应`INSERT`、`QUERY` 或 `DROP` 语句中的占位符。|

## 语法示例

- 不指定列名向时序表写入一行数据。

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

- 不指定列名向时序表写入多行数据。

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

- 查询数据。

    ```sql
    PREPARE p3 AS SELECT * FROM vehicle_gps_track WHERE imei=$1;
    PREPARE

    EXECUTE p3(12345678);
                time            | latitude | longitude | altitude | speed | direction |   imei
    ----------------------------+----------+-----------+----------+-------+-----------+-----------
      2024-02-06 12:00:00+00:00 |  34.0522 | -118.2437 |      100 |    60 | North     | 12345678
    ```

- 删除数据。

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
