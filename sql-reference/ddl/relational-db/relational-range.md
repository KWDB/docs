---
title: 数据分片
id: relational-range
---

# 数据分片

KWDB 将所有用户数据（表、索引等）和几乎所有系统数据存储在键值对的排序映射中。这个键空间被划分为多个数据分片（range），即键空间的连续块，每个键始终可以在单个数据分片内找到。

从 SQL 的角度来看，表及其二级索引最初映射到单个数据分片，数据分片内的每个键值对表示表中的一行（也称为主索引）或二级索引中的一行。一旦该数据分片达到 512 MiB，就会分为两个数据分片。随着表格及其索引的不断增长，这些新数据分片将继续进行相同的操作。当用户数据减少时，数据分片会自动进行合并。注意，由于 KWDB 的关系数据采用标记删除的方式，数据删除后，数据分片不会立即合并。数据分片内的实际数据删除被垃圾回收时，才会进行数据分片合并。

KWDB 支持用户使用 SHOW RANGES 语句查看关系库、关系表和索引的数据分片信息。

## 查看数据分片

`SHOW RANGES` 语句用于显示数据库、表、索引的 Range 数据分片信息，验证 SQL 数据如何映射到基础 Range 数据分片以及 Range 副本的位置。

### 所需权限

用户为 Admin 用户或者 Admin 角色成员。默认情况下，root 用户具有 Admin 角色。

### 语法格式

![](../../../static/sql-reference/T3oHb3y7MoiSttxGFL1cjutqnve.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 待查看的表名。 |
| `index_name` | 待查看的索引名。 |
| `database_name` | 待查看的数据库名。 |

### 语法示例

- 查看表的数据分片。

    以下示例查看 `orders` 表的数据分片。

    ```sql
    SHOW RANGES FROM TABLE orders;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      start_key | end_key | range_id | range_size_mb | lease_holder | lease_holder_locality | replicas | replica_localities
    ------------+---------+----------+---------------+--------------+-----------------------+----------+---------------------
      NULL      | NULL    |      180 |      0.000077 |            1 |                       | {1}      | {""}
    (1 row)
    ```

- 查看索引的数据分片。

    以下示例查看 `orders` 表的 `primary` 索引的数据分片。

    ```sql
    SHOW RANGES FROM INDEX orders @ primary;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      start_key | end_key | range_id | range_size_mb | lease_holder | lease_holder_locality | replicas | replica_localities
    ------------+---------+----------+---------------+--------------+-----------------------+----------+---------------------
      NULL      | NULL    |      180 |      0.000077 |            1 |                       | {1}      | {""}
    (1 row)
    ```

- 查看数据库的 Range 数据分片。

    以下示例查看 `db3` 数据库的 Range 数据分片。

    ```sql
    SHOW RANGES FROM DATABASE db3;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      table_name | start_key | end_key | range_id | range_size_mb | lease_holder | lease_holder_locality | replicas | replica_localities
    -------------+-----------+---------+----------+---------------+--------------+-----------------------+----------+---------------------
      order_list | NULL      | NULL    |      185 |      0.000145 |            1 |                       | {1}      | {""}
      orders     | NULL      | NULL    |      180 |      0.000077 |            1 |                       | {1}      | {""}
      orders_seq | NULL      | NULL    |      183 |      0.000114 |            1 |                       | {1}      | {""}
    (3 rows)
    ```
