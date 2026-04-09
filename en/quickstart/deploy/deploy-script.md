---
title: Script Deployment
id: quickstart-script
---

# Script Deployment

When deploying KWDB using scripts, the system verifies configuration files, runtime environment, hardware, and software dependencies. If hardware requirements are not met, installation continues with a warning. If software dependencies are missing, installation aborts with an error message.

During deployment, the system automatically generates logs. If errors occur, check terminal output or log files in the `log` directory within the KWDB installation directory for details.

After bare-metal script deployment, the system packages KWDB as a system service (named `kaiwudb`) and generates the following files:

- `kaiwudb.service`: Configures CPU resource usage.
- `kaiwudb_env`: Configures KWDB startup flags.

After container script deployment, the system generates a Docker Compose configuration file `docker-compose.yml` for configuring KWDB startup flags and CPU resource usage.

For specific configuration steps, see [Cluster Configuration](../../db-operation/cluster-settings-config.md).

## Prerequisites

- Obtained KWDB [installation package](../prepare.md#installation-packages).
- The hardware, operating system, software dependencies, and ports of the node to be deployed meet the [installation deployment requirements](../prepare.md).
- Installation user is `root` or a regular user with `sudo` privileges
  - `root` users and regular users with passwordless `sudo` configured will not be prompted for a password during script execution.
  - Regular users without passwordless `sudo` will be prompted to enter a password to escalate privileges.
- For container deployment, non-root users added to `docker` group: `sudo usermod -aG docker $USER`.

## Steps

1. Log in to the target node and edit the `deploy.cfg` file in the `kwdb_install` directory.

    ::: warning Note

    By default, the `deploy.cfg` configuration file contains cluster and primary-secondary cluster configuration parameters. Please delete or comment out the `[cluster]` and `[additional]` configuration item.

    :::

    Configuration example:

    ```yaml
    [global]
    # Whether to turn on secure mode
    secure_mode=tls
    # Management KaiwuDB user
    management_user=kaiwudb
    # KaiwuDB cluster http port
    rest_port=8080
    # KaiwuDB service port
    kaiwudb_port=26257
    # KaiwuDB brpc port
    brpc_port=27257
    # KaiwuDB data directory
    data_root=/var/lib/kaiwudb
    # CPU usage[0-1]
    # cpu=1

    [local]
    # local node configuration
    node_addr=127.0.0.1

    # [cluster]
    # remote node addr,split by ','
    # node_addr=127.0.0.2
    # ssh info
    # ssh_port=22
    # ssh_user=admin

    # [additional]
    # IPs=127.0.0.3,127.0.0.4
    ```

    Parameter description:

    | Configuration Level | Parameter | Description |
    |---|---|---|
    | **global** | `secure_mode` | Defines the security mode. Options include:<br>- `insecure`: Enables insecure mode.<br>- `tls`: (Default) Enables secure mode. This generates TLS certificates for client and application connections, stored in `/etc/kaiwudb/certs`.|
    | | `management_user` | The user account for managing KWDB, set to `kaiwudb` by default. After installation, KWDB creates this user and a user group with the same name. |
    | | `rest_port` | Port for web services (default: `8080`). |
    | | `kaiwudb_port` | Port for client and application connections (default: `26257`). |
    | | `brpc_port` | The brpc communication port between KWDB time-series engines, used for inter-node communication. <br>This parameter is ignored in single-node deployment. |
    | | `data_root` | Data directory (default: `/var/lib/kaiwudb`). |
    | | `cpu` | (Optional) Specifies CPU usage for KWDB on the node. The default is unlimited. The value range is [0,1], with a precision of up to two decimal places. <br>**Note:** If the deployment environment is **Ubuntu 18.04**, you need to modify the `CPUQuota` value in the `kaiwudb.service` file after deployment is complete. Specifically, change any decimal values to integers (e.g., change `180.0%` to `180%`) to ensure the setting takes effect. For instructions, see [CPU Usage Configuration](../../db-operation/cluster-settings-config.md#cpu-resource-usage-configuration). |
    | **local** | `node_addr` | The IP address for client and application connections. The default listening address is `0.0.0.0`, meaning the node will listen on `kaiwudb_port` across all IP addresses on the host. |

2. Install KWDB in single-node mode.

    ```shell
    ./deploy.sh install --single
    ```

3. After verifying that the configuration is correct, enter `Y` or `y`. To return and modify the `deploy.cfg` configuration file, enter `N` or `n`.

    ```shell
    ================= KaiwuDB Basic Info =================
    Deploy Mode: bare-metal
    Start Mode: single
    RESTful Port: 8080
    KaiwuDB Port: 26257
    BRPC Port: 27257
    Data Root: /var/lib/kaiwudb
    Secure Mode: tls
    CPU Usage Limit: unlimited
    Local Node Address: 127.0.0.1
    =========================================================
    Please confirm the installation information above(Y/n):
    ```

    Upon successful execution, the console displays the following message:

      ```shell
      [INSTALL COMPLETED]:KaiwuDB has been installed successfully! ...
      ```

4. Start KWDB.

    ```shell
    ./deploy.sh start
    ```

    Upon successful execution, the console displays the following message:

    ```shell
    [START COMPLETED]:KaiwuDB start successfully.
    ```

5. Check the database status using any of the following methods:

    - The deployment script in the current directory

        ```shell
        ./deploy.sh status
        ```

    - The `systemctl` command from any directory

        ```shell
        systemctl status kaiwudb
        ```

    - The helper script from any directory (recommended)

        ```shell
        kw-status
        ```

6. (Optional) Enable KWDB to start automatically after a system reboot.

    ```shell
    systemctl enable kaiwudb
    ```

7. (Optional) Run the `add_user.sh` script to create a database user. If skipped, the system will use the database deployment user by default, and no password is required to access the database.

    ```bash
    ./add_user.sh
    Please enter the username:
    Please enter the password:
    ```

    Upon successful execution, the console displays the following message:

    ```plain
    [ADD USER COMPLETED]: User creation completed.
    ```

8. Connect to and manage KWDB via [kwbase CLI](../access/access-cli.md), [KaiwuDB JDBC](../access/access-jdbc.md), or [KaiwuDB Developer Center](../access/access-kdc.md).
