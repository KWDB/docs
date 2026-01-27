---
title: Product Features
id: product-features
---

# Product Features

## Multi-Model Fusion: One Database for Multiple Use Cases

KWDB combines time-series and relational data models into a single unified system. Applications access data through a consistent interface regardless of the underlying data model. This design supports simple deployments using a single data model as well as complex enterprise environments requiring multiple data models at scale.

## Decentralized Distributed Architecture

**Decentralized and Transparent Distributed Architecture**: KWDB utilizes a fully decentralized, peer-to-peer architecture where all nodes in the cluster are equal, eliminating any single point of failure. In the event of node failure, services are seamlessly transferred to other nodes.

**Distributed Linear Scalability**: KWDB supports rapid business scaling with seamless scale-out and scale-in capabilities. Data remains accessible during redistribution with no impact on operations, offering transparent service continuity and petabyte-scale storage capacity.

**High-Performance and Consistent Distributed Transactions**: KWDB supports multi-replica clusters that use the RAFT protocol to maintain data consistency. The system also includes self-healing and adaptive failover capabilities to ensure high availability.

## High-Performance Read/Write Operations

### High-Performance Data Writing

KWDB provides several high-performance data writing methods for both ordered and unordered data:

- Supports standard SQL inserts and imports
- Capable of writing millions of rows in seconds
- Provides nanosecond-level precision for data writing

### Fast Data Query and Analysis

In IoT and similar scenarios, each device type generates data with similar characteristics. KWDB addresses this through time-series tables, an optimized design specifically tailored for high-speed read/write operations on massive time-series datasets.

Time-series tables use primary tags to identify different devices. During data insertion, KWDB automatically partitions data by these tags and creates indexes, enabling rapid location of device-specific data. This design delivers high-performance queries for individual devices and efficient aggregation across large-scale datasets.

Leveraging in-place computation techniques, KWDB efficiently locates and retrieves target data within large datasets. This delivers significant performance improvements for complex query scenarios including total counts, maximum values by year, `GROUP BY`, and `JOIN` operations. Aggregation queries across millions of records complete in seconds.

KWDB provides specialized capabilities for time-series data analysis. It supports user-defined functions and includes a comprehensive set of built-in functions: time/date operations, mathematical calculations, aggregations (`MIN`, `MAX`, `AVG`, etc.), and window functions.

For time-series-specific scenarios, KWDB offers dedicated query features such as LAST value retrieval, value filters, condition-based queries, and interpolation functions.

### Stream Computing

KWDB features built-in stream computing functionality. Users can define tasks using standard SQL, and when data is written to source tables, it is automatically processed and written to target tables based on the defined transformation rules and filter criteria.

Stream computing supports two key use cases:

- Intelligent downsampling: Compresses high-frequency data in real-time to lower frequencies, then synchronizes to the cloud via publish-subscribe mechanisms, reducing storage and transmission costs.
- Pre-computation acceleration: Performs real-time calculations on complex queries and stores results persistently, significantly improving query response times.

## Cost-Effective Storage

### Online Data Compression

KWDB supports real-time online data compression. The system automatically selects the optimal compression algorithm based on data types, achieving compression ratios of 5-30x to reduce storage costs.

### Lifecycle Management

KWDB provides lifecycle management at both the database and table levels, automatically deleting data older than a specified retention period. This helps optimize disk space usage and prevent disk overflows, ensuring efficient space utilization.

## Multi-Layered Security

KWDB offers multiple authentication methods that can be used simultaneously. User accounts can be created with customizable permissions and adjusted as needed. For comprehensive data protection, KWDB supports database operation auditing and provides end-to-end security through encrypted communication between clients and servers.

## Ecosystem Tools and Compatibility

### Ecosystem Tools

#### Visual Management Tools

KWDB offers a graphical database management tool that covers database connections, database management, schema management, table management, and other key functions, encompassing nearly all database operations to improve the user experience.

#### Heterogeneous Database Migration Tools

KWDB provides a complete migration tool for seamless data transfer from heterogeneous databases including MySQL, Oracle, MongoDB, InfluxDB, OpenTSDB, and TDengine. Supporting both full and incremental migration modes, it ensures accurate, consistent, and timely data transfer with minimal operational disruption.

#### Performance Testing Tools

kwdb-tsbs is KWDB's professional time-series database performance benchmarking tool, developed based on Timescale TSBS. It covers the complete testing workflow: data generation, batch import, query execution, and result statistics.

The tool supports CPU monitoring and IoT scenarios with 26 query types to meet diverse business requirements. Key features include high-concurrency processing, flexible parameter configuration, and one-click automated testing. This enables enterprises to conduct reliable performance evaluations for capacity planning, performance tuning, and technology selection.

### Ecosystem Compatibility

#### Programming Languages and Operating Systems

KWDB supports multiple popular programming languages including C/C++, Java, C#, and Python, enabling developers to use their preferred language and reduce development costs. For more details, see [Development](../development/overview.md).

KWDB runs on major operating systems including Ubuntu, CentOS, and UOS. For a complete list of supported operating systems and CPU architectures, see [Supported Operating Systems and CPU Architectures](./product-metrics.md#operating-systems-and-cpu-architectures).

#### Third-Party Ecosystem Tools

KWDB integrates seamlessly with third-party tools like [EMQX](https://www.emqx.io/), [Kafka](https://kafka.apache.org/), [Flink](https://flink.apache.org/), and [Telegraf](https://github.com/influxdata/telegraf). Users can easily read and write data to and from these tools with simple configuration—no additional coding required.