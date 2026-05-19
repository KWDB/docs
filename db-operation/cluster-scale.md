---
title: 集群扩缩容
id: cluster-scale
---

# 集群扩缩容

KWDB 支持集群的动态扩容和缩容操作，以满足不同业务场景下的容量和性能需求。不同集群类型的扩缩容特性如下：

| 集群类型 | 扩容 | 缩容 | 数据重分布机制 | 操作方式 |
|---------|------|------|--------------|---------| 
| 多副本集群 | 支持 | 支持 | 自动触发，平衡所有节点数据 | 安装程序 / 命令行 |
| 单副本集群 | 支持 | 不支持 | 仅对新建表生效，已有数据不迁移 | 安装程序 / 命令行 |

::: warning 说明

- **许可证限制**：集群节点数必须在许可证允许的范围内。超出限制时，扩容操作将被拒绝。
- **DDL 操作**：扩缩容期间，时序索引相关的 DDL 操作（如 `CREATE INDEX`、`DROP INDEX`）可能返回超时错误，操作完成后重试即可。
- **磁盘容量**：扩缩容期间，因数据迁移需要，集群磁盘使用量可能临时增加。操作完成后将恢复正常水平。
- **操作建议**：建议在业务低峰期执行扩缩容操作，以降低对业务的影响。

:::

## 集群扩容

### 多副本集群扩容

KWDB 多副本集群支持安装程序和命令行两种扩容方式。扩容完成后，集群会自动进行数据重分布，确保负载均衡。

**数据重分布**

扩容完成后，系统默认自动将现有数据均匀分布到所有节点。如需关闭自动重分布功能，可设置以下参数：

```sql
SET CLUSTER SETTING kv.allocator.ts_consider_rebalance.enabled = false;
```

重分布期间建议避免频繁执行 `ALTER` 语句，以免延长数据重分布时间。

#### 前提条件

- 待扩容节点未安装 KWDB。
- 目标集群处于运行状态。
- 当前节点数未达到许可证上限。
- 安装程序扩容方式还需满足以下条件：
  - 已获取 KWDB 安装程序（`.run` 文件）。
  - 执行节点（集群内任一节点）可通过 SSH 登录至待扩容节点，并对待扩容节点的安装目录拥有写入权限。
  - 不同模式对用户的要求不同：
    - 命令行模式或终端图形交互模式：用户为 `root` 用户或已配置 `sudo` 免密的普通用户。
    - 可视化 GUI 模式：用户为 `root` 用户或拥有 `sudo` 权限的普通用户。
  - （可选）如果集群采用安全模式，需已在待扩容节点上构建临时证书目录并授予读取权限：

    ```bash
    sudo rm -rf /tmp/kaiwudb_certs
    sudo mkdir -p /tmp/kaiwudb_certs
    sudo cp -r /etc/kaiwudb/certs/*ca* /tmp/kaiwudb_certs/
    sudo chmod +r /tmp/kaiwudb_certs/*ca*
    sudo ls -ltr /tmp/kaiwudb_certs
    ```

- 命令行扩容方式采用安全部署模式时，还需满足以下条件：
  - 已准备 `kaiwudb_certs.tar.gz` 证书文件。
  - 主节点的 `sudo` 权限，用于准备和打包证书文件。
  - 主节点到待扩容节点的 SSH 登录权限，用于传输证书。
  - 待扩容节点安装目录的写入权限。

#### 安装程序扩容

##### 命令行模式

1. 将 KWDB 安装程序复制至执行扩容操作的集群节点，并赋予执行权限：

    ```bash
    chmod +x KaiwuDB-*.run
    ```

2. 以命令行模式启动安装程序：

    ```bash
    ./KaiwuDB-*.run -c
    # 或者
    ./KaiwuDB-*.run --cli
    ```

3. 在主功能菜单中，输入 `3` 选择`安装 KaiwuDB 并加入集群`：

    ```plain
    1. 安装 KaiwuDB
    2. 卸载 KaiwuDB
    3. 安装 KaiwuDB 并加入集群
    4. 升级节点
    5. 退出

    请输入操作 [1-5]:
    ```

