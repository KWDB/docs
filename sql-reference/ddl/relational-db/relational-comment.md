---
title: 注释
id: relational-comment
---

# 注释

## 添加注释

`COMMENT ON` 语句用于为数据库、表、列、索引、存储过程添加注释。

### 所需权限

用户拥有操作对象的 CREATE 权限。

### 语法格式

![](../../../static/sql-reference/addcomment.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `database_name` | 数据库的名称。 |
| `table_name` | 表的名称。 |
| `column_name` |列的名称。 |
| `index_name` | 索引的名称。 |
| `proc_name` | 存储过程的名称。|
| `comment_text` | 注释内容。 |

### 语法示例

- 为数据库添加注释。

    以下示例为 `db3` 数据库添加注释。

    ```sql
    -- 1. 添加注释。

    COMMENT ON DATABASE db3 IS 'database for order statistics';
    COMMENT ON DATABASE

    -- 2. 查看注释。

    SHOW DATABASES WITH COMMENT;
      database_name | engine_type |            comment
    ----------------+-------------+--------------------------------
      db1           | RELATIONAL  | NULL
      db2           | RELATIONAL  | NULL
      db3           | RELATIONAL  | database for order statistics
    ...
    (6 rows)
    ```

- 为表添加注释。

    以下示例为 `orders` 表添加注释。

    ```sql
    -- 1. 添加注释。

    COMMENT ON TABLE orders IS 'orders from 2020 till now.';
    COMMENT ON TABLE

    -- 2. 查看注释。

    SHOW TABLES WITH COMMENT;
      table_name | table_type |          comment
    -------------+------------+-----------------------------
      orders     | BASE TABLE | orders from 2020 till now.
      order_list | BASE TABLE |
    (2 rows)
    ```

- 为列添加注释。

    以下示例为 `orders` 表的 `id` 列添加注释。

    ```sql
    -- 1. 添加注释。

    COMMENT ON COLUMN orders.id IS 'auto-generated';
    COMMENT ON COLUMN

    -- 2. 查看注释。

    SHOW COLUMNS FROM orders WITH COMMENT;
      column_name | data_type | is_nullable | column_default  | generation_expression |                 indices                 | is_hidden | is_tag |    comment
    --------------+-----------+-------------+-----------------+-----------------------+-----------------------------------------+-----------+--------+-----------------
      id          | INT4      |    false    | NULL            |                       | {primary,orders_customer_id_key_rename} |   false   | false  | auto-generated
      date        | TIMESTAMP |    false    | NULL            |                       | {}                                      |   false   | false  | NULL
      priority    | INT4      |    true     | 1:::INT8        |                       | {}                                      |   false   | false  | NULL
      customer_id | INT4      |    true     | NULL            |                       | {orders_customer_id_key_rename}         |   false   | false  | NULL
      status      | STRING    |    true     | 'open':::STRING |                       | {}                                      |   false   | false  | NULL
    (5 rows)
    ```

- 为索引添加注释。

    以下示例为 `orders` 表的 `primary` 索引添加注释。

    ```sql
    -- 1. 添加注释。

    COMMENT ON INDEX orders @ primary is 'auto-generated';
    COMMENT ON INDEX

    -- 2. 查看注释。

    SHOW INDEXES FROM orders WITH COMMENT;
      table_name |          index_name           | non_unique | seq_in_index | column_name | direction | storing | implicit |    comment
    -------------+-------------------------------+------------+--------------+-------------+-----------+---------+----------+-----------------
      orders     | primary                       |   false    |            1 | id          | ASC       |  false  |  false   | auto-generated
      orders     | orders_customer_id_key_rename |   false    |            1 | customer_id | ASC       |  false  |  false   | NULL
      orders     | orders_customer_id_key_rename |   false    |            2 | id          | ASC       |  false  |   true   | NULL
    (3 rows)
    ```

- 为存储过程添加注释。

    以下示例为 `proc1` 存储过程添加注释。

    ```sql
    -- 1. 添加注释。

    ALTER PROCEDURE proc1 COMMENT IS 'test query sql and if else logical';

    -- 2. 查看存储过程的注释信息。

    SHOW PROCEDURES WITH COMMENT;
    procedure_name |              comment
    -----------------+-------------------------------------
    proc1           | test query sql and if else logical
    (1 row)
    ```