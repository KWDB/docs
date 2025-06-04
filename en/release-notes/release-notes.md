---
title: 2.2.0 Release Notes
id: 2.2.0-release-notes
---

# KWDB 2.2.0 Release Notes

KWDB is a distributed, multi-model database, designed for AIoT scenarios. It seamlessly integrates time-series and relational databases within the same instance, enabling efficient multi-model data processing. With high-performance time-series capabilities, it supports connections for tens of millions of devices, real-time insertion of millions of records within seconds, and query responses in just a few seconds for hundreds of millions of records. Built for stability, security, high availability, and easy maintenance, KWDB is ideal for industrial IoT, digital energy, connected vehicles, and smart industries, providing a unified platform for data storage, management, and analysis.

KWDB 2.2.0 retains the core features of previous versions while introducing enhancements in time precision, database objects, DML operations, data queries, and database maintenance.

## Version Details

| Version   | Release Date   |
| :------- | :--------- |
| 2.2.0    | 2025.03.31 |

## New Features

### Time Precision

- **Time Precision:** The time-series engine now supports timestamp data types with microsecond and nanosecond precision.
- **Time and Date Functions**: The `time_bucket` and `time_bucket_gapfill` functions support time input at nanosecond precision.

### Database Objects

- **Isolation Levels:** The relational engine now supports the *Repeatable Read (RR)* and *Read Committed (RC)* isolation levels.

### DML Operations

- **Schema-Less Writing:**
  - Supports data insertion using OpenTSDB's telnet and JSON format protocols.
  - When creating databases and tables with schema-less writing, the system automatically distinguishes between uppercase and lowercase.

### Data Querying

- **Window Functions:** Supports *count-based*, *event-based*, *session-based*, *state-based* and *time-based* window functions, allowing data grouping and aggregation queries based on time intervals, row counts, sessions, data values, or event conditions.
- **`TWA` Function:** Calculates the time-weighted average for a specified column within a given time range.
- **`ELAPSED` Function:** Calculates continuous time durations within a specified period.
- **`INSERT INTO SELECT` Statement:** Supports writing cross-model query results directly into a time-series table.


### Database Operation and Maintenance

- **Preallocated Space Control:** Allows controlling the size of preallocated space via cluster parameters.
- **Import/Export:**
  - Supports importing user information, user privileges, and cluster configurations.
  - Supports importing and exporting schemas with uppercase names.

## Important Changes

### Operating Systems and Environments

- Supports Ubuntu 18.04.

### Development Tools

The KaiwuDB Developer Center introduces the following enhancements and features:

- Pagination support for displaying query results, improving query performance for wide tables.
- Improved debug logs: logs thread names, class names, executed SQL statements, and result processing time.
- Enhanced logging capabilities: improves logging for task scheduling, query result handling, and graphical rendering modules.

## Upgrade Notes

KWDB 2.2.0 supports the following upgrade methods:

- **Multi-replica clusters**: online upgrade from 2.1.0.
- **Single-replica clusters**: offline upgrade from 2.1.0.
- **Standalone deployments**: offline upgrade from 2.1.0.
- **KWDB 2.0.x series**: data export and import.

For instructions, see [Database Upgrade](../db-operation/db-upgrade.md), [Data Export](../db-administration/import-export-data/export-data.md), and [Data Import](../db-administration/import-export-data/import-data.md).