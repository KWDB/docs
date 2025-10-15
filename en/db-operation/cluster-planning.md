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

### Disk Management

#### Space Monitoring

KWDB provides the `df.sh` script for monitoring disk usage.

**Script Location**

- Bare-metal deployment: `/usr/local/kaiwudb/bin` by default.
- Container deployment: `/kaiwudb/bin` by default.

**Usage Syntax**:

```shell
<path-to-df.sh>/df.sh [OPTION]
```

**Available options:**

| Option     | Description                        |
|------------|------------------------------------|
| `--squashfs` | Display squashfs-mounted loop devices. Squashfs-mounted loop devices are excluded by default. |
| `--help`    | Show usage information            |

**Example**:

```shell
./df.sh
File systems information(excluding squashfs):
Filesystem     Type      Size  Used Avail Use% Mounted on
udev           devtmpfs   31G     0   31G    0% /dev
tmpfs          tmpfs     6.2G  1.4M  6.2G    1% /run
/dev/nvme0n1p5 ext4      916G  209G  661G   25% /
tmpfs          tmpfs      31G     0   31G    0% /dev/shm
tmpfs          tmpfs     5.0M  4.0K  5.0M    1% /run/lock
tmpfs          tmpfs      31G     0   31G    0% /sys/fs/cgroup
/dev/nvme0n1p1 vfat      511M  6.2M  505M    2% /boot/efi
tmpfs          tmpfs     6.2G  8.0K  6.2G    1% /run/user/114
tmpfs          tmpfs     6.2G  8.0K  6.2G    1% /run/user/1000

Number of squashfs mounted: 1
```

#### Estimate Disk Usage

Use the following formulas to estimate required storage space:

- **Pre-compression storage**:

    ```text
    Total Storage (GB) = (Device Count × Daily Writes per Device × Partition Days × Total Partitions × 
                         (Row Width/1024/1024 + 15/64/Max Rows per Segment/500/1000))/1024
    ```

- **Post-compression storage**:

    ```text
    Total Storage (GB) = (Device Count × Daily Writes per Device × Partition Days × Total Partitions × 
                     (Row Width/1024/1024/Compression Ratio + 15/64/Max Rows per Segment/500/1000))/1024
    ```

  Key Parameters:

  - **Partition Days**: Determined by the `PARTITION INTERVAL` value of the time-series table. The default value is `10`(representing 10 days). If the interval is set to `1mon`, the value will be `30` (representing 30 days in a month).
  - **Total Partitions**: Determined by the `RETENTIONS` and `PARTITION INTERVAL` values of the time-series table. For example, with a retention of `10` days and a partition interval of `10`, the total partitions will be `1`. If no retention is set, the total partitions will depend on the business cycle. For instance, if you need to store data for a year with a partition interval of `10`, the total partitions will be `37`.
  - **Row Width**: The total bytes per row across all columns. The following table provides the byte usage for each data type:

    | Data Type                | Bytes Occupied                     |
    | ------------------------ | ----------------------------------- |
    | TIMESTAMP(First Column)  | 16 bytes                           |
    | BOOL                      | 1 byte                             |
    | INT2                      | 2 bytes                            |
    | INT4, FLOAT4              | 4 bytes                            |
    | DOUBLE, TIMESTAMP, INT8   | 8 bytes                            |
    | CHAR, BYTES               | DDL-defined width + 1              |
    | NCHAR                     | DDL-defined width x 2 + 1          |
    | VARCHAR, VARBYTES         | 8-byte offset width + average content width |

  - **Maximum Rows per Segement**: The product of `ts.blocks_per_segment.max_limit` and `ts.rows_per_block.max_limit`. The default value is `1,000,000`.
  - **Compression Ratio**: Determined by data redundancy. Compression ratio can range from 5x to 30x for time-series data. Higher redundancy typically results in higher compression ratios.

**Example**

For the following parameters:

