---
title: Prepare for Bare-Metal Deployment 
id: before-deploy-bare-metal
---

# Prepare for Bare-Metal Deployment 

## Hardware

:::warning Note

KWDB uses cross-node replication to maintain data redundancy across multiple nodes. To maintain high availability and protect against data loss, deploy each KWDB node on a separate physical or virtual machine.

:::

The following specifications are required for KWDB deployment:

| Item  | Requirements  |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| CPU and Memory | - Minimum: 4 CPU cores and 8 GB RAM per node <br> - For high-volume data, complex workloads, high concurrency, or performance-critical applications, allocate additional resources accordingly |
| Disk       | - Recommended: SSD or NVMe devices<br>- Minimum performance: 500 IOPS and 30 MB/s throughput<br>- Storage: <1 GB for KWDB system, with additional space needed based on data volume<br>- Avoid shared storage (NFS, CIFS, CEPH)<br> - HDDs not recommended for distributed cluster deployments |
| File System | ext4 recommended for optimal performance |

## Operating System and CPU Architectures

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

- Operating systems or versions not listed here **may** work with KWDB but are not officially supported.
- For installation packages not available on the [download page](https://gitee.com/kwdb/kwdb/releases/), contact [KWDB Technical Support](https://www.kaiwudb.com/support/).
:::


## Software Dependencies

The following table lists the required dependencies:

| Dependency    | Version   | Remarks |
| ------------- | --------- | ----------- |
| OpenSSL       | v1.1.1+   | N/A         |
| libprotobuf      | v3.6.1 ~ v21.x   | The default version of libprotobuf included in Ubuntu 18.04 is lower than the required version. Before deployment, install the required version in advance (versions 3.6.1 and 3.12.4 are recommended).       |
| GEOS          | v3.3.8+   | Optional    |
| xz-libs       | v5.2.0+   | N/A         |
| libgcc        | v7.3.0+   | N/A         |
| libgflags | System default | N/A |
| libkrb5 | System default | N/A |

During installation, KWDB verifies the necessary dependencies. If any are missing, the installation process will halt and prompt you to install them. If the target machine is offline, you will need to download the required dependencies from an internet-connected device and then transfer the files to the target machine.

## Ports

Ensure these default ports are available and not blocked by firewalls. Port settings can be modified during installation.

| Port        | Description |
| ----------- | ----------- |
| `8080`      | Port for HTTP requests and web services |
| `26257`     | Port for connections from clients, applications, and other nodes |
|`27257`| Port for inter-node brpc communication between KWDB time-series engines|

## Installation Packages and Compiled Versions

Use pre-compiled installation packages or compile from source code as needed.

### Installation Package

Obtain the DEB or RPM installation package for your system environment, copy the package to the target machine, and then decompress it.

::: warning Note
The KWDB repository currently provides [DEB or RPM installation packages](https://gitee.com/kwdb/kwdb/releases/) for the following systems and architectures. For packages for other systems or architectures, please contact [KWDB Technical Support](https://www.kaiwudb.com/support/).

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

### Source Code Compilation

Complete source code download and compilation according to the [KWDB Compilation and Installation Instructions](https://gitee.com/kwdb/kwdb/blob/master/README.en.md#compilation-and-installation).

## Node Configuration

### SSH Passwordless Login

To enable secure communication between cluster nodes, configure passwordless SSH authentication:

1. Log into a node and generate a public/private key pair.

   ```shell
   ssh-keygen -f ~/.ssh/id_rsa -N ""
   ```

   Parameters:

   - `-f ~/.ssh/id_rsa`: Sets the output path for the key files.
   - `-N`: Creates the key without a passphrase, necessary for automated authentication.

2. Copy the public key to each cluster node.

   ```shell
   ssh-copy-id -f -i ~/.ssh/id_rsa.pub -o StrictHostKeyChecking=no <target_node>
   ```

3. Verify SSH connectivity with each node.

   ```shell
   ssh <target_node>
   ```

### Time Synchronization

KWDB requires synchronized time across all nodes to maintain data consistency. If a node's system time differs by more than 80% of the allowed error (default 500 ms) from at least half of the other nodes, it will stop automatically to avoid data inconsistencies. Ensure every node runs NTP or another time synchronization service.

The following example demonstrates how to configure time synchronization on CentOS 7.

1. SSH into the target node.

2. Disable the `timesyncd` service.

   ```shell
   timedatectl set-ntp no
   ```

3. Install the NTP package.

   ```shell
   sudo apt install ntp
   ```

4. Stop any running NTP processes.

   ```shell
   service ntp stop
   ```

5. Synchronize time with a public NTP server.

   ```shell
   ntpdate -u 0.cn.pool.ntp.org
   ```

6. Configure NTP servers by editing `/etc/ntp.conf`.

   ```shell
   server 0.cn.pool.ntp.org iburst
   server 1.cn.pool.ntp.org iburst
   server 2.cn.pool.ntp.org iburst
   server 3.cn.pool.ntp.org iburst
   ```

7. Start and enable the NTP service.

   ```shell
   service ntp start
   ```

8. Repeat these steps on every node in the cluster.
