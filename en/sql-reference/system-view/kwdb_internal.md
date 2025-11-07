# kwdb_internal

The `kwdb_internal` schema contains system views that describe the database's internal objects, processes, and metrics.

To list all system views in the `kwdb_internal` schema, use the SQL statement `SHOW TABLES FROM [<database_name>.]kwdb_internal;`. If no database is specified, the current database is used by default. To view data from specific system views, use standard `SELECT` statements.

This section lists commonly used system views in the `kwdb_internal` schema.

## Privileges

The user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

## kwdb_internal.audit_policies

The `kwdb_internal.audit_policies` system view describes audit policies.

| Column Name   | Data Type       | Description                                                                                                                                                                                                 |
|---------------|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `audit_name`  | STRING | The name of the audit policy.                                                                                                                                                                               |
| `target_type` | STRING | The type of audit target (e.g., users, roles, databases, tables, views, indexes, constraints, sequences, privileges, ranges, queries, jobs, sessions, statistics, audits, properties).                      |
| `target_name` | STRING          | The name of the audit target.                                                                                                                                                                               |
| `target_id`   | INT             | The ID of the audit target.                                                                                                                                                                                 |
| `operations`  | STRING | The audited operation(s).                                                                                                                                                                                   |
| `operators`   | STRING | The user(s) performing the audited operation.                                                                                                                                                               |
| `condition`   | INT             | Reserved field. The audit condition.                                                                                                                                                                        |
| `whenever`    | STRING | The audit trigger condition (when the audit is recorded).                                                                                                                                                   |
| `action`      | INT             | Reserved field. The post-audit operations.                                                                                                                                                                  |
| `level`       | INT             | Reserved field. The audit level.                                                                                                                                                                            |
| `enable`      | BOOL   | Whether the audit policy is enabled.                                                                                                                                                                        |

## kwdb_internal.audit_trail

The `kwdb_internal.audit_trail` system view describes audit log information.

| Column Name   | Data Type | Description                                                              |
|---------------|-----------|--------------------------------------------------------------------------|
| `event_time`  | TIMESTAMP | The time when the audit event occurred.                                  |
| `username`    | STRING    | The user name.                                                           |
| `operation`   | STRING    | The type of operation performed on the audit target.                     |
| `target_type` | STRING    | The type of audit target.                                                |
| `result`      | STRING    | The execution result of the audit event. `OK` indicates success; `FAIL` indicates failure. |
| `detail`      | STRING    | Additional audit information.                                            |

## kwdb_internal.cluster_sessions

The `kwdb_internal.cluster_sessions` system view describes cluster session information.

| Column Name          | Data Type | Description                                           |
|----------------------|-----------|-------------------------------------------------------|
| `node_id`            | INT8      | The ID of the node to which the session is connected. |
| `session_id`         | STRING    | The session ID.                                       |
| `user_name`          | STRING    | The name of the user who initiated the session.       |
| `client_address`     | STRING    | The client address that initiated the session.        |
| `application_name`   | STRING    | The name of the application that initiated the session. |
| `active_queries`     | STRING    | Active SQL queries in the session.                    |
| `last_active_query`  | STRING    | The most recently completed SQL query in the session. |
| `session_start`      | TIMESTAMP | The timestamp when the session started.               |
| `oldest_query_start` | TIMESTAMP | The timestamp when the earliest active SQL query in the session started. |
| `kv_txn`             | STRING    | The ID of the current key-value transaction in the session. |
| `alloc_bytes`        | INT8      | The number of bytes allocated by the session.         |
| `max_alloc_bytes`    | INT8      | The maximum number of bytes allocated by the session. |
| `connection_id`      | STRING    | The session connection ID.                            |
| `schema`             | STRING    | The default schema.                                   |
| `status`             | STRING    | The session status.                                   |

## kwdb_internal.gossip_nodes

The `kwdb_internal.gossip_nodes` system view describes information about nodes in the cluster gossip network.

