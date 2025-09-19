---
title: 时序表
id: ts-table
---

# 时序表

时序表（TIME SERIES TABLE）是用于存储时间序列数据的数据表。

## 创建表

### 所需权限

用户拥有 DATABASE CREATE 权限。

### 语法格式

![](../../../static/sql-reference/create_table_ts.png)

### 参数说明

:::warning 说明

- 目前，时序表名、列名和标签名称不支持中文字符。
- 配置可选参数时，必须严格按照 `[RETENTIONS <keep_duration>] [DICT ENCODING] [COMMENT [=] <'comment_text'>] [WITH HASH(hash_value)]` 的顺序，否则系统将会报错。

:::

| 参数 | 说明 |
| --- | --- |
| `table_name`| 待创建的时序表的名称，表名的最大长度为 128 字节。在指定数据库中，时序表名称必须唯一，并且遵循[数据库标识符规则](../../sql-identifiers.md)。 |
| `column_list`| 待创建的数据列列表，支持添加两个以上的列定义，最多可指定 4096 列。列定义包括列名、数据类型、注释信息和默认值。<br>- 列名的最大长度为 128 字节，支持指定 NOT NULL，默认为空值。支持自定义第一列的列名，但数据类型必须是 TIMESTAMPTZ 或 TIMESTAMP 且非空。默认时区为 UTC。<br >- 对于非时间类型的数据列，默认值只能是常量。对于时间类型的列（TIMESTAMPTZ 或 TIMESTAMP），默认值可以是常量，也可以是 `now()` 函数。如果默认值类型与列类型不匹配，设置默认值时，系统报错。支持默认值设置为 NULL。<br >- 时间戳列支持设置时间精度。目前，KWDB 支持毫秒、微秒和纳秒的时间精度。默认情况下，KWDB 采用毫秒时间精度。<br >- 支持在数据类型之后添加数据列的注释信息。 |
| `tag_list`| 标签列表，支持添加一个或多个标签定义，最多可指定 `128` 个标签。标签定义包含标签名、数据类型和注释信息。<br>- 标签名的最大长度为 128 字节，支持指定 NOT NULL，默认为空值。不支持 TIMESTAMP、TIMESTAMPTZ、NVARCHAR 和 GEOMETRY 数据类型。<br >- 支持在 nullable 条件之后添加标签列的注释信息。 |
| `primary_tag_list`| 主标签列表，支持添加一个或多个主标签名称，最多可指定 `4` 个。主标签必须包含在标签列表内且指定为 NOT NULL，不支持浮点类型和除 VARCHAR 之外的变长数据类型。VARCHAR 类型长度默认 `64` 字节，最大长度为 `128` 字节。|
| `keep_duration` | 可选参数，设置表的数据生命周期。数据超过此时长后将被系统自动清除。<br>默认值： `0s`（永久保留）<br>时间单位：<br>- 秒：`s` 或 `second`<br>- 分钟：`m` 或 `minute`<br>- 小时：`h` 或 `hour`<br>- 天：`d` 或 `day`<br>- 周：`w` 或 `week`<br>- 月：`mon` 或 `month`<br>- 年：`y` 或 `year`<br>取值范围:正整数，上限为 1000 年<br>**说明：**<br>- 表级设置优先于库级设置。<br>- 保留时长越长，存储空间占用越大，请根据业务需求合理配置。<br>- 如果待写入的数据已超过生命周期限制，系统会直接丢弃该数据，不予写入。|
| `DICT ENCODING`| 可选参数，启用字符串的字典编码功能，提升字符串数据的压缩能力。表中存储的字符串数据重复率越高，压缩优化效果越明显。该功能只适用于 CHAR 和 VARCHAR 长度小于等于 `1023` 的字符串，且只能在建表时开启。开启后不支持禁用。 |
| `[COMMENT [=] <'comment_text'>` | 可选参数，定义表的注释信息。 |
| `hash_value`| 可选参数，用于定义分布式集群中 HASH 环的大小，决定最大 Range 分片数量。例如 HASH(100) 表示最多可产生 100 个不同的 Range 分片。<br><br>默认值为 2000，表示最多可产生 2000 个 Range 分片。支持设置范围为 [1,50000]。<br><br>性能影响：HASH 值过小时将导致多个设备的数据集中在少数 Range 中，形成写入热点，HASH 值过大时则会导致 Range 数量过多，增加管理开销。<br><br>推荐配置：建议根据预期设备数量选择合适的 HASH 值：<br>- 设备数 ≤ 1,000：HASH 值 < 20<br>- 设备数 ≤ 50,000：HASH 值 < 2,000<br>- 设备数 ≤ 1,000,000：HASH 值 < 10,000 <br><br>最佳实践：建议配合集群参数 `SET CLUSTER SETTING sql.ts_create.leaseholder_auto_relocated.enabled = true;`使用，可在建表时自动将 Range 分片和 Leaseholder 均匀分布到各节点，从源头避免热点问题。 |

