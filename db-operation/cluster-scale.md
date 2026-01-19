---
title: 集群扩缩容
id: cluster-scale
---
# 集群扩缩容

KWDB 支持集群的动态扩容和缩容操作，以满足不同业务场景下的容量和性能需求。不同集群类型的扩缩容特性如下:

| 集群类型 | 扩容 | 缩容 | 数据重分布机制 | 操作方式 |
|---------|------|------|--------------|---------|
| 多副本集群 | 支持 | 支持 | 自动触发，平衡所有节点数据 | 脚本 / 命令行 |
| 单副本集群 | 支持 | 不支持 | 仅对新建表生效，已有数据不迁移 | 命令行 |

::: warning 说明

- **数据查询**：扩缩容期间，可能会出现短暂的数据查询不完整情况，操作完成后，系统将自动同步并确保数据查询的完整性和准确性。
- **DDL 操作**：扩缩容期间，时序索引相关的 DDL 操作（如 `CREATE INDEX`、`DROP INDEX`）可能返回超时错误，操作完成后重试即可。
- **磁盘容量**：扩缩容期间，因数据迁移需要，集群磁盘使用量可能临时增加。操作完成后将恢复正常水平。
- **操作建议**：建议在业务低峰期执行扩缩容操作，以降低对业务的影响。

:::

## 集群扩容

### 多副本集群扩容

KWDB 多副本集群支持脚本扩容和命令行扩容两种方式。扩容完成后，集群会自动进行数据重分布，确保负载均衡。

**数据重分布**

扩容完成后，系统默认自动将现有数据均匀分布到所有节点。如需关闭自动重分布功能，可设置以下参数:

```sql
SET CLUSTER SETTING kv.allocator.ts_consider_rebalance.enabled = false;
```

重分布期间建议避免频繁执行 `ALTER` 语句，以免延长数据重分布时间。

#### 前提条件

- 待扩容节点已通过多副本集群部署方式完成 KWDB 安装（参见[集群部署](../deployment/cluster-deployment/script-deployment.md)）
- 目标集群处于运行状态
- 脚本扩容方式: 待扩容节点需使用脚本部署方式安装
- 命令行扩容方式: 如采用安全部署模式，需准备 `kaiwudb_certs.tar.gz` 证书文件
- 用户权限（仅安全模式需要）:
  - 主节点的 `sudo` 权限，用于准备和打包证书文件
  - 主节点到待扩容节点的 SSH 登录权限，用于传输证书
  - 待扩容节点安装目录的写入权限

#### 脚本扩容

1. （可选）如果集群采用安全部署模式，需要在主节点上准备并传输证书文件到待扩容节点。

   1. 登录集群主节点（集群初始部署节点），进入安装包目录：

      ```shell
      cd <install_dir>
      ```

   2. 将 KWDB 的安全证书和密钥复制到当前目录：

      ```shell
      sudo cp /etc/kaiwudb/certs/ca.key ./
      sudo cp /etc/kaiwudb/certs/ca.crt ./
      ```

   3. 将文件所有者修改为 kaiwudb 用户：

         ```shell
         sudo chown kaiwudb:kaiwudb ./ca.key ./ca.crt
         ```

   4. 设置证书文件权限：

      ```shell
      sudo chmod 644 ./ca.crt
      ```

   5. 打包证书文件：

      ```shell
      sudo tar -czf kaiwudb_certs.tar.gz ./ca.key ./ca.crt
      ```

   6. 将压缩包所有者修改为 `admin` 用户：

      ```shell
      sudo chown admin:admin kaiwudb_certs.tar.gz
      ```

   7. 将压缩包传输到待扩容节点：

      ```shell
      scp kaiwudb_certs.tar.gz admin@<new_node_ip>:<install_dir>
      ```

2. 登录待扩容节点，在安装包目录执行加入集群命令：

   - 安全模式

      ```shell
      ./deploy.sh join --addr <any_cluster_node_ip>:<port> --tls
      ```

   - 非安全模式

      ```shell
      ./deploy.sh join --addr <any_cluster_node_ip>:<port>
      ```

   参数说明：

   - `<any_cluster_node_ip>`：集群任一健康节点的 IP 地址，例如 `192.168.122.221`。
   - `<port>`：KWDB 服务端口，默认端口为 `26257`。

3. 执行以下命令检查新节点是否成功加入：

   ```shell
   kw-status
   ```

#### 命令行扩容

1. 登录待扩容节点。

2. 如果集群采用安全部署模式，将 `kaiwudb_certs.tar.gz` 复制到当前节点并解压到 `/etc/kaiwudb/certs` 目录。

