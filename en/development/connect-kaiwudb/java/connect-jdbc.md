---
title: KaiwuDB JDBC
id: connect-jdbc
---

# Connect to KWDB using JDBC

Java Database Connectivity (JDBC) is the standard API for accessing databases in Java applications. It provides a comprehensive set of interfaces that enable Java applications to interact with various database types.

KWDB offers a JDBC driver that allows Java applications to connect to KWDB instances and perform operations such as querying, inserting, updating, and deleting data. The driver handles the conversion of Java data types to their corresponding JDBC types before sending them to the database. For more information on data type conversions, see [Supported Data Types](#supported-data-types).

KaiwuDB JDBC driver is the official Java connector for KWDB. Built on the PgJDBC extension, it complies with JDBC 4.0, 4.1, and 4.2 specifications. Java developers can use this driver to communicate with KWDB and access tabular data. The operation process is as follows:

1. Connect to the data source and establish a database connection
2. Create query or update commands
3. Execute these commands on the database
4. Process the database's response and handle the results

## Prerequisites

- [OpenJDK 1.8 or higher]((https://openjdk.org/install/)) installed
- [Maven 3.6 or higher](https://maven.apache.org/install.html) installed
- KaiwuDB JDBC driver package obtained
- KWDB installed and running with:
  - Properly configured database authentication
  - A database created for your connection
  - A user with appropriate privileges on tables or higher

## Configuring the Connection

1. Add the dependency in your `pom.xml` to include the KaiwuDB JDBC driver in your Java application:

   ```xml
   <dependency>
     <groupId>com.kaiwudb</groupId>
     <artifactId>kaiwudb-jdbc</artifactId>
     <version>3.1.0</version>
   </dependency>
   ```

2. If the KaiwuDB JDBC dependency cannot be loaded, install the driver into your local Maven repository with the following command:

   ```shell
   mvn install:install-file "-Dfile=../kaiwudb-jdbc-3.1.0.jar" "-DgroupId=com.kaiwudb" "-DartifactId=kaiwudb-jdbc" "-Dversion=3.1.0" "-Dpackaging=jar"
   ```

## Connecting to the Database

### Connection Methods

To connect to the database, your Java code needs to include the following components:

- **Driver**: Provided by the database vendor, it handles communication with the database server. For KWDB, load the KaiwuDB driver class:

  ```java
  Class.forName("com.kaiwudb.Driver");
  ```

- **Database Connection Interface**: Use `DriverManager.getConnection()` to establish a connection to KWDB. The supported connection methods are:

  - **Standard URL connection**

    `Connection conn = DriverManager.getConnection(url)`: Specifies all required connection details in the URL, including address, port, database name, username, and password. For supported URL parameters, see [URL Parameters](#url-parameters).

  - **Connection with username and password**

    `Connection conn = DriverManager.getConnection(url, user, password)`: Specifies the database address, port, and name in the `url` parameter, and authentication credentials separately.

  - **Connection with properties**

    `Connection conn = DriverManager.getConnection(url, props)`: Specifies database details in the `url` parameter and additional properties in the `props` parameter. For supported property parameters, see [URL Parameters](#url-parameters) and [Property Parameters](#property-parameters).

### Connection Parameters

#### URL Parameters

The table below lists the standard connection parameters that can be specified in `url` or `props`.

| Parameter  | Default | Description                                  |
| ---------- | ------- | -------------------------------------------- |
| `hostname` | null    | IP address of the KWDB database           |
| `port`     | null    | Port for connecting to the KWDB database  |
| `dbname`   | null    | Name of the database to be accessed          |
| `user`     | null    | Username for connecting to the database      |
| `password` | null    | Password for connecting to the database      |

#### Property Parameters

In addition to the standard connection parameters, the driver supports many additional properties to control behavior. The following table lists these parameters, which that can be specified in `url` or `props`.

| Parameter                  | Default               | Description                                                  |
| -------------------------- | --------------------- | ------------------------------------------------------------ |
| `user`                     | null                  | Username for connecting to the database                      |
| `password`                 | null                  | Password for connecting to the database                      |
| `ssl`                      | null                  | Use SSL for connection; the server must support SSL          |
| `sslmode`                  | null                  | SSL mode options: `disable`, `allow`, `prefer`, `require`, `verify-ca`, and `verify-full`. See [SSL Mode Parameters](#ssl-mode-parameters) for more information |
| `sslcert`                  | null                  | Path to the client TLS certificate                   |
| `sslkey`                   | null                  | Path to the client `pkcs#8` format TLS private key   |
| `sslrootcert`              | null                  | Path to the TLS root certificate                     |
| `ApplicationName`          | `KaiwuDB JDBC Driver` | Application name                                             |
| `tcpKeepAlive`             | `false`               | Enable or disable TCP keep-alive                             |
| `loginTimeout`             | `0`                   | Time (in seconds) to wait for the database connection        |
| `connectTimeout`           | `10`                  | Socket connection timeout (in seconds). A value of `0` disables it |
| `socketTimeout`            | `0`                   | Socket read timeout (in seconds). A value of `0` disables it |
| `cancelSignalTimeout`      | `10`                  | Timeout for sending `cancel` commands (in seconds)           |
| `readOnly`                 | `false`               | Set connection mode to read-only                             |
| `preferQueryMode`          | `extended`            | Query execution mode. Supported values include: `simple`, `extended`, `extendedForPrepared`, and `extendedCacheEverything`.<br><br>**Note**: When using `setXXX()` methods in `PreparedStatement` objects (e.g., `setBytes(int i, byte[] value)`), `preferQueryMode` must use the default value `extended` and cannot be set to `simple` |

#### SSL Mode Parameters

In secure mode, JDBC supports multiple authentication methods via the `sslmode` parameter.

| Parameter     | Encryption Protection | MITM Protection      | Description                                                  | Supported |
| ------------- | --------------------- | -------------------- | ------------------------------------------------------------ | --------- |
| `disable`     | No                    | No                   | Do not use encrypted connections                             | Yes       |
| `allow`       | Possible              | No                   | Attempt encryption after a non-encrypted connection          | Yes       |
| `prefer`      | Possible              | No                   | (Default) Prefer encrypted connection, but fall back to non-encrypted | Yes       |
| `require`     | Yes                   | No                   | Ensure the connection is encrypted                           | Yes       |
| `verify-ca`   | Yes                   | Depends on CA policy | Ensure the connection is encrypted and trusted by the server's certificate | Yes       |
| `verify-full` | Yes                   | Yes                  | Ensure the connection is encrypted, the server's certificate is trusted, and the hostname matches the certificate | No        |

### Connection Examples

#### Non-Secure Connection

- **URL Connection**

  The following example uses the `url` parameter to connect to the database:

    ```java
    public Connection getConnection() throws Exception{
      Class.forName("com.kaiwudb.Driver");
      Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=kwdbuser&password=123");
      return conn;
    }
    ```

- **Connection with Properties**

  The following example uses property parameters to connect to the database:

    ```java
    public Connection getConnection() throws Exception{
      Class.forName("com.kaiwudb.Driver");
      String jdbcUrl= "jdbc:kaiwudb://127.0.0.1:26257/defaultdb";
      Properties props = newProperties();
      props.setProperty("user", "kwdbuser");
      props.setProperty("password", "123");
      Connection conn = DriverManager.getConnection(jdbcUrl, props);
      return conn;
    }
    ```

#### TLS Secure Connection

The following example uses the `url` parameter with TLS parameters to connect securely:

```java
public Connection getConnection() throws Exception{
  Class.forName("com.kaiwudb.Driver");
  Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=kwdbuser&password=123&sslmode=verify-ca&sslcert=../certs/client.kwdbuser.crt&sslkey=../certs/client.kwdbuser.pk8&sslrootcert=../certs/ca.crt");
  return conn;
}
```

## Configuration Examples

This section provides examples demonstrating how to perform SQL operations on a KWDB database using Java applications. For more information on SQL statements, see [SQL Reference](../../../sql-reference/overview.md).

::: warning Note
Due to differences in JDBC interface support across various data engines, some interfaces have limitations:

- The time series engine does not support transactions. When `autoCommit` is set to `false`, `INSERT` statements are not allowed.
- The time series engine does not support savepoints, cursors, or batch update operations.
- Both relational and time series engines do not support:
  - Creation or use of SQLXML objects
  - Setting the `Holdability` parameter
  - Stored procedures
  - Executing `EXPORT` and `IMPORT` statements

:::

### Create, Use, and Delete Databases

::: warning Note

If the `use <db_name>` statement is not executed to specify the database, subsequent table operations must include the database name as a prefix, such as `ts_db.t1`.

:::

```java
// Get database connection
Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=kwdbuser&password=123");

// Create statement
Statement stmt = conn.createStatement();

// Create time series database
stmt.executeUpdate("create ts database ts_db");

// Use database
stmt.executeUpdate("use ts_db");

// Delete database
stmt.executeUpdate("drop database ts_db cascade");
```

### Create and Delete Tables

::: warning Note

- When creating time series tables, the first column must be of type `timestamp` or `timestamptz` and cannot be null.
- Each time series table must have at least one primary tag, and the primary tag must not be null.

:::

```java
// Create statement
Statement stmt = conn.createStatement();

// Create time series table
stmt.executeUpdate("CREATE TABLE sensor_data (k_timestamp TIMESTAMPTZ NOT NULL, temperature FLOAT8 NOT NULL, humidity FLOAT8) TAGS (sensor_id INT4 NOT NULL, sensor_type INT4 NOT NULL) PRIMARY TAGS(sensor_id)");

// Delete time series table
stmt.executeUpdate("drop table ts_table");
```

### Insert Data

```java
// Create statement
Statement stmt = conn.createStatement();

// Insert data by specifying column names
int rows1 = stmt.executeUpdate("insert into sensor_data (k_timestamp, temperature, humidity, sensor_id, sensor_type) values ('2023-07-20 16:12:12.123', 23.34, 55.20, 1,1)");
System.out.println("specify column name insert " + rows1 + " rows data.");

// Insert data by default column order
int rows2 = stmt.executeUpdate("insert into sensor_data values ('2023-07-20 16:12:12.123', 23.34, 55.20, 1,1)");
System.out.println("not specify column name insert " + rows2 + " rows data.");
```

### Query Data

::: warning Note
KWDB supports retrieving data by index or field name. When using index, data retrieval starts at 1. It is recommended to use field names for data retrieval.
:::

```java
// Create statement
Statement stmt = conn.createStatement();

// Query data
ResultSet resultSet = stmt.executeQuery("select k_timestamp as ts, temperature, humidity from sensor_data");

Timestamp ts = null;
float temperature = 0;
float humidity = 0;

while(resultSet.next()){
  ts = resultSet.getTimestamp(1);
  temperature = resultSet.getFloat(2);
  humidity = resultSet.getFloat(3);
  System.out.printf("%s, %s, %s\n", ts, temperature, humidity);
}
```

## References

### Supported Data Types

The following table lists the mapping between SQL and JDBC data types:

| SQL       | JDBC | Relational Engine | Time Series Engine |
|-----------|-------------------------------------|---------------------------|---------------------------|
| BIT       | java.lang.Boolean                   | Yes                       | No                        |
| BOOL      | java.lang.Boolean                   | Yes                       | Yes                       |
| TIMESTAMP | java.sql.Timestamp                  | Yes                       | Yes                       |
| DATE      | java.sql.Date                       | Yes                       | No                        |
| TIME      | java.sql.Time                       | Yes                       | No                        |
| NUMERIC   | Java.math.BigDecimal                | Yes                       | No                        |
| INTEGER   | java.lang.Integer                   | Yes                       | Yes                       |
| BIGINT    | java.lang.Long                      | Yes                       | Yes                       |
| FLOAT     | java.lang.Float                     | Yes                       | Yes                       |
| DOUBLE    | java.lang.Double                    | Yes                       | Yes                       |
| SMALLINT  | java.lang.Short                     | Yes                       | Yes                       |
| TINYINT   | java.lang.Byte                      | Yes                       | No                        |
| REAL      | java.lang.Float                     | Yes                       | Yes                       |
| BYTES     | [B                                  | Yes                       | Yes                       |
| VARBYTES  | [B                                  | Yes                       | Yes                       |
| CHAR      | java.lang.String                    | Yes                       | Yes                       |
| NCHAR     | java.lang.String                    | Yes                       | Yes                       |
| VARCHAR   | java.lang.String                    | Yes                       | Yes                       |
| NVARCHAR  | java.lang.String                    | Yes                       | Yes                       |
| ARRAY     | java.sql.Array                      | Yes                       | No                        |
| BLOB      | java.sql.Blob                       | Yes                       | No                        |
| CLOB      | java.sql.Clob                       | No                        | No                        |

### Exception Handling

Both the driver and the database may raise `SQLException` exceptions. When a `SQLException` occurs, the exception object is passed to the `catch` clause. Users can access error messages and error codes through this object. The following table shows the methods available for `SQLException`:

| Method                           | Description                                                                                                     |
|----------------------------------|-----------------------------------------------------------------------------------------------------------------|
| `getErrorCode()`                 | Gets the error code associated with the exception as an integer value                                           |
| `getMessage()`                   | Gets the error message from the JDBC driver or the database (includes error code and message)                   |
| `getSQLState()`                  | Gets the XOPEN SQLstate string (five-digit code for database errors, may return no useful information for driver errors)                           |
| `getNextException()`             | Gets the next Exception object in the exception chain                                                           |
| `printStackTrace()`              | Prints the current exception or a throwable exception and traces it to the standard error stream                                                                                                      |
| `printStackTrace(PrintStream s)` | Prints the throwable exception and its stack trace to the specified print stream                                                                                                            |
| `printStackTrace(PrintWriter w)` | Prints the exception and its stack trace to the specified print writer                                                                                                      |

Using the information provided by the `SQLException` object, you can catch exceptions and continue running your program. Here's the general format of a `try-catch-finally` block:

```java
**try** {
   // Your risky code goes between these curly braces.
} **catch**(SQLException e) {
   // Your exception handling code goes between these curly braces.
   // similar to the exception clause in a SQL block.
} **finally** {
   // Your must-always-be-executed code goes between these curly braces.
   // Like closing database connection.
}
```

### Bulk Insertion Interface

The KaiwuDB JDBC bulk insertion interface enables you to combine multiple data insertions into a single SQL statement for the same time series table, reducing CPU usage and significantly improving write performance. For configuration examples, see [Optimizing Bulk Data Insertion Using KaiwuDB JDBC Extended Interface](../../../best-practices/jdbc-batch.md).

### Error Codes

KaiwuDB JDBC connector error codes fall into two categories:

- Errors raised by the KaiwuDB JDBC Driver itself. For more information, see [KaiwuDB JDBC Driver Error Codes](../../../db-operation/error-code/error-code-jdbc-driver.md).
- Errors raised by other KWDB functional modules. For more information, see [KWDB Specific Error Codes](../../../db-operation/error-code/error-code-kaiwudb.md) and [PostgreSQL Error Codes](../../../db-operation/error-code/error-code-postgresql.md).

### Troubleshooting

For troubleshooting information, see [Troubleshooting KaiwuDB JDBC](../../../troubleshooting-guide/troubleshooting.md#kaiwudb-jdbc).