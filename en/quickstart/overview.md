---
title: Overview
id: overview
---

# Overview

This section describes how to quickly get started with KWDB using single-node deployment. For cluster deployment, see [Cluster Deployment](../deployment/overview.md).

## Deployment Preparation

Before deploying KWDB, check that the hardware, operating system, software dependencies, and ports of the node to be deployed meet the requirements. For details, see [Deployment Preparation](./prepare.md).

## Deploying KWDB

KWDB provides multiple deployment methods to meet the needs of different users and scenarios:

| Deployment Method | Features | Target Scenarios | Technical Requirements | Supported Environments |
|---------|------|---------|------|---------|
| **[Quick Deployment](./deploy/quick-deploy.md)** | One-click automated deployment using scripts | First-time users evaluating KWDB | Basic Linux operation experience | Bare-metal, Containerized |
| **[Installer — Command-Line Mode](./deploy/quickstart-installer-cli.md)** | Step-by-step guided installation through text menus; no extra dependencies required; single-command deployment | Users who need a stable and fast deployment | Basic Linux operation experience | Bare-metal, Containerized |
| **[Installer — Terminal Graphical Interaction Mode](./deploy/quickstart-installer-dialog.md)** | Graphical interaction experience in the character interface, with checkboxes, input boxes, progress bars, and other components | Users who prefer a character-interface graphical experience | Basic Linux operation experience | Bare-metal, Containerized |
| **[Container - Docker Run](./deploy/deploy-docker-run.md)** | Run containers directly using `docker run` commands | Scenarios that require quickly setting up a test or verification environment | Familiar with Docker command-line operations | Containerized |
| **[Container - Docker Compose](./deploy/deploy-yaml.md)** | Orchestration deployment based on YAML files; currently only supports insecure mode | Scenarios for testing, verification, and container orchestration | Familiar with Docker and Compose basics | Containerized |
| **[CLI Command Line](./deploy/deploy-cli.md)** | Supports fine-grained control and deep customization | Scenarios with customization requirements | Familiar with database deployment and command-line operations | Bare-metal |

::: warning Note
KWDB single-node deployment supports [DRBD-based primary-replica replication](../best-practices/single-ha.md) high availability. If you plan to implement a high availability solution, refer to the relevant documentation first.
:::

## Using KWDB

After deployment, you can connect to and manage KWDB using any of the following methods:

| Connection Method | Features | Use Cases |
|---------|------|---------|
| **[kwbase CLI Tool](./access/access-cli.md)** | Built-in CLI tool supporting both secure and insecure modes, suitable for automation scripts | Command-line operations, automation scripts, operations management |
| **[KaiwuDB JDBC](./access/access-jdbc.md)** | Standard JDBC interface with connection pooling support, suitable for Java application integration | Java application development, production environment integration |
| **[KaiwuDB Developer Center](./access/access-kdc.md)** | Graphical management interface with intuitive, user-friendly design, supports visual operations | Visual management, data browsing, query debugging |

## Uninstalling KWDB

If you need to uninstall KWDB, see [Uninstall KWDB](../deployment/uninstall-cluster.md).
