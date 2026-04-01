---
title: Deployment Preparation
id: quickstart-prepare
---

# Deployment Preparation

## Hardware

The following table lists the required hardware specifications for KWDB deployment.

| Item | Requirements |
| --- | --- |
| CPU and Memory | We recommend a minimum of 4 CPU cores and 8GB RAM for single-node deployment. For workloads with large data volumes, complex operations, high concurrency, and high-performance scenarios, configure higher CPU and memory resources to ensure efficient system operation. |
| Disk | - Use SSD or NVMe devices; avoid shared storage systems like NFS, CIFS, or CEPH.<br>- The disk must achieve 500 IOPS and 30 MB/s processing efficiency.<br>- When deploying single-node version using HDD disks, avoid using too many devices or too high write operations per second, as this significantly decreases data write performance.<br>- KWDB system startup requires minimal disk capacity (less than 1GB). The actual required disk size mainly depends on your workload. |
| File System | We recommend using the ext4 file system. |

## Operating System

KWDB supports the following operating systems:

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

- Container deployment requires Docker to be installed on the target machine. If not installed, see [Docker Official Installation Documentation](https://docs.docker.com/desktop/install/linux-install/) for installation. For environments without internet access, download Docker binary packages for offline installation. For details, see [Docker Offline Installation Guide](https://docs.docker.com/engine/install/binaries/).
- Unmentioned operating system versions **may** run KWDB, but are not officially supported.

:::

## Software Dependencies

### Bare-Metal Deployment

The following table lists the required dependencies for the target machine:

| Dependency | Version | Description |
| --- | --- | --- |
| OpenSSL | v1.1.1+ | N/A |
| libprotobuf | v3.6.1 ~ v21.x | The default libprotobuf version in Ubuntu 18.04 is lower than required. You need to install a higher version before deployment. |
| GEOS | v3.3.8+ | Optional dependency |
| xz-libs | v5.2.0+ | N/A |
| libgcc | v7.3.0+ | N/A |
| libgflags | System default | N/A |
| libkrb5 | System default | N/A |

During installation, KWDB checks dependencies. If dependencies are missing, the installation exits and prompts for missing dependencies. If the target machine cannot access the internet, download all dependency files on a machine with internet access, then copy them to the target machine for installation.

### Container Deployment

When using [script](./deploy/deploy-script.md) for deployment, the target machine needs to have Docker Compose (version 1.20.0 and above) installed.

- Online installation: See [Docker Compose Official Installation Documentation](https://docs.docker.com/compose/install/)
- Offline installation: See [Docker Compose Offline Installation Guide](https://docs.docker.com/compose/install/standalone/)
- Quick installation for Ubuntu/Debian systems:

    ```shell
    sudo apt-get install docker-compose
    ```

## Port Requirements

The following table lists the default ports used by KWDB services. You can modify these ports during installation and deployment if needed.

| Port | Description |
| --- | --- |
| `8080` | Database web service port |
| `26257` | Database service port and external connection port |

## Installation Packages

Obtain the appropriate installation package for your system, copy it to the target machine, and extract it:

```shell
tar -zxvf <package_name>
```

The extracted directory contains these files:

| File | Description |
| --- | --- |
| `add_user.sh` | Creates users for the KWDB database after installation and startup. |
| `deploy.cfg` | Configuration file for setting up node IP addresses, ports, and other deployment settings. |
| `deploy.sh` | Deployment script for installation, uninstallation, startup, status checks, shutdown, and restart operations. |
| `packages` directory | Contains DEB, RPM, and Docker image packages.<br>**Note**: Specific files included vary by package type. |
| `utils` directory | Contains utility scripts. |

