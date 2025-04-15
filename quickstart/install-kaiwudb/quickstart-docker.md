---
title: 单节点容器部署
id: quickstart-docker
---

# 单节点容器部署

本文介绍如何使用 KWDB 容器镜像或容器安装包在单个节点上部署 KWDB。

- 使用容器镜像部署：仅支持非安全模式，登录 KWDB 数据库时需使用非安全连接模式，具体操作说明，参见[使用 YAML 文件部署 KWDB](#使用-yaml-文件部署-kwdb)。
- 使用容器安装包部署：同时支持安全模式和非安全模式，登录 KWDB 数据库时应选择相应的连接模式，具体操作说明，参见[使用安装脚本部署 KWDB](#使用安装脚本部署-kwdb)。

::: warning 说明
KWDB 支持基于 DRBD 块设备复制的开源软件方案，实现主备节点间的数据复制，如需实现单机高可用性，请先参阅[单机高可用性方案](../../best-practices/single-ha.md)。
:::

## 部署准备

### 硬件

下表列出部署 KWDB 所需的硬件规格。

| 项目       | 要求                                                                                                                               |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| CPU 和内存 | 单节点配置建议不低于 4 核 8G。对于数据量大、复杂的工作负载、高并发和高性能场景，建议配置更高的 CPU 和内存资源以确保系统的高效运行。  |
| 磁盘       | - 推荐使用 SSD 或者 NVMe 设备，尽量避免使用 NFS、CIFS、CEPH 等共享存储。<br > - 磁盘必须能够实现 500 IOPS 和 30 MB/s 处理效率。 |
| 文件系统   | 建议使用 ext4 文件系统。                                                                                                           |

实际部署时，用户可以根据实际的业务规模和性能要求规划硬件资源。更多详细信息，参见[预估磁盘使用量](../../db-operation/cluster-planning.md#预估磁盘使用量)。

### 操作系统

:::warning 说明

- 如果目标机器尚未安装 Docker，请提前安装适合您操作系统的 Docker 容器。更多信息，参见 [Docker 安装文档](https://docs.docker.com/desktop/install/linux-install/)。
- 如果目标机器无法联网且未安装 Docker，请采用二进制包安装 Docker。更多信息，参见 [Docker 安装文档](https://docs.docker.com/engine/install/binaries/)和[安装后说明](https://docs.docker.com/engine/install/linux-postinstall/)。
- 未提及的操作系统版本**也许可以**运行 KWDB，但尚未得到 KWDB 官方支持。

:::

KWDB 支持在以下已安装 Docker 的操作系统中进行容器部署。

| **操作系统** | **版本**                     | **架构** |
| :----------- | :--------------------------- | :------- |
| Anolis       | 7.9                          | ARM_64   |
|              | 7.9                          | x86_64   |
|              | 8.6                          | ARM_64   |
|              | 8.6                          | x86_64   |
| CentOS       | 7                            | x86_64   |
|              | 8                            | x86_64   |
| Debian       | V11                          | ARM_64   |
| KylinOS      | V10 SP3 2403<br>V10 SP3 2303 | ARM_64   |
|              | V10 SP3 2403<br>V10 SP3 2303 | x86_64   |
| openEuler    | 22.03                        | x86_64   |
| Ubuntu       | V18.04                       | x86_64   |
|              | V20.04                       | ARM_64   |
|              | V20.04                       | x86_64   |
|              | V22.04                       | ARM_64   |
|              | V22.04                       | x86_64   |
|              | V24.04                       | ARM_64   |
|              | V24.04                       | x86_64   |
| UOS          | 1050e                        | x86_64   |
|              | 1060e                        | x86_64   |
|              | 1060e                        | ARM_64   |
|              | 1070e                        | x86_64   |

### 软件依赖

目标机器已安装 Docker Compose（1.20.0 及以上版本）。

- 在线安装 Docker Compose，参见 [Docker 官方文档](https://docs.docker.com/compose/install/)。
- 离线安装 Docker Compose，参见 [Docker 官方文档](https://docs.docker.com/compose/install/standalone/)。

```shell
sudo apt-get install docker-compose
```

### 端口要求

下表列出 KWDB 服务需要映射的端口。在安装部署前，确保目标机器的以下端口没有被占用且没有被防火墙拦截。在安装部署时，用户可以修改 `deploy.cfg` 文件中的端口配置参数。

| 端口号 | 说明    |
| ------------------------------------- | ------------------------------------------ |
| `8080`                                | 数据库 Web 服务端口                        |
| `26257`                               | 数据库服务端口、节点监听端口和对外连接端口 |

### 安装包和镜像

#### 获取容器安装包

获取系统环境对应的[安装包](https://gitee.com/kwdb/kwdb/releases)，将安装包复制到待安装 KWDB 的目标机器上，然后解压缩安装包：

::: warning 说明

目前 KWDB Gitee 仓库提供了 Ubuntu V22.04 ARM_64 和 x86_64 架构对应的[安装包](https://gitee.com/kwdb/kwdb/releases/) ，如需其它版本的容器安装包，请联系 [KWDB 技术支持](https://www.kaiwudb.com/support/)。
:::

```shell
tar -zxvf <install_package_name>
```

解压后生成的目录包含以下文件：

| 文件              | 说明                                                        |
|-------------------|-----------------------------------------------------------|
| `add_user.sh`     | 安装、启动 KWDB 后，为 KWDB 数据库创建用户。             |
| `deploy.cfg`      | 安装部署配置文件，用于配置部署节点的 IP 地址、端口等配置信息。 |
| `deploy.sh`       | 安装部署脚本，用于安装、卸载、启动、状态获取、关停和重启等操作。  |
| `packages` 目录   | 存放 DEB、RPM 和镜像包。                                      |
| `utils` 目录      | 存放工具类脚本。                                             |

#### 获取容器镜像

KWDB 支持通过以下方式获取容器镜像：

- [安装包](https://gitee.com/kwdb/kwdb/releases)：下载系统环境对应的安装包，解压后在 `kwdb_install/packages` 目录下导入 `KaiwuDB.tar` 文件。

    ```bash
    docker load < KaiwuDB.tar
    Loaded image: "image-name"
    ```

- Docker 命令：执行 `docker pull kwdb/kwdb:2.2.0` 获取镜像。

## 部署 KWDB

部署 KWDB 时，系统将对配置文件、运行环境、硬件配置和软件依赖进行检查。如果相应硬件未能满足要求，系统将继续安装，并提示硬件规格不满足要求。如果软件依赖未能满足要求，系统将中止安装，并提供相应的提示信息。

在部署过程中，系统会自动生成相关日志。如果部署时出现错误，用户可以通过查看终端输出或 KWDB 安装目录中 `log` 目录里的日志文件，获取详细的错误信息。

部署完成后，系统生成 `/etc/kaiwudb/` 目录。Docker Compose 配置文件 `docker-compose.yml` 位于 `/etc/kaiwudb/script` 目录下。部署完成后，用户可以修改 Docker Compose 配置文件 `docker-compose.yml`，配置 KWDB 的启动参数和 CPU 资源占用率。有关定制化部署配置的详细信息，参见[配置集群](../../deployment/docker/cluster-config-docker.md)。

### 使用 YAML 文件部署 KWDB

**前提条件**：

- 已获取 [KWDB 容器镜像](#获取容器镜像)。
- 待部署节点的硬件、操作系统、软件依赖和端口满足安装部署要求。
- 安装用户为 root 用户或者拥有 `sudo` 权限的普通用户。
  - root 用户和配置 `sudo` 免密的普通用户在执行部署脚本时无需输入密码。
  - 未配置 `sudo` 免密的普通用户在执行部署脚本时，需要输入密码进行提权。
- 安装用户为非 root 用户时，需要通过 `sudo usermod -aG docker $USER` 命令将用户添加到 `docker` 组。

**步骤**：

如需使用 YAML 文件部署 KWDB，遵循以下步骤。

1. 创建 `docker-compose.yml` 配置文件。

    ::: warning 说明
    `image` 参数的取值必须是导入 `KaiwuDB.tar` 文件后获取的镜像名或拉取的镜像名。
    :::

    配置文件示例：

    ```yaml
    version: '3.3'
    services:
      kaiwudb-container:
        image: "kwdb/kwdb:2.2.0"
        container_name: kaiwudb-experience
        hostname: kaiwudb-experience
        ports:
          - 8080:8080
          - 26257:26257
        ulimits:
          memlock: -1
        volumes:
          - /dev:/dev
        networks: 
          - default
        restart: on-failure
        ipc: shareable
        privileged: true
        environment:
          - LD_LIBRARY_PATH=/kaiwudb/lib
        tty: true
        working_dir: /kaiwudb/bin
        command: 
          - /bin/bash
          - -c
          - |
            /kaiwudb/bin/kwbase start-single-node --insecure --listen-addr=0.0.0.0:26257 --advertise-addr=127.0.0.1:26257 --http-addr=0.0.0.0:8080 --store=/kaiwudb/deploy/kaiwudb
    ```

2. 运行以下命令，快速启动 KWDB。

    ```shell
    docker-compose up -d
    ```

3. （可选）配置 KWDB 开机自启动。

    配置 KWDB 开机自启动后，如果系统重启，则自动启动 KWDB。

    ```shell
    systemctl enable kaiwudb
    ```

### 使用安装脚本部署 KWDB

**前提条件**：

- 已获取 [KWDB 容器安装包](#获取容器安装包)。
- 待部署节点的硬件、操作系统、软件依赖和端口满足安装部署要求。
- 安装用户为 root 用户或者拥有 `sudo` 权限的普通用户。
  - root 用户和配置 `sudo` 免密的普通用户在执行部署脚本时无需输入密码。
  - 未配置 `sudo` 免密的普通用户在执行部署脚本时，需要输入密码进行提权。
- 安装用户为非 root 用户时，需要通过 `sudo usermod -aG docker $USER` 命令将用户添加到 `docker` 组。

**步骤**：

如需使用安装脚本部署 KWDB，遵循以下步骤。

1. 登录待部署节点，编辑安装包目录下的 `deploy.cfg` 配置文件，设置安全模式、管理用户、服务端口等信息。

    ::: warning 说明
    默认情况下，`deploy.cfg` 配置文件中包含集群配置参数。请删除或注释 `[cluster]` 集群配置项。
    :::

    配置文件示例：

    ```yaml
    [global]
    secure_mode=tls
    management_user=kaiwudb
    rest_port=8080
    kaiwudb_port=26257
    data_root=/var/lib/kaiwudb
    cpu=1
    [local]
    node_addr=your-host-ip

    # [cluster]
    # node_addr=your-host-ip, your-host-ip
    # ssh_port=22
    # ssh_user=admin
    ```

    参数说明：

    - `global`：全局配置
      - `secure_mode`：是否开启安全模式，支持以下两种取值：
        - `insecure`：使用非安全模式。
        - `tls`：（默认选项）开启 TLS 安全模式。开启安全模式后，KWDB 生成 TLS 证书，作为客户端或应用程序连接数据库的凭证。生成的客户端相关证书存放在 `/etc/kaiwudb/certs` 目录。
      - `management_user`：KWDB 的管理用户，默认为 `kaiwudb`。安装部署后，KWDB 创建相应的管理用户以及和管理用户同名的用户组。
      - `rest_port`：KWDB Web 服务端口，默认为 `8080`。
      - `kaiwudb_port`：KWDB 服务端口，默认为 `26257`。
      - `data_root`：数据目录，默认为 `/var/lib/kaiwudb`。
      - `cpu`: 可选参数，用于指定 KWDB 服务占用当前节点服务器 CPU 资源的比例，默认无限制。取值范围为 `[0,1]`，最大精度为小数点后两位。
    - `local`：本地节点配置
      - `node_addr`：本地节点对外提供服务的 IP 地址，监听地址为 `0.0.0.0`，端口为 KWDB 服务端口。

2. 为 `deploy.sh` 脚本添加运行权限。

    ```shell
    chmod +x ./deploy.sh
    ```

3. 执行单机部署安装命令。

    ```shell
    ./deploy.sh install --single
    ```

    执行成功后，控制台输出以下信息：

    ```shell
    INSTALL COMPLETED: KaiwuDB has been installed successfuly! ...
    ```

4. 根据系统提示重新加载 `systemd` 守护进程的配置文件。

    ```shell
    systemctl daemon-reload
    ```

5. 启动 KWDB 节点。

    ```shell
    ./deploy.sh start
    ```

    执行成功后，控制台输出以下信息：

    ```shell
    START COMPLETED: KaiwuDB has started successfuly.
    ```

6. 查看 KWDB 节点状态。

    ```shell
    ./deploy.sh status
    ```

    或者

    ```shell
    systemctl status kaiwudb
    ```

7. （可选）配置 KWDB 开机自启动。

    配置 KWDB 开机自启动后，如果系统重启，则自动启动 KWDB。

    ```shell
    systemctl enable kaiwudb
    ```

8. （可选）执行 `add_user.sh` 脚本创建数据库用户。如果跳过该步骤，系统将默认使用 `root` 用户，且无需密码访问数据库。

    ```shell
    ./add_user.sh
    Please enter the username: 
    Please enter the password:
    ```

    执行成功后，控制台输出以下信息：

    ```shell
    [ADD USER COMPLETED]:User creation completed.
    ```