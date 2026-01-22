---
title: Deploy Using Scripts
id: script-deployment
---

# Deploy Using Scripts

During deployment, the system verifies configuration files, runtime environment, hardware setup, and software dependencies. The installation will proceed with a warning if hardware requirements are not met, but will abort with error messages if required software dependencies are missing.

All deployment activities are logged in the `log` directory within `kwdb_install`. If an error occurs during deployment, you can find error prompts in the terminal output and detailed information in the log files.

## Prerequisites

**System Requirements**:

- All target nodes meet the requirements for hardware, operating system, and software dependencies.
- Network requirements:
  - Network connectivity: All nodes are network-connected.
  - Location: All nodes are located in the same data center.
  - Ports: All required ports are open and accessible.
  - Network latency between machines: Less than 50 ms.
  - Clock synchronization between nodes: less than 500 ms.
- The bare-metal or container installation package is obtained.

**User Access Requirements**:

- SSH passwordless authentication configured between the deployment node and all cluster nodes.
- One of the following user permissions:
  - Root user access
  - Regular user with `sudo` privileges:
    - Users with passwordless `sudo` won't need to enter passwords during installation.
    - Users without passwordless `sudo` will be prompted for passwords when needed.
  - For container deployment: regular users must be in the docker group (add with `sudo usermod -aG docker $USER`).

## Steps

1. Log in to the deployment node, navigate to the `kwdb_install` directory and edit the `deploy.cfg` file.

    Example:

    ```yaml
    [global]
    # Whether to turn on secure mode
    secure_mode=tls
    # Management KWDB user
    management_user=kaiwudb
    # KWDB cluster http port
    rest_port=8080
    # KWDB service port
    kaiwudb_port=26257
    # KWDB brpc port
    brpc_port=27257
    # KWDB data directory
    data_root=/var/lib/kaiwudb
    # CPU usage[0-1]
    cpu=1

    [local]
    # local node configuration
    node_addr=192.168.122.221

    [cluster]
    # remote node addr,split by ','
    node_addr=192.168.122.222,192.168.122.223
    # ssh info
    ssh_port=22
    ssh_user=admin

    # [additional]
    # IPs=127.0.0.3,127.0.0.4
    ```

    Parameters:

    | Configuration Level | Parameter | Description |
    |---|---|---|
    | **global** | `secure_mode` | Defines the security mode. Options include:<br>- `insecure`: Enables insecure mode.<br>- `tls`: (Default) Enable TLS mode. This generates TLS certificates for clients or application connections, stored in `/etc/kaiwudb/certs`.|
    | | `management_user` | The user account for managing KWDB, set to `kaiwudb` by default. After installation, KWDB creates this user and a user group with the same name. |
    | | `rest_port` | Port for web services (default: `8080`). |
    | | `kaiwudb_port` | Port for client, application and node connections (default: `26257`). |
    | | `brpc_port` | The brpc communication port between KWDB time-series engines, used for inter-node communication (default: `27257`). |
    | | `data_root` | Data directory (default: `/var/lib/kaiwudb`). |
    | | `cpu` | (Optional) Specifies CPU usage for KWDB on the node. The default is unlimited. The value range is [0,1], with a precision of up to two decimal places. After deployment, you can also adjust the CPU resource limit for KWDB. For more information, see [Configure Bare-Metal Cluster](../cluster-config/cluster-config-bare-metal.md) or [Configure Container Cluster](../cluster-config/cluster-config-docker.md).<br>**Note:** For bare-metal deployment, if the environment is Ubuntu 18.04, you need to modify the `CPUQuota` value in the `kaiwudb.service` file after the deployment is complete. Specifically, change any decimal values to integers (e.g., change `180.0%` to `180%`) to ensure the setting takes effect. For instructions, see [CPU usage configuration](../cluster-config/cluster-config-bare-metal.md#manage-cpu-resources). |
    | **local** | `node_addr` | The IP address for client and application connection. The default listening address is `0.0.0.0`, meaning the node will listen on `kaiwudb_port` across all IP addresses on the host. |
    | **cluster** | `cluster_node_ips` | The IP addresses of remote nodes. The IP addresses of each node should be separated by commas (`,`), and there must be at least two remote nodes. |
    | | `ssh_port` | The SSH port used for remote node access; it must be identical across all nodes. |
    | | `ssh_user` | The SSH username for remote node login; it must be identical across all nodes. |
    | **additional** <br>(Primary-standby node configuration) | `IPs` | (Optional) Used when deploying primary-standby clusters in secure mode, not supported by KWDB. |

2. Install the KWDB cluster.

   - Multi-replica clusters:

        ```shell
        ./deploy.sh install --multi-replica
        ```

   - Single-replica clusters:

        ```shell
        ./deploy.sh install --single-replica
        ```

3. After verifying that the configuration is correct, enter `Y` or `y`. To return and modify the `deploy.cfg` configuration file, enter `N` or `n`.

    ```shell
    ================= KaiwuDB Basic Info =================
    Deploy Mode: bare-metal
    Management User: kaiwudb
    Start Mode: multi-replication
    RESTful Port: 8080
    KaiwuDB Port: 26257
    BRPC Port: 27257
    Data Root: /var/lib/kaiwudb
    Secure Mode: tls
    CPU Usage Limit: 1
    Local Node Address: 192.168.122.221
    ================= KaiwuDB Cluster Info =================
    Cluster Node Address: 192.168.122.222 192.168.122.223
    SSH User: admin
    SSH Port: 22
    =========================================================
    Please confirm the installation information above(Y/n):
    ```

    Upon successful execution, the console displays the following message:

      ```shell
      [INSTALL COMPLETED]:KaiwuDB has been installed successfully! ...
      ```

4. Initialize and start the cluster.

    ::: warning Note
    Multi-replica cluster initialization and startup takes approximately 10 seconds. If nodes fail during this period, the cluster may fail to trigger high availability mechanisms.
    :::
  
    ```shell
    ./deploy.sh cluster -i
    ```

    or

    ```shell
    ./deploy.sh cluster --init
    ```

5. Check the cluster status using either of the following methods:

    - Using the deployment script in the current directory:

      ```shell
      ./deploy.sh cluster -s
      # or
      ./deploy.sh cluster --status
      ```

    - Using the `kw-status` script from any directory (recommended):

      ```shell
      kw-status
      ```

    Output fields:

    | Field         | Description                                                                                                                                                                      |
    |---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | `id`          | Node ID.                                                                                                                                                                          |
    | `address`     | Node address.                                                                                                                                                                     |
    | `sql_address` | SQL address.                                                                                                                                                                     |
    | `build`       | The KWDB version running on the node.                                                                                                                                                   |
    | `started_at`  | The date and time when the node was started.                                                                                                                                             |
    | `updated_at`  | The date and time when the node's status was last updated. When the node is healthy, a new status is recorded approximately every 10 seconds. If the node is unhealthy, the update information may be delayed.|
    | `locality`    | Node ID.                        |
    | `start_mode`  | The startup mode of the node.                                                                                                                                                       |
    | `is_available`<br>`is_live` | If both are `true`, the node is considered healthy.<br>If both are `false`, the node is considered non-functional.                                                               |

6. (Optional) Enable KWDB to start automatically after a system reboot.

    ::: warning Note
    KWDB startup may fail after system reboot if node time differs by >500 ms from other nodes. Ensure clock synchronization before manually starting KWDB if automatic startup fails.
    :::

    ```shell
    systemctl enable kaiwudb
    ```