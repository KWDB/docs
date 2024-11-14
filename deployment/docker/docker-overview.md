---
title: 概述
id: docker-overview
---

# 容器部署概述

部署 KWDB 集群前，请先根据[容器部署准备](./before-deploy-docker.md)检查待部署节点的硬件和软件环境是否符合要求。

部署 KWDB 集群时，系统将对配置文件、运行环境、硬件配置、软件依赖和 SSH 免密登录进行检查。如果相应硬件未能满足要求，系统将继续安装，并提示硬件规格不满足要求。如果软件依赖未能满足要求，系统将中止安装，并提供相应的提示信息。在部署过程中，系统会自动生成相关日志。如果部署时出现错误，用户可以通过查看终端输出或 KWDB 安装目录中 `log` 目录里的日志文件，获取详细的错误信息。

部署完成后，系统将生成 `/etc/kaiwudb/` 目录。Docker Compose 配置文件 `docker-compose.yml` 位于 `/etc/kaiwudb/script` 目录下。部署完成后，用户可以修改 Docker Compose 配置文件 `docker-compose.yml`，配置 KWDB 的启动参数和 CPU 资源占用率。有关定制化部署配置的详细信息，参见[配置集群](./cluster-config-docker.md)。

部署完成后，用户可以使用安装包目录中的 `add_user.sh` 脚本为数据库[创建用户和密码](./user-config-docker.md)，然后使用该用户名和密码连接和操作数据库，也可以直接使用 [KaiwuDB 开发者中心](../../kaiwudb-developer-center/overview.md) 或 KWDB 支持的[连接器](../../development/overview.md)进行数据库操作。

如需停止或重启集群中的单个节点，参见[启动与停止 KWDB 服务](./local-start-stop-docker.md)。

如需卸载集群，参见[卸载集群](./uninstall-cluster-bare-metal.md)。