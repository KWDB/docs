---
title: 单节点容器部署
id: quickstart-docker
---

# 单节点容器部署

KWDB 支持两种单节点容器化部署方式：

- **使用容器安装包部署**：通过安装包内提供的部署脚本进行部署，支持配置数据库的部署模式、数据存储路径、端口等参数。更多信息，参见[使用脚本部署 KWDB](#使用脚本部署-kwdb)。

- **使用容器镜像部署**：直接基于 Docker 容器镜像进行部署，提供以下两种方式：
  - 使用 Docker Compose 和 YAML 配置文件部署，目前只支持非安全部署模式，更多信息，参见[使用 YAML 文件部署 KWDB](#使用-yaml-文件部署-kwdb)。
  - 使用 `docker run` 命令行部署，支持安全和非安全部署模式，更多信息，参见[执行 Docker Run 命令部署 KWDB](#执行-docker-run-命令部署-kwdb)。

::: warning 说明

KWDB 支持基于 DRBD 块设备复制的开源软件方案，实现主备节点间的数据复制，如需实现单机高可用性，请先参阅[单机高可用性方案](../../best-practices/single-ha.md)。

:::

## 部署准备

### 硬件

下表列出部署 KWDB 所需的硬件规格。

| 项目       | 要求                                                         |
| ---------- | ------------------------------------------------------------ |
| CPU 和内存 | 单节点配置建议不低于 4 核 8G。对于数据量大、复杂的工作负载、高并发和高性能场景，建议配置更高的 CPU 和内存资源以确保系统的高效运行。 |
| 磁盘       | - 推荐使用 SSD 或者 NVMe 设备，尽量避免使用 NFS、CIFS、CEPH 等共享存储。<br > - 磁盘必须能够实现 500 IOPS 和 30 MB/s 处理效率。 <br>- 使用 HDD 硬盘部署单机版本时，避免设备数过多或每秒写入测点数过高，否则数据写入性能将显著下降。<br> - KWDB 系统自身启动不会占用过多磁盘容量（低于 1G）。实际所需磁盘大小主要取决于用户的业务量。 |
| 文件系统   | 建议使用 ext4 文件系统。                                     |

### 操作系统

:::warning 说明

- 如果目标机器尚未安装 Docker，请提前安装适合您操作系统的 Docker 容器。更多信息，参见 [Docker 安装文档](https://docs.docker.com/desktop/install/linux-install/)。
- 如果目标机器无法联网且未安装 Docker，请采用二进制包安装 Docker。更多信息，参见 [Docker 安装文档](https://docs.docker.com/engine/install/binaries/)和[安装后说明](https://docs.docker.com/engine/install/linux-postinstall/)。
- 未提及的操作系统版本**也许可以**运行 KWDB，但尚未得到 KWDB 官方支持。

:::

KWDB 支持在以下已安装 Docker 的操作系统中进行容器部署。

| **操作系统** | **版本**   | **ARM_64** | **x86_64** |
| :----------- | :--------- | :--------- | :--------- |
| Anolis       | 7        | ✓          | ✓          |
|              | 8       | ✓          | ✓          |
| CentOS       | 7          |            | ✓          |
|              | 8          |            | ✓          |
| Debian       | V11        | ✓          |            |
| KylinOS      | V10 SP2    | ✓          | ✓          |
|              | V10 SP3 2403    | ✓          | ✓          |
| openEuler    | 24.03      |            | ✓          |
| Ubuntu       | V20.04     | ✓          | ✓          |
|              | V22.04     | ✓          | ✓          |
|              | V24.04     | ✓          | ✓          |
| UOS          | 1050e      | ✓           | ✓          |
|              | 1060e      | ✓          | ✓          |
|              | 1070e      | ✓          | ✓          |
| Windows Server  | WSL2     |           | ✓          |

### 软件依赖（可选）

如采用部署脚本或 YAML 文件部署 KWDB, 目标机器需已安装 Docker Compose（1.20.0 及以上版本）。

- 在线安装 Docker Compose，参见 [Docker 官方文档](https://docs.docker.com/compose/install/)。
- 离线安装 Docker Compose，参见 [Docker 官方文档](https://docs.docker.com/compose/install/standalone/)。

```shell
sudo apt-get install docker-compose
```

### 端口要求

下表列出 KWDB 服务默认使用的端口。在安装部署前，确保目标机器的以下端口没有被占用且没有被防火墙拦截。如需使用其他端口，可在安装部署过程中进行修改。

| 端口号 | 说明    |
| ------------------------------------- | ------------------------------------------ |
| `8080`                                | 数据库 Web 服务端口                        |
| `26257`                               | 数据库服务端口、节点监听端口和对外连接端口 |

### 安装包和镜像

根据需要使用预编译安装包或容器镜像。

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
| `packages` 目录   | 存放镜像包。                                      |
| `utils` 目录      | 存放工具类脚本。                                             |

#### 获取容器镜像

KWDB 支持通过以下方式获取容器镜像：

- [安装包](https://gitee.com/kwdb/kwdb/releases)：下载系统环境对应的安装包，解压后在 `kwdb_install/packages` 目录下导入 `KaiwuDB.tar` 文件。

    ```bash
    docker load < KaiwuDB.tar
    Loaded image: "image-name"
    ```

- Docker 命令：执行 `docker pull kwdb/kwdb:<version>` 获取镜像。

## 部署 KWDB

### 使用脚本部署 KWDB

使用脚本部署 KWDB 时，系统将对配置文件、运行环境、硬件配置和软件依赖进行检查。如果相应硬件未能满足要求，系统将继续安装，并提示硬件规格不满足要求。如果软件依赖未能满足要求，系统将中止安装，并提供相应的提示信息。

在部署过程中，系统会自动生成相关日志。如果部署时出现错误，用户可以通过查看终端输出或 KWDB 安装目录中 `log` 目录里的日志文件，获取详细的错误信息。

部署完成后，系统生成 `/etc/kaiwudb/` 目录。Docker Compose 配置文件 `docker-compose.yml` 位于 `/etc/kaiwudb/script` 目录下。部署完成后，用户可以修改 Docker Compose 配置文件 `docker-compose.yml`，配置 KWDB 的启动参数和 CPU 资源占用率。有关定制化部署配置的详细信息，参见[配置集群](../../deployment/cluster-config/cluster-config-docker.md)。

**前提条件**：

- 已获取 [KWDB 容器安装包](#获取容器安装包)。
- 待部署节点的硬件、操作系统、软件依赖和端口满足安装部署要求。
- 安装用户为 root 用户或者拥有 `sudo` 权限的普通用户。
  - root 用户和配置 `sudo` 免密的普通用户在执行部署脚本时无需输入密码。
  - 未配置 `sudo` 免密的普通用户在执行部署脚本时，需要输入密码进行提权。
- 安装用户为非 root 用户时，需要通过 `sudo usermod -aG docker $USER` 命令将用户添加到 `docker` 组。

**步骤**：

如需使用脚本部署 KWDB，遵循以下步骤。

1. 登录待部署节点，编辑安装包目录下的 `deploy.cfg` 配置文件，设置安全模式、管理用户、服务端口等信息。

    ::: warning 说明
    默认情况下，`deploy.cfg` 配置文件中包含集群和主备集群地址配置参数。请删除或注释 `[cluster]` 和 `[additional]` 配置项。
    :::

    配置文件示例：

    ```yaml
    [global]
    # Whether to turn on secure mode
    secure_mode=tls
    # Management KaiwuDB user
    management_user=kaiwudb
    # KaiwuDB cluster http port
    rest_port=8080
    # KaiwuDB service port
    kaiwudb_port=26257
    # KaiwuDB brpc port
    brpc_port=27257
    # KaiwuDB data directory
    data_root=/var/lib/kaiwudb
    # CPU usage[0-1]
    # cpu=1

    [local]
    # local node configuration
    node_addr=127.0.0.1

    # [cluster]
    # remote node addr,split by ','
    # node_addr=127.0.0.2
    # ssh info
    # ssh_port=22
    # ssh_user=admin

    # [additional]
    # IPs=127.0.0.3,127.0.0.4
    ```

    参数说明：

    - `global`：全局配置
      - `secure_mode`：是否开启安全模式，支持以下两种取值：
        - `insecure`：使用非安全模式。
        - `tls`：（默认选项）开启 TLS 安全模式。开启安全模式后，KWDB 生成 TLS 证书，作为客户端或应用程序连接数据库的凭证。生成的客户端相关证书存放在 `/etc/kaiwudb/certs` 目录。
      - `management_user`：KWDB 的管理用户，默认为 `kaiwudb`。安装部署后，KWDB 创建相应的管理用户以及和管理用户同名的用户组。
      - `rest_port`：KWDB Web 服务端口，默认为 `8080`。
      - `kaiwudb_port`：KWDB 服务端口，默认为 `26257`。
      - `brpc_port`：KWDB 时序引擎间的 brpc 通信端口，用于节点间通信。单节点部署时系统会自动忽略该设置。
      - `data_root`：数据目录，默认为 `/var/lib/kaiwudb`。
      - `cpu`：可选参数，用于指定 KWDB 服务占用当前节点服务器 CPU 资源的比例，默认无限制。取值范围为 `[0,1]`，最大精度为小数点后两位。
    - `local`：本地节点配置
      - `node_addr`：本地节点对外提供服务的 IP 地址，监听地址为 `0.0.0.0`，端口为 KWDB 服务端口。

2. 执行单机部署安装命令。

    ```shell
    ./deploy.sh install --single
    ```

3. 检查配置无误后输入 `Y` 或 `y`，如需返回修改 `deploy.cfg` 配置文件，输入 `N` 或 `n`。

    ```shell
    ================= KaiwuDB Basic Info =================
    Deploy Mode: container
    Start Mode: single
    RESTful Port: 8080
    KaiwuDB Port: 26257
    BRPC Port: 27257
    Data Root: /var/lib/kaiwudb
    Secure Mode: tls
    CPU Usage Limit: unlimited
    Local Node Address: 127.0.0.1
    ======================================================
    Please confirm the installation information above(Y/n):
    ```

    执行成功后，控制台输出以下信息：

    ```shell
    [INSTALL COMPLETED]:KaiwuDB has been installed successfully! ...
    ```

4. 启动 KWDB 节点。

    ```shell
    ./deploy.sh start
    ```

    执行成功后，控制台输出以下信息：

    ```shell
    [START COMPLETED]:KaiwuDB start successfully.
    ```

5. 使用以下任一方式查看节点状态：

    - 在当前目录使用部署脚本

        ```shell
        ./deploy.sh status
        ```

    - 在任一目录下使用 `systemctl` 命令

        ```shell
        systemctl status kaiwudb
        ```

    - 在任一目录下使用便捷脚本（推荐）

        ```shell
        kw-status
        ```

6. （可选）配置 KWDB 开机自启动。

    配置 KWDB 开机自启动后，如果系统重启，则自动启动 KaiwuDB。

    ```shell
    systemctl enable kaiwudb
    ```

7. （可选）执行 `add_user.sh` 脚本创建数据库用户。如果跳过该步骤，系统将默认使用部署数据库时使用的用户，且无需密码访问数据库。

    ```shell
    ./add_user.sh
    Please enter the username: 
    Please enter the password:
    ```

    执行成功后，控制台输出以下信息：

    ```shell
    [ADD USER COMPLETED]:User creation completed.
    ```
  
8. 执行 `kw-sql` 使用 `root` 用户登录数据库或使用 [kwbase CLI 工具登录数据库](../access-kaiwudb/access-kaiwudb-cli.md)。

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
      kwdb-container:
        image: "kwdb/kwdb:3.0.0"
        container_name: kaiwudb-experience
        hostname: kaiwudb-experience
        ports:
          - 8080:8080
          - 26257:26257
        ulimits:
          memlock: -1
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

### 执行 Docker Run 命令部署 KWDB

**前提条件**：

- 已获取 [KWDB 容器镜像](#获取容器镜像)。
- 待部署节点的硬件、操作系统、软件依赖和端口满足安装部署要求。
- 安装用户为 root 用户或者拥有 `sudo` 权限的普通用户。
  - root 用户和配置 `sudo` 免密的普通用户在执行部署脚本时无需输入密码。
  - 未配置 `sudo` 免密的普通用户在执行部署脚本时，需要输入密码进行提权。
- 安装用户为非 root 用户时，需要通过 `sudo usermod -aG docker $USER` 命令将用户添加到 `docker` 组。

**步骤**：

1. （可选）如需以安全模式部署 KWDB, 使用以下命令创建数据库证书颁发机构、数据库部署用户的客户端证书以及节点服务器证书。

      ```shell
      docker run --rm --privileged \
        -v /etc/kaiwudb/certs:<certs_dir> \
        -w /kaiwudb/bin \
        <kwdb_image> \
        bash -c './kwbase cert create-ca --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key && \
                  ./kwbase cert create-client root --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key && \
                  ./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key'
      ```

    参数说明：
    - `--rm`：容器停止后自动删除。
    - `--privileged`：给予容器扩展权限。
    - `-v`：设置容器目录映射, 将主机的 `/etc/kaiwudb/certs` 目录挂载到容器内的 `<certs_dir>` 目录，用于存放证书和密钥。
    - `-w /kaiwudb/bin`：将容器内的工作目录设置为 `/kaiwudb/bin`。
    - `kwdb_image`：容器镜像，需填入实际的镜像名以及标签, 例如 `kwdb:3.0.0`。
    - `bash -c`：在容器中执行后面的证书创建命令, 其中：
      - `./kwbase cert create-ca`：创建证书颁发机构(CA)，生成 CA 证书和密钥。
      - `./kwbase cert create-client root`：为 `root` 用户创建客户端证书和密钥。
      - `./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0`：创建节点证书和密钥，支持通过三种网络标识符访问：本地回环地址 (`127.0.0.1`)、本地主机名 (`localhost`) 和所有网络接口 (`0.0.0.0`)。
      - 所有命令均使用 `--certs-dir=<certs_dir>` 指定证书存储目录，使用 `--ca-key=<certs_dir>/ca.key` 指定密钥路径。

2. 启动基于 Docker 的 KWDB 数据库节点。

    - 非安全模式

      ```shell
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

    - 安全模式

        ```bash
      docker run -d --privileged --name kwdb \
        --ulimit memlock=-1 \
        --ulimit nofile=$max_files \
        -p $db_port:26257 \
        -p $http_port:8080 \
        -v /etc/kaiwudb/certs:<certs_dir> \
        -v /var/lib/kaiwudb:/kaiwudb/deploy/kwdb-container \
        --ipc shareable \
        -w /kaiwudb/bin \
        <kwdb_image> \
        ./kwbase start-single-node \
          --certs-dir=<certs_dir> \
          --listen-addr=0.0.0.0:26257 \
          --http-addr=0.0.0.0:8080 \
          --store=/kaiwudb/deploy/kwdb-container
      ```

    参数说明：
    - `-d`：后台运行容器并返回容器 ID。
    - `--name kwdb`：指定容器名称为 `kwdb`，便于后续管理。
    - `--privileged`：给予容器扩展权限。
    - `--ulimit memlock=-1`：取消容器内存大小限制。
    - `--ulimit nofile=$max_files`：设置容器内进程可以打开的最大文件数。
    - `-p $db_port:26257`：将容器的 26257 端口(数据库主端口)映射到主机的指定端口。
    - `-p $http_port:8080`：将容器的 8080 端口(HTTP 端口)映射到主机的指定端口。
    - `-v`：将主机的 `/var/lib/kaiwudb` 目录挂载到容器内的 `/kaiwudb/deploy/kwdb-container` 目录，用于持久化数据存储。安全模式下，将主机的 `/etc/kaiwudb/certs` 目录挂载到容器内的 `<certs_dir>` 目录，用于存放证书和密钥。
    - `--ipc shareable`：允许其他容器共享此容器的IPC命名空间。
    - `-w /kaiwudb/bin`：将容器内的工作目录设置为 `/kaiwudb/bin`。
    - `kwdb_image`：容器镜像变量，需替换为实际的镜像名称及标签, 例如 `kwdb:3.0.0`。
    - `./kwbase start`：容器内运行的数据库启动命令, 根据安全模式和非安全模式有所不同:
      - `--insecure`：（仅非安全模式）指定以非安全模式运行。
      - `--certs-dir=<certs_dir>`：（安全模式）指定证书目录位置。
      - `--listen-addr=0.0.0.0:26257`：指定数据库监听的地址和端口。
      - `--http-addr=0.0.0.0:8080`：指定HTTP接口监听的地址和端口。
      - `--store=/kaiwudb/deploy/kwdb-container`：指定数据存储位置。

3. （可选）创建数据库用户并授予用户管理员权限。如果跳过该步骤，系统将默认使用部署数据库时的用户，且无需密码访问数据库。

    - 非安全模式（不带密码）：

        ```bash
        docker exec kwdb bash -c "./kwbase sql --insecure --host=<host_ip> -e \"create user <username>;grant admin to <username> with admin option;\""
        ```

    - 安全模式（带密码）：

        ```bash
        docker exec kwdb bash -c "./kwbase sql --host=<host_ip> --certs-dir=<cert_dir> -e \"create user <username> with password \\\"<user_password>\\\";grant admin to <username> with admin option;\""
        ```