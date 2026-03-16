---
title: Flink
id: flink
---

# Flink

Apache Flink is a distributed stream and batch processing framework open-sourced by the Apache Software Foundation. It is widely used in big data scenarios including stream processing, batch processing, complex event processing, real-time data warehouse construction, and machine learning.

KWDB provides the **KaiwuDB Flink Connector** to enable seamless integration between Flink and KWDB. This connector allows you to:

- Read data from KWDB using the Source component for real-time analysis
- Write Flink-processed results back to KWDB using the Sink component for efficient storage and management

The KaiwuDB Flink Connector supports the following two interfaces to suit different use cases:

- **DataStream API**: A low-level programming interface for fine-grained stream processing control and flexible data transformations
- **Flink Table API**: A high-level declarative interface that enables complex data processing through SQL statements

## Key Features

KaiwuDB Flink Connector supports the following features:

- **Bidirectional Data Flow**: Read from and write to KWDB seamlessly
- **Automatic Type Mapping**: Built-in conversion between KWDB and Flink data types
- **Flexible Configuration**: Customize URL addresses, batch sizes, database and table names, parallelism levels, and more
- **Parallel Processing**: Support for concurrent data reading through timestamp-based and tag-based splitting

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

If you haven't already installed Apache Flink, follow these steps:

```bash
# Download Apache Flink
$ wget https://downloads.apache.org/flink/flink-1.19.2/flink-1.19.2-bin-scala_2.11.tgz

# Extract the archive
$ tar -xvzf flink-1.19.2-bin-scala_2.11.tgz

# Navigate to the Flink directory
$ cd flink-1.19.2

# Start the Flink cluster
$ ./bin/start-cluster.sh

# Verify installation: 
# Open http://127.0.0.1:8081 in your browser
# The Flink Dashboard should be visible if installation was successful
```

### Configure Connector

1. Add the KaiwuDB Flink Connector dependency to your project's `pom.xml` file:

   ```xml
    <dependency>
    <groupId>com.kaiwudb.flink</groupId>
    <artifactId>flink-connector-kaiwudb</artifactId>
    <version>1.0.0</version>
    </dependency>
   ```

2. If the dependency cannot be resolved automatically, install it manually to your local Maven repository:

   ```bash
    mvn install:install-file \
    -Dfile=./flink-connector-kaiwudb-1.0.0.jar \
    -DgroupId=com.kaiwudb.flink \
    -DartifactId=flink-connector-kaiwudb \
    -Dversion=1.0.0 \
    -Dpackaging=jar
   ```

### Configure Semantic Guarantees

Flink provides different semantic guarantees for data processing. Based on the characteristics and performance profile of KWDB's time-series engine, we recommend using **At-Least-Once** semantics.

Example:

```java
StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();

// Configure parallelism level
environment.setParallelism(4);

// Enable checkpointing with 30-second interval
environment.enableCheckpointing(30000);

// Configure At-Least-Once semantic guarantee
environment.getCheckpointConfig().setCheckpointingMode(CheckpointingMode.AT_LEAST_ONCE); 
```

### Configure Database Connection

The connector requires proper database connection configuration. The following sections describe the available parameters for both basic usage and Flink Table API.

#### Connection Parameters

| Parameter | Description | Required | Default Value |
|--------|----------|--------|------|
| url  | JDBC connection URL for the database | Yes | - |
| dbname  | Name of the target database | Yes | - |
| table.name  | Name of the target table| Yes | - |
| fetch.size | Number of records fetched per batch read | No | 1000 |
| batch.size | Number of records written per batch write | No | 1000 |

#### Connection URL Format

Use the following format for your JDBC connection URL:

```java
jdbc:kaiwudb://[host]:[port]/[dbname]?user={user}&password={password}
```

Parameters:

- `host`: Database server IP address or hostname (default: `localhost`)
- `port`: Database server port (default: `26257`)
- `dbname`: Name of the database to connect to
- `user`: Database username for authentication
- `password`: Password for the specified user

#### Flink Table API Parameters

When using the Flink Table SQL API, configure these additional parameters:

