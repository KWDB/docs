---
title: 索引管理
id: index-mgmt-relational
---

# 索引管理

## 创建索引

KWDB 支持为表或物化视图创建标准索引和倒排索引。创建索引后，系统可以使用索引快速定位数据而无需查看表或物化视图的全部数据，有助于提高数据库的性能。

::: warning 说明
KWDB 不支持为物化视图创建交错索引（Interleaving Index）、Hash-sharded 索引、唯一性索引（UNIQUE Index）。
:::

KWDB 支持创建函数索引，函数索引的索引列不是表中的列，而是函数列。在搜索时，触发函数索引的不是投影列，而是 `WHERE` 条件的左值是否为函数索引存放的函数。在搜索带有固定函数的数据时，可以减少计算时间，提高搜索效率。目前，函数索引不支持窗口函数、聚合函数、子查询以及带返回值的函数等。如果使用了这些未支持的函数，客户端将报告类型错误。当前支持的函数包括数学和数值函数（例如 `abs` 和 `floor`）、字符串和字节函数、比较函数等。

### 前提条件

用户拥有目标表或物化视图的 CREATE 权限。

### 语法格式

- 标准索引

    ```sql
    CREATE [UNIQUE] INDEX [CONCURRENTLY] [IF NOT EXISTS] [<index_name>] ON {<table_name> | <mv_name>}
    [USING <name>] 
    (<column_name> [ASC | DESC], <column_name> [ASC | DESC], ...) 
    [COVERING | STORING | INCLUDE] (<name_list>) 
    [interleave_clause];
    ```

- 倒排索引

    ```sql
    CREATE [UNIQUE] INVERTED INDEX [CONCURRENTLY] [IF NOT EXISTS] [<index_name>] ON {<table_name> | <mv_name>}
    (<column_name> [ASC | DESC], <column_name> [ASC | DESC], ...) 
    [COVERING | STORING | INCLUDE] (<name_list>) 
    [interleave_clause];
    ```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `UNIQUE` | 可选关键字，为索引列应用唯一性约束，系统在创建索引时检查重复值。在表级别应用唯一性约束，系统在写入或更新表数据时会检查重复值。<br > **说明** <br > 物化视图不支持创建唯一性索引。 |
| `CONCURRENTLY` | 可选关键字，兼容 PostgreSQL 语法，表示 KWDB 支持并发创建索引，无需额外操作。 |
| `IF NOT EXISTS` | 可选关键字，当使用 `IF NOT EXISTS` 关键字时，如果索引名不存在，系统创建索引。如果索引名存在，系统创建索引失败，但不会报错。当未使用 `IF NOT EXISTS` 关键字时，如果索引名不存在，系统创建索引。如果索引名存在，系统报错，提示索引名已存在。 |
| `index_name` | 待创建的索引的名称。该名称在数据库中必须唯一，并且遵循[数据库标识符规则](../../../sql-reference/sql-identifiers.md)。 |
| `table_name` | 待创建索引的目标表的名称。 |
| `mv_name` | 待创建索引的目标物化视图的名称。 |
| `USING name` | 与第三方工具兼容的可选子句。`name` 支持 `btree` 和 `gin`。其中，`btree` 表示标准的二级索引，`gin` 用于 JSONB 列中无模式数据的倒排索引，与 PostgreSQL 兼容。 |
| `column_name` | 待创建索引的目标列的名称。 |
| `ASC` 或 `DESC` | 在索引中按升序（ASC）或降序（DESC）对列进行排序。列的排序方式会影响查询结果，尤其是在使用 `LIMIT` 语句时。默认为 `ASC`。  |
| `STORING` | 存储指定列的值但不对其进行排序。当只检索但不过滤列值时，存储列有助于提高查的性能。`COVERING` 和 `INCLUDE` 是 `STORING` 的别名，工作原理相同。<br > **说明** <br > 主键列无法指定为 `STORING` 表二级索引中的列。使用存储列时，查询必须包括索引列，并且至少包括对一个索引列的过滤条件，才能检索存储的列值。 |
| `interleave_clause` | 支持使用交错索引（Interleaving Indexes）优化查询性能，这会改变 KWDB 存储数据的方式。<br > **说明** <br > 物化视图不支持创建交叉索引。  |
| `INVERTED` | 在指定的 JSONB 列上创建倒排索引，适用于无模式数据。也可以使用与 PostgreSQL 兼容的语法 `USING GIN`。 |

