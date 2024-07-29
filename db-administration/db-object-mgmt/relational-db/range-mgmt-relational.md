---
title: Range 分区管理
id: range-mgmt-relational
---

# Range 分区管理

## 查看 Range 分区

`SHOW RANGES` 语句用于显示数据库、表、索引的 Range 分区信息，验证 SQL 数据如何映射到基础 Range 分区以及 Range 副本的位置。

### 前提条件

用户为 Admin 用户或者 Admin 角色成员。默认情况下，root 用户具有 Admin 角色。

### 语法格式

```sql
SHOW RANGES FROM [TABLE <table_name> | INDEX <table_name> @ <index_name> | DATABASE <database_name>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 待查看 Range 分区的表的名称。 |
| `index_name` | 待查看 Range 分区的索引的名称。 |
| `database_name` | 待查看 Range 分区的数据库的名称。 |

### 语法示例

- 查看表的 Range 分区。

    以下示例查看 `orders` 表的 Range 分区。

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

- 查看索引的 Range 分区。

    以下示例查看 `orders` 表的 `primary` 索引的 Range 分区。

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

- 查看数据库的 Range 分区。

    以下示例查看 `db3` 数据库的 Range 分区。

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

## 修改 RANGE 分区配置

除了用户可见的数据库和表之外，KWDB 在以下系统 Range 分区存储了部分内部数据，进行了区域配置。

- `meta` 系统 Range 分区：存储集群中所有数据的位置信息。其中，`num_replicas` 设置为 `5`，提高对节点故障的容错性。`gc.ttlseconds` 设置低于默认值，保证 Range 分区大小适中，确保可靠性。
- `liveness` 系统 Range 分区：存储特定时间内活动节点的信息。其中，`num_replicas` 设置为 `5`，提高对节点故障的容错性。`gc.ttlseconds` 设置低于默认值，保证 Range 分区大小适中，确保可靠性。
- `system` 系统 Range 分区：存储分配新表 ID 所需的信息以及跟踪集群节点状态。其中 `num_replicas` 设置为 `5`，提高对节点故障的容错性。
- `timeseries` 系统 Range 分区：存储集群监控数据。

### 前提条件

修改 `system` 系统 Range 分区时，用户为 Admin 用户或者 Admin 角色成员。默认情况下，root 用户属于 admin 角色。

### 语法格式

```sql
ALTER RANGE <range_name> CONFIGURE ZONE [USING <variable> = [COPY FROM PARENT | <value>], <variable> = [<value> | COPY FROM PARENT], ... | DISCARD]
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `range_name` | 待修改系统 Range 分区的名称。 |
| `variable` | 待修改的变量，KWDB 支持修改以下变量：<br > - `range_min_bytes`：区域的最小数据范围（单位：字节）。当数据范围小于该阈值时会与相邻范围合并。默认值为 `134217728`（128 MiB）。<br >- `range_max_bytes`：区域的最大数据范围（单位：字节）。数据范围达到该阈值时，KWDB 会将其切分到两个范围。默认值为`536870912` (512 MiB)。<br >- `gc.ttlseconds`：垃圾回收前，保留被覆盖的值的时间（单位：秒）。取值较小，有助于节省磁盘空间。取值较大，增加 `AS OF SYSTEM TIME` 查询允许的范围。不建议取值小于 `600` 秒（`10` 分钟），避免对长时间运行的查询产生影响。另外，由于一行的所有版本都存储在一个永不拆分的单个范围内，也不建议取值太高，避免对该行的所有更改加起来可能超过 `64` MiB，从而导致服务器内存不足或其他问题。默认值为 `90000`（`25` 小时）。<br > - `num_replicas`：区域的副本数，默认值为 `3`。对于 `system` 数据库以及 `.meta`、`.liveness` 和 `.system` 范围，默认值为 `5`。<br > - `constraints`：全能型副本位置的必需（`+`）和/或禁止（`-`）约束。<br >- `lease_preferences`：影响租约位置的必需（`+`）和/或禁止（`-`）约束的有序列表。如果不能满足第一个优先级，KWDB 将尝试满足第二个优先级，依此类推。如果不能满足所有首选项，KWDB 使用默认的租约放置算法，该算法基于每个节点已拥有的租约数量来决定租约放置。用户可以尽量让所有节点拥有大致相同数量的租约。列表中的每个值可以包含多个约束。<br > 例如，`[[+zone=zn-east-1b, +ssd], [+zone=zn-east-1a], [+zone=zn-east-1c, +ssd]]` 列表表示首选位于 `zn-east-1b` 区域具有 SSD 的节点，然后是位于 `zn-east-1a` 区域的节点，最后位于 `zn-east-1c` 区域具有 SSD 的节点。如未指定此字段，则不应用租约偏好首选项。注意，租约偏好约束无需与 `constraints` 字段共享，用户可以只定义 `lease_preferences` 而不引用 `constraints` 字段中的任何值。用户也可以不定义 `constraints` 字段而只定义 `lease_preferences`。|
| `COPY FROM PARENT` | 从父区域中复制取值。 |
| `value` | 拟修改的变量值。 |
| `DISCARD` | 移除 Range 分区配置。 |

### 语法示例

以下示例修改 `meta` 系统 Range 分区的区域配置。

::: warning 说明
修改系统 Range 分区的区域配置可能导致部分或全部集群停止工作，因此需要格外谨慎。
:::

```sql
-- 1. 修改 meta 系统 Range 分区的区域配置。

ALTER RANGE meta CONFIGURE ZONE USING num_replicas = 7;
ALTER RANGE 

-- 2. 查看 meta 系统 Range 分区的区域配置。

SHOW ZONE CONFIGURATION FOR RANGE meta;
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
