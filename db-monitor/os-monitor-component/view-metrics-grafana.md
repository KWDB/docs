---
title: 查看指标数据
id: view-metrics-grafana
---

# 使用 Grafana 查看指标数据

Grafana 支持查看 KWDB 集群及各个节点的监控指标，包括指标概览、硬件指标、运行指标、SQL 指标、存储指标、副本指标、分布式指标、队列指标和慢查询指标。

## 概览

**概览**页面展示集群和节点的关键指标。

- **SQL Queries**

    ![](../../static/db-monitor/UXH3b1gfsoZhgVxiBFhcHrponpe.png)

    在节点视图中，该时间序列图展示指定节点处理客户端请求的 QPS（Queries Per Second，每秒查询数）。支持的类型包括查询、更新、插入、删除。采样值为 `10` 秒内的平均值。在集群视图中，该时间序列图展示当前集群查询负载的估计值。该估计值为每个节点最近 `10` 秒的活动情况的汇总值。

- **Service Latency: SQL 99th percentile**

    服务延迟是集群从接收到查询请求到查询结束之间的时间，不包含将查询结果传输给客户端的时间。

    ![](../../static/db-monitor/NzxRbv5uhofltKxpLr1cs1kanQd.png)

    该时间序列图展示指定节点或者集群内所有节点的服务延迟的 99th 百分位数，即在观察时间内，百分之九十九（`99%`）的节点的服务延迟低于或等于这个值。

- **Replicas per Node**

    ![](../../static/db-monitor/Jo9RbQvxmosI7qxth1ccI2kNn0c.png)

    该时间序列图展示指定节点或者集群内所有节点的副本数量。

- **Capacity**

    ![](../../static/db-monitor/U7j1byuD8oRTeixI21CcbmWLnlc.png)

    用户可以通过监控存储容量图来判断什么时候需要为集群添加新的存储空间。

## 硬件

- **CPU Usage**

    ![](../../static/db-monitor/J7vqbSnEtoGhBBxjHFZcuxZSnGg.png)

    该时间序列图展示指定节点或者集群内所有节点上 KWDB 进程的 CPU 使用率。

- **Memory Usage**

    ![](../../static/db-monitor/JeIdbdVggok26xxs18WcVmH7nOd.png)

    该时间序列图展示指定节点或者集群内所有节点上 KWDB 进程的内存使用情况。

- **Disk Read Bytes**

    ![](../../static/db-monitor/E1qsb8K1Co80u9xkGRhce12Nn9e.png)

    该时间序列图展示指定节点或者集群内所有节点上运行的所有进程（包括 KWDB 进程）读取硬盘的速率。采样值为 `10` 秒内 RPS（Read Per Second，每秒读取速度）的平均值。

- **Disk Write Bytes**

    ![](../../static/db-monitor/KNSDbu45jo8GJsxYcxPcprSenbe.png)

    该时间序列图展示指定节点或者集群内所有节点上运行的所有进程（包括 KWDB 进程）写入硬盘的速率。采样值为 `10` 秒内 WPS（Write Per Second，每秒写入速度）的平均值。

- **Disk Read Ops**

    ![](../../static/db-monitor/Lz7jbOyQWodTbOxJ3KNcvbFlnXc.png)

    该时间序列图展示指定节点或者集群内所有节点上运行的所有进程（包括 KWDB 进程）读取硬盘的速率。采样值为 `10` 秒内 OPS（Operations Per Second，每秒运算次数）的平均值。

- **Disk Write Ops**

    ![](../../static/db-monitor/HJLtb61ImoiEcwxpUrXccRypnzg.png)

    该时间序列图展示指定节点或者集群内所有节点上运行的所有进程（包括 KWDB 进程）写入硬盘的速率。采样值为 `10` 秒内 OPS（Operations Per Second，每秒运算次数）的平均值。

- **Disk IPOS In Progress**

    ![](../../static/db-monitor/NwQxbJ16LoGPMuxeloccf1VFnod.png)

    该时间序列图展示指定节点或者集群内所有节点上运行的所有进程（包括 KWDB 进程）读写队列中请求的数量。采样值为 `10` 秒内的平均值。

- **Available Disk Capacity**

    ![](../../static/db-monitor/LDbTbxjSqohHTbxBuOdcAObwnke.png)

    该时间序列图展示指定节点或者集群内所有节点可用的存储容量。

