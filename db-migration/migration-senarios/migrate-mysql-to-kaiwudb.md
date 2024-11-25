---
title: 从 MySQL 迁移到 KWDB
id: migrate-mysql-to-kaiwudb
---
# 从 MySQL 迁移到 KWDB

KWDB 支持以单表、多表、单库、多库的形式将数据从 MySQL 迁移到 KWDB。本文档提供单表迁移、单库迁移和多库迁移的配置示例。有关多表迁移的配置示例，参见[从 TDengine 迁移到 KWDB](./migrate-tdengine-to-kaiwudb.md)。

## 单表迁移

### 前提条件

- 完成[迁移准备](../before-migration.md)。
- 在 MySQL 数据库中创建 `sensor_data_db` 数据库和 `sensor_data` 表。
- 在 KWDB 数据库中创建 `tsdb` 时序数据库。

::: warning 说明
从关系表向时序表迁移时，需要配置合适的列或者常量作为时序表的标签和主标签。
:::

### 步骤

1. 解压缩 KaiwuDB DataX 插件包，将解压后的 Reader 和 Writer 插件复制到 DataX 对应的插件目录下。例如，复制 `kaiwudbwriter` 到 `datax/plugin/writer` 目录。
2. 创建配置文件（`.yml`），配置源数据库和目标数据库的连接信息、数据表信息、迁移设置、核心信息参数。有关源数据库、目标数据库、迁移设置、核心信息的配置参数，参见[配置参数](../config-params.md)。

    以下配置文件使用 `where` 参数读取 `2024-01-01 00:00:00` 到 `2024-02-01 00:00:00` 期间的数据，并使用 `preSql` 参数在目标数据库中创建待写入数据的 `sensor_data` 时序表。

    ```yaml ts{11,22-23}
    source:
      pluginName: mysqlreader
      databases:
        - name: sensor_data_db
          url: jdbc:mysql://127.0.0.1:3306/sensor_data_db?useSSL=false&useUnicode=true&characterEncoding=utf8
          username: <user_name>
          password: <password>
          tables:
            - name: sensor_data
              column: timestamp, sensor_id, temperature, humidity, 1 as tag1
              where: timestamp >= '2024-01-01 00:00:00' and timestamp <= '2024-02-01 00:00:00'
    target:
      pluginName: kaiwudbwriter
      databases:
        - name: tsdb
          url: jdbc:kaiwudb://127.0.0.1:26257/tsdb
          username: <user_name>
          password: <password>
          tables:
            - name: sensor_data
              column: time, sensor_id, temperature, humidity, tag1
              preSql:
                - "create table sensor_data (time TIMESTAMPTZ NOT NULL, sensor_id INT, temperature FLOAT, humidity FLOAT) tags (tag1 int not null) primary tags (tag1))"
      batchSize: 1000
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
    java -jar -Dtype=data -DyamlPath=<yml_path> -DdataxPath=<datax_path> -Dpython=<python> -Darguments=<arguments> kaiwudb-datax-utils-1.2.3.jar
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

## 单库迁移

### 前提条件

- 完成[迁移准备](../before-migration.md)。
- 在 MySQL 数据库中创建 `metrics_db` 数据库和 `sensor_metrics`、`system_metrics` 表。
- 在 KWDB 数据库中创建 `metrics` 关系数据库和 `sensor_metrics`、`system_metrics` 关系表。

### 步骤

1. 解压缩 KaiwuDB DataX 插件包，将解压后的 Reader 和 Writer 插件复制到 DataX 对应的插件目录下。例如，复制 `kaiwudbwriter` 到 `datax/plugin/writer` 目录。
2. 创建配置文件（`.yml`），配置源数据库和目标数据库的连接信息以及迁移设置参数。有关源数据库、目标数据库、迁移设置的配置参数，参见[配置参数](../config-params.md)。

    ```yaml
    source:
      pluginName: mysqlreader
      databases:
        - name: metrics_db
          url: jdbc:mysql://127.0.0.1:3306/metrics_db?useSSL=false&useUnicode=true&characterEncoding=utf8
          username: <user_name>
          password: <password>
    target:
      pluginName: kaiwudbwriter
      databases:
        - name: metrics
          url: jdbc:kaiwudb://127.0.0.1:26257/metrics
          username: <user_name>
          password: <password>
      batchSize: 1000
    setting:
      speed:
        channel: 1
      errorLimit:
        percentage: 0.02
    ```

3. 在 KaiwuDB DataX Utils 的 JAR 文件所在目录，执行以下命令，开始迁移数据。

    ```shell
    java -jar -Dtype=data -DyamlPath=<yml_path> -DdataxPath=<datax_path> -Dpython=<python> -Darguments=<arguments> kaiwudb-datax-utils-1.2.3.jar
    ```

## 多库迁移

### 前提条件

- 完成[迁移准备](../before-migration.md)。
- 在 MySQL 数据库中创建 `production_db` 和 `analytics_db` 数据库，以及对应的关系表。
- 在 KWDB 数据库中创建 `production_data` 和 `analytics_data` 关系数据库，以及对应的关系表。

### 步骤

1. 解压缩 KaiwuDB DataX 插件包，将解压后的 Reader 和 Writer 插件复制到 DataX 对应的插件目录下。例如，复制 `kaiwudbwriter` 到 `datax/plugin/writer` 目录。
2. 创建配置文件（`.yml`），配置源数据库和目标数据库的连接信息以及迁移设置参数。有关源数据库、目标数据库、迁移设置的配置参数，参见[配置参数](../config-params.md)。

    ```yaml
    source:
      pluginName: mysqlreader
      databases:
        - name: production_db
          url: jdbc:mysql://127.0.0.1:3306/production_db?useSSL=false&useUnicode=true&characterEncoding=utf8
          username: <user_name>
          password: <password>
        - name: analytics_db
          url: jdbc:mysql://127.0.0.1:3306/analytics_db?useSSL=false&useUnicode=true&characterEncoding=utf8
          username: <user_name>
          password: <password>
    target:
      pluginName: kaiwudbwriter
      databases:
        - name: production_data
          url: jdbc:kaiwudb://127.0.0.1:26257/production_data
          username: <user_name>
          password: <password>
        - name: analytics_data
          url: jdbc:kaiwudb://127.0.0.1:26257/analytics_data
          username: <user_name>
          password: <password>
      batchSize: 1000
    setting:
      speed:
        channel: 1
      errorLimit:
        percentage: 0.02
    ```

3. 在 KaiwuDB DataX Utils 的 JAR 文件所在目录，执行以下命令，开始迁移数据。

    ```shell
    java -jar -Dtype=data -DyamlPath=<yml_path> -DdataxPath=<datax_path> -Dpython=<python> -Darguments=<arguments> kaiwudb-datax-utils-1.2.3.jar
    ```
