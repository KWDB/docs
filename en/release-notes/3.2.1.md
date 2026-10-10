---
title: KWDB 3.2.1 Release Notes
id: 3.2.1-release-notes
---

# KWDB 3.2.1 Release Notes

KWDB  is a distributed, multi-model database designed for AIoT scenarios. It supports creating both time-series and relational databases within the same instance and enables unified multi-model data processing. With high-performance time-series capabilities, it supports connections for tens of millions of devices, real-time insertion of millions of records within seconds, and query responses in just a few seconds for hundreds of millions of records. Built for stability, security, high availability, and easy maintenance, KWDB is ideal for industrial IoT, digital energy, connected vehicles, and smart industries, providing a unified platform for data storage, management, and analysis.

KWDB 3.2.1 introduces new features and optimizations in data types and time zone settings while maintaining its original characteristics.

## Version Details

| Version | Release Date |
|--------|------|
| 3.2.1  | 2026.06.30 |

## New Features

## Data Management and Querying

### Data Type Extension

- **CITEXT Type Support**：The relational data now includes a new case-insensitive text type `CITEXT`.Queries are case-insensitive, and support case-insensitive pattern matching.

### Global Time Zone Setting

- Support dynamic configuration of global time zone through cluster parameters during runtime: When the client connection does not carry a time zone, the `TIMESTAMPTZ` data adopts the cluster-configured time zone; when the connection explicitly specifies a time zone, the time zone carried by the connection is used as the session time zone.

## Important Changes

### Development Tools

- **KaiwuDB Developer Center**：Added support for the `CITEXT` data type

##  Upgrade Notes

- **Multi-replica clusters**：Supports offline upgrade from KWDB 3.0.0 ,3.1.0 and 3.2.0 to 3.2.1.

- **Single-replica clusters**：Supports offline upgrade from KWDB 3.0.0 ,3.1.0 and 3.2.0 to 3.2.1.

- **Standalone deployments**：Supports offline upgrade from KWDB 3.0.0 ,3.1.0 and 3.2.0 to 3.2.1.

- **KWDB 2.x **：Supports upgrade to 3.2.1 via data export and import.