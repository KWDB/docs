---
title: Single-Node Bare-Metal Deployment
id: quickstart-bare-metal
---

# Single-Node Bare-Metal Deployment

KWDB supports multiple deployment methods to meet different user needs:

| Deployment Method                        | Features                                                      | Target Users/Scenarios                           | Technical Requirements        | Detailed Guide                                                                           |
| ---------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------ | ----------------------------- | ---------------------------------------------------------------------------------------- |
| **Script Deployment (Recommended)**      | One-click deployment using built-in scripts     | Production environments requiring stable and rapid deployment | Basic Linux operational skills | [Deploy KWDB Using Scripts](#deploy-kwdb-using-scripts)                           |
| **Command Line Interface (CLI)**        | Fine-grained control and deep customization        | Advanced users with customization needs | Familiarity with database deployment processes and command-line operations  | [Deploy KWDB Using kwbase CLI](#deploy-kwdb-using-kwbase-cli) |

::: warning Note

KWDB supports open-source DRBD block device replication for data synchronization between primary and standby nodes. For single-node high availability, see [Single-Node High Availability Solution](../../best-practices/single-ha.md) first.

:::

## Preparation

### Hardware

The following specifications are required for KWDB deployment:

| Item  | Requirements  |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| CPU and Memory | - Minimum: 4 CPU cores and 8 GB RAM per node <br> - For large data volumes, complex workloads, high concurrency, or performance-critical applications, allocate higher CPU and memory resources to ensure efficient system operation |
| Disk       | - Recommended: SSD or NVMe devices<br>- Minimum performance: 500 IOPS and 30 MB/s throughput<br>- Storage: <1 GB for KWDB system, with additional space needed based on data volume<br>- Avoid shared storage (NFS, CIFS, CEPH)<br>- Avoid excessive device count and high write loads for deployment on HDDs, as concurrent writes can significantly degrade performance |
| File System | ext4 recommended for optimal performance |

### Operating Systems and CPU Architectures

KWDB can be deployed on the following operating systems:

| Operating System | Version                   | ARM_64 | x86_64 |
| :----------- | :--------------------------- | :--------- | :--------- |
| Anolis       | 8                          | ✓          | ✓          |
| KylinOS      | V10 SP2                      | ✓          | ✓          |
|              | V10 SP3 2303                 | ✓          | ✓          |
|              | V10 SP3 2403                 | ✓          | ✓          |
| Ubuntu       | V20.04                       | ✓          | ✓          |
|              | V22.04                       | ✓          | ✓          |
|              | V24.04                       | ✓          | ✓          |
| UOS          | 1070e                        | ✓          | ✓          |
| Windows Server  | WSL2                      |           | ✓          |

::: warning Note

- Operating systems or versions not listed here **may** run KWDB but are not officially supported.
- For installation packages not listed on the [download page](https://gitee.com/kwdb/kwdb/releases/), contact [KWDB Technical Support](https://www.kaiwudb.com/support/).
:::

### Software Dependencies

The following table lists the required dependencies:

| Dependency    | Version   | Remarks |
| ------------- | --------- | ----------- |
| OpenSSL       | v1.1.1+   | N/A         |
| libprotobuf      | v3.6.1 ~ v21.x   |  The default version of libprotobuf included in Ubuntu 18.04 is lower than required. You must install a compatible version beforehand (3.6.1 and 3.12.4 recommended).       |
| GEOS          | v3.3.8+   | Optional    |
| xz-libs       | v5.2.0+   | N/A         |
| libgcc        | v7.3.0+   | N/A         |
| libgflags | System default | N/A |
| libkrb5 | System default | N/A |

During installation, KWDB verifies the necessary dependencies. If any are missing, the installation process will halt and prompt you to install them. If the target machine is offline, you will need to download the required dependencies from an internet-connected device and then transfer the files to the target machine.

### Ports

Ensure these default ports are available and not blocked by firewalls. Port settings can be modified during installation.

| Port        | Description |
| ----------- | ----------- |
| `8080`      | Port for HTTP requests and web services |
| `26257`     | Port for client and application connections |

### Installation Packages and Compiled Versions

Use pre-compiled installation packages or compile from source code as needed.

#### Installation Package

Obtain the appropriate installation package for your system environment, copy the package to the target machine and then decompress it.

::: warning Note
The KWDB repository provides [DEB or RPM installation packages](https://gitee.com/kwdb/kwdb/releases/) for the following systems and architectures. For installation packages for other systems or architectures, please contact [KWDB Technical Support](https://www.kaiwudb.com/support/).

- Ubuntu V20.04 x86_64
- Ubuntu V22.04 x86_64
- Kylin V10_2403 x86_64
- Kylin V10_2403 ARM_64

:::

```shell
tar -zxvf <install_package_name>
```

The extracted `kwdb_install` directory contains the following files and folders:

| File/Folder         | Description                                               |
|-------------------|-----------------------------------------------------------|
| `add_user.sh`     | Script for creating KWDB users after installation and startup.           |
| `deploy.cfg`      | Configuration file for node IP addresses, ports, and other options. |
| `deploy.sh`       | Script for KWDB installation, uninstallation, start, status check, and stop operations. |
| `packages`  | Stores DEB or RPM packages.                                    |
| `utils`      | Stores utility scripts.                                             |

#### Source Code Compilation

Complete source code download, compilation, and installation according to the [KWDB Compilation and Installation Instructions](https://gitee.com/kwdb/kwdb/blob/master/README.en.md#compilation-and-installation).

## Deploy KWDB

### Deploy KWDB Using Scripts

When deploying KWDB using scripts, the system verifies configuration files, runtime environment, hardware setup, and software dependencies. The deployment will proceed with a warning if hardware requirements are not met but will abort with error messages if required software dependencies are missing.

Deployment logs are saved in the `log` directory within `kwdb_install`. Once deployment is complete, KWDB will be packaged as a system service (`kaiwudb`), and the following files will be generated:

- `kaiwudb.service`: Configures CPU resources for KWDB.
- `kaiwudb_env`: Configures startup flags for KWDB.

#### Prerequisites

- The installation package is obtained.
- The target node meets all requirements for hardware, operating system, software, and ports.
- The user performing the installation is the `root` user or a regular user with `sudo` privileges:
  - `root` users or users with passwordless `sudo` configured will not be prompted for a password during script execution.
  - Users without passwordless `sudo` will be prompted to enter a password to escalate privileges.

#### Steps

1. Log in to the target node and edit the `deploy.cfg` file in the `kwdb_install` directory.

    ::: warning Note

    By default, the `deploy.cfg` configuration file contains cluster and primary-secondary cluster configuration parameters. Please delete or comment out the `[cluster]` and `[additional]` configuration item.

    :::

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

    Parameters:

    | Configuration Level | Parameter | Description |
    |---|---|---|
    | **global** | `secure_mode` | Defines the security mode. Options include:<br>- `insecure`: Enables insecure mode.<br>- `tls`: (Default) Enables secure mode. This generates TLS certificates for client and application connections, stored in `/etc/kaiwudb/certs`.|
    | | `management_user` | The user account for managing KWDB, set to `kaiwudb` by default. After installation, KWDB creates this user and a user group with the same name. |
    | | `rest_port` | Port for web services (default: `8080`). |
    | | `kaiwudb_port` | Port for client and application connections (default: `26257`). |
    | | `brpc_port` | The brpc communication port between KWDB time-series engines, used for inter-node communication. <br>This parameter is ignored in single-node deployment. |
    | | `data_root` | Data directory (default: `/var/lib/kaiwudb`). |
    | | `cpu` | (Optional) Specifies CPU usage for KWDB on the node. The default is unlimited. The value range is [0,1], with a precision of up to two decimal places. <br>**Note:** If the deployment environment is **Ubuntu 18.04**, you need to modify the `CPUQuota` value in the `kaiwudb.service` file after deployment is complete. Specifically, change any decimal values to integers (e.g., change `180.0%` to `180%`) to ensure the setting takes effect. For instructions, see [CPU Usage Configuration](../../deployment/cluster-config/cluster-config-bare-metal.md#manage-cpu-resources). |
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

8. Execute `kw-sql` to log in to the database as the `root` user, or use the [kwbase CLI tool to log in to the database](../access-kaiwudb/access-kaiwudb-cli.md).

### Deploy KWDB Using kwbase CLI

#### Prerequisites

- The target node meets all the requirements for hardware, operating system, software, and ports.
- The user performing the deployment is the `root` user or a regular user with `sudo` privileges.
- KWDB source code is compiled and installed according to [KWDB Compilation and Installation Instructions](https://gitee.com/kwdb/kwdb/blob/master/README.en.md#compilation-and-installation).

#### Steps

1. Navigate to the directory where the `kwbase` script is located:

   ```bash
   cd /home/go/src/gitee.com/kwbasedb/install/bin
   ```

2. (Optional) For secure mode, create certificates and keys by following these steps:

   1. Create a directory to store the certificates and keys:

        ```bash
        mkdir -p <certs_dir>
        ```

   2. Generate certificates and keys:

        ```bash
        # Create database certificate authority and key
        ./kwbase cert create-ca --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key && \

        # Create client certificate and key for database installation user (replace username with actual username)
        ./kwbase cert create-client <username> --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key && \

        # Create node certificate and key
        ./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key
        ```

3. Start the database.

    - Insecure mode:

        ```bash
        ./kwbase start-single-node --insecure \
            --listen-addr=0.0.0.0:26257 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb
        ```

    - Secure mode:

        ```bash
        ./kwbase start-single-node \
            --certs-dir=<certs_dir> \
            --listen-addr=0.0.0.0:26257 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb
        ```

4. Check database status.

    - Insecure mode:

        ```bash
        ./kwbase node status --insecure --host=<address_of_any_alive_node>
        ```

    - Secure mode:

        ```bash
        ./kwbase node status --certs-dir=<certs_dir> --host=<address_of_any_alive_node>
        ```

5. (Optional) Create a database user and grant administrator privileges to the user. If this step is skipped, the system will use database deployment user by default, and no password is required to access the database.

    - Insecure mode (without password):

        ```bash
        ./kwbase sql --host=127.0.0.1:<local_port> --insecure \
        -e "create user <username>; \
            grant admin to <username> with admin option;"
        ```

    - Secure mode (with password):

        ```bash
        ./kwbase sql --certs-dir=<certs_dir> --host=127.0.0.1:<local_port> \
        -e "create user <username> with password \"<user_password>\"; \
            grant admin to <username> with admin option;"
        ```