- **Network Bytes Received**

    ![](../../static/db-monitor/O6CIbkRcPoS9MAx1XlUcm9QZnJc.png)

    该时间序列图展示指定节点或者集群内所有节点上运行的所有进程（包括 KWDB 进程）每秒接收的网络字节数的总和。采样值为 `10` 秒内的平均值。

- **Network Bytes Sent**

    ![](../../static/db-monitor/RB5xbslwxoWdakxxJP1cytMonQb.png)

    该时间序列图展示指定节点或者集群内所有节点上运行的所有进程（包括 KWDB 进程）每秒发送的网络字节数的总和。采样值为 `10` 秒内的平均值。

## 运行时

- **Live Node Count**

    ![](../../static/db-monitor/QfKTbN5gSo014kxY9iBcYfiunAg.png)

    该时间序列图展示集群内所有活跃节点的数量。曲线下降表示存在异常节点或不可用节点。

- **Memory Usage**

    ![](../../static/db-monitor/IR0CboQNQoT2SQxljqDcGMVvn4g.png)

    该时间序列图展示指定节点或者集群内所有节点的内存使用量。

    将鼠标悬停在图表上，可以查看更多指标信息。

    | 指标     | 描述                   |
    | -------- | ----------------------- |
    | RSS      | KWDB 内存的使用量。  |
    | Go 总计  | Go 语言层管理的总内存。 |
    | CGo 总计 | C 语言层管理的总内存。  |

- **Kmalloc  memory request**

    ![](../../static/db-monitor/KjVHbf8IjoEoiVxZtTJcB7g1n5f.png)

    该时间序列图展示指定节点的 Kmalloc 内存申请量或者集群内所有节点的内存申请总量。

- **Memory Map virtual size**

    ![](../../static/db-monitor/CZHabyp2Uo88EuxCPJjc32PdnZc.png)

    该时间序列图展示指定节点占用的 Memory Map 虚拟内存量或者集群内所有节点占用的 Memory Map 虚拟内存总量。

- **Memory Map physical size**

    ![](../../static/db-monitor/YDCMbPTg1orfxwxQD1aceFGTnrd.png)

    该时间序列图展示指定节点占用的 Memory Map 物理内存量或者集群内所有节点占用的 Memory Map 物理内存总量。

- **Memory Map range count**

    ![](../../static/db-monitor/DW28bHy7KoQS62xBnDgcY8TznPc.png)

    该时间序列图展示指定节点和集群内所有节点进程中连续开启的虚拟内存块的数量。单个节点中，每个内存块的大小可能不同，所有内存块的大小总和即为该节点占用的 Memory Map 虚拟内存量。所有节点的内存块的大小总和即为该集群所有节点占用的 Memory Map 虚拟内存总量。

- **Goroutine Count**

    ![](../../static/db-monitor/Okg9bC67po8nLjxeHS1cZiIAn7d.png)

    该时间序列图展示指定节点或者集群内所有节点的当前 Goroutine 的数目。

- **GC Runs**

    ![](../../static/db-monitor/N1bNbb37AosZ72xUVvXcTWiDnPf.png)

    该时间序列图展示指定节点或者集群内所有节点的 GC 运行次数。

- **GC Pause Time**

    ![](../../static/db-monitor/FVwJbohXiolWq9xoD9uc86Rlnvh.png)

    在节点视图中，该时间序列图展示指定节点的 GC 阻塞时间。在集群视图中，该时间序列图展示集群中所有节点的 GC 阻塞时间总和。

- **CPU Time**

    ![](../../static/db-monitor/RJ27bQtNFoLSEpxNvC3ccjian6d.png)

    在节点视图中，该时间序列图展示指定节点上的 KWDB 用户级进程和相关系统级操作的 CPU 时间。在集群视图中，该时间序列图展示集群中所有节点的 KWDB 用户级进程和相关系统级操作的 CPU 时间总和。

- **Clock Offset**

    ![](../../static/db-monitor/OQeAbjN1BotOfmxALcfch4yIn5g.png)

    在节点视图中，该时间序列图展示指定节点与集群其他节点的时钟偏差值的平均值。在集群视图中，该时间序列图展示集群中每个节点与集群其他节点的时钟偏差值的平均值。

## SQL

- **Total SQL Connections**

    ![](../../static/db-monitor/PSYhbF7hboLRBZxUi43cPaKYn0f.png)

    该时间序列图展示指定节点或者集群内所有节点的瞬时 SQL 连接数, 包括成功建立的连接和因密码错误或超过最大连接数等原因未能建立的连接。

