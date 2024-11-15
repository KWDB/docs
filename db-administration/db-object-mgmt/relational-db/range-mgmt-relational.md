---
title: 数据分片管理
id: range-mgmt-relational
---

# 数据分片管理

KWDB 将所有用户数据和几乎所有系统数据存储在排序的键值对映射中。这个键空间被划分为多个键空间中的连续块，即数据分片（range）。每个键始终可以在单个数据分片内找到。 从 SQL 的角度来看，表最初会映射到单个数据分片，数据分片中的每个键值对对应表中的一行。数据分片的大小达到 512 MiB后，系统会自动将其拆分为两个数据分片。随着表的增长，新生成的数据分片也会继续进行类似的拆分操作。当用户数据减少时，数据分片会自动合并。注意：由于 KWDB 采用标记删除的方式处理数据删除，数据分片不会立即合并，只有在垃圾回收过程中实际删除数据后，数据分片才会合并。

## 查看数据分片

`SHOW RANGES` 语句用于显示数据库、表、索引的数据分片信息，验证 SQL 数据如何映射到基础数据分片以及数据分片副本的位置。

### 前提条件

用户为 Admin 用户或者 Admin 角色成员。默认情况下，root 用户具有 Admin 角色。

### 语法格式

```sql
SHOW RANGES FROM [TABLE <table_name> | INDEX <table_name> @ <index_name> | DATABASE <database_name>];
```

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

- 查看数据库的数据分片。

    以下示例查看 `db3` 数据库的数据分片。

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