### 语法示例

- 创建时序表。

    以下示例创建一个名为 `sensor_data` 的时序表。

    ```sql
    -- 1. 创建 sensor_data 时序表。

    CREATE TABLE sensor_data (
      k_timestamp TIMESTAMP NOT NULL,
      temperature FLOAT NOT NULL,
      humidity FLOAT,
      pressure FLOAT
    ) TAGS (
          sensor_id INT NOT NULL,
          sensor_type VARCHAR(30) NOT NULL
    ) PRIMARY TAGS (sensor_id);
    
    -- 2. 查看创建的表。
    
    SHOW CREATE sensor_data;
      table_name  |                        create_statement
    --------------+-----------------------------------------------------------------
      sensor_data | CREATE TABLE sensor_data (
                  |     k_timestamp TIMESTAMPTZ NOT NULL,
                  |     temperature FLOAT8 NOT NULL,
                  |     humidity FLOAT8 NULL,
                  |     pressure FLOAT8 NULL
                  | ) TAGS (
                  |     sensor_id INT4 NOT NULL,
                  |     sensor_type VARCHAR(30) NOT NULL ) PRIMARY TAGS(sensor_id)
    (1 row)
    ```

- 创建时序表并设置表的生命周期。

    以下示例创建一个名为 `temp` 的时序表并将表的生命周期设置为 `20D`。

    ```sql
    -- 1. 创建 temp 时序表并设置表的生命周期。

    CREATE TABLE temp (ts TIMESTAMP NOT NULL, value FLOAT) TAGS (sensor_id INT NOT NULL) PRIMARY TAGS (sensor_id) RETENTIONS 20D;
    CREATE TABLE

    -- 2. 查看表的生命周期。

    SHOW RETENTIONS ON TABLE temp;
      name | retentions | sample
    -------+------------+---------
      temp | 20d        | NULL
    (1 row)
    ```

- 创建时序表并开启字符串字典编码。

    以下示例创建一个名为 `water` 的时序表并开启字符串字典编码。

    ```sql
    CREATE TABLE water (ts TIMESTAMP NOT NULL, value FLOAT) TAGS (sensor_id INT NOT NULL) PRIMARY TAGS (sensor_id) DICT ENCODING;
    ```

- 创建时序表并为表及其数据列和标签列添加注释信息。

    以下示例创建一个名为 `device_info` 的时序表并为表及其数据列和标签列添加注释信息。

    ```sql
    CREATE TABLE device_info (create_time TIMESTAMPZ NOT NULL, device_id INT COMMENT 'device ID' NOT NULL, install_date TIMESTAMPZ, warranty_period INT2) TAGS (plant_code INT2 NOT NULL COMMENT = 'plant code', workshop VARCHAR(128) NOT NULL, device_type CHAR(1023) NOT NULL, manufacturer NCHAR(254) NOT NULL) PRIMARY TAGS(plant_code, workshop, device_type, manufacturer) COMMENT = 'table for device information';
    CREATE TABLE
    ```

- 创建时序表并设置 HASH 环大小。

    以下示例创建一个名为 `sensors` 的时序表并将 HASH 环大小设置为 20。

    ```sql
    CREATE TABLE sensors (ts TIMESTAMP NOT NULL, value FLOAT) TAGS (sensor_id INT NOT NULL) PRIMARY TAGS (sensor_id) WITH HASH(20);
    ```

## 查看表

`SHOW TABLES` 语句用于查看当前或指定数据库下的所有表，如未指定数据库则默认为当前数据库。

### 所需权限

用户拥有指定表的任何权限。

### 语法格式

查看当前或指定数据库下的所有表。如未指定，则默认使用当前数据库。

