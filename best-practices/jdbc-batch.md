---
title: KaiwuDB JDBC 扩展协议
id: jdbc-batch
---

# KaiwuDB JDBC 简介

KaiwuDB JDBC 是 KWDB 的官方 Java 语言连接器，基于 PgJDBC 扩展实现，符合 JDBC 4.0、JDBC 4.1 和 JDBC 4.2 规范。Java 开发人员可以使用 KaiwuDB JDBC 驱动程序连接 KWDB 的服务进程，进行数据增删改查操作
- 支持PG扩展协议‘M’类消息支持，支持列式批量数据传输及Snappy/LZ4压缩功能（3.2.2 及以上版本）。
- 支持扩展 pgwire prepare/bind 写入模式，新增私有 ‘j/k/l’ 消息，实现数据批量快速写入（3.3.0 及以上版本）。

KaiwuDB JDBC 提供了传统的批量执行 SQL 接口，用户可以通过手动拼接 SQL 实现批量数据写入，同时提供了 `addBatchInsert`、`executeBatchInsert` 和 `clearBatchInsert` 接口，能够将同一张时序表的多次数据写入合并到一条 SQL 语句，降低 CPU 占用，提升写入性能。

 使用批量接口写入数据时，如果待写入的值与列的数据类型不符或者待写入的字段不存在，KaiwuDB JDBC 会返回成功写入条数、写入失败条数，并将具体错误信息记录到日志中。本文提供了使用 KaiwuDB JDBC 批量接口写入数据的最佳实践。

