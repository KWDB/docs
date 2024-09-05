---
title: 应用开发概述
id: overview
---

# 应用开发概述

本节旨在提供与 KWDB 应用程序开发相关的内容，包括以下内容：

- **连接 KWDB**：介绍 KWDB 支持的应用程序连接器、如何配置连接器，并提供不同连接器的应用开发示例。
  - [JDBC](./connect-kaiwudb/connect-jdbc.md)
  - [PostgreSQL ODBC](./connect-kaiwudb/connect-odbc.md)
  - [MyBatis](./connect-kaiwudb/connect-mybatis.md)
  - [MyBatis-Plus](./connect-kaiwudb/connect-mybatis-plus.md)
  - [RESTful API](./connect-kaiwudb/connect-restful-api.md)
  - [Hibernate](./connect-kaiwudb/connect-hibernate.md)
- **读写数据**：介绍如何使用 [Kafka](https://kafka.apache.org/)、[DataX](https://github.com/alibaba/DataX)、[EMQX](https://www.emqx.io/)、[Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) 将数据写入到 KaiwuDB 数据库，或者从 KWDB 数据库读取数据。
  - [Kafka](./read-write-data/kafka.md)
  - [DataX](./read-write-data/datax.md)
  - [EMQX](./read-write-data/emqx.md)
  - [Telegraf](./read-write-data/telegraf.md)
