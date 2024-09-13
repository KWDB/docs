---
title: RESTful API
id: connect-restful-api
---

# RESTful API 连接 KWDB 数据库

KWDB 支持用户通过发送 HTTP 请求与数据库进行交互。用户可以在 HTTP 请求头部添加认证信息，在请求体中包含执行数据库操作的 SQL 语句，并获得 JSON 格式的响应结果。KWDB 提供的 RESTful API 接口见 [RESTful API 接口](#restful-api-接口)，支持的认证方式见[认证方式](#认证方式)，使用的 HTTP 状态码见 [HTTP 状态码](#http-状态码)。

KWDB 支持同时使用多个 HTTP 请求连接数据库，最多支持 150 个 HTTP 连接。所有请求通过 HTTPS 发送，并在 HTTP 请求头部包含认证信息。HTTP 请求的 URL 格式为：

```shell
https://<hostname>:<port>/<endpoint>?[db=<db_name>]
```

参数说明：

- `hostname`：KWDB 服务器的 IP 地址或者 FQDN（Fully Qualified Domain Name，完全限定域名）。
- `port`：KWDB 服务器的 HTTP 访问端口，默认是 `8080`。
- `db_name`：可选参数, 用于指定目标数据库。如未指定，则使用系统默认创建的 `defaultdb` 数据库。[Login 接口](#login-接口)不支持设置该参数。

## RESTful API 接口

::: warning 说明
目前，RESTful API 接口只支持与单个节点交互通信。
:::

KWDB 提供以下 RESTful API 接口进行数据操作：

| 接口            | 描述                                                         | Endpoint                                           |
| --------------- | ------------------------------------------------------------ | -------------------------------------------------- |
| Login           | 登录接口，获取认证令牌。                                     | `GET/restapi/login`                                |
| DDL             | 用于数据库创建、删除等 DDL 操作请求。                        | `POST/restapi/ddl`                                 |
| Insert          | 用于数据插入操作请求。                                       | `POST/restapi/insert`                              |
| Query           | 用于数据查询操作请求。                                       | `POST/restapi/query`                               |
| Telegraf Insert | 用于将来自 Telegraf 的数据插入表中。                         | `POST/restapi/telegraf`                            |
| Session         | 用于查询本节点会话信息或删除指定会话信息。管理员用户可以查看所有会话信息或删除指定会话信息。普通用户可以查看或删除自己的会话信息。 | `GET/restapi/session` <br>`DELETE/restapi/session` |

## Login 接口

Login 接口用于用户身份授权，系统根据用户提供的 Base64 编码后的用户名和密码信息，生成默认有效期为 60 分钟的令牌。用户使用其他 API 接口，例如 DDL 接口、Insert 接口等发送 HTTP 请求时，可以在 HTTP 请求头部中使用该令牌进行认证。

::: warning 说明

- 用户每次登录或使用令牌进行操作后，系统会自动更新令牌起始时间，重新计算令牌的到期时间。
- 默认情况下，系统生成的令牌有效期为 60 分钟。用户可以通过 `SET CLUSTER SETTING server.rest.timeout=<value>` SQL 语句设置令牌的有效期。可配置范围为 `[1, 2^63-1]`，单位为分钟。
- 使用 RESTful API 进行并发编程时，建议为每个线程分配一个独立的 token，以确保业务操作的顺利进行。并发数限制为 100。
- KWDB 也支持直接使用 Base64 编码后的用户名和密码在 HTTP 请求头部中进行用户认证，两种认证方式的区别见[认证方式](#认证方式)。

:::

### 请求信息

下表列出 Login 接口的请求信息：

<table>
  <thead>
    <tr>
      <th>信息</th>
      <th>内容</th>
      <th>说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Endpoint</td>
      <td><code>/restapi/login</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Method</td>
      <td><code>GET</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>请求头部</td>
      <td><pre><code>Content-Type: text/plain
Accept: application/json
Authorization: Basic "base64(user:password)"</code></pre></td>
      <td> <code>base64(user:password)</code>：Base64 编码后的用户名和密码信息。</td>
    </tr>
    <tr>
      <td>请求体</td>
      <td>空</td>
      <td>-</td>
    </tr>
  </tbody>
</table>

### 响应信息

下表列出 Login 接口的响应信息：

<table>
  <thead>
    <tr>
      <th>信息</th>
      <th>内容</th>
      <th>说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTTP 状态码</td>
      <td><code>HTTP/1.1 "code" "desc"</code></td>
      <td><br>- <code>code（int）</code>：HTTP 状态码。<br>- <code>desc（string）</code>：状态码描述。有关 HTTP 状态码详细信息，参见 <a href="#http-状态码">HTTP 状态码</a>。</td>
    </tr>
    <tr>
      <td>响应头部</td>
      <td><pre><code>Content-Type: application/json
Accept: text/plain</code></pre></td>
      <td> - </td>
    </tr>
    <tr>
      <td>响应体</td>
      <td> - 成功
      <pre><code>{
"code": "code",
"token": "token"
}</code></pre>
      - 失败<pre><code>{
  "code": "code",
  "desc": "desc",
}</code></pre></td>
      <td><br>- <code>code（int）</code>：HTTP 状态码。0 表示成功，-1 表示失败。<br> - <code>token（string）</code>：基于用户名和密码编码生成的令牌。用户可以使用令牌进行认证。<br>- <code>desc（string）</code>：失败对应的错误码描述。</td>
    </tr>
  </tbody>
</table>


### 配置示例

以下示例发送 HTTP 请求，获取认证令牌。

```shell
GET /restapi/login HTTP/1.1
Host: localhost:8080
Content-Type: plain/text
Accept: application/json
Authorization: dTE6a3dkYnBhc3N3b3Jk
```

如果请求成功，返回以下信息：

```shell
HTTP/1.1 200 OK
Content-Type: application/json

{
  "code": 0,
  "token": "cm9vdDprd2RicGFzc3dvcmQ="
}
```

如果请求失败，返回以下信息：

```shell
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "code": -1,
  "desc": "the provided username and password did not match any credentials on the server"
}
```

## DDL 接口

DDL 接口用于发送包含 DDL 语句的 HTTP 请求。用户可以使用此接口创建数据库、表等 DDL 操作。发送 DDL API 请求的用户，需要有相应 DDL 的操作权限。例如创建数据库、表需要拥有相应数据库库、表的 CREATE 权限。删除数据库、表需要有相应数据库、表的 DROP 权限。KWDB 支持 CREATE、DROP、DELETE、USE、ALTER、UPDATE、GRANT、REVOKE 等 DDL 操作。

### 请求信息

下表列出 DDL 接口的请求信息：

<table>
  <thead>
    <tr>
      <th>信息</th>
      <th>内容</th>
      <th>说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Endpoint</td>
      <td><code>/restapi/ddl</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Method</td>
      <td><code>POST</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>请求头部</td>
      <td><pre><code>Content-Type: text/plain
Accept: application/json
Authorization: Basic "token" 或 Basic "base64(user:password)</code></pre></td>
      <td> - <code>token（string）</code>：Login 接口生成的认证令牌。<br> - <code>base64(user:password)</code>：Base64 编码后的用户名和密码信息。</td>
    </tr>
    <tr>
      <td>请求体</td>
      <td><code>"sql"</code></td>
      <td> <code>sql（string）</code>：执行的 SQL 语句。支持一次发送多条 SQL 语句，语句间使用英文分号（<code>;</code>）隔开。</td>
    </tr>
  </tbody>
</table>


### 响应信息

下表列出 DDL 接口的响应信息：

<table>
  <thead>
    <tr>
      <th>信息</th>
      <th>内容</th>
      <th>说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTTP 状态码</td>
      <td><code>HTTP/1.1 "code" "desc"</code></td>
      <td><br>- <code>code（int）</code>：HTTP 状态码。<br>- <code>desc（string）</code>：状态码描述。有关 HTTP 状态码详细信息，参见 <a href="#http-状态码">HTTP 状态码</a>。</td>
    </tr>
    <tr>
      <td>响应头部</td>
      <td><pre><code>Content-Type: application/json
Accept: text/plain</code></pre></td>
      <td> - </td>
    </tr>
    <tr>
      <td>响应体</td>
      <td> - 成功
      <pre><code>{
"code": "code",
"time": "time"
}</code></pre>
      - 失败<pre><code>{
  "code": "code",
  "desc": "desc1", "desc2", ...,
}</code></pre></td>
      <td><br>- <code>code（int）</code>：SQL 语句执行状态码。所有语句执行成功，返回 <code>0</code>。如有执行失败的语句，返回 <code>-1</code>。<br>- <code>desc（string）</code>：SQL 语句执行结果的描述。执行成功，返回 <code>success</code>。执行错误，返回错误描述。<br >- <code>time（float）</code>：SQL 语句的执行时间（单位：秒）。</td>
    </tr>
  </tbody>
</table>


### 配置示例

以下示例发送 HTTP 请求，创建表 `meters`。

```shell
POST /restapi/ddl HTTP/1.1
Host: localhost:8080
Authorization: Basic cm9vdDprd2RicGFzc3dvcmQ=
Content-Type: plain/text
Accept: application/json

CREATE TABLE meters (ts timestamp not null, power int) tags(location varchar not null) primary tags (location); CREATE TABLE wind (ts timestamp not null, speed int) tags(location varchar not null) primary tags (location);
```

如果请求成功，返回以下信息：

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

## Insert 接口

Insert 接口用于发送 INSERT 语句的 HTTP 请求。该接口支持来自 EMQX 的数据插入请求。发送 INSERT API 请求的用户，需要拥有目标表的 INSERT 权限。

### 请求信息

下表列出 Insert 接口的请求信息：

<table>
  <thead>
    <tr>
      <th>信息</th>
      <th>内容</th>
      <th>说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Endpoint</td>
      <td><code>/restapi/insert</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Method</td>
      <td><code>POST</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>请求头部</td>
      <td><pre><code>Content-Type: text/plain
Accept: application/json
Authorization: Basic "token" 或 Basic "base64(user:password)"</code></pre></td>
      <td>- <code>token（string）</code>：Login 接口生成的认证令牌。<br> - <code>base64(user:password)</code>：Base64 编码后的用户名和密码信息。</td>
    </tr>
    <tr>
      <td>请求体</td>
      <td><code>"sql"</code></td>
      <td> <code>sql（string）</code>：执行的 SQL 语句。支持一次发送多条 SQL 语句，语句间使用英文分号（<code>;</code>）隔开。</td>
    </tr>
  </tbody>
</table>


### 响应信息

下表列出 Insert 接口的响应信息：

<table>
  <thead>
    <tr>
      <th>信息</th>
      <th>内容</th>
      <th>说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTTP 状态码</td>
      <td><code>HTTP/1.1 "code" "desc"</code></td>
      <td><br>- <code>code（int）</code>：HTTP 状态码。<br>- <code>desc（string）</code>：状态码描述。有关 HTTP 状态码详细信息，参见 <a href="#http-状态码">HTTP 状态码</a>。</td>
    </tr>
    <tr>
      <td>响应头部</td>
      <td><pre><code>Content-Type: application/json
Accept: text/plain</code></pre></td>
      <td> - </td>
    </tr>
    <tr>
      <td>响应体</td>
      <td><pre><code>{
  "code": "code",
  "desc": "desc1","desc2" ... "descN",
  "notice": "string",
  "time": "time"
}</code></pre></td>
      <td><br>- <code>code（int）</code>：SQL 语句执行状态码。所有语句执行成功，返回 <code>0</code>。如有执行失败的语句，返回 <code>-1</code>。<br>- <code>desc（string）</code>：每条 SQL 语句执行结果的描述。执行成功，返回 <code>success</code>。执行错误，返回错误描述。<br>- <code>rows(string)</code>：插入的数据行数。写入失败，返回 null。<br>- <code>notice（string）</code>: 写入失败的条数和原因。执行成功，返回 null。<br >- <code>time（float）</code>：SQL 语句的执行时间（单位：秒）。</td>
    </tr>
  </tbody>
</table>


### 配置示例

以下示例发送 HTTP 请求，向表 `meters` 中写入数据。

```shell
POST /restapi/insert HTTP/1.1
Host: localhost:8080
Authorization: Basic cm9vdDprd2RicGFzc3dvcmQ=
Content-Type: plain/text

insert into meters values("2023-07-30T06:44:40.32Z", "198352498", "beijing");insert into meters values("2023-07-30T06:45:40.32Z", "198352495", "beijing");
```

如果请求成功，返回以下信息：

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

如果请求失败，返回以下信息：

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

## Query 接口

Query 接口用于发送 SELECT 语句的 HTTP 请求。用户通过此接口查询数据。发送 Query API 请求的用户，需要有目标表的 SELECT 权限。目前，Query 接口支持 SELECT、SHOW CREATE TABLE、SHOW 语句。

### 请求信息

下表列出 Query 接口的请求信息：

<table>
  <thead>
    <tr>
      <th>信息</th>
      <th>内容</th>
      <th>说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Endpoint</td>
      <td><code>/restapi/query</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Method</td>
      <td><code>POST</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>请求头部</td>
      <td><pre><code>Content-Type: text/plain
Accept: application/json
Authorization: Basic "token" 或 Basic "base64(user:password)"</code></pre></td>
      <td> - <code>token（string）</code>：Login 接口生成的认证令牌。<br> - <code>base64(user:password)</code>：Base64 编码后的用户名和密码信息。</td>
    </tr>
    <tr>
      <td>请求体</td>
      <td><code>"sql"</code></td>
      <td> <code>sql（string）</code>：执行的 SQL 语句。支持一次发送多条 SQL 语句，语句间使用英文分号（<code>;</code>）隔开。</td>
    </tr>
  </tbody>
</table>


### 响应信息

::: warning 说明
查询结果可能会包含大量数据。为避免数据量过大导致性能问题，KWDB 限制了响应体的大小。最大为 5 MB，超过最大限制的数据将会被截断。
:::

下表列出 Query 接口的响应信息：

<table>
  <thead>
    <tr>
      <th>信息</th>
      <th>内容</th>
      <th>说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTTP 状态码</td>
      <td><code>HTTP/1.1 "code" "desc"</code></td>
      <td><br>- <code>code（int）</code>：HTTP 状态码。<br>- <code>desc（string）</code>：状态码描述。有关 HTTP 状态码详细信息，参见 <a href="#http-状态码">HTTP 状态码</a>。</td>
    </tr>
    <tr>
      <td>响应头部</td>
      <td><pre><code>Content-Type: application/json
Accept: text/plain</code></pre></td>
      <td> - </td>
    </tr>
    <tr>
      <td>响应体</td>
      <td><pre><code>
{
  "code": "code",
  "desc": "desc",
  "time": "time",
  "column_meta": "column_meta",
  "data": "data",
  "rows": "rows"
}</code></pre></td>
      <td><br>- <code>code（int）</code>：状态码。0 表示成功，其它值表示失败。<br>- <code>desc（string）</code>：SQL 语句执行失败对应的错误码描述。只有失败时，才会出现并返回该字段。<br >- <code>time（float）</code>：SQL 语句的执行时间（单位：秒）。<br />- <code>column_meta（array）</code>：列的元数据信息，每个列的元数据的信息形式为 <code>[column_name, column_type, type_length]</code>。其中，<code>column_name（string）</code>指列的名称，<code>column_type（string）</code>指列的数据类型，<code>type_length（int）</code> 指列的数据类型长度（单位：字节）。<br />- <code>data（array）</code>：查询的行数据。<br />- <code>rows（int）</code>：查询的数据行数。</td>
    </tr>
  </tbody>
</table>


### 配置示例

以下示例发送 HTTP 请求，查询表 `ts_table` 的内容。

```shell
POST /restapi/query HTTP/1.1
Host: localhost:8080
Authorization: Basic cm9vdDprd2RicGFzc3dvcmQ=
Content-Type: plain/text

select * from ts_table;
```

如果请求成功，返回以下信息：

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

如果请求失败，返回以下信息：

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

## Telegraf Insert 接口

Telegraf 是一款开源的数据采集器。Telegraf Insert 接口是特殊的 RESTful API 接口，用于将来自 Telegraf 的数据通过 HTTP 请求的方式写入 KWDB 数据库。与其它 API 接口不同，Telegraf Insert 接口的请求体不是 SQL 语句而是 InfluxDB Line 格式的数据。

KWDB 会将该格式的数据转为数据库可执行的 SQL 语句，然后执行对应的操作。发送 Telegraf Insert API 请求的用户，需要拥有目标表的 INSERT 权限。使用 Telegraf Insert API 向 KWDB 时序库写入数据之前，用户需要根据 Telegraf 数据及数据顺序提前在 KWDB 数据库创建好对应的时序表。

InfluxDB Line 格式的数据如下所示：

```json
<measurement>[,<tag_key>=<tag_value>[,<tag_key>=<tag_value>]] <field_key>=<field_value>[,<field_key>=<field_value>] [<timestamp>]
```

参数说明：

- `measurement`：对应数据库的表名，KWDB 根据该字段确定向时序数据库中的哪个表写入数据。用户需要根据 `measurement` 字段在 KWDB 数据库提前创建相应名称的时序表。时序表名需要与 `measurement` 字段保持一致。
- `tag_key=tag_value`：数据标签，对应 KWDB 时序数据库中表的 attribute（属性）或者 tag（标签）。创建时序表时，用户根据 `tag_key=tag_value` 字段定义对应的 `tag_key` 及 `tag_value`。
- `field_key=field_value`：表的列及列数据，多个列之间使用英文逗号（`,`）隔开。KWDB 根据 `field_key` 字段确定向表的哪个列插入对应的数据。创建时序表时，用户需要根据 `field_key=field_value` 字段名及字段顺序创建对应的列。
- `timestamp`：本行数据对应的主键时间戳。

以下示例说明如何将 InfluxDB Line 格式的数据转换为 SQL 语句，并在 KWDB 数据库中创建对应的表：

- InfluxDB Line 格式的数据

  ```sql
  meters,location=Beijing, current=17.01,voltage=220,phase=0.29 1556813561098000000
  ```

- SQL 语句

  ```sql
  create table meters (ts timestamp not null, current float, voltage int, phase float) tags (location varchar(20) not null) primary tags (location);
  ```

有关 InfluxDB Line 的详细信息，参见 [InfluxDB Line 官方文档](https://docs.influxdata.com/influxdb/v2.0/reference/syntax/line-protocol/)。

### 请求信息

下表列出 Telegraf Insert 接口的请求信息：

<table>
  <thead>
    <tr>
      <th>信息</th>
      <th>内容</th>
      <th>说明</th>
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
      <td>请求头部</td>
      <td><pre><code>Content-Type: text/plain
Accept: application/json
Authorization: Basic "token" 或 Basic "base64(user:password)"</code></pre></td>
      <td> - <code>token（string）</code>：Login 接口生成的认证令牌。<br> - <code>base64(user:password)</code>：Base64 编码后的用户名和密码信息。</td>
    </tr>
    <tr>
      <td>请求体</td>
      <td><code>"line_format"</code></td>
      <td> <code>line_format（string）</code>：待插入的 InfluxDB Line 格式的数据。KWDB 会将该格式的数据转为数据库可执行的 SQL 语句。</td>
    </tr>
  </tbody>
</table>


### 响应信息

下表列出 Telegraf Insert 接口的响应信息：

<table>
  <thead>
    <tr>
      <th>信息</th>
      <th>内容</th>
      <th>说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTTP 状态码</td>
      <td><code>HTTP/1.1 "code" "desc"</code></td>
      <td><br>- <code>code（int）</code>：HTTP 状态码。<br>- <code>desc（string）</code>：状态码描述。有关 HTTP 状态码详细信息，参见 <a href="#http-状态码">HTTP 状态码</a>。</td>
    </tr>
    <tr>
      <td>响应头部</td>
      <td><pre><code>Content-Type: application/json
Accept: text/plain</code></pre></td>
      <td> - </td>
    </tr>
    <tr>
      <td>响应体</td>
      <td><pre><code>{
  "code": "code",
  "desc": "desc",
  "rows": "rows",
  "time": "time"
}</code></pre></td>
      <td><br>- <code>code（int）</code>：SQL 语句执行状态码。所有语句执行成功，返回 <code>0</code>。如有执行失败的语句，返回 <code>-1</code>。<br>- <code>desc（string）</code>：成功时返回null，失败时返回对应的错误码描述。<br />- <code>rows（int）</code>：查询的数据行数。<br >- <code>time（float）</code>：SQL 语句的执行时间（单位：秒）。</td>
    </tr>
  </tbody>
</table>


### 配置示例

以下示例发送 HTTP 请求，创建表 `myMeasurement`。

```shell
POST /restapi/telegraf HTTP/1.1
Host: localhost:8080
Authorization: Basic cm9vdDprd2RicGFzc3dvcmQ=
Content-Type: plain/text

myMeasurement,tag1=value1,tag2=value2 fieldKey="fieldValue" 1556813561098000000
```

如果请求成功，返回以下信息：

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

如果请求失败，返回以下信息：

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

## Session 接口

Session 接口用于查询本节点会话信息或删除指定会话信息，管理员用户可查看所有会话信息和删除指定会话信息，普通用户只可查看和删除自己的会话信息。

### 请求信息

下表列出 Session 接口的请求信息：

<table>
  <thead>
    <tr>
      <th>信息</th>
      <th>内容</th>
      <th>说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Endpoint</td>
      <td><code>/restapi/session</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>Method</td>
      <td><br> - 查看会话：<code>GET</code> <br> - 删除会话：<code>DELETE</code></td>
      <td>-</td>
    </tr>
    <tr>
      <td>请求头部</td>
      <td><pre><code>Content-Type: text/plain
Accept: application/json
Authorization: Basic "token" 或 Basic "base64(user:password)"</code></pre></td>
      <td> - <code>token（string）</code>：Login 接口生成的认证令牌。<br> - <code>base64(user:password)</code>：Base64 编码后的用户名和密码信息。</td>
    </tr>
    <tr>
      <td>请求体</td>
      <td>- 查看会话：<br>空<br>- 删除会话：<br> <code>"conn_id"</code></td>
      <td><code>"conn_id"</code>：待删除的会话连接 ID，只有需要删除指定会话信息时才需要提供。</td>
    </tr>
  </tbody>
</table>


### 响应信息

下表列出查看会话信息的响应信息：

<table>
  <thead>
    <tr>
      <th>信息</th>
      <th>内容</th>
      <th>说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTTP 状态码</td>
      <td><code>HTTP/1.1 "code" "desc"</code></td>
      <td><br>- <code>code（int）</code>：HTTP 状态码。<br>- <code>desc（string）</code>：状态码描述。有关 HTTP 状态码详细信息，参见 <a href="#http-状态码">HTTP 状态码</a>。</td>
    </tr>
    <tr>
      <td>响应头部</td>
      <td><pre><code>Content-Type: application/json
Accept: text/plain</code></pre></td>
      <td> - </td>
    </tr>
    <tr>
      <td>响应体</td>
      <td><pre><code>{
    "code": "code",
    "conns": [{"conn_info"}]
}</code></pre></td>
      <td><br>- <code>code（int）</code>：状态码。<code>0</code>表示成功，其它值表示失败。 <br>- <code>conn_info</code>：会话连接相关信息，如连接ID、用户名、令牌、超时时间等。</td>
    </tr>
  </tbody>
</table>


下表列出删除会话的响应信息：

<table>
  <thead>
    <tr>
      <th>信息</th>
      <th>内容</th>
      <th>说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTTP 状态码</td>
      <td><code>HTTP/1.1 "code" "desc"</code></td>
      <td><br>- <code>code（int）</code>：HTTP 状态码。<br>- <code>desc（string）</code>：状态码描述。有关 HTTP 状态码详细信息，参见 <a href="#http-状态码">HTTP 状态码</a>。</td>
    </tr>
    <tr>
      <td>响应头部</td>
      <td><pre><code>Content-Type: application/json
Accept: text/plain</code></pre></td>
      <td> - </td>
    </tr>
    <tr>
      <td>响应体</td>
      <td><pre><code>{
  "code": "code",
  "desc": "desc"
}</code></pre></td>
      <td><br>- <code>code（int）</code>：状态码。<code>0</code>表示成功，其它值表示失败。。<br>- <code>desc（string）</code>：删除操作的结果描述。</td>
    </tr>
  </tbody>
</table>


### 配置示例

示例 1：以下示例发送 HTTP 请求，查看会话信息。

```shell
GET /restapi/session HTTP/1.1
Content-Type: text/plain
Accept: application/json
Authorization: Basic cm9vdDprd2RicGFzc3dvcmQ=
```

如果请求成功，返回以下信息：

- 普通用户：查看自己正在使用的会话的信息。

    ```json
  {"code":0,
  "conns":[
  {"Connid":"50830553-3e83-11ef-a323-b4055d17f786","Username":"u1","Token":"c2ff2c6d*","MaxLife Time":3600,"LastLoginTime":"2024-07-10 06:11:58","ExpirationTime":"2024-07-10 07:11:58"}
  ]
  }
  ```

- 管理员用户：查看所有会话的相关信息。

  ```json
  {"code":0,
  "conns":[
  {"Connid":"50830553-3e83-11ef-a323-b4055d17f786","Username":"u1","Token":"c2ff2c6d*","MaxLife Time":3600,"LastLoginTime":"2024-07-10 06:11:58","ExpirationTime":"2024-07-10 07:11:58"},
  {"Connid":"9bf2fa13-3e83-11ef-a323-b4055d17f786","Username":"u1","Token":"f9f3a39d*","MaxLife Time":3600,"LastLoginTime":"2024-07-10 06:14:04","ExpirationTime":"2024-07-10 07:14:04"}
  ]
  }
  ```

示例 2：以下示例发送 HTTP 请求，删除会话。

```shell
DELETE /restapi/session HTTP/1.1
Content-Type: text/plain
Accept: application/json
Authorization: Basic cm9vdDprd2RicGFzc3dvcmQ=

0339f5b5-c492-11ee-a7c9-000c29066670
```

如果请求成功，返回以下信息：

```json
{
  "code":0,
  "desc": "Delete Success"
}
```

## 认证方式

出于安全考虑，KWDB 的所有 RESTful API 请求使用 HTTPS 发送，并通过 HTTP Header 进行身份认证。
HTTP Header 支持以下认证方式：

**用户名及密码认证**

用户在 HTTP 请求的 Header 中添加经过 Base64 编码的数据库用户名和密码信息。认证通过后，系统会自动创建一个临时令牌用于身份认证，并在请求响应结束后自动销毁该令牌。用户名及密码认证方式操作简便，且不受连接数限制，但对系统性能要求较高，适用于数据量较小且性能要求不高的场景。

**Token 认证**

用户通过调用 RESTful API 的登录接口（Login）获取令牌。在后续的 API 调用中（例如 DDL 接口、Insert 接口等），可以在请求 Header 中使用该令牌进行认证。令牌的默认有效期为 60 分钟。用户可以通过执行 `set cluster setting server.rest.timeout=<value>` SQL 语句来实时调整令牌的有效期，范围为 [1, 2^63-1] 分钟。令牌认证免除了临时令牌的创建和销毁过程，更适合对性能要求较高的场景。

在使用 RESTful API 进行并发编程时，每个线程应分配一个独立的令牌，以确保业务操作的顺利进行。并发连接数的限制为 100。

HTTPS 使用 SSL 加密数据，在与 KWDB 数据库进行加密通信时，需要将 KWDB 服务端生成的证书拷贝到发起请求客户端能访问的路径下，具体操作见示例 3。

示例 1：使用用户名及密码认证

```shell
<!--请求-->
POST /restapi/ddl HTTP/1.1
Host: localhost:8080
Authorization: Basic dTE6a3dkYnBhc3N3b3Jk
Content-Type: plain/text
Accept: application/json

CREATE TABLE ts_table(ts timestamp not null, power int) tags(location varchar(15) not null) primary tags (location);
```

示例 2：使用令牌认证

```shell
<!--请求-->
POST /restapi/ddl HTTP/1.1
Host: localhost:8080
Authorization: Basic cm9vdDprd2RicGFzc3dvcmQ=
Content-Type: plain/text
Accept: application/json

CREATE TABLE ts_table(ts timestamp not null, power int) tags(location varchar(15));
```

示例 3：与 KWDB 数据库进行加密通信

1. 以安全模式部署和启动数据库。
2. 使用 SQL 语句在数据库中创建新用户。

    ```sql
    create user rest_user password 'user123456';
    ```
3. 将 KWDB 服务端生成的证书拷贝到发起请求客户端可访问的路径下。证书默认存放目录为`/etc/kaiwudb/certs`。
4. 使用安全证书进行 Restful API 连接。

    - 登录示例
    
      ```bash
      curl -L --cacert ../certs/ca.crt -H "Authorization: Basic dTE6a3dkYnBhc3N3b3Jk" -X GET your-host-ip:port/restapi/login
      ```
    - 查询示例

      ```bash
      curl -L -H "Content-Type:text/plain" -H "Authorization: Basic dTE6a3dkYnBhc3N3b3Jk"  --cacert ../certs/ca.crt -d "select*from t1;" -X POST your-host-ip:port/restapi/query?db=db1
      ```

## HTTP 状态码

每次 HTTP 请求完成后，系统都会返回一个 HTTP 状态码。下表列出 KWDB RESTful API 使用的 HTTP 状态码。

| HTTP 状态码 | 描述          |
| ------------------------------------------ | -------------------------------------------- |
| 200                                        | 成功                                         |
| 400                                        | 参数错误                                     |
| 401                                        | 认证失败                                     |
| 404                                        | URL不存在                                   |
| 500                                        | 内部错误                                    |
| 503                                        | 系统资源不足                                 |
