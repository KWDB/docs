---
title: 单节点裸机部署
id: quickstart-bare-metal
---

# 单节点裸机部署

本文介绍如何使用 KWDB 二进制安装包在单个节点上安装部署 KWDB。

::: warning 提示

KWDB 支持基于 DRBD 块设备复制的开源软件方案，实现主备节点间的数据复制，如需实现单机高可用性，请先参阅[单机高可用性方案](../../best-practices/single-ha.md)。

:::

## 部署准备

### 硬件

下表列出部署 KWDB 所需的硬件规格。

| <div style="width:90px">项目</div>  | 要求  |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| CPU 和内存 | 单节点配置建议不低于 4 核 8G。对于数据量大、复杂的工作负载、高并发和高性能场景，建议配置更高的 CPU 和内存资源以确保系统的高效运行。  |
| 磁盘       | - 推荐使用 SSD 或者 NVMe 设备，尽量避免使用 NFS、CIFS、CEPH 等共享存储。<br > - 磁盘必须能够实现 500 IOPS 和 30 MB/s 处理效率。 |
| 文件系统   | 建议使用 ext4 文件系统。                                                                                                             |

实际部署时，用户可以根据实际的业务规模和性能要求规划硬件资源。更多详细信息，参见[预估磁盘使用量](../../db-operation/cluster-planning.md#预估磁盘使用量)。

### 操作系统

KWDB 支持在以下服务器操作系统进行安装部署。

| **操作系统** | **版本**                     | **架构** |
| :----------- | :--------------------------- | :------- |
| Anolis       | 8.6                          | ARM_64   |
|              | 8.6                          | x86_64   |
| KylinOS      | V10 SP3 2403<br>V10 SP3 2303 | ARM_64   |
|              | V10 SP3 2403<br>V10 SP3 2303 | x86_64   |
| Ubuntu       | V18.04                       | x86_64   |
|              | V20.04                       | ARM_64   |
|              | V20.04                       | x86_64   |
|              | V22.04                       | ARM_64   |
|              | V22.04                       | x86_64   |
|              | V24.04                       | ARM_64   |
|              | V24.04                       | x86_64   |
| UOS          | 1060e                        | x86_64   |
|              | 1060e                        | ARM_64   |

::: warning 说明
未提及的操作系统版本**也许可以**运行 KWDB，但尚未得到 KWDB 官方支持。
:::

### 软件依赖

安装时，KWDB 会对依赖进行检查。如果缺少依赖会退出安装并提示依赖缺失。如果目标机器不能联网，用户需要在能联网的机器上根据目标机器的操作系统下载好所有依赖文件，然后将依赖文件复制到目标机器上进行安装。

不同操作系统及安装包的依赖略有不同，请根据实际安装包类型及操作系统，在部署前安装好相应的依赖。下表列出需要在目标机器安装的依赖：

| 依赖 | 版本 | 说明 |
| --- | --- | --- |
| OpenSSL | v1.1.1+ | N/A |
| libprotobuf | v3.6.1+ | **注意**：Ubuntu 18.04 默认的 libprotobuf 版本不满足要求，用户需要提前安装所需版本（推荐 3.6.1 和 3.12.4）。|
| GEOS | v3.3.8+ | 可选依赖 |
| xz-libs | v5.2.0+ | N/A |
| squashfs-tools | any | N/A |
| libgcc | v7.3.0+ | N/A |
| mount | any | N/A |
| squashfuse | any | 可选依赖 |

### 端口要求

下表列出 KWDB 服务需要映射的端口。在安装部署前，确保目标机器的以下端口没有被占用且没有被防火墙拦截。在安装部署时，用户可以修改 `deploy.cfg` 文件中的端口配置参数。

| 端口号 | 说明    |
| ------------------------------------- | ------------------------------------------ |
| `8080`                                | 数据库 Web 服务端口                        |
| `26257`                               | 数据库服务端口、节点监听端口和对外连接端口 |

### 安装包

获取系统环境对应的 DEB 或 RPM 安装包，将安装包复制到待安装 KWDB 的目标机器上，然后解压缩安装包：

```shell
tar -zxvf <package_name>
```

解压后生成的目录包含以下文件：

| 文件              | 说明                                                        |
|-------------------|-----------------------------------------------------------|
| `add_user.sh`     | 安装、启动 KWDB 后，为 KWDB 数据库创建用户。             |
| `deploy.cfg`      | 安装部署配置文件，用于配置部署节点的 IP 地址、端口等配置信息。 |
| `deploy.sh`       | 安装部署脚本，用于安装、卸载、启动、状态获取、关停和重启等操作。  |
| `packages` 目录   | 存放 DEB、RPM 和镜像包。                                      |
| `utils` 目录      | 存放工具类脚本。                                             |

## 部署 KWDB

部署 KWDB 时，系统将对配置文件、运行环境、硬件配置和软件依赖进行检查。如果相应硬件未能满足要求，系统将继续安装，并提示硬件规格不满足要求。如果软件依赖未能满足要求，系统将中止安装，并提供相应的提示信息。

在部署过程中，系统会自动生成相关日志。如果部署时出现错误，用户可以通过查看终端输出或 KWDB 安装目录中 `log` 目录里的日志文件，获取详细的错误信息。

部署完成后，系统会将 KWDB 封装成系统服务（名称为 `kaiwudb`），并生成以下文件：

- `kaiwudb.service`：配置 KWDB 的 CPU 资源占用率。
- `kaiwudb_env`：配置 KWDB 启动参数。

### 前提条件

- 待部署节点的硬件、操作系统、软件依赖和端口满足安装部署要求。
- 安装用户为 root 用户或者拥有 `sudo` 权限的普通用户。

### 部署步骤

如需部署 KWDB，遵循以下步骤。

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
      - `cpu`: 可选参数，用于指定 KWDB 服务占用当前节点服务器 CPU 资源的比例，默认无限制。取值范围为 `[0,1]`，最大精度为小数点后两位。**注意**：如果部署环境为 Ubuntu 18.04 版本，部署集群后，需要将 `kaiwudb.service` 文件中的 `CPUQuota` 修改为整型值，例如，将 `180.0%` 修改为 `180%`，以确保设置生效。具体操作步骤，参见[配置 CPU 资源占用率](../../deployment/bare-metal/cluster-config-bare-metal.md#配置-cpu-资源占用率)。
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