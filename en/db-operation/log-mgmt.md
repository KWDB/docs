---
title: Log Management
id: log-mgmt
---

# Log Management

KWDB maintains several types of logs to help you monitor and troubleshoot your database operations. This section explains how to work with these logs effectively.

## Log Types and Locations

| **Log Type**              | **Description**                                                                 | **Storage Location**                                                                 |
|---------------------------|---------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Time-Series Engine Log    | - Tracks the runtime status of the time-series engine. <br>- Files starting with `TsEngine`. | -  Located in the `logs` subdirectory of the KWDB user data directory <br>- Configurable via the `--log-dir` startup flag. <br>- Default: `/var/lib/kaiwudb/logs` |
| Relational Engine Log     | - Records the runtime status of the relational engine. <br>- Files starting with `kwbase-rocksdb`. | -  Located in the `logs` subdirectory of the KWDB user data directory <br>- Configurable via the `--log-dir` startup flag. <br> - Default: `/var/lib/kaiwudb/logs`. |
| General Log    | - Captures system-wide events and non-storage operations. <br> - Files starting with `kwbase`. | -  Located in the `logs` subdirectory of the KWDB user data directory <br>- Configurable via the `--log-dir` startup flag. <br> - Default: `/var/lib/kaiwudb/logs`. |
| Audit Log                 | - Records database activities and operations. <br> - Files starting with `kwbase-sql-audit`.<br>- The audit function is disabled by default. When enabled, system-level operations are automatically logged.| -  Located in the `logs` subdirectory of the KWDB user data directory <br>- Configurable via the `--sql-audit-dir` startup flag. <br> - Default: `/var/lib/kaiwudb/logs`. |
| Error Log                 | - Records information when the time-series engine crashes. <br>- Files starting with `errlog`.                        | - Located in the database startup directory.                                           |

## Log Formats

### Time-Series Engine Log, Relational Engine Log, and General Log

**Log format**:

```plain
[Log Level and Date] [Timestamp] [Thread ID] [File and Line Number] [Custom Log Information]
```

- Log Level: Includes `D` (DEBUG), `I` (INFO), `W` (WARNING), `E` (ERROR), and `F` (FATAL).
  - DEBUG: detailed information about code execution, used for on-site analysis and development debugging.
  - INFO (default level): important user operations, system events, and state changes.
  - WARNING: Issues requiring attention but not affecting core operations.
  - ERROR: Problems that prevent specific operations from completing.
  - FATAL: Critical issues requiring immediate action.
- Date: The date when the event occurs.
- Timestamp: Format `[yymmdd HH:MM:SS.usec]`.
- Thread ID: Thread identifier.
- File and Line Number: Format `filename:loc`.
- Custom Log Information: Engine-specific operational data.

**Example:**

- Time-Series Engine Log:

    ```plain
    I2407 11:28:05.862568 246 MMapHashIndex.cpp:163 Hash Index 79.tag.ht rehash, new_size: 256
    ```

- Relational Engine Log:

    ```plain
    I240702 03:28:09.254802 8370 storage/rocksdb.go:103 EVENT_LOG_v1 {"time_micros": 1719890889254695, "job": 262, "event": "compaction_finished", "compaction_time_micros": 34185, "compaction_time_cpu_micros": 33466, "output_level": 6, "num_output_files": 1}
    ```

- General Log:

    ```plain
    W240706 00:57:35.240359 1511957 vendor/google.golang.org/grpc/clientconn.go:1206 grpc: addrConn.createTransport failed to connect to {server_svt_node_4:26257 0 <nil>}. Err :connection error
    ```

### Audit Log

**Log format**:

```plain
[Log Level and Date] [Timestamp] [Goroutine ID] [Source File Path] [Node ID] [Log Input Count] [Event Time] [Event Execution Period] [User Info] [Event Type] [Target Info] [Audit Level] [Client Info] [Event Execution Result] [Executed Command] [Record Node]
```

For more information, see [Audit Management](../db-security/audit-mgmt.md).

**Example:**

```plain
I240415 06:49:34.207014 538 security/audit/actions/record_to_log.go:45 [n1] 3 {"EventTime":"2024-04-15T06:49:34.206948441Z","User":{"UserID":0,"Username":"root","Roles":[{"ID":0,"Name":"admin"}]},"Event":"CREATE","Target":{"Typ":"DATABASE","Targets":{"78":{"ID":78,"Name":"db1"}}},"Level":1,"Client":{"AppName":"$ kwbase sql","Address":"127.0.0.1:55564"},"Result":{"Status":"OK","ErrMsg":"","RowsAffected":0},"Command":{"Cmd":"CREATE DATABASE db1","Params":"{}"}}
```

