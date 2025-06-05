---
title: RESTful API
id: connect-restful-api
---

# Connect to KWDB Using RESTful API

The KWDB RESTful API enables interaction with KWDB databases through HTTP requests. It provides the following capabilities:

- Authenticate users and manage sessions
- Execute DDL operations (create/drop tables, databases, etc.)
- Insert data
- Query data
- Support for third-party data formats (Telegraf, InfluxDB, OpenTSDB)
- Manage user sessions

All API requests use HTTPS and must include authentication information. The API supports up to 150 simultaneous HTTP connections.

The format of the HTTP request URL is:

```shell
https://<hostname>:<port>/<endpoint>?[tz=<timezone>][db=<db_name>]
```

Parameter descriptions:

- `hostname`: The IP address or fully qualified domain name (FQDN) of the KWDB server.
- `port`: The HTTP access port of the KWDB server (default: `8080`).
- `tz`: Specifies the timezone for the request. If provided, this timezone is used; otherwise, the system uses the value from the cluster parameter `server.restful_service.default_request_timezone`. Timezone information in the data itself takes precedence when present.
- `db_name`: (Optional) Specifies the target database. KWDB encloses the database name in double quotes (`""`) to handle case sensitivity and special characters. If not specified, the system uses the default database (`defaultdb`). The Login endpoint does not support this parameter.

## API Endpoints

::: warning
RESTful API endpoints currently support interaction with a single node only.
:::

KWDB provides the following RESTful API endpoints:

| Endpoint        | Description                                                  | Path                                             |
| --------------- | ------------------------------------------------------------ | ------------------------------------------------ |
| Login           | Authenticates users and provides authentication tokens        | `GET /restapi/login`                             |
| DDL             | Processes Data Definition Language operations                | `POST /restapi/ddl`                              |
| Insert          | Handles data insertion operations                            | `POST /restapi/insert`                           |
| Query           | Processes data query operations                              | `POST /restapi/query`                            |
| Telegraf        | Handles data insertion from Telegraf                         | `POST /restapi/telegraf`                         |
| InfluxDB        | Handles data insertion from InfluxDB                         | `POST /restapi/influxdb`                         |
| OpenTSDB JSON   | Handles data insertion in OpenTSDB JSON format               | `POST /restapi/opentsdbjson`                     |
| OpenTSDB Telnet | Handles data insertion in OpenTSDB Telnet format             | `POST /restapi/opentsdbtelnet`                   |
| Session         | Manages sessions; allows viewing or deleting sessions based on user privileges | `GET /restapi/session`<br>`DELETE /restapi/session` |


## Login Endpoint

The Login endpoint authenticates users and provides tokens for subsequent API calls. Based on the provided Base64-encoded username and password, the system generates a token with a configurable validity period.

::: warning Note