### 语法示例

- 创建单列索引，对单列的值进行排序。

    以下示例为 `re_users` 表的 `city` 列创建索引，并对 `city` 列的取值进行排序。

    ```sql
    CREATE INDEX ON re_users (city);
    CREATE INDEX
    ```

- 创建多列索引按列出的顺序对列进行排序。

    以下示例为 `re_users` 表的 `city` 和 `name` 列创建索引，并对根据列的顺序进行排序。

    ```sql
    CREATE INDEX ON re_users (city, name);
    CREATE INDEX
    ```

- 创建唯一索引，不允许其列中包含重复值。

    以下示例为  `re_users` 表的 `credit_card` 和 `dl` 列创建唯一索引。这同样适用于设置表级别的唯一约束，等同于 `ALTER TABLE re_users ADD CONSTRAINT re_users_credit_card_dl_key UNIQUE (credit_card, dl);`

    ```sql
    CREATE UNIQUE INDEX ON re_users (credit_card, dl);
    CREATE INDEX
    ```

- 创建倒排索引。

    以下示例为 `users` 表创建倒排索引。

    ```sql
    CREATE INVERTED INDEX ON users (profile);
    ```

- 存储列。

    以下示例为 `products` 表的 `price` 列创建索引，并存储 `name` 列的值。

    ```sql
    CREATE INDEX ON products (price) STORING (name);
    ```

- 更改排序顺序。

    以下示例为 `products` 表的 `price` 和 `stock` 列创建索引，并对 `price` 列进行降序排列。

    ```sql
    CREATE INDEX ON products (price DESC, stock);
    ```

- 查询特定索引。

    以下示例查看 `customers` 表的 `customers_id_idx` 索引。

    ```sql
    -- 1. 查看 customers 表的索引。

    SHOW INDEX FROM customers;
      table_name |       index_name       | non_unique | seq_in_index | column_name | direction | storing | implicit
    -------------+------------------------+------------+--------------+-------------+-----------+---------+-----------
      customers  | primary                |   false    |            1 | id          | ASC       |  false  |  false
      customers  | customers_id_idx       |    true    |            1 | id          | ASC       |  false  |  false
      customers  | customers_name_id_idx  |    true    |            1 | name        | ASC       |  false  |  false
      customers  | customers_name_id_idx  |    true    |            2 | id          | ASC       |  false  |  false
    (4 rows)

    -- 2. 查看 customers_id_idx  索引。

    SELECT name FROM customers@customers_id_idx;
        name
    --------------
      Li Ming
      Liu Yang
      Wang Cheng
    (3 rows)
    ```

- 创建函数索引。

    以下示例为 `t1` 表创建函数索引。

    ```sql
    -- 1. 创建表。
    CREATE TABLE t1 (a FLOAT);
    CREATE TABLE

    -- 2. 创建函数索引。

    CREATE INDEX idx ON t1(abs(a));
    CREATE INDEX

    -- 3. 写入数据。

    INSERT INTO t1 VALUES (0),(1);
    INSERT 2

    -- 4. 查询数据。

    EXPLAIN (opt,verbose) SELECT * FROM t1 WHERE abs(a)>-1 ;
    +-------------------------------------------------------+
      scan t1@idx                                            
      ├── columns: a:1                                   
      ├── CONSTRAINT: /1/3/2: [/-0.9999999999999999 - ]  
      ├── stats: [rows=333.333333]                       
      └── cost: 346.676667                               
    (5 rows）
    ```

