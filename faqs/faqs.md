---
title: 常见问题解答（FAQ）
id: faqs
---

# 常见问题解答（FAQ）

## 安装部署 FAQ

### 操作系统适配

- **问题描述**

  用户希望在龙芯 3C5000L 或兆芯 KH-30000 操作系统上部署 KWDB。

- **问题解答**

  目前，KWDB 尚未在龙芯 3C5000L 和兆芯 KH-30000 操作系统系统进行全面、系统化的验证，用户如果有相关需求，请[联系](https://www.kaiwudb.com/support/) KWDB 技术支持人员，我们将提供编译适配和测试支持。

### 依赖缺失

- **问题描述**

    安装 KWDB 时，系统提示安装失败。

- **问题解答**

    用户可能未安装所需依赖。建议查看 `kwdb_install/log` 目录下的相关日志，然后根据日志信息，使用 `apt install` 命令安装缺失的依赖。

    日志示例：

    ```shell
    root@node:/home/admin/kwdb_install/log# cat 2024-08-28
    [INFO] 2024-08-28 09:35:57 start init directory /etc/kaiwudb/data/kaiwudb
    [INFO] 2024-08-28 09:35:57 init directory success
    [INFO] 2024-08-28 09:35:57 start install binaries and libraries to /usr/local/kaiwudb
    [ERROR] 2024-08-28 09:35:57 error: Failed dependencies: squashfs-tools is needed by kaiwudb-server-2.0.3.2-kylin.kyl0.aarch64
    ```

## 存储 FAQ

### 删表后存储空间未释放

- **问题描述**

    删除表后，发现存储空间没有立即释放。

- **问题解答**

    在 KWDB 中，执行删除表操作后，如果有其他线程仍在使用该表，系统不会立即删除表，而会等待所有线程完成对该表的操作后再删除。系统会每 5 分钟检查一次是否可以删除该表。在异常情况下，如果有线程长时间持有该表，可能会导致存储空间无法释放。此时，建议手动删除相关数据以释放存储空间。

## SQL FAQ

### 数据写入

#### 空间不足

- **问题描述**

    向数据库写入数据时写入失败，错误提示为 `could not PutData`，日志中显示 `resize file failed` 和 `No space left on device`。

- **问题解答**

    可能是因为待写入的列数过多，达到句柄上限，可以通过增加文件描述符上限来解决这个问题。

    ::: warning 注意

  - 该设置只适用于裸机部署。
  - 该配置为节点级别，如果需要修改整个集群的配置，需要登录到集群的每个节点并完成相应的配置。
    :::

    **步骤：**

    1. 进入 `/etc/systemd/system` 目录，打开 `kaiwudb.service` 文件。

    2. 在 `[Service]` 部分添加 `LimitNOFILE=1048576`，增加单个进程能够打开的最大文件描述符数量。

        ```YAML
        ...
        [Service]
        ...
        LimitNOFILE=1048576
        ...
        ```

    3. 保存 `kaiwudb.service` 文件后，重新加载配置。

          ```Shell
          systemctl daemon-reload
          ```

    4. 检查修改是否生效：

          ```Shell
          systemctl show kaiwudb | grep LimitNOFILE
          ```

#### 建表报错

- **问题描述**

    在 CentOS 操作系统的容器环境下安装 KWDB 后，用户可以创建时序数据库，但是创建时序表时报错 `Error: have been trying 30s, timed out of AdminReplicaVoterStatusConsistent`。查看日志，系统提示 `Err :connection error: desc = "transport: Error while dialing dial tcp 100.153.0.246:26257: connect: connection refused`。

- **问题解答**

    可能是因为容器无法访问宿主机的 IP 地址，导致建表时报错。建议修改防火墙配置，允许容器网段访问宿主机。

    配置示例：

    ```shell
    firewall-cmd --zone=public --add-rich-rule='rule family="ipv4" source address="172.18.0.4/24" port protocol="tcp" port="22" accept' --permanent
    ```

#### 多行写入失败

- **问题描述**

  使用 JDBC 和 PREPARE INSERT 语句向一个包括几千列的表写入数据时，批量写入 10 行数据可以成功，批量写入 20 行数据出错。

- **问题解答**

  可能是批量写入的 SQL 语句长度超过了 PostgreSQL 协议规定的长度上限。建议通过以下方式解决：

  - **减少 SQL 语句长度**：尝试减少单次批量写入的行数或列数。
  - **避免使用 PREPARE 语句**：直接执行 INSERT 语句而不使用预编译的 PREPARE 语句。

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

    KWDB 对关系数据和时序数据执行时间加减运算时，如果运算符两边均为 timestamp 或 timestamptz 类型，只支持减法运算，且差值对应的纳秒数不得超过 INT64 范围，对应的天数不得超过 `106751` 天。如果超过该范围，关系数据的计算结果将统一显示为 `106751 days 23:47:16.854776`，时序数据的计算结果取决于实际处理引擎，可能是正确的结果，也可能为 `106751 days 23:47:16.854776`。

#### 内存不足

- **问题描述**

  在单机部署的 KWDB 上执行海量数据的复杂排序查询时，提示内存不足（Insufficient memory）。

- **问题解答**

  可能是排序算子在特定场景下内存占用过多，导致内存池耗尽后报错，可以通过设置启动参数`buffer-pool-size`，增大 buffer pool 的大小来解决内存不足报错的问题。

  **裸机部署：**

  1. 停止 KWDB 服务。

     ```SQL
     systemctl stop kaiwudb
     ```

  2. 进入 `/etc/kaiwudb/script` 目录，打开 `kaiwudb_env` 文件，添加启动参数 `buffer-pool-size`。

     ```YAML
     KAIWUDB_START_ARG="--buffer-pool-size=32657"
     ```

  3. 保存 `kaiwudb_env` 文件并重新加载文件。

     ```Bash
     systemctl daemon-reload
     ```

  4. 重新启动 KWDB 服务。

     ```SQL
     systemctl restart kaiwudb
     ```

  **容器部署：**

  1. 进入 `/etc/kaiwudb/script` 目录，停止并删除 KWDB 容器。

     ```Bash
     docker-compose down
     ```

  2. 打开 `docker-compose.yml` 文件，添加启动参数 `buffer-pool-size`。

     ```YAML
     ...
         command: 
           - /bin/bash- -c- |
             /kaiwudb/bin/kwbase  start-single-node --certs-dir=/kaiwudb/certs --listen-addr=0.0.0.0:26257 --advertise-addr=your-host-ip:port --store=/kaiwudb/deploy/kaiwudb-container --buffer-pool-size=32657
     ```

  3. 保存配置，重新创建并启动 KWDB 容器。

     ```Bash
     systemctl start kaiwudb
     ```


## 性能调优

### 写入调优

#### 海量数据写入调优

- **问题描述**

  使用 SQL 语句向 KWDB 写入海量数据时，写入速率较慢。

- **问题解答**

  可以根据实际业务场景调整部分参数设置或关闭部分可能影响性能的功能，来提升数据写入速度：

  1. 提高处理器可用内存上限，减少对临时存储的依赖。默认值为 64 MiB，建议设置为物理内存的 1/8，以提高处理效率。

      示例：

        ```SQL
        SET CLUSTER SETTING sql.distsql.temp_storage.workmem = '32768Mib';
        ```

  2. 启用 SQL 下推功能，减少数据处理的开销。

       ```SQL
        SET CLUSTER SETTING sql.all_push_down.enabled = TRUE;
       ```

  3. 打开短路优化，减少不必要的操作步骤。

      ```SQL
        SET CLUSTER SETTING sql.pg_encode_short_circuit.enabled = TRUE;
      ```

  4. 关闭自动统计时序数据信息收集功能。注意：关闭此功能后将无法查看监控数据，适用于对性能要求较高且对监控数据依赖较低的场景。

        ```SQL
        SET CLUSTER SETTING sql.stats.ts_automatic_collection.enabled = FALSE;
        ```

  5. 关闭数据压缩功能，减少写入时的计算开销，适用于对空间占用不敏感的场景。

        ```SQL
        ALTER SCHEDULE scheduled_table_compress F Recurring '0 0 1 1 ？2099';
        ```

  6. 关闭生命周期管理功能，避免定期的表清理操作，适用于数据持久性要求较高且对写入性能要求较高的场景。

        ```SQL
        ALTER SCHEDULE scheduled_table_retention Recurring '0 0 1 1 ? 2099';
        ```

  7. 关闭 WAL 日志功能。注意：关闭 WAL 日志功能会影响宕机后的数据恢复，适用于对数据一致性要求较低的场景。

     1. 关闭 WAL 日志功能。

           ```SQL
           SET CLUSTER SETTING ts.wal.flush_interval = -1s;
           ```

     2. 重启 KWDB 服务。

           ```Bash
           systemctl restart kaiwudb
           ```

#### 超大宽表写入调优

- **问题描述**

  向超大宽表，即列字段大于 500 的表，每次批量写入 500 条以上数据或单次写入数据量大于 4M，写入性能较差。

- **问题解答**

  可以在集群中的每个节点配置 `KWBASE_RAFT_ELECTION_TIMEOUT_TICKS` 环境变量，具体步骤如下：

  **裸机部署：**

  1. 停止 KWDB 服务。

     ```Shell
     systemctl stop kaiwudb
     ```

  2. 进入 `/etc/kaiwudb/script` 目录，编辑 `kaiwudb_env` 配置文件，添加 `KWBASE_RAFT_ELECTION_TIMEOUT_TICKS` 环境变量。

     ```Plain
     KAIWUDB_START_ARG=""
     KWBASE_RAFT_ELECTION_TIMEOUT_TICKS=100
     ```

  3. 保存文件并重新加载。

     ```Shell
     systemctl daemon-reload
     ```

  4. 重启 KWDB 服务。

     ```Shell
     systemctl restart kaiwudb
     ```

  **容器部署：**

  1. 在 `/etc/kaiwudb/script` 目录停止并删除 KWDB 容器。

     ```Shell
     docker-compose down
     ```

  2. 打开 `docker-compose.yml` 文件，添加 `KWBASE_RAFT_ELECTION_TIMEOUT_TICKS` 环境变量。

     ```Plain
     ...
         environment:
           - LD_LIBRARY_PATH=/kaiwudb/lib
           - KWBASE_RAFT_ELECTION_TIMEOUT_TICKS=100
     ...
     ```

  3. 保存配置，重新创建和启动 KWDB 容器。

     ```Shell
     systemctl start kaiwudb
     ```


### 查询调优

- **问题描述**

  使用 SQL 语句获取某个时序表的所有标签值，查询速率较慢。

- **问题解答**

  可以通过以下 SQL 语句向数据库查询优化器提供特定指令，优化查询性能：

  ```SQL
  SELECT /*+ STMT_HINT(ACCESS_HINT(TAG_ONLY,<table_name>)) */ <tag_name> FROM <table_name> GROUP BY <tag_name>;
  ```

  参数说明：

  - `/*+ STMT_HINT(ACCESS_HINT(TAG_ONLY, <table_name>)) */`： 给优化器提供查询优化建议，具体参数如下：
    - `ACCESS_HINT`： 表的访问方式。
    - `TAG_ONLY`： 只查询标签数据。
    - `table_name`： 目标表的名称。
  - `tag_name`：目标标签的名称。

  示例：

  ```SQL
  > SELECT /*+ STMT_HINT(ACCESS_HINT(TAG_ONLY,t1)) */ tag1 FROM t1 GROUP BY tag1;
    tag1
  ------
     3
     1
     2
     5
     6
     4
  (6 rows)
  ```

## 数据迁移 FAQ

- **问题描述**

    使用 KaiwuDB DataX Utils 从 InfluxDB 向 KWDB 写入数据时，写入速率较慢。

- **问题解答**

    数据的实际写入速率与数据特性、硬件规格相关。用户可以采取以下步骤，调整相关参数配置，提升写入速率。

    1. （可选）关闭 WAL 日志实时写入功能。

        1. 关闭 WAL 日志写入功能

            ```SQL
            SET CLUSTER SETTING ts.wal.flush_interval = -1s;
            ```

        2. 重启 KWDB 服务。

            ```shell
            systemctl restart kaiwudb
            ```

    2. 调整 KaiwuDB DataX Utils 配置文件中的相关参数。

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

    3. 在 KaiwuDB DataX Utils 所在目录，执行数据迁移命令时，设置 JVM 参数，增加内存。

        ```shell
        java -jar -Dtype=data -DyamlPath=<yml_path> -DdataxPath=<datax_path> -Dpython=<python>  -Darguments="--jvm=\"-Xms2G -Xmx4G\"" kaiwudb-datax-utils-1.2.3.jar
        ```

## 产品生态 FAQ

### MyBatis 和 MyBatis-Plus

#### `BigInteger` 类型写入失败

- **问题描述**

    通过 Spring + MyBatis 将 `BigInteger` 类型的数据插入时序表的 `INT8` 列时，返回 `unsupported input type *tree.DDecimal` 错误。

- **问题解答**

    使用 JDBC 写入数据时，Java 中定义的 `BigInteger` 类型的数据会被处理为 `BigDecimal` 类型。在 KWDB 数据库中，`BigDecimal` 对应的数据类型为 `DECIMAL` 和 `NUMERIC`。时序表不支持 `DECIMAL` 和 `NUMERIC` 数据类型，因此系统报错。为避免上述错误，建议将 Java 中的数据类型修改为 `Integer`。

#### `NCHAR` 类型查询报错

- **问题描述**

  通过 Spring + MyBatis 查询 NCHAR 列，会返回 `SQLSTATE(0A000)` 错误，提示 `getNString` 方法未实现。

- **问题解答**

  JDBC 2.0.3 版本不支持 `getNString` 方法，导致在查询 NCHAR 列时出现错误，建议通过自定义一个 MyBatis 类型处理器改为使用 `getString` 获取数据或升级到 JDBC 2.0.4 版本以解决该问题。

#### 分页查询报错

- **问题描述**

  使用 MyBatis-Plus 连接 KWDB，执行分页查询时，收到系统报错：`Error querying database. com.baomidou.mybatisplus.core.exceptions.MybatisPlusException: other database not supported`。

- **问题解答**

  可能是 MyBatis 分页插件在数据库类型校验时出错，建议显式声明 `DbType.POSTGRE_SQL` 的 `InnerInterceptor`。

  具体操作如下：

  1. 在应用代码中创建 MybatisPlus 配置类，比如 `MybatisPlusConfig`。

  2. 添加分页配置。

        ```Bash
        @Configuration
        public class MybatisPlusConfig {
          @Bean
          public MybatisPlusInterceptor mybatisPlusInterceptor() {
            MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
            interceptor.addInnerInterceptor(new PaginationInnerInterceptor(DbType.POSTGRE_SQL));
            return interceptor;
          }
        }
        ```

#### 时序模式不支持事务

- **问题描述**

  使用 Mybatis-Plus 原生接口连接数据库，调用接口方法时，数据库返回时序引擎不支持事务，收到系统报错：`ERROR: explicit transaction is not supported in TS mode`。  

- **问题解答**

  用户需要重写 Mybatis-Plus 的接口方法的实现，使用 `@Transactional(propagation = Propagation.NOT_SUPPORTED)` 注解来禁用该方法的事务管理机制，具体示例如下：

  ```java
  @Service
  public class TimeSeriesServiceImpl extends ServiceImpl<TimeSeriesMapper, TimeSeriesData> implements TimeSeriesService {
    @Override
    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public boolean saveBatch(Collection<TimeSeriesData> entityList) {
      return super.saveBatch(entityList);
    }
  }
  ```