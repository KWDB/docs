---
title: 使用 kwbase CLI 工具管理 KWDB
id: use-kaiwudb-cli
---

# 使用 kwbase CLI 工具管理 KWDB

## 时序数据

以下示例说明如何使用 SQL 语句创建时序数据库、时序表、向时序表中读写数据。

1. 创建时序数据库。

    以下示例创建 `ts_db` 数据库。

    ```sql
    CREATE TS DATABASE ts_db;
    ```

2. 创建时序表。

    以下示例创建 `t1` 时序表。

    ```sql
    CREATE TABLE ts_db.t1(ts timestamp not null,a int, b int) tags(tag1 int not null, tag2 int) primary tags(tag1);
    ```

3. 向 `t1` 时序表中写入数据。

    ```sql
    INSERT INTO ts_db.t1 VALUES(now(),11,11,33,44);
    INSERT INTO ts_db.t1 VALUES(now(),22,22,33,44);
    INSERT INTO ts_db.t1 VALUES(now(),11,33,33,44);
    INSERT INTO ts_db.t1 VALUES(now(),22,44,33,44);
    INSERT INTO ts_db.t1 VALUES(now(),33,55,44,44);
    INSERT INTO ts_db.t1 VALUES(now(),22,44,44,44);
    INSERT INTO ts_db.t1 VALUES(now(),33,44,55,44);
    INSERT INTO ts_db.t1 VALUES(now(),null,null,66,66);
    INSERT INTO ts_db.t1 VALUES(now(),null,null,66,77);
    ```

4. 查询 `t1` 时序表中的数据。

    ```sql
    SELECT * FROM t1;
    ts               |  a   |  b   | tag1 | tag2
    --------------------------------+------+------+------+-------
    2024-09-30 09:47:33.63+00:00  |   11 |   11 |   33 |   44
    2024-09-30 09:47:33.656+00:00 |   22 |   22 |   33 |   44
    2024-09-30 09:47:33.668+00:00 |   11 |   33 |   33 |   44
    2024-09-30 09:47:33.678+00:00 |   22 |   44 |   33 |   44
    2024-09-30 09:47:33.698+00:00 |   33 |   55 |   44 |   44
    2024-09-30 09:47:33.717+00:00 |   22 |   44 |   44 |   44
    2024-09-30 09:47:33.737+00:00 |   33 |   44 |   55 |   44
    2024-09-30 09:47:33.756+00:00 | NULL | NULL |   66 |   66
    2024-09-30 09:47:33.774+00:00 | NULL | NULL |   66 |   66
    (9 rows)
    ```

## 关系数据

以下示例说明如何使用 SQL 语句创建关系数据库、关系表、向关系表中读写数据。

1. 创建关系数据库。

    以下示例创建 `db1` 关系数据库。

    ```sql
    CREATE DATABASE db1;
    ```

2. 创建关系表。

    以下示例创建 `accounts` 关系表。

    ```sql
    CREATE TABLE db1.accounts(id INT8 DEFAULT unique_rowid() PRIMARY KEY, name STRING, balance DECIMAL, enabled BOOL);
    ```

3. 向 `accounts` 关系表中写入数据。

    ```sql
    INSERT INTO db1.accounts VALUES (1, 'lily', 10000.5, true), (2, 'ruarc', 20000.75, true), (3, 'tullia', 30000, false), (4, 'arturo', 45000, false);
    ```

4. 查询 `accounts` 关系表中的数据。

    ```sql
    SELECT * FROM accounts;
    id|name  |balance |enabled
    --+------+--------+-------
    1 |lily  |10000.5 |true      
    2 |ruarc |20000.75|true       
    3 |tullia|30000   |false      
    4 |arturo|45000   |false      
    (4 rows)
    ```
