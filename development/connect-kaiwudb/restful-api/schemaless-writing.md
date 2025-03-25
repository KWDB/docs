---
title: 无模式写入
id: schemaless-writing
---

# 无模式写入

无模式写入（Schemaless Writing） 是一种灵活的数据库写入方式，允许用户在未预定义数据结构或模式的情况下，直接将数据写入数据库。数据库会根据写入数据的格式和内容自动解析数据，在没有表的情况下自动建表并写入数据。此外，当列数变多，数据库也会自动使用 `ALTER TABLE ... ADD COLUMN` 或者 `ALTER TABLE ... ADD TAG` SQL 语句添加数据列或标签列，然后再写入数据。这种方式使得数据库能够更灵活地处理数据。

::: warning 注意

在分布式集群中执行无模式写入时，有极小概率会出现节点宕机。

:::


## 无模式写入的处理逻辑

KWDB 支持通过 RESTful API 接口无模式写入 InfluxDB Line 格式的数据、OpenTSDB Telnet 格式的数据以及 OpenTSDB JSON 格式的数据。

1. 按照不同的协议格式解析输入的数据，得到目标表名、数据列名、标签列、数据及数据类型。
2. 根据解析的数据，按照语法规则生成 SQL 语句。
3. 执行 `INSERT` 语句，写入数据。
    1. 无模式写入的表名大小写敏感，支持数字和特殊符号开头的表名。
    2. 无模式写入的列名大小写敏感，支持数字和特殊符号开头的列名。
    3. 如果目标表不存在，系统自动创建目标表，然后再写入数据。
    4. 如果目标表存在且可用，系统检查指定列是否存在，以及列的类型和宽度是否相等。如果列不存在或者输入类型宽度大于列类型宽度，系统执行 `ALTER TABLE ... ADD CLOUM/ALTER TYPE` SQL 语句添加列或修改列的类型。对于 VARCHAR 类型的数据，系统自动补齐其长度。

### InfluxDB Line 格式的数据

InfluxDB Line 格式的数据如下所示：

```json
<measurement>,<tag_set> <field_set> <timestamp>
```

参数说明：

- `measurement`：必填参数，用于指定 KWDB 的时序表名。KWDB 根据该字段确定是否需要创建新表或向现有时序表中写入数据。解析时，KWDB 使用英文双引号（`""`）将时序表名包裹起来，从而解决大小写敏感或以特殊字符、数字开头的表名等问题。如果指定的时序表名不存在，KWDB 先创建该表，然后写入数据。`measurement` 和 `tag_set` 之间使用英文逗号（`,`）隔开。
- `tag_set`：可选参数，格式为 `<tag_key>=<tag_value>,<tag_key>=<tag_value>, ...`，用于指定时序表的标签名和标签值。多个标签之间使用英文逗号（`,`）隔开。KWDB 根据 `tag_key` 确定向表的哪个标签写入对应数据以及是否需要新增标签。解析时，KWDB 使用英文双引号（`""`）将标签名包裹起来，从而解决大小写敏感或以特殊字符、数字开头的标签名等问题。如果指定的标签名不存在，KWDB 会先添加标签，然后写入数据。未指定的标签列会自动填充为 NULL 值。KWDB 会根据标签列值和名字自动添加主标签列，命名为 `primary_tag`, 并生成对应的主标签值。主标签列的类型为 VARCHAR。`tag_set` 和 `field_set` 之间使用半角空格隔开。
- `field_set`：必填参数，格式为 `<field_key>=<field_value>,<field_key>=<field_value>, ...`，用于指定时序表的数据列及列数据，多列之间使用英文逗号（`,`）隔开。KWDB 根据 `field_key` 确定向表的哪个列写入对应数据以及是否需要新增列。解析时，KWDB 使用英文双引号（`""`）将列名包裹起来，从而解决大小写敏感或以特殊字符、数字开头的列名等问题。如果指定的列名不存在，KWDB 会先添加列，然后写入数据，未指定的列会自动填充为 NULL 值。`field_set` 和 `timestamp` 之间使用半角空格分隔。
- `timestamp`：可选参数，指定本行数据对应的时间戳。未指定时，KWDB 将使用所在主机的系统时间（UTC 时区）作为时间戳。目前，KWDB 支持毫秒、微秒和纳秒的时间精度。默认情况下，KWDB 采用纳秒时间精度。

