---
title: pg_catalog
id: pg_catalog
---

# pg_catalog

KWDB 中的 `pg_catalog` 模式旨在与 PostgreSQL 兼容。

用户可通过 `SHOW TABLES FROM [<database_name>.]pg_catalog;` SQL 语句列出指定数据库 `pg_catalog` 模式下的所有系统视图。未指定数据库时，默认使用当前数据库进行查询；也可以使用 `SELECT` 语句查看 `pg_catalog` 模式下的指定系统视图信息。

本节列出了 `pg_catalog` 模式中常用的系统视图。

## 所需权限

用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。

## pg_catalog.pg_database

`pg_catalog.pg_database` 系统视图描述集群中的数据库信息。

| 列名            | 数据类型 | 描述               |
| --------------- | -------- | ------------------ |
| `oid`           | OID      | 数据库对象标识符   |
| `datname`       | NAME     | 数据库名称         |
| `datdba`        | OID      | 数据库拥有者       |
| `databatype`    | STRING   | 数据库类型         |
| `encoding`      | INT4     | 字符编码           |
| `datcollate`    | STRING   | 排序规则           |
| `datctype`      | STRING   | 字符类型           |
| `datistemplate` | BOOL     | 是否为模板数据库   |
| `datallowconn`  | BOOL     | 是否允许连接       |
| `datconnlimit`  | INT4     | 连接数限制         |
| `datlastsysoid` | OID      | 最后一个系统对象 ID |
| `datfrozenxid`  | INT8     | 冻结事务 ID         |
| `datminmxid`    | INT8     | 最小多事务 ID       |
| `dattablespace` | OID      | 默认表空间         |
| `datacl`        | STRING[] | 访问权限           |
| `datstatement`  | STRING   | 数据库创建语句     |