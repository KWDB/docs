---
title: 使用 kwbase CLI 工具管理 KWDB
id: use-kaiwudb-cli
---

# 使用 kwbase CLI 工具管理 KWDB

## 时序数据

本节介绍如何使用 kwbase CLI 工具管理 KWDB 数据库，并通过实际示例展示如何处理时序数据和关系数据。

## 时序数据

1. 创建时序数据库。

    以下示例创建 `sensor_data` 数据库。

   ```sql
   CREATE TS DATABASE sensor_data;
   ```

2. 创建时序表。

    以下示例在 `sensor_data` 数据库中创建名为 `readings` 的时序表，存储温度和湿度数据，并使用传感器 ID 和位置作为标签。

    ```sql
    CREATE TABLE sensor_data.readings (
        ts timestamp NOT NULL,         -- 数据读取时间戳
        temperature FLOAT,             -- 温度（摄氏度）
        humidity FLOAT                 -- 湿度（百分比）
    ) TAGS (
        sensor_id INT NOT NULL,        -- 传感器 ID
        location CHAR(256) NOT NULL    -- 传感器位置（如 "Room 101"）
    ) PRIMARY TAGS(sensor_id);
    ```

3. 向 `readings` 时序表中写入数据。

    ```sql
    INSERT INTO sensor_data.readings 
    VALUES 
    (NOW(), 23.0, 59.5, 101, 'Room 101'),
    (NOW(), 23.5, 58.9, 102, 'Room 102'),
    (NOW(), 19.8, 65.5, 103, 'Room 103');
    ```

4. 查询 `readings` 时序表中的数据。

    ```sql
    SELECT * FROM sensor_data.readings;
                ts               | temperature | humidity | sensor_id | location
    --------------------------------+-------------+----------+-----------+-----------
    2024-12-16 07:37:30.584+00:00 |          23 |     59.5 |       101 | Room 101
    2024-12-16 07:37:30.584+00:00 |        23.5 |     58.9 |       102 | Room 102
    2024-12-16 07:37:30.584+00:00 |        19.8 |     65.5 |       103 | Room 103
    (3 rows)
    ```

## 关系数据

1. 创建关系数据库。

    以下示例创建 `rdb` 关系数据库。

    ```sql
    CREATE DATABASE rdb;
    ```

2. 创建关系表。

    以下示例在 `rdb` 数据库中创建名为 `accounts` 的关系表，存储客户账户信息。

    ```sql
    CREATE TABLE rdb.accounts (
        id INT8 DEFAULT unique_rowid() PRIMARY KEY,  -- 自动生成唯一 ID
        name STRING,                                 -- 客户姓名
        balance DECIMAL,                             -- 账户余额
        enabled BOOL                                 -- 账户状态（启用/禁用）
    );
    ```

3. 向 `accounts` 关系表中写入数据。

    ```sql
    INSERT INTO rdb.accounts 
    VALUES 
    (1, 'Lily', 10000.5, true), 
    (2, 'Ruarc', 20000.75, true), 
    (3, 'Tullia', 30000.0, false), 
    (4, 'Arturo', 45000.0, false);
    ```

4. 查询 `accounts` 关系表中的数据。

    ```sql
    SELECT * FROM rdb.accounts;
    id | name  | balance | enabled
    ---+-------+---------+--------
    1  | Lily  | 10000.5 | true
    2  | Ruarc | 20000.75| true
    3  | Tullia| 30000   | false
    4  | Arturo| 45000   | false
    (4 rows)
    ```