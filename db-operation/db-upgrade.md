---
title: 数据库升级
id: db-upgrade
---

# 数据库升级

## 概述

本节介绍 KWDB 数据库的升级方法。请根据实际部署拓扑完成升级准备，再按安装时选择的部署方式执行对应的升级步骤。

### 升级路径

| 部署拓扑 | 当前版本 | 目标版本 | 升级方式 |
|---------|---------|---------|---------|
| 单机部署 | 3.0.0、3.1.0 | 3.2.0 | 脚本和命令行部署：升级程序<br>容器镜像部署：容器镜像升级 |
|  | 1.x、2.x | 3.2.0 | 导入导出 |
| 多副本集群 | 3.0.0、3.1.0 | 3.2.0 | 脚本和命令行部署：升级程序<br>容器镜像部署：容器镜像升级 |
|  | 1.x、2.x | 3.2.0 | 导入导出 |
| 单副本集群 | 3.0.0、3.1.0 | 3.2.0 | 脚本和命令行部署：升级程序<br>容器镜像部署：容器镜像升级 |
|  | 1.x、2.x | 3.2.0 | 导入导出 |


:::warning 说明
从 3.0.0 升级至 3.2.0 时，如需使用 3.1.0 以后新增的时序 raft log 存储引擎，请先部署全新集群，再导入历史数据。
:::


**注意事项**

- 升级后无法简单降级至之前版本。如果需要降级，必须先卸载当前版本，再使用原有版本安装 KWDB，然后使用卸载前创建的备份将数据还原到数据库。有关卸载数据库的详细信息，参见[卸载 KWDB](../deployment/uninstall-cluster.md)。
- KWDB 支持通过导入导出方式将之前任一版本升级至最新版本。具体操作，参见[数据导出](../db-administration/import-export-data/export-data.md)和[数据导入](../db-administration/import-export-data/import-data.md)。**注意**：从 2.x 版本升级时，导出的 `meta.sql` 文件中包含时序表的 `PARTITION INTERVAL` 语法。由于 3.1.0 及以后版本的时序表已废弃该语法（注：时序库仍然支持），导入前需手动删除文件中的相关语法，否则会导致导入失败；使用导入导出升级方式升级后，多副本集群的高可用性可能会受到影响。

## 升级准备

### 单机部署

1. 确认新版本高于已安装版本。

2. 停止 KWDB 服务：

    ```bash
    systemctl stop kaiwudb
    ```

3. 备份用户数据目录。

### 集群部署

1. 确认新版本高于已安装版本。

2. 检查集群状态：

   - 查看集群状态：
      ```bash
      kw-status
      ```
   - 查看副本状态：
      ```sql
      SELECT sum((metrics->>'ranges.unavailable')::DECIMAL)::INT AS ranges_unavailable,
            sum((metrics->>'ranges.underreplicated')::DECIMAL)::INT As ranges_underreplicated
      FROM kwdb_internal.kv_store_status;
      ```

4. 通过 `SHOW JOBS` SQL 命令检查是否存在正在执行的模式更改或批量导入操作。

5. 检查集群内表的 leaseholder 和副本的分布是否均匀：

    ```sql
    SELECT * from kwdb_internal.ranges
    ```

6. 备份集群。如果升级失败，可以使用备份将集群还原到之前的状态。

## 执行升级

### 安装程序升级

使用安装程序升级过程中，如果出现节点未安装 KWDB、KWDB 仍在运行中、版本有误或部署方式有误等错误，系统将中止升级并给予相应提示。

#### 前提条件

- 已获取新版本的 KWDB 安装程序（`.run` 文件）。
- 待升级节点已安装 KWDB。
- 已备份待升级节点的用户数据目录。
- 执行节点（集群内任一节点）可通过 SSH 登录至待升级节点，并对待升级节点的安装目录拥有写入权限。
- 用户为 `root` 用户或已配置 `sudo` 免密的普通用户。
- 容器部署方式下，如果用户为非 `root` 用户，需要通过 `sudo usermod -aG docker $USER` 命令将用户添加到 `docker` 组。

#### 命令行模式

1. 将新版本安装程序复制至执行升级操作的集群节点，并赋予执行权限：

    ```bash
    chmod +x KaiwuDB-*.run
    ```

2. 在待升级节点，停止 KWDB 服务：

    ```bash
    sudo systemctl stop kaiwudb
    ```

3. 在执行节点，以命令行模式启动安装程序：

    ```bash
    ./KaiwuDB-*.run -c
    # 或者
    ./KaiwuDB-*.run --cli
    ```

4. 在主功能菜单中，输入 `4` 选择升级节点：

    ```plain
    1. 安装 KaiwuDB
    2. 卸载 KaiwuDB
    3. 安装 KaiwuDB 并加入集群
    4. 升级节点
    5. 退出

    请输入操作 [1-5]:
    ```

