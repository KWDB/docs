---
title: 时序数据库管理
id: db-mgmt-ts
---

# 时序数据库管理

## 创建数据库

### 前提条件

用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。创建成功后，用户拥有该数据库的全部权限。

### 语法格式

```sql
CREATE TS DATABASE <db_name> [RETENTIONS <keep_duration>] [COMMENT [=] <'comment_text'>];
```

### 参数说明

:::warning 说明
- 配置可选参数时，必须严格按照 `[RETENTIONS <keep_duration>] [COMMENT [=] <'comment_text'>]` 的顺序，否则系统将会报错。
- 3.0.0 版本数据库分区间隔仅支持 10 天，其他配置值无效。

:::

| 参数 | 说明 |
| --- | --- |
| `db_name` | 待创建的数据库的名称。该名称必须唯一，且遵循[数据库标识符规则](../../sql-reference/sql-identifiers.md)。目前，数据库名称不支持中文字符，最大长度不能超过 63 个字节。|
| `keep_duration` | 可选参数，设置数据库的数据生命周期。数据超过此时长后将被系统自动清除。<br>默认值： `0s`（永久保留）<br>时间单位：<br>- 秒：`s` 或 `second`<br>- 分钟：`m` 或 `minute`<br>- 小时：`h` 或 `hour`<br>- 天：`d` 或 `day`<br>- 周：`w` 或 `week`<br>- 月：`mon` 或 `month`<br>- 年：`y` 或 `year`<br>取值范围：正整数，上限为 1000 年<br>**说明：**<br>- 表级设置优先于库级设置。<br>- 保留时长越长，存储空间占用越大，请根据业务需求合理配置。<br>- 如果待写入的数据已超过生命周期限制，系统会直接丢弃该数据，不予写入。|
| `comment_text` | 可选参数。指定数据库的注释信息。 |

### 语法示例

- 创建数据库。

    以下示例创建一个名为 `ts_db` 的数据库。

    ```sql
    CREATE TS DATABASE ts_db;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
    CREATE TS DATABASE
    ```

- 创建数据库时，指定数据库的生命周期。

    以下示例创建一个名为 `ts_db_temp` 的数据库，并将数据库的生命周期设置为 `50d`。

    ```sql
    CREATE TS DATABASE ts_db_temp RETENTIONS 50d;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
    CREATE TS DATABASE
    ```

- 创建数据库时，指定数据库的注释信息。

    以下示例创建一个名为 `ts_db_power` 的数据库，并将数据库的注释信息设置为 `database for power statistics`。

    ```sql
    CREATE TS DATABASE ts_db_power COMMENT = 'database for power statistics';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
    CREATE TS DATABASE
    ```

## 查看数据库

### 前提条件

无

### 语法格式

```sql
SHOW DATABASES [WITH COMMENT];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `WITH COMMENT` | 可选关键字，查看数据库的注释信息。默认情况下，数据库的注释信息为 `NULL`。|

### 语法示例

:::warning 说明
时序数据库和关系数据库的 `engine_type` 分别为 `TIME SERIES` 和 `RELATIONAL`。
:::

- 查看已创建的数据库。

    以下示例查看已创建的数据库。

    ```sql
    SHOW DATABASES;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      database_name  |   engine_type 
    -----------------+-------------------        
      defaultdb      | RELATIONAL
      postgres       | RELATIONAL
      system         | RELATIONAL
      ts_db          | TIME SERIES
    (4 rows)
    ```

- 查看已创建数据库的注释信息。

    以下示例查看数据库的注释信息。

    ```sql
    SHOW DATABASES WITH COMMENT;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      database_name       | engine_type |            comment
    ----------------------+-------------+--------------------------------
      defaultdb           | RELATIONAL  | NULL
      postgres            | RELATIONAL  | NULL
      ts_db               | TIME SERIES | database for power statistics
      system              | RELATIONAL  | NULL
    (4 rows)
    ```

## 查看数据库的建库语句

`SHOW CREATE DATABASE` 语句用于查看创建数据库的 SQL 语句以及创建数据库时指定的相关参数。

时序数据库支持查看创建数据库时使用的数据库名称、以及生命周期 `retentions` 参数的取值。创建数据库时，如果指定 `retentions` 的取值，则显示指定的取值。如未指定，则显示该参数的默认值 `0s`。

### 前提条件

无

### 语法格式

```sql
SHOW CREATE DATABASE <database_name>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `database_name` | 待查看数据库的名称。|

### 语法示例

以下示例查看 `tsdb1` 数据库的建库语句和相关参数取值。

