---
title: 脚本部署
id: script-deployment
---

# 脚本部署

使用脚本部署集群时，系统将对配置文件、运行环境、硬件配置、软件依赖和 SSH 免密登录进行检查。

- 如果硬件配置未满足要求，系统将继续安装，并提示硬件规格不满足要求。
- 如果软件依赖未满足要求，系统会中止安装并提供相应的错误信息。

在部署过程中，系统会自动生成相关日志。如果部署时出现错误，用户可以通过查看终端输出或 KWDB 安装目录中 `log` 目录里的日志文件，获取详细的错误信息。

## 前提条件

- 已获取 [KWDB 安装包](https://gitee.com/kwdb/kwdb/releases)。
- 待部署节点的硬件、操作系统、软件依赖和端口满足安装部署要求。
- 各节点间网络联通，节点所在机器位于同一机房内。物理机器间网络延迟不高于 50 ms，时钟相差不大于 500 ms。
- 已配置当前节点与集群内其他节点的 SSH 免密。
- 安装用户为 root 用户或者拥有 `sudo` 权限的普通用户。
  - root 用户和配置 `sudo` 免密的普通用户在执行部署脚本时无需输入密码。
  - 未配置 `sudo` 免密的普通用户在执行部署脚本时，需要输入密码进行提权。
- 容器部署的安装用户为非 root 用户时，需要通过 `sudo usermod -aG docker $USER` 命令将用户添加到 `docker` 组。

## 步骤

1. 登录待部署节点，编辑安装包目录下的 `deploy.cfg` 配置文件，设置安全模式、管理用户、服务端口等信息，并添加其他节点信息。

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
    cpu=1

    [local]
    # local node configuration
    node_addr=192.168.122.221

    [cluster]
    # remote node addr,split by ','
    node_addr=192.168.122.222,192.168.122.223
    # ssh info
    ssh_port=22
    ssh_user=admin

    # [additional]
    # IPs=127.0.0.3,127.0.0.4
    ```

    配置参数说明：

    - `global`：全局配置
        - `secure_mode`：是否开启安全模式，支持以下两种取值：
            - `insecure`：使用非安全模式。
            - `tls`：（默认选项）开启 TLS 安全模式。开启安全模式后，KWDB 生成 TLS 证书，作为客户端或应用程序连接数据库的凭证。生成的客户端相关证书存放在 `/etc/kaiwudb/certs` 目录。
        - `management_user`：KWDB 的管理用户，默认为 `kaiwudb`。安装部署后，KWDB 创建相应的管理用户以及和管理用户同名的用户组。
        - `rest_port`：KWDB Web 服务端口，默认为 `8080`。
        - `kaiwudb_port`：KWDB 服务端口，默认为 `26257`。
        - `brpc_port`：KWDB 时序引擎间的 brpc 通信端口，用于节点间通信，默认为 `27257`。
        - `data_root`：数据目录，默认为 `/var/lib/kaiwudb`。
        - `cpu`：可选参数，用于指定 KWDB 服务占用当前节点服务器 CPU 资源的比例，默认无限制。取值范围为 `[0,1]`，最大精度为小数点后两位。KWDB 支持调整 CPU 资源占用率。更多信息，参见[配置裸机部署集群](../cluster-config/cluster-config-bare-metal.md)或[配置容器部署集群](../cluster-config/cluster-config-docker.md) 。**注意**：如果部署环境为 Ubuntu 18.04 版本，在裸机部署集群完成后，需要将 `kaiwudb.service` 文件中的 `CPUQuota` 修改为整型值，例如，将 `180.0%` 修改为 `180%`，以确保设置生效。具体操作步骤，参见[配置 CPU 资源占用率](../cluster-config/cluster-config-bare-metal.md#配置-cpu-资源占用率)。
    - `local`：本地节点配置
        - `local_node_ip`：本地节点对外提供服务的 IP 地址，监听地址为 `0.0.0.0`，端口为 KWDB 服务端口。
    - `cluster`：集群内其他节点的配置
        - `cluster_node_ips`：远程节点对外提供服务的 IP 地址。各节点的 IP 地址使用逗号（`,`）分割，远程节点数应不少于 2 个。
        - `ssh_port`：远程节点的 SSH 服务端口。各节点的 SSH 服务端口必须相同。
        - `ssh_user`：远程节点的 SSH 登录用户。各节点的 SSH 登录用户必须相同。
    - `additional`：主备集群 IP 地址配置。KWDB 暂不支持该功能。

2. 执行安装命令。

   - 多副本集群

        ```shell
        ./deploy.sh install --multi-replica
        ```

   - 单副本集群

        ```shell
        ./deploy.sh install --single-replica
        ```

3. 检查配置无误后输入 `Y` 或 `y`，如需返回修改 `deploy.cfg` 配置文件，输入 `N` 或 `n`。

    ```shell
    ================= KaiwuDB Basic Info =================
    Deploy Mode: bare-metal
    Management User: kaiwudb
    Start Mode: multi-replication
    RESTful Port: 8080
    KaiwuDB Port: 26257
    BRPC Port: 27257
    Data Root: /var/lib/kaiwudb
    Secure Mode: tls
    CPU Usage Limit: 1
    Local Node Address: 192.168.122.221
    ================= KaiwuDB Cluster Info =================
    Cluster Node Address: 192.168.122.222 192.168.122.223
    SSH User: admin
    SSH Port: 22
    =========================================================
    Please confirm the installation information above(Y/n):
    ```

    执行成功后，控制台输出以下信息：

      ```shell
      [INSTALL COMPLETED]:KaiwuDB has been installed successfully! ...
      ```

4. 初始化并启动集群。

    ::: warning 提示
    集群初始化和启动大约需要 10 秒左右时间。在此期间，如果有节点死亡，可能会导致集群无法触发高可用机制。
    :::
  
    ```shell
    ./deploy.sh cluster -i
    ```

    或者

    ```shell
    ./deploy.sh cluster --init
    ```

5. 使用以下任一方式查看集群节点状态：

    - 在当前目录使用部署脚本

      ```shell
      ./deploy.sh cluster -s
      # 或者
      ./deploy.sh cluster --status
      ```

    - 在任一目录下使用便捷脚本（推荐）

      ```shell
      kw-status
      ```

    返回字段说明：

    | 字段         | 描述                                                                                                                                                                      |
    |--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | `id`           | 节点 ID。                                                                                                                                                                   |
    | `address`      | 节点地址。                                                                                                                                                                  |
    | `sql_address`  | SQL 地址。                                                                                                                                                                  |
    | `build`        | 节点运行的 KWDB 版本                                                                                                                                                       |
    | `started_at`   | 节点启动的日期和时间。                                                                                                                                                     |
    | `updated_at`   | 节点状态更新的日期和时间。节点正常时，每 10 秒左右记录一次新的状态；节点异常时，更新信息可能会有所滞后。                                                           |
    | `locality`     | 节点 ID。                                                                                                            |
    | `start_mode`   | 节点的启动模式。                                                                                                                                  |
    | `is_available`<br>`is_live` | 如果均为 `true`，表示节点处于正常状态。<br>如果均为 `false`，表示节点处于异常状态。                                                                                     |

6. （可选）配置 KWDB 开机自启动。

    配置 KWDB 开机自启动后，如果系统重启，则自动启动 KWDB。

    ::: warning 说明
    系统重启后，如果当前节点与其它节点时钟相差大于 500 ms，可能会导致 KWDB 自启动失败。用户需要先进行时钟同步，再手动启动 KWDB。
    :::

    ```shell
    systemctl enable kaiwudb
    ```