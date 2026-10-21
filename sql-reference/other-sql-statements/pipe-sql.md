---
title: 数据推送管道
id: pipe-sql
---

# 数据推送管道

## 创建数据推送管道

`CREATE PIPE` 语句用于创建数据推送管道。

### 所需权限

- 用户是 `admin` 角色的成员或者拥有目标表的 SELECT 权限。默认情况下，`root` 用户属于 `admin` 角色。

### 语法格式

- 单库推送

    ![](../../static/sql-reference/createpipe_database.png)

- 单表推送

    ![](../../static/sql-reference/createpipe.png)

- 多表推送

    ![](../../static/sql-reference/createpipe_multiple_tables.png)

### 参数说明

::: warning 说明

- `database_name` 参数只适用于单库推送。
- `ts_table_list` 参数只适用于多表推送。
- `ts_table_name`、`ts_column` 和 `ts_column_condition` 参数只适用于单表推送。
:::

| 参数 | 说明 |
| --- | --- |
| `name` | KWDB 数据推送管道的名称。该名称系统内必须唯一。 |
| `database_name` | 待推送数据库的名称。|
| `ts_table_name` | 时序表名称。用户可以使用 `ALTER PIPE <name> SET TABLE` 语句修改待监听的时序表。|
| `ts_table_list` | 待推送的时序表列表。支持指定多个时序表，各表名之间使用逗号（`,`）隔开。|
| `ts_column` | 待监听的时序表列。支持监听目标时序表的全部列或部分列。<br >- *：按照目标时序表结构监听全部列。<br >- 当待监听列被删除或重命名后，系统不再监听和推送该列数据。<br >- 用户可以添加新列，但新列不会出现在推送数据的列表中。 |
| `ts_column_condition` | 可选参数，时序数据过滤条件。用户可以使用 `ALTER PIPE <name> SET TABLE` 语句修改时序数据的过滤条件。<br >- 支持数据列、Primary Tag 列和普通 Tag 列的过滤运算。<br >- 支持基于时序表时间戳列的条件过滤。<br >- 不支持聚合函数、类型转换、排序规则、系统列引用或非不可变内置函数。 |
| `push_parameter` | 数据推送参数。用户可以使用 `ALTER PIPE <name> SET OPTIONS` 语句修改数据推送管道的推送参数。支持以下参数：<br >- `enable`：是否启用实时数据推送服务。支持 `on` 和 `off` 两个取值。`on` 表示启用实时数据推送服务。`off` 表示停止实时数据推送。默认情况下，启用实时数据推送服务。<br >- `sink`：数据推送的目标。目前，KWDB 仅支持推送数据到 Kafka 主题。如果用户未指定合法的推送目标，系统报错。<br >- `message_format`：数据推送的数据格式。目前，KWDB 只支持推送 JSON 格式的数据。KWDB 支持推送一条或多条记录，其中正常数据推送的消息类型为 `insert`，重启补发数据推送的消息类型为 `snapshot`，删除操作的消息类型为 `delete`，更新操作的消息类型为 `update`。<br >- `ignore_history`：是否忽略历史数据。支持 `on` 和 `off` 两个取值。`on` 表示忽略历史数据，即不推送历史数据。`off` 表示推送历史数据。默认情况下，不推送历史数据。<br >- `buffer_size`：缓冲大小，单位 MiB。`0` 表示立即发送。默认情况下，设置为 `1`。<br >- `retrieve_tags`：是否开启补充普通 Tag 功能。当用户未在推送任务输出列或者过滤列中指定普通 Tag 时，无论是否开启补充普通 Tag 功能，系统都不会补充普通 Tag 值。支持 `on` 和 `off` 两个取值。`on` 表示开启补充普通 Tag 功能。当开启补充普通 Tag 功能时，如果用户在推送任务输出列或者过滤列中指定了普通 Tag 但写入数据时未指定普通 Tag 的取值，系统读取已经写入的相同 Primary Tag 数据中的普通 Tag 的值并自动补充到写入的数据中。如果用户写入普通 Tag 的值与首次写入 Primary Tag 中普通 Tag 的取值不匹配，系统读取第一次写入 Primary Tag 中普通 Tag 的取值并更新当前普通 Tag 的取值，然后再进行推送或过滤。`off` 表示不开启补充普通 Tag 功能。当未开启补充普通 Tag 功能时，用户在推送任务输出列或者过滤列中指定了普通 Tag 但写入数据时未指定普通 Tag 的取值，系统按照 NULL 值处理省略的普通 Tag。如果用户写入的 Primary Tag 和普通 Tag 与第一次写入时的取值不匹配，系统会按照当前写入的普通 Tag 值进行推送或过滤。默认情况下，开启补充普通 Tag 功能。<br >- `publish`：数据推送的操作类型，支持 `insert`、`update`、`delete`、`ddl` 和 `all` 操作。默认情况下，设置为 `insert`。 |
| `value` | 数据推送参数的取值。 |

