---
title: 故障排查
id: troubleshooting
---

# 故障排查

## KWDB 集群

KWDB 提供日志、监控方案、核心转储功能，用于收集问题诊断数据，定位和分析问题。

- 日志：KWDB 支持通过日志记录各模块程序的运行状态，并将日志输出到日志文件。
- 监控：KWDB 支持使用 Prometheus](https://prometheus.io/) 和 [Grafana](https://grafana.com/grafana) 查看集群节点状态、监控集群指标。更多详细信息，参见[使用 Grafana 查看指标数据](../db-monitor/view-metrics-grafana.md)。
- 核心转储功能：在某些情况下，KWDB 可能会因为严重的错误而崩溃或终止运行。如果开启核心转储功能，当进程发生严重错误时，系统生成 core 文件，用于诊断问题，找到解决方法。KWDB 支持在启动脚本、执行会话或者在系统层面配置 `ulimit`，开启核心转储功能。

    配置示例：

    ```shell
    ulimit -c
    echo '{KWDB_CORE_PATH}/core.%e.%p' > /proc/sys/kernel/core_pattern
    ```

    ::: warning 注意
    一般情况下，core 文件较大。建议将其存储到单独的硬盘分区。

    :::

### 功能问题

查询数据时，如果系统返回错误结果或者某个功能无法正常工作，用户可以通过错误码、日志和监控信息来定位和分析问题。

1. 查阅[错误码](../db-operation/error-code/error-code-overview.md)参考手册，根据建议措施尝试解决问题。

2. 进入用户数据目录下的 `log` 子目录，查看已有日志信息，汇总问题发生的时间、背景信息及错误信息。

3. 通过[Grafana](../db-monitor/os-monitor-component/view-metrics-grafana.md) 查看 KWDB 集群及各个节点的监控指标。

4. 如果仍无法定位或解决问题，[联系](https://cs.kaiwudb.com/support/) KWDB 技术支持人员并提供详细的错误日志和问题报告来定位和解决问题。

### 性能问题

如果 KWDB 系统响应时间变慢，性能下降，可以通过Grafana 监控系统、日志找出性能瓶颈。

1. 通过 [Grafana 概览指标模板](../db-monitor/os-monitor-component/view-metrics-grafana.md#概览)确认网络是否存在问题。

2. 通过 [Grafana 硬件指标模板](../db-monitor/os-monitor-component/view-metrics-grafana.md#硬件)查看 CPU 使用率、内存使用率以及已用空间和可用空间有无告警。

3. 如果仍无法定位或解决问题，[联系](https://cs.kaiwudb.com/support/) KWDB 技术支持人员并提供详细的性能报告来定位和解决问题。

### 稳定性问题

如果 KWDB 系统出现系统崩溃、服务中断等稳定性问题，可以通过 Grafana 监控系统、日志、core 文件来定位和分析问题。

1. 通过 [Grafana](../db-monitor/os-monitor-component/view-metrics-grafana.md) 查看 CPU、内存、磁盘 I/O、网络流量等，定位可能导致系统不稳定的因素。

2. 查看故障日志中的 `call stack` 信息和 `core` 文件，收集系统崩溃的时间、范围、持续时间等信息。

    ::: warning 注意
    默认情况下，禁用核心转储功能。用户可以在启动脚本、执行会话或者在系统层面配置 `ulimit` 或者编辑 `ulimit` 配置文件，开启核心转储功能。
    :::

3. 如果仍无法定位或解决问题，[联系](https://cs.kaiwudb.com/support/) KWDB 技术支持人员并提供详细的系统状态数据和日志文件来定位和解决问题。

## 应用开发

### KaiwuDB JDBC

KWDB 支持使用日志记录功能来帮助解决 KaiwuDB JDBC 驱动程序在应用程序使用时遇到的问题。KaiwuDB JDBC 驱动程序使用 `java.util.logging` 日志 API，其根记录器是 `com.kaiwudb`。

用户可以采用以下任一方式开启日志：

- 使用连接属性启动日志
- 使用 `logging.properties` 文件开启日志

#### 使用连接属性启动日志

KaiwuDB JDBC 驱动程序支持使用连接属性启用日志记录。连接属性使用 `loggerLevel` 和 `loggerFile` 参数定义日志的级别和输出文件名。

```shell
jdbc:kaiwudb://127.0.0.1:26257/defaultdb?loggerLevel=DEBUG     //只配置loggerLevel
jdbc:kaiwudb://127.0.0.1:26257/defaultdb?loggerLevel=Trace&loggerFile=kaiwudb-jdbc.log  //同时配置loggerLevel和loggerFile
```

参数说明：

- **loggerLevel**：驱动程序的级别，支持 `OFF`、`DEBUG` 和 `TRACE` 取值。这些值与 `java.util.logging.Logger` 的等级对应关系如下：

  | LoggerLevel | java.util.logging | 描述              |
  | ----------- | ----------------- | ------------------------------------------------ |
  | OFF         | OFF               | 不启用日志。                                     |
  | DEBUG       | FINE              | 一般的消息跟踪。                                 |
  | TRACE       | FINEST            | 非常详细的跟踪，包括调试问题所需的所有详细信息。 |

- **loggerFile**：Logger 的输出文件名。
  - 如果指定输出文件名，Logger 使用 `java.util.logging.Filehandler` 将日志写入指定的文件。
  - 如未指定输出文件名，或者 `java.util.logging.Filehandler` 参数无法创建文件，则使用 `java.util.logging.Consolehandler` 输出日志。`java.util.logging.Consolehandler`参数需要与 `loggerLevel` 一起使用。

#### 使用 logging.properties 文件开启日志

默认情况下，Java 日志框架将其日志配置存储到一个名为 `logging.properties` 的文件中。用户可以在 Java 安装目录的 `lib` 文件夹中安装全局配置文件。

`logging.properties` 文件日志设置的示例如下：

```java
// 指定处理程序，处理程勋在 VM 启动时安装
handlers= java.util.logging.Filehandler

// 默认的全局日志级别
.level = OFF

// 默认文件输出在用户的主目录中
java.util.logging.Filehandler.pattern = %h/kaiwudb-jdbc%u.log
java.util.logging.Filehandler.limit = 5000000
java.util.logging.Filehandler.count = 20
java.util.logging.Filehandler.formatter = java.util.logging.SimpleFormatter
java.util.logging.Filehandler.level =FINEST
java.util.logging.SimpleFormatter.format = %1$tY-%1$tm-%1$td %1$tH:%1$tM:%1$tS %4$s %2$s %5$s%6$s%n

// 特性属性
com.kaiwudb.level=FINEST
```

用户也可以在启动 Java 程序时，通过配置 `java.util.logging.config.file` 参数来使用单独的日志配置文件。

```java
java -jar -Djava.util.logging.config.file=logging.properties run.jar
```

## 数据读取

### Kafka Connect

当 Kafka Connect 出现故障，无法正常工作时，用户可以从以下方面进行故障排查：

- 查看 Kafka Connect 日志文件：默认情况下，Kafka Connect 的日志文件位于 Kafka 安装目录的 `logs` 文件夹下。在该文件夹中，用户找到名为 `connect.log` 的日志文件，查找相关的故障记录。
- 确认连接器配置：通常情况下，连接器的配置文件位于 Kafka Connect 安装目录下的 `config` 文件夹下。主要的连接器配置文件是 `connect-distributed.properties`（分布式模式）或 `connect-standalone.properties`（独立模式）。用户可以打开相应的配置文件，检查各个连接器的配置属性。
- 检查 Kafka 集群状态：用户可以通过访问 Kafka 的 Zookeeper 节点来检查 Kafka 集群状态。连接到 Zookeeper 服务器并使用 Zookeeper 命令行工具，在 Zookeeper 的 shell 提示符下，输入 `ls /brokers/ids` 命令，可以列出所有 Kafka 代理 ID。用户还可以使用 Kafka 的管理工具，如 `kafka-topics.sh` 和 `kafka-consumer-groups.sh` 来验证主题和 Consumer Group 的状态。
- 检查源系统和目标系统：如果问题涉及到特定的源系统或目标系统（如数据库或文件系统），确保这些系统正常运行并且与 Kafka Connect 所在的主机可以正常通信。确认是否正确配置与源系统或目标系统进行连接的参数，如 URL、用户名和密码等。
- 验证数据格式和转换：检查连接器配置文件中的 `key.converter` 和 `value.converter` 属性，确定使用的数据转换器。转换器配置文件位于 Kafka Connect 安装目录下的 `config` 文件夹下。打开相应的转换器配置文件，检查数据转换器配置是否正确，并确保转换器能够处理源数据和目标数据的格式。
- 重启 Kafka Connect 进程：在排除其他问题后，尝试重新启动 Kafka Connect 进程可以解决一些常见问题。停止 Kafka Connect 进程，并使用启动脚本或命令来重新启动。
- 使用 Kafka Connect 工具：
  - `connect-distributed.sh`：运行 `connect-distributed.sh config` 或 `connect-distributed.properties`命令，启动分布式模式的 Kafka Connect，并在日志中查看详细信息。
  - `connector-plugins.sh`：运行 `connector-plugins.sh list` 命令，获取当前已加载的连接器和转换器的信息。
