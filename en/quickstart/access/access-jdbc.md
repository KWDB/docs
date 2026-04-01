---
title: KaiwuDB JDBC
id: access-jdbc
---

# KaiwuDB JDBC

KaiwuDB JDBC driver is the official Java connector provided by KaiwuDB, supporting database operations such as querying, inserting, updating, and deleting.

This article describes how to use KaiwuDB JDBC to access and manage KWDB databases.

## Installing KaiwuDB JDBC

### Prerequisites

- [Install openJDK](https://openjdk.org/install/) (version 1.8 and above)
- [Install Maven](https://maven.apache.org/install.html) (version 3.6 and above)
- Install and start KWDB database
- Obtain KaiwuDB JDBC driver package

### Steps

1. Add dependency in `pom.xml` to introduce KaiwuDB JDBC into your Java application:

   ```xml
   <dependency>
     <groupId>com.kaiwudb</groupId>
     <artifactId>kaiwudb-jdbc</artifactId>
     <version>3.1.0</version>
   </dependency>
   ```

2. If the above dependency cannot be loaded normally, run the following command to install KaiwuDB JDBC driver to your local Maven repository:

   ```shell
   mvn install:install-file "-Dfile=../kaiwudb-jdbc-3.1.0.jar" "-DgroupId=com.kaiwudb" "-DartifactId=kaiwudb-jdbc" "-Dversion=3.1.0" "-Dpackaging=jar"
   ```

## Connecting to KWDB

Users need to write Java program code to connect to the database. Java program code needs to include the following:

- Driver: Provided by the database vendor, handles communication with the database server. For KWDB, the KWDB database driver class must be loaded first, as follows:

  ```java
  Class.forName("com.kaiwudb.Driver");
  ```

- Database connection interface: Establish connection to KWDB database through `DriverManager.getConnection()` method. KWDB supports the following connection methods:

  - `Connection conn = DriverManager.getConnection(url)`
  - `Connection conn = DriverManager.getConnection(url, props)`
  - `Connection conn = DriverManager.getConnection(url, user, password)`

**Code Example**

```java
public Connection getConnection() throws Exception{
  Class.forName("com.kaiwudb.Driver");
  Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=kwdbuser&password=123");
  return conn;
}
```

For details on KaiwuDB JDBC connection methods and connection parameters, see [Connection Methods](../../development/java/connect-jdbc.md#connection-methods) and [Connection Parameters](../../development/java/connect-jdbc.md#connection-parameters).

## Managing KWDB

This section demonstrates how to use KaiwuDB JDBC to manage KWDB's multi-model database, including:

- **Relational data operations**: Managing relatively static basic data, such as device information, user profiles, etc.
- **Time-series data operations**: Processing dynamic data that changes over time series, such as sensor readings, monitoring metrics, etc.

### Time-Series Data Operations

#### Managing Time-Series Databases

:::warning Note
- If `use <db_name>` is not used to specify the database, subsequent operations on tables need to use the database name as a prefix, for example `tsdb.record`.
- Currently, time-series database names do not support Chinese characters.
:::

```java
// Get database connection
Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=root&password=123");

// Create statement
Statement stmt = conn.createStatement();

// Create tsdb time-series database
stmt.executeUpdate("CREATE TS DATABASE tsdb");

// Use tsdb time-series database
stmt.executeUpdate("USE tsdb");

// Drop tsdb time-series database
stmt.executeUpdate("DROP DATABASE tsdb");
```

#### Managing Time-Series Tables

:::warning Note
- When creating time-series tables, the data type of the first column must be `timestamp` or `timestamptz`, and cannot be null.
- Each time-series table must have at least one primary tag, and the primary tag must be a non-null tag.
- Currently, time-series table names, column names, and tag names do not support Chinese characters.
:::

```java
// Create statement
Statement stmt = conn.createStatement();

// Create record time-series table
stmt.executeUpdate("CREATE TABLE record (RecordedTime timestamptz NOT NULL, Longitude float, Latitude float, EngineRPM int) TAGs (LicensePlate varchar(10) NOT NULL, VehicleColor varchar(10)) PRIMARY TAGS (LicensePlate)");

// Drop record time-series table
stmt.executeUpdate("DROP TABLE record");
```

#### Writing Time-Series Data

```java
// Create statement
Statement stmt = conn.createStatement();

// Write data to record table in specified column order
int rows1 = stmt.executeUpdate("insert into record (RecordedTime, Longitude, Latitude, EngineRPM, LicensePlate, VehicleColor) values ('2024-06-06 10:00:00', 40.2, 116.2, 3000, 'BJ-A11111', 'Black')");
System.out.println("specify column name insert " + rows1 + " rows data.");

// Write data to record table in default column order
int rows2 = stmt.executeUpdate("insert into record values ('2024-06-06 10:00:01', 39.3, 116.1, 0, 'BJ-A22222', 'White')");
System.out.println("not specify column name insert " + rows2 + " rows data.");
```

#### Querying Time-Series Data

::: warning Note
KWDB supports retrieving data using index or field name. When retrieving data using index, the return content starts from 1. It is recommended to use field names to retrieve data.
:::

```java
// Create statement
Statement stmt = conn.createStatement();

// Query record table data
ResultSet resultSet = stmt.executeQuery("select RecordedTime as ts, LicensePlate, VehicleColor from record");

Timestamp ts = null;
String LicensePlate = null;
String VehicleColor = null;

while(resultSet.next()){
    ts = resultSet.getTimestamp(1);
    LicensePlate = resultSet.getString("LicensePlate");
    VehicleColor = resultSet.getString("VehicleColor");
    System.out.printf("%s, %s, %s\n", ts, LicensePlate, VehicleColor);
}
```

### Relational Data Operations

#### Managing Relational Databases

::: warning Note
If `use <db_name>` is not used to specify the database, subsequent operations on tables need to use the database name as a prefix, for example `rdb.vehicles`.
:::

```java
// Get database connection
Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=root&password=123");

// Create statement
Statement stmt = conn.createStatement();

// Create rdb relational database
stmt.executeUpdate("CREATE DATABASE rdb");

// Use rdb database
stmt.executeUpdate("USE rdb");

// Drop rdb database
stmt.executeUpdate("DROP DATABASE rdb");
```

#### Managing Relational Tables

```java
// Create statement
Statement stmt = conn.createStatement();

// Create vehicles relational table
stmt.executeUpdate("CREATE TABLE vehicles (VehicleID int4, LicensePlate varchar(10), Owner varchar(10), Model varchar(50), Year int4)");

// Drop vehicles relational table
stmt.executeUpdate("DROP TABLE vehicles");
```

#### Writing Relational Data

```java
// Create statement
Statement stmt = conn.createStatement();

// Write data to vehicles table in specified column order
int rows1 = stmt.executeUpdate("INSERT INTO vehicles (VehicleID, LicensePlate, Owner, Model, Year) VALUES (1, 'BJ-A11111', 'Li Ming', 'Mercedes', 2020)");
System.out.println("specify column name insert " + rows1 + " rows data.");

// Write data to vehicles table in default column order
int rows2 = stmt.executeUpdate("INSERT INTO vehicles VALUES (2, 'BJ-A22222', 'Zhao Zhi', 'Buick', 2022)");
System.out.println("not specify column name insert " + rows2 + " rows data.");
```

#### Querying Relational Data

::: warning Note
KWDB supports retrieving data using index or field name. When retrieving data using index, the return content starts from 1. It is recommended to use field names to retrieve data.
:::

```java
// Create statement
Statement stmt = conn.createStatement();

// Query vehicles table data
ResultSet resultSet = stmt.executeQuery("select LicensePlate, Owner, Model from vehicles");

String LicensePlate = null;
String Owner = null;
String Model = null;

while(resultSet.next()){
    LicensePlate = resultSet.getString("LicensePlate");
    Owner = resultSet.getString("Owner");
    Model = resultSet.getString("Model");
    System.out.printf("%s, %s, %s\n", LicensePlate, Owner, Model);
}
```
