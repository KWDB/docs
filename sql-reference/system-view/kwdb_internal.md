---
title: kwdb_internal
id: kwdb_internal
---

# kwdb_internal

`kwdb_internal` 模式包含数据库的系统视图，描述数据库的内部对象、进程和指标信息。

用户可通过 `SHOW TABLES FROM [<database_name>.]kwdb_internal;` SQL 语句列出指定数据库 `kwdb_internal` 模式下的所有系统视图。未指定数据库时，默认使用当前数据库进行查询；也可以使用 `SELECT` 语句查看 `kwdb_internal` 模式下的指定系统视图信息。

本节列出了 `kwdb_internal` 模式中常用的系统视图。

## 所需权限

用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。

## kwdb_internal.audit_policies

`kwdb_internal.audit_policies` 系统视图描述审计策略。

| 列名        | 数据类型        | 描述                                                                                                                    |
| ----------- | --------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `audit_name`  | STRING  | 审计策略名称                                                                                                            |
| `target_type` | STRING  | 审计目标类型，例如用户、角色、数据库、表、视图、索引、约束、序列、权限、Range、查询、任务、会话、统计信息、审计、属性等 |
| `target_name` | STRING          | 审计目标名称                                                                                                            |
| `target_id`   | INT             | 审计目标对象 ID                                                                                                         |
| `operations`  | STRING  | 审计操作                                                                                                                |
| `operators`   | STRING  | 审计的用户                                                                                                              |
| `condition`   | INT             | 审计条件，预留字段                                                                                                      |
| `whenever`    | STRING  | 执行审计的条件                                                                                                                |
| `action`      | INT             | 审计后操作，预留字段                                                                                                    |
| `level`       | INT             | 审计等级，预留字段                                                                                                      |
| `enable`      | bool    | 审计策略开关                                                                                                            |

## kwdb_internal.audit_trail

`kwdb_internal.audit_trail` 系统视图描述审计日志的相关信息。

| 列名          | 数据类型  | 描述                                            |
|---------------|-----------|-----------------------------------------------|
| `event_time`  | TIMESTAMP | 审计事件发生的时间                              |
| `username`    | STRING    | 用户名                                          |
| `operation`   | STRING    | 在审计对象上的操作类型                          |
| `target_type` | STRING    | 审计对象类型                                    |
| `result`      | STRING    | 审计事件执行结果。`OK` 表示成功，`FAIL` 表示失败。 |
| `detail`      | STRING    | 其他审计信息                                    |

## kwdb_internal.cluster_sessions

`kwdb_internal.cluster_sessions` 系统视图描述集群的会话信息。

| **列名**             | **类型**  | **描述**                          |
| -------------------- | --------- | --------------------------------- |
| `node_id`            | INT8      | 会话连接到的节点 ID                |
| `session_id`         | STRING    | 会话的 ID                          |
| `user_name`          | STRING    | 发起会话的用户名称                |
| `client_address`     | STRING    | 发起会话的客户端地址              |
| `application_name`   | STRING    | 发起会话的应用程序名称            |
| `active_queries`     | STRING    | 会话中活跃的 SQL 查询               |
| `last_active_query`  | STRING    | 会话中最近完成的 SQL 查询           |
| `session_start`      | TIMESTAMP | 会话开始的时间戳                  |
| `oldest_query_start` | TIMESTAMP | 会话中最早 SQL 查询开始的时间戳 |
| `kv_txn`             | STRING    | 会话当前键值事务的 ID              |
| `alloc_bytes`        | INT8      | 会话分配的字节数                  |
| `max_alloc_bytes`    | INT8      | 会话分配的最大字节数              |
| `connection_id`    | STRING      | 会话连接的 ID              |
| `schema`    | STRING      | 缺省模式              |
| `status`    | STRING      | 会话状态              |

## kwdb_internal.gossip_nodes

`kwdb_internal.gossip_nodes` 系统视图描述集群 gossip 网络中节点的信息。

| 列名                    | 数据类型  | 描述              |
| ----------------------- | --------- | ----------------- |
| `node_id`               | INT8      | 节点 ID            |
| `network`               | STRING    | 网络协议类型      |
| `address`               | STRING    | 节点地址          |
| `advertise_address`     | STRING    | 对外广播的地址    |
| `sql_network`           | STRING    | SQL 网络协议类型   |
| `sql_address`           | STRING    | SQL 服务地址       |
| `advertise_sql_address` | STRING    | 对外广播的 SQL 地址 |
| `attrs`                 | JSONB     | 节点属性          |
| `locality`              | STRING    | 节点 ID      |
| `start_mode`            | STRING    | 启动模式          |
| `cluster_name`          | STRING    | 集群名称          |
| `server_version`        | STRING    | 服务器版本        |
| `build_tag`             | STRING    | 版本标签          |
| `started_at`            | TIMESTAMP | 启动时间          |
| `is_live`               | BOOL      | 节点是否存活      |
| `ranges`                | INT8      | 数据分片数量      |
| `leases`                | INT8      | 租约数量          |

## kwdb_internal.metrics_metadata

`kwdb_internal.metrics_metadata` 系统视图描述监控指标的元数据。

| 列名          | 数据类型        | 描述               |
|---------------|-----------------|------------------|
| `name`        | STRING  | 监控指标的名称     |
| `help`        | STRING          | 监控指标的描述信息 |
| `measurement` | STRING          | 监控指标的测量方式 |
| `unit`        | STRING          | 监控指标的单位     |

## kwdb_internal.node_metrics

`kwdb_internal.node_metrics` 系统视图描述集群中节点的指标数据。

| 列名          | 数据类型        | 描述               |
|---------------|-----------------|------------------|
| `store_id`    | INT8            | 存储位置 ID      |
| `name`        | STRING  | 指标名称     |
| `value`       | FLOAT8  | 指标值     |

## kwdb_internal.node_statement_statistics

`kwdb_internal.node_statement_statistics` 系统视图描述节点执行语句相关统计信息。

| 列名                  | 数据类型 | 描述             |
| --------------------- | -------- | ---------------- |
| `node_id`             | INT8     | 节点 ID           |
| `application_name`    | STRING   | 应用程序名称     |
| `flags`               | STRING   | 标志位           |
| `key`                 | STRING   | SQL 语句的键值    |
| `anonymized`          | STRING   | 匿名化的 SQL 语句  |
| `count`               | INT8     | 执行次数         |
| `first_attempt_count` | INT8     | 首次尝试执行次数 |
| `max_retries`         | INT8     | 最大重试次数     |
| `last_error`          | STRING   | 最后一次错误信息 |
| `rows_avg`            | FLOAT8   | 平均返回行数     |
| `rows_var`            | FLOAT8   | 返回行数的方差   |
| `parse_lat_avg`       | FLOAT8   | 平均解析延迟     |
| `parse_lat_var`       | FLOAT8   | 解析延迟的方差   |
| `plan_lat_avg`        | FLOAT8   | 平均计划延迟     |
| `plan_lat_var`        | FLOAT8   | 计划延迟的方差   |
| `run_lat_avg`         | FLOAT8   | 平均运行延迟     |
| `run_lat_var`         | FLOAT8   | 运行延迟的方差   |
| `service_lat_avg`     | FLOAT8   | 平均服务延迟     |
| `service_lat_var`     | FLOAT8   | 服务延迟的方差   |
| `overhead_lat_avg`    | FLOAT8   | 平均开销延迟     |
| `overhead_lat_var`    | FLOAT8   | 开销延迟的方差   |
| `bytes_read`          | INT8     | 读取字节数       |
| `rows_read`           | INT8     | 读取行数         |
| `implicit_txn`        | BOOL     | 是否为隐式事务   |
| `failed_count`        | INT8     | 失败次数         |
| `user_name`           | STRING   | 用户名           |
| `database`            | STRING   | 数据库名         |

## kwdb_internal.processes

`kkwdb_internal.processes` 系统视图描述数据库进程相关信息。

| 列名              | 数据类型   | 描述                     |
|------------------ |-----------|-------------------------|
| `process_id`      | INT8     | 进程 ID                 |
| `node_id`         | INT8     | 进程所属节点 ID               |
| `process_name`         | STRING    | 进程名称                 |
| `process_type`        | STRING    | 进程类型                 |
| `os_user` | STRING    | 进程启动用户           |
| `memory`  | INT8      | 缓存大小     |
| `created`   | INT8      | 进程启动时间       |

## kwdb_internal.role_options

`kwdb_internal.role_options` 系统视图描述用户的选项。

| 列名     | 数据类型        | 描述         |
| -------- | --------------- | ------------ |
| `username` | STRING  | 用户名       |
| `option`   | STRING  | 用户的选项   |
| `value`    | STRING          | 用户选项的值 |


## kwdb_internal.table_columns

`kwdb_internal.table_columns` 系统视图描述数据库中所有表的列信息。

| 列名              | 数据类型 | 描述           |
| ----------------- | -------- | -------------- |
| `descriptor_id`   | INT8     | 表描述符 ID     |
| `descriptor_name` | STRING   | 表名称         |
| `column_id`       | INT8     | 列 ID           |
| `column_name`     | STRING   | 列名称         |
| `column_type`     | STRING   | 列类型详细信息 |
| `nullable`        | BOOL     | 是否允许为空   |
| `default_expr`    | STRING   | 默认值表达式   |
| `hidden`          | BOOL     | 是否为隐藏列   |

## kwdb_internal.table_indexes

`kwdb_internal.table_indexes` 系统视图描述数据库中所有表的索引信息。

| 列名              | 数据类型 | 描述                  |
| ----------------- | -------- | --------------------- |
| `descriptor_id`   | INT8     | 表描述符 ID            |
| `descriptor_name` | STRING   | 表名称                |
| `index_id`        | INT8     | 索引 ID                |
| `index_name`      | STRING   | 索引名称              |
| `index_type`      | STRING   | 索引类型              |
| `is_unique`       | BOOL     | 是否为唯一索引        |
| `is_inverted`     | BOOL     | 是否为倒排索引        |

## kwdb_internal.tables

`kwdb_internal.tables` 系统视图描述数据库中所有表的元数据信息。

| 列名                       | 数据类型  | 描述                    |
| -------------------------- | --------- | ----------------------- |
| `table_id`                 | INT8      | 表的唯一标识符          |
| `parent_id`                | INT8      | 父对象的标识符          |
| `name`                     | STRING    | 表名                    |
| `database_name`            | STRING    | 数据库名称              |
| `version`                  | INT8      | 表的版本号              |
| `mod_time`                 | TIMESTAMP | 最后修改时间            |
| `mod_time_logical`         | DECIMAL   | 逻辑修改时间戳          |
| `format_version`           | STRING    | 表格式版本              |
| `state`                    | STRING    | 表状态（PUBLIC/DROP 等） |
| `sc_lease_node_id`         | INT8      | 模式变更租约节点 ID      |
| `sc_lease_expiration_time` | TIMESTAMP | 模式变更租约过期时间    |
| `drop_time`                | TIMESTAMP | 表删除时间              |
| `audit_mode`               | STRING    | 审计模式                |
| `schema_name`              | STRING    | 模式名称                |

## kwdb_internal.user_login_status

`kwdb_internal.user_login_status` 系统视图描述了用户的当前登录信息、历史登录记录、失败登录统计和账户状态。

| 列名 | 数据类型 | 描述 |
|----------|----------|----------|
| username | STRING | 用户登录名 |
| login_time | TIMESTAMP | 本次登录时间 |
| login_application | STRING | 本次登录的应用系统 |
| login_host | STRING | 本次登录的 IP 地址 |
| login_method | STRING | 本次登录使用的登录方式 |
| login_node_id | INT8 | 本次登录的节点 ID |
| last_login_time | TIMESTAMP | 上一次成功登录的时间 |
| last_login_application | STRING | 上一次登录的应用系统 |
| last_login_host | STRING | 上一次登录的 IP 地址 |
| last_login_method | STRING | 上一次使用的登录方式 |
| last_login_node_id | INT8 | 上一次登录的节点 ID |
| failed_login_time | TIMESTAMP | 最近一次登录失败的时间 |
| failed_login_application | STRING | 最近一次登录失败的应用系统 |
| failed_login_host | STRING | 最近一次登录失败的 IP 地址 |
| failed_login_method | STRING | 最近一次登录失败时使用的方式 |
| failed_login_node_id | INT8 | 最近一次登录失败的节点 ID |
| failed_attempts | INT8 | 累计登录失败次数 |
| first_login | BOOL | 是否为首次登录 |
| latest_status | STRING | 用户当前登录状态 |