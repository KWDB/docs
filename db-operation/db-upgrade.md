---
title: 数据库升级
id: db-upgrade
---

# 数据库升级

本节介绍了 KWDB 数据库在不同部署方式下的升级方法，包括使用部署脚本、编译版本及容器镜像部署的升级流程。升级前请务必仔细阅读相关注意事项，并根据实际部署方式选择合适的升级方案。

## 使用部署脚本升级

部署脚本升级是 KWDB 最常用的升级方式，适用于通过部署脚本安装的 KWDB 实例。根据部署拓扑的不同，可分为单机升级、多副本集群升级和单副本集群场景。
不同部署方式支持的升级方式有所不同：

- **单机部署**：使用升级脚本将 3.0.0 离线升级至 3.1.0，有关详细信息，参见[单机升级](#单机升级)。
- **多副本集群**：使用升级脚本将 3.0.0 集群节点逐一升级至 3.1.0，有关详细信息，参见[多副本集群升级](#多副本集群升级)。**注意**：若需使用 3.1.0 新增的时序 raft log 存储引擎，请先部署全新的 3.1.0 集群，再导入历史数据。
- **单副本集群**：使用升级脚本将 3.0.0 离线升级至 3.1.0，有关详细信息，参见[单副本集群升级](#单副本集群升级)。

::: warning 说明

- 升级后无法简单降级至之前版本。如果需要降级，必须先卸载当前版本，再使用原有版本安装 KWDB，然后使用卸载前创建的备份将数据还原到数据库。有关卸载单机版数据库的详细信息，参见[卸载数据库](../quickstart/uninstall-kaiwudb/uninstall-db.md)。有关卸载集群版本的详细信息，参见[卸载集群](../deployment/uninstall-cluster.md)。
- KWDB 支持通过导入导出方式将之前任一版本升级至最新版本。具体操作，参见[数据导出](../db-administration/import-export-data/export-data.md)和[数据导入](../db-administration/import-export-data/import-data.md)。**注意**：从 2.x 版本升级时，导出的 `meta.sql` 文件中包含时序表的 `PARTITION INTERVAL` 语法。由于 3.1.0 版本的时序表已废弃该语法（注：时序库仍然支持），导入前需手动删除文件中的相关语法，否则会导致导入失败；使用导入导出升级方式升级后，多副本集群的高可用性可能会受到影响。
:::

### 单机升级

升级过程中，如果出现节点未安装 KWDB、KWDB 仍在运行中、版本有误或部署方式有误等错误，系统将中止升级，并给与用户相应提示。

升级过程中，如果因新版本导入失败导致升级失败，系统将保留数据目录、证书和配置文件，删除节点中的新版本安装文件，用户可以选择手动安装新版本或旧版本。

#### 前提条件

- 待升级节点已安装 KWDB。
- 已备份待升级节点的用户数据目录。
- 已获取新版本的 KWDB 安装包，且新版本高于已安装版本。
- 用户为 root 用户或者拥有 `sudo` 权限的普通用户。
  - root 用户和配置 `sudo` 免密的普通用户在执行命令时无需输入密码。
  - 未配置 `sudo` 免密的普通用户在执行命令时，需要输入密码进行提权。
  - 容器部署方式下，如果用户为非 root 用户，需要通过 `sudo usermod -aG docker $USER` 命令将用户添加到 `docker` 组。

#### 步骤

1. 将新版本安装包拷贝至待升级的节点，解压安装包。

2. 检查 KWDB 服务是否已停止。如果 KWDB 服务仍在运行中，执行 `systemctl stop kaiwudb` 命令停止服务。

   ```shell
   systemctl status kaiwudb
   ```

3. 切换至新版本的安装包目录。

4. 执行本地升级命令。

   ```shell
   ./deploy.sh upgrade -l
   ```

   或者

   ```shell
   ./deploy.sh upgrade --local
   ```

   执行成功后，控制台输出以下信息：

   ```shell
   UPGRADE COMPLETED: KaiwuDB has been upgraded successfully! 
   ```

5. 启动 KWDB。

   ```shell
   systemctl start kaiwudb
   ```

6. 启动成功后，检查数据库是否已正常运行。

   ```shell
   systemctl status kaiwudb
   ```

### 多副本集群升级

在升级过程中，升级节点上的压缩与生命周期可能会执行失败，在升级完成后恢复正常。如果升级过程中出现错误，例如节点未安装 KWDB、节点状态异常或部署方式有误，系统将中止升级，并给与相应提示。

#### 准备升级

**步骤**：

1. 确保客户端与多个节点通信，避免单节点升级时客户端通信中断。

2. 查看集群状态。

   1. 检查集群节点状态。

         - 脚本部署

            ```shell
            kw-status
            ```

         - kwbase 命令

            ```shell
            <kwbase_path>/kwbase node status [--host=<ip:port>] [--insecure | --certs-dir=<path>]
            ```

   2. 查看副本状态。

         ```sql
      SELECT sum((metrics->>'ranges.unavailable')::DECIMAL)::INT AS ranges_unavailable,
         sum((metrics->>'ranges.underreplicated')::DECIMAL)::INT As ranges_underreplicated
      FROM kwdb_internal.kv_store_status;
         ```

3. 使用 `SHOW JOBS` SQL 命令检查是否存在正在执行的模式更改或批量导入操作。

4. 使用 `SELECT * from kwdb_internal.ranges` SQL 命令检查集群内表的 leaseholder（租约持有者）和副本的分布是否均匀。

5. 备份集群。如果升级失败，可以使用备份将集群还原到之前的状态。

#### 执行升级

为集群中的每个节点，执行以下升级操作。确保每次只升级一个节点。该节点重新加入集群后，确认节点版本、状态无误后，再升级下一个节点。

**前提条件**：

- 待升级节点已安装 KWDB，且节点状态为存活状态（ `is_available` 和 `is_live` 均为 `true`）。
- 已备份待升级节点的用户数据目录。
- 已获取新版本的 KWDB 安装包，且新版本高于已安装版本。
- 用户为 root 用户或者拥有 `sudo` 权限的普通用户。
  - root 用户和配置 `sudo` 免密的普通用户在执行命令时无需输入密码。
  - 未配置 `sudo` 免密的普通用户在执行命令时，需要输入密码进行提权。
  - 容器部署方式下，如果用户为非 root 用户，需要通过 `sudo usermod -aG docker $USER` 命令将用户添加到 `docker` 组。

**步骤**：

1. 将新版本的安装包拷贝到待升级的节点，解压安装包。

2. 检查 KWDB 服务是否已停止。如果 KWDB 服务仍在运行中，执行 `systemctl stop kaiwudb` 命令停止服务。

   ```shell
   systemctl status kaiwudb
   ```

3. 切换至新版本的安装包目录。

4. 执行本地升级命令。

   ```shell
   ./deploy.sh upgrade -l
   ```

   或者

   ```shell
   ./deploy.sh upgrade --local
   ```

   执行成功后，控制台输出以下信息：

   ```shell
   UPGRADE COMPLETED: KaiwuDB has been upgraded successfully! ...
   ```

5. 启动 KWDB。

   ```shell
   systemctl start kaiwudb
   ```

6. 启动成功后，检查数据库是否已正常运行。

   ```shell
   systemctl status kaiwudb
   ```

### 单副本集群升级

升级过程中，如果出现节点未安装 KWDB、KWDB 仍在运行中、版本有误或部署方式有误等错误，系统将中止升级，并给与用户相应提示。

升级过程中，如果因新版本导入失败导致升级失败，系统将保留数据目录、证书和配置文件，删除节点中的新版本安装文件，用户可以选择手动安装新版本或旧版本。

#### 前提条件

- 待升级节点已安装 KWDB。
- 已备份所有节点的用户数据目录。
- 已获取新版本的 KWDB 安装包，且新版本高于已安装版本。
- 用户为 root 用户或者拥有 `sudo` 权限的普通用户。
  - root 用户和配置 `sudo` 免密的普通用户在执行命令时无需输入密码。
  - 未配置 `sudo` 免密的普通用户在执行命令时，需要输入密码进行提权。
  - 容器部署方式下，如果用户为非 root 用户，需要通过 `sudo usermod -aG docker $USER` 命令将用户添加到 `docker` 组。

#### 步骤

1. 在集群所有节点执行停止数据库命令。

   ```shell
   systemctl stop kaiwudb
   ```

2. 在每个节点执行以下升级操作：
   1. 将新版本安装包拷贝至待升级的节点，解压安装包。
   2. 切换至新版本的安装包目录。
   3. 执行本地升级命令。

      ```shell
      ./deploy.sh upgrade -l
      ```

      或者

      ```shell
      ./deploy.sh upgrade --local
      ```

      执行成功后，控制台输出以下信息：

      ```shell
      UPGRADE COMPLETED: KaiwuDB has been upgraded successfully! 
      ```

3. 所有节点完成升级后，在每个节点执行以下命令启动数据库。
   1. 启动数据库。

      ```shell
      systemctl start kaiwudb
      ```

   2. 启动成功后，检查数据库是否已正常运行。

      ```shell
      systemctl status kaiwudb
      ```

## 编译版本升级

对于从源代码编译安装的 KWDB 实例，可以通过编译新版本源代码的方式进行升级。这种升级方式适用于有特殊定制需求的用户，但需要用户具备一定的编译和部署能力。

### 前提条件

- 已完成数据和配置备份
- 已下载新版本的[源代码](https://gitee.com/kwdb/kwdb)
- [编译环境和相关依赖](https://gitee.com/kwdb/kwdb#%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F%E5%92%8C%E8%BD%AF%E4%BB%B6%E4%BE%9D%E8%B5%96)满足 KWDB 要求

### 步骤

1. 按照 [KWDB 编译文档](https://gitee.com/kwdb/kwdb#%E7%BC%96%E8%AF%91%E5%92%8C%E5%AE%89%E8%A3%85)编译新版本。
2. 使用与原版本相同的[启动命令](../tool-command-reference/client-tool/kwbase-sql-reference.md#kwbase-start)启动服务。
3. 验证服务是否正常运行。

## 容器镜像部署升级

使用 Docker 容器镜像部署的 KWDB 实例，可以通过更新容器镜像的方式进行升级。具体升级方式包括 Docker Compose 升级和 Docker Run 升级。

### Docker Compose 升级

#### 前提条件

- 已完成数据和配置备份
- 已获取新版本容器镜像

#### 步骤

1. 加载新版本容器镜像：

   ```bash
   docker load < KaiwuDB.tar
   ```

2. 停止并移除现有容器：

   ```bash
   docker-compose down
   ```

3. 删除旧版本镜像：

   ```bash
   docker rmi ${image_name}
   ```

4. 修改 `docker-compose.yml` 文件，更新镜像版本。

5. 启动新版本 KWDB。

   ```bash
   docker-compose up -d
   ```

### Docker Run 升级

#### 前提条件

- 已完成数据和配置备份
- 已获取新版本容器镜像

#### 步骤

1. 停止 KWDB 容器。容器名称为运行容器时通过 `--name` 参数指定的容器名称。

   ```bash
   docker stop <kwdb-container>
   ```

2. 删除容器。

   ```bash
   docker rm <kwdb-container>
   ```

3. 获取新版本镜像。

   - 从镜像仓库拉取：

     ```bash
     docker pull kwdb/kwdb:<新版本号>
     ```

   - 从本地文件导入：

     ```bash
     docker load < KaiwuDB.tar
     ```

4. 启动新版本容器。注意：除镜像名称外，所有参数应与原容器保持一致。

   - 非安全模式:

     ```bash
     docker run -d --privileged --name kwdb \
         --ulimit memlock=-1 \
         --ulimit nofile=$max_files \
         -p $db_port:26257 \
         -p $http_port:8080 \
         -v /var/lib/kaiwudb:/kaiwudb/deploy/kwdb-container \
         --ipc shareable \
         -w /kaiwudb/bin \
         <kwdb_image> \
         ./kwbase start-single-node \
         --insecure \
         --listen-addr=0.0.0.0:26257 \
         --http-addr=0.0.0.0:8080 \
         --store=/kaiwudb/deploy/kwdb-container
     ```

   - 安全模式:

     ```bash
     docker run -d --privileged --name kwdb \
         --ulimit memlock=-1 \
         --ulimit nofile=$max_files \
         -p $db_port:26257 \
         -p $http_port:8080 \
         -v /etc/kaiwudb/certs:<certs_dir> \
         -v /var/lib/kaiwudb:/kaiwudb/deploy/kwdb-container \
         --ipc shareable \
         -w /kaiwudb/bin \<kwdb_image> \
         ./kwbase start-single-node \
         --certs-dir=<certs_dir> \
         --listen-addr=0.0.0.0:26257 \
         --http-addr=0.0.0.0:8080 \
         --store=/kaiwudb/deploy/kwdb-container
     ```