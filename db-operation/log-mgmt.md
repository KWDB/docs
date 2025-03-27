---
title: 日志管理
id: log-mgmt
---

# 日志管理

KWDB 根据不同的数据库操作生成不同类型的日志，并将这些日志存储在指定位置，以便运维人员进行数据库监控和故障排查。

## 日志类型和存储位置

下表列出了在数据库运维期间可能生成的日志类型及其存储位置。

| **日志类型**       | **描述**                                                         | **存储位置**                                                     |
|-------------------|------------------------------------------------------------------|------------------------------------------------------------------|
| 时序引擎日志       | - 记录时序引擎的运行状态<br>- 日志名以 `TsEngine` 开头              | - KWDB 用户数据目录下的 `logs` 子目录<br>- 支持通过 `--log-dir` 启动参数指定日志目录<br>- 默认路径：`/var/lib/kaiwudb/logs`|
| 关系引擎日志       | - 记录关系引擎的运行状态<br>- 日志名以 `kwbase-rocksdb` 开头       |  - KWDB 用户数据目录下的 `logs` 子目录<br>- 支持通过 `--log-dir` 启动参数指定日志目录<br>- 默认路径：`/var/lib/kaiwudb/logs` |
|通用日志         | - 记录非存储引擎的运行状态<br>- 日志名以 `kwbase` 开头         |  - KWDB 用户数据目录下的 `logs` 子目录<br>- 支持通过 `--log-dir` 启动参数指定日志目录<br>- 默认路径：`/var/lib/kaiwudb/logs` |
| 审计日志           | - 记录数据库活动和操作的详细信息<br>- 日志名以 `kwbase-sql-audit` 开头<br>- 审计功能默认关闭。开启后会自动审计系统级操作，并生成审计日志| - KWDB 用户数据目录下的 `logs` 子目录<br>- 支持通过 `--sql-audit-dir` 启动参数指定审计日志路径。<br>- 默认路径：`/var/lib/kaiwudb/logs` |
| 错误日志           | - 记录时序引擎崩溃时的信息<br>- 日志名以 `errlog` 开头    |   - 数据库的启动目录                                                |

## 日志格式

### 时序引擎日志、关系引擎日志和通用日志

**日志格式：**

```plain
[日志级别和日期] [时间戳] [线程号] [代码文件和行号] [定制化日志信息]
```

- 日志级别：包括 `D`（DEBUG）、`I`（INFO）、`W`（WARNING）、`E`（ERROR）、`F`（FATAL）。

  - DEBUG：用于现场分析和开发调试，记录代码执行过程中的详细信息。
  - INFO：默认级别，记录用户操作或应用触发的重要操作、系统重要事件和状态变化。
  - WARNING：记录系统遇到的异常情况，通常能自行恢复，但需要运维人员关注。
  - ERROR：记录无法自行恢复的错误，系统可能会继续运行，但当前操作失败或阻塞。
  - FATAL：记录致命错误，系统无法继续正常工作，可能需要立即停止服务。

- 日期：事件发生的日期。
- 时间戳：格式为 `[yymmdd HH:MM:SS.usec]`。
- 线程号：线程标识符。
- 代码文件和行号：格式为 `filename:loc`。
- 定制化日志信息：相关引擎的运行记录信息。

**示例：**

- 时序引擎日志:

    ```plain
    I2407 11:28:05.862568 246 MMapHashIndex.cpp:163 Hash Index 79.tag.ht rehash, new_size: 256
    ```

- 关系引擎日志:

    ```plain
    I240702 03:28:09.254802 8370 storage/rocksdb.go:103 EVENT_LOG_v1 {"time_micros": 1719890889254695, "job": 262, "event": "compaction_finished", "compaction_time_micros": 34185, "compaction_time_cpu_micros": 33466, "output_level": 6, "num_output_files": 1}
    ```

- 通用日志:

    ```plain
    W240706 00:57:35.240359 1511957 vendor/google.golang.org/grpc/clientconn.go:1206 grpc: addrConn.createTransport failed to connect to {server_svt_node_4:26257 0 <nil>}. Err :connection error
    ```

### 审计日志

**日志格式：**

```plain
[日志级别和日期] [时间] [goroutine id] [审计源码文件路径] [节点 ID] [日志输入计数] [事件发生时间] [事件执行时间] [用户信息] [事件类型] [操作对象] [审计级别] [客户端信息] [事件执行结果] [执行语句] [审计事件记录节点]
```

更多详细信息，参见[审计管理](../db-security/audit-mgmt.md)。

**示例：**

```plain
I240415 06:49:34.207014 538 security/audit/actions/record_to_log.go:45 [n1] 3 {"EventTime":"2024-04-15T06:49:34.206948441Z","User":{"UserID":0,"Username":"root","Roles":[{"ID":0,"Name":"admin"}]},"Event":"CREATE","Target":{"Typ":"DATABASE","Targets":{"78":{"ID":78,"Name":"db1"}}},"Level":1,"Client":{"AppName":"$ kwbase sql","Address":"127.0.0.1:55564"},"Result":{"Status":"OK","ErrMsg":"","RowsAffected":0},"Command":{"Cmd":"CREATE DATABASE db1","Params":"{}"}}

```