4. 根据现有集群类型，选择对应的加入模式：

    ```plain
    加入 KaiwuDB 集群
    1. 加入单副本集群
    2. 加入三副本集群
    3. 返回主菜单

    请选择 [1-3]:
    ```

5. 依次输入集群任一节点的 IP 地址和 KWDB 服务端口 (默认 26257)：

    ```plain
    配置集群地址
    请输入集群任一节点地址：
    请输入对应节点 KaiwuDB 服务端口： 
    ```

6. 配置 CA 证书及私钥路径（非安全模式可选择跳过该配置），选择是否为所有用户安装：

    ```plain
    配置 CA 证书目录
    请输入 CA 证书及私钥路径：
    是否为所有用户安装(y/N)：
    ```

7. 安装程序自动生成配置文件模板并打开编辑器，确认或修改各配置项后保存退出，安装程序将自动开始安装并加入集群。

    配置文件示例：

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
    host=192.168.122.224
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
    | `secure_mode` | 安全模式，需与目标集群保持一致。 |
    | `rest_port` | Admin UI 端口，默认为 `8080`。 |
    | `kaiwudb_port` | KWDB 服务端口，默认为 `26257`。 |
    | `brpc_port` | 数据传输端口，默认为 `27257`。 |
    | `data_root` | 数据目录，默认为 `/var/lib/kaiwudb`。 |
    | `host` | 待扩容节点的 IP 地址。 |
    | `port` | SSH 连接端口，默认为 `22`。 |
    | `user` | SSH 连接用户名。 |
    | `passwd` | SSH 连接密码。 |

8. 安装完成后，检查新节点是否成功加入：

    ```shell
    kw-status
    ```

##### 终端图形交互模式

1. 将 KWDB 安装程序复制至执行扩容操作的集群节点，并赋予执行权限：

    ```bash
    chmod +x KaiwuDB-*.run
    ```

2. 以终端图形交互模式启动安装程序：

    ```bash
    ./KaiwuDB-*.run -i
    # 或者
    ./KaiwuDB-*.run --interact
    ```

3. 在主功能菜单中，使用方向键选中**安装 KaiwuDB 并加入集群**，按回车确认。

4. 进入安装参数设置菜单，根据需要依次设置以下配置项：

    | 配置项 | 说明 |
    |--------|------|
    | 设置安全模式 | 需与目标集群安全模式保持一致。 |
    | 设置数据库服务端口 | KWDB 服务端口，默认为 `26257`。 |
    | 设置 Admin UI 端口 | KWDB Web 服务端口，默认为 `8080`。 |
    | 设置数据传输端口 | 时序引擎间的数据传输端口，默认为 `27257`。 |
    | 选择部署模式 | 需与目标集群部署模式保持一致。 |
    | 增加节点 | 填写待扩容节点的主机名、端口、用户名和密码。 |
    | 设置数据目录 | 数据目录，默认为 `/var/lib/kaiwudb`。 |
    | 设置目标集群地址 | 目标集群任一节点的 IP 地址。 |
    | 设置目标集群 KaiwuDB 服务端口 | 目标集群的 KWDB 服务端口。 |
    | 设置 CA 证书路径 | 安全模式下需要上传目标集群的 CA 证书及私钥文件，通过文件选择器选择路径。 |

5. 选择是否为所有用户安装。

6. 所有配置完成后，选中**开始安装**，按回车开始安装并加入集群。

7. 安装完成后，检查新节点是否成功加入：

    ```shell
    kw-status
    ```

##### 可视化 GUI 模式

1. 将 KWDB 安装程序复制至执行扩容操作的集群节点，并赋予执行权限：

    ```bash
    chmod +x KaiwuDB-*.run
    ```

2. 以可视化 GUI 模式启动安装程序：

    ```bash
    sudo ./KaiwuDB-*.run -g
    # 或者
    sudo ./KaiwuDB-*.run --gui
    ```

