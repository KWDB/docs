---
title: KWDB 3.2.2 Release Notes
id: 3.2.2-release-notes
---

# KWDB 3.2.2 Release Notes

KWDB is a distributed, multi-model database designed for AIoT scenarios. It supports creating both time-series and relational databases within the same instance and enables unified multi-model data processing. With high-performance time-series capabilities, it supports connections for tens of millions of devices, real-time insertion of millions of records within seconds, and query responses in just a few seconds for hundreds of millions of records. Built for stability, security, high availability, and easy maintenance, KWDB is ideal for industrial IoT, digital energy, connected vehicles, and smart industries, providing a unified platform for data storage, management, and analysis.

KWDB 3.2.2, while maintaining its original features, introduces multiple new features and optimizations in areas such as time series data processing, database connection, and installation and deployment.

## Version Details

| Version | Release Date |
|--------|------|
| 3.2.2  | 2026.07.15 |

## New Features

## Data Management and Querying

### Time Series Data Processing

- **Stream Computing Supports Optimization**：Support real-time calculation by setting the sorting time to 0 and enabling the real-time calculation parameter.

- **Support for Sparse Tables**：Supports the creation of sparse tables with up to 20,000 columns, high sparsity, and continuous time series; supports various DDL operations, including but not limited to modifying column names, column types, column widths, adding or deleting columns; supports data writing, querying, deleting, importing, and exporting.

## Important Changes

### Installation and Deployment

- **Optimization of Deployment Methods**：Add a quick deployment script.

### Database Connection Method

- **KaiwuDB JDBC**：The JDBC driver now supports the 'M' message type of the PG extension protocol, columnar batch data transmission, and two compression methods: Snappy and LZ4.

### Development Tools

- **KaiwuDB Developer Center**：Newly added support for sparse table management.

## Upgrade Notes

- **Multi-replica clusters**：Supports offline upgrade from KWDB 3.0.0 ,3.1.0 and 3.2.0 to 3.2.2.

- **Single-replica clusters**：Supports offline upgrade from KWDB 3.0.0 ,3.1.0 and 3.2.0 to 3.2.2.

- **Standalone deployments**：Supports offline upgrade from KWDB 3.0.0 ,3.1.0 and 3.2.0 to 3.2.2.

- **KWDB 2.x **：Supports upgrade to 3.2.2 via data export and import.