- **Successful SQL Connections**

    ![](../../static/db-monitor/RIi6bhxUvoG0B6xn6nYcoUBOnsd.png)

    该时间序列图展示指定节点或者集群内所有节点已建立的活跃的 SQL 连接数。

- **SQL Byte Traffic**

    SQL 字节流量视图帮助用户关联 SQL 查询数量和字节流量，特别适合监控批量数据插入或者返回大量数据的分析型查询。

    ![](../../static/db-monitor/XlrfbRwbqoUbiwxr1HRccNkvnYd.png)

    该时间序列图展示指定节点或者集群内所有节点的客户端网络流量的总和，单位为 BPS（Bytes Per Second，每秒字节数）。

- **SQL Queries**

    ![](../../static/db-monitor/Qfavb06w0oq2AAx49p3cVBzentd.png)

    在节点视图中，该时间序列图展示指定节点处理客户端请求的 QPS（Queries Per Second，每秒查询数）。支持的类型包括查询、更新、插入、删除。采样值为 `10` 秒内的平均值。在集群视图中，该时间序列图展示当前集群所有节点处理客户端请求的 QPS。

- **SQL Query Errors**

    ![](../../static/db-monitor/YB2VbbcVNohY4JxH6lycuhukn0b.png)

    该时间序列图展示指定节点或者集群内所有节点返回计划或运行时错误的 SQL 语句数。采样值为 `10` 秒内的平均值。

- **Active Distributed SQL Queries**

    ![](../../static/db-monitor/DuNobhXV1oQnfCxz6rtcEH0inwc.png)

    该时间序列图展示指定节点或者集群内所有节点运行的分布式 SQL 操作数目。

- **Active Flows for Distributed SQL Queries**

    ![](../../static/db-monitor/WpWhb2xrmogqHMxxbT2cwNbHnkc.png)

    该时间序列图展示指定节点或者集群内所有节点协助执行当前分布式 SQL 操作的流的数量。

- **Service Latency: SQL 99th percentile**

    服务延迟是集群从接收到查询请求到查询执行结束之间的时间，不包含将结果传输给客户端的延迟。

    ![](../../static/db-monitor/XG61bho9HopTeKx5u5LcYSqnnKh.png)

    在节点视图中，该时间序列图展示指定节点的服务延迟的 99th 百分位数，即在观察时间内，99% 的服务延迟低于或等于这个值。在集群视图中，该时间序列图展示集群中所有节点的服务延迟的 99th 百分位数，即在观察时间内，99% 的节点的服务延迟低于或等于这个值。

- **Service Latency: SQL 90th percentile**

    ![](../../static/db-monitor/MTzCbnkdvokd9xxfz8dc6lORnhc.png)

    在节点视图中，该时间序列图展示每个节点的服务延迟的 90th 百分位数，即在观察时间内，90% 的服务延迟低于或等于这个值。在集群视图中，该时间序列图展示集群中所有节点的服务延迟的 90th 百分位数，即在观察时间内，90% 的节点的服务延迟低于或等于这个值。

- **KV Execution Latency: 99th percentile**

    ![](../../static/db-monitor/NGyebN55voe7QMxz49XcbSvpnlT.png)

    在节点视图中，该时间序列图展示指定节点在一分钟内执行延迟的 99th 百分位数，即在观察时间内，99% 完成时间低于或等于这个值。在集群视图中，该时间序列图展示集群中所有节点在一分钟内执行延迟的 99th 百分位数，即在观察时间内，99% 的节点的完成时间低于或等于这个值。

- **KV Execution Latency: 90th percentile**

    ![](../../static/db-monitor/HqerbViJlorxB4xM7SfcgpqwnWI.png)

    在节点视图中，该时间序列图展示指定节点在一分钟内执行延迟的 90th 百分位数，即在观察时间内，90% 完成时间低于或等于这个值。在集群视图中，该时间序列图展示集群中所有节点在一分钟内执行延迟的 90th 百分位数，即在观察时间内，90% 的节点的完成时间低于或等于这个值。

- **Transactions**

    ![](../../static/db-monitor/K41wbRNm3oc8ETx3OH1cbsrAncb.png)

    在节点视图中，该时间序列图展示指定节点每秒打开、提交、回滚或中止的事务总数。采样值为 `10` 秒内的平均值。在集群视图中，该时间序列图汇总了所有节点每秒打开、提交、回滚或中止的事务总数。

