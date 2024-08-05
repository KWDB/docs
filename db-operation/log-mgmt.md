---
title: 日志管理
id: log-mgmt
---

# 日志管理

数据类型不同，KWDB 生成的日志和存储位置也有所不同。下表列出目前 KWDB 在数据库运维期间可能生成的所有日志。

| <div style="width:100px">日志</div>  | 描述 | 存储位置  |
| ---| ---- | ---|
| 时序引擎日志 | 记录时序引擎的运行状态，日志名以 `TsEngine` 开头。 | KWDB 用户数据目录下的 `logs` 子目录，默认路径为 `/var/lib/kaiwudb/logs`。|
| 关系引擎日志 | 记录关系引擎的运行状态，日志名以 `kwbase-rocksdb` 开头。| KWDB 用户数据目录下的 `logs` 子目录，默认路径为 `/var/lib/kaiwudb/logs`。 |
| 非存储日志   | 记录非存储引擎的运行状态，日志名以 `kwbase.log` 开头。| KWDB 用户数据目录下的 `logs` 子目录，默认路径为 `/var/lib/kaiwudb/logs`。 |
| 审计日志     | 数据库活动和操作的详细记录。默认情况下，审计功能关闭。开启审计功能后，系统自动审计系统级操作。有关审计日志和审计功能的更多信息，参见[审计管理](../db-security/audit-mgmt.md)。 | KWDB 用户数据目录下的 `logs` 子目录，默认路径为 `/var/lib/kaiwudb/logs`。部署完成后，KWDB 支持修改部署生成的 `kaiwudb_env` 文件或 `docker-compose.yml` 文件 中的 `--sql-audit-dir` 参数，指定审计日志的位置。 |
| 错误日志     | 记录时序引擎崩溃时的信息。|  - |