- Device Count: 1,000
- Daily Writes per Device: 1,000 rows/day
- Partition Days: 10 (default)
- Retentions: 30 days
- Row Width: 913 bytes
- Max Rows per Segement: 5,000
- Compression Ratio: 30

**Pre-compression storage**:

```plain
1000 * 1000 * 10 * 3 * (913/1024/1024 + 15/64/1000/10)/1024 ≈ 26 GB
```

**Post-compression storage**:

```plain
1000 * 1000 * 10 * 3 * (913/1024/1024/30 + 15/64/1000/10) / 1024 ≈ 1.5 GB
```

#### Recommended Configuration

The table below lists the recommended configuration and the estimated total size of pre-compression storage and post-compression storage for databases of different scales, assuming the following:

- 20 data columns per table
- Row width of 500 bytes
- Data retention period of 3 years
- Compression ratio of 10
- Single-node deployment. For cluster deployment, multiply the estimated storage by the number of cluster replicas.

| Device Count | Write Rate | Data Volume | Cluster Configuration | Table Configuration | Estimated Storage |
|--------------|------------|-------------|-----------------------------------|---------------------------------|-----------------|
| 100          | 1 row/min  | 144k/day    | - `ts.entities_per_subgroup.max_limit`: `100` <br>- `ts.blocks_per_segment.max_limit`: `1500`<br>- `ts.rows_per_block.max_limit`: `1000`|- `PARTITION INTERVAL`: `10d`<br>- `ACTIVETIME`:`200d`         | 20 GB           |
| 1000         | 1 row/10s  | 8.64M/day   | -`ts.entities_per_subgroup.max_limit: 500` <br>- `ts.blocks_per_segment.max_limit`: `25000` <br>- `ts.rows_per_block.max_limit`: `1000` <br>- `ts.mount.max_limit`:`2000` |- `PARTITION INTERVAL`: `5d` <br>- `ACTIVETIME`: `10d`           | 551 GB          |
| 10,000       | 1 row/10s  | 86.4M/day   | - `ts.entities_per_subgroup.max_limit`: `500` <br>- `ts.blocks_per_segment.max_limit`: `230000` <br>- `ts.rows_per_block.max_limit`: `1000` <br>- `ts.mount.max_limit`:`5000`  |- `PARTITION INTERVAL`: `1d` <br>- `ACTIVETIME`:`2d`        | 5.3 TB          |
| 100,000      | 1 row/sec  | 8.64B/day    | - `ts.entities_per_subgroup.max_limit`: `500` <br>- `ts.blocks_per_segment.max_limit`: `230000` <br>- `ts.rows_per_block.max_limit`: `1000` <br>- `ts.mount.max_limit`:`5000`  |- `PARTITION INTERVAL`: `1d`<br>- `ACTIVETIME`:`2d`         | 502 TB          |
| 1,000,000    | 1 row/sec  | 86.4B/day   | - `ts.entities_per_subgroup.max_limit`: `500`  <br>- `ts.blocks_per_segment.max_limit`: `230000` <br>- `ts.rows_per_block.max_limit`: `1000` <br>- `ts.mount.max_limit`:`5000`  |- `PARTITION INTERVAL`: `1d` <br>- `ACTIVETIME`:`2d`        | 5020 TB         |

## Security

Running a cluster in non-secure mode exposes you to serious security risks:

- **Open access**: The cluster is open to all clients and any node’s IP address can be accessed without restrictions.
- **No authentication**: Users can connect without a password, and any user can log in as `root`, gaining full read/write access to all data.
- **Unencrypted communication**: Data is transmitted without encryption, leaving it vulnerable to interception and tampering.

To avoid these risks, KWDB strongly recommends deploying your cluster in **secure mode** using **TLS** or **TLCP** encryption. This ensures that both nodes and clients are properly authenticated, and all data transfers are securely encrypted, protecting against unauthorized access and data manipulation.