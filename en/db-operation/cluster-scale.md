---
title: Cluster Scaling
id: cluster-scale
---
# Cluster Scaling

KWDB supports dynamic scale-out and scale-in operations to meet varying capacity and performance requirements across different business scenarios. The scaling characteristics vary by cluster type:

| Cluster Type | Scale-Out | Scale-In | Data Redistribution Mechanism | Operation Method |
|--------------|-----------|----------|------------------------------|------------------|
| Multi-Replica Cluster | Supported | Supported | Automatically triggered; balances data across all nodes | Deployment Script / kwbase Commands |
| Single-Replica Cluster | Supported | Not Supported | Applies only to newly created tables; existing data is not migrated | kwbase Commands |

::: warning Note

- **Data Queries**: During scaling operations, data queries may be temporarily incomplete. After the operation completes, the system automatically synchronizes to ensure data completeness and accuracy.
- **DDL Operations**: During scaling operations, DDL operations related to time-series indexes (such as `CREATE INDEX`, `DROP INDEX`) may return timeout errors. Retry these operations after the scaling operation completes.
- **Disk Capacity**: During scaling operations, disk usage may temporarily increase due to data migration. Disk usage returns to normal levels after the operation completes.
- **Operational Recommendations**: Perform scaling operations during off-peak hours to minimize impact on business operations.

:::

## Scale-Out Operations

### Multi-Replica Cluster Scale-Out

KWDB multi-replica clusters support scale-out using either the deployment script or kwbase commands. After scale-out completes, the cluster automatically redistributes data to ensure load balancing.

**Data Redistribution**

After scale-out completes, the system automatically distributes existing data evenly across all nodes by default. To disable automatic redistribution, set the following parameter:

```sql
SET CLUSTER SETTING kv.allocator.ts_consider_rebalance.enabled = false;
```

Avoid frequently executing `ALTER` statements during redistribution, as this may prolong the process.

#### Prerequisites

- KWDB is installed on the nodes to be added using the multi-replica cluster deployment method (see [Cluster Deployment](../deployment/cluster-deployment/script-deployment.md))
- The target cluster is running
- **Additional requirements by method:**
  - **Using deployment script**: The nodes to be added are deployed using the script (`deploy.sh`)
  - **Using kwbase commands**: If using secure mode, the `kaiwudb_certs.tar.gz` certificate file must be available
- User permissions (required only for secure mode):
  - `sudo` permission on the master node to prepare and package certificate files
  - SSH login permission from the master node to the nodes to be added for certificate transfer
  - Write permission to the installation directory on the nodes to be added

#### Using Deployment Script

1. (Optional) If the cluster uses secure mode, prepare and transfer certificate files from the master node to the nodes to be added.

   1. Log in to the cluster master node (the initial deployment node) and navigate to the installation directory:

      ```shell
      cd <install_dir>
      ```

   2. Copy KWDB's security certificates and keys to the current directory:

      ```shell
      sudo cp /etc/kaiwudb/certs/ca.key ./
      sudo cp /etc/kaiwudb/certs/ca.crt ./
      ```

   3. Change the file owner to the kaiwudb user:

      ```shell
      sudo chown kaiwudb:kaiwudb ./ca.key ./ca.crt
      ```

   4. Set certificate file permissions:

      ```shell
      sudo chmod 644 ./ca.crt
      ```

   5. Package the certificate files:

      ```shell
      sudo tar -czf kaiwudb_certs.tar.gz ./ca.key ./ca.crt
      ```

   6. Transfer the archive to the node to be added:

      ```shell
      scp kaiwudb_certs.tar.gz <username>@<new_node_ip>:<install_dir>
      ```

2. Log in to the node to be added and run the deployment script in the installation directory:

   - Secure mode:

      ```shell
      ./deploy.sh join --addr <any_cluster_node_ip>:<port> --tls
      ```

   - Insecure mode:

      ```shell
      ./deploy.sh join --addr <any_cluster_node_ip>:<port>
      ```

   Parameters:

   - `<any_cluster_node_ip>`: The IP address of any alive node in the cluster (e.g., `192.168.122.221`)
   - `<port>`: The KWDB service port (default: `26257`)

3. Verify that the new node has successfully joined:

   ```shell
   kw-status
   ```

#### Using kwbase Commands

1. Log in to the node to be added.

2. If the cluster uses secure mode, copy `kaiwudb_certs.tar.gz` to the current node and extract it to the `/etc/kaiwudb/certs` directory.

3. Start the KWDB node and join it to the cluster:

   ::: warning Note
   The following commands show only commonly used startup flags. For all supported startup flags, see [Startup Flags](../db-operation/cluster-settings-config.md).
   :::

   - Secure mode:

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

   - Insecure mode:

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

   Parameters:

   - `<kwbase_path>`: Directory containing the kwbase binary (default: `/usr/local/kaiwudb/bin` for bare-metal, `/kaiwudb/bin` for container deployment)
   - `<cert_path>`: Directory containing certificates and keys (default: `/etc/kaiwudb/certs`)
   - `<data_dir>`: (Optional) Data and log storage location (default: `/var/lib/kaiwudb`)
   - `<new_node_ip>:<kaiwudb_port>`: (Optional) New node IP address and KWDB service port (default port: `26257`)
   - `<new_node_ip>:<rest_port>`: (Optional) New node IP address and RESTful API port (default port: `8080`)
   - `<node_address_list>`: Comma-separated list of existing cluster node addresses to connect to
   - `--background`: (Optional) Runs the process in the background