3. 在操作向导页面，选中**全新安装**，点击**下一步**。

    ![](../static/quickstart/gui-welcome.png)

4. 在用户许可页面，勾选同意许可协议，点击**下一步**。

    ![](../static/quickstart/gui-agreement.png)

5. 在参数配置页面，设置安全模式、各端口和数据目录，参数需与目标集群保持一致，完成后点击**下一步**。

    ![](../static/quickstart/gui-config.png)

6. 在节点管理页面，选择多副本集群模式，点击**增加节点**，填写待扩容节点的 IP、端口、用户名和密码，点击**保存**。然后勾选底部的**加入集群**选项。

    ![](../static/quickstart/gui-scale.png)

7. 在弹出的**目标集群参数**对话框中填写目标集群相关信息，点击**确定**，然后点击**下一步**。

    ![](../static/quickstart/gui-target.png)

    | 参数 | 说明 |
    |------|------|
    | 目标集群模式 | 目标集群的安全模式。 |
    | 目标集群 IP | 目标集群任一节点的 IP 地址。 |
    | 目标集群服务端口 | 目标集群的 KWDB 服务端口。 |

8. 在开始安装页面，等待安装完成，然后点击**结束**。

9. 检查新节点是否成功加入：

    ```shell
    kw-status
    ```

#### 命令行扩容

1. 登录待扩容节点。

2. 如果集群采用安全部署模式，将 `kaiwudb_certs.tar.gz` 复制到当前节点并解压到 `/etc/kaiwudb/certs` 目录。

3. 执行加入集群命令：

   ::: warning 提示
   以下命令仅列出了常用的启动参数，KWDB 支持的所有启动参数见[启动参数](../db-operation/cluster-settings-config.md)。
   :::

   - 安全模式

      ```shell
      <kwbase_path>/kwbase start \
      --certs-dir=<cert_path> \
      --store=<data_dir> \
      --brpc-addr=:27257 \
      --listen-addr=<new_node_ip>:<kaiwudb_port> \
      --http-addr=<new_node_ip>:<rest_port> \
      --join=<node_address_list> \
      --background
      ```

   - 非安全模式

      ```shell
      <kwbase_path>/kwbase start \
      --insecure \
      --store=<data_dir> \
      --brpc-addr=:27257 \
      --listen-addr=<new_node_ip>:<kaiwudb_port> \
      --http-addr=<new_node_ip>:<rest_port> \
      --join=<node_address_list> \
      --background
      ```

   参数说明：

   - `<kwbase_path>`：kwbase 二进制文件所在目录，裸机部署默认目录为 `/usr/local/kaiwudb/bin`，容器部署默认目录为 `/kaiwudb/bin`。
   - `<cert_path>`：指定存放证书和密钥的文件夹，默认存储位置为 `/etc/kaiwudb/certs`。
   - `<data_dir>`：可选参数，用于指定节点的数据和日志存储位置，默认位置为 `/var/lib/kaiwudb`。
   - `<new_node_ip>:<kaiwudb_port>`：可选参数，用于指定新节点地址和 KWDB 服务端口，默认端口为 `26257`。
   - `<new_node_ip>:<rest_port>`：可选参数，用于指定新节点地址以及 KWDB RESTful 的端口，默认端口为 `8080`。
   - `<node_address_list>`：待连接的集群节点列表，支持指定一个或多个节点地址，节点地址间使用逗号隔开。
   - `--background`：可选参数，在后台运行。

4. 检查集群节点状态：

   - 安全模式

      ```shell
      <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
      ```

   - 非安全模式

      ```shell
      <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>]
      ```

   参数说明：

   - `<kwbase_path>`：kwbase 二进制文件所在目录，裸机部署默认目录为 `/usr/local/kaiwudb/bin`，容器部署默认目录为 `/kaiwudb/bin`。
   - `<cert_path>`：证书目录，默认存储位置为 `/etc/kaiwudb/certs`。
   - `--host=<address_of_any_alive_node>`：可选参数，用于指定执行命令的节点，该节点必须为健康节点，地址格式为 `<ip>:<port>`，不指定时默认使用 `127.0.0.1:26257`。

