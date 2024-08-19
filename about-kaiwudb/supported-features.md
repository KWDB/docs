---
title: 功能概览
id: supported-features
---

# 功能概览

本文列出 KaiwuDB 支持的主要功能。

## 数据类型

### 时序数据

| 数据类型  | 2.0 |
| --- | --- |
| [时间戳类型](../sql-reference/data-type/data-type-ts-db.md#时间类型) | Y |
| [数值类型](../sql-reference/data-type/data-type-ts-db.md#数值类型) | Y |
| [布尔类型](../sql-reference/data-type/data-type-ts-db.md#布尔类型) | Y |
| [字符类型](../sql-reference/data-type/data-type-ts-db.md#字符类型) | Y |

### 关系数据

| 功能 | 2.0 |
| --- | --- |
| [数值类型](../sql-reference/data-type/data-type-relational-db.md#数值类型) | Y |
| [布尔类型](../sql-reference/data-type/data-type-relational-db.md#布尔类型) | Y |
| [字符类型](../sql-reference/data-type/data-type-relational-db.md#字符类型) | Y |
| [日期和时间类型](../sql-reference/data-type/data-type-relational-db.md#日期和时间类型) | Y |
| [JSONB 类型](../sql-reference/data-type/data-type-relational-db.md#jsonb-类型) | Y |
| [数组类型](../sql-reference/data-type/data-type-relational-db.md#数组类型) | Y |
| [INET 类型](../sql-reference/data-type/data-type-relational-db.md#inet-类型) | Y |
| [UUID 类型](../sql-reference/data-type/data-type-relational-db.md#uuid-类型) | Y |

## 数据定义语言（DDL）

### 时序数据

| 功能       | 2.0 |
| ---------- | --- |
| [数据库管理](../sql-reference/ddl/ts-db/ts-database.md) | Y   |
| [时序表管理](../sql-reference/ddl/ts-db/ts-table.md)  | Y   |
| [列管理](../sql-reference/ddl/ts-db/ts-column.md)     | Y   |
| [标签管理](../sql-reference/ddl/ts-db/ts-label.md)    | Y   |

### 关系数据

| 功能         | 2.0 |
| ------------ | --- |
| [数据库管理](../sql-reference/ddl/relational-db/relational-database.md)  | Y   |
| [模式管理](../sql-reference/ddl/relational-db/relational-schema.md)     | Y   |
| [关系表管理](../sql-reference/ddl/relational-db/relational-table.md)   | Y   |
| [列管理](../sql-reference/ddl/relational-db/relational-column.md)       | Y   |
| [视图管理](../sql-reference/ddl/relational-db/relational-view.md)     | Y   |
| [索引管理](../sql-reference/ddl/relational-db/relational-index.md)     | Y   |
| [约束管理](../sql-reference/ddl/relational-db/relational-constraint.md)     | Y   |
| [区域配置管理](../sql-reference/ddl/relational-db/relational-zone.md) | Y   |
| [序列管理](../sql-reference/ddl/relational-db/relational-sequence.md)     | Y   |
| [分区管理](../sql-reference/ddl/relational-db/relational-range.md)     | Y   |
| [注释管理](../sql-reference/ddl/relational-db/relational-comment.md)     | Y   |

## 数据标记语言（DML）

### 时序数据

| 功能             | 2.0 |
| ---------------- | --- |
| [插入 `INSERT`](../sql-reference/dml/ts-db/ts-insert.md)    | Y   |
| [删除 `DELETE`](../sql-reference/dml/ts-db/ts-delete.md)    | Y   |
| [更新 `UPDATE`](../sql-reference/dml/ts-db/ts-update.md)    | Y   |
| [预处理 `PREPARE`](../sql-reference/dml/ts-db/ts-prepare.md) | Y   |

### 关系数据

| 功能                    | 2.0 |
| ----------------------- | --- |
| [插入 `INSERT`](../sql-reference/dml/relational-db/relational-insert.md)           | Y   |
| [删除 `DELETE`](../sql-reference/dml/relational-db/relational-delete.md)           | Y   |
| [更新 `UPDATE`](../sql-reference/dml/relational-db/relational-update.md)           | Y   |
| [更新/插入 `UPSERT`](../sql-reference/dml/relational-db/relational-upsert.md)      | Y   |
| [截断表 `TRUNCATE TABLE`](../sql-reference/dml/relational-db/relational-truncate.md) | Y   |

## 数据查询语言（DQL）

### 时序数据

| 功能                                                                                | 2.0 |
| ----------------------------------------------------------------------------------- | --- |
| [指定查询 `SELECT`](../sql-reference/dml/ts-db/ts-select.md)                         | Y   |
| 嵌套查询 <br > `INNER JOIN`、`LEFT JOIN`、`RIGHT JOIN`、`FULL JOIN`                        | Y   |
| 联合查询 <br >`UNION`、`UNION ALL`、`INTERSECT`、`INTERSECT ALL`、`EXCEPT`、`EXCEPT ALL` | Y   |
| 表表达式 <br >`FROM`、`WHERE`、`GROUP BY`、`HAVING`                                      | Y   |
| 公共表表达式（CTE）`WITH`                                                           | Y   |
| 删除重复行 `DISTINCT`                                                               | Y   |
| 行排序 `ORDER BY`                                                                    | Y   |
| 标签查询                                                                            | Y   |
| 插值查询                                                                            | Y   |
| 最新值查询                                                                          | Y   |
| 时间窗口聚合查询                                                                    | Y   |

### 关系数据

| 功能                                                                                | 2.0 |
| ----------------------------------------------------------------------------------- | --- |
| [指定查询 `SELECT`](../sql-reference/dml/relational-db/relational-select.md)                                                                   | Y   |
| 嵌套查询 <br >`INNER JOIN`、`LEFT JOIN`、`RIGHT JOIN`、`FULL JOIN`                        | Y   |
| 联合查询 <br >`UNION`、`UNION ALL`、`INTERSECT`、`INTERSECT ALL`、`EXCEPT`、`EXCEPT ALL` | Y   |
| 表表达式 <br >`FROM`、`WHERE`、`GROUP BY`、`HAVING`                                      | Y   |
| 公共表表达式（CTE）`WITH`                                                           | Y   |
| 删除重复行 `DISTINCT`                                                               | Y   |
| 行排序 `ORDER BY`                                                                    | Y   |

## 函数

### 时序数据

| 函数               | 2.0 |
| ------------------ | --- |
| [条件和类函数运算符](../sql-reference/functions/functions-ts-db.md#条件和类函数运算符) | Y |
| [日期和时间函数](../sql-reference/functions/functions-ts-db.md#日期和时间函数) | Y |
| [数学和数值函数](../sql-reference/functions/functions-ts-db.md#数学和数值函数) | Y |
| [字符串和字节函数](../sql-reference/functions/functions-ts-db.md#字符串和字节函数) | Y |
| [聚合函数](../sql-reference/functions/functions-ts-db.md#聚合函数) | Y |
| [地理函数](../sql-reference/functions/functions-ts-db.md#地理函数) | Y |
| [自定义函数](../sql-reference/other-sql-statements/self-defined-functions-sql.md) | Y |

### 关系数据

| 函数             | 2.0 |
| ------------------ | --- |
| [条件和类函数运算符](../sql-reference/functions/functions-relational-db.md#条件和类函数运算符) | Y |
| [数组函数](../sql-reference/functions/functions-relational-db.md#数组函数) | Y |
| [布尔函数](../sql-reference/functions/functions-relational-db.md#布尔函数) | Y |
| [比较函数](../sql-reference/functions/functions-relational-db.md#比较函数) | Y |
| [日期和时间函数](../sql-reference/functions/functions-relational-db.md#日期和时间函数) | Y |
| [ID 生成函数](../sql-reference/functions/functions-relational-db.md#id-生成函数) | Y |
| [网络函数](../sql-reference/functions/functions-relational-db.md#系统信息函数) | Y |
| [JSONB 函数](../sql-reference/functions/functions-relational-db.md#jsonb-函数) | Y |
| [数学和数值函数](../sql-reference/functions/functions-relational-db.md#数学和数值函数) | Y |
| [序列函数](../sql-reference/functions/functions-relational-db.md#序列函数) | Y |
| [设定-返回函数](../sql-reference/functions/functions-relational-db.md#设定-返回函数) | Y |
| [字符串和字节函数](../sql-reference/functions/functions-relational-db.md#字符串和字节函数) | Y |
| [系统信息函数](../sql-reference/functions/functions-relational-db.md#系统信息函数) | Y |
| [时间函数](../sql-reference/functions/functions-relational-db.md#时间函数) | Y |
| [元组函数](../sql-reference/functions/functions-relational-db.md#元组函数) | Y |
| [兼容性函数](../sql-reference/functions/functions-relational-db.md#兼容性函数) | Y |
| [聚合函数](../sql-reference/functions/functions-relational-db.md#聚合函数) | Y |
| [窗口函数](../sql-reference/functions/functions-relational-db.md#窗口函数) | Y |
| [自定义函数](../sql-reference/other-sql-statements/self-defined-functions-sql.md) | Y |

## 分布式架构

| 功能       | 2.0 |
| ---------- | --- |
| 多副本集群 | Y   |
| [集群高可用](../db-operation/cluster-ha.md) | Y   |
| 数据均衡   | Y   |

## 数据库运维管理

| 功能                   | 2.0 |
| ---------------------- | --- |
| [裸机部署](../deployment/bare-metal/bare-metal-deployment.md)               | Y   |
| [容器部署](../deployment/docker/docker-deployment.md)              | Y   |
| [数据导入](../db-administration/import-export-data/import-data.md)               | Y   |
| [数据导出](../db-administration/import-export-data/export-data.md)               | Y   |
| 数据压缩               | Y   |
| [KaiwuDB 可视化管理工具](../kdc/overview.md)  | Y   |
| [KaiwuDB 监控平台](../db-monitor/view-metrics-adminui.md)       | Y   |
| [KaiwuDB 数据库迁移工具](../db-migration/overview.md) | Y   |

## 数据库连接

| 功能         | 2.0 |
| ------------ | --- |
| [驱动程序连接](../development/connect-kaiwudb/connect-jdbc.md) | Y   |
| [框架协议连接](../development/connect-kaiwudb/connect-mybatis.md) | Y   |
| [RESTful API](../development/connect-kaiwudb/connect-restful-api.md)  | Y   |

## 数据库安全

| 功能                       | 2.0 |
| -------------------------- | --- |
| [加密传输](../db-security/transport-encryption.md) | Y |
| [基于用户名和密码的身份鉴别](../db-security/identity-authn.md#基于用户名和密码的身份鉴别) | Y |
| [基于主机的认证](../db-security/identity-authn.md#基于主机的认证) | Y |
| [用户和角色管理](../db-security/user-role-mgmt.md) | Y |
| [权限管理](../db-security/privilege-mgmt.md) | Y |
| [审计管理](../db-security/audit-mgmt.md) | Y |

## 第三方工具

| 第三方工具    | 2.0 |
| -------------------------- | --- |
| [Prometheus](https://prometheus.io/) | Y |
| [Grafana](https://grafana.com/grafana) | Y |
| [OpenTelemetry](https://opentelemetry.io/) | Y |
| [Kafka](https://kafka.apache.org/) | Y |
| [EMQX](https://www.emqx.io/) | Y |
| [DataX](https://github.com/alibaba/DataX) | Y |
| [Telegraf](https://github.com/influxdata/telegraf)      | Y   |
| [MyBatis](https://mybatis.org/mybatis-3/index.html) | Y |
| [MyBatis-Plus](../development/connect-kaiwudb/connect-mybatis-plus.md) | Y |

## AI 预测分析

| 功能                    | 2.0 |
| ----------------------- | --- |
| [基于 SQL 函数的预测分析](../ml-services/ml-service-overview.md) | Y |
| [基于 WEB 界面的预测分析](../ml-services/ml-service-overview.md) | Y |
