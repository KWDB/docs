---
title: SQL 跨模查询性能调优
id: sql-tuning
---

# SQL 跨模查询性能调优

SQL 是一种声明性语言，是用户使用数据库的常用方式。用户可以通过 SQL 语句定义、存储、更新、查询数据等操作。一条 SQL 语句描述的应该是最终结果，而非顺序执行的步骤。SQL 调优旨在使 SQL 语句高效，在最短时间内、使用最少的资源获取查询结果，以最小的代价实现最大的效益。

KWDB 支持以下 SQL 查询性能调优方式：

- 多谓词顺序优化
- 标量子查询优化
- Inside-out 下推聚合优化
- Inside-out 下推 time_bucket 优化

用户可以使用 `ts.sql.query_opt_mode` 集群参数配置是否开启各优化功能。以下示例开启多谓词顺序优化和标量子查询优化。

```sql
SET CLUSTER SETTING ts.sql.query_opt_mode = 1100;
```

有关开启各优化功能的详细信息，参见[集群参数配置](../db-operation/cluster-settings-config.md)。

## 多谓语顺序优化

通常，在数据库查询中，谓词用于 `SELECT` 语句中的 `WHERE` 子句或者 `HAVING` 子句中，筛选出满足特定条件的数据行。多谓词顺序优化指的是针对查询语句中的多个过滤条件，根据谓词选择率调整谓词顺序，使得尽可能少的执行过滤条件，减少查询的数据集大小，从而提高查询的效率。

通常情况下，系统自上向下遍历过滤表达式，基于统计信息计算每个条件的选择率。用户需要手动建立统计信息。建议为表和列都建立统计信息，这样选择率的计算结果才比较准确。如果谓词不能利用统计信息，系统将采用默认的选择率计算每个条件的选择率，优化效果可能不如预期。

目前，KWDB 只针对 `AND` 和 `OR` 表达式进行了优化，针对 `AND` 和 `OR` 左右的过滤条件计算选择率。

- 对于 `AND` 表达式，选择率高的过滤条件放在表达式的右树。
- 对于 `OR` 表达式，选择率高的过滤条件放在表达式的左树。

例如，对于 `SELECT * FROM <table_name> WHERE A AND B` 语句，如果 条件 B 为 `false` 的概率比条件 A 为 `false` 的概率高，则将条件 B 调整到条件 A 的前面。调整后的 SQL 语句为 `SELECT * FROM <table_name> WHERE B AND A`。这样执行查询的时候，如果条件 B 为 `false`，则不再执行后续的条件 A 查询。

同理，对于 `SELECT * FROM <table_name> WHERE C OR D` 语句，如果 条件 D 为 `true` 的概率比条件 C 为 `true` 的概率高，则将条件 D 调整到条件 C 的前面，调整后的 SQL 语句为 `SELECT * FROM <table_name> WHERE D OR C`。这样执行查询的时候，如果条件 D 为 `true`，则不再执行后续的条件 C 查询。

## 标量子查询优化

标量子查询（Scalar Subquery）是一种特殊的子查询，它返回单个值作为结果。标量子查询通常嵌套在另一个查询的 `SELECT` 列表、`WHERE` 子句、`HAVING` 子句或表达式中，返回一个确定的值。

标量子查询优化指的是在下推逻辑中将投影层和过滤层的标量子查询下推的限制放开。系统先对标量子查询进行物理计划构建与执行，获取到标量子查询的结果，然后对主查询进行物理计划构建。构建时，系统会将标量子查询替换成值，再执行主查询。

## Inside-out 优化

在跨模查询中，Inside 指跨模场景中的时序端，Outside 指跨模场景中的关系端。Inside-out 优化指跨模场景中，由时序端发起的优化。当跨模场景中需要内连接（`INNER JOIN`）关联查询数据时，若符合分组（`GROUP BY`）和关联查询（`JOIN ON`）前提条件，时序相关的查询操作下推至时序引擎执行，减少数据传输和编码量，提升查询效率。

Inside-out 优化包括 Inside-out 下推聚合优化和 Inside-out 下推 time_bucket 优化两种方式。这两种方式都必须满足一定的前提条件，才能实查询优化。Inside-out 下推聚合优化和 Inside-out 下推 time_bucket 优化对分组（`GROUP BY`） 和关联查询（`JOIN ON`）的要求基本一致。只是对于 Inside-out 下推 time_bucket 优化而言，`GROUP BY` 列可以是时序表的单个标签列，也可以是 `time_bucket` 列。

- 分组（`GROUP BY`）
  - 跨模查询未使用 `GROUP BY` 子句对查询结果进行分组，直接对时序表和关系表的关联查询结果进行聚合操作，例如 `SELECT MAX(ts.e1) FROM ts, re WHERE ts.tag1 = re.id;`。
  - 跨模查询使用 `GROUP BY` 子句对查询结果进行分组时，对于 Inside-out 下推聚合优化，`GROUP BY` 列只支持时序表的单个标签列，例如 `SELECT MAX(ts.e1) FROM ts, re WHERE ts.tag1 = re.tag1 GROUP BY tag1;`。对于 Inside-out 下推 time_bucket 优化，`GROUP BY` 列可以是时序表的单个标签列，也可以是 `time_bucket` 列。
- 关联查询（`JOIN ON`）
  - 必须为内连接（`INNER JOIN`）关联查询，且连接条件为时序表单标签列和关系表单列的等值连接。若有多个连接条件，则需要 `AND` 连接。
  - 关联查询的关系对象为一张关系单表或关系结果表，时序对象为一张时序单表或时序单表不带 `GROUP BY` 的子查询。
  - 多表关联查询时，只允许一张时序表，但可以查询多张关系表。

KWDB 支持优化以下聚合函数。

- MAX、MIN 函数：
  - 满足分组（`GROUP BY`） 前提。
  - 满足关联查询（`JOIN ON`）前提。
  - 聚合对象不能跨模。时序数据的聚合函数在时序引擎中计算，关系数据的聚合函数在关系引擎中计算。
- COUNT、SUM、AVG 函数
  - 满足分组（`GROUP BY`） 前提。
  - 满足关联查询（`JOIN ON`）前提。
  - 聚合对象只能是时序数据。

::: warning 说明
当一条 SQL 查询语句中存在多个聚合函数，只有部分聚合函数符合优化条件时，无法优化此条 SQL 查询语句。
:::
