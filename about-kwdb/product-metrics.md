---
title: 环境要求
id: product-metrics
---

# 软硬件环境要求

## 操作系统及架构

KWDB 支持在以下服务器操作系统进行安装部署。

<table>
    <thead>
        <tr>
            <th rowspan="2">操作系统</th>
            <th rowspan="2">版本</th>
            <th colspan="2">裸机部署</th>
            <th colspan="2">容器部署</th>
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
            <td rowspan="2" class="os-name">KylinOS</td>
            <td>V10 SP2</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
            <td class="check">✓</td>
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

::: warning 说明
未提及的操作系统和版本**也许可以**运行 KWDB，但尚未得到 KWDB 官方支持。
:::

## 硬件环境

| 项目  | 要求                                                                                                                                                                                                 |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CPU 和内存 | 单节点配置建议不低于 4 核 8G。                                                                                                                                                                           |
| 磁盘       | - 推荐使用 SSD 或者 NVMe 设备，尽量避免使用 NFS、CIFS、CEPH 等共享存储。<br> - 磁盘至少能够实现 500 IOPS 和 30 MB/s 处理效率。<br> - KWDB 系统自身启动不会占用过多磁盘容量（低于 1G）。实际所需磁盘大小主要取决于用户的业务量。 |
| 文件系统   | 建议使用 ext4 文件系统。                                                                                                                                                                                 |
