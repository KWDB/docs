---
title: MySQL 原生协议支持
id: mysql-protocol
---

# KWDB MySQL 原生协议支持

自 KWDB V3.3.0 起，KWDB 在独立端口上提供 MySQL 客户端线协议支持，使 MySQL 生态的驱动、应用与工具无需更换驱动即可直接连接 KWDB，执行 SQL 并读取关系表与时序表数据。

## 概述

KWDB 此前仅提供 PostgreSQL 线协议，MySQL 生态的应用、驱动（如 Connector/J、mysql-connector-python、go-sql-driver/mysql）及客户端工具（如 DBeaver、mysql CLI）无法直接连接，用户需改用 PG 驱动并改造应用侧代码。

MySQL 协议与 PostgreSQL 协议在连接建立时的行为存在本质差异（MySQL 由服务端先发包，PostgreSQL 由客户端先发包），且无法通过首字节分流复用同一端口。因此，MySQL 协议服务必须监听独立端口，与现有的 PostgreSQL 端口互不干扰。

::: warning 说明
MySQL 协议支持默认关闭，需显式配置监听地址后才会启用。未配置时的部署行为与之前版本完全一致，不影响现有的 PostgreSQL 链路。
:::

## 启用方式

在启动 KWDB 服务进程时，通过 `--mysql-addr` 参数指定 MySQL 协议的监听地址和端口。

```shell
kwbase start --mysql-addr=0.0.0.0:3306
```

::: warning 说明
`--mysql-addr` 仅接受独立的监听地址，不能与 PostgreSQL 协议共用端口。PostgreSQL 协议默认监听端口为 26257，MySQL 协议建议使用 3306 或其他未被占用的端口。
:::

## 支持的认证方式

KWDB MySQL 协议支持以下三种密码认证插件，每种插件均可通过 TLS/SSL 加密传输或 RSA 公钥交换加密传输凭据：

| 认证插件 | 说明 | 支持情况 |
| --- | --- | --- |
| `caching_sha2_password` | MySQL 8.0 默认认证插件 | 支持 |
| `mysql_native_password` | MySQL 5.7 及更早版本默认认证插件 | 支持 |
| `sha256_password` | SHA-256 哈希认证插件 | 支持 |

各认证插件的传输加密覆盖情况如下：

| 认证插件 | TLS/SSL 加密传输 | RSA 公钥交换加密传输 | 无加密快速路径 |
| --- | --- | --- | --- |
| `caching_sha2_password` | 支持 | 支持 | 支持（凭据缓存命中时） |
| `mysql_native_password` | 支持 | 不适用 | 支持 |
| `sha256_password` | 支持 | 支持 | 不支持 |

服务端同时上报 `CLIENT_SSL` 能力位，客户端可根据自身配置选择是否升级到 TLS 加密连接。

## 支持的协议特性

### 连接与握手

- 服务端在独立端口监听 MySQL 协议握手请求，回复握手初始化包。
- 支持能力位（capability flags）协商，包括客户端支持的协议版本、认证插件、是否支持预处理语句等。
- 连接 ID 取自独立的握手计数器，确保每个连接获得唯一标识（此前 PG 链路上报的连接 ID 取自存活连接数，串行建立的连接可能重复）。
- 上报 `NO_BACKSLASH_ESCAPES` 状态位，与 KWDB 的 `standard_conforming_strings = on` 行为保持一致，避免客户端按 MySQL 默认规则做反斜杠转义导致的字面量错误。

### 文本协议

KWDB MySQL 协议支持以下核心命令：

| 命令 | 说明 | 支持情况 |
| --- | --- | --- |
| `COM_QUERY` | 执行 SQL 查询或语句 | 支持 |
| `COM_INIT_DB` | 切换当前数据库 | 支持 |
| `COM_PING` | 心跳探测 | 支持 |
| `COM_RESET_CONNECTION` | 重置连接会话 | 支持 |
| `COM_QUIT` | 断开连接 | 支持 |
| `COM_CHANGE_USER` | 切换用户 | 不支持 |

### 二进制协议与预处理语句

- 支持 `COM_STMT_PREPARE`、`COM_STMT_EXECUTE`、`COM_STMT_CLOSE`、`COM_STMT_RESET`、`COM_STMT_SEND_LONG_DATA` 等二进制协议命令。
- 预处理语句中的 `?` 占位符在执行前被改写为 KWDB 内部 SQL 引擎使用的 `$N` 形式，结果编码层按 MySQL 二进制协议输出列定义与行数据。
- 文本协议与二进制协议共享同一 SQL 执行引擎与事务/会话状态。

### 结果集与错误码

- PostgreSQL SQLSTATE 映射为 MySQL 错误码（如密码错误返回 SQLSTATE `28000` / MySQL 错误码 `1045`）。
- 支持多结果集分帧（多条语句用分号分隔一次提交时）。
- 零列结果集按 MySQL 协议正确编码。

### MySQL 方言兼容

