---
title: 数据分片管理
id: range-mgmt-relational
---

# 数据分片管理

KWDB 将所有用户数据和几乎所有系统数据存储在排序的键值对映射中。这个键空间被划分为多个键空间中的连续块，即数据分片（range）。每个键始终可以在单个数据分片内找到。 从 SQL 的角度来看，表最初会映射到单个数据分片，数据分片中的每个键值对对应表中的一行。数据分片的大小达到 512 MiB 后，系统会自动将其拆分为两个数据分片。随着表的增长，新生成的数据分片也会继续进行类似的拆分操作。当用户数据减少时，数据分片会自动合并。注意：由于 KWDB 采用标记删除的方式处理数据删除，数据分片不会立即合并，只有在垃圾回收过程中实际删除数据后，数据分片才会合并。

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

## 修改数据分片

`ALTER RANGE` 语句用于修改数据分片的副本区域配置。 除了用户可见的数据库和表之外，KWDB 在以下系统数据分片内存储了部分内部数据，进行了副本区域配置：

- `meta`：包含集群中所有数据的位置信息，副本数设置为 5，以提高容错性，`gc.ttlseconds` 设置低于默认值，以保持数据分片大小适中，确保性能稳定。
- `liveness`：包含给定时间活动节点的信息，副本数设置为 5，以提高容错性，`gc.ttlseconds` 设置低于默认值，以保持数据分片大小适中。
- `system`：包括分配新表ID所需的信息以及追踪集群节点状态，副本数设置为5，以提高容错性。
- `timeseries`：包含集群监控数据。

::: warning 注意
修改系统数据分片的区域配置可能导致部分或全部集群停止工作，因此需要格外谨慎。
:::

### 所需权限

用户为 Admin 用户或 Admin 角色成员。默认情况下，root 用户具有 Admin 角色。

### 语法格式

```sql
ALTER RANGE <range_name> CONFIGURE ZONE [USING <variable> = [COPY FROM PARENT | <value>], <variable> = [<value> | COPY FROM PARENT], ... | DISCARD];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `range_name` | 待修改的数据分片名称，包括：<br>-  `default`：默认副本设置<br>- `meta`：所有数据的位置信息<br>- `liveness`：给定时间活动节点的信息 <br>- `system`：分配新表ID所需的信息以及追踪集群节点状态<br>- `timeseries`：集群监控数据|
| `variable` | 待修改的变量名，关系库支持修改以下变量：<br> - `range_min_bytes`：数据分片的最小大小，单位为字节。数据分片小于该值时，KWDB 会将其与相邻数据分片合并。默认值：256 MiB，设置值应大于 1 MiB（1048576 字节），小于数据分片的最大大小。<br> - `range_max_bytes`：数据分片的最大大小，单位为字节。数据分片大于该值时，KWDB 会将其切分到两个数据分片。默认值： 512 MiB。设置值不得小于 5 MiB（5242880 字节）。<br> - `gc.ttlseconds`：数据在垃圾回收前保留的时间，单位为秒。默认值为 `90000`（25 小时）。设置值建议不小于 600 秒（10 分钟），以免影响长时间运行的查询。设置值较小时可以节省磁盘空间，设置值较大时会增加 `AS OF SYSTEM TIME` 查询的时间范围。另外，由于每行的所有版本都存储在一个永不拆分的单一数据分片内，不建议将该值设置得太大，以免单行的所有更改累计超过 64 MiB，导致内存不足或其他问题。<br>- `num_replicas`：副本数量。默认值为 3。`system` 数据库、`meta`、`liveness` 和 `system` 数据分片的默认副本数为 5。 **注意**：集群中存在不可用节点时，副本数量不可缩减。<br>- `constraints`：副本位置的必需（+）和/或禁止（-）约束。<br> - `lease_preferences`：租约位置的必需（+）和/或禁止（-）约束的有序列表。每个约束前可带 + 表示必需，或 - 表示禁止。注意，租约偏好不必与 `constraints` 字段共享，用户可以单独定义 `lease_preferences`，也可以单独定义 `lease_preferences`。如果不能满足首选项，KWDB 将尝试下一个优先级。如果所有首选项都无法满足，KWDB 将使用默认的租约分布算法，该算法基于每个节点已持有的租约数量来决定租约位置，尝试平衡租约分布。列表中的每个值可以包含多个约束。例如，列表 `[[+zone=zn-east-1b, +ssd], [+zone=zn-east-1a], [+zone=zn-east-1c, +ssd]]` 表示首选位于 `zn-east-1b` 区域具有 SSD 的节点，其次是位于 `zn-east-1a` 区域的节点，最后是 `zn-east-1c` 区域具有 SSD 的节点。默认值：如果未指定此字段，则不应用租约偏好。 |
| `value` | 变量值。 |
|`COPY FROM PARENT`| 使用父区域的设置值。|
|`DISCARD` | 移除区域配置，采用默认值。|

### 语法示例

- 修改系统数据分片的区域配置
  
  以下示例将 `meta` 系统数据分片的副本数改为7个。

  ```SQL
  > ALTER RANGE meta CONFIGURE ZONE USING num_replicas=7;
  ALTER RANGE 

  > SHOW ZONE CONFIGURATION FOR RANGE meta;
      target   |            raw_config_sql
  -------------+----------------------------------------
    RANGE meta | ALTER RANGE meta CONFIGURE ZONE USING
              |     range_min_bytes = 134217728,
              |     range_max_bytes = 536870912,
              |     gc.ttlseconds = 3600,
              |     num_replicas = 7,
              |     constraints = '[]',
              |     lease_preferences = '[]'
  (1 row)
  ```