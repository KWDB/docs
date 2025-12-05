---
title: Using KaiwuDB JDBC Extended Interface to Optimize Batch Data Writing
id: jdbc-batch
---

# Using KaiwuDB JDBC Extended Interface to Optimize Batch Data Writing

KaiwuDB JDBC is the official Java connector for KWDB. Built as an extension of PgJDBC, it complies with JDBC 4.0, 4.1, and 4.2 specifications. Java developers can use the KaiwuDB JDBC driver to connect to KWDB service processes and perform create, read, update, and delete operations on data.

In addition to traditional batch SQL execution interfaces that support manual SQL concatenation, KaiwuDB JDBC provides specialized batch interfaces: `addBatchInsert`, `executeBatchInsert`, and `clearBatchInsert`. These interfaces can merge multiple writes to the same time-series table into a single SQL statement, reducing CPU usage and improving write performance.

When writing data with batch interfaces, KaiwuDB JDBC handles errors gracefully. If written values don't match column data types or if specified fields don't exist, the driver returns counts for both successfully written and failed records, and logs detailed error information. This document provides best practices for writing data using KaiwuDB JDBC batch interfaces.

::: warning Note

Currently, the batch write functionality is only available for the standalone version of KWDB.

:::

For more information, see:

- Database connection methods, basic usage, data types, and exception handling: [Connect to KWDB using JDBC](../development/connect-kaiwudb/java/connect-jdbc.md)
- Error codes: [KaiwuDB JDBC Driver Error Codes](../db-operation/error-code/error-code-jdbc-driver.md)
- Troubleshooting: [KaiwuDB JDBC Driver Troubleshooting](../troubleshooting-guide/troubleshooting.md#kaiwudb-jdbc)

## Prerequisites

- [OpenJDK 1.8 or higher]((https://openjdk.org/install/)) installed
- [Maven 3.6 or higher](https://maven.apache.org/install.html) installed
- KaiwuDB JDBC driver package obtained
- KWDB 2.1.0 or above installed and running with:
  - Properly configured database authentication
  - A database created for your connection
  - A user with appropriate privileges on tables or higher

## Configure Database

Users can configure the system to skip error data during writes and continue writing other data normally, thereby improving write performance.

```sql
SET SESSION ts_ignore_batcherror=true;
```

## Configure Connection

1. Add the KaiwuDB JDBC dependency to your `pom.xml` file:

   ```xml
   <dependency>
     <groupId>com.kaiwudb</groupId>
     <artifactId>kaiwudb-jdbc</artifactId>
     <version>2.2.0</version>
   </dependency>
   ```

2. If KaiwuDB JDBC cannot be loaded, install the driver to your local Maven repository using the following command:

   ```shell
   mvn install:install-file "-Dfile=../kaiwudb-jdbc-2.2.0.jar" "-DgroupId=com.kaiwudb" "-DartifactId=kaiwudb-jdbc" "-Dversion=2.2.0" "-Dpackaging=jar"
   ```

## Configuration Example

The following example demonstrates how to use KaiwuDB JDBC to batch write data from multiple devices to time-series tables.

1. Create time-series tables.

   This example creates ten time-series tables (`tbl_raw_1` through `tbl_raw_10`) for batch insertion of data from different devices. All tables share the same data structure:

   ```sql
   CREATE TABLE tsdb.tbl_raw_1 (ts TIMESTAMPTZ NOT NULL, data FLOAT8 NULL, type CHAR(10) NULL, parse VARCHAR NULL) TAGS (device CHAR(10) NOT NULL, iot_hub_name VARCHAR(64) NOT NULL) PRIMARY TAGS (device, iot_hub_name);

   CREATE TABLE tsdb.tbl_raw_2 (ts TIMESTAMPTZ NOT NULL, data FLOAT8 NULL, type CHAR(10) NULL, parse VARCHAR NULL) TAGS (device CHAR(10) NOT NULL, iot_hub_name VARCHAR(64) NOT NULL) PRIMARY TAGS (device, iot_hub_name);

   CREATE TABLE tsdb.tbl_raw_3 (ts TIMESTAMPTZ NOT NULL, data FLOAT8 NULL, type CHAR(10) NULL, parse VARCHAR NULL) TAGS (device CHAR(10) NOT NULL, iot_hub_name VARCHAR(64) NOT NULL) PRIMARY TAGS (device, iot_hub_name);

   CREATE TABLE tsdb.tbl_raw_4 (ts TIMESTAMPTZ NOT NULL, data FLOAT8 NULL, type CHAR(10) NULL, parse VARCHAR NULL) TAGS (device CHAR(10) NOT NULL, iot_hub_name VARCHAR(64) NOT NULL) PRIMARY TAGS (device, iot_hub_name);

   CREATE TABLE tsdb.tbl_raw_5 (ts TIMESTAMPTZ NOT NULL, data FLOAT8 NULL, type CHAR(10) NULL, parse VARCHAR NULL) TAGS (device CHAR(10) NOT NULL, iot_hub_name VARCHAR(64) NOT NULL) PRIMARY TAGS (device, iot_hub_name);

   CREATE TABLE tsdb.tbl_raw_6 (ts TIMESTAMPTZ NOT NULL, data FLOAT8 NULL, type CHAR(10) NULL, parse VARCHAR NULL) TAGS (device CHAR(10) NOT NULL, iot_hub_name VARCHAR(64) NOT NULL) PRIMARY TAGS (device, iot_hub_name);

   CREATE TABLE tsdb.tbl_raw_7 (ts TIMESTAMPTZ NOT NULL, data FLOAT8 NULL, type CHAR(10) NULL, parse VARCHAR NULL) TAGS (device CHAR(10) NOT NULL, iot_hub_name VARCHAR(64) NOT NULL) PRIMARY TAGS (device, iot_hub_name);

   CREATE TABLE tsdb.tbl_raw_8 (ts TIMESTAMPTZ NOT NULL, data FLOAT8 NULL, type CHAR(10) NULL, parse VARCHAR NULL) TAGS (device CHAR(10) NOT NULL, iot_hub_name VARCHAR(64) NOT NULL) PRIMARY TAGS (device, iot_hub_name);

   CREATE TABLE tsdb.tbl_raw_9 (ts TIMESTAMPTZ NOT NULL, data FLOAT8 NULL, type CHAR(10) NULL, parse VARCHAR NULL) TAGS (device CHAR(10) NOT NULL, iot_hub_name VARCHAR(64) NOT NULL) PRIMARY TAGS (device, iot_hub_name);

   CREATE TABLE tsdb.tbl_raw_10 (ts TIMESTAMPTZ NOT NULL, data FLOAT8 NULL, type CHAR(10) NULL, parse VARCHAR NULL) TAGS (device CHAR(10) NOT NULL, iot_hub_name VARCHAR(64) NOT NULL) PRIMARY TAGS (device, iot_hub_name);
   ```

2. Batch write data to time-series tables.

   This example loops 1,000 times, writing 1,000 rows per iteration for a total of 1 million rows. Each iteration inserts data for 20 devices with 50 rows per device:

   ```java
   public class BatchInsertTest {

   public static void main(String[] args) {
      String url = "jdbc:kaiwudb://127.0.0.1:26257/tsdb?preferQueryMode=simple";
      String user = "<user_name>";
      String password = "<password>";

      try (Connection connection = DriverManager.getConnection(url, user, password)) {
         KwStatement statement = (KwStatement) connection.createStatement();
         long timestamp = 1731373200000L; // Initial timestamp: 2024-11-12 09:00:00.000
         for (int i = 0; i < 1000; i++) {
         // Loop 1000 times, writing 1000 rows per iteration for a total of 1 million rows
         // Each iteration inserts data for 20 devices, with 50 rows per device
         for (int row = 1; row <= 50; row++) {
         int index = (row - 1) % 10 + 1;
            long finalTime = timestamp + (row * 1000L) + (i * 50 * 1000L);
            for (int num = 1; num <= 20; num++) {
               String device = "device_" + num;
               String iot = "iot_" + num;
               statement.addBatchInsert(finalTime, ("tbl_raw_" + index),
               new LinkedHashMap<String, Object>() {{
                  put("ts", finalTime);
                  put("data", ThreadLocalRandom.current().nextDouble());
                  put("type", "t_001");
                  put("parse", UUID.randomUUID() + "'123");
               }},
               new LinkedHashMap<String, Object>() {{
                  put("device", device);
                  put("iot_hub_name", iot);
               }});
            }
         }

         // Execute the batch insert
         statement.executeBatchInsert();

         // Clear temporary batch insert data
         statement.clearBatchInsert();
         }
         // Close the statement
         statement.colse();
      } catch (SQLException ex) {
         ex.printStackTrace();
      }
   }
   }
   ```
