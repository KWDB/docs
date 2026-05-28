---
title: Cluster Scaling
id: cluster-scale
---

# Cluster Scaling

KWDB supports dynamic scale-out and scale-in operations to meet different capacity and performance requirements across business scenarios. The scaling characteristics vary by cluster type:

| Cluster Type | Scale-Out | Scale-In | Data Redistribution Mechanism | Operation Method |
| ------------ | --------- | -------- | ------------------------------ | ---------------- |
| Multi-Replica Cluster | Supported | Supported | Automatically triggered to balance data across all nodes | Installer / Command Line |
| Single-Replica Cluster | Supported | Not Supported | Only applies to newly created tables; existing data is not migrated | Installer / Command Line |

::: warning Note

- **DDL Operations**: During scaling, DDL operations related to time-series indexes, such as `CREATE INDEX` and `DROP INDEX`, may time out. Retry them after the scaling operation finishes.
- **Disk Capacity**: During scaling, disk usage may temporarily increase because of data migration. It returns to normal after the operation completes.
- **Operational Recommendation**: Perform scaling during off-peak hours to minimize impact on business operations.

:::

## Scale-Out

### Multi-Replica Cluster Scale-Out

KWDB multi-replica clusters support scale-out using either the installer or the command line. After the scale-out completes, the cluster automatically performs data redistribution to ensure load balancing.

#### Data Redistribution

After scale-out finishes, the system automatically distributes existing data evenly across all nodes by default. To disable automatic redistribution, set the following parameter:

```sql
SET CLUSTER SETTING kv.allocator.ts_consider_rebalance.enabled = false;
```

Avoid frequent `ALTER` statements during redistribution, because they may prolong the process.

#### Multi-Replica Prerequisites

- The nodes to be added have not installed KWDB yet.
- The target cluster is running.
- The installer-based scale-out method also requires:
  - You have obtained the KWDB installer (`.run` file).
  - The execution node (any node in the cluster) can SSH into the target node and has write permission in the target node's installation directory.
  - The user is `root` or a normal user with `sudo` privileges.
  - (Optional) If the cluster uses secure mode, you must first build a temporary certificate directory on the target node and grant read permissions:

    ```bash
    sudo rm -rf /tmp/kaiwudb_certs
    sudo mkdir -p /tmp/kaiwudb_certs
    sudo cp -r /etc/kaiwudb/certs/*ca* /tmp/kaiwudb_certs/
    sudo chmod +r /tmp/kaiwudb_certs/*ca*
    sudo ls -ltr /tmp/kaiwudb_certs
    ```

- The command-line scale-out method in secure deployment mode also requires:
  - The `kaiwudb_certs.tar.gz` certificate file is prepared.
  - The master node has `sudo` privileges to prepare and package the certificates.
  - The master node can SSH into the target node to transfer the certificates.
  - The target node has write permission in the installation directory.

#### Installer Scale-Out (Single-Replica) (Multi-Replica)

##### CLI Mode (Single-Replica) (Multi-Replica)

1. Copy the KWDB installer to the cluster node where you will perform the scale-out and grant it execute permission:

   ```bash
   chmod +x KWDB-*.run
   ```

2. Start the installer in CLI mode:

   ```bash
   ./KWDB-*.run -c
   # or
   ./KWDB-*.run --cli
   ```

3. In the main menu, enter `3` to select **Install KWDB and Join the Cluster**:

   ```plain
   1. Install KWDB
   2. Uninstall KWDB
   3. Install KWDB and Join the Cluster
   4. Upgrade Nodes
   5. Exit

   Please enter the operation [1-5]:
   ```

4. Select the appropriate join mode based on the current cluster type:

   ```plain
   Join KWDB Cluster
   1. Join a Single-Replica Cluster
   2. Join a Three-Replica Cluster
   3. Return to the Main Menu

   Please select [1-3]:
   ```

5. Enter the IP address of any cluster node and the KWDB service port (default `26257`):

   ```plain
   Configure cluster address
   Please enter the address of any cluster node:
   Please enter the corresponding KWDB service port:
   ```

6. Configure the CA certificate and private key path. For insecure mode, you can skip this configuration. Select whether to install for all users:

   ```plain
   Configure CA certificate directory
   Please enter the CA certificate and private key path:
   Install for all users (y/N):
   ```

