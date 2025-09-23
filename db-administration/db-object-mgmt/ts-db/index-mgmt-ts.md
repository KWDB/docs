---
title: 索引管理
id: ts-index
---

# 索引管理

索引是基于单列或多列来组织数据的数据结构。时序表创建后，KWDB 会自动为主标签列创建索引，以加速数据查询。

KWDB 同时支持为普通标签列创建索引。创建索引后，用户在执行以下查询时，系统可以利用普通标签索引快速定位数据，而无需扫描整张表，从而提高查询性能：

- 等值查询，且输出列不含主标签列, 例如 `select c1, tag1 from t1 where tag1 = 100;`
- IN 查询，且输出列不含主标签列或其他普通标签索引，例如 `select c1, tag1 from t1 where tag1 in (100,200,300);`
- 已创建索引标签与其他普通列的组合查询，组合条件为 AND, 且输出列不含主标签列，例如 `select c1, tag1 from t1 where tag1 = 100 and c1 = 200;`
- 多个已创建索引标签的组合查询，组合条件为 OR 或 AND，且输出列不含主标签列，例如 `select c1, tag1 from t1 where tag1 = 100 or tag2 = 100;`

## 创建索引

### 所需权限

用户是 `admin` 角色的成员或拥有目标表的 CREATE 权限，默认情况下，`root` 用户属于 `admin` 角色。


### 语法格式

```sql
CREATE INDEX <index_name> ON <table_name> (<tag_name_list>);
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `index_name` | 待创建的索引名称。该名称在数据库中必须唯一，并且遵循[数据库标识符规则](../../../sql-reference/sql-identifiers.md)。 |
| `table_name` | 目标表的名称。 |
| `tag_name_list` | 待创建索引的标签名称列表，最多支持指定 4 个标签，标签名称之间用逗号分隔。注意：标签必须是普通标签，而不是主标签，数据类型必须是整数类型、浮点类型、CHAR 或 NCHAR 类型。|

### 语法示例

以下示例为 `temperature` 表的 `sensor_type` 普通标签列创建索引。

```sql
CREATE INDEX sensor_type_index ON temperature (sensor_type);
```

## 查看索引

`SHOW INDEXES` 语句用于查看时序表的索引信息。

### 所需权限

用户拥有目标表的任何权限。

### 语法格式

```sql
SHOW INDEXES FROM <table_name>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 索引所在表的名称。 |


### 语法示例

以下示例查看 `temperature` 表的所有索引。

```sql
SHOW INDEXES FROM temperature;
```

## 修改索引

`ALTER INDEX` 语句用于更改索引的名称。

### 所需权限

用户是 `admin` 角色的成员或拥有索引所属表的 CREATE 权限，默认情况下，`root` 用户属于 `admin` 角色。

### 语法格式

```sql
ALTER INDEX <index_name> RENAME TO <new_name>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `index_name` | 当前索引的名称。|
| `new_name` | 索引的新名称。该名称在数据库中必须唯一，并且[遵循数据库标识符规则](../../../sql-reference/sql-identifiers.md)。|

### 语法示例

以下示例将 `temperature` 表的 `sensor_type_index` 索引重命名为 `sensor_index`。

```sql
-- 1. 重命名索引。
ALTER INDEX sensor_type_index RENAME TO sensor_index;

-- 2. 检查是否修改成功。
SHOW INDEXES FROM temperature;
```

## 删除索引

`DROP INDEX` 语句用于删除表的索引。

### 所需权限

用户是 `admin` 角色的成员或拥有目标表的 CREATE 权限，默认情况下，`root` 用户属于 `admin` 角色。

### 语法格式

```sql
DROP INDEX <database_name>.<index_name>;
```

或

```sql
DROP INDEX <table_name>@<index_name>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `database_name` | 待删除索引所在的数据库名。|
| `table_name` | 待删除索引所在的表名。|
| `index_name` | 待删除索引的名称。|

### 语法示例

以下示例删除 `temperature` 表中的 `sensor_index` 索引。

```sql
-- 1. 删除 temperature 表中的 sensor_index 索引。
DROP INDEX temperature@sensor_index;

-- 2. 查看索引是否删除成功。
SHOW INDEXES FROM temperature;
```