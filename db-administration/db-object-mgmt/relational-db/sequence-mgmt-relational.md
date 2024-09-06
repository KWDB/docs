---
title: 序列管理
id: sequence-mgmt-relational
---

# 序列管理

## 创建序列

### 前提条件

用户拥有新建序列所属数据库的 CREATE 权限。

### 语法格式

```sql
CREATE SEQUENCE [IF NOT EXISTS] <seq_name> 
[NO [CYCLE | MINVALUE | MAXVALUE] 
|OWNED BY [NONE | <column_name>] 
|INCREMENT [BY] <integer> 
|MINVALUE <integer> 
|MAXVALUE <integer> 
|START [WITH] <integer> 
|VIRTUAL];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `seq_name` | 待创建的序列的名称，该名称在数据库中必须唯一，并且遵循[数据库标识符规则](../../../sql-reference/sql-identifiers.md)。如果没有将父数据库设置为默认值，必须将名称格式设置为 `database.seq_name`。 |
| `NO CYCLE` | 当前所有序列都设置为 `NO CYCLE`，即不循环序列。  |
| `OWNED BY` | 将序列与表中的特定列进行关联。默认值为 `OWNED BY NONE`。如果删除关联列或者关联列所属的表，关联序列也会一同被删除。使用 `OWNED BY` 指定关联列会覆盖序列现有关联的列。如需移除序列的关联列并使序列变为独立序列，可以使用 `OWNED BY NONE`。 |
| `INCREMENT` | 序列递增的值。取值为负数，创建递减序列。取值为正数，创建递增序列。默认值为 `1`。 |
| `MINVALUE` | 序列的最小值。如未指定或输入 `NO MINVALUE`，则使用默认值。递增序列的默认值为 `1`。递减序列的默认值为 `MININT`。 |
| `MAXVALUE` | 序列的最大值。如未指定或输入 `NO MAXVALUE`，则使用默认值。递增序列的默认值为 `MAXINT`。递减序列的默认值为 `-1`。 |
| `START` | 序列的起始值。递增序列的默认值为 `1`。递减序列的默认值为 `-1`。  |

### 语法示例

- 使用默认配置创建序列。

    以下示例使用默认配置创建 `orders_seq` 序列。

    ```sql
    -- 1. 创建 orders_seq 序列。

    CREATE SEQUENCE orders_seq;
    CREATE SEQUENCE

    -- 2. 查看 orders_seq 序列。

    SHOW CREATE orders_seq;
      table_name |                                    create_statement
    -------------+-----------------------------------------------------------------------------------------
      orders_seq | CREATE SEQUENCE orders_seq MINVALUE 1 MAXVALUE 9223372036854775807 INCREMENT 1 START 1
    (1 row)
    ```

- 使用自定义配置创建序列。

    以下示例创建 `desc_orders_list` 序列，并将序列的起始值和递增值分别设置为 `-1` 和 `-2`。

    ```sql
    -- 1. 创建 desc_orders_list 序列。

    CREATE SEQUENCE desc_orders_list START -1 INCREMENT -2;
    CREATE SEQUENCE

    -- 2. 查看 desc_orders_list 序列。

    SHOW CREATE desc_orders_list;
        table_name    |                                         create_statement
    -------------------+---------------------------------------------------------------------------------------------------
      desc_orders_list | CREATE SEQUENCE desc_orders_list MINVALUE -9223372036854775808 MAXVALUE -1 INCREMENT -2 START -1
    (1 row)
    ```

- 使用序列创建表。

    以下示例使用 `orders_seq` 序列创建 `order_list` 表。

    ```sql

    -- 1. 使用 orders_seq 序列创建 order_list 表。

    CREATE TABLE order_list (id int primary key default nextval ('orders_seq'), customer string, date date);
    CREATE TABLE

    -- 2. 写入数据。

    INSERT INTO order_list (customer, date) values ('Li Ming', '2024-01-02'), ('Li Hua', '2024-01-02');
    INSERT 2

    -- 3. 查看表数据。

    SELECT * FROM order_list;
      id | customer |           date
    -----+----------+----------------------------
      1 | Li Ming  | 2024-01-02 00:00:00+00:00
      2 | Li Hua   | 2024-01-02 00:00:00+00:00
    (2 rows)
    ```

- 查看序列的当前值。

    以下示例查看 `customer_seq` 序列的信息。

    ```sql
    SELECT * FROM customer_seq;
      last_value | log_cnt | is_called
    -------------+---------+------------
              2 |       0 |   true
    (1 row)
    ```

    如果当前会话从序列获取新值，支持使用 `currval('seq_name')` 函数获取最新的序列值。

    ```sql
    SELECT currval('customer_seq');
    currval
    -------
    2      
    (1 row)
    ```

- 查看所有序列。

    ```sql
    SELECT * FROM information_schema.sequences;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      sequence_catalog | sequence_schema |  sequence_name   | data_type | numeric_precision | numeric_precision_radix | numeric_scale | start_value |    minimum_value     |    maximum_value    | increment | cycle_option
    -------------------+-----------------+------------------+-----------+-------------------+-------------------------+---------------+-------------+----------------------+---------------------+-----------+---------------
      db3              | public          | orders_seq       | bigint    |                64 |                       2 |             0 | 1           | 1                    | 9223372036854775807 | 1         | NO
      db3              | public          | desc_orders_list | bigint    |                64 |                       2 |             0 | -1          | -9223372036854775808 | -1                  | -2        | NO
    (2 rows)
    ```

## 查看序列

`SHOW SEQUENCES` 用于查看数据库的序列信息。

### 语法格式

```sql
SHOW SEQUENCES [FROM <name>];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `name` | 数据库名称。如未指定，则默认查看当前数据库的序列。 |

