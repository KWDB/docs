---
title: 时序数据查询
id: ts-data-query
---

# 时序数据查询

时序数据库支持使用 SQL 语句执行简单查询、嵌套查询、关联查询、联合查询和插值查询。


## 创建查询

### 前提条件

用户拥有目标表的 SELECT 权限。

### 语法格式

有关时序数据查询的语法格式，参见 [SQL 参考](../../sql-reference/dml/ts-db/ts-select.md#语法格式)。

### 参数说明

有关时序数据查询的参数说明，参见 [SQL 参考](../../sql-reference/dml/ts-db/ts-select.md#参数说明)。

### 语法示例

- 查询时序表的数据。

    以下示例假设经创建 `ts_db` 数据库。以下示例查询 `t1` 时序表的数据。

    ```sql
    -- 1. 创建 t1 时序表并写入数据。

    CREATE TABLE ts_db.t1(ts timestamp not null,a int, b int) tags(tag1 int not null, tag2 int) primary tags(tag1);
    CREATE TABLE

    -- 2. 向表中写入数据。

    INSERT INTO ts_db.t1 VALUES(now(),11,11,33,44);
    INSERT INTO ts_db.t1 VALUES(now(),22,22,33,44);
    INSERT INTO ts_db.t1 VALUES(now(),11,33,33,44);
    INSERT INTO ts_db.t1 VALUES(now(),22,44,33,44);
    INSERT INTO ts_db.t1 VALUES(now(),33,55,44,44);
    INSERT INTO ts_db.t1 VALUES(now(),22,44,44,44);
    INSERT INTO ts_db.t1 VALUES(now(),33,44,55,44);
    INSERT INTO ts_db.t1 VALUES(now(),null,null,66,66);
    INSERT INTO ts_db.t1 VALUES(now(),null,null,66,77);

    -- 3. 查看表的内容。

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

- 查询指定的数据列。

    以下示例查询 `t1` 表的 `a` 列并进行求和。

    ```sql
    SELECT sum(a) FROM ts_db.t1;
      sum
    -------
      154
    (1 row)
    ```

- 去重查询。

    以下示例对 `t1` 表的 `a` 列进行去重查询。

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

- 使用 `WHERE` 语句过滤标签列。

    以下示例使用 `WHERE` 语句过滤 `t1` 表的 `a` 列。

    ```sql
    SELECT tag1 FROM ts_db.t1 WHERE a =11;
      tag1
    --------
        33
        33
    (2 rows)
    ```

- 使用 `GROUP BY` 和 `ORDER BY` 语句对数据列进行分类和排序。

    以下示例使用 `GROUP BY` 语句对 `t1` 表的 `a` 列进行分类和排序。

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

## 插值查询

时间序列数据有时会存在缺失和偏离的数据，影响后续数据的使用和分析。插值查询可以实现对指定窗口间隔的数据进行时间戳对齐，插入缺失的时间戳行，并选择是否进行补值。

如需插值查询，需要使用 `time_bucket_gapfill` 函数和 `GROUP BY` 语句。如需查询其他时间窗口的数据，需要使用聚合函数。如果选择补值，需要使用 `interpolate` 函数。

### 前提条件

用户拥有目标表的 SELECT 权限。

### 语法格式

- 插入缺失的时间戳行但不补值

    ```sql
    SELECT time_bucket_gapfill (<timestamp_column>, <interval>) AS <alias> FROM <table_name> GROUP BY <alias> [ORDER BY <alias>];
    ```

- 插入缺失的时间戳行并进行补值

    ```sql
    SELECT time_bucket_gapfill (<timestamp_column>, <interval>) AS <alias> interpolate (expression_1, expression_2) FROM <table_name> GROUP BY <alias> [ORDER BY <alias>];
    ```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `timestamp_column` | 时间戳列。 |
| `interval` | 指定时间间隔，支持的单位包括秒（s）、分（m）、小时（h）、天（d）、周（w）、月（mon）、年（y）。目前，KWDB 不支持复合时间格式，例如 `1d1h`。|
| `alias` | 为生产的时间桶结果起的别名，便于后续引用。|
| `expression_1` |  补值算法，必须是聚合函数且数据类型为数字。 |
| `expression_2` | 补值模式，支持常量值（constant）、前值（prev）、后值（next）、线性值（linear）和 NULL。补值结果类型应与原始值一致。 |
| `table_name` | 待查询表的名称。|

### 语法示例

- 插入缺失的时间戳行但不补值。

    以下示例对 `t1` 表进行插值查询，但不补值。

    ```sql
    SELECT time_bucket_gapfill (timestamp, 600) AS a FROM t1 GROUP BY a ORDER BY a;
    time_bucket_gapfill
    ---------------------------
    2022-11-04 19:20:00
    2022-11-04 19:30:00
    2022-11-04 19:40:00
    2022-11-04 19:50:00
    2022-11-04 20:00:00
    2022-11-04 20:10:00
    (6 rows)
    ```

- 插入缺失的时间戳行并使用前值进行补值。

    以下示例对 `t1` 表进行插值查询，并使用前值进行补值。

    ```sql
    SELECT time_bucket_gapfill(timestamp, 600) AS a, interpolate(avg(e6), PREV) FROM t1 GROUP BY a ORDER BY a;
    time_bucket_gapfill    | interpolate
    -----------------------+---------------
    2022-11-04   19:20:00  | 499.999
    2022-11-04   19:30:00  | 499.999
    2022-11-04   19:40:00  | 99.999
    2022-11-04   19:50:00  | 99.999
    2022-11-04   20:00:00  | 177.999
    2022-11-04   20:10:00  | 20.999
    (6 rows)
    ```

- 插入缺失的时间戳行并使用常量进行补值。

    以下示例对 `t1` 表进行插值查询，并使用常量进行补值。

    ```sql
    SELECT time_bucket_gapfill(timestamp, 600) AS a, interpolate(avg(e6), '40') FROM t1 GROUP BY a ORDER BY a;
    time_bucket_gapfill  | interpolate
    ---------------------+---------------
    2022-11-04 19:20:00  |   499.999
    2022-11-04 19:30:00  |   40
    2022-11-04 19:40:00  |   99.999
    2022-11-04 19:50:00  |   40
    2022-11-04 20:00:00  |   177.999
    2022-11-04 20:10:00  |   20.999
    (6 rows)
    ```