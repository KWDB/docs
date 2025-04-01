---
title: 使用 KaiwuDB JDBC 扩展接口优化批量数据写入
id: jdbc-batch
---

# 使用 KaiwuDB JDBC 扩展接口优化批量数据写入

KaiwuDB JDBC 是 KWDB 的官方 Java 语言连接器，基于 PgJDBC 扩展实现，符合 JDBC 4.0、JDBC 4.1 和 JDBC 4.2 规范。Java 开发人员可以使用 KaiwuDB JDBC 驱动程序连接 KWDB 的服务进程，进行数据增删改查操作。

KaiwuDB JDBC 提供了传统的批量执行 SQL 接口，用户可以通过手动拼接 SQL 实现批量数据写入，同时提供了
 `addBatchInsert`、`executeBatchInsert` 和 `clearBatchInsert` 接口，能够将同一张时序表的多次数据写入合并到一条 SQL 语句，降低 CPU 占用，提升写入性能。

 使用批量接口写入数据时，如果待写入的值与列的数据类型不符或者待写入的字段不存在，KaiwuDB JDBC 会返回成功写入条数、写入失败条数，并将具体错误信息记录到日志中。本文提供了使用 KaiwuDB JDBC 批量接口写入数据的最佳实践。

::: warning 说明

目前，批量写入功能只适用于 KWDB 单机版本。

:::

有关 KaiwuDB JDBC 的数据库连接方式、基础使用、数据类型和异常处理，参见[使用 JDBC 连接 KWDB 数据库](../development/connect-kaiwudb/java/connect-jdbc.md)；更多错误码信息，参见 [KaiwuDB JDBC Driver 错误码](../db-operation/error-code/error-code-jdbc-driver.md)；更多故障排查信息，参见 [KaiwuDB JDBC 故障排查](../troubleshooting-guide/troubleshooting.md#kaiwudb-jdbc)。

## 前提条件

- [安装 openJDK](https://openjdk.org/install/)（1.8 及以上版本）。
- [安装 Maven](https://maven.apache.org/install.html)（3.6 及以上版本）。
- 安装 KWDB 2.1.0 或以上版本数据库、配置数据库认证方式、创建数据库。
- 创建具有表级别及以上操作权限的用户。
- 获取 KaiwuDB JDBC 驱动包。

## 配置数据库

1. 启用时序写入短接功能，该功能默认关闭，，启用后可以直接将数据写入存储，减少中间处理环节，提高性能。
   - 为当前会话启用时序写入短接功能。

      ```SQL
      SET SESSION tsinsert_direct=true;
      ```

   - 为 KWDB 集群启用时序写入短接功能：

      ```SQL
      SET CLUSTER SETTING server.tsinsert_direct.enabled = TRUE;
      ```

2. 允许写入时跳过错误数据，正常写入其他数据：

      ```SQL
      SET SESSION ts_ignore_batcherror=true;
      ```

## 配置连接

1. 在 `pom.xml` 中添加依赖，将 KaiwuDB JDBC 引入 Java 项目：

   ```xml
   <dependency>
     <groupId>com.kaiwudb</groupId>
     <artifactId>kaiwudb-jdbc</artifactId>
     <version>2.2.0</version>
   </dependency>
   ```

2. 如果 KaiwuDB JDBC 无法正常加载使用，执行以下命令，将驱动安装到本地 Maven 仓库中：

   ```shell
   mvn install:install-file "-Dfile=../kaiwudb-jdbc-2.2.0.jar" "-DgroupId=com.kaiwudb" "-DartifactId=kaiwudb-jdbc" "-Dversion=2.2.0" "-Dpackaging=jar"
   ```

## 配置示例

以下示例演示了如何使用 KaiwuDB JDBC 将不同设备的数据批量写入到时序表。

1. 创建时序表。

   以下示例创建 `tbl_raw_1` 到 `tbl_raw_10` 多个时序表用于批量插入不同设备的数据。每个表的数据结构相同。

   ```SQL
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

2. 向时序表中批量写入数据。

   ```JAVA
   public class BatchInsertTest {

   public static void main(String[] args) {
      String url = "jdbc:kaiwudb://127.0.0.1:26257/tsdb?preferQueryMode=simple";
      String user = "<user_name>";
      String password = "<password>";

      try (Connection connection = DriverManager.getConnection(url, user, password)) {
         KwStatement statement = (KwStatement) connection.createStatement();
         long timestamp = 1731373200000L; // 2024-11-12 09:00:00.000 初始时间戳
         for (int i = 0; i < 1000; i++) {
         // 循环1000次，每次写入1000行数据，共计100万行数据；每次循环插入20个设备，每个设备50行的数据
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

         // execute batch insert sql data
         statement.executeBatchInsert();

         // clear batch insert temp data
         statement.clearBatchInsert();
         }
         // close statement
         statement.colse();
      } catch (SQLException ex) {
         ex.printStackTrace();
      }
   }
   }
   ```