驱动在握手完成后会立即发送若干 MySQL 特有语句进行初始化，任何一条失败都会导致连接无法建立。KWDB 在 MySQL 协议层内增加了语句改写层，透明处理常见的驱动初始化语句：

| MySQL 语句/函数 | 改写为 KWDB 等价形式 |
| --- | --- |
| `@@x`（系统变量读取） | `current_setting('x', true)`，合成 `AS "@@x"` 保持列标签 |
| `USER()` | `current_user()` |
| `CONNECTION_ID()` | 内联该连接的握手编号 |
| `SET character_set_results = NULL` | 接受为空操作 |
| `SET SESSION TRANSACTION ...` | 映射为会话默认的隔离级别 / 只读属性 |

部分变量由于 KWDB 取值与 MySQL 客户端预期不一致，采用覆盖表返回值而非照抄 KWDB 的实际配置：

- `transaction_isolation`：KWDB 的拼写与 MySQL Connector/J 映射表不符，改写后返回 MySQL 兼容的隔离级别名称。
- `autocommit`：KWDB 返回的 `on` 会被 `Boolean.parseBoolean` 读成 `false`，改写后返回 `1` / `0`。
- `transaction_read_only`：KWDB 返回的 `off` 会让 `Integer.parseInt` 抛异常，改写后返回 `0` / `1`。

::: warning 说明
语句改写在 MySQL 协议层内部进行，未修改 KWDB 的 SQL 语法定义。因此：

- PostgreSQL 客户端不会因这些改写行为受到影响。
- 字符串字面量、注释、反引号内的 `@@` 在结构上不可能被误改。
- 一条语句中任一项不可识别则整句不改写，原样透传至 SQL 引擎。
:::

## 基本操作支持

### DDL、DML 与查询

通过 MySQL 协议连接的客户端可正常执行以下操作：

- 创建、删除、修改关系数据库与时序数据库
- 创建、删除、修改关系表与时序表
- 插入、更新、删除数据
- 查询数据（包括聚合、分组、排序、时序窗口等）
- 执行事务（BEGIN / COMMIT / ROLLBACK）
- 使用 MySQL 客户端工具（如 mysql CLI）查看和管理数据库对象

::: warning 说明
KWDB 的 DDL 语法与 MySQL 存在差异，例如时序表使用 `CREATE TABLE ... TAGS (...)` 语法。MySQL 客户端连接 KWDB 时，SQL 语句需遵循 KWDB 的语法，而非 MySQL 原生语法。
:::

## 支持的客户端和驱动

以下客户端和驱动可连接 KWDB 的 MySQL 协议端口：

- mysql CLI 8.0.46
- libmysqlclient
- go-sql-driver/mysql
- MySQL Connector/J 8.4.0

## 已知限制与差异

### 功能限制

| 项目 | 说明 |
| --- | --- |
| 时间戳输出精度 | 仅输出到微秒（部分驱动无法解析纳秒） |
| 时序表 INSERT 路径 | 在 MySQL 协议连接上不走 `insert_direct` 快速路径，写入性能略有差异 |
| `COM_CHANGE_USER` | 不支持 MySQL 协议的切换用户命令 |
| `SET SESSION TRANSACTION` 语义 | 改写为设置会话默认值，从下一个事务开始生效，不改变已开始的事务 |

### 与 PostgreSQL 协议的差异

MySQL 协议结果输出格式与 KWDB PostgreSQL 链路存在以下固有差异：

| 项目 | MySQL 协议 | PostgreSQL 协议 |
| --- | --- | --- |
| 布尔值文本格式 | `1` / `0` | `t` / `f` |
| TIMETZ 输出格式 | MySQL 兼容格式 | PostgreSQL 原生格式 |
| 数组/元组/区间输出格式 | MySQL 兼容格式 | PostgreSQL 原生格式 |

上述差异不影响数据读取正确性，仅影响结果集的文本呈现方式。

### 连接行为

MySQL 协议连接的 `transaction_read_only` 和 `transaction_isolation` 会话变量通过改写层模拟，实际隔离级别和只读属性在 KWDB 内核中按 PostgreSQL 语义生效。

## 兼容性与灰度保护

MySQL 协议支持引入以下灰度保护机制，确保现有部署不受影响：

- **默认关闭**：`mysql-addr` 配置项默认值为空串。服务进程仅在其非空时创建 MySQL 监听器，未配置时 `s.mysqlServer` 为 `nil`，不会占用任何端口。
- **独立端口**：MySQL 协议使用独立的 TCP 监听端口，与 PostgreSQL 协议端口完全分离，互不干扰。
- **不修改 SQL 语法**：MySQL 方言兼容层在协议层内部完成，未改动 KWDB 的 SQL 语法定义（`sql.y`），PostgreSQL 客户端不会意外接受 MySQL 语法。
- **用户凭据向后兼容**：`system.users` 表新增的 MySQL 认证列对现有 PostgreSQL 链路完全透明，既有集群通过 `sqlmigrations` 自动补列。
