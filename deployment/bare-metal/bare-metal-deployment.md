---
title: 裸机部署
id: bare-metal-deployment
---

# 裸机部署

## 前提条件

- 待部署节点的硬件、操作系统、软件依赖和端口满足安装部署要求。
- 各节点间网络联通，节点所在机器位于同一机房内。物理机器间网络延迟不高于 50 ms，时钟相差不大于 500 ms。
- 已配置当前部署节点与集群内其他节点的 SSH 免密。
- 安装用户为 root 用户或者拥有 `sudo` 权限的普通用户。
  - root 用户和配置 `sudo` 免密的普通用户在执行部署脚本时无需输入密码。
  - 未配置 `sudo` 免密的普通用户在执行部署脚本时，需要输入密码进行提权。

## 部署步骤

1. 登录待部署节点，编辑安装包目录下的 `deploy.cfg` 配置文件，设置安全模式、管理用户、服务端口等信息，并添加其他节点信息。

    配置文件示例：

    ```yaml
    [global]
    secure_mode=tls
    management_user=kaiwudb
    rest_port=8080
    kaiwudb_port=26257
    data_root=/var/lib/kaiwudb

    [local]
    node_addr= local_node_ip

    [cluster]
    node_addr= cluster_node_ips
    ssh_port=22
    ssh_user=admin
    ```

    配置参数说明：

    - `global`：全局配置
        - `secure_mode`：是否开启安全模式，支持以下两种设置：
            - `insecure`：使用非安全模式。
            - `tls`：（默认选项）开启 TLS 安全模式。开启安全模式后，KWDB 生成 TLS 证书，作为客户端或应用程序连接数据库的凭证。生成的客户端相关证书存放在 `/etc/kaiwudb/certs` 目录。
        - `management_user`：KWDB 的管理用户，默认为 `kaiwudb`。安装部署后，KWDB 创建相应的管理用户以及和管理用户同名的用户组。
        - `rest_port`：KWDB Web 服务端口，默认为 `8080`。
        - `kaiwudb_port`：KWDB 服务端口，默认为 `26257`。
        - `data_root`：数据目录，默认为 `/var/lib/kaiwudb`。
        - `cpu`: 可选参数，用于指定 KWDB 服务占用当前节点服务器 CPU 资源的比例，默认无限制。取值范围为 `[0,1]`，最大精度为小数点后两位。KWDB 支持调整 CPU 资源占用率。更多信息，参见[配置集群](./cluster-config-bare-metal.md)。**注意**：如果部署环境为 Ubuntu 18.04 版本，部署集群后，需要将 `kaiwudb.service` 文件中的 `CPUQuota` 修改为整型值，例如，将 `180.0%` 修改为 `180%`，以确保设置生效。具体操作步骤，参见[配置 CPU 资源占用率](./cluster-config-bare-metal.md#配置-cpu-资源占用率)。
    - `local`：本地节点配置
        - `local_node_ip`：本地节点对外提供服务的 IP 地址，监听地址为 `0.0.0.0`，端口为 KWDB 服务端口。
    - `cluster`：集群内其他节点的配置
        - `cluster_node_ips`：远程节点对外提供服务的 IP 地址。各节点的 IP 地址使用逗号（`,`）分割，远程节点数应不少于 2 个。
        - `ssh_port`：远程节点的 SSH 服务端口。各节点的 SSH 服务端口必须相同。
        - `ssh_user`：远程节点的 SSH 登录用户。各节点的 SSH 登录用户必须相同。

2. 为 `deploy.sh` 脚本增加运行权限。

    ```shell
    chmod +x ./deploy.sh
    ```

3. 执行安装命令。

   - 多副本集群

        ```shell
        ./deploy.sh install --multi-replica
        ```

   - 单副本集群

        ```shell
        ./deploy.sh install --single-replica
        ```

        执行成功后，控制台输出以下信息：

        ```shell
        INSTALL COMPLETED: KaiwuDB has been installed successfuly! ...
        ```

4. 根据系统提示重新加载 `systemd` 守护进程的配置文件。

    ```shell
    systemctl daemon-reload
    ```

5. 初始化并启动集群。

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

6. 查看集群节点状态。

    ```shell
    ./deploy.sh cluster -s
    ```

    或者

    ```shell
    ./deploy.sh cluster --status
    ```

    返回字段说明：

    | 字段         | 描述                                                                                                                                                                      |
    |--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | `id`           | 节点 ID。                                                                                                                                                                   |
    | `address`      | 节点地址。                                                                                                                                                                  |
    | `sql_address`  | SQL 地址。                                                                                                                                                                  |
    | `build`        | 节点的 KWDB 版本                                                                                                                                                       |
    | `started_at`   | 节点启动的日期和时间。                                                                                                                                                     |
    | `updated_at`   | 节点更新命令结果的日期和时间。节点正常时，每 10 秒左右记录一次新状态。节点不正常时，此命令的统计信息可能会较旧。                                                             |
    | `locality`     | 节点机器的地理位置，例如国家、数据中心或机架等。用户需要在启动节点指定节点机器的地理位置。                                                                                                            |
    | `start_mode`   | 节点启动模式。                                                                                                                                  |
    | `is_available`<br>`is_live` | 如果均为 `true`，表示节点为存活状态。<br>如果均为 `false`，表示节点为异常状态。                                                                                      |

7. （可选）配置 KWDB 开机自启动。

    配置 KWDB 开机自启动后，如果系统重启，则自动启动 KWDB。

    ```shell
    systemctl enable kaiwudb
    ```