### 单副本集群扩容

KWDB 单副本集群支持安装程序扩容和命令行扩容两种方式。

#### 前提条件

- 待扩容节点未安装 KWDB。
- 目标集群处于运行状态。
- 当前节点数未达到许可证上限。
- 安装程序扩容方式还需满足以下条件：
  - 已获取 KWDB 安装程序（`.run` 文件）。
  - 执行节点（集群内任一节点）可通过 SSH 登录至待扩容节点，并对待扩容节点的安装目录拥有写入权限。
  - 不同模式对用户的要求不同：
    - 命令行模式或终端图形交互模式：用户为 `root` 用户或已配置 `sudo` 免密的普通用户。
    - 可视化 GUI 模式：用户为 `root` 用户或拥有 `sudo` 权限的普通用户。
  - （可选）如果集群采用安全模式，需已在待扩容节点上构建临时证书目录并授予读取权限：

    ```bash
    sudo rm -rf /tmp/kaiwudb_certs
    sudo mkdir -p /tmp/kaiwudb_certs
    sudo cp -r /etc/kaiwudb/certs/*ca* /tmp/kaiwudb_certs/
    sudo chmod +r /tmp/kaiwudb_certs/*ca*
    sudo ls -ltr /tmp/kaiwudb_certs
    ```

- 命令行扩容方式采用安全部署模式时，还需满足以下条件：
  - 已准备 `kaiwudb_certs.tar.gz` 证书文件。
  - 主节点的 `sudo` 权限，用于准备和打包证书文件。
  - 主节点到待扩容节点的 SSH 登录权限，用于传输证书。
  - 待扩容节点安装目录的写入权限。

#### 安装程序扩容

##### 命令行模式

1. 将 KWDB 安装程序复制至执行扩容操作的集群节点，并赋予执行权限：

    ```bash
    chmod +x KaiwuDB-*.run
    ```

2. 以命令行模式启动安装程序：

    ```bash
    ./KaiwuDB-*.run -c
    # 或者
    ./KaiwuDB-*.run --cli
    ```

3. 在主功能菜单中，输入 `3` 选择`安装 KaiwuDB 并加入集群`：

    ```plain
    1. 安装 KaiwuDB
    2. 卸载 KaiwuDB
    3. 安装 KaiwuDB 并加入集群
    4. 升级节点
    5. 退出

    请输入操作 [1-5]:
    ```

4. 根据现有集群类型，选择对应的加入模式：

    ```plain
    加入 KaiwuDB 集群
    1. 加入单副本集群
    2. 加入三副本集群
    3. 返回主菜单

    请选择 [1-3]:
    ```

5. 依次输入集群任一节点的 IP 地址和 KWDB 服务端口 (默认 26257)：

    ```plain
    配置集群地址
    请输入集群任一节点地址：
    请输入对应节点 KaiwuDB 服务端口： 
    ```

6. 配置 CA 证书及私钥路径（非安全模式可选择跳过该配置），选择是否为所有用户安装：

    ```plain
    配置 CA 证书目录
    请输入 CA 证书及私钥路径：
    是否为所有用户安装(y/N)：
    ```

7. 安装程序自动生成配置文件模板并打开编辑器，确认或修改各配置项后保存退出，安装程序将自动开始安装并加入集群。

    配置文件示例：

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
    host=192.168.122.224
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
    | `secure_mode` | 安全模式，需与目标集群保持一致。 |
    | `rest_port` | Admin UI 端口，默认为 `8080`。 |
    | `kaiwudb_port` | KWDB 服务端口，默认为 `26257`。 |
    | `brpc_port` | 数据传输端口，默认为 `27257`。 |
    | `data_root` | 数据目录，默认为 `/var/lib/kaiwudb`。 |
    | `host` | 待扩容节点的 IP 地址。 |
    | `port` | SSH 连接端口，默认为 `22`。 |
    | `user` | SSH 连接用户名。 |
    | `passwd` | SSH 连接密码。 |