### 语法示例

以下示例查看当前数据库的序列。

```sql
SHOW SEQUENCES;
```

执行成功后，控制台输出以下信息：

```sql
   sequence_name
--------------------
  desc_orders_list
  orders_seq
(2 rows)
```

## 修改序列

`ALTER SEQUENCE` 语句用于修改序列的名称、增量值和其他设置。

### 前提条件

用户拥有序列所属数据库的 CREATE 权限。

### 语法格式

```sql
ALTER SEQUENCE [IF EXISTS] <seq_name> 
[NO [CYCLE | MINVALUE | MAXVALUE] 
|OWNED BY [NONE | <column_name>] 
|INCREMENT [BY] <integer> 
|MINVALUE <integer> 
|MANVALUE <integer> 
|START [WITH] <integer> 
|VIRTUAL];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF EXISTS` | 可选关键字。当使用 `IF EXISTS` 关键字时，如果目标序列存在，系统修改目标序列。如果目标序列不存在，系统修改目标序列失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果目标序列存在，系统修改目标序列。如果目标序列不存在，系统报错，提示目标序列不存在。 |
| `seq_name` | 待创建的序列的名称，该名称在数据库中必须唯一，并且[遵循数据库标识符规则](../../../sql-reference/sql-identifiers.md)。如果没有将父数据库设置为默认值，必须将名称格式设置为 `database.seq_name`。 |
| `NO CYCLE` | 当前所有序列都设置为 `NO CYCLE`，即不循环序列。  |
| `OWNED BY` | 将序列与表中的特定列进行关联。默认值为 `OWNED BY NONE`。如果删除关联列或者关联列所属的表，关联序列也会一同被删除。使用 `OWNED BY` 指定关联列会覆盖序列现有关联的列。如需移除序列的关联列并使序列变为独立序列，可以使用 `OWNED BY NONE`。 |
| `INCREMENT` | 序列递增的值。取值为负数，创建递减序列。取值为正数，创建递增序列。默认值为 `1`。 |
| `MINVALUE` | 序列的最小值。如未指定或输入 `NO MINVALUE`，则使用默认值。递增序列的默认值为 `1`。递减序列的默认值为 `MININT`。 |
| `MAXVALUE` | 序列的最大值。如未指定或输入 `NO MAXVALUE`，则使用默认值。递增序列的默认值为 `MAXINT`。递减序列的默认值为 `-1`。 |
| `START` | 序列的起始值。递增序列的默认值为 `1`。递减序列的默认值为 `-1`。  注意：使用 `ALTER SEQUENCE` 语句修改序列起始值后, 变更不会立刻生效，建议使用 `SELECT SETval()`语句手动设置序列的当前值，具体示例见设置序列的下一个值。|