| Parameter | Type | Required | Description |
|--------|------|----------|------|
| connector | String | Yes | Must be set to `kaiwudb-connector` |
| mode | String | Yes | Connector mode: `source` (read) or `sink` (write) |
| url | String | Yes | JDBC connection URL |
| dbname | String | No | Source database name (source mode only) |
| table.name | String | No | Source table name for reading (source mode only) |
| scan.query | String | No | Custom SQL query for data retrieval (source mode only) |
| fetch.size | Integer | No | Batch size for read operations (source mode only) |
| sink.db.name | String | No | Target database name (sink mode only) |
| sink.table.name | String | No | Target table name (sink mode only) |
| sink.batch.size | Integer | No | Batch size for write operations (sink mode only) |
| sink.parallelism | Integer | No | Parallelism level for writes (sink mode only) |

## Examples

This section provides comprehensive examples demonstrating how to use the KaiwuDB Flink Connector for both reading and writing data. Each scenario includes implementations using both the DataStream API and the Flink Table API.

### Read Data

#### DataStream API

The following example demonstrates how to read data from KWDB using the DataStream API:

```java
// Basic Read with DataStream API
public void testSource() throws Exception {
    System.out.println("Test flink source start!");
    
    // Create SQL query object specifying the table and columns
    SplitObject sqlObject = new SplitObject("select ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 from test_tb");
    
    // Execute the source query with parallelism of 1
    sourceQuery(sqlObject, 1);
    System.out.println("Test flink source finished!");
}

// Time-Based Splitting
public void testSourceByTimeSplit() throws Exception {
    System.out.println("Test flink source by time split start!");
    
    // Configure SQL query with timestamp-based splitting
    SplitObject sqlObject = new SplitObject();
    sqlObject.setSql("select ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 from test_tb")
        .setSplitType(SplitType.TIMESTAMP)  // Set split type to timestamp split
        .setTimestampSplit(new SplitTimestamp(
            "2025-06-11 15:00:00.000",      // Start time
            "2025-06-11 17:00:00.000",      // End time
            "ts",                            // Timestamp column name
            Duration.ofHours(1),             // Time interval (1 hour)
            new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS"),  // Date format
            ZoneId.of("Asia/Shanghai")));    // Time zone
    
    // Execute with parallelism of 3 (matches number of time splits)
    sourceQuery(sqlObject, 3);
    System.out.println("Test flink source by time split finished!");
}

// Tag-Based Splitting
public void testSourceByTagSplit() throws Exception {
    System.out.println("Test flink source by tag split start!");
    
    // Configure SQL query with tag-based splitting
    SplitObject sqlObject = new SplitObject();
    sqlObject.setSql("select ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 from test_tb")
        .setSplitType(SplitType.TAG)  // Set split type to tag split
        .setTagList(Arrays.asList("t1 = 1", "t1 = 2", "t1 = 3"));  // Tag filter conditions
    
    // Execute with parallelism of 3 (matches number of tag splits)
    sourceQuery(sqlObject, 3);
    System.out.println("Test flink source by tag split finished!");
}

// Generic source query method
private void sourceQuery(SplitObject sqlObject, int parallelism) throws Exception {
    // Initialize the stream execution environment
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    // Set parallelism
    environment.setParallelism(parallelism);
    
    // Load source connection properties
    Properties sourceProps = SqlHelper.getProperties("flink_source", null);
    
    // Create the KWDB source with RowData output type
    KwdbSource<RowData> source = new KwdbSource <> (sourceProps, sqlObject, RowData.class);
    
    // Create the data stream
    DataStreamSource<RowData> streamSource = environment.fromSource(source, WatermarkStrategy.noWatermarks(), "kaiwudb-source");
    
    // Transform RowData to readable string format
    DataStream<String> resultStream = streamSource.map((MapFunction<RowData, String>) rowData - >
        "ts: " + rowData.getTimestamp(0, 5) +          
        ", c1: " + rowData.getShort(1) +               
        ", c2: " + rowData.getInt(2) +                 
        ", c3: " + rowData.getLong(3) +                
        ", c4: " + rowData.getFloat(4) +               
        ", c5: " + rowData.getDouble(5) +              
        ", c6: " + rowData.getBoolean(6) +             
        ", c7: " + rowData.getString(7).toString() +   
        ", c8: " + rowData.getString(8).toString() +   
        ", c9: " + rowData.getString(9).toString() +   
        ", c10: " + rowData.getString(10).toString() + 
        ", c11: " + Arrays.toString(rowData.getBinary(11)) +  
        ", c12: " + rowData.getTimestamp(12, 5) +      
        ", t1: " + rowData.getInt(13) +                
        ", t2: " + rowData.getString(14).toString());  
    
    // Print results to console
    resultStream.print();
    
    // Execute the Flink job
    environment.execute("flink kaiwudb source");
}}
```

