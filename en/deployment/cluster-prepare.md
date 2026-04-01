---
title: Deployment Preparation
id: cluster-prepare
---

# Deployment Preparation

## Hardware

:::warning Note
To improve availability and reduce the risk of data loss, it is recommended to run only one node on a single computer. KWDB uses a cross-node replication mechanism. If multiple nodes are running on one computer, data is more likely to be lost when the computer fails.
:::

The following table lists the hardware specifications required for deploying KWDB.

| Item | Requirements |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| CPU and Memory | Single-node configuration should not be lower than 4 cores and 8GB. For large data volumes, complex workloads, high concurrency, and high-performance scenarios, higher CPU and memory resources are recommended to ensure efficient system operation. |
| Disk | - SSD or NVMe devices are recommended. Avoid using shared storage such as NFS, CIFS, CEPH, etc.<br> - Disks must achieve 500 IOPS and 30 MB/s processing efficiency.<br>- HDD is not recommended for distributed cluster deployment.<br> - KWDB system startup does not consume excessive disk capacity (less than 1GB). Actual disk requirements mainly depend on user business volume.|
| File System | ext4 file system is recommended. |

## Operating System

KWDB supports installation and deployment on the following operating systems:

| Operating System | Version | Bare Metal | Bare Metal | Container | Container |
|---------|------|---------------|---------------|---------------|---------------|
| | | ARM64 | x86_64 | ARM64 | x86_64 |
| Anolis | 7 | | | ✓ | ✓ |
|  | 8 | ✓ | ✓ | ✓ | ✓ |
| CentOS | 7 | | | | ✓ |
|  | 8 | | | | ✓ |
| Debian | V11 | | | ✓ | |
| openEuler | 24.03 | | | | ✓ |
| Ubuntu | V20.04 | ✓ | ✓ | ✓ | ✓ |
|  | V22.04 | ✓ | ✓ | ✓ | ✓ |
|  | V24.04 | ✓ | ✓ | ✓ | ✓ |
| UOS | 1050e | | | ✓ | ✓ |
|  | 1060e | | | ✓ | ✓ |
|  | 1070e | ✓ | ✓ | ✓ | ✓ |
| Windows Server | WSL2 | | ✓ | | ✓ |

:::warning Note

- Container deployment requires Docker to be installed on the target machine. If not installed, please refer to the [Docker Official Installation Documentation](https://docs.docker.com/desktop/install/linux-install/). For offline environments, you can download Docker binary packages for offline installation. See [Docker Offline Installation Guide](https://docs.docker.com/engine/install/binaries/).
- Operating system versions not mentioned **may** run KWDB but are not officially supported by KWDB.

:::

## Software Dependencies

### Bare Metal Deployment

During installation, KWDB will check for dependencies. If dependencies are missing, the installation will exit and prompt for missing dependencies. If the target machine cannot connect to the internet, users need to download all dependency files on a machine that can connect to the internet according to the target machine's operating system, then copy the dependency files to the target machine for installation.

The following table lists the dependencies that need to be installed on the target machine.

| Dependency | Version | Description |
| --- | --- | --- |
| OpenSSL | v1.1.1+ | N/A |
| libprotobuf | v3.6.1 ~ v21.x | **Note**: The default libprotobuf version in Ubuntu 18.04 does not meet the requirements. Users need to install the required version in advance (3.6.1 and 3.12.4 are recommended).|
| GEOS | v3.3.8+ | Optional dependency |
| xz-libs | v5.2.0+ | N/A |
| libgcc | v7.3.0+ | N/A |
| libgflags | System default | N/A |
| libkrb5 | System default | N/A |

### Container Deployment

When deploying using [scripts](./cluster-deployment/script-deployment.md), the target machine needs to have Docker Compose (version 1.20.0 and above) installed.

- Online installation: Refer to [Docker Compose Official Installation Documentation](https://docs.docker.com/compose/install/)
- Offline installation: Refer to [Docker Compose Offline Installation Guide](https://docs.docker.com/compose/install/standalone/)
- Quick installation for Ubuntu/Debian systems:

    ```shell
    sudo apt-get install docker-compose
    ```

## Port Requirements

The following table lists the default ports used by KWDB services. If you need to use other ports, you can modify them during the installation and deployment process.

| Port Number | Description |
|--------|------|
| `8080` | Database Web service port |
| `26257` | Database service port, node listening port, and external connection port |
| `27257` | brpc communication port between database time-series engines |

## Installation Packages

Obtain the installation package corresponding to your system environment, copy the package to the target machine where KWDB will be installed, then extract the installation package:

```shell
tar -zxvf <package_name>
```

The extracted directory contains the following files:

| File | Description |
|-------------------|-----------------------------------------------------------|
| `add_user.sh` | After installing and starting KWDB, create users for the KWDB database. |
| `deploy.cfg` | Installation deployment configuration file for configuring IP addresses, ports, and other configuration information of deployment nodes. |
| `deploy.sh` | Installation deployment script for installation, uninstallation, startup, status retrieval, shutdown, and restart operations. |
| `packages` directory | Stores DEB, RPM, and Docker image packages.<br>**Note**: Specific files included vary by installation package type. |
| `utils` directory | Stores utility scripts. |

## Node Configuration

### SSH Passwordless Login

1. Log in to the current node and generate a public-private key pair.

   ```shell
   ssh-keygen -f ~/.ssh/id_rsa -N ""
   ```

   Parameter description:

   - `-f ~/.ssh/id_rsa`: Specifies the directory for the generated key pair files.
   - `-N`: Sets the key password to empty to achieve passwordless login.

2. Distribute the keys to other nodes in the cluster.

   ```shell
   ssh-copy-id -f -i ~/.ssh/id_rsa.pub -o StrictHostKeyChecking=no <target_node>
   ```

3. Confirm whether you can use SSH passwordless login to other nodes in the cluster.

   ```shell
   ssh <target_node>
   ```

### Clock Synchronization

KWDB uses a moderate-strength clock synchronization mechanism to maintain data consistency. When a node detects that its machine time error with at least 50% of the nodes in the cluster exceeds 80% of the cluster's maximum allowed time error (default is 500 ms), the node will automatically stop to avoid violating data consistency and bringing the risk of reading and writing stale data. Each node must run NTP (Network Time Protocol) or other clock synchronization software to prevent clock drift.

The following example uses CentOS 7 to introduce how to configure clock synchronization.

1. Use SSH to log in to the node where the cluster will be deployed.

2. Stop the timesyncd service.

   ```shell
   timedatectl set-ntp no
   ```

3. Install NTP service.

   ```shell
   sudo apt install ntp
   ```

4. Stop the NTP background process.

   ```shell
   service ntp stop
   ```

5. Synchronize machine time through NTP service.

   ```shell
   ntpdate -u 0.cn.pool.ntp.org
   ```

6. Open the `/etc/ntp.conf` file, find the `server` and `pool` related configurations and modify them as follows.

   ```shell
   server 0.cn.pool.ntp.org iburst
   server 1.cn.pool.ntp.org iburst
   server 2.cn.pool.ntp.org iburst
   server 3.cn.pool.ntp.org iburst
   ```

7. Start NTP service.

   ```shell
   service ntp start
   ```

8. Repeat the above steps on all cluster nodes where KWDB services will be installed.
