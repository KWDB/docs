---
title: Using KaiwuDB JDBC
id: access-jdbc
---

# Using KaiwuDB JDBC

After deploying KWDB, use KaiwuDB JDBC to connect and manage the database. This guide shows how to access and manage KWDB using JDBC.

## Install KaiwuDB JDBC

### Prerequisites

- [openJDK](https://openjdk.org/install/): Version 1.8 or higher.
- [Maven](https://maven.apache.org/install.html): Version 3.6 or higher.
- KWDB installed and running
- KaiwuDB JDBC Driver: Downloaded and available.


### Steps

1. Add the following dependency to `pom.xml`:

   ```xml
   <dependency>
     <groupId>com.kaiwudb</groupId>
     <artifactId>kaiwudb-jdbc</artifactId>
     <version>3.1.0</version>
   </dependency>
   ```

2. If the dependency fails to load, install the driver manually to your local Maven repository:

   ```shell
   mvn install:install-file "-Dfile=../kaiwudb-jdbc-3.1.0.jar" "-DgroupId=com.kaiwudb" "-DartifactId=kaiwudb-jdbc" "-Dversion=3.1.0" "-Dpackaging=jar"
   ```

## Connect to KWDB

Write Java code to connect to the database:

- **Driver**: Load the KaiwuDB driver class to handle database communication:

  ```java
  Class.forName("com.kaiwudb.Driver");
  ```

- **Connection**: Use `DriverManager.getConnection()` to establish a connection. Supported methods:

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

For connection methods and parameters, see [Connection Methods](../../development/java/connect-jdbc.md#connection-methods) and [Connection Parameters](../../development/java/connect-jdbc.md#connection-parameters).

## Manage KWDB

This section demonstrates managing KWDB's multi-model database using JDBC:

- **Relational Data**: Static data like device information
- **Time-Series Data**: Dynamic data like sensor readings

### Time Series Data Operations

#### Manage Time Series Database

::: warning Note
- If you don't use `USE <db_name>` to specify the database, prefix table operations with the database name, e.g., `tsdb.record`.
- Time-series database names must use English characters.
:::

```java
// Get connection
Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=root&password=123");

// Create statement
Statement stmt = conn.createStatement();

// Create time-series database
stmt.executeUpdate("CREATE TS DATABASE tsdb");

// Use database
stmt.executeUpdate("USE tsdb");

// Drop database
stmt.executeUpdate("DROP DATABASE tsdb");
```

#### Manage Time Series Table

::: warning Note
- The first column must be `timestamp` or `timestamptz` and cannot be null.
- Each time-series table must have at least one primary tag, which must be non-null.
- Table names, column names, and tag names must use English characters.
:::

```java
// Create statement
Statement stmt = conn.createStatement();

// Create time-series table
stmt.executeUpdate("CREATE TABLE record (RecordedTime timestamptz NOT NULL, Longitude float, Latitude float, EngineRPM int) TAGS (LicensePlate varchar(10) NOT NULL, VehicleColor varchar(10)) PRIMARY TAGS (LicensePlate)");

// Drop the table
stmt.executeUpdate("DROP TABLE record");

```

#### Write Time Series Data

```java
// Create statement
Statement stmt = conn.createStatement();

// Insert data with specified column order
int rows1 = stmt.executeUpdate("insert into record (RecordedTime, Longitude, Latitude, EngineRPM, LicensePlate, VehicleColor) values ('2024-06-06 10:00:00', 40.2, 116.2, 3000, 'A11111', 'black')");
System.out.println("Inserted " + rows1 + " rows of data with specified column names.");

// Insert data with default column order
int rows2 = stmt.executeUpdate("insert into record values ('2024-06-06 10:00:01', 39.3, 116.1, 0, 'A22222', 'white')");
System.out.println("Inserted " + rows2 + " rows of data with default column order.");
```

#### Query Time Series Data

::: warning Note
KWDB supports accessing data by index or field name. Index access starts from 1. Field name access is recommended.
:::

```java
// Create statement
Statement stmt = conn.createStatement();

// Query data
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

#### Manage Relational Database

::: warning Note
If you don't use `USE <db_name>` to specify the database, prefix table operations with the database name, e.g., `rdb.vehicles`.
:::

```java
// Get connection
Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=root&password=123");

// Create statement
Statement stmt = conn.createStatement();

// Create relational database
stmt.executeUpdate("CREATE DATABASE rdb");

// Use database
stmt.executeUpdate("USE rdb");

// Drop database
stmt.executeUpdate("DROP DATABASE rdb");
```

#### Manage Relational Table

```java
// Create statement
Statement stmt = conn.createStatement();

// Create relational table
stmt.executeUpdate("CREATE TABLE vehicles (VehicleID int4, LicensePlate varchar(10), Owner varchar(10), Model varchar(50), Year int4)");

// Drop table
stmt.executeUpdate("DROP TABLE vehicles");
```

#### Write Relational Data

```java
// Create statement
Statement stmt = conn.createStatement();

// Insert with specified columns
int rows1 = stmt.executeUpdate("INSERT INTO vehicles (VehicleID, LicensePlate, Owner, Model, Year) VALUES (1, '京A11111', '李明', '奔驰', 2020)");
System.out.println("specify column name insert " + rows1 + " rows data.");

// Insert with default column order
int rows2 = stmt.executeUpdate("INSERT INTO vehicles VALUES (2, '京A22222', '赵志', '别克', 2022)");
System.out.println("not specify column name insert " + rows2 + " rows data.");
```

#### Query Relational Data

::: warning Note
KWDB supports accessing data by index or field name. Index access starts from 1. Field name access is recommended.
:::

```java
// Create statement
Statement stmt = conn.createStatement();

// Query data
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
