---
title: Overview
id: overview
---

# Cluster Deployment Overview

KWDB offers flexible deployment options. You can choose between two main cluster types based on your specific needs:

| Feature | Multi-Replica Cluster | Single-Replica Cluster |
|---------|----------------------|----------------------|
| **Basic Architecture** | Distributes three copies (default) of each dataset across multiple nodes within a data center. | Maintains a single copy of data across multiple nodes within a data center. |
| **Performance** | - Write operations are optimized for reliability over speed.<br>- Read performance varies:<br> • Simple queries: slightly lower than single-node deployments.<br>  • Complex queries: comparable to single-replica clusters. | - Faster writes compared to multi-replica setup.<br> - Read performance varies:<br>  • Simple queries: slightly lower than single-node deployments.<br>  • Complex queries: comparable to multiple-replica clusters. |
| **High Availability** | - Full high-availability support, including automatic failover.<br>- Ensures strong data consistency.<br>- For more information, see [High Availability](../../en/db-operation/ha/cluster-ha.md). | - No high-availability features.<br>- Node failures may disrupt read, write and DDL operations.<br>- Cluster stops if more than 50% of nodes fail. |

For single-node deployment, see [Single-Node Deployment](../../en/quickstart/overview.md) for specific requirements and commands.

This section includes the following documents:

- [Workflow](./deploy-workflow.md)
- Preparation
  - [Prepare for Bare-Metal Clusters](./prepare/before-deploy-bare-metal.md)
  - [Prepare for Container Clusters](./prepare/before-deploy-docker.md)
- Deployment
  - [Deploy Using Scripts](./cluster-deployment/script-deployment.md)
  - [Deploy Using kwbase CLI](./cluster-deployment/kwbase-cli-deployment.md)
  - [Deploy Using Docker](./cluster-deployment/docker-deployment.md)
- Cluster Configuration
  - [Create Users](./user-config.md)
  - Configure Cluster
    - [Configure Bare-Metal Clusters](./cluster-config/cluster-config-bare-metal.md)
    - [Configure Container Clusters](./cluster-config/cluster-config-docker.md)
- Cluster Management
  - [Start and Stop KWDB](./local-start-stop.md)
  - [Uninstall Clusters](./uninstall-cluster.md)