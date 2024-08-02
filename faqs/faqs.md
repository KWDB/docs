---
title: 常见问题解答（FAQ）
id: faqs
---

# 常见问题解答（FAQ）

## 安装部署 FAQ

### 依赖缺失

- **问题描述**

    安装 KWDB 时，系统提示安装失败。

    ```shell
    root@node:/home/admin/kaiwudb_install# ./deploy.sh install --single
    [ERROR] 2024-05-27 06:02:25 Error occurred during libopentelemetry-kw_1.8.1_amd64.deb installation. Please check log.
    ```

- **问题解答**

    用户可能未安装所需依赖。建议查看 `kaiwudb_install/log` 目录下的相关日志，然后根据日志信息，使用 `apt install` 命令安装缺失的依赖。

    日志示例：

    ```sql
    root@node:/home/admin/kaiwudb_install/log# cat 2024-05-27
    [INFO] 2024-05-27 06:02:25 start init directory /etc/kwdb /var/lib/kwdb
    [INFO] 2024-05-27 06:02:25 init directory success
    [INFO] 2024-05-27 06:02:25 start install binaries and libraries to /usr/local/kwdb
    [ERROR] 2024-05-27 06:02:25 Selecting previously unselected package libopentelemetry-kw. (Reading database ... 181016 files and directories currently installed.) Preparing to unpack .../libopentelemetry-kw_1.8.1_amd64.deb ... Unpacking libopentelemetry-kw (1.8.1) ... dpkg: dependency problems prevent configuration of libopentelemetry-kw: libopentelemetry-kw depends on libprotobuf17 | libprotobuf23; however: Package libprotobuf17 is not installed. Package libprotobuf23 is not installed. dpkg: error processing package libopentelemetry-kw (--install): dependency problems - leaving unconfigured Errors were encountered while processing: libopentelemetry-kw
    ```

## SQL FAQ

### 数据写入

- **问题描述**

    在 CentOS 操作系统的容器环境下安装 KWDB 后，用户可以创建时序数据库，但是创建时序表时报错 `Error: have been trying 30s, timed out of AdminReplicaVoterStatusConsistent`。查看日志，系统提示 `Err :connection error: desc = "transport: Error while dialing dial tcp 100.153.0.246:26257: connect: connection refused`。

- **问题解答**

    可能是因为容器无法访问宿主机的 IP 地址，导致建表时报错。建议修改防火墙配置，允许容器网段访问宿主机。

    配置示例：

    ```shell
    firewall-cmd --zone=public --add-rich-rule='rule family="ipv4" source address="172.18.0.4/24" port protocol="tcp" port="22" accept' --permanent
    ```

### 数据查询

#### 生命周期设置

- **问题描述**

    用户创建了生命周期为 `1` 分钟的时序表，并写入数据。然而，表的生命周期到期后，用户仍然可以查询到表数据。

    ```sql
    show create temp;
      table_name |              create_statement
    -------------+----------------------------------------------
      temp       | CREATE TABLE temp (
                |     ts TIMESTAMPTZ NOT NULL,
                |     c1 INT4 NULL
                | ) TAGS (
                |     tag1 INT4 NOT NULL ) PRIMARY TAGS(tag1)
                |      retentions 1m
    (1 row)

    select * from temp;
                  ts               | c1 | tag1
    --------------------------------+----+-------
      2024-05-27 03:06:14.465+00:00 |  3 |    1
      2024-05-27 03:06:39.188+00:00 |  1 |    1
      2024-05-27 03:06:46.104+00:00 |  2 |    1
      2024-05-27 03:10:55.501+00:00 |  3 |    1
    (4 rows)
    ```

- **问题解答**

    时序表的生命周期设置不适用于当前分区。默认情况下，系统每 10 天进行一次分区。即使表的生命周期已到期，由于数据仍存储在当前的分区中，因此用户仍然可以查到数据。

#### 时间加减计算

- **问题描述**

    执行较大范围的时间加减运算时，计算结果有误。

    ```sql
    select '2060-01-01 00:00:00':: timestamptz -'1600-01-01 00:00:00':: timestamptz;
              ?column?
    -------------------------------
      106751 days 23:47:16.854776
    (1 row)
    ```

