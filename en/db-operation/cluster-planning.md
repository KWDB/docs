---
title: Cluster Planning
id: cluster-planning
---

# Cluster Planning

This section outlines the key considerations and requirements for planning your KWDB cluster deployment, including topology, hardware specifications, and security measures.

## Topology

When planning your deployment, choose a topology that meets your requirements for latency, availability, and resilience:

- **Cross-node replication**: KWDB uses cross-node replication to maintain data redundancy across multiple nodes. To ensure high availability and protect against data loss, deploy each KWDB node on a separate physical or virtual machine.
- **Replica count**: The default replica count for KWDB multi-replica clusters is 3. Ensure that the number of active nodes exceeds the replica count to maintain stable operation.

## Hardware

Each node requires essential resources such as CPU, memory, network, and storage. Review the hardware specifications for each node before deployment.

The following table outlines the minimum and recommended hardware requirements for deploying KWDB:

| Item  | Requirements  |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| CPU and Memory | - Minimum: 4 CPU cores and 8 GB RAM per node <br> - For high-volume data, complex workloads, high concurrency, or performance-critical applications, allocate additional resources accordingly |
| Disk       | - Recommended: SSD or NVMe devices<br>- Minimum performance: 500 IOPS and 30 MB/s throughput<br>- Storage: <1GB for KWDB system, additional space needed based on data volume and enabled features like compression that reduce disk usage. For production environments, plan hardware resources according to your business scale and performance requirements.<br>- Avoid using shared storage (NFS, CIFS, CEPH). <br> - When deploying the standalone version on HDDs, avoid excessive device count and high write loads, as concurrent writes can significantly degrade performance. Additionally, HDDs are not recommended for distributed cluster deployments.|
| File System | ext4 recommended for optimal performance |


## Security

Running a cluster in insecure mode exposes you to serious security risks:

- **Open access**: The cluster is open to all clients and any node’s IP address can be accessed without restrictions.
- **No authentication**: Users can connect without a password, and any user can log in as `root`, gaining full read/write access to all data.
- **Unencrypted communication**: Data is transmitted without encryption, leaving it vulnerable to interception and tampering.

To avoid these risks, KWDB strongly recommends deploying your cluster in **secure mode** using **TLS** encryption. This ensures that both nodes and clients are properly authenticated, and all data transfers are securely encrypted, protecting against unauthorized access and data manipulation.