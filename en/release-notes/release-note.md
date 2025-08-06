---
title: 2.2.2 Release Notes
id: 2.2.2-release-notes
---

# KWDB 2.2.2 Release Notes

KWDB is a distributed, multi-model database, designed for AIoT scenarios. It seamlessly integrates time-series and relational databases within the same instance, enabling efficient multi-model data processing. With high-performance time-series capabilities, it supports connections for tens of millions of devices, real-time insertion of millions of records within seconds, and query responses in just a few seconds for hundreds of millions of records. Built for stability, security, high availability, and easy maintenance, KWDB is ideal for industrial IoT, digital energy, connected vehicles, and smart industries, providing a unified platform for data storage, management, and analysis.

KWDB 2.2.2 retains the core features of previous versions while introducing enhancements in tag index management and distributed high availability architecture.

## Version Details

| Version   | Release Date   |
| :------- | :--------- |
| 2.2.2    | 2025.07.21 |

## Bug Fixes

- **Cluster Management**  
  - Fixed an issue that caused upgrade failures in single-replica clusters

- **Query Functions**  
  - Resolved inconsistencies between direct table write statistics and `time_bucket_gapfill()` counts in subqueries  
  - Corrected inaccurate results from the `count_window()` function  
  - Fixed query errors when combining the `count()` and `coalesce()` functions  
  - Resolved discrepancies in `current_time()` function results between time-series and relational engines  
  - Fixed incorrect results when using the `twa()` function within subqueries

- **Date Handling**  
  - Addressed inconsistencies BCE date logic under different `WHERE` clause conditions

- **Data Operations**  
  - Fixed an issue that prevented deletion of time-series data in `PREPARE` mode

- **Performance Optimizations**  
  - Improved count performance following pipeline test data writes  
  - Enhanced query performance for TSBS `high-cpu-1`  
  - Optimized query performance for TSBS `double-groupby-1`

## Upgrade Notes

KWDB 2.2.2 supports the following upgrade methods:

- **Multi-replica clusters**: online upgrade from 2.2.x.
- **Single-replica clusters**: offline upgrade from 2.2.x.
- **Standalone deployments**: offline upgrade from 2.2.x.
- **KWDB 2.0.x and 2.1.0**: data export and import.

For instructions, see [Database Upgrade](../db-operation/db-upgrade.md), [Data Export](../db-administration/import-export-data/export-data.md), and [Data Import](../db-administration/import-export-data/import-data.md).