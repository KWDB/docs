---
title: 视图管理
id: view-mgmt-relational
---

# 视图管理

视图，即系统存储的以虚拟表形式表示的查询结果。

## 创建视图

### 前提条件

用户是 `admin` 角色的成员或者拥有所属数据库的 CREATE 权限和引用表的 SELECT 权限。默认情况下，`root` 用户属于 `admin` 角色。

### 语法格式

```sql
CREATE VIEW [IF NOT EXISTS] <view_name> [(<name_list>)] AS <select_stmt>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF NOT EXISTS` | 可选关键字，当使用 `IF NOT EXISTS` 关键字时，如果目标视图不存在，系统创建视图。如果目标视图存在，系统创建视图失败，但不会报错。当未使用 `IF NOT EXISTS` 关键字时，如果目标视图不存在，系统创建视图。如果目标视图存在，系统报错，提示目标视图已存在。 |
| `view_name` | 待创建视图的名称，该名称在数据库中必须唯一，并且遵循[数据库标识符规则](../../../sql-reference/sql-identifiers.md)。如果没有将父数据库设置为默认值，必须将视图名称格式设置为 `database.view_name`。 |
| `name_list` | 可选项，视图列名列表。支持指定一个或多个视图的列名，列名之间使用逗号（`,`）隔开。如果指定视图的列名，控制台输出指定的列名，而不是输出通过 `select_stmt` 语句指定的列的列名。 |
| `select_stmt` | `SELECT` 查询语句。支持使用 `*` 选择源表中的所有列。<br >- 当 `select_stmt` 的结果集中存在同名列时，系统报错，提示 `duplicate column name: "a"`。<br >- 当源表新增列后，视图结构不会发生变化。<br >- 当删除视图依赖的源表中的列时，系统报错，提示 `cannot drop column "b" because view "v" depends on it`。|

### 语法示例

以下示例假设已经创建一个名为 `orders` 的表，包括顾客 ID，订单号和订单金额，并为 `orders` 表创建一个名为 `short_order` 视图，获取订单号和订单金额，并显示列名。

```sql
-- 1. 查看 orders 表的信息。

SELECT * FROM orders;
  customer_id |   id   | total
--------------+--------+--------
       100001 | 100001 |   234
       100001 | 100002 |   120
       100002 | 100003 |    59
       100002 | 100004 |   120
(4 rows)

-- 2. 创建 short_order 视图，获取订单号和订单金额，并显示列名。

CREATE VIEW short_order (id, amount) AS SELECT id, total FROM orders;
CREATE VIEW

-- 3. 查看视图信息。

SELECT * FROM short_order;
    id   | amount
---------+---------
  100001 |    234
  100002 |    120
  100003 |     59
  100004 |    120
(4 rows)
```

## 修改视图

### 前提条件

用户是 `admin` 角色的成员或者拥有重命名前视图的 DROP 权限以及重命名后视图所属父数据库的 CREATE 权限。默认情况下，`root` 用户属于 `admin` 角色。

### 语法格式

```sql
ALTER VIEW [IF EXISTS] <view_name> RENAME TO <name>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF EXISTS` | 可选关键字。当使用 `IF EXISTS` 关键字时，如果目标视图存在，系统修改目标视图。如果目标视图不存在，系统修改目标视图失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果目标视图存在，系统修改目标视图。如果目标视图不存在，系统报错，提示目标视图不存在。 |
| `view_name` | 待重命名的视图的名称。支持使用 `SELECT * FROM information_schema.tables WHERE table_type = 'VIEW'` 语句查看视图名称。 |
| `name` | 新的视图名称。该名称在数据库中必须唯一，并且[遵循数据库标识符规则](../../../sql-reference/sql-identifiers.md)。 |

### 语法示例

以下示例将 `test_view` 视图重命名为 `names`。

```sql
-- 1. 查看所有视图。

SELECT * FROM information_schema.tables WHERE table_type = 'VIEW';
  table_catalog | table_schema | table_name  | table_type | is_insertable_into | version | namespace_oid
----------------+--------------+-------------+------------+--------------------+---------+----------------
  db2           | public       | test_view   | VIEW       | NO                 |       1 |    1497612465
  db2           | public       | short_order | VIEW       | NO                 |       1 |    1497612465
(2 rows)

-- 2. 将 test_view 视图重命名为 names。

ALTER VIEW test_view rename to names;
RENAME VIEW

-- 3. 查看所有视图。

SELECT * FROM information_schema.tables WHERE table_type = 'VIEW';
  table_catalog | table_schema | table_name  | table_type | is_insertable_into | version | namespace_oid
----------------+--------------+-------------+------------+--------------------+---------+----------------
  db2           | public       | names       | VIEW       | NO                 |       3 |    1497612465
  db2           | public       | short_order | VIEW       | NO                 |       1 |    1497612465
(2 rows)
```

## 删除视图

### 前提条件

- 删除无依赖关系的视图：用户是 `admin` 角色的成员或者拥有目标视图的 DROP 权限。默认情况下，`root` 用户属于 `admin` 角色。
- 删除存在依赖关系的视图：用户是 `admin` 角色的成员或者拥有目标视图及其关联对象的 DROP 权限。默认情况下，`root` 用户属于 `admin` 角色。

### 语法格式

```sql
DROP VIEW [IF EXISTS] <view_name_list> [CASCADE | RESTRICT];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF EXISTS` | 可选关键字。当使用 `IF EXISTS` 关键字时，如果目标视图存在，系统删除目标视图。如果目标视图不存在，系统删除目标视图失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果目标视图存在，系统删除目标视图。如果目标视图不存在，系统报错，提示目标视图不存在。 |
| `view_name_list` | 待删除的视图名称列表。支持指定一个或多个无依赖关系的视图，视图名称之间使用逗号（`,`）隔开。支持使用 `SELECT * FROM information_schema.tables WHERE table_type = 'VIEW'` 语句查看视图名称。  |
| `CASCADE` | 可选关键字。删除目标视图及其关联对象。`CASCADE` 不会列出待删除的关联对象，应谨慎使用。 |
| `RESTRICT` | 默认设置，可选关键字。如果其他对象依赖目标视图，则无法删除该视图。 |

### 语法示例

以下示例删除 `names` 视图。

```sql
-- 1. 查看所有视图。

SELECT * FROM information_schema.tables WHERE table_type = 'VIEW';
  table_catalog | table_schema | table_name  | table_type | is_insertable_into | version | namespace_oid
----------------+--------------+-------------+------------+--------------------+---------+----------------
  db2           | public       | names       | VIEW       | NO                 |       3 |    1497612465
  db2           | public       | short_order | VIEW       | NO                 |       1 |    1497612465
(2 rows)

-- 2. 删除 names 视图。

DROP VIEW names;
DROP VIEW

-- 3. 查看所有视图。

SELECT * FROM information_schema.tables WHERE table_type = 'VIEW';
  table_catalog | table_schema | table_name  | table_type | is_insertable_into | version | namespace_oid
----------------+--------------+-------------+------------+--------------------+---------+----------------
  db2           | public       | short_order | VIEW       | NO                 |       1 |    1497612465
(1 row)
```
