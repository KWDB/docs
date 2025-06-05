---
title: Schemaless Writing
id: schemaless-writing
---

# Schemaless Writing

Schemaless Writing is a powerful feature that allows you to insert data into KWDB without requiring predefined data structures or schemas. Rather than manually creating tables and defining columns before writing data, schemaless writing automatically handles the schema creation and adaptation process.

When you send data to KWDB using schemaless writing, the system intelligently:

- Creates tables on-demand when they don't exist
- Adds columns or tags dynamically as new fields are encountered
- Adjusts data types and column lengths to accommodate incoming data
- Handles all necessary `ALTER TABLE` operations behind the scenes

This approach is particularly valuable for:

- IoT devices sending varying sensor data
- Monitoring systems with evolving metrics
- Applications with changing or unpredictable data requirements

## Processing Logic

KWDB's schemaless writing capabilities are accessible via RESTful APIs using three industry-standard protocols:

- InfluxDB Line protocol
- OpenTSDB Telnet protocol
- OpenTSDB JSON protocol

Regardless of the protocol used, the processing flow follows these steps:

1. **Data parsing**: The input data is parsed according to protocol-specific rules to extract:
   - Target table name
   - Column names and data
   - Tags and their values
   - Timestamps
   - Data types

2. **SQL generation**: The system generates appropriate SQL statements based on the parsed data.
3. **Execution and schema adaptation**:
   - If the target table doesn't exist, it is created automatically
   - If the target table exists, the system verifies column and tag compatibility
   - Missing columns and tags are added through `ALTER TABLE ... ADD COLUMN` and `ALTER TABLE ... ADD TAG` operations
   - Insufficient column lengths and tag lengths are extended via `ALTER TABLE ... ALTER COLUMN` and `ALTER TABLE ... ALTER TAG` operations
   - Data is inserted into the table

## Supported Protocols

### InfluxDB Line Protocol

The InfluxDB Line protocol uses a compact, text-based format designed specifically for time-series data:

```json
<measurement>,<tag_set> <field_set> <timestamp>
```

Parameter Descriptions:

- `measurement`: Required. Specifies the time-series table name in KWDB. KWDB uses this field to determine whether to create a new table or insert data into an existing one. The table name is enclosed in double quotes (`""`) to handle case sensitivity and names starting with special characters or digits. If the specified table does not exist, it will be created first, then data is written. A comma (`,`) separates `measurement` and `tag_set`.
- `tag_set`: Optional. Format: `<tag_key>=<tag_value>,<tag_key>=<tag_value>, ...`. Specifies tag names and values for the time-series table. Tags are separated by commas. KWDB determines which tag to write and whether to add new tags based on the `tag_key`. Tag names are enclosed in double quotes (`""`) to handle case sensitivity and names starting with special characters or digits. Missing tags are added automatically; unspecified tags will be set to `NULL`. KWDB will also generate a `primary_tag` column with corresponding values, using `VARCHAR` type. A comma (`,`) separates `tag_set` and `field_set`.
- `field_set`: Required. Format: `<field_key>=<field_value>,<field_key>=<field_value>, ...`. Specifies data field names and values. Fields are separated by commas. KWDB determines which column to write to and whether to add new columns based on the `field_key`. Column names are enclosed in double quotes (`""`). Missing columns are added automatically; unspecified fields will be set to `NULL`. A space separates the `field_set` and `timestamp`.
- `timestamp`: Optional. Specifies the timestamp of the record. If omitted, KWDB uses the host's system time in UTC. Millisecond, microsecond, and nanosecond precisions are supported, with nanoseconds as the default.

Type conversion between InfluxDB and KWDB:

| InfluxDB       | KWDB     |
| -------------- | ----------- |
| Float          | FLOAT8      |
| Integer        | INT8        |
| UInteger       | INT8        |
| String         | VARCHAR     |
| Boolean        | BOOL        |
| Unix timestamp | TIMESTAMPTZ |