### 错误日志

错误日志 (`errlog.log`) 记录数据库严重异常时的当前 call stack 信息。

**示例：**

```plain
Exception time(UTC):2024-11-02 13:33:22signal:Segmentation fault(11)pid=109818 tid=110896 si_code=1 si_addr=0x48backtrace: size:14#0 /usr/local/kaiwudb/bin/../lib/libcommon.so(kwdbts::PrintBacktrace(std::ostream&)+0x3d) [0x7fa9805b2f9d]#1 /usr/local/kaiwudb/bin/../lib/libcommon.so(kwdbts::ExceptionHandler(int, siginfo_t*, void*)+0x281) [0x7fa9805b36a1]#2 /lib/x86_64-linux-gnu/libc.so.6(+0x42520) [0x7fa97fd51520]#3 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(+0x2546d3) [0x7fa98082c6d3]#4 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(kwdbts::SynchronizerOperator::~SynchronizerOperator()+0x2a7) [0x7fa98082e0b7]#5 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(kwdbts::SynchronizerOperator::~SynchronizerOperator()+0xd) [0x7fa98082e1dd]#6 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(kwdbts::Processors::Reset()+0x37) [0x7fa980816677]#7 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(kwdbts::DmlExec::DestroyTsScan(kwdbts::DmlExec::TsScan*)+0x4e) [0x7fa9807963ee]#8 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(kwdbts::DmlExec::ClearTsScans(kwdbts::_kwdbContext_t*)+0x51) [0x7fa980796771]#9 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(kwdbts::DmlExec::Next(kwdbts::_kwdbContext_t*, int, bool, _QueryInfo*)+0xeb) [0x7fa980796e7b]#10 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(kwdbts::DmlExec::ExecQuery(kwdbts::_kwdbContext_t*, _QueryInfo*, _QueryInfo*)+0x174) [0x7fa980797004]#11 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(TSExecQuery+0x261) [0x7fa980728571]#12 /usr/local/kaiwudb/bin/kwbase(_cgo_b2bb81300987_Cfunc_TSExecQuery+0x31) [0x36abbe1]#13 /usr/local/kaiwudb/bin/kwbase() [0x6a1b70]
```

## 日志管理

### 通用日志管理

KWDB 支持通过以下任一方式设置日志相关参数，控制日志存储目录、输出级别等信息：

- `kwbase start` 命令
- 裸机部署后生成的 `kaiwudb_env` 文件
- 容器部署后生成的 `docker-compose.yml` 文件

更多详细信息，参见[集群配置](./cluster-settings-config.md)。

下表列出了 KWDB 支持设置的日志启动参数：

| **参数**              | **描述**                                                     |
|----------------------|------------------------------------------------------------|
| `--log-dir`           | 启动日志功能并指定日志目录。若配置为空字符串 (`--log-dir=`)，则关闭日志功能。<br>默认值：`/var/lib/kaiwudb/logs` |
| `--log-dir-max-size`  | 设置日志目录最大大小。超过设置值时，系统会删除最老的日志。<br>默认值：`100MiB` |
| `--log-file-max-size` | 设置单个日志文件的最大大小。超过设置阈值时，系统会创建新文件继续输出日志。<br>默认值: `10MiB` |
| `--log-file-verbosity`| 设置日志输出的最小级别。支持设置以下日志级别：`DEBUG`、`INFO`、`WARNING`、`ERROR`和`FATAL`。<br>默认值：`INFO`|
| `--sql-audit-dir`     | 指定审计日志目录。默认与其他日志存储在同一目录。 |
| `--logtostderr`       | 将指定级别及以上的日志输出到 `stderr`。如果不指定值（`--logtostderr`），默认输出所有级别的日志；`--logtostderr=NONE` 会禁止日志输出到 `stderr`。<br>默认值：`NONE` |
| `--no-color`          | 是否对 `stderr` 输出着色，支持设置为 `true` 或 `false`。<br>默认值: `false` 
| `--vmodule`           | 启用文件过滤日志记录，支持通过逗号分隔的 `pattern=N` 列表配置，但可能会严重影响性能。 |

### 审计日志管理

审计功能默认关闭，用户启动审计功能后，系统将自动输出系统级别的审计日志。

- 启动审计功能和审计日志：

    ``` SQL
    SET CLUSTER SETTING audit.enabled = true;
    ```

- 启动审计功能，关闭审计日志：

    ```SQL
    -- 启动审计功能
    SET CLUSTER SETTING audit.enabled = true;

    -- 关闭审计日志
    SET CLUSTER SETTING audit.log.enabled = false;
    ```

- 关闭审计功能和审计日志：

    ``` SQL
    SET CLUSTER SETTING audit.enabled = false;
    ```