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
For Docker container deployments, the system uses the host path with automatic mounting.
:::

### Storage Path Configuration 

KWDB supports the following storage path configuration methods:

- During deployment, customize the data path by modifying the `data_root` parameter in the `deploy.cfg` file.
- After deployment, modify storage paths by editing the generated `kaiwudb_env` file, the `docker-compose.yml` file, or using the `kwbase start` command.


## Data Reorganization

Time-series data reorganization refers to the process of cleaning and organizing raw data according to specific rules, primarily applied in the following scenarios:

- **Delete Data Cleanup**: After executing DELETE operations, clean up data marked for deletion to free up storage space
- **Expired Data Cleanup**: Clean up expired data identified through lifecycle management functionality

Data reorganization optimizes storage space utilization, improves database query performance and response speed, and enhances overall system efficiency.

### Reorganization Process

Data reorganization operates on a partition basis. The system uses a single-threaded serial approach to process reorganization tasks, ensuring operational stability and data consistency.

The specific process is as follows:

1. **Task Trigger**: The system periodically triggers reorganization tasks automatically
2. **Partition Traversal**: Sequentially scans each partition and performs reorganization operations
3. **Data Cleanup**:
   - Clean up expired data
   - Clean up data marked for deletion
4. **File Reconstruction**: Generate optimized new data files to replace the original files
5. **Marker Cleanup**: Clean up related deletion marker to complete the reorganization process

Reorganization operations and merge operations are mutually exclusive; the same entity segment will not execute both operations simultaneously.

### Reorganization Configuration

In KWDB, the data reorganization feature is enabled by default. You can enable or disable this feature through the `ts.auto_vacuum.enabled` cluster parameter. For more information, see [Cluster Parameters](./cluster-settings-config.md#cluster-parameters).