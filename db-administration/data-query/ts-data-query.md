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

时间序列数据中，有时会存在缺失和偏离的数据，影响后续数据的使用和分析。KWDB 提供了 `time_bucket_gapfill()` 函数和 `interpolate()` 函数，支持用户对指定窗口间隔的数据进行时间戳对齐，插入缺失的时间戳行，并根据需要选择是否进行补值。

KWDB 的插值函数支持与以下功能联合使用：

- `LIMIT`：限制插值和补值后返回的结果集数量。
- `LIMIT...OFFSET`：限制插值和补值后返回的结果集数量，并跳过指定行数的记录。
- 子查询：包括非相关 `FROM` 子查询以及相关和非相关 `WHERE` 子查询，子查询中的表可以是时序表或关系表。
- `JOIN`：包括 `JOIN`、`FULL JOIN`、`LEFT JOIN` 和 `RIGHT JOIN`，插值查询与 `JOIN` 联合使用时，会先执行 `JOIN` 操作，然后对结果进行插值处理。
- `UNION`：包括 `UNION` 和 `UNION ALL`，插值查询与 UNION 联合使用时，每个子查询或数据集会先进行插值处理，然后再合并结果。

::: warning 说明

`time_bucket_gapfill()` 函数必须与 `GROUP BY` 配合使用。如果需要同时查询其他列信息，且待查询的列不在 `GROUP BY` 指定的范围内，需要使用聚合函数来处理这些列。例如，系统不支持以下查询：

```sql
SELECT time_bucket_gapfill (time, 86400) AS a, c1 FROM t1 GROUP BY a;
```

但支持使用聚合函数的查询：

```sql
SELECT time_bucket_gapfill (time, 86400) AS a, max(c1) FROM t1 GROUP BY a;
```

:::

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
| `interval` | 时间间隔，支持的单位包括纳秒、微秒、毫秒、秒、分、小时、天、周、月、年。目前，KWDB 不支持复合时间格式，如 `1d1h`。 <br> 各时间单位支持的输入格式如下所示：<br> - 纳秒：`ns`、`nsec`、`nsecs`、`nanosecond`、`nanoseconds` <br> - 微秒：`us` 、`usec`、`usecs`、`microsecond`、`microseconds` <br> - 毫秒：`ms`、`msec`、`msecs`、`millisecond`、`milliseconds` <br> - 秒：`s`、`sec`、`secs`、`second`、`seconds` <br> - 分：`m`、`min`、`mins`、`minute`、`minutes` <br> - 小时：`h`、`hr`、`hrs`、`hour`、`hours`<br> - 天：`d`、`day`、`days` <br> - 周：`w`、`week`、`weeks` <br> - 月：`mon`、`mons`、`month`、`months` <br> - 年：`y`、`yr`、`yrs`、`year`、`years`|
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
      2024-08-01 00:00:00+00:00 |           2
      2024-08-03 00:00:00+00:00 |           2
      2024-08-05 00:00:00+00:00 |           2
      2024-08-07 00:00:00+00:00 |           2
      2024-08-09 00:00:00+00:00 |           2
      2024-08-11 00:00:00+00:00 |           2
    ...
    (16 rows)
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
  
## 最值上下文查询

KWDB 的最值上下文查询功能允许用户在使用 `min` 或 `max` 聚合函数查询最小值或最大值的同时，获取该最值所在行的其他列数据。该功能突破了标准 SQL 的语法限制，使用户能够在一次查询中获得最值数据的完整上下文信息。

**使用说明：**

- 当前该功能仅支持在**单个时序表**上进行查询。
- 每次查询中只能使用 **一个** `min` 或 `max` 函数。
- 仅支持以下聚合函数：`min`、`max`、`first`、`last`，其中
  - `min` 和 `max` 不支持对标签列进行聚合。
  - `first` 和 `last` 仅支持对时间戳列进行聚合。
- `SELECT` 子句中必须包含至少一个**非聚合列**，且这些非聚合列不能完全被 `GROUP BY` 子句包含。

### 前提条件

用户拥有目标表的 SELECT 权限。

### 语法格式

  ```sql
  SELECT <non_agg_column_list>, [<min_function> | <max_function>] [, <first_function>] [, <last_function>]
  FROM <table_name>
  [WHERE <condition>]
  [GROUP BY <grouping_columns>]
  [ORDER BY <ordering_columns>];
  ```

::: warning 说明

SELECT 子句中各列顺序可以自由排列，但必须包含：

- 至少一个非聚合列
- 一个 `min_function` 或 `max_function`

:::

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `non_agg_column_list` | （必选）非聚合列列表，支持多列，每列可以是普通列名、函数表达式，或列名与函数的组合。例如：`voltage`、`round(voltage)` 等，支持所有时序数据类型，支持数学函数、字符串函数与表达式计算。|
| `min_fuction` | 最小值聚合函数，支持嵌套函数，例如 `min(voltage)`、`min(abs(voltage))`。|
| `max_function` | 最大值聚合函数，支持嵌套函数，例如 `max(temperature)`、`max(sqrt(power))`。|
| `first_fuction` | 获取条件范围内时间戳最小的数据（不包含空值 NULL）。|
| `last_function` | 获取条件范围内时间戳最大的数据（不包含空值 NULL）。|
| `table_name` | 要查询的时序表名称。|
| `grouping_columns` | 用于分组的列名，可以是普通列、表达式，时间桶函数，分组窗口函数，如时间窗口、事件窗口、计数窗口、会话窗口等。|
| `ordering_columns` | 用于排序的列名，支持多个字段，使用逗号（`,`）分隔。可添加 `ASC`（升序）或 `DESC`（降序），默认为升序。|

### 语法示例

- 全表查询

  以下示例查询整张表中电压的最小值及对应的时间戳、温度和设备 ID。

  ```sql
  SELECT k_timestamp, temperature, device_id, min(voltage) FROM sensors;
  ```

- 条件查询

  以下示例查询 2024 年 1 月 1 日的数据中，电压的最小值及对应信息。

  ```sql
  SELECT k_timestamp, temperature, device_id, min(voltage) 
  FROM sensors 
  WHERE k_timestamp >= '2024-01-01' AND k_timestamp < '2024-01-02';
  ```

- 分组查询

  以下示例按设备分组，查询每个设备的最小电压及对应信息。

  ```sql
  SELECT device_id, k_timestamp, temperature, min(voltage) 
  FROM sensors 
  GROUP BY device_id;
  ```

- 时间窗口分组查询

  以下示例按 10 分钟为单位进行时间窗口分组，查询每个时间窗口的电压最小值及其对应的上下文数据。

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