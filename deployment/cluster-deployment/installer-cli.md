---
title: 命令行模式部署
id: installer-cli
---

# 命令行模式部署

命令行模式通过文本菜单逐步引导完成安装，支持数字输入进行选择操作，无需额外依赖，适用于无图形化环境。

安装过程中内置参数实时校验，配置有误时自动提示重新输入，支持安全模式与非安全模式，部署完成后可选择立即启动数据库。

::: warning

命令行模式不支持在一台机器上部署多个节点。

:::

## 前提条件

**系统要求**：

- 所有待部署节点的硬件、操作系统和软件依赖满足[部署准备](../cluster-prepare.md)要求。
- 网络设置：
  - 各节点间网络联通。
  - 节点所在机器位于同一机房内。
  - 物理机器间网络延迟不高于 50 ms。
  - 各节点时钟相差不大于 500 ms。
  - 各节点已预留 KWDB 服务所需端口。
- 已获取 KWDB 安装程序（`.run` 文件）。

**用户权限要求**：

- 安装用户为 `root` 用户或已配置 `sudo` 免密的普通用户。
- 使用容器安装程序部署时，如果安装用户为非 `root` 用户，需要通过以下命令将用户添加到 `docker` 组：

  ```bash
  sudo usermod -aG docker $USER
  ```

## 步骤

1. 登录待部署节点，将 `.run` 安装程序复制到安装目录，并赋予执行权限：

    ```bash
    chmod +x KWDB-*.run
    ```

2. 执行以下命令，以命令行模式启动安装程序：

    ```bash
    ./KWDB-*.run -c
    # 或者
    ./KWDB-*.run --cli
    ```

3. 安装程序启动后，进入主功能菜单，输入 `1` 选择安装 KWDB：

    ```plain
    1. 安装 KWDB
    2. 卸载 KWDB
    3. 安装 KWDB 并加入集群
    4. 升级节点
    5. 退出

    请输入操作 [1-5]:
    ```

4. 根据实际业务需求，输入对应数字选择单副本或三副本集群：

    ```plain
    1. 单机安装
    2. 单副本集群
    3. 三副本集群
    4. 返回主菜单
    
    请选择 [1-4]:
    ```

5. 输入待安装的节点数量，例如输入 `3` 表示安装三个节点。

6. 安装程序自动生成配置文件模板并打开编辑器。根据实际环境修改各参数，保存并退出后，安装程序将自动开始安装。

    配置文件示例（以三节点为例）：

    ```ini
    [global]
    # 是否开启安全模式
    secure_mode=tls
    # adminui 端口
    rest_port=8080
    # 数据库服务端口
    kaiwudb_port=26257
    # 数据传输端口
    brpc_port=27257
    # 数据目录
    data_root=/var/lib/kaiwudb
    [node1]
    host=192.168.122.237
    # ssh 连接端口
    port=22
    # ssh 连接用户
    user=admin
    # ssh 连接密码
    passwd=******
    [node2]
    host=192.168.122.79
    # ssh 连接端口
    port=22
    # ssh 连接用户
    user=admin
    # ssh 连接密码
    passwd=******
    [node3]
    host=192.168.122.169
    # ssh 连接端口
    port=22
    # ssh 连接用户
    user=admin
    # ssh 连接密码
    passwd=******
    ```

    参数说明：

    | 参数 | 说明 |
    |------|------|
    | `secure_mode` | 安全模式，支持以下取值：<br>- `insecure`：非安全模式。<br>- `tls`：（默认）TLS 安全模式。开启安全模式后，KWDB 自动生成相应证书，存放于 `/etc/kaiwudb/certs` 目录。 |
    | `rest_port` | KWDB Web 服务端口，默认为 `8080`。 |
    | `kaiwudb_port` | KWDB 服务端口，默认为 `26257`。 |
    | `brpc_port` | 时序引擎间的数据传输端口，用于节点间通信，默认为 `27257`。 |
    | `data_root` | 数据目录，默认为 `/var/lib/kaiwudb`。 |
    | `host` | 节点 IP 地址，需确保各节点间网络可达。 |
    | `port` | 远程节点的 SSH 服务端口。各节点的 SSH 服务端口必须相同。 |
    | `user` | 远程节点的 SSH 登录用户。各节点的 SSH 登录用户必须相同。 |
    | `passwd` | 远程节点的 SSH 登录密码。各节点的 SSH 登录密码必须相同。 |

7. 选择是否为所有用户安装 KWDB：

    ```plain
    是否为所有用户安装：(y/N)
    ```

8. 安装过程中终端会实时显示安装进度。出现错误时，可以通过查看安装目录 `log` 目录下的日志文件获取详细信息。

9. 所有节点部署完成后，根据提示选择是否初始化集群：

    ```plain
    是否初始化集群：(y/N)
    ```

    - 输入 `y`：系统自动初始化 KWDB 集群。
    - 输入 `N`：跳过初始化，后续需手动初始化集群：

        ```bash
        systemctl start kaiwudb
        ```

        :::warning 提示
        多副本集群初始化和启动大约需要 10 秒左右时间。在此期间，如果有节点死亡，可能会导致集群无法触发高可用机制。
        :::

10. 在主功能菜单，输入 `5` 退出部署流程。

11. 使用以下任一方式查看服务或集群状态：

    ```bash
    # 查看服务状态
    systemctl status kaiwudb

    # 查看集群状态
    kw-status
    ```

    集群状态返回字段说明：

    | 字段 | 描述 |
    |------|------|
    | `id` | 节点 ID。 |
    | `address` | 节点地址。 |
    | `sql_address` | SQL 地址。 |
    | `build` | 节点运行的 KWDB 版本。 |
    | `started_at` | 节点启动的日期和时间。 |
    | `updated_at` | 节点状态更新的日期和时间。节点正常时，每 10 秒左右记录一次新状态；节点异常时，更新信息可能会有所滞后。 |
    | `locality` | 节点 ID。 |
    | `start_mode` | 节点启动模式。 |
    | `is_available` / `is_live` | 均为 `true` 表示节点处于正常状态；均为 `false` 表示节点处于异常状态。 |

12. （可选）配置 KWDB 开机自启动。

    ```bash
    systemctl enable kaiwudb
    ```

    :::warning 说明
    系统重启后，如果当前节点与其他节点时钟相差大于 500 ms，可能导致 KWDB 自启动失败。需先完成时钟同步，再手动启动 KWDB。
    :::

13. 执行 `kw-sql` 使用数据库部署用户登录数据库或者通过以下任一方式连接和管理 KWDB:
    - [kwbase CLI](../../quickstart/access/access-cli.md)
    - [KWDB 支持的连接器](../../development/overview.md)
    - [KaiwuDB 开发者中心](../../kaiwudb-tools/kaiwudb-developer-center/overview.md)