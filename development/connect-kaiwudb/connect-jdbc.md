---
title: KaiwuDB JDBC
id: connect-jdbc
---

# JDBC 连接 KWDB 数据库

Java 数据库连接（Java Database Connectivity，JDBC）是 Java 应用程序访问数据库的标准 API。它提供一套完整的接口，允许 Java 应用程序与不同类型的数据库进行交互。KWDB 提供了 JDBC 驱动程序 KaiwuDB JDBC，支持 Java 应用程序与 KWDB 数据库交互，执行查询、插入、更新和删除等操作。JDBC 驱动程序在将 Java 数据类型发送到数据库之前，会将其转换为相应的 JDBC 类型。有关 Java 数据类型和 JDBC 数据类型对比转换的详细信息，参见[支持的数据类型](#支持的数据类型)。

KaiwuDB JDBC 是 KWDB 的官方 Java 语言连接器。它基于 PgJDBC 扩展实现，符合 JDBC 4.0、JDBC 4.1 和 JDBC 4.2 规范。Java 开发人员可以使用 KaiwuDB JDBC 驱动程序向 KWDB 的服务进程发送消息，访问任何形式的表格数据，操作流程如下：

1. 连接数据源并创建到数据库的连接。
2. 创建查询或更新指令。
3. 为数据库传递查询和更新指令。
4. 处理数据库响应并返回的结果。

## 前提条件

- [安装 Java](https://docs.oracle.com/en/java/javase/22/install/overview-jdk-installation.html)（1.8 及以上版本）。
- [安装 Maven](https://maven.apache.org/install.html)（3.6 及以上版本）。
- 安装 KWDB 数据库、配置数据库认证方式、创建数据库。
- 获取 KaiwuDB JDBC 驱动包。

## 配置连接

如需安装 KaiwuDB JDBC 连接器，遵循以下步骤。

1. 运行以下命令，将 KaiwuDB JDBC 安装到本地 Maven 仓库中。

   ```shell
   mvn install:install-file "-Dfile=../kaiwudb-jdbc.2.0.4.jar" "-DgroupId=com.kaiwudb" "-DartifactId=kaiwudb-jdbc" "-Dversion=2.0.4" "-Dpackaging=jar"
   ```

2. 在 `pom.xml` 中添加依赖，将 KaiwuDB JDBC 引入到 Java 应用程序中。

   ```xml
   <dependency>
     <groupId>com.kaiwudb</groupId>
     <artifactId>kaiwudb-jdbc</artifactId>
     <version>2.0.4</version>
   </dependency>
   ```

## 连接数据库

用户需要编写 Java 程序代码，连接数据库。Java 程序代码需要包含以下内容：

- Driver：由数据库厂家提供，处理与数据库服务器的通信。对于 KWDB，必须先加载 KWDB 数据库驱动程序类，加载方式如下：

  ```java
  Class.forName("com.kaiwudb.Driver");
  ```

- 数据库连接接口：通过 `DriverManager.getConnection()` 方法与 KWDB 数据库建立连接。KWDB 支持的连接方式如下：

  - `Connection conn = DriverManager.getConnection(url)`
  - `Connection conn = DriverManager.getConnection(url, props)`
  - `Connection conn = DriverManager.getConnection(url, user, password)`

**代码示例**

```java
public Connection getConnection() throws Exception{
  Class.forName("com.kaiwudb.Driver");
  Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=kwdbuser&password=123");
  return conn;
}
```

有关 KaiwuDB JDBC 连接方式和连接参数的详细信息，参见[连接方式](#连接方式)和[连接参数](#连接参数)。

## 配置示例

本节通过一些简单的示例展示如何使用 Java 应用程序进行数据库的 SQL 操作。如需了解更多 SQL 语句的使用，参见 [SQL 参考](../../sql-reference/overview.md)。

::: warning 说明
由于不同数据引擎对 JDBC 不同接口的支持有差异，在连接不同引擎后，部分接口的使用存在一些限制：

- 时序引擎不支持事务，在 `autoCommit` 参数设置为 `false` 时，不允许执行 `INSERT` 语句。
- 时序引擎不支持设置保存点、游标以及批量更新操作等功能。
- 关系和时序引擎均不支持用户创建、使用 SQLXML 对象。
- 关系和时序引擎均不支持用户设置可保持性级别参数（`Holdability`）。
- 关系和时序引擎均不支持存储过程功能。
- 关系和时序引擎均不支持执行 `EXPORT` 和 `IMPORT` 语句。

:::

### 创建、使用、删除数据库

:::warning 说明

- 如果未使用 `use <db_name>` 参数指定数据库，后续对表的操作都需要使用数据库名称作为前缀，例如 `ts_db.t1`。
- 目前，时序数据库名称不支持中文字符。

:::

```java
// 获取数据库连接
Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=kwdbuser&password=123");

// 创建statement
Statement stmt = conn.createStatement();

// 创建时序数据库
stmt.executeUpdate("create ts database ts_db");

// 使用数据库
stmt.executeUpdate("use ts_db");

// 删除数据库
stmt.executeUpdate("drop database ts_db cascade");
```

### 创建、删除表

:::warning 说明

- 在创建时序表时，第一列的数据类型必须为 timestamp 或 timestamptz 且不可为空值。
- 每张时序表需要设置至少一个主标签，且主标签必须为非空标签。
- 时序表名、列名和标签名暂不支持中文字符。

:::

```java
// 创建statement
Statement stmt = conn.createStatement();

// 创建时序表
stmt.executeUpdate("CREATE TABLE sensor_data (k_timestamp TIMESTAMPTZ NOT NULL, temperature FLOAT8 NOT NULL, humidity FLOAT8) TAGS (sensor_id INT4 NOT NULL, sensor_type INT4 NOT NULL) PRIMARY TAGS(sensor_id)");

// 删除时序表
stmt.executeUpdate("drop table ts_table");
```

### 写入数据

```java
// 创建statement
Statement stmt = conn.createStatement();

// 按照指定的列顺序插入数据
int rows1 = stmt.executeUpdate("insert into sensor_data (k_timestamp, temperature, humidity, sensor_id, sensor_type) values ('2023-07-20 16:12:12.123', 23.34, 55.20, 1,1)");
System.out.println("specify column name insert " + rows1 + " rows data.");

// 按照默认的列顺序插入数据
int rows2 = stmt.executeUpdate("insert into sensor_data values ('2023-07-20 16:12:12.123', 23.34, 55.20, 1,1)");
System.out.println("not specify column name insert " + rows2 + " rows data.");
```

### 查询数据

::: warning 说明
KWDB 支持使用下标或字段名获取数据。使用下标获取数据时，返回内容从 1 开始。建议使用字段名称获取数据。
:::

```java
// 创建statement
Statement stmt = conn.createStatement();

// 查询数据
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

## 错误码与异常处理

### 错误码

KaiwuDB JDBC 连接器的错误码分为两种：

- KaiwuDB JDBC Driver 本身的报错。有关详细信息，参见 [KaiwuDB JDBC Driver 错误码](../../db-operation/error-code/error-code-jdbc-driver.md)。
- KWDB 其它功能模块的报错。有关详细信息，参见 [KWDB 专有错误码](../../db-operation/error-code/error-code-kaiwudb.md)和 [PostgreSQL 错误码](../../db-operation/error-code/error-code-postgresql.md)。

### 异常处理

驱动程序和数据库都可能出现 SQLException 异常。出现 SQLException 异常时，异常对象将被传递到 `catch` 子句。用户可通过 `catch` 子句获取错误的消息和错误码等信息。SQLException 接口方法如下表所示：

| 方法                           | 描述                                                                                                                                                    |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `getErrorCode()`                 | 获取与异常关联的错误码，返回为 INT 类型值。                                                                                                             |
| `getMessage()`                   | - 获取 JDBC 驱动程序的错误信息，该错误由驱动程序处理。<br>- 获取数据库错误的错误码和错误信息。                                                        |
| `getSQLState()`                  | 获取 XOPEN SQLstate 字符串。对于 JDBC 驱动程序错误，此方法不返回任何有用信息。对于数据库错误，将返回五位数的 XOPEN SQLstate 代码。此方法可以返回 Null。 |
| `getNextException()`             | 获取异常链中的下一个 Exception 对象。                                                                                                                   |
| `printStackTrace()`              | 打印当前异常或可调用异常，并将其回溯到标准错误流。                                                                                                      |
| `printStackTrace(PrintStream s)` | 将可丢弃对象及其回溯，打印到指定的打印流。                                                                                                            |
| `printStackTrace(PrintWriter w)` | 打印一次性文件，并将其回溯到指定的打印编写器。                                                                                                      |

利用 SQLException 对象提供的信息，用户可以捕获异常并继续运行程序。以下是 `try .... catch ... finally` 代码块的一般格式：

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

## 参考信息

### 支持的数据类型

下表列出 Java 数据类型和 JDBC 数据类型的对比转换关系。

| SQL       | JDBC | 关系引擎支持 | 时序引擎支持 |
|-----------|-------------------------------------|-------------|-------------|
| BIT       | java.lang.Boolean                   | 是           | 否           |
| BOOL      | java.lang.Boolean                   | 是           | 是           |
| TIMESTAMP | java.sql.Timestamp                  | 是           | 是           |
| DATE      | java.sql.Date                       | 是           | 否           |
| TIME      | java.sql.Time                       | 是           | 否           |
| NUMERIC   | Java.math.BigDecimal                | 是           | 否           |
| INTEGER   | java.lang.Integer                   | 是           | 是           |
| BIGINT    | java.lang.Long                      | 是           | 是           |
| FLOAT     | java.lang.Float                     | 是           | 是           |
| DOUBLE    | java.lang.Double                    | 是           | 是           |
| SMALLINT  | java.lang.Short                     | 是           | 是           |
| TINYINT   | java.lang.Byte                      | 是           | 否           |
| REAL      | java.lang.Float                     | 是           | 是           |
| BYTES     | [B                                  | 是           | 是           |
| VARBYTES  | [B                                  | 是           | 是           |
| CHAR      | java.lang.String                    | 是           | 是           |
| NCHAR     | java.lang.String                    | 是           | 是           |
| VARCHAR   | java.lang.String                    | 是           | 是           |
| NVARCHAR  | java.lang.String                    | 是           | 是           |
| ARRAY     | java.sql.Array                      | 是           | 否           |
| BLOB      | java.sql.Blob                       | 是           | 否           |
| CLOB      | java.sql.Clob                       | 否           | 否           |

### 连接方式

KaiwuDB JDBC 支持通过 `DriverManager.getConnection()` 方法与 KWDB 数据库建立安全连接和非安全连接，包括：

- `Connection conn = DriverManager.getConnection(url)`：标准连接，通过 `url` 参数指定连接数据库所需的所有信息，包括数据库地址、端口、名称、用户名和密码。
- `Connection conn = DriverManager.getConnection(url, user, password)`：带用户名和密码的连接，通过 `url` 参数指定数据库地址、端口和名称。通过 `user` 和 `password` 参数指定用户名称和密码。
- `Connection conn = DriverManager.getConnection(url, props)`：带属性的连接，通过 `url` 参数指定数据库地址、端口和名称。通过 `props` 参数单独指定其它需要必要信息。

连接方式示例：

- 非安全模式下的标准连接

    ```java
    public Connection getConnection() throws Exception{
      Class.forName("com.kaiwudb.Driver");
      Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=kwdbuser&password=123");
      return conn;
    }
    ```

- 安全模式下的标准连接

    ```java
    public Connection getConnection() throws Exception{
      Class.forName("com.kaiwudb.Driver");
      Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=kwdbuser&password=123&sslmode=verify-ca&sslcert=../certs/client.kwdbuser.crt&sslkey=../certs/client.kwdbuser.pk8&sslrootcert=../certs/ca.crt");
      return conn;
    }
    ```

- 非安全模式下的带属性的连接

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

### 连接参数

下表列出驱动程序支持在连接 `url` 或 `props` 对象中指定的标准连接参数。

| 参数 | 默认值 | 说明 |
| --- | --- |---|
| `hostname` | null | KWDB 数据库的 IP 地址。|
| `port` | null | KWDB 数据库的连接端口。|
| `dbname` | null | 需要访问的数据库名称。|
| `user` | null | 连接数据库的用户名。|
| `password` | null | 身份验证时使用的密码。安全模式下，优先使用 SSL 证书进行登录认证。|

除标准连接参数之外，驱动程序还支持许多附加属性，用于指定附加驱动行为。下表列出驱动程序支持在连接 `url` 或 `props` 对象中指定的其他参数。

| 参数                | 默认值              | 说明                                                                                 |
| ------------------- | ------------------- | ------------------------------------------------------------------------------------ |
| `user`                | null                | 连接数据库的用户名。                                                                 |
| `password`            | null                | 身份验证时使用的密码。安全模式下，优先使用 SSL 证书进行登录认证。                    |
| `ssl`                 | null                | 使用 SSL 连接，服务器必须使用 SSL 进行编译。                                         |
| `sslmode`             | null                | SSL 模式，支持的取值包括 `disable`、`allow`、`prefer`、`require`、`verify-ca` 和 `verify-full`。有关 SSL 模式参数的详细信息，参见 [SSL 模式参数](#ssl-模式参数)。 |
| `sslcert`             | null                | 客户端 SSL 证书的存放位置。                                                              |
| `sslkey`              | null                | 客户端 `pkcs#8` SSL 密钥的存放位置。                                                       |
| `sslrootcert`         | null                | 用于验证服务器身份的根证书的存放位置。                                                   |
| `ApplicationName`     | `KaiwuDB JDBC Driver` | 应用名称。                                                                           |
| `tcpKeepAlive`        | `false`             | 开启或禁用 TCP 保持连接功能。                                                        |
| `loginTimeout`        | `0`                 | 指定等待建立数据库连接的时间（单位：秒）。                                        |
| `connectTimeout`      | `10`                | 用于 Socket 连接操作的超时值（单位：秒）。取值为 `0` 时，表示禁用。               |
| `socketTimeout`       | `0`                 | 用于 Socket 读操作的超时值（单位：秒）。取值为 `0` 时，表示禁用。                 |
| `cancelSignalTimeout` | `10`                | 发送 `cancel` 命令的超时时间（单位：秒）。                                        |
| `readOnly`            | `false`             | 配置连接模式为只读模式。                                                             |

### SSL 模式参数

安全模式下，JDBC 支持多种连接认证。通过 `sslmode` 连接参数，用户可以进一步控制 SSL 连接。

| 参数     | 窃听保护 | MITM 保护        | 说明                                                                                 | 是否支持 |
| ----------- | -------- | ---------------- | ------------------------------------------------------------------------------------ | -------- |
| `disable`     | 否       | 否               | 不使用加密连接。                                                                       | 是       |
| `allow`       | 可能     | 否               | 从非加密连接开始，然后尝试加密连接。                                                   | 是       |
| `prefer`      | 可能     | 否               | （默认选项）从加密连接开始，回退到非加密连接。                                                 | 是       |
| `require`     | 是       | 否               | 确保已加密连接。                                                                       | 是       |
| `verify-ca`   | 是       | 取决于 CA 的政策 | 确保已加密连接，并且客户端信任服务器证书。                                           | 是       |
| `verify-full` | 是       | 是               | 确保已加密连接，客户端信任服务器证书，并且服务器主机名与服务器证书列出的主机名匹配。 | 否       |

### 故障诊断与排查

有关详细信息，参见 [KaiwuDB JDBC 故障排查](../../troubleshooting-guide/troubleshooting.md#kaiwudb-jdbc)。
