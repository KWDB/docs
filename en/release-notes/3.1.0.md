---
title: 3.1.0 Release Notes
id: 3.1.0-release-notes
---

# KWDB 3.1.0 Release Notes

KWDB is a distributed, multi-model database, designed for AIoT scenarios. It seamlessly integrates time-series and relational databases within the same instance, enabling efficient multi-model data processing. With high-performance time-series capabilities, it supports connections for tens of millions of devices, real-time insertion of millions of records within seconds, and query responses in just a few seconds for hundreds of millions of records. Built for stability, security, high availability, and easy maintenance, KWDB is ideal for industrial IoT, digital energy, connected vehicles, and smart industries, providing a unified platform for data storage, management, and analysis.

KWDB 3.1.0 retains all existing features while delivering comprehensive optimizations and enhancements across database object management, data ingestion and querying, operations, stability, and performance.

## Version Details

| Version | Release Date |
|:--------|:-------------|
| 3.1.0   | 2026.02.03   |

## New Features

### Database Object Management

#### Time-Series Database and Table Creation Enhancements

- Supports `IF NOT EXISTS` clause when creating time-series databases and tables to prevent duplicate creation errors
- Supports custom time partition intervals when creating time-series databases (default: 10 days), with tables automatically inheriting the configuration from their parent database

#### Stored Procedure Optimization

- Supports setting custom variables within stored procedures
- Supports `PREPARE`, `EXECUTE`, and `DEALLOCATE` statements within stored procedures

### Data Ingestion and Processing

#### Data Deduplication Strategy

- Supports configuring data deduplication strategy to `merge`, which deduplicates and consolidates data with identical timestamps for the same device—ideal for scenarios with duplicate writes from data sources or multi-path data collection

#### Time-Series Data Performance Optimization

- Introduces a dedicated storage engine for Raft log, improving read/write performance on mechanical hard drives

#### Time-Series Data Compression Management

- New `ts.compress.last_segment.enabled` cluster parameter controls whether compression is enabled for the last segment (most recent data segment)
- New `ts.compress.stage` cluster parameter controls time-series data compression levels, supporting no compression, single-level compression, and dual-level compression
- New `SHOW DISTRIBUTION` statement views storage space usage and compression ratios for specified time-series databases or tables

### Data Querying and Analysis

#### Query Performance Optimization

- New `ts.last_cache_size.max_limit` cluster parameter sets memory limit for time-series `last_row()` cache, improving response speed for `last()` and `last_row()` queries

#### Enhanced Connection Capacity

- Maximum concurrent connections increases to 50,000

#### SQL Function Enhancements

- New `to_timestamp()` function converts timestamp formats to standard time formats

### Operations and Management

#### Cluster Operations

- Supports multi-replica cluster scaling operations via deployment scripts
- Supports manually triggering reorganization operations via the `VACUUM TS DATABASES` SQL statement to immediately free storage space or optimize query performance

#### Job Management

- `SHOW JOBS` statement now displays information related to stream computing jobs

## Important Changes

### Installation and Deployment

#### Deployment Script Optimization

- **Deployment configuration confirmation mechanism**: Configuration information from `deploy.cfg` is summarized and displayed in the terminal; installation proceeds only after user confirmation, otherwise installation is canceled
- **New convenient operation scripts**: `kw-status.sh` and `kw-sql.sh` scripts are automatically generated during installation for viewing cluster status and connecting to the database
- **Uninstallation optimization**: Database uninstallation now supports certificate retention

#### Quick Deployment Script

- Added `quick_deploy.sh` script that automates the complete deployment process, including system detection, parameter configuration, installation package download, and deployment

### Development Tools

#### KaiwuDB Developer Center

- Supports BLOB and CLOB large object data types

### Ecosystem Compatibility

#### KaiwuDB JDBC Driver

- Upgraded to secure version, eliminating known security vulnerabilities; supports additional data types

## Upgrade Notes

- **Multi-replica clusters**: offline upgrade from 3.0.0 to 3.1.0
- **Single-replica clusters**: offline upgrade from 3.0.0 to 3.1.0
- **Standalone deployments**: offline upgrade from 3.0.0 to 3.1.0
- **KWDB 2.x**: data export and import

For instructions, see [Database Upgrade](../db-operation/db-upgrade.md), [Data Export](../db-administration/import-export-data/export-data.md), and [Data Import](../db-administration/import-export-data/import-data.md).