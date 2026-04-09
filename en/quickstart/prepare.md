---
title: Deployment Preparation
id: quickstart-prepare
---

# Deployment Preparation

## Hardware

The following specifications are required for KWDB deployment:

| Item  | Requirements  |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| CPU and Memory | - Minimum: 4 CPU cores and 8 GB RAM per node <br> - For high-volume data, complex workloads, high concurrency, or performance-critical applications, allocate additional resources accordingly |
| Disk       | - Recommended: SSD or NVMe devices<br>- Minimum performance: 500 IOPS and 30 MB/s throughput<br>- Storage: <1 GB for KWDB system, with additional space needed based on data volume<br>- Avoid shared storage (NFS, CIFS, CEPH)<br> - HDDs not recommended for distributed cluster deployments |
| File System | ext4 recommended for optimal performance |

## Operating System

KWDB can be deployed on the following operating systems:

| Operating System | Version | Bare Metal |Bare Metal | Container |Container |
|---------|------|---------------|---------------|---------------|---------------|
| | | ARM64 |  x86_64 | ARM64 | x86_64 |
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

::: warning Note

- Container deployment requires Docker installed on the target machine. For new Docker installations, follow [Install Docker Engine](https://docs.docker.com/engine/install/). For offline Docker installations, see [Install Docker Engine from Binaries](https://docs.docker.com/engine/install/binaries/) and [Linux Post-Installation Steps for Docker Engine](https://docs.docker.com/engine/install/linux-postinstall/).
- Operating systems or versions not listed above **may** work with KWDB but are not officially supported.
- For installation packages not available on the [download page](https://gitee.com/kwdb/kwdb/releases/), contact [KWDB Technical Support](https://www.kaiwudb.com/support/).
:::

## Software Dependencies

### Bare-Metal Deployment

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

During installation, KWDB verifies the necessary dependencies. If any are missing, the installation process will halt and prompt you to install them. If the target machine is offline, you will need to download the required dependencies from an internet-connected device and then transfer the files to the target machine.

### Container Deployment

For deployment using scripts, Docker Compose (version 1.20.0 or higher) is required.

- For online installation instructions, see [Install Docker Compose](https://docs.docker.com/compose/install/).
- For offline installation instructions, see [Install Docker Compose Standalone](https://docs.docker.com/compose/install/standalone/).
- Quick installation for Ubuntu/Debian systems:

    ```shell
    sudo apt-get install docker-compose
    ```

## Port Requirements

Ensure these default ports are available and not blocked by firewalls. Port settings can be modified during installation.

| Port        | Description |
| ----------- | ----------- |
| `8080`      | Port for HTTP requests and web services |
| `26257`     | Port for connections of clients, applications, and other nodes |

## Installation Packages, Container Images, and Compilation Versions

Obtain installation packages, container images, or source code compilation versions based on your scenarios:

### Installation Packages

The KWDB repository currently provides [DEB or RPM installation packages](https://gitee.com/kwdb/kwdb/releases/) for the following systems and architectures. For packages for other systems or architectures, please contact [KWDB Technical Support](https://www.kaiwudb.com/support/).

- Ubuntu V20.04 x86_64
- Ubuntu V20.04 ARM64
- Ubuntu V22.04 x86_64
- Ubuntu V22.04 ARM64

After obtaining the DEB or RPM installation package for your system environment, copy the package to the target machine, then extract the installation package:

```shell
tar -zxvf <package_name>
```

The extracted directory contains the following files:

| File/Folder         | Description                                               |
|-------------------|-----------------------------------------------------------|
| `add_user.sh`     | Script for creating KWDB users after installation and startup.           |
| `deploy.cfg`      | Configuration file for node IP addresses, ports, and other options. |
| `deploy.sh`       | Script for KWDB installation, uninstallation, start, status check, and stop operations. |
| `packages`  | Stores DEB or RPM packages. <br>**Note**: Specific files included vary by installation package type.                                   |
| `utils`      | Stores utility scripts.                                             |

### Container Images

KWDB supports obtaining container images through the following methods:

- **KWDB versions before 3.1.0**

  [Download](https://gitee.com/kwdb/kwdb/releases) the container installation package, then import the `KaiwuDB.tar` file from the `kwdb_install/packages` directory.

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

Follow the [KWDB Compilation and Installation Instructions](https://gitee.com/kwdb/kwdb#compilation-and-installation) to download, compile, and install from source code.

