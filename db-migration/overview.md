---
title: 数据库迁移概述
id: overview
---

# 数据库迁移概述

[DataX](https://github.com/alibaba/DataX) 是一款广泛使用的离线数据同步工具。KWDB 基于 DataX 开发了数据库迁移工具 KaiwuDB DataX Utils，实现 KWDB（2.0.3 及以上版本）与 MySQL、TDengine、MongoDB、InfluxDB、OpenTSDB、Oracle、PostgreSQL、ClickHouse、KWDB（1.2.x）、KWDB（2.0.x）等数据库的离线数据同步。

KaiwuDB DataX Utils 支持以[单表](./migration-senarios/migrate-mysql-to-kaiwudb.md#单表迁移)、[多表](./migration-senarios/migrate-tdengine-to-kaiwudb.md)、[单库](./migration-senarios/migrate-mysql-to-kaiwudb.md#单库迁移)和[多库](./migration-senarios/migrate-mysql-to-kaiwudb.md#多库迁移)的形式对数据进行迁移，其中：

- 以表的形式迁移数据时，支持全量数据迁移和增量数据迁移。
- 以数据库的形式迁移数据时，只支持关系数据库之间的数据迁移。多库迁移时，源数据库与目标数据库必须一一对应。

用户通过配置文件设置源数据库和目标数据库的连接、访问、数据迁移等信息。KaiwuDB DataX Utils 自动校验、统计迁移数据并输出迁移报告。在迁移过程中，用户可以查看整体的数据迁移进度。

## 数据类型映射

KaiwuDB DataX Utils 支持 DataX 的数据类型。DataX 数据类型与 KWDB 数据类型的映射关系如下表所示：

| DataX 数据类型 | KWDB 数据类型   |
|----------------|---------------------------------------------------|
| INT            | TINYINT、SMALLINT、INT                              |
| LONG           | TINYINT、SMALLINT、INT、BIGINT、TIMESTAMP、TIMESTAMPTZ |
| DOUBLE         | FLOAT、REAL、DOUBLE、DECIMAL                         |
| BOOL           | BOOL、BIT                                          |
| DATE           | DATE、TIME、TIMESTAMP、TIMESTAMPTZ                   |
| BYTES          | BYTES、VARBYTES                                    |
| STRING         | CHAR、NCHAR、VARCHAR、NVARCHAR、TIMESTAMP、TIMESTAMPTZ |

不同数据库支持的数据类型和处理方式不同。下表列出了 KaiwuDB DataX Utils 处理以下数据库数据的方式和注意事项：

| 数据库 | 数据类型 | 注意事项 |
| --- | --- | --- |
| ClickHouse | - 在 ClickHouse 中，NULL 值显示为 `0`。导入 KWDB 后，NULL 值会被处理为 `false`。<br >- 二进制类型数据导入 KWDB 后，会以 `\x+` 空字符串的形式显示。| DataX 插件使用的 JDBC 驱动版本较低，不支持毫秒级精度的时间读取，可能导致错误删除数据。建议先升级 DataX 插件的 JDBC 驱动版本。解决升级导致的问题后，再进行数据迁移。|
| MongoDB | - 不支持迁移 MongoDB 数据库的 `_id` 列。| DataX 自带的 Reader 插件不支持 MongoDB 7。|
| OpenTSDB | - OpenTSDB 是键值对类型的数据库。因此，在读取数据时，数据以键值对的形式呈现。<br >- KaiwuDBWriter 支持修改读取的 OpenTSDB metric，将 metric 中的句点（`.`） 转化为下划线 （`_`），然后将该 metric 作为 KWDB 数据库的表名。每张表包括 `k_timestamp` 和 `value` 两列。<br >- 如果待写入的表不存在，支持自动创建表。 | - |
| TDengine | - 在 TDengine 中，如果 BOOL 类型的字段值显示为 `null`，导入 KWDB 后，BOOL 类型的字段值会被处理为 `false`。<br >- 在 TDengine 中，如果 NCHAR 类型的字段值显示为 `null`，导入 KWDB 后，NCHAR 类型的字段值会以空字符串的形式显示。<br>- TDengineReader 不支持读取 JSON 数据。如果数据表的标签列采用 JSON 格式，需要将其转为其他类型，否则会导致迁移失败。| - 从 TDengine（2.4.0.14 及以下版本）向 KWDB 迁移数据时，需要使用 TDengine 提供的 [TDengine20Reader](https://github.com/taosdata/DataX/tree/master/tdengine20reader) 插件。 <br>- 从 TDengine（3.0.0 及以上版本）向 KWDB 迁移数据时，需要使用 TDengine 提供的 [TDengine30Reader](https://github.com/taosdata/DataX/tree/master/tdengine30reader) 插件。|
