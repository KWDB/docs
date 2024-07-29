---
title: 配置参数
id: config-params
---

# 配置参数

本文介绍数据迁移配置文件中源数据库、目标数据库、迁移设置、以及核心信息的相关配置参数。

## 源数据库（source）

下表列出源数据库的相关配置参数。

| 参数 | 说明 |
|---| ---|
| `pluginName`                         | 必选字段。Reader 插件的名称，区分大小写。                                                                                                                                                                                                                                                                                                                                                    |
| `databases`                          | 源数据库的连接信息和表的配置。                                                                                                                                                                                                                                                                                                                                                    |
| `databases.name`                     | 必选字段。源数据库的名称，区分大小写。InfluxDB 2.X 中，该参数用作 `bucket` 的值。                                                                                                                                                                                                                                                                                                              |
| `databases.url`                      | 必选字段。指定连接到源数据库的 JDBC URL。部分源数据库中，该参数用作 `endpoint` 的值。                                                                                                                                                                                                                                                                                                         |
| `databases.username`                 | 必选字段。源数据库的用户名，InfluxDB 2.X 中，该参数用作 `org` 的值。                                                                                                                                                                                                                                                                                                                          |
| `databases.password`                 | 必选字段。源数据库的用户密码，密码不得为空，InfluxDB 2.X 中，该参数用作 `token` 的值。                                                                                                                                                                                                                                                                                                         |
| `databases.tables`                   | 待读取数据的表的配置。<br >以库的形式迁移数据时，无需填写表的相关配置。以表的形式迁移数据时，该参数为必选字段。                                                                                                                                                                                                                                                                            |
| `databases.tables.name`              | 待读取数据的表的名称，例如 `sensor_data`。InfluxDB 中，该参数用作 `measurement` 的值。MongoDB 中，该参数用作 `collectionName` 的值。<br >以库的形式迁移数据时，无需填写该参数。以表的形式迁移数据时，该参数为必选字段。                                                                                                                                                                         |
| `databases.tables.column`            | 待读取数据的表的列。根据数据源，可以配置为使用逗号（`,`）隔开的字符串或 Json 字符串。<br > 以库的形式迁移数据时，无需填写该参数。以表的形式迁移数据时，该参数为必选字段。                                                                                                                                                                                                                         |
| `databases.tables.querySql[]`        | 自定义的 SQL 查询语句集合。<br>- 用户可以使用 `column` 或 `query_sql` 参数指定数据读取范围。如果同时指定 `column_list` 和 `query_sql` 参数，系统根据 `query_sql` 参数限定数据读取范围。<br>- 同步时序表时，由于时序表的第一列必须是 timestamp 或 timestamptz 列，此处定义的数据列也必须包含第一列（时间戳列）。<br >以库的形式迁移数据时，无需填写该参数。以表的形式迁移数据时，该参数为必选字段。 |
| `databases.tables.splitPk`           | 可选字段。自定义的切分主键。                                                                                                                                                                                                                                                                                                                                                                |
| `databases.tables.where`             | 可选字段。自定义的 `where` 过滤条件，适用于增量数据迁移的应用场景。                                                                                                                                                                                                                                                                                                                          |
| `databases.tables.beginDateTime`     | 可选字段。自定义的时间过滤条件，适用于支持时序的数据库系统，例如 KWDB、TDengine、InfluxDB、OpenTSDB。                                                                                                                                                                                                                                                                                         |
| `databases.tables.endDateTime`       | 可选字段。自定义的时间过滤条件，适用于支持时序的数据库系统，例如 KWDB、TDengine、InfluxDB、OpenTSDB。                                                                                                                                                                                                                                                                                         |
| `databases.tables.splitIntervalS`    | 可选字段。切分时间间隔。该参数只适用于 InfluxDB。                                                                                                                                                                                                                                                                                                                                            |
| `databases.tables.tsColumn`          | 可选字段。指定时序表第一列（时间戳列），与 `databases.tables.column` 参数同效。适用于从 KWDB 同步到其它数据库的应用场景。                                                                                                                                                                                                                                                                    |
| `databases.tables.mandatoryEncoding` | 可选字段。指定字符编码，默认为 UTF-8，适用于从 KWDB 同步到其它数据库的应用场景。                                                                                                                                                                                                                                                                                                           |
| `fetchSize`                          | 可选字段。单次读取数据的条数，默认值为 `1000`。                                                                                                                                                                                                                                                                                                                                              |

