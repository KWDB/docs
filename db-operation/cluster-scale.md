---
title: 集群扩缩容
id: cluster-scale
---
# 集群扩缩容

## 集群扩容

KWDB 多副本集群和单副本集群均支持集群扩容操作。

- 多副本集群扩容后，系统默认自动触发数据重新分布，具体操作信息，参见[多副本集群扩容](#多副本集群扩容)。
- 单副本集群扩容后，系统不会对已有数据进行重新分布，只会在新建表后进行数据均衡，具体操作信息，参见[单副本集群扩容](#单副本集群扩容)。

::: warning 说明

集群执行扩容期间，可能会出现短暂的数据查询不完整情况，操作完成后，系统将自动同步并确保数据查询的完整性和准确性。
:::

### 多副本集群扩容

KWDB 多副本集群扩容操作简单，只需将新节点加入现有集群即可。集群默认会自动完成数据重分布。用户也可通过 `kv.allocator.ts_consider_rebalance.enabled` 参数关闭自动重分布功能，选择在系统负载较低时重新启用该参数进行数据重分布。

在扩容期间，由于数据迁移，集群所需的磁盘总容量可能会增加。一旦扩容完成，集群所需的磁盘总容量将会回落到扩容前的水平，仅有细微差异。

在扩容期间执行时序索引相关的 DDL 操作可能会报错，扩容完成后操作会执行成功。

在扩容期间，如果频繁执行 `ALTER` 语句操作，可能会延迟扩容后的数据自平衡。

**前提条件：**

- 待扩容节点已通过多副本集群部署方式安装 KWDB, 具体操作信息，参见[集群部署](../deployment/cluster-deployment/script-deployment.md)。
- 目标集群已启动。
- 如果集群采用安全部署模式，已备好 `kaiwudb_certs.tar.gz` 文件。

**步骤：**

1. 登录需要加入集群的节点。

2. 如果集群采用安全部署模式，将部署后在安装包目录生成的 `kaiwudb_certs.tar.gz` 文件复制到当前节点。

3. 执行加入集群命令。

   ::: warning 提示
   以下命令仅列出了常用的启动参数，KWDB 支持的所有启动参数见[启动参数](../db-operation/cluster-settings-config.md)。
   :::

   - 安全模式

      ```Shell
      <kwbase_path>/kwbase start --certs-dir=<cert_path> --store=<data_dir> --brpc-addr=:27257 --listen-addr=<new_node>:<kaiwudb_port> --http-addr=<new_node>:<rest_port> --join=<node_address_list> --background
      ```

   - 非安全模式

      ```Shell
      <kwbase_path>/kwbase start --insecure --store=<data_dir> --brpc-addr=:27257 --listen-addr=<new_node>:26257 --http-addr=<new_node>:<rest_port> --join=<node_address_list> --background
      ```

   参数说明：

   - `<kwbase_path>`：kwbase 二进制文件所在目录，裸机部署默认目录为 `/usr/local/kaiwudb/bin`， 容器部署默认目录为 `/kaiwudb/bin`。

   - `<cert_path>`：指定存放证书和密钥的文件夹，默认存储位置为 `/etc/kaiwudb/certs`。

   - `<data_dir>`：可选参数，用于指定节点的数据和日志存储位置，默认位置为 `/var/lib/kaiwudb`。

   - `<new_node>:<kaiwudb_port>`：可选参数，用于指定新节点地址和 KWDB 服务端口，默认端口为 `26257`。

   - `<new_node>:<rest_port>`：可选参数，用于指定新节点地址以及 RESTful 的端口，默认端口为 `8080`。

   - `<node_address_list>`：待连接的集群节点列表，支持指定一个或多个节点地址，节点地址间使用逗号隔开。

   - `--background`：可选参数，在后台运行。

4. 检查集群节点状态。

   - 安全模式

      ```Shell
      <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
      ```

   - 非安全模式

      ```Bash
      <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>]
      ```

    参数说明：

   - `<kwbase_path>`：kwbase 二进制文件所在目录，裸机部署默认目录为 `/usr/local/kaiwudb/bin`， 容器部署默认目录为 `/kaiwudb/bin`。
   - `cert_path`：证书目录，默认存储位置为 `/etc/kaiwudb/certs`。
   - `--host=<address_of_any_alive_node>`：可选参数，用于指定执行命令的节点，该节点必须为健康节点，地址格式为 `<ip>:<port>`, 不指定时默认使用 `127.0.0.1:26257`。
  
### 单副本集群扩容

KWDB 单副本集群的扩容非常简单，只需要将待扩容节点加入到现有集群即可。

**前提条件：**

- 待扩容节点已通过单副本集群部署方式安装 KWDB, 具体操作信息，参见[集群部署](../deployment/cluster-deployment/script-deployment.md)。
- 目标集群已启动。
- 如果集群采用安全部署模式，已备好 `kaiwudb_certs.tar.gz` 文件。

**步骤：**

1. 登录需要加入集群的节点。

2. 如果集群采用安全部署模式，将部署后在安装包目录生成的 `kaiwudb_certs.tar.gz` 文件复制到当前节点。

3. 执行加入集群命令。

   ::: warning 提示
   以下命令仅列出了常用的启动参数，KWDB 支持的所有启动参数见[启动参数](../db-operation/cluster-settings-config.md)。
   :::

   - 安全模式

      ```Shell
      <kwbase_path>/kwbase start-single-replica --certs-dir=<cert_path> --store=<data_dir> --brpc-addr=:27257 --listen-addr=<new_node>:<kaiwudb_port> --http-addr=<new_node>:<rest_port> --join=<node_address_list> --background
      ```

   - 非安全模式

      ```Shell
      <kwbase_path>/kwbase start-single-replica --insecure --store=<data_dir> --brpc-addr=:27257 --listen-addr=<new_node>:26257 --http-addr=<new_node>:<rest_port> --join=<node_address_list> --background
      ```

4. 检查集群节点状态。

   - 安全模式

      ```Shell
      <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
      ```

   - 非安全模式

      ```Bash
      <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>]
      ```

## 集群缩容

目前，单副本集群不支持集群缩容操作。

在多副本集群中，用户主动移除节点时，KWDB 会允许节点完成正在执行的请求，拒绝任何新的请求，同时将该节点上的分片副本和分片租约迁移到其他节点，以确保数据的平稳迁移。移除后的节点可以根据实际需求选择永久移除，以最大程度地保障系统的可用性和数据的完整性。

::: warning 注意

- 移除节点时，必须确保有其他节点可以接管该节点的分区副本。如果没有可用的其他节点，移除操作将无限期挂起。
- KWDB 集群采用三副本机制，最小集群节点数为 3，不允许进一步缩容。
- 在缩容过程中，缩容节点的重启可能导致宕机。
- 如果之前通过 `CONFIGURE ZONE` 语句设置了副本约束，且约束规则中包含待缩容节点，可能会影响集群缩容的正常运行。此时需要重新配置约束规则，将待缩容节点从规则中移除，集群缩容即可恢复正常。

:::

在缩容期间，由于数据迁移，集群所需的磁盘总容量可能会增加。一旦缩容完成，集群所需的磁盘总容量将会回落到缩容前的水平，仅有细微差异。

缩容期间，因数据分区迁移，时序索引相关的 DDL 操作可能会报错，数据查询可能不完整，但缩容完成后将确保操作成功执行且数据查询完整准确。

节点退役后再次加入集群时，需要清空数据目录作为新节点重新加入集群。

**前提条件：**

- 集群内所有节点均处于存活状态（`is_available` 和 `is_live` 均为 `true`）。

  - 在安装包目录执行集群节点状态查看命令：

    ```Shell
    ./deploy.sh cluster --status
    ```

  - 通过 `kwbase node status` 命令查看节点状态：

    ```Shell
    <kwbase_path>/kwbase node status [--host=<ip:port>] [--insecure | --certs-dir=<path>]
    ```

- 已获得待退役节点的 ID。

- 没有不可用分片和副本不足分片：

    ```SQL
    SELECT sum((metrics->>'ranges.unavailable')::DECIMAL)::INT AS ranges_unavailable,
        sum((metrics->>'ranges.underreplicated')::DECIMAL)::INT As ranges_underreplicated
    FROM kwdb_internal.kv_store_status;
    ```

**步骤：**

1. 登录集群中的任一节点，执行节点退役命令：

   - 安全模式

      ```Shell
      <kwbase_path>/kwbase node decommission <node_id> --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
      ```

   - 非安全模式

      ```Bash
      <kwbase_path>/kwbase node decommission <node_id> --insecure [--host=<address_of_any_alive_node>]
      ```

2. 检查集群节点状态。退役节点状态变为 `decommissioning`, 节点上的副本数缩减到 `0` 时表示退役完成。

   - 安全模式

     ```Shell
     <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>] --decommission
     ```

   - 非安全模式

     ```Bash
     <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>] --decommission
     ```

3. （可选）如需将退役节点彻底移出集群，执行以下命令：

   - 安全模式

     ```Bash
     <kwbase_path>/kwbase quit --certs-dir=<cert_path> --host=<decommissioned_node>
     ```

   - 非安全模式

     ```Bash
     <kwbase_path>/kwbase quit --insecure --host=<decommissioned_node>
     ```

4. （可选）检查集群节点是否移除成功。

   - 安全模式

     ```Shell
     <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
     ```

   - 非安全模式

      ```Shell
      <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>]
      ```