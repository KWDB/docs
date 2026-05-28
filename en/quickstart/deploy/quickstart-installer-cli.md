---
title: Command-Line Mode Deployment
id: quickstart-installer-cli
---

# Command-Line Mode Deployment

Command-line mode guides you through the installation step by step using text menus, supports numeric input for option selection, requires no extra dependencies, and is suitable for non-graphical environments.

During installation, the program performs real-time parameter validation. If a configuration is invalid, it prompts you to re-enter the value. It supports both secure and insecure modes, and after deployment completes, you can choose to start the database immediately.

## Prerequisites

**System requirements**:

- The hardware, operating system, and software dependencies of the node to be deployed meet the requirements in [Deployment Preparation](../prepare.md).
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

4. Enter `1` to choose single-node mode:

    ```plain
    1. Single-node installation
    2. Single-replica cluster
    3. Three-replica cluster
    4. Return to the main menu

    Please select [1-4]:
    ```

5. The installer automatically generates a configuration template and opens it in an editor. Modify the parameters according to your environment, save the file, and exit. The installer will then start the installation automatically.

    Example configuration file:

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
    host=127.0.0.1
    # SSH port
    port=22
    # SSH user
    user=admin
    # SSH password
    passwd=*******
    ```

    Parameter descriptions:

    | Parameter | Description |
    |-----------|-------------|
    | `secure_mode` | Secure mode. Supported values are:<br>- `insecure`: insecure mode.<br>- `tls`: (default) TLS secure mode. When secure mode is enabled, KWDB automatically generates certificates and stores them in `/etc/kaiwudb/certs`. |
    | `rest_port` | Admin UI port; default is `8080`. |
    | `kaiwudb_port` | KWDB service port; default is `26257`. |
    | `brpc_port` | Data transfer port between time-series engines. For single-node deployment, the system ignores this setting automatically; default is `27257`. |
    | `data_root` | Data directory; default is `/var/lib/kaiwudb`. |
    | `host` | Local node IP address. |
    | `port` | SSH connection port. |
    | `user` | SSH connection user. |
    | `passwd` | SSH connection password. |

6. Choose whether to install KWDB for all users:

    ```plain
    Install for all users? (y/N)
    ```

7. During installation, the terminal displays the progress in real time. If an error occurs, you can review the log files in the `log` directory under the installation directory for detailed information.

8. After the installation is complete, choose whether to start the database immediately when prompted:

    ```plain
    Start the database? (y/N)
    ```

    - Enter `y`: The system starts and initializes KWDB automatically.
    - Enter `N`: Skip startup and start KWDB manually later:

        ```bash
        systemctl start kaiwudb
        ```

9. In the main menu, enter `5` to exit the deployment process.

10. View the service or node status:

    ```bash
    # View service status
    systemctl status kaiwudb

    # View node status
    kw-status
    ```

    Field descriptions for node status:

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
    | `is_available` / `is_live` | `true` means the node is healthy; `false` means the node is abnormal. |

11. (Optional) Configure KWDB to start automatically at system startup:

    ```bash
    systemctl enable kaiwudb
    ```

12. Run `kw-sql` to log in to the database as the deployment user, or connect to and manage KWDB using any of the following methods:
    - [kwbase CLI](../access/access-cli.md)
    - [KaiwuDB JDBC](../access/access-jdbc.md)
    - [KaiwuDB Developer Center](../access/access-kdc.md)
