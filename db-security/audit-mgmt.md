---
title: 审计管理
id: audit-mgmt
---

# 审计管理

数据库审计以安全事件为中心，以全面审计和精确审计为基础，实时记录数据库活动，对数据库操作进行细粒度审计的合规性管理。通过记录、分析和汇报用户访问数据库的行为，帮助用户事后生成合规报告、追溯事故根源。通过大数据搜索技术提供高效查询审计报告，定位事件原因，以便日后查询、分析、过滤，加强内外部数据库网络行为的监控与审计，提高数据资产安全。

KWDB 支持监控和记录包括管理员在内的所有用户操作，提供三个级别的审计：

- **系统级审计**：开启审计功能后自动启动，无需额外配置
- **语句级审计**：审计数据库管理语句的执行，包括 DDL 语句（如创建用户、创建表等）以及系统管理操作（如作业控制、会话管理等）
- **对象级审计**：审计 DML 语句的执行，如对特定表或视图进行的查询、插入、更新、删除等数据操作

下表列出 KWDB 支持的系统级审计操作。

| 对象            | 操作                                                                         |
| --------------- | ---------------------------------------------------------------------------- |
| NODE            | - 重启（RESTART）<br >- 退役（DECOMMISON）<br >- 复役（RECOMMISION）<br >- 退出（QUIT）<br >- 加入（JOIN） |
| CONNECT         | - 登录（LOGIN）<br >- 登出（LOGOUT）                                                  |
| CLUSTER SETTING | - 设置（SET）<br >- 重置（RESET）                                                      |

用户需要通过 SQL 语句创建、启用相应的语句级和对象级审计策略。

下表列出 KWDB 支持的语句级审计操作。

| 对象       | 关系数据库                                                              | 时序数据库                                                          |
| ---------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------- |
| USER       | - CREATE USER <br >- ALTER USER <br >- DROP USER                                    | - CREATE USER <br >- ALTER USER <br >- DROP USER                                 |
| ROLE       | - CREATE ROLE <br >- ALTER ROLE <br >- GRANT ROLE <br >- REVOKE ROLE  <br >- DROP ROLE           | - CREATE ROLE <br >- ALTER ROLE <br >- GRANT ROLE <br >- REVOKE ROLE  <br >- DROP ROLE        |
| DATABASE   | - CREATE DATABASE <br >- ALTER DATABASE <br >- DROP DATABASE <br >- IMPORT <br >- EXPORT       | - CREATE DATABASE <br >- ALTER DATABASE <br >- DROP DATABASE <br >- IMPORT <br >- EXPORT |
| SCHEMA     | - CREATE SCHEMA <br >- DROP SCHEMA                                            | -                                                                   |
| TABLE      | - CREATE TABLE <br >- ALTER TABLE <br >- DROP TABLE <br >- TRUNCATE TABLE <br >- IMPORT <br >- EXPORT | - CREATE TABLE <br >- ALTER TABLE <br >- DROP TABLE <br >- IMPORT <br >- EXPORT            |
| VIEW       | - CREATE VIEW <br >- ALTER VIEW <br >- DROP VIEW                                    | -                                                                   |
| INDEX      | - CREATE INDEX <br >- ALTER INDEX <br >- DROP INDEX                                 | -                                                                   |
| SEQUENCE   | - CREATE SEQUENCE <br >- ALTER SEQUENCE <br >- DROP SEQUENCE                        | -                                                                   |
| PRIVILEGE  | - GRANT PRIVILEGE <br >- REVOKE PRIVILEGE                                     | - GRANT PRIVILEGE <br >- REVOKE PRIVILEGE                                 |
| AUDIT      | - CREATE AUDIT <br >- ALTER AUDIT <br >- DROP AUDIT                                 | - CREATE AUDIT <br >- ALTER AUDIT <br >- DROP AUDIT                             |
| QUERY      | - CANCEL QUERY <br >- EXPLAIN QUERY                                           | - CANCEL QUERY <br >- EXPLAIN QUERY                                       |
| JOB        | - CANCEL JOB <br >- PAUSE JOB <br >- RESUME JOB                                     | - CANCEL JOB <br >- PAUSE JOB <br >- RESUME JOB                                  |
| SCHEDULE   | - ALTER SCHEDULE <br >- PAUSE SCHEDULE <br >- RESUME SCHEDULE                       | - ALTER SCHEDULE <br >- PAUSE SCHEDULE <br >- RESUME SCHEDULE                   |
| SESSION    | - SET SESSION <br >- RESET SESSION <br >- CANCEL SESSION                            | - SET SESSION <br >- RESET SESSION <br >- CANCEL SESSION                        |
| STATISTICS | CREATE STATISTICS                                                     | CREATE STATISTICS                                                 |