有关 KaiwuDB JDBC 的数据库连接方式、基础使用、数据类型和异常处理，参见[使用 JDBC 连接 KWDB 数据库](../development/java/connect-jdbc.md)；更多错误码信息，参见 [KaiwuDB JDBC Driver 错误码](../db-operation/error-code/error-code-jdbc-driver.md)；更多故障排查信息，参见 [KaiwuDB JDBC 故障排查](../troubleshooting-guide/troubleshooting.md#kaiwudb-jdbc)。

## 前提条件

- [安装 openJDK](https://openjdk.org/install/)（1.8 及以上版本）。
- [安装 Maven](https://maven.apache.org/install.html)（3.6 及以上版本）。
- 安装 KWDB 3.3.0 或以上版本数据库、配置数据库认证方式、创建数据库。
- 创建具有表级别及以上操作权限的用户。
- 获取 KaiwuDB JDBC 驱动包（3.3.0）。

## 配置数据库

默认情况下，数据库开启时序写入短接功能。开启后，系统直接将数据写入存储，减少中间处理环节。此外，用户可以设置允许写入时跳过错误数据，正常写入其他数据，从而提高写入性能。

```sql
SET SESSION ts_ignore_batcherror=true;
```

## 配置连接

1. 在 `pom.xml` 中添加依赖，将 KaiwuDB JDBC 引入 Java 项目：

   ```xml
   <dependency>
     <groupId>com.kaiwudb</groupId>
     <artifactId>kaiwudb-jdbc</artifactId>
     <version>3.3.0</version>
   </dependency>
   ```

2. 如果 KaiwuDB JDBC 无法正常加载使用，执行以下命令，将驱动安装到本地 Maven 仓库中：

   ```shell
   mvn install:install-file "-Dfile=../kaiwudb-jdbc-3.3.0.jar" "-DgroupId=com.kaiwudb" "-DartifactId=kaiwudb-jdbc" "-Dversion=3.3.0" "-Dpackaging=jar"
   ```
# 使用 KaiwuDB JDBC 扩展接口优化批量数据写入

启用PG扩展协议压缩功能，通过会话变量 `pg_extend_compress` 控制：

   ```sql
   SET pg_extend_compress = off --关闭扩展协议（默认，走标准PG协议）
   SET pg_extend_compress = lz4_compress --启用LZ4压缩的扩展协议
   SET pg_extend_compress = snappy_compress --启用Snappy压缩的扩展协议
   ```

::: 说明
大批量结果集（如≥1W行）可设置启用压缩走扩展传输链路实现传输提速；小批量结果集（如≤1W行）保持原生协议，无明显损耗。
:::

## 配置示例

以下示例演示了如何使用 KaiwuDB JDBC 将不同设备的数据批量写入到时序表。

1. 创建时序表。

   以下示例创建 `tbl_raw_1` 到 `tbl_raw_10` 多个时序表用于批量插入不同设备的数据。每个表的数据结构相同。

   ```sql
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

   ```java
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

# Prepare-extend 扩展写入模式

prepare-extend 写入模式是 KaiwuDB 自定义的时序表批量直插协议，使用该模式需要满足以下条件：
- KaiwuDB数据库服务端版本需支持 `prepare_extend` 写入模式，KaiwuDB 版本不低于 3.3.0。
- JDBC 驱动版本不低于3.3.0。
- 会话开启 `tsinsert_direct`，否则 ‘j’ 消息被服务端拒绝（错误码 08P01 ）。
- prepare-extend 写入模式仅支持时序表。支持单表名、库表.表名、库名.public.表名。

## 接口明细

| 接口 | 说明 |
| ----- | ---- |
| setTimePrecision(columnIndex, precision)                                       | precision ∈ {3,6,9}，默认3（毫秒）；<br > 1起始列下标，含时间列；<br > 仅 TIMESTAMP/TIMESTAMPTZ 列可设置，非时间列抛异常；<br > 须在 executeBatch 前调用 |
| getMaxBindExBytes()                                                            | 获取/设置单条'l'消息大小上限（默认 512MB，须为正数） |
| setMaxBindExBytes(int)                                                         | 单条 'l' 消息大小上限，默认512MB；<br > 须为正数，超限时报错 |
| addBatch()	                                                                  | 将当前 setter 行缓冲为一新行；时间列与全部主标签列必须已设置且主标签非NULL，其余数据列未设置默认 NULL（部分列插入，NOT NULL 列由服务端约束报错） |
| addBatch(Object[] ptagValues, Object[] ordinaryTagValues, Object[] dataValues) | 按主标签值数组+普通标签值数组+数据列值数组直接追加一行；普通标签允许 NULL，可为 `null` 或空数组 |
| getTsParameterDescription()	                                                   | 返回服务端'k'消息下发的列元数据（列OID、tagIndex、主标签列下标、存储长度） |
| getTsRowCount()	                                                               | 返回当前已缓冲未发送的行数 |
| executeBatch                                                                   | 整批行一次提交完成写入，返回单元素数组，元素值 = 服务端实际写入的总行数；数组求和即实际写入行数；executeBatch() 在总行数超 int 范围时提示改用 executeLargeBatch() |

## 批量直插示例

```java
public void testPrepareExtend() {
    Class.forName("com.kaiwudb.Driver");
    String url = "jdbc :kaiwudb://127.0.0.1:26257/tsdb?user=test&password=Password@2024";
    try (Connection connection = DriverManager.getConnection(url);  Statement stmt = conn.createStatement() ) {
        // 删除表
        stmt.execute("drop table if exists tsdb.ts_tb cascade");
        // 建表：时间列 + 数据列 + 标签列，主标签 (t1, t2)
        stmt.execute("create table tsdb.ts_tb (ts timestamptz not null, c1 int8, c2 varchar(32)) tags (t1 int not null, t2 varchar not null) primary tags (t1, t2)");

        try (KWTSPreparedStatement ps = ((KwConnection) conn).prepareTsStatement("tsdb.ts_tb")) {
            for (int i = 0; i < 10000; i++) {
                ps.setTimestamp(1, new Timestamp(System.currentTimeMillis() + i * 1000L));
                ps.setLong(2, i);
                ps.setString(3, "v" + i);
                ps.setInt(4, i % 2);
                ps.setString(5, "host" + (i % 100));
                ps.addBatch();
            }
                int[] rows = ps.executeBatch();
                System.out.println("inserted: " + rows[0]);
        } catch (SQLException ex) {
            System.err.println("Exception: " + ex.getMessage());
        }
    }
} 
```

::: warning 说明
- 支持的 setter ：setObject 、 setBoolean 、 setByte 、 setShort 、 setInt 、 setLong 、 setFloat 、 setDouble 、 setBigDecimal 、 setString 、 setBytes 、 setDate 、 setTime 、 setTimestamp 、 setNull；
- 不支持的 setter （抛 SQLException）：setAsciiStream 、 setBinaryStream 、 setCharacterStream 、 setBlob 、 setClob 、 setArray 、 setSQLXML 、 setNString 等流式与大对象接口；
- 不支持的标准执行方法（抛 SQLException）：execute 、 executeQuery 、 executeUpdate 、 executeLargeUpdate 、 executeWithFlags 、 addBatch(String)。
:::