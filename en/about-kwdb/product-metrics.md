---
title: System Requirements
id: product-metrics
---

# System Requirements

## Operating Systems and CPU Architectures

KWDB can be deployed on the following operating systems.

| Operating System | Supported CPU Architectures |
|---|---|
| CentOS 7, 8 | x86_64 |
| openEuler 22.03, 24.03 | x86_64 |
| Ubuntu 20.04, 22.04, 24.04 | x86_64 / ARM64 |
| UOS 1070e | x86_64 / ARM64 |

::: warning Note
Operating systems or versions not listed here **may** work with KWDB but are not officially supported.
:::

## Hardware Requirements

| Item | Requirements |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| CPU and Memory | A minimum of 4 CPU cores and 8 GB RAM per node is recommended. |
| Disk | - Recommended: SSD or NVMe devices. Avoid shared storage (NFS, CIFS, CEPH).<br>- Minimum performance: 500 IOPS and 30 MB/s throughput.<br>- Storage: less than 1 GB for the KWDB system itself; actual disk space depends on business data volume. |
| File System | ext4 recommended. |
