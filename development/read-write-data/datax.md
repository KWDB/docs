---
title: DataX 读写数据
id: datax
---

# DataX 读写数据

[DataX](https://github.com/alibaba/DataX) 是一款广泛使用的离线数据同步工具，能够实现 [MySQL](https://www.mysql.com/)、[SQL Server](https://www.microsoft.com/zh-cn/sql-server/)、[Oracle](https://www.oracle.com/)、[PostgreSQL](https://www.postgresql.org/)、[Hadoop HDFS](https://hadoop.apache.org/)、[Apache Hive](https://hive.apache.org/)、[Apache HBase](https://hbase.apache.org/)、[OTS](https://www.aliyun.com/product/ots) 等各种异构数据源之间的数据同步。

## 概述

作为数据同步框架，DataX 能够将不同数据源的同步抽象为从源数据源读取数据的 Reader 插件，以及向目标数据源写入数据的 Writer 插件，从而实现不同数据源的数据同步工作。基于 DataX 框架，KWDB 提供了用于写入和读取数据的 KaiwuDBWriter 和 KaiwuDBReader 插件。

### 数据类型映射

下表列出 DataX 数据类型与 KWDB 数据类型之间的映射关系。

| DataX 数据类型 | KWDB 数据类型  |
|----------------|---------------------------------------------------|
| INT            | TINYINT、SMALLINT、INT                              |
| LONG           | TINYINT、SMALLINT、INT、BIGINT、TIMESTAMP、TIMESTAMPTZ |
| DOUBLE         | FLOAT、REAL、DOUBLE、DECIMAL                         |
| BOOL           | BOOL、BIT                                          |
| DATA           | DATE、TIME、TIMESTAMP、TIMESTAMPTZ                   |
| BYTES          | BYTES、VARBYTES                                    |
| STRING         | CHAR、NCHAR、VARCHAR、NVARCHAR、TIMESTAMP、TIMESTAMPTZ |

### KaiwuDBWriter

KaiwuDBWriter 通过 DataX 获取 Reader 生成的协议数据，将目标表的数据以全量或增量的方式写入 KWDB 的时序表和关系表中。KaiwuDBWriter 支持将以下版本的数据库数据同步到 KWDB 数据库：

::: warning 说明
理论上，支持使用 DataX 将其它类型的数据库数据同步到 KWDB，但未经测试。
:::

| 数据库     | 插件                                                                               | 版本                  | 说明                                                                                                                                                                                                                                                                                                                              |
| ---------- | ---------------------------------------------------------------------------------- | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ClickHouse | ClickHouseReader                                                                   | 插件支持的版本        | - DataX 插件使用的 JDBC 驱动版本较低，不支持毫秒级精度的时间读取，可能导致错误删除数据。建议先升级 DataX 插件的 JDBC 驱动版本。解决升级导致的问题后，再进行数据迁移。<br> - 在 ClickHouse 中，NULL 值会显示为 `0`，导入 KWDB 后，NULL 值会被处理为 `false`。<br> - 二进制类型数据导入 KWDB 后，会以 `\x+` 空字符串的形式显示。                 |
| InfluxDB   | InfluxDB10Reader                                                                   | 1.x 版本              | -                                                                                                                                                                                                                                                                                                                                 |
|            | InfluxDB20Reader                                                                   | 2.x 版本              |                                                                                                                                                                                                                                                                                                                                   |
| KWDB    | KaiwuDBReader                                                                      | 2.0.0 及以上版本      | -                                                                                                                                                                                                                                                                                                                                 |
| MongoDB    | DataX MongoDBReader                                                                | 插件支持的版本        | - DataX 自带的 Reader 插件不支持 MongoDB 7。 <br>- 不支持迁移 MongoDB 数据库的 `_id` 列。                                                                                                                                                                                                                                         |
| MySQL      | DataX MysqlReader                                                                  | 插件支持的版本        | -                                                                                                                                                                                                                                                                                                                                 |
| OpenTSDB   | DataX OpenTSDBReader                                                               | 2.3.X 版本            | - OpenTSDB 是键值对类型的数据库。在读取 OpenTSDB 数据时，数据以键值对的形式呈现。<br>- KaiwuDBWriter 会对读取的 OpenTSDB metric 进行修改，将 metric 中的英文句号（`.`）修改为下划线（`\`），然后将其作为 KWDB 数据库的表名。每张表中存储的数据包括 `k_timestamp` 和 `value` 两列。<br >- 当写入数据的表不存在时，支持自动创建表。 |
| Oracle     | OracleReader                                                                       | 插件支持的版本        | -                                                                                                                                                                                                                                                                                                                                  |
| PostgreSQL | DataX PostgresqlReader                                                             | 插件支持的版本        | -                                                                                                                                                                                                                                                                                                                                 |
| TDengine   | [tdengine20reader](https://github.com/taosdata/DataX/tree/master/tdengine20reader) | 2.4.0.14 以下版本     | - TDengine 数据库中，如果 BOOL 类型的字段值为 null，导入 KWDB 后，会显示为 `false`。<br> - TDengine 数据库中，如果 NCHAR 类型的字段值为 null，导入 KWDB 后，会显示为空字符串。<br>- TDengineReader 不支持读取 JSON 类型数据。如果数据表的标签列采用 JSON 格式，需要转为其他类型，否则会导致迁移失败。                                  |
|            | DataX TDengineReader                                                               | 2.4.0.14 - 3.0.0 版本 | -                                                                                                                                                                                                                                                                                                                                  |
|            | [tdengine30reader](https://github.com/taosdata/DataX/tree/master/tdengine30reader) | 3.0.0 以上版本        | -                                                                                                                                                                                                                                                                                                                                  |

### KaiwuDBReader

KaiwuDBReader 通过 DataX 将 KWDB 数据库的数据写出到其他数据库，完成数据库的异步数据迁移。KaiwuDBReader 支持将 KWDB 数据库的数据同步到以下版本的数据库。

::: warning 说明
理论上，支持使用 DataX 将 KWDB 数据库的数据读取到其它类型的数据库数据，但未经测试。
:::

| 数据库   | 插件                 | 版本             | 说明                                                   |
| -------- | -------------------- | ---------------- | ------------------------------------------------------ |
| MySQL    | DataX MysqlWriter    | 插件支持的版本   |  -                                                      |
| TDengine | DataX TDengineReader | 2.x 和 3.x       | 大数据量场景下，建议将 `batchSize` 设置为 `1000`。 |
| KWDB  | KaiwuDBWriter        | 2.0.0 及以上版本 |   -                                                     |

## 配置 KaiwuDBWriter

### 前提条件

- DataX 部署环境
  - Linux 系统环境。
  - [安装 Java](https://docs.oracle.com/en/java/javase/22/install/overview-jdk-installation.html)（1.8 及以上版本）。
  - [安装 Python](https://www.python.org/downloads/)（2.X 或 3.X）。
- DataX 工具
  - [安装 DataX](https://gitee.com/mirrors/DataX/blob/master/userGuid.md)。
  - 获取 KaiwuDBWriter 插件压缩包。
- 数据库及权限设置
  - 获取源数据库的登录用户凭证。
  - 创建 KWDB 数据库。
  - 用户拥有表和数据库的操作权限，包括数据库的创建权限、表数据的读取和写入权限。

### 配置步骤

1. 将 KWDB 插件包上传到安装 DataX 的机器，解压缩插件包，然后将解压后的文件复制到 `datax/plugin/writer/` 目录下。
2. 进入 DataX 的 `datax/job/` 目录，创建 DataX 作业配置文件，定义源数据库和目标数据库的连接、读写的数据和相应的格式要求。

   ::: warning 说明
   不同数据源的作业配置文件要求不同，用户可以在 `datax/datax/` 目录下运行 `python ../bin/datax.py -r {YOUR_READER} -w {YOUR_WRITER}` 命令查看源数据库和目标数据库的作业配置模板，参考模板定义所需的配置文件，例如 `python ./bin/datax.py -r mysqlreader -w kaiwudbwriter`。
   :::

   - 有关将 MySQL 的原表数据同步到 KWDB 中的 DataX 作业配置文件，参见[从 MySQL 同步到 KWDB](#从-mysql-同步到-kaiwudb)。
   - 有关将 TDengine 的原表数据同步到 KWDB 中的 DataX 作业配置文件，参见[从 TDengine 同步到 KWDB](#从-tdengine-同步到-kaiwudb)。

3. 执行创建的 JSON 配置文件，启动 DataX，开启数据同步。

   ::: warning 说明
   在迁移大数据量数据时，建议在启动命令后加上参数 `--jvm`，增大 JVM 内存，例如 `python ../bin/datax.py mysql2kaiwudb.json --jvm="-Xms10G -Xmx10G"`。

   ```shell
   cd datax/datax/job/
   python ../bin/datax.py mysql2kaiwudb.json
   ```

   :::

   如果同步正常结束，控制台将输出以下信息：

   ```shell
   ...
   2024-01-24 9:20:25.262 [job-0] INFO  JobContainer -
   任务启动时刻            : 2024-01-24 9:20:15
   任务结束时刻            : 2024-01-24 9:20:20
   任务总计耗时            : 5s
   任务平均流量            : 205B/s
   记录写入速度            : 5rec/s
   读出记录总数            : 50
   读写失败总数            : 0
   ```

   如果同步异常，可能会出现以下异常信息，请根据异常提示原因，进行检查。

   | 异常信息                                               | 处理措施                                                                                              |
   | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
   | KaiwuDBWriter-00:您的配置错误                         | 检查 DataX 作业配置文件。                                                                             |
   | KaiwuDBWriter-01:缺少必要的值                          | 检查 JSON 配置文件中必须字段，确认是否配置相应的值。                                                  |
   | KaiwuDBWriter-02:值非法                                | 检查 JSON 配置文件中相关字段的值，确认是否符合规范和数据类型要求。                                    |
   | KaiwuDBWriter-03:运行时异常                            | 检查 JSON 配置文件后重试。如果问题仍然存在，请联系 KWDB 技术支持人员。                             |
   | KaiwuDBWriter-04:DataX 类型无法正确映射到 KWDB 类型 | 检查使用的 DataX 是否支持映射到 KWDB 数据类型。更多信息，参见[数据类型映射](#数据类型映射)。 |
   | KaiwuDBWriter-05:尚未支持实现                          | 功能不支持。                                                                                          |

### 配置举例

#### 从 MySQL 同步到 KWDB

KWDB 支持通过 DataX 将 MySQL 的数据同步到 KWDB 数据库的时序表和关系表中。不同类型的表对应的 DataX 作业配置（`job.json` 文件）有所不同。

##### 时序表

以下示例假设已经在 KWDB 数据库中创建时序数据库（`benchmark`）和时序表（`cpu`）。

```sql
/* 创建时序数据库：benchmark */
CREATE TS DATABASE benchmark;

/* 创建时序表：cpu */
CREATE TABLE benchmark.cpu (k_timestamp TIMESTAMPTZ NOT NULL, usage_user INT8 NOT NULL, usage_system INT8 NOT NULL, usage_idle INT8 NOT NULL) TAGS (id INT8 NOT NULL, hostname VARCHAR NOT NULL, region VARCHAR NOT NULL, datacenter VARCHAR NOT NULL) PRIMARY TAGS (id);
```

**全量数据同步配置举例**

- 有关 MysqlWriter 配置参数的详细信息，参见 [Writer 参数说明](#writer-参数说明)。
- 有关 KaiwuDBReader 配置参数的详细信息，参见 [Reader 参数说明](#reader-参数说明)。

```json
{
  "job": {
    "content": [
      {
        "reader": {
          "name": "mysqlreader",
          "parameter": {
            "username": "mysql_user",
            "password": "123456",
            "column": [
              "k_timestamp",
              "usage_user",
              "usage_system",
              "usage_idle",
              "9001 as id",
              "'localhost' as hostname",
              "'beijing' as region",
              "'center' as datacenter"
            ],
            "splitPk": "id",
            "connection": [
              {
                "table": [
                  "cpu"
                ],
                "jdbcUrl": [
                  "jdbc:mysql://127.0.0.1:3306/mysql_db?useSSL=false&useUnicode=true&characterEncoding=utf8"
                ]
              }
            ]
          }
        },
        "writer": {
          "name": "kaiwudbwriter",
          "parameter": {
            "username": "kaiwudb_user",
            "password": "kaiwudb@123",
            "column": [
              "k_timestamp",
              "usage_user",
              "usage_system",
              "usage_idle",
              "id",
              "hostname",
              "region",
              "datacenter"
            ],
            "connection": [
              {
                "table": [
                  "cpu"
                ],
                "jdbcUrl": "jdbc:kaiwudb://127.0.0.1:26257/benchmark"
              }
            ],
            "preSql": [
              ""
            ],
            "postSql": [
              ""
            ],
            "batchSize": 100
          }
        }
      }
    ],
    "setting": {
      "speed": {
        "channel": 1
      }
    }
  }
 }
```

**增量数据同步配置举例**

DataX 支持通过 reader 中的 `querySql` 或 `table` 和 `where` 参数限定数据读取范围，从而实现增量数据同步。

- 有关 MysqlWriter 配置参数的详细信息，参见 [Writer 参数说明](#writer-参数说明)。
- 有关 KaiwuDBReader 配置参数的详细信息，参见 [Reader 参数说明](#reader-参数说明)。

示例 1：通过 `querySql` 限定数据同步范围。

```json
{
  "job": {
    "content": [
      {
        "reader": {
          "name": "mysqlreader",
          "parameter": {
            "username": "root",
            "password": "123456",
            "connection": [
              {
                "querySql": [
                  "select k_timestamp, usage_user, usage_system, usage_idle, 9001 as id, 'localhost' as hostname, 'beijing' as region, 'center' as datacenter from cpu where id > 2000"
                ],
                "jdbcUrl": [
                  "jdbc:mysql://127.0.0.1:3306/test_db?useSSL=false&useUnicode=true&characterEncoding=utf8"
                ]
              }
            ]
          }
        },
        "writer": {
          "name": "kaiwudbwriter",
          "parameter": {
            "username": "root",
            "password": "kaiwudb@123",
            "column": [
              "k_timestamp",
              "usage_user",
              "usage_system",
              "usage_idle",
              "id",
              "hostname",
              "region",
              "datacenter"
            ],
            "connection": [
              {
                "table": [
                  "cpu"
                ],
                "jdbcUrl": "jdbc:kaiwudb://127.0.0.1:26257/ts_db"
              }
            ],
            "batchSize": 100
          }
        }
      }
    ],
    "setting": {
      "speed": {
        "channel": 1
      }
    }
  }
}
```

示例 2：通过 `table` 和 `where` 参数限定数据同步范围。

```json
{
  "job": {
    "content": [
      {
        "reader": {
          "name": "mysqlreader",
          "parameter": {
            "username": "root",
            "password": "123456",
            "column": [
              "k_timestamp",
              "usage_user",
              "usage_system",
              "usage_idle",
              "9001 as id",
              "'localhost' as hostname",
              "'beijing' as region",
              "'center' as datacenter"
            ],
            "connection": [
              {
                "table": [
                  "cpu"
                ],
                "jdbcUrl": [
                  "jdbc:mysql://127.0.0.1:3306/test_db?useSSL=false&useUnicode=true&characterEncoding=utf8"
                ]
              }
            ],
            "where": "id > 1000"
          }
        },
        "writer": {
          "name": "kaiwudbwriter",
          "parameter": {
            "username": "root",
            "password": "kaiwudb@123",
            "column": [
              "k_timestamp",
              "usage_user",
              "usage_system",
              "usage_idle",
              "id",
              "hostname",
              "region",
              "datacenter"
            ],
            "connection": [
              {
                "table": [
                  "cpu"
                ],
                "jdbcUrl": "jdbc:kaiwudb://127.0.0.1:26257/ts_db"
              }
            ],
            "batchSize": 100
          }
        }
      }
    ],
    "setting": {
      "speed": {
        "channel": 1
      }
    }
  }
}
```

##### 关系表

关系表与时序表的同步区别在于关系表在写入时支持通过 `writeMode` 指定选择 INSERT 或 UPDATE 模式。

以下示例假设已经在 KWDB 数据库中创建关系库（`relation_db`）和关系表（`base_tb`）。

```sql
/*创建关系库：relation_db*/
create database relation_db;

/*创建关系表：base_tb */
create table relation_db.base_tb (id serial primary key, ts timestamp, c1 smallint, c2 int, c3 bigint);
```

DataX 作业配置示例如下：

```json
{
  "job": {
    "content": [
      {
        "reader": {
          "name": "mysqlreader",
          "parameter": {
            "username": "mysql_user",
            "password": "123456",
            "column": [
              "id",
              "ts",
              "c1",
              "c2",
              "c3"
            ],
            "splitPk": "id",
            "connection": [
              {
                "table": [
                  "mysql_tb"
                ],
                "jdbcUrl": [
                  "jdbc:mysql://127.0.0.1:3306/mysql_db?useSSL=false&useUnicode=true&characterEncoding=utf8"
                ]
              }
            ]
          }
        },
        "writer": {
          "name": "kaiwudbwriter",
          "parameter": {
            "username": "kaiwudb_user",
            "password": "kaiwudb@123",
            "column": [
              "id",
              "ts",
              "c1",
              "c2",
              "c3"
            ],
            "connection": [
              {
                "table": [
                  "base_tb"
                ],
                "jdbcUrl": "jdbc:kaiwudb://127.0.0.1:26257/relation_db"
              }
            ],
            "writeMode": "INSERT",
            "preSql": [
              "update base_tb set c1=11 where c1=1"
            ],
            "postSql": [
              "update base_tb set c1=10 where c1=0"
            ],
            "batchSize": 100
          }
        }
      }
    ],
    "setting": {
      "speed": {
        "channel": 1
      }
    }
  }
}
```

- 有关 MysqlReader 配置参数的详细信息，参见 [Reader 参数说明](#reader-参数说明)。
- 有关 KaiwuDBWriter 配置参数的详细信息，参见 [Writer 参数说明](#writer-参数说明)。

#### 从 TDengine 同步到 KWDB

KWDB 支持通过 DataX 将 TDengine 的数据同步到 KWDB 数据库的时序表。用户可以选择将 TDengine 的子表或普通表同步到 KWDB 的时序表，也可以选择将 TDengine 超表下所有子表的数据同步到 KWDB 的时序表。

以下示例假设已经在 TDengine 数据库中创建一张超表 `st`，两张子表 `ct1` 和 `ct2` 和一张普通表 `cpu`。

```sql
/* 源数据库benchmark */
CREATE DATABASE if not exists benchmark;

/* 超表st  */
CREATE TABLE benchmark.cpu (k_timestamp TIMESTAMPTZ NOT NULL, usage_user INT8 NOT NULL, usage_system INT8 NOT NULL, usage_idle INT8 NOT NULL, hostname VARCHAR NOT NULL, region VARCHAR NOT NULL, datacenter VARCHAR NOT NULL) tags (id INT8 NOT NULL);

/* 子表 ct1和ct2*/
CREATE TABLE benchmark.ct1 using st tags (1);
CREATE TABLE benchmark.ct2 using st tags (2);

/* 普通表 cpu*/
CREATE TABLE benchmark.cpu (k_timestamp TIMESTAMPTZ NOT NULL, usage_user INT8 NOT NULL, usage_system INT8 NOT NULL, usage_idle INT8 NOT NULL, id INT8 NOT NULL, hostname VARCHAR NOT NULL, region VARCHAR NOT NULL, datacenter VARCHAR NOT NULL);
```

##### 普通表或子表

以下示例假设已经在 KWDB 数据库中创建时序数据库（`benchmark`）和时序表（`cpu`），用于同步 TDengine 中的普通表 `cpu`。

```sql
/*创建时序数据库：benchmark */
CREATE TS DATABASE benchmark;
/*创建时序表：cpu */
CREATE TABLE benchmark.cpu (k_timestamp TIMESTAMPTZ NOT NULL, usage_user INT8 NOT NULL, usage_system INT8 NOT NULL, usage_idle INT8 NOT NULL) TAGS (id INT8 NOT NULL, hostname VARCHAR NOT NULL, region VARCHAR NOT NULL, datacenter VARCHAR NOT NULL) PRIMARY TAGS (id);
```

DataX 作业配置示例如下：

```json
{
  "job": {
    "content": [
      {
        "reader": {
          "name": "tdengine30reader",
          "parameter": {
            "username": "root",
            "password": "taosdata",
            "column": [
              "k_timestamp",
              "usage_user",
              "usage_system",
              "usage_idle",
              "9001 as id",
              "'localhost' as hostname",
              "'beijing' as region",
              "'center' as datacenter"
            ],
            "connection": [
              {
                "table": [
                  "cpu"
                ],
                "jdbcUrl": [
                  "jdbc:TAOS-RS://127.0.0.1:6041/test_db?timestampFormat=STRING"
                ]
              }
            ]
          }
        },
        "writer": {
          "name": "kaiwudbwriter",
          "parameter": {
            "username": "root",
            "password": "kaiwudb@123",
            "column": [
              "k_timestamp",
              "usage_user",
              "usage_system",
              "usage_idle",
              "id",
              "hostname",
              "region",
              "datacenter"
            ],
            "connection": [
              {
                "table": [
                  "cpu"
                ],
                "jdbcUrl": "jdbc:kaiwudb://127.0.0.1:26257/tdengine_kwdb"
              }
            ],
            "batchSize": 100
          }
        }
      }
    ],
    "setting": {
      "speed": {
        "channel": 1
      }
    }
  }
}
```

##### 超表

以下示例假设已经在 KWDB 数据库中创建时序数据库（`benchmark`）和时序表（`st`），用于同步 TDengine 中的超表 `st`。

```sql
/*创建时序数据库：benchmark */
create ts database benchmark;
/*创建时序表：st */
CREATE TABLE benchmark.st (k_timestamp TIMESTAMPTZ NOT NULL, usage_user INT8 NOT NULL, usage_system INT8 NOT NULL, usage_idle INT8 NOT NULL) TAGS (id INT8 NOT NULL, hostname VARCHAR NOT NULL, region VARCHAR NOT NULL, datacenter VARCHAR NOT NULL) PRIMARY TAGS (id);
```

DataX 作业配置示例如下：

```json
{
  "job": {
    "content": [
      {
        "reader": {
          "name": "tdengine30reader",
          "parameter": {
            "username": "root",
            "password": "taosdata",
            "column": [
              "k_timestamp",
              "usage_user",
              "usage_system",
              "usage_idle",
              "9001 as id",
              "'localhost' as hostname",
              "'beijing' as region",
              "'center' as datacenter"
            ],
            "connection": [
              {
                "table": [
                  "st"
                ],
                "jdbcUrl": [
                  "jdbc:TAOS-RS://127.0.0.1:6041/test_db?timestampFormat=STRING"
                ]
              }
            ]
          }
        },
        "writer": {
          "name": "kaiwudbwriter",
          "parameter": {
            "username": "root",
            "password": "kaiwudb@123",
            "column": [
              "k_timestamp",
              "usage_user",
              "usage_system",
              "usage_idle",
              "id",
              "hostname",
              "region",
              "datacenter"
            ],
            "connection": [
              {
                "table": [
                  "st"
                ],
                "jdbcUrl": "jdbc:kaiwudb://127.0.0.1:26257/tdengine_kwdb"
              }
            ],
            "batchSize": 100
          }
        }
      }
    ],
    "setting": {
      "speed": {
        "channel": 1
      }
    }
  }
}
```

## 配置 KaiwuDBReader

### 前提条件

- DataX 部署环境：
  - Linux 系统环境。
  - [安装 Java](https://docs.oracle.com/en/java/javase/22/install/overview-jdk-installation.html)（1.8 及以上版本）。
  - [安装 Python](https://www.python.org/downloads/)（2.X 或 3.X）。
- DataX 工具：
  - [安装 DataX](https://gitee.com/mirrors/DataX/blob/master/userGuid.md)。
  - 已获取 KaiwuDBReader 插件压缩包。
- 数据库及权限设置：
  - 获取源数据库的登录用户凭证。
  - 创建 KWDB 数据库。
  - 用户拥有表和数据库的操作权限，包括数据库的创建权限、表数据的读取和写入权限。

### 配置步骤

1. 将 KWDB 插件包上传到安装 DataX 的机器，解压缩插件包，将解压后的文件复制到 `datax/plugin/reader/` 目录下。
2. 进入 DataX 的 `datax/job/` 目录，创建 JSON 格式的 DataX 作业配置文件，定义源数据库和目标数据库的连接、读写的数据和相应的格式要求。

   ::: warning 说明
   不同数据源的作业配置文件要求不同，用户可以在 `datax/datax/` 目录下运行 `python ../bin/datax.py -r {YOUR_READER} -w {YOUR_WRITER}` 命令查看源数据库和目标数据库的作业配置模板，参考模板定义所需的配置文件，例如 `python ./bin/datax.py -r kaiwudbreader -w mysqlwriter`。
   :::

   - 有关将 KWDB 的原表数据同步到 MySQL 中的 DataX 作业配置文件，参见[从 KWDB 同步到 MySQL](#从-kaiwudb-同步到-mysql)。
   - 有关将 KWDB 的原表数据同步到 KWDB 目标表中的 DataX 作业配置文件，参见[从 KWDB 同步到 KWDB](#从-kaiwudb-同步到-kaiwudb)。

3. 执行创建的 JSON 配置文件，启动 DataX，开启数据同步。

   ```shell
   cd datax/datax/job/
   python ../bin/datax.py kaiwudb2mysql.json
   ```

### 配置举例

#### 从 KWDB 同步到 MySQL

以下示例假设已经在 KWDB 数据库中创建时序数据库（`benchmark`）和时序表（`cpu`）。

```sql
/* 创建时序数据库：benchmark */
CREATE TS DATABASE benchmark;

/* 创建时序表：cpu */
CREATE TABLE benchmark.cpu (k_timestamp TIMESTAMPTZ NOT NULL, usage_user INT8 NOT NULL, usage_system INT8 NOT NULL, usage_idle INT8 NOT NULL) TAGS (id INT8 NOT NULL, hostname VARCHAR NOT NULL, region VARCHAR NOT NULL, datacenter VARCHAR NOT NULL) PRIMARY TAGS (id);
```

DataX 作业配置示例如下：

```json
{
  "job": {
    "content": [
      {
        "reader": {
          "name": "kaiwudbreader",
          "parameter": {
            "username": "test",
            "password": "Password@2024",
            "column": [
              "k_timestamp",
              "usage_user",
              "usage_system",
              "usage_idle",
              "id",
              "hostname",
              "region",
              "datacenter"
            ],
            "tsColumn": "k_timestamp",
            "beginTime": "2024-05-01 10:00:000",
            "endTime": "2024-05-02 10:00:000",
            "connection": [
              {
                "table": [
                  "cpu"
                ],
                "jdbcUrl": [
                  "jdbc:kaiwudb://127.0.0.1:26257/benchmark"
                ]
              }
            ]
          }
        },
        "writer": {
          "name": "mysqlwriter",
          "parameter": {
            "writeMode": "insert",
            "username": "root",
            "password": "123456",
            "column": [
              "k_timestamp",
              "usage_user",
              "usage_system",
              "usage_idle",
              "id",
              "hostname",
              "region",
              "datacenter"
            ],
            "preSql": [
              ""
            ],
            "connection": [
              {
                "table": [
                  "cpu"
                ],
                "jdbcUrl": "jdbc:mysql://127.0.0.1:3306/benchmark?useSSL=false&useUnicode=true&characterEncoding=utf8"
              }
            ]
          }
        }
      }
    ],
    "setting": {
      "speed": {
        "channel": 1
      }
    }
  }
}
```

#### 从 KWDB 同步到 KWDB

以下示例假设已经在源数据库创建时序数据库（`source`）和时序表（`cpu`），在目标数据库创建时序数据库（`target`）和时序表（`cpu`）。

```sql
/*创建时序数据库：source */
CREATE TS DATABASE source;
/*创建时序表：cpu */
CREATE TABLE source.cpu (k_timestamp TIMESTAMPTZ NOT NULL, usage_user INT8 NOT NULL, usage_system INT8 NOT NULL, usage_idle INT8 NOT NULL) TAGS (id INT8 NOT NULL, hostname VARCHAR NOT NULL, region VARCHAR NOT NULL, datacenter VARCHAR NOT NULL) PRIMARY TAGS (id);

/*创建时序数据库：target */
CREATE TS DATABASE target;
/*创建时序表：cpu */
CREATE TABLE target.cpu (k_timestamp TIMESTAMPTZ NOT NULL, usage_user INT8 NOT NULL, usage_system INT8 NOT NULL, usage_idle INT8 NOT NULL) TAGS (id INT8 NOT NULL, hostname VARCHAR NOT NULL, region VARCHAR NOT NULL, datacenter VARCHAR NOT NULL) PRIMARY TAGS (id);
```

DataX 作业配置示例如下：

```json
{
  "job": {
    "content": [
      {
        "reader": {
          "name": "kaiwudbreader",
          "parameter": {
            "username": "test",
            "password": "Password@2024",
            "mandatoryEncoding": "utf-8", 
            "connection": [
              {
                "querySql": [
                  "select k_timestamp, usage_user, usage_system, usage_idle, id, hostname, region, datacenter from cpu"
                ],
                "jdbcUrl": [
                  "jdbc:kaiwudb://127.0.0.1:26257/source"
                ]
              }
            ]
          }
        },
        "writer": {
          "name": "kaiwudbwriter",
          "parameter": {
            "username": "test",
            "password": "Password@2024",
            "column": [
              "k_timestamp",
              "usage_user",
              "usage_system",
              "usage_idle",
              "id",
              "hostname",
              "region",
              "datacenter"
            ],
            "connection": [
              {
                "table": [
                  "cpu"
                ],
                "jdbcUrl": "jdbc:kaiwudb://127.0.0.1:26257/target"
              }
            ],
            "preSql": [
              ""
            ],
            "batchSize": 100
          }
        }
      }
    ],
    "setting": {
      "speed": {
        "channel": 1
      }
    }
  }
}
```

## 参考信息

### Writer 参数说明

| 参数 | 说明 |
| --- | --- |
| `name` | 目标数据库插件的名称，例如 `kaiwudbwriter`。|
| `username` | 连接 KWDB 数据库的用户名。|
| `password` | 连接 KWDB 数据库的密码。|
| `column` | 指定将源表的列数据写入到目标表对应的列中。列的顺序和数量需要与 Reader 中 `column` 或 `querySql select` 中定义的列顺序和数量一致。|
| `connection` | 定义数据库的连接信息，包括两个参数：<br >- `table`：指定将数据写入的目标时序表和关系表。该表应该是 `column` 字段列对应的表。<br>- `jdbcUrl`：指定 KWDB 数据库的 JDBC 连接信息。|
| `writeMode` | 可选参数，指定写入模式，包括 `INSERT` 和 `UPDATE` 模式。默认是 `INSERT` 模式，表示使用 `INSERT` 语句插入数据。如果设置为 `UPDATE` 模式，则使用 `UPSERT` 语句写入数据。|
| `preSql` | 可选参数，配置在迁移同步数据之前在 KWDB 数据库执行的 SQL 语句。|
| `postSql` | 可选参数，配置在迁移同步数据之后在 KWDB 数据库执行的 SQL 语句。|
| `batchSize` | 定义批量写入数据的大小。|

### Reader 参数说明

| 参数         | 说明                                                                                                                                                                                                                                                                                                                |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`       |目标数据库插件名称，例如 `kaiwudbwriter`。                                                                                                                                                                                                                                                      |
| `username`   | 连接源数据库的用户名。                                                                                                                                                                                                                                                                                              |
| `password`   | 连接源数据库的密码。                                                                                                                                                                                                                                                                                  |
| `column`     | 指定读取源数据库目标表的列数据。 <br >- 如果数据库连接选择使用 `querySql` 来指定源表数据读取范围，则无需设置 `colunm` 参数。<br> - 由于时序表的第一列必须是 timestamp 或 timestamptz 列，此处定义的数据列也必须包含时间列。                                                                                         |
| `tsColumn` | 只适用于 `kaiwudbreader` 插件。用于指定时序表的第一列时间戳列，与 `column` 参数同用。如果使用 `querySql` 参数指定源表数据读取范围，则无需设置 `tsColumn` 参数。 |
| `beginDateTime` | 可选参数，指定表的起始数据读取时间，与 `column` 参数同用。适用支持时序的数据库系统，如 TDengine、InfluxDB 和 OpenTSDB。如果使用 `querySql` 参数指定源表数据读取范围，则无需设置 `beginDateTime` 参数。|
| `endDateTime` | 可选参数，指定表的终止数据读取时间，与 `column` 参数同用。适用支持时序的数据库系统，如 TDengine、InfluxDB 和 OpenTSDB。如果使用 `querySql` 指定源表数据读取范围，则无需设置 `endDateTime` 参数。<br >**说明** <br > 如果 Reader 为 OpenTSDB Reader，`beginDateTime` 和 `endDateTime` 的间隔需为 `1` 小时以上。|
| `mandatoryEncoding` | 可选参数，指定字符编码。对于 `kaiwudbreader` 插件，默认为 `UTF-8`。 |
| `splitPk`    | 可选参数，用于表中有 ID 列时指定 ID 列。没有 ID 列时可不配置。只适用于 `mysqlreader` 插件，用于对 `splitPk` 代表的字段进行数据分片，启动并发任务。目前，`splitPk` 只支持整形数据切分。|
| `splitIntervalS` | 可选参数，切分时间间隔，仅适用于 InfluxDB。|
| `connection` | 数据库的连接信息，包括 `table` 和 `jdbcUrl` 参数或 `querySql` 和 `jdbcUrl` 参数。如果用户同时配置 `table` 和 `querySql` 参数，系统将自动忽略 `table` 参数配置。 <br >- `table`：指定读取数据的目标表。 <br >- `querySql`：指定源数据库表和列数据的读取范围。 <br >- `jdbcUrl`：指定源数据库的 JDBC 连接信息。 |
| `where`      | 可选参数，与 `table` 参数共同使用时，限定同步数据的范围，适用于增量数据同步场景。更多详细信息，参见[时序表配置示例](#时序表)。                                                                                                                                                                                      |
