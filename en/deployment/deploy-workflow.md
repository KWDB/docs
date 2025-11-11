---
title: Workflow
id: deploy-workflow
---

# Workflow

## Preparation

Before deploying a KWDB cluster, verify that the hardware and software environment of the nodes meets the requirements:

- [Prepare for Bare-Metal Deployment](./prepare/before-deploy-bare-metal.md)
- [Prepare for Container Deployment](./prepare/before-deploy-docker.md)

## Cluster Deployment

Choose from the following deployment methods:

| Method | Description | Best For | Requirements |
|--------|-------------|----------|--------------|
| **[Deploy Using Scripts (Recommended)](./cluster-deployment/script-deployment.md)** | Automated deployment with a few commands. Includes built-in fault detection and node recovery. | Quick setup of test or production environments | - |
| **[Deploy Using kwbase CLI](./cluster-deployment/kwbase-cli-deployment.md)** | Manual deployment using kwbase CLI commands with full customization control. | Advanced users needing fine-grained configuration | - |
| **[Deploy Using Docker Run Command](./cluster-deployment/docker-deployment.md)** | Container-based deployment. | Lightweight containerized development and testing | Docker installed |

## Cluster Configuration

After the cluster is deployed and started, complete the following operations:

**1. Create Database Users (Optional)**: Create database users using the `add_user.sh` script in the installation package directory or using kwbase CLI, then use the credentials to connect and operate the database. For details, see [Create Users](./user-config.md).

**2. Configure Cluster Parameters (Optional)**: Configuration methods vary depending on your deployment type:

- Script Deployment: using the following files to set startup flags and CPU resource usage:
  - Bare Metal: `kaiwudb_env` and `kaiwudb.service`. For details, see  [Configure Bare-Metal Deployments](./cluster-config/cluster-config-bare-metal.md).
  - Container: `docker-compose.yml`. For details, see [Configure Container Deployments](./cluster-config/cluster-config-docker.md).

- kwbase CLI and Docker Run Deployment: set cluster startup flags through the following commands:
  - [`kwbase start`](../tool-command-reference/client-tool/kwbase-sql-reference.md#kwbase-start) for multi-replica clusters
  - [`kwbase start-single-replica`](../tool-command-reference/client-tool/kwbase-sql-reference.md#kwbase-start-single-replica) for for single-replica clusters

**3. Connect to Cluster**: Connect to the cluster for data operations using any of the following methods:

- [`kwbase` CLI tool](../quickstart/access-kaiwudb/access-kaiwudb-cli.md)
- [KaiwuDB Developer Center](../kaiwudb-developer-center/overview.md)
- [Connectors](../development/overview.md) supported by KWDB

## Cluster Management

- To stop or restart a single node in the cluster, see [Start and Stop KWDB Services](./local-start-stop.md).
- To uninstall the cluster, see [Uninstall Cluster](./uninstall-cluster.md).