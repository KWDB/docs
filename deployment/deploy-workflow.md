---
title: 部署流程
id: deploy-workflow
---

# 部署流程

## 部署准备

部署 KWDB 集群前，请根据以下内容检查待部署节点的硬件和软件环境是否符合要求：

- [裸机部署准备](./prepare/before-deploy-bare-metal.md)
- [容器部署准备](./prepare/before-deploy-docker.md)

## 集群部署

集群部署支持以下三种部署方式：

- [使用部署脚本部署（推荐）](./cluster-deployment/script-deployment.md)：最简便的集群部署方式, 用户只需几个命令即可完成整个集群的部署，内置故障检测和节点恢复机制，适合快速搭建测试或生产环境。
- [使用 kwbase CLI 部署](./cluster-deployment/kwbase-cli-deployment.md)：适用于使用源码自行编译部署的用户，适合有一定技术背景、希望深度定制部署过程的用户。
- [使用 Docker Run 部署](./cluster-deployment/docker-deployment.md)：适用于偏好使用容器化技术进行部署的用户，适合容器化测试环境或轻量级的开发场景。

## 集群配置

集群部署和启动后，用户需要完成以下操作：

- **创建数据库用户（可选）**：用户可以使用安装包目录中的 `add_user.sh` 脚本或使用 kwbase CLI 为数据库创建用户，然后使用该用户名和密码连接和操作数据库，有关详细信息，参见[创建用户](./user-config.md)。
- **配置集群参数（可选）**：
  - **脚本部署** 裸机安装部署后，系统生成 `kaiwudb_env` 和 `kaiwudb.service` 文件，用于配置 KWDB 启动参数和 CPU 资源占用, 有关详细信息，参见[配置集群](./cluster-config/cluster-config-bare-metal.md)。容器安装部署后，系统在 `/etc/kaiwudb/script` 目录下生成 Docker Compose 配置文件 `docker-compose.yml` 。用户可以修改通过该文件来配置 KWDB 的启动参数和 CPU 资源占用。有关详细信息，参见[配置集群](./cluster-config/cluster-config-docker.md)。
  - **kwbase CLI 和 Docker Run 部署**: 用户可以通过 `kwbase start` 和 `kwbase start-single-replica` 命令设置集群启动参数，有关详细信息，参见 [kwbase start](../tool-command-reference/client-tool/kwbase-sql-reference.md#kwbase-start) 和 [kwbase start-single-replica](../tool-command-reference/client-tool/kwbase-sql-reference.md#kwbase-start-single-replica)。

- **连接集群**：用户可以使用以下任一方式，连接集群，进行数据操作：
  - [`kwbase` CLI 工具](../quickstart/access-kaiwudb/access-kaiwudb-cli.md)
  - [KaiwuDB 开发者中心](../kaiwudb-developer-center/overview.md)
  - KWDB 支持的[连接器](../development/overview.md)

## 集群管理

- 如需停止或重启集群中的单个节点，参见[启动与停止 KWDB 服务](./local-start-stop.md)。
- 如需卸载集群，参见[卸载集群](./uninstall-cluster.md)。
