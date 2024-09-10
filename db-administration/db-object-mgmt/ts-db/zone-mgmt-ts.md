---
title: 区域配置管理
id: zone-mgmt-ts
---

# 区域配置管理

## 查看区域配置

`SHOW ZONE CONFIGURATIONS` 语句用于查看指定对象的副本区域信息。

### 前提条件

无

### 语法格式

- 查看指定分区、数据库或表的副本区域信息

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
| `range_name` | 系统分区的名称。 |
| `database_name` | 数据库的名称。 |
| `table_name` | 表的名称。 |

### 语法示例

- 查看指定系统分区的副本信息
  
     以下示例查看 `default` 默认系统分区的副本区域信息
     
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
