---
title: Disaster Recovery and Backup
id: backup-and-restore
---

# Disaster Recovery and Backup

## Disaster Recovery

KWDB implements Write-Ahead Logging (WAL) as its primary mechanism for ensuring data durability and recovery capabilities. The WAL system records all schema modifications and data changes for time-series tables, offering robust disaster recovery capabilities while maintaining data consistency and atomicity.

### WAL Operation

The WAL system operates through the following process:

1. Database operations are first recorded in the WAL cache.
2. A background thread performs the following tasks every 5 minutes:

   - Writes cached log entries to WAL files.
   - Updates the checkpoint log sequence number (`CHECKPOINT_LSN`) in both WAL and data files.
   - Writes WAL checkpoint.
   - Synchronizes data files to disk.

### Recovery Process

- **Normal Shutdown**: During a controlled shutdown, KWDB proactively synchronizes all data files to disk and updates the `CHECKPOINT_LSN`.
- **Crash Recovery**: Following an unexpected shutdown, KWDB automatically initiates recovery by replaying all logs from the latest `CHECKPOINT_LSN`, ensuring data integrity.

### Supported WAL Operations

KWDB's WAL system supports the following operation types:

| Operation Type      | Description                                    |
| ------------------ | ---------------------------------------------- |
| `INSERT`           | Records new time-series data insertions         |
| `UPDATE`           | Tracks modifications to existing time-series data           |
| `DELETE`           | Documents data deletion operations              |
| `CHECKPOINT`       | Records system checkpoint states                |
| `TSBEGIN`          | Marks the start of a time-series transaction    |
| `TSCOMMIT`         | Records successful transaction completion       |
| `TSROLLBACK`       | Tracks transaction rollback operations          |
| `DDL_CREATE`       | Logs time-series table creation                 |
| `DDL_DROP`         | Documents table deletion operations             |
| `DDL_ALTER_COLUMN` | Records schema modification operations          |

### WAL File Management

KWDB organizes WAL files into a log file group with the following characteristics:

- **Default Configuration**:

  - 3 log files per group
  - 64 MiB size per file
  - Files stored in the `wal` subdirectory alongside time-series table data
  - File naming convention: `kwdb_wal<number>`

- **Log Rotation Process**:

  1. System initially writes to `kwdb_wal0`.
  2. When current file reaches capacity, system moves to next sequential file.
  3. After filling all files in the group, system cycles back to `kwdb_wal0`.
  4. This circular process continues throughout database operation.

## Backup

KWDB currently supports two levels of data backup:

- **Database-level Backup**: Complete database export and import.
- **Table-level Backup**: Individual table export and import.

For more information, see [Data Import](../../en/db-administration/import-export-data/import-data.md) and [Data Export](../../en/db-administration/import-export-data/export-data.md).
