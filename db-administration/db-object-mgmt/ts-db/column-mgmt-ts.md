---
title: 列管理
id: column-mgmt-ts
---

# 列管理

## 添加列

KWDB 支持使用 `ALTER TABLE ... ADD COLUMN` 语句添加列。`ADD COLUMN` 为在线操作，不会阻塞表中的数据读写。每张表最多支持 4096 列。

::: warning 说明
目前，KWDB 不支持一次添加多列。
:::

### 前提条件

用户拥有目标表的 CREATE 权限。

### 语法格式

```sql
ALTER TABLE <table_name> ADD [COLUMN] [IF NOT EXISTS] <colunm_name> <data_type> [ DEFAULT <default_expr> | NULL ];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。如未指定，则默认使用当前数据库。 |
| `COLUMN` | 可选关键字，是否使用不影响添加列。 |
| `IF NOT EXISTS` | 可选关键字，当使用 `IF NOT EXISTS` 关键字时，如果列名不存在，系统创建列。如果列名存在，系统创建列失败，但不会报错。当未使用 `IF NOT EXISTS` 关键字时，如果列名不存在，系统创建列。如果列名存在，系统报错，提示列名已存在。 |
| `column_name` | 列名，新增列名不得与待修改表的当前列名和标签名重复。列名的最大长度为 128 字节。 |
| `data_type` | 数据类型。有关时序表支持的数据类型，参见[时序数据类型](../../../sql-reference/data-type/data-type-ts-db.md)。|
| `DEFAULT <default expr>` | 可选关键字。设置数据列的默认值。对于非时间类型的数据列，默认值只能是常量。对于时间类型的列（TIMESTAMPTZ 或 TIMESTAMP），默认值可以是常量，也可以是 `now()` 函数。如果默认值类型与列类型不匹配，设置默认值时，系统报错。支持默认值设置为 NULL。|
| `NULL` | 可选关键字，默认为 `NULL`，且只支持 `NULL`。 |

### 语法示例

- 以下示例为 `ts_table` 表增加一个名为 `c3` 的列。

    ```sql
    ALTER TABLE ts_table ADD COLUMN c3 INT NULL;
    ```

- 以下示例为 `ts_table` 表增加一个名为 `c4` 的列并设置该列的默认值为 `aaa`。

    ```sql
    ALTER TABLE ts_table ADD COLUMN c4 DEFAULT 'aaa';
    ```

## 查看列

`SHOW COLUMNS` 语句用于查看表中各列的详细信息，包括列名、标签列名、数据类型以及是否非空。

### 前提条件

用户拥有目标表的任何权限。

### 语法格式

```sql
SHOW COLUMNS FROM <table_name> [WITH COMMENT];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。如未指定，则默认使用当前数据库。 |
| `WITH COMMENT` | 可选关键字，查看列的注释信息。默认情况下，列的注释信息为 `NULL`。 |

### 语法示例

- 查看列的信息。

    以下示例查看 `sensor_data` 表中各列的详细信息。

    ```sql
    SHOW COLUMNS FROM sensor_data;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      column_name |  data_type  | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
    --------------+-------------+-------------+----------------+-----------------------+-----------+-----------+---------
      k_timestamp | TIMESTAMPTZ |    false    | NULL           |                       | {primary} |   false   | false
      temperature | FLOAT8      |    false    | NULL           |                       | {}        |   false   | false
      humidity    | FLOAT8      |    true     | NULL           |                       | {}        |   false   | false
      pressure    | FLOAT8      |    true     | NULL           |                       | {}        |   false   | false
      sensor_id   | INT4        |    false    | NULL           |                       | {}        |   false   |  true
      sensor_type | VARCHAR(30) |    false    | NULL           |                       | {}        |   false   |  true
    (6 rows)
    ```

- 查看列的注释信息。

    以下示例查看 `sensor_data` 表中各列的注释信息。

    ```sql
    -- 1. 为 sensor_data 表的 sensor_id 列添加注释信息。

    COMMENT ON COLUMN sensor_data.sensor_id IS 'device ID statistics';
    COMMENT ON COLUMN

    -- 2. 查看 sensor_data 表中各列的注释信息。

    SHOW COLUMNS FROM sensor_data WITH COMMENT;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
     column_name |  data_type  | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag |       comment
    --------------+-------------+-------------+----------------+-----------------------+-----------+-----------+--------+-----------------------
      k_timestamp | TIMESTAMPTZ |    false    | NULL           |                       | {primary} |   false   | false  | NULL
      temperature | FLOAT8      |    false    | NULL           |                       | {}        |   false   | false  | NULL
      humidity    | FLOAT8      |    true     | NULL           |                       | {}        |   false   | false  | NULL
      pressure    | FLOAT8      |    true     | NULL           |                       | {}        |   false   | false  | NULL
      sensor_id   | INT4        |    false    | NULL           |                       | {}        |   false   |  true  | device ID statistics
      sensor_type | VARCHAR(30) |    false    | NULL           |                       | {}        |   false   |  true  | NULL
    (6 rows) 
    ```

