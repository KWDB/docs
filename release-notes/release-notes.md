---
title: 发版说明
id: release-notes
---

# 发版说明

KWDB 是一款面向 AIoT（Artificial Intelligence of Things，智能物联网）场景的分布式、多模融合、支持原生 AI 的数据库产品。KWDB 支持在同一实例同时创建时序库和关系库并融合处理多模数据，具备时序数据高效处理能力，具有稳定安全、高可用、易运维等特点。面向工业物联网、数字能源、车联网、智慧产业等领域，KWDB 提供一站式数据存储、管理与分析的基座。

本文列出 KWDB 2.0 版本的主要功能。有关 KWDB 2.0 版本支持的功能，参见[功能概览](../about-kaiwudb/supported-features.md)。

## 版本信息

| 版本号 | 发版日期   |
| -------- | ---------- |
| 2.0  | 2024.07.31 |

## 功能特性

### 数据写入

- 支持标准 SQL 写入及导入。
- 支持毫秒精度数据写入。
- 支持百万行数据秒级写入。

### 数据查询

- 支持标签条件查询、插值查询、最新值查询、标签分组聚合查询、时间窗口聚合查询等多种查询方式。
- 支持进行关系与时序表的跨模查询。
- 支持亿级数据简单聚合查询秒级响应。

### 分布式架构

- 支持部署三副本分布式数据库集群，单点故障不影响数据库集群的正常使用。
- 支持根据标签值和时间对时序数据自动进行分区，并根据标签创建索引，快速定位指定设备数据，加速查询性能。

### 数据库存储

- 支持在线数据压缩，数据压缩不影响业务使用。
- 支持自定义库、表级数据保存的生命周期。
- 具备提供 3-30 倍以上的数据压缩的能力。

### 数据库运维管理

- 支持容器化安装部署。支持在 Ubuntu、CentOS 等多种主流操作系统下稳定运行。支持在海光、飞腾、统信、麒麟等主流国产 CPU 和操作系统下稳定运行。
- 具备数据操作管理的可视化客户端工具。

有关数据库运维的更多详细信息，参见[数据库运维概述](../db-operation/db-operation-overview.md)。

### 数据库连接

- 支持通过 JDBC、RESTful API 等方式连接数据库。

有关数据库连接的更多详细信息，参见[应用开发概述](../development/overview.md)。

### 数据库安全

- 支持对接入数据库用户进行身份认证工作，允许设置、修改用户名密码。
- 支持为所有或指定用户授予或撤销不同的权限，包括创建、删除、查询、写入、更新等权限。
- 支持开启、关闭数据库审计操作，支持审计 DDL 操作、DML 操作、DCL 操作、DQL 操作。
- 支持客户端与服务器端通过 HTTPS 等方式进行加密通信。

有关数据库安全的更多详细信息，参见[集群安全概述](../db-operation/security/security-overview.md)。

### 数据库兼容

- 兼容 [Prometheus](https://prometheus.io/)、[Grafana](https://grafana.com/grafana)、[OpenTelemetry](https://opentelemetry.io/)、[Kafka](https://kafka.apache.org/)、[EMQX](https://www.emqx.io/)、[DataX](https://github.com/alibaba/DataX) 等生态工具。
- 支持通过 [MyBatis](../development/connect-kaiwudb/connect-mybatis.md)、[MyBatis-Plus](../development/connect-kaiwudb/connect-mybatis-plus.md) 等主流框架协议连接数据库并读写数据。

### 预测分析引擎（企业版特性）

- 提供可插拔的 AI 预测分析引擎，提供自动化安装配置能力。
- 支持 Python 语言以及 [TensorFlow](https://tensorflow.google.cn/?hl=zh-cn)、[XGBoost](https://xgboost.readthedocs.io/en/stable/#)、[scikit-learn](https://scikit-learn.org/stable/index.html)、[LightGBM](https://lightgbm.readthedocs.io/en/latest/index.html#) 等主流机器学习框架。
- 支持通过 SQL 语句管理模型和训练流水线，包括导入模型和训练流水线、训练模型、评估模型、在线预测、批量预测及模型和作业流水线的生命周期管理。
- 支持通过 WEB 图形化的工具管理模型和训练流水线，包括导入模型和训练流水线、训练模型、评估模型、在线预测、批量预测及模型和作业流水线的生命周期管理。
- 支持模型训练作业、模型评估作业和批量预测作业的生命周期管理，支持多个作业的并行运行。

有关预测分析引擎的更多详细信息，参见[预测分析引擎概述](../ml-services/ml-service-overview.md)。
