---
title: System Requirements
id: product-metrics
---

# Hardware and Software Requirements

## Operating Systems and CPU Architectures

KWDB can be deployed on the following operating systems.

<table>
    <thead>
        <tr>
            <th rowspan="2">Operating System</th>
            <th rowspan="2">Version</th>
            <th colspan="2">Bare-Metal Deployment</th>
            <th colspan="2">Container Deployment</th>
        </tr>
        <tr>
            <th>ARM_64</th>
            <th>x86_64</th>
            <th>ARM_64</th>
            <th>x86_64</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="2" class="os-name">Anolis</td>
            <td>7</td>
            <td></td>
            <td></td>
            <td class="check">✓</td>
            <td class="check">✓</td>
        </tr>
        <tr>
            <td>8</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
        </tr>
        <tr>
            <td rowspan="2" class="os-name">CentOS</td>
            <td>7</td>
            <td></td>
            <td></td>
            <td></td>
            <td class="check">✓</td>
        </tr>
        <tr>
            <td>8</td>
            <td></td>
            <td></td>
            <td></td>
            <td class="check">✓</td>
        </tr>
        <tr>
            <td class="os-name">Debian</td>
            <td>V11</td>
            <td></td>
            <td></td>
            <td class="check">✓</td>
            <td></td>
        </tr>
        <tr>
            <td rowspan="3" class="os-name">KylinOS</td>
            <td>V10 SP2</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
        </tr>
        <tr>
            <td>V10 SP3 2303</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
            <td class="check"></td>
            <td class="check"></td>
        </tr>
        <tr>
            <td>V10 SP3 2403</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
        </tr>
        <tr>
            <td class="os-name">openEuler</td>
            <td>24.03</td>
            <td></td>
            <td></td>
            <td></td>
            <td class="check">✓</td>
        </tr>
        <tr>
            <td rowspan="3" class="os-name">Ubuntu</td>
            <td>V20.04</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
        </tr>
        <tr>
            <td>V22.04</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
        </tr>
        <tr>
            <td>V24.04</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
        </tr>
        <tr>
            <td rowspan="3" class="os-name">UOS</td>
            <td>1050e</td>
            <td></td>
            <td></td>
            <td class="check">✓</td>
            <td class="check">✓</td>
        </tr>
        <tr>
            <td>1060e</td>
            <td></td>
            <td></td>
            <td class="check">✓</td>
            <td class="check">✓</td>
        </tr>
        <tr>
            <td>1070e</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
        </tr>
        <tr>
            <td class="os-name">Windows Server</td>
            <td>WSL2</td>
            <td></td>
            <td class="check">✓</td>
            <td></td>
            <td class="check">✓</td>
        </tr>
    </tbody>
</table>

::: warning Note
Operating systems or versions not listed here **may** work with KWDB but are not officially supported.
:::

## Hardware Requirements

| Item  | Requirements  |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| CPU and Memory | - Minimum: 4 CPU cores and 8GB RAM per node <br> - For high-volume data, complex workloads, high concurrency, or performance-critical applications, allocate additional resources accordingly |
| Disk       | - Recommended: SSD or NVMe devices<br>- Minimum performance: 500 IOPS and 30 MB/s throughput<br>- Storage: <1GB for KWDB system, additional space needed based on data volume. For production environments, plan hardware resources according to your business scale and performance requirements.<br>- Avoid shared storage (NFS, CIFS, CEPH)|
| File System | ext4 recommended for optimal performance |
