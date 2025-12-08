---
title: Overview
id: overview
---

# Cluster Deployment Overview

KWDB supports the following cluster deployment types:

| Category | Multi-Replica Cluster | Single-Replica Cluster |
| -------- | --------------------- | ---------------------- |
| **Definition** | KWDB runs on multiple nodes within the same data center. Each data range has 3 replicas by default, distributed across different nodes. | KWDB runs on multiple nodes within the same data center. Each data range has only one replica; all data storage and update operations are handled by that single replica. |
| **Performance** | - **Writes:** Lower than single node and single-replica clusters<br>- **Reads:**<br>  • Simple queries: slightly lower than single node<br>  • Complex queries: same as single-replica clusters<br><br>**Tip**: You can optimize write performance with the following parameters:<br>- `ts.raft_log.sync_period`: Extends the disk flush cycle for time-series data raft logs<br>- `ts.raftlog_combine_wal.enabled`: Enables merging of time-series data raft logs and WAL<br>For more information, see [Cluster Parameters](../db-operation/cluster-settings-config.md#cluster-parameters).<br>**Note**: After enabling these optimizations, unflushed data may be lost if a node crashes unexpectedly. | - **Writes:** Higher than multi-replica clusters but slightly lower than single node<br>- **Reads:**<br>  • Simple queries: slightly lower than single node<br>  • Complex queries: same as multi-replica clusters |
| **Cluster Scaling** | Supports cluster scale-out and scale-in. For more information, see [Cluster Scaling](../db-operation/cluster-scale.md#multi-replica-cluster-scale-out). | Supports only cluster scale-out. For more information, see [Cluster Scaling](../db-operation/cluster-scale.md#single-replica-cluster-scale-out). |
| **High Availability** | Supports high availability with automatic failover and strong data consistency. For more information, see [Cluster High Availability](../db-operation/cluster-ha.md#multi-replica-cluster-high-availability).<br><br>**Note**: After extending the disk flush cycle for time-series data raft logs, unflushed data may be lost if a node crashes unexpectedly. | - Does not support high availability.<br>- When cluster nodes fail, write operations, queries, and DDL statements may fail.<br>- When the number of failed nodes exceeds half of the total nodes, all operations will be suspended. |
| **Data Balancing** | Supports automatic data balancing after scaling operations. | Does not support automatic data balancing after scaling out the cluster. |

single-node deployment differs slightly from cluster deployment. For more information, see [Single-node Deployment](../quickstart/overview.md).

This section includes the following documents:

- [Deployment Workflow](./deploy-workflow.md)
- Preparation
  - [Prepare for Bare-Metal Deployment](./prepare/before-deploy-bare-metal.md)
  - [Prepare for Container Deployment](./prepare/before-deploy-docker.md)
- Cluster Deployment
  - [Deploy Using Scripts](./cluster-deployment/script-deployment.md)
  - [Deploy Using kwbase CLI](./cluster-deployment/kwbase-cli-deployment.md)
  - [Deploy Using Docker Run Command](./cluster-deployment/docker-deployment.md)
- Cluster Configuration
  - [Create Users](./user-config.md)
  - Configure Cluster Settings
    - [Bare-Metal Deployment](./cluster-config/cluster-config-bare-metal.md)
    - [Container Deployment](./cluster-config/cluster-config-docker.md)
- Cluster Management
  - [Start and Stop KWDB Service](./local-start-stop.md)
  - [Uninstall Clusters](./uninstall-cluster.md)