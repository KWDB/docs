---
title: Kafka 读写数据
id: kafka
---

# Kafka 读写数据

基于 Kafka connect-api 和 Confluent 开发的功能模块，KWDB 支持 KaiwuDB Kafka Connector，实现 Kafka 与 KWDB 之间的数据双向读取。KaiwuDB Kafka Connector 包含 KaiwuDB Sink Connector 和 KaiwuDB Source Connector 两个连接器。

- KaiwuDB Sink Connector：将 Kafka 指定主题的数据批量或实时同步到 KWDB 中。
- KaiwuDB Source Connector：将 KWDB 中指定数据库的数据批量或实时同步到 Kafka 主题中。

## 配置 KaiwuDB Kafka Connector

目前，KaiwuDB Kafka Connector 只支持 Linux 操作系统。

### 前提条件

- [安装 openJDK](https://openjdk.org/install/)（1.8 及以上版本）。
- [安装 Maven](https://maven.apache.org/install.html)（3.6 及以上版本）。
- [安装 Kafka](https://kafka.apache.org/)（3.4.1 及以上版本），并且将 `$KAFKA_HOME/bin` 目录加入系统环境变量路径中。

  ```shell
  // 打开profile文件
  vi ~/.profile
  // 在文件添加配置信息：
  export KAFKA_HOME=/opt/kafka
  export PATH=$PATH:$KAFKA_HOME/bin
  ```
  
- 安装 KWDB 数据库、配置数据库认证方式、创建数据库。
- 获取 KaiwuDB Kafka Connector 插件安装包。

### 配置步骤

1. 解压缩 KaiwuDB Kafka Connector 安装包，将解压后的 KaiwuDB Kafka Connector 插件放置在 `$KAFKA_HOME/components/` 目录。

    ```shell
    unzip -d $KAFKA_HOME/components/ target/components/packages/kaiwudb-kafka-connect-*.zip
    ```

2. 修改 Kafka 的 `$KAFKA_HOME/config/connect-distributed.properties` 配置文件。在文件的 `plugin.path` 字段添加 KaiwuDB Kafka Connector 的路径。

    ```shell
    plugin.path=/usr/share/java,/opt/kafka/components
    ```

3. 进入 `kafka/bin` 目录，启动 Kafka 服务。

    ```shell
    ./zookeeper-server-start.sh -daemon $KAFKA_HOME/config/zookeeper.properties
    ./kafka-server-start.sh -daemon $KAFKA_HOME/config/server.properties
    ./connect-distributed.sh -daemon $KAFKA_HOME/config/connect-distributed.properties
    ```

4. 验证 Kafka 是否启动成功。

    ```shell
    curl http://localhost:8083/connectors
    ```

    如果各组件都启动成功，控制台输出以下信息：

    ```shell
    []
    ```

    ::: warning 说明

    如需管理 Kafka 主题信息，在 `kafka/bin` 目录下，执行以下命令：

    - 查看主题：`./kafka-topics.sh --bootstrap-server localhost:9092 --list`
    - 查看主题内的数据信息：`./kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic kw-tsdb-ts_json_kaiwudb_tb`
    - 删除主题：`./kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic kw-tsdb-ts_json_kaiwudb_tb`

    :::

## 配置 KaiwuDB Sink Connector

KaiwuDB Sink Connector 将指定的 Kafka 主题数据写入到 KWDB 数据库。

### 前提条件

- [配置 KaiwuDB Kafka Connector](#配置-kaiwudb-kafka-connector)。
- 创建待写入数据的 KWDB 数据库。
- 配置用于连接 KWDB 数据库的用户和密码。

::: warning 说明
在将 Kafka 数据写入 KWDB 数据库时，如果没有提前在数据库中创建表，KWDB 可以根据 Kafka 数据格式自动创建时序表，InfluxDB Line 数据格式除外。
:::

### 配置步骤

1. （可选）如需以多任务方式写入数据，创建自定义 Kafka 主题。无多任务需求可跳过此步骤。

    以下示例创建了名为 `kw-tsdb-ts_json_kaiwudb_tb` 的主题，并为该主题分配 5 个分区。

    ::: warning 注意

    分区数应根据 KaiwuDB Sink Connector 配置文件中的 `tasks.max` 参数值进行设置，分区数必须大于或等于 `tasks.max` 的值。例如，如果 `tasks.max` 值为 `5`，那么 `--partitions` 参数至少应设置为 `5`。

    :::

    ```shell
    ./kafka-topics.sh --create --topic kw-tsdb-ts_json_kaiwudb_tb --partitions 5 --bootstrap-server localhost:9092
    ```

2. 创建 KaiwuDB Sink Connector 配置文件，定义 Kafka 主题、KaiwuDB 连接信息及数据格式等信息。

    以下示例创建一个名为 `kw-json-kaiwudb-sink.json` 的 KaiwuDB Sink Connector 文件。

    ```json
    {
      "name": "KwdbSinkConnector",
      "config": {
        "connector.class": "com.kaiwudb.kafka.connect.sink.KwdbSinkConnector",
        "tasks.max": "5",
        "topics": "kw-tsdb-ts_json_kaiwudb_tb",
        "connection.url": "jdbc:kaiwudb://localhost:26257",
        "connection.user": "test",
        "connection.password": "Password@2024",
        "connection.database": "tsdb",
        "connection.attempts": 3,
        "connection.backoff.ms": 5000,
        "max.retries": 3,
        "retry.backoff.ms": 3000,
        "batch.size": 1000,
        "protocol.type": "json_kaiwudb",
        "timestamp.precision": "ms",
        "key.converter": "org.apache.kafka.connect.storage.StringConverter",
        "value.converter": "org.apache.kafka.connect.storage.StringConverter"
      }
    }
    ```

3. 启动 KaiwuDB Sink Connector。

    ```shell
    curl -X POST -d @kw-json-kaiwudb-sink.json http://localhost:8083/connectors -H "Content-Type: application/json"
    ```

    配置成功后，当 Kafka 指定的主题收到新消息时，KaiwuDB Sink Connector 将根据定义的配置将信息写入到 KWDB 数据库。

### 验证 KaiwuDB Sink Connector

1. 准备测试数据。

    以下示例创建一个名为 `kw-json-kaiwudb-data.txt` 的文件。

    ::: warning 说明
    Kafka 按行接收数据，不支持发送格式化的 JSON 数据。用户必须将每个完整的 JSON 对象压缩成单行字符串，确保系统能够正确解析数据。
    :::

    ```json
    {"table":"ts_json_kaiwudb_tb","columns":[{"name":"ts","type":"TIMESTAMPTZ","length":64},{"name":"c1","type":"INT2","length":16},{"name":"c2","type":"INT4","length":32},{"name":"c3","type":"INT8","length":64},{"name":"c4","type":"FLOAT4","length":32},{"name":"c5","type":"FLOAT8","length":64},{"name":"c6","type":"BOOL","length":1}],"tags":[{"name":"location","type":"VARCHAR","length":64,"primary":true,"nullable":false},{"name":"temperature","type":"FLOAT4","length":64,"primary":false,"nullable":true}],"data":[{"ts":1690855924005,"c1":11,"c2":21,"c3":2535208944865431245,"c4":6.14545,"c5":5.15656,"c6":true,"location":"tianjin","temperature":35.5},{"ts":1691853703011,"c1":12,"c2":22,"c3":6422208944865124578,"c4":1.01635,"c5":0.53533,"c6":false,"location":"tianjin","temperature":35.5},{"ts":1692065524004,"c1":13,"c2":23,"c3":1542408944865124535,"c4":3.25456,"c5":2.56356,"c6":true,"location":"tianjin","temperature":35.5},{"ts":1692199303011,"c1":14,"c2":24,"c3":1245658944865439256,"c4":2.72652,"c5":5.83533,"c6":false,"location":"tianjin","temperature":35.5},{"ts":1692285703011,"c1":15,"c2":25,"c3":5625658944865439256,"c4":5.71635,"c5":1.26562,"c6":false,"location":"tianjin","temperature":35.5}]}
    ```

2. 使用 kafka-console-producer 向主题 `kw-tsdb-ts_json_kaiwudb_tb` 写入测试数据。

    ```shell
    cat kw-json-kaiwudb-data.txt | ./../bin/kafka-console-producer.sh --broker-list localhost:9092 --topic kw-tsdb-ts_json_kaiwudb_tb
    ```

3. 打开 KWDB 客户端，验证是否收到数据。

    ```sql
    -- 1. 切换到 tsdb 数据库。
    
    USE tsdb;
    
    -- 2. 查看 tsdb 数据库中的表。
    
    SHOW TABLES;
    
    -- 3. 查看 tsdb 数据库中 ts_json_kaiwudb_tb 表的数据。
    
    SELECT * FROM tsdb.ts_json_kaiwudb_tb;
    ```

### 卸载 KaiwuDB Sink Connector

如需卸载 KaiwuDB Sink Connector，运行以下命令：

```shell
curl -X DELETE http://localhost:8083/connectors/KwdbSinkConnector
```

## 配置 KaiwuDB Source Connector

KaiwuDB Source Connector 将 KWDB 数据库中的数据实时推送到 Apache Kafka 主题中。KaiwuDB Source Connector 通过定期执行查询语句加载最新数据。默认情况下，时序表的数据都被推送到各自对应的输出主题。

### 前提条件

- [配置 KaiwuDB Kafka Connector](#配置-kaiwudb-kafka-connector)。
- 创建待读取数据的 KWDB 数据库。
- 配置用于连接 KWDB 数据库的用户和密码。

### 配置步骤

1. 创建 KaiwuDB Source Connector 文件，定义 Kafka 主题、KWDB 连接信息及数据格式等信息。

    以下示例创建一个名为 `kw-json-kaiwudb-source.json` 的 KaiwuDB Source Connector 文件。

    ```json
    {
      "name": "KwdbSourceConnector",
      "config": {
        "connector.class": "com.kaiwudb.kafka.connect.source.KwdbSourceConnector",
        "tasks.max": 1,
        "connection.url": "jdbc:kaiwudb://localhost:26257",
        "connection.user": "test",
        "connection.password": "Password@2024",
        "connection.database": "benchmark",
        "connection.attempts": 3,
        "connection.backoff.ms": 5000,
        "poll.interval.ms": 5000,
        "topic.prefix": "kw",
        "topic.delimiter": "-",
        "fetch.max.rows": 100,
        "query.interval.ms": 1000,
        "topic.per.stable": true,
        "topic.ignore.db": false,
        "out.format": "json_kaiwudb",
        "read.method": "query",
        "key.converter": "org.apache.kafka.connect.storage.StringConverter",
        "value.converter": "org.apache.kafka.connect.storage.StringConverter"
      }
    }
    ```

   有关 KaiwuDB Source Connector 参数配置信息，参见 [KaiwuDB Source Connector 参数配置](#kaiwudb-source-connector-参数说明)。

2. 启动 KaiwuDB Source Connector。

    ```shell
    curl -X POST -d @kw-json-kaiwudb-source.json http://localhost:8083/connectors -H "Content-Type: application/json"
    ```

    配置成功后，KaiwuDB Source Connector 根据定义的配置和规则轮询指定数据库中的表数据，将其写入到 Kafka 主题中。

### 验证 KaiwuDB Source Connector

1. 查看 Kafka 主题记录。

    ```shell
    kafka-topics.sh --bootstrap-server localhost:9092  --list
    kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic kw-benchmark-cpu_kaiwudb_tb
    ```

2. 登录 KWDB 客户端，写入测试数据。

    ```sql
    INSERT INTO benchmark.cpu_kaiwudb_tb (k_timestamp, usage_user, usage_system, usage_idle, usage_nice, usage_iowait, usage_irq, usage_softirq, usage_steal, usage_guest, usage_guest_nice, id, hostname, region, datacenter) VALUES ('2024-01-22 22:22:22.224',1,2,3,4,5,6,7,8,9,10,647470401348904608,'locahost','beijing','center');
    ```

3. 验证 Kafka 主题记录。

    ```shell
    kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic kaiwudb-benchmark-ts_line_influxdb_tb
    ```

    执行脚本后，控制台将输出以下信息：

    ```JSON
    {"table":"cpu_kaiwudb_tb","columns":[{"name":"k_timestamp","type":"TIMESTAMP","length":64},{"name":"usage_user","type":"INT8","length":64},{"name":"usage_system","type":"INT8","length":64},{"name":"usage_idle","type":"INT8","length":64},{"name":"usage_nice","type":"INT8","length":64},{"name":"usage_iowait","type":"INT8","length":64},{"name":"usage_irq","type":"INT8","length":64},{"name":"usage_softirq","type":"INT8","length":64},{"name":"usage_steal","type":"INT8","length":64},{"name":"usage_guest","type":"INT8","length":64},{"name":"usage_guest_nice","type":"INT8","length":64}],"data":[{"k_timestamp":1705962142224,"usage_user":1,"usage_system":2,"usage_idle":3,"usage_nice":4,"usage_iowait":5,"usage_irq":6,"usage_softirq":7,"usage_steal":8,"usage_guest":9,"usage_guest_nice":10,"id":647470401348904608,"hostname":"locahost","region":"beijing","datacenter":"center","rack":null,"os":null,"arch":null,"team":null,"service":null,"service_version":null,"service_environment":null}],"tags":[{"name":"id","type":"INT8","length":64,"isPrimary":true,"nullable":false},{"name":"hostname","type":"VARCHAR","length":254,"isPrimary":false,"nullable":false},{"name":"region","type":"VARCHAR","length":254,"isPrimary":false,"nullable":false},{"name":"datacenter","type":"VARCHAR","length":254,"isPrimary":false,"nullable":false},{"name":"rack","type":"VARCHAR","length":254,"isPrimary":false,"nullable":true},{"name":"os","type":"VARCHAR","length":254,"isPrimary":false,"nullable":true},{"name":"arch","type":"VARCHAR","length":254,"isPrimary":false,"nullable":true},{"name":"team","type":"VARCHAR","length":254,"isPrimary":false,"nullable":true},{"name":"service","type":"VARCHAR","length":254,"isPrimary":false,"nullable":true},{"name":"service_version","type":"VARCHAR","length":254,"isPrimary":false,"nullable":true},{"name":"service_environment","type":"VARCHAR","length":254,"isPrimary":false,"nullable":true}]}
    ```

### 卸载 KaiwuDB Source Connector

如需卸载 KaiwuDB Source Connector，运行以下命令：

```shell
curl -X DELETE http://localhost:8083/connectors/KwdbSourceConnector
```

## 参考信息

### 支持的数据格式

本节介绍 KWDB 支持的 Kafka 数据格式。

#### KWDB JSON 格式数据

::: warning 说明

- JSON 数据已包含列名、列类型和列长度等信息。如果写入数据的目标时序表不存在，KaiwuDB 支持自动创建时序表。
- Kafka 按行接收数据，不支持发送格式化的 JSON 数据。用户必须将每个完整的 JSON 对象压缩成单行字符串，确保系统能够正确解析数据。

:::

KWDB JSON 格式协议采用 JSON 字符串表示一行或多行数据。

数据示例：

```json
{"table":"ts_json_kaiwudb_tb","columns":[{"name":"ts","type":"TIMESTAMPTZ","length":64},{"name":"c1","type":"INT2","length":16},{"name":"c2","type":"INT4","length":32},{"name":"c3","type":"INT8","length":64},{"name":"c4","type":"FLOAT4","length":32},{"name":"c5","type":"FLOAT8","length":64},{"name":"c6","type":"BOOL","length":1}],"tags":[{"name":"location","type":"VARCHAR","length":64,"primary":true,"nullable":false},{"name":"temperature","type":"FLOAT4","length":64,"primary":false,"nullable":true}],"data":[{"ts":1690855924005,"c1":11,"c2":21,"c3":2535208944865431245,"c4":6.14545,"c5":5.15656,"c6":true,"location":"tianjin","temperature":35.5},{"ts":1691853703011,"c1":12,"c2":22,"c3":6422208944865124578,"c4":1.01635,"c5":0.53533,"c6":false,"location":"tianjin","temperature":35.5},{"ts":1692065524004,"c1":13,"c2":23,"c3":1542408944865124535,"c4":3.25456,"c5":2.56356,"c6":true,"location":"tianjin","temperature":35.5},{"ts":1692199303011,"c1":14,"c2":24,"c3":1245658944865439256,"c4":2.72652,"c5":5.83533,"c6":false,"location":"tianjin","temperature":35.5},{"ts":1692285703011,"c1":15,"c2":25,"c3":5625658944865439256,"c4":5.71635,"c5":1.26562,"c6":false,"location":"tianjin","temperature":35.5}]}
{"table":"ts_json_kaiwudb_tb","columns":[{"name":"ts","type":"TIMESTAMPTZ","length":64},{"name":"c1","type":"INT2","length":16},{"name":"c2","type":"INT4","length":32},{"name":"c3","type":"INT8","length":64},{"name":"c4","type":"FLOAT4","length":32},{"name":"c5","type":"FLOAT8","length":64},{"name":"c6","type":"BOOL","length":1}],"tags":[{"name":"location","type":"VARCHAR","length":64,"primary":true,"nullable":false},{"name":"temperature","type":"FLOAT4","length":64,"primary":false,"nullable":true}],"data":[{"ts":1690855924005,"c1":11,"c2":21,"c3":2535208944865431245,"c4":6.14545,"c5":5.15656,"c6":true,"location":"tianjin","temperature":35.5},{"ts":1691853703011,"c1":12,"c2":22,"c3":6422208944865124578,"c4":1.01635,"c5":0.53533,"c6":false,"location":"tianjin","temperature":35.5},{"ts":1692065524004,"c1":13,"c2":23,"c3":1542408944865124535,"c4":3.25456,"c5":2.56356,"c6":true,"location":"tianjin","temperature":35.5},{"ts":1692199303011,"c1":14,"c2":24,"c3":1245658944865439256,"c4":2.72652,"c5":5.83533,"c6":false,"location":"tianjin","temperature":35.5},{"ts":1692285703011,"c1":15,"c2":25,"c3":5625658944865439256,"c4":5.71635,"c5":1.26562,"c6":false,"location":"tianjin","temperature":35.5}]}
```

参数说明：

| 参数      | 描述                                                                                                                                                       |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `table`   | 必填参数，数据表名称。如果用户已经在 KWDB 数据库中创建时序表，表名需要与 `table` 名称保持一致。                                                         |
| `columns` | 必填参数，用于指定数据表的列名、类型、长度以及是否为空。如果用户已经在 KWDB 数据库中创建时序表，列名及相关配置需要与 `columns` 下的配置和顺序保持一致。 |
| `tags`    | 必填参数，用于指定数据表的标签名称、类型、长度、是否为主标签以及是否为空。每张表必须有一个及以上主标签，且主标签不能为空。                                 |
| `data`    | 要写入的数据集数据，对应列和标签字段。目前，timestamp 类型数据仅支持毫秒级精度。                                                                           |

#### OpenTSDB JSON 格式数据

OpenTSDB JSON 格式协议采用 JSON 字符串表示一行或多行数据。

::: warning 说明

- 由于数据格式的特性，写入的时序表名是 `table_name.column_name` 形式组成。如果写入的数据表不存在，系统将自动创建时序表。每个表的数据列只有 `timestamp` 和 `value` 两列。
- 目前，在自动创建表时，由于无法保证表对应的标签列名均一致，暂不支持对标签的处理。
- Kafka 按行接收数据，不支持发送格式化的 JSON 数据。用户必须将每个完整的 JSON 对象压缩成单行字符串，确保系统能够正确解析数据。

:::

数据示例：

```json
[{"metric":"ts_json_opentsdb_tb.c1","timestamp":1648432611249,"value":10.3,"tags":{"tag_name":"tag_value"}},{"metric":"ts_json_opentsdb_tb.c2","timestamp":1648432611339,"value":219,"tags":{"tag_name":"tag_value"}},{"metric":"ts_json_opentsdb_tb.c1","timestamp":1648432611340,"value":12.6,"tags":{"tag_name":"tag_value"}},{"metric":"ts_json_opentsdb_tb.c2","timestamp":1648432611250,"value":218,"tags":{"tag_name":"tag_value"}}]
```

参数说明：

| 参数        | 描述                                                                                                                      |
| ----------- | ------------------------------------------------------------------------------------------------------------------------- |
| `metric`    | 指定表名和列名，格式为 `table_name.column_name`。在 KWDB 数据库中创建的时序表表名需要与此处的 `metric` 中的表名一致。               |
| `timestamp` | 时间戳，支持秒（s）和毫秒（ms）两种时间精度。在 KWDB 数据库中创建的表的时间戳列需要与此处定义的 `timestamp` 名称一致。 |
| `value`     | 数据列的值。                                                                                                              |
| `tags`      | 标签信息，所有标签自动转为 `VARCHAR` 数据类型。                                                                           |

#### OpenTSDB Line 格式数据

OpenTSDB Line 格式协议采用一行字符串来表示一行数据。

OpenTSDB 采用单列模型，因此一行只能包含一个普通数据列，标签列可以有多个。

::: warning 说明

- 由于数据格式的特性，写入的时序表名是 `table_name.column_name` 形式组成。如果写入的数据表不存在，系统将自动创建时序表。每个表的数据列只有 `timestamp` 和 `value` 两列。
- 在自动创建表时，由于不能保证表对应的标签列名均一致，故暂不支持对标签的处理。

:::

数据格式如下：

```json
<metric> <timestamp> <value> <tagk_1>=<tagv_1>[ <tagk_n>=<tagv_n>]
```

参数说明：

| 参数        | 描述                                                                                                      |
| ----------- | --------------------------------------------------------------------------------------------------------- |
| `metric`    | 指定表名和列名，格式为 `table_name.column_name`。用户在 KWDB 数据库中创建时序表时，需要与此处的 `metric` 名称一致。 |
| `timestamp` | 数据对应的时间戳。支持秒（s）和毫秒（ms）两种时间精度。                                                   |
| `value`     | 度量值，对应的列名是 `value`。                                                                            |
| `tag_set`   | 标签集，标签间用半角空格隔开，所有标签自动转化为 `VARCHAR` 数据类型。                                     |

数据示例：

```shell
ts_line_opentsdb_tb.c1 1648432611249 10.3 tag1=1
ts_line_opentsdb_tb.c2 1648432611249 219 tag1=1
ts_line_opentsdb_tb.c1 1648432611250 12.6 tag1=1
ts_line_opentsdb_tb.c2 1648432611250 218 tag1=1
ts_line_opentsdb_tb.c1 1648432611249 10.8 tag1=1
ts_line_opentsdb_tb.c2 1648432611249 221 tag1=1
ts_line_opentsdb_tb.c1 1648432611250 11.3 tag1=1
ts_line_opentsdb_tb.c2 1648432611250 217 tag1=1
```

#### InfluxDB Line 格式数据

InfluxDB Line 格式协议采用一行字符串来表示一行数据。

::: warning 说明
对于 InfluxDB Line 格式数据，系统无法获取表中列和属性的类型和长度信息。因此，如果写入的数据表不存在，不支持自动创建表。
:::

数据格式如下:

```json
<measurement>[,<tag_key>=<tag_value>[,<tag_key>=<tag_value>]] <field_key>=<field_value>[,<field_key>=<field_value>] [<timestamp>]
```

参数说明：

| 参数          | 描述                                                                                                                                                                                                                                         |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `measurement` | 表名。在 KWDB 数据库中创建时序表时，表名需要与此处的表名一致。                                                                                                                                                                            |
| `tag_set`     | 标签集，格式为 `<tag_key>=<tag_value>,<tag_key>=<tag_value>`，多个标签之间使用逗号（`,`）隔开。                                                                                                                                                         |
| `field_set`   | 普通列数据，格式为 `<field_key>=<field_value>,<field_key>=<field_value>`，多列之间之间使用逗号（`,`）隔开。`field_set` 中的每个数据项都需要对自身的数据类型进行描述，例如 `1.2f32` 代表 `FLOAT` 类型的数值 `1.2`、`3.63f64` 代表 `DOUBLE` 类型的数值 `3.63` 处理，更多详细信息，参见下表。 |
| `timestamp`   | 本行数据对应的时间戳。timestamp 支持多种时间精度，写入数据的时候需要用参数指定时间精度，支持毫秒（ms）、微妙级（us）、纳秒（ns）3 种时间精度。                                                                                                       |

数据类型描述：

| 数据类型  | 描述方式  |示例                                                                                                                                                                                                                                       |
| -----------------------------------------------|----------------------------------------------|--------------------------------------------------------------------------------------------------------- |
| INT2      |  后缀添加 `i16`         | `11i16`              |
| INT4      |  后缀添加 `i32`              | `21i32`              |
| INT8 | 后缀添加 `i64` 或 `i` | `31i64`              |
| FLOAT4         | 后缀添加 `f32`                         | `1.8f32`              |
| FLOAT8    | 无需后缀，或后缀添加 `f64`                      | `0.16f64`              |
| BOOL    | 使用 `true`, `True`, `TRUE`, `false`, `False` 或  `FALSE`                    | `true`              |
| VARBYTES、CHAR、NCHAR、VARCHAR、NVARCHAR  | - 使用单引号（`'`）或双引号（`"`）包裹数据<br>- 空格、等号（`=`）、逗号（`,`）、双引号（`"`）、反斜杠（`\`）需要转义（`\`）。<br> - NCHAR 和 NVARCHAR 需要使用双引号（`"`）包裹数据，而且带有 `L` 前缀                    | - `'a'`<br>- `\"rfv\"`<br>- `L\"ikl\"` |
| TIMESTAMP    | Unix 时间戳格式，或 `\"YYYY-MM-DD HH:MI:SS.MS\"` 格式                    | `1648432611249` 或 `\"2023-08-11 12:12:10.249\"`            |

数据示例：

```json
ts_line_influxdb_tb,tag_name=tag_value c1=11i16,c2=21i32,c3=31i64,c4=11.8f32,c5=0.16f64,c6=true,c7=\"112132\",c8=\"213645\",c9='a',c10=L\"1\",c11=\"qaz\",c12=L\"tgb\",c13=1648432611249 1648432611249000000
ts_line_influxdb_tb,tag_name=tag_value c1=12i16,c2=22i32,c3=32i64,c4=12.8f32,c5=0.29f64,c6=false,c7=\"123563\",c8=\"213621\",c9='b',c10=L\"2\",c11=\"wsx\",c12=L\"yhn\",c13=\"2023-08-11 12:12:10.249\" 1648432611249000000",
ts_line_influxdb_tb,tag_name=tag_value c1=13i16,c2=23i32,c3=33i64,c4=13.8f32,c5=0.32f64,c6=true,c7=\"\\x313233\",c8=\"\\x6664736665\",c9='c',c10=L\"3\",c11=\"edc\",c12=L\"ujm\",c13=1648432611250 1648432611250000000",
ts_line_influxdb_tb,tag_name=tag_value c1=14i16,c2=24i32,c3=34i64,c4=14.8f32,c5=0.45f64,c6=false,c7=\"\\x343536\",c8=\"\\x6173646666\",c9='d',c10=L\"4\",c11=\"rfv\",c12=L\"ikl\",c13=\"2023-08-11 12:12:10.250\" 1648432611250000000"
```

### KaiwuDB Sink Connector 参数说明

| 参数 | 类型   | 描述                                                                                                                                                                                                                                 | 默认值 |
| ---------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------ |
| `name`                             | string | 连接器的名称。                                                                                                                                                                                                                                                     | -                                    |
| `connector.class`                  | string | 连接器类的名称。对于 Kafka Sink Connector，需要指定为 `com.kaiwudb.kafka.connect.sink.KwdbSinkConnector`。                                                                                                                                                         | -                                    |
| `tasks.max`                        | int    | 连接器支持运行的任务数量。                                                                                                                                                                                                                                         | 1                                    |
| `topics`                           | string | 用来组织消息的类别，多个主题之间使用英文逗号（`,`）隔开。                                                                                                                                                                                                              | -                                    |
| `connection.url`                   | string | KaiwuDB JDBC 连接 URL。                                                                                                                                                                                                                                         | -                                    |
| `connection.user`                  | string | KaiwuDB JDBC 连接用户名。                                                                                                                                                                                                                                       | -                                    |
| `connection.password`              | string | KaiwuDB JDBC 的连接密码。                                                                                                                                                                                                                                       | -                                    |
| `connection.database`              | string | 待写入数据的 KWDB 数据库。                                                                                                                                                                                                                                      | -                                    |
| `connection.attempts`              | int    | JDBC 连接的最大尝试次数，必须是正整数。                                                                                                                                                                                                                            | 3                                    |
| `connection.backoff.ms`            | int    | 连接尝试之间的退回时间（单位：毫秒）。                                                                                                                                                                                                                       | 5000                                 |
| `max.retries`                      | int    | 任务失败之前，最大重试次数。                                                                                                                                                                                                                                       | 3                                    |
| `retry.backoff.ms`                 | int    | 发生错误后，重试之前的等待时间（单位：毫秒）。                                                                                                                                                                                                               | 3                                    |
| `batch.size`                       | int    | 批量插入目标表的记录数量。                                                                                                                                                                                                                                         | 1000                                 |
| `protocol.type`                    | string | 写入 KWDB 的数据格式，支持 `json_kaiwudb`、`json_opentsdb`、`line_opentsdb`、`line_influxdb`。更多信息，参见[支持的数据格式](#支持的数据格式)。                                                                                                                 | -                                    |
| `timestamp.precision`              | string | 写入 KWDB 的数据时间精度，支持秒（s）、毫秒（ms）、微妙（us）、纳秒（ns）。其中 <br >- `json_kaiwudb`：支持毫秒（ms）。 <br >- `line_influxdb`：支持毫秒（ms）、微妙（us）、纳秒（ns）。<br >-`json_opentsdb` 和 `line_opentsdb`：支持秒（s）、毫秒（ms）。 | -                                    |
| `key.converter`                    | string | 在 Kafka Connect 格式和从 Kafka 读取的序列化格式之间进行转换的转换类。                                                                                                                                                                                             | -                                    |
| `value.converter`                  | string | 在 Kafka Connect 格式和从 Kafka 读取的序列化格式之间进行转换的转换类。                                                                                                                                                                                             | -                                    |

### KaiwuDB Source Connector 参数说明

| 参数 | 类型   | 描述                                                                               | 默认值 |
| ---------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `name`                             | string | 连接器的名称。                                                                                                   | -                                    |
| `connector.class`                  | string | 连接器类的名称。对于 Kafka Source Connector，需要指定为 `com.kaiwudb.kafka.connect.source.KwdbSourceConnector`。 | -                                    |
| `tasks.max`                        | int    | 连接器支持运行的任务数量。                                                                                       | 1                                    |
| `connection.url`                   | string | KaiwuDB JDBC 连接 URL。                                                                                       | -                                    |
| `connection.user`                  | string | KaiwuDB JDBC 的连接用户名。                                                                                   | -                                    |
| `connection.password`              | string | KaiwuDB JDBC 的连接密码。                                                                                     | -                                    |
| `connection.database`              | string | 待读取数据的 KWDB 数据库。                                                                                    | -                                    |
| `connection.attempts`              | int    | JDBC 连接的最大尝试次数，必须是正整数。                                                                          | 3                                    |
| `connection.backoff.ms`            | int    | 连接尝试之间的退回时间（单位：毫秒）。                                                                     | 5000                                 |
| `topic.prefix`                     | string | 主题名称的前缀，用于生成要发布到的 Kafka 主题名称。默认生成的主题名是前缀+库名+表名+输出格式。                   | -                                    |
| `topic.delimiter`                  | string | 主题名称分隔符，默认为连字符（`-`）。                                                                                      | -                                    |
| `timestamp.initial`                | string | 用于查询的初始时间戳，格式为 `yyyy-MM-dd HH:MM:SS`。未指定时，将检索表中所有数据。                               | -                                    |
| `poll.interval.ms`                 | int    | 轮询新表或删除表的频率（单位：毫秒）。                                                                     | 5000                                 |
| `fetch.max.rows`                   | int    | 单次轮询获取新数据时最大检索行数。此设置用于限制连接器内部缓存的数据量。                                         | 100                                  |
| `query.interval.ms`                | int    | 单次查询起止时间间隔。                                                                                           | 1000                                 |
| `topic.per.stable`                 | bool   | 是否为每张表创建一个主题。                                                                                       | true                                 |
| `topic.ignore.db`                  | bool   | 命名主题时，忽略数据库名。建议保持默认值 `false`。                                                               | false                                |
| `out.format`                       | string | 结果输出格式。支持`json_kaiwudb`、`json_opentsdb`、`line_opentsdb`、`line_influxdb` 格式。                       | -                                    |
| `read.method`                      | string | 获取数据的方式，目前只支持 query。                                                                               | -                                    |
| `key.converter`                    | string | 在 Kafka Connect 格式和从 Kafka 读取的序列化格式之间进行转换的转换类。                                           | -                                    |
| `value.converter`                  | string | 在 Kafka Connect 格式和从 Kafka 读取的序列化格式之间进行转换的转换类。                                           | -                                    |

### 故障诊断与排查

有关详细信息，参见 [Kafka Connect 故障排查](../../troubleshooting-guide/troubleshooting.md#kafka-connect)。