### 语法示例

- 单库推送

    以下示例创建一个名为 `benchmark_pipe` 数据推送管道，将 `benchmark` 数据库中的数据实时推送到 `test_topic` Kafka 主题中并指定发送方式为实时发送。

    ```sql
    CREATE PIPE benchmark_pipe FOR DATABASE benchmark WITH OPTIONS( enable = 'on', sink = 'kafka://localhost:9092?topic_name=test_topic', ignore_history = 'off', buffer_size = '0');
    ```

- 单表推送

    以下示例创建一个名为 `ts_table_a_pipe_a` 数据推送管道，按照指定条件筛选 `ts_table_a` 时序表的数据并将其实时推送到 `test_topic` Kafka 主题中。

    ```sql
    CREATE PIPE ts_table_a_pipe_a FOR TABLE ts_table_a(*) WHERE hostname='www.example1.com' AND max_usage_user > 60 WITH OPTIONS( enable = 'on', sink = 'kafka://localhost:9092?topic_name=test_topic');
    ```

- 多表推送

    以下示例创建一个名为 `benchmark_pipe` 数据推送管道，将 `benchmark` 数据库中 `disk` 和 `memory` 表中的数据实时推送到 `test_topic` Kafka 主题中并指定发送方式为实时发送。

    ```sql
    CREATE PIPE benchmark_pipe FOR TABLE benchmark.disk, benchmark.memory WITH OPTIONS( enable = 'on', sink = 'kafka://localhost:9092?topic_name=test_topic', ignore_history = 'off', buffer_size = '0');
    ```

## 查看数据推送管道

`SHOW PIPES` 或 `SHOW PIPE` 语句用于查看所有或指定数据推送管道的信息，包括数据推送管道名称、目标时序表、创建参数、创建时间、创建者、当前状态、开始时间、结束时间、失败原因等重要信息。

### 所需权限

无

### 语法格式

![](../../static/sql-reference/showpipe.png)

### 参数说明

| 参数   | 说明                        |
|--------|---------------------------|
| `name` | KWDB 数据推送管道的名称。 |

### 返回字段说明

| 字段            | 说明                                        |
|-----------------|-------------------------------------------|
| `name`          | 数据推送管道的名称。该名称系统内必须唯一。    |
| `table_name`    | 数据推送服务的目标时序表的名称。             |
| `column_names`  | 数据推送服务的目标列。                       |
| `filter`        | 数据推送服务的过滤条件。                     |
| `sink`          | 数据推送服务的推送目标。                     |
| `low_watermark` | 数据推送服务的复制标识。                     |
| `status`        | 是否启用实时数据推送服务。                   |
| `create_at`     | 数据推送管道的创建时间。                     |
| `start_time`    | 最后一次开始推送数据的时间。如未开始，则为空。 |
| `create_by`     | 数据推送管道的创建者。                       |
| `end_time`      | 最后一次停止推送数据的时间。默认为空。        |
| `error_message` | 数据推送失败的原因。                         |

### 语法示例

以下示例查看 `ts_table_a_pipe_a` 数据推送管道的详细信息。

