---
title: Deployment Preparation
id: cluster-prepare
---

# Deployment Preparation

## Hardware

:::warning Note
To improve availability and reduce the risk of data loss, it is recommended to run only one node per machine. KWDB uses a cross-node replication mechanism. Running multiple nodes on a single machine increases the likelihood of data loss if that machine fails.
:::

The following table lists the hardware specifications required for KWDB deployment:

| Item | Requirements |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| CPU and Memory | A minimum of 4 CPU cores and 8 GB RAM per node is recommended. For high-volume data, complex workloads, high concurrency, or performance-critical applications, allocate additional CPU and memory resources accordingly. |
| Disk | - Recommended: SSD or NVMe devices. Avoid shared storage (NFS, CIFS, CEPH).<br>- Minimum performance: 500 IOPS and 30 MB/s throughput.<br>- Storage: less than 1 GB for the KWDB system itself; actual disk space depends on business data volume. |
| File System | ext4 recommended. |


## Operating System

KWDB has been fully and systematically verified on the following operating systems and CPU architecture combinations:

| Operating System | Version | Bare Metal - ARM64 | Bare Metal - x86_64 | Container - ARM64 | Container - x86_64 |
|---------|------|:---:|:---:|:---:|:---:|
| CentOS | 7 | | | | ✓ |
| | 8 | | | | ✓ |
| openEuler | 22.03 | | ✓ | | ✓ |
| | 24.03 | | ✓ | | ✓ |
| Ubuntu | 20.04 | ✓ | ✓ | ✓ | ✓ |
| | 22.04 | ✓ | ✓ | ✓ | ✓ |
| | 24.04 | ✓ | ✓ | ✓ | ✓ |
| UOS | 1070e | ✓ | ✓ | ✓ | ✓ |

:::warning Note

- Container deployment requires Docker installed on the target machine. If Docker is not installed, refer to the [Docker official installation documentation](https://docs.docker.com/desktop/install/linux-install/). For offline environments, download the Docker binary package for offline installation. See [Docker Offline Installation Guide](https://docs.docker.com/engine/install/binaries/).
- If SELinux is enabled on the system, the `service` command cannot be used to manage KWDB. It is recommended to disable SELinux before deployment.
- To deploy on bare metal using other Linux distributions, run `ldd --version` to check the glibc version. Version >= 2.28 should work in theory but is not officially supported by KWDB.
- For installation packages not available on the [download page](https://www.kaiwudb.com/download?tab=2), contact [KWDB Technical Support](https://www.kaiwudb.com/about/support).

:::

## Software Dependencies

### Bare Metal Deployment

During installation, KWDB verifies the necessary dependencies. If any are missing, the installation process will halt and prompt you to install them. If the target machine is offline, you will need to download the required dependencies on an internet-connected machine based on the target machine's operating system, and then copy the dependency files to the target machine.

The following table lists the dependencies that must be installed on the target machine when deploying with the installer:

| OS Type | libc | libgcc | libstdc++ |
| --- | --- | --- | --- |
| Debian series | libc6 >= 2.28 | libgcc1/libgcc-s1 >= 7.3.0 | libstdc++6 >= 7.3.0 |
| Red Hat series | glibc >= 2.28 | libgcc >= 8.3.0 | libstdc++ >= 8.3.0 |

### Container Deployment

In addition to the above dependencies, when deploying with the installer, Docker Compose (version 1.20.0 or higher) must be installed on the target machine.

- For online installation, see [Docker Compose official installation documentation](https://docs.docker.com/compose/install/).
- For offline installation, see [Docker Compose Offline Installation Guide](https://docs.docker.com/compose/install/standalone/).
- Quick installation for Ubuntu/Debian systems:

    ```shell
    sudo apt-get install docker-compose
    ```

## Port Requirements

The following table lists the default ports used by KWDB services. Ports can be modified during installation and deployment.

| Port | Description |
|--------|------|
| `8080` | Database Web service port |
| `26257` | Database service port, node listening port, and external connection port |
| `27257` | brpc communication port between KWDB time-series engines |

## Installation Packages, Container Images, and Compilation Versions

Choose the installation package, container image, or source code compilation version based on your deployment scenario:

### Installation Packages

The KWDB installer is packaged as a `.run` self-extracting executable that bundles all deployment resources and supports both command-line mode and terminal graphical interaction mode.

The KWDB [download page](https://www.kaiwudb.com/download?tab=2) currently provides installers for the following systems and architectures. For other systems or architectures, contact [KWDB Technical Support](https://www.kaiwudb.com/about/support):

- Ubuntu V20.04 x86_64
- Ubuntu V20.04 ARM64
- Ubuntu V22.04 x86_64
- Ubuntu V22.04 ARM64

### Container Images

KWDB supports obtaining container images through the following methods:

- **KWDB versions before 3.1.0**

  [Download](https://gitee.com/kwdb/kwdb/releases) the release package, then import the `KaiwuDB.tar` file from the `kwdb_install/packages` directory.

  ```bash
  docker load < KaiwuDB.tar
  Loaded image: "image-name"
  ```

- **KWDB 3.1.0 and later versions**

  Run the following command to obtain the KWDB Docker image. To get the latest version, run `docker pull kwdb/kwdb:latest`.

  ```bash
  docker pull kwdb/kwdb:<version>
  ```

### Source Code Compilation and Installation

Follow the [KWDB Compilation and Installation Instructions](https://gitee.com/kwdb/kwdb#%E7%BC%96%E8%AF%91%E5%92%8C%E5%AE%89%E8%A3%85) to download, compile, and install from source code.

## Node Configuration

### SSH Passwordless Login

1. Log into the current node and generate a public/private key pair.

   ```shell
   ssh-keygen -f ~/.ssh/id_rsa -N ""
   ```

   Parameters:

   - `-f`: Specifies the output path for the generated key files.
   - `-N`: Sets the key passphrase to empty to enable passwordless login.

2. Copy the public key to each cluster node.

   ```shell
   ssh-copy-id -f -i ~/.ssh/id_rsa.pub -o StrictHostKeyChecking=no <target_node>
   ```

3. Verify that SSH passwordless login works for each cluster node.

   ```shell
   ssh <target_node>
   ```

### Time Synchronization

KWDB uses a moderate clock synchronization mechanism to maintain data consistency. When a node detects that its machine time differs from the machine time of at least 50% of the other nodes in the cluster by more than 80% of the maximum allowed clock error (default 500 ms), that node will stop automatically to avoid violating data consistency and introducing stale data read/write risks. Every node must run NTP (Network Time Protocol) or another clock synchronization service to prevent clock drift.

The following example demonstrates how to configure time synchronization on CentOS 7.

1. SSH into the node where the cluster will be deployed.

2. Disable the `timesyncd` service.

   ```shell
   timedatectl set-ntp no
   ```

3. Install the NTP service.

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

6. Open `/etc/ntp.conf`, find the `server` and `pool` entries, and update them as follows:

   ```shell
   server 0.cn.pool.ntp.org iburst
   server 1.cn.pool.ntp.org iburst
   server 2.cn.pool.ntp.org iburst
   server 3.cn.pool.ntp.org iburst
   ```

7. Start the NTP service.

   ```shell
   service ntp start
   ```

8. Repeat these steps on every node in the cluster where KWDB will be installed.
