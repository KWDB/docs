---
title: 从 TDengine 迁移到 KWDB
id: migrate-tdengine-to-kaiwudb
---

# 从 TDengine 迁移到 KWDB

KWDB 支持以单表、多表的形式将数据从 TDengine 迁移到 KWDB。本文档提供多表迁移的配置示例。有关单表迁移的配置示例，参见[从 MySQL 迁移到 KWDB](./migrate-mysql-to-kaiwudb.md#单表迁移)。

## 前提条件

- 完成[迁移准备](../before-migration.md)。
- 在 TDengine 数据库中创建 `tdengine_kaiwudb`、`temperature_humidity` 时序数据库和 `custom_metrics` 表。
- 在 KWDB 数据库中创建 `tdengine_kaiwudb` 时序数据库。

## 步骤

1. 解压缩 KaiwuDB DataX 插件包，将解压后的 Reader 和 Writer 插件复制到 DataX 对应的插件目录下。例如，复制 `kaiwudbwriter` 到 `datax/plugin/writer` 目录。
2. 创建配置文件（`.yml`），配置源数据库和目标数据库的连接信息、数据表信息、以及迁移设置参数。有关源数据库、目标数据库、迁移设置、核心信息的配置参数，参见[配置参数](../config-params.md)。

    以下配置文件使用 `column` 和 `querySql` 参数，限定源数据库中表的读取范围，使用 `preSql` 参数在目标数据库中创建待写入数据的 `temperature_humidity` 和 `custom_metrics` 时序表。

    ```yaml ts{10,12-13,24-31}
    source:
      pluginName: tdengine30reader
      databases:
        - name: tdengine_kaiwudb
          url: jdbc:TAOS-RS://127.0.0.1:6041/tdengine_kaiwudb?timestampFormat=STRING&timezone=Asia%2FShanghai
          username: root
          password: taosdata
          tables:
            - name: temperature_humidity
              column: timestamp, sensor_id, temperature, humidity, tag1
            - name: custom_metrics
              querySql:
                - "select timestamp, sensor_id, pressure, voltage, tag1 from custom_metrics"
    target:
      pluginName: kaiwudbwriter
      databases:
        - name: tdengine_kaiwudb
          url: jdbc:kaiwudb://127.0.0.1:26257/tdengine_kaiwudb
          username: kaiwu_user
          password: Password@2024
          tables:
            - name: temperature_humidity
              column: timestamp, sensor_id, temperature, humidity, tag1
              preSql:
                - "drop table if exists temperature_humidity"
                - "create table temperature_humidity (timestamp timestamptz not null, sensor_id int, temperature float, humidity float) tags (tag1 int not null) primary tags (tag1)"
            - name: custom_metrics
              column: timestamp, sensor_id, pressure, voltage, tag1
              preSql:
                - "drop table if exists custom_metrics"
                - "create table custom_metrics (timestamp timestamptz not null, sensor_id int, pressure float, voltage float) tags (tag1 int not null) primary tags (tag1)"
      batchSize: 1000
    setting:
      speed:
        channel: 1
      errorLimit:
        percentage: 0.02
    ```

3. 在 `kaiwudb-datax-utils-1.2.2.jar` 所在目录，执行以下命令，开始迁移数据。

    ```shell
    java -jar -DyamlPath=<yml_path> -DdataxPath=<datax_path> -Dpython=<python> -Darguments=<arguments> kaiwudb-datax-utils-1.2.2.jar
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
