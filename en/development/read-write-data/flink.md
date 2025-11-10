---
title: Flink
id: flink
---

# Flink

Apache Flink is a distributed stream and batch processing framework open-sourced by the Apache Software Foundation, widely used in big data scenarios such as stream processing, batch processing, complex event processing, real-time data warehouse construction, and machine learning.

To achieve efficient integration between Flink and KWDB, KWDB provides a dedicated connector called KaiwuDB Flink Connector. This connector reads data from KWDB through the Source component for real-time analysis, and writes Flink-processed results to KWDB through the Sink component, enabling efficient data storage and management.

KaiwuDB Flink Connector supports the following two usage methods:

- **DataStream API**: Used for low-level stream processing programming, providing flexible data processing capabilities
- **Flink Table**: Provides a high-level declarative interface where users can implement complex data processing logic through SQL statements

## Overview

KaiwuDB Flink Connector supports the following features:

- Read data from KWDB and use Flink for analysis and processing
- Write Flink's complex computation and deep analysis results to KWDB
- Automatic mapping and conversion between KWDB and Flink data types
- Flexible parameter configuration: supports URL address, batch size, database and table names, parallelism, and other configurations
- Supports data partitioning by timestamp and primary tags for concurrent reading

## Configure KaiwuDB Flink Connector

### Prerequisites

