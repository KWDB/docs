---
title: 部署准备
id: quickstart-prepare
---

# 部署准备

## 硬件

下表列出部署 KWDB 所需的硬件规格。

| 项目  | 要求  |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| CPU 和内存 | 单节点配置建议不低于 4 核 8G。对于数据量大、复杂的工作负载、高并发和高性能场景，建议配置更高的 CPU 和内存资源以确保系统的高效运行。  |
| 磁盘       | - 推荐使用 SSD 或者 NVMe 设备，尽量避免使用 NFS、CIFS、CEPH 等共享存储。<br> - 磁盘必须能够实现 500 IOPS 和 30 MB/s 处理效率。<br> - KWDB 系统自身启动不会占用过多磁盘容量（低于 1G）。实际所需磁盘大小主要取决于用户的业务量。|
| 文件系统   | 建议使用 ext4 文件系统。  |

## 操作系统

KWDB 产品特性在以下操作系统及对应的 CPU 架构组合上经过全面且系统化的验证：

| 操作系统 | 版本 | 裸机-ARM64 | 裸机-x86_64 |  容器-ARM64 | 容器-x86_64 |
|---------|------|:---:|:---:|:---:|:---:|
| CentOS | 7 | | | | ✓ |
| | 8 | | | | ✓ |
| openEuler | 22.03 | | ✓ | | ✓ |
| | 24.03 | | ✓ | | ✓ |
| Ubuntu | 20.04 | ✓ | ✓ | ✓ | ✓ |
| | 22.04 | ✓ | ✓ | ✓ | ✓ |
| | 24.04 | ✓ | ✓ | ✓ | ✓ |
| UOS | 1070e | ✓ | ✓ | ✓ | ✓ |

:::warning 说明

- 容器部署需要目标机器已安装 Docker。如未安装，请参考 [Docker 官方安装文档](https://docs.docker.com/desktop/install/linux-install/) 进行安装。对于无法联网的环境，可下载 Docker 二进制包进行离线安装，详见 [Docker 离线安装指南](https://docs.docker.com/engine/install/binaries/)。
- 如果系统开启了 SELinux，将无法使用 `service` 命令管理 KWDB，部署前建议关闭 SELinux。
- 如需在其他 Linux 发行版上裸机部署，可先通过 `ldd --version` 检查 glibc 版本，>= 2.28 理论上即可运行，但尚未得到 KWDB 官方支持。。
- 如需获取[下载页面](https://www.kaiwudb.com/download?tab=2)未提供的对应版本安装包，请联系 [KWDB 技术支持](https://www.kaiwudb.com/about/support)。

:::

## 软件依赖

### 裸机部署

下表列出使用安装程序部署时，需要在目标机器安装的依赖：

| 系统类型 | libc | libgcc | libstdc++ |
|---------|------|--------|-----------|
| x86_64、aarch64 | Debian 系列 | libc6 >= 2.28 | libgcc1/libgcc-s1 >= 7.3.0 | libstdc++6 >= 7.3.0 |
| RedHat 系列 | glibc >= 2.28 | libgcc >= 8.3.0 | libstdc++ >= 8.3.0 |


安装时，KWDB 会对依赖进行检查。如果缺少依赖会退出安装并提示依赖缺失。如果目标机器不能联网，用户需要在能联网的机器上根据目标机器的操作系统下载好所有依赖文件，然后将依赖文件复制到目标机器上进行安装。

### 容器部署

除上述依赖外，使用安装程序部署时，目标机器需已安装 Docker Compose（1.20.0 及以上版本）。

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
| `26257` | 数据库服务端口和对外连接端口 |

## 安装程序、容器镜像和编译版本

根据不同的使用场景，获取安装程序、容器镜像或源码编译版本：

### 安装程序

KWDB 安装程序封装为 `.run` 自解压可执行包，内置所有部署所需资源，支持命令行模式和终端图形交互模式。

目前 KWDB [下载页面](https://www.kaiwudb.com/download?tab=2)提供了以下系统与架构的安装程序，如需其它系统或架构的安装程序，请联系 [KWDB 技术支持](https://www.kaiwudb.com/about/support)：

- Ubuntu V20.04 x86_64
- Ubuntu V20.04 ARM64
- Ubuntu V22.04 x86_64
- Ubuntu V22.04 ARM64

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