---
title: Overview
id: overview
---

# Overview

This guide walks you through setting up KWDB for single-node deployment. For instructions on cluster deployment, see [Cluster Deployment](../deployment/overview.md).

## Deployment Preparation

Before deploying KWDB, ensure your environment meets the minimum requirements. For details, see [Deployment Preparation](./prepare.md).

## Deploying KWDB

KWDB provides multiple deployment methods to meet the needs of different users and scenarios:

| Method | Features | Target Users | Technical Requirements | Supported Environments |
|---------|------|---------|------|---------|
| **[Quick Deployment](./deploy/quick-deploy.md)** | One-click automated deployment | First-time users evaluating KWDB | Basic Linux operation experience | Bare-metal, Containerized |
| **[Script (Recommended)](./deploy/deploy-script.md)** | One-click deployment using built-in scripts | Production users requiring stable and quick deployment | Basic Linux operation experience | Bare-metal, Containerized |
| **[Container - Docker Run](./deploy/deploy-docker-run.md)** | Run containers directly using `docker run` command | Users who need to quickly set up testing or validation environments | Familiar with Docker command-line operations | Containerized |
| **[Container - Docker Compose](./deploy/deploy-yaml.md)** | Orchestration deployment based on YAML files, currently only supports insecure mode | Users familiar with container orchestration, suitable for testing or quick validation | Familiar with Docker & Compose basics | Containerized |
| **[CLI Command Line](./deploy/deploy-cli.md)** | Supports fine-grained control and deep customization | Experienced users, customized deployment scenarios | Familiar with database deployment process and command-line operations | Bare-metal |

::: warning Note
Single-node KWDB deployments support [DRBD-based primary-replica replication](../best-practices/single-ha.md). If you plan to implement a high availability solution, refer to the relevant documentation first.
:::

## Using KWDB

After deployment, you can connect to KWDB and manage database operations using any of the following methods:

| Method | Features | Use Cases |
|---------|------|---------|
| **[kwbase CLI](./access/access-cli.md)** | Built-in CLI tool supporting both secure and insecure modes, suitable for automation scripts | Command-line operations, automation scripts, operations management |
| **[KaiwuDB JDBC](./access/access-jdbc.md)** | Standard JDBC interface with connection pooling support, suitable for Java application integration | Java application development, production environment integration |
| **[KaiwuDB Developer Center](./access/access-kdc.md)** | Graphical management interface with intuitive, user-friendly design, supports visual operations | Visual management, data browsing, query debugging |

## Uninstalling KWDB

If you need to uninstall KWDB, see [Uninstall KWDB](../deployment/uninstall-cluster.md).
