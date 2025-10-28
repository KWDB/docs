---
title: Cluster Scaling
id: cluster-scale
---
# Cluster Scaling

## Scaling Out a Cluster

::: warning Note

During cluster scale-out, there may be brief periods of incomplete data queries. After the operation completes, the system will automatically synchronize to ensure data query integrity and accuracy.
:::

Both KWDB multi-replica clusters and single-replica clusters support scale-out operations.

- After scaling out a multi-replica cluster, the system automatically triggers data redistribution by default. For more information, see [Multi-Replica Cluster Scale-Out](#multi-replica-cluster-scale-out).
- After scaling out a single-replica cluster, the system will not redistribute existing data and will only balance data when new tables are created. For more information, see [Single-Replica Cluster Scale-Out](#single-replica-cluster-scale-out).

### Multi-Replica Cluster Scale-Out

Scaling out a KWDB multi-replica cluster is straightforward—simply add new nodes to the existing cluster. The cluster will automatically complete data redistribution by default. You can also disable the automatic redistribution feature using the `kv.allocator.ts_consider_rebalance.enabled` parameter, then re-enable this parameter for data redistribution when system load is lower.

During scale-out, the total disk capacity required by the cluster may temporarily increase due to data migration. Once scale-out is complete, the total disk capacity will return to pre-scale-out levels, with only minor differences.

DDL operations related to tag indexes may fail during scale-out but will execute successfully after scale-out completes.

Frequent execution of `ALTER` statements during scale-out may delay the automatic data rebalancing process.

**Prerequisites**

- KWDB has been installed on the nodes to be added using the multi-replica cluster deployment method. For instructions, see [Cluster Deployment](../deployment/cluster-deployment/script-deployment.md).
- The target cluster is running.
- If the cluster uses secure mode, the `kaiwudb_certs.tar.gz` file is available.

**Steps**

1. Log in to the node that needs to join the cluster.

2. If the cluster uses secure mode, copy the `kaiwudb_certs.tar.gz` file generated in the installation directory after deployment to the current node.

3. Execute the command to join the cluster.

   ::: warning Note
   The following commands list only commonly used startup flags. For all startup flags supported by KWDB, see [Startup Flags](../db-operation/cluster-settings-config.md).
   :::

   - Secure mode

      ```Shell
      <kwbase_path>/kwbase start --certs-dir=<cert_path> --store=<data_dir> --brpc-addr=:27257 --listen-addr=<new_node>:<kaiwudb_port> --http-addr=<new_node>:<rest_port> --join=<node_address_list> --background
      ```

   - Insecure mode

      ```Shell
      <kwbase_path>/kwbase start --insecure --store=<data_dir> --brpc-addr=:27257 --listen-addr=<new_node>:26257 --http-addr=<new_node>:<rest_port> --join=<node_address_list> --background
      ```

   **Parameters:**

   - `<kwbase_path>`: The directory where the kwbase binary file is located. The default directory is `/usr/local/kaiwudb/bin` for bare-metal deployment and `/kaiwudb/bin` for container deployment.

   - `<cert_path>`: Specifies the folder containing certificates and keys. The default storage location is `/etc/kaiwudb/certs`.

   - `<data_dir>`: (Optional) specifies the data and log storage location for the node. The default location is `/var/lib/kaiwudb`.

   - `<new_node>:<kaiwudb_port>`: (Optional) specifies the new node address and KWDB service port. The default port is `26257`.

   - `<new_node>:<rest_port>`: (Optional) specifies the new node address and the port for RESTful API. The default port is `8080`.

   - `<node_address_list>`: List of cluster nodes to connect to. Supports one or multiple node addresses, separated by commas.

   - `--background`: (Optional) runs the process in the background.

4. Check the cluster node status:

   - Secure mode

      ```Shell
      <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
      ```

   - Insecure mode

      ```Bash
      <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>]
      ```

    **Parameters:**

   - `<kwbase_path>`: The directory where the kwbase binary file is located. The default directory is `/usr/local/kaiwudb/bin` for bare-metal deployment and `/kaiwudb/bin` for container deployment.
   - `cert_path`: Certificate directory. The default storage location is `/etc/kaiwudb/certs`.
   - `--host=<address_of_any_alive_node>`: (Optional) specifies the node on which to execute the command. This node must be healthy. The address format is `<ip>:<port>`. If not specified, the default is `127.0.0.1:26257`.

### Single-Replica Cluster Scale-Out

Scaling out a KWDB single-replica cluster is straightforward—simply add the nodes to the existing cluster.

**Prerequisites**

- KWDB has been installed on the nodes to be added using the single-replica cluster deployment method. For detailed information, see [Cluster Deployment](../deployment/cluster-deployment/script-deployment.md).
- The target cluster is running.
- If the cluster uses secure mode, the `kaiwudb_certs.tar.gz` file is available.

**Steps**

1. Log in to the node that needs to join the cluster.

2. If the cluster uses secure mode, copy the `kaiwudb_certs.tar.gz` file generated in the installation directory after deployment to the current node.

3. Execute the command to join the cluster.

   ::: warning Note
   The following commands list only commonly used startup flags. For all startup flags supported by KWDB, see [Startup Flags](../db-operation/cluster-settings-config.md).
   :::

   - Secure mode

      ```Shell
      <kwbase_path>/kwbase start-single-replica --certs-dir=<cert_path> --store=<data_dir> --brpc-addr=:27257 --listen-addr=<new_node>:<kaiwudb_port> --http-addr=<new_node>:<rest_port> --join=<node_address_list> --background
      ```

   - Insecure mode

      ```Shell
      <kwbase_path>/kwbase start-single-replica --insecure --store=<data_dir> --brpc-addr=:27257 --listen-addr=<new_node>:26257 --http-addr=<new_node>:<rest_port> --join=<node_address_list> --background
      ```

4. Check the cluster node status:

   - Secure mode

      ```Shell
      <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
      ```

   - Insecure mode

      ```Bash
      <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>]
      ```

## Scaling Down a Cluster

Currently, single-replica clusters do not support scale-down operations.

In a multi-replica cluster, when you actively remove a node, KWDB will allow the node to complete requests currently being executed, reject any new requests, and migrate range replicas and leases on that node to other nodes to ensure smooth data migration. The removed node can be permanently decommissioned as needed, maximizing system availability and data integrity.

::: warning Note

- When removing a node, you must ensure that other nodes are available to take over the range replicas from that node. If no other nodes are available, the removal operation will hang indefinitely.
- KWDB clusters use a three-replica mechanism with a minimum cluster node count of 3. Further scale-down is not allowed.
- If replica constraints have been previously set through the `CONFIGURE ZONE` statement and the constraint rules include the node to be scaled down, this may affect the normal operation of cluster scale-down. In this case, the constraint rules need to be reconfigured to remove the node being scaled down from the rules before cluster scale-down can resume normally.

:::

During scale-down, the total disk capacity required by the cluster may temporarily increase due to data migration. Once scale-down is complete, the total disk capacity will return to pre-scale-down levels, with only minor differences.

During scale-down, DDL operations related to tag indexes may fail and data queries may be incomplete due to data partition migration. However, after scale-down completes, operations will execute successfully and data queries will be complete and accurate.

When a decommissioned node rejoins the cluster, the data directory needs to be cleared before it can rejoin as a new node.

**Prerequisites**

- All nodes in the cluster are in a live state (`is_available` and `is_live` are both `true`):

   - Execute the cluster node status view command in the installation directory:

      ```Shell
      ./deploy.sh cluster --status
      ```

   - View node status through the `kwbase node status` command:

      ```Shell
      <kwbase_path>/kwbase node status [--host=<ip:port>] [--insecure | --certs-dir=<path>]
      ```

- The ID of the node to be decommissioned has been obtained:

- There are no unavailable ranges under-replicated ranges.

    ```SQL
    SELECT sum((metrics->>'ranges.unavailable')::DECIMAL)::INT AS ranges_unavailable,
        sum((metrics->>'ranges.underreplicated')::DECIMAL)::INT As ranges_underreplicated
    FROM kwdb_internal.kv_store_status;
    ```

**Steps**

1. Log in to any node in the cluster and execute the node decommission command:

   - Secure mode

      ```Shell
      <kwbase_path>/kwbase node decommission <node_id> --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
      ```

   - Insecure mode

      ```Bash
      <kwbase_path>/kwbase node decommission <node_id> --insecure [--host=<address_of_any_alive_node>]
      ```

2. Check the cluster node status using the following command. When the decommissioned node status changes to `decommissioning` and the number of replicas on the node is reduced to `0`, the decommission is complete.

   - Secure mode

     ```Shell
     <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>] --decommission
     ```

   - Insecure mode

     ```Bash
     <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>] --decommission
     ```

3. (Optional) If you need to completely remove the decommissioned node from the cluster, execute the following command:

   - Secure mode

     ```Bash
     <kwbase_path>/kwbase quit --certs-dir=<cert_path> --host=<decommissioned_node>
     ```

   - Insecure mode

     ```Bash
     <kwbase_path>/kwbase quit --insecure --host=<decommissioned_node>
     ```

4. (Optional) Check whether the cluster node has been removed:

   - Secure mode

     ```Shell
     <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
     ```

   - Insecure mode

      ```shell
      <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>]
      ```