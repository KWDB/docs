---
title: 应用开发概述
id: overview
---

# 应用开发概述

本节旨在提供与 KWDB 应用程序开发相关的内容，包括以下内容：

- **连接 KWDB**：介绍 KWDB 支持的应用程序连接器、如何配置连接器，并提供不同连接器的应用开发示例。
  - JAVA
    - [JDBC](./connect-kaiwudb/java/connect-jdbc.md)
    - [MyBatis](./connect-kaiwudb/java/connect-mybatis.md)
    - [MyBatis-Plus](./connect-kaiwudb/java/connect-mybatis-plus.md)
    - [Hibernate](./connect-kaiwudb/java/connect-hibernate.md)
    - [R2DBC](./connect-kaiwudb/java/connect-r2dbc.md)
    - [hsweb_r2dbc](./connect-kaiwudb/java/connect-hsweb-r2dbc.md)
  - [C++](./connect-kaiwudb/c-plus-plus/connect-odbc.md)
  - [C#](./connect-kaiwudb/c-sharp/connect-npgsql.md)
  - Python
    - [Psycopg 2](./connect-kaiwudb/python/connect-psycopg2.md)
    - [Psycopg 3](./connect-kaiwudb/python/connect-psycopg3.md)
  - PHP
    - [PHP pgsql](./connect-kaiwudb/php/connect-php-pgsql.md)
    - [ThinkPHP](./connect-kaiwudb/php/connect-thinkphp.md)
  - RESTful API
    - [无模式写入](./connect-kaiwudb/restful-api/schemaless-writing.md)
    - [RESTful API](./connect-kaiwudb/restful-api/connect-restful-api.md)
  - [Golang](./connect-kaiwudb/golang/connect-pgx.md)
  - [Node.js](./connect-kaiwudb/node-js/connect-knex.md)
  - [Rust](./connect-kaiwudb/rust/connect-rust.md)
- **读写数据**：介绍如何使用 [Kafka](https://kafka.apache.org/)、[DataX](https://github.com/alibaba/DataX)、[EMQX](https://www.emqx.io/)、[Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) 将数据写入到 KWDB 数据库，或者从 KWDB 数据库读取数据。
  - [Kafka](./read-write-data/kafka.md)
  - [DataX](./read-write-data/datax.md)
  - [EMQX](./read-write-data/emqx.md)
  - [Telegraf](./read-write-data/telegraf.md)
