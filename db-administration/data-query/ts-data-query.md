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

时间序列数据中，有时会存在缺失和偏离的数据，影响后续数据的使用和分析。KWDB 提供了 `time_bucket_gapfill` 函数和 `interpolate` 函数，支持用户对指定窗口间隔的数据进行时间戳对齐，插入缺失的时间戳行，并根据需要选择是否进行补值。

KWDB 的插值函数支持与以下功能联合使用：

- `LIMIT`：限制插值和补值后返回的结果集数量。
- `LIMIT...OFFSET`：限制插值和补值后返回的结果集数量，并跳过指定行数的记录。
- 子查询：包括非相关 `FROM` 子查询以及相关和非相关 `WHERE` 子查询，子查询中的表可以是时序表或关系表。
- `JOIN`：包括 `JOIN`、`FULL JOIN`、`LEFT JOIN` 和 `RIGHT JOIN`，插值查询与 `JOIN` 联合使用时，会先执行 `JOIN` 操作，然后对结果进行插值处理。
- `UNION`：包括 `UNION` 和 `UNION ALL`，插值查询与 UNION 联合使用时，每个子查询或数据集会先进行插值处理，然后再合并结果。

### 前提条件

用户拥有目标表的 SELECT 权限。

### 语法格式

- 插入缺失时间戳行但不补值

    ```sql
    SELECT time_bucket_gapfill(<timestamp_column>, <interval>) AS <alias_1> 
    FROM <table_name> 
    GROUP BY <column_list_1> 
    [ORDER BY <column_list_2>] 
    [LIMIT <n>] 
    [OFFSET <m>];
    ```

- 插入缺失时间戳行并进行补值

    ```sql
    SELECT time_bucket_gapfill(<timestamp_column>, <interval>) AS <alias_1>, 
          interpolate(<expression_1>, <expression_2>) [AS <alias_2>] 
    FROM <table_name> 
    GROUP BY <column_list_1> 
    [ORDER BY <column_list_2] 
    [LIMIT <n>] 
    [OFFSET <m>];
    ```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `timestamp_column` | 时间戳列。 |
| `interval` | 时间间隔，支持的单位包括秒（s）、分（m）、小时（h）、天（d）、周（w）、月（mon）、年（y），不支持复合时间格式，例如 `1d1h`。|
| `alias_1` | 为生成的时间桶结果起的别名，便于后续引用。|
| `table_name` | 待查询表的名称。|
| `column_list_1` | 用于分组的列或列的组合。多个列之间使用逗号（`,`）分隔。KWDB 会将除时间列外的其余列作为一组，进行组内补行，组与组之间互不影响。|
| `column_list_2` | 用于排序的列或列的组合，多个列之间使用逗号（`,`）分隔。支持添加可选的关键字 `ASC` 和 `DESC`, 指定顺序为升序或降序，默认值为 `ASC`，即升序。|
| `n` | 可选参数，指定返回结果的最大行数。|
| `m` | 可选参数，跳过前面 `m` 行结果。`OFFSET` 需与 `LIMIT` 连用。|
| `expression_1` | 补值算法，必须是聚合函数且数据类型为数值。 |
| `expression_2` | 补值模式，支持常量值（constant）、前值（prev）、后值（next）、线性值（linear）和 NULL。补值结果类型应与原始值一致。 |
| `alias_2` | 可选参数，为补值结果起的别名，便于后续引用。|

### 语法示例

以下示例假设用户已创建时序表 `t1`, `t2`, 并向表内写入对应的数值。

```sql
-- 创建表 t1, 并向表内写入数据
create table t1(time timestamp not null,  temperature DOUBLE, humidity DOUBLE) tags(device_id int not null) primary tags(device_id);
INSERT INTO t1 (time, device_id, temperature, humidity) VALUES ('2024-08-01 12:00:00', 1, 25.3, 60.2);
INSERT INTO t1 (time, device_id, temperature, humidity) VALUES ('2024-09-01 12:00:00', 2, 25.6, 60.3);

-- 创建表 t2, 并向表内写入数据
create table t2(time timestamp not null,  temperature DOUBLE, humidity DOUBLE) tags(device_id int not null) primary tags(device_id);
INSERT INTO t2 (time, device_id, temperature, humidity) VALUES ('2024-08-01 12:00:00', 1, 25.3, 60.2);
INSERT INTO t2 (time, device_id, temperature, humidity) VALUES ('2024-09-01 12:00:00', 2, 25.6, 60.3);
```

- 插入缺失的时间戳行但不补值。

    以下示例对 `t1` 表进行插值查询，但不补值。

    ```sql
    SELECT time_bucket_gapfill (timestamp, 600) AS tt FROM t1 GROUP BY tt ORDER BY tt;
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

- 插入缺失的时间戳行并使用前值补值。

    以下示例对 `t1` 表进行插值查询，并使用前值（PREV）补值。

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

- 插入缺失的时间戳行，使用常量补值，并使用 `limit` 和 `offset` 限制补值后返回的结果集。

    以下示例对 `t1` 表进行插值查询，使用常量补值后，限制返回的结果为 8 行，同时跳过前两行结果。

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

- 插值查询与 `FROM` 子查询联合使用。

    以下示例在子查询中先对原始数据进行每日（1 day）的分组和插值操作，然后在外层查询中按两天（2 day）的时间窗口再次进行分组和插值操作。

    ```sql
    select time_bucket_gapfill(tt, 2 * 86400) as c,interpolate(count(b), null) from (select time_bucket_gapfill(time,86400) as tt,interpolate(max(device_id),linear) as b from t1 group by tt order by tt ) group by c order by c;
                  c             | interpolate
    ----------------------------+--------------
      2024-08-01 00:00:00+00:00 |           1
    (1 row)
    ```

- 插值查询与 `WHERE` 子查询联合使用。

    以下示例先找出 `t1` 表中最大的时间戳，然后筛选出 `t1` 表中所有时间戳大于该最大时间戳的记录。

    ```sql
    select * from t1 where time> (select time_bucket_gapfill(time,86400) as tb from t1 group by tb order by tb desc limit 1) order by time;
    time                   |temperature|humidity|device_id|
    -----------------------|-----------|--------|---------|
    2024-09-01 12:00:00.000|       25.6|    60.3|        2|
    (1 row)
    ```

- 使用联合查询各自补值后再合并结果。

    以下示例将两个表 t1 和 t2 的插值结果合并。

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