- **Transaction Execution Latency: 99th percentile**

    ![](../../static/db-monitor/VnnabZQJEozwi2xw54fcHzoonmg.png)

    在节点视图中，该时间序列图展示指定节点在一分钟内事务延迟的 99th 百分位数，即在观察时间内，99% 的事务延迟低于或等于这个值。在集群视图中，该时间序列图展示集群中所有节点在一分钟内事务延迟的 99th 百分位数，即在观察时间内，99% 的节点的事务延迟低于或等于这个值。

- **Transaction Execution Latency: 90th percentile**

    ![](../../static/db-monitor/K6zfbPWtDo6Rq7xAGb2cnoGhnyb.png)

    在节点视图中，该时间序列图展示指定节点在一分钟内事务延迟的 90th 百分位数，即在观察时间内，90% 的事务延迟低于或等于这个值。在集群视图中，该时间序列图展示集群中所有节点在一分钟内事务延迟的 90th 百分位数，即在观察时间内，90% 的节点的事务延迟低于或等于这个值。

- **Schema Changes**

    ![](../../static/db-monitor/UbELbo6bxoGlZnx0fKBc91hmnVe.png)

    该时间序列图展示指定节点或者集群内所有节点每秒 DDL 语句的总数。

## 存储

- **Capacity**

    用户可以通过监控存储容量来判断是否需要为集群添加新的存储空间。

    ![](../../static/db-monitor/V9yWbSSRZoNPDzxAN34cxhdBnyc.png)

    在节点视图中，该时间序列图展示指定节点的总容量（即数据库占用的磁盘空间）、时序数据库占用的磁盘空间、关系数据库占用的磁盘空间、时序和关系数据库已用总空间和磁盘剩余空间。在集群视图中，该时间序列图展示集群中所有节点的磁盘总空间、时序数据库占用的总磁盘空间、关系数据库占用的总磁盘空间、时序和关系数据库已用总空间和磁盘剩余空间。

- **Live Bytes**

    热数据指应用程序和 KWDB 数据库可以读取的数据量，不包括历史数据和已删除数据。

    ![](../../static/db-monitor/RVtQbaT5uoXLwBx0aYTcPG3Jnqe.png)

    该时间序列图展示指定节点或者集群内所有节点应用程序和系统可以读取的数据量，不包括历史数据和已删除数据。

- **Log Commit Latency: 99th percentile**

    Raft 日志提交延迟可视为对存储引擎的预写式日志执行 fdatasync 的度量。

    ![](../../static/db-monitor/PUmbbsx4BoIohrxbS4McYMj1nqb.png)

    在节点视图中，该时间序列图展示指定节点 Raft 日志提交延迟的 99th 百分位数，即在观察时间内，99% 的提交延迟低于或等于这个值。在集群视图中，该时间序列图展示集群中所有节点 Raft 日志提交延迟的 99th 百分位数，即在观察时间内，99% 的节点的提交延迟低于或等于这个值。

- **Log Commit Latency: 50th percentile**

    Raft 日志提交延迟可视为对存储引擎的预写式日志执行 fdatasync 的度量。

    ![](../../static/db-monitor/SsJBb90tvoA3XNxYqgJcGYo8njf.png)

    在节点视图中，该时间序列图展示指定节点 Raft 日志提交延迟的 50th 百分位数，即在观察时间内，50% 的提交延迟低于或等于这个值。在集群视图中，该时间序列图展示集群中所有节点 Raft 日志提交延迟的 50th 百分位数，即在观察时间内，50% 的节点的提交延迟低于或等于这个值。

- **Command Commit Latency: 99th percentile**

    ![](../../static/db-monitor/S9vHbVUAkoAOfuxq0mzcWlmTn6S.png)

    在节点视图中，该时间序列图展示指定节点 Raft 命令提交延迟的 99th 百分位数，即在观察时间内，99% 的提交延迟低于或等于这个值。在集群视图中，该时间序列图展示集群中所有节点 Raft 命令提交延迟的 99th 百分位数，即在观察时间内，99% 的节点的提交延迟低于或等于这个值。

