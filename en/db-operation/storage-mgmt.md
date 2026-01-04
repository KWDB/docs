---
title: Storage Management
id: storage-mgmt
---

# Storage Management

## Storage Path Configuration

### Default Storage Paths and System Requirements

The following table lists the default storage paths, file systems, and configuration information for different file types in KWDB.

| <div style="width:80px">File Type</div> | Default Path | Size | File System | Configuration Parameter |
|-----------|--------------|--------------|------------------------|------------------------|
| Data Files | `/var/lib/kaiwudb` | Data-dependent | - ext4 file system recommended.<br>- For data exceeding 16 TB, XFS file system recommended. | - `data_root` parameter in the `deploy.cfg` file<br> - `--store` startup flag |
| Logs | `/var/lib/kaiwudb/logs` | Default 1 GB (configurable) | ext4 file system recommended. | `--log-dir` startup flag |
| Certificates | `/etc/kaiwudb/certs` | N/A | ext4 file system recommended. | `--certs-dir` startup flag |
| Binary Files | `/usr/local/kaiwudb/bin` | > 200 MB | ext4 file system recommended. | N/A |
| Dynamic Libraries | `/usr/local/kaiwudb/lib` | > 100 MB | ext4 file system recommended. | N/A |

::: warning Note
For container deployments, the system uses the host path with automatic mounting.
:::

### Storage Path Configuration 

KWDB supports the following storage path configuration methods:

- During deployment, customize the data path by modifying the `data_root` parameter in the `deploy.cfg` file.
- After deployment, modify storage paths by editing the generated `kaiwudb_env` file, the `docker-compose.yml` file, or using the `kwbase start` command.

## Data Reorganization

Time-series data reorganization is the process of cleaning and organizing raw data according to specific rules. It is primarily used in the following scenarios:

- **Delete Data Cleanup**: After executing DELETE or DROP operations, remove data marked for deletion to free up storage space
- **Expired Data Cleanup**: Remove expired data identified through the lifecycle management functionality
- **Data File Organization and Sorting**: After bulk data writes, organize and sort data files to improve query efficiency

Data reorganization optimizes storage space utilization, improves database query performance and response speed, and enhances overall system efficiency.

### Reorganization Methods

KWDB provides two data reorganization methods: automatic reorganization and manual reorganization.

#### Automatic Reorganization

The system automatically triggers reorganization tasks at regular intervals, operating on a partition-by-partition basis. It uses a single-threaded serial approach to ensure operational stability and data consistency. The process works as follows:

1. Task Trigger: The system automatically triggers reorganization tasks at scheduled intervals
2. Partition Traversal: Sequentially scans each partition and performs reorganization operations
3. Data Cleanup:
   - Remove expired data
   - Remove data marked for deletion
4. File Reconstruction: Generate optimized new data files to replace the original files
5. Marker Cleanup: Remove related deletion marker records to complete the reorganization process

Reorganization operations and compact operations are mutually exclusive—the same entity segment cannot execute both operations simultaneously.

#### Manual Reorganization

When you need to immediately free up storage space or optimize query performance, you can manually trigger a reorganization operation using the `VACUUM TS DATABASES;` command.

Manual reorganization is particularly useful in the following scenarios:

- **Freeing Space After Deleting Data or Dropping Tables**: After executing DELETE or DROP operations, immediately remove deleted data to quickly reclaim storage space
- **Data Organization After Bulk Writes**: After large batch data writes, organize and sort data files to improve subsequent query performance

Manual reorganization is compatible with automatic reorganization—they do not interfere with each other. Manual reorganization also offers the following capabilities:

- Performs reorganization operations on current partition
- Reorganizes and sorts non-contiguous entity data, consolidating scattered blocks to improve query efficiency (regardless of whether delete operations occurred)
- Promptly identifies and removes data related to dropped tables
- Persists in-memory data to disk and merges last files

### Reorganization Configuration

- **Automatic Reorganization**: The automatic data reorganization feature is enabled by default. You can enable or disable this feature using the `ts.auto_vacuum.enabled` real-time parameter. For more information, see [Cluster Parameters](./cluster-settings-config.md#cluster-parameters).
- **Manual Reorganization**: Manually trigger reorganization operations by executing the [`VACUUM TS DATABASES;`](../sql-reference/other-sql-statements/vacuum.md) command.

## RaftLog Store for Time-Series Data

RaftLog Store is a storage optimization for distributed clusters handling time-series data. It significantly improves write performance on mechanical hard drives by reducing disk I/O pressure and streamlining the write path.

This feature is ideal for:

- Distributed clusters with high-volume time-series data writes
- Deployments using mechanical hard disk storage
- Applications requiring high write throughput

When enabled, the system automatically creates a `raftlog` subdirectory within the time-series engine directory. Active log files automatically rotate to historical files when they reach 512MB. The system checks for merge eligibility every 30 minutes.

### Configuration

To enable RaftLog Store, add the `--use-raft-store` flag to your node startup command.

::: warning

- This parameter must be set during **initial database installation and startup**. It is disabled by default.
- Once the database is initialized, you **cannot** change the storage engine by modifying startup flags.

:::

For detailed startup command information and examples, see [kwbase start](../tool-command-reference/client-tool/kwbase-sql-reference.md#kwbase-start).