- 创建物化视图的索引。

    以下示例为 `small_order` 物化视图创建索引。

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

    -- 2. 创建 small_order 物化视图，获取订单号和订单金额。

    CREATE MATERIALIZED VIEW small_order (id, amount) AS SELECT id, total FROM orders;

    -- 3. 为 small_order 物化视图创建索引。

    CREATE INDEX idx1 ON small_order(id)
    ```

## 查看索引

`SHOW INDEX` 语句用于查看目标表、数据库、物化视图的索引信息。

### 前提条件

用户拥有对应数据库、表、物化视图的任意权限。

### 语法格式

```sql
SHOW [INDEX | INDEXES | KEYS] FROM [<table_name> | DATABASE <database_name> | <mview_name>] [WITH COMMENT];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 索引所在表的名称。 |
| `database_name` | 索引所在数据库的名称。 |
| `mview_name` | 索引所在物化视图的名称。 |
| `WITH COMMENT` | 可选关键字，查看索引的注释信息。默认情况下，索引的注释信息为 `NULL`。 |

### 返回字段说明

| 字段 | 说明 |
| --- | --- |
| `table_name` | 表名。 |
| `index_name` | 索引名。|
| `non_unique` | 索引列中的值是否唯一。 |
| `seq_in_index` | 列在索引中的位置，从 `1` 开始计数。 |
| `column_name` | 索引的列。 |
| `direction` | 列在索引中的排序方式。存储列的值为 `N/A`。 |
| `storing` | 在创建索引过程中是否使用 `STORING` 子句。|
| `implicit` | 是否隐式包含列在索引中。 |

### 语法示例

- 查看表的索引。

    以下示例查看 `re_users` 表的索引。

    ```sql
    SHOW INDEX FROM re_users;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      table_name |        index_name        | non_unique | seq_in_index | column_name | direction | storing | implicit
    -------------+--------------------------+------------+--------------+-------------+-----------+---------+-----------
      re_users   | primary                  |   false    |            1 | city        | ASC       |  false  |  false
      re_users   | primary                  |   false    |            2 | id          | ASC       |  false  |  false
      re_users   | re_users_city_idx        |    true    |            1 | city        | ASC       |  false  |  false
      re_users   | re_users_city_idx        |    true    |            2 | id          | ASC       |  false  |   true
      re_users   | re_users_city_name_idx   |    true    |            1 | city        | ASC       |  false  |  false
      re_users   | re_users_city_name_idx   |    true    |            2 | name        | ASC       |  false  |  false
      re_users   | re_users_city_name_idx   |    true    |            3 | id          | ASC       |  false  |   true
      re_users   | re_users_credit_card_key |   false    |            1 | credit_card | ASC       |  false  |  false
      re_users   | re_users_credit_card_key |   false    |            2 | city        | ASC       |  false  |   true
      re_users   | re_users_credit_card_key |   false    |            3 | id          | ASC       |  false  |   true
    (10 rows)
    ```

- 查看物化视图的索引。

    以下示例查看 `small_order` 物化视图的索引。

    ```sql
    -- 查看当前数据库中的表。
    SHOW TABLES;
      table_name  |    table_type
    --------------+--------------------
      accounts    | BASE TABLE
      small_order | MATERIALIZED VIEW
    (2 rows)

    -- 查看指定物化视图的索引。
    SHOW INDEX FROM small_order;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      table_name  | index_name | non_unique | seq_in_index | column_name | direction | storing | implicit
    --------------+------------+------------+--------------+-------------+-----------+---------+-----------
      small_order | primary    |   false    |            1 | rowid       | ASC       |  false  |  false
      small_order | idx1       |    true    |            1 | id          | ASC       |  false  |  false
      small_order | idx1       |    true    |            2 | rowid       | ASC       |  false  |   true
    (3 rows)
    ```

## 修改索引

`ALTER INDEX` 语句用于更改索引的名称和对指定行进行范围分割。

### 前提条件

- 更改索引名称：用户拥有索引所属表或物化视图的 CREATE 权限。
- 对指定行进行范围分割：用户拥有索引的 INSERT 权限。

### 语法格式

