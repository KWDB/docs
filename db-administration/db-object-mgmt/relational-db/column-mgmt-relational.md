---
title: 列管理
id: column-mgmt-relational
---

# 列管理

## 添加列

KWDB 支持在创建表时创建列，也支持使用 `ALTER TABLE ... ADD COLUMN` 语句为表创建列。`ADD COLUMN` 为在线操作，不会阻塞表中的数据读写。

### 前提条件

用户拥有目标表的 CREATE 权限。

### 语法格式

```sql
ALTER TABLE [IF EXISTS] <table_name> ADD [COLUMN] [IF NOT EXISTS] <column_name> <type_name> [<col_qual_list>];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF EXISTS`  | 可选关键字。当使用 `IF EXISTS` 关键字时，如果目标表存在，系统添加列。如果目标表不存在，系统添加列失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果目标表存在，系统添加列。如果目标表不存在，系统报错，提示目标表不存在。 |
| `table_name`  | 待添加列的表。 |
| `IF NOT EXISTS` | 可选关键字，当使用 `IF NOT EXISTS` 关键字时，如果列名不存在，系统创建列。如果列名存在，系统创建列失败，但不会报错。当未使用 `IF NOT EXISTS` 关键字时，如果列名不存在，系统创建列。如果列名存在，系统报错，提示列名已存在。 |
| `column_name`  | 待添加列的名称。该名称在表中必须唯一，并且遵循[数据库标识符规则](../../../sql-reference/sql-identifiers.md)。  |
| `type_name`  | 待添加列的数据类型。 |
| `col_qual_list`  | 列定义列表，支持定义以下信息：<br >- `<col_qualification_elem>`：`NULL`、`NOT NULL`、`UNIQUE`、`PRIMARY KEY`、`CHECK`、`DEFAULT`、`REFERENCES`、`AS`。<br >- `CONSTRAINT <constraint_name> <col_qualification_elem>` <br >- `COLLATE <collation_name>` <br >- `FAMILY <family_name>`：如果未指定列族，则该列将被添加到第一个列族。 <br >- `CREATE FAMILY [<family_name>]` <br > **说明** <br > KWDB 不支持直接添加带有外键约束的列。有关为列添加外键约束的详细信息，参见[添加约束](./constraint-mgmt-relational.md#添加约束)。 |

### 语法示例

- 添加单列。

    以下示例为 `re_users` 表添加一个名为 `names` 的列。

    ```sql
    -- 1. 为 re_users 表添加 names 列。

    ALTER TABLE re_users ADD COLUMN names STRING;
    ALTER TABLE

    -- 2. 查看 re_users 表的列。

    SHOW COLUMNS FROM re_users;
      column_name | data_type | is_nullable |  column_default   | generation_expression |              indices               | is_hidden | is_tag
    --------------+-----------+-------------+-------------------+-----------------------+------------------------------------+-----------+---------
      id          | UUID      |    false    | gen_random_uuid() |                       | {primary,re_users_credit_card_key} |   false   | false
      city        | STRING    |    false    | NULL              |                       | {primary,re_users_credit_card_key} |   false   | false
      name        | STRING    |    true     | NULL              |                       | {}                                 |   false   | false
      address     | STRING    |    true     | NULL              |                       | {}                                 |   false   | false
      credit_card | STRING    |    true     | NULL              |                       | {re_users_credit_card_key}         |   false   | false
    (5 rows)
    ```

- 添加多列。

    以下示例为 `re_users` 表添加 `location` 和 `amount` 列。

    ```sql
    -- 1. 为 re_users 表添加 location 和 amount 列。

    ALTER TABLE re_users ADD COLUMN location STRING, ADD COLUMN amount DECIMAL;
    ALTER TABLE

    -- 2. 查看 re_users 表的列。 

    SHOW COLUMNS FROM re_users;
      column_name | data_type | is_nullable |  column_default   | generation_expression |              indices               | is_hidden | is_tag
    --------------+-----------+-------------+-------------------+-----------------------+------------------------------------+-----------+---------
      id          | UUID      |    false    | gen_random_uuid() |                       | {primary,re_users_credit_card_key} |   false   | false
      city        | STRING    |    false    | NULL              |                       | {primary,re_users_credit_card_key} |   false   | false
      name        | STRING    |    true     | NULL              |                       | {}                                 |   false   | false
      address     | STRING    |    true     | NULL              |                       | {}                                 |   false   | false
      credit_card | STRING    |    true     | NULL              |                       | {re_users_credit_card_key}         |   false   | false
      location    | STRING    |    true     | NULL              |                       | {}                                 |   false   | false
      amount      | DECIMAL   |    true     | NULL              |                       | {}                                 |   false   | false
    (7 rows)
    ```

- 添加具有默认值的非空列。

    以下示例为 `re_users` 表添加具有默认值的 `interest` 列。

    ```sql
    -- 1. 为 re_users 表添加具有默认值的 interest 列。

    ALTER TABLE re_users ADD COLUMN interest DECIMAL NOT NULL DEFAULT (DECIMAL '1.3');
    ALTER TABLE

    -- 2. 查看 re_users 表的列。

    SHOW COLUMNS FROM re_users;

      column_name | data_type | is_nullable |     column_default     | generation_expression |              indices               | is_hidden | is_tag
    --------------+-----------+-------------+------------------------+-----------------------+------------------------------------+-----------+---------
      id          | UUID      |    false    | gen_random_uuid()      |                       | {primary,re_users_credit_card_key} |   false   | false
      city        | STRING    |    false    | NULL                   |                       | {primary,re_users_credit_card_key} |   false   | false
      name        | STRING    |    true     | NULL                   |                       | {}                                 |   false   | false
      address     | STRING    |    true     | NULL                   |                       | {}                                 |   false   | false
      credit_card | STRING    |    true     | NULL                   |                       | {re_users_credit_card_key}         |   false   | false
      location    | STRING    |    true     | NULL                   |                       | {}                                 |   false   | false
      amount      | DECIMAL   |    true     | NULL                   |                       | {}                                 |   false   | false
      interest    | DECIMAL   |    false    | 1.3:::DECIMAL::DECIMAL |                       | {}                                 |   false   | false
    (8 rows)
    ```

- 添加具有唯一值的非空列。

    以下示例为 `re_users` 表添加具有唯一值的 `cust_number` 列。

    ```sql
    ALTER TABLE re_users ADD COLUMN cust_number DECIMAL UNIQUE NOT NULL;
    ```

- 添加列并将其分配给新列族。

    以下示例为 `re_users` 表添加 `location1` 列并将其分配给新列族。

    ```sql
    ALTER TABLE re_users ADD COLUMN location1 STRING CREATE FAMILY new_family;
    ```

- 添加列并将其分配给当前列族。

    以下示例为 `re_users` 表添加 `location2` 列并将其分配给当前列族。

    ```sql
    ALTER TABLE re_users ADD COLUMN location2 STRING FAMILY existing_family;
    ```

- 如果列族不存在，添加列并创建新列族。

    以下示例为 `re_users` 表添加 `new_name` 列，创建 `f1` 列族，并将 `new_name` 列分配给 `f1` 列族。

    ```sql
    ALTER TABLE re_users ADD COLUMN new_name STRING CREATE IF NOT EXISTS FAMILY f1;
    ```

## 查看列

`SHOW COLUMNS` 语句用于查看表中列的详细信息，包括列的名称、类型、默认值、是否非空。

### 前提条件

用户拥有目标表的任何权限。

### 语法格式

```sql
SHOW COLUMNS FROM <table_name> [WITH COMMENT];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 列所在表的名称。 |
| `WITH COMMENT` | 可选关键字，查看列的注释信息。默认情况下，列的注释信息为 `NULL`。 |

### 语法示例

以下示例查看 `re_users` 表的列。

```sql
SHOW COLUMNS FROM re_users;
```

执行成功后，控制台输出以下信息：

```sql
  column_name |     data_type     | is_nullable |     column_default     | generation_expression |              indices               | is_hidden | is_tag
--------------+-------------------+-------------+------------------------+-----------------------+------------------------------------+-----------+---------
  id          | UUID              |    false    | gen_random_uuid()      |                       | {primary,re_users_credit_card_key} |   false   | false
  city        | STRING            |    false    | NULL                   |                       | {primary,re_users_credit_card_key} |   false   | false
  name        | STRING            |    true     | NULL                   |                       | {}                                 |   false   | false
  address     | STRING            |    true     | NULL                   |                       | {}                                 |   false   | false
  credit_card | STRING            |    true     | NULL                   |                       | {re_users_credit_card_key}         |   false   | false
  location    | STRING            |    true     | NULL                   |                       | {}                                 |   false   | false
  amount      | DECIMAL           |    true     | NULL                   |                       | {}                                 |   false   | false
  interest    | DECIMAL           |    false    | 1.3:::DECIMAL::DECIMAL |                       | {}                                 |   false   | false
  more_names  | STRING COLLATE en |    true     | NULL                   |                       | {}                                 |   false   | false
(9 rows)
```

## 修改列

KWDB 支持使用 `ALTER TABLE ... ALTER COLUMN` 语句执行以下操作。`ALTER COLUMN` 为在线操作，不会阻塞表中的数据读写。

- 配置、更改、删除列的默认值。
- 配置、删除列的 `NOT NULL` 约束。
- 修改列的数据类型。

### 前提条件

用户拥有目标表的 CREATE 权限。

### 语法格式

```sql
ALTER TABLE [IF EXISTS] <table_name> ALTER [COLUMN] <column_name> 
[SET DEFAULT <a_expr> |SET NOT NULL | DROP DEFAULT | DROP NOT NULL | DROP STORED | [SET DATA] TYPE <type_name> [COLLATE <collation_name>] ];
```

### 支持的操作

- SET
  - `SET DEFAULT`：默认值约束。系统写入表数据时写入指定的默认值，从而不需要显式定义该列的值。如果列已经存在默认值，可以使用此语句修改列的默认值。
  - `SET NOT NULL`：指定列不允许出现空值。
- DROP
  - `DROP DEFAULT`：删除已定义的默认值约束，删除后将不再写入默认值。
  - `DROP NOT NULL`：删除非空约束。删除非空约束后，该列的值可以为空。
  - `DROP STORED`：将计算出的列转换为常规列。
- `SET DATA TYPE`：修改列的数据类型，`SET DATA` 是可选关键字，是否使用不影响修列的数据类型。

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF EXISTS`  | 可选关键字。当使用 `IF EXISTS` 关键字时，如果目标表存在，系统修改列。如果目标表不存在，系统修改列失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果目标表存在，系统修改列。如果目标表不存在，系统报错，提示目标表不存在。 |
| `table_name`  | 表名，支持通过 `<database_name>.<table_name>` 指定其他数据库中的表。 |
| `COLUMN` | 可选关键字，是否使用不影响修改列。 |
| `column_name`  | 待修改列的名称。 |
| `a_expr` | 待使用的默认值。|
| `type_name`  | 待修改列的数据类型。 |
| `collation_name`  | 排序规则的名称。 |

### 语法示例

- 配置、更改列的默认值。

    以下示例将 `office_dogs` 表 `alive` 列的默认值设置为 `true`。

    ```sql
    ALTER TABLE office_dogs ALTER COLUMN alive SET DEFAULT 'true';
    ```

- 删除列的默认值约束。

    以下示例删除 `office_dogs` 表 `alive` 列的默认值约束。

    ```sql
    ALTER TABLE office_dogs ALTER COLUMN alive DROP DEFAULT;
    ```

- 删除列的非空约束。

    以下示例删除 `office_dogs` 表 `alive` 列的非空约束。

    ```sql
    ALTER TABLE office_dogs ALTER COLUMN alive DROP NOT NULL;
    ```

- 将计算列转换为常规列。

    以下示例将 `office_dogs` 表的 `full_name` 列转换为常规列。

    ```sql
    -- 1. 创建数据库。

    CREATE TABLE office_dogs (                                                 
                        id INT8 NOT NULL,                                                      
                        first_name STRING NULL,                                                
                        last_name STRING NULL,                                                 
                        full_name STRING NULL AS (concat(first_name, ' ', last_name)) STORED,  
                        alive STRING NULL,                                                     
                        CONSTRAINT "primary" PRIMARY KEY (id ASC),                             
                        FAMILY "primary" (id, first_name, last_name, full_name, alive)         
                    );
    CREATE TABLE

    -- 2. 写入数据。

    INSERT INTO office_dogs (id, first_name, last_name) VALUES(1, 'Petee', 'Hirate'), (2, 'Carl', 'Kimball'), (3, 'Ernie', 'Narayan');
    INSERT 3

    -- 3. 查看表数据。

    SELECT * FROM office_dogs;
      id | first_name | last_name |   full_name   | alive
    -----+------------+-----------+---------------+--------
      1 | Petee      | Hirate    | Petee Hirate  | NULL
      2 | Carl       | Kimball   | Carl Kimball  | NULL
      3 | Ernie      | Narayan   | Ernie Narayan | NULL
    (3 rows)

    -- 4. 将 full_name 列转为常规列。full_name 列是根据 first_name 列和 last_name 列计算得出的列。

    ALTER TABLE office_dogs ALTER COLUMN full_name DROP STORED;
    ALTER TABLE

    -- 5. 查看是否已经将 full_name 列转为常规列。

    SHOW COLUMNS FROM office_dogs;
      column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
    --------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
      id          | INT8      |    false    | NULL           |                       | {primary} |   false   | false
      first_name  | STRING    |    true     | NULL           |                       | {}        |   false   | false
      last_name   | STRING    |    true     | NULL           |                       | {}        |   false   | false
      full_name   | STRING    |    true     | NULL           |                       | {}        |   false   | false
      alive       | STRING    |    true     | NULL           |                       | {}        |   false   | false
    (5 rows)

    -- 6. 写入数据。计算列变成常规列后，数据写入方式也发生了变化。

    INSERT INTO office_dogs (id, first_name, last_name, full_name) VALUES (4, 'Lola', 'McDog', 'This is not computed');
    INSERT 1

    -- 7. 查看表数据。

    SELECT * FROM office_dogs;
      id | first_name | last_name |      full_name       | alive
    -----+------------+-----------+----------------------+--------
      1 | Petee      | Hirate    | Petee Hirate         | NULL
      2 | Carl       | Kimball   | Carl Kimball         | NULL
      3 | Ernie      | Narayan   | Ernie Narayan        | NULL
      4 | Lola       | McDog     | This is not computed | NULL
    (4 rows)
    ```

## 重命名列

KWDB 支持使用 `ALTER TABLE ... RENAME COLUMN` 语句修改列名。

### 前提条件

用户拥有目标表的 CREATE 权限。

### 语法格式

```sql
ALTER TABLE [IF EXISTS] <table_name> RENAME [COLUMN] <current_name> TO <new_name>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF EXISTS` | 可选关键字。当使用 `IF EXISTS` 关键字时，如果目标表存在，系统重命名目标列。如果目标表不存在，系统重命名目标列失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果目标表存在，系统重命名目标列。如果目标表不存在，系统报错，提示目标表不存在。 |
| `table_name` | 待重命名列所在表的名称。|
| `current_name` | 列的当前名称。|
| `new_name` | 列的新名称。|

### 语法示例

以下示例将 `orders` 表的 `customer` 列重命名为 `customer_id`。

```sql
-- 1. 查看 orders 表的列。

SHOW COLUMNS FROM orders;
  column_name |   data_type   | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+---------------+-------------+----------------+-----------------------+-----------+-----------+---------
  customer    | INT4          |    false    | NULL           |                       | {primary} |   false   | false
  id          | INT4          |    false    | NULL           |                       | {primary} |   false   | false
  total       | DECIMAL(20,5) |    true     | NULL           |                       | {}        |   false   | false
(3 rows)

-- 2. 将 orders 表的 customer 列重命名为 customer_id。

ALTER TABLE orders RENAME customer TO customer_id;
ALTER TABLE

-- 3. 查看 orders 表的列。

SHOW COLUMNS FROM orders;
  column_name |   data_type   | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+---------------+-------------+----------------+-----------------------+-----------+-----------+---------
  customer_id | INT4          |    false    | NULL           |                       | {primary} |   false   | false
  id          | INT4          |    false    | NULL           |                       | {primary} |   false   | false
  total       | DECIMAL(20,5) |    true     | NULL           |                       | {}        |   false   | false
(3 rows)
```

## 删除列

KWDB 支持使用 `ALTER TABLE ... DROP COLUMN` 语句修改列名。`DROP COLUMN` 为在线操作，不会阻塞表中的数据读写。

### 前提条件

用户拥有目标表的 CREATE 权限。

### 语法格式

```sql
ALTER TABLE [IF EXISTS] <table_name> DROP COLUMN [IF EXISTS] <name> [CASCADE | RESTRICT];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF EXISTS` | 可选关键字。当使用 `IF EXISTS` 关键字时，如果目标列存在，系统删除目标列。如果目标列不存在，系统删除目标列失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果目标列存在，系统删除目标列。如果目标列不存在，系统报错，提示目标列不存在。 |
| `table_name` | 待删除列所在表的名称。|
| `name` | 待删除列的名称。如果目标列配置检查约束，检查约束也会被一同删除。|
| `CASCADE` | 可选关键字。删除目标列及其关联对象。`CASCADE` 不会列出待删除的关联对象，应谨慎使用。 |
| `RESTRICT` | 默认设置，可选关键字。如果其他对象依赖目标列，则无法删除该列。 |

### 语法示例

- 删除列。

    以下示例删除 `office_dogs` 表的 `alive` 列。

    ```sql
    ALTER TABLE office_dogs DROP COLUMN alive;
    ALTER TABLE
    ```

- 阻止删除包含关联对象的列。

    以下示例阻止删除 `office_dogs` 表带有关联对象的 `first_name` 列。

    ```sql
    ALTER TABLE office_dogs DROP COLUMN first_name RESTRICT;
    ```

- 删除列及其关联对象。

    以下示例删除 `office_dogs` 表的 `first_name` 列及其关联的 `test_view` 视图。

    ::: warning 说明
    默认情况下，当 `sql_safe_updates` 会话变量设置为 `true` 时，禁止执行潜在不安全的 SQL 语句。当 `sql_safe_updates` 会话变量设置为 `false` 时，支持删除非空数据库及其所有从属对象语句、没有 `WHERE` 子句的 `DELETE` 语句、没有 `WHERE` 子句的 `UPDATE` 语句、以及 `ALTER TABLE ... DROP COLUMN` 等语句。如需执行级联删除操作，必须将 `sql_safe_updates` 会话变量设置为 `false`。
    :::

    ```sql
    -- 1. 为 office_dogs 表的 first_name 列创建 test_view 视图。

    CREATE VIEW test_view (first_name) AS SELECT first_name FROM db4.public.office_dogs;
    CREATE VIEW

    -- 2. 查看创建的 test_view 视图。

    SHOW CREATE test_view;
    table_name|create_statement                                                                   
    ----------+-----------------------------------------------------------------------------------
    test_view |CREATE VIEW test_view (first_name) AS SELECT first_name FROM db4.public.office_dogs
    (1 row)

    -- 3. 级联删除 first_name 列及其关联视图，系统报错。

    ALTER TABLE office_dogs DROP COLUMN first_name CASCADE;
    ERROR: rejected: ALTER TABLE DROP COLUMN will remove all data in that column (sql_safe_updates = true)

    -- 4. 修改 sql_safe_updates 设置。

    SET sql_safe_updates = FALSE;
    SET 

    -- 5. 查看 sql_safe_updates 设置。

    SHOW sql_safe_updates;
    sql_safe_updates
    ----------------
    off             
    (1 row)

    -- 6. 级联删除 first_name 列及其关联视图，删除成功
    ALTER TABLE office_dogs DROP COLUMN first_name CASCADE;
    ALTER TABLE
    
    -- 7. 查看创建的 test_view 视图。

    SHOW CREATE test_view;
    ERROR:  relation "test_view" does not exist
    ```