下表列出 InfluxDB 和 KWDB 之间的数据类型转换。

| InfluxDB       | KWDB     |
| -------------- | ----------- |
| Float          | FLOAT8      |
| Integer        | INT8        |
| UInteger       | INT8        |
| String         | VARCHAR     |
| Boolean        | BOOL        |
| Unix timestamp | TIMESTAMPTZ |

有关 InfluxDB Line 协议、参数、支持的数据类型和符号，参见 [InfluxDB 官方文档](https://docs.influxdata.com/influxdb/v2.0/reference/syntax/line-protocol/)。

以下示例说明 KWDB 如何将 InfluxDB Line 协议格式的数据转换为 SQL 语句，在数据库中创建对应的时序表，并写入数据：

- InfluxDB Line 协议格式的数据

  ```json
  meters,location=Beijing current=17.01,voltage=220,phase=0.29
  ```

- 转换后的 SQL 语句

  ```sql
  -- 创建时序表 meters
  CREATE TABLE meters (k_timestamp TIMESTAMPTZ NOT NULL, current FLOAT8, voltage FLOAT8, phase FLOAT8) TAGS (primary_tag VARCHAR(64) NOT NULL, location VARCHAR) PRIMARY TAGS (primary_tag);
  
  -- 写入数据
  INSERT INTO meters VALUES (NOW(), 17.01, 220, 0.29, 'c15cf362f37e0acc7ecc2db55ec1cc57fc9579ccba9e72c273abb140f568472d', 'Beijing');
  ```
  
- 对应的时序表数据
  
  ```sql
  SELECT * FROM meters;
            k_timestamp           | current | voltage | phase |                           primary_tag                               | location
  --------------------------------+---------+---------+-------+---------------------------------------------------------------------+-----------
    2024-10-08 07:16:30.404+00:00 |   17.01 |     220 |  0.29 | c15cf362f37e0acc7ecc2db55ec1cc57fc9579ccba9e72c273abb140f568472d    | Beijing
  (1 row)
  ```

有关如何使用 InfluxDB API 接口向 KWDB 数据库写入数据的详细信息，参见 [InfluxDB 接口](./connect-restful-api.md#influxdb-接口)。

### OpenTSDB Telnet 格式的数据

::: warning 说明
所有参数之间之间使用空格分隔。因此，`metric` 和 `tag` 参数的取值尽量避免使用空格。
:::

OpenTSDB Telnet 格式的数据如下所示。

```json
<metric> <timestamp> <value> <tag1> <tag2> ...
```

参数说明：

- `metric`：必填参数，用于指定 KWDB 的时序表名。KWDB 根据该字段确定是否需要创建新表或向现有时序表中写入数据。解析时，KWDB 使用英文双引号（`""`）将时序表名包裹起来，从而解决大小写敏感或以特殊字符、数字开头的表名等问题。如果指定的时序表名不存在，KWDB 先创建该表，然后写入数据。
- `timestamp`：可选参数，指定本行数据对应的时间戳。未指定时，KWDB 使用所在主机的系统时间（UTC 时区）作为时间戳。目前，KWDB 支持毫秒、微秒和纳秒的时间精度。默认情况下，KWDB 采用毫秒时间精度。
- `value`：必填参数，用于指定时序表的数据列及列数据。KWDB 根据 `value` 确定向表的哪个列写入对应数据以及是否需要新增列。解析时，KWDB 使用英文双引号（`""`）将列名包裹起来，从而解决大小写敏感或以特殊字符、数字开头的列名等问题。如果指定的列名不存在，KWDB 会先添加列，然后写入数据，未指定的列会自动填充为 NULL 值。
- `tag`: 必填参数，格式为 `<tag_key1>=<tag_value1>,<tag_key2>=<tag_value2>, ...`，用于指定时序表的标签名和标签值。至少指定一个标签。多个标签之间使用空格隔开。KWDB 根据 `tag_key` 确定向表的哪个标签写入对应数据以及是否需要新增标签。解析时，KWDB 使用英文双引号（`""`）将标签名包裹起来，从而解决大小写敏感或以特殊字符、数字开头的标签名等问题。如果指定的标签名不存在，KWDB 会先添加标签，然后写入数据。未指定的标签列会自动填充为 NULL 值。KWDB 会根据标签列值和名字自动添加主标签列，命名为 `primary_tag`，并生成对应的主标签值。KWDB 自动将所有标签列的数据类型转换为 VARCHAR 类型，同时根据实际插入的数据长度修改列宽。

下表列出 OpenTSDB Telnet 和 KWDB 之间的数据类型转换。有关 OpenTSDB Telnet 协议、参数、支持的数据类型和符号，参见 [OpenTSDB Telnet 官方文档](https://opentsdb.net/docs/build/html/api_telnet/put.html)。

| 参数 | OpenTSDB Telnet 数据格式 | KWDB 数据格式 |
| --- | --- | --- |
| `metric` | String | VARCHAR |
| `timestamp` | Unix timestamp | TIMESTAMPTZ |
| `value` | Integer | FLOAT8 |
| | Float | FLOAT8 |
| `tag` | String | VARCHAR |
| | Integer | VARCHAR |
| | Float | VARCHAR |

有关如何使用 OpenTSDB Telnet API 接口向 KWDB 数据库写入数据的详细信息，参见 [OpenTSDB Telnet 接口](./connect-restful-api.md#opentsdb-telnet-接口)。

### OpenTSDB JSON 格式的数据

OpenTSDB JSON 格式的数据结构与 OpenTSDB Telnet 格式的数据结构类似，包括 `metric`、`timestamp`、`value` 和 `tag` 参数。但是，KWDB 只接收 JSON 数组格式的字符串，即使一行数据也需要转换成数组形式。

OpenTSDB JSON 格式的数据如下所示。

```json
[
  {
    "metric": "sys.cpu.nice",
    "timestamp": 1346846400,
    "value": 18,
    "tags": {
      "host": "web01",
      "dc": "1"
    }
  }
]
```

下表列出 OpenTSDB JSON 和 KWDB 之间的数据类型转换。有关 OpenTSDB JSON 协议、参数、支持的数据类型和符号，参见 [OpenTSDB JSON 官方文档](https://opentsdb.net/docs/build/html/api_http/put.html)。

| 参数 | OpenTSDB JSON 数据格式 | KWDB 数据格式 |
| --- | --- | --- |
| `metric` | String | VARCHAR |
| `timestamp` | Unix timestamp | TIMESTAMPTZ |
| `value` | Integer | FLOAT8 |
| | Float | FLOAT8 |
|  | String | VARCHAR |
| `tag` | String | VARCHAR |
| | Integer | FLOAT8 |
| | Float | FLOAT8 |

对于 OpenTSDB JSON 格式的数据，KWDB 不会自动把所有标签转成 VARCHAR 类型。而是将字符串类型的数据转化为 VARCHAR 类型。将数值类型的数据转换为 FLOAT8 类型。对于其他类型的数据输入，系统提示报错。

有关如何使用 OpenTSDB JSON API 接口向 KWDB 数据库写入数据的详细信息，参见 [OpenTSDB JSON 接口](./connect-restful-api.md#opentsdb-json-接口)。