### 语法示例

- 更改序列的增量值。

    以下示例将 `orders_seq` 序列的增量值设置为 `2`。

    ```sql
    -- 1. 将 orders_seq 序列的增量值设置为 2。

    ALTER SEQUENCE orders_seq INCREMENT 2;
    ALTER SEQUENCE

    -- 2. 向表 order_list 中写入数据，并检查新记录是否符合新序列设置。

    INSERT INTO order_list (customer, date) values ('Zhou Mi', '2024-01-02');
    INSERT 1

    -- 3. 查看表数据。

    SELECT * FROM order_list;
      id | customer |           date
    -----+----------+----------------------------
      1 | Li Ming  | 2024-01-02 00:00:00+00:00
      2 | Li Hua   | 2024-01-02 00:00:00+00:00
      4 | Zhou Mi  | 2024-01-02 00:00:00+00:00
    (3 rows)
    ```

- 设置序列的下一个值。

    以下示例将 `orders_seq` 序列的下一个值设置为 `7`。

    ::: warning 说明
    序列的下一个值不能大于序列的 `MAXVALUE` 或者小于序列的 `MINVALUE`。
    :::

    ```sql
    -- 1. 将 orders_seq 序列的下一个值更改为 7。

    SELECT SETval('orders_seq', 7, false);
      setval
    ----------
          7
    (1 row)

    -- 2. 向表 order_list 中写入数据，并检查新记录是否符合新序列设置。

    insert into order_list (customer, date) values ('Wang Ming', '2024-01-02');
    INSERT 1

    -- 3. 查看表数据。

    SELECT * FROM order_list;
      id | customer  |           date
    -----+-----------+----------------------------
      1 | Li Ming   | 2024-01-02 00:00:00+00:00
      2 | Li Hua    | 2024-01-02 00:00:00+00:00
      4 | Zhou Mi   | 2024-01-02 00:00:00+00:00
      7 | Wang Ming | 2024-01-02 00:00:00+00:00
    (4 rows)
    ```

- 设置序列所属关系。

    以下示例创建、解除 `orders_seq` 序列和 `order_list` 表 `id` 列的关联关系。

    ```sql
    -- 创建序列的关联列
    ALTER SEQUENCE orders_seq OWNED BY order_list.id;
    ALTER SEQUENCE

    -- 解除关联
    ALTER SEQUENCE orders_seq OWNED BY NONE;
    ALTER SEQUENCE
    ```

## 重命名序列

`ALTER SEQUENCE` 语句用于修改序列的名称。

### 前提条件

用户拥有序列所属数据库的 CREATE 权限。

### 语法格式

```sql
ALTER SEQUENCE [IF EXISTS] <current_name> RENAME TO <new_name>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF EXISTS` | 可选关键字。当使用 `IF EXISTS` 关键字时，如果目标序列存在，系统重命名目标序列。如果目标序列不存在，系统重命名目标序列失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果目标序列存在，系统重命名目标序列。如果目标序列不存在，系统报错，提示目标序列不存在。 |
| `current_name` | 待修改的序列的当前名称。 |
| `new_name` | 序列的新名称，该名称在数据库中必须唯一，并且遵循[数据库标识符规则](../../../sql-reference/sql-identifiers.md)。如需将该序列移动到其他数据库，名称格式为 `<database_name>.<current_name>`。 |

### 语法示例

