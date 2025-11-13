---
title: 跨模查询
id: data-query
---

# 跨模查询

跨模查询是一种用于检索相关联数据的查询方法，通常用于在不同类型的数据库之间进行查询，例如在关系数据库和时序数据库之间检索相关的数据。

KWDB 跨模查询支持对关系表和时序表进行关联查询、嵌套查询、联合查询。

KWDB 跨模查询支持以下关联查询：

- 内连接（INNER JOIN）
- 左连接（LEFT JOIN）
- 右连接（RIGHT JOIN）
- 全连接（FULL JOIN）

KWDB 跨模查询支持以下嵌套查询：

- 相关子查询（Correlated Subquery）：内部查询依赖于外部查询的结果，每次外部查询的都触发内部查询的执行。
- 非相关子查询（Non-Correlated Subquery）：内部查询独立于外部查询，只执行一次内部查询并返回固定的结果。
- 相关投影子查询（Correlated Scalar Subquery）: 内部查询依赖于外部查询的结果，并且只返回一个单一的值作为外部查询的结果。
- 非相关投影子查询（Non-Correlated Scalar Subquery）：内部查询独立于外部查询，并且只返回一个单一的值作为外部查询的结果。
- `FROM` 子查询：将一个完整的 SQL 查询嵌套在另一个查询的 `FROM` 子句中，作为临时表格使用。

KWDB 跨模查询支持以下联合查询：

- UNION：合并多个查询结果集，并去除重复行。
- UNION ALL：合并多个查询结果集，但不去除重复行。
- INTERSECT：返回两个查询结果集中都存在的所有行，去除重复行。
- INTERSECT ALL：返回两个查询结果集中都存在的所有行，但不去除重复行。
- EXCEPT：返回第一个查询结果集中不包含在第二个结果集中的行，去除重复行。
- EXCEPT ALL：返回第一个查询结果集中不包含在第二个结果集中的行，不去除重复行。

::: warning 说明

- KWDB 支持显式事务内执行时序数据的查询以及写入，但不保证时序引擎的事务性，也不保证跨模查询结果的一致性。
- 使用 `FULL JOIN` 时，避免在连接条件中使用子查询。

:::

## 前提条件

用户是 `admin` 角色的成员或者拥有目标表的 SELECT 权限。默认情况下，`root` 用户属于 `admin` 角色。

## 语法示例

以下示例假设已创建关系数据库 `rdb`、关系表 `DeviceModel` 和 `Device`、 时序数据库 `tsdb` 、时序表 `MonitoringCenter` 并写入相关数据。

```sql
-- 创建关系数据库
CREATE DATABASE rdb;

-- 切换到关系数据库
USE rdb;

-- 创建设备型号表
CREATE TABLE DeviceModel (
    modelID INT PRIMARY KEY,
    TypeName VARCHAR(50),
    ModelName VARCHAR(50)
);

-- 创建设备表
CREATE TABLE Device (
    deviceID INT PRIMARY KEY,
    modelID INT,
    deviceName VARCHAR(100),
    FOREIGN KEY (modelID) REFERENCES DeviceModel(modelID)
);

-- 插入设备型号数据
INSERT INTO DeviceModel (modelID, TypeName, ModelName) VALUES
(101, '智能电表', 'SM-E100单相电表'),
(102, '智能电表', 'SM-E300三相电表'),
(201, '配电变压器', 'TR-D500油浸式变压器'),
(202, '配电变压器', 'TR-D800干式变压器'),
(301, '断路器', 'CB-V200真空断路器');

-- 插入设备数据
INSERT INTO Device (deviceID, modelID, deviceName) VALUES
(1001, 101, '1号楼单相电表'),
(1002, 101, '2号楼单相电表'),
(1003, 102, '3号楼三相电表'),
(2001, 201, 'A区主变压器'),
(2002, 201, 'B区主变压器'),
(2003, 202, 'C区干式变压器'),
(3001, 301, '总进线断路器'),
(3002, 301, '1号线路断路器'),
(3003, 301, '2号线路断路器'),
(3004, 301, '3号线路断路器');

-- 创建时序数据库
CREATE TS DATABASE tsdb;

-- 切换到时序数据库
USE tsdb;

-- 创建监控中心时序表
CREATE TABLE MonitoringCenter (
    ts TIMESTAMP NOT NULL,
    status INT
) TAGS (
    deviceID INT NOT NULL,
    location VARCHAR(100)
) PRIMARY TAGS (deviceID);

-- 插入监控中心数据
-- 设备状态说明: 0-正常运行, 1-轻微告警, -1-严重故障
INSERT INTO MonitoringCenter (ts, status, deviceID, location) VALUES
('2024-11-13 10:00:00', 0, 1001, '北京海淀'),
('2024-11-13 10:00:00', 0, 1002, '北京朝阳'),
('2024-11-13 10:00:00', -1, 1003, '北京丰台'),    -- 严重故障: 三相电表
('2024-11-13 10:00:00', 0, 2001, '上海浦东'),
('2024-11-13 10:00:00', 1, 2002, '上海静安'),
('2024-11-13 10:00:00', 0, 2003, '上海徐汇'),
('2024-11-13 10:00:00', 0, 3001, '广州天河'),
('2024-11-13 10:00:00', 1, 3002, '广州越秀'),
('2024-11-13 10:00:00', -1, 3003, '深圳南山'),    -- 严重故障: 2号线路断路器
('2024-11-13 10:00:00', 0, 3004, '深圳福田');
```

