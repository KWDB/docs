---
title: Audit Management
id: audit-mgmt
---

# Audit Management

Database audit is centered on security events and based on comprehensive and accurate audit. It achieves compliance management through real-time recording of database activities and fine-grained audit of database operations. By logging, analyzing, and reporting access to databases, it helps generate post-event compliance reports and trace the root causes of events. Leveraging big data search technology, it provides efficient querying of audit reports to locate the cause of an event for later query, analysis and filter. This strengthens the monitoring and audit of internal and external database behaviors, enhancing the security of data assets.

KWDB supports monitoring and logging user operations, including those of administrators, and audits system-level, statement-level, and object-level operations. When database audit is enabled, the system automatically initiates system-level audit.

This table lists all the system-level audit operations supported by KWDB.

| Object          | Operation                                                              |
|-----------------|------------------------------------------------------------------------|
| NODE            | - RESTART <br >- DECOMMISON <br >- RECOMMISION <br >- QUIT <br >- JOIN |
| CONNECT         | - LOGIN <br >- LOGOUT                                                  |
| CLUSTER SETTING | - SET <br >- RESET                                                     |

You can use SQL statements to create or enable related statement-level and object-level audit policies.

This table lists all the statement-level audit operations supported by KWDB.

| Object     | Relational Database                                                                                   | Time-series Database                                                                     |
|------------|-------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| USER       | - CREATE USER <br >- ALTER USER <br >- DROP USER                                    | - CREATE USER <br >- ALTER USER <br >- DROP USER                                 |
| ROLE       | - CREATE ROLE <br >- ALTER ROLE <br >- GRANT ROLE <br >- REVOKE ROLE  <br >- DROP ROLE           | - CREATE ROLE <br >- ALTER ROLE <br >- GRANT ROLE <br >- REVOKE ROLE  <br >- DROP ROLE        |
| DATABASE   | - CREATE DATABASE <br >- ALTER DATABASE <br >- DROP DATABASE <br >- IMPORT <br >- EXPORT       | - CREATE DATABASE <br >- ALTER DATABASE <br >- DROP DATABASE <br >- IMPORT <br >- EXPORT |
| SCHEMA     | - CREATE SCHEMA <br >- DROP SCHEMA                                            | -                                                                   |
| TABLE      | - CREATE TABLE <br >- ALTER TABLE <br >- DROP TABLE <br >- TRUNCATE TABLE <br >- IMPORT <br >- EXPORT | - CREATE TABLE <br >- ALTER TABLE <br >- DROP TABLE <br >- IMPORT <br >- EXPORT            |
| VIEW       | - CREATE VIEW <br >- ALTER VIEW <br >- DROP VIEW                                    | -                                                                   |
| INDEX      | - CREATE INDEX <br >- ALTER INDEX <br >- DROP INDEX                                 | - CREATE INDEX <br >- ALTER INDEX <br >- DROP INDEX                                                                   |
| SEQUENCE   | - CREATE SEQUENCE <br >- ALTER SEQUENCE <br >- DROP SEQUENCE                        | -                                                                   |
| PRIVILEGE  | - GRANT PRIVILEGE <br >- REVOKE PRIVILEGE                                     | - GRANT PRIVILEGE <br >- REVOKE PRIVILEGE                                 |
| AUDIT      | - CREATE AUDIT <br >- ALTER AUDIT <br >- DROP AUDIT                                 | - CREATE AUDIT <br >- ALTER AUDIT <br >- DROP AUDIT                             |
| QUERY      | - CANCEL QUERY <br >- EXPLAIN QUERY                                           | - CANCEL QUERY <br >- EXPLAIN QUERY                                       |
| JOB        | - CANCEL JOB <br >- PAUSE JOB <br >- RESUME JOB                                     | - CANCEL JOB <br >- PAUSE JOB <br >- RESUME JOB                                  |
| SCHEDULE   | - ALTER SCHEDULE <br >- PAUSE SCHEDULE <br >- RESUME SCHEDULE                       | - ALTER SCHEDULE <br >- PAUSE SCHEDULE <br >- RESUME SCHEDULE                   |
| SESSION    | - SET SESSION <br >- RESET SESSION <br >- CANCEL SESSION                            | - SET SESSION <br >- RESET SESSION <br >- CANCEL SESSION                        |
| STATISTICS | CREATE STATISTICS                                                     | CREATE STATISTICS                                                 |