- **问题解答**

    KWDB 执行时间加减运算时，如果运算符两边均为 timestamp 或 timestamptz 类型，只支持减法运算，且差值对应的纳秒数不得超过 INT64 范围，对应的天数不得超过 `106751` 天。如果超过该范围，系统将统一显示 `106751 days 23:47:16.854776`。

## 监控 FAQ

::: warning 说明
目前，KaiwuDB 监控平台是企业版特性。如需了解 KaiwuDB 监控平台的更多详细信息，[联系](https://cs.kaiwudb.com/support/) KaiwuDB 技术支持人员。
:::

- **问题描述**

    在 Linux 系统上部署 KWDB 数据库后，在 Windows 操作系统下使用 URL 登录 KaiwuDB 监控平台时，提示验证码错误。

- **问题解答**

    如果用户名和密码均准确无误，可能是 KWDB 数据库所在的 Linux 服务器和 Windows 操作系统之间存在较高的网络时延，导致验证超时。建议进行时间校准，确保 Linux 服务器和 Windows 系统的时间同步，避免由于时间不同步导致的验证超时问题。

## 数据迁移 FAQ

- **问题描述**

    使用 KaiwuDB DataX Utils 从 InfluxDB 向 KWDB 写入数据时，写入速率较慢。

- **问题解答**

    数据的实际写入速率与数据特性、硬件规格相关。用户可以采取以下步骤，调整相关参数配置，提升写入速率。

    1. 开启数据库短接写入功能。

        ```SQL
        SET CLUSTER SETTING server.tsinsert_direct.enabled = 'TRUE';
        ```

    2. （可选）关闭 WAL 日志实时写入功能。

        1. 关闭 WAL 日志写入功能

            ```SQL
            SET CLUSTER SETTING ts.wal.flush_interval = -1s;
            ```

        2. 重启 KWDB 服务。

            ```shell
            systemctl restart kaiwudb
            ```

    3. 调整 KaiwuDB DataX Utils 配置文件中的相关参数。

        - `splitIntervalS`：数据读取时间间隔。建议根据时间间隔内的数据量大小进行调整，默认值为 60，即 60 秒。该参数只适用于 InfluxDB。
        - `batchsize`：批量写入数据的条数。建议根据业务实际数据量进行调整。
        - `channel`：数据传输的并发数。建议根据机器性能进行配置。

        配置示例：

        ```yaml{13,24,27}
        source:
          pluginName: influxdb20reader
          databases:
            - name: db_example
              url: db_url
              username: user_example
              password: password_example
              tables:
                - name: 4301
                  column: _time,factorValue,factorCode
                  beginDateTime: "2024-04-07 08:00:00"
                  endDateTime: "2024-07-16 08:00:05"
                  splitIntervalS: 600
        target:
          pluginName: kaiwudbwriter
          databases:
            - name: tsdb
              url: jdbc_url
              username: user_example
              password: password_example
              tables:
                - name: xmtest
                  column: ts,factorvalue,factorcode
          batchSize: 5000
        setting:
          speed:
            channel: 5
          errorLimit:
            percentage: 0.02
        ```

    4. 在 KaiwuDB DataX Utils 所在目录，执行数据迁移命令时，设置 JVM 参数，增加内存。

        ```shell
        java -jar -DyamlPath=<yml_path> -DdataxPath=<datax_path> -Dpython=<python>  -Darguments="$bin_path --jvm=\"-Xms2G -Xmx4G\"" kaiwudb-datax-utils-2.0.3.jar
        ```

## 产品生态 FAQ

### MyBatis

- **问题描述**

    通过 Spring + MyBatis 将 `BigInteger` 类型的数据插入时序表的 `INT8` 列时，返回 `unsupported input type *tree.DDecimal` 错误。

- **问题解答**

    使用 JDBC 写入数据时，Java 中定义的 `BigInteger` 类型的数据会被处理为 `BigDecimal` 类型。在 KWDB 数据库中，`BigDecimal` 对应的数据类型为 `DECIMAL` 和 `NUMERIC`。时序表不支持 `DECIMAL` 和 `NUMERIC` 数据类型，因此系统报错。为避免上述错误，建议将 Java 中的数据类型修改为 `Integer`。
