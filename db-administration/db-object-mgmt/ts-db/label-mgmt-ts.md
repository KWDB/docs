---
title: 标签管理
id: label-mgmt-ts
---

# 标签管理

数据库标签（TAG）描述数据对象特征和行为，例如数据类型、长度、默认值等。标签定义了数据对象的结构和规则，确保数据的完整性和有效性。

KWDB 支持使用 ATTRIBUTE 和 ATTRIBUTES 作为 TAG 和 TAGS 的别名。

## 添加标签

KWDB 支持在创建表时创建表的标签，也支持使用 `ALTER TABLE ... ADD TAG` 语句为表添加标签。`ADD TAG` 为在线操作，不会阻塞表中的数据读写

::: warning 说明
目前，KWDB 不支持一次添加多个标签或者为已有时序表添加主标签和非空标签。
:::

### 前提条件

用户拥有目标表的 CREATE 权限。

### 语法格式

```sql
ALTER TABLE <table_name> ADD [TAG | ATTRIBUTE] <tag_name> <tag_type>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。 |
| `tag_name` | 标签名，不支持数据库级别的自定义标签。标签名的最大长度为 128 字节。 |
| `tag_type` | 标签类型，不支持 TIMESTAMP、TIMESTAMPTZ、NVARCHAR、GEOMETRY 数据类型。 |

### 语法示例

以下示例为 `ts_table` 表添加名为 `color` 的标签。

```sql
ALTER TABLE ts_table ADD TAG color VARCHAR(30);
```

## 查看标签

### 前提条件

用户拥有目标表的任何权限。

### 语法格式

```sql
SHOW [TAGS | ATTRIBUTES] FROM <table_name>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。 |

### 语法示例

以下示例查看 `sensor_data` 表的标签。

```sql
SHOW TAGS FROM sensor_data;
```

执行成功后，控制台输出以下信息：

```sql
      tag     |    type     | is_primary | nullable
--------------+-------------+------------+-----------
  sensor_id   | INT4        |    true    |  false
  sensor_type | VARCHAR(30) |   false    |  false
(2 rows)
```

## 查看标签值

### 前提条件

用户拥有目标表的 SELECT 权限。

### 语法格式

```sql
SHOW TAG VALUES FROM <table_name>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。 |

### 语法示例

以下示例查看 `sensor_data` 表的标签值。

```sql
SHOW TAG VALUES FROM sensor_data;
```

执行成功后，控制台输出以下信息：

```sql
  sensor_id 
------------
          1
(1 row)
```

## 修改标签

### 修改数据类型和宽度

KWDB 支持使用 `ALTER TABLE ... ALTER TAG` 语句修改标签的数据类型和宽度。`ALTER TAG` 为在线操作，不会阻塞表中的数据读写。

::: warning 说明

在分布式集群下避免修改标签的数据类型和宽度。

:::

#### 前提条件

用户拥有目标表的 CREATE 权限。

#### 语法格式

```sql
ALTER TABLE <table_name> ALTER [TAG | ATTRIBUTE] <tag_name> [SET DATA] TYPE <new_type>;
```

#### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。如未指定，则默认使用当前数据库。|
| `tag_name` | 待修改标签的名称。 |
| `SET DATA:` | 可选关键字，是否使用不影响修改标签的数据类型和宽度。 |
| `new_type` |  拟修改的数据类型和宽度。<br > **说明** <br >- 转换后的数据类型宽度必须大于原数据类型的宽度。例如，INT4 可以转成 INT8，但不能转成 INT2，CHAR(200) 可以转为 VARCHAR (254), 但不能转为 VARCHAR (100)。<br >- CHAR、VARCHAR、NCHAR、NVARCHAR 字符类型支持同数据类型的宽度转换，但只能增加宽度不能降低宽度。例如，CHAR(100) 可以转转为 CHAR(200)，不能转为 CHAR(50)。有关 KWDB 支持修改的数据类型、默认宽度、最大宽度、可转换的数据类型等详细信息，参见[时序数据类型](../../../sql-reference/data-type/data-type-ts-db.md)。 |

#### 语法示例

以下示例将 `ts_table` 表的 `color` 标签的宽度修改为 `VARCHAR(50)`。

```sql
ALTER TABLE ts_table ALTER color TYPE VARCHAR(50);
```

### 修改标签名称

KWDB 支持使用 `ALTER TABLE ... RENAME TAG` 语句修改标签名称。

#### 前提条件

用户拥有目标表的 CREATE 权限。

#### 语法格式

```sql
ALTER TABLE <table_name> RENAME [ TAG | ATTRIBUTE] <old_name> TO <new_name>;
```

#### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。如未指定，则默认使用当前数据库。|
| `old_name` | 当前标签名，不支持修改主标签名称。 |
| `new_name` | 拟修改的标签名。标签名的最大长度为 128 字节。 |

#### 语法示例

以下示例将 `ts_table` 表的 `site` 标签重命名为 `location`。

```sql
ALTER TABLE ts_table RENAME TAG site TO location;
```

### 修改标签值

KWDB 支持通过 `UPDATE` 语句修改标签值。

#### 前提条件

用户拥有目标表的 UPDATE 权限。

#### 语法格式

```sql
UPDATE <table_name> SET <tag_name> = <tag_value> <where_clause>;
```

#### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。如未指定，则默认使用当前数据库。 |
| `tag_name` | 标签名，不支持修改主标签的标签值。 |
| `tag_value` | 标签值。|
| `where_clause` | 指定表的主标签和主标签值，格式为 `where <primary_tag> = <tag_value>`。如果目标表有多个主标签，需要列出所有主标签及主标签值，用 `and` 连接。 |

#### 语法示例

以下示例修改含有多个主标签的表的标签值。

```sql
-- 1. 创建时序数据库 ts。

