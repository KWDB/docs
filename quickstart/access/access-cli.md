---
title: kwbase CLI
id: access-cli
---

# kwbase CLI

kwbase 是 KaiwuDB 提供的内置命令行工具。用户可以通过 kwbase 连接 KWDB，进行数据库操作和管理，支持安全模式（适用于生产环境）和非安全模式（适用于测试）。

如果使用脚本部署 KWDB，系统还会自动生成 `kw-sql` 便捷脚本，并在 `/usr/bin` 目录下创建软链接 `kw-sql`。该脚本封装了 kwbase 连接命令，方便 root 用户快速登录数据库。

## 连接 KWDB

### 使用便捷脚本快速登录

::: warning 说明
`kw-sql` 不支持指定其他用户，如需使用其他用户或三权分立模式，请使用 kwbase 命令登录。
:::

**前提条件**：

已使用 `deploy.sh` 脚本部署并启动 KWDB。

**步骤**：

1. 在节点任一位置执行以下命令，使用 root 用户连接数据库：

    ```shell
    kw-sql
    ```

### 使用 kwbase 命令连接

::: warning 提示
如采用容器部署方式，需使用以下命令格式连接数据库：
```bash
docker exec -it <container-name> ./kwbase sql [security-options] --host=<your-host-ip> [-u <user-name>]
```
:::

#### 非安全模式

::: warning 提示
非安全模式应仅在测试环境中使用。
:::

**前提条件**
- 以非安全模式部署并启动 KWDB

**步骤**

- 使用部署数据库时所用的用户连接 KWDB。

    ```shell
    ./kwbase sql --insecure --host=<your-host-ip>
    ```

- 普通用户连接 KWDB。

    1. 使用部署数据库时所用的用户连接 KWDB。

        ```shell
        ./kwbase sql --insecure --host=<your-host-ip>
        ```

    2. 创建普通用户。

        ```sql
        CREATE USER user1;
        ```

    3. 退出登录。
    4. 新用户连接 KWDB。

        ```shell
        ./kwbase sql --insecure --host=<your-host-ip> -u user1
        ```

#### 安全模式连接

KWDB 默认支持用户使用证书或密码登录数据库。以下示例说明管理员用户和普通用户如何在标准安全模式下使用证书安全登录数据库。有关其他认证方式的详细信息，参见[身份鉴别与认证](../../db-security/identity-authn.md)。

**前提条件**

- 安全模式部署并启动 KWDB。

**步骤**

- 使用部署数据库时所用的用户连接 KWDB。

    ```shell
    ./kwbase sql --certs-dir=<certs-dir> --host=<your-host-ip> 
    ```

- 普通用户连接 KWDB。

    1. 使用部署数据库时所用的用户连接 KWDB。

        ```shell
        ./kwbase sql --certs-dir=<certs-dir> --host=<your-host-ip> 
        ```

    2. 创建普通用户。

        ```sql
        CREATE USER user1;
        ```

    3. 为新用户生成证书。

        ```shell
        ./kwbase cert create-client user1 --certs-dir=<certs-dir> --ca-key=<certs-dir>/ca.key
        ```

    4. 退出登录。
    5. 新用户连接 KWDB。

        ```shell
        ./kwbase sql --certs-dir=<certs-dir> --host=<your-host-ip> -u user1
        ```

## 管理 KWDB

本节通过监控场景，演示如何使用 kwbase CLI 工具管理 KWDB 多模数据库，具体包括：

- **关系数据操作**：管理相对静态的基础数据，如设备信息、用户档案等
- **时序数据操作**：处理按时间序列变化的动态数据，如传感器读数、监控指标等
- **跨模查询**：通过联合查询关系库和时序库数据，实现多模数据融合分析

### 关系数据操作

#### 创建数据库和数据表

1. 创建和使用关系数据库：
    ```sql
    -- 创建关系数据库
    CREATE DATABASE device_info;
    -- 切换到指定数据库
    USE device_info;
    ```

2. 创建设备表：
    ```sql
    CREATE TABLE devices (
        device_id INT PRIMARY KEY,        -- 设备ID
        device_name VARCHAR NOT NULL,     -- 设备名称
        location VARCHAR,                 -- 位置
        status VARCHAR DEFAULT 'active'   -- 状态
    );
    ```

#### 写入数据

```sql
-- 批量插入设备基础信息
INSERT INTO devices VALUES
    (101, '传感器A', '机房1', 'active'),
    (102, '传感器B', '机房2', 'active'),
    (103, '传感器C', '机房1', 'active');
```

#### 查询数据

