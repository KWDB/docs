---
title: 2.0.4.1 发版说明
id: 2.0.4.1-release-notes
---

# KWDB 2.0.4.1 发版说明

KWDB 是一款面向 AIoT 场景的分布式多模数据库产品，支持在同一实例同时建立时序库和关系库并融合处理多模数据，具备千万级设备接入、百万级数据秒级写入、亿级数据秒级读取等时序数据高效处理能力，具有稳定安全、高可用、易运维等特点，一站式满足 AIoT 等场景下数据管理需求及关键行业核心系统的自主可控需求。

KWDB 2.0.4.1 版本在保持原有特性的基础上，新增了对无模式写入的支持，用户可以通过 RESTful API 以无模式方式将数据写入 KWDB。。

## 版本信息

| 版本号   | 日期   |
| :------- | :--------- |
| 2.0.4.1    | 2024.10.25 |

## 新增特性

支持通过 RESTful API 以无模式方式向 KWDB 写入数据。

## 升级说明

支持 KWDB 2.0.3.2 集群通过导入导出方式升级到 KWDB 2.0.4.1 版本，支持 KWDB 2.0.4 集群在线升级到 KWDB 2.0.4.1 版本。支持 KWDB 2.0.3.2 及以上单机版本离线升级到 KWDB 2.0.4.1 单机版本。相关信息见[数据库升级](../db-operation/db-upgrade.md)、[数据导出](../db-administration/import-export-data/export-data.md)和[数据导入](../db-administration/import-export-data/import-data.md)。