CREATE TS DATABASE ts;
CREATE TS DATABASE

-- 2. 使用时序数据库 ts。

USE ts;
SET

-- 3. 创建时序表 table1 并写入数据。

CREATE TABLE table1 (time timestamp not null, e1 smallint, e2 float, e3 bool)
tags (tag1 smallint not null, tag2 int not null, tag3 bool)
primary tags (tag1, tag2);
CREATE TABLE

insert into table1 values ('2023-05-31 10:00:00', 1000,1000000,true, 1, 1, false), ('2023-05-31 11:00:00', 2000,2000000, true, 1, 1, false), ('2023-05-31 10:00:00', 1000,1000000,true, 2, 1, false), ('2023-05-31 11:00:00', 2000,2000000,true, 2, 1, false), ('2023-05-31 10:00:00', 1000,1000000,true, 3, 1, false), ('2023-05-31 11:00:00', 2000,2000000,true, 3, 1, false);
INSERT 6

-- 4. 查看表数据。

select * from table1;
            time            |  e1  |  e2   |  e3  | tag1 | tag2 | tag3
----------------------------+------+-------+------+------+------+--------
  2023-05-31 10:00:00+00:00 | 1000 | 1e+06 | true |    1 |    1 | false
  2023-05-31 11:00:00+00:00 | 2000 | 2e+06 | true |    1 |    1 | false
  2023-05-31 10:00:00+00:00 | 1000 | 1e+06 | true |    2 |    1 | false
  2023-05-31 11:00:00+00:00 | 2000 | 2e+06 | true |    2 |    1 | false
  2023-05-31 10:00:00+00:00 | 1000 | 1e+06 | true |    3 |    1 | false
  2023-05-31 11:00:00+00:00 | 2000 | 2e+06 | true |    3 |    1 | false
(6 rows)

-- 5. 指定 table1 表的主标签值的情况下，修改 tag3 标签的标签值。

UPDATE table1 SET tag3 = true WHERE tag1 = 1 and tag2 =1;
UPDATE 1
select * from table1;
            time            |  e1  |  e2   |  e3  | tag1 | tag2 | tag3
----------------------------+------+-------+------+------+------+--------
  2023-05-31 10:00:00+00:00 | 1000 | 1e+06 | true |    2 |    1 | false
  2023-05-31 11:00:00+00:00 | 2000 | 2e+06 | true |    2 |    1 | false
  2023-05-31 10:00:00+00:00 | 1000 | 1e+06 | true |    3 |    1 | false
  2023-05-31 11:00:00+00:00 | 2000 | 2e+06 | true |    3 |    1 | false
  2023-05-31 10:00:00+00:00 | 1000 | 1e+06 | true |    1 |    1 | true
  2023-05-31 11:00:00+00:00 | 2000 | 2e+06 | true |    1 |    1 | true
(6 rows)
```

## 删除标签

KWDB 支持使用 `ALTER TABLE ... DROP TAG` 语句删除标签。`DROP TAG` 为在线操作，不会阻塞表中的数据读写。

::: warning 说明

- KWDB 不支持删除主标签。
- 目前，KWDB 不支持一次删除多个标签。

:::

### 前提条件

用户拥有目标表的 CREATE 权限。

### 语法格式

```sql
ALTER TABLE <table_name> DROP [TAG | ATTRIBUTE] <tag_name>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。如未指定，则默认使用当前数据库。 |
| `tag_name` | 待删除标签的名称，不支持删除主标签。|

### 语法示例

以下示例删除 `ts_table` 表的 `color` 标签。

```sql
ALTER TABLE ts_table DROP TAG color;
```