7. The installer automatically generates a configuration template and opens the editor. After you confirm or modify the settings and save and exit, the installer starts the installation and joins the cluster automatically.

   Example configuration:

   ```ini
   [global]
   # Whether to enable secure mode
   secure_mode=tls
   # Admin UI port
   rest_port=8080
   # Database service port
   kaiwudb_port=26257
   # Data transfer port
   brpc_port=27257
   # Data directory
   data_root=/var/lib/kaiwudb

   [node1]
   host=192.168.122.224
   # SSH port
   port=22
   # SSH username
   user=admin
   # SSH password
   passwd=******
   ```

   Parameter description:

   | Parameter | Description |
   |-----------|-------------|
   | `secure_mode` | Secure mode; it must match the target cluster. |
   | `rest_port` | KWDB Web port, default `8080`. |
   | `kaiwudb_port` | KWDB service port, default `26257`. |
   | `brpc_port` | Data transfer port, default `27257`. |
   | `data_root` | Data directory, default `/var/lib/kaiwudb`. |
   | `host` | IP address of the node to be added. |
   | `port` | SSH port, default `22`. |
   | `user` | SSH username. |
   | `passwd` | SSH password. |

8. After installation completes, verify that the new node has joined the cluster:

   ```shell
   kw-status
   ```

##### Terminal Graphical Interaction Mode

1. Copy the KWDB installer to the cluster node where you will perform the scale-out and grant it execute permission:

   ```bash
   chmod +x KWDB-*.run
   ```

2. Start the installer in terminal graphical interaction mode:

   ```bash
   ./KWDB-*.run -i
   # or
   ./KWDB-*.run --interact
   ```

3. In the main menu, use the arrow keys to select **Install KWDB and Join the Cluster**, then press Enter.

4. Enter the installation settings menu and configure the following items in order:

   | Option | Description |
   |--------|-------------|
   | Set secure mode | Must match the target cluster's secure mode. |
   | Set database service port | KWDB service port, default `26257`. |
   | Set Admin UI port | KWDB Web service port, default `8080`. |
   | Set data transfer port | Data transfer port between the time-series engines, default `27257`. |
   | Select deployment mode | Must match the target cluster's deployment mode. |
   | Add node | Enter the host name, port, username, and password of the node to be added. |
   | Set data directory | Data directory, default `/var/lib/kaiwudb`. |
   | Set target cluster address | IP address of any node in the target cluster. |
   | Set target cluster KWDB service port | The target cluster's KWDB service port. |
   | Set CA certificate path | In secure mode, upload the target cluster's CA certificate and private key files by selecting the path in the file picker. |

5. Select whether to install for all users.

6. After all settings are complete, select **Start Installation** and press Enter to install and join the cluster.

7. After installation completes, verify that the new node has joined the cluster:

   ```shell
   kw-status
   ```

#### Command-Line Scale-Out (Single-Replica) (Multi-Replica)

1. Log in to the node to be added.

2. If the cluster uses secure deployment mode, copy `kaiwudb_certs.tar.gz` to the current node and extract it to `/etc/kaiwudb/certs`.

3. Run the join-cluster command:

   ::: warning Note
   The following commands only list common startup parameters. For all supported startup parameters, see [Startup Flags](../db-operation/cluster-settings-config.md).
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

   Parameter description:

   - `<kwbase_path>`: Directory of the kwbase binary. The default path is `/usr/local/kaiwudb/bin` for bare-metal deployment and `/kaiwudb/bin` for container deployment.
   - `<cert_path>`: Directory that stores certificates and keys. The default location is `/etc/kaiwudb/certs`.
   - `<data_dir>`: Optional. Specifies the data and log storage path for the node. The default path is `/var/lib/kaiwudb`.
   - `<new_node_ip>:<kaiwudb_port>`: Optional. Specifies the new node address and KWDB service port. The default port is `26257`.
   - `<new_node_ip>:<rest_port>`: Optional. Specifies the new node address and the KWDB RESTful port. The default port is `8080`.
   - `<node_address_list>`: List of cluster nodes to connect to. Separate multiple addresses with commas.
   - `--background`: Optional. Runs the process in the background.

4. Check the cluster node status:

   - Secure mode:

     ```shell
     <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
     ```

   - Insecure mode:

     ```shell
     <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>]
     ```

   Parameter description:

   - `<kwbase_path>`: Directory of the kwbase binary. The default path is `/usr/local/kaiwudb/bin` for bare-metal deployment and `/kaiwudb/bin` for container deployment.
   - `<cert_path>`: Certificate directory. The default location is `/etc/kaiwudb/certs`.
   - `--host=<address_of_any_alive_node>`: Optional. Specifies the node to run the command on. The node must be healthy. The format is `<ip>:<port>`. If not specified, the default is `127.0.0.1:26257`.

