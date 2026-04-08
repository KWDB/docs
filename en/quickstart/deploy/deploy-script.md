---
title: Script Deployment
id: quickstart-script
---

# Script Deployment

When deploying KWDB using scripts, the system will check configuration files, runtime environment, hardware configuration, and software dependencies:
- If hardware requirements are not met, the installation will continue but prompt that hardware specifications are insufficient.
- If software dependencies are not met, the installation will be aborted and corresponding error messages will be provided.

During the deployment process, the system automatically generates relevant logs. If errors occur during deployment, users can view detailed error information through terminal output or log files in the `log` directory of the KWDB installation directory.

After bare-metal script deployment, the system packages KWDB as a system service (named `kaiwudb`) and generates the following files:

- `kaiwudb.service`: Configures KWDB CPU resource usage.
- `kaiwudb_env`: Configures KWDB startup parameters.

After container script deployment, the system generates a Docker Compose configuration file `docker-compose.yml` for configuring KWDB startup parameters and CPU resource usage.

For specific configuration steps, see [Cluster Parameter Configuration](../../db-operation/cluster-settings-config.md).

## Prerequisites

- Obtained KWDB [installation package](../prepare.md#installation-packages).
- The hardware, operating system, software dependencies, and ports of the node to be deployed meet the [installation deployment requirements](../prepare.md).
- Installation user is root or a regular user with `sudo` privileges.
  - Root users and regular users configured with `sudo` passwordless access do not need to enter a password when executing deployment scripts.
  - Regular users without `sudo` passwordless configuration need to enter a password for privilege escalation when executing deployment scripts.
- For container deployment with non-root installation users, the user needs to be added to the `docker` group using `sudo usermod -aG docker $USER`.

## Steps

1. Log in to the node to be deployed and edit the `deploy.cfg` configuration file in the installation package directory to set security mode, management user, service ports, and other information.

    ::: warning Note
    By default, the `deploy.cfg` configuration file contains cluster and primary-replica cluster address configuration parameters. Please delete or comment out the `[cluster]` and `[additional]` configuration items.
    :::

    Configuration file example:

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

    | Level | Parameter | Description |
    |---|---|---|
    | **global** <br>(Global configuration) | `secure_mode` | Whether to enable secure mode. Supports the following values:<br>- `insecure`: Use insecure mode.<br>- `tls`: (Default) Enable TLS secure mode. When enabled, KWDB generates corresponding TLS certificates as credentials for clients or applications to connect to the database. Generated client certificates are stored in the `/etc/kaiwudb/certs` directory. |
    | | `management_user` | KWDB management user, defaults to `kaiwudb`. After installation and deployment, KWDB creates the corresponding management user and a user group with the same name as the management user. |
    | | `rest_port` | KWDB Web service port, defaults to `8080`. |
    | | `kaiwudb_port` | KWDB service port, defaults to `26257`. |
    | | `brpc_port` | brpc communication port between KWDB time-series engines for inter-node communication. This setting is automatically ignored for single-node deployment. |
    | | `data_root` | Data directory, defaults to `/var/lib/kaiwudb`. |
    | | `cpu` | Optional parameter to specify the proportion of CPU resources that the KWDB service occupies on the current node server. No limit by default. Value range is `[0,1]`, with maximum precision of two decimal places.<br>**Note**: If the deployment environment is Ubuntu 18.04, after deployment is complete, you need to modify `CPUQuota` in the `kaiwudb.service` file to an integer value, for example, change `180.0%` to `180%` to ensure the setting takes effect. For specific operation steps, see [Configure CPU Resource Usage](../../db-operation/cluster-settings-config.md#cpu-resource-usage-configuration). |
    | **local** <br>(Local node configuration) | `node_addr` | IP address for external service of the local node, listening address is `0.0.0.0`, port is the KWDB service port. |

2. Execute the single-node deployment installation command.

    ```shell
    ./deploy.sh install --single
    ```

3. After verifying the configuration is correct, enter `Y` or `y`. To return and modify the `deploy.cfg` configuration file, enter `N` or `n`.

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
    ======================================================
    Please confirm the installation information above(Y/n):
    ```

    After successful execution, the console outputs the following information:

    ```shell
    [INSTALL COMPLETED]:KaiwuDB has been installed successfully! ...
    ```

4. Start the KWDB node.

    ```shell
    ./deploy.sh start
    ```

    After successful execution, the console outputs the following information:

    ```shell
    [START COMPLETED]:KaiwuDB start successfully.
    ```

5. Check node status using any of the following methods:

    - Use deployment script in the current directory

        ```shell
        ./deploy.sh status
        ```

    - Use `systemctl` command in any directory

        ```shell
        systemctl status kaiwudb
        ```

    - Use convenient script in any directory (recommended)

        ```shell
        kw-status
        ```

6. (Optional) Configure KWDB to start automatically on boot.

    After configuring KWDB to start automatically on boot, if the system restarts, KWDB will start automatically.

    ```shell
    systemctl enable kaiwudb
    ```

7. (Optional) Execute the `add_user.sh` script to create a database user. If this step is skipped, the system will default to using the user that deployed the database without requiring a password to access the database.

    ```shell
    ./add_user.sh
    Please enter the username: 
    Please enter the password:
    ```

    After successful execution, the console outputs the following information:

    ```shell
    [ADD USER COMPLETED]:User creation completed.
    ```

8. Connect to and manage KWDB via [kwbase CLI](../access/access-cli.md), [KaiwuDB JDBC](../access/access-jdbc.md), or [KaiwuDB Developer Center](../access/access-kdc.md).
