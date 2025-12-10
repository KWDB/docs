---
title: Kafka
id: kafka
---

# Kafka

KWDB offers bidirectional data transfer with Apache Kafka through the KaiwuDB Kafka Connector. Built on the Kafka Connect API and Confluent platform, the connector consists of two components:

- **KaiwuDB Sink Connector**: Transfers data from Kafka topics to KWDB in batch or real-time mode.
- **KaiwuDB Source Connector**: Exports data from KWDB databases to Kafka topics in batch or real-time mode.

## Configure KaiwuDB Kafka Connector

KaiwuDB Kafka Connector is currently supported only on Linux operating systems.

### Prerequisites

- [OpenJDK 1.8 or higher](https://openjdk.org/install/)
- [Maven 3.6 or higher](https://maven.apache.org/install.html)
- [Kafka 3.4.1 or higher](https://kafka.apache.org/) with `$KAFKA_HOME/bin` in your system PATH:

  ```shell
  # Open the profile file
  vi ~/.profile

  # Add the following configuration
  export KAFKA_HOME=/opt/kafka
  export PATH=$PATH:$KAFKA_HOME/bin
  ```

- KWDB database installed and configured with appropriate authentication
- KaiwuDB Kafka Connector installation package

### Steps

1. Extract the KaiwuDB Kafka Connector package to Kafka's `components/` directory:

    ```shell
    unzip -d $KAFKA_HOME/components/ target/components/packages/kaiwudb-kafka-connect-*.zip
    ```

2. Configure Kafka to recognize the connector by adding the path to `plugin.path` in `$KAFKA_HOME/config/connect-distributed.properties`:

    ```shell
    plugin.path=/usr/share/java,/opt/kafka/components
    ```

3. Navigate to Kafka's `bin` directory and start the Kafka services:

    ```shell
    ./zookeeper-server-start.sh -daemon $KAFKA_HOME/config/zookeeper.properties
    ./kafka-server-start.sh -daemon $KAFKA_HOME/config/server.properties
    ./connect-distributed.sh -daemon $KAFKA_HOME/config/connect-distributed.properties
    ```

4. Verify that Kafka has started successfully:

    ```shell
    curl http://localhost:8083/connectors
    ```

   If the components have started successfully, you should see an empty array:

    ```shell
    []
    ```

    ::: tip

    Here are some useful Kafka topic management commands:

    - List all topics: `./kafka-topics.sh --bootstrap-server localhost:9092 --list`
    - View data in a specific topic: `./kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic kw-tsdb-json_kaiwudb_with_tag_tb`
    - Delete a topic: `./kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic kw-tsdb-json_kaiwudb_with_tag_tb`

    :::

## Configure KaiwuDB Sink Connector

The KaiwuDB Sink Connector transfers data from specified Kafka topics to the KWDB database.

When writing data to time-series databases, the following formats are supported:

- [KaiwuDB JSON Format](#kaiwudb-json-format)
- [OpenTSDB JSON Format](#opentsdb-json-format)
- [OpenTSDB Telnet Format](#opentsdb-telnet-format)
- [InfluxDB Line Format](#influxdb-line-format)

When writing data to relational databases, the [KaiwuDB JSON Format](#kaiwudb-json-format) is supported.

### Prerequisites

- Complete the [KaiwuDB Kafka Connector configuration](#configure-kaiwudb-kafka-connector).
- Create the target KWDB database.
- Set up authentication credentials (user and password) for KWDB database access.

::: warning Note
KWDB supports automatic creation of time-series or relational tables based on the data format. When the target table does not exist, the system will automatically create the corresponding table structure, except when using the InfluxDB Line format.
:::

### Steps

1. (Optional) Create a custom Kafka topic for multi-tasking scenarios. Skip this step if you don't need multi-task support.

    The following example creates a topic named `kw-tsdb-json_kaiwudb_with_tag_tb` with 5 partitions.

    ::: warning Note

    The number of partitions should match or exceed the `tasks.max` parameter in your Sink Connector configuration. For example, with `tasks.max: 5`, use at least 5 partitions.

    :::

    ```shell
    ./kafka-topics.sh --create --topic kw-tsdb-json_kaiwudb_with_tag_tb --partitions 5 --bootstrap-server localhost:9092
    ```

2. Create a KaiwuDB Sink Connector configuration file (e.g., `kw-json-kaiwudb-sink.json`), defining Kafka topics, KWDB connection details, and data format.

    ```json
    {
      "name": "KwdbSinkConnector",
      "config": {
        "connector.class": "com.kaiwudb.kafka.connect.sink.KwdbSinkConnector",
        "tasks.max": "5",
        "topics": "kw-tsdb-json_kaiwudb_with_tag_tb",
        "connection.url": "jdbc:kaiwudb://localhost:26257",
        "connection.user": "test",
        "connection.password": "<password>",
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

    For more information on the parameters of KaiwuDB Sink Connector, see [KaiwuDB Sink Connector Parameters](#kaiwudb-sink-connector-parameters).

3. Deploy the KaiwuDB Sink Connector:

   ```shell
   curl -X POST -d @kw-json-kaiwudb-sink.json http://localhost:8083/connectors -H "Content-Type: application/json"
   ```

   Once configured, the connector will automatically write messages from the Kafka topic to the KWDB database.

### Testing and Verification

1. Prepare test data in a file named `kw-json-kaiwudb-data.txt`:

    ::: warning Note
    Kafka processes data line by line and does not support formatted JSON data. Each complete JSON object must be compressed into a single-line string to ensure correct parsing.
    :::

    ```json
    {"table":"ts_json_kaiwudb_tb","columns":[{"name":"ts","type":"TIMESTAMPTZ","length":64},{"name":"c1","type":"INT2","length":16},{"name":"c2","type":"INT4","length":32},{"name":"c3","type":"INT8","length":64},{"name":"c4","type":"FLOAT4","length":32},{"name":"c5","type":"FLOAT8","length":64},{"name":"c6","type":"BOOL","length":1}],"tags":[{"name":"location","type":"VARCHAR","length":64,"primary":true,"nullable":false},{"name":"temperature","type":"FLOAT4","length":64,"primary":false,"nullable":true}],"data":[{"ts":1690855924005,"c1":11,"c2":21,"c3":2535208944865431245,"c4":6.14545,"c5":5.15656,"c6":true,"location":"tianjin","temperature":35.5},{"ts":1691853703011,"c1":12,"c2":22,"c3":6422208944865124578,"c4":1.01635,"c5":0.53533,"c6":false,"location":"tianjin","temperature":35.5},{"ts":1692065524004,"c1":13,"c2":23,"c3":1542408944865124535,"c4":3.25456,"c5":2.56356,"c6":true,"location":"tianjin","temperature":35.5},{"ts":1692199303011,"c1":14,"c2":24,"c3":1245658944865439256,"c4":2.72652,"c5":5.83533,"c6":false,"location":"tianjin","temperature":35.5},{"ts":1692285703011,"c1":15,"c2":25,"c3":5625658944865439256,"c4":5.71635,"c5":1.26562,"c6":false,"location":"tianjin","temperature":35.5}]}
    ```

2. Send the test data to your Kafka topic:

    ```shell
    cat kw-json-kaiwudb-data.txt | ./../bin/kafka-console-producer.sh --broker-list localhost:9092 --topic kw-tsdb-json_kaiwudb_with_tag_tb
    ```

3. Verify that the data has been written to KWDB:

    ```sql
    -- Switch to the target database
    USE tsdb;
    
    -- List available tables
    SHOW TABLES;
    
    -- Query the data
    SELECT * FROM tsdb.ts_json_kaiwudb_tb;
    ```

### Uninstalling KaiwuDB Sink Connector

To remove the KaiwuDB Sink Connector:

```shell
curl -X DELETE http://localhost:8083/connectors/KwdbSinkConnector
```

## Configure KaiwuDB Source Connector

The KaiwuDB Source Connector exports data from KWDB databases to Apache Kafka topics through periodic queries. It automatically retrieves the latest data at configurable intervals and publishes time-series data to designated Kafka topics. By default, data from each time-series table is published to its corresponding independent topic.

### Prerequisites

- Complete the [KaiwuDB Kafka Connector configuration](#configure-kaiwudb-kafka-connector).
- Ensure the source KWDB database contains data to be exported.
- Set up authentication credentials (user and password) for KWDB database access.

### Steps

1. Create a KaiwuDB Source Connector configuration file (e.g., `kw-json-kaiwudb-source.json`) defining Kafka topic, KWDB connection, and data format.

    ```json
    {
      "name": "KwdbSourceConnector",
      "config": {
        "connector.class": "com.kaiwudb.kafka.connect.source.KwdbSourceConnector",
        "tasks.max": 1,
        "connection.url": "jdbc:kaiwudb://localhost:26257",
        "connection.user": "test",
        "connection.password": "<password>",
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

    For more information on the parameters of KaiwuDB Source Connector, see [KaiwuDB Source Connector Parameters](#kaiwudb-source-connector-parameters).

2. Deploy the KaiwuDB Source Connector:

    ```shell
    curl -X POST -d @kw-json-kaiwudb-source.json http://localhost:8083/connectors -H "Content-Type: application/json"
    ```

    After deployment, the connector will automatically extract data from the specified database and stream it to the designated Kafka topic.

### Testing and Verification

1. Check available Kafka topics and monitor the output:

    ```shell
    kafka-topics.sh --bootstrap-server localhost:9092  --list
    kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic kw-benchmark-cpu_kaiwudb_tb
    ```

2. Log in to KWDB and insert test data:

    ```sql
    INSERT INTO benchmark.cpu_kaiwudb_tb (k_timestamp, usage_user, usage_system, usage_idle, usage_nice, usage_iowait, usage_irq, usage_softirq, usage_steal, usage_guest, usage_guest_nice, id, hostname, region, datacenter) VALUES ('2024-01-22 22:22:22.224',1,2,3,4,5,6,7,8,9,10,647470401348904608,'locahost','beijing','center');
    ```

3. Verify that the data appears in the Kafka topic:

    ```shell
    kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic kaiwudb-benchmark-ts_line_influxdb_tb
    ```

    You should see output similar to:

    ```json
    {"table":"cpu_kaiwudb_tb","columns":[{"name":"k_timestamp","type":"TIMESTAMP","length":64},{"name":"usage_user","type":"INT8","length":64},{"name":"usage_system","type":"INT8","length":64},{"name":"usage_idle","type":"INT8","length":64},{"name":"usage_nice","type":"INT8","length":64},{"name":"usage_iowait","type":"INT8","length":64},{"name":"usage_irq","type":"INT8","length":64},{"name":"usage_softirq","type":"INT8","length":64},{"name":"usage_steal","type":"INT8","length":64},{"name":"usage_guest","type":"INT8","length":64},{"name":"usage_guest_nice","type":"INT8","length":64}],"data":[{"k_timestamp":1705962142224,"usage_user":1,"usage_system":2,"usage_idle":3,"usage_nice":4,"usage_iowait":5,"usage_irq":6,"usage_softirq":7,"usage_steal":8,"usage_guest":9,"usage_guest_nice":10,"id":647470401348904608,"hostname":"locahost","region":"beijing","datacenter":"center","rack":null,"os":null,"arch":null,"team":null,"service":null,"service_version":null,"service_environment":null}],"tags":[{"name":"id","type":"INT8","length":64,"isPrimary":true,"nullable":false},{"name":"hostname","type":"VARCHAR","length":254,"isPrimary":false,"nullable":false},{"name":"region","type":"VARCHAR","length":254,"isPrimary":false,"nullable":false},{"name":"datacenter","type":"VARCHAR","length":254,"isPrimary":false,"nullable":false},{"name":"rack","type":"VARCHAR","length":254,"isPrimary":false,"nullable":true},{"name":"os","type":"VARCHAR","length":254,"isPrimary":false,"nullable":true},{"name":"arch","type":"VARCHAR","length":254,"isPrimary":false,"nullable":true},{"name":"team","type":"VARCHAR","length":254,"isPrimary":false,"nullable":true},{"name":"service","type":"VARCHAR","length":254,"isPrimary":false,"nullable":true},{"name":"service_version","type":"VARCHAR","length":254,"isPrimary":false,"nullable":true},{"name":"service_environment","type":"VARCHAR","length":254,"isPrimary":false,"nullable":true}]}
    ```

### Uninstalling KaiwuDB Source Connector

To remove the KaiwuDB Source Connector:

```shell
curl -X DELETE http://localhost:8083/connectors/KwdbSourceConnector
```

## References

### Supported Data Formats

KWDB supports multiple data formats for integration with Kafka.

#### KaiwuDB JSON Format

This format uses a JSON string to represent one or more rows of data, including detailed schema information.

::: warning Note

- JSON data includes information about column names, types, and lengths. If the target time-series or relational table does not exist, KWDB will automatically create it.
- Kafka processes data line by line. Each complete JSON object must be compressed into a single-line string.

:::

Example:

```json
{"table":"ts_json_kaiwudb_tb","columns":[{"name":"ts","type":"TIMESTAMPTZ","length":64},{"name":"c1","type":"INT2","length":16},{"name":"c2","type":"INT4","length":32},{"name":"c3","type":"INT8","length":64},{"name":"c4","type":"FLOAT4","length":32},{"name":"c5","type":"FLOAT8","length":64},{"name":"c6","type":"BOOL","length":1}],"tags":[{"name":"location","type":"VARCHAR","length":64,"primary":true,"nullable":false},{"name":"temperature","type":"FLOAT4","length":64,"primary":false,"nullable":true}],"data":[{"ts":1690855924005,"c1":11,"c2":21,"c3":2535208944865431245,"c4":6.14545,"c5":5.15656,"c6":true,"location":"tianjin","temperature":35.5},{"ts":1691853703011,"c1":12,"c2":22,"c3":6422208944865124578,"c4":1.01635,"c5":0.53533,"c6":false,"location":"tianjin","temperature":35.5},{"ts":1692065524004,"c1":13,"c2":23,"c3":1542408944865124535,"c4":3.25456,"c5":2.56356,"c6":true,"location":"tianjin","temperature":35.5},{"ts":1692199303011,"c1":14,"c2":24,"c3":1245658944865439256,"c4":2.72652,"c5":5.83533,"c6":false,"location":"tianjin","temperature":35.5},{"ts":1692285703011,"c1":15,"c2":25,"c3":5625658944865439256,"c4":5.71635,"c5":1.26562,"c6":false,"location":"tianjin","temperature":35.5}]}
{"table":"ts_json_kaiwudb_tb","columns":[{"name":"ts","type":"TIMESTAMPTZ","length":64},{"name":"c1","type":"INT2","length":16},{"name":"c2","type":"INT4","length":32},{"name":"c3","type":"INT8","length":64},{"name":"c4","type":"FLOAT4","length":32},{"name":"c5","type":"FLOAT8","length":64},{"name":"c6","type":"BOOL","length":1}],"tags":[{"name":"location","type":"VARCHAR","length":64,"primary":true,"nullable":false},{"name":"temperature","type":"FLOAT4","length":64,"primary":false,"nullable":true}],"data":[{"ts":1690855924005,"c1":11,"c2":21,"c3":2535208944865431245,"c4":6.14545,"c5":5.15656,"c6":true,"location":"tianjin","temperature":35.5},{"ts":1691853703011,"c1":12,"c2":22,"c3":6422208944865124578,"c4":1.01635,"c5":0.53533,"c6":false,"location":"tianjin","temperature":35.5},{"ts":1692065524004,"c1":13,"c2":23,"c3":1542408944865124535,"c4":3.25456,"c5":2.56356,"c6":true,"location":"tianjin","temperature":35.5},{"ts":1692199303011,"c1":14,"c2":24,"c3":1245658944865439256,"c4":2.72652,"c5":5.83533,"c6":false,"location":"tianjin","temperature":35.5},{"ts":1692285703011,"c1":15,"c2":25,"c3":5625658944865439256,"c4":5.71635,"c5":1.26562,"c6":false,"location":"tianjin","temperature":35.5}]}
```

Parameter Descriptions:

| Parameter      | Description                                                                                                                                            |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `table`   | Required. The name of the time-series or relational table. If the table already exists in KWDB, it must match this name.                                                         |
| `columns` | Required. Specifies column names, types, lengths, and nullability. If the table already exists, these must match the structure of the existing table. |
| `tags`    | Optional. Specifies tag names, types, lengths, primary status, and nullability. For time-series databases, each table must have at least one non-nullable primary tag. For relational databases, this parameter can be set to null or omitted.                                 |
| `data`    | The dataset to write. Corresponds to column and tag fields. For time-series databases, timestamp supports millisecond, microsecond, and nanosecond precision. For relational databases, timestamp currently only supports millisecond precision. In relational databases, timestamp values must be in string format; numeric timestamp format is not supported.                                                             |

#### OpenTSDB JSON Format

This format uses a JSON string to represent one or more rows of data following the OpenTSDB specification. For more information, see [OpenTSDB API Documentation](https://opentsdb.net/docs/build/html/api_http/put.html).

::: warning Note

- Time-series table names follow the `table_name.column_name` structure. If the target table doesn't exist, it will be automatically created.
- Each time-series table will have `timestamp` and `value` columns. These columns and all tag fields are stored as `VARCHAR`.
- Kafka processes data line by line. Each complete JSON object must be compressed into a single-line string.

:::

Example:

```json
[{"metric":"ts_json_opentsdb_tb.c1","timestamp":1648432611249,"value":10.3,"tags":{"tag_name":"tag_value"}},{"metric":"ts_json_opentsdb_tb.c2","timestamp":1648432611339,"value":219,"tags":{"tag_name":"tag_value"}},{"metric":"ts_json_opentsdb_tb.c1","timestamp":1648432611340,"value":12.6,"tags":{"tag_name":"tag_value"}},{"metric":"ts_json_opentsdb_tb.c2","timestamp":1648432611250,"value":218,"tags":{"tag_name":"tag_value"}}]
```

Parameter Descriptions:

| Parameter        | Description                                                                                                                      |
| ----------- | ------------------------------------------------------------------------------------------------------------------------- |
| `metric`    | Specifies the table and column name in the format `table_name.column_name`. The table name must match the one in KWDB.               |
| `timestamp` | Timestamp, supporting second (`s`) and millisecond (`ms`) precision. Must match the `timestamp` column name in the KWDB table. |
| `value`     | Column value. Must be of type `INTEGER`, `FLOAT`, `BOOLEAN`, or `STRING`.                                                                                                         |
| `tags`      | Tag information. All tag data types are automatically converted to `VARCHAR`.                                                              |

#### OpenTSDB Telnet Format

This format uses a single-line string to represent one row of data, following the OpenTSDB Telnet specification. Each row contains only one data column but can include multiple tag columns. For more information, see [OpenTSDB Telnet API Documentation](https://opentsdb.net/docs/build/html/api_telnet/put.html).

::: warning Note

- Time-series table names follow the `table_name.column_name` structure.
- If the target table doesn't exist, it will be automatically created with `timestamp` and `value` columns.
- All columns, including tags, are stored as `VARCHAR`.

:::

Format:

```json
<metric> <timestamp> <value> <tagk_1>=<tagv_1>[<tagk_n>=<tagv_n>]
```

Parameter Descriptions:

| Parameter       | Description                                                                                                      |
| ----------- | --------------------------------------------------------------------------------------------------------- |
| `metric`    | Specifies table and column in `table_name.column_name` format. Must match the existing table in KWDB. |
| `timestamp` | Time of the data point, supporting second (`s`) and millisecond (`ms`) precision.                                          |
| `value`     | Metric value. Must be of type `INTEGER` or `FLOAT`. |
| `tag_set`   | A set of tags separated by spaces. All tags are automatically converted to `VARCHAR`.                                   |

Example:

```shell
line_opentsdb_tb.c1 1648432611249 10.3 tag1=1
line_opentsdb_tb.c2 1648432611249 219 tag1=1
line_opentsdb_tb.c1 1648432611250 12.6 tag1=1
line_opentsdb_tb.c2 1648432611250 218 tag1=1
line_opentsdb_tb.c1 1648432611249 10.8 tag1=1
line_opentsdb_tb.c2 1648432611249 221 tag1=1
line_opentsdb_tb.c1 1648432611250 11.3 tag1=1
line_opentsdb_tb.c2 1648432611250 217 tag1=1
```

#### InfluxDB Line Format

This format uses a single-line string to represent one row of data in InfluxDB Line Protocol format.

::: warning Note
For this format, the system cannot infer the types and lengths of columns and tags. Therefore, if the target table does not exist, it will not be created automatically.
:::

Format:

```json
<measurement>[,<tag_key>=<tag_value>[,<tag_key>=<tag_value>]] <field_key>=<field_value>[,<field_key>=<field_value>] [<timestamp>]
```

Parameter Descriptions:

| Parameter          | Description                                                                                                                                                                                                                                         |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `measurement` | Table name. Must match the existing table in KWDB.                                                                                                                                                                 |
| `tag_set`     | A set of tags in the format `<key>=<value>`, separated by commas.                                                                                                                                                   |
| `field_set`   | Column data in the format `<field_key>=<field_value>`, separated by commas. Each value must include its data type suffix (see table below). |
| `timestamp`   | Timestamp of the data. Supports millisecond (`ms`), microsecond (`us`), and nanosecond (`ns`) precision.                                                                                                 |

Data type specifications:

| Type          | Format | Example |
|---------------|--------|---------|
| INT2          | `i16` suffix | `11i16` |
| INT4          | `i32` suffix | `21i32` |
| INT8          | `i64` or `i` suffix | `31i64` |
| FLOAT4        | `f32` suffix | `1.8f32` |
| FLOAT8        | `f64` or none | `0.16f64` |
| BOOL          | `true`, `false` (case-insensitive) | `true` |
| VARBYTES, CHAR, NCHAR, VARCHAR, NVARCHAR  | - Data must be enclosed in single (`'`) or double (`"`) quotes. <br>- Special characters (space, `=`, `,`, `"`, `\`) must be escaped with a backslash. <br>- For `NCHAR`/`NVARCHAR`, use double (`"`) quotes with the `L` prefix.| `'a'`, `\"rfv\"`, `L\"ikl\"` |
| TIMESTAMP     | A Unix timestamp or a string formatted as `"YYYY-MM-DD HH:MI:SS.MS"`. | `1648432611249`, `"2023-08-11 12:12:10.249"` |

Example:

```json
ts_line_influxdb_tb,tag_name=tag_value c1=11i16,c2=21i32,c3=31i64,c4=11.8f32,c5=0.16f64,c6=true,c7=\"112132\",c8=\"213645\",c9='a',c10=L\"1\",c11=\"qaz\",c12=L\"tgb\",c13=1648432611249 1648432611249000000
ts_line_influxdb_tb,tag_name=tag_value c1=12i16,c2=22i32,c3=32i64,c4=12.8f32,c5=0.29f64,c6=false,c7=\"123563\",c8=\"213621\",c9='b',c10=L\"2\",c11=\"wsx\",c12=L\"yhn\",c13=\"2023-08-11 12:12:10.249\" 1648432611249000000",
ts_line_influxdb_tb,tag_name=tag_value c1=13i16,c2=23i32,c3=33i64,c4=13.8f32,c5=0.32f64,c6=true,c7=\"\\x313233\",c8=\"\\x6664736665\",c9='c',c10=L\"3\",c11=\"edc\",c12=L\"ujm\",c13=1648432611250 1648432611250000000",
ts_line_influxdb_tb,tag_name=tag_value c1=14i16,c2=24i32,c3=34i64,c4=14.8f32,c5=0.45f64,c6=false,c7=\"\\x343536\",c8=\"\\x6173646666\",c9='d',c10=L\"4\",c11=\"rfv\",c12=L\"ikl\",c13=\"2023-08-11 12:12:10.250\" 1648432611250000000"
```

### KaiwuDB Sink Connector Parameters

| Parameter | Type   | Description                                                                                                                                                                                                                                 | Default Value |
| ---------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------ |
| `name`                             | string | Name of the connector.                                                                                                                                                                                                                                                     | -                                    |
| `connector.class`                  | string | Class name of the connector. For Kafka Sink Connector, set to `com.kaiwudb.kafka.connect.sink.KwdbSinkConnector`.                                                                                                                                          | -                                    |
| `tasks.max`                        | int    | Maximum number of tasks that the connector can run.                                                                                                                                                                                                                                         | 1                                    |
| `topics`                           | string | Kafka topics to consume data from. Separate multiple topics with commas (`,`).                                                                                                                                                                                                 | -                                    |
| `connection.url`                   | string | JDBC connection URL used to connect to KWDB.                                                                                                                           | -                                    |
| `connection.user`                  | string | Username used for the KaiwuDB JDBC connection.                                                                                                                                                                                                                                      | -                                    |
| `connection.password`              | string | Password used for the KaiwuDB JDBC connection.                                                                                                                                                                                                                 | -                                    |
| `connection.database`              | string | KWDB database to write data into.                                                                                                                                                                                            | -                                    |
| `connection.attempts`              | int    | Maximum number of attempts for JDBC connection. Must be a positive integer.                                                                                                                                                                                | 3                                    |
| `connection.backoff.ms`            | int    | Backoff time between connection attempts (in milliseconds).                                                                                                                                                                                       | 5000                                 |
| `max.retries`                      | int    | Maximum number of retries before a task fails.                                                                                                                                                                                              | 3                                    |
| `retry.backoff.ms`                 | int    | Wait time before retrying after an error (in milliseconds).                                                                                                                                                                   | 3                                    |
| `batch.size`                       | int    | Maximum number of records to insert in one batch operation.                                                                                                                                                                                                                                  | 1000                                 |
| `protocol.type`                    | string | Data format to write into KWDB. For time-series databases: `json_kaiwudb`, `json_opentsdb`, `line_opentsdb`, `line_influxdb`. For relational databases: `json_kaiwudb`. For more information, see [Supported Data Formats](#supported-data-formats).                                                                                                          | -                                    |
| `timestamp.precision`              | string | Precision of timestamps written to KWDB: <br>- `json_kaiwudb`: time-series databases support `ms`, `us`, `ns`; relational databases support `ms` only <br>- `line_influxdb`: supports `ms`, `us`, `ns`<br>- `json_opentsdb` and `line_opentsdb`: support `s`, `ms` | -                                    |
| `key.converter`                    | string | Converter class for transforming between Kafka Connect format and the serialization format read from Kafka.                                                                                                                                                   | -                                    |
| `value.converter`                  | string | Converter class for transforming between Kafka Connect format and the serialization format read from Kafka.                                                                                                                                                 | -                                    |

### KaiwuDB Source Connector Parameters

| Parameter | Type   | Description                                                                                                                                                                                                                                 | Default Value |
| ---------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `name`                             | string | Name of the connector.                                                     | -                                    |
| `connector.class`                  | string | Class name of the connector. For Kafka Source Connector, set to `com.kaiwudb.kafka.connect.source.KwdbSourceConnector`. | -                                    |
| `tasks.max`                        | int    | Maximum number of tasks that the connector can run.                                           | 1                                    |
| `connection.url`                   | string | JDBC connection URL used to connect to KWDB.                                                                                  | -                                    |
| `connection.user`                  | string |  Username used for the KaiwuDB JDBC connection.                                                                         | -                                    |
| `connection.password`              | string | Password used for the KaiwuDB JDBC connection.                                                                             | -                                    |
| `connection.database`              | string | KWDB time-series database to read data from.                                        | -                                    |
| `connection.attempts`              | int    | Maximum number of attempts for JDBC connection. Must be a positive integer.                             | 3                                    |
| `connection.backoff.ms`            | int    | Backoff time between connection attempts (in milliseconds).                           | 5000                                 |
| `topic.prefix`                     | string | Prefix for Kafka topic names. By default, topic names are generated using the pattern: `[prefix]+[database]+[table]+[format]`.                   | -                                    |
| `topic.delimiter`                  | string | Delimiter for topic names. Default is hyphen.                                           | `-`                                    |
| `timestamp.initial`                | string | Initial timestamp for queries. Format: `yyyy-MM-dd HH:MM:SS`. If unspecified, all data in the table will be retrieved.                                    | -                                    |
| `poll.interval.ms`                 | int    | Frequency to poll for new or dropped tables (in milliseconds).                                                        | 5000                                 |
| `fetch.max.rows`                   | int    | Maximum number of rows to fetch per polling for new data. Limits the internal cache size of the connector.                | 100                                  |
| `query.interval.ms`                | int    | Time interval between consecutive queries (in milliseconds).                                         | 1000                                 |
| `topic.per.stable`                 | bool   | Whether to create a separate topic for each table.                    | true                                 |
| `topic.ignore.db`                  | bool   | Whether to ignore the database name when naming the topic. It is recommended to keep the default value `false`.                         | false                                |
| `out.format`                       | string | Output format. Supported formats: `json_kaiwudb`, `json_opentsdb`, `line_opentsdb`, `line_influxdb`.                       | -                                    |
| `read.method`                      | string | Method to fetch data. Currently, only `query` is supported.                                       | -                                    |
| `key.converter`                    | string | Converter class for transforming between Kafka Connect format and the serialization format written to Kafka.                                          | -                                    |
| `value.converter`                  | string | Converter class for transforming between Kafka Connect format and the serialization format written to Kafka.                               | -                                    |

### Troubleshooting

For additional troubleshooting information, see [Troubleshooting Kafka Connector](../../troubleshooting-guide/troubleshooting.md#kafka-connect).