### Single-Replica Cluster Scale-Out

KWDB single-replica clusters support both installer scale-out and command-line scale-out.

#### Single-Replica Prerequisites

- The nodes to be added have not installed KWDB yet.
- The target cluster is running.
- The installer-based scale-out method also requires:
  - You have obtained the KWDB installer (`.run` file).
  - The execution node (any node in the cluster) can SSH into the target node and has write permission in the target node's installation directory.
  - The user is `root` or a normal user with passwordless `sudo` configured.
  - (Optional) If the cluster uses secure mode, you must first build a temporary certificate directory on the target node and grant read permissions:

    ```bash
    sudo rm -rf /tmp/kaiwudb_certs
    sudo mkdir -p /tmp/kaiwudb_certs
    sudo cp -r /etc/kaiwudb/certs/*ca* /tmp/kaiwudb_certs/
    sudo chmod +r /tmp/kaiwudb_certs/*ca*
    sudo ls -ltr /tmp/kaiwudb_certs
    ```

- The command-line scale-out method in secure deployment mode also requires:
  - The `kaiwudb_certs.tar.gz` certificate file is prepared.
  - The master node has `sudo` privileges to prepare and package the certificates.
  - The master node can SSH into the target node to transfer the certificates.
  - The target node has write permission in the installation directory.

#### Installer Scale-Out

##### CLI Mode

1. Copy the KWDB installer to the cluster node where you will perform the scale-out and grant it execute permission:

   ```bash
   chmod +x KWDB-*.run
   ```

2. Start the installer in CLI mode:

   ```bash
   ./KWDB-*.run -c
   # or
   ./KWDB-*.run --cli
   ```

3. In the main menu, enter `3` to select **Install KWDB and Join the Cluster**:

   ```plain
   1. Install KWDB
   2. Uninstall KWDB
   3. Install KWDB and Join the Cluster
   4. Upgrade Nodes
   5. Exit

   Please enter the operation [1-5]:
   ```

4. Select the appropriate join mode based on the current cluster type:

   ```plain
   Join KWDB Cluster
   1. Join a Single-Replica Cluster
   2. Join a Three-Replica Cluster
   3. Return to the Main Menu

   Please select [1-3]:
   ```

5. Enter the IP address of any cluster node and the KWDB service port (default `26257`):

   ```plain
   Configure cluster address
   Please enter the address of any cluster node:
   Please enter the corresponding KWDB service port:
   ```

6. Configure the CA certificate and private key path. For insecure mode, you can skip this configuration. Select whether to install for all users:

   ```plain
   Configure CA certificate directory
   Please enter the CA certificate and private key path:
   Install for all users (y/N):
   ```

7. The installer automatically generates a configuration template and opens the editor. After you confirm or modify the settings and save and exit, the installer starts the installation and joins the cluster automatically.

   Example configuration:

   ```ini
   [global]
   # Whether to enable secure mode
   secure_mode=tls
   # Admin UI port
   rest_port=8080
   # Database service port
   kaiwudb_port=26257
   # Data transfer port
   brpc_port=27257
   # Data directory
   data_root=/var/lib/kaiwudb

   [node1]
   host=192.168.122.224
   # SSH port
   port=22
   # SSH username
   user=admin
   # SSH password
   passwd=******
   ```

   Parameter description:

   | Parameter | Description |
   |-----------|-------------|
   | `secure_mode` | Secure mode; it must match the target cluster. |
   | `rest_port` | KWDB Web port, default `8080`. |
   | `kaiwudb_port` | KWDB service port, default `26257`. |
   | `brpc_port` | Data transfer port, default `27257`. |
   | `data_root` | Data directory, default `/var/lib/kaiwudb`. |
   | `host` | IP address of the node to be added. |
   | `port` | SSH port, default `22`. |
   | `user` | SSH username. |
   | `passwd` | SSH password. |

8. After installation completes, verify that the new node has joined the cluster:

   ```shell
   kw-status
   ```

##### Terminal Graphical Interaction Mode

1. Copy the KWDB installer to the cluster node where you will perform the scale-out and grant it execute permission:

   ```bash
   chmod +x KWDB-*.run
   ```

2. Start the installer in terminal graphical interaction mode:

   ```bash
   ./KWDB-*.run -i
   # or
   ./KWDB-*.run --interact
   ```

3. In the main menu, use the arrow keys to select **Install KWDB and Join the Cluster**, then press Enter.

