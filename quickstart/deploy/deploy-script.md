---
title: 脚本部署
id: quickstart-script
---

# 脚本部署

使用脚本部署 KWDB 时，系统将对配置文件、运行环境、硬件配置和软件依赖进行检查：
- 如果硬件配置未满足要求，系统将继续安装，并提示硬件规格不满足要求。
- 如果软件依赖未满足要求，系统会中止安装并提供相应的错误信息。

在部署过程中，系统会自动生成相关日志。如果部署时出现错误，用户可以通过查看终端输出或 KWDB 安装目录中 `log` 目录里的日志文件，获取详细的错误信息。

裸机脚本部署完成后，系统会将 KWDB 封装成系统服务（名称为 `kaiwudb`），并生成以下文件：

- `kaiwudb.service`：配置 KWDB 的 CPU 资源占用率。
- `kaiwudb_env`：配置 KWDB 启动参数。

容器脚本部署完成后，系统会生成 Docker Compose 配置文件 `docker-compose.yml`，用于配置 KWDB 的启动参数和 CPU 资源占用率。

具体配置步骤，参见[集群参数配置](../../db-operation/cluster-settings-config.md)。

## 前提条件

- 已获取 KWDB [安装包](../prepare.md#安装包)。
- 待部署节点的硬件、操作系统、软件依赖和端口满足[安装部署要求](../prepare.md)。
- 安装用户为 root 用户或者拥有 `sudo` 权限的普通用户。
  - root 用户和配置 `sudo` 免密的普通用户在执行部署脚本时无需输入密码。
  - 未配置 `sudo` 免密的普通用户在执行部署脚本时，需要输入密码进行提权。
- 容器部署且安装用户为非 root 用户时，需要通过 `sudo usermod -aG docker $USER` 命令将用户添加到 `docker` 组。

## 步骤

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

    | 层级 | 参数 | 描述 |
    |---|---|---|
    | **global** <br>(全局配置) | `secure_mode` | 是否开启安全模式，支持以下三种取值：<br>- `insecure`：使用非安全模式。<br>- `tls`：（默认选项）开启 TLS 安全模式。开启后，KWDB 生成相应的 TLS 证书，作为客户端或应用程序连接数据库的凭证。生成的客户端相关证书存放在 `/etc/kaiwudb/certs` 目录。 |
    | | `management_user` | KWDB 的管理用户，默认为 `kaiwudb`。安装部署后，KWDB 创建相应的管理用户以及和管理用户同名的用户组。 |
    | | `rest_port` | KWDB Web 服务端口，默认为 `8080`。 |
    | | `kaiwudb_port` | KWDB 服务端口，默认为 `26257`。 |
    | | `brpc_port` | KWDB 时序引擎间的 brpc 通信端口，用于节点间通信。单节点部署时系统会自动忽略该设置。 |
    | | `data_root` | 数据目录，默认为 `/var/lib/kaiwudb`。 |
    | | `cpu` | 可选参数，用于指定 KWDB 服务占用当前节点服务器 CPU 资源的比例，默认无限制。取值范围为 `[0,1]`，最大精度为小数点后两位。<br>**注意**：如果部署环境为 Ubuntu 18.04 版本，部署完成后，需要将 `kaiwudb.service` 文件中的 `CPUQuota` 修改为整型值，例如，将 `180.0%` 修改为 `180%`，以确保设置生效。具体操作步骤，参见[配置 CPU 资源占用率](../../db-operation/cluster-settings-config.md)。 |
    | **local** <br>(本地节点配置) | `node_addr` | 本地节点对外提供服务的 IP 地址，监听地址为 `0.0.0.0`，端口为 KWDB 服务端口。 |

2. 执行单机部署安装命令。

    ```shell
    ./deploy.sh install --single
    ```

3. 检查配置无误后输入 `Y` 或 `y`，如需返回修改 `deploy.cfg` 配置文件，输入 `N` 或 `n`。

    ```shell
    ================= KaiwuDB Basic Info =================
    Deploy Mode: bare-metal
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

    配置 KWDB 开机自启动后，如果系统重启，则自动启动 KWDB。

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

8. 通过 [kwbase CLI ](../access/access-cli.md) 、[KaiwuDB JDBC](../access/access-jdbc.md)或 [KaiwuDB 开发者中心](../access/access-kdc.md)连接并管理 KWDB。
