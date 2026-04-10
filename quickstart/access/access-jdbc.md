---
title: KaiwuDB JDBC
id: access-jdbc
---

# KaiwuDB JDBC

KaiwuDB JDBC 驱动程序是 KWDB 官方提供的 Java 连接器，支持执行查询、插入、更新和删除等数据库操作。

本文介绍如何使用 KaiwuDB JDBC 访问和管理 KWDB 数据库。

## 安装 KaiwuDB JDBC

### 前提条件

- [安装 openJDK](https://openjdk.org/install/)（1.8 及以上版本）
- [安装 Maven](https://maven.apache.org/install.html)（3.6 及以上版本）
- 安装和启动 KWDB 数据库
- 获取 KaiwuDB JDBC 驱动包

### 步骤

1. 在 `pom.xml` 中添加依赖，将 KaiwuDB JDBC 引入到 Java 应用程序中：

   ```xml
   <dependency>
     <groupId>com.kaiwudb</groupId>
     <artifactId>kaiwudb-jdbc</artifactId>
     <version>3.1.0</version>
   </dependency>
   ```

2. 如果上述依赖无法正常加载使用，运行以下命令，将 KaiwuDB JDBC 驱动安装到本地 Maven 仓库中：

   ```shell
   mvn install:install-file "-Dfile=../kaiwudb-jdbc-3.1.0.jar" "-DgroupId=com.kaiwudb" "-DartifactId=kaiwudb-jdbc" "-Dversion=3.1.0" "-Dpackaging=jar"
   ```

## 连接 KWDB

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

有关 KaiwuDB JDBC 连接方式和连接参数的详细信息，参见[连接方式](../../development/java/connect-jdbc.md#连接方式)和[连接参数](../../development/java/connect-jdbc.md#连接参数)。

## 管理 KWDB

本节演示如何使用 KaiwuDB JDBC 管理 KWDB 多模数据库，具体包括：

- **关系数据操作**：管理相对静态的基础数据，如设备信息、用户档案等
- **时序数据操作**：处理按时间序列变化的动态数据，如传感器读数、监控指标等

### 时序数据操作

#### 管理时序数据库

:::warning 说明
- 如未使用 `use <db_name>` 指定数据库，后续对表的操作都需要使用数据库名称作为前缀，例如 `tsdb.record`。
- 目前，时序数据库名称不支持中文字符。
:::

```java
// 获取数据库连接
Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=root&password=123");

// 创建 statement
Statement stmt = conn.createStatement();

// 创建 tsdb 时序数据库
stmt.executeUpdate("CREATE TS DATABASE tsdb");

// 使用 tsdb 时序数据库
stmt.executeUpdate("USE tsdb");

// 删除 tsdb 时序数据库
stmt.executeUpdate("DROP DATABASE tsdb");
```

#### 管理时序表

:::warning 说明
- 在创建时序表时，第一列的数据类型必须为 `timestamp` 或 `timestamptz`，且不可为空值。
- 每张时序表设置至少一个主标签，且主标签必须为非空标签。
- 目前，时序表名、列名和标签名不支持中文字符。
:::

```java
// 创建 statement
Statement stmt = conn.createStatement();

// 创建 record 时序表
stmt.executeUpdate("CREATE TABLE record (RecordedTime timestamptz NOT NULL, Longitude float, Latitude float, EngineRPM int) TAGs (LicensePlate varchar(10) NOT NULL, VehicleColor varchar(10)) PRIMARY TAGS (LicensePlate)");

// 删除 record 时序表
stmt.executeUpdate("DROP TABLE record");
```

#### 写入时序数据

```java
// 创建 statement
Statement stmt = conn.createStatement();

// 按照指定的列顺序向 record 表中写入数据
int rows1 = stmt.executeUpdate("insert into record (RecordedTime, Longitude, Latitude, EngineRPM, LicensePlate, VehicleColor) values ('2024-06-06 10:00:00', 40.2, 116.2, 3000, '京A11111', '黑')");
System.out.println("specify column name insert " + rows1 + " rows data.");

// 按照默认的列顺序向 record 表中写入数据
int rows2 = stmt.executeUpdate("insert into record values ('2024-06-06 10:00:01', 39.3, 116.1, 0, '京A22222', '白')");
System.out.println("not specify column name insert " + rows2 + " rows data.");
```

#### 查询时序数据

::: warning 说明
KWDB 支持使用下标或字段名获取数据。使用下标获取数据时，返回内容从 1 开始。建议使用字段名称获取数据。
:::

```java
// 创建 statement
Statement stmt = conn.createStatement();

// 查询 record 表数据
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

### 关系数据操作

#### 管理关系数据库

::: warning 说明
如未使用 `use <db_name>` 指定数据库，后续对表的操作都需要使用数据库名称作为前缀，例如 `rdb.vehicles`。
:::

```java
// 获取数据库连接
Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=root&password=123");

// 创建 statement
Statement stmt = conn.createStatement();

// 创建 rdb 关系数据库
stmt.executeUpdate("CREATE DATABASE rdb");

// 使用 rdb 数据库
stmt.executeUpdate("USE rdb");

// 删除 rdb 数据库
stmt.executeUpdate("DROP DATABASE rdb");
```

#### 管理关系表

```java
// 创建 statement
Statement stmt = conn.createStatement();

// 创建 vehicles 关系表
stmt.executeUpdate("CREATE TABLE vehicles (VehicleID int4, LicensePlate varchar(10), Owner varchar(10), Model varchar(50), Year int4)");

// 删除 vehicles 关系表
stmt.executeUpdate("DROP TABLE vehicles");
```

#### 写入关系数据

```java
// 创建 statement
Statement stmt = conn.createStatement();

// 按照指定的列顺序向 vehicles 表中写入数据 
int rows1 = stmt.executeUpdate("INSERT INTO vehicles (VehicleID, LicensePlate, Owner, Model, Year) VALUES (1, '京A11111', '李明', '奔驰', 2020)");
System.out.println("specify column name insert " + rows1 + " rows data.");

// 按照默认的列顺序向 vehicles 表中写入数据
int rows2 = stmt.executeUpdate("INSERT INTO vehicles VALUES (2, '京A22222', '赵志', '别克', 2022)");
System.out.println("not specify column name insert " + rows2 + " rows data.");
```

#### 查询关系数据

::: warning 说明
KWDB 支持使用下标或字段名获取数据。使用下标获取数据时，返回内容从 1 开始。建议使用字段名称获取数据。
:::

```java
// 创建 statement
Statement stmt = conn.createStatement();

// 查询 vehicles 表数据
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