- **Command Commit Latency: 50th percentile**

    ![](../../static/db-monitor/C1P3bewDKouy0GxNMUoc00o7nWf.png)

    在节点视图中，该时间序列图展示指定节点 Raft 命令提交延迟的 50th 百分位数，即在观察时间内，50% 的提交延迟低于或等于这个值。在集群视图中，该时间序列图展示集群中所有节点 Raft 命令提交延迟的 50th 百分位数，即在观察时间内，50% 的节点的提交延迟低于或等于这个值。

- **Read Amplification**

    RocksDB 读放大统计用来衡量节点中每个逻辑读操作的实际读操作的平均值。

    ![](../../static/db-monitor/IPavbkW11oEwJax8MAZc1ZY8nhf.png)

    在节点视图中，该时间序列图展示指定节点 RocksDB 读放大统计。在集群视图中，该时间序列图展示集群中所有节点 RocksDB 读放大统计总和。

- **RocksDB SSTables**

    ![](../../static/db-monitor/Pz7LbYpW3olNNtxV2s5ctcCmnyg.png)

    在节点视图中，该时间序列图展示指定节点在用的 RocksDB SSTable 的数目。在集群视图中，该时间序列图展示集群中所有节点在用的 RocksDB SSTable 的数目总和。

- **File Descriptors**

    ![](../../static/db-monitor/VaWCb76IboTENJxKD8BcL3lRnqb.png)

    该时间序列图展示指定节点或者集群内所有节点开放的文件描述符数量以及文件描述符数量的上限。

- **Compactions/Flushes**

    ![](../../static/db-monitor/Okqab55NRok2QkxS1rec0Kxwn7b.png)

    该时间序列图展示指定节点或者集群内所有节点每秒 RocksDB 压缩和写入硬盘的数目。

- **Time Series Monitoring Data Sampling Writes**

    ![](../../static/db-monitor/UcUMbFiUnoQwgjxFzKPclxsZnld.png)

    该时间序列图展示指定节点或者集群内所有节点每秒写入 metrics 监控数据成功的数目和错误的数目。

- **Time Series Monitoring Data Written Bytes**

    ![](../../static/db-monitor/Rs1gb1gT9oIT9TxZLmNcrr7Tnmh.png)

    在节点视图中，该时间序列图展示指定节点每秒 metrics 监控数据写入的字节数。在集群视图中，该时间序列图展示集群中所有节点每秒 metrics 监控数据写入的字节数总和。

    ::: warning 注意
    由于数据在磁盘上高度压缩，本视图展示的是 metrics 监控写数据产生的网络流量和硬盘活动量，不是 metrics 监控数据写占用磁盘的速率。可通过数据库页面查看 metrics 监控数据的当前硬盘使用情况。
    :::

## 副本

- **Ranges**

    Ranges 数目视图展示 Range 状态相关的具体信息。

    ![](../../static/db-monitor/BQKgbaSe3otJdaxG9Gtcx0DRn7e.png)

    该时间序列图展示指定节点或者集群内所有节点持有的 Range 的详细信息。

- **Replicas per Store**

    ![](../../static/db-monitor/B9W9b43TYoIT1pxAN26cpQZRnWe.png)

    该时间序列图展示指定节点或者集群内所有节点的每个 store 的副本数量。

- **Leaseholders per Store**

    租赁副本指接收和协调其 Range 上所有读取和写入请求的副本。

    ![](../../static/db-monitor/Q3fPbkTFAoOVP4x4ApIcFPrmnbg.png)

    该时间序列图展示指定节点或者集群内所有节点的每个 Store 的租赁副本数。

- **Average Queries per Store**

    每个 Store 的平均访问次数指每个 Store 的租赁副本每秒处理的 KV 批量请求的数目的指数加权平均值。记录大约最后 `30` 分钟的请求，用来协助基于负载的再平衡决策。

    ![](../../static/db-monitor/MbeDb27l4oQxQQxU8eAcCE4envg.png)

    该时间序列图展示指定节点或者集群内所有节点的每个 Store 的平均访问次数。

- **Logical Bytes per Store**

    ![](../../static/db-monitor/Bd0IbSI2DoBwJQxqQnccyuHxnXo.png)

    该时间序列图展示指定节点或者集群内所有节点的每个 Store 的数据逻辑字节数，包含历史数据和已删除数据。

- **Replicas Quiescence**

    ![](../../static/db-monitor/BNJmbZmLxoOPdUxjL4qcFvzwnod.png)

    在节点视图中，该时间序列图展示指定节点的副本和静止副本数量。在集群视图中，该时间序列图展示集群中所有节点的副本和静止副本数量总和。