| Column Name             | Data Type | Description                          |
|-------------------------|-----------|--------------------------------------|
| `node_id`               | INT8      | The node ID.                         |
| `network`               | STRING    | The network protocol type.           |
| `address`               | STRING    | The node address.                    |
| `advertise_address`     | STRING    | The advertised address.              |
| `sql_network`           | STRING    | The SQL network protocol type.       |
| `sql_address`           | STRING    | The SQL service address.             |
| `advertise_sql_address` | STRING    | The advertised SQL address.          |
| `attrs`                 | JSONB     | The node attributes.                 |
| `locality`              | STRING    | The node ID.                   |
| `start_mode`            | STRING    | The startup mode.                    |
| `cluster_name`          | STRING    | The cluster name.                    |
| `server_version`        | STRING    | The server version.                  |
| `build_tag`             | STRING    | The build tag.                       |
| `started_at`            | TIMESTAMP | The startup time.                    |
| `is_live`               | BOOL      | Whether the node is alive.           |
| `ranges`                | INT8      | The number of data ranges.           |
| `leases`                | INT8      | The number of leases.                |

## kwdb_internal.metrics_metadata

The `kwdb_internal.metrics_metadata` system view describes metadata of monitoring metrics.

| Column Name   | Data Type       | Description                                 |
|---------------|-----------------|---------------------------------------------|
| `name`        | STRING | The name of the metric.          |
| `help`        | STRING          | The description of the metric.   |
| `measurement` | STRING          | The measurement type of metric.  |
| `unit`        | STRING          | The unit of measurement for metric.        |

## kwdb_internal.node_metrics

The `kwdb_internal.node_metrics` system view describes metrics data for nodes in the cluster.

| Column Name | Data Type       | Description           |
|-------------|-----------------|-----------------------|
| `store_id`  | INT8            | The storage ID.       |
| `name`      | STRING | The metric name.      |
| `value`     | FLOAT8 | The metric value.     |

## kwdb_internal.node_statement_statistics

The `kwdb_internal.node_statement_statistics` system view describes statistics related to statement execution on nodes.

| Column Name           | Data Type | Description                                 |
|-----------------------|-----------|---------------------------------------------|
| `node_id`             | INT8      | The node ID.                                |
| `application_name`    | STRING    | The application name.                       |
| `flags`               | STRING    | The flags.                                  |
| `key`                 | STRING    | The key of the SQL statement.               |
| `anonymized`          | STRING    | The anonymized SQL statement.               |
| `count`               | INT8      | The number of executions.                   |
| `first_attempt_count` | INT8      | The number of first-attempt executions.     |
| `max_retries`         | INT8      | The maximum number of retries.              |
| `last_error`          | STRING    | The last error message.                     |
| `rows_avg`            | FLOAT8    | The average number of rows returned.        |
| `rows_var`            | FLOAT8    | The variance of rows returned.              |
| `parse_lat_avg`       | FLOAT8    | The average parse latency.                  |
| `parse_lat_var`       | FLOAT8    | The variance of parse latency.              |
| `plan_lat_avg`        | FLOAT8    | The average plan latency.                   |
| `plan_lat_var`        | FLOAT8    | The variance of plan latency.               |
| `run_lat_avg`         | FLOAT8    | The average run latency.                    |
| `run_lat_var`         | FLOAT8    | The variance of run latency.                |
| `service_lat_avg`     | FLOAT8    | The average service latency.                |
| `service_lat_var`     | FLOAT8    | The variance of service latency.            |
| `overhead_lat_avg`    | FLOAT8    | The average overhead latency.               |
| `overhead_lat_var`    | FLOAT8    | The variance of overhead latency.           |
| `bytes_read`          | INT8      | The number of bytes read.                   |
| `rows_read`           | INT8      | The number of rows read.                    |
| `implicit_txn`        | BOOL      | Whether it is an implicit transaction.      |
| `failed_count`        | INT8      | The number of failures.                     |
| `user_name`           | STRING    | The user name.                              |
| `database`            | STRING    | The database name.                          |

## kwdb_internal.processes

The `kwdb_internal.processes` system view describes database process information.

| Column Name    | Data Type | Description                          |
|----------------|-----------|--------------------------------------|
| `process_id`   | INT8      | The process ID.                      |
| `node_id`      | INT8      | The ID of the node to which the process belongs. |
| `process_name` | STRING    | The process name.                    |
| `process_type` | STRING    | The process type.                    |
| `os_user`      | STRING    | The OS user who started the process. |
| `memory`       | INT8      | The memory cache size.               |
| `created`      | INT8      | The process startup time.            |

## kwdb_internal.role_options

The `kwdb_internal.role_options` system view describes user options.

