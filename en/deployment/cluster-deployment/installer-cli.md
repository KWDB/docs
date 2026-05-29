---
title: Command-Line Mode Deployment
id: installer-cli
---

# Command-Line Mode Deployment

Command-line mode guides you through the installation step by step using text menus, supports numeric input for option selection, requires no extra dependencies, and is suitable for non-graphical environments.

During installation, the program performs real-time parameter validation. If a configuration is invalid, it prompts you to re-enter the value. It supports both secure and insecure modes, and after deployment completes, you can choose to start the database immediately.

::: warning

Command-line mode does not support deploying multiple nodes on a single machine.

:::

## Prerequisites

**System requirements**:

- The hardware, operating system, and software dependencies of all nodes to be deployed meet the requirements in [Deployment Preparation](../cluster-prepare.md).
- Network settings:
  - The nodes can communicate with each other over the network.
  - The machines are located in the same data center.
  - The network latency between physical machines is no more than 50 ms.
  - The time difference between nodes is no more than 500 ms.
  - The required KWDB service ports are reserved on each node.
- You have obtained the KaiwuDB installer (`.run` file).

**User permission requirements**:

- The installation user must be `root` or a regular user with passwordless `sudo` configured.
- If you are using the container installer and the installation user is not `root`, run the following command to add the user to the `docker` group:

  ```bash
  sudo usermod -aG docker $USER
  ```

## Steps

1. Log in to the node to be deployed, copy the `.run` installer to the installation directory, and grant execution permissions:

    ```bash
    chmod +x KWDB-*.run
    ```

2. Start the installer in command-line mode:

    ```bash
    ./KWDB-*.run -c
    # or
    ./KWDB-*.run --cli
    ```

3. After the installer starts, go to the main menu and enter `1` to choose Install KWDB:

    ```plain
    1. Install KWDB
    2. Uninstall KWDB
    3. Install KWDB and Join a Cluster
    4. Upgrade Node
    5. Exit

    Please enter an option [1-5]:
    ```

4. Based on your business requirements, enter the corresponding number to select a single-replica or three-replica cluster:

    ```plain
    1. Single-node installation
    2. Single-replica cluster
    3. Three-replica cluster
    4. Return to the main menu

    Please select [1-4]:
    ```

5. Enter the number of nodes to install. For example, enter `3` to install three nodes.

6. The installer automatically generates a configuration template and opens it in an editor. Modify the parameters according to your environment, save the file, and exit. The installer will then start the installation automatically.

    Example configuration file (for a three-node cluster):

    ```ini
    [global]
    # Whether secure mode is enabled
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
    host=192.168.122.237
    # SSH port
    port=22
    # SSH user
    user=admin
    # SSH password
    passwd=******
    [node2]
    host=192.168.122.79
    # SSH port
    port=22
    # SSH user
    user=admin
    # SSH password
    passwd=******
    [node3]
    host=192.168.122.169
    # SSH port
    port=22
    # SSH user
    user=admin
    # SSH password
    passwd=******
    ```

    Parameter descriptions:

    | Parameter | Description |
    |-----------|-------------|
    | `secure_mode` | Secure mode. Supported values are:<br>- `insecure`: insecure mode.<br>- `tls`: (default) TLS secure mode. When secure mode is enabled, KWDB automatically generates certificates and stores them in `/etc/kaiwudb/certs`. |
    | `rest_port` | KWDB Web service port; default is `8080`. |
    | `kaiwudb_port` | KWDB service port; default is `26257`. |
    | `brpc_port` | Data transfer port between time-series engines for inter-node communication; default is `27257`. |
    | `data_root` | Data directory; default is `/var/lib/kaiwudb`. |
    | `host` | Node IP address; ensure the nodes can reach one another over the network. |
    | `port` | SSH service port on the remote nodes. All nodes must use the same SSH port. |
    | `user` | SSH login user on the remote nodes. All nodes must use the same SSH user. |
    | `passwd` | SSH login password on the remote nodes. All nodes must use the same SSH password. |

7. Choose whether to install KWDB for all users:

    ```plain
    Install for all users? (y/N)
    ```

8. During installation, the terminal displays the progress in real time. If an error occurs, you can review the log files in the `log` directory under the installation directory for detailed information.

9. After all nodes are deployed, choose whether to initialize the cluster when prompted:

    ```plain
    Initialize the cluster? (y/N)
    ```

    - Enter `y`: The system automatically initializes the KWDB cluster.
    - Enter `N`: Skip initialization and initialize the cluster manually later:

        ```bash
        systemctl start kaiwudb
        ```

        :::warning Note
        Initializing and starting a multi-replica cluster usually takes about 10 seconds. During this period, if a node fails, the cluster may be unable to trigger its high-availability mechanism.
        :::

10. In the main menu, enter `5` to exit the deployment process.

11. Use either of the following methods to view service status or cluster status:

    ```bash
    # View service status
    systemctl status kaiwudb

    # View cluster status
    kw-status
    ```

    Field descriptions for cluster status:

    | Field | Description |
    |-------|-------------|
    | `id` | Node ID. |
    | `address` | Node address. |
    | `sql_address` | SQL address. |
    | `build` | KWDB version running on the node. |
    | `started_at` | Node startup date and time. |
    | `updated_at` | Node status update time. When the node is healthy, a new status record is written about every 10 seconds. If the node is abnormal, the update may lag. |
    | `locality` | Node ID. |
    | `start_mode` | Node startup mode. |
    | `is_available` / `is_live` | Both `true` means the node is healthy; both `false` means the node is abnormal. |

12. (Optional) Configure KWDB to start automatically at system startup:

    ```bash
    systemctl enable kaiwudb
    ```

    :::warning Note
    After a system restart, if the current node and other nodes differ by more than 500 ms in clock time, KWDB may fail to start automatically. Synchronize the clocks first, then start KWDB manually.
    :::

13. Run `kw-sql` to log in to the database as the deployment user, or connect to and manage KWDB using any of the following methods:
    - [kwbase CLI](../../quickstart/access/access-cli.md)
    - [KaiwuDB-supported connectors](../../development/overview.md)
    - [KaiwuDB Developer Center](../../kaiwudb-tools/kaiwudb-developer-center/overview.md)
