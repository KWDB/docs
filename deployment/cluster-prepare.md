---
title: 部署准备
id: cluster-prepare
---

# 部署准备

## 硬件

:::warning 说明
为了提高可用性，降低数据丢失的风险，建议在单台计算机上只运行一个节点。KWDB 采用跨节点复制机制，如果在一台计算机上同时运行多个节点，当计算机发生故障时，更有可能丢失数据。
:::

下表列出部署 KWDB 所需的硬件规格。

| 项目  | 要求  |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| CPU 和内存 | 单节点配置建议不低于 4 核 8G。对于数据量大、复杂的工作负载、高并发和高性能场景，建议配置更高的 CPU 和内存资源以确保系统的高效运行。  |
| 磁盘       | - 推荐使用 SSD 或者 NVMe 设备，尽量避免使用 NFS、CIFS、CEPH 等共享存储。<br> - 磁盘必须能够实现 500 IOPS 和 30 MB/s 处理效率。<br>- 不建议使用 HDD 部署分布式集群版本。<br> - KWDB 系统自身启动不会占用过多磁盘容量（低于 1G）。实际所需磁盘大小主要取决于用户的业务量。|
| 文件系统   | 建议使用 ext4 文件系统。  |

## 操作系统

KWDB 支持在以下操作系统进行安装部署：

| 操作系统 | 版本 | 裸机部署 | 裸机部署  | 容器部署 | 容器部署 |
|---------|------|---------------|---------------|---------------|---------------|
| | | ARM64 |  x86_64 | ARM64 | x86_64 |
| Anolis | 7 | | | ✓ | ✓ |
|  | 8 | ✓ | ✓ | ✓ | ✓ |
| CentOS | 7 | | | | ✓ |
|  | 8 | | | | ✓ |
| Debian | V11 | | | ✓ | |
| openEuler | 24.03 | | | | ✓ |
| Ubuntu | V20.04 | ✓ | ✓ | ✓ | ✓ |
|  | V22.04 | ✓ | ✓ | ✓ | ✓ |
|  | V24.04 | ✓ | ✓ | ✓ | ✓ |
| UOS | 1050e | | | ✓ | ✓ |
|  | 1060e | | | ✓ | ✓ |
|  | 1070e | ✓ | ✓ | ✓ | ✓ |
| Windows Server | WSL2 | | ✓ | | ✓ |

:::warning 说明

