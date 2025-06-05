---
title: Using the KaiwuDB JDBC Driver
id: use-kaiwudb-jdbc
---

# Manage KWDB Using the KaiwuDB JDBC Driver

This section explains how to use the [KaiwuDB JDBC Driver](../../development/connect-kaiwudb/java/connect-jdbc.md) to manage both time-series and relational data in KWDB. You'll learn how to create and manage databases and tables, and perform basic data operations.

## Time-Series Data

### Managing Time-Series Databases

```java
// Connect to KWDB
Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=root&password=123");

// Create a statement
Statement stmt = conn.createStatement();

// Create a hew time-series database
stmt.executeUpdate("CREATE TS DATABASE tsdb");

// Select the database for use
stmt.executeUpdate("USE tsdb");

// Drop the database
stmt.executeUpdate("DROP DATABASE tsdb");
```

::: warning Note

- Database names must be in English only.
- If a database is not explicitly selected using the `USE` statement, all table operations in that database must include the database name as a prefix (e.g., `tsdb.record`) to specify the target database.
:::

### Managing Time-Series Tables

```java
// Create a statement
Statement stmt = conn.createStatement();

// Create a time-series table named 'record'
stmt.executeUpdate("CREATE TABLE record (RecordedTime timestamptz NOT NULL, Longitude float, Latitude float, EngineRPM int) TAGS (LicensePlate varchar(10) NOT NULL, VehicleColor varchar(10)) PRIMARY TAGS (LicensePlate)");

// Drop the 'record' table
stmt.executeUpdate("DROP TABLE record");

```

::: warning Note

- The first column must be a `timestamp` or `timestamptz` and cannot be null.
- At least one primary tag is required and cannot be null.
- Table names, column names, and tag names must use English characters.

:::

### Inserting Time-Series Data

```java
// Create a statement
Statement stmt = conn.createStatement();

// Insert data into the 'record' table with specified column order
int rows1 = stmt.executeUpdate("insert into record (RecordedTime, Longitude, Latitude, EngineRPM, LicensePlate, VehicleColor) values ('2024-06-06 10:00:00', 40.2, 116.2, 3000, 'A11111', 'black')");
System.out.println("Inserted " + rows1 + " rows of data with specified column names.");

// Insert data into the 'record' table with default column order
int rows2 = stmt.executeUpdate("insert into record values ('2024-06-06 10:00:01', 39.3, 116.1, 0, 'A22222', 'white')");
System.out.println("Inserted " + rows2 + " rows of data with default column order.");
```

### Querying Time-Series Data

```java
// Create a statement
Statement stmt = conn.createStatement();

// Query data from the 'record' table
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

::: warning Note
KaiwuDB JDBC driver allows data retrieval by index or column name. It is recommended to use column names. When using indices, remember that they start at 1, not 0.
:::

## Relational Data

### Managing Relational Databases

```java
// Connect to KWDB
Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=root&password=123");

// Create a statement
Statement stmt = conn.createStatement();

// Create a relational database named 'rdb'
stmt.executeUpdate("CREATE DATABASE rdb");

// Switch to the 'rdb' database
stmt.executeUpdate("USE rdb");

// Drop the 'rdb' database
stmt.executeUpdate("DROP DATABASE rdb");
```

::: warning Note
When a database is not explicitly selected using the `USE` statement, table operations must include the database name as a prefix (e.g., `rdb.vehicles`) to specify the target database.
:::

### Managing Relational Tables

```java
// Create a statement
Statement stmt = conn.createStatement();

// Create a relational table named 'vehicles'
stmt.executeUpdate("CREATE TABLE vehicles (VehicleID int4, LicensePlate varchar(10), Owner varchar(10), Model varchar(50), Year int4)");

// Drop the 'vehicles' table
stmt.executeUpdate("DROP TABLE vehicles");
```

### Inserting Relational Data

```java
// Create a statement
Statement stmt = conn.createStatement();

// Insert data into the 'vehicles' table with specified column order
int rows1 = stmt.executeUpdate("INSERT INTO vehicles (VehicleID, LicensePlate, Owner, Model, Year) VALUES (1, 'A11111', 'Mark', 'Benz', 2020)");
System.out.println("Inserted " + rows1 + " rows of data with specified column names.");

// Insert data into the 'vehicles' table with default column order
int rows2 = stmt.executeUpdate("INSERT INTO vehicles VALUES (2, 'A22222', 'Mike', 'Buick', 2022)");
System.out.println("Inserted " + rows2 + " rows of data with default column order.");

```

### Querying Relational Data

```java
// Create a statement
Statement stmt = conn.createStatement();

// Query data from the 'vehicles' table
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

::: warning Note
KaiwuDB JDBC driver allows data retrieval by index or column name. It is recommended to use column names. When using indices, remember that they start at 1, not 0.
:::