This table lists all the object-level audit operations supported by KWDB.

| Object | Relational Database                                | Time-series Database                                                                          |
|--------|----------------------------------------------------|-----------------------------------------------------------------------------------------------|
| TABLE  | - INSERT <br >- SELECT <br >- UPDATE <br >- DELETE | - INSERT <br >- SELECT <br >- UPDATE <br >- DELETE <br >Where, the `UPDATE` and `DELETE` statements only support error-reporting audit. |
| VIEW   | SELECT                                             | -                                                                                             |

After database audit is enabled, the system will save the audit results to the audit logs by default. For more information about audit logs, see [Log Management](../db-operation/log-mgmt.md).

## Enable Database Audit

By default, database audit is disabled. To enable it, you can set the `audit.enabled` cluster parameter to `true`.

### Privileges

The user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

### Syntax

```sql
SET CLUSTER SETTING audit.enabled = [true | false];
```

### Parameters

N/A

### Examples

This example enables database audit.

```sql
SET CLUSTER SETTING audit.enabled = true;
```

## Manage Audit Policies

### CREATE AUDIT

The `CREATE AUDIT` statement creates statement-level or object-level audit policies.

#### Privileges

The user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

#### Syntax

```sql
CREATE AUDIT [IF NOT EXISTS] <audit_name>
ON [ALL | <target_type> [<target_name>]]
FOR [ALL | <operations>]
TO [ALL | <operators>]
[WHENEVER [ALL]];
```

#### Parameters

| Parameter | Description |
| --- | --- |
| `IF NOT EXISTS` | Optional. <br>- When the `IF NOT EXISTS` keyword is used, the system creates a new audit policy only if an audit policy of the same name does not already exist. Otherwise, the system fails to create a new audit policy without returning an error. <br>- When the `IF NOT EXISTS` keyword is not used, the system creates a new audit policy only if an audit policy of the same name does not already existed. Otherwise, the system fails to create a new audit policy and returns an error. |
| `audit_name` | The name of the audit policy to create. The audit policy name must be unique. |
| `target_type` | The type of audit objects. Available options are `user`, `role`, `database`, `schema`, `table`, `view`, `index`, `sequence`, `privilege`, `audit`, `range`, `query`, `job`, `schedule`, `session`, `statistics`. If it is set to `ALL`, it means to perform audits on all object types. |
| `target_name` | The name of audit objects in a format of `database_name.target_name`. If the `database_name` is not specified, perform audits on objects in the current database. If the `target_name` is not specified, perform audits on all audit object types in the specified database. <br > **Note** <br >If the audit object type is set to `database`, you cannot specify the `target_name`. |
| `operations` | A comma-separated list of audit operations. If it is set to `ALL`, it means to perform audits on all operations. The supported audit operations depends on the audit object. |
| `operators` | A comma-separated list of roles or users to perform audits on. If it is set to `ALL`, it means to perform audits on all roles or users. |
| `WHENEVER` | Optional. Specify the conditions to perform audits on. By default, it is set to `ALL` and only supports to be set to `ALL`, which means to always record audits. |

#### Examples

- Create a statement-level audit policy.

    This example creates a statement-level audit policy to perform audits on the `root` user when the user creates a database.

    ```sql
    CREATE AUDIT atest ON DATABASE FOR create TO root;
    ```

- Create an object-level audit policy.

    This example creates an object-level audit policy to perform audits on the `root` user when the user queries a table.

    ```sql
    CREATE AUDIT atest ON TABLE t1 FOR SELECT TO root;
    ```

### ALTER AUDIT

The `ALTER AUDIT` statement enables, disables, or renames audit policies.

#### Privileges

The user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

#### Syntax

```sql
ALTER AUDIT [IF EXISTS] <audit_name> [ENABLE | DISABLE | RENAME TO <new_name>];
```

#### Parameters

