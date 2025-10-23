---
title: 容灾和备份
id: backup-and-restore
---

# 容灾和备份

## 容灾

KWDB 通过 WAL（Write-Ahead Logging，预写式日志）技术，在 VGroup（虚拟组）级别记录时序表的模式变更和数据变更，实现时序数据灾难恢复，确保时序数据的一致性与原子性。

### WAL 工作机制

WAL 通过以下三个核心步骤保障数据安全：

1. **预写日志**：所有时序数据修改操作在执行前必须先写入 WAL 日志，确保即使系统异常退出也能完整恢复数据
2. **定期检查点（Checkpoint）**：系统后台定期将内存中的数据写入磁盘以确保数据安全。默认执行间隔为 1 分钟，可通过 `ts.wal.checkpoint_interval` 参数调整
3. **故障恢复**：系统重启时自动检查上次关闭状态，重放未完成的 WAL 操作并回滚异常事务，保证数据完整性

### WAL 文件管理

KWDB 采用**双文件轮转策略**实现高效的 WAL 文件管理：

- **current_file**：当前活跃的 WAL 写入文件，文件大小根据系统负载和配置参数动态调整
- **checkpoint_file**：执行检查点时由 current_file 转换的临时文件，数据同步完成后自动删除

具体轮转流程如下：

1. 正常运行时，所有 WAL 操作记录在 current_file 中
2. 触发检查点时，当前 current_file 转换为 checkpoint_file
3. 系统立即创建新的 current_file 继续接收 WAL 写入
4. 数据同步完成后，checkpoint_file 被安全删除

### WAL 配置

用户可通过以下参数调整 WAL 行为：

| 参数名称 | 描述 | 默认值 |
|---------|------|--------|
| `ts.wal.wal_level` | WAL 写入级别，控制数据持久化策略：<br>- `0` (`off`)：关闭 WAL，重启时通过时序存储引擎接口恢复数据状态<br>- `1` (`sync`)：日志实时写入磁盘并强制持久化，提供最高安全性，性能相对较低<br>- `2` (`flush`)：日志写入文件系统缓冲区，在性能和安全性间取得平衡<br>- `3` (`byrl`)：基于 Raft Log 保证数据一致性，WAL 仅负责元数据一致性 | `1` |
| `ts.wal.checkpoint_interval` | 检查点执行间隔，控制时序数据从内存持久化到磁盘的频率 | `1m` |

::: warning 说明
- 支持从 `2` (`flush`) 或 `1` (`sync`) 动态切换到 `0` (`off`) / `3` (`byrl`)，切换过程会产生短暂阻塞，阻塞时长取决于当前检查点的执行时间
- 实例级别的 DDL 操作不受 `ts.wal.wal_level` 影响，始终启用 WAL 并实时持久化
:::

示例：

```sql
-- 设置 WAL 为同步模式，确保最高数据安全性
SET cluster setting ts.wal.wal_level = 1;

-- 调整检查点间隔为 5 分钟
SET cluster setting ts.wal.checkpoint_interval = '5m';
```

## 备份

目前，KWDB 支持通过数据导入、导出的方式进行数据库库级别和表级别的数据备份。具体信息，参见[数据导入](../db-administration/import-export-data/import-data.md)和[数据导出](../db-administration/import-export-data/export-data.md)。
