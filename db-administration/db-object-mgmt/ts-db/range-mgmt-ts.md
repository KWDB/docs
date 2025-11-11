---
title: 数据分片管理
id: range-mgmt-ts
---

# 数据分片管理

KWDB 将所有用户数据和几乎所有系统数据存储在排序的键值对映射中。这个键空间被划分为多个键空间中的连续块，即数据分片（range）。每个键始终可以在单个数据分片内找到。 从 SQL 的角度来看，时序表最初会映射到单个数据分片，数据分片中的每个键值对对应表中的一行。数据分片的大小达到 512 MiB后，系统会自动将其拆分为两个数据分片。随着表的增长，新生成的数据分片也会继续进行类似的拆分操作。当用户数据减少时，数据分片会自动合并。注意：由于 KWDB 采用标记删除的方式处理数据删除，数据分片不会立即合并，只有在垃圾回收过程中实际删除数据后，数据分片才会合并。

每个数据分片都隶属于一个特定的副本区域（zone）。集群在重新平衡数据分片时，会考虑副本区域的配置，以确保遵守所有约束条件。副本区域更多信息见[副本区域](./zone-mgmt-ts.md)。

KWDB 支持用户使用 `SELECT * from kwdb_internal.ranges` 语句查看时序库、表的数据分片信息，使用 `ALTER RANGE` 语句修改、移除数据分片的区域配置。

## 修改数据分片

`ALTER RANGE` 语句用于修改、移除数据分片的区域配置。

除了用户可见的数据库和表之外，KWDB 在以下系统数据分片内存储了部分内部数据，进行了副本区域配置：

- `meta`：包含集群中所有数据的位置信息，副本数设置为 5，以提高容错性，`gc.ttlseconds` 设置低于默认值，以保持数据分片大小适中，确保性能稳定。
- `liveness`：包含给定时间活动节点的信息，副本数设置为 5，以提高容错性，`gc.ttlseconds` 设置低于默认值，以保持数据分片大小适中。
- `system`：包括分配新表ID所需的信息以及追踪集群节点状态，副本数设置为5，以提高容错性。
- `timeseries`：包含集群监控数据。

::: warning 注意

修改系统数据分片的区域配置可能导致部分或全部集群停止工作，因此需要格外谨慎。
:::

### 所需权限

用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。

### 语法格式

```sql
ALTER RANGE <range_name> CONFIGURE ZONE [USING <variable> = [COPY FROM PARENT | <value>], <variable> = [<value> | COPY FROM PARENT], ... | DISCARD];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `range_name` | 待修改的数据分片名称，包括：<br>-  `default`：默认副本设置<br>- `meta`：所有数据的位置信息<br>- `liveness`：给定时间活动节点的信息 <br>- `system`：分配新表ID所需的信息以及追踪集群节点状态<br>- `timeseries`：集群监控数据|
| `variable` | 要修改的变量名，支持修改以下变量：<br>- `range_min_bytes`：数据分片的最小大小，单位为字节。数据分片小于该值时，KWDB 会将其与相邻数据分片合并。默认值：256 MiB，设置值应大于 1 MiB（1048576 字节），小于数据分片的最大大小。 <br>- `range_max_bytes`：数据分片的最大大小，单位为字节。数据分片大于该值时，KWDB 会将其切分到两个数据分片。默认值： 512 MiB。设置值不得小于 5 MiB（5242880 字节）。<br>- `gc.ttlseconds`：数据在垃圾回收前保留的时间，单位为秒。默认值为 `90000`（25 小时）。设置值建议不小于 600 秒（10 分钟），以免影响长时间运行的查询。设置值较小时可以节省磁盘空间，设置值较大时会增加 `AS OF SYSTEM TIME` 查询的时间范围。另外，由于每行的所有版本都存储在一个永不拆分的单一数据分片内，不建议将该值设置得太大，以免单行的所有更改累计超过 64 MiB，导致内存不足或其他问题。<br>- `num_replicas`：副本数量。默认值为 3。`system` 数据库、`meta`、`liveness` 和 `system` 数据分片的默认副本数为 5。 **注意**：集群中存在不可用节点时，副本数量不可缩减。<br>- `constraints`：副本位置的必需（+）和/或禁止（-）约束。例如 `constraints = '{"+region=NODE1": 1, "+region=NODE2": 1, "+region=NODE3": 1}'` 表示在节点 1、2 和 3 上必须各放置 1 个副本。目前只支持 `region=NODEx` 格式。 <br> - `lease_preferences`：主副本位置的必需（+）和/或禁止（-）约束的有序列表。例如 `lease_preferences = '[[+region=NODE1]]'` 表示倾向将主副本放置在节点 1。如果不能满足首选项，KWDB 将尝试下一个优先级。如果所有首选项都无法满足，KWDB 将使用默认的租约分布算法，基于每个节点已持有的租约数量来决定租约位置，尝试平衡租约分布。列表中的每个值可以包含多个约束。<br>- `ts_merge.days`：时序数据分片合并时间。同一个时序表同哈希点按照时间戳分裂后，超过该时间的数据分片将自动合并，且合并后不会再自动拆分。默认值：10（10天）。设置值必须大于等于 0，设置值为 0 时表示时序数据分片按照时间戳分裂后便立刻自动合并。系统数据分片数量过多导致出现网络等故障时可以将该值适当调小，以缓解数据过大的问题。<br><br>**提示**：<br>- 租约偏好不必与 `constraints` 字段共享，用户可以单独定义 `lease_preferences`。<br>- 设置 `constraints` 时需要同步设置 `num_replicas`，且 `constraints` 数量需要小于等于 `num_replicas` 数量。`constraints` 中的顺序无影响。<br>- KWDB 默认只根据哈希点拆分数据分片，因此数据分片按时间合并功能默认关闭，如需支持按时间合并数据分片，需将 `kv.kvserver.ts_split_interval` 实时参数设置为 `1`, 将 `kv.kvserver.ts_split_by_timestamp.enabled` 实时参数设置为 `true` 以支持按照哈希点和时间戳拆分数据分片。|
| `value` | 变量值。 |
|`COPY FROM PARENT`| 使用父区域的设置值。|
|`DISCARD` | 移除区域配置，采用默认值。|

### 语法示例

- 修改系统数据分片的区域配置

  以下示例将 `meta` 数据分片的副本数改为 7 个。

  ```SQL
  ALTER RANGE meta CONFIGURE ZONE USING num_replicas=7;
  ALTER RANGE 

  SHOW ZONE CONFIGURATION FOR RANGE meta;
      target   |            raw_config_sql
  -------------+----------------------------------------
    RANGE meta | ALTER RANGE meta CONFIGURE ZONE USING
              |     range_min_bytes = 268435456,
              |     range_max_bytes = 536870912,
              |     gc.ttlseconds = 3600,
              |     num_replicas = 7,
              |     constraints = '[]',
              |     lease_preferences = '[]'
  (1 row)
  ```
