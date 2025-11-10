---
title: pg_catalog
id: pg_catalog
---

# pg_catalog

The `pg_catalog` schema in KWDB provides PostgreSQL compatibility.

To list all system views in the `pg_catalog` schema, use `SHOW TABLES FROM [<database_name>.]pg_catalog;`. If no database is specified, the current database is used by default. To view data from specific system views, use standard `SELECT` statements.

This section covers the most commonly used system views in the `pg_catalog` schema.

## Privileges

The user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

## pg_catalog.pg_database

The `pg_catalog.pg_database` system view describes database information in the cluster.

| Column Name       | Data Type | Description                          |
|-------------------|-----------|--------------------------------------|
| `oid`             | OID       | The database object identifier.      |
| `datname`         | NAME      | The database name.                   |
| `datdba`          | OID       | The database owner.                  |
| `databatype`      | STRING    | The database type.                   |
| `encoding`        | INT4      | The character encoding.              |
| `datcollate`      | STRING    | The collation order.                 |
| `datctype`        | STRING    | The character type.                  |
| `datistemplate`   | BOOL      | Whether the database is a template.  |
| `datallowconn`    | BOOL      | Whether new connections are allowed.     |
| `datconnlimit`    | INT4      | Maximum concurrent connections           |
| `datlastsysoid`   | OID       | The last system object ID.           |
| `datfrozenxid`    | INT8      | The frozen transaction ID.           |
| `datminmxid`      | INT8      | The minimum multitransaction  ID.            |
| `dattablespace`   | OID       | The default tablespace.              |
| `datacl`          | STRING[]  | The access privileges.               |
| `datstatement`    | STRING    | The database creation statement.     |