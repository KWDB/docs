---
title: Prepare for Container Deployment
id: before-deploy-docker
---

#  Prepare for Container Deployment

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

## Operating Systems and CPU Architectures

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

## Software Dependencies (Optional)

For deployment using scripts, Docker Compose (version 1.20.0 or higher) is required.

- For online installation instructions, see [Install Docker Compose](https://docs.docker.com/compose/install/).
- For offline installation instructions, see [Install Docker Compose Standalone](https://docs.docker.com/compose/install/standalone/).

To install Docker Compose via the command line:

```shell
sudo apt-get install docker-compose
```

## Ports

Ensure these default ports are available and not blocked by firewalls. Port settings can be modified during installation.

| Port        | Description |
| ----------- | ----------- |
| `8080`      | Port for HTTP requests and web services |
| `26257`     | Port for connections of clients, applications, and other nodes |
|`27257`| Port for inter-node brpc communication between KWDB time-series engines|

## Installation Packages and Images

Use pre-compiled installation packages or container images as needed.

### Installation Package

Obtain the [installation package](https://gitee.com/kwdb/kwdb/releases) for your system environment, copy the package to the target machine, and then decompress it.

::: warning Note
The KWDB repository currently provides [installation packages](https://gitee.com/kwdb/kwdb/releases/) for Ubuntu V22.04 ARM_64 and x86_64 architectures. For installation packages for other system and architectures, please contact [KWDB Technical Support](https://www.kaiwudb.com/support/).
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

### Obtaining Container Images

KWDB supports obtaining container images through the following methods:

- [Installation package](https://gitee.com/kwdb/kwdb/releases): Download the installation package corresponding to your system environment, then import the `KaiwuDB.tar` file from the `kwdb_install/packages` directory after extraction.

    ```bash
    docker load < KaiwuDB.tar
    Loaded image: "image-name"
    ```

- Docker command: Execute `docker pull kwdb/kwdb:<version>` to obtain the image.

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