- 更改索引名称。

    ```sql
    ALTER INDEX [IF EXISTS] [<table_name> @ | <mv_name> @] <index_name> RENAME TO <new_name>;
    ```

- 在索引中的指定行上强制进行范围分割。

    ```sql
    ALTER INDEX [<table_name> @] <index_name> SPLIT AT <select_stmt> [WITH EXPIRATION <a_expr>];
    ```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF EXISTS` | 可选关键字。当使用 `IF EXISTS` 关键字时，如果目标索引存在，系统修改目标索引。如果目标索引不存在，系统修改目标索引失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果目标索引存在，系统修改目标索引。如果目标索引不存在，系统报错，提示目标索引不存在。 |
| `table_name` | 索引所在表的名称。支持使用 `SHOW TABLES` 语句查找表名。 |
| `mv_name` | 索引所在物化视图的名称。支持使用 `SHOW TABLES` 语句查找物化视图名。 |
| `index_name` | 当前索引的名称。|
| `new_name` | 索引的新名称。该名称在数据库中必须唯一，并且[遵循数据库标识符规则](../../../sql-reference/sql-identifiers.md)。|
| `SPLIT AT` | 在索引中的指定行上强制进行范围分割。|
| `select_stmt` | `SELECT` 查询语句。选择查询，查询结果为一个或多个用于拆分索引的行。|
| `a_expr` | 强制执行索引分割的到期时间，支持 DECIMAL、INTERVAL、TIMESTAMP 或 TIMESTAMPTZ 数据类型。|

### 语法示例

- 重命名索引。

    以下示例将 `re_users` 表的 `re_users_city_idx` 索引重命名为 `re_users_city_idx_rename`。

    ```sql
    -- 1. 查看 re_users 表的索引。

    SHOW INDEXES FROM re_users;
      table_name |        index_name        | non_unique | seq_in_index | column_name | direction | storing | implicit
    -------------+--------------------------+------------+--------------+-------------+-----------+---------+-----------
      re_users   | primary                  |   false    |            1 | city        | ASC       |  false  |  false
      re_users   | primary                  |   false    |            2 | id          | ASC       |  false  |  false
      re_users   | re_users_city_idx        |    true    |            1 | city        | ASC       |  false  |  false
      re_users   | re_users_city_idx        |    true    |            2 | id          | ASC       |  false  |   true
      re_users   | re_users_city_name_idx   |    true    |            1 | city        | ASC       |  false  |  false
      re_users   | re_users_city_name_idx   |    true    |            2 | name        | ASC       |  false  |  false
      re_users   | re_users_city_name_idx   |    true    |            3 | id          | ASC       |  false  |   true
      re_users   | re_users_credit_card_key |   false    |            1 | credit_card | ASC       |  false  |  false
      re_users   | re_users_credit_card_key |   false    |            2 | city        | ASC       |  false  |   true
      re_users   | re_users_credit_card_key |   false    |            3 | id          | ASC       |  false  |   true
    (10 rows)

    -- 2. 将 re_users 表的 re_users_city_idx 索引重命名为 re_users_city_idx_rename。

    ALTER INDEX re_users@re_users_city_idx RENAME TO re_users_city_idx_rename;
    ALTER INDEX

    -- 3. 查看 re_users 表的索引。

    SHOW INDEXES FROM re_users;
      table_name |        index_name        | non_unique | seq_in_index | column_name | direction | storing | implicit
    -------------+--------------------------+------------+--------------+-------------+-----------+---------+-----------
      re_users   | primary                  |   false    |            1 | city        | ASC       |  false  |  false
      re_users   | primary                  |   false    |            2 | id          | ASC       |  false  |  false
      re_users   | re_users_city_idx_rename |    true    |            1 | city        | ASC       |  false  |  false
      re_users   | re_users_city_idx_rename |    true    |            2 | id          | ASC       |  false  |   true
      re_users   | re_users_city_name_idx   |    true    |            1 | city        | ASC       |  false  |  false
      re_users   | re_users_city_name_idx   |    true    |            2 | name        | ASC       |  false  |  false
      re_users   | re_users_city_name_idx   |    true    |            3 | id          | ASC       |  false  |   true
      re_users   | re_users_credit_card_key |   false    |            1 | credit_card | ASC       |  false  |  false
      re_users   | re_users_credit_card_key |   false    |            2 | city        | ASC       |  false  |   true
      re_users   | re_users_credit_card_key |   false    |            3 | id          | ASC       |  false  |   true
    (10 rows)
    ```

- 拆分索引。

    以下示例拆分 `customers` 表的 `customers_id_idx` 索引。

    ```sql
    -- 1. 查看 customers 表的索引。

    SHOW INDEX FROM customers;
      table_name |       index_name       | non_unique | seq_in_index | column_name | direction | storing | implicit
    -------------+------------------------+------------+--------------+-------------+-----------+---------+-----------
      customers  | primary                |   false    |            1 | id          | ASC       |  false  |  false
      customers  | customers_id_idx       |    true    |            1 | id          | ASC       |  false  |  false
      customers  | customers_name_id_idx  |    true    |            1 | name        | ASC       |  false  |  false
      customers  | customers_name_id_idx  |    true    |            2 | id          | ASC       |  false  |  false
      customers  | customers_name_id_idx1 |    true    |            1 | name        | ASC       |  false  |  false
      customers  | customers_name_id_idx1 |    true    |            2 | id          | ASC       |  false  |  false
    (6 rows)

    -- 2. 拆分 customers 表的 customers_id_idx 索引。

    ALTER INDEX customers@customers_id_idx SPLIT AT SELECT id FROM customers;
            key        |       pretty        |       split_enforced_until
    -------------------+---------------------+-----------------------------------
      \xf6c18af80186a1 | /Table/193/2/100001 | 2262-04-11 23:47:16.854776+00:00
      \xf6c18af80186a2 | /Table/193/2/100002 | 2262-04-11 23:47:16.854776+00:00
      \xf6c18af80186a3 | /Table/193/2/100003 | 2262-04-11 23:47:16.854776+00:00
    (3 rows)

    -- 3. 查看 customers_id_idx 索引 的数据分片。

    SHOW RANGES FROM INDEX customers@customers_id_idx;
      start_key | end_key | range_id | range_size_mb | lease_holder | lease_holder_locality | replicas | replica_localities
    ------------+---------+----------+---------------+--------------+-----------------------+----------+---------------------
      NULL      | /100001 |      162 |      0.000109 |            1 |                       | {1}      | {""}
      /100001   | /100002 |      177 |      0.000026 |            1 |                       | {1}      | {""}
      /100002   | /100003 |      178 |      0.000026 |            1 |                       | {1}      | {""}
      /100003   | NULL    |      179 |       0.00025 |            1 |                       | {1}      | {""}
    (4 rows)
    ```

## 删除索引

`DROP INDEX` 语句用于删除表或物化视图的索引信息。

### 前提条件

用户拥有索引所属表或物化视图的 CREATE 权限。

### 语法格式

```sql
DROP INDEX [CONCURRENTLY] [IF EXISTS] [<table_name>@ | <mv_name> @]<index_name> [CASCADE | RESTRICT];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `CONCURRENTLY` | 可选关键字，兼容 PostgreSQL 语法，表示 KWDB 支持并发删除索引，无需额外操作。 |
| `IF EXISTS` | 可选关键字。当使用 `IF EXISTS` 关键字时，如果目标索引存在，系统删除目标索引。如果目标索引不存在，系统删除目标索引失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果目标索引存在，系统删除目标索引。如果目标索引不存在，系统报错，提示目标索引不存在。 |
| `table_name` | 索引所在表的名称。支持使用 `SHOW TABLES` 语句查找表名。 |
| `mv_name` | 索引所在物化视图的名称。支持使用 `SHOW TABLES` 语句查找物化视图名。 |
| `index_name` | 待删除索引的名称。支持使用 `SHOW INDEX` 查找索引名称。不支持删除表的主索引。|
| `CASCADE` | 可选关键字。删除目标索引及其关联对象。`CASCADE` 不会列出待删除的关联对象，应谨慎使用。 |
| `RESTRICT` | 默认设置，可选关键字。如果其他对象依赖目标索引，则无法删除该索引。 |

