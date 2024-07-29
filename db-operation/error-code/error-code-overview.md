---
title: 错误码概述
id: error-code-overview
---

# 错误码概述

当用户使用 KaiwuDB JDBC 连接器连接 KWDB 数据库失败时，或者用户连接 KWDB 数据库后，SQL 语句执行失败，KWDB 会返回相应的错误码信息。目前 KWDB 支持以下三种类型的错误码：

- [KWDB 专有错误码](./error-code-kaiwudb.md)：以 `KW` 开头，由 `5` 位字符组成。
- [PostgreSQL 错误码](./error-code-postgresql.md)：KWDB 兼容 PostgreSQL 错误码。PostgreSQL 错误码也由 `5` 位字符组成。
- [KaiwuDB JDBC Driver 错误码](./error-code-jdbc-driver.md)：与 KaiwuDB JDBC Driver 相关的错误码，由 `5` 位字符组成。

这三类错误码包含以下信息：

- 错误码：错误对应的编码。通常情况下，一组有规律的错误码属于同一种错误类型。例如，数据库连接错误相关的错误码范围是 **KW001-KW015**。
- 错误消息：错误码对应的消息，提示错误的具体内容。