#### Flink Table SQL

The following example demonstrates how to read data from KWDB using Flink Table SQL:

```java
// Test creating table using SQL DDL and reading data
public void testFlinkTableSourceBySql() throws Exception {
    System.out.println("Test flink table source by sql start!");
    
    // Configure streaming environment
    EnvironmentSettings settings = EnvironmentSettings.newInstance().inStreamingMode().build();
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    StreamTableEnvironment tableEnvironment = StreamTableEnvironment.create(environment, settings);
    
    // Define source table using DDL
    String sourceTableSql = "CREATE TABLE source_test_tb (" +
        "ts TIMESTAMP, " +                    
        "c1 SMALLINT, " +                     
        "c2 INT, " +                          
        "c3 BIGINT, " +                       
        "c4 FLOAT, " +                        
        "c5 DOUBLE, " +                       
        "c6 BOOLEAN, " +                      
        "c7 CHAR(1), " +                      
        "c8 VARCHAR(10), " +                  
        "c9 VARCHAR(10), " +                  
        "c10 VARCHAR(10), " +                 
        "c11 BYTES, " +                       
        "c12 TIMESTAMP, " +                   
        "t1 INT, " +                          // Tag 1
        "t2 VARCHAR(10)" +                    // Tag 2
        ") WITH (" +                          // Connector configuration
        "  'connector' = 'kaiwudb-connector', " +     // Specify connector type
        "  'mode' = 'source', " +                     // Set the source mode
        "  'url' = 'jdbc:kaiwudb://127.0.0.1:26257/flink_source?user=test&password=Password@2024', " +  // Database connection URL
        "  'table.name' = 'test_tb', " +              // Source table name
        "  'scan.query' = 'SELECT ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 FROM test_tb'" +  // Scan query SQL
        ")";
    
    // Execute DDL to create table
    tableEnvironment.executeSql(sourceTableSql);
    
    // Query the data
    String querySql = "SELECT ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 FROM source_test_tb";

    Table resultTable = tableEnvironment.sqlQuery(querySql);
    
    // Print results
    printDataStream(tableEnvironment, resultTable);
    
    // Execute the job
    environment.execute("Flink Table Source By Sql API Example");
    System.out.println("Test flink table source by sql finished!");
}

// Test using TableDescriptor API and reading data
public void testFlinkTableSourceByTableDescriptor() throws Exception {
    System.out.println("Test flink table source by TableDescriptor start!");
    
    // Configure streaming environment
    EnvironmentSettings settings = EnvironmentSettings.newInstance().inStreamingMode().build();
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    StreamTableEnvironment tableEnvironment = StreamTableEnvironment.create(environment, settings);
    
    // Build table descriptor programmatically
    TableDescriptor sourceDescriptor = TableDescriptor.forConnector("kaiwudb-connector")
        // Define table structure
        .schema(Schema.newBuilder()
            .column("ts", DataTypes.TIMESTAMP_WITH_LOCAL_TIME_ZONE().notNull())  // Timestamp with local timezone, not null
            .column("c1", DataTypes.SMALLINT())          
            .column("c2", DataTypes.INT())               
            .column("c3", DataTypes.BIGINT())            
            .column("c4", DataTypes.FLOAT())             
            .column("c5", DataTypes.DOUBLE())            
            .column("c6", DataTypes.BOOLEAN())           
            .column("c7", DataTypes.CHAR(1))             
            .column("c8", DataTypes.VARCHAR(10))         
            .column("c9", DataTypes.VARCHAR(10))         
            .column("c10", DataTypes.VARCHAR(10))        
            .column("c11", DataTypes.BYTES())            
            .column("c12", DataTypes.TIMESTAMP())        
            .column("t1", DataTypes.INT().notNull())     // Tag 1, not null
            .column("t2", DataTypes.VARCHAR(10))         // Tag 2
            .build())
        // Configure connector options
        .option("url", "jdbc:kaiwudb://127.0.0.1:26257/flink_source?user=test&password=Password@2024")  // Database connection URL
        .option("mode", "source")                        // Set the source mode
        .option("table.name", "test_tb")                 // Source table name
        .option("scan.query", "SELECT ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 FROM test_tb")  // Scan query SQL
        .build();
    
    // Register the table
    tableEnvironment.createTemporaryTable("source_test_tb", sourceDescriptor);

    // Query with a filter condition
    String querySql = "SELECT ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 FROM source_test_tb WHERE t1 > 2";
    
    // Execute query
    Table resultTable = tableEnvironment.sqlQuery(querySql);
    
    // Print results
    printDataStream(tableEnvironment, resultTable);
    
    // Execute the job
    environment.execute("Test flink table source by TableDescriptor API Example");
    System.out.println("Test flink table source by TableDescriptor finished!");
}

// Generic data stream print method
private void printDataStream(StreamTableEnvironment tableEnvironment, Table resultTable) {
    // Convert table to data stream
    DataStream<RowData> resultStream = tableEnvironment.toAppendStream(resultTable, RowData.class);
    
    // Transform and print
    resultStream.map((MapFunction<RowData, String>) rowData ->
        "ts: " + rowData.getTimestamp(0, 5)                           
         + ", c1: " + rowData.getShort(1)                             
         + ", c2: " + rowData.getInt(2)                               
         + ", c3: " + rowData.getLong(3)                              
         + ", c4: " + rowData.getFloat(4)                             
         + ", c5: " + rowData.getDouble(5)                            
         + ", c6: " + rowData.getBoolean(6)                           
         + ", c7: " + rowData.getString(7).toString()                 
         + ", c8: " + rowData.getString(8).toString()                 
         + ", c9: " + rowData.getString(9).toString()                 
         + ", c10: " + rowData.getString(10).toString()               
         + ", c11: " + new String(rowData.getBinary(11), StandardCharsets.UTF_8)  
         + ", c12: " + rowData.getTimestamp(12, 5)                    
         + ", t1: " + rowData.getInt(13)                              // Tag 1
         + ", t2: " + rowData.getString(14).toString()                // Tag 2
    ).print();
}
```