## 修改列

KWDB 支持使用 `ALTER TABLE ... ALTER COLUMN` 语句修改列的数据类型、宽度、设置或者删除列的默认值。`ALTER COLUMN` 为在线操作，不会阻塞表中的数据读写。

### 前提条件

用户拥有目标表的 CREATE 权限。

### 语法格式

```sql
ALTER TABLE <table_name> ALTER [COLUMN] <colunm_name> [SET DATA] TYPE <new_type> [ SET DEFAULT <default_expr> | DROP DEFAULT];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。如未指定，则默认使用当前数据库。 |
| `column_name` | 待修改列的名称。 |
| `COLUMN` | 可选关键字，是否使用不影响修改列的数据类型和宽度。 |
| `SET DATA` | 可选关键字，是否使用不影响修改列的数据类型和宽度。 |
| `new_type` | 拟修改的数据类型和宽度。<br > **说明** <br >- 转换后的数据类型宽度必须大于原数据类型的宽度。例如，INT4 可以转成 INT8，但不能转成 INT2，CHAR(200) 可以转为 VARCHAR (254), 但不能转为 VARCHAR (100)。<br >- CHAR、VARCHAR、NCHAR、NVARCHAR 字符类型支持同数据类型的宽度转换，但只能增加宽度不能降低宽度。例如，CHAR(100) 可以转转为 CHAR(200)，不能转为 CHAR(50)。有关 KWDB 支持修改的数据类型、默认宽度、最大宽度、可转换的数据类型等详细信息，参见[时序数据类型](../../../sql-reference/data-type/data-type-ts-db.md)。 |
| `SET DEFAULT <default_expr>` | 必选关键字。系统写入表数据时写入指定的默认值，从而不需要显式定义该列的值。对于非时间类型的数据列，默认值只能是常量。对于时间类型的列（TIMESTAMPTZ 或 TIMESTAMP），默认值可以是常量，也可以是 `now()` 函数。如果默认值类型与列类型不匹配，设置默认值时，系统报错。支持默认值设置为 NULL。|
| `DROP DEFAULT` | 必选关键字。删除已定义的列的默认值，删除后将不再写入默认值。|

### 语法示例

- 以下示例修改 `ts_table` 表中 `c3` 列的数据类型。

    ```sql
    ALTER TABLE ts_table ALTER COLUMN c3 TYPE INT8;
    ```

- 以下示例为 `ts_table` 表中 `c4` 列设置默认值 `789`。

    ```sql
    ALTER TABLE ts_table ALTER COLUMN c4 SET DEFAULT '789';
    ```

- 以下示例删除 `ts_table` 表中 `c4` 列的默认值。

    ```sql
    ALTER TABLE ts_table ALTER COLUMN c4 DROP DEFAULT;
    ```

## 重命名列

KWDB 支持使用 `ALTER TABLE ... RENAME COLUMN` 语句修改列名。

### 前提条件

用户拥有目标表的 CREATE 权限。

### 语法格式

```sql
ALTER TABLE <table_name> RENAME COLUMN <old_name> TO <new_name>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。如未指定，则默认使用当前数据库。 |
| `old_name` | 当前列名。|
| `new_name` | 拟修改的列名。新增列名不得与待修改表的当前列名和标签名称重复。列名的最大长度为 128 字节。 |

### 语法示例

以下示例将 `ts_table` 表的 `c2` 列重命名为 `c4`。

```sql
ALTER TABLE ts_table RENAME COLUMN c2 TO c4;
```

## 删除列

KWDB 支持使用 `ALTER TABLE ... DROP COLUMN` 语句删除列。`DROP COLUMN` 为在线操作，不会阻塞表中的数据读写。

::: warning 说明

- 删除列时，原表至少保留两列数据列，且不支持删除第一列（时间戳列）。
- 目前，KWDB 不支持一次删除多个列。

:::

### 前提条件

用户拥有目标表的 CREATE 权限。

### 语法格式

```sql
ALTER TABLE <table_name> DROP [COLUMN] [IF EXISTS] <colunm_name>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。如未指定，则默认使用当前数据库。 |
| `COLUMN` | 可选关键字，是否使用不影响删除列。 |
| `IF EXISTS` | 可选关键字，当使用 `IF EXISTS` 关键字时，如果列名存在，系统删除列。如果列名不存在，系统删除列失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果列名存在，系统删除列。如果列名不存在，系统报错，提示列名不存在。|
| `column_name` | 待删除列的名称。 |

### 语法示例

以下示例删除 `ts_table` 表的 `c4` 列。

```sql
ALTER TABLE ts_table DROP c4;
```
