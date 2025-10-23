---
title: Using the KaiwuDB JDBC Driver
id: access-kaiwudb-jdbc
---

# Connect to KWDB Using the KaiwuDB JDBC Driver

This section explains how to connect to KWDB using the [KaiwuDB JDBC Driver](../../development/connect-kaiwudb/java/connect-jdbc.md) after KWDB is deployed and started.

## Install the KaiwuDB JDBC Driver

### Prerequisites

Before installing the KaiwuDB JDBC Driver, ensure you have the following:

- [openJDK](https://openjdk.org/install/): Version 1.8 or higher.
- [Maven](https://maven.apache.org/install.html): Version 3.6 or higher.
- KWDB: A deployed and running KWDB instance.
  - For bare-metal deployment, see [Deploy KWDB Using Bare-Metal Installation Package](../install-kaiwudb/quickstart-bare-metal.md).
  - For container-based deployment, see [Deploy KWDB Using YAML or Container Installation Package](../install-kaiwudb/quickstart-docker.md).
- KaiwuDB JDBC Driver: Downloaded and available.

### Steps

1. Add the following dependency to your `pom.xml` file to include the KaiwuDB JDBC Driver in your Java project:

   ```xml
   <dependency>
     <groupId>com.kaiwudb</groupId>
     <artifactId>kaiwudb-jdbc</artifactId>
     <version>2.2.0</version>
   </dependency>
   ```

2. If the dependency fails to load automatically, manually install the KaiwuDB JDBC Driver into your local Maven repository:

   ```shell
   mvn install:install-file "-Dfile=../kaiwudb-jdbc-2.2.0.jar" "-DgroupId=com.kaiwudb" "-DartifactId=kaiwudb-jdbc" "-Dversion=2.2.0" "-Dpackaging=jar"
   ```

## Connect to KWDB

To connect to KWDB, write Java code that includes the following components:

- **Driver**: The driver handles communication with the database server. Load the KaiwuDB driver class as follows:

  ```java
  Class.forName("com.kaiwudb.Driver");
  ```

- **Database Connection**: Use the `DriverManager.getConnection()` method to establish a connection. KWDB supports the following connection methods:

  - `Connection conn = DriverManager.getConnection(url)`
  - `Connection conn = DriverManager.getConnection(url, props)`
  - `Connection conn = DriverManager.getConnection(url, user, password)`

**Example**

The following example demonstrates how to establish a connection to KWDB:

```java
public Connection getConnection() throws Exception {
  Class.forName("com.kaiwudb.Driver");
  Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=kwdbuser&password=123");
  return conn;
}
```

For more information on connection methods and parameters, see [Connection Methods](../../development/connect-kaiwudb/java/connect-jdbc.md#connection-methods) and [Connection Parameters](../../development/connect-kaiwudb/java/connect-jdbc.md#connection-parameters).