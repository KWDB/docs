---
title: Flink 读写数据
id: flink
---

# Flink 读写数据

Apache Flink 是 Apache 软件基金会开源的分布式流批一体化处理框架，广泛应用于流处理、批处理、复杂事件处理、实时数据仓库构建以及机器学习等大数据场景。

为实现 Flink 与 KWDB 的高效集成，KWDB 提供了专用的连接器 KaiwuDB Flink Connector。该连接器通过 Source 组件从 KWDB 读取数据进行实时分析，通过 Sink 组件将 Flink 处理后的结果写入 KWDB，实现高效的数据存储与管理。

KaiwuDB Flink Connector 支持以下两种使用方式：

- **DataStream API**：用于底层的流处理编程，提供灵活的数据处理能力
- **Flink Table**：提供高层的声明式接口，用户可通过 SQL 语句实现复杂的数据处理逻辑

## 功能概述

KaiwuDB Flink Connector 支持以下功能：

- 从 KWDB 读取数据并使用 Flink 进行分析处理
- 将 Flink 的复杂计算和深度分析结果写入 KWDB
- KWDB 与 Flink 数据类型的自动映射转换
- 灵活的参数配置：支持 URL 地址、批处理大小、数据库和表名、并发度等配置
- 支持按时间戳和主标签进行数据分片，实现并发读取

## 配置 KaiwuDB Flink Connector 

### 前提条件