- 关联查询

    以下示例通过内连接将 `Device`、`DeviceModel`、`MonitoringCenter` 表关联，查询故障设备的详细信息。

    ```sql
    SELECT d.deviceID, dm.TypeName, dm.ModelName
    FROM rdb.Device AS d
    INNER JOIN rdb.DeviceModel AS dm ON d.modelID = dm.modelID
    INNER JOIN tsdb.MonitoringCenter AS mc ON d.deviceID = mc.deviceID
    WHERE mc.status = -1
    ORDER BY d.deviceID;
    ```

    查询结果：

    ```sql
      deviceid | typename |     modelname
    -----------+----------+--------------------
          1003 | 智能电表 | SM-E300三相电表
          3003 | 断路器   | CB-V200真空断路器
    (2 rows)
    ```

- 嵌套查询

    以下示例使用相关投影子查询，对设备 ID 与 `tsdb.MonitoringCenter` 的表进行关联，获取每个设备的最新状态。

    ```sql
    SELECT d.deviceID,
          (SELECT MAX(status) FROM tsdb.MonitoringCenter WHERE deviceID = d.deviceID) AS LatestStatus
    FROM rdb.Device AS d ORDER by d.deviceID;
    ```

    查询结果：

    ```sql
      deviceid | lateststatus
    -----------+---------------
          1001 |            0
          1002 |            0
          1003 |           -1
          2001 |            0
          2002 |            1
          2003 |            0
          3001 |            0
          3002 |            1
          3003 |           -1
          3004 |            0
    (10 rows)
    ```

- 联合查询

    以下示例使用 `UNION` 操作符合并 `rdb.Device` 和 `tsdb.MonitoringCenter` 表的查询结果，生成需要重点关注的设备列表（电表类设备和故障设备）。

    ```sql
    SELECT deviceID, deviceName, '电表类设备' AS category
    FROM rdb.Device
    WHERE modelID IN (101, 102)
    UNION ALL
    SELECT d.deviceID, d.deviceName, '故障设备' AS category
    FROM rdb.Device AS d
    INNER JOIN tsdb.MonitoringCenter AS mc ON d.deviceID = mc.deviceID
    WHERE mc.status = -1
    ORDER BY deviceID;
    ```

    查询结果：

    ```sql
      deviceid |  devicename   |  category
    -----------+---------------+-------------
          1001 | 1号楼单相电表 | 电表类设备
          1002 | 2号楼单相电表 | 电表类设备
          1003 | 3号楼三相电表 | 电表类设备
          1003 | 3号楼三相电表 | 故障设备
          3003 | 2号线路断路器 | 故障设备
    (5 rows)
    ```