| Column Name | Data Type       | Description                |
|-------------|-----------------|----------------------------|
| `username`  | STRING | The user name.             |
| `option`    | STRING | The user option.      |
| `value`     | STRING          | The value of the user option. |

## kwdb_internal.table_columns

The `kwdb_internal.table_columns` system view describes column information for all tables in the database.

| Column Name       | Data Type | Description                         |
|-------------------|-----------|-------------------------------------|
| `descriptor_id`   | INT8      | The table descriptor ID.            |
| `descriptor_name` | STRING    | The table name.                     |
| `column_id`       | INT8      | The column ID.                      |
| `column_name`     | STRING    | The column name.                    |
| `column_type`     | STRING    | The column type.           |
| `nullable`        | BOOL      | Whether the column allows NULL values.     |
| `default_expr`    | STRING    | The default value expression.       |
| `hidden`          | BOOL      | Whether the column is hidden.       |

## kwdb_internal.table_indexes

The `kwdb_internal.table_indexes` system view describes index information for all tables in the database.

| Column Name       | Data Type | Description                     |
|-------------------|-----------|---------------------------------|
| `descriptor_id`   | INT8      | The table descriptor ID.        |
| `descriptor_name` | STRING    | The table name.                 |
| `index_id`        | INT8      | The index ID.                   |
| `index_name`      | STRING    | The index name.                 |
| `index_type`      | STRING    | The index type.                 |
| `is_unique`       | BOOL      | Whether the index is unique.    |
| `is_inverted`     | BOOL      | Whether the index is inverted.  |

## kwdb_internal.tables

The `kwdb_internal.tables` system view describes metadata information for all tables in the database.

| Column Name                | Data Type | Description                                  |
|----------------------------|-----------|----------------------------------------------|
| `table_id`                 | INT8      | The unique identifier of the table.          |
| `parent_id`                | INT8      | The identifier of the parent object.         |
| `name`                     | STRING    | The table name.                              |
| `database_name`            | STRING    | The database name.                           |
| `version`                  | INT8      | The version number of the table.             |
| `mod_time`                 | TIMESTAMP | The last modification time.                  |
| `mod_time_logical`         | DECIMAL   | The logical modification timestamp.          |
| `format_version`           | STRING    | The table format version.                    |
| `state`                    | STRING    | The table state (e.g., PUBLIC, DROP).        |
| `sc_lease_node_id`         | INT8      | The ID of the node holding the schema change lease.             |
| `sc_lease_expiration_time` | TIMESTAMP | The expiration time of the schema change lease.     |
| `drop_time`                | TIMESTAMP | The table drop time.                         |
| `audit_mode`               | STRING    | The audit mode.                              |
| `schema_name`              | STRING    | The schema name.                             |

## kwdb_internal.user_login_status

The `kwdb_internal.user_login_status` system view describes users' current login information, historical login records, failed login statistics, and account status.

| Column Name              | Data Type | Description                                         |
|--------------------------|-----------|-----------------------------------------------------|
| `username`               | STRING    | The user login name.                                |
| `login_time`             | TIMESTAMP | The current login time.                             |
| `login_application`      | STRING    | The application system of the current login.        |
| `login_host`             | STRING    | The IP address of the current login.                |
| `login_method`           | STRING    | The login method used for the current login.        |
| `login_node_id`          | INT8      | The node ID of the current login.                   |
| `last_login_time`        | TIMESTAMP | The time of the last successful login.              |
| `last_login_application` | STRING    | The application system of the last successful login.           |
| `last_login_host`        | STRING    | The IP address of the last successful login.                   |
| `last_login_method`      | STRING    | The login method used for the last successful login.           |
| `last_login_node_id`     | INT8      | The node ID of the last successful login.                      |
| `failed_login_time`      | TIMESTAMP | The time of the most recent failed login attempt.           |
| `failed_login_application` | STRING  | The application system of the most recent failed login attempt. |
| `failed_login_host`      | STRING    | The IP address of the most recent failed login attempt.     |
| `failed_login_method`    | STRING    | The login method used for the most recent failed login attempt. |
| `failed_login_node_id`   | INT8      | The node ID of the most recent failed login attempt.        |
| `failed_attempts`        | INT8      | The cumulative number of failed login attempts.     |
| `first_login`            | BOOL      | Whether this is the user's first login.             |
| `latest_status`          | STRING    | The current login status of the user.               |