## 目标数据库（target）

下表列出目标数据库的相关配置参数。

| 参数                         | 说明  |
|-------|---|
| `pluginName`                 | 必选字段。Writer 插件的名称，区分大小写。                                                                                                                                                                                   |
| `databases`                  | 必选字段。目标数据库的连接信息和表的配置。                                                                                                                                                                                 |
| `databases.name`             | 必选字段。目标数据库的名称，区分大小写。                                                                                                                                                                                    |
| `databases.url`              | 必选字段。目标数据库的 JDBC URL。部分源数据库中，该参数用作 `endpoint` 的值。                                                                                                                                                |
| `databases.username`         | 必选字段。目标数据库的用户名。                                                                                                                                                                                             |
| `databases.password`         | 必选字段。目标数据库的用户密码。                                                                                                                                                                                           |
| `databases.tables`           | 待写入数据的表的配置。<br >以库的形式迁移数据时，无需填写表的相关配置。以表的形式迁移数据时，该参数为必选字段。                                                                                                           |
| `databases.tables.name`      | 待写入数据的表的名称，以库形式进行迁移时无需填写，以表形式迁移时为必填选项。MongoDB 中，该参数用作 `collectionName` 的值。<br >以库的形式迁移数据时，无需填写该参数。以表的形式迁移数据时，该参数为必选字段。                 |
| `databases.tables.column`    | 待写入数据的表的列，根据数据源，可以配置为使用逗号（`,`）隔开的字符串或 Json 字符串。写入的列名数量和顺序必须与读取的列名数量和顺序保持一致。<br >以库的形式迁移数据时，无需填写该参数。以表的形式迁移数据时，该参数为必选字段。 |
| `databases.tables.writeMode` | 可选字段。数据写入模式，支持 `INSERT`、`UPSERT`，默认为 `INSERT`。                                                                                                                                                            |
| `databases.tables.preSql[]`  | 可选字段。写入数据前要执行的 SQL 语句。该参数只适用于目标数据库为 KWDB 或 TDengine 数据库的应用场景。                                                                                                                    |
| `databases.tables.postSql[]` | 可选字段。写入数据后要执行的 SQL 语句。该参数只适用于目标数据库为 KWDB 或 TDengine 数据库的应用场景。                                                                                                                    |
| `batchSize` | 可选字段。批量写入的数据条数。默认值为 `1000`。|

## 迁移设置（setting）

下表列出核心数据迁移设置的相关配置参数。

| 参数                    | 说明                                                                                         |
|-------------------------|--------------------------------------------------------------------------------------------|
| `speed`                 | 数据传输速度。                                                                                |
| `speed.channel`         | 可选字段。通道的数量。                                                                                  |
| `speed.byte`            | 可选字段。通道速度。如果单通道速度为 1 MB，该参数取值为 `1048576`时, 表示一个通道。                       |
| `speed.record`          | 可选字段。传输的记录的数量。                                                                            |
| `errorLimit`            | 数据传输时的出错限制。                                                                        |
| `errorLimit.percentage` | 可选字段。出错限制百分比。取值为 `1` 时，表示 100%。                                                      |
| `errorLimit.record`     | 可选字段。发生错误的记录的数量，用于定义系统何时抛出异常。取值为 `0` 时，表示报错后立即抛出异常，任务失败。 |
| `errorLimit.byte`       | 可选字段。读写数据时，允许出现的错误所占的字节数的上限。                                                 |

## 核心信息（core）

下表列出核心传输通道的相关配置参数。

| 参数 | 说明 |
|------------------------------------|-----------------------------------|
| `byte`                             | 可选字段。通道速度。                           |
| `record`                           | 可选字段。读取的记录的数量。                   |
