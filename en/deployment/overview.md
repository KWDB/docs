---
title: Overview
id: overview
---

# Overview

## Cluster Types

KWDB supports the following cluster deployment types:

| Category | Multi-Replica Cluster | Single-Replica Cluster |
| -------- | --------------------- | ---------------------- |
| **Definition** | KWDB runs on multiple nodes within the same data center. Each data range has 3 replicas by default, distributed across different nodes. | KWDB runs on multiple nodes within the same data center. Each data range has only one replica; all data storage and update operations are handled by that single replica. |
| **Performance** | - **Writes:** Lower than single node and single-replica clusters<br>- **Reads:**<br>  - Simple queries: slightly lower than single node<br>  - Complex queries: same as single-replica clusters<br><br>**Tip**: You can optimize write performance with the following parameters:<br>- `ts.raft_log.sync_period`: Extends the disk flush cycle for time-series data raft logs<br>- `ts.raftlog_combine_wal.enabled`: Enables merging of time-series data raft logs and WAL<br>For more information, see [Cluster Parameters](../db-operation/cluster-settings-config.md#cluster-parameters).<br>**Note**: After enabling these optimizations, unflushed data may be lost if a node crashes unexpectedly. | - **Writes:** Higher than multi-replica clusters but slightly lower than single node<br>- **Reads:**<br>  - Simple queries: slightly lower than single node<br>  - Complex queries: same as multi-replica clusters |
| **Cluster Scaling** | Supports cluster scale-out and scale-in. For more information, see [Cluster Scaling](../db-operation/cluster-scale.md#multi-replica-cluster-scale-out). | Supports only cluster scale-out. For more information, see [Cluster Scaling](../db-operation/cluster-scale.md#single-replica-cluster-scale-out). |
| **High Availability** | Supports high availability with automatic failover and strong data consistency. For more information, see [Cluster High Availability](../db-operation/cluster-ha.md#multi-replica-cluster-high-availability).<br><br>**Note**: After extending the disk flush cycle for time-series data raft logs, unflushed data may be lost if a node crashes unexpectedly. | - Does not support high availability.<br>- When cluster nodes fail, write operations, queries, and DDL statements may fail.<br>- When the number of failed nodes exceeds half of the total nodes, all operations will be suspended. |
| **Data Balancing** | Supports automatic data balancing after scaling operations. | Does not support automatic data balancing after scaling out the cluster. |

Single-node deployment differs slightly from cluster deployment. For more information, see [Single-node Deployment](../quickstart/overview.md).

## Deployment Process

### Preparation

Before deploying a KWDB cluster, follow [Preparation](./cluster-prepare.md) to verify that the hardware and software environments on the target nodes meet the requirements.

### Cluster Deployment

KWDB provides multiple cluster deployment methods to meet different user needs and scenarios:

| Deployment Method | Characteristics | Target Users/Scenarios | Technical Requirements | Supported Environments |
|---------|------|---------|------|---------|
| **[Installer CLI](./cluster-deployment/installer-cli.md)** | No extra dependencies are required; the installer guides the deployment step by step through text menus and validates parameters in real time. | Users who need a simple, command-line deployment flow on basic Linux systems | Basic Linux command-line experience | Bare metal, Containerized |
| **[Installer Dialog](./cluster-deployment/installer-dialog.md)** | Provides a graphical dialog-based deployment flow with guided prompts and configuration screens. | Users who prefer a visual deployment interface | Basic Linux operation experience | Bare metal, Containerized |
| **[Docker Run](./cluster-deployment/docker-deployment.md)** | Containerized deployment using `docker run` directly | Users who are familiar with Docker command-line operations | Docker command-line experience | Containerized |
| **[kwbase CLI](./cluster-deployment/kwbase-cli-deployment.md)** | Supports deep customization of the deployment process | Users with a technical background who want fine-grained control | Familiarity with database deployment and command-line operations | Bare metal |

### Cluster Management

- To stop or restart individual nodes in the cluster, see [Start and Stop KWDB Service](./local-start-stop.md).
- To uninstall the cluster, see [Uninstall KWDB](./uninstall-cluster.md).