4. Check the cluster node status:

   - Secure mode:

      ```shell
      <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
      ```

   - Insecure mode:

      ```shell
      <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>]
      ```

   Parameters:

   - `<kwbase_path>`: Directory containing the kwbase binary (default: `/usr/local/kaiwudb/bin` for bare-metal, `/kaiwudb/bin` for container deployment)
   - `<cert_path>`: Certificate directory (default: `/etc/kaiwudb/certs`)
   - `--host=<address_of_any_alive_node>`: (Optional) Node on which to execute the command (must be alive; format: `<ip>:<port>`; default: `127.0.0.1:26257`)
  
### Single-Replica Cluster Scale-Out

KWDB single-replica cluster scale-out is straightforward—simply add new nodes to the existing cluster.

#### Prerequisites

- KWDB is installed on the new nodes using the single-replica deployment method (see [Cluster Deployment](../deployment/cluster-deployment/script-deployment.md))
- The target cluster is running
- If the cluster is deployed in secure mode, the `kaiwudb_certs.tar.gz` file is available

#### Steps

1. Log in to the node to be added.

2. If the cluster is deployed in secure mode, copy the `kaiwudb_certs.tar.gz` file to the current node and extract it to the `/etc/kaiwudb/certs` directory.

3. Start the KWDB node and join it to the cluster:

   ::: warning Note
   The following commands show only commonly used startup flags. For all supported startup flags, see [Startup Flags](../db-operation/cluster-settings-config.md).
   :::

   - Secure mode:

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

   - Insecure mode:

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

4. Check the cluster node status:

   - Deployment script:

      ```shell
      kw-status
      ```

   - kwbase command:

      ```shell
      # Secure mode
      <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]

      # Insecure mode
      <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>]
      ```

## Scale-In Operations

Single-replica clusters do not currently support scale-in operations.

KWDB multi-replica clusters support scale-in using either the deployment script or kwbase commands. When you remove a node, KWDB allows it to complete requests in progress, rejects new requests, and migrates range replicas and range leases to other nodes to ensure smooth data migration. Removed nodes can be permanently decommissioned based on your requirements to maximize system availability and data integrity.

::: warning Note

- When removing a node, ensure that other nodes are available to take over its range replicas. If no other nodes are available, the removal operation will hang indefinitely.
- KWDB clusters use a three-replica mechanism with a minimum of 3 nodes. Scale-in below this minimum is not allowed.
- If you set replica constraints through the `CONFIGURE ZONE` statement and the constraint rules include the node to be removed, this may affect the scale-in operation. Reconfigure the constraint rules to exclude this node before proceeding.

:::

To add a decommissioned node back to the cluster, you must first clear its data directory and rejoin it as a new node.

### Prerequisites

- All cluster nodes are alive (`is_available` and `is_live` are both `true`):

  - Use the Deployment script:

      ```shell
      kw-status
      ```

  - Use the cluster status command (in the installation directory):

      ```shell
      ./deploy.sh cluster --status
      ```

  - Use the `kwbase node status` command:

      ```shell
      <kwbase_path>/kwbase node status [--host=<ip:port>] [--insecure | --certs-dir=<path>]
      ```

- You have obtained the ID of the node to be decommissioned

- There are no unavailable or under-replicated ranges:

   ```sql
   SELECT sum((metrics->>'ranges.unavailable')::DECIMAL)::INT AS ranges_unavailable,
      sum((metrics->>'ranges.underreplicated')::DECIMAL)::INT AS ranges_underreplicated
   FROM kwdb_internal.kv_store_status;
   ```

### Using Deployment Script

1. Log in to the node to be removed and run the decommission command in the installation directory:

   ```shell
   ./deploy.sh decommission
   ```

2. In the same directory, view the `decommission_progress` file to monitor the remaining replica count.

3. Once the remaining replica count reaches 0, stop the database:

   ```shell
   systemctl stop kaiwudb
   ```

4. Confirm that the node has been successfully removed:

   ```shell
   kw-status
   ```

### Using kwbase Commands

1. Log in to any node in the cluster and run the decommission command:

   - Secure mode:

      ```shell
      <kwbase_path>/kwbase node decommission <node_id> --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
      ```

   - Insecure mode:

      ```bash
      <kwbase_path>/kwbase node decommission <node_id> --insecure [--host=<address_of_any_alive_node>]
      ```

2. Check the cluster node status. When the decommissioned node status changes to `decommissioning` and the number of replicas on the node is reduced to `0`, the decommission is complete.

   - Secure mode:

     ```shell
     <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>] --decommission
     ```

   - Insecure mode:

     ```bash
     <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>] --decommission
     ```

3. (Optional) To completely remove the decommissioned node from the cluster:

   - Secure mode:

     ```bash
     <kwbase_path>/kwbase quit --certs-dir=<cert_path> --host=<decommissioned_node>
     ```

   - Insecure mode:

     ```bash
     <kwbase_path>/kwbase quit --insecure --host=<decommissioned_node>
     ```

4. (Optional) Verify that the node has been removed:

   - Deployment script:

      ```shell
      kw-status
      ```

   - kwbase command:

      ```shell
      # Secure mode
      <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
      
      # Insecure mode
      <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>]
      ```