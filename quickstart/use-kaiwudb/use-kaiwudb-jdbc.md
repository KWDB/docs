---
title: 使用 KaiwuDB JDBC 管理 KWDB
id: use-kaiwudb-jdbc
---

# 使用 KaiwuDB JDBC 管理 KWDB

安装部署完 KWDB 以后，用户可以使用 [KaiwuDB JDBC](../../development/connect-kaiwudb/java/connect-jdbc.md) 连接 KWDB 数据库，并创建数据库、管理数据库对象等。

## 时序数据

### 管理时序数据库

:::warning 说明

- 如未使用 `use <db_name>` 参数指定数据库，后续对表的操作都需要使用数据库名称作为前缀，例如 `ts_db.record`。
- 目前，时序数据库名称不支持中文字符。

:::

```java
// 获取数据库连接。
Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=root&password=123");

// 创建 statement。
Statement stmt = conn.createStatement();

// 创建 ts_db 时序数据库。
stmt.executeUpdate("create ts database ts_db");

// 使用 ts_db 时序数据库。
stmt.executeUpdate("use ts_db");

// 删除 ts_db 时序数据库。
stmt.executeUpdate("drop database ts_db");
```

### 管理时序表

:::warning 说明

- 在创建时序表时，第一列的数据类型必须为 timestamp 或 timestamptz，且不可为空值。
- 每张时序表设置至少一个主标签，且主标签必须为非空标签。
- 目前，时序表名、列名和标签名不支持中文字符。

:::

```java
// 创建 statement。
Statement stmt = conn.createStatement();

// 创建 record 时序表。
stmt.executeUpdate("CREATE TABLE record (RecordedTime timestamptz NOT NULL, Longitude float, Latitude float, EngineRPM int) TAGs (LicensePlate varchar(10) NOT NULL, VehicleColor varchar(10)) PRIMARY TAGS (LicensePlate)");

// 删除 record 时序表。
stmt.executeUpdate("drop table record");
```

### 写入数据

```java
// 创建 statement。
Statement stmt = conn.createStatement();

// 按照指定的列顺序向 record 表中写入数据。
int rows1 = stmt.executeUpdate("insert into record (RecordedTime, Longitude, Latitude, EngineRPM, LicensePlate, VehicleColor) values ('2024-06-06 10:00:00', 40.2, 116.2, 3000, '京A11111', '黑')");
System.out.println("specify column name insert " + rows1 + " rows data.");

// 按照默认的列顺序向 record 表中写入数据。
int rows2 = stmt.executeUpdate("insert into record values ('2024-06-06 10:00:01', 39.3, 116.1, 0, '京A22222', '白')");
System.out.println("not specify column name insert " + rows2 + " rows data.");
```

### 查询数据

::: warning 说明
KWDB 支持使用下标或字段名获取数据。使用下标获取数据时，返回内容从 1 开始。建议使用字段名称获取数据。
:::

```java
// 创建 statement。
Statement stmt = conn.createStatement();

// 查询 record 表数据。
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

## 关系数据

### 管理关系数据库

::: warning 说明
如未使用 `use <db_name>` 参数指定数据库，后续对表的操作都需要使用数据库名称作为前缀，例如 `rdb.vehicles`。
:::

```java
// 获取数据库连接。
Connection conn = DriverManager.getConnection("jdbc:kaiwudb://127.0.0.1:26257/defaultdb?user=root&password=123");

// 创建 statement。
Statement stmt = conn.createStatement();

// 创建 rdb 关系数据库。
stmt.executeUpdate("create database rdb");

// 使用 rdb 数据库。
stmt.executeUpdate("use rdb");

// 删除 rdb 数据库。
stmt.executeUpdate("drop database rdb");
```

### 管理关系表

```java
// 创建 statement。
Statement stmt = conn.createStatement();

// 创建 vehicles 关系表。
stmt.executeUpdate("CREATE TABLE vehicles (VehicleID int4, LicensePlate varchar(10), Owner varchar(10), Model varchar(50), Year int4)");

// 删除 vehicles 关系表。
stmt.executeUpdate("drop table vehicles");
```

### 写入数据

```java
// 创建 statement。
Statement stmt = conn.createStatement();

// 按照指定的列顺序向 vehicles 表中写入数据。 
int rows1 = stmt.executeUpdate("INSERT INTO vehicles (VehicleID, LicensePlate, Owner, Model, Year) VALUES (1, '京A11111', '李明', '奔驰', 2020)");
System.out.println("specify column name insert " + rows1 + " rows data.");

// 按照默认的列顺序向 vehicles 表中写入数据。
int rows2 = stmt.executeUpdate("INSERT INTO vehicles VALUES (2, '京A22222', '赵志', '别克', 2022)");
System.out.println("not specify column name insert " + rows2 + " rows data.");
```

### 查询数据

::: warning 说明
KWDB 支持使用下标或字段名获取数据。使用下标获取数据时，返回内容从 1 开始。建议使用字段名称获取数据。
:::

```java
// 创建 statement。
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
