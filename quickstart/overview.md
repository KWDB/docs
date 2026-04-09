---
title: 概述
id: overview
---

# 概述

本节介绍如何通过单节点部署方式快速上手体验 KWDB 数据库。集群部署相关信息，参见[集群部署](../deployment/overview.md)。

## 部署准备

部署 KWDB 前，请根据[部署准备](./prepare.md)检查待部署节点的硬件、操作系统、软件依赖和端口是否满足要求。

## 部署 KWDB

KWDB 提供多种部署方式，满足不同用户和场景的需求：

| 部署方式 | 特点 | 适用用户/场景 | 技术要求 | 支持环境 |
|---------|------|---------|------|---------|
| **[快速部署](./deploy/quick-deploy.md)** | 自动化脚本一键部署 | 首次体验 KWDB 的用户 | 基本 Linux 操作经验 | 裸机、容器化 |
| **[脚本（推荐）](./deploy/deploy-script.md)** | 使用安装包内置脚本，一键完成部署 | 需要稳定、快捷上线的生产用户 | 基本 Linux 操作经验 | 裸机、容器化 |
| **[容器镜像 - Docker Run](./deploy/deploy-docker-run.md)** | 使用 `docker run` 命令直接运行容器 | 需要快速搭建测试或验证环境的用户 | 熟悉 Docker 命令行操作 | 容器化 |
| **[容器镜像 - Docker Compose](./deploy/deploy-yaml.md)** | 基于 YAML 文件进行编排部署，目前仅支持非安全模式 | 熟悉容器编排的用户，适合测试或快速验证 | 具备 Docker & Compose 基础 | 容器化 |
| **[CLI 命令行](./deploy/deploy-cli.md)** | 支持精细化控制和深度定制 | 有经验的资深用户，定制化需求场景 | 熟悉数据库部署流程和命令行操作 | 裸机 |


::: warning 提示
KWDB 单节点部署支持[基于 DRBD 的主备复制](../best-practices/single-ha.md)高可用方案。如果您计划实施高可用方案，请先参阅相关文档。
:::

## 使用 KWDB

部署完成后，您可以通过以下任一方式连接和管理 KWDB：

| 连接方式 | 特点 | 适用场景 |
|---------|------|---------|
| **[kwbase CLI 工具](./access/access-cli.md)** | 内置命令行工具，支持安全和非安全模式，适合自动化脚本 | 命令行操作、自动化脚本、运维管理 |
| **[KaiwuDB JDBC](./access/access-jdbc.md)** | 标准 JDBC 接口，支持连接池，适合 Java 应用集成 | Java 应用程序开发、生产环境集成 |
| **[KaiwuDB 开发者中心](./access/access-kdc.md)** | 图形化管理界面，直观易用，支持可视化操作 | 可视化管理、数据浏览、查询调试 |

## 卸载 KWDB

如需了解如何卸载 KWDB，请参见[卸载 KWDB](../deployment/uninstall-cluster.md)。
