---
title: 概述
id: bare-metal-overview
---

# 概述

部署 KWDB 集群前，请先根据[裸机部署准备](./before-deploy-bare-metal.md)检查待部署节点的硬件和软件环境是否符合要求。

在部署过程中，系统将对配置文件、运行环境、硬件配置、软件依赖和免密登录进行检查。如果硬件不满足要求，系统仍会继续安装，并提示硬件规格不足。如果软件依赖未满足要求，系统将中止安装，并给出相应提示。在部署期间，系统会生成相关日志。如果部署时出现错误，用户可以通过终端输出或 KWDB 安装目录下 `log` 文件夹里的日志文件获取详细信息。

部署完成后，系统会将 KWDB 封装成系统服务（名称为 `kaiwudb`），并生成以下文件：

- `kaiwudb.service`：配置 KWDB 的 CPU 资源占用率。
- `kaiwudb_env`：配置 KWDB 启动参数和环境变量。

用户可根据需要对集群进行定制化配置，更多详细信息，参见[配置集群](./cluster-config-bare-metal.md)。

部署完成后，用户可以使用安装包目录中的 `add_user.sh` 脚本为数据库[创建用户和密码](./user-config-bare-metal.md)，然后使用该用户名和密码连接和操作数据库，也可以直接使用 [KaiwuDB 开发者中心](../../kaiwudb-developer-center/overview.md) 或 KWDB 支持的[连接器](../../development/overview.md)进行数据库操作。

如需停止或重启集群中的单个节点，参见[启动与停止 KWDB 服务](./local-start-stop-bare-metal.md)。

如需卸载集群，参见[卸载集群](./uninstall-cluster-bare-metal.md)。