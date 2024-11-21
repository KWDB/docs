---
title: hsweb_r2dbc
id: connect-hsweb-r2dbc
---

# 使用 hsweb_r2dbc 连接 KWDB

hsweb 是基于 Spring Boot 2.x 开发的企业级后台管理系统基础项目。

KWDB 支持用户通过 hsweb_r2dbc 连接数据库，并执行创建、插入和查询操作。本示例演示了如何通过 hsweb_r2dbc 连接和使用 KWDB。

## 前提条件

- [安装 openJDK](https://openjdk.org/install/)（1.8 及以上版本）。
- [安装 Maven](https://maven.apache.org/install.html)（3.6 及以上版本）。
- 安装 KWDB 数据库、配置数据库认证方式、创建数据库。
- 创建具有表级别及以上操作权限的用户。
- 获取 KaiwuDB JDBC 驱动包。

## 配置示例

1. 下载 hsweb R2DBC 相关代码。

2. 编译项目。

    ```bash
    cd ./java/hsweb_r2dbc
    mvn clean package -Dmaven.test.skip=true
    ```

3. 创建目录并复制文件：

    ```bash
    mkdir /opt/hsweb_r2dbc
    cp target/hsweb_r2dbc-1.0.0.jar target/classes/application.yml /opt/hsweb_r2dbc/
    ```

4. 修改 `application.yml` 文件中的数据源连接方式。

    ```yml
    spring:
    application:
        name: hsweb_r2dbc
    r2dbc:
        primary:
        url: r2dbc:postgresql://localhost:26257/defaultdb
        username: kaiwudb
        password: <password>
        secondary:
        url: r2dbc:postgresql://localhost:26257/benchmark
        username: kaiwudb
        password: <password>

    easyorm:
    dialect: postgres
    auto-ddl: false
    allow-alter: false
    default-schema: public
    dialect-type: org.hswebframework.ezorm.rdb.supports.postgres.PostgresqlDialect

    logging:
    level:
        org:
        hswebframework: debug

    server:
    port: 8090
    ```

5. 进入 `hsweb_r2dbc` 目录并创建日志目录：

    ```bash
    cd /opt/hsweb_r2dbc
    mkdir logs
    ```

6. 启动应用：

    ```bash
    nohup java -jar /opt/hsweb_r2dbc/hsweb_r2dbc-1.0.0.jar --spring.config.location=/opt/hsweb_r2dbc/application.yml > /opt/hsweb_r2dbc/logs/output.log 2>&1 &
    ```

7. 在 `/opt/hsweb_r2dbc/` 目录执行数据写入、查询和删除操作，验证配置：
    以下示例假设已创建名为 `hsweb_r2dbc` 的时序库，名为 `cpu` 的时序表，并向表内写入数据。

    ```sql
    CREATE TS DATABASE hsweb_r2dbc;

    CREATE TABLE hsweb_r2dbc.cpu (
        k_timestamp TIMESTAMPTZ NOT NULL,
        usage_user INT8 NOT NULL,
        usage_system INT8 NOT NULL,
        usage_idle INT8 NOT NULL,
        usage_nice INT8 NOT NULL,
        usage_iowait INT8 NOT NULL,
        usage_irq INT8 NOT NULL,
        usage_softirq INT8 NOT NULL,
        usage_steal INT8 NOT NULL,
        usage_guest INT8 NOT NULL
    ) TAGS (
        ptag INT4 NOT NULL,
        region INT4 NOT NULL,
        datacenter INT4 NOT NULL,
        rack VARCHAR(1024),
        os VARCHAR(1024),
        arch VARCHAR(1024),
        team VARCHAR(1024),
        service VARCHAR(1024)
    ) PRIMARY TAGS (ptag);

    INSERT INTO hsweb_r2dbc.cpu (k_timestamp, usage_user, usage_system, usage_idle, usage_nice,
        usage_iowait, usage_irq, usage_softirq, usage_steal, usage_guest, ptag, region, datacenter,
        rack, os, arch, team, service)
    VALUES
        ('2024-01-21 22:22:22.221', 1, 2, 3, 4, 5, 6, 7, 8, 1, 1, 1, 1, '2', '2', '2', '2', '2'),
        ('2024-01-22 22:22:22.221', 1, 2, 3, 4, 5, 6, 7, 8, 1, 1, 1, 1, '2', '2', '2', '2', '2'),
        ('2024-01-23 22:22:22.221', 1, 2, 3, 4, 5, 6, 7, 8, 1, 1, 1, 1, '2', '2', '2', '2', '2');
    ```

    - 使用 curl 查询数据：

        ```bash
        curl -X GET -H  "Accept:*/*" -H  "Content-Type:application/x-www-form-urlencoded" "http://localhost:8090/hsweb_r2dbc/cpus/1?end=1706106142221&start=1705760542221"
        ```

    - 使用 curl 写入数据：

        ```bash
        curl -X POST -H  "Accept:*/*" -H  "Content-Type:application/json" -d "{\"arch\":\"\",\"dataCenter\":2,\"id\":2,\"os\":\"\",\"rack\":\"\",\"region\":2,\"service\":\"\",\"team\":\"\",\"time\":1722579427867,\"usageGuest\":1,\"usageIdle\":1,\"usageIoWait\":1,\"usageIrq\":1,\"usageNice\":1,\"usageSoftIrq\":1,\"usageSteal\":1,\"usageSystem\":1,\"usageUser\":1}" "http://localhost:8090/hsweb_r2dbc/cpu"

        ```

    - 使用 curl 删除数据：

        ```bash
        curl -X POST -H  "Accept:*/*" -H  "Content-Type:application/json" -d "{\"id\":1,\"time\":1722579427867}" "http://localhost:8090/hsweb_r2dbc/cpu/delete"

        ```