- **Range Operations**

    ![](../../static/db-monitor/NWe5b4o54ofDPyxquQoc0Fdmnt8.png)

    该时间序列图展示指定节点或者集群内所有节点的操作涉及的 Range 操作次数。

- **Snapshots**

    ![](../../static/db-monitor/RAHbbrJkXojxpMx0nx6c3m8YniZ.png)

    在节点视图中，该时间序列图展示指定节点的快照数目。在集群视图中，该时间序列图展示集群中所有节点的快照数目总和。

## 分布式

- **Batches**

    ![](../../static/db-monitor/XoYZb24Eso27FLx3jKncLuLAndb.png)

    该时间序列图展示指定节点或者集群内所有节点的 Batch 数目。

- **RPCs**

    ![](../../static/db-monitor/H6nUb9TKdopgIyxrOVvcHbzynwh.png)

    该时间序列图展示指定节点或者集群内所有节点的 RPC（Remote Procedure Call，远程过程调用）数目。

- **RPC Errors**

    ![](../../static/db-monitor/SwHabHj3ZoM4jyxMYawcxIayn4b.png)

    该时间序列图展示指定节点或者集群内所有节点的 RPC 错误数。

- **KV Transactions**

    ![](../../static/db-monitor/AMqFb6DLaoFNIMxaVjhcY1FynkX.png)

    该时间序列图展示指定节点或者集群内所有节点的 KV 事务数。

- **KV Transaction Restarts**

    ![](../../static/db-monitor/K92ibNmHroANmgxzIo3c7OSenId.png)

    该时间序列图展示指定节点或者集群内所有节点的 KV 事务的重试次数。

- **KV Transaction Durations: 99th percentile**

    ![](../../static/db-monitor/G5gMbXAjyoKaFmxmyeRc4iAYnoc.png)

    在节点视图中，该时间序列图展示指定节点过去一分钟 KV 事务持续时间的 99th 百分位数，即在观察时间内，99% 的持续时间低于或等于这个值。在集群视图中，该时间序列图展示集群中所有节点过去一分钟 KV 事务持续时间的 99th 百分位数，即在观察时间内，99% 的节点的持续时间低于或等于这个值。

- **KV Transaction Durations: 90th percentile**

    ![](../../static/db-monitor/P6bcbOABDos5zZxjK9TcLX9YnRb.png)

    在节点视图中，该时间序列图展示指定节点 KV 事务持续时间的 90th 百分位数，即在观察时间内，90% 的持续时间低于或等于这个值。在集群视图中，该时间序列图展示集群中所有节点 KV 事务持续时间的 90th 百分位数，即在观察时间内，90% 的节点的持续时间低于或等于这个值。

- **Node Heartbeat Latency: 99th percentile**

    ![](../../static/db-monitor/VTkibQmCqo3rYhxlsNCcJZkxnDf.png)

    在节点视图中，该时间序列图展示指定节点心跳延迟的 99th 百分位数，即在观察时间内，99% 的心跳延迟低于或等于这个值。在集群视图中，该时间序列图展示集群中所有节点心跳延迟的 99th 百分位数，即在观察时间内，99% 的节点的心跳延迟低于或等于这个值。

- **Node Heartbeat Latency: 90th percentile**

    ![](../../static/db-monitor/LnZvbcHD2oemfbxLU52cXII5nZg.png)

    在节点视图中，该时间序列图展示指定节点心跳延迟的 90th 百分位数，即在观察时间内，90% 的心跳延迟低于或等于这个值。在集群视图中，该时间序列图展示集群中所有节点心跳延迟的 90th 百分位数，即在观察时间内，90% 的节点的心跳延迟低于或等于这个值。

## 队列

- **Queue Processing Failures**

    ![](../../static/db-monitor/NzkObSr39op3h8xQCTrcNwjDnrh.png)

    该时间序列图展示指定节点或者集群内所有节点的队列操作处理失败数目。

- **Queue Processing Times**

    ![](../../static/db-monitor/R6jnbw35XorWPmx5wwIc6QNRn0g.png)

    在节点视图中，该时间序列图展示指定节点各队列处理时间。在集群视图中，该时间序列图展示集群中所有节点各队列处理时间的总和。

