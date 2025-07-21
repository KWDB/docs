---
title: Workflow
id: deploy-workflow
---

# Workflow

This section outlines the steps for deploying, configuring, and maintaining your KWDB cluster in both bare-metal and container environments.

## Preparation

Before deploying your KWDB cluster, ensure that all target nodes meet the hardware and software requirements outlined in:

- [Prepare for Bare-Metal Clusters](./prepare/before-deploy-bare-metal.md)
- [Prepare for Container Clusters](./prepare/before-deploy-docker.md)

## Deployment

KWDB supports three deployment methods to accommodate different use cases and technical preferences:

- **[Deploy using scripts (Recommended)](./cluster-deployment/script-deployment.md)**: The most streamlined deployment approach that requires only a few commands to set up a complete cluster. This method provides built-in fault detection, automated node recovery, and optimal configuration for both test and production environments.

- **[Deploy using kwbase CLI](./cluster-deployment/kwbase-cli-deployment.md)**: Suitable for users who compile and deploy from source code. This method is ideal for:

  - Users with technical expertise who need fine-grained control
  - Scenarios requiring deep customization of the deployment process

- **[Deploy using Docker](./cluster-deployment/docker-deployment.md)**: Container-based deployment suitable for:

  - Users who prefer containerization technology
  - Containerized test environments
  - Lightweight development scenarios

## Cluster Configuration

After deployment, perform the following post-deployment operations:

- **Create Database Users (Optional)**: Create database users using either
  - The `add_user.sh` script located in the installation directory
  - kwbase CLI commands

  For instructions, see [Create Users](./user-config.md).

- **Configure Cluster Parameters (Optional)**:

  - **For deployment using scripts:**
  
    - Bare metal: The system generates `kaiwudb_env` and `kaiwudb.service` files for configuring startup flags and resource allocation. For instructions, see [Configure Bare Metal Clusters](./cluster-config/cluster-config-bare-metal.md).
    - Container: The system creates a Docker Compose configuration file (`docker-compose.yml`) in `/etc/kaiwudb/script/` for flag configuration and resource allocation. For instructions, see [Configure Container Clusters](./cluster-config/cluster-config-docker.md).

  - **For Deployment using kwbase CLI or Docker**: You can configure startup flags using `kwbase start` or `kwbase start-single-replica` commands. For instructions, see [kwbase start](../tool-command-reference/client-tool/kwbase-sql-reference.md#kwbase-start) and [kwbase start-single-replica](../tool-command-reference/client-tool/kwbase-sql-reference.md#kwbase-start-single-replica).

- **Connect to KWDB**: You can interact with your KWDB cluster through multiple interfaces:

  - [kwbase CLI tool](../../en/quickstart/access-kaiwudb/access-kaiwudb-cli.md)
  - Supported [connectors](../../en/development/overview.md)
  - [KaiwuDB Developer Center](../../en/kaiwudb-developer-center/overview.md)

## Cluster Management

For cluster management operations, see:

- [Start and Stop KWDB](./local-start-stop.md) for node management
- [Uninstall Clusters](./uninstall-cluster.md) for complete cluster removal