4. Configure the following settings in the installation parameter menu:

   | Option | Description |
   |--------|-------------|
   | Set secure mode | Must match the target cluster's secure mode. |
   | Set database service port | KWDB service port, default `26257`. |
   | Set Admin UI port | KWDB Web service port, default `8080`. |
   | Set data transfer port | Data transfer port between the time-series engines, default `27257`. |
   | Select deployment mode | Must match the target cluster's deployment mode. |
   | Add node | Enter the host name, port, username, and password of the node to be added. |
   | Set data directory | Data directory, default `/var/lib/kaiwudb`. |
   | Set target cluster address | IP address of any node in the target cluster. |
   | Set target cluster KWDB service port | The target cluster's KWDB service port. |
   | Set CA certificate path | In secure mode, upload the target cluster's CA certificate and private key files by selecting the path in the file picker. |

5. Select whether to install for all users.

6. After all settings are complete, select **Start Installation** and press Enter to install and join the cluster.

7. After installation completes, verify that the new node has joined the cluster:

   ```shell
   kw-status
   ```

#### Command-Line Scale-Out

1. Log in to the node to be added.

2. If the cluster uses secure deployment mode, copy `kaiwudb_certs.tar.gz` to the current node and extract it to `/etc/kaiwudb/certs`.

3. Run the join-cluster command:

   ::: warning Note
   The following commands only list common startup parameters. For all supported startup parameters, see [Startup Flags](../db-operation/cluster-settings-config.md).
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

   - Installer deployment:

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

## Scale-In

Single-replica clusters do not currently support scale-in operations.

KWDB multi-replica clusters support command-line scale-in. When a node is removed, KWDB allows the node to finish in-flight requests, rejects new requests, and migrates its range replicas and range leases to other nodes to ensure smooth data migration. The removed node can be permanently decommissioned according to your needs to maximize system availability and data integrity.

::: warning Note

- When removing a node, make sure that other nodes are available to take over its range replicas. If no other nodes are available, the removal operation hangs indefinitely.
- KWDB clusters use a three-replica mechanism with a minimum of 3 nodes. Scale-in below this minimum is not allowed.
- If you previously set replica constraints by using the `CONFIGURE ZONE` statement and the rules include the node to be removed, this may affect the scale-in operation. Reconfigure the constraint rules to exclude the node before proceeding.

:::

After a node is decommissioned, if you need to add it back to the cluster, clear its data directory first and then rejoin it as a new node.

### Scale-In Prerequisites

- All cluster nodes are alive (`is_available` and `is_live` are both `true`):

  - Installer deployment:

    ```shell
    kw-status
    ```

  - Use `kwbase node status` to inspect node status:

    ```shell
    <kwbase_path>/kwbase node status [--host=<ip:port>] [--insecure | --certs-dir=<path>]
    ```

- You have obtained the ID of the node to be decommissioned.

- There are no unavailable ranges or under-replicated ranges:

  ```sql
  SELECT sum((metrics->>'ranges.unavailable')::DECIMAL)::INT AS ranges_unavailable,
         sum((metrics->>'ranges.underreplicated')::DECIMAL)::INT AS ranges_underreplicated
  FROM kwdb_internal.kv_store_status;
  ```

### Steps

1. Log in to any node in the cluster and run the decommission command:

   - Secure mode:

     ```shell
     <kwbase_path>/kwbase node decommission <node_id> --certs-dir=<cert_path> [--host=<address_of_any_alive_node>]
     ```

   - Insecure mode:

     ```bash
     <kwbase_path>/kwbase node decommission <node_id> --insecure [--host=<address_of_any_alive_node>]
     ```

2. Check the cluster node status. When the decommissioned node status changes to `decommissioning` and the number of replicas on the node drops to `0`, the decommission is complete.

   - Secure mode:

     ```shell
     <kwbase_path>/kwbase node status --certs-dir=<cert_path> [--host=<address_of_any_alive_node>] --decommission
     ```

   - Insecure mode:

     ```bash
     <kwbase_path>/kwbase node status --insecure [--host=<address_of_any_alive_node>] --decommission
     ```

3. (Optional) To remove the decommissioned node from the cluster completely, run the following command:

   - Secure mode:

     ```bash
     <kwbase_path>/kwbase quit --certs-dir=<cert_path> --host=<decommissioned_node>
     ```

   - Insecure mode:

     ```bash
     <kwbase_path>/kwbase quit --insecure --host=<decommissioned_node>
     ```

4. (Optional) Verify that the node has been removed:

   - Installer deployment:

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