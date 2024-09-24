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

- 时序数据不支持事务。因此，跨模查询也不支持语句的事务完整性。
- 使用 `FULL JOIN` 时，避免在连接条件中使用子查询。
:::

## 所需权限

用户拥有目标表的 SELECT 权限。

## 语法示例

以下示例假设已创建 `tsdb` 时序数据库、`rdb`关系数据库、关系表 `DeviceModel` 和 `Device`、时序表 `MonitoringCenter` 并写入相关数据。

- 关联查询

    以下示例通过内连接将 `Device`、`DeviceModel`、`MonitoringCenter` 表关联在一起，获取特定条件下的设备信息和相关型号与监控中心信息。

    ```sql
    SELECT d.deviceID, dm.TypeName, dm.ModelName
    FROM rdb.Device AS d
    INNER JOIN rdb.DeviceModel AS dm ON d.modelID = dm.modelID
    INNER JOIN tsdb.MonitoringCenter AS mc ON d.deviceID = mc.deviceID
    WHERE mc.status = -1
    ORDER BY d.deviceID;
      deviceid | typename |  modelname
    -----------+----------+--------------
            7 | 电表     | 电表模型2
            16 | 变压器   | 变压器模型6
    (2 rows)
    ```

- 嵌套查询

    以下示例使用相关投影子查询，对设备 ID 与 `tsdb.MonitoringCenter` 的表进行关联，返回相应设备 ID 下的最新状态。

    ```sql
    SELECT d.deviceID,
          (SELECT MAX(status) FROM tsdb.MonitoringCenter WHERE deviceID = d.deviceID) AS LatestStatus
    FROM rdb.Device AS d ORDER by d.deviceID;
      deviceid | lateststatus
    -----------+---------------
            1 | NULL
            2 |            0
            3 | NULL
            4 | NULL
            5 | NULL
            6 | NULL
            7 |           -1
            8 | NULL
            9 | NULL
            10 | NULL
            11 | NULL
            12 | NULL
            13 | NULL
            14 |            0
            15 | NULL
            16 |           -1
            17 | NULL
            18 |            0
            19 | NULL
            20 | NULL
            21 | NULL
    (21 rows)
    ```

- 联合查询

    以下示例使用 `UNION` 操作符合并 `rdb.Device` 和 `tsdb.MonitoringCenter` 表的查询结果，并将最终结果以 `deviceID` 和 `status` 进行升序排序。

    ```sql
    SELECT deviceID, NULL AS status
    FROM rdb.Device
    UNION
    SELECT NULL AS deviceID, status
    FROM tsdb.MonitoringCenter order by deviceID,status;
      deviceid | status
    -----------+---------
      NULL     |     -1
      NULL     |      0
            1 | NULL
            2 | NULL
            3 | NULL
            4 | NULL
            5 | NULL
            6 | NULL
            7 | NULL
            8 | NULL
            9 | NULL
            10 | NULL
            11 | NULL
            12 | NULL
            13 | NULL
            14 | NULL
            15 | NULL
            16 | NULL
            17 | NULL
            18 | NULL
            19 | NULL
            20 | NULL
            21 | NULL
    (23 rows)
    ```