8. 安装完成后，检查新节点是否成功加入：

    ```shell
    kw-status
    ```

##### 终端图形交互模式

1. 将 KWDB 安装程序复制至执行扩容操作的集群节点，并赋予执行权限：

    ```bash
    chmod +x KaiwuDB-*.run
    ```

2. 以终端图形交互模式启动安装程序：

    ```bash
    ./KaiwuDB-*.run -i
    # 或者
    ./KaiwuDB-*.run --interact
    ```

3. 在主功能菜单中，使用方向键选中**安装 KaiwuDB 并加入集群**，按回车确认。

4. 进入安装参数设置菜单，根据需要依次设置以下配置项：

    | 配置项 | 说明 |
    |--------|------|
    | 设置安全模式 | 需与目标集群安全模式保持一致。 |
    | 设置数据库服务端口 | KWDB 服务端口，默认为 `26257`。 |
    | 设置 Admin UI 端口 | KWDB Web 服务端口，默认为 `8080`。 |
    | 设置数据传输端口 | 时序引擎间的数据传输端口，默认为 `27257`。 |
    | 选择部署模式 | 需与目标集群部署模式保持一致。 |
    | 增加节点 | 填写待扩容节点的主机名、端口、用户名和密码。 |
    | 设置数据目录 | 数据目录，默认为 `/var/lib/kaiwudb`。 |
    | 设置目标集群地址 | 目标集群任一节点的 IP 地址。 |
    | 设置目标集群 KaiwuDB 服务端口 | 目标集群的 KWDB 服务端口。 |
    | 设置 CA 证书路径 | 安全模式下需要上传目标集群的 CA 证书及私钥文件，通过文件选择器选择路径。 |

5. 选择是否为所有用户安装。

6. 所有配置完成后，选中**开始安装**，按回车开始安装并加入集群。

7. 安装完成后，检查新节点是否成功加入：

    ```shell
    kw-status
    ```

##### 可视化 GUI 模式

1. 将 KWDB 安装程序复制至执行扩容操作的集群节点，并赋予执行权限：

    ```bash
    chmod +x KaiwuDB-*.run
    ```

2. 以可视化 GUI 模式启动安装程序：

    ```bash
    sudo ./KaiwuDB-*.run -g
    # 或者
    sudo ./KaiwuDB-*.run --gui
    ```

3. 在操作向导页面，选中**全新安装**，点击**下一步**。

    ![](../static/quickstart/gui-welcome.png)

4. 在用户许可页面，勾选同意许可协议，点击**下一步**。

    ![](../static/quickstart/gui-agreement.png)

5. 在参数配置页面，设置安全模式、各端口和数据目录，参数需与目标集群保持一致，完成后点击**下一步**。

    ![](../static/quickstart/gui-config.png)

6. 在节点管理页面，选择多副本集群模式，点击**增加节点**，填写待扩容节点的 IP、端口、用户名和密码，点击**保存**。然后勾选底部的**加入集群**选项。

    ![](../static/quickstart/gui-scale.png)

7. 在弹出的**目标集群参数**对话框中填写目标集群相关信息，点击**确定**，然后点击**下一步**。

    ![](../static/quickstart/gui-target.png)

    | 参数 | 说明 |
    |------|------|
    | 目标集群模式 | 目标集群的安全模式。 |
    | 目标集群 IP | 目标集群任一节点的 IP 地址。 |
    | 目标集群服务端口 | 目标集群的 KWDB 服务端口。 |

8. 在开始安装页面，等待安装完成，然后点击**结束**。

9. 检查新节点是否成功加入：

    ```shell
    kw-status
    ```

#### 命令行扩容

1. 登录待扩容节点。

2. 如果集群采用安全部署模式，将 `kaiwudb_certs.tar.gz` 复制到当前节点并解压到 `/etc/kaiwudb/certs` 目录。