- 重命名序列。

    以下示例将 `desc_orders_list` 序列重命名为 `orders_list_seq`。

    ```sql
    -- 1. 将 desc_orders_list 序列重命名为 orders_list_seq。

    ALTER SEQUENCE desc_orders_list RENAME TO orders_list_seq;
    RENAME SEQUENCE

    -- 2. 查看所有的序列。

    SELECT * FROM information_schema.sequences;
      sequence_catalog | sequence_schema |  sequence_name  | data_type | numeric_precision | numeric_precision_radix | numeric_scale | start_value |    minimum_value     |    maximum_value    | increment | cycle_option
    -------------------+-----------------+-----------------+-----------+-------------------+-------------------------+---------------+-------------+----------------------+---------------------+-----------+---------------
      db3              | public          | orders_seq      | bigint    |                64 |                       2 |             0 | 1           | 1                    | 9223372036854775807 | 2         | NO
      db3              | public          | orders_list_seq | bigint    |                64 |                       2 |             0 | -1          | -9223372036854775808 | -1                  | -2        | NO
    (2 rows)
    ```

- 移动序列。

    以下示例将 `orders_list_seq` 从当前数据库移动到 `db1` 数据库。

    ```sql
    -- 1. 将 orders_list_seq 从当前数据库移动到 db1 数据库。

    ALTER SEQUENCE orders_list_seq RENAME TO db1.orders_list_seq;
    RENAME SEQUENCE

    -- 2. 查看 db1 数据库的序列。

    SELECT * FROM db1.information_schema.sequences;
      sequence_catalog | sequence_schema |  sequence_name  | data_type | numeric_precision | numeric_precision_radix | numeric_scale | start_value |    minimum_value     | maximum_value | increment | cycle_option
    -------------------+-----------------+-----------------+-----------+-------------------+-------------------------+---------------+-------------+----------------------+---------------+-----------+---------------
      db1              | public          | orders_list_seq | bigint    |                64 |                       2 |             0 | -1          | -9223372036854775808 | -1            | -2        | NO
    (1 row)
    ```

## 删除序列

`DROP SEQUENCE` 用于从数据库中删除序列。KWDB 支持一次删除多条序列。

### 前提条件

用户拥有目标序列的 DROP 权限。

### 语法格式

```sql
DROP SEQUENCE [IF EXISTS] <sequence_name_list> [RESTRICT];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF EXISTS` | 可选关键字。当使用 `IF EXISTS` 关键字时，如果目标序列存在，系统删除目标序列。如果目标序列不存在，系统删除目标序列失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果目标序列存在，系统删除目标序列。如果目标序列不存在，系统报错，提示目标序列不存在。 |
| `seq_name_list` | 待删除的序列名称列表。支持指定一个或多个无依赖关系的序列，序列名称之间使用逗号（`,`）隔开。支持使用 `SHOW CREATE TABLE <table_name>` 语句查看指定表的序列名称。 |
| `RESTRICT` | 默认设置，可选关键字。如果约束、表等对象依赖目标序列，则无法删除该序列。 |

### 语法示例

以下示例删除 `db1` 数据库中 `information_ schema` 模式下 `sequences` 表的 `orders_list_seq` 序列。

```sql
-- 1. 查看 db1 数据库的序列。

SELECT * FROM db1.information_schema.sequences;
  sequence_catalog | sequence_schema |  sequence_name  | data_type | numeric_precision | numeric_precision_radix | numeric_scale | start_value |    minimum_value     | maximum_value | increment | cycle_option
-------------------+-----------------+-----------------+-----------+-------------------+-------------------------+---------------+-------------+----------------------+---------------+-----------+---------------
  db1              | public          | orders_list_seq | bigint    |                64 |                       2 |             0 | -1          | -9223372036854775808 | -1            | -2        | NO
(1 row)

-- 2. 删除 orders_list_seq 序列。

DROP SEQUENCE orders_list_seq;
DROP SEQUENCE

-- 3. 查看 db1 数据库的序列。

SELECT * FROM information_schema.sequences;
  sequence_catalog | sequence_schema | sequence_name | data_type | numeric_precision | numeric_precision_radix | numeric_scale | start_value | minimum_value | maximum_value | increment | cycle_option
-------------------+-----------------+---------------+-----------+-------------------+-------------------------+---------------+-------------+---------------+---------------+-----------+---------------
(0 rows)
```
