---
title: 集群部署概述
id: overview
---

# 集群部署概述

KWDB 支持使用部署以下集群：

|    类别       | 多副本集群                                                   | 单副本集群                                                   |
| ---------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 定义       | KWDB 在同一机房的多个节点上运行，每份数据默认有 3 份副本，且副本分布在不同节点上。 | KWDB 在同一机房的多个节点上运行，整个集群只有一份数据副本，所有数据的存储和更新操作都由该副本负责。 |
| 性能       | 数据写入性能弱于单节点部署和单副本集群；<br>简单场景下数据读取性能略弱于单节点部署，复杂场景下数据读取性能与单副本集群相同。 | 数据写入性能优于多副本集群，略弱于单节点部署；<br>简单场景下数据读取性能略弱于单节点部署，复杂场景下数据读取性能与多副本集群相同。 |
| 高可用性   | 支持高可用性，能够实现故障转移和数据强一致性。更多详细信息，参见[集群高可用](../db-operation/cluster-ha.md)。 | 不支持高可用性。集群节点出现故障时，数据写入、查询和 DDL 操作可能失败；故障节点数超过集群节点总数的一半时，所有操作将会暂停。 |

单节点部署与集群部署方式略有不同，单节点部署详细信息，参见[单节点部署](../quickstart/overview.md)。

本节包含以下文档：

- [部署流程](./deploy-workflow.md)
- 部署准备
  - [裸机部署准备](./prepare/before-deploy-bare-metal.md)
  - [容器部署准备](./prepare/before-deploy-docker.md)
- 集群部署
  - [使用脚本部署](./cluster-deployment/script-deployment.md)
  - [使用 kwbase CLI 部署](./cluster-deployment/kwbase-cli-depployment.md)
  - [使用 Docker Run 部署](./cluster-deployment/docker-deployment.md)
- 集群配置
  - [配置许可证](./configure-license.md)
  - [创建用户](./user-config.md)
  - 配置集群
    - [裸机集群配置](./cluster-config/cluster-config-bare-metal.md)
    - [容器集群配置](./cluster-config/cluster-config-docker.md)
- 集群管理
  - [启动与停止 KaiwuDB 服务](./local-start-stop.md)
  - [卸载集群](./uninstall-cluster.md)