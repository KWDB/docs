---
title: Single-Node Bare-Metal Deployment
id: quickstart-bare-metal
---

# Single-Node Bare-Metal Deployment

KWDB supports two single-node bare-metal deployment methods:

- **Script Deployment**: Deploy KWDB using the deployment script in the installation package, which supports configuring database deployment mode, data storage path, ports, and other parameters. For more information, see [Deploy KWDB Using Scripts](#deploy-kwdb-using-scripts).
- **CLI Deployment**: Deploy KWDB using the source code, which also supports configuring database deployment mode, data storage path, ports, and other parameters. For more information, see [Deploy KWDB Using kwbase CLI](#deploy-kwdb-using-kwbase-cli).

::: warning Note

KWDB supports open-source DRBD block device replication for data synchronization between primary and standby nodes. For single-node high availability, see [Single-Node High Availability Solution](../../best-practices/single-ha.md) first.

:::

## Preparation

### Hardware Requirements

The following specifications are required for KWDB deployment:

| Item  | Requirements  |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| CPU and Memory | - Minimum: 4 CPU cores and 8GB RAM per node <br> - For high-volume data, complex workloads, high concurrency, or performance-critical applications, allocate additional resources accordingly |
| Disk       | - Recommended: SSD or NVMe devices<br>- Minimum performance: 500 IOPS and 30 MB/s throughput<br>- Storage: <1GB for KWDB system, additional space needed based on data volume and enabled features like compression that reduce disk usage. For production environments, plan hardware resources according to your business scale and performance requirements. For more information, see [Estimate Disk Usage](../../db-operation/cluster-planning.md#estimate-disk-usage).<br>- Avoid shared storage (NFS, CIFS, CEPH)|
| File System | ext4 recommended for optimal performance |

### Supported Operating Systems and CPU Architectures

KWDB can be deployed on the following operating systems:

| Operating System | Version                  | CPU Architecture |
| :----------- | :--------------------------- | :------- |
| Anolis       | 8.6                          | ARM_64   |
|              | 8.6                          | x86_64   |
| KylinOS      | V10 SP3 2403                 | [ARM_64](https://gitee.com/kwdb/kwdb/releases/)   |
|              | V10 SP3 2303                 | ARM_64   |
|              | V10 SP3 2403                 | [x86_64](https://gitee.com/kwdb/kwdb/releases/)   |
|              | V10 SP3 2303                 | x86_64   |
| Ubuntu       | V18.04                       | x86_64   |
|              | V20.04                       | ARM_64   |
|              | V20.04                       | [x86_64](https://gitee.com/kwdb/kwdb/releases/)   |
|              | V22.04                       | ARM_64   |
|              | V22.04                       | [x86_64](https://gitee.com/kwdb/kwdb/releases/)   |
|              | V24.04                       | ARM_64   |
|              | V24.04                       | x86_64   |
| UOS          | 1060e                        | x86_64   |
|              | 1060e                        | ARM_64   |

::: warning Note

- Operating systems or versions not listed here **may** work with KWDB but are not officially supported.
- For installation packages not listed on the download page, contact [KWDB Technical Support](https://www.kaiwudb.com/support/).
:::

### Software Dependencies

The following table lists the required dependencies:

| Dependency    | Version   | Remarks |
| ------------- | --------- | ----------- |
| OpenSSL       | v1.1.1+   | N/A         |
| libprotobuf      | v3.6.1+   | The default version of libprotobuf included in Ubuntu 18.04 is lower than the required version. Users need to install a compatible version beforehand (3.6.1 and 3.12.4 recommended).         |
| GEOS          | v3.3.8+   | Optional    |
| xz-libs       | v5.2.0+   | N/A         |
| squashfs-tools| any       | N/A         |
| libgcc        | v7.3.0+   | N/A         |
| mount         | any       | N/A         |
| squashfuse    | any       | Optional    |

During installation, KWDB verifies the necessary dependencies. If any are missing, the installation process will halt and prompt you to install them. If the target machine is offline, you will need to download the required dependencies from an internet-connected device and then transfer the files to the target machine.

### Port Requirements

Ensure these default ports are available and not blocked by firewalls. Port settings can be modified during installation.

| Port        | Description |
| ----------- | ----------- |
| `8080`      | Port for HTTP requests and web services |
| `26257`     | Port for client and application connections |

### Installation Packages and Compiled Versions

Use pre-compiled installation packages or compile from source code as needed.

#### Installation Packages

Obtain the appropriate installation package for your system environment, copy the package to the target machine and then decompress it.

::: warning Note
Currently, the KWDB repository provides [DEB or RPM installation packages](https://gitee.com/kwdb/kwdb/releases/) for the following systems and architectures. For installation packages for other systems or architectures, please contact [KWDB Technical Support](https://www.kaiwudb.com/support/).

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
| `deploy.sh`       | Script for KWDB installation, uninstallation, start, status check, stop, start, and restart. |
| `packages`  | Stores DEB or RPM packages.                                    |
| `utils`      | Stores utility scripts.                                             |

#### Source Code Compilation

Complete source code download, compilation, and installation according to the [KWDB Compilation and Installation Instructions](https://gitee.com/kwdb/kwdb/blob/master/README.en.md#compilation-and-installation).

## Deploy KWDB

### Deploy KWDB Using Scripts

When deploying KWDB using scripts, the system verifies configuration files, runtime environment, hardware setup, and software dependencies. The deployment will proceed with a warning if hardware requirements are not met, but will abort with error messages if required software dependencies are missing.

Deployment logs are saved in the `log` directory within `kwdb_install`. Once the deployment is complete, KWDB will be packaged as a system service (`kaiwudb`) and the following files will be generated:

- `kaiwudb.service`: Configures CPU resources for KWDB.
- `kaiwudb_env`: Configures startup flags for KWDB.

#### Prerequisites

- The target node meets all the requirements for hardware, operating system, software, and ports.
- The user performing the installation is the `root` user or a regular user with `sudo` privileges:
  - `root` users or users with passwordless `sudo` configured will not be prompted for a password during script execution.
  - Users without passwordless `sudo` will be prompted to enter a password to escalate privileges.

#### Steps

1. Log in to the target node and edit the `deploy.cfg` file in the `kwdb_install` directory.

    ::: warning Note

    By default, the `deploy.cfg` configuration file includes cluster configuration parameters. Please remove or comment out the `[cluster]` section.

    :::

    Example:

    ```yaml
    [global]
    secure_mode=tls
    management_user=kaiwudb
    rest_port=8080
    kaiwudb_port=26257
    data_root=/var/lib/kaiwudb
    cpu=1
    [local]
    node_addr=your-host-ip

    # [cluster]
    # node_addr=your-host-ip, your-host-ip
    # ssh_port=22
    # ssh_user=admin
    ```

    Parameters:

    - `global`: Global configuration settings.
        - `secure_mode`: Defines the security mode. Options include:
            - `insecure`: Enables non-secure mode.
            - `tls`: (Default) Enables TLS mode. This generates TLS certificates for clients and application connections, stored in `/etc/kaiwudb/certs`.
        - `management_user`: The user account for managing KWDB, set to `kaiwudb` by default. After installation, KWDB creates this user and a user group with the same name.
        - `rest_port`: Port for web services (default: `8080`).
        - `kaiwudb_port`: Port for client and application connections (default: `26257`).
        - `data_root`: Data directory (default: `/var/lib/kaiwudb`).
        - `cpu`: (Optional) Specifies CPU usage for KWDB on the node. The default is unlimited. The value range is [0,1], with a precision of up to two decimal places. **Note:** If the deployment environment is **Ubuntu 18.04**, you need to modify the `CPUQuota` value in the `kaiwudb.service` file after the deployment is complete. Specifically, change any decimal values to integers (e.g., change `180.0%` to `180%`) to ensure the setting takes effect. For instructions, see [Manage CPU Resources](../../deployment/cluster-config/cluster-config-bare-metal.md#manage-cpu-resources).
    - `local`: Local node configuration.
        - `node_addr`: The IP address for client and application connection. The default listening address is `0.0.0.0`, meaning the node will listen on `kaiwudb_port` across all IP addresses on the host.

2. Grant execution permission to the `deploy.sh` script.

    ```shell
    chmod +x ./deploy.sh
    ```

3. Install KWDB in single-node mode.

    ```shell
    ./deploy.sh install --single
    ```

    Upon successful execution, the console will display the following message:

    ```shell
    INSTALL COMPLETED: KaiwuDB has been installed successfuly! ...
    ```

4. Reload the `systemd` daemon configuration.

    ```shell
    systemctl daemon-reload
    ```

5. Start KWDB.

    ```shell
    ./deploy.sh start
    ```

    Upon successful execution, the console will display the following message:

    ```shell
    START COMPLETED: KaiwuDB has started successfuly.
    ```

6. Check the database status.

    ```shell
    ./deploy.sh status
    ```

    or

    ```shell
    systemctl status kaiwudb
    ```

7. (Optional) Enable KWDB to start automatically after a system reboot.

    ```shell
    systemctl enable kaiwudb
    ```

8. (Optional) Run the `add_user.sh` script to create a database user. If this step is skipped, the system will use database deployment user by default, and no password is required to access the database.

    ```bash
    ./add_user.sh
    Please enter the username:
    Please enter the password:
    ```

    Upon successful execution, the following message will be displayed in the console:

    ```plain
    [ADD USER COMPLETED]: User creation completed.
    ```

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

2. (Optional) For secure deployment, create certificates and keys by following these steps:

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

    - Non-secure mode:

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

    - Non-secure mode:

        ```bash
        ./kwbase node status --insecure --host=<address_of_any_alive_node>
        ```

    - Secure mode:

        ```bash
        ./kwbase node status --certs-dir=<certs_dir> --host=<address_of_any_alive_node>
        ```

5. (Optional) Create a database user and grant administrator privileges to the user. If this step is skipped, the system will use database deployment user by default, and no password is required to access the database.

    - Non-secure mode (without password):

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