---
title: 数据库升级
id: db-upgrade
---

# 数据库升级

## 单机升级

KWDB 单机部署仅支持离线升级。

如果升级过程中出现错误，例如节点未安装 KWDB, KWDB 仍在运行中、版本有误或部署方式有误，系统将中止升级，并给与用户相应提示。

如果升级过程中因新版本导入失败导致升级失败，系统将保留数据目录、证书和配置文件，删除节点中的新版本安装文件，由用户自行决定后续手动安装新版本或旧版本。

::: warning 注意
升级后无法简单降级到之前版本。如果需要降级，必须先卸载现有版本，使用原有版本安装后，并通过卸载前创建的备份将数据还原到数据库。数据库卸载步骤见[卸载裸机部署的数据库](../deployment/bare-metal/uninstall-db-bare-metal.md)和[卸载容器部署的数据库](../deployment/docker/uninstall-db-docker.md)。
:::

前提条件：

- 待升级节点已安装 KWDB。
- 已备份待升级节点的用户数据目录。
- 已获取新版本的 KWDB 安装包，且新版本高于已安装版本。
- 用户为 root 用户或者拥有 sudo 权限的普通用户。
  - root 用户和配置 sudo 免密的普通用户在执行命令时无需输入密码。
  - 未配置免密的普通用户在执行命令时需要输入密码进行提权。
  ::: warning 提示
   容器部署方式下，如果用户为非 root 用户，还需要通过 `sudo usermod -aG docker $USER` 命令将用户添加到 `docker` 组。
  :::

步骤：

1. 将新版本的安装包拷贝到待升级的节点，解压安装包。

2. 检查 KWDB 服务是否已停止，如果KWDB服务仍在运行中，需执行 `systemctl stop kaiwudb` 命令停止服务。

   ```Shell
   systemctl status kaiwudb
   ```

3. 在新版本的安装包目录执行本地升级命令。

   ```Shell
   ./deploy.sh upgrade -l
   ```

   或者

   ```Shell
   ./deploy.sh upgrade --local
   ```

   升级成功后，系统将显示以下提示信息：

   ```Shell
   UPGRADE COMPLETED: KaiwuDB has been upgraded successfully! ...
   ```

4. 启动 KWDB。

   ```Shell
   systemctl start kaiwudb
   ```

5. 启动成功后，检查数据库是否已正常运行。

   ```Shell
   systemctl status kaiwudb
   ```

## 集群升级

KWDB 集群支持 KWDB 2.0 和 2.0.4 版本通过导入导出方式升级到 2.1.0 版本，具体导入导出操作见[数据导出](../db-administration/import-export-data/export-data.md)和[数据导入](../db-administration/import-export-data/import-data.md)。

::: warning 注意
由于 2.0.4 版本与早期版本之间存在兼容性差异，使用导入导出方式升级到 2.0.4 版本后，集群的高可用性可能会受到影响.
:::