| Parameter | Description |
| --- | --- |
| `IF EXISTS` | Optional. <br>- When the `IF EXISTS` keyword is used, the system changes an audit policy only if the target audit policy has already existed. Otherwise, the system fails to change the audit policy without returning an error. <br>- When the `IF EXISTS` keyword is not used, the system changes an audit policy only if the target audit policy has already existed. Otherwise, the system fails to change the audit policy and returns an error. |
| `audit_name` | The current name of the audit policy.|
| `ENABLE` | Enable an audit policy. By default, the system disables audit policies. |
| `DISABLE` | Disable an audit policy. |
| `new_name` | The new name of the audit policy. The audit policy name must be unique. |

#### Examples

These examples assume that you have created an audit policy named `atest`.

- Enable an audit policy.

    ```sql
    ALTER AUDIT atest ENABLE;
    ```

- Rename an audit policy.

    ```sql
    ALTER AUDIT atest RENAME TO btest;
    ```

### SHOW AUDITS

The `SHOW AUDITS` statement lists all audit policies.

#### Privileges

N/A

#### Syntax

```sql
SHOW AUDITS [ON <target_type> [<target_name>] [FOR <operations>] [TO <operators>]];
```

#### Parameters

| Parameter | Description |
| --- | --- |
| `target_type` | Optional. The type of audit objects. Available options are `user`, `role`, `database`, `schema`, `table`, `view`, `index`, `sequence`, `privilege`, `audit`, `range`, `query`, `job`, `schedule`, `session`, `statistics`. If it is set to `ALL`, it means to list audit policies on all object types. |
| `target_name` | Optional. The name of audit objects in a format of `database_name.target_name`. If the `database_name` is not specified, list audit policies on objects in the current database. If the `target_name` is not specified, list audit policies on all audit object types in the specified database. <br > **Note** <br >If the audit object type is set to `database`, you cannot specify the `target_name`. |
| `operations` | A comma-separated list of audit operations. |
| `operators` | A comma-separated list of roles or users whose audit policies to show. |

#### Examples

- Show all audit policies.

    ```sql
    SHOW AUDITS;
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
      audit_name | target_type | target_name | target_id | operations | operators | condition | whenever | action | level | enable
    -------------+-------------+-------------+-----------+------------+-----------+-----------+----------+--------+-------+---------
      b          | ALL         |             |         0 | ALL        | rest_user |         0 | ALL      |      0 |     0 | false
      c          | DATABASE    |             |         0 | ALL        | rest_user |         0 | ALL      |      0 |     0 | false
      d          | ALL         |             |         0 | ALL        | rest_user |         0 | ALL      |      0 |     0 | false
    (3 rows)
    ```

- Show audit policies on a specified object.

    ```sql
    SHOW AUDITS ON DATABASE;
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
      audit_name | target_type | target_name | target_id | operations | operators | condition | whenever | action | level | enable
    -------------+-------------+-------------+-----------+------------+-----------+-----------+----------+--------+-------+---------
      c          | DATABASE    |             |         0 | ALL        | rest_user |         0 | ALL      |      0 |     0 | false
    (1 row)
    ```

### DROP AUDIT

The `DROP AUDIT` statement removes one or more audit policies.

#### Privileges

The user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

#### Syntax

```sql
DROP AUDIT [IF EXISTS] <audit_name>;
```

#### Parameters

| Parameter | Description |
| --- | --- |
| `IF EXISTS` | Optional. <br>- When the `IF EXISTS` keyword is used, the system removes an audit policy only if the target audit policy has already existed. Otherwise, the system fails to remove the audit policy without returning an error. <br>- When the `IF EXISTS` keyword is not used, the system removes an audit policy only if the target audit policy has already existed. Otherwise, the system fails to remove the audit policy and returns an error. |
| `audit_name` | A comma-separated list of audit policy names.|

#### Examples

This example removes an audit policy named `btest`.

```sql
DROP AUDIT btest;
```

## Audit Logs

By default, when database audit is enabled, the system will store audit results to audit logs. To disable audit logs, set the `audit.log.enabled` cluster parameter to `false`.

```sql
SET CLUSTER SETTING audit.log.enabled=false;
```

This table lists fields in an audit log.

