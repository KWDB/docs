---
title: 从 InfluxDB 迁移到 KWDB
id: migrate-influxdb-to-kaiwudb
---

# 从 InfluxDB 迁移到 KWDB

KWDB 支持以单表、多表的形式将用户数据从 InfluxDB 迁移到 KWDB。本文档提供多表迁移的配置示例。

## 前提条件

- 完成[迁移准备](../before-migration.md)。
- 在 InfluxDB 数据库中已创建待迁移的数据库 `sensor_data` 和数据表 `sensor_tb_2024` 和 `sensor_tb_2023`。
- 在 KWDB 数据库中已创建 `sensor_data` 时序数据库。

## 步骤

1. 解压缩 KaiwuDB DataX 插件包，将解压后的 `kaiwudbwriter` 复制到 `datax/plugin/writer` 目录。
2. 创建 `.yml` 格式的用户数据配置文件，配置源数据库和目标数据库的连接信息、数据表信息、以及迁移设置参数。有关源数据库、目标数据库、迁移设置、核心信息的配置参数，参见[配置参数](../config-params.md)。

    以下配置文件分别使用 `column`、`beginDateTime` 和 `endDateTime` 参数，限定源表的读取数据和时间范围，使用 `preSql` 参数在 KWDB 数据库中创建待写入数据的 `sensor_tb_2024` 和 `sensor_tb_2023` 时序表。

    ```yaml ts{11-20}
    source:
      pluginName: influxdb20reader
      databases:
        - name: sensor_data
          url: http://example_ip:port
          username: user_name
          password: secret_password
          readTimeout: 120
          connectTimeout: 120
          tables:
            - name: sensor_tb_2024
              column: _time,temperature,humidity,pressure,wind_speed,wind_direction,precipitation,t1
              beginDateTime: "2024-01-01 00:00:00"
              endDateTime: "2024-12-31 23:59:59"
              splitIntervalS: 43200
            - name: sensor_tb_2023
              column: _time,temperature,humidity,pressure,wind_speed,wind_direction,precipitation,t1
              beginDateTime: "2023-01-01 00:00:00"
              endDateTime: "2023-12-31 23:59:59"
              splitIntervalS: 86400
    target:
      pluginName: kaiwudbwriter
      databases:
        - name: sensor_data
          url: jdbc:kaiwudb://example_ip:port/sensor_data
          username: user_name
          password: secret_password
          tables:
            - name: sensor_tb_2024
              column: ts,temperature,humidity,pressure,wind_speed,wind_direction,precipitation,t1
              preSql:
                - drop table if exists sensor_tb_2024
                - create table sensor_tb_2024 (ts timestamptz not null, temperature float8, humidity float4, pressure float8, wind_speed float4, wind_direction varchar(20), precipitation float4) tags (t1 varchar not null) primary tags (t1)
            - name: sensor_tb_2023
              column: ts,temperature,humidity,pressure,wind_speed,wind_direction,precipitation,t1
              preSql:
                - drop table if exists sensor_tb_2023
                - create table sensor_tb_2023 (ts timestamptz not null, temperature float8, humidity float4, pressure float8, wind_speed float4, wind_direction varchar(20), precipitation float4) tags (t1 varchar not null) primary tags (t1)
      batchSize: 500
    setting:
      speed:
        channel: 1
      errorLimit:
        percentage: 0.02
    core:
      transport:
        channel:
          speed:
            byte: 1048576
            record: 1000
    ```

3. 在 KaiwuDB DataX Utils 的 JAR 文件所在目录，执行以下命令，开始迁移数据。

    ```shell
    java -jar -Dtype=data -DyamlPath=<yml_path> -DdataxPath=<datax_path> -Dpython=<python> -Darguments=<arguments> kaiwudb-datax-utils-2.1.0.jar
    ```

    参数说明：
    - `yamlPath`：配置文件的路径。
    - `dataxPath`：`DataX` 文件夹的路径。
    - `python`: 已安装的 Python 版本。
      - Python 2.X：`python`
      - Python 3.X：`python3`
    - `arguments`：DataX 环境参数。支持配置以下参数：
      - `-j <jvm paramenters>` 或 `--jvm=<jvm paramenters>`：配置必要的 JVM 参数。
      - `-m <job runtime mode>` 或 `--mode=<job runtime mode>`：配置 DataX 作业运行模式，支持 `standalone`（独立模式）、`local`（本地模式）、`distribute`（分布式模式）。默认为 `standalone`（独立模式）。
