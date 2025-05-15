---
title: 常见问题解答（FAQ）
id: faqs
---

# 常见问题解答（FAQ）

## 安装部署 FAQ

### 依赖缺失

- **问题描述**

    安装 KWDB 时，系统提示安装失败。

- **问题解答**

    用户可能未安装所需依赖。建议查看 `kaiwudb_install/log` 目录下的相关日志，然后根据日志信息，使用 `apt install` 命令安装缺失的依赖。

    日志示例：

    ```shell
    root@node:/home/admin/kaiwudb_install/log# cat 2024-08-28
    [INFO] 2024-08-28 09:35:57 start init directory /etc/kaiwudb/data/kaiwudb
    [INFO] 2024-08-28 09:35:57 init directory success
    [INFO] 2024-08-28 09:35:57 start install binaries and libraries to /usr/local/kaiwudb
    [ERROR] 2024-08-28 09:35:57 error: Failed dependencies: squashfs-tools is needed by kaiwudb-server-2.0.3.2-kylin.kyl0.aarch64
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

## 产品生态 FAQ

### MyBatis

- **问题描述**

    通过 Spring + MyBatis 将 `BigInteger` 类型的数据插入时序表的 `INT8` 列时，返回 `unsupported input type *tree.DDecimal` 错误。

- **问题解答**

    使用 JDBC 写入数据时，Java 中定义的 `BigInteger` 类型的数据会被处理为 `BigDecimal` 类型。在 KWDB 数据库中，`BigDecimal` 对应的数据类型为 `DECIMAL` 和 `NUMERIC`。时序表不支持 `DECIMAL` 和 `NUMERIC` 数据类型，因此系统报错。为避免上述错误，建议将 Java 中的数据类型修改为 `Integer`。
