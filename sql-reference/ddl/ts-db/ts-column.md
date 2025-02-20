---
title: 列
id: ts-column
---

# 列

## 添加列

用户可以在创建表的时候直接创建表的数据列，也可以使用 `ALTER TABLE` 语句向表中添加列。每张表最多支持 4096 列。

::: warning 说明

- 添加列时需要应用停机，以确保结构变更的原子性、一致性，避免潜在的一致性问题。
- 目前，KWDB 不支持一次添加多列。

:::

### 所需权限

用户拥有目标表的 CREATE 权限。

### 语法格式

![](../../../static/sql-reference/ts-add-column.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。如未指定，则默认使用当前数据库。 |
| `COLUMN` | 可选关键字，是否使用不影响添加列。 |
| `IF NOT EXISTS` | 可选关键字，当使用 `IF NOT EXISTS` 关键字时，如果列名不存在，系统创建列。如果列名存在，系统创建列失败，但不会报错。当未使用 `IF NOT EXISTS` 关键字时，如果列名不存在，系统创建列。如果列名存在，系统报错，提示列名已存在。 |
| `column_name` | 列名，新增列名不得与待修改表的当前列名和标签名重复。列名的最大长度为 128 字节。 |
| `data_type` | 数据类型。有关时序表支持的数据类型，参见[时序数据类型](../../data-type/data-type-ts-db.md)。|
| `NULL` | 可选关键字，默认为 `NULL`，且只支持 `NULL`。 |

### 语法示例

以下示例为 `ts_table` 表增加一个名为 `color` 的列。

```sql
ALTER TABLE ts_table ADD COLUMN color varchar(30);
```

## 查看列

`SHOW COLUMNS` 语句用于查看表中各列的详细信息，包括列名、标签列名、数据类型以及是否非空。

### 所需权限

用户拥有目标表的任意权限。

### 语法格式

![](../../../static/sql-reference/G7Dpb9VAIoZO0ExHAaFcmoc9nkg.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。如未指定，则默认使用当前数据库。 |

### 语法示例

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

## 修改列

KWDB 支持通过 `ALTER TABLE` 语句修改列的数据类型和宽度。

### 所需权限

用户拥有目标表的 CREATE 权限。

### 语法格式

![](../../../static/sql-reference/A1ypbwKAdoiJPfxQlTScIY0knOh.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。如未指定，则默认使用当前数据库。 |
| `column_name` | 待修改列的名称。 |
| `new_type` | 拟修改的数据类型和宽度。<br > **说明** <br >- 转换后的数据类型宽度必须大于原数据类型的宽度。例如，INT4 可以转成 INT8，但不能转成 INT2，CHAR(200) 可以转为 VARCHAR (254), 但不能转为 VARCHAR (100)。<br >- CHAR、VARCHAR、NCHAR、NVARCHAR 字符类型支持同数据类型的宽度转换，但只能增加宽度不能降低宽度。例如，CHAR(100) 可以转转为 CHAR(200)，不能转为 CHAR(50)。有关 KWDB 支持修改的数据类型、默认宽度、最大宽度、可转换的数据类型等详细信息，参见[时序数据类型](../../data-type/data-type-ts-db.md)。 |

### 语法示例

以下示例修改 `ts_table` 表中 `c3` 列的数据类型。

```sql
ALTER TABLE ts_table ALTER COLUMN c3 TYPE INT8;
```

## 重命名列

`RENAME COLUMN` 语句是 `ALTER TABLE` 语句的一部分，用于修改表的列名。

### 所需权限

用户拥有目标表的 CREATE 权限。

### 语法格式

![](../../../static/sql-reference/YWzubTWQOotivQxhvpUcsijZn8b.png)

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

::: warning 说明

- 删除列时需要应用停机，待修改的表不在修改过程中，以确保结构变更的原子性、一致性，避免潜在的一致性问题。
- 删除列时，原表至少保留两列数据列，且不支持删除第一列（时间戳列）。
- 目前，KWDB 不支持一次删除多个列。

:::

### 所需权限

用户拥有目标表的 CREATE 权限。

### 语法格式

![](../../../static/sql-reference/ND7EbmrMLoJgRMxs64ocgWzinyg.png)

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
