---
title: Storage Management
id: storage-mgmt
---

# Storage Management

This section covers the features of storage management in KWDB, including path configuration, pre-allocated space management, cold and hot data tiered storage, data compression and data reorganization.

## Storage Path Configuration

### Storage Paths and Requirements

The table below lists the default storage paths, typical file sizes, recommended file systems, and the configuration parameters for different types of files in KWDB.

| File Type | Default Path | Typical Size | Recommended File System | Configuration Parameter |
|-----------|--------------|--------------|------------------------|------------------------|
| Data Files | `/var/lib/kaiwudb` | Data-dependent | - < 16TB: ext4<br>- > 16TB: XFS | - `data_root` parameter in `deploy.cfg`<br> - `--store` startup flag |
| Logs | `/var/lib/kaiwudb/logs` | 1GB (configurable) | ext4 | `--log-dir` startup flag |
| Certificates | `/etc/kaiwudb/certs` | - | ext4 | `--certs-dir` startup flag |
| Binary Files | `/usr/local/kaiwudb/bin` | > 200MB | ext4 | - |
| Dynamic Libraries | `/usr/local/kaiwudb/lib` | > 100MB | ext4 | - |

::: warning Note
For container deployments, the system automatically handles host path mounting.
:::

### Storage Path Configuration 

You can configure storage paths using either of the following ways:

- **During Deployment**: Specify the data file path by setting the `data_root` parameter in the `deploy.cfg` file.
- **After Deployment**: Specify the storage paths using the startup flags through the following methods:
  - Modify the `kaiwudb_env` file for bare-metal deployments
  - Modify the `docker-compose.yml` file for container deployments
  - Use the `kwbase start` command for both bare-metal and container depployments.

## Pre-allocated Space Management

KWDB uses pre-allocated space management to efficiently store time-series data and prevent storage-related issues by proactively monitoring and managing available disk space.

### Threshold for Pre-Allocation Management

The `ts.disk_free_space.alert_threshold` parameter defines when KWDB stops pre-allocating space for new data segments based on the remaining available storage:

- **When available storage falls below the threshold:**
  - In standalone mode: The system issues a warning, allows queries, but prevents data writes and imports.
  - In distributed clusters: The system issues a warning, and the affected node enters a down state.
- **When the feature is disabled (default: `0 B`):**
  - Pre-allocation fails when storage is insufficient.
  - In distributed clusters, nodes with insufficient space enter a down state.

### Threshold Calculation Formula

The minimum recommended threshold depends on your table structure and can be calculated as follows:

```plain
ts.disk_free_space.alert_threshold (B) ≥ (type_a_size * column_count_a + type_b_size * column_count_b + ...) * ts.blocks_per_segment.max_limit * ts.rows_per_block.max_limit
```

Where:

