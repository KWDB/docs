---
title: Disaster Recovery and Backup
id: backup-and-restore
---

# Disaster Recovery and Backup

## Disaster Recovery

KWDB implements disaster recovery for time-series data through Write-Ahead Logging (WAL) technology, which records schema changes and data modifications at the Virtual Group(VGroup) level, ensuring data consistency and atomicity.

### WAL Operation Mechanism

WAL ensures data safety through three core steps:

1. **Write-ahead logging**: All time-series data modification operations must be written to the WAL log before execution, ensuring complete data recovery even in the event of an abnormal system shutdown.
2. **Periodic checkpoints**: The system periodically writes in-memory data to disk in the background to ensure data safety. The default execution interval is 1 minute, configurable via the `ts.wal.checkpoint_interval` parameter.
3. **Crash recovery**: Upon system restart, the system automatically checks the last shutdown status, replays incomplete WAL operations, and rolls back failed transactions to ensure data integrity.

### WAL File Management

KWDB employs a **dual-file rotation strategy** for efficient WAL file management:

- **current_file**: The currently active WAL file, with size dynamically adjusted based on system load and configuration parameters.
- **checkpoint_file**: A temporary file converted from current_file during checkpoint execution, automatically deleted after data synchronization completes.

The rotation process works as follows:

1. Under normal operation, all WAL operations are recorded in current_file.
2. When a checkpoint is triggered, the current current_file is renamed to checkpoint_file.
3. The system immediately creates a new current_file to continue receiving WAL writes.
4. After data synchronization completes, the checkpoint_file is safely deleted.

### WAL Configuration

You can adjust WAL behavior through the following parameters:

| Parameter | Description | Default Value |
|----------------|-------------|---------------|
| `ts.wal.wal_level` | WAL write level, controlling data persistence strategy:<br>- `0` (`off`): Disables WAL; restores data state through time-series storage engine interface upon restart<br>- `1` (`sync`): Writes logs to disk in real-time with forced persistence, providing the highest safety with relatively lower performance<br>- `2` (`flush`): Writes logs to file system buffer, balancing performance and safety<br>- `3` (`byrl`): Ensures data consistency based on raft Log, with WAL responsible only for metadata consistency | `1` |
| `ts.wal.checkpoint_interval` | Checkpoint execution interval, controlling the frequency of persisting time-series data from memory to disk | `1m` |

::: warning Note

- Dynamic switching from `2` (`flush`) or `1` (`sync`) to `0` (`off`) / `3` (`byrl`) is supported. The switching process will cause brief blocking, with duration depending on the current checkpoint execution time.
- Instance-level DDL operations are not affected by `ts.wal.wal_level` and always have WAL enabled with real-time persistence.
:::

Example:

```sql
-- Set WAL to synchronous mode for highest data safety
SET cluster setting ts.wal.wal_level = 1;

-- Adjust checkpoint interval to 5 minutes
SET cluster setting ts.wal.checkpoint_interval = '5m';
```

## Backup and Restore

KWDB currently supports two levels of data backup:

- **Database-level Backup**: Complete database export and import.
- **Table-level Backup**: Individual table export and import.

For more information, see [Data Import](../../db-administration/import-export-data/import-data.md) and [Data Export](../../db-administration/import-export-data/export-data.md).
