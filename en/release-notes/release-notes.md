---
title: 3.3.0 Release Notes
id: 3.3.0-release-notes
---

# KWDB 3.3.0 Release Notes

KWDB is a distributed, multi-model database designed for AIoT scenarios. It supports creating both time-series and relational databases within the same instance and enables unified multi-model data processing. With high-performance time-series capabilities, it supports connections for tens of millions of devices, real-time insertion of millions of records within seconds, and query responses in just a few seconds for hundreds of millions of records. Built for stability, security, high availability, and easy maintenance, KWDB is ideal for industrial IoT, digital energy, connected vehicles, and smart industries, providing a unified platform for data storage, management, and analysis.

KWDB 3.3.0 introduces a number of new features and optimizations in time-series data processing, ecosystem tools, installation and deployment while retaining its original capabilities.

## Version Details

| Version | Release Date |
|---------|------|
| 3.3.0   | 2026.10.19 |

## New Features

### Database Object Management

- Time-series view management support:
    - Support creating, modifying, deleting and viewing views;
    - Support referencing table data within the permission scope under both relational and time-series scenarios, and support cross-module queries;

### Data Management and Query

- Data publishing:
    - Support flexible configuration of subscription objects, including time-series databases, time-series tables, and query statements with WHERE conditions;
    - Published data supports deletion and update operations for time-series data;
    - Published data objects include out-of-order inserted data, data imported via IMPORT statements, and data updated before task startup or during task suspension

- Data push: Support real-time push of data in the database to Kafka topics;
    - Historical data push control: Support configuring whether to push historical data through parameters
    - Flexible push scope: Support data push for a single time-series database, a single time-series table or multiple time-series tables
    - Comprehensive filtering support: Support filtering for all metrics and tag columns
    - Instant push configuration: Support independent configuration of immediate push for each push task
    - DDL operation push: Full support for DDL operation push, including:
        - create table
        - drop table
        - alter table

### Operations and Maintenance Management

- Range report download: Provide the Kwbase debug range-report subcommand to pull diagnostic information for the specified rangeID and generate a static HTML report locally.

## Important Changes

### Ecosystem & Tools

- KaiwuDB Developer Center: Time series supports view management.
- KaiwuDB JDBC: The JDBC driver supports the prepare extend write mode. New private 'j/k/l' messages are added to directly insert data by table objects to achieve high-speed data writing.
- Advanced custom installation support for installation and deployment:
    - Support setting different data service ports, adminUI ports and data directories for each node;
    - Support installing multiple nodes on a single server.

### Operating System and Environment

- Provide binary files for the Windows 11 environment with relational operation support.


## Upgrade Notes

- **Multi-replica clusters**：Supports offline upgrade from KWDB 3.0.0 ,3.1.0 and 3.2.0 to 3.3.0.

- **Single-replica clusters**：Supports offline upgrade from KWDB 3.0.0 ,3.1.0 and 3.2.0 to 3.3.0.

- **Standalone deployments**：Supports offline upgrade from KWDB 3.0.0 ,3.1.0 and 3.2.0 to 3.3.0.

- **KWDB 2.x **：Supports upgrade to 3.3.0 via data export and import.