- Each login or token usage refreshes the token's start time and expiration time.
- The default token validity period is 60 minutes, configurable using the SQL statement `SET CLUSTER SETTING server.rest.timeout=<value>` (range: `[1, 2^63-1]` minutes).
- When implementing concurrent RESTful API requests, assign a separate token for each thread to ensure reliable operation (concurrency limit: 100).
- KWDB also supports direct authentication using Base64-encoded username and password in the HTTP request header, see [Authentication Methods](#authentication-methods) for differences.
:::

### Request Information
<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Endpoint</td>
      <td><br>- Without timezone: <code>/restapi/login</code><br>- With timezone:<code>/restapi/login?tz="timezone"</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Method</td>
      <td><code>GET</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Request Header</td>
      <td><pre><code>Content-Type: text/plain
Accept: application/json
Authorization: Basic "base64(user:password)"</code></pre></td>
      <td> <code>base64(user:password)</code>: Base64-encoded username and password.</td>
    </tr>
    <tr>
      <td>Request Body</td>
      <td>Empty</td>
      <td>-</td>
    </tr>
  </tbody>
</table>

### Response Information

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTTP Status Code</td>
      <td><code>HTTP/1.1 "code" "desc"</code></td>
      <td><br>- <code>code(int)</code>: HTTP status code.<br>- <code>desc(string)</code>: Status description. For details, see <a href="#http-status-code">HTTP Status Codes</a>.</td>
    </tr>
    <tr>
      <td>Response Header</td>
      <td><pre><code>Content-Type: application/json
Accept: text/plain</code></pre></td>
      <td> - </td>
    </tr>
    <tr>
      <td>Response Body</td>
      <td> - Success
      <pre><code>{
"code": "code",
"token": "token"
}</code></pre>
      - Failure<pre><code>{
  "code": "code",
  "desc": "desc",
}</code></pre></td>
      <td><br>- <code>code(int)</code>: HTTP status code. (0 = success, -1 = failure). <br> - <code>token(string)</code>: Token generated from credentials. <br>- <code>desc (string)</code>: Error description (for failures only).</td>
    </tr>
  </tbody>
</table>

### Configuration Example

The following example sends an HTTP request to obtain an authentication token:

```shell
GET /restapi/login HTTP/1.1
Host: localhost:8080
Content-Type: plain/text
Accept: application/json
Authorization: dTE6a3dkYnBhc3N3b3Jk
```

Successful response:

```shell
HTTP/1.1 200 OK
Content-Type: application/json

{
  "code": 0,
  "token": "cm9vdDprd2RicGFzc3dvcmQ="
}
```

Failed response:

```shell
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "code": -1,
  "desc": "the provided username and password did not match any credentials on the server"
}
```

## DDL Endpoint

The DDL endpoint processes HTTP requests containing Data Definition Language (DDL) statements. Users must have permissions for the specific DDL operations they intend to perform.

KWDB supports the following DDL operations through this endpoint:

- `CREATE`
- `DROP`
- `DELETE`
- `USE`
- `ALTER`
- `UPDATE`
- `GRANT`
- `REVOKE`

### Request Information

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Endpoint</td>
      <td><br>- Without timezone: <code>/restapi/ddl</code><br>- With timezone: <code>/restapi/ddl?tz="timezone"</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Method</td>
      <td><code>POST</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Request Header</td>
      <td><pre><code>Content-Type: text/plain
Accept: application/json
Authorization: Basic "token" or Basic "base64(user:password)"</code></pre></td>
      <td> - <code>token(string)</code>: Token generated from credentials.<br> - <code>base64(user:password)</code>: Base64-encoded username and password.</td>
    </tr>
    <tr>
      <td>Request Body</td>
      <td><code>"sql"</code></td>
      <td> <code>sql(string)</code>:  SQL statement(s) to execute. Multiple statements must be separated by semicolons (<code>;</code>).</td>
    </tr>
  </tbody>
</table>

### Response Information

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTTP Status Code</td>
      <td><code>HTTP/1.1 "code" "desc"</code></td>
      <td><br>- <code>code(int)</code>: HTTP Status Code.<br>- <code>desc(string)</code>: Status description. For details, see <a href="#http-status-code">HTTP Status Codes</a>.</td>
    </tr>
    <tr>
      <td>Response Header</td>
      <td><pre><code>Content-Type: application/json
Accept: text/plain</code></pre></td>
      <td> - </td>
    </tr>
    <tr>
      <td>Response Body</td>
      <td> - Success
      <pre><code>{
"code": "code",
"time": "time"
}</code></pre>
      - Failure<pre><code>{
  "code": "code",
  "desc": "desc1", "desc2", ...,
}</code></pre></td>
      <td><br>- <code>code(int)</code>: Execution status (0 = all statements succeeded, -1 = at least one statement failed)<br>- <code>desc(string)</code>: Array of execution results, one per statement ("success" or error message)<br>- <code>time(float)</code>: Execution time in seconds</td>
    </tr>
  </tbody>
</table>

### Configuration Example

The following example sends an HTTP request to create a table named `meters`:

```shell
POST /restapi/ddl HTTP/1.1
Host: localhost:8080
Authorization: Basic cm9vdDprd2RicGFzc3dvcmQ=
Content-Type: plain/text
Accept: application/json

CREATE TABLE meters (ts timestamp not null, power int) tags(location varchar not null) primary tags (location); CREATE TABLE wind (ts timestamp not null, speed int) tags(location varchar not null) primary tags (location);
```

Successful response:

```shell
HTTP/1.1 200 OK
Content-Type: application/json

{
  "code": 0,
  "desc": [
      "success",
      "success"
  ],
  "time": 0.002
}
```

## Insert Endpoint

The Insert endpoint processes HTTP requests containing `INSERT` statements. It supports data insertion requests, including those from EMQX. Users must have INSERT privileges on the target table to use this endpoint.

### Request Information


<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Endpoint</td>
      <td><br>- Without timezone: <code>/restapi/insert</code><br>- With timezone: <code>/restapi/insert?tz="timezone"</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Method</td>
      <td><code>POST</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Request Header</td>
      <td><pre><code>Content-Type: text/plain
Accept: application/json
Authorization: Basic "token" or Basic "base64(user:password)"</code></pre></td>
      <td>- <code>token(string)</code>: Token generated from credentials.<br> - <code>base64(user:password)</code>: Base64-encoded username and password.</td>
    </tr>
    <tr>
      <td>Request Body</td>
      <td><code>"sql"</code></td>
      <td> <code>sql(string)</code>: SQL statement(s) to execute. Multiple statements must be separated by semicolons(<code>;</code>).</td>
    </tr>
  </tbody>
</table>

### Response Information

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTTP Status Code</td>
      <td><code>HTTP/1.1 "code" "desc"</code></td>
      <td><br>- <code>code(int)</code>: HTTP Status Code.<br>- <code>desc(string)</code>: Status description. For details, see <a href="#http-status-code">HTTP Status Codes</a>.</td>
    </tr>
    <tr>
      <td>Response Header</td>
      <td><pre><code>Content-Type: application/json
Accept: text/plain</code></pre></td>
      <td> - </td>
    </tr>
    <tr>
      <td>Response Body</td>
      <td><pre><code>{
  "code": "code",
  "desc": "desc1","desc2" ... "descN",
  "rows": "string",
  "notice": "string",
  "time": "time"
}</code></pre></td>
      <td><br>- <code>code(int)</code>: Execution status (0 = all statements succeeded, -1 = at least one statement failed)<br>- <code>desc(string)</code>: Array of execution results, one per statement ("success" or error message)<br>- <code>rows(string)</code>: Number of rows inserted (null if operation failed)<br>- <code>notice(string)</code>: Failed insertion details (null if all operations succeeded)<br>- <code>time(float)</code>: Execution time in seconds</td>
    </tr>
  </tbody>
</table>

### Configuration Example

The following example sends an HTTP request to insert data to the `meters` table:

```shell
POST /restapi/insert HTTP/1.1
Host: localhost:8080
Authorization: Basic cm9vdDprd2RicGFzc3dvcmQ=
Content-Type: plain/text

insert into meters values("2023-07-30T06:44:40.32Z", "198352498", "beijing");insert into meters values("2023-07-30T06:45:40.32Z", "198352495", "beijing");
```

Successful response:

```shell
HTTP/1.1 200 OK
Content-Type: application/json

{
  "code": 0,
  "desc": [
    "success",
    "success"
  ],
  "rows": 1,
  "notice": null
  "time": 0.002
}
```

Failed response:

```shell
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "code": -1,
  "desc": [
    "Incorrect authentication token",
    "Incorrect authentication token"
  ],
  "rows": null,
  "notice": null
  "time": null
}
```

## Query Endpoint

The Query endpoint processes HTTP requests for data retrieval. Users must have SELECT privileges for the queried tables. Currently, this endpoint supports `SELECT`, `SHOW CREATE TABLE`, and `SHOW` statements.

### Request Information

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Endpoint</td>
      <td><br>- Without timezone: <code>/restapi/query</code><br>- With timezone: <code>/restapi/query?tz="timezone"</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Method</td>
      <td><code>POST</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Request Header</td>
      <td><pre><code>Content-Type: text/plain
Accept: application/json
Authorization: Basic "token" or Basic "base64(user:password)"</code></pre></td>
      <td> - <code>token(string)</code>: Token generated from credentials.<br> - <code>base64(user:password)</code>: Base64-encoded username and password.</td>
    </tr>
    <tr>
      <td>Request Body</td>
      <td><code>"sql"</code></td>
      <td> <code>sql(string)</code>: SQL statement(s) to execute. Multiple statements must be separated by semicolons (<code>;</code>).</td>
    </tr>
  </tbody>
</table>

### Response Information

::: warning Note
To prevent performance issues, response body size is limited to 5 MB. Data exceeding this limit will be truncated.
:::

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTTP Status Code</td>
      <td><code>HTTP/1.1 "code" "desc"</code></td>
      <td><br>- <code>code(int)</code>: HTTP Status Code.<br>- <code>desc(string)</code>: Status description. For details, see <a href="#http-status-code">HTTP Status Codes</a>.</td>
    </tr>
    <tr>
      <td>Response Header</td>
      <td><pre><code>Content-Type: application/json
Accept: text/plain</code></pre></td>
      <td> - </td>
    </tr>
    <tr>
      <td>Response Body</td>
      <td><pre><code>
{
  "code": "code",
  "desc": "desc",
  "time": "time",
  "column_meta": "column_meta",
  "data": "data",
  "rows": "rows"
}</code></pre></td>
      <td><br>- <code>code(int)</code>: Status code (0 = success, other values = failure)<br>- <code>desc(string)</code>: Error description (null or error messages)<br>- <code>time(float)</code>: Execution time in seconds<br>- <code>column_meta(array)</code>: Array of column metadata in format [column_name, data_type, type_length]<br>- <code>data(array)</code>: Array of query result rows<br>- <code>rows(int)</code>: Number of rows returned</td>
    </tr>
  </tbody>
</table>

### Configuration Example

The following example sends an HTTP request to query the data in table `ts_table`.

```shell
POST /restapi/query HTTP/1.1
Host: localhost:8080
Authorization: Basic cm9vdDprd2RicGFzc3dvcmQ=
Content-Type: plain/text

select * from ts_table;
```

Successful response:

```shell
HTTP/1.1 200 OK
Content-Type: application/json

{
  "code": 0,
  "desc": null,
  "time": 0.022829285,
  "column_meta": [
      [
          "ts",
          "TIMESTAMP",
          8
      ],
      [
          "id",
          "VARCHAR",
          128
      ],
      [
          "electricity",
          "FLOAT",
          8
      ]
  ],
  "data": [
      [
          "2023-07-30T06:44:40.32Z",
          "198352498",
          0.31
      ],
      [
          "2023-07-30T06:44:41.32Z",
          "234758890",
          0.33
      ]
  ],
  "rows": 2
}
```

Failed response:

```shell
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "code": 500,
  "desc": "No table named ts_table found",
  "time": null，
  "column_meta": null,
  "data": null,
  "rows": null
}
```

## Telegraf Endpoint

The Telegraf endpoint accepts data in InfluxDB Line format from Telegraf collectors. Users must have INSERT privileges on the target tables to use this endpoint.

Before using this endpoint, you need to create the corresponding time-series tables in KWDB based on the Telegraf data structure. KWDB will convert the InfluxDB Line format data into SQL statements for insertion.

The data format used by the Telegraf endpoint is:

```json
<measurement>,<tag_set> <field_set> <timestamp>
```

Parameter Descriptions:

- `measurement`: Required. Specifies the time-series table name in KWDB. KWDB uses this field to determine whether to create a new table or insert data into an existing one. The table name is enclosed in double quotes (`""`) to handle case sensitivity and names starting with special characters or digits. If the specified table does not exist, it will be created first, then data is written. A comma (`,`) separates `measurement` and `tag_set`.
- `tag_set`: Optional. Format: `<tag_key>=<tag_value>,<tag_key>=<tag_value>, ...`. Specifies tag names and values for the time-series table. Tags are separated by commas. KWDB determines which tag to write and whether to add new tags based on the `tag_key`. Tag names are enclosed in double quotes (`""`) to handle case sensitivity and names starting with special characters or digits. Missing tags are added automatically; unspecified tags will be set to `NULL`. KWDB will also generate a `primary_tag` column with corresponding values, using `VARCHAR` type. A comma (`,`) separates `tag_set` and `field_set`.
- `field_set`: Required. Format: `<field_key>=<field_value>,<field_key>=<field_value>, ...`. Specifies data field names and values. Fields are separated by commas. KWDB determines which column to write to and whether to add new columns based on the `field_key`. Column names are enclosed in double quotes (`""`). Missing columns are added automatically; unspecified fields will be set to `NULL`. A space separates the `field_set` and `timestamp`.
- `timestamp`: Optional. Specifies the timestamp of the record. If omitted, KWDB uses the host's system time in UTC. Millisecond, microsecond, and nanosecond precisions are supported, with nanosecond as the default.

Example of converting InfluxDB Line protocol data to KWDB SQL statements:

- InfluxDB data

  ```sql
  meters,location=Beijing current=17.01,voltage=220,phase=0.29 1556813561098000000
  ```

- Converted KWDB SQL statements

  ```sql
  create table meters (ts timestamp not null, current float, voltage int, phase float) tags (location varchar(20) not null) primary tags (location);
  ```

For more information on InfluxDB Line protocol, see [InfluxDB Official Documentation](https://docs.influxdata.com/influxdb/v2.0/reference/syntax/line-protocol/).

### Request Information

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Endpoint</td>
      <td><code>/restapi/telegraf</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Method</td>
      <td><code>POST</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Request Header</td>
      <td><pre><code>Content-Type: text/plain
Accept: application/json
Authorization: Basic "token" or Basic "base64(user:password)"</code></pre></td>
      <td> - <code>token(string)</code>: Token generated from credentials.<br> - <code>base64(user:password)</code>: Base64-encoded username and password.</td>
    </tr>
    <tr>
      <td>Request Body</td>
      <td><code>"line_format"</code></td>
      <td><code>line_format(string)</code>: The InfluxDB Line format data to be inserted.</td>
    </tr>
  </tbody>
</table>

### Response Information

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTTP Status Code</td>
      <td><code>HTTP/1.1 "code" "desc"</code></td>
      <td><br>- <code>code(int)</code>: HTTP Status Code.<br>- <code>desc(string)</code>: Status description. For details, see <a href="#http-status-code">HTTP Status Codes</a>.</td>
    </tr>
    <tr>
      <td>Response Header</td>
      <td><pre><code>
      Content-Type: application/json
      Accept: text/plain
      </code></pre></td>
      <td> - </td>
    </tr>
    <tr>
      <td>Response Body</td>
      <td><pre><code>
      {
        "code": "code",
        "desc": "desc",
        "rows": "rows",
        "time": "time"
      }</code></pre></td>
      <td><br>- <code>code(int)</code>: Execution status (0 = all operations succeeded, -1 = at least one operation failed)<br>- <code>desc(string)</code>: Error description (null for successful operations)<br>- <code>rows(int)</code>: Number of rows inserted<br>- <code>time(float)</code>: Execution time in seconds</td>
    </tr>
  </tbody>
</table>

### Configuration Example

The following example sends an HTTP request to insert data into the  `myMeasurement` table.

```shell
POST /restapi/telegraf HTTP/1.1
Host: localhost:8080
Authorization: Basic cm9vdDprd2RicGFzc3dvcmQ=
Content-Type: plain/text

myMeasurement,tag1=value1,tag2=value2 fieldKey="fieldValue" 1556813561098000000
```

Successful response:

```shell
HTTP/1.1 200 OK
Content-Type: application/json

{
  "code": 0,
  "desc": null,
  "rows": 1,
  "time": 0.002
}
```

Failed response:

```shell
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "code": 500,
  "desc": "Incorrect authentication token",
  "rows": null,
  "time": null
}
```

## InfluxDB Endpoint

The InfluxDB endpoint accepts data in InfluxDB Line Protocol format. Users must have appropriate privileges to execute the generated SQL statements. Unlike the Telegraf endpoint, you only need to create the time-series database before using this endpoint; KWDB will automatically handle table creation, column addition, and data insertion as needed.


### Request Information

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Endpoint</td>
      <td><br>- Without timezone: <code>/restapi/influxdb</code><br>- With timezone: <code>/restapi/influxdb?tz="timezone"</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Method</td>
      <td><code>POST</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Request Header</td>
      <td><pre><code>Content-Type: text/plain
Accept: application/json
Authorization: Basic "token" or Basic "base64(user:password)"</code></pre></td>
      <td> - <code>token(string)</code>: Token generated from credentials.<br> - <code>base64(user:password)</code>: Base64-encoded username and password.</td>
    </tr>
    <tr>
      <td>Request Body</td>
      <td><code>"line_format"</code></td>
      <td><code>line_format(string)</code>: One or more lines of data in InfluxDB Line format.</td>
    </tr>
  </tbody>
</table>

### Response Information

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTTP Status Code</td>
      <td><code>HTTP/1.1 "code" "desc"</code></td>
      <td><br>- <code>code(int)</code>: HTTP Status Code.<br>- <code>desc(string)</code>: Status description. For details, see <a href="#http-status-code">HTTP Status Codes</a>.</td>
    </tr>
    <tr>
      <td>Response Header</td>
      <td><pre><code>Content-Type: application/json
Accept: text/plain</code></pre></td>
      <td> - </td>
    </tr>
    <tr>
      <td>Response Body</td>
      <td><pre><code>{
  "code": "code",
  "desc": "desc",
  "rows": "rows",
  "time": "time"
}</code></pre></td>
      <td><br>- <code>code(int)</code>: Execution status (0 = all operations succeeded, -1 = at least one operation failed)<br>- <code>desc(string)</code>: Error description (null for successful operations)<br>- <code>rows(stringint)</code>: Number of rows inserted<br>- <code>time(float)</code>: Execution time in seconds</td>
    </tr>
  </tbody>
</table>

### Configuration Example

The following table sends an HTTP request to create the table `myMeasurement` or insert data into the `myMeasurement` table.

```shell
POST /restapi/influxdb HTTP/1.1
Host: localhost:8080
Authorization: Basic cm9vdDprd2RicGFzc3dvcmQ=
Content-Type: plain/text

myMeasurement,tag1=value1,tag2=value2 fieldKey="fieldValue" 1556813561098000000
```

Successful response:

```shell
HTTP/1.1 200 OK
Content-Type: application/json

{
  "code": 0,
  "desc": null,
  "rows": 1,
  "time": 0.002
}
```

Failed response:

```shell
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "code": -1,
  "desc": "Incorrect authentication token",
  "rows": null,
  "time": null
}
```

## OpenTSDB JSON Endpoint

The OpenTSDB JSON endpoint accepts data in OpenTSDB JSON format. Users must have appropriate privileges to execute the generated SQL statements. You only need to create the time-series database before using this endpoint; KWDB will automatically handle table creation, column addition, and data insertion as needed.

### Request Information

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Endpoint</td>
      <td><br>- Without timezone: <code>/restapi/opentsdbjson</code><br>- With timezone: <code>/restapi/opentsdbjson?tz="timezone"</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Method</td>
      <td><code>POST</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Request Header</td>
      <td><pre><code>Content-Type: text/plain
Accept: application/json
Authorization: Basic "token" or Basic "base64(user:password)"</code></pre></td>
      <td> - <code>token(string)</code>: Token generated from credentials.<br> - <code>base64(user:password)</code>: Base64-encoded username and password.</td>
    </tr>
    <tr>
      <td>Request Body</td>
      <td><code>"line_format"</code></td>
      <td><code>line_format(string)</code>: One or more lines of data in the OpenTSDB JSON format.</td>
    </tr>
  </tbody>
</table>

### Response Information

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTTP Status Code</td>
      <td><code>HTTP/1.1 "code" "desc"</code></td>
      <td><br>- <code>code(int)</code>: HTTP Status Code.<br>- <code>desc(string)</code>: Status description. For details, see <a href="#http-status-code">HTTP Status Codes</a>.</td>
    </tr>
    <tr>
      <td>Response Header</td>
      <td><pre><code>Content-Type: application/json
Accept: text/plain</code></pre></td>
      <td> - </td>
    </tr>
    <tr>
      <td>Response Body</td>
      <td><pre><code>{
  "code": "code",
  "desc": "desc",
  "rows": "rows",
  "time": "time"
}</code></pre></td>
      <td><br>- <code>code(int)</code>: Execution status (0 = all operations succeeded, -1 = at least one operation failed)<br>- <code>desc(string)</code>: Error description (null for successful operations)<br>- <code>rows(stringint)</code>: Number of rows inserted<br>- <code>time(float)</code>: Execution time in seconds</td>
    </tr>
  </tbody>
</table>


### Configuration Example

The following example sends an HTTP request to create the `sys.cpu.usage` table or insert data into the `sys.cpu.usage` table.

```shell
POST /restapi/opentsdbjson HTTP/1.1
Host: localhost:8081
Content-Type: text/plain
Authorization: Basic *******


[{"metric": "sys.cpu.usage","timestamp": 1654567205,"value": 0.5,"tags": {"host": "server1","dc": "1"}},{"metric": "sys.cpu.usage","timestamp": 1654567205,"value": 0.7,"tags": {"host": "server1","dc2": "us-west"}}]
```

Successful response:

```shell
HTTP/1.1 200 OK
Content-Type: application/json

{
  "code":0,
  "desc":"success;success;",
  "time":0.088146837,
  "rows":2
}
```

Failed response:

```shell
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "code": -1,
  "desc": "Incorrect authentication token",
  "rows": null,
  "time": null
}
```

## OpenTSDB Telnet Endpoint

The OpenTSDB Telnet endpoint accepts data in OpenTSDB Telnet format. Users must have appropriate privileges to execute the generated SQL statements. You only need to create the time-series database before using this endpoint; KWDB will automatically handle table creation, column addition, and data insertion as needed.



### Request Information

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Endpoint</td>
      <td><br>- Without timezone: <code>/restapi/opentsdbtelnet</code><br>- With timezone: <code>/restapi/opentsdbtelnet?tz="timezone"</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Method</td>
      <td><code>POST</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Request Header</td>
      <td><pre><code>Content-Type: text/plain
Accept: application/json
Authorization: Basic "token" or Basic "base64(user:password)"</code></pre></td>
      <td> - <code>token(string)</code>: Token generated from credentials.<br> - <code>base64(user:password)</code>: Base64-encoded username and password.</td>
    </tr>
    <tr>
      <td>Request Body</td>
      <td><code>"line_format"</code></td>
      <td><code>line_format(string)</code>: One or more lines of data in the OpenTSDB Telnet format.</td>
    </tr>
  </tbody>
</table>

### Response Information

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTTP Status Code</td>
      <td><code>HTTP/1.1 "code" "desc"</code></td>
      <td><br>- <code>code(int)</code>: HTTP Status Code.<br>- <code>desc(string)</code>: Status description. For details, see <a href="#http-status-code">HTTP Status Codes</a>.</td>
    </tr>
    <tr>
      <td>Response Header</td>
      <td><pre><code>Content-Type: application/json
Accept: text/plain</code></pre></td>
      <td> - </td>
    </tr>
    <tr>
      <td>Response Body</td>
      <td><pre><code>{
  "code": "code",
  "desc": "desc",
  "rows": "rows",
  "time": "time"
}</code></pre></td>
      <td><br>- <code>code(int)</code>: Execution status (0 = all operations succeeded, -1 = at least one operation failed)<br>- <code>desc(string)</code>: Error description (null for successful operations)<br>- <code>rows(stringint)</code>: Number of rows inserted<br>- <code>time(float)</code>: Execution time in seconds</td>
    </tr>
  </tbody>
</table>


### Configuration Example

The following example sends an HTTP request to create the `meters` table or insert data into the `meters` table.

```shell
POST /restapi/opentsdbtelnet HTTP/1.1
Host: localhost:8081
Content-Type: text/plain
Authorization: Basic *******


meters.current 1648432611250 11.3 location=California.LosAngeles groupid=3 extraTag=value
```

Successful response:

```shell
HTTP/1.1 200 OK
Content-Type: application/json

{
  "code":0,
  "desc":"success;",
  "time":1.279927072,
  "rows":1
}
```

Failed response:

```shell
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "code": -1,
  "desc": "Incorrect authentication token",
  "rows": null,
  "time": null
}
```

## Session Endpoint

The Session endpointallows users to query session information and delete specified sessions. Administrators can view all session information and delete any session, while regular users can only view and delete their own sessions.

### Request Information

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Endpoint</td>
      <td><br>- Without timezone: <code>/restapi/session</code><br>- With timezone: <code>/restapi/session?tz="timezone"</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Method</td>
      <td><br> - View sessions: <code>GET</code> <br> - Delete sessions: <code>DELETE</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Request Header</td>
      <td><pre><code>Content-Type: text/plain
Accept: application/json
Authorization: Basic "token" or Basic "base64(user:password)"</code></pre></td>
      <td> - <code>token(string)</code>: Token generated from credentials.<br> - <code>base64(user:password)</code>: Base64-encoded username and password.</td>
    </tr>
    <tr>
      <td>Request Body</td>
      <td>- View sessions: Empty<br>- Delete sessions: <code>"conn_id"</code></td>
<td><code>"conn_id"</code>: The SessionID of the session to be deleted, required only when deleting a specific session.</td>
    </tr>
  </tbody>
</table>

### Response Information

**Viewing Sessions**
<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTTP Status Code</td>
      <td><code>HTTP/1.1 "code" "desc"</code></td>
      <td><br>- <code>code(int)</code>: HTTP Status Code.<br>- <code>desc(string)</code>: Status description. For details, see <a href="#http-status-code">HTTP Status Codes</a>.</td>
    </tr>
    <tr>
      <td>Response Header</td>
      <td><pre><code>Content-Type: application/json
Accept: text/plain</code></pre></td>
      <td> - </td>
    </tr>
    <tr>
      <td>Response Body</td>
      <td><pre><code>{
    "code": "code",
    "tokens": [{"session_info"}]
}</code></pre></td>
      <td><br>- <code>code(int)</code>: Status code. <code>0</code> indicates success, other values indicate failure. <br>- <code>conn_info</code>: Session connection-related information, such as connection ID, username, token and timeout.</td>
    </tr>
  </tbody>
</table>

**Deleting Sessions**

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Content</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTTP Status Code</td>
      <td><code>HTTP/1.1 "code" "desc"</code></td>
      <td><br>- <code>code(int)</code>: HTTP Status Code.<br>- <code>desc(string)</code>: Status description. For details, see <a href="#http-status-code">HTTP Status Codes</a>.</td>
    </tr>
    <tr>
      <td>Response Header</td>
      <td><pre><code>Content-Type: application/json
Accept: text/plain</code></pre></td>
      <td> - </td>
    </tr>
    <tr>
      <td>Response Body</td>
      <td><pre><code>{
  "code": "code",
  "desc": "desc"
}</code></pre></td>
      <td><br>- <code>code(int)</code>: Status code(0 = success, other values = failure).<br>- <code>desc(string)</code>: Description of the delete operation result.</td>
    </tr>
  </tbody>
</table>

### Configuration Example

Example 1: Viewing session information

Request:

```shell
GET /restapi/session HTTP/1.1
Content-Type: text/plain
Accept: application/json
Authorization: Basic cm9vdDprd2RicGFzc3dvcmQ=
```

Successful response:

- Regular users (view their own session only):

    ```json
  {
   "code":0,
   "tokens":[{"SessionID":"1970e371-5947-11ef-8726-000c29585cae","Username":"u1","Token":"9c7e0ad44a9e02dc67fb2f3e48446769","MaxLifeTime":3600,"LastLoginTime":"2024-08-13 07:41:08","ExpirationTime":"2024-08-13 08:41:08"}]
  }
  ```

- Administrators (view all sessions):

  ```json
  {"code":0,
  "tokens":[
  {"SessionID":"50830553-3e83-11ef-a323-b4055d17f786","Username":"u1","Token":"c2ff2c6d*","MaxLife Time":3600,"LastLoginTime":"2024-07-10 06:11:58","ExpirationTime":"2024-07-10 07:11:58"},
  {"SessionID":"9bf2fa13-3e83-11ef-a323-b4055d17f786","Username":"u1","Token":"f9f3a39d*","MaxLife Time":3600,"LastLoginTime":"2024-07-10 06:14:04","ExpirationTime":"2024-07-10 07:14:04"}
  ]
  }
  ```

Example 2: Deleting a session

Request:

```shell
DELETE /restapi/session HTTP/1.1
Content-Type: text/plain
Accept: application/json
Authorization: Basic cm9vdDprd2RicGFzc3dvcmQ=

0339f5b5-c492-11ee-a7c9-000c29066670
```

Successful response:

```json
{
  "code":0,
  "desc": "Delete Success"
}
```

## Authentication Methods

All KWDB RESTful API requests are sent using HTTPS and All KWDB RESTful API requests use HTTPS and are authenticated through the HTTP Header. 

The following authentication methods are supported:

**Username and Password Authentication**

Users include a Base64-encoded database username and password in the HTTP request header. Upon successful authentication, the system creates a temporary token for identity verification that is automatically destroyed after the request completes. This method is simple to implement with no connection limits but requires higher system performance, making it suitable for scenarios with small data volumes and low performance requirements.

**Token Authentication**

Users first obtain a token by calling the RESTful API login interface. This token can then be used for authentication in subsequent API calls, such as the DDL endpoint and the Insert endpoint. 

Token Configuration:

- Tokens are valid for 60 minutes by default
- Adjust token validity using `SET CLUSTER SETTING server.rest.timeout=<minutes>;`
- Validity can be set between 1 minute and 2^63-1 minutes
- System supports up to 100 concurrent token-based connections

Token authentication eliminates the need to create and destroy temporary tokens with each request, making it more suitable for high-performance scenarios.

When implementing concurrent requests using the RESTful API, assign a unique token to each thread to ensure smooth operation.

**Secure Communication with KWDB**

HTTPS uses SSL encryption for data transmission. When communicating securely with the KWDB database, the KWDB server-generated certificate must be accessible by the client making the request. See Example 3 for the operation procedure.

Example 1: Using Username and Password for Authentication

```shell
<!--Request-->
POST /restapi/ddl HTTP/1.1
Host: localhost:8080
Authorization: Basic dTE6a3dkYnBhc3N3b3Jk
Content-Type: plain/text
Accept: application/json

CREATE TABLE ts_table(ts timestamp not null, power int) tags(location varchar(15) not null) primary tags (location);
```

Example 2: Using Token for Authentication

```shell
<!--Request-->
POST /restapi/ddl HTTP/1.1
Host: localhost:8080
Authorization: Basic cm9vdDprd2RicGFzc3dvcmQ=
Content-Type: plain/text
Accept: application/json

CREATE TABLE ts_table(ts timestamp not null, power int) tags(location varchar(15));
```

Example 3: Secure Communication with KWDB

1. Deploy and start the database in secure mode.
2. Create a new user in the database:
    ```sql
    create user rest_user password 'user123456';
    ```
3. Copy the KWDB server-generated certificate to a path accessible by the client. The default certificate location is `/etc/kaiwudb/cert`.
4. Use the secure certificate for Restful API connections.

      - Login Example
        ```bash
        curl -L --cacert ../certs/ca.crt -H "Authorization: Basic dTE6a3dkYnBhc3N3b3Jk" -X GET your-host-ip:port/restapi/login
        ```
      - Query Example
        ```
        curl -L -H "Content-Type:text/plain" -H "Authorization: Basic dTE6a3dkYnBhc3N3b3Jk"  --cacert ../certs/ca.crt -d "select*from t1;" -X POST your-host-ip:port/restapi/query?db=db1
        ```

## HTTP Status Codes

After each HTTP request completes, the system returns an HTTP status code. The following table lists the HTTP status codes used by the KWDB RESTful API:

| HTTP Status Code | Description                   |
| ---------------- | ----------------------------- |
| 200              | Success                       |
| 400              | Parameter Error               |
| 401              | Authentication Failed         |
| 404              | URL Not Found                 |
| 500              | Internal Error                |
| 503              | Insufficient System Resources |
