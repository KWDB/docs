---
title: UPDATE
id: relational-update
---

# UPDATE

`UPDATE` 语句用于更新目标表中某行数据。当 `sql_safe_updates` 会话变量设置为 `true` 时，无法更新所有数据列数据。如需更新所有数据，应先将 `sql_safe_updates` 会话变量设置为 `false`。

## 所需权限

用户是 `admin` 角色的成员或者拥有目标表的 UPDATE 和 SELECT 权限。默认情况下，`root` 用户属于 `admin` 角色。

## 语法格式

![](../../../static/sql-reference/CxpwbXo5motA9QxTgzscFzLtnYd.png)

- `common_table_expr`

    ![](../../../static/sql-reference/Y5HCbIflLoltisxDzrGcqlgZndb.png)

- `limit_clause`

    ![](../../../static/sql-reference/D3Gwb55NkoEUjxxzpyacw5vingi.png)

- `sort_clause`

    ![](../../../static/sql-reference/Ve7zb135hoZ2snxPkoScGr30nfd.png)

- `target_list`

    ![](../../../static/sql-reference/FsbWbfNSkoOorxxxMn1cbI8wnif.png)

## 参数说明

| 参数 | 说明 |
| --- | --- |
| `common_table_expr` |可与 `WITH` 关键字结合，组成 `WITH AS` 短语。通过将需要频繁执行的 SQL 片段用别名添加到全局范围，可以在需要时直接调用该别名的 SQL 片段，从而减少重复执行，优化执行效率。 |
| `table_name` |待更新的行的表名。 |
| `AS table_alias_name` |目标表的别名。使用别名时，可以完全隐藏实际的表名。 |
| `column_name` | 待更新的列名。支持指定一个或多个列名，列名之间使用逗号（`,`）隔开。如果省略列名，将更新表中所有的列。|
| `a_expr` | 更新的新值、聚合函数或标量表达式。如需使用默认值填充所有列，将 `a_expr` 替换为 `DEFAULT VALUES`。如需为特定列使用默认值，在 `a_expr` 中保留该值或在适当位置使用 `DEFAULT`。|
| `FROM table_ref` | 在 `UPDATE` 表达式、`RETURNING` 子句和 `WHERE` 子句中引用但不更新的表。|
| `select_stmt` | 生成要写入数据的 `SELECT` 子句。确保每个值的数据类型与目标列的数据类型匹配。如果指定列名，必须按照列名指定的顺序提供列值。如未指定列名，则按照表中列的声明顺序提供列值。|
| `WHERE a_expr` | `UPDATE` 操作的筛选语句，只更新 `a_expr` 返回 `TRUE` 的记录。`a_expr` 必须是使用列返回布尔值的标量表达式（例如 `<column> = <value>`）。如未使用 `WHERE` 子句，则更新表中所有行中的数据。|
| sort_clause | `OEDER BY` 子句，指定更新操作的行顺序。|
| limit_clause | `LIMIT` 子句，限制更新操作的行数。|
| `RETURNING target_list` | 基于更新的行返回指定类型的列值。`target_list` 可以是表中特定列的名称。支持使用星号（`*`）表示返回所有列，也可以使用标量表达式指定列。如果不希望在响应中返回任何内容，甚至不返回更新的行数，使用 `RETURNING NOTHING`。 |

## 语法示例

以下示例假设已经创建 `accounts` 表并写入数据。

```sql
-- 1. 创建 accounts 表。

CREATE TABLE accounts(id INT8 DEFAULT unique_rowid() PRIMARY KEY, balance DECIMAL, customer STRING);
CREATE TABLE 

-- 2. 向 accounts 表中写入数据。

INSERT INTO accounts (id, balance, customer) VALUES (1, 10000.50, 'Zhang San'), (2, 4000.0, 'Li Si'), (3, 8700.0, 'Wang Wu'), (4, 3400.0, 'Zhao Liu');
INSERT 4

-- 3. 查看表数据。

SELECT * FROM accounts;
  id | balance  | customer
-----+----------+------------
   1 | 10000.50 | Zhang San
   2 |   4000.0 | Li Si
   3 |   8700.0 | Wang Wu
   4 |   3400.0 | Zhao Liu
(4 rows)
```