| Field | <div style="width:330px">Description</div> | Example |
| --- | --- | ---|
| Log level and log date | The level and recording date of the audit log, where `I` refers to the log level. | `I240415` |
| Time | The UTC-format timestamp of the audit log. | `06:49:34.207014` |
| Goroutine ID | The Goroutine ID used to record the audit log. | `538` |
| Path to the audit source file | The source file and line number of codes of the printed audit log.| `security/audit/actions/record_to_log.go:45` |
| Node ID | The ID of the node that records the audit log. | `[n1]` |
| Log count | The number of historical audit logs. | `3` |
| `EventTime` | The time when an audit event happens. | `"EventTime":"2024-04-15T06:49:34.206948441Z"` |
| `Elapsed` | The interval to perform audit events. | `"Elapsed":2242701` |
| `User` | The information about users and roles. Available options are: <br >- `UserID`: Reserved field. The ID of the user who performs the event. By default, it is set to `0`. <br >- `Username`: The name of the user who performs the event. <br >- `Roles`: The information about roles. In which, `ID` is a reserved field indicating the ID of the role who performs the event. By default, it is set to `0`. `Name` refers to the name of the role who performs the event. | `"User":{"UserID":0,"Username":"root","Roles":[{"ID":0,"Name":"admin"}]}` |
| `Event` | The type of operations performed on the specific object(s), such as `CREATE`, `DROP`. | `"Event":"CREATE"`  |
| `Target` | The information about the object. Available options are: <br >- `Typ`: The type of the object. <br >- `Targets`: The detailed information about one or more objects. <br >- `ID`: The ID of the specific object(s). <br >- `Name`: The name of the specific object(s). <br >- `Cascades`: Whether to remove dependent objects. | `"Target":{"Typ":"DATABASE","Targets":{"78":{"ID":78,"Name":"db1","Cascades":null}}}` |
| `Level` | The audit level. Available options are: <br>- `0`: System-level <br >- `1`: Statement-level <br >- `2`: Object-level | `"Level":1` |
| `Client` | The information about the client. Available options are: <br >- `AppName`: The name of the client. <br >- `Address`: The address of the client, in a format of `<ip_address>:<port_id>`. | `Client":{"AppName":"$ kwbase sql","Address":"127.0.0.1:55564"}` |
| `Result` | The result of the event to perform. Available options are:<br >- `Status`: The status of the event to perform. `OK` means that the event is performed successfully while `FAIL` means that the event is failed to be performed. <br >- `ErrMsg`: The error message of the event. <br >- `RowsAffected`: The number of affected rows. | `"Result":{"Status":"OK","ErrMsg":"","RowsAffected":0}` |
| `Command` | The information about the SQL statements to perform. Available options are: <br >- `Cmd`: The SQL statement to perform. <br >- `Params`: The parameters of the SQL statement. | `"Command":{"Cmd":"CREATE DATABASE db1","Params":"{}"}` |
| `Reporter` | The information about the node that records the audit events. Available options are: <br >- `ClusterID`: The cluster ID. <br >- `NodeID`: The node ID. <br >- `HostIP`: The IP address of the node. <br >- `HostPort`: The port ID of the node. <br >- `HostMac`: The MAC address of the node. <br >- `LastUp`: Reserved field. The time when the node was started last time. By default, it is set to `0`. | `"Reporter":{"ClusterID":"ae93118d-28bc-492f-bd4f-852cafab0ad9","NodeID":1,"HostIP":"localhost","HostPort":"26257","HostMac":"","LastUp":0}}` |

Here is an example of an audit log for creating a database:

```xml
I240415 06:49:34.207014 538 security/audit/actions/record_to_log.go:45  [n1] 3 {"EventTime":"2024-04-15T06:49:34.206948441Z","Elapsed":2242701,"User":{"UserID":0,"Username":"root","Roles":[{"ID":0,"Name":"admin"}]},"Event":"CREATE","Target":{"Typ":"DATABASE","Targets":{"78":{"ID":78,"Name":"db1","Cascades":null}}},"Level":1,"Client":{"AppName":"$ kwbase sql","Address":"127.0.0.1:55564"},"Result":{"Status":"OK","ErrMsg":"","RowsAffected":0},"Command":{"Cmd":"CREATE DATABASE db1","Params":"{}"},"Reporter":{"ClusterID":"ae93118d-28bc-492f-bd4f-852cafab0ad9","NodeID":1,"HostIP":"localhost","HostPort":"26257","HostMac":"","LastUp":0}}
```
