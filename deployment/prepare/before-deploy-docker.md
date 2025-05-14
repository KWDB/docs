---
title: 容器部署准备
id: before-deploy-docker
---

# 容器部署准备

## 硬件

:::warning 说明
为了提高可用性，降低数据丢失的风险，建议在单台计算机上只运行一个节点。KWDB 采用跨节点复制机制，如果在一台计算机上同时运行多个节点，当计算机发生故障时，更有可能丢失数据。
:::

下表列出部署 KWDB 所需的硬件规格要求。在实际部署时，用户需要根据实际的业务规模和性能要求，规划硬件资源。

| <div style="width:90px">项目</div>  | 要求                                                                                                                                                                                                 |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CPU 和内存 | 单节点配置建议不低于 4 核 8G。对于数据量大、复杂的工作负载、高并发和高性能场景，建议配置更高的 CPU 和内存资源以确保系统的高效运行。  |
| 磁盘                               | - 推荐使用 SSD 或者 NVMe 设备，尽量避免使用 NFS、CIFS、CEPH 等共享存储。<br>- 使用 HDD 硬盘部署单机版本时，避免设备数过多或每秒写入测点数过高，否则数据写入性能将显著下降；不建议使用 HDD 部署分布式集群版本。<br> - 磁盘至少能够实现 500 IOPS 和 30 MB/s 处理效率。<br> - KWDB 系统自身启动不会占用过多磁盘容量（低于 1G）。实际所需磁盘大小主要取决于用户的业务量以及是否开启 KWDB 压缩等可以减少原始数据磁盘占用的功能。用户可以结合下面的公式预估原始业务数据对磁盘的需求量：<br> - 总存储空间 = 设备数量 x 单台设备每天写入行数 x 分区天数 x 总分区数 x (行宽/1024/1024+15/64/1000000)/1024。更多详细信息，参见[预估磁盘使用量](../../db-operation/cluster-planning.md#预估磁盘使用量)。 <br> - 每个节点的存储空间 = 总存储空间/节点数 |
| 文件系统                           | 建议使用 ext4 文件系统。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

## 操作系统

:::warning 说明

- 如果目标机器尚未安装 Docker，请提前安装适合您操作系统的 Docker 容器。更多信息，参见 [Docker 安装文档](https://docs.docker.com/desktop/install/linux-install/)。
- 如果目标机器无法联网且未安装 Docker，请采用二进制包安装 Docker。更多信息，参见 [Docker 安装文档](https://docs.docker.com/engine/install/binaries/)和[安装后说明](https://docs.docker.com/engine/install/linux-postinstall/)。
- 未提及的操作系统版本**也许可以**运行 KWDB，但尚未得到 KWDB 官方支持。

:::

KWDB 容器镜像支持在以下已安装 Docker 的操作系统中进行安装部署。

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

## 软件依赖（可选）

如采用部署脚本部署 KWDB, 目标机器需已安装 Docker Compose（1.20.0 及以上版本）。

- 在线安装 Docker Compose，参见 [Docker 官方文档](https://docs.docker.com/compose/install/)。
- 离线安装 Docker Compose，参见 [Docker 官方文档](https://docs.docker.com/compose/install/standalone/)。

示例：

```shell
sudo apt-get install docker-compose
```

## 端口

下表列出 KWDB 服务需要映射的端口。在安装部署前，确保目标机器的以下端口没有被占用且没有被防火墙拦截。在安装部署时，用户可以修改 `deploy.cfg` 文件中的端口配置参数。

| 端口号 | 说明    |
| ------------------------------------- | ------------------------------------------ |
| `8080`                                | 数据库 Web 服务端口                        |
| `26257`                               | 数据库服务端口、节点监听端口和对外连接端口 |

### 安装包和镜像

根据需要使用预编译安装包或容器镜像。

#### 获取容器安装包

获取系统环境对应的[安装包](https://gitee.com/kwdb/kwdb/releases)，将安装包复制到待安装 KWDB 的目标机器上，然后解压缩安装包：

::: warning 说明

目前 KWDB 开源仓库提供了 Ubuntu V22.04 ARM_64 和 x86_64 架构对应的[安装包](https://gitee.com/kwdb/kwdb/releases/) ，如需其它版本的容器安装包，请联系 [KWDB 技术支持](https://www.kaiwudb.com/support/)。
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

- Docker 命令：执行 `docker pull kwdb/kwdb:<version>` 获取镜像。

## 节点配置

### SSH 免密登录

1. 登录当前节点，生成公私密钥对。

   ```shell
   ssh-keygen -f ~/.ssh/id_rsa -N ""
   ```

   参数说明：

   - `-f`：指定生成的密钥对文件名。
   - `-N`：指定使用密钥时的密码。为了实现非交互式登录，建议将密码设置为空。

2. 将密钥分发至集群其它节点。

   ```shell
   ssh-copy-id -f -i ~/.ssh/id_rsa.pub -o StrictHostKeyChecking=no <node1>
   ```

3. 确认是否可以使用非交互式的方法登录集群其它节点。

   ```shell
   ssh <node1>
   ```

### 时钟同步

KWDB 采用中等强度的时钟同步机制来维持数据的一致性。当节点检测到自身的机器时间与集群中至少 50% 的节点的机器时间的误差值超过集群最大允许时间误差值（默认为 500 ms）的 80% 时，该节点会自动停止，从而避免违反数据一致性，带来读写旧数据的风险。每个节点都必须运行 NTP（Network Time Protocol，网络时间协议）或其他时钟同步软件，防止时钟漂移得太远。

以下示例以 CentOS 7 为例，介绍如何配置时钟同步：

1. 使用 SSH 连接到将要部署集群的节点。

2. 关闭 timesyncd 服务。在一些 Linux 发行版中，默认开启 timesyncd 服务。

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

7. 保存修改并退出文本编辑器。
8. 启动 NTP 服务。

   ```shell
   service ntp start
   ```

9. 在所有要安装 KWDB 服务的集群节点上重复执行以上步骤。
