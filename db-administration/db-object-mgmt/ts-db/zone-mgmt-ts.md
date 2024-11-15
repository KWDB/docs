---
title: 区域配置管理
id: zone-mgmt-ts
---

# 区域配置管理

KWDB 将所有用户数据和几乎所有系统数据存储在排序的键值对映射中。这个键空间被划分为多个键空间中的连续块，即数据分片（range）。每个键始终可以在单个数据分片内找到。 从 SQL 的角度来看，时序表最初会映射到单个数据分片，数据分片中的每个键值对对应表中的一行。数据分片的大小达到 512 MiB后，系统会自动将其拆分为两个数据分片。随着表的增长，新生成的数据分片也会继续进行类似的拆分操作。当用户数据减少时，数据分片会自动合并。注意：由于 KWDB 采用标记删除的方式处理数据删除，数据分片不会立即合并，只有在垃圾回收过程中实际删除数据后，数据分片才会合并。

KWDB 集群中，每个数据分片都隶属于一个特定的副本区域（zone）。集群在重新平衡数据分片时，会考虑副本区域的配置，以确保遵守所有约束条件。

集群启动时，会自动生成预配置的副本区域和 `default` 副本区域。其中预配置的副本区域适用于内部系统数据，`default` 副本区域适用于集群中的其他数据。

## 查看区域配置

`SHOW ZONE CONFIGURATIONS` 语句用于查看指定对象的副本区域信息。

### 前提条件

无

### 语法格式

- 查看指定数据分片、数据库或表的副本区域信息

    ```sql
    SHOW ZONE CONFIGURATION FOR [RANGE range_name | DATABASE database_name | TABLE table_name];
    ```

- 查看所有副本区域信息

    ```sql
    SHOW [ALL] ZONE CONFIGURATIONS;
    ```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `range_name` | 系统数据分片的名称。 |
| `database_name` | 数据库的名称。 |
| `table_name` | 表的名称。 |

### 语法示例

- 查看指定系统数据分片的副本信息
  
     以下示例查看 `default` 默认系统数据分片的副本区域信息
     
     ```sql
     SHOW ZONE CONFIGURATION FOR RANGE default;
     ```
     
     执行成功后，控制台输出以下信息：
     
     ```sql
          target     |              raw_config_sql
     ----------------+-------------------------------------------
     RANGE default | ALTER RANGE default CONFIGURE ZONE USING
                    |     range_min_bytes = 268435456,
                    |     range_max_bytes = 536870912,
                    |     gc.ttlseconds = 90000,
                    |     num_replicas = 3,
                    |     constraints = '[]',
                    |     lease_preferences = '[]'
     (1 row)
     ```
     
- 查看指定数据库的副本信息
  
     以下示例查看 `db1` 数据库的副本区域信息。
     
     ```sql
     SHOW ZONE CONFIGURATION FOR DATABASE db1;
     ```
     
     执行成功后，控制台输出以下信息：
     
     ```sql
          target    |             raw_config_sql
     ---------------+------------------------------------------
     DATABASE db1 | ALTER DATABASE db1 CONFIGURE ZONE USING
                    |     range_min_bytes = 1048576,
                    |     range_max_bytes = 8388608,
                    |     gc.ttlseconds = 100000,
                    |     num_replicas = 5,
                    |     constraints = '[]',
                    |     lease_preferences = '[]'
     (1 row)
     ```
     
- 查看指定表的副本区域信息
  
     以下示例查看 `t1` 表的副本区域信息。
     
     ```sql
     SHOW ZONE CONFIGURATION FOR TABLE t1;
     ```
     
     执行成功后，控制台输出以下信息：
     
     ```sql
          target     |              raw_config_sql
     ----------------+-------------------------------------------
     RANGE default | ALTER RANGE default CONFIGURE ZONE USING
                    |     range_min_bytes = 268435456,
                    |     range_max_bytes = 536870912,
                    |     gc.ttlseconds = 90000,
                    |     num_replicas = 3,
                    |     constraints = '[]',
                    |     lease_preferences = '[]'
     (1 row)
     ```