3. 执行加入集群命令：

   ::: warning 提示
   以下命令仅列出了常用的启动参数，KWDB 支持的所有启动参数见[启动参数](../db-operation/cluster-settings-config.md)。
   :::

   - 安全模式

      ```shell
      <kwbase_path>/kwbase start-single-replica \
      --certs-dir=<cert_path> \
      --store=<data_dir> \
      --brpc-addr=:27257 \
      --listen-addr=<new_node_ip>:<kaiwudb_port> \
      --http-addr=<new_node_ip>:<rest_port> \
      --join=<node_address_list> \
      --background
      ```

   - 非安全模式

      ```shell
      <kwbase_path>/kwbase start-single-replica \
      --insecure \
      --store=<data_dir> \
      --brpc-addr=:27257 \
      --listen-addr=<new_node_ip>:<kaiwudb_port> \
      --http-addr=<new_node_ip>:<rest_port> \
      --join=<node_address_list> \
      --background
      ```

4. 检查集群节点状态：

   - 安装程序部署

      ```shell
      kw-status
      ```

   - kwbase 命令

      ```shell
      # 安全模式
      <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]

      # 非安全模式
      <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>]
      ```

## 集群缩容

目前，单副本集群不支持集群缩容操作。

KWDB 多副本集群支持命令行缩容方式。用户主动移除节点时，KWDB 会允许节点完成正在执行的请求，拒绝任何新的请求，同时将该节点上的分区副本和分区租约迁移到其他节点，以确保数据的平稳迁移。移除后的节点可以根据实际需求选择永久移除，以最大程度地保障系统的可用性和数据的完整性。

::: warning 注意

- 移除节点时，必须确保有其他节点可以接管该节点的分区副本。如果没有可用的其他节点，移除操作将无限期挂起。
- KWDB 集群采用三副本机制，最小集群节点数为 3，不允许进一步缩容。
- 如果之前通过 `CONFIGURE ZONE` 语句设置了副本约束，且约束规则中包含待缩容节点，可能会影响集群缩容的正常运行。此时需要重新配置约束规则，将待缩容节点从规则中移除，集群缩容即可恢复正常。

:::

节点退役后如需再次加入集群时，需要先清空数据目录，作为新节点重新加入集群。

### 前提条件

- 集群内所有节点均处于存活状态（`is_available` 和 `is_live` 均为 `true`）。

   - 安装程序部署

   ```shell
   kw-status
   ```

   - 通过 `kwbase node status` 命令查看节点状态

   ```shell
   <kwbase_path>/kwbase node status [--host=<ip:port>] [--insecure | --certs-dir=<path>]
   ```

- 已获得待退役节点的 ID。

- 没有不可用分区和副本不足分区。

   ```sql
   SELECT sum((metrics->>'ranges.unavailable')::DECIMAL)::INT AS ranges_unavailable,
      sum((metrics->>'ranges.underreplicated')::DECIMAL)::INT As ranges_underreplicated
   FROM kwdb_internal.kv_store_status;
   ```

### 步骤

1. 登录集群中的任一节点，执行节点退役命令：

   - 安全模式

      ```shell
      <kwbase_path>/kwbase node decommission <node_id> --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
      ```

   - 非安全模式

      ```bash
      <kwbase_path>/kwbase node decommission <node_id> --insecure [--host=<address_of_any_alive_node>]
      ```

2. 检查集群节点状态。退役节点状态变为 `decommissioning`，节点上的副本数缩减到 `0` 时表示退役完成。

   - 安全模式

     ```shell
     <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>] --decommission
     ```

   - 非安全模式

     ```bash
     <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>] --decommission
     ```

3. （可选）如需将退役节点彻底移出集群，执行以下命令：

   - 安全模式

     ```bash
     <kwbase_path>/kwbase quit --certs-dir=<cert_path> --host=<decommissioned_node>
     ```

   - 非安全模式

     ```bash
     <kwbase_path>/kwbase quit --insecure --host=<decommissioned_node>
     ```

4. （可选）确认节点已成功移除：

   - 安装程序部署

      ```shell
      kw-status
      ```

   - kwbase 命令

      ```shell
      # 安全模式
      <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
      
      # 非安全模式
      <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>]
      ```