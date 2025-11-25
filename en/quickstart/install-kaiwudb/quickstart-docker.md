---
title: Single-Node Container Deployment
id: quickstart-docker
---

# Single-Node Container Deployment

KWDB supports multiple deployment methods to meet different user needs:

| Deployment Method                        | Features                                                      | Target Users/Scenarios                           | Technical Requirements        | Detailed Guide                                                                           |
| ---------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------ | ----------------------------- | ---------------------------------------------------------------------------------------- |
| **Script Deployment (Recommended)**      | One-click containerized deployment using built-in scripts     | Production environments requiring stable and rapid deployment | Basic Linux operational skills | [Deploy KWDB Using Scripts](#deploy-kaiwudb-using-scripts)                           |
| **Container Image Deployment - Docker Compose** | YAML-based orchestration deployment (insecure mode only) | Users familiar with container orchestration, suitable for testing or rapid validation scenarios | Docker and Docker Compose knowledge | [Deploy KWDB Using YAML Files](#deploy-kaiwudb-using-yaml-files)                     |
| **Container Image Deployment - Docker Run** | Direct container execution via `docker run` commands           | Testing and rapid validation scenarios        | Docker CLI proficiency | [Deploy KWDB by Executing Docker Run Commands](#deploy-kaiwudb-by-executing-docker-run-commands) |

::: warning Note

KWDB supports open-source DRBD block device replication for data synchronization between primary and standby nodes. For single-node high availability, see [Single-Node High Availability Solution](../../best-practices/single-ha.md) first.

:::

## Preparation

### Hardware

The following specifications are required for KWDB deployment:

| Item  | Requirements  |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| CPU and Memory | - Minimum: 4 CPU cores and 8 GB RAM per node <br> - For high-volume data, complex workloads, high concurrency, or performance-critical applications, allocate additional resources accordingly |
| Disk       | - Recommended: SSD or NVMe devices<br>- Minimum performance: 500 IOPS and 30 MB/s throughput<br>- Storage: <1 GB for KWDB system, with additional space needed based on data volume<br>- Avoid shared storage (NFS, CIFS, CEPH)<br>- Avoid excessive device count and high write loads for deployment on HDDs, as concurrent writes can significantly degrade performance|
| File System | ext4 recommended for optimal performance |

### Operating Systems and CPU Architectures

KWDB can be deployed on the following operating systems with Docker installed:

| Operating System | Version                  | **ARM_64** | **x86_64** |
| :----------- | :--------- | :--------- | :--------- |
| Anolis       | 7        | ✓          | ✓          |
|              | 8       | ✓          | ✓          |
| CentOS       | 7          |            | ✓          |
|              | 8          |            | ✓          |
| Debian       | V11        | ✓          |            |
| KylinOS      | V10 SP2    | ✓          | ✓          |
|              | V10 SP3 2403    | ✓          | ✓          |
| openEuler    | 24.03      |            | ✓          |
| Ubuntu       | V20.04     | ✓          | ✓          |
|              | V22.04     | ✓          | ✓          |
|              | V24.04     | ✓          | ✓          |
| UOS          | 1050e      | ✓           | ✓          |
|              | 1060e      | ✓          | ✓          |
|              | 1070e      | ✓          | ✓          |
| Windows Server  | WSL2     |           | ✓          |

::: warning Note

- For new Docker installations, follow [Install Docker Engine](https://docs.docker.com/engine/install/).
- For offline Docker installations, see [Install Docker Engine from Binaries](https://docs.docker.com/engine/install/binaries/) and [Linux Post-Installation Steps for Docker Engine](https://docs.docker.com/engine/install/linux-postinstall/).
- Operating systems or versions not listed below **may** work with KWDB but are not officially supported.
:::

### Software Dependencies (Optional)

If using installation scripts or yaml files to deploy KWDB, Docker Compose (version 1.20.0 or higher) is required.

- For online installation instructions, see [Install Docker Compose](https://docs.docker.com/compose/install/).
- For offline installation instructions, see [Install Docker Compose Standalone](https://docs.docker.com/compose/install/standalone/).

To install Docker Compose via the command line:

```shell
sudo apt-get install docker-compose
```

### Ports

Ensure these default ports are available and not blocked by firewalls. Port settings can be modified during installation.

| Port        | Description |
| ----------- | ----------- |
| `8080`      | Port for HTTP requests and web services |
| `26257`     | Port for client and application connections |

### Installation Packages and Docker Images

Use pre-compiled installation packages or compile from source code as needed.

#### Installation Package

Obtain the appropriate [installation package](https://gitee.com/kwdb/kwdb/releases) for your system environment, copy the package to the target machine and then decompress it.

::: warning Note
Currently, the KWDB repository provides [installation packages](https://gitee.com/kwdb/kwdb/releases/) for Ubuntu V22.04 ARM_64 and x86_64 architectures. For container installation packages of other versions, please contact [KWDB Technical Support](https://www.kaiwudb.com/support/).

:::

```shell
tar -zxvf <install_package_name>
```

The extracted `kwdb_install` directory contains the following files and folders:

| File/Folder          | Description                                               |
|-------------------|-----------------------------------------------------------|
| `add_user.sh`     | Script for creating KWDB users after installation and startup.           |
| `deploy.cfg`      | Configuration file for node IP addresses, ports, and other options. |
| `deploy.sh`       | Script for KWDB installation, uninstallation, start, status check, stop, start, and restart. |
| `packages`   | Stores image packages.                                    |
| `utils`      | Stores utility scripts.                                             |

#### Container Images

KWDB supports obtaining container images through the following methods:

- [Installation package](https://gitee.com/kwdb/kwdb/releases): Download the installation package corresponding to your system environment, and after extraction, import the `KaiwuDB.tar` file from the `kwdb_install/packages` directory.

    ```bash
    docker load < KaiwuDB.tar
    Loaded image: "image-name"
    ```

- Docker command: Execute `docker pull kwdb/kwdb:<version>` to obtain the image.

## Deploy KWDB

### Deploy KWDB Using Scripts

When deploying KWDB using scripts, the system verifies configuration files, runtime environment, hardware setup, and software dependencies. The deployment will proceed with a warning if hardware requirements are not met, but will abort with error messages if required software dependencies are missing.

Deployment logs are saved in the `log` directory within `kwdb_install`. The system creates `/etc/kaiwudb/` and places the Docker Compose configuration file `docker-compose.yml` at `/etc/kaiwudb/script/`. For custom configurations of the startup flags and CPU resources, see [Cluster Configuration](../../deployment/cluster-config/cluster-config-docker.md).

#### Prerequisites

- The installation package is obtained.
- The target node meets all the requirements for hardware, operating system, software, and ports.
- The user performing the deployment is the `root` user or a regular user with `sudo` privileges:
  - `root` users or users with passwordless `sudo` configured will not be prompted for a password during script execution.
  - Users without passwordless `sudo` will be prompted to enter a password to escalate privileges.
- If the user is not a `root` user, add the user to the `docker` group by running `sudo usermod -aG docker $USER`.  

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
    brpc_port=27257
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

    | Configuration Level | Parameter | Description |
    |---|---|---|
    | **global** | `secure_mode` | Defines the security mode. Options include:<br>- `insecure`: Enables insecure mode.<br>- `tls`: (Default) Enables secure mode. This generates TLS certificates for client and application connections, stored in `/etc/kaiwudb/certs`.|
    | | `management_user` | The user account for managing KWDB, set to `kaiwudb` by default. After installation, KWDB creates this user and a user group with the same name. |
    | | `rest_port` | Port for web services (default: `8080`). |
    | | `kaiwudb_port` | Port for client and application connections (default: `26257`). |
    | | `brpc_port` | The brpc communication port between KWDB time-series engines, used for inter-node communication. <br>This parameter is ignored in single-node deployment. |
    | | `data_root` | Data directory (default: `/var/lib/kaiwudb`). |
    | | `cpu` | (Optional) Specifies CPU usage for KWDB on the node. The default is unlimited. The value range is [0,1], with a precision of up to two decimal places. |
    | **local** | `node_addr` | The IP address for client and application connections. The default listening address is `0.0.0.0`, meaning the node will listen on `kaiwudb_port` across all IP addresses on the host. |

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

6. Check the system status.

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

8. (Optional) Run the `add_user.sh` script to create a database user. If skipped, the system will use database deployment user by default, and no password is required to access the database.

    ```bash
    ./add_user.sh
    Please enter the username:
    Please enter the password:
    ```

    Upon successful execution, the following message will be displayed in the console:

    ```shell
    [ADD USER COMPLETED]: User creation completed.
    ```

### Deploy KWDB using YAML Files

#### Prerequisites

- The Docker image is obtained.
- The target node meets all the requirements for hardware, operating system, software, and ports.
- The user performing the installation is the `root` user or a regular user with `sudo` privileges:
  - `root` users or users with passwordless `sudo` configured will not be prompted for a password during script execution.
  - Users without passwordless `sudo` will be prompted to enter a password to escalate privileges.
- If the user is not a `root` user, add the user to the `docker` group by running `sudo usermod -aG docker $USER`.

#### Steps

1. Create the `docker-compose.yml` configuration file.

    ::: warning Note
    The `image` parameter must match the image name obtained after importing the `KaiwuDB.tar` file or the pulled image name.
    :::

    Example:

    ```yaml
    version: '3.3'
    services:
      kwdb-container:
        image: "kwdb/kwdb:3.0.0"
        container_name: kaiwudb-experience
        hostname: kaiwudb-experience
        ports:
          - 8080:8080
          - 26257:26257
        ulimits:
          memlock: -1
        networks: 
          - default
        restart: on-failure
        ipc: shareable
        privileged: true
        environment:
          - LD_LIBRARY_PATH=/kaiwudb/lib
        tty: true
        working_dir: /kaiwudb/bin
        command: 
          - /bin/bash
          - -c
          - |
            /kaiwudb/bin/kwbase start-single-node --insecure --listen-addr=0.0.0.0:26257 --advertise-addr=127.0.0.1:26257 --http-addr=0.0.0.0:8080 --store=/kaiwudb/deploy/kaiwudb
    ```

2. Sart KWDB.

    ```bash
    docker-compose up -d
    ```

### Deploy KWDB by Executing Docker Run Commands

#### Prerequisites

- The Docker image is obtained.
- The target node meets all the requirements for hardware, operating system, software, and ports.
- The user performing the installation is the `root` user or a regular user with `sudo` privileges:
  - `root` users or users with passwordless `sudo` configured will not be prompted for a password during script execution.
  - Users without passwordless `sudo` will be prompted to enter a password to escalate privileges.
- If the user is not a `root` user, add the user to the `docker` group by running `sudo usermod -aG docker $USER`.

#### Steps

1. (Optional) If you need to deploy KWDB in secure mode, create the necessary certificates and keys using the following commands:

    ```shell
    docker run --rm --privileged \
      -v /etc/kaiwudb/certs:<certs_dir> \
      -w /kaiwudb/bin \
      <kwdb_image> \
      bash -c './kwbase cert create-ca --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key && \
                ./kwbase cert create-client root --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key && \
                ./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key'
    ```

    Parameters:

    | Parameter | Description |
    |---|---|
    | `--rm` | Automatically removes the container after it stops. |
    | `--privileged` | Grants extended privileges to the container. |
    | `-v` | Mounts the host's `/etc/kaiwudb/certs` directory to the container's `<certs_dir>` directory for certificate and key storage. |
    | `-w /kaiwudb/bin` | Sets the working directory inside the container to `/kaiwudb/bin`. |
    | `kwdb_image` | Container image name and tag (e.g., `kwdb:3.0.0`). |
    | `bash -c` | Executes the following certificate creation commands within the container:<br>- `./kwbase cert create-ca`: Creates a certificate authority (CA), generating CA certificates and keys.<br>- `./kwbase cert create-client root`: Creates client certificates and keys for the `root` user.<br>- `./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0`: Creates node server certificates and keys, supporting access through three network identifiers: local loopback address (`127.0.0.1`), local hostname (`localhost`), and all network interfaces (`0.0.0.0`).<br>- `--certs-dir=<certs_dir>`: Specifies the certificate storage directory.<br>- `--ca-key=<certs_dir>/ca.key`: Specifies the CA key path.|

2. Start KWDB database.

    - Insecure mode

      ```shell
      docker run -d --privileged --name kwdb \
        --ulimit memlock=-1 \
        --ulimit nofile=$max_files \
        -p $db_port:26257 \
        -p $http_port:8080 \
        -v /var/lib/kaiwudb:/kaiwudb/deploy/kwdb-container \
        --ipc shareable \
        -w /kaiwudb/bin \
        <kwdb_image> \
        ./kwbase start-single-node \
          --insecure \
          --listen-addr=0.0.0.0:26257 \
          --http-addr=0.0.0.0:8080 \
          --store=/kaiwudb/deploy/kwdb-container
      ```

    - Secure mode

        ```bash
        docker run -d --privileged --name kwdb \
          --ulimit memlock=-1 \
          --ulimit nofile=$max_files \
          -p $db_port:26257 \
          -p $http_port:8080 \
          -v /etc/kaiwudb/certs:<certs_dir> \
          -v /var/lib/kaiwudb:/kaiwudb/deploy/kwdb-container \
          --ipc shareable \
          -w /kaiwudb/bin \
          <kwdb_image> \
          ./kwbase start-single-node \
            --certs-dir=<certs_dir> \
            --listen-addr=0.0.0.0:26257 \
            --http-addr=0.0.0.0:8080 \
            --store=/kaiwudb/deploy/kwdb-container
      ```

    Parameters:

    | Parameter | Description |
    |---|---|
    | `-d` | Runs the container in the background and returns the container ID. |
    | `--name` | Specifies the container name for easier management. |
    | `--privileged` | Grants extended privileges to the container. |
    | `--ulimit memlock=-1` | Removes container memory size limit. |
    | `--ulimit nofile=$max_files` | Sets the maximum number of file descriptors that can be opened concurrently by processes within the container. |
    | `-p` | Maps ports between host and container (database service port 26257 and HTTP port 8080). |
    | `-v` | Sets up volume mounts:<br>- Mounts host's `/var/lib/kaiwudb` directory to container's `/kaiwudb/deploy/kwdb-container` directory for persistent data storage.<br>- In secure mode, mounts host's `/etc/kaiwudb/certs` directory to container's `<certs_dir>` directory for certificate and key storage. |
    | `--ipc shareable` | Allows other containers to share this container's IPC namespace. |
    | `-w /kaiwudb/bin` | Sets the working directory inside the container to `/kaiwudb/bin`. |
    | `kwdb_image` | Container image variable (replace with actual image name and tag, e.g., `kwdb:3.0.0`). |
    | `./kwbase start` | Database startup command with different flags for different mode:<br>- `--insecure`: (Insecure mode only) Runs in insecure mode.<br>- `--certs-dir=<certs_dir>`: (Secure mode) Specifies certificate directory location.<br>- `--listen-addr=0.0.0.0:26257`: Address and port for database client connections.<br>- `--http-addr=0.0.0.0:8080`: Address and port for the web-based admin UI and API endpoints.<br>- `--store=/kaiwudb/deploy/kwdb-container`: Specifies data storage location.|

3. (Optional) Create a database user and grant administrator privileges to the user. If skipped, the system will use database deployment user by default, and no password is required to access the database.

      - Insecure mode (without password):

          ```bash
          docker exec kwdb bash -c "./kwbase sql --insecure --host=<host_ip> -e \"create user <username>;grant admin to <username> with admin option;\""
          ```

      - Secure mode (with password):

          ```bash
          docker exec kwdb bash -c "./kwbase sql --host=<host_ip> --certs-dir=<cert_dir> -e \"create user <username> with password \\\"<user_password>\\\";grant admin to <username> with admin option;\""
          ```