```sql
-- 1. 创建数据库 tsdb1，并将 `retentions` 参数的取值设置为 `10d`。

CREATE TS DATABASE tsdb1 RETENTIONS 10d;

--2. 查看已创建的 tsdb1 数据库。

SHOW CREATE DATABASE tsdb1;
  database_name |       create_statement
----------------+-------------------------------
  tsdb1         | CREATE TS DATABASE tsdb1
                |      retentions 864000s
                |      partition interval 10d
(1 row)
```

## 切换数据库

### 前提条件

无

### 语法格式

```sql
USE <db_name>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `db_name` | 待使用的数据库的名称。|

### 语法示例

以下示例将 `ts_db` 数据库设置为当前数据库。

```sql
USE ts_db;
```

## 修改数据库

KWDB 支持修改数据库的名称、生命周期和区域配置。

### 前提条件

- 修改数据库的名称
  - 用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。
  - 目标数据库不是当前数据库。
- 修改数据库生命周期
  - 用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。
- 修改数据库区域设置
  - 修改系统数据库区域配置：用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。
  - 修改其他数据库区域配置：用户是 `admin` 角色的成员或者拥有目标数据库的 CREATE 或 ZONECONFIG 权限。默认情况下，`root` 用户属于 `admin` 角色。

### 语法格式

- 修改数据库名称

    ```sql
    ALTER DATABASE <old_name> RENAME TO <new_name>;
    ```

- 修改数据生命周期

    ```sql
    ALTER TS DATABASE <db_name> SET RETENTIONS = <keep_duration>;
    ```

- 修改数据库区域配置
  
  ```sql
  ALTER DATABASE <db_name> CONFIGURE ZONE 
  [USING <variable> = [COPY FROM PARENT | <value>], <variable> = [<value> | COPY FROM PARENT], ... | DISCARD];
  ```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `old_name` | 当前数据库的名称。|
| `new_name` | 拟修改的数据库名称，新数据库名称必须唯一，并且[遵循数据库标识符规则](../../sql-reference/sql-identifiers.md)。目前，数据库名称不支持中文字符，最大长度不能超过 63 个字节。|
| `db_name` | 待修改的数据库名称。|
| `keep_duration` | 可选参数，设置数据库的数据生命周期。数据超过此时长后将被系统自动清除。<br>默认值： `0s`（永久保留）<br>时间单位：<br>- 秒：`s` 或 `second`<br>- 分钟：`m` 或 `minute`<br>- 小时：`h` 或 `hour`<br>- 天：`d` 或 `day`<br>- 周：`w` 或 `week`<br>- 月：`mon` 或 `month`<br>- 年：`y` 或 `year`<br>取值范围：正整数，上限为 1000 年<br>**说明：**<br>- 表级设置优先于库级设置。<br>- 保留时长越长，存储空间占用越大，请根据业务需求合理配置。<br>- 如果待写入的数据已超过生命周期限制，系统会直接丢弃该数据，不予写入。|
| `variable` | 要修改的变量名，支持修改以下变量：<br>- `range_min_bytes`：数据分片的最小大小，单位为字节。数据分片小于该值时，KWDB 会将其与相邻数据分片合并。默认值：256 MiB，设置值应大于 1 MiB（1048576 字节），小于数据分片的最大大小。 <br>- `range_max_bytes`：数据分片的最大大小，单位为字节。数据分片大于该值时，KWDB 会将其切分到两个数据分片。默认值： 512 MiB。设置值不得小于 5 MiB（5242880 字节）。<br>- `num_replicas`：副本数量。默认值为 3。`system` 数据库、`meta`、`liveness` 和 `system` 数据分片的默认副本数为 5。 **注意**：集群中存在不可用节点时，副本数量不可缩减。<br>- `constraints`：副本位置的必需（+）和/或禁止（-）约束。例如 `constraints = '{"+region=NODE1": 1, "+region=NODE2": 1, "+region=NODE3": 1}'` 表示在节点 1、2 和 3 上必须各放置 1 个副本。目前只支持 `region=NODEx` 格式。 <br> - `lease_preferences`：主副本位置的必需（+）和/或禁止（-）约束的有序列表。例如 `lease_preferences = '[[+region=NODE1]]'` 表示倾向将主副本放置在节点 1。如果不能满足首选项，KWDB 将尝试下一个优先级。如果所有首选项都无法满足，KWDB 将使用默认的租约分布算法，基于每个节点已持有的租约数量来决定租约位置，尝试平衡租约分布。列表中的每个值可以包含多个约束。<br>- `ts_merge.days`：时序数据分片合并时间。同一个时序表同哈希点按照时间戳分裂后，超过该时间的数据分片将自动合并，且合并后不会再自动拆分。默认值：10（10天）。设置值必须大于等于 0，设置值为 0 时表示时序数据分片按照时间戳分裂后便立刻自动合并。系统数据分片数量过多导致出现网络等故障时可以将该值适当调小，以缓解数据过大的问题。<br><br>**提示**：<br>- 租约偏好不必与 `constraints` 字段共享，用户可以单独定义 `lease_preferences`。<br>- 设置 `constraints` 时需要同步设置 `num_replicas`，且 `constraints` 数量需要小于等于 `num_replicas` 数量。`constraints` 中的顺序无影响。<br>- KWDB 默认只根据哈希点拆分数据分片，因此数据分片按时间合并功能默认关闭，如需支持按时间合并数据分片，需将 `kv.kvserver.ts_split_interval` 实时参数设置为 `1`, 将 `kv.kvserver.ts_split_by_timestamp.enabled` 实时参数设置为 `true` 以支持按照哈希点和时间戳拆分数据分片。|
| `value` | 变量值。 |
|`COPY FROM PARENT`| 使用父区域的设置值。|
|`DISCARD` | 移除区域配置，采用默认值。|

### 语法示例

- 修改数据库的名称。

    以下示例将 `ts_db` 数据库重命名为 `tsdb`。

    ```sql
    ALTER DATABASE ts_db RENAME TO tsdb;
    ```

- 修改数据库的生命周期。

    以下示例将 `tsdb` 数据库的生命周期设置为 `10 day`。

    ```sql
    ALTER TS DATABASE tsdb SET RETENTIONS = 10 day;
    ```

- 修改数据库的区域配置。
  
    以下示例将 `tsdb` 数据库的副本数改为 5 个。

    ```sql
    -- 1. 修改区域配置
    ALTER DATABASE tsdb CONFIGURE ZONE USING num_replicas = 5;
    CONFIGURE ZONE 1

    -- 2. 查看修改是否成功
    SHOW ZONE CONFIGURATION FOR DATABASE tsdb;
        target     |              raw_config_sql
    ----------------+-------------------------------------------
      DATABASE tsdb | ALTER DATABASE tsdb CONFIGURE ZONE USING
                    |     range_min_bytes = 134217728,
                    |     range_max_bytes = 536870912,
                    |     gc.ttlseconds = 90000,
                    |     num_replicas = 5,
                    |     constraints = '[]',
                    |     lease_preferences = '[]'
    (1 row)
    ```

## 删除数据库

`DROP DATABASE` 语句用于删除目标数据库。删除成功后，所有用户针对目标数据库和其对象的所有权限均被删除。

::: warning 说明
删除时序库时，系统检查当前时序库是否被流计算引用。如果是，则输出错误消息并列出所有引用此时序库的流计算名称。用户可以使用 `CASCADE` 关键字级联删除时序库及相关的流计算。
:::

### 前提条件

- 用户是 `admin` 角色的成员或者拥有目标数据库及对象的 DROP 权限。默认情况下，`root` 用户属于 `admin` 角色。删除成功后，所有用户针对目标数据库和其对象的所有权限均被删除。
- 目标数据库不能是当前数据库。如需删除当前数据库，使用 `USE <database_name>` 语句将当前数据库切换成其他数据库，再进行删除。

### 语法格式

```sql
DROP DATABASE [IF EXISTS] <db_name> [CASCADE];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF EXISTS` | 可选关键字。当使用 `IF EXISTS` 关键字时，如果目标数据库存在，系统删除目标数据库。如果目标数据库不存在，系统删除数据库失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果目标数据库存在，系统删除目标数据库。如果目标数据库不存在，系统报错，提示目标数据库不存在。 |
| `db_name` | 待删除的数据库的名称。|
| `CASCADE` | 可选关键字，表示级联删除，即删除数据库中的所有表。`CASCADE` 关键字不会列出待删除的关联对象，应谨慎使用。|

### 语法示例

以下示例使用 `CASCADE` 关键字删除 `tsdb` 数据库及其级联对象。

```sql
-- 1. 查看 tsdb 数据库中的时序表。

SHOW TABLES FROM tsdb;
  table_name  |    table_type
--------------+--------------------
  sensor_data | TIME SERIES TABLE
  temp        | TIME SERIES TABLE
  water       | TIME SERIES TABLE
(3 rows)

-- 2. 删除 tsdb 数据库及其级联对象。

DROP DATABASE tsdb CASCADE;
DROP DATABASE

-- 3. 查看 tsdb 数据库中的时序表。

SHOW TABLES FROM tsdb;
ERROR: target database or schema does not exist
```