- **Replica GC Queue**

    ![](../../static/db-monitor/ZIfibavDwoRzbRxbd47cKoQPnrc.png)

    在节点视图中，该时间序列图展示指定节点的 GC 副本队列数目。在集群视图中，该时间序列图展示集群中所有节点的 GC 副本队列数目总和。

- **Replication Queue**

    ![](../../static/db-monitor/TCGjbxEP5of7y3xZ2Osc4Dyvnpo.png)

    在节点视图中，该时间序列图展示指定节点的副本队列数目。在集群视图中，该时间序列图展示集群中所有节点的副本队列数目总和。

- **Split Queue**

    ![](../../static/db-monitor/X7Cjb6lHXoMnJ1xjiw2cqbgTncf.png)

    在节点视图中，该时间序列图展示指定节点的分割队列数目。在集群视图中，该时间序列图展示集群中所有节点分割队列数目总和。

- **Merge Queue**

    ![](../../static/db-monitor/RNf5bqPM7ocIcwxbXyOcXdPKngg.png)

    在节点视图中，该时间序列图展示指定节点的合并队列数目。在集群视图中，该时间序列图展示集群中所有节点合并队列数目总和。

- **GC Queue**

    ![](../../static/db-monitor/LXVGb8dYFozUw5xTaV1cR4vtnrd.png)

    在节点视图中，该时间序列图展示指定节点的 GC 队列数目。在集群视图中，该时间序列图展示集群中所有节点 GC 队列数目总和。

- **Raft Log Queue**

    ![](../../static/db-monitor/Wm11bdBUbonOaWx9H6RcRCZBnul.png)

    在节点视图中，该时间序列图展示指定节点的 Raft 日志队列数目。在集群视图中，该时间序列图展示集群中所有节点 Raft 日志队列数目总和。

- **Raft Snapshot Queue**

    ![](../../static/db-monitor/OKTnbVKYnoPKB6xUP24cZrnJnjk.png)

    在节点视图中，该时间序列图展示指定节点的 Raft 快照队列数目。在集群视图中，该时间序列图展示集群中所有节点 Raft 快照队列数目总和。

- **Consistency Checker Queue**

    ![](../../static/db-monitor/QqBTbhsjVoW2JIxP03Rcd1Bjnkc.png)

    在节点视图中，该时间序列图展示指定节点一致性检查器队列数目。在集群视图中，该时间序列图展示集群中所有节点一致性检查器队列数目总和。

- **Metrics Monitoring Data Maintenance Queue**

    ![](../../static/db-monitor/M1OTb9v0goNcXOxwtEAcyodZnfc.png)

    在节点视图中，该时间序列图展示指定节点的 metrics 监控维护队列数目。在集群视图中，该时间序列图展示集群中所有节点 metrics 监控维护队列数目总和。

- **Compaction Queue**

    ![](../../static/db-monitor/Kei4bq7PZoj82lxboEqcA57Cnyd.png)

    在节点视图中，该时间序列图展示指定节点通过强制 RocksDB 压缩回收或可能回收的已完成或估计的存储字节。在集群视图中，该时间序列图展示集群中所有节点通过强制 RocksDB 压缩回收或可能回收的已完成或估计的存储字节。

## 慢查询

- **Slow Raft Proposals**

    ![](../../static/db-monitor/QRMobB49QoTYDhxsITVcNU8Tnhh.png)

    在节点视图和集群视图中，该时间序列图展示集群中所有节点 Raft 中提案提交变缓的请求数。

- **Slow DistSender RPCs**

    ![](../../static/db-monitor/JzflbuXWKo94hSxzTQOcZqLJnSb.png)

    在节点视图和集群视图中，该时间序列图展示集群中所有节点不同节点之间发送 RPC 变缓的请求数。

- **Slow Lease Acquisitions**

    分布式系统中，租约（Lease）通常用于协调和同步操作。

    ![](../../static/db-monitor/Ujx5b5TcHoymDvxpuPPcNQ1engf.png)

    在节点视图和集群视图中，该时间序列图展示集群中所有节点的租约获取变缓的请求数。

- **Slow Latch Acquisitions**

    Latch 是一种低级别的同步机制，用于保护共享资源。

    ![](../../static/db-monitor/DCtGbzNCioIgPvxfJLEcVWQ8nZb.png)

    在节点视图和集群视图中，该时间序列图展示集群中所有节点的 Latch 获取变缓的请求数。
