---
title: 立即重组
id: vacuum-sql
---

# 立即重组

用户需要立即释放时序数据存储空间或优化时序数据查询性能时，可以通过立即重组命令手动触发重组操作。

立即重组命令特别适用于以下场景：

- 删除数据或删除库表后释放空间：执行 DELETE 或 DROP 操作后，立即清理已删除数据，快速释放存储空间
- 批量写入后数据整理：大批量数据写入后，对数据文件进行整理排序，加速后续查询性能

## 所需权限

无

## 语法格式

![](../../static/sql-reference/vacuum.png)

## 参数说明

无

## 语法示例

以下示例说明如何执行立即重组命令释放存储空间或优化查询性能。

- 释放存储空间

  ```sql
  -- 执行删除操作
  DELETE FROM sensor_data WHERE ts < '2024-01-01';

  -- 立即重组以释放存储空间
  VACUUM TS DATABASES;
  ```

- 优化查询性能

  ```sql
  -- 大批量多设备数据写入
    INSERT INTO sensor_data VALUES
        (NOW(), 25.5, 60.2, 101, 'temperature'),
        (NOW(), 26.1, 58.7, 102, 'temperature'),
        (NOW(), 24.8, 62.1, 103, 'temperature'),
        ...;

  -- 立即重组以整理数据,提升查询性能
  VACUUM TS DATABASES;
  ```
