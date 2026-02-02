---
title: 3.0.0 Release Notes
id: 3.0.0-release-notes
---

# KWDB 3.0.0 Release Notes

KWDB is a distributed, multi-model database, designed for AIoT scenarios. It seamlessly integrates time-series and relational databases within the same instance, enabling efficient multi-model data processing. With high-performance time-series capabilities, it supports connections for tens of millions of devices, real-time insertion of millions of records within seconds, and query responses in just a few seconds for hundreds of millions of records. Built for stability, security, high availability, and easy maintenance, KWDB is ideal for industrial IoT, digital energy, connected vehicles, and smart industries, providing a unified platform for data storage, management, and analysis.

KWDB 3.0.0 delivers comprehensive optimizations and enhancements across database object management, data management and querying, and distributed architecture.

## Version Details

| Version | Release Date |
|:--------|:-------------|
| 3.0.0   | 2025.11.12   |

## New Features

### Database Object Management

- **Large Object Support**: The relational engine now supports BLOB (Binary Large Objects) and CLOB (Character Large Objects) with comprehensive DDL, DML, and DCL lifecycle management
- **Trigger Support**: The relational engine supports creating, modifying, and deleting triggers with flexible trigger conditions and event configurations
- **Stored Procedure Support**: Supports creation, viewing, altering, validation, execution, renaming, and deletion, with full compatibility for standard SQL syntax and special syntax structures
- **Enhanced Comment Support**: Supports adding comments during creation of time-series databases, relational databases, time-series tables, and relational tables, eliminating the need for separate subsequent operations

### Data Management and Querying

#### Data Storage and Compression

- **Real-time Compression**: Supports real-time compression of time-series data during write operations, with automatic algorithm selection based on data type for optimal compression efficiency

#### Query Enhancements

- **Contextual Min/Max Query**: When querying time-series data using `min()` or `max()` function, the system can retrieve additional fields from the rows containing the minimum or maximum values

### Session Management

- **Custom Variables**: Supports user-defined variables prefixed with "@" in SQL statements. Variables can be assigned values, referenced in queries, and used in calculations

#### Data Import/Export

- **Import/Export Enhancements**: Supports exporting data in SQL format

#### Time-Series Data Processing

- **Stream Computing**: Supports creating and managing real-time stream computations. Features include multiple trigger modes, configurable strategies for handling out-of-order and expired data, and capabilities to subscribe to and publish computation results

### Distributed Architecture

- **Data Distribution Optimization**:
  - **Relational Data**:
    - Supports hash, range, or list partitioning when creating or altering tables, with configurable zones for each partition
    - Provides hash-sharded index functionality, allowing hash-partitioned primary keys to be defined during table creation and hash partitions to be created during table alteration
  - **Time-Series Data**:
    - Supports hash partitioning when altering tables, with configurable zones for each partition
    - Allows hash size to be specified during table creation to determine the maximum number of data ranges
    - Provides control over automatic data rebalancing and replica replenishment for failed nodes
- **Write Performance Optimization**: Supports extended raft log flush cycles and the option to merge raft logs with WAL to improve write performance in multi-replica clusters
- **Data Synchronization Monitoring**: Displays data synchronization lag between leaseholders and followers

## Important Changes

### Operating Systems and Environments

- Added support for KylinOS V10 SP2

### Development Tools

- **KaiwuDB Developer Center**:
  - Added support for macOS with Apple M-series chips
  - Added stored procedure and trigger management capabilities
  - Added ability to copy and paste database connections
- **Performance Testing Tool (kwdb-tsbs)**: A TSBS-based performance testing tool for time-series databases that generates standardized datasets and benchmarks KWDB read and write performance

### Ecosystem Support

- **Deep Flink Integration**: The KaiwuDB Flink Connector enables bidirectional data flow via the DataStream API and Flink Table API. Features include automatic type mapping, flexible parameter configuration, and optimized concurrent read operations
- **Kafka Data Ingestion**: Supports direct data writes from Kafka to the KWDB relational engine

## Feature Adjustments

The following features are not available in this release and may be added in future versions:

- **Database/Table Settings**: Time-series databases do not support custom partition intervals; time-series tables do not support active time and partition interval settings
- **Data Writing**: Deduplication strategy does not support merge mode (merging duplicate data with identical timestamps)
- **Data Storage**: Pre-allocated space management; `df.sh` script for monitoring disk usage
- **Data Compression**: Periodic compression (replaced by real-time compression); custom compression algorithm and level settings; on-demand compression

## Upgrade Notes

KWDB 3.0.0 supports upgrades from versions 2.x using the import/export method. For instructions, see [Data Export](../db-administration/import-export-data/export-data.md) and [Data Import](../db-administration/import-export-data/import-data.md)