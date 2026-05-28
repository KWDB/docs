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

## Data Compression

KWDB supports setting an encoding algorithm, a compression algorithm, and a compression level for each data column when you create or modify a time-series table. This lets you balance storage space and system resources according to different data characteristics. The configuration only affects newly written data; existing data is not changed.

### Encoding Algorithms, Compression Algorithms, and Compression Levels

#### Encoding Algorithms

The following table lists the supported encoding algorithms and defaults for different data types.

| Data Type | Supported Encoding Algorithms | Default |
| --- | --- | --- |
| INT2 / INT4 / INT8 | `simple8b` / `disabled` | `simple8b` |
| TIMESTAMP / TIMESTAMPTZ | `simple8b` / `disabled` | `simple8b` |
| FLOAT / DOUBLE | `chimp` / `disabled` | `chimp` |
| BOOL | `bitpacking` / `disabled` | `bitpacking` |
| Character types | `disabled` | `disabled` |

#### Compression Algorithms

All data types support the following compression algorithms. The default is `lz4`.

| Algorithm | Compression Ratio | Compression Speed | Decompression Speed | CPU Usage | Memory Usage | Suitable Scenarios |
| --- | --- | --- | --- | --- | --- | --- |
| `lz4` | Low to medium (2x-3x) | Extremely fast | Fastest | Very low | Very low | High-frequency writes and latency-sensitive scenarios (default) |
| `zstd` | Medium to high (2.5x-5x+) | Very fast | Extremely fast (similar to `lz4`) | Low to medium (depends on level) | Medium (tunable) | Storage-sensitive scenarios that still need good read/write performance |
| `zlib` | Medium (2.5x-4x) | Medium | Fast | Medium | Medium | Storage-sensitive scenarios with lower write-performance requirements |
| `snappy` | Low (1.5x-2x) | Extremely fast | Extremely fast | Very low | Very low | Scenarios that prioritize speed and do not need tunable compression levels |
| `disabled` | — | — | — | — | — | Disable compression |

::: warning Note
- `zstd` is usually close to `lz4` in speed but provides higher compression ratio and similarly fast decompression. It is often the best choice when you need a balance between space and performance.
- `zlib` has compression ratios similar to `zstd`, but compression and decompression are slower and use more CPU and memory. Use it carefully in high-frequency and large-volume write scenarios.
:::

#### Compression Levels

Supported values are `low`, `medium` (default), and `high`, which can also be abbreviated as `l`, `m`, and `h`. Higher levels improve compression ratio but also increase CPU and memory usage. Configure them based on your workload.

::: warning Note
`snappy` and `lz4` do not support compression-level settings. Setting a level for them has no actual effect.
:::

### Compression Configuration

The priority rules for compression configuration are:

- When no cluster setting is changed: column-level custom configuration > data type default > global cluster setting
- When a cluster setting is already set: column-level custom configuration > data type default = global cluster setting

It is recommended to define a global baseline with cluster settings and only override specific columns when necessary.

#### Global Compression Configuration

Use cluster settings to set the global default compression behavior without configuring every column individually:

```sql
SET CLUSTER SETTING ts.compress.stage = 3;
SET CLUSTER SETTING ts.compress.algorithm = 'lz4';
SET CLUSTER SETTING ts.compress.level = 'medium';
```

Parameter description:

| Parameter | Description | Default | Type |
| --- | --- | --- | --- |
| `ts.compress.stage` | Controls the time-series compression mode: <br>- `0`: disable encoding and compression <br>- `1`: enable encoding and disable compression <br>- `2`: disable encoding and enable compression <br>- `3`: enable encoding and compression | `3` | int |
| `ts.compress.algorithm` | Global default compression algorithm. Supports `lz4`, `zstd`, `zlib`, `snappy`, and `disabled`. This has lower priority than column-level configuration. | `lz4` | string |
| `ts.compress.level` | Global default compression level. Supports `low`, `medium`, and `high`. This has lower priority than column-level configuration. | `medium` | string |

#### Column-Level Compression Configuration

- Specify encoding and compression for columns during table creation:

  ```sql
  CREATE TABLE test_compress.t1 (
      k_timestamp TIMESTAMPTZ ENCODE 'Simple8B' COMPRESS 'lz4' LEVEL 'high' NOT NULL,
      c1 INT ENCODE 'Simple8B' COMPRESS 'zlib' LEVEL 'high',
      c2 FLOAT COMPRESS 'zlib' LEVEL 'medium',
      c3 INT ENCODE 'Simple8B',
      c4 BLOB COMPRESS 'disabled',
      c5 BOOL ENCODE 'disabled',
      c7 VARCHAR ENCODE 'disabled' COMPRESS 'disabled'
  ) TAGS (
      code1 INT2 NOT NULL
  ) PRIMARY TAGS (code1);
  ```

- Modify compression settings for an existing column:

  ```sql
  ALTER TABLE t1 ALTER COLUMN c2 COMPRESS 'zstd' LEVEL 'high';
  ALTER TABLE t1 ALTER COLUMN c1 ENCODE 'Simple8B' COMPRESS 'zstd' LEVEL 'medium';
  ALTER TABLE t1 ALTER COLUMN c4 COMPRESS 'disabled';
  ```

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

For detailed startup command information and examples, see [kwbase start](../kaiwudb-tools/kwbase-cli-tool.md#kwbase-start).