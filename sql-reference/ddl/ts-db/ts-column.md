---
title: 列
id: ts-column
---

# 列

## 添加列

KWDB 支持使用 `ALTER TABLE ... ADD COLUMN` 语句添加列。`ADD COLUMN` 为在线操作，不会阻塞表中的数据读写。每张表最多支持 4096 列。

::: warning 说明

- 目前，KWDB 不支持一次添加多列。
- 添加列时，系统检查当前时序表是否被流计算引用。如果是，则输出错误消息并列出所有引用此时序表的流计算名称。用户需要首先停止相关的流计算，然后再添加列。有关停止流计算的详细信息，参见[修改流计算](../../other-sql-statements/stream-sql.md#修改流计算)。

:::

### 所需权限

用户是 `admin` 角色的成员或者拥有目标表的 CREATE 权限。默认情况下，`root` 用户属于 `admin` 角色。

### 语法格式

![](../../../static/sql-reference/add_column_ts.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。如未指定，则默认使用当前数据库。 |
| `COLUMN` | 可选关键字，是否使用不影响添加列。 |
| `IF NOT EXISTS` | 可选关键字，当使用 `IF NOT EXISTS` 关键字时，如果列名不存在，系统创建列。如果列名存在，系统创建列失败，但不会报错。当未使用 `IF NOT EXISTS` 关键字时，如果列名不存在，系统创建列。如果列名存在，系统报错，提示列名已存在。 |
| `column_name` | 列名，新增列名不得与待修改表的当前列名和标签名重复。列名的最大长度为 128 字节。 |
| `data_type` | 数据类型。有关时序表支持的数据类型，参见[时序数据类型](../../data-type/data-type-ts-db.md)。|
| `DEFAULT <default expr>` | 可选关键字。设置数据列的默认值。对于非时间类型的数据列，默认值只能是常量。对于时间类型的列（TIMESTAMPTZ 或 TIMESTAMP），默认值可以是常量，也可以是 `now()` 函数。如果默认值类型与列类型不匹配，设置默认值时，系统报错。支持默认值设置为 NULL。|
| `NULL` | 可选关键字，默认为 `NULL`，且只支持 `NULL`。 |
| `encode_algo` | 可选，设置列的编码算法，大小写不敏感。不同数据类型支持的编码算法不同，详见数据压缩中[编码说明](../../../db-operation/storage-mgmt.md#编码算法)。设置为 `disabled` 表示关闭该列的编码。如未指定，使用该数据类型的默认编码算法。 |
| `compress_algo` | 可选，设置列的压缩算法，大小写不敏感，支持 `lz4`、`zstd`、`zlib`、`snappy`。设置为 `disabled` 表示关闭该列的压缩。如未指定，默认使用 `lz4`。 |
| `level` | 可选，设置压缩算法的压缩级别，大小写不敏感，必须紧跟在 `COMPRESS` 之后指定。支持 `low`（简写 `l`）、`medium`（简写 `m`）、`high`（简写 `h`），默认 `medium`。如果 `compress_algo` 设置为 `disabled`，则指定该参数会报错。 |

### 语法示例

- 以下示例为 `ts_table` 表增加一个名为 `color` 的列。

    ```sql
    ALTER TABLE ts_table ADD COLUMN c3 INT NULL;
    ```

- 以下示例为 `ts_table` 表增加一个名为 `c4` 的列并设置该列的默认值为 `aaa`。

    ```sql
    ALTER TABLE ts_table ADD COLUMN c4 VARCHAR(50) DEFAULT 'aaa';
    ```

- 以下示例为 `ts_table` 表增加一个名为 `c5` 的列并指定编码和压缩算法。

    ```sql
    ALTER TABLE ts_table ADD COLUMN c5 INT ENCODE 'Simple8B' COMPRESS 'lz4' LEVEL 'high';
    ```

## 查看列

`SHOW COLUMNS` 语句用于查看表中各列的详细信息，包括列名、标签列名、数据类型以及是否非空。

### 所需权限

用户拥有目标表的任意权限。

### 语法格式

![](../../../static/sql-reference/show_column_ts.png)

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

KWDB 支持使用 `ALTER TABLE ... ALTER COLUMN` 语句修改列的数据类型、宽度、设置或者删除列的默认值。`ALTER COLUMN` 为在线操作，不会阻塞表中的数据读写。修改数据类型时，如果已有数值与新数据类型不匹配，修改操作仍然可以执行成功，不符合新数据类型的数值在查询时将显示为 `NULL`。

::: warning 说明
修改列时，系统检查当前时序表是否被流计算引用。如果是，则输出错误消息并列出所有引用此时序表的流计算名称。用户需要首先停止相关的流计算，然后再修改列。有关停止流计算的详细信息，参见[修改流计算](../../other-sql-statements/stream-sql.md#修改流计算)。
:::


### 所需权限

用户是 `admin` 角色的成员或者拥有目标表的 CREATE 权限。默认情况下，`root` 用户属于 `admin` 角色。

### 语法格式

![](../../../static/sql-reference/alter_column_ts.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。如未指定，则默认使用当前数据库。 |
| `column_name` | 待修改列的名称。 |
| `new_type` | 拟修改的数据类型和宽度。转换规则详见[支持修改的数据类型](#支持修改的数据类型)。 |
| `SET DEFAULT <default_expr>` | 必选关键字。系统写入表数据时写入指定的默认值，从而不需要显式定义该列的值。对于非时间类型的数据列，默认值只能是常量。对于时间类型的列（TIMESTAMPTZ 或 TIMESTAMP），默认值可以是常量，也可以是 `now()` 函数。如果默认值类型与列类型不匹配，设置默认值时，系统报错。支持默认值设置为 NULL。|
| `DROP DEFAULT` | 必选关键字。删除已定义的列的默认值，删除后将不再写入默认值。|
| `encode_algo` | 可选，设置列的编码算法，大小写不敏感。不同数据类型支持的编码算法不同，详见数据压缩中[编码说明](../../../db-operation/storage-mgmt.md#编码算法)。设置为 `disabled` 表示关闭该列的编码。如未指定，使用该数据类型的默认编码算法。同时指定 `ENCODE` 和 `COMPRESS` 时，必须严格按照 `ENCODE ... COMPRESS ... LEVEL ...` 顺序。|
| `compress_algo` | 可选，设置列的压缩算法，大小写不敏感，支持 `lz4`、`zstd`、`zlib`、`snappy`。设置为 `disabled` 表示关闭该列的压缩。如未指定，默认使用 `lz4`。 |
| `level` | 可选，设置压缩算法的压缩级别，大小写不敏感，必须紧跟在 `COMPRESS` 之后指定。支持 `low`（简写 `l`）、`medium`（简写 `m`）、`high`（简写 `h`），默认 `medium`。如果 `compress_algo` 设置为 `disabled`，则指定该参数会报错。 |

### 支持修改的数据类型

下表列出了 KWDB 支持修改的时序数据类型、默认宽度、最大宽度、可转换的数据类型和特殊要求。

::: warning 说明

- 转换后的数据类型宽度必须大于原数据类型的宽度。例如，INT4 可以转成 INT8，但不能转成 INT2，CHAR(200) 可以转为 VARCHAR(254)，但不能转为 VARCHAR(100)。
- CHAR、VARCHAR、NCHAR、NVARCHAR 字符类型支持同数据类型的宽度转换，但只能增加宽度不能降低宽度。例如，CHAR(100) 可以转为 CHAR(200)，不能转为 CHAR(50)。

:::

| 原数据类型  | 默认宽度 | 最大宽度   | 支持转换的数据类型                                   | 说明                                                                                            |
| ----------- | -------- | ---------- | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| TIMESTAMP   | -        | -          | TIMESTAMPTZ、INT8、FLOAT4、FLOAT8                     | 标签不支持该类型。TIMESTAMP 转 INT8 时，输出结果固定为毫秒精度的数字，即 13 位数字。TIMESTAMP 转 FLOAT4 时，输出结果只能保证约前 7 位有效数字的精度。TIMESTAMP 转 FLOAT8 时，输出结果只能保证约前 15-17 位有效数字的精度。    |
| TIMESTAMPTZ | -        | -          | TIMESTAMP、INT8、FLOAT4、FLOAT8                      | 标签不支持该类型。TIMESTAMPTZ 转 INT8 时，输出结果固定为毫秒精度的数字，即 13 位数字。TIMESTAMPTZ 转 FLOAT4 时，输出结果只能保证约前 7 位有效数字的精度。TIMESTAMPTZ 转 FLOAT8 时，输出结果只能保证约前 15-17 位有效数字的精度。 |
| INT2        | 2 字节   | -          | INT4、INT8、VARCHAR                                  | INT2 转 VARCHAR 时，VARCHAR 的最小宽度为 6。                                                    |
| INT4        | 4 字节   | -          | INT8、VARCHAR                                        | INT4 转 VARCHAR 时，VARCHAR 的最小宽度为 11。                                                   |
| INT8        | 8 字节   | -          | VARCHAR                                              | INT8 转 VARCHAR 时，VARCHAR 的最小宽度为 20。                                                   |
| FLOAT4      | 4 字节   | -          | FLOAT、VARCHAR                                       | REAL 转 VARCHAR 时，VARCHAR 的最小宽度为 30。                                                   |
| FLOAT8      | 8 字节   | -          | VARCHAR                                              | FLOAT 转 VARCHAR 时，VARCHAR 的最小宽度为 30。                                                  |
| CHAR        | 1 字节   | 1023       | NCHAR、VARCHAR、NVARCHAR                             | CHAR 转 NCHAR 或 NVARCHAR 时，NCHAR 或 NVARCHAR 的宽度不得小于原宽度的 ¼。                     |
| VARCHAR     | 254 字节 | 65534 字节 | CHAR、NCHAR、NVARCHAR、INT2、INT4、INT8、REAL、FLOAT | VARCHAR 转 NCHAR 或 NVARCHAR 时，NCHAR 和 NVARCHAR 的宽度不得小于原宽度的 ¼。                  |
| NCHAR       | 1 字符   | 254 字符   | CHAR、VARCHAR、NVARCHAR                              | NCHAR 转 CHAR 或 VARCHAR 时，CHAR 和 VARCHAR 的宽度不得小于原宽度的 4 倍。                      |
| NVARCHAR    | 63 字符  | 16383 字符 | CHAR、VARCHAR、NCHAR                                 | NVARCHAR 转 CHAR 或 VARCHAR 时，CHAR 和 VARCHAR 的宽度不得小于原宽度的 4 倍。标签不支持该类型。 |

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

- 以下示例修改 `ts_table` 表中 `c3` 列的编码算法。

    ```sql
    ALTER TABLE ts_table ALTER COLUMN c3 ENCODE 'Simple8B';
    ```

- 以下示例修改 `ts_table` 表中 `c3` 列的压缩算法和压缩级别。

    ```sql
    ALTER TABLE ts_table ALTER COLUMN c3 COMPRESS 'zstd' LEVEL 'high';
    ```

- 以下示例同时修改 `ts_table` 表中 `c3` 列的编码和压缩算法（`ENCODE` 必须在 `COMPRESS` 之前）。

    ```sql
    ALTER TABLE ts_table ALTER COLUMN c3 ENCODE 'Simple8B' COMPRESS 'zstd' LEVEL 'medium';
    ```

- 以下示例关闭 `ts_table` 表中 `c3` 列的通用压缩。

    ```sql
    ALTER TABLE ts_table ALTER COLUMN c3 COMPRESS 'disabled';
    ```

## 重命名列

KWDB 支持使用 `ALTER TABLE ... RENAME COLUMN` 语句修改列名。

::: warning 说明
重命名列时，系统检查当前时序表是否被流计算引用。如果是，则输出错误消息并列出所有引用此时序表的流计算名称。用户需要首先停止相关的流计算，然后再重命名列。有关停止流计算的详细信息，参见[修改流计算](../../other-sql-statements/stream-sql.md#修改流计算)。
:::

### 所需权限

用户是 `admin` 角色的成员或者拥有目标表的 CREATE 权限。默认情况下，`root` 用户属于 `admin` 角色。

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

KWDB 支持使用 `ALTER TABLE ... DROP COLUMN` 语句删除列。`DROP COLUMN` 为在线操作，不会阻塞表中的数据读写。

::: warning 说明

- 删除列时，原表至少保留两列数据列，且不支持删除第一列（时间戳列）。
- 目前，KWDB 不支持一次删除多个列。
- 删除列时，系统检查当前时序表是否被流计算引用。如果是，则输出错误消息并列出所有引用此时序表的流计算名称。用户需要首先停止相关的流计算，然后再删除列。有关停止流计算的详细信息，参见[修改流计算](../../other-sql-statements/stream-sql.md#修改流计算)。

:::

### 所需权限

用户是 `admin` 角色的成员或者拥有目标表的 CREATE 权限。默认情况下，`root` 用户属于 `admin` 角色。

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
