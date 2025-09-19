---
title: 关系数据库管理
id: db-mgmt-relational
---

# 关系数据库管理

## 创建数据库

### 前提条件

用户具有 Admin 角色。默认情况下，root 用户具有 Admin 角色。创建成功后，用户拥有该数据库的全部权限。

### 语法格式

```sql
CREATE DATABASE [IF NOT EXISTS] <db_name> [WITH] [ENCODING [=] <'code_name'>] [COMMENT [=] <'comment_text'>];
```

### 参数说明

:::warning 说明
配置可选参数时，必须严格按照 `[ENCODING [=] <'code_name'>] [COMMENT [=] <'comment_text'>]` 的顺序，否则系统将会报错。
:::

| 参数 | 说明 |
| --- | --- |
| `IF NOT EXISTS` | 可选关键字。当使用 `IF NOT EXISTS` 关键字时，如果目标数据库不存在，系统创建目标数据库。如果目标数据库存在，系统创建数据库失败，但不会报错。当未使用 `IF NOT EXISTS` 关键字时，如果目标数据库不存在，系统创建目标数据库。如果目标数据库存在，系统报错，提示目标数据库已存在。 |
| `db_name` | 待创建的数据库的名称。该名称必须唯一，且遵循[数据库标识符规则](../../sql-reference/sql-identifiers.md)。|
| `WITH` | 可选关键字，是否使用该关键字不影响数据库的创建。 |
| `ENCODING` | 可选关键字，指定编码方式。目前，KWDB 只支持 UTF-8 编码以及 UTF-8 的别名（UTF8 和 UNICODE）。编码值应该用单引号（`''`）括起来，并且不区分大小写。例如：`CREATE DATABASE bank ENCODING = 'UTF-8'`。 |
| `COMMENT` | 可选关键字。指定数据库的注释信息。|

### 语法示例

- 创建数据库。

    以下示例创建一个名为 `db1` 的关系数据库。

    ```sql
    CREATE DATABASE db1;
    ```

- 创建数据库时，指定数据库的注释信息。

    以下示例创建一个名为 `db_student` 的关系数据库，并将数据库的注释信息设置为 `database for student statistics`。

    ```sql
    CREATE DATABASE db_student COMMENT = 'database for student statistics';
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

以下示例查看已创建的数据库。

```sql
SHOW DATABASES;
```

执行成功后，控制台输出以下信息：

```sql
  database_name | engine_type
----------------+--------------
  db1           | RELATIONAL
  db2           | RELATIONAL
  defaultdb     | RELATIONAL
  postgres      | RELATIONAL
  system        | RELATIONAL
  iot           | TIME SERIES 
 (6 rows)
```

## 查看数据库的建库语句

`SHOW CREATE DATABASE` 语句用于查看创建数据库的 SQL 语句。目前，关系数据库只支持查看创建数据库时使用的数据库名称。

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

以下示例查看 `reldb1` 数据库的建库语句。

```sql
-- 1. 创建数据库 reldb1。

CREATE DATABASE reldb1 WITH ENCODING = 'UTF8';

--2. 查看已创建的 reldb1 数据库。

SHOW CREATE DATABASE reldb1;
  database_name |    create_statement
----------------+-------------------------
  reldb1        | CREATE DATABASE reldb1
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

以下示例将 `db1` 数据库设置为当前数据库。

```sql
USE db1;
```

## 修改数据库

KWDB 支持修改数据库名称以及数据库区域配置。

::: warning 说明
KWDB 不支持修改视图关联的数据库的名称。
:::

### 前提条件

- 修改数据库名称：用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。
- 修改数据库区域配置：
  - 修改系统数据库区域配置：用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。
  - 修改其他数据库区域配置：用户是 `admin` 角色的成员或者拥有目标数据库的 CREATE 或 ZONECONFIG 权限。默认情况下，`root` 用户属于 `admin` 角色。

### 语法格式

- 修改数据库名称：

  ```sql
  ALTER DATABASE <db_name> RENAME TO <new_name>;
  ```

- 修改数据库区域配置：
  
  ```sql
  ALTER DATABASE <db_name> CONFIGURE ZONE 
  [USING <variable> = [COPY FROM PARENT | <value>], <variable> = [<value> | COPY FROM PARENT], ... | DISCARD];
  ```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `db_name` | 待修改的数据库名称。如果目标数据库为当前数据库，或者将 `sql_safe_updates` 参数设置为 `true`，则无法重命名该数据库。|
