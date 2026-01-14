---
title: Cluster Scaling
id: cluster-scale
---
# Cluster Scaling

## Scale-Out Operations

Both KWDB multi-replica clusters and single-replica clusters support scale-out operations.

- After scaling out a multi-replica cluster, the system automatically triggers data redistribution. For more information, see [Scaling Out Multi-Replica Clusters](#scaling-out-multi-replica-clusters).
- After scaling out a single-replica cluster, the system does not redistribute existing data and only balances data when new tables are created. For more information, see [Scaling Out Single-Replica Clusters](#scaling-out-single-replica-clusters).

::: warning Note
During cluster scale-out, there may be brief periods where data queries are incomplete. After the operation completes, the system will automatically synchronize to ensure data integrity and query completeness.
:::

### Scaling Out Multi-Replica Clusters

To scale out a KWDB multi-replica cluster, you only need to add new nodes to the cluster. By default, the cluster automatically completes data redistribution. If needed, you can disable this automatic redistribution using the `kv.allocator.ts_consider_rebalance.enabled` parameter.

During the scale-out process, note the following: The total disk capacity required by the cluster may temporarily increase due to data migration but returns to normal levels once complete. DDL operations related to time-series indexes may fail during scale-out but execute successfully afterward. Additionally, frequent execution of `ALTER` statements may delay the automatic data rebalancing process.

**Prerequisites**

- KWDB is installed on the new nodes using the multi-replica deployment method. For instructions, see [Cluster Deployment](../deployment/cluster-deployment/script-deployment.md).
- The target cluster is running.
- If the cluster is deployed in secure mode, the `kaiwudb_certs.tar.gz` file is available.

**Steps**

1. Log in to the node that needs to join the cluster.

2. If the cluster is deployed in secure mode, copy the `kaiwudb_certs.tar.gz` file generated in the installation directory after deployment to the current node.

3. Run the following command to join the node to the cluster.

   ::: warning Note
   The following commands show only commonly used startup flags. For all startup flags supported by KWDB, see [Startup Flags](../db-operation/cluster-settings-config.md).
   :::

   - Secure mode

      ```shell
      <kwbase_path>/kwbase start --certs-dir=<cert_path> --store=<data_dir> --brpc-addr=:27257 --listen-addr=<new_node>:<kaiwudb_port> --http-addr=<new_node>:<rest_port> --join=<node_address_list> --background
      ```

   - Insecure mode

      ```shell
      <kwbase_path>/kwbase start --insecure --store=<data_dir> --brpc-addr=:27257 --listen-addr=<new_node>:26257 --http-addr=<new_node>:<rest_port> --join=<node_address_list> --background
      ```

   Parameters:

   - `<kwbase_path>`: The directory where the kwbase binary file is located. The default directory is `/usr/local/kaiwudb/bin` for bare-metal deployment and `/kaiwudb/bin` for container deployment.

   - `<cert_path>`: Specifies the folder containing certificates and keys. The default storage location is `/etc/kaiwudb/certs`.

   - `<data_dir>`: (Optional) specifies the data and log storage location for the node. The default location is `/var/lib/kaiwudb`.

   - `<new_node>:<kaiwudb_port>`: (Optional) specifies the new node address and KWDB service port. The default port is `26257`.

   - `<new_node>:<rest_port>`: (Optional) specifies the new node address and the port for RESTful API. The default port is `8080`.

   - `<node_address_list>`: List of cluster nodes to connect to. Supports one or multiple node addresses, separated by commas.

   - `--background`: (Optional) runs the process in the background.

4. Check the cluster node status using the following command:

   - Deployment script

      ```shell
      kw-status
      ```

   - kwbase command

      ```shell
      # Secure mode
      <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
   
      # Insecure mode
      <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>]
      ```

   Parameters:

   - `<kwbase_path>`: The directory where the kwbase binary file is located. The default directory is `/usr/local/kaiwudb/bin` for bare-metal deployment and `/kaiwudb/bin` for container deployment.
   - `cert_path`: Certificate directory. The default storage location is `/etc/kaiwudb/certs`.
   - `--host=<address_of_any_alive_node>`: (Optional) specifies the node on which to execute the command. This node must be healthy. The address format is `<ip>:<port>`. If not specified, the default is `127.0.0.1:26257`.

### Scaling Out Single-Replica Clusters

To scale out a KWDB single-replica cluster, you only need to add the nodes to the cluster.

**Prerequisites**

- KWDB is installed on the new nodes using the single-replica deployment method. For more information, see [Cluster Deployment](../deployment/cluster-deployment/script-deployment.md).
- The target cluster is running.
- If the cluster is deployed in secure mode, the `kaiwudb_certs.tar.gz` file is available.

**Steps**

1. Log in to the node that needs to join the cluster.

2. If the cluster is deployed in secure mode, copy the `kaiwudb_certs.tar.gz` file generated in the installation directory after deployment to the current node.

3. Run the following command to join the node to the cluster.

   ::: warning Note
   The following commands show only commonly used startup flags. For all startup flags supported by KWDB, see [Startup Flags](../db-operation/cluster-settings-config.md).
   :::

   - Secure mode

      ```shell
      <kwbase_path>/kwbase start-single-replica --certs-dir=<cert_path> --store=<data_dir> --brpc-addr=:27257 --listen-addr=<new_node>:<kaiwudb_port> --http-addr=<new_node>:<rest_port> --join=<node_address_list> --background
      ```

   - Insecure mode

      ```shell
      <kwbase_path>/kwbase start-single-replica --insecure --store=<data_dir> --brpc-addr=:27257 --listen-addr=<new_node>:26257 --http-addr=<new_node>:<rest_port> --join=<node_address_list> --background
      ```

4. Check the cluster node status using the following command:

   - Deployment script

      ```shell
      kw-status
      ```

   - kwbase command

      ```shell
      # Secure mode
      <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
      
      # Insecure mode
      <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>]
      ```

## Scale-Down Operations

Currently, single-replica clusters do not support scale-down operations.

In a multi-replica cluster, when a node is decommissioned, KWDB allows the node to complete requests currently in progress, rejects new requests, and migrates range replicas and range leases to other nodes to ensure smooth data migration. The decommissioned node can be permanently removed from the cluster if required, ensuring system availability and data integrity.

::: warning Note

- When removing a node, you must ensure that other nodes are available to take over the range replicas from that node. If no other nodes are available, the decommission operation will not complete.
- KWDB clusters use a three-replica mechanism with a minimum cluster node count of 3. Further scale-down is not allowed.
- If replica constraints were set through the `CONFIGURE ZONE` statement and the constraint rules include the node to be scaled down, this may affect the scale-down operation. In this case, the constraint rules need to be reconfigured to remove the node being scaled down from the rules before the scale-down operation can proceed.

:::

During the scale-down process, note the following: The total disk capacity required by the cluster may temporarily increase due to data migration but returns to normal levels once complete. DDL operations related to time-series indexes may fail and data queries may be incomplete due to data partition migration. However, after the operation completes, operations execute successfully and data queries are complete and accurate.

If you want to add a decommissioned node back to the cluster, you must clear its data directory first.

**Prerequisites**

- All nodes in the cluster are alive (`is_available` and `is_live` are both `true`).

   - Use the deployment script:

      ```shell
      kw-status
      ```

   - Use the `kwbase node status` command:

      ```shell
      <kwbase_path>/kwbase node status [--host=<ip:port>] [--insecure | --certs-dir=<path>]
      ```

- You have obtained the ID of the node to be decommissioned.

- There are no unavailable ranges and under-replicated ranges.

    ```sql
    SELECT sum((metrics->>'ranges.unavailable')::DECIMAL)::INT AS ranges_unavailable,
        sum((metrics->>'ranges.underreplicated')::DECIMAL)::INT As ranges_underreplicated
    FROM kwdb_internal.kv_store_status;
    ```

**Steps**

1. Log in to any node in the cluster and execute the node decommission command:

   - Secure mode

      ```shell
      <kwbase_path>/kwbase node decommission <node_id> --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
      ```

   - Insecure mode

      ```bash
      <kwbase_path>/kwbase node decommission <node_id> --insecure [--host=<address_of_any_alive_node>]
      ```

2. Check the cluster node status using the following command. When the decommissioned node status changes to `decommissioning` and the number of replicas on the node is reduced to `0`, the decommission is complete.

   - Secure mode

     ```shell
     <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>] --decommission
     ```

   - Insecure mode

     ```bash
     <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>] --decommission
     ```

3. (Optional) To completely remove the decommissioned node from the cluster, execute the following command:

   - Secure mode

     ```bash
     <kwbase_path>/kwbase quit --certs-dir=<cert_path> --host=<decommissioned_node>
     ```

   - Insecure mode

     ```bash
     <kwbase_path>/kwbase quit --insecure --host=<decommissioned_node>
     ```

4. (Optional) Check whether the cluster node has been removed using the following command:

   - Deployment script

      ```shell
      kw-status
      ```

   - kwbase command

      ```shell
      # Secure mode
      <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
      
      # Insecure mode
      <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>]
      ```