### Write Data

#### DataStream API

The following example demonstrates how to write data to KWDB using the DataStream API:

```java
// Test complete flow of reading data from KWDB and writing to another KWDB instance
public void testSourceToSink() throws Exception {
    System.out.println("Test flink source to sink start!");
    
    // Configure execution environment
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    environment.setParallelism(1); 
    environment.enableCheckpointing(3000, AT_LEAST_ONCE);  

    //  Configure source with time-based splitting
    SplitObject sqlObject = new SplitObject();
    sqlObject.setSql("select ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 from test_tb")
        .setSplitType(SplitType.TIMESTAMP)  // Set split type to timestamp split
        .setTimestampSplit(new SplitTimestamp(
            "2025-06-11 15:00:00.000",      // Start time
            "2025-06-11 18:00:00.000",      // End time
            "ts",                            // Timestamp column name
            Duration.ofHours(1),             // Time interval (1 hour)
            new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS"),  // Date format
            ZoneId.of("Asia/Shanghai")));    // Time zone
    
    // Create source
    Properties sourceProps = SqlHelper.getProperties("flink_source", null);
    KwdbSource<RowData> source = new KwdbSource<> (sourceProps, sqlObject, RowData.class);
    DataStreamSource<RowData> streamSource = environment.fromSource(source, WatermarkStrategy.noWatermarks(), "KaiwuDB-Source");

    // Create sink
    Properties sinkProps = SqlHelper.getProperties("flink_kaiwudb_sink", "2000");
    List<String> fieldNames = Arrays.asList("ts", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12", "t1", "t2");
    KwdbSink<RowData> sink = new KwdbSink <> (sinkProps, fieldNames);
    
    // Connect source to sink
    streamSource.sinkTo(sink);
    
    // Execute the pipeline
    environment.execute("flink kaiwudb source");
    
    // Verify results
    String querySumSql = "select sum(t1) from flink_kaiwudb_sink.test_tb";
    int querySumResult = SqlHelper.querySumResult(querySumSql);
    Assertions.assertEquals(30, querySumResult);  

    System.out.println("Test flink source to sink finished!");
}
```

