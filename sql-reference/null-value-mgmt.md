---
title: NULL 值管理
id: null-value-mgmt 
---

# NULL 值管理

KWDB 支持向表中未定义 NOT NULL 的列写入 NULL 值，并支持计算和查询插入的 NULL 值。

## 插入 NULL 值

创建表时，如果表的某个列未被定义为 NOT NULL，则该列可以插入 NULL 值。

::: warning 说明
向表中写入数据时，会对表的列进行 nullablity（是否可为空值）校验。如果目标列被定义为 NOT NULL，则不能插入 NULL 值，否则系统报错。
:::

以下示例创建 `nulls` 时序表，并向表中写入 NULL 值。

```sql
-- 1. 创建时序表，允许写入 NULL 值
CREATE TABLE nulls (ts TIMESTAMP NOT NULL, power INT, speed INT) TAGS (id INT NOT NULL, site INT) PRIMARY TAGS (id);
CREATE TABLE

-- 2. 写入 NULL 值
INSERT INTO nulls VALUES ('2024-01-01 10:00:00', 10, 219, 1, 1), ('2024-01-01 10:10:00', 11, 220, 1, 1), ('2024-01-01 10:20:00', 14, 225, 1, 1), ('2024-01-01 10:30:00', NULL, 225, 1, 1), ('2024-01-01 10:40:00', NULL, NULL, 1, 1);
INSERT 5

-- 3. 查看表数据
SELECT * FROM nulls;
             ts             | power | speed | id | site
----------------------------+-------+-------+----+-------
  2024-01-01 10:00:00+00:00 |    10 |   219 |  1 |    1
  2024-01-01 10:10:00+00:00 |    11 |   220 |  1 |    1
  2024-01-01 10:20:00+00:00 |    14 |   225 |  1 |    1
  2024-01-01 10:30:00+00:00 | NULL  |   225 |  1 |    1
  2024-01-01 10:40:00+00:00 | NULL  | NULL  |  1 |    1
(5 rows)
```

## 查询 NULL 值

使用 `SELECT` 查询表数据时，如果查询结果包含 NULL 值，则会显示 NULL。

```sql
SELECT * FROM nulls;
             ts             | power | speed | id | site
----------------------------+-------+-------+----+-------
  2024-01-01 10:00:00+00:00 |    10 |   219 |  1 |    1
  2024-01-01 10:10:00+00:00 |    11 |   220 |  1 |    1
  2024-01-01 10:20:00+00:00 |    14 |   225 |  1 |    1
  2024-01-01 10:30:00+00:00 | NULL  |   225 |  1 |    1
  2024-01-01 10:40:00+00:00 | NULL  | NULL  |  1 |    1
(5 rows)
```

## NULL 值计算规则

KWDB 支持涉及聚合、算术运算等内置函数计算、查询场景时的 NULL 值计算，计算规则如下：

- 查询场景

  - 使用 SELECT 语句查询 NULL 值时，相应的 NULL 值结果显示为 NULL。

    ```sql
    SELECT * FROM nulls;
    ts             | power | speed | id | site
    ----------------------------+-------+-------+----+-------
    2024-01-01 10:00:00+00:00 |    10 |   219 |  1 |    1
    2024-01-01 10:10:00+00:00 |    11 |   220 |  1 |    1
    2024-01-01 10:20:00+00:00 |    14 |   225 |  1 |    1
    2024-01-01 10:30:00+00:00 | NULL  |   225 |  1 |    1
    2024-01-01 10:40:00+00:00 | NULL  | NULL  |  1 |    1
    (5 rows)
    ```

  - 任何值与 NULL 的简单比较运算结果都是 NULL。

    ```sql
    SELECT 1 = NULL;
    ?column?
    --------
    NULL
    
    SELECT 4 IN (1, 2, NULL);
    ?column?
    --------
    NULL
    ```

  - WHERE 条件句中使用小于号（`<`）、大于号（`>`）、等号（`=`）与 NULL 比较时，由于比较结果为 NULL（既不是 TRUE 也不是 FALSE），因此返回 0 行结果。

    ```sql
    SELECT power FROM nulls WHERE power > NULL;
    power
    ---
    Output has 0 rows
    ```

  - WHERE 条件句使用 NULL 值判断时，应使用 `IS NULL` 或 `IS NOT NULL` 语法。

    ```sql
    SELECT power FROM nulls WHERE power IS NULL;
    power
    -----
    NULL
    NULL
    ```

  - WHERE 条件句除上面 `IS NULL` 或 `IS NOT NULL` 过滤语句外，其余情况 NULL 值均不参与计算，NULL 值的行会被忽略掉。

    ```sql
    SELECT power FROM nulls WHERE power > 1;
    power
    -----
    10
    11
    14
    ```

- 聚合运算

  - 使用 `count(*)` 统计行数时，行数结果包含 NULL 值的行数。

    ```sql
    SELECT COUNT(*) FROM nulls;
    count
    ---
    5
    (5 rows)
    ```

  - SUM、AVG、COUNT、FIRST、LAST 及其它聚合函数指定列聚合运算，NULL 不参与运算。

    ```sql
    SELECT AVG(power) FROM nulls;
                avg
    -------------------------
        11.666666666666666667
    (1 row)
    ```

- 数学和数值函数

    NULL 值的四则运算、`round()`、`pow()` 等数学运算，运算结果为 NULL。

    ```sql
    SELECT power+1 FROM nulls;
    ?column?
    ---
    11
    12
    15
    NULL
    NULL
    (5 rows)
    ```

- 日期和时间函数

    `DAY()`、`DATE()`、`ADDTIME()` 等函数对 NULL 值进行计算时，结果仍为 NULL。

- 字符串函数

    LOWER、RIGHT、LOCATE 等字符串函数对 NULL 值进行计算时，结果仍为 NULL。