5. 将待升级的节点数量设置为 `1`。

6. 安装程序自动生成升级配置文件并打开编辑器，将 `host` 地址修改为待升级节点的 IP 地址，确认其余配置无误后保存退出，系统自动开始升级。

    ```ini
    [node1]
    host=192.168.122.224
    port=22
    user=admin
    passwd=*******
    ```

7. 在待升级节点，根据部署方式修改相关配置文件：

    - 裸机部署：修改以下配置文件，将 IP 地址替换为实际节点 IP：

        ```bash
        sudo vim /etc/systemd/system/kaiwudb.service
        sudo vim /usr/local/kaiwudb/bin/kw-status.sh
        sudo vim /usr/local/kaiwudb/bin/kw-sql.sh
        ```

    - 容器部署：
        1. 修改 `/etc/kaiwudb/script/docker-compose.yml`：
            1. 删除 `ports` 配置块和 `deploy.resources` 配置块。
            2. 将 `networks` 改为 host 模式：
                ```yaml
                network_mode: host
                ```
            3. 将 `command` 中的 IP 改为实际节点 IP。

        2. 修改以下脚本中的节点 IP：

            ```bash
            sudo vim /etc/kaiwudb/script/kw-status.sh
            sudo vim /etc/kaiwudb/script/kw-sql.sh
            ```

8. 在待升级节点，重新加载系统服务配置并启动 KWDB：

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start kaiwudb
    ```

9. 在待升级节点，检查节点状态：

    ```bash
    kw-status
    ```

10. 对集群中的其余节点重复步骤 2–9，逐一完成升级。

11. 完成所有节点升级后，验证数据是否完整。

#### 终端图形交互模式

1. 将新版本安装程序复制至执行升级操作的集群节点，并赋予执行权限：

    ```bash
    chmod +x KaiwuDB-*.run
    ```

2. 在待升级节点，停止 KWDB 服务：

    ```bash
    sudo systemctl stop kaiwudb
    ```

3. 在执行节点，以终端图形交互模式启动安装程序：

    ```bash
    ./KaiwuDB-*.run -i
    # 或者
    ./KaiwuDB-*.run --interact
    ```

4. 在主功能菜单中，使用方向键选中**升级节点**，按回车确认。

5. 进入升级参数设置菜单，点击**设置升级节点**，依次填写待升级节点的 IP、端口、用户名和密码，点击**保存**。选中**开始升级**，按回车开始升级。

6. 在待升级节点，根据部署方式修改相关配置文件：

    - 裸机部署：修改以下配置文件，将 IP 地址替换为实际节点 IP：

        ```bash
        sudo vim /etc/systemd/system/kaiwudb.service
        sudo vim /usr/local/kaiwudb/bin/kw-status.sh
        sudo vim /usr/local/kaiwudb/bin/kw-sql.sh
        ```

    - 容器部署：
        1. 修改 `/etc/kaiwudb/script/docker-compose.yml`：
            1. 删除 `ports` 配置块和 `deploy.resources` 配置块。
            2. 将 `networks` 改为 host 模式：
                ```yaml
                network_mode: host
                ```
            3. 将 `command` 中的 IP 改为实际节点 IP。

        2. 修改以下脚本中的节点 IP：

            ```bash
            sudo vim /etc/kaiwudb/script/kw-status.sh
            sudo vim /etc/kaiwudb/script/kw-sql.sh
            ```

7. 在待升级节点，重新加载系统服务配置并启动 KWDB：

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start kaiwudb
    ```

8. 在待升级节点，检查节点状态：

    ```bash
    kw-status
    ```

9. 对集群中的其余节点重复步骤 2–8，逐一完成升级。

10. 完成所有节点升级后，验证集群数据是否完整。


## 编译版本升级

对于从源代码编译安装的 KWDB 实例，可以通过编译新版本源代码的方式进行升级。这种升级方式适用于有特殊定制需求的用户，但需要用户具备一定的编译和部署能力。

### 前提条件

- 已完成数据和配置备份
- 已下载新版本的[源代码](https://gitee.com/kwdb/kwdb)
- [编译环境和相关依赖](https://gitee.com/kwdb/kwdb#%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F%E5%92%8C%E8%BD%AF%E4%BB%B6%E4%BE%9D%E8%B5%96)满足 KWDB 要求

### 步骤

1. 按照 [KWDB 编译文档](https://gitee.com/kwdb/kwdb#%E7%BC%96%E8%AF%91%E5%92%8C%E5%AE%89%E8%A3%85)编译新版本。
2. 使用与原版本相同的[启动命令](../kaiwudb-tools/kwbase-cli-tool.md#kwbase-start)启动服务。
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