#### Flink Table SQL

##### Write SQL Data to KWDB

The following example demonstrates how to read data from MySQL CDC and write to KWDB using Flink Table:

```java
// Test reading data from MySQL CDC and writing to KWDB
public void testMysqlSourceToKaiwuDBSink() throws Exception {
    // Configure execution environment
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    environment.setParallelism(1);  
    environment.enableCheckpointing(3000, AT_LEAST_ONCE);  
    
    // Configure Debezium for MySQL boolean type conversion
    Properties debeziumProperties = new Properties();
    debeziumProperties.setProperty("converters", "boolean");  
    debeziumProperties.setProperty("boolean.type", "io.debezium.connector.mysql.converters.TinyIntOneToBooleanConverter");  

    // Build MySQL CDC source
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
    
    // Create data stream from MySQL CDC
    DataStreamSource<RowData> streamSource = environment.fromSource(source, WatermarkStrategy.noWatermarks(), "MySQL Source");

    // Create KWDB sink
    Properties sinkProps = SqlHelper.getProperties("flink_mysql_sink", "2000");
    List<String> fieldNames = Arrays.asList("ts", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12", "t1", "t2");
    KwdbSink<RowData> sink = new KwdbSink<> (sinkProps, fieldNames);
    
    // Write MySQL changes to KWDB
    streamSource.sinkTo(sink);
    
    System.out.println("Test flink cdc source mysql to sink kaiwudb starting!");
    
    // Execute the Flink job
    environment.execute("flink kaiwudb source");
}
```

##### Write ROW Data to KWDB

The following example demonstrates how to write row data to KWDB using Flink Table API:

