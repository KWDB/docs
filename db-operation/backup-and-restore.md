---
title: 容灾和备份
id: backup-and-restore
---

# 容灾和备份

## 容灾

KWDB 采用 WAL（Write-Ahead Logging，预写式日志），记录每个时序表的模式变更和数据变更，实现时序数据库的数据灾难恢复、时序数据的一致性和原子性。默认情况下，KWDB 将保存在 WAL 日志缓存中的日志条目写入日志文件，每 5 分钟通过后台线程更新 WAL 文件和数据文件的检查点日志序列号（CHECKPOINT_LSN），写入检查点 WAL 日志，然后同步数据文件到磁盘。

正常停机时，KWDB 主动同步数据文件到磁盘并更新 CHECKPOINT_LSN。出现宕机时，KWDB 重启时会从最新的 CHECKPOINT_LSN 回放日志，保证数据完整性。这种机制确保即使系统崩溃，也能通过重新执行日志中的操作来恢复数据库的数据，确保数据一致性。

KWDB 支持对 WAL 记录进行以下操作。

| 语句             | 描述              |
| ---------------- | ----------------- |
| `INSERT`           | 写入时序数据。      |
| `UPDATE`           | 更新时序数据。      |
| `DELETE`           | 删除时序数据。      |
| `CHECKPOINT`       | 检查点操作。        |
| `TSBEGIN`          | 开始时序数据事务。  |
| `TSCOMMIT`         | 结束时序数据事务。  |
| `TSROLLBACK`       | 回滚时序数据事务。  |
| `DDL_CREATE`       | 创建时序表。        |
| `DDL_DROP`         | 删除时序表。        |
| `DDL_ALTER_COLUMN` | 修改时序表 schema。 |

WAL 日志文件由多个文件组成，称为 WAL 日志文件组。默认情况下，WAL 日志文件组包含三个大小相同的日志文件，每个文件的大小为 64 MiB。这些日志文件保存在时序表数据同级目录下的 `wal` 子目录中，文件以 `kwdb_wal<number>` 的形式进行命名。初始时，系统使用 `kwdb_wal0` 作为活跃的当前日志文件。当前日志文件写满后，系统按照顺序创建或使用下一个日志文件，直到日志文件组中的所有文件都被写满。之后，系统会重新使用 `kwdb_wal0` 继续写入日志条目。

## 备份

目前，KWDB 支持通过数据导入、导出的方式进行数据库库级别和表级别的数据备份。具体信息，参见[数据导入](../db-administration/import-export-data/import-data.md)和[数据导出](../db-administration/import-export-data/export-data.md)。