### Error Log

The error log (`errlog.log`) records call stack information during serious database failures.

**Example:**

```plain
Exception time(UTC):2024-11-02 13:33:22signal:Segmentation fault(11)pid=109818 tid=110896 si_code=1 si_addr=0x48backtrace: size:14#0 /usr/local/kaiwudb/bin/../lib/libcommon.so(kwdbts::PrintBacktrace(std::ostream&)+0x3d) [0x7fa9805b2f9d]#1 /usr/local/kaiwudb/bin/../lib/libcommon.so(kwdbts::ExceptionHandler(int, siginfo_t*, void*)+0x281) [0x7fa9805b36a1]#2 /lib/x86_64-linux-gnu/libc.so.6(+0x42520) [0x7fa97fd51520]#3 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(+0x2546d3) [0x7fa98082c6d3]#4 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(kwdbts::SynchronizerOperator::~SynchronizerOperator()+0x2a7) [0x7fa98082e0b7]#5 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(kwdbts::SynchronizerOperator::~SynchronizerOperator()+0xd) [0x7fa98082e1dd]#6 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(kwdbts::Processors::Reset()+0x37) [0x7fa980816677]#7 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(kwdbts::DmlExec::DestroyTsScan(kwdbts::DmlExec::TsScan*)+0x4e) [0x7fa9807963ee]#8 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(kwdbts::DmlExec::ClearTsScans(kwdbts::_kwdbContext_t*)+0x51) [0x7fa980796771]#9 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(kwdbts::DmlExec::Next(kwdbts::_kwdbContext_t*, int, bool, _QueryInfo*)+0xeb) [0x7fa980796e7b]#10 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(kwdbts::DmlExec::ExecQuery(kwdbts::_kwdbContext_t*, _QueryInfo*, _QueryInfo*)+0x174) [0x7fa980797004]#11 /usr/local/kaiwudb/bin/../lib/libkwdbts2.so(TSExecQuery+0x261) [0x7fa980728571]#12 /usr/local/kaiwudb/bin/kwbase(_cgo_b2bb81300987_Cfunc_TSExecQuery+0x31) [0x36abbe1]#13 /usr/local/kaiwudb/bin/kwbase() [0x6a1b70]
```

## Log Management

### General Log Settings

KWDB provides several startup flags to control how logs are generated, stored, and managed. You can set these flags using any of the following methods:

- The `kwbase start` command
- The `kaiwudb_env` file (bare-metal deployments).
- The `docker-compose.yml` file (container deployments).

For instructions, see [Cluster Settings](./cluster-scale.md).

The following table lists all configurable startup flags related to log management:

| **Flag**              | **Description**                                                                 |
|----------------------------|---------------------------------------------------------------------------------|
| `--log-dir`                | Enables logging and sets the log directory. When set to a black string (`--log-dir=`), logging is disabled. <br>Default: `/var/lib/kaiwudb/logs`.|
| `--log-dir-max-size`       | Controls total log storage. Oldest logs are removed when the limit is reached. <br>Default: `100MiB`.|
| `--log-file-max-size`      | Sets the maximum size of a single log file. A new file is created when the limit is reached. <br>Default: `10MiB`.|
| `--log-file-verbosity`     | Sets the minimum severity level for log output. Available options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `FATAL`. <br>Default: `INFO`.|
| `--sql-audit-dir`          | Sets the directory where audit logs are stored.<br>Default: Same directory as other logs. |
| `--logtostderr`            | Logs at or above the specified level are printed to `stderr`. If no level is specified (`--logtostderr`), logs of all levels are printed. Use `--logtostderr=NONE` to disable the function. <br> Default: `None`.|
| `--no-color`               | Enables/disables colored stderr output. Values can be `true` or `false` <br>Default: `false`. |
| `--vmodule`                | Enables file-filtered logging. Supports a comma-separated list of `pattern=N` configurations but may greatly impact performance. |

### Managing Audit Logging

The audit function is disabled by default. When the audit function is enabled, the audit logging is enabled.

- To enable audit and audit logging:

    ``` SQL
    SET CLUSTER SETTING audit.enabled = true;
    ```

- To enable audit while disabling audit loging:

    ```sql
    -- Enable audit
    SET CLUSTER SETTING audit.enabled = true;

    -- Disable audit logging
    SET CLUSTER SETTING audit.log.enabled = false;
    ```

- To disable both audit and audit loging:

    ``` SQL
    SET CLUSTER SETTING audit.enabled = false;
    ```