```sql
-- 查询所有设备信息
SELECT * FROM devices;
```

查询结果示例：
```plain
device_id | device_name | location | status
----------+-------------+----------+--------
      101 | 传感器A     | 机房1    | active
      102 | 传感器B     | 机房2    | active
      103 | 传感器C     | 机房1    | active
```

### 时序数据操作

时序表具有特殊的结构要求：
- **时间戳列**：必须作为表的第一列
- **标签列（TAGS）**：用于标识设备静态属性
- **主标签（PRIMARY TAGS）**：用于区分不同的实体对象

#### 创建时序库和时序表

1. 创建时序数据库：
    ```sql
    -- 创建时序数据库
    CREATE TS DATABASE monitoring;
    -- 切换到时序数据库
    USE monitoring;
    ```

2. 创建监控数据表：
    ```sql
    CREATE TABLE sensor_data (
        ts TIMESTAMP NOT NULL,            -- 时间戳（必须为第一列）
        temperature FLOAT,                -- 温度
        humidity FLOAT                    -- 湿度
    ) TAGS (
        device_id INT NOT NULL,           -- 设备ID（标签）
        sensor_type VARCHAR NOT NULL      -- 传感器类型（标签）
    ) PRIMARY TAGS(device_id);            -- 主标签
    ```

#### 写入数据

```sql
-- 插入当前时间的传感器监控数据
INSERT INTO sensor_data VALUES
    (NOW(), 25.5, 60.2, 101, 'temperature'),
    (NOW(), 26.1, 58.7, 102, 'temperature'),
    (NOW(), 24.8, 62.1, 103, 'temperature');
```

#### 查询数据

```sql
-- 查询最新的5条传感器数据，按时间倒序排列
SELECT * FROM sensor_data 
ORDER BY ts DESC 
LIMIT 5;
```

查询结果示例：
```plain
        ts                    | temperature | humidity | device_id | sensor_type
---------------------------+-------------+----------+-----------+-------------
2025-08-01 10:30:15.123+00:00 |        24.8 |     62.1 |       103 | temperature
2025-08-01 10:30:15.123+00:00 |        26.1 |     58.7 |       102 | temperature
2025-08-01 10:30:15.123+00:00 |        25.5 |     60.2 |       101 | temperature
```

### 跨模查询

KWDB 的核心优势在于支持跨时序库和关系库的联合查询，实现多模数据的深度融合分析。

#### 查询设备基础信息及其最新监控数据

```sql
-- 联合查询设备基础信息和最新监控数据
-- 使用 DISTINCT ON 获取每个设备的最新数据记录
SELECT 
    d.device_name,           -- 设备名称
    d.location,              -- 设备位置
    s.temperature,           -- 最新温度
    s.humidity,              -- 最新湿度
    s.ts as last_update      -- 最后更新时间
FROM device_info.devices d
JOIN (
    -- 子查询：获取每个设备的最新监控数据
    SELECT DISTINCT ON (device_id) 
        device_id, temperature, humidity, ts
    FROM monitoring.sensor_data 
    ORDER BY device_id, ts DESC
) s ON d.device_id = s.device_id
WHERE d.status = 'active'    -- 只查询激活状态的设备
ORDER BY d.device_id;
```

查询结果示例：
```plain
device_name | location | temperature | humidity |        last_update
------------+----------+-------------+----------+---------------------------
传感器A     | 机房1    |        25.5 |     60.2 | 2025-08-01 10:30:15.123+00:00
传感器B     | 机房2    |        26.1 |     58.7 | 2025-08-01 10:30:15.123+00:00
传感器C     | 机房1    |        24.8 |     62.1 | 2025-08-01 10:30:15.123+00:00
```

#### 按位置统计平均温湿度

```sql
-- 按设备位置统计最近1小时内的平均温湿度
SELECT 
    d.location,                      -- 设备位置
    COUNT(*) as device_count,        -- 该位置的设备数量
    AVG(s.temperature) as avg_temp,  -- 平均温度
    AVG(s.humidity) as avg_humidity  -- 平均湿度
FROM device_info.devices d
JOIN monitoring.sensor_data s ON d.device_id = s.device_id
WHERE s.ts > NOW() - INTERVAL '1 hour'  -- 筛选最近1小时的数据
GROUP BY d.location                     -- 按位置分组
ORDER BY d.location;
```

查询结果示例：
```plain
location | device_count | avg_temp | avg_humidity
---------+--------------+----------+--------------
机房1    |            2 |     25.2 |         61.2
机房2    |            1 |     26.1 |         58.7
```
