---
title: Product Features
id: product-features
---

# Product Features

## Multi-Model Fusion: One Database for Multiple Use Cases

KWDB integrates both time-series and relational data models into a unified system, enabling seamless data fusion. With unified data access and management across different models, KWDB abstracts data models from applications. This approach meets the needs of both simple data management for single data models in various use cases, and complex system requirements for handling multi-model data in large-scale environments.

## Decentralized Distributed Architecture

**Decentralized and Transparent Distributed Architecture**: KWDB utilizes a fully decentralized, peer-to-peer architecture where all nodes in the cluster are equal, removing any single point of failure.

**High-Performance and Consistent Distributed Transactions**: KWDB supports multi-replica clusters that use the RAFT protocol to maintain data consistency. The system also includes self-healing and adaptive failover capabilities to ensure high availability.

## High-Performance Read/Write Operations

### High-Performance Data Writing

KWDB provides several high-performance data writing methods for both ordered and unordered data:

- Supports standard SQL inserts and imports.
- Capable of writing millions of rows per second.
- Provides nanosecond-level precision for data writing.

### Fast Data Query and Analysis

The time-series table of KWDB is optimized for handling massive amounts of time-series data, improving read/write performance. Users can define primary tags for time-series data and create indexes for fast data retrieval. During data insertion, KWDB automatically partitions data based on tags and uses indexes for rapid query execution. This optimizes both query speed and aggregation performance.

Leveraging in-place computation techniques, KWDB efficiently locates and retrieves target data within large datasets. This delivers significant performance improvements for complex query scenarios including total counts, maximum values by year, `GROUP BY`, and `JOIN` operations. Aggregation queries across millions of records complete in seconds.

KWDB also offers specialized time-series queries to simplify data analysis. It supports user-defined functions and provides a rich set of time/date functions, mathematical functions, aggregation functions and window functions, including `LAST`, value filters, condition-based queries, interpolation functions, as well as `MIN`, `MAX`, `AVG`, and other basic aggregations.

## Cost-Effective Storage

### Online Data Compression

KWDB supports online data compression for both instant and periodic compression. Users can choose from various compression algorithms, including gzip, lz4, lzo, Xz, and zstd, achieving compression ratios of 5-30x to reduce storage costs. The system also allows querying compressed data directly, without the need for decompression.

### Lifecycle Management

KWDB provides lifecycle management at both the database and table levels, automatically deleting data older than a specified retention period. This helps optimize disk space usage and prevent disk overflows, ensuring efficient space utilization.

## Multi-Layered Security

KWDB offers multiple authentication methods that can be used simultaneously. User accounts can be created with customizable permissions and adjusted as needed. For comprehensive data protection, KWDB supports database operation auditing and provides end-to-end security through encrypted communication between clients and servers.

## Ecosystem Tools and Compatibility

### Ecosystem Tools

#### Visual Management Tools

KWDB offers a comprehensive graphical database management tool covering database connections, database management, schema management, table management, and other key functions. This encompasses nearly all database operations, significantly improving user experience.

#### Heterogeneous Database Migration Tools

KWDB provides a comprehensive migration tool for seamless data transfer from heterogeneous databases including MySQL, Oracle, MongoDB, InfluxDB, OpenTSDB, and TDengine. Supporting both full and incremental migration modes, it ensures accurate, consistent, and timely data transfer with minimal operational disruption.

### Ecosystem Compatibility

#### Compatibility with Popular Programming Languages and Operating Systems

KWDB supports connections from a variety of popular programming languages, including C/C++, Java, C#, Python, and more. This flexibility enables developers to choose the most suitable programming language for their projects, educing development costs and improving efficiency. For more details, see [Application Development](../development/overview.md).

KWDB is also compatible with several major operating systems, including Ubuntu, CentOS, Kylin, and UOS, ensuring stable operation across various environments. For a complete list of supported operating systems and CPU architectures, see [Supported Operating Systems and CPU Architectures](./product-metrics.md#operating-systems-and-cpu-architectures).

#### Compatibility with Third-Party Ecosystem Tools

KWDB integrates seamlessly with third-party tools like [EMQX](https://www.emqx.io/), [Kafka](https://kafka.apache.org/), and [Telegraf](https://github.com/influxdata/telegraf). Users can easily read and write data to and from these tools with simple configuration—no additional coding required. This simplifies system setup and maintenance while enhancing flexibility and scalability.