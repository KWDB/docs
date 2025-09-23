---
title: 注释
id: ts-comment
---

# 注释

## 添加注释

`COMMENT ON` 语句用于为数据库、表、列添加注释。

### 所需权限

用户是 `admin` 角色的成员或者拥有操作对象的 CREATE 权限。默认情况下，`root` 用户属于 `admin` 角色。

### 语法格式

![](../../../static/sql-reference/add_comment_ts.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `database_name` | 数据库的名称。 |
| `table_name` | 表的名称。 |
| `column_name` | 列的名称。 |
| `comment_text` | 注释内容。当目标对象已有注释信息，如果新的注释消息不为空，系统将更新目标对象的原有注释信息。如果新的注释消息为空，系统将删除目标对象的原有注释信息。 |

### 语法示例

- 为数据库添加注释。

    以下示例为 `ts_db` 数据库添加注释。

    ```sql
    -- 1. 添加注释。

    COMMENT ON DATABASE ts_db IS 'database for power statistics';
    COMMENT ON DATABASE

    -- 2. 查看注释。

    SHOW DATABASES WITH COMMENT;
      database_name | engine_type |            comment
    ----------------+-------------+--------------------------------
      db1           | RELATIONAL  | NULL
      db2           | RELATIONAL  | NULL
      ts_db         | RELATIONAL  | database for power statistics
    ...
    (6 rows)
    ```

- 为表添加注释。

    以下示例为 `power` 表添加注释。

    ```sql
    -- 1. 添加注释。

    COMMENT ON TABLE power IS 'power for all devices';
    COMMENT ON TABLE

    -- 2. 查看注释。

    SHOW TABLES WITH COMMENT;
      table_name  |    table_type     |      comment
    --------------+-------------------+--------------------
      power       | TIME SERIES TABLE | power for all devices
    (1 row)
    ```

- 为列添加注释。

    以下示例为 `power` 表的 `ts` 列添加注释。

    ```sql
    -- 1. 添加注释。

    COMMENT ON COLUMN power.ts IS 'auto-generated';
    COMMENT ON COLUMN

    -- 2. 查看注释。

    SHOW COLUMNS FROM power WITH COMMENT;
      column_name |  data_type  | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag |              comment
    --------------+-------------+-------------+----------------+-----------------------+-----------+-----------+--------+-------------------------------------
      ts          | TIMESTAMPTZ |    false    | NULL           |                       | {primary} |   false   | false  | auto-generated
      col         | INT4        |    true     | NULL           |                       | {}        |   false   | false  | NULL
      tag1        | INT4        |    false    | NULL           |                       | {}        |   false   |  true  | primary tag for comment
      tag2        | INT4        |    true     | NULL           |                       | {}        |   false   |  true  | tag for comment
    (4 rows)
    ```