3. 执行加入集群命令。

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
      --listen-addr=<new_node_ip>:26257 \
      --http-addr=<new_node_ip>:<rest_port> \
      --join=<node_address_list> \
      --background
      ```

   参数说明：

   - `<kwbase_path>`：kwbase 二进制文件所在目录，裸机部署默认目录为 `/usr/local/kaiwudb/bin`，容器部署默认目录为 `/kaiwudb/bin`。
   - `<cert_path>`：指定存放证书和密钥的文件夹，默认存储位置为 `/etc/kaiwudb/certs`。
   - `<data_dir>`：可选参数，用于指定节点的数据和日志存储位置，默认位置为 `/var/lib/kaiwudb`。
   - `<new_node_ip>:<kaiwudb_port>`：可选参数，用于指定新节点地址和 KWDB 服务端口，默认端口为 `26257`。
   - `<new_node_ip>:<rest_port>`：可选参数，用于指定新节点地址以及 RESTful 的端口，默认端口为 `8080`。
   - `<node_address_list>`：待连接的集群节点列表，支持指定一个或多个节点地址，节点地址间使用逗号隔开。
   - `--background`：可选参数，在后台运行。

4. 使用以下命令检查集群节点状态：

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

KWDB 单副本集群的扩容非常简单，只需要将待扩容节点加入到现有集群即可。

#### 前提条件

- 待扩容节点已通过单副本集群部署方式安装 KWDB，具体操作信息，参见[集群部署](../deployment/cluster-deployment/script-deployment.md)。
- 目标集群已启动。
- 如果集群采用安全部署模式，已备好 `kaiwudb_certs.tar.gz` 文件。

#### 步骤

1. 登录待扩容节点。

2. 如果集群采用安全部署模式，将 `kaiwudb_certs.tar.gz` 复制到当前节点并解压到 `/etc/kaiwudb/certs` 目录。

3. 执行加入集群命令。

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
      --listen-addr=<new_node_ip>:26257 \
      --http-addr=<new_node_ip>:<rest_port> \
      --join=<node_address_list> \
      --background
      ```

4. 使用以下命令检查集群节点状态。

   - 脚本部署

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

KWDB 多副本集群支持脚本缩容和命令行缩容两种方式。用户主动移除节点时，KWDB 会允许节点完成正在执行的请求，拒绝任何新的请求，同时将该节点上的分区副本和分区租约迁移到其他节点，以确保数据的平稳迁移。移除后的节点可以根据实际需求选择永久移除，以最大程度地保障系统的可用性和数据的完整性。

::: warning 注意

- 移除节点时，必须确保有其他节点可以接管该节点的分区副本。如果没有可用的其他节点，移除操作将无限期挂起。
- KWDB 集群采用三副本机制，最小集群节点数为 3，不允许进一步缩容。
- 如果之前通过 `CONFIGURE ZONE` 语句设置了副本约束，且约束规则中包含待缩容节点，可能会影响集群缩容的正常运行。此时需要重新配置约束规则，将待缩容节点从规则中移除，集群缩容即可恢复正常。

:::

节点退役后如需再次加入集群时，需要先清空数据目录，作为新节点重新加入集群。

### 前提条件

- 集群内所有节点均处于存活状态（`is_available` 和 `is_live` 均为 `true`）。

   - 脚本部署

      ```shell
      kw-status
      ```

   - 在安装包目录执行集群节点状态查看命令：

      ```shell
      ./deploy.sh cluster --status
      ```

   - 通过 `kwbase node status` 命令查看节点状态：

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

### 脚本缩容

1. 登录需要移除的节点，在安装包目录执行节点退役命令：

   ```shell
   ./deploy.sh decommission
   ```

2. 在同级目录下查看 `decommission_progress` 文件，监控剩余副本数。

3. 待剩余副本数为 0 后，停止数据库运行：

   ```shell
   systemctl stop kaiwudb
   ```

4. 使用以下命令确认节点已成功移除：

   ```shell
   kw-status
   ```

### 命令行缩容

1. 登录集群中的任一节点，执行节点退役命令：

   - 安全模式

      ```shell
      <kwbase_path>/kwbase node decommission <node_id> --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
      ```

   - 非安全模式

      ```bash
      <kwbase_path>/kwbase node decommission <node_id> --insecure [--host=<address_of_any_alive_node>]
      ```

2. 使用以下命令检查集群节点状态。退役节点状态变为 `decommissioning`，节点上的副本数缩减到 `0` 时表示退役完成。

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

4. （可选）使用以下命令确认节点已成功移除。

   - 脚本部署

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