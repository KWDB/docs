---
title: Overview
id: overview
---

# Overview

## Cluster Types

KWDB supports the following cluster deployment types:

| Category | Multi-Replica Cluster | Single-Replica Cluster |
| -------- | --------------------- | ---------------------- |
| **Definition** | KWDB runs on multiple nodes within the same data center. Each data range has 3 replicas by default, distributed across different nodes. | KWDB runs on multiple nodes within the same data center. The entire cluster has only one data replica; all data storage and update operations are handled by that single replica. |
| **Performance** | Write performance is lower than single-node deployment and single-replica clusters. Read performance in simple scenarios is slightly lower than single-node deployment; in complex scenarios it is the same as single-replica clusters.<br><br>**Tip**: Multi-replica clusters can optimize write performance using the following parameters:<br>- `ts.raft_log.sync_period`: Extends the disk flush cycle for time-series data raft logs<br>- `ts.raftlog_combine_wal.enabled`: Enables merging of time-series data raft logs and WAL<br>For more information, see [Cluster Parameters](../db-operation/cluster-settings-config.md#cluster-parameters).<br>**Note**: After enabling these optimizations, unflushed data may be lost if a node crashes unexpectedly. | Write performance is higher than multi-replica clusters but slightly lower than single-node deployment. Read performance in simple scenarios is slightly lower than single-node deployment; in complex scenarios it is the same as multi-replica clusters. |
| **Cluster Scaling** | Supports cluster scale-out and scale-in. For more information, see [Cluster Scaling](../db-operation/cluster-scale.md). | Supports only cluster scale-out. For more information, see [Cluster Scaling](../db-operation/cluster-scale.md). |
| **High Availability** | Supports high availability with automatic failover and strong data consistency. For more information, see [Cluster High Availability](../db-operation/cluster-ha.md).<br><br>**Note**: After extending the disk flush cycle for time-series data raft logs, unflushed data may be lost if a node crashes unexpectedly. | Does not support high availability. When cluster nodes fail, write operations, queries, and DDL statements may fail. When the number of failed nodes exceeds half of the total nodes, all operations will be suspended. |
| **Data Balancing** | Supports automatic data balancing after scaling operations. | Does not support automatic data balancing after scaling out the cluster. |

Single-node deployment differs slightly from cluster deployment. For more information, see [Single-node Deployment](../quickstart/overview.md).

## Deployment Process

### Preparation

Before deploying a KWDB cluster, follow [Deployment Preparation](./cluster-prepare.md) to verify that the hardware, operating system, software dependencies, and ports on the target nodes meet the requirements.

### Cluster Deployment

KWDB provides multiple cluster deployment methods to meet different user needs and scenarios:

| Deployment Method | Characteristics | Target Scenarios | Technical Requirements | Supported Environments |
|---------|------|---------|------|---------|
| **[Installer — Command-Line Mode](./cluster-deployment/installer-cli.md)** | No extra dependencies required; numeric input for operation; built-in parameter validation; step-by-step guided installation through menus | Users who need a stable and fast deployment | Basic Linux command-line experience | Bare metal, Containerized |
| **[Installer — Terminal Graphical Interaction Mode](./cluster-deployment/installer-dialog.md)** | Graphical interaction experience in the character interface, with checkboxes, input boxes, progress bars, and other components | Users who prefer a character-interface graphical experience | Basic Linux operation experience | Bare metal, Containerized |
| **[Docker Run](./cluster-deployment/docker-deployment.md)** | Runs containers directly using `docker run` commands | Scenarios that require quickly setting up a test or verification environment | Docker command-line experience | Containerized |
| **[kwbase CLI](./cluster-deployment/kwbase-cli-deployment.md)** | Supports fine-grained control and deep customization | Scenarios with customization requirements | Familiarity with database deployment and command-line operations | Bare metal |

### Cluster Management

- To stop or restart individual nodes in the cluster, see [Start and Stop KWDB Service](./local-start-stop.md).
- To uninstall the cluster, see [Uninstall KWDB](./uninstall-cluster.md).