```sql
SHOW PIPE ts_table_a_pipe_a;
```

执行成功后，控制台输出以下信息：

```sql
     name    |        table_name        |     column_names     |  filter   |                       sink                        |    low_watermark     | status |            create_at             | create_by |        start_time         | end_time | error_message
-------------+--------------------------+----------------------+-----------+---------------------------------------------------+----------------------+--------+----------------------------------+-----------+---------------------------+----------+----------------
  ts_table_a_pipe_a | test_data_pipe.public.ts_table_a | k_timestamp,id,code1 | code1 = 3 | kafka://localhost:9092?topic_name=test_topic2 | 1717632000000 | Enable | 2025-02-17 01:41:42.135389+00:00 | root      | 2025-02-17 01:41:42+00:00 | NULL     |
(1 row)
```

## 修改数据推送管道

`ALTER PIPE` 语句用于修改数据推送管道，包括 `ALTER PIPE SET TABLE` 和 `ALTER PIPE SET OPTIONS` 两个子命令：

- `ALTER PIPE SET TABLE`：用于修改数据推送管道的目标时序表、输出列、过滤条件。
- `ALTER PIPE SET OPTIONS`：用于修改数据推送管道的推送参数和推送目标，以及开始和停止数据推送服务。

::: warning 说明

- `ALTER PIPE SET TABLE` 和 `ALTER PIPE SET OPTIONS` 子命令需要单独使用。KWDB 不支持同时修改数据推送管道的目标时序表和推送参数。
- 对于单库推送和多表推送，不支持修改时序库或时序表的名称。
:::

### 所需权限

- 用户是 `admin` 角色的成员或者数据推送管道的创建者。默认情况下，`root` 用户属于 `admin` 角色。

::: warning 说明
如果创建数据推送管道的用户被删除后，只有 Admin 用户 或 `sysadmin` 用户可以修改目标数据推送管道。
:::

### 语法格式

- 修改数据推送管道的目标时序表、输出列或时序数据的过滤条件

    ![](../../static/sql-reference/alterpipe_tables.png)

- 修改数据推送管道的推送参数

    ![](../../static/sql-reference/alterpipe_parameters.png)

### 参数说明

::: warning 说明
`ts_table_name`、`ts_column` 和 `ts_column_condition` 参数只适用于单表推送。
:::