- 容器部署需要目标机器已安装 Docker。如未安装，请参考 [Docker 官方安装文档](https://docs.docker.com/desktop/install/linux-install/) 进行安装。对于无法联网的环境，可下载 Docker 二进制包进行离线安装，详见 [Docker 离线安装指南](https://docs.docker.com/engine/install/binaries/)。
- 未提及的操作系统版本**也许可以**运行 KWDB，但尚未得到 KWDB 官方支持。
- 如需获取[下载页面](https://gitee.com/kwdb/kwdb/releases/)未提供的对应版本安装包，请联系 [KWDB 技术支持](https://www.kaiwudb.com/support/)。

:::

## 软件依赖

### 裸机部署

安装时，KWDB 会对依赖进行检查。如果缺少依赖会退出安装并提示依赖缺失。如果目标机器不能联网，用户需要在能联网的机器上根据目标机器的操作系统下载好所有依赖文件，然后将依赖文件复制到目标机器上进行安装。

下表列出需要在目标机器安装的依赖。

| 依赖 | 版本 | 说明 |
| --- | --- | --- |
| OpenSSL | v1.1.1+ | N/A |
| libprotobuf | v3.6.1 ~ v21.x | **注意**：Ubuntu 18.04 默认的 libprotobuf 版本不满足要求，用户需要提前安装所需版本（推荐 3.6.1 和 3.12.4）。|
| GEOS | v3.3.8+ | 可选依赖 |
| xz-libs | v5.2.0+ | N/A |
| libgcc | v7.3.0+ | N/A |
| libgflags | 系统默认 | N/A |
| libkrb5 | 系统默认 | N/A |

### 容器部署

使用[脚本](./cluster-deployment/script-deployment.md)部署时，目标机器需已安装 Docker Compose（1.20.0 及以上版本）。

- 在线安装：参考 [Docker Compose 官方安装文档](https://docs.docker.com/compose/install/)
- 离线安装：参考 [Docker Compose 离线安装指南](https://docs.docker.com/compose/install/standalone/)
- Ubuntu/Debian 系统快速安装：

    ```shell
    sudo apt-get install docker-compose
    ```

## 端口要求

下表列出 KWDB 服务默认使用的端口。如需使用其他端口，可在安装部署过程中进行修改。

| 端口号 | 说明 |
|--------|------|
| `8080` | 数据库 Web 服务端口 |
| `26257` | 数据库服务端口、节点监听端口和对外连接端口 |
| `27257` | 数据库时序引擎间的 brpc 通信端口 |

## 安装包、容器镜像和编译版本

根据不同的使用场景，获取安装包、容器镜像或源码编译版本：

### 安装包

目前 KWDB 开源仓库提供了以下系统与架构的 [DEB 或 RPM 安装包](https://gitee.com/kwdb/kwdb/releases/)，如需其它系统或架构的安装包，请联系 [KWDB 技术支持](https://www.kaiwudb.com/support/)：

- Ubuntu V20.04 x86_64
- Ubuntu V20.04 ARM64
- Ubuntu V22.04 x86_64
- Ubuntu V22.04 ARM64

获取系统环境对应的 DEB 或 RPM 安装包后，将安装包复制到待安装 KWDB 的目标机器上，然后解压缩安装包：

```shell
tar -zxvf <package_name>
```

解压后生成的目录包含以下文件：

| 文件              | 说明                                                        |
|-------------------|-----------------------------------------------------------|
| `add_user.sh`     | 安装、启动 KWDB 后，为 KWDB 数据库创建用户。             |
| `deploy.cfg`      | 安装部署配置文件，用于配置部署节点的 IP 地址、端口等配置信息。 |
| `deploy.sh`       | 安装部署脚本，用于安装、卸载、启动、状态获取、关停和重启等操作。  |
| `packages` 目录   | 存放 DEB 或 RPM 包。<br>**说明**：具体包含的文件因安装包类型而异。                                      |
| `utils` 目录      | 存放工具类脚本。                                             |

### 容器镜像

KWDB 支持通过以下方式获取容器镜像：

- KWDB 3.1.0 之前的版本

  [下载](https://gitee.com/kwdb/kwdb/releases)容器安装包，解压后在 `kwdb_install/packages` 目录下导入 `KaiwuDB.tar` 文件。

  ```bash
  docker load < KaiwuDB.tar
  Loaded image: "image-name"
  ```

- KWDB 3.1.0 及以后的版本

  运行以下命令，获取 KWDB Docker 镜像。如获取最新的镜像版本，运行 `docker pull kwdb/kwdb:latest"` 命令。

  ``` bash
  docker pull kwdb/kwdb:<version>
  ```

### 源码编译和安装

根据 [KWDB 编译和安装说明](https://gitee.com/kwdb/kwdb#%E7%BC%96%E8%AF%91%E5%92%8C%E5%AE%89%E8%A3%85)完成源码下载、编译和安装。

## 节点配置

### SSH 免密登录

1. 登录当前节点，生成公私密钥对。

   ```shell
   ssh-keygen -f ~/.ssh/id_rsa -N ""
   ```

   参数说明：

   - `-f`：指定生成的密钥对文件名。
   - `-N`：将密钥密码设置为空，以实现免密登录。

2. 将密钥分发至集群其它节点。

   ```shell
   ssh-copy-id -f -i ~/.ssh/id_rsa.pub -o StrictHostKeyChecking=no <target_node>
   ```

3. 确认是否可以使用 SSH 免密登录到集群其它节点。

   ```shell
   ssh <target_node>
   ```

### 时钟同步

KWDB 采用中等强度的时钟同步机制来维持数据的一致性。当节点检测到自身的机器时间与集群中至少 50% 的节点的机器时间的误差值超过集群最大允许时间误差值（默认为 500 ms）的 80% 时，该节点会自动停止，从而避免违反数据一致性，带来读写旧数据的风险。每个节点都必须运行 NTP（Network Time Protocol，网络时间协议）或其他时钟同步软件，防止时钟漂移得太远。

以下示例以 CentOS 7 为例，介绍如何配置时钟同步。

1. 使用 SSH 登录到将要部署集群的节点。

2. 关闭 timesyncd 服务。

   ```shell
   timedatectl set-ntp no
   ```

3. 安装 NTP 服务。

   ```shell
   sudo apt install ntp
   ```

4. 关闭 NTP 后台进程。

   ```shell
   service ntp stop
   ```

5. 通过 NTP 服务同步机器时间。

   ```shell
   ntpdate -u 0.cn.pool.ntp.org
   ```

6. 打开 `/etc/ntp.conf` 文件，查找 `server` 和 `pool` 的相关配置并将其修改为如下内容。

   ```shell
   server 0.cn.pool.ntp.org iburst
   server 1.cn.pool.ntp.org iburst
   server 2.cn.pool.ntp.org iburst
   server 3.cn.pool.ntp.org iburst
   ```

7. 启动 NTP 服务。

   ```shell
   service ntp start
   ```

8. 在所有要安装 KWDB 服务的集群节点上重复执行以上步骤。
