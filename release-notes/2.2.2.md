---
title: 2.2.2 发版说明
id: 2.2.2-release-notes
---

# KWDB 2.2.2 发版说明

KWDB 是一款面向 AIoT 物联网场景的分布式、多模融合的数据库产品，支持在同一实例同时创建时序库和关系库并融合处理多模数据，具备千万级设备接入、百万级数据秒级写入、亿级数据秒级读取等时序数据高效处理能力，具有稳定、安全、高可用、易运维等特点。面向工业物联网、数字能源、车联网、智慧产业等领域，提供一站式数据存储、管理与分析的基座。

KWDB 2.2.2 版本在保持原有特性的基础上，修复了产品典型问题，优化了系统性能和稳定性。

## 版本信息

| 版本号 | 日期       |
| :----- | :--------- |
| 2.2.2  | 2025.07.21 |

## 缺陷修复

- 修复单副本集群升级失败问题
- 修复子查询中 `time_bucket_gapfill()` 统计 count 与直接写入表后统计 count 值不一致问题
- 修复 `count_window()` 函数查询结果错误问题
- 修复 where 条件中公元前时间在不同条件下处理逻辑不一致问题
- 修复 `count()` 函数结合 `coalesce()` 函数查询错误问题
- 修复时序和关系引擎下 `current_time()` 函数结果不一致问题
- 修复 `twa()` 函数结合子查询结果错误问题
- 修复 PREPARE 模式下时序数据无法删除问题
- 优化流水线测试数据写入后 count 性能
- 优化单机 TSBS 查询场景 high-cpu-1 性能
- 优化单机 TSBS 查询场景 double group by 性能

## 升级说明

- 多副本集群：支持 KWDB 2.2.x 在线升级至 KWDB 2.2.2
- 单副本集群：支持 KWDB 2.2.x 离线升级至 KWDB 2.2.2
- 单机版本：支持 KWDB 2.2.x 离线升级至 KWDB 2.2.2
- KWDB 2.0.x 和 2.1.0 版本：支持通过导入导出方式升级至 KWDB 2.2.2

相关信息见[数据库升级](../db-operation/db-upgrade.md)、[数据导出](../db-administration/import-export-data/export-data.md)和[数据导入](../db-administration/import-export-data/import-data.md)。