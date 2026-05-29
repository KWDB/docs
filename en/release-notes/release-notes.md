---
title: 3.2.0 Release Notes
id: 3.2.0-release-notes
---

# KWDB 3.2.0 Release Notes

KWDB is a distributed, multi-model database designed for AIoT scenarios. It supports creating both time-series and relational databases within the same instance and enables unified multi-model data processing. With high-performance time-series capabilities, it supports connections for tens of millions of devices, real-time insertion of millions of records within seconds, and query responses in just a few seconds for hundreds of millions of records. Built for stability, security, high availability, and easy maintenance, KWDB is ideal for industrial IoT, digital energy, connected vehicles, and smart industries, providing a unified platform for data storage, management, and analysis.

KWDB 3.2.0 builds on existing features by introducing several new capabilities in data management and querying and operations monitoring, along with important changes to installation, deployment, and development tools.

## Version Details

| Version | Release Date |
|---------|------|
| 3.2.0   | 2026.05.28 |

## New Features

### Data Management and Querying

#### Data Ingestion and Deletion

- The DELETE statement now supports filtering by partial primary tags: you can specify partial primary tags alone or in combination with a timestamp as filter conditions for deletion.

#### Data Storage and Compression

- **Custom compression**:
  - Supports setting the encoding method, compression algorithm, and compression level per column when creating time-series tables.
  - Supports modifying the encoding method, compression algorithm, and compression level of existing columns.
  - Supports configuring a global default compression algorithm and level through cluster parameters.

#### Query Enhancements

- Time-series grouped window functions now support grouping and aggregation by any column or combination of columns in a table.
- **Value fill queries**: Time-series data supports returning fill values when no data exists at a specified time point, using one of six strategies: exact, previous value, next value, nearest value, constant, or linear interpolation.
- **Extended last/first aggregate functions**: The time-series and relational `last()`, `lastts()`, `last_row()`, `last_row_ts()`, `first()`, `firstts()`, `first_row()`, and `first_row_ts()` functions now support a two-argument form for explicitly specifying the sort timestamp column.

#### Data Import and Export

- **Export logic optimization**: Before exporting, the system checks whether the target folder is empty. If it is not empty, an error is returned to prevent overwriting existing data.
- **New control parameters**: New `thread_concurrency` and `limit_memory` parameters for configuring the number of concurrent export threads and limiting the amount of data imported or exported.

## Important Changes

### Installation and Deployment

- **Installer redesign**: The installer is now packaged as a `.run` file and offers both a command-line interactive menu and a dialog interactive menu installation mode. Different startup options launch the corresponding installation workflow.

## Upgrade Notes

- **Multi-replica clusters**: Supports offline upgrade from KWDB 3.0.0 and 3.1.0 to 3.2.0.
- **Single-replica clusters**: Supports offline upgrade from KWDB 3.0.0 and 3.1.0 to 3.2.0.
- **Standalone deployments**: Supports offline upgrade from KWDB 3.0.0 and 3.1.0 to 3.2.0.
- **KWDB 2.x**: Supports upgrade to 3.2.0 via data export and import.

For instructions, see [Database Upgrade](../db-operation/db-upgrade.md), [Data Export](../db-administration/import-export-data/export-data.md), and [Data Import](../db-administration/import-export-data/import-data.md).