### 语法示例

- 删除没有依赖关系的索引。

    以下示例删除 `t1` 表中没有依赖关系的 `t1_name_idx` 索引。

    ```sql
    -- 1. 查看 t1 表的索引。

    SHOW INDEX FROM t1;
    table_name | index_name  | non_unique | seq_in_index | column_name | direction | storing | implicit |
    -----------+-------------+------------+--------------+-------------+-----------+---------+----------+
    t1         | primary     |   false    |            1 | id          | ASC       |  false  |  false   |
    t1         | t1_name_idx |    true    |            1 | name        | ASC       |  false  |  false   |
    t1         | t1_name_idx |    true    |            2 | id          | ASC       |  false  |   true   |
    (3 rows)

    -- 2. 删除 t1 表中没有依赖关系的 t1_name_idx 索引。

    DROP INDEX t1@t1_name_idx;
    DROP INDEX 

    -- 3. 查看 t1 表的索引。

    SHOW INDEX FROM t1;
    table_name | index_name | non_unique | seq_in_index | column_name | direction | storing | implicit |
    -----------+------------+------------+--------------+-------------+-----------+---------+----------+
    t1         | primary    |   false    |            1 | id          | ASC       |  false  |  false   |
    (1 row)
    ```

- 删除具有依赖关系的索引。

    以下示例删除 `orders` 表中具有依赖关系的 `orders_auto_index_fk_customer_ref_customers` 索引。

    ```sql

    -- 1. 查看 orders 表的索引。

    SHOW INDEX FROM orders;
    table_name |                 index_name                  | non_unique | seq_in_index | column_name | direction | storing | implicit |
    -----------+---------------------------------------------+------------+--------------+-------------+-----------+---------+----------+
    orders     | primary                                     |   false    |            1 | id          | ASC       |  false  |  false   |
    orders     | orders_auto_index_fk_customer_ref_customers |    true    |            1 | customer    | ASC       |  false  |  false   |
    orders     | orders_auto_index_fk_customer_ref_customers |    true    |            2 | id          | ASC       |  false  |   true   |
    (3 rows)

    -- 2. 删除 orders 表中具有依赖关系的 orders_auto_index_fk_customer_ref_customers 索引，系统删除索引失败。

    DROP INDEX orders_auto_index_fk_customer_ref_customers;
    pq: index "orders_auto_index_fk_customer_ref_customers" is in use as a foreign key CONSTRAINT

    -- 3. 查看 orders 表的约束。

    SHOW CONSTRAINTS FROM orders;
    table_name |      CONSTRAINT_name      | CONSTRAINT_type |                     details                      | validated |
    -----------+---------------------------+-----------------+--------------------------------------------------+-----------+
    orders     | fk_customer_ref_customers | FOREIGN KEY     | FOREIGN KEY (customer) REFERENCES customers (id) |   true    |
    orders     | primary                   | PRIMARY KEY     | PRIMARY KEY (id ASC)                             |   true    |
    (2 rows)

    -- 4. 级联删除 orders 表中具有依赖关系的 orders_auto_index_fk_customer_ref_customers 索引，系统删除索引成功。

    DROP INDEX orders_auto_index_fk_customer_ref_customers CASCADE;
    DROP INDEX

    -- 5. 查看 orders 表的约束。

    SHOW CONSTRAINTS FROM orders;
    table_name | CONSTRAINT_name | CONSTRAINT_type |       details        | validated |
    -----------+-----------------+-----------------+----------------------+-----------+
    orders     | primary         | PRIMARY KEY     | PRIMARY KEY (id ASC) |   true    |
    (1 row)
    ```

- 删除物化视图的索引。

    以下示例删除 `small_order` 物化视图的 `idx1` 索引。

    ```sql
    DROP INDEX small_order@idx1
    ```