- [安装 openJDK](https://openjdk.org/install/)（1.8 及以上版本）。
- [安装 Maven](https://maven.apache.org/install.html)（3.6 及以上版本）。
- 安装 KWDB 数据库、配置数据库认证方式、创建数据库。
- 创建具有表级别及以上操作权限的用户。
- 获取 KaiwuDB Flink Connector 安装包。
- [安装 Apache Flink](https://flink.apache.org/)（1.19.0 及以上版本）。

  Apache Flink 安装示例：

  ```bash
  # 下载 Apache Flink
  $ wget https://downloads.apache.org/flink/flink-1.19.2/flink-1.19.2-bin-scala_2.11.tgz

  # 解压 Flink 压缩包
  $ tar -xvzf flink-1.19.2-bin-scala_2.11.tgz

  # 启动 Flink 集群
  $ cd flink-1.19.2
  $ ./bin/start-cluster.sh

  # 验证安装：在浏览器中访问 http://127.0.0.1:8081
  # 如果能看到 Flink Dashboard，表示安装成功
  ```

### 配置连接器

1. 在项目的 `pom.xml` 文件中添加以下依赖：

   ```xml
    <dependency>
    <groupId>com.kaiwudb.flink</groupId>
    <artifactId>flink-connector-kaiwudb</artifactId>
    <version>1.0.0</version>
    </dependency>
   ```

2. 如果无法正常加载上述依赖，运行以下命令，将 KaiwuDB Flink Connector 安装到本地 Maven 仓库：

   ```bash
    mvn install:install-file \
    -Dfile=./flink-connector-kaiwudb-1.0.0.jar \
    -DgroupId=com.kaiwudb.flink \
    -DartifactId=flink-connector-kaiwudb \
    -Dversion=1.0.0 \
    -Dpackaging=jar
   ```

### 配置语义保证

配置连接器后，需要为 Flink 作业选择合适的语义保证级别。基于 KWDB 时序引擎的特性和性能考虑，建议采用 **At-Least-Once** 语义配置。

代码示例：

```java
StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
// 设置并行度
environment.setParallelism(4);
// 启用检查点，间隔30秒
environment.enableCheckpointing(30000);
// 设置 At-Least-Once 语义
environment.getCheckpointConfig().setCheckpointingMode(CheckpointingMode.AT_LEAST_ONCE); 
```

### 配置数据库连接

使用连接器之前，需要正确配置数据库连接参数。连接器支持基础连接参数配置和 Flink Table API 专用参数配置。

#### 基础连接参数

| 参数名 | 说明 |是否必填 | 默认值 |
|--------|----------|--------|------|
| url  | 数据库连接 URL |是 | - |
| dbname  | 数据库名称 |是 | - |
| table.name  | 表名 | 是 | - |
| fetch.size | 批量获取数据大小 | 否 | 1000 |
| batch.size | 批量写入大小 | 否 | 1000 |

#### URL 格式规范

数据库连接 URL 的标准格式为：

```java
jdbc:kaiwudb://[host]:[port]/[dbname]?user={user}&password={password}
```

参数说明：

- `host`：数据库主机 IP 或域名，默认为 localhost
- `port`：数据库端口，默认为 26257
- `dbname`：数据库名称
- `user`：数据库用户名
- `password`：数据库用户登录密码

#### Flink Table 连接器参数

使用 Flink Table SQL API 时，需要配置以下专用参数：

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| connector | String | 是 | 固定值：`kaiwudb-connector` |
| mode | String | 是 | 连接器模式：`source`（读取数据）或 `sink`（写入数据） |
| url | String | 是 | KWDB 连接 URL |
| dbname | String | 否 | 源端数据库名称（source 模式使用） |
| table.name | String | 否 | 源端读取数据的表名（source 模式使用） |
| scan.query | String | 否 | 自定义读取数据的 SQL 语句（source 模式使用） |
| fetch.size | Integer | 否 | 读取数据的批大小（source 模式使用） |
| sink.db.name | String | 否 | 目标数据库名（sink 模式使用） |
| sink.table.name | String | 否 | 目标表名（sink 模式使用） |
| sink.batch.size | Integer | 否 | 写入批量大小（sink 模式使用） |
| sink.parallelism | Integer | 否 | 写入并行度（sink 模式使用） |

## 配置示例

本节提供了使用 KaiwuDB Flink Connector 的完整示例，包括数据读取和写入的两种场景，每种场景都提供了 DataStream API 和 Table SQL 两种实现方式。

### 读取数据

#### 使用 DataStream API 读取数据

以下示例展示如何使用 DataStream API 从 KWDB 读取数据：

```java
// 测试基础数据源读取功能
public void testSource() throws Exception {
    System.out.println("Test flink source start！");
    
    // 创建 SQL 分片对象，指定要查询的表和字段
    SplitObject sqlObject = new SplitObject("select ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 from test_tb");
    
    // 执行源查询，并行度设置为1
    sourceQuery(sqlObject, 1);
    System.out.println("Test flink source finished！");
}

// 测试基于时间分片的数据源读取
public void testSourceByTimeSplit() throws Exception {
    System.out.println("Test flink source by time split start！");
    
    // 创建 SQL 分片对象并配置时间分片参数
    SplitObject sqlObject = new SplitObject();
    sqlObject.setSql("select ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 from test_tb")
        .setSplitType(SplitType.TIMESTAMP)  // 设置分片类型为时间戳分片
        .setTimestampSplit(new SplitTimestamp(
            "2025-06-11 15:00:00.000",      // 开始时间
            "2025-06-11 17:00:00.000",      // 结束时间
            "ts",                            // 时间戳字段名
            Duration.ofHours(1),             // 每个分片的时间间隔（1小时）
            new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS"),  // 时间格式
            ZoneId.of("Asia/Shanghai")));    // 时区设置
    
    // 执行源查询，并行度设置为3（对应时间分片数量）
    sourceQuery(sqlObject, 3);
    System.out.println("Test flink source by time split finished！");
}

// 测试基于标签分片的数据源读取
public void testSourceByTagSplit() throws Exception {
    System.out.println("Test flink source by tag split start！");
    
    // 创建 SQL 分片对象并配置标签分片参数
    SplitObject sqlObject = new SplitObject();
    sqlObject.setSql("select ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 from test_tb")
        .setSplitType(SplitType.TAG)  // 设置分片类型为标签分片
        .setTagList(Arrays.asList("t1 = 1", "t1 = 2", "t1 = 3"));  // 设置标签过滤条件列表
    
    // 执行源查询，并行度设置为3（对应标签分片数量）
    sourceQuery(sqlObject, 3);
    System.out.println("Test flink source by tag split finished！");
}

// 通用的源查询方法
private void sourceQuery(SplitObject sqlObject, int parallelism) throws Exception {
    // 获取流执行环境
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    // 设置并行度
    environment.setParallelism(parallelism);
    
    // 获取数据源连接属性配置
    Properties sourceProps = SqlHelper.getProperties("flink_source", null);
    
    // 创建 KWDB 数据源，指定返回数据类型为 RowData
    KwdbSource<RowData> source = new KwdbSource <> (sourceProps, sqlObject, RowData.class);
    
    // 从数据源创建数据流，不使用水印策略
    DataStreamSource<RowData> streamSource = environment.fromSource(source, WatermarkStrategy.noWatermarks(), "kaiwudb-source");
    
    // 将 RowData 转换为字符串格式，方便打印输出
    DataStream<String> resultStream = streamSource.map((MapFunction<RowData, String>) rowData - >
        "ts: " + rowData.getTimestamp(0, 5) +          // 获取时间戳字段（索引0，精度5）
        ", c1: " + rowData.getShort(1) +               // 获取 SMALLINT 字段
        ", c2: " + rowData.getInt(2) +                 // 获取 INT 字段
        ", c3: " + rowData.getLong(3) +                // 获取 BIGINT 字段
        ", c4: " + rowData.getFloat(4) +               // 获取 FLOAT 字段
        ", c5: " + rowData.getDouble(5) +              // 获取 DOUBLE 字段
        ", c6: " + rowData.getBoolean(6) +             // 获取 BOOLEAN 字段
        ", c7: " + rowData.getString(7).toString() +   // 获取 CHAR 字段
        ", c8: " + rowData.getString(8).toString() +   // 获取 VARCHAR 字段
        ", c9: " + rowData.getString(9).toString() +   // 获取 VARCHAR 字段
        ", c10: " + rowData.getString(10).toString() + // 获取 VARCHAR 字段
        ", c11: " + Arrays.toString(rowData.getBinary(11)) +  // 获取 BYTES 字段
        ", c12: " + rowData.getTimestamp(12, 5) +      // 获取第二个时间戳字段
        ", t1: " + rowData.getInt(13) +                // 获取标签字段1
        ", t2: " + rowData.getString(14).toString());  // 获取标签字段2
    
    // 打印结果流
    resultStream.print();
    
    // 执行 Flink 作业
    environment.execute("flink kaiwudb source");
}}
```

#### 使用 Flink Table 读取数据

以下示例展示如何使用 Flink Table 从 KWDB 读取数据：

```java
// 测试使用 SQL DDL 方式创建表并读取数据
public void testFlinkTableSourceBySql() throws Exception {
    System.out.println("Test flink table source by sql start！");
    
    // 创建流式处理环境设置
    EnvironmentSettings settings = EnvironmentSettings.newInstance().inStreamingMode().build();
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    StreamTableEnvironment tableEnvironment = StreamTableEnvironment.create(environment, settings);
    
    // 定义源表的 DDL SQL，包含表结构和连接器配置
    String sourceTableSql = "CREATE TABLE source_test_tb (" +
        "ts TIMESTAMP, " +                    // 时间戳字段
        "c1 SMALLINT, " +                     // 短整型字段
        "c2 INT, " +                          // 整型字段
        "c3 BIGINT, " +                       // 长整型字段
        "c4 FLOAT, " +                        // 浮点型字段
        "c5 DOUBLE, " +                       // 双精度浮点型字段
        "c6 BOOLEAN, " +                      // 布尔型字段
        "c7 CHAR(1), " +                      // 定长字符字段
        "c8 VARCHAR(10), " +                  // 变长字符字段
        "c9 VARCHAR(10), " +                  // 变长字符字段
        "c10 VARCHAR(10), " +                 // 变长字符字段
        "c11 BYTES, " +                       // 字节数组字段
        "c12 TIMESTAMP, " +                   // 时间戳字段
        "t1 INT, " +                          // 标签字段1
        "t2 VARCHAR(10)" +                    // 标签字段2
        ") WITH (" +                          // 连接器配置
        "  'connector' = 'kaiwudb-connector', " +     // 指定连接器类型
        "  'mode' = 'source', " +                     // 设置为源模式
        "  'url' = 'jdbc:kaiwudb://127.0.0.1:26257/flink_source?user=test&password=Password@2024', " +  // 数据库连接URL
        "  'table.name' = 'test_tb', " +              // 源表名
        "  'scan.query' = 'SELECT ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 FROM test_tb'" +  // 扫描查询SQL
        ")";
    
    // 执行 DDL 语句创建表
    tableEnvironment.executeSql(sourceTableSql);
    
    // 定义查询 SQL
    String querySql = "SELECT ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 FROM source_test_tb";
    
    // 执行查询获取结果表
    Table resultTable = tableEnvironment.sqlQuery(querySql);
    
    // 打印数据流结果
    printDataStream(tableEnvironment, resultTable);
    
    // 执行 Flink 作业
    environment.execute("Flink Table Source By Sql API Example");
    System.out.println("Test flink table source by sql finished！");
}

// 测试使用 TableDescriptor API 方式创建表并读取数据
public void testFlinkTableSourceByTableDescriptor() throws Exception {
    System.out.println("Test flink table source by TableDescriptor start！");
    
    // 创建流式处理环境设置
    EnvironmentSettings settings = EnvironmentSettings.newInstance().inStreamingMode().build();
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    StreamTableEnvironment tableEnvironment = StreamTableEnvironment.create(environment, settings);
    
    // 使用 TableDescriptor 构建器模式创建表描述符
    TableDescriptor sourceDescriptor = TableDescriptor.forConnector("kaiwudb-connector")
        // 定义表结构 Schema
        .schema(Schema.newBuilder()
            .column("ts", DataTypes.TIMESTAMP_WITH_LOCAL_TIME_ZONE().notNull())  // 带本地时区的时间戳，非空
            .column("c1", DataTypes.SMALLINT())          // 短整型
            .column("c2", DataTypes.INT())               // 整型
            .column("c3", DataTypes.BIGINT())            // 长整型
            .column("c4", DataTypes.FLOAT())             // 浮点型
            .column("c5", DataTypes.DOUBLE())            // 双精度浮点型
            .column("c6", DataTypes.BOOLEAN())           // 布尔型
            .column("c7", DataTypes.CHAR(1))             // 定长字符
            .column("c8", DataTypes.VARCHAR(10))         // 变长字符
            .column("c9", DataTypes.VARCHAR(10))         // 变长字符
            .column("c10", DataTypes.VARCHAR(10))        // 变长字符
            .column("c11", DataTypes.BYTES())            // 字节数组
            .column("c12", DataTypes.TIMESTAMP())        // 时间戳
            .column("t1", DataTypes.INT().notNull())     // 标签字段1，非空
            .column("t2", DataTypes.VARCHAR(10))         // 标签字段2
            .build())
        // 配置连接器选项
        .option("url", "jdbc:kaiwudb://127.0.0.1:26257/flink_source?user=test&password=Password@2024")  // 数据库连接URL
        .option("mode", "source")                        // 设置为源模式
        .option("table.name", "test_tb")                 // 源表名
        .option("scan.query", "SELECT ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 FROM test_tb")  // 扫描查询SQL
        .build();
    
    // 注册临时表
    tableEnvironment.createTemporaryTable("source_test_tb", sourceDescriptor);

    // 定义带过滤条件的查询 SQL
    String querySql = "SELECT ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 FROM source_test_tb WHERE t1 > 2";
    
    // 执行查询获取结果表
    Table resultTable = tableEnvironment.sqlQuery(querySql);
    
    // 打印数据流结果
    printDataStream(tableEnvironment, resultTable);
    
    // 执行 Flink 作业
    environment.execute("Test flink table source by TableDescriptor API Example");
    System.out.println("Test flink table source by TableDescriptor finished！");
}

// 通用的数据流打印方法
private void printDataStream(StreamTableEnvironment tableEnvironment, Table resultTable) {
    // 将 Table 转换为 AppendStream（仅追加流）
    DataStream<RowData> resultStream = tableEnvironment.toAppendStream(resultTable, RowData.class);
    
    // 将 RowData 映射为字符串格式并打印
    resultStream.map((MapFunction<RowData, String>) rowData ->
        "ts: " + rowData.getTimestamp(0, 5)                           // 时间戳字段
         + ", c1: " + rowData.getShort(1)                             // 短整型字段
         + ", c2: " + rowData.getInt(2)                               // 整型字段
         + ", c3: " + rowData.getLong(3)                              // 长整型字段
         + ", c4: " + rowData.getFloat(4)                             // 浮点型字段
         + ", c5: " + rowData.getDouble(5)                            // 双精度浮点型字段
         + ", c6: " + rowData.getBoolean(6)                           // 布尔型字段
         + ", c7: " + rowData.getString(7).toString()                 // 定长字符字段
         + ", c8: " + rowData.getString(8).toString()                 // 变长字符字段
         + ", c9: " + rowData.getString(9).toString()                 // 变长字符字段
         + ", c10: " + rowData.getString(10).toString()               // 变长字符字段
         + ", c11: " + new String(rowData.getBinary(11), StandardCharsets.UTF_8)  // 字节数组字段，转为UTF-8字符串
         + ", c12: " + rowData.getTimestamp(12, 5)                    // 第二个时间戳字段
         + ", t1: " + rowData.getInt(13)                              // 标签字段1
         + ", t2: " + rowData.getString(14).toString()                // 标签字段2
    ).print();
}
```

### 写入数据

#### 使用 DataStream API 写入数据

以下示例展示如何使用 DataStream API 将数据写入 KWDB：

```java
// 测试从 KWDB 读取数据并写入另一个 KWDB 实例的完整流程
public void testSourceToSink() throws Exception {
    System.out.println("Test flink source to sink start！");
    
    // 获取流执行环境
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    environment.setParallelism(1);  // 设置并行度为1
    environment.enableCheckpointing(3000, AT_LEAST_ONCE);  // 启用检查点，间隔3秒，至少一次语义

    // 配置数据源的时间分片参数
    SplitObject sqlObject = new SplitObject();
    sqlObject.setSql("select ts, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, t1, t2 from test_tb")
        .setSplitType(SplitType.TIMESTAMP)  // 设置分片类型为时间戳分片
        .setTimestampSplit(new SplitTimestamp(
            "2025-06-11 15:00:00.000",      // 开始时间
            "2025-06-11 18:00:00.000",      // 结束时间
            "ts",                            // 时间戳字段名
            Duration.ofHours(1),             // 每个分片的时间间隔（1小时）
            new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS"),  // 时间格式
            ZoneId.of("Asia/Shanghai")));    // 时区设置
    
    // 获取数据源连接属性配置
    Properties sourceProps = SqlHelper.getProperties("flink_source", null);
    
    // 创建 KWDB 数据源
    KwdbSource<RowData> source = new KwdbSource<> (sourceProps, sqlObject, RowData.class);
    
    // 从数据源创建数据流
    DataStreamSource<RowData> streamSource = environment.fromSource(source, WatermarkStrategy.noWatermarks(), "KaiwuDB-Source");

    // 获取数据汇连接属性配置，设置批大小为2000
    Properties sinkProps = SqlHelper.getProperties("flink_kaiwudb_sink", "2000");
    
    // 定义字段名列表，与源表字段对应
    List<String> fieldNames = Arrays.asList("ts", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12", "t1", "t2");
    
    // 创建 KWDB 数据汇
    KwdbSink<RowData> sink = new KwdbSink <> (sinkProps, fieldNames);
    
    // 将数据流写入目标数据库
    streamSource.sinkTo(sink);
    
    // 执行 Flink 作业
    environment.execute("flink kaiwudb source");
    
    // 验证数据写入结果：查询目标表中 t1 字段的总和
    String querySumSql = "select sum(t1) from flink_kaiwudb_sink.test_tb";
    int querySumResult = SqlHelper.querySumResult(querySumSql);
    Assertions.assertEquals(30, querySumResult);  // 断言结果为30

    System.out.println("Test flink source to sink finished！");
}
```

#### 使用 Flink Table 写入数据

##### 将 SQL 类型数据写入 KWDB

以下示例展示如何使用 Flink Table 从 MySQL CDC 读取数据并写入 KWDB：

```java
// 测试从 MySQL CDC 读取数据并写入 KWDB
public void testMysqlSourceToKaiwuDBSink() throws Exception {
    // 获取流执行环境并设置检查点
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    environment.setParallelism(1);  // 设置并行度为1
    environment.enableCheckpointing(3000, AT_LEAST_ONCE);  // 启用检查点，间隔3秒，至少一次语义
    
    // 声明 MySQL 中 boolean 类型的转换处理配置
    Properties debeziumProperties = new Properties();
    debeziumProperties.setProperty("converters", "boolean");  // 设置转换器
    debeziumProperties.setProperty("boolean.type", "io.debezium.connector.mysql.converters.TinyIntOneToBooleanConverter");  // MySQL TINYINT(1) 转 Boolean

    // 构建 MySQL CDC 数据源
    MySqlSource<RowData> source = MySqlSource.<RowData>builder()
        .hostname("127.0.0.1")              // MySQL 主机地址
        .port(3306)                         // MySQL 端口
        .databaseList("flink_source")       // 监听的数据库列表
        .tableList("flink_source.test_tb")  // 监听的表列表
        .username("root")                   // 用户名
        .password("123456")                 // 密码
        .deserializer(new RowDataDebeziumDeserializationSchema())  // 反序列化器
        .debeziumProperties(debeziumProperties)  // Debezium 配置属性
        .build();
    
    // 从 MySQL CDC 源创建数据流
    DataStreamSource<RowData> streamSource = environment.fromSource(source, WatermarkStrategy.noWatermarks(), "MySQL Source");

    // 获取 KWDB 汇的连接属性配置，设置批大小为2000
    Properties sinkProps = SqlHelper.getProperties("flink_mysql_sink", "2000");
    
    // 定义字段名列表
    List<String> fieldNames = Arrays.asList("ts", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12", "t1", "t2");
    
    // 创建 KWDB 数据汇
    KwdbSink<RowData> sink = new KwdbSink<> (sinkProps, fieldNames);
    
    // 将 MySQL CDC 数据流写入 KWDB
    streamSource.sinkTo(sink);
    
    System.out.println("Test flink cdc source mysql to sink kaiwudb starting！");
    
    // 执行 Flink 作业
    environment.execute("flink kaiwudb source");
}
```

##### 将 ROW 类型数据写入 KWDB

以下示例展示如何使用 Flink Table API 将行数据写入 KWDB：

```java
// 测试从 Flink Table 行数据写入 KWDB
public void testFlinkTableRowToSink() throws Exception {
    System.out.println("Test flink table row source to sink start！");
    
    // 创建流式处理环境设置
    EnvironmentSettings settings = EnvironmentSettings.newInstance().inStreamingMode().build();
    StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
    environment.enableCheckpointing(3000, AT_LEAST_ONCE);  // 启用检查点
    StreamTableEnvironment tableEnvironment = StreamTableEnvironment.create(environment, settings);
    
    // 定义目标表的 DDL SQL
    String sinkTableSql = "CREATE TABLE sink_test_tb (" +
        "ts TIMESTAMP, " +                    // 时间戳字段
        "c1 INT, " +                          // 整型字段
        "c2 INT, " +                          // 整型字段
        "c3 INT, " +                          // 整型字段
        "c4 FLOAT, " +                        // 浮点型字段
        "c5 DOUBLE, " +                       // 双精度浮点型字段
        "c6 BOOLEAN, " +                      // 布尔型字段
        "c7 CHAR(1), " +                      // 定长字符字段
        "c8 VARCHAR(10), " +                  // 变长字符字段
        "c9 VARCHAR(10), " +                  // 变长字符字段
        "c10 VARCHAR(10), " +                 // 变长字符字段
        "c11 BYTES, " +                       // 字节数组字段
        "c12 TIMESTAMP, " +                   // 时间戳字段
        "t1 INT, " +                          // 标签字段1
        "t2 VARCHAR(10)" +                    // 标签字段2
        ") WITH (" +                          // 连接器配置
        "  'connector' = 'kaiwudb-connector', " +     // 指定连接器类型
        "  'mode' = 'sink', " +                       // 设置为汇模式
        "  'url' = 'jdbc:kaiwudb://127.0.0.1:26257/flink_table_kaiwudb_sink?user=test&password=Password@2024', " +  // 数据库连接URL
        "  'sink.db.name' = 'flink_table_kaiwudb_sink', " +   // 目标数据库名
        "  'sink.table.name' = 'test_tb'" +                   // 目标表名
        ")";
    
    // 执行 DDL 语句创建汇表
    tableEnvironment.executeSql(sinkTableSql);
    
    // 获取输入数据表（包含测试数据）
    Table inputTable = getInputTable(tableEnvironment);
    
    // 执行插入操作，将数据写入目标表
    TableResult tableResult = inputTable.executeInsert("sink_test_tb");
    tableResult.await();  // 等待插入操作完成
    
    // 验证数据写入结果：查询目标表中满足条件的 t1 字段总和
    String querySumSql = "SELECT sum(t1) FROM flink_table_kaiwudb_sink.test_tb WHERE t1 < 5";
    int querySumResult = SqlHelper.querySumResult(querySumSql);
    Assertions.assertEquals(20, querySumResult);  // 断言结果为20
    
    System.out.println("Test flink table row source to sink finished！");
}

// 生成测试输入数据表
private Table getInputTable(StreamTableEnvironment tableEnvironment) {
    // 创建行数据列表
    List<Row> rowData = new ArrayList<>();
    ThreadLocalRandom random = ThreadLocalRandom.current();  // 线程安全的随机数生成器
    long tsTime = 1749625212123 L;  // 基准时间戳
    
    // 生成10行测试数据
    for (int i = 0; i < 10; i++) {
        long timestamp = tsTime + (15 * 60 * 1000) * i;  // 每行数据间隔15分钟
        Row row = Row.of(
            new Timestamp(timestamp),                     // 时间戳字段
            random.nextInt(10),                          // 随机整数（0-9）
            random.nextInt(100),                         // 随机整数（0-99）
            random.nextInt(1000),                        // 随机整数（0-999）
            random.nextFloat(),                          // 随机浮点数
            random.nextDouble(),                         // 随机双精度浮点数
            random.nextBoolean(),                        // 随机布尔值
            RandomStringUtils.randomAlphanumeric(1),     // 随机1位字母数字字符
            RandomStringUtils.randomAlphanumeric(10),    // 随机10位字母数字字符串
            RandomStringUtils.randomAlphanumeric(10),    // 随机10位字母数字字符串
            RandomStringUtils.randomAlphanumeric(10),    // 随机10位字母数字字符串
            RandomStringUtils.randomAlphanumeric(10),    // 随机10位字母数字字符串（作为字节数组）
            new Timestamp(timestamp),                     // 第二个时间戳字段
            (i / 2) + 1,                                 // 标签字段1：根据索引计算（1,1,2,2,3,3...）
            "tianjin"                                    // 标签字段2：固定值
        );
        rowData.add(row);
    }
    
    // 使用 fromValues 方法创建表，定义数据类型和字段结构
    return tableEnvironment.fromValues(
        DataTypes.ROW(
            DataTypes.FIELD("ts", DataTypes.TIMESTAMP(6)),      // 时间戳字段，精度6
            DataTypes.FIELD("c1", DataTypes.INT()),             // 整型字段
            DataTypes.FIELD("c2", DataTypes.INT()),             // 整型字段
            DataTypes.FIELD("c3", DataTypes.INT()),             // 整型字段
            DataTypes.FIELD("c4", DataTypes.FLOAT()),           // 浮点型字段
            DataTypes.FIELD("c5", DataTypes.DOUBLE()),          // 双精度浮点型字段
            DataTypes.FIELD("c6", DataTypes.BOOLEAN()),         // 布尔型字段
            DataTypes.FIELD("c7", DataTypes.CHAR(1)),           // 定长字符字段
            DataTypes.FIELD("c8", DataTypes.STRING()),          // 字符串字段
            DataTypes.FIELD("c9", DataTypes.STRING()),          // 字符串字段
            DataTypes.FIELD("c10", DataTypes.STRING()),         // 字符串字段
            DataTypes.FIELD("c11", DataTypes.BYTES()),          // 字节数组字段
            DataTypes.FIELD("c12", DataTypes.TIMESTAMP(6)),     // 时间戳字段，精度6
            DataTypes.FIELD("t1", DataTypes.INT()),             // 标签字段1
            DataTypes.FIELD("t2", DataTypes.STRING())           // 标签字段2
        ),
        rowData  // 传入生成的测试数据
    );
}
```

## 参考信息

### 数据类型转换

**时序数据**

| KWDB                 | Flink RowData    | Flink Table SQL   |
|------------------------|------------------|--------------------|
| TIMESTAMP              | Timestamp        | TIMESTAMP          |
| TIMESTAMPTZ            | Timestamp        | TIMESTAMP_LTZ      |
| BOOL                   | Boolean          | BOOLEAN            |
| SMALLINT               | Short            | SMALLINT           |
| INT                    | Integer          | INT                |
| BIGINT                 | Long             | BIGINT             |
| REAL                   | Float            | FLOAT              |
| DOUBLE                 | Double           | DOUBLE             |
| VARBYTES               | byte[]           | BYTES              |
| CHAR                   | String           | CHAR/STRING        |
| VARCHAR、NCHAR、NVARCHAR | String         | VARCHAR/STRING     |
| GEOMETRY               | String           | STRING             |

**关系数据**

::: warning 说明
DECIMAL 类型必须设置 precision 和 scale 值，否则不支持处理此类型的数据。
:::

| KWDB                 | Flink RowData    | Flink Table SQL   |
|-------------------------|------------------|--------------------|
| TIMESTAMP               | Timestamp        | TIMESTAMP          |
| TIMESTAMPTZ             | Timestamp        | TIMESTAMP_LTZ      |
| DATE                    | String           | STRING             |
| TIME                    | Time             | TIME               |
| BOOL                    | Boolean          | BOOLEAN            |
| SMALLINT                | Short            | SMALLINT           |
| INT                     | Integer          | INT                |
| BIGINT、SERIAL           | Long             | BIGINT             |
| REAL                  | Float            | FLOAT              |
| DOUBLE                  | Double           | DOUBLE             |
| DECIMAL(p,s)            | BigDecimal       | DECIMAL(p,s)       |
| BIT、VARBIT              | String           | STRING             |
| BYTES、VARBYTES          | byte[]           | BYTES              |
| CHAR                    | String           | CHAR/STRING        |
| VARCHAR、NCHAR、NVARCHAR  | String           | VARCHAR/STRING     |
| JSON、JSONB、TEXT         | String           | STRING             |
| STRING[]、STRING、COLLATE | String           | STRING             |
| INTERVAL、INET、UUID      | String           | STRING             |