For more information on InfluxDB Line protocol, see [InfluxDB Official Documentation](https://docs.influxdata.com/influxdb/v2.0/reference/syntax/line-protocol/).

Example of converting InfluxDB Line protocol data to KWDB SQL statements:

- InfluxDB data

  ```json
  meters,location=Beijing current=17.01,voltage=220,phase=0.29
  ```

- Converted KWDB SQL statements

  ```sql
  -- Create time-series table `meters`
  CREATE TABLE meters (k_timestamp TIMESTAMPTZ NOT NULL, current FLOAT8, voltage FLOAT8, phase FLOAT8) TAGS (primary_tag VARCHAR(64) NOT NULL, location VARCHAR) PRIMARY TAGS (primary_tag);
  
  -- Insert data
  INSERT INTO meters VALUES (NOW(), 17.01, 220, 0.29, 'c15cf362f37e0acc7ecc2db55ec1cc57fc9579ccba9e72c273abb140f568472d', 'Beijing');
  ```
  
- Resulting data in KWDB
  
  ```sql
  SELECT * FROM meters;
            k_timestamp           | current | voltage | phase |                           primary_tag                               | location
  --------------------------------+---------+---------+-------+---------------------------------------------------------------------+-----------
    2024-10-08 07:16:30.404+00:00 |   17.01 |     220 |  0.29 | c15cf362f37e0acc7ecc2db55ec1cc57fc9579ccba9e72c273abb140f568472d    | Beijing
  (1 row)
  ```

For more information on writing data via the InfluxDB endpoint, see [InfluxDB Endpoint](./connect-restful-api.md#influxdb-endpoint).

### OpenTSDB Telnet Protocol

The OpenTSDB Telnet protocol uses a space-delimited format for metric data:

```json
<metric> <timestamp> <value> <tag1> <tag2> ...
```

::: warning Note
As all parameters are separated by spaces, avoid using spaces in the `metric` and `tag` values.
:::

Parameter Descriptions:

- `metric`: Required. Specifies the time-series table name in KWDB. KWDB uses this field to determine whether to create a new table or insert data into an existing one. The table name is enclosed in double quotes (`""`) to handle case sensitivity and names starting with special characters or digits. If the specified table does not exist, it will be created first, then data is written.
- `timestamp`: Optional. Specifies the timestamp of the record. If omitted, KWDB uses the host's system time in UTC. Millisecond, microsecond, and nanosecond precisions are supported, with millisecond as the default.
- `value`: Required. Specifies data field names and values. KWDB determines which column to write to and whether to add new columns based on the `value`. Column names are enclosed in double quotes (`""`) to handle case sensitivity and names starting with special characters or digits. Missing columns are added automatically; unspecified fields will be set to `NULL`.
- `tag`: Required. Format: `<tag_key1>=<tag_value1>,<tag_key2>=<tag_value2>, ...`. Specifies tag names and values for the time-series table. Tags are separated by commas. At least one tag is required. KWDB determines which tag to write and whether to add new tags based on the `tag_key`. Tag names are enclosed in double quotes (`""`) to handle case sensitivity and names starting with special characters or digits. Missing tag columns are added automatically; unspecified tags will be set to `NULL`. KWDB will also generate a `primary_tag` column with corresponding values using `VARCHAR` type. All tag columns are automatically converted to the `VARCHAR` type, and KWDB adjusts their column widths dynamically based on the length of the inserted values.

Type conversion between OpenTSDB Telnet and KWDB:

| Parameter | OpenTSDB Telnet | KWDB |
| --- | --- | --- |
| `metric` | String | VARCHAR |
| `timestamp` | Unix timestamp | TIMESTAMPTZ |
| `value` | Integer | FLOAT8 |
| | Float | FLOAT8 |
| `tag` | String | VARCHAR |
| | Integer | VARCHAR |
| | Float | VARCHAR |

For more information on OpenTSDB Telnet protocol, see [OpenTSDB Telnet Official Docs](https://opentsdb.net/docs/build/html/api_telnet/put.html).
For more information on how to use the OpenTSDB Telnet endpoint to write data into KWDB, see [OpenTSDB Telnet Endpoint](./connect-restful-api.md#opentsdb-telnet-endpoint).

### OpenTSDB JSON Protocol

The OpenTSDB JSON protocol uses a structured JSON format that provides more flexibility:

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

::: warning Note
KWDB accepts data only in JSON array format, even for single records.
:::

Type conversion between OpenTSDB JSON and KWDB:

| Parameter | OpenTSDB JSON | KWDB |
| --- | --- | --- |
| `metric` | String | VARCHAR |
| `timestamp` | Unix timestamp | TIMESTAMPTZ |
| `value` | Integer | FLOAT8 |
| | Float | FLOAT8 |
|  | String | VARCHAR |
| `tag` | String | VARCHAR |
| | Integer | FLOAT8 |
| | Float | FLOAT8 |

Unlike the Telnet protocol, KWDB preserves data types when parsing JSON:

- String values are stored as `VARCHAR`
- Numeric values are stored as `FLOAT8`
- Other data types will result in an error

For more information on OpenTSDB JSON protocol, see [OpenTSDB JSON Official Docs](https://opentsdb.net/docs/build/html/api_http/put.html).
For more information on how to use OpenTSDB JSON endpoint to write data into KWDB, see [OpenTSDB JSON Endpoint](./connect-restful-api.md#opentsdb-json-endpoint).
