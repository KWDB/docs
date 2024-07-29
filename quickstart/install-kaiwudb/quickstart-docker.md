---
title: 单节点容器部署
id: quickstart-docker
---

# 单节点容器部署

本文介绍如何使用 KWDB 容器镜像在单个节点上部署 KWDB。

::: warning 说明
目前，KWDB 未提供可供下载的 KWDB 容器镜像。如需使用容器镜像部署 KWDB，[联系](https://cs.kaiwudb.com/support/) KWDB 技术支持人员获取 KWDB 容器镜像。
:::

## 部署准备

### 硬件

下表列出部署 KWDB 所需的硬件规格。

| 项目       | 要求                                                                                                                               |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| CPU 和内存 | 建议不低于 4 核 8G。                                                                                                               |
| 磁盘       | - 推荐使用 SSD 或者 NVME 设备，尽量避免使用 NFS、CIFS、CEPH 等共享存储。<br >- 磁盘必须能够实现 500 IOPS 和 30 MB/s 处理效率。 |
| 文件系统   | 建议使用 ext4 文件系统。                                                                                                           |

实际部署时，用户可以根据实际的业务规模和性能要求规划硬件资源。更多详细信息，参见[硬件](../../db-operation/cluster-planning.md#硬件)。

### 操作系统

:::warning 说明

- 如果目标机器尚未安装 Docker，请提前安装适合您操作系统的 Docker 容器。更多信息，参见 [Docker 安装文档](https://docs.docker.com/desktop/install/linux-install/)。
- 如果目标机器无法联网且未安装 Docker，请采用二进制包安装 Docker。更多信息，参见 [Docker 安装文档](https://docs.docker.com/engine/install/binaries/)和[安装后说明](https://docs.docker.com/engine/install/linux-postinstall/)。
- 未提及的操作系统版本**也许可以**运行 KWDB，但尚未得到 KWDB 官方支持。

:::

KWDB 容器镜像支持在以下已安装 Docker 的操作系统中进行安装部署。

| 操作系统 | 版本 | 架构 |
| --- | --- | --- |
| Ubuntu | V20.04 | ARM_64 |
|  | V20.04 | x86_64 |
|  | V22.04 | x86_64 |
|  | V22.04 | ARM_64 |
| KylinOS | V10 | x86_64 |
|  | V10 | ARM_64 |
| Debian | V11 | ARM_64 |
| UOS | V20 | x86_64 |
| CentOS | 7 | x86_64 |
|  | 8 | x86_64 |
| openEuler | 22.03 | x86_64 |

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

### 安装包

获取系统环境对应的安装包，将安装包复制到待安装 KWDB 的目标机器上，然后解压缩安装包：

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
| `monitoring` 目录 | 存放 Prometheus 配置文件、Grafana Dashboard 模板等文件。|

## 部署 KWDB

部署 KWDB 时，系统将对配置文件、运行环境、硬件配置和软件依赖进行检查。如果相应硬件未能满足要求，系统将继续安装，并提示硬件规格不满足要求。如果软件依赖未能满足要求，系统将中止安装，并提供相应的提示信息。

在部署过程中，系统会自动生成相关日志。如果部署时出现错误，用户可以通过查看终端输出或 KWDB 安装目录中 `log` 目录里的日志文件，获取详细的错误信息。

::: warning 提示
容器部署支持使用 YAML（`.yml`）文件和安装脚本两种方式，使用 YAML（`.yml`）文件进行快速部署时，仅支持非安全模式，登录 KWDB 数据库时需使用非安全连接模式。安装脚本部署支持安全模式和非安全模式。具体部署步骤，参见[容器部署](../../deployment/docker/docker-deployment.md)。
:::

### 前提条件

- [联系](https://cs.kaiwudb.com/support/) KWDB 技术支持人员，获取 KWDB 容器镜像。
- 待部署节点的硬件、操作系统、软件依赖和端口满足安装部署要求。
- 安装用户为 root 用户或者拥有 `sudo` 权限的普通用户。
  - root 用户和配置 `sudo` 免密的普通用户在执行部署脚本时无需输入密码。
  - 未配置 `sudo` 免密的普通用户在执行部署脚本时，需要输入密码进行提权。
- 安装用户为非 root 用户时，需要通过 `sudo usermod -aG docker $USER` 命令将用户添加到 `docker` 组。

### 部署步骤

如需部署 KWDB，遵循以下步骤。

1. 在 `kaiwudb_install/packages` 目录下导入 `KaiwuDB.tar` 文件，获取镜像名称。

    ```yaml
    # docker load < KaiwuDB.tar
    Loaded image: "path-to-your-docker-image"
    ```

2. 创建 `docker-compose.yml` 配置文件。

    ::: warning 说明
    `image` 参数的取值必须是导入 `KaiwuDB.tar` 文件后获取的镜像名称。
    :::

    配置文件示例：

    ```yaml
    version: '3.3'
    services:
      kaiwudb-container:
        image: "path-to-your-docker-image"
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

3. 运行以下命令，快速启动 KWDB。

    ```shell
    docker-compose up -d
    ```

4. （可选）配置 KWDB 开机自启动。

    配置 KWDB 开机自启动后，如果系统重启，则自动启动 KWDB。

    ```shell
    systemctl enable kaiwudb
    ```