![](../../../static/sql-reference/show_tables_ts.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `db_name` | 待查看表所在的数据库的名称。如未指定，则默认使用当前数据库。|
| `schema_name` | 可选参数，待查看表所使用的模式名称。时序表只支持使用目标数据库的 public 模式。 |
| `table_name` | 待查看表的名称。|
| `WITH COMMENT` | 可选关键字，查看表的注释信息。默认情况下，时序表的注释信息为空。|

### 语法示例

- 查看当前数据库的所有表。

    ```sql
    SHOW TABLES;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
    table_name    | table_type
    --------------+-------------------------------       
    sensor_data   | TIME SERIES TABLE
    ```

- 查看其它数据库中的表。

    以下示例查看 `tsdb` 数据库中的表。

    ```sql
    SHOW TABLES FROM tsdb;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      table_name  |    table_type
    --------------+--------------------
      t1          | TIME SERIES TABLE
      t2          | TIME SERIES TABLE
      t3          | TIME SERIES TABLE
      t4          | TIME SERIES TABLE
      t5          | TIME SERIES TABLE
    (5 rows)
    ```

- 查看带有注释信息的表。

    以下示例查看带有注释信息的表。

    ```sql
    -- 1. 为 power 表添加注释。

    COMMENT ON TABLE power IS 'power for all devices';
    COMMENT ON TABLE

    -- 2. 查看带有注释信息的表。

    SHOW TABLES WITH COMMENT;
      table_name  |    table_type     |      comment
    --------------+-------------------+--------------------
      power       | TIME SERIES TABLE | power for all devices
    (1 row)
    ```

## 查看表的建表语句

`SHOW CREATE [TABLE] <table_name>` 语句用于查看当前或指定数据库下指定表的建表语句。如未指定数据库，则默认为当前数据库。

创建时序表时，如果指定生命周期 `retentions` 参数的取值，则显示指定的取值。如未指定则显示默认值 `0s`。

### 所需权限

用户拥有指定表的任何权限。

### 语法格式

![](../../../static/sql-reference/showcreatetable.png)

### 参数说明

| 参数            | 说明                                                      |
|-----------------|---------------------------------------------------------|
| `database_name` | 待查看表所在的数据库的名称。如未指定，则默认使用当前数据库。 |
| `table_name`    | 待查看表的名称。                                           |

### 语法示例

- 查看当前数据库中指定表的建表语句。

    以下示例查看当前数据库中 `t3` 表的建表语句。

    ```sql
    -- 1. 创建 t3 时序表，不指定 retentions 参数的取值。

    CREATE TABLE t3(ts timestamp NOT NULL, a int) TAGS(ptag int NOT NULL) PRIMARY TAGS(ptag);

    -- 2. 查看已创建的 t1 时序表。

    SHOW CREATE TABLE t3;
      table_name |              create_statement
    -------------+----------------------------------------------
      t3         | CREATE TABLE t3 (
                |     ts TIMESTAMPTZ NOT NULL,
                |     a INT4 NULL
                | ) TAGS (
                |     ptag INT4 NOT NULL ) PRIMARY TAGS(ptag)
                |     retentions 0s
    (1 row)
    ```

- 查看其它数据库中指定表的建表语句。

    以下示例查看 `tsdb` 数据库中 `t1` 表的建表语句。

    ```sql
    SHOW CREATE tsdb.t1;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
        table_name   |              create_statement
    -----------------+----------------------------------------------
      tsdb.public.t1 | CREATE TABLE t1 (
                    |     ts TIMESTAMPTZ NOT NULL,
                    |     c1 INT4 NULL
                    | ) TAGS (
                    |     site INT4 NOT NULL ) PRIMARY TAGS(site)
                    |     retentions 0s
    (1 row)
    ```

## 修改表

`ALTER TABLE` 语句用于修改以下表信息：

- 修改表名
- 设置表的数据生命周期
- 添加列、修改列名、列的数据类型或宽度、设置列的默认值、删除列的默认值
- 添加标签、修改标签名、标签的数据类型或宽度、删除标签
- 修改表的区域配置
- 创建表分区

::: warning 说明

- 删除列时，原表至少保留两列数据列，且不支持删除第一列（时间戳列）。
- 不支持添加、删除、重命名主标签。
- 目前，不支持一次添加、删除多个列或标签。
- 修改时序表结构时，系统检查当前时序表是否被流计算引用。如果是，则输出错误消息并列出所有引用此时序表的流计算名称。用户需要首先删除相关的流计算，然后再修改目标时序表。有关删除流计算的详细信息，参见[删除流计算](../../other-sql-statements/stream-sql.md#删除流计算)。

:::

### 所需权限

- 重命名表：用户拥有目标表的 DROP 权限及所在数据库的 CREATE 权限。
- 添加、修改、删除、重命名列或标签：用户拥有目标表的 CREATE 权限。
- 设置表的数据生命周期：用户拥有目标表的 CREATE 权限。
- 修改表的区域配置：用户拥有目标表的 CREATE 或 ZONECONFIG 权限。
- 创建表分区：用户拥有目标表的 CREATE 权限。

### 语法格式

![](../../../static/sql-reference/alter-ts-table.png)

### 支持的操作

- ADD
  - `ADD COLUMN`: 添加列，需指定列名和数据类型，也支持指定列的默认值。每张表最多支持 4096 列。
    - `COLUMN`：可选关键字，如未使用，默认添加列。
    - `IF NOT EXISTS`：可选关键字。当使用 `IF NOT EXISTS` 关键字时，如果列名不存在，系统创建列。如果列名存在，系统创建列失败，但不会报错。当未使用 `IF NOT EXISTS` 关键字时，如果列名不存在，系统创建列。如果列名存在，系统报错，提示列名已存在。
    - `DEFAULT <default_expr>`：可选关键字。系统写入表数据时写入指定的默认值，从而不需要显式定义该列的值。对于非时间类型的数据列，默认值只能是常量。对于时间类型的列（TIMESTAMPTZ 或 TIMESTAMP），默认值可以是常量，也可以是 `now()` 函数。如果默认值类型与列类型不匹配，设置默认值时，系统报错。支持默认值设置为 NULL。
    - `NULL`：可选关键字，默认为 `NULL`，且只支持 `NULL`。
  - `ADD TAG/ATTRITBUTE`：添加标签，需指定标签的名称和数据类型，不支持添加主标签。
- ALTER
  - `ALTER COLUMN`: 修改列的数据类型或宽度，设置或删除列的默认值。
    - `SET DATA`：可选关键字，是否使用不影响修改列的数据类型和宽度。
    - `SET DEFAULT <default_expr>`：必选关键字。系统写入表数据时写入指定的默认值，从而不需要显式定义该列的值。对于非时间类型的数据列，默认值只能是常量。对于时间类型的列（TIMESTAMPTZ 或 TIMESTAMP），默认值可以是常量，也可以是 `now()` 函数。如果默认值类型与列类型不匹配，设置默认值时，系统报错。支持默认值设置为 NULL。
    - `DROP DEFAULT`：必选关键字。删除已定义的列的默认值，删除后将不再写入默认值。
  - `ALTER TAG/ATTRITBUTE`：修改标签的数据类型或宽度，其中 `SET DATA` 为可选关键字，是否使用不影响修改标签的数据类型和宽度，不支持修改主标签的数据类型和宽度。**注意**：如果待修改的标签列已创建索引，必须先删除该索引，再进行修改。
- `CONFIGURE ZONE`：修改表的区域配置。更多详细信息，参见[区域配置](./ts-zone.md)。
- DROP
  - `DROP COLUMN`: 删除列，需指定列名。
    - `COLUMN`：可选关键字，如未使用，默认添加列。
    - `IF EXISTS`：可选关键字。当使用 `IF EXISTS` 关键字时，如果列名存在，系统删除列。如果列名不存在，系统删除列失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果列名存在，系统删除列。如果列名不存在，系统报错，提示列名不存在。
  - `DROP TAG/ATTRITBUTE`：删除标签，需指定标签名称。不支持删除主标签。如果待删除的标签列已创建索引，删除该标签时，需要先删除标签列关联的索引。
- PARTITION BY：创建表分区，更多详细信息，参见[分区](./ts-partition.md)。
- RENAME
  - `RENAME TO`: 修改表的名称。
  - `RENAME COLUMN`：修改列的名称。
  - `RENAME TAG/ATTRIBUTE`：修改标签的名称。
- `SET RETENTIONS`：设置表的生命周期。

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。如未指定，则默认使用当前数据库。 |
| `column_name` | 列名，新增列名不得与待修改表的当前列名和标签名重复。列名的最大长度为 128 字节。 |
| `data_type` | 数据类型。有关时序表支持的数据类型，参见[时序数据类型](../../../sql-reference/data-type/data-type-ts-db.md)。|
| `tag_name` | 标签名，不支持数据库级别的自定义标签。标签名的最大长度为 128 字节。 |
| `tag_type` | 标签类型，支持所有数值类型、布尔类型以及除 NVARCHAR 之外的字符类型。 |
| `new_type` | 拟修改的数据类型和宽度。<br > **说明** <br >- 转换后的数据类型宽度必须大于原数据类型的宽度。例如，INT4 可以转成 INT8，但不能转成 INT2，CHAR(200) 可以转为 VARCHAR (254), 但不能转为 VARCHAR (100)。<br >- CHAR、VARCHAR、NCHAR、NVARCHAR 字符类型支持同数据类型的宽度转换，但只能增加宽度不能降低宽度。例如，CHAR(100) 可以转转为 CHAR(200)，不能转为 CHAR(50)。有关 KWDB 支持修改的数据类型、默认宽度、最大宽度、可转换的数据类型等详细信息，参见[时序数据类型](../../../sql-reference/data-type/data-type-ts-db.md)。 |
| `new_table_name` | 拟修改的表名。表名最大长度为 128 字节。 |
| `old_name` | 当前列名或标签名，不支持修改主标签名称。|
| `new_name` | 拟修改的列名或标签名。列名或标签名的最大长度为 128 字节。 |
| `keep_duration` | 可选参数，设置表的数据生命周期。数据超过此时长后将被系统自动清除。<br>默认值： `0s`（永久保留）<br>时间单位：<br>- 秒：`s` 或 `second`<br>- 分钟：`m` 或 `minute`<br>- 小时：`h` 或 `hour`<br>- 天：`d` 或 `day`<br>- 周：`w` 或 `week`<br>- 月：`mon` 或 `month`<br>- 年：`y` 或 `year`<br>取值范围:正整数，上限为 1000 年<br>**说明：**<br>- 表级设置优先于库级设置。<br>- 保留时长越长，存储空间占用越大，请根据业务需求合理配置。<br>- 如果待写入的数据已超过生命周期限制，系统会直接丢弃该数据，不予写入。|

### 语法示例

以下示例对 `ts_table` 表进行以下操作：

- 修改表的名称
- 修改表的生命周期
- 增加、删除列、修改列的名称、数据类型
- 增加、删除标签、修改标签的名称、宽度

```sql
-- 修改表的名称。

ALTER TABLE ts_table RENAME TO tstable;

-- 修改表的生命周期。

ALTER TABLE ts_table SET RETENTIONS = 20d;

-- 新增列。

ALTER TABLE ts_table ADD COLUMN c3 INT NULL;

-- 新增列并设置列的默认值。

ALTER TABLE ts_table ADD COLUMN c4 VARCHAR(50) DEFAULT 'aaa';

-- 删除列。

ALTER TABLE ts_table DROP c3;

-- 修改列的名称。

ALTER TABLE ts_table RENAME COLUMN c2 TO c4;

-- 修改列的数据类型。

ALTER TABLE ts_table ALTER COLUMN c3 TYPE INT8;

-- 修改列的默认值。

ALTER TABLE ts_table ALTER COLUMN c4 SET DEFAULT '789';

-- 删除列的默认值。

ALTER TABLE ts_table ALTER COLUMN c4 DROP DEFAULT;

-- 新增标签。

ALTER TABLE ts_table ADD TAG color VARCHAR(30);

-- 删除标签。

ALTER TABLE ts_table DROP TAG color;

-- 修改标签名。

ALTER TABLE ts_table RENAME TAG site TO location;

-- 修改标签的宽度。

ALTER TABLE ts_table ALTER color TYPE VARCHAR(50);
```

## 删除表

`DROP TABLE` 语句用于删除当前或指定数据库的所有表。

::: warning 说明
删除时序表时，系统检查当前时序表是否被流计算引用。如果是，则输出错误消息并列出所有引用此时序表的流计算名称。用户可以使用 `CASCADE` 关键字级联删除时序表及相关的流计算。
:::

### 所需权限

用户拥有目标表的 DROP 权限。删除成功后，所有用户针对目标表的所有权限均被删除。

### 语法格式

![](../../../static/sql-reference/PmXObFcQHogL4MxbNPKc8I1Pn1u.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 待删除表的名称。支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。如未指定，则默认使用当前数据库。|

### 语法示例

以下示例删除 `ts_table` 表。

```sql
DROP TABLE ts_table;
```