```java
// Test writing row data from Flink Table to KWDB
public void testFlinkTableRowToSink() throws Exception {
    System.out.println("Test flink table row source to sink start!");
    
    // Configure streaming environment
    EnvironmentSettings settings = EnvironmentSettings.newInstance().inStreamingMode().build();
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    environment.enableCheckpointing(3000, AT_LEAST_ONCE);  // Enable checkpointing
    StreamTableEnvironment tableEnvironment = StreamTableEnvironment.create(environment, settings);
    
    // Define sink table using DDL
    String sinkTableSql = "CREATE TABLE sink_test_tb (" +
        "ts TIMESTAMP, " +                    
        "c1 INT, " +                          
        "c2 INT, " +                          
        "c3 INT, " +                          
        "c4 FLOAT, " +                        
        "c5 DOUBLE, " +                       
        "c6 BOOLEAN, " +                      
        "c7 CHAR(1), " +                      
        "c8 VARCHAR(10), " +                  
        "c9 VARCHAR(10), " +                  
        "c10 VARCHAR(10), " +                 
        "c11 BYTES, " +                       
        "c12 TIMESTAMP, " +                   
        "t1 INT, " +                          // Tag 1
        "t2 VARCHAR(10)" +                    // Tag 2
        ") WITH (" +                          // Connector configuration
        "  'connector' = 'kaiwudb-connector', " +     // Specify connector type
        "  'mode' = 'sink', " +                       // Set the sink mode
        "  'url' = 'jdbc:kaiwudb://127.0.0.1:26257/flink_table_kaiwudb_sink?user=test&password=Password@2024', " +  // Database connection URL
        "  'sink.db.name' = 'flink_table_kaiwudb_sink', " +   // Target database name
        "  'sink.table.name' = 'test_tb'" +                   // Target table name
        ")";
    
    // Create the sink table
    tableEnvironment.executeSql(sinkTableSql);
    
    // Generate test data
    Table inputTable = getInputTable(tableEnvironment);
    
    // Insert data into sink table
    TableResult tableResult = inputTable.executeInsert("sink_test_tb");
    tableResult.await();  // Wait for insert operation to complete
    
    // Verify the write operation
    String querySumSql = "SELECT sum(t1) FROM flink_table_kaiwudb_sink.test_tb WHERE t1 < 5";
    int querySumResult = SqlHelper.querySumResult(querySumSql);
    Assertions.assertEquals(20, querySumResult);  
    
    System.out.println("Test flink table row source to sink finished!");
}

// Helper method to generate test data
private Table getInputTable(StreamTableEnvironment tableEnvironment) {
    List<Row> rowData = new ArrayList<>();
    ThreadLocalRandom random = ThreadLocalRandom.current(); 
    long tsTime = 1749625212123 L;  
    
    // Generate 10 test rows with 15-minute intervals
    for (int i = 0; i < 10; i++) {
        long timestamp = tsTime + (15 * 60 * 1000) * i;  
        Row row = Row.of(
            new Timestamp(timestamp),                   
            random.nextInt(10),                         
            random.nextInt(100),                        
            random.nextInt(1000),                       
            random.nextFloat(),                         
            random.nextDouble(),                        
            random.nextBoolean(),                       
            RandomStringUtils.randomAlphanumeric(1),    
            RandomStringUtils.randomAlphanumeric(10),   
            RandomStringUtils.randomAlphanumeric(10),   
            RandomStringUtils.randomAlphanumeric(10),   
            RandomStringUtils.randomAlphanumeric(10),
            new Timestamp(timestamp),                     
            (i / 2) + 1,                                 // Tag 1: calculated based on index (1,1,2,2,3,3...)
            "tianjin"                                    // Tag 2: fixed value
        );
        rowData.add(row);
    }
    
    // Create table from row data with schema definition
    return tableEnvironment.fromValues(
        DataTypes.ROW(
            DataTypes.FIELD("ts", DataTypes.TIMESTAMP(6)),      
            DataTypes.FIELD("c1", DataTypes.INT()),             
            DataTypes.FIELD("c2", DataTypes.INT()),             
            DataTypes.FIELD("c3", DataTypes.INT()),             
            DataTypes.FIELD("c4", DataTypes.FLOAT()),           
            DataTypes.FIELD("c5", DataTypes.DOUBLE()),          
            DataTypes.FIELD("c6", DataTypes.BOOLEAN()),         
            DataTypes.FIELD("c7", DataTypes.CHAR(1)),           
            DataTypes.FIELD("c8", DataTypes.STRING()),          
            DataTypes.FIELD("c9", DataTypes.STRING()),          
            DataTypes.FIELD("c10", DataTypes.STRING()),         
            DataTypes.FIELD("c11", DataTypes.BYTES()),          
            DataTypes.FIELD("c12", DataTypes.TIMESTAMP(6)),     
            DataTypes.FIELD("t1", DataTypes.INT()),             
            DataTypes.FIELD("t2", DataTypes.STRING())           
        ),
        rowData  
    );
}
```

## Reference

### Data Type Mapping

The connector automatically converts between KWDB and Flink data types. The following tables show the supported type mappings for time-series and relational data.

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
| VARCHAR, NCHAR, NVARCHAR | String         | VARCHAR/STRING     |
| GEOMETRY               | String           | STRING             |

**Relational Data**

::: warning Note
The DECIMAL type must have both precision and scale values specified. DECIMAL types without these specifications are not supported.
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
| BIGINT, SERIAL           | Long             | BIGINT             |
| REAL                  | Float            | FLOAT              |
| DOUBLE                  | Double           | DOUBLE             |
| DECIMAL(p,s)            | BigDecimal       | DECIMAL(p,s)       |
| BIT, VARBIT              | String           | STRING             |
| BYTES, VARBYTES          | byte[]           | BYTES              |
| CHAR                    | String           | CHAR/STRING        |
| VARCHAR, NCHAR, NVARCHAR  | String           | VARCHAR/STRING     |
| JSON, JSONB, TEXT         | String           | STRING             |
| STRING[], STRING, COLLATE | String           | STRING             |
| INTERVAL, INET, UUID      | String           | STRING             |