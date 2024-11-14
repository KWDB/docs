---
title: 使用 KaiwuDB JDBC 连接 KWDB
id: access-kaiwudb-jdbc
---

# 使用 KaiwuDB JDBC 连接 KWDB

安装部署完 KWDB 以后，用户可以使用 [KaiwuDB JDBC](../../development/connect-kaiwudb/java/connect-jdbc.md) 连接和管理 KWDB。本文介绍如何使用 KaiwuDB JDBC 访问 KWDB 数据库。

## 安装 KaiwuDB JDBC

## 前提条件

- [安装 openJDK](https://openjdk.org/install/)（1.8 及以上版本）。
- [安装 Maven](https://maven.apache.org/install.html)（3.6 及以上版本）。
- 安装 KWDB 数据库、配置数据库认证方式、创建数据库。
- 创建具有表级别及以上操作权限的用户。
- 获取 KaiwuDB JDBC 驱动包。

## 配置连接

1. 在 `pom.xml` 中添加依赖，将 KaiwuDB JDBC 引入到 Java 应用程序中。

   ```xml
   <dependency>
     <groupId>com.kaiwudb</groupId>
     <artifactId>kaiwudb-jdbc</artifactId>
     <version>2.0.4.1</version>
   </dependency>
   ```

2. 如上述依赖无法正常加载使用，运行以下命令，将 KaiwuDB JDBC 驱动安装到本地 Maven 仓库中。

   ```shell
   mvn install:install-file "-Dfile=../kaiwudb-jdbc-2.0.4.1.jar" "-DgroupId=com.kaiwudb" "-DartifactId=kaiwudb-jdbc" "-Dversion=2.0.4.1" "-Dpackaging=jar"
   ```

## 连接 KWDB 数据库

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
