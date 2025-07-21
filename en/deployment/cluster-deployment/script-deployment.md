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
    secure_mode=tls
    management_user=kaiwudb
    rest_port=8080
    kaiwudb_port=26257
    data_root=/var/lib/kaiwudb

    [local]
    node_addr= local_node_ip

    [cluster]
    node_addr= cluster_node_ips
    ssh_port=22
    ssh_user=admin
    ```

    Parameters:

    - `global`: Global settings.
        - `secure_mode`: Defines the security mode. Options include:
            - `insecure`: Enables non-secure mode.
            - `tls`: (Default) Enable TLS mode. This generates TLS certificates for clients or application connections, stored in `/etc/kaiwudb/certs`.
        - `management_user`: The user account for managing KWDB, set to `kaiwudb` by default. After installation, KWDB creates this user and a user group with the same name.
        - `rest_port`: Port for web services (default: `8080`).
        - `kaiwudb_port`: Port for client, application and node connections (default: `26257`).
        - `data_root`: Data directory (default: `/var/lib/kaiwudb`).
        - `cpu`: (Optional) Specifies CPU usage for KWDB on the node. The default is unlimited. The value range is `[0,1]`, with a precision of up to two decimal places. After deployment, you can also adjust the CPU resource limit. For instructions, see [Configure Bare-Metal Cluster](../cluster-config/cluster-config-bare-metal.md) or [Configure Container Cluster](../cluster-config/cluster-config-docker.md).
        **Note:** For bare-metal deployment, if the environment is Ubuntu 18.04, you need to modify the `CPUQuota` value in the `kaiwudb.service` file after the deployment is complete. Specifically, change any decimal values to integers (e.g., change `180.0%` to `180%`) to ensure the setting takes effect. For instructions, see [Manage CPU Resources](../cluster-config/cluster-config-bare-metal.md#manage-cpu-resources).
    - `local`: Local node configuration.
        - `node_addr`: The IP address for client and application connection. The default listening address is `0.0.0.0`, meaning the node will listen on `kaiwudb_port` across all IP addresses on the host.
    - `cluster`: Cluster configuration.
        - `cluster_node_ips`: The IP addresses of remote nodes. The IP addresses of each node should be separated by commas (`,`), and there must be at least two remote nodes.
        - `ssh_port`: The SSH port used for remote node access; it must be identical across all nodes.
        - `ssh_user`: The SSH username for remote node login; it must be identical across all nodes.

2. Grant execution permission to the `deploy.sh` script.

    ```shell
    chmod +x ./deploy.sh
    ```

3. Install the KWDB cluster.

   - For multi-replica clusters:

        ```shell
        ./deploy.sh install --multi-replica
        ```

   - For single-replica clusters:

        ```shell
        ./deploy.sh install --single-replica
        ```

4. Reload the `systemd` daemon configuration.

    ```shell
    systemctl daemon-reload
    ```

5. Initialize and start the cluster.

    ::: warning
    Multi-replica cluster initialization takes approximately 10 seconds. High availability features may not activate if nodes fail during this period.
    :::

    ```shell
    ./deploy.sh cluster -i
    ```

    or

    ```shell
    ./deploy.sh cluster --init
    ```

6. Verify the cluster status.

    ```shell
    ./deploy.sh cluster -s
    ```

    or

    ```shell
    ./deploy.sh cluster --status
    ```

    Output fields:

    | Field         | Description                                                                                                                                                                      |
    |---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | `id`          | Node ID.                                                                                                                                                                          |
    | `address`     | Node address.                                                                                                                                                                     |
    | `sql_address` | SQL address.                                                                                                                                                                     |
    | `build`       | The KWDB version running on the node.                                                                                                                                                   |
    | `started_at`  | The date and time when the node was started.                                                                                                                                             |
    | `updated_at`  | The date and time when the node's status was last updated. When the node is healthy, a new status is recorded approximately every 10 seconds. If the node is unhealthy, the recorded status may be older.|
    | `locality`    | The geographical location of the node, such as the country, data center, or rack.             |
    | `start_mode`  | The startup mode of the node.                                                                                                                                                       |
    | `is_available`<br>`is_live` | Node health indicators: <br> - If both are `true`, the node is considered healthy. <br> - If both are `false`, the node is considered non-functional.                                                               |

7. (Optional) Enable KWDB to start automatically after a system reboot.

    ::: warning Note

    KWDB startup may fail after system reboot if node time differs by >500ms from other nodes. Ensure clock synchronization before manually starting KWDB if automatic startup fails.

    :::

    ```shell
    systemctl enable kaiwudb
    ```