| `new_name` | 拟修改的数据库名称，新数据库名称必须唯一，并且[遵循数据库标识符规则](../../sql-reference/sql-identifiers.md)。|
| `variable` | 待修改的变量名，关系库支持修改以下变量：<br> - `range_min_bytes`：数据分片的最小大小，单位为字节。数据分片小于该值时，KWDB 会将其与相邻数据分片合并。默认值：256 MiB，设置值应大于 1 MiB（1048576 字节），小于数据分片的最大大小。<br> - `range_max_bytes`：数据分片的最大大小，单位为字节。数据分片大于该值时，KWDB 会将其切分到两个数据分片。默认值： 512 MiB。设置值不得小于 5 MiB（5242880 字节）。<br> - `gc.ttlseconds`：数据在垃圾回收前保留的时间，单位为秒。默认值为 `90000`（25 小时）。设置值建议不小于 600 秒（10 分钟），以免影响长时间运行的查询。设置值较小时可以节省磁盘空间，设置值较大时会增加 `AS OF SYSTEM TIME` 查询的时间范围。另外，由于每行的所有版本都存储在一个永不拆分的单一数据分片内，不建议将该值设置得太大，以免单行的所有更改累计超过 64 MiB，导致内存不足或其他问题。<br>- `num_replicas`：副本数量。默认值为 3。`system` 数据库、`meta`、`liveness` 和 `system` 数据分片的默认副本数为 5。 **注意**：集群中存在不可用节点时，副本数量不可缩减。<br>- `constraints`：副本位置的必需（+）和/或禁止（-）约束。<br> - `lease_preferences`：租约位置的必需（+）和/或禁止（-）约束的有序列表。每个约束前可带 + 表示必需，或 - 表示禁止。注意，租约偏好不必与 `constraints` 字段共享，用户可以单独定义 `lease_preferences`，也可以单独定义 `lease_preferences`。如果不能满足首选项，KWDB 将尝试下一个优先级。如果所有首选项都无法满足，KWDB 将使用默认的租约分布算法，该算法基于每个节点已持有的租约数量来决定租约位置，尝试平衡租约分布。列表中的每个值可以包含多个约束。例如，列表 `[[+zone=zn-east-1b, +ssd], [+zone=zn-east-1a], [+zone=zn-east-1c, +ssd]]` 表示首选位于 `zn-east-1b` 区域具有 SSD 的节点，其次是位于 `zn-east-1a` 区域的节点，最后是 `zn-east-1c` 区域具有 SSD 的节点。默认值：如果未指定此字段，则不应用租约偏好。 |
| `value` | 变量值。 |
|`COPY FROM PARENT`| 使用父区域的设置值。|
|`DISCARD` | 移除区域配置，采用默认值。|

### 语法示例

- 修改数据库的名称。

    以下示例将 `rdb` 数据库重命名为 `relationaldb`。

    ```sql
    -- 1. 查看所有数据库。
    
    SHOW DATABASES;
    database_name|engine_type
    -------------+-----------
    defaultdb    |RELATIONAL
    postgres     |RELATIONAL
    rdb          |RELATIONAL
    system       |RELATIONAL
    tsdb         |TIME SERIES
    (5 rows)
    
    -- 2. 重命名数据库。
    
    ALTER DATABASE rdb RENAME TO relationaldb;
    ALTER DATABASE
    
    -- 3. 查看所有数据库。
    
    SHOW DATABASES;
    database_name|engine_type
    -------------+-----------
    defaultdb    |RELATIONAL
    postgres     |RELATIONAL
    relationaldb |RELATIONAL
    system       |RELATIONAL
    tsdb         |TIME SERIES
    (5 rows)
    ```

- 修改数据库区域配置
  
  以下示例将 `db3` 数据库副本数改为 5， 将数据在垃圾回收前保留的时间改为100000。
  
  ```sql
  -- 1. 修改数据库区域配置
  > ALTER DATABASE db3 CONFIGURE ZONE USING num_replicas = 5, gc.ttlseconds = 100000;
  CONFIGURE ZONE 1

  -- 2. 查看数据库区域配置

  > SHOW ZONE CONFIGURATION FOR DATABASE db3;
        target  |               raw_config_sql
  -------------------+------------------------------------------
    DATABASE db3 | ALTER DATABASE db3 CONFIGURE ZONE USING
                |     range_min_bytes = 134217728,
                |     range_max_bytes = 536870912,
                |     gc.ttlseconds = 100000,
                |     num_replicas = 5,
                |     constraints = '[]',
                |     lease_preferences = '[]'
  (1 row)
  ```
  
## 删除数据库

### 前提条件

- 用户拥有目标数据库和其下全部模式及对象的 DROP 权限。删除成功后，所有用户针对目标数据库和其下全部模式及对象的所有权限均被删除。
- 目标数据库不能是当前数据库。如需删除当前数据库，使用 `USE <database_name>` 语句将当前数据库切换成其他数据库，再进行删除。

### 语法格式

```sql
DROP DATABASE [IF EXISTS] <db_name> [CASCADE | RESTRICT];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF EXISTS` | 可选关键字。当使用 `IF EXISTS` 关键字时，如果目标数据库存在，系统删除目标数据库。如果目标数据库不存在，系统删除数据库失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果目标数据库存在，系统删除目标数据库。如果目标数据库不存在，系统报错，提示目标数据库不存在。 |
| `db_name` | 待删除的数据库的名称。|
| `CASCADE` | 可选关键字，表示级联删除，即删除数据库中的所有表、视图及其关联对象（例如约束和视图）。`CASCADE` 不会列出待删除的关联对象，应谨慎使用。|
| `RESTRICT` | 可选关键字，如果目标数据库包含表和视图，系统报错，提示目标数据库为非空数据库。|

### 语法示例

- 使用 `CASCADE` 关键字删除数据库及其对象。

    以下示例使用 `CASCADE` 关键字删除 `relationaldb` 数据库及其级联对象。

    ```sql
    -- 1. 查看 relationaldb 数据库中的关系表。

    SHOW TABLES FROM relationaldb;
    table_name|table_type
    ----------+----------
    ints      |BASE TABLE
    (1 row)

    -- 2. 删除 relationaldb 数据库及其级联对象。

    DROP DATABASE relationaldb CASCADE;
    DROP DATABASE

    -- 3. 查看 relationaldb 数据库中的关系表。

    SHOW TABLES FROM relationaldb;
    ERROR: target database or schema does not exist
    ```

- 使用 `RESTRICT` 关键字阻止删除非空数据库。

    以下示例使用 `RESTRICT` 关键字阻止删除 `db1` 非空数据库。

    ```sql
    -- 1. 查看 db1 数据库中的关系表。
    
    SHOW TABLES FROM db1;
    table_name|table_type
    ----------+----------
    int       |BASE TABLE
    ints      |BASE TABLE
    (2 rows)
    
    -- 2. 删除 db1 数据库。
    
    DROP DATABASE db1 RESTRICT;
    ERROR:  database "db1" is not empty and RESTRICT was specified
    ```