下表列出 KWDB 支持的对象级审计操作。

| 对象  | 关系数据库                       | 时序数据库                                                              |
| ----- | -------------------------------- | ----------------------------------------------------------------------- |
| TABLE | - INSERT <br >- SELECT <br >- UPDATE <br >- DELETE |- INSERT <br >- SELECT <br >- UPDATE <br >- DELETE <br >其中，UPDATE 和 DELETE 只支持报错审计。 |
| VIEW  | SELECT                         | -                                                                       |

开启审计功能后，系统会默认将审计结果保存在审计日志文件中。更多审计日志相关的信息，参见[审计日志](#审计日志)。

## 开启审计功能

默认情况下，系统关闭审计功能，如需对用户操作进行审计，需要通过 SQL 语句开启审计功能。

### 前提条件

用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。

### 参数说明

无

### 语法格式

```sql
SET CLUSTER SETTING audit.enabled = true;
```

## 管理审计策略

KWDB 支持使用 SQL 语句创建、启用、修改、删除语句级和对象级审计策略。用户无需设置系统级审计策略。开启审计功能后，系统自动启动系统级审计。一旦发生支持的系统级审计操作，系统会自动生成相应的审计日志。

### 创建审计策略

`CREATE AUDIT` 语句用于创建语句级、对象级审计策略。

#### 前提条件

用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。

#### 语法格式

```sql
CREATE AUDIT [IF NOT EXISTS] <audit_name>
ON [ALL | <target_type> [<target_name>]]
FOR [ALL | <operations>]
TO [ALL | <operators>]
[WHENEVER [ALL]];
```

#### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF NOT EXISTS` | 可选关键字。当使用 `IF NOT EXISTS` 关键字时，如果目标审计策略不存在，系统创建审计策略。如果目标审计策略存在，系统创建审计策略失败，但不会报错。当未使用 `IF NOT EXISTS` 关键字时，如果目标审计策略不存在，系统创建审计策略。如果目标审计策略存在，系统报错，提示目标审计策略已存在。 |
| `audit_name` | 审计策略的名称。审计策略名称必须唯一。 |
| `target_type` | 审计对象类型。支持 user、role、database、schema、table、view、index、sequence、privilege、audit、query、job、schedule、session、statistics。支持使用 `ALL` 作为参数值，表示对所有对象类型进行审计。 |
| `target_name` | 可选参数。审计对象的名称，格式为 `database_name.target_name` 或 `target_name`。<br/>- 指定对象名称时：进行对象级审计，审计对指定对象的数据操作。如未指定数据库，则默认使用当前数据库。<br/>- 未指定对象名称时：进行语句级审计，审计与该对象类型相关的管理语句。<br/>**注意：** <br/>1. 进行对象级审计时，对象类型必须是 table 或 view。<br/>2. 指定具体对象名称时，只能进行对象级审计。 |
| `operations` | 审计操作。支持指定一个或多个审计操作，审计操作之间使用逗号（`,`）隔开。支持使用 `ALL` 作为参数值，表示对所有操作进行审计。支持的审计操作取决于对象可执行的操作。 |
| `operators` | 用户或角色名称。支持指定一个或多个用户或角色，用户或角色名称之间使用逗号（`,`）隔开。支持使用 `ALL` 作为参数值，表示对所有用户和角色进行审计。 |
| `WHENEVER` | 可选关键字，指定执行审计的条件。默认为 `ALL`，且只支持设置为 `ALL`，表示总是记录审计。 |

#### 语法示例

- 创建语句级审计策略。

    以下示例创建 `atest` 语句级审计策略，对 root 用户执行的数据库创建操作进行审计。

    ```sql
    CREATE AUDIT atest ON DATABASE FOR create TO root;
    ```

- 创建对象级审计策略。

    以下示例创建 `atest` 对象级审计策略，对 root 用户执行的 `t1` 表的查询操作进行审计。

    ```sql
    CREATE AUDIT atest ON TABLE t1 FOR SELECT TO root;
    ```

### 修改审计策略

`ALTER AUDIT` 语句用于启用、禁用、重命名审计策略。

#### 前提条件

用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。

#### 语法格式

```sql
ALTER AUDIT [IF EXISTS] <audit_name> [ENABLE | DISABLE | RENAME TO <new_name>];
```

#### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF  EXISTS` | 可选关键字。当使用 `IF EXISTS` 关键字时，如果目标审计策略存在，系统修改目标审计策略。如果目标审计策略不存在，系统修改审计策略失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果目标审计策略存在，系统修改审计策略。如果目标审计策略不存在，系统报错，提示目标审计策略不存在。 |
| `audit_name` | 当前的审计策略名称。|
| `ENABLE` | 启用审计策略。默认情况下，禁用审计策略。 |
| `DISABLE` | 禁用审计策略。 |
| `new_name` | 新的审计策略名称。审计策略名称必须唯一。 |

#### 语法示例

- 启动审计策略。

    以下示例启用 `atest` 审计策略。

    ```sql
    ALTER AUDIT atest ENABLE;
    ```

- 重命名审计策略。

    以下示例将 `atest` 审计策略重命名未 `btest`。

    ```sql
    ALTER AUDIT atest RENAME TO btest;
    ```

### 查看审计策略

`SHOW AUDITS` 语句用于查看已创建的审计策略。

#### 前提条件

无

#### 语法格式

```sql
SHOW AUDITS [ON <target_type> [<target_name>] [FOR <operations>] [TO <operators>]];
```

#### 参数说明

| 参数 | 说明 |
| --- | --- |
| `target_type` | 可选参数，审计对象类型。支持 user、role、database、schema、table、view、index、sequence、privilege、audit、query、job、schedule、session、statistics。支持使用 `ALL` 作为参数值，表示查看所有对象的审计策略。 |
| `target_name` | 可选参数，数据库已存在的审计对象的名称。格式为 `database_name.target_name`。如果只提供了审计对象名称，则默认对查看当前数据库中指定对象的审计策略。如未指定对象名称，KWDB 查看指定对象的审计策略。<br > **说明** <br >如果对象类型为 database，无法指定对象名称。 |
| `operations` | 可选参数，审计操作。支持指定一个或多个审计操作，审计操作之间使用逗号（`,`）隔开。 |
| `operators` | 可选参数，用户或角色名称。支持指定一个或多个用户或角色，用户或角色名称之间使用逗号（`,`）隔开。 |

#### 语法示例

- 查看所有审计策略。

    ```sql
    SHOW AUDITS;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      audit_name | target_type | target_name | target_id | operations | operators | condition | whenever | action | level | enable
    -------------+-------------+-------------+-----------+------------+-----------+-----------+----------+--------+-------+---------
      b          | ALL         |             |         0 | ALL        | rest_user |         0 | ALL      |      0 |     0 | false
      c          | DATABASE    |             |         0 | ALL        | rest_user |         0 | ALL      |      0 |     0 | false
      d          | ALL         |             |         0 | ALL        | rest_user |         0 | ALL      |      0 |     0 | false
    (3 rows)
    ```

- 查看指定对象类型的审计策略。

    ```sql
    SHOW AUDITS ON DATABASE;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      audit_name | target_type | target_name | target_id | operations | operators | condition | whenever | action | level | enable
    -------------+-------------+-------------+-----------+------------+-----------+-----------+----------+--------+-------+---------
      c          | DATABASE    |             |         0 | ALL        | rest_user |         0 | ALL      |      0 |     0 | false
    (1 row)
    ```

### 删除审计策略

`DROP AUDIT` 语句用于删除已创建的审计策略。

#### 前提条件

用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。

#### 语法格式

```sql
DROP AUDIT [IF EXISTS] <audit_name>;
```

#### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF  EXISTS` | 可选关键字。当使用 `IF EXISTS` 关键字时，如果目标审计策略存在，系统删除目标审计策略。如果目标审计策略不存在，系统删除审计策略失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果目标审计策略存在，系统删除审计策略。如果目标审计策略不存在，系统报错，提示目标审计策略不存在。 |
| `audit_name` | 审计策略的名称。支持同时删除多个审计策略，审计策略名称之间使用逗号（`,`）隔开。|

#### 语法示例

以下示例删除 `btest` 审计策略。

```sql
DROP AUDIT btest;
```

## 审计日志

默认情况下，开启审计功能后，系统将审计结果保存在审计日志文件中。如需关闭审计日志，使用以下 SQL 语句将 `audit.log.enabled` 设为 `false`。

```sql
SET CLUSTER SETTING audit.log.enabled=false;
```

审计日志文件包含以下信息：

| 字段             | <div style="width:275px">说明</div>                                                                                                                                                                                                                                                                           | 示例                                                                                                                                        |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 日志级别和日期   | 审计日志的级别和记录日期，其中日志级别为 I。                                                                                                                                                                                                                                   | `I240415`                                                                                                                                     |
| 时间             | UTC 格式的时间戳。                                                                                                                                                                                                                                                               | `06:49:34.207014`                                                                                                                             |
| goroutine id     | 记录该审计的 goroutine ID。                                                                                                                                                                                                                                                      | `538`                                                                                                                                         |
| 审计源码文件路径 | 打印日志的源码文件及代码行。                                                                                                                                                                                                                                                     | `security/audit/actions/record_to_log.go:45`                                                                                                  |
| 节点             | 记录审计日志的节点 ID。                                                                                                                                                                                                                                                          | `[n1]`                                                                                                                                        |
| 日志输入计数     | 历史累计审计消息数。                                                                                                                                                                                                                                                             | `3`                                                                                                                                           |
| 事件发生时间     | 审计事件的发生时间。                                                                                                                                                                                                                                                             | `"EventTime":"2024-04-15T06:49:34.206948441Z"`                                                                                               |
| 事件执行时间     | 审计事件的执行时间间隔。                                                                                                                                                                                                                                                         | `"Elapsed":2242701`                                                                                                                          |
| 用户信息         | 用户和角色信息，包括以下字段：<br >- `UserID`：预留字段，执行事件的用户 ID，默认值为 `0`。 <br >- `Username`：执行事件的用户名称。 <br >- `Roles`：角色信息，其中 `ID` 是预留字段，表示执行事件的角色 ID，默认值为 `0`。`Name` 表示执行事件的角色名称。     | `"User":{"UserID":0,"Username":"root","Roles":[{"ID":0,"Name":"admin"}]}`                                                                    |
| 事件类型         | 在对象上的操作类型，例如创建、删除等                                                                                                                                                                                                                                           | `"Event":"CREATE"`                                                                                                                           |
| 操作对象         | 操作对象的信息，包括以下字段：<br >- `Typ`：操作对象类型。 <br >- `Targets`：具体的操作对象信息，支持一个或多个操作对象。 <br >- `ID`：操作对象 ID。 <br >- `Name`：操作对象的名称。 <br >- `Cascades`：是否级联删除对象。                                                                       | `"Target":{"Typ":"DATABASE","Targets":{"78":{"ID":78,"Name":"db1","Cascades":null}}}`                                                        |
| 审计级别         | - 系统级：0 <br >- 语句级：1 <br >- 对象级：2                                                                                                                                                                                                                                                | `"Level":1`                                                                                                                                   |
| 客户端信息       | 客户端信息，包括以下字段：<br >- `AppName`：客户端应用名称。 <br >- `Address`：客户端地址，包含 IP 地址和端口。                                                                                                                                                  | `Client":{"AppName":"$ kwbase sql","Address":"127.0.0.1:55564"}`                                                                              |
| 事件执行结果     | 事件执行结果，包括以下字段：<br >- `Status`：事件执行的状态，`OK` 表示成功，`FAIL` 表示失败。 <br >- `ErrMsg`：事件的错误信息。 <br >- `RowsAffected`：受影响的行数。               | `"Result":{"Status":"OK","ErrMsg":"","RowsAffected":0}` |
| 执行语句         | 执行语句信息，包括以下字段：<br >- `Cmd`：执行的语句。 <br >- `Params`：执行的参数。                                                                                                                                                                                         | `"Command":{"Cmd":"CREATE DATABASE db1","Params":"{}`"}                                                                                       |
| 审计事件记录节点 | 审计事件记录节点的信息，包括以下字段：<br >- `ClusterID`：集群 ID。 <br >- `NodeID`：节点 ID。 <br >- `HostIP`：节点的 IP 地址。 <br >- `HostPort`：节点端口。 <br >- `HostMac`：节点的 MAC 地址。 <br >- `LastUp`：预留字段，节点上一次启动时间，默认值为 `0`。 | `"Reporter":{"ClusterID":"ae93118d-28bc-492f-bd4f-852cafab0ad9","NodeID":1,"HostIP":"localhost","HostPort":"26257","HostMac":"","LastUp":0}}` |

审计日志示例：

```xml
I240415 06:49:34.207014 538 security/audit/actions/record_to_log.go:45  [n1] 3 {"EventTime":"2024-04-15T06:49:34.206948441Z","Elapsed":2242701,"User":{"UserID":0,"Username":"root","Roles":[{"ID":0,"Name":"admin"}]},"Event":"CREATE","Target":{"Typ":"DATABASE","Targets":{"78":{"ID":78,"Name":"db1","Cascades":null}}},"Level":1,"Client":{"AppName":"$ kwbase sql","Address":"127.0.0.1:55564"},"Result":{"Status":"OK","ErrMsg":"","RowsAffected":0},"Command":{"Cmd":"CREATE DATABASE db1","Params":"{}"},"Reporter":{"ClusterID":"ae93118d-28bc-492f-bd4f-852cafab0ad9","NodeID":1,"HostIP":"localhost","HostPort":"26257","HostMac":"","LastUp":0}}
```