- [OpenJDK 1.8 or higher](https://openjdk.org/install/)
- [Maven 3.6 or higher](https://maven.apache.org/install.html)
- KWDB installed and running with:
  - Properly configured database authentication
  - A database created for your connection
  - A user with appropriate privileges on tables or higher
- KaiwuDB Flink Connector installation package obtained
- [Apache Flink 1.19.0 or higher](https://flink.apache.org/)

  Apache Flink installation example:

  ```bash
  # Download Apache Flink
  $ wget https://downloads.apache.org/flink/flink-1.19.2/flink-1.19.2-bin-scala_2.11.tgz

  # Extract Flink archive
  $ tar -xvzf flink-1.19.2-bin-scala_2.11.tgz

  # Start Flink cluster
  $ cd flink-1.19.2
  $ ./bin/start-cluster.sh

  # Verify installation: Access http://127.0.0.1:8081 in browser
  # If you can see the Flink Dashboard, the installation is successful
  ```

### Configure Connector

1. Add the following dependency to your project's `pom.xml` file:

   ```xml
    <dependency>
    <groupId>com.kaiwudb.flink</groupId>
    <artifactId>flink-connector-kaiwudb</artifactId>
    <version>1.0.0</version>
    </dependency>
   ```

2. If the above dependency cannot be loaded normally, run the following command to install KaiwuDB Flink Connector to the local Maven repository:

   ```bash
    mvn install:install-file \
    -Dfile=./flink-connector-kaiwudb-1.0.0.jar \
    -DgroupId=com.kaiwudb.flink \
    -DartifactId=flink-connector-kaiwudb \
    -Dversion=1.0.0 \
    -Dpackaging=jar
   ```

### Configure Semantic Guarantees

After configuring the connector, you need to select an appropriate semantic guarantee level for the Flink job. Based on the characteristics and performance considerations of KWDB's time-series engine, **At-Least-Once** semantic configuration is recommended.

Code example:

```java
StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
// Set parallelism
environment.setParallelism(4);
// Enable checkpointing with 30-second interval
environment.enableCheckpointing(30000);
// Set At-Least-Once semantics
environment.getCheckpointConfig().setCheckpointingMode(CheckpointingMode.AT_LEAST_ONCE); 
```

### Configure Database Connection

Before using the connector, you need to correctly configure database connection parameters. The connector supports basic connection parameter configuration and Flink Table API-specific parameter configuration.

#### Basic Connection Parameters

| Parameter Name | Description | Required | Default Value |
|--------|----------|--------|------|
| url  | Database connection URL | Yes | - |
| dbname  | Database name | Yes | - |
| table.name  | Table name | Yes | - |
| fetch.size | Batch fetch data size | No | 1000 |
| batch.size | Batch write size | No | 1000 |

#### URL Format Specification

The standard format for the database connection URL is:

```java
jdbc:kaiwudb://[host]:[port]/[dbname]?user={user}&password={password}
```

Parameter description:

- `host`: Database host IP or domain name, default is localhost
- `port`: Database port, default is 26257
- `dbname`: Database name
- `user`: Database username
- `password`: Database user login password

#### Flink Table Connector Parameters

When using the Flink Table SQL API, you need to configure the following specific parameters:

| Parameter Name | Type | Required | Description |
|--------|------|----------|------|
| connector | String | Yes | Fixed value: `kaiwudb-connector` |
| mode | String | Yes | Connector mode: `source` (read data) or `sink` (write data) |
| url | String | Yes | KWDB connection URL |
| dbname | String | No | Source database name (used in source mode) |
| table.name | String | No | Source table name for reading data (used in source mode) |
| scan.query | String | No | Custom SQL statement for reading data (used in source mode) |
| fetch.size | Integer | No | Batch size for reading data (used in source mode) |
| sink.db.name | String | No | Target database name (used in sink mode) |
| sink.table.name | String | No | Target table name (used in sink mode) |
| sink.batch.size | Integer | No | Write batch size (used in sink mode) |
| sink.parallelism | Integer | No | Write parallelism (used in sink mode) |

## Configuration Examples

This section provides complete examples of using KaiwuDB Flink Connector, including two scenarios for data reading and writing. Each scenario provides two implementation methods: DataStream API and Table SQL.

### Read Data

#### Read Data Using DataStream API

The following example demonstrates how to read data from KWDB using the DataStream API:

```java
// Test basic data source read functionality
public void testSource() throws Exception {
    System.out.println("Test flink source start！");
    
    // Create SQL split object, specifying the table and fields to query
    SplitObject sqlObject = new SplitObject("select ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 from test_tb");
    
    // Execute source query with parallelism set to 1
    sourceQuery(sqlObject, 1);
    System.out.println("Test flink source finished！");
}

// Test data source read based on time splitting
public void testSourceByTimeSplit() throws Exception {
    System.out.println("Test flink source by time split start！");
    
    // Create SQL split object and configure time split parameters
    SplitObject sqlObject = new SplitObject();
    sqlObject.setSql("select ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 from test_tb")
        .setSplitType(SplitType.TIMESTAMP)  // Set split type to timestamp split
        .setTimestampSplit(new SplitTimestamp(
            "2025-06-11 15:00:00.000",      // Start time
            "2025-06-11 17:00:00.000",      // End time
            "ts",                            // Timestamp field name
            Duration.ofHours(1),             // Time interval per split (1 hour)
            new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS"),  // Time format
            ZoneId.of("Asia/Shanghai")));    // Timezone setting
    
    // Execute source query with parallelism set to 3 (corresponding to number of time splits)
    sourceQuery(sqlObject, 3);
    System.out.println("Test flink source by time split finished！");
}

// Test data source read based on tag splitting
public void testSourceByTagSplit() throws Exception {
    System.out.println("Test flink source by tag split start！");
    
    // Create SQL split object and configure tag split parameters
    SplitObject sqlObject = new SplitObject();
    sqlObject.setSql("select ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 from test_tb")
        .setSplitType(SplitType.TAG)  // Set split type to tag split
        .setTagList(Arrays.asList("t1 = 1", "t1 = 2", "t1 = 3"));  // Set tag filter condition list
    
    // Execute source query with parallelism set to 3 (corresponding to number of tag splits)
    sourceQuery(sqlObject, 3);
    System.out.println("Test flink source by tag split finished！");
}

// Generic source query method
private void sourceQuery(SplitObject sqlObject, int parallelism) throws Exception {
    // Get stream execution environment
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    // Set parallelism
    environment.setParallelism(parallelism);
    
    // Get data source connection properties configuration
    Properties sourceProps = SqlHelper.getProperties("flink_source", null);
    
    // Create KWDB data source, specifying return data type as RowData
    KwdbSource<RowData> source = new KwdbSource <> (sourceProps, sqlObject, RowData.class);
    
    // Create data stream from data source, without watermark strategy
    DataStreamSource<RowData> streamSource = environment.fromSource(source, WatermarkStrategy.noWatermarks(), "kaiwudb-source");
    
    // Convert RowData to string format for easy printing
    DataStream<String> resultStream = streamSource.map((MapFunction<RowData, String>) rowData - >
        "ts: " + rowData.getTimestamp(0, 5) +          // Get timestamp field (index 0, precision 5)
        ", c1: " + rowData.getShort(1) +               // Get SMALLINT field
        ", c2: " + rowData.getInt(2) +                 // Get INT field
        ", c3: " + rowData.getLong(3) +                // Get BIGINT field
        ", c4: " + rowData.getFloat(4) +               // Get FLOAT field
        ", c5: " + rowData.getDouble(5) +              // Get DOUBLE field
        ", c6: " + rowData.getBoolean(6) +             // Get BOOLEAN field
        ", c7: " + rowData.getString(7).toString() +   // Get CHAR field
        ", c8: " + rowData.getString(8).toString() +   // Get VARCHAR field
        ", c9: " + rowData.getString(9).toString() +   // Get VARCHAR field
        ", c10: " + rowData.getString(10).toString() + // Get VARCHAR field
        ", c11: " + Arrays.toString(rowData.getBinary(11)) +  // Get BYTES field
        ", c12: " + rowData.getTimestamp(12, 5) +      // Get second timestamp field
        ", t1: " + rowData.getInt(13) +                // Get tag field 1
        ", t2: " + rowData.getString(14).toString());  // Get tag field 2
    
    // Print result stream
    resultStream.print();
    
    // Execute Flink job
    environment.execute("flink kaiwudb source");
}}
```

#### Read Data Using Flink Table

The following example demonstrates how to read data from KWDB using Flink Table:

```java
// Test creating table using SQL DDL and reading data
public void testFlinkTableSourceBySql() throws Exception {
    System.out.println("Test flink table source by sql start！");
    
    // Create streaming processing environment settings
    EnvironmentSettings settings = EnvironmentSettings.newInstance().inStreamingMode().build();
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    StreamTableEnvironment tableEnvironment = StreamTableEnvironment.create(environment, settings);
    
    // Define source table DDL SQL, including table structure and connector configuration
    String sourceTableSql = "CREATE TABLE source_test_tb (" +
        "ts TIMESTAMP, " +                    // Timestamp field
        "c1 SMALLINT, " +                     // Smallint field
        "c2 INT, " +                          // Integer field
        "c3 BIGINT, " +                       // Bigint field
        "c4 FLOAT, " +                        // Float field
        "c5 DOUBLE, " +                       // Double field
        "c6 BOOLEAN, " +                      // Boolean field
        "c7 CHAR(1), " +                      // Fixed-length character field
        "c8 VARCHAR(10), " +                  // Variable-length character field
        "c9 VARCHAR(10), " +                  // Variable-length character field
        "c10 VARCHAR(10), " +                 // Variable-length character field
        "c11 BYTES, " +                       // Byte array field
        "c12 TIMESTAMP, " +                   // Timestamp field
        "t1 INT, " +                          // Tag field 1
        "t2 VARCHAR(10)" +                    // Tag field 2
        ") WITH (" +                          // Connector configuration
        "  'connector' = 'kaiwudb-connector', " +     // Specify connector type
        "  'mode' = 'source', " +                     // Set to source mode
        "  'url' = 'jdbc:kaiwudb://127.0.0.1:26257/flink_source?user=test&password=Password@2024', " +  // Database connection URL
        "  'table.name' = 'test_tb', " +              // Source table name
        "  'scan.query' = 'SELECT ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 FROM test_tb'" +  // Scan query SQL
        ")";
    
    // Execute DDL statement to create table
    tableEnvironment.executeSql(sourceTableSql);
    
    // Define query SQL
    String querySql = "SELECT ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 FROM source_test_tb";
    
    // Execute query to get result table
    Table resultTable = tableEnvironment.sqlQuery(querySql);
    
    // Print data stream result
    printDataStream(tableEnvironment, resultTable);
    
    // Execute Flink job
    environment.execute("Flink Table Source By Sql API Example");
    System.out.println("Test flink table source by sql finished！");
}

// Test creating table using TableDescriptor API and reading data
public void testFlinkTableSourceByTableDescriptor() throws Exception {
    System.out.println("Test flink table source by TableDescriptor start！");
    
    // Create streaming processing environment settings
    EnvironmentSettings settings = EnvironmentSettings.newInstance().inStreamingMode().build();
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    StreamTableEnvironment tableEnvironment = StreamTableEnvironment.create(environment, settings);
    
    // Use TableDescriptor builder pattern to create table descriptor
    TableDescriptor sourceDescriptor = TableDescriptor.forConnector("kaiwudb-connector")
        // Define table structure Schema
        .schema(Schema.newBuilder()
            .column("ts", DataTypes.TIMESTAMP_WITH_LOCAL_TIME_ZONE().notNull())  // Timestamp with local timezone, not null
            .column("c1", DataTypes.SMALLINT())          // Smallint
            .column("c2", DataTypes.INT())               // Integer
            .column("c3", DataTypes.BIGINT())            // Bigint
            .column("c4", DataTypes.FLOAT())             // Float
            .column("c5", DataTypes.DOUBLE())            // Double
            .column("c6", DataTypes.BOOLEAN())           // Boolean
            .column("c7", DataTypes.CHAR(1))             // Fixed-length character
            .column("c8", DataTypes.VARCHAR(10))         // Variable-length character
            .column("c9", DataTypes.VARCHAR(10))         // Variable-length character
            .column("c10", DataTypes.VARCHAR(10))        // Variable-length character
            .column("c11", DataTypes.BYTES())            // Byte array
            .column("c12", DataTypes.TIMESTAMP())        // Timestamp
            .column("t1", DataTypes.INT().notNull())     // Tag field 1, not null
            .column("t2", DataTypes.VARCHAR(10))         // Tag field 2
            .build())
        // Configure connector options
        .option("url", "jdbc:kaiwudb://127.0.0.1:26257/flink_source?user=test&password=Password@2024")  // Database connection URL
        .option("mode", "source")                        // Set to source mode
        .option("table.name", "test_tb")                 // Source table name
        .option("scan.query", "SELECT ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 FROM test_tb")  // Scan query SQL
        .build();
    
    // Register temporary table
    tableEnvironment.createTemporaryTable("source_test_tb", sourceDescriptor);

    // Define query SQL with filter condition
    String querySql = "SELECT ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 FROM source_test_tb WHERE t1 > 2";
    
    // Execute query to get result table
    Table resultTable = tableEnvironment.sqlQuery(querySql);
    
    // Print data stream result
    printDataStream(tableEnvironment, resultTable);
    
    // Execute Flink job
    environment.execute("Test flink table source by TableDescriptor API Example");
    System.out.println("Test flink table source by TableDescriptor finished！");
}

// Generic data stream print method
private void printDataStream(StreamTableEnvironment tableEnvironment, Table resultTable) {
    // Convert Table to AppendStream (append-only stream)
    DataStream<RowData> resultStream = tableEnvironment.toAppendStream(resultTable, RowData.class);
    
    // Map RowData to string format and print
    resultStream.map((MapFunction<RowData, String>) rowData ->
        "ts: " + rowData.getTimestamp(0, 5)                           // Timestamp field
         + ", c1: " + rowData.getShort(1)                             // Smallint field
         + ", c2: " + rowData.getInt(2)                               // Integer field
         + ", c3: " + rowData.getLong(3)                              // Bigint field
         + ", c4: " + rowData.getFloat(4)                             // Float field
         + ", c5: " + rowData.getDouble(5)                            // Double field
         + ", c6: " + rowData.getBoolean(6)                           // Boolean field
         + ", c7: " + rowData.getString(7).toString()                 // Fixed-length character field
         + ", c8: " + rowData.getString(8).toString()                 // Variable-length character field
         + ", c9: " + rowData.getString(9).toString()                 // Variable-length character field
         + ", c10: " + rowData.getString(10).toString()               // Variable-length character field
         + ", c11: " + new String(rowData.getBinary(11), StandardCharsets.UTF_8)  // Byte array field, converted to UTF-8 string
         + ", c12: " + rowData.getTimestamp(12, 5)                    // Second timestamp field
         + ", t1: " + rowData.getInt(13)                              // Tag field 1
         + ", t2: " + rowData.getString(14).toString()                // Tag field 2
    ).print();
}
```

### Write Data

#### Write Data Using DataStream API

The following example demonstrates how to write data to KWDB using the DataStream API:

```java
// Test complete flow of reading data from KWDB and writing to another KWDB instance
public void testSourceToSink() throws Exception {
    System.out.println("Test flink source to sink start！");
    
    // Get stream execution environment
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    environment.setParallelism(1);  // Set parallelism to 1
    environment.enableCheckpointing(3000, AT_LEAST_ONCE);  // Enable checkpointing with 3-second interval, at-least-once semantics

    // Configure data source time split parameters
    SplitObject sqlObject = new SplitObject();
    sqlObject.setSql("select ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 from test_tb")
        .setSplitType(SplitType.TIMESTAMP)  // Set split type to timestamp split
        .setTimestampSplit(new SplitTimestamp(
            "2025-06-11 15:00:00.000",      // Start time
            "2025-06-11 18:00:00.000",      // End time
            "ts",                            // Timestamp field name
            Duration.ofHours(1),             // Time interval per split (1 hour)
            new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS"),  // Time format
            ZoneId.of("Asia/Shanghai")));    // Timezone setting
    
    // Get data source connection properties configuration
    Properties sourceProps = SqlHelper.getProperties("flink_source", null);
    
    // Create KWDB data source
    KwdbSource<RowData> source = new KwdbSource<> (sourceProps, sqlObject, RowData.class);
    
    // Create data stream from data source
    DataStreamSource<RowData> streamSource = environment.fromSource(source, WatermarkStrategy.noWatermarks(), "KaiwuDB-Source");

    // Get data sink connection properties configuration, set batch size to 2000
    Properties sinkProps = SqlHelper.getProperties("flink_kaiwudb_sink", "2000");
    
    // Define field name list, corresponding to source table fields
    List<String> fieldNames = Arrays.asList("ts", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12", "t1", "t2");
    
    // Create KWDB data sink
    KwdbSink<RowData> sink = new KwdbSink <> (sinkProps, fieldNames);
    
    // Write data stream to target database
    streamSource.sinkTo(sink);
    
    // Execute Flink job
    environment.execute("flink kaiwudb source");
    
    // Verify data write result: Query sum of t1 field in target table
    String querySumSql = "select sum(t1) from flink_kaiwudb_sink.test_tb";
    int querySumResult = SqlHelper.querySumResult(querySumSql);
    Assertions.assertEquals(30, querySumResult);  // Assert result is 30

    System.out.println("Test flink source to sink finished！");
}
```

#### Write Data Using Flink Table

##### Write SQL Type Data to KWDB

The following example demonstrates how to read data from MySQL CDC and write to KWDB using Flink Table:

```java
// Test reading data from MySQL CDC and writing to KWDB
public void testMysqlSourceToKaiwuDBSink() throws Exception {
    // Get stream execution environment and set checkpointing
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    environment.setParallelism(1);  // Set parallelism to 1
    environment.enableCheckpointing(3000, AT_LEAST_ONCE);  // Enable checkpointing with 3-second interval, at-least-once semantics
    
    // Declare conversion processing configuration for boolean type in MySQL
    Properties debeziumProperties = new Properties();
    debeziumProperties.setProperty("converters", "boolean");  // Set converter
    debeziumProperties.setProperty("boolean.type", "io.debezium.connector.mysql.converters.TinyIntOneToBooleanConverter");  // Convert MySQL TINYINT(1) to Boolean

    // Build MySQL CDC data source
    MySqlSource<RowData> source = MySqlSource.<RowData>builder()
        .hostname("127.0.0.1")              // MySQL host address
        .port(3306)                         // MySQL port
        .databaseList("flink_source")       // List of databases to monitor
        .tableList("flink_source.test_tb")  // List of tables to monitor
        .username("root")                   // Username
        .password("123456")                 // Password
        .deserializer(new RowDataDebeziumDeserializationSchema())  // Deserializer
        .debeziumProperties(debeziumProperties)  // Debezium configuration properties
        .build();
    
    // Create data stream from MySQL CDC source
    DataStreamSource<RowData> streamSource = environment.fromSource(source, WatermarkStrategy.noWatermarks(), "MySQL Source");

    // Get KWDB sink connection properties configuration, set batch size to 2000
    Properties sinkProps = SqlHelper.getProperties("flink_mysql_sink", "2000");
    
    // Define field name list
    List<String> fieldNames = Arrays.asList("ts", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12", "t1", "t2");
    
    // Create KWDB data sink
    KwdbSink<RowData> sink = new KwdbSink<> (sinkProps, fieldNames);
    
    // Write MySQL CDC data stream to KWDB
    streamSource.sinkTo(sink);
    
    System.out.println("Test flink cdc source mysql to sink kaiwudb starting！");
    
    // Execute Flink job
    environment.execute("flink kaiwudb source");
}
```

##### Write ROW Type Data to KWDB

The following example demonstrates how to write row data to KWDB using Flink Table API:

```java
// Test writing row data from Flink Table to KWDB
public void testFlinkTableRowToSink() throws Exception {
    System.out.println("Test flink table row source to sink start！");
    
    // Create streaming processing environment settings
    EnvironmentSettings settings = EnvironmentSettings.newInstance().inStreamingMode().build();
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    environment.enableCheckpointing(3000, AT_LEAST_ONCE);  // Enable checkpointing
    StreamTableEnvironment tableEnvironment = StreamTableEnvironment.create(environment, settings);
    
    // Define target table DDL SQL
    String sinkTableSql = "CREATE TABLE sink_test_tb (" +
        "ts TIMESTAMP, " +                    // Timestamp field
        "c1 INT, " +                          // Integer field
        "c2 INT, " +                          // Integer field
        "c3 INT, " +                          // Integer field
        "c4 FLOAT, " +                        // Float field
        "c5 DOUBLE, " +                       // Double field
        "c6 BOOLEAN, " +                      // Boolean field
        "c7 CHAR(1), " +                      // Fixed-length character field
        "c8 VARCHAR(10), " +                  // Variable-length character field
        "c9 VARCHAR(10), " +                  // Variable-length character field
        "c10 VARCHAR(10), " +                 // Variable-length character field
        "c11 BYTES, " +                       // Byte array field
        "c12 TIMESTAMP, " +                   // Timestamp field
        "t1 INT, " +                          // Tag field 1
        "t2 VARCHAR(10)" +                    // Tag field 2
        ") WITH (" +                          // Connector configuration
        "  'connector' = 'kaiwudb-connector', " +     // Specify connector type
        "  'mode' = 'sink', " +                       // Set to sink mode
        "  'url' = 'jdbc:kaiwudb://127.0.0.1:26257/flink_table_kaiwudb_sink?user=test&password=Password@2024', " +  // Database connection URL
        "  'sink.db.name' = 'flink_table_kaiwudb_sink', " +   // Target database name
        "  'sink.table.name' = 'test_tb'" +                   // Target table name
        ")";
    
    // Execute DDL statement to create sink table
    tableEnvironment.executeSql(sinkTableSql);
    
    // Get input data table (containing test data)
    Table inputTable = getInputTable(tableEnvironment);
    
    // Execute insert operation to write data to target table
    TableResult tableResult = inputTable.executeInsert("sink_test_tb");
    tableResult.await();  // Wait for insert operation to complete
    
    // Verify data write result: Query sum of t1 field in target table that meets conditions
    String querySumSql = "SELECT sum(t1) FROM flink_table_kaiwudb_sink.test_tb WHERE t1 < 5";
    int querySumResult = SqlHelper.querySumResult(querySumSql);
    Assertions.assertEquals(20, querySumResult);  // Assert result is 20
    
    System.out.println("Test flink table row source to sink finished！");
}

// Generate test input data table
private Table getInputTable(StreamTableEnvironment tableEnvironment) {
    // Create row data list
    List<Row> rowData = new ArrayList<>();
    ThreadLocalRandom random = ThreadLocalRandom.current();  // Thread-safe random number generator
    long tsTime = 1749625212123 L;  // Base timestamp
    
    // Generate 10 rows of test data
    for (int i = 0; i < 10; i++) {
        long timestamp = tsTime + (15 * 60 * 1000) * i;  // 15-minute interval between rows
        Row row = Row.of(
            new Timestamp(timestamp),                     // Timestamp field
            random.nextInt(10),                          // Random integer (0-9)
            random.nextInt(100),                         // Random integer (0-99)
            random.nextInt(1000),                        // Random integer (0-999)
            random.nextFloat(),                          // Random float
            random.nextDouble(),                         // Random double
            random.nextBoolean(),                        // Random boolean
            RandomStringUtils.randomAlphanumeric(1),     // Random 1-character alphanumeric
            RandomStringUtils.randomAlphanumeric(10),    // Random 10-character alphanumeric string
            RandomStringUtils.randomAlphanumeric(10),    // Random 10-character alphanumeric string
            RandomStringUtils.randomAlphanumeric(10),    // Random 10-character alphanumeric string
            RandomStringUtils.randomAlphanumeric(10),
            ```java
            RandomStringUtils.randomAlphanumeric(10),    // Random 10-character alphanumeric string (as byte array)
            new Timestamp(timestamp),                     // Second timestamp field
            (i / 2) + 1,                                 // Tag field 1: calculated based on index (1,1,2,2,3,3...)
            "tianjin"                                    // Tag field 2: fixed value
        );
        rowData.add(row);
    }
    
    // Create table using fromValues method, defining data types and field structure
    return tableEnvironment.fromValues(
        DataTypes.ROW(
            DataTypes.FIELD("ts", DataTypes.TIMESTAMP(6)),      // Timestamp field, precision 6
            DataTypes.FIELD("c1", DataTypes.INT()),             // Integer field
            DataTypes.FIELD("c2", DataTypes.INT()),             // Integer field
            DataTypes.FIELD("c3", DataTypes.INT()),             // Integer field
            DataTypes.FIELD("c4", DataTypes.FLOAT()),           // Float field
            DataTypes.FIELD("c5", DataTypes.DOUBLE()),          // Double field
            DataTypes.FIELD("c6", DataTypes.BOOLEAN()),         // Boolean field
            DataTypes.FIELD("c7", DataTypes.CHAR(1)),           // Fixed-length character field
            DataTypes.FIELD("c8", DataTypes.STRING()),          // String field
            DataTypes.FIELD("c9", DataTypes.STRING()),          // String field
            DataTypes.FIELD("c10", DataTypes.STRING()),         // String field
            DataTypes.FIELD("c11", DataTypes.BYTES()),          // Byte array field
            DataTypes.FIELD("c12", DataTypes.TIMESTAMP(6)),     // Timestamp field, precision 6
            DataTypes.FIELD("t1", DataTypes.INT()),             // Tag field 1
            DataTypes.FIELD("t2", DataTypes.STRING())           // Tag field 2
        ),
        rowData  // Pass in generated test data
    );
}
```

## Reference Information

### Data Type Conversion

**Time-Series Data**

| KWDB                 | Flink RowData    | Flink Table SQL   |
|------------------------|------------------|--------------------|
| TIMESTAMP              | Timestamp        | TIMESTAMP          |
| TIMESTAMPTZ            | Timestamp        | TIMESTAMP_LTZ      |
| BOOL                   | Boolean          | BOOLEAN            |
| SMALLINT               | Short            | SMALLINT           |
| INT                    | Integer          | INT                |
| BIGINT                 | Long             | BIGINT             |
| REAL                   | Float            | FLOAT              |
| DOUBLE                 | Double           | DOUBLE             |
| VARBYTES               | byte[]           | BYTES              |
| CHAR                   | String           | CHAR/STRING        |
| VARCHAR、NCHAR、NVARCHAR | String         | VARCHAR/STRING     |
| GEOMETRY               | String           | STRING             |

**Relational Data**

::: warning Note
The DECIMAL type must have precision and scale values set, otherwise processing data of this type is not supported.
:::

| KWDB                 | Flink RowData    | Flink Table SQL   |
|-------------------------|------------------|--------------------|
| TIMESTAMP               | Timestamp        | TIMESTAMP          |
| TIMESTAMPTZ             | Timestamp        | TIMESTAMP_LTZ      |
| DATE                    | String           | STRING             |
| TIME                    | Time             | TIME               |
| BOOL                    | Boolean          | BOOLEAN            |
| SMALLINT                | Short            | SMALLINT           |
| INT                     | Integer          | INT                |
| BIGINT、SERIAL           | Long             | BIGINT             |
| REAL                  | Float            | FLOAT              |
| DOUBLE                  | Double           | DOUBLE             |
| DECIMAL(p,s)            | BigDecimal       | DECIMAL(p,s)       |
| BIT、VARBIT              | String           | STRING             |
| BYTES、VARBYTES          | byte[]           | BYTES              |
| CHAR                    | String           | CHAR/STRING        |
| VARCHAR、NCHAR、NVARCHAR  | String           | VARCHAR/STRING     |
| JSON、JSONB、TEXT         | String           | STRING             |
| STRING[]、STRING、COLLATE | String           | STRING             |
| INTERVAL、INET、UUID      | String           | STRING             |