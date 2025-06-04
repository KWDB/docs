---
title: System Requirements
id: product-metrics
---

# Hardware and Software Requirements

## Operating Systems and CPU Architectures

KWDB can be deployed on the following operating systems.

| **Operating System** | **Version**            | **CPU Architecture** | **Container** | **Bare-Metal** |
| :------------------- | :--------------------- | :--------------- | ------------- | -------------- |
| Anolis               | 7                      | ARM_64           | √             | -              |
|                      | 7                      | x86_64           | √             | -              |
|                      | 8                      | ARM_64           | √             | √              |
|                      | 8                      | x86_64           | √             | √              |
| CentOS               | 7                      | x86_64           | √             | -              |
|                      | 8                      | x86_64           | √             | -              |
| Debian               | 11                    | ARM_64           | √             | -              |
| KylinOS              | 10                    | ARM_64           | √             | √              |
|                      | 10                    | x86_64           | √             | √              |
| openEuler            | 22.03                  | x86_64           | √             | -              |
| Ubuntu               | 18.04                 | x86_64           | √             | √              |
|                      | 20.04                 | ARM_64           | √             | √              |
|                      | 20.04                 | x86_64           | √             | √              |
|                      | 22.04                 | ARM_64           | √             | √              |
|                      | 22.04                 | x86_64           | √             | √              |
|                      | 24.04                 | ARM_64           | √             | √              |
|                      | 24.04                 | x86_64           | √             | √              |
| UOS                  | 20                    | x86_64           | √             | √              |
|                      | 20                    | ARM_64           | √             | √              |

::: warning Note
Operating systems or versions not listed here **may** work with KWDB but are not officially supported.
:::

## Hardware Requirements

| Item  | Requirements  |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| CPU and Memory | - Minimum: 4 CPU cores and 8GB RAM per node <br> - For high-volume data, complex workloads, high concurrency, or performance-critical applications, allocate additional resources accordingly |
| Disk       | - Recommended: SSD or NVMe devices<br>- Minimum performance: 500 IOPS and 30 MB/s throughput<br>- Storage: <1GB for KWDB system, additional space needed based on data volume and enabled features like compression that reduce disk usage. For production environments, plan hardware resources according to your business scale and performance requirements.<br>- Avoid shared storage (NFS, CIFS, CEPH)|
| File System | ext4 recommended for optimal performance |
