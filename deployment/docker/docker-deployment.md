---
title: 容器部署
id: docker-deployment
---

# 容器部署

部署 KWDB 集群时，系统将对配置文件、运行环境、硬件配置、软件依赖和 SSH 免密登录进行检查。如果相应硬件未能满足要求，系统将继续安装，并提示硬件规格不满足要求。如果软件依赖未能满足要求，系统将中止安装，并提供相应的提示信息。

在部署过程中，系统会自动生成相关日志。如果部署时出现错误，用户可以通过查看终端输出或 KWDB 安装目录中 `log` 目录里的日志文件，获取详细的错误信息。

部署完成后，系统将生成 `/etc/kaiwudb/` 目录。Docker Compose 配置文件 `docker-compose.yml` 位于 `/etc/kaiwudb/script` 目录下。部署完成后，用户可以修改 Docker Compose 配置文件 `docker-compose.yml`，配置 KWDB 的启动参数和 CPU 资源占用率。有关定制化部署配置的详细信息，参见[配置集群](./cluster-config-docker.md)。

## 前提条件

- [联系](https://cs.kaiwudb.com/support/) KWDB 技术支持人员，获取 KWDB 容器镜像。
- 待部署节点的硬件、操作系统、软件依赖和端口满足安装部署要求。
- 各节点间网络联通，且已配置当前节点与集群内其他节点的 SSH 免密。
- 当前节点与集群内所有节点的时钟相差不大于 500 ms。
- 安装用户为 root 用户或者拥有 `sudo` 权限的普通用户。
  - root 用户和配置 `sudo` 免密的普通用户在执行部署脚本时无需输入密码。
  - 未配置 `sudo` 免密的普通用户在执行部署脚本时，需要输入密码进行提权。
- 安装用户为非 root 用户时，需要通过 `sudo usermod -aG docker $USER` 命令将用户添加到 `docker` 组。

## 部署步骤

1. 登录待部署节点，编辑安装包目录下的 `deploy.cfg` 配置文件，设置安全模式、管理用户、服务端口等信息，并添加其他节点信息。

    配置文件示例：

    ```yaml
    [global]
    secure_mode=y
    management_user=kaiwudb
    rest_port=8080
    kaiwudb_port=26257
    data_root=/var/lib/kaiwudb
    cpu=1

    [local]
    node_addr=192.168.64.128

    [cluster]
    node_addr=192.168.64.129, 192.168.64.130
    ssh_port=22
    ssh_user=admin
    ```

    配置参数说明：

    - `global`：全局配置
        - `secure_mode`：是否开启安全模式，默认开启安全模式。开启安全模式后，KWDB 生成 TLS 安全证书，作为客户端或应用程序连接数据库的凭证。生成的客户端相关证书存放在 `/etc/kaiwudb/certs` 目录。
        - `management_user`：KWDB 的管理用户，默认为 `kaiwudb`。安装部署后，KWDB 创建相应的管理用户以及和管理用户同名的用户组。
        - `rest_port`：KWDB Web 服务端口，默认为 `8080`。
        - `kaiwudb_port`：KWDB 服务端口，默认为 `26257`。
        - `data_root`：数据目录，默认为 `/var/lib/kaiwudb`。
        - `cpu`: 可选参数，用于指定 KWDB 服务占用当前节点服务器 CPU 资源的比例，默认无限制。取值范围为 `[0,1]`，最大精度为小数点后两位。KWDB 支持调整 CPU 资源占用率。更多信息，参见[集群配置](./cluster-config-docker.md)。
    - `local`：本地节点配置
        - `node_addr`：本地节点对外提供服务的 IP 地址，监听地址为 `0.0.0.0`，端口为 KWDB 服务端口。
    - `cluster`：集群内其他节点的配置
        - `node_addr`：远程节点对外提供服务的 IP 地址。各节点的 IP 地址使用逗号（`,`）分割。
        - `ssh_port`：远程节点的 SSH 服务端口。各节点的 SSH 服务端口必须相同。
        - `ssh_user`：远程节点的 SSH 登录用户。各节点的 SSH 登录用户必须相同。

2. 为 `deploy.sh` 脚本增加运行权限。

    ```shell
    chmod +x ./deploy.sh
    ```

3. 执行安装命令。

    ```shell
    ./deploy.sh install --multi-replica
    ```

    执行成功后，控制台输出以下信息：

    ```shell
    INSTALL COMPLETED: KaiwuDB has been installed successfuly! ...
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

5. 查看集群节点状态。

    ```shell
    ./deploy.sh cluster -s
    ```

    或者

    ```shell
    ./deploy.sh cluster --status
    ```

    执行成功后，控制台输出以下信息：

    ```shell
      id |       address       |     sql_address     | build |           started_at            |            updated_at            | locality |    start_mode     | is_available | is_live  | status
    -----+---------------------+---------------------+-------+---------------------------------+----------------------------------+----------+-------------------+--------------+----------+-------
      1 | 10.110.10.153:26257 | 10.110.10.153:26257 | 2.0.3 | 2024-01-31 08:07:54.76191+00:00 | 2024-02-02 06:22:09.792831+00:00 |          | start-single-node | true         | true     | healthy
    (1 row)
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
    | `is_available` | 如果为 `true`，当前节点可用。                                                                                                                                             |
    | `is_live`      | 如果为 `true`，当前节点处于活跃状态。 |
    | `status`       | 当前节点的状态。                                                                                                                                                              |

6. （可选）配置 KWDB 开机自启动。

    配置 KWDB 开机自启动后，如果系统重启，则自动启动 KWDB。

    ::: warning 说明
    系统重启后，如果当前节点与其它节点时钟相差大于 500 ms，可能会导致 KWDB 自启动失败。用户需要先进行时钟同步，再手动启动 KWDB。
    :::

    ```shell
    systemctl enable kaiwudb
    ```
