---
title: Product Architecture
id: product-architecture
---

# Product Architecture

KWDB takes a different approach from traditional databases by offering multi-model data management, allowing you to store various types of data in a single, unified system. This flexibility enables businesses to seamlessly integrate and manage data from different departments and applications, making it possible to support a wide range of services under one roof.

The architecture of KWDB is illustrated below:

<img src="../static/about-kaiwudb/kwdb-architecture.png" alt="KWDB Architecture" style="max-width:80%; height:auto;" />

**Interface Layer**: Supports multiple standardized interface protocols, including JDBC, ODBC, and RESTful API, ensuring seamless compatibility with various applications and development tools.

**Computing Layer**:

- **SQL Execution Engine**: Delivers a complete SQL processing workflow, including protocol parsing, multi-model SQL parser, multi-model SQL optimizer, and multi-model SQL executor. Enables unified querying and processing across time-series and relational data.

- **Monitoring and Management Module**: Provides comprehensive system monitoring and management capabilities, including session management, memory management, thread management, message management, heartbeat management, performance monitoring, and log tracing.

- **Core Service Components**: Includes essential database services such as metadata management, transaction management, job management, and security management.

- **Value-Added Services**: Offers advanced features including real-time compression, lifecycle management, specialized built-in functions, system tasks, and Write-Ahead Logging (WAL).

- **Multi-Engine Integration**: Integrates multiple data computing engines that automatically select the optimal storage and computation mode based on data characteristics while providing a unified interface. This delivers diverse analytical capabilities and enhanced query efficiency.
  - **Adaptive Time-Series Engine**: Specifically optimized for time-series data, supporting complex time-series queries and multi-dimensional aggregation. Capable of inserting millions of records in real-time within seconds and delivering query responses in seconds for hundreds of millions of records. Provides 5-30x real-time compression, with compressed data directly usable without decompression.
  - **Transaction Processing Engine**: Supports distributed transactions and Multi-Version Concurrency Control (MVCC), with complete relational database capabilities including comments, views, constraints, indexes, sequences, stored procedures, and triggers.

**Storage Layer**:

- **Time-Series Storage Engine**: Optimized for time-series data, enabling efficient data storage and retrieval.
- **Relational Storage Engine**: Traditional relational database engine that provides full ACID transaction guarantees.