- 使用 `WHERE` 子句更新指定行中的某一列。

    ```sql
    -- 1. 更新 accounts 表。

    UPDATE accounts SET balance = 5000.0 WHERE id = 2;
    UPDATE 1

    -- 2. 查看表数据。

    SELECT * FROM accounts;
      id | balance  | customer
    -----+----------+------------
      1 | 10000.50 | Zhang San
      2 |   5000.0 | Li Si
      3 |   8700.0 | Wang Wu
      4 |   3400.0 | Zhao Liu 
    (4 rows)
    ```

- 使用 `WHERE` 子句更新指定行中的多列。

    ```sql
    -- 1. 更新 accounts 表。
    UPDATE accounts SET (balance, customer) = (9000.0, 'Qian Qi') WHERE id = 2;
    UPDATE 1

    -- 2. 查看表数据。

    SELECT * FROM accounts;
      id | balance  | customer
    -----+----------+------------
      1 | 10000.50 | Zhang San
      2 |   9000.0 | Qian Qi
      3 |   8700.0 | Wang Wu
      4 |   3400.0 | Zhao Liu
    (4 rows)

    -- 3. 更新 accounts 表。

    UPDATE accounts SET balance = 6300.0, customer = 'Sun Yang' WHERE id = 3;
    UPDATE 1

    -- 4. 查看表数据。

    SELECT * FROM accounts;
      id | balance  | customer
    -----+----------+------------
      1 | 10000.50 | Zhang San
      2 |   9000.0 | Qian Qi
      3 |   6300.0 | Sun Yang
      4 |   3400.0 | Zhao Liu
    (4 rows)
    ```

- 使用 `SELECT` 语句更新数据。

    ```sql
    -- 1. 更新 accounts 表。

    UPDATE accounts SET (balance, customer)=(SELECT balance, customer FROM accounts WHERE id = 2) WHERE id = 4;
    UPDATE 1

    -- 2. 查看表数据。

    SELECT * FROM accounts;
      id | balance  | customer
    -----+----------+------------
      1 | 10000.50 | Zhang San
      2 |   9000.0 | Qian Qi
      3 |   6300.0 | Sun Yang
      4 |   9000.0 | Qian Qi
    (4 rows)
    ```

- 使用默认值更新指定行。

    ```sql
    -- 1. 更新 accounts 表。

    UPDATE accounts SET balance = DEFAULT WHERE customer = 'Sun Yang';
    UPDATE 1

    -- 2. 查看表数据。

    SELECT * FROM accounts;
      id | balance  | customer
    -----+----------+------------
      1 | 10000.50 | Zhang San
      2 |   9000.0 | Qian Qi
      3 |   NULL   | Sun Yang
      4 |   9000.0 | Qian Qi
    (4 rows)
    ```

- 使用其他表的数据进行更新。

    ```sql
    -- 1. 创建 accounts2 表。

    CREATE TABLE accounts2(id INT8 DEFAULT unique_rowid(),balance DECIMAL);
    CREATE TABLE 

    -- 2. 向 accounts2 表中写入数据。

    INSERT INTO accounts2 (id, balance) VALUES (4, 1000);
    INSERT 1

    -- 3. 查看accounts2 表数据。

    SELECT * FROM accounts2;
    id|balance
    --+-------
    4 |1000   
    (1 row)

    -- 4. 更新 accounts 表。

    UPDATE accounts SET customer = 'Li Ming' FROM accounts2 WHERE accounts.id=accounts2.id;
    UPDATE 1

    -- 5. 查看 accounts 表数据。

    SELECT * FROM accounts;
      id | balance  | customer
    -----+----------+------------
      1 | 10000.50 | Zhang San
      2 |   9000.0 | Qian Qi
      3 | NULL     | Sun Yang
      4 |   9000.0 | Li Ming
    (4 rows)
    ```

- 更新所有行。

    ```sql
    -- 1. 设置 sql_safe_updates 会话参数。
    SET sql_safe_updates = false;
    SET

    -- 2. 更新 accounts 表。

    UPDATE accounts SET balance = 5000.0;
    UPDATE 4

    -- 3. 查看表数据。

    SELECT * FROM accounts;
      id | balance | customer
    -----+---------+------------
      1 |  5000.0 | Zhang San
      2 |  5000.0 | Qian Qi
      3 |  5000.0 | Sun Yang
      4 |  5000.0 | Li Ming
    (4 rows)
    ```

- 更新并返回特定列的值。

    ```sql
    UPDATE accounts SET balance = DEFAULT WHERE id = 1 RETURNING id;
      id
    ------
      1
    (1 row)
    ```
