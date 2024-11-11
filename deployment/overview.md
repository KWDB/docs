---
title: 集群部署概述
id: overview
---

# 集群部署概述

KWDB 支持使用 KWDB 容器镜像或二进制安装包部署 KWDB 集群。在同一机房内的多个节点上运行 KWDB，并将数据分散存储在这些节点上。这种方式有助于提高系统的可用性和容错性，能够实现故障转移和数据强一致性。更多详细信息，参见[集群高可用](../db-operation/cluster-ha.md)。

::: warning 说明
目前，KWDB 未提供可供下载的 KWDB 容器镜像。如需使用容器镜像部署 KWDB，[联系](https://www.kaiwudb.com/support/) KWDB 技术支持人员获取 KWDB 容器镜像。
:::

本节包含以下文档：

- [部署流程](./deploy-workflow.md)
- 裸机部署
  - [部署准备](./bare-metal/before-deploy-bare-metal.md)
  - [裸机部署](./bare-metal/bare-metal-deployment.md)
  - [启动与停止 KWDB 服务](./bare-metal/local-start-stop-bare-metal.md)
  - [配置集群](./bare-metal/cluster-config-bare-metal.md)
  - [创建用户](./bare-metal/user-config-bare-metal.md)
  - [卸载集群](./bare-metal/uninstall-cluster-bare-metal.md)
- 容器部署
  - [部署准备](./docker/before-deploy-docker.md)
  - [容器部署](./docker/docker-deployment.md)
  - [启动与停止 KWDB 服务](./docker/local-start-stop-docker.md)
  - [配置集群](./docker/cluster-config-docker.md)
  - [创建用户](./docker/user-config-docker.md)
  - [卸载集群](./docker/uninstall-cluster-docker.md)