- `type_X_size`: Bytes per data type. For more information, see [Estimated Disk Usage](./cluster-planning.md#estimated-disk-usage).
- `column_count_X`: Number of columns for each data type
- `ts.blocks_per_segment.max_limit`: Maximum number of data blocks per segment (default: `1000`)
- `ts.rows_per_block.max_limit`: Maximum number of rows per data block (default: `1000`)

For example, for a table with 100 INT8 columns (8 bytes each), using default settings:

```plain
Minimum threshold = 8 B * 100 columns * 1000 blocks * 1000 rows = 800,000,000 B = 800 MB
```

## Data Compression

Data compression reduces storage usage by encoding original data more efficiently, removing redundancy while preserving core information and data integrity.

KWDB provides robust compression capabilities with ratios ranging from 5× to 30×, significantly lowering storage costs. It supports both periodic and on-demand compression for time-series data, offering automated compression with the flexibility of manual execution when needed.

A key advantage of KWDB is its ability to directly mount compressed data without decompression, enabling immediate querying and analysis.

### Compression Types

KWDB supports two types of compression:

#### Periodic Compression

The system automatically compresses data based on a user-defined active duration, following this process:

1. Runs in the background during each compression cycle.
2. Identifies data segments exceeding the active duration.
3. Marks qualifying segments as `InActiveSegment` in the first cycle.
4. Compresses these segments into squashfs format in the next cycle, freeing storage space.

By default, the active duration for time-series data is 1 day. You can modify or disable periodic compression using the `active_duration` parameter in `CREATE TABLE` or `ALTER TABLE`. For instructions, see [Create Table](../sql-reference/ddl/ts-db/ts-table.md#create-table) and [Alter Table](../sql-reference/ddl/ts-db/ts-table.md#alter-table).

#### On-Demand Compression

On-demand compression allows users to manually trigger immediate compression. It is independent of active duration settings and is ideal for data migration or instant space reclamation.

To execute on-demand compression, use the `COMPRESS` command to process all eligible data segments. You can adjust the number of threads via the `immediate_compression.threads` parameter.

Compression time varies based on dataset size—larger datasets require more time.

For more information:

- For the `COMPRESS` command, see [On-Demand Compression](../sql-reference/other-sql-statements/compression-sql.md).
- For thread configuration, see [Cluster Parameters](../db-operation/cluster-settings-config.md#cluster-parameters).

#### Comparison of Compression Types

| Feature | Periodic Compression | On-Demand Compression |
|---------|---------------------|----------------------|
| **Trigger Method** | Automatic (based on data active time) | Manual execution |
| **Compression Criteria** | Based on active time; eligible segments marked as `InActiveSegment`, then compressed in next cycle | Immediate compression of target data |
| **Default Active Time** | 1 day (configurable) | Not applicable |
| **Best Use Case** | Regular maintenance and optimization | Data migration, immediate space needs |

::: warning Note

If both compression types are triggered simultaneously, execution priority is based on trigger order:

- If periodic compression starts first, on-demand compression waits until periodic compression completes.
- If on-demand compression starts first, periodic compression for the current cycle is skipped.

:::

### Compression Algorithms

#### Supported Compression Algorithms

KWDB supports the following lossless compression algorithms for time-series data. You can configure the algorithm using the `ts.compression.type` cluster parameter:

| Algorithm | Description | Performance |  
|-----------|------------|-------------|  
| **GZIP** | Uses a variant of the LZ77 algorithm for initial compression, followed by Huffman coding. | High compression ratio, but relatively slow. |  
| **LZ4** | Member of the LZ77 compression family. | Very fast decompression, but lower compression ratio. |  
| **LZMA** | An advanced compression method based on LZ77 and DEFLATE, using dictionary-based encoding. | High compression ratio, but slow compression and decompression. |  
| **LZO** | Block compression algorithm in the LZ77 family. | Fast, but less effective compared to algorithms optimized for specific data types. |  
| **XZ** | Uses the LZMA2 algorithm for enhanced compression. | Very high compression ratio, but slow compression and decompression. |  
| **ZSTD (Zstandard)** | A modern algorithm balancing speed and compression ratio using Finite State Entropy (FSE) encoding. | Fast compression and decompression with a high compression ratio. |  

By default, KWDB uses the **GZIP** compression algorithm.

::: warning Note

If the `mksquashfs` or `mount` tool does not support the specified compression algorithm, KWDB will fall back to GZIP and log a warning message.

:::

#### Algorithm Support Requirements

A compression algorithm is fully supported in KWDB only if all the following components support it:

- mksquashfs compression tool
- Mount tool or Squashfuse (when applicable)

**`mksquashfs` Requirements**

The `mksquashfs` compression tool supports different algorithms depending on its version:

| Version | Supported Compression Algorithms |
|---------|----------------------------------|
| 4.0 and below | GZIP |
| 4.1 | GZIP, LZMA, LZO |
| 4.2 | GZIP, LZMA, LZO, XZ |
| 4.3 | GZIP, LZMA, LZO, XZ, LZ4 |
| 4.4 and above | GZIP, LZMA, LZO, XZ, LZ4, ZSTD |

**Mount Tool Requirements**

The compression algorithms supported by the mount tool depend on the kernel's squashfs support. The table below shows common OS support:

| OS | Supported Compression Algorithms |
|----|----------------------------------|
| CentOS 7 | GZIP, LZO, XZ |
| Ubuntu 20.04/24.04 | GZIP, LZO, XZ, LZ4, ZSTD |

::: warning Note

When deploying KWDB via Docker, you must ensure proper kernel configuration access to support all compression algorithms using either of the following methods and then restart KWDB:

- Add the directory mapping: `-v /boot:/boot`
- Copy the host's `/boot/config-$(uname -r)` file into the container's `/boot` directory

Otherwise, only the GZIP compression algorithm will be available.

:::

#### Compression Levels

KWDB allows configuring compression levels via the `ts.compression.level` cluster parameter. The compression level affects both compression speed and the resulting file size:

| Compression Level | Description | File Size | Processing Speed |
|-------------------|-------------|-----------|------------------|
| **low** | Lower compression ratio | Larger files | Faster compression |
| **middle** | Balanced compression | Medium files | Medium compression speed |
| **high** | Higher compression ratio | Smaller files | Slower compression |

The table below outlines which compression algorithms support which compression levels in KWDB:

| Compression Level | GZIP | LZO | ZSTD | LZ4 | XZ | LZMA |
|-------------------|------|-----|------|-----|----|----- |
| **low** | ✓ | ✓ | ✓ | ✓ (same as middle) | ✗ | ✗ |
| **middle** | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| **high** | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |

## Data Reorganization

Data reorganization optimizes how KWDB stores and manages user data. When enabled, the system automatically cleans, sorts, and reorganizes data to improve performance and reduce storage costs.

KWDB employs iterator sorting, examines data partitions and reorganizes data when necessary by:

- Removing deleted data
- Updating data types of historical data
- Optimizing data ordering

These enhancements maximize storage efficiency, accelerate queries, reduce storage costs, and improve database access and operations.

### Reorganization Process

Before reorganization begins, the system performs an evaluation to check the following:

- The version and number of segments within each partition
- The last modification timestamp of each partition
- Whether any data has been deleted within the partitions
- The current data order

Reorganization is carried out on a partition-by-partition basis. Before starting, the system briefly locks the target partition and sets it to a read-write-disabled state to assess whether reorganization is necessary.

Once reorganization begins, all segments in the partition are set to a write-disabled state, and the partition is unlocked to ensure uninterrupted data reading. New data will be written to newly created segments. If data deletion or insertion occurs during the reorganization process, the system will abort the operation for that partition and schedule a retry in the next reorganization cycle.

### Reorganization Configuration

In KWDB, data reorganization is enabled by default. You can manage this feature through the `ts.auto_vacuum.enabled` cluster parameter. For more information, see [Cluster Parameters](./cluster-settings-config.md#cluster-parameters).