| 参数 | 说明 |
| --- | --- |
| `name` | KWDB 数据推送管道的名称。 |
| `ts_table_name` | 时序表名称。 |
| `ts_column` | 待监听的时序表列。支持监听目标时序表的全部列或部分列。<br >- *：按照目标时序表结构监听全部列。<br >- 当待监听列被删除或重命名后，系统不再监听和推送该列数据。<br >- 用户可以添加新列，但新列不会出现在推送数据的列表中。 |
| `ts_column_condition` | 可选参数，时序数据过滤条件。<br >- 支持数据列、Primary Tag 列和普通 Tag 列的过滤运算。<br >- 支持基于时序表时间戳列的条件过滤。<br >- 不支持聚合函数、类型转换、排序规则、系统列引用或非不可变内置函数。 |
| `push_parameter` | 数据推送参数。支持以下参数：<br >- `enable`：是否启用实时数据推送服务。支持 `on` 和 `off` 两个取值。`on` 表示启用实时数据推送服务。`off` 表示停止实时数据推送。默认情况下，启用实时数据推送服务。<br >- `sink`：数据推送的目标。目前，KWDB 仅支持推送数据到 Kafka 主题。如果用户未指定合法的推送目标，系统报错。<br >- `message_format`：数据推送的数据格式。目前，KWDB 只支持推送 JSON 格式的数据。KWDB 支持推送一条或多条记录，其中正常数据推送的消息类型为 `insert`，重启补发数据推送的消息类型为 `snapshot`，删除操作的消息类型为 `delete`，更新操作的消息类型为 `update`。<br >- `ignore_history`：是否忽略历史数据。支持 `on` 和 `off` 两个取值。`on` 表示忽略历史数据，即不推送历史数据。`off` 表示推送历史数据。默认情况下，不推送历史数据。<br >- `buffer_size`：缓冲大小，单位 MiB。`0` 表示立即发送。默认情况下，设置为 `1`。<br >- `retrieve_tags`：是否开启补充普通 Tag 功能。当用户未在推送任务输出列或者过滤列中指定普通 Tag 时，无论是否开启补充普通 Tag 功能，系统都不会补充普通 Tag 值。支持 `on` 和 `off` 两个取值。`on` 表示开启补充普通 Tag 功能。当开启补充普通 Tag 功能时，如果用户在推送任务输出列或者过滤列中指定了普通 Tag 但写入数据时未指定普通 Tag 的取值，系统读取已经写入的相同 Primary Tag 数据中的普通 Tag 的值并自动补充到写入的数据中。如果用户写入普通 Tag 的值与首次写入 Primary Tag 中普通 Tag 的取值不匹配，系统读取第一次写入 Primary Tag 中普通 Tag 的取值并更新当前普通 Tag 的取值，然后再进行推送或过滤。`off` 表示不开启补充普通 Tag 功能。当未开启补充普通 Tag 功能时，用户在推送任务输出列或者过滤列中指定了普通 Tag 但写入数据时未指定普通 Tag 的取值，系统按照 NULL 值处理省略的普通 Tag。如果用户写入的 Primary Tag 和普通 Tag 与第一次写入时的取值不匹配，系统会按照当前写入的普通 Tag 值进行推送或过滤。默认情况下，开启补充普通 Tag 功能。<br >- `publish`：数据推送的操作类型，支持 `insert`、`update`、`delete`、`ddl` 和 `all` 操作。默认情况下，设置为 `insert`。 <br > **说明** <br >目前，KWDB 只支持在线修改 `enable` 参数。如需修改其它参数，用户需要先停止实时数据推送服务，然后再修改相关参数。|

### 语法示例

- 修改数据推送管道的目标时序表

    以下示例将修改数据推送管道的过滤条件，将 `ts_table_a` 时序表的 `max_usage_user` 参数的取值设置为 `> 50`。

    ```sql
    ALTER PIPE ts_table_a_pipe_a SET TABLE ts_table_a(*) WHERE hostname='www.example1.com' AND max_usage_user > 50;
    ```

- 修改数据推送管道的推送参数

    以下示例修改数据推送管道的推送参数，停止 `ts_table_a_pipe` 数据推送管道实时数据推送。

    ```sql
    -- 停止 PIPE
    ALTER PIPE ts_table_a_pipe_a SET OPTIONS (enable = 'off');
    ```

    用户也可以直接使用 `ALTER PIPE <name> SET <push_parameter> = '<value>'` 的格式修改数据推送管道的推送参数。

    ```sql
    -- 停止 PIPE
    ALTER PIPE ts_table_a_pipe_a SET enable = 'off';
    ```

## 删除数据推送管道

`DROP PIPE` 语句用于删除指定的数据推送管道。若系统正在推送数据数据，当前推送正常完成后才能删除指定的数据推送管道。

### 所需权限

- 用户是 `admin` 角色的成员或者数据推送管道的创建者。默认情况下，`root` 用户属于 `admin` 角色。

::: warning 说明
如果创建数据推送管道的用户被删除后，只有 Admin 用户 或 `sysadmin` 用户可以删除目标数据推送管道。
:::

### 语法格式

![](../../static/sql-reference/droppipe.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF EXISTS` | 可选关键字。当使用 `IF EXISTS` 关键字时，如果目标数据推送管道存在，系统删除目标数据推送管道。如果目标数据推送管道不存在，系统删除目标数据推送管道失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果目标数据推送管道存在，系统删除目标数据推送管道。如果目标数据推送管道不存在，系统报错，提示目标数据推送管道不存在。 |
| `name` | KWDB 数据推送管道的名称。 |

### 语法示例

以下示例删除 `ts_table_a_pipe_a` 数据推送管道。

```sql
DROP PIPE ts_table_a_pipe_a;
```
