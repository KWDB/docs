---
title: 故障排查
id: db-operation-troubleshooting
---

# 故障排查

KWDB 提供日志、监控方案、核心转储功能，用于收集问题诊断数据，定位和分析问题。

- 日志：KWDB 支持通过日志记录各模块程序的运行状态，并将日志输出到日志文件。
- 监控：KWDB 支持使用 [Prometheus](https://prometheus.io/) 和 [Grafana](https://grafana.com/grafana) 查看集群节点状态、监控集群指标。更多详细信息，参见[集群监控](./cluster-monitoring/monitor-cluster-overview.md)。
- 核心转储功能：在某些情况下，KWDB 可能会因为严重的错误而崩溃或终止运行。如果开启核心转储功能，当进程发生严重错误时，系统生成 core 文件，用于诊断问题，找到解决方法。KWDB 支持在启动脚本、执行会话或者在系统层面配置 `ulimit`，开启核心转储功能。

    配置示例：

    ```shell
    ulimit -c
    echo '{KWDB_CORE_PATH}/core.%e.%p' > /proc/sys/kernel/core_pattern
    ```

    ::: warning 注意
    一般情况下，core 文件较大。建议将其存储到单独的硬盘分区。

    :::

## 功能问题

查询数据时，如果系统返回错误结果或者某个功能无法正常工作，用户可以通过错误码、日志和监控信息来定位和分析问题。

1. 查阅[错误码](./error-code/error-code-overview.md)参考手册，根据建议措施尝试解决问题。

2. 进入用户数据目录下的 `log` 子目录，查看已有日志信息，汇总问题发生的时间、背景信息及错误信息。

3. 通过 Grafana，查看 KWDB 集群及各个节点的监控指标。更多详细信息，参见[查看数据指标](./cluster-monitoring/view-metrics.md)。

4. 如果仍无法定位或解决问题，[联系](https://cs.kaiwudb.com/support/) KWDB 技术支持人员并提供详细的错误日志和问题报告来定位和解决问题。

## 性能问题

如果 KWDB 系统响应时间变慢，性能下降，可以通过 Grafana 监控系统和日志，找出性能瓶颈。

1. 通过 Grafana [概览指标模板](./cluster-monitoring/view-metrics.md#概览)确认网络有无问题。

2. 通过 Grafana [硬件指标模板](./cluster-monitoring/view-metrics.md#硬件)查看 CPU 使用率、内存使用率以及已用空间和可用空间有无告警。

3. 如果仍无法定位或解决问题，[联系](https://cs.kaiwudb.com/support/) KWDB 技术支持人员并提供详细的性能报告来定位和解决问题。

## 稳定性问题

如果 KWDB 系统出现系统崩溃、服务中断等稳定性问题，可以通过 Grafana 监控系统、日志、 core 文件来定位和分析问题。

1. 通过 Grafana 各指标模板查看 CPU、内存、磁盘 I/O、网络流量等，定位可能导致系统不稳定的因素。

2. 查看故障日志中的 `call stack` 信息和 `core` 文件，收集系统崩溃的时间、范围、持续时间等信息。

    ::: warning 注意
    默认情况下，禁用核心转储功能。用户可以在启动脚本、执行会话或者在系统层面配置 `ulimit` 或者编辑 `ulimit` 配置文件，开启核心转储功能。
    :::

3. 如果仍无法定位或解决问题，[联系](https://cs.kaiwudb.com/support/) KWDB 技术支持人员并提供详细的系统状态数据和日志文件来定位和解决问题。
