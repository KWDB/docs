---
title: TRUNCATE
id: relational-truncate
---

# TRUNCATE

`TRUNCATE` 语句用于从表中删除所有行。

## 所需权限

用户拥有目标表的 DROP 权限。

## 语法格式

![](../../../static/sql-reference/ZxUobElItoWiPgxsjASc3yoan8c.png)

## 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 待删除的表的名称。|
| `CASCADE` | 可选关键字，表示级联删除，即使其他表包含对目标表的外键依赖，也会一并截断。`CASCADE` 不会列出被截断的依赖表，应谨慎使用。|
| `RESTRICT` | 可选关键字，如果其他表包含对目标表的外键依赖，则无法删除目标表。如未在语句中指定字段，默认为 `RESTRICT`。|

## 语法示例

以下示例假设用户已经创建 `t1`、`customer`、`orders` 表并写入数据。

```sql
-- 1. 创建 t1 表。

CREATE TABLE t1(id INT8 DEFAULT unique_rowid() PRIMARY KEY, name STRING);
CREATE TABLE 

-- 2. 向表中写入数据。

INSERT INTO t1 VALUES(1, 'foo'), (2, 'bar');
INSERT 2

-- 3. 查看表数据。

SELECT * FROM t1;
  id | name
-----+-------
   1 | foo
   2 | bar
(2 rows)

-- 4. 创建 customer 表，并写入数据

CREATE TABLE customer(id INT8 DEFAULT unique_rowid() PRIMARY KEY, email STRING);
CREATE TABLE

-- 5. 向表中写入数据。

INSERT INTO customer VALUES (1, 'zhangsan@163.com'), (2, 'lisi@163.com');
INSERT 2

-- 6. 查看表数据。

SELECT * FROM customer;
  id |      email
-----+-------------------
   1 | zhangsan@163.com
   2 | lisi@163.com
(2 rows)

-- 7. 创建 orders 表，设置外键依赖。

CREATE TABLE orders(id INT8 DEFAULT unique_rowid() PRIMARY KEY, customer_id INT REFERENCES customer(id) ON DELETE CASCADE);
CREATE TABLE 

-- 8. 向表中写入数据。

INSERT INTO orders VALUES (1,1),(2,1),(3,2),(4,2);
INSERT 4

-- 9. 查看表数据。

SELECT * FROM orders;
  id | customer_id
-----+--------------
   1 |           1
   2 |           1
   3 |           2
   4 |           2
(4 rows)
```

- 截断没有外键依赖的表。

    ```sql
    -- 1. 截断 t1 表。

    TRUNCATE t1;
    TRUNCATE

    -- 2. 查看表数据。
    SELECT * FROM t1;
    id|name
    --+----
    (0 rows)
    ```

- 截断有外键依赖的表。

    ```sql
    -- 1. 不指定关键字截断有外键依赖的 customer 表。
    TRUNCATE customer;
    ERROR:  "customer" is referenced by foreign key from table "orders"

    -- 2. 使用 CASCADE 关键字截断有外键依赖的 customer 表，关联的表数据也被删除。

    TRUNCATE customer CASCADE;
    TRUNCATE 

    -- 3. 查看 customer 表数据。
    SELECT * FROM customer;
    id|email
    --+-----
    (0 rows)

    -- 4. 查看 orders 表数据。
    SELECT * FROM orders;
    id|customer_id
    --+-----------
    (0 rows)
    ```
