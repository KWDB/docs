# Cluster Configuration

After deploying KWDB, you can customize its behavior through two main configuration mechanisms: startup flags and cluster parameters.

| **Parameter Type**       | **Scope**                          | **When Changes Take Effect**                           | **How to Configure**                                          |
| :---------------------- | :----------------------------------------- | :------------------------------------------ | :---------------------------------------------------------------- |
| **Startup flags**  | Individual node | Only at node startup (requires service restart)|• Bare-metal deployment: Edit `/etc/kaiwudb/script/kaiwudb_env`<br>• Container deployment: Edit `/etc/kaiwudb/script/docker-compose.yml`<br>• Command line: Use `kwbase start` with flags |
| **Cluster parameters** | Entire cluster (all nodes)| Immediately (no restart needed)| Execute SQL statements (changes are stored in system tables) |

## Startup Flags

### Startup Flag Overview

Startup flags control how individual KWDB nodes operate. These include settings for general operation, networking, security, logging, and more.

::: warning Note

- Most cluster startup flags have default values that can be overridden by explicitly specifying the flags. Except for the `--join` flag, all other flag values are non-persistent and must be reconfigured each time the node is restarted. The `--join` flag value is stored in the node's data directory. It is recommended to reconfigure the `--join` flag each time KWDB starts, so that nodes can rejoin the cluster and recover even if the data directory is lost.
- New startup flag configurations take effect only after a system restart.

:::

#### General Flags

| Flag           | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--background`      | Run in the background. <br> **Note** <br> The `--background` flag is suitable for short-term and testing scenarios. It is not recommended for long-running services due to limitations in detaching from the current terminal. A service manager or tools like `daemon(8)` are recommended for long-term operation.                                                                                                                                                                                                                                                                                 |
| `--cache`           | Cache size, shared across multiple physical storage devices. The value can be an exact memory value (in bytes), a decimal value (converted to percentage), or a percentage value: <br>- `--cache=.25` <br>- `--cache=25%` <br>- `--cache=1000000000`: 1,000,000,000 bytes <br>- `--cache=1GB`: 1,000,000,000 bytes <br>- `--cache=1GiB`: 1,073,741,824 bytes <br> **Note** <br> If using the percentage sign (`%`) format, ensure the system can correctly recognize the escaped percentage sign. In some configuration files, the percentage sign may be interpreted as a comment marker. Therefore, decimal values are recommended. <br> Default: 128 MiB. This default is set for local cluster deployment scenarios. In production environments, `25%` or higher is recommended. |
| `--external-io-dir` | Path for external I/O directories when performing backup and restore using local node directories or NFS drives. If set to `disabled`, NFS is disabled, and data is backed up locally using the local node directory. <br> Default: The `extern` subdirectory of the first `--store` configuration. You can create symbolic links to the `extern` directory to change `--external-io-dir` without restarting the node.|
| `--max-sql-memory`  | Maximum in-memory storage allowed for SQL query cache, including prepared queries and intermediate data rows during execution. This can be a decimal value (converted to percentage), a percentage value, or an exact value (in bytes), such as: <br>- `--max-sql-memory=.25` <br>- `--max-sql-memory=25%` <br>- `--max-sql-memory=10000000000`: 10,000,000,000 bytes <br>- `--max-sql-memory=1GB`: 1,000,000,000 bytes <br>- `--max-sql-memory=1GiB`: 1,073,741,824 bytes. <br> The temporary files are stored in the path specified by `--temp-dir`. <br> **Note** <br> If using the percentage sign (`%`) format, ensure the system can correctly recognize the escaped percentage sign. In some configuration files, the percentage sign may be interpreted as a comment marker. Therefore, decimal values are recommended. |
| `--store` <br>`-s`   | Path to storage devices for database data. You can specify both device attributes and space size. For multiple devices, specify the flag separately for each device, for example: `--store=/mnt/ssd01 --store=/mnt/ssd02`. For more information, see [Storage Flags](#storage-flags).    |

#### Networking Flags

| Flag            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `--advertise-addr`     | The IP address/hostname and port used by the node for communication with other nodes. If a hostname is used, it must resolve correctly. If an IP address is used, it must be accessible. For IPv6, use formats like `[::1]` or `[fe80::f6f2:::]`. <br>This flag's effect depends on the combination with the `--listen-addr` flag. For example, if the port differs from `--listen-addr`, port forwarding is required. <br>**Default:** Value of `--listen-addr`. If `--listen-addr` is not specified, defaults to canonical hostname (second column in `/etc/hosts`) with port `26257`.|
| `--brpc-addr`            | The brpc communication address between time-series engines. Format: `<host>:<port>` or `:<port>`: <br>- Must include a port number; otherwise, the system will report an error: `failed to start server: --brpc-addr's port not specified`. <br>- The IP address can be omitted. If not specified, the system will use the IP from `--advertise-addr` or `--listen-addr` in that order. <br>**Note**<br>Both `--advertise-addr` and `--brpc-addr` are inter-node communication addresses, so network connectivity between nodes must be ensured. It is recommended to use the format `--brpc-addr=:<port>`, allowing the system to automatically obtain the IP address.|
| `--listen-addr`        | The IP address/hostname and port for receiving connections from nodes and clients. For IPv6, use formats like `[::1]` or `[fe80::f6f2:::]`. <br> This flag's effect depends on the combination with `--advertise-addr`. <br> **Default**: Listens on all IPs on port `26257`. If `--advertise-addr` is not specified, the canonical hostname is used for communication with other nodes.                                                                                                                                                                                                                                            |
| `--http-addr`          | The IP address/hostname for the external Admin interface. For IPv6, use formats like `[::1]:8080` or `[fe80::f6f2:::]:8080`. <br> **Default**: Same as `--listen-addr` on port `8080`.                                                                                                                                                                                                                                                 |
| `--join` <br>`-j`      | Addresses of the cluster nodes to connect to. On initialization, specify 3-5 node addresses and ports, then run `kwbase init` to start the cluster. If not specified, a single-node cluster is started and `kwbase init` is not needed. To add new nodes to an existing cluster, specify the address and port of 3-5 nodes using this flag. |
| `--restful-port`       | RESTful service port. Default: `8080`, range: `[0, 65535]`.                                                                                                                                                                                                                                                                                                                                                                               |

#### Security Flags

| Flag         | Description                                                                                                                                                                                                                                                                                                                                                     |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--certs-dir`     | Path to the directory of security certificates for accessing and validating a secure cluster. <br> Default: `${HOME}/.kaiwudb-certs/`                                                                                                                                                                                                                              |
| `--insecure`      | Start the cluster in insecure mode. If not specified, the cluster starts in secure mode. See [Security](./cluster-planning.md#security) for risks of running in insecure mode. <br> Default: `false` |

#### Storage Flags

The `--store` flag supports the following configurations, separated by commas. Avoid using commas in configuration values.

::: warning Note

- Memory storage is not suitable for production environments.
- Without special replication constraints, KWDB rebalances replicas to utilize available storage space. However, in a 3-node cluster, if each node has multiple stores, KWDB cannot rebalance replicas from one store to another on the same node, as this would temporarily result in multiple replicas of the same range on that node. The rebalancing mechanism does not allow this. Under this mechanism, the cluster first deletes the target replica and then creates a copy of the replica at the target location. This means that to allow cross-store rebalancing, the cluster must have 4 or more nodes. This allows the cluster to create a copy of the replica on a node that doesn't already have a replica of that range before removing the source replica, and then migrate the new replica to the store with more capacity on the original node.

:::

| Configuration | Description |
| ------------- | ----------- |
| `type`        | Set to `mem` for memory storage (leave `path` empty). Otherwise, leave empty. |
| `path`        | Storage device path, for example, `--store=path=/mnt/ssd01,size=20GB`. <br> Default: `kaiwudb-data`. |
| `size`        | Maximum size allocated to the node. When the threshold is reached, KWDB attempts to redistribute data to other nodes with available capacity. If no other nodes have available capacity, the node will exceed the limit and continue using more space. Once new space becomes available in the cluster, data exceeding the threshold will be moved to the new available space. This value can be a percentage based on disk size or an exact value (in bytes). For example: <br>- `--store=path=/mnt/ssd01,size=10000000000` ----> 10,000,000,000 bytes<br> - `--store=path=/mnt/ssd01,size=20GB` ----> 20,000,000,000 bytes<br>- `--store=path=/mnt/ssd01,size=20GiB` ----> 21,474,836,480 bytes<br>- `--store=path=/mnt/ssd01,size=0.02TiB` ----> 21,474,836,480 bytes<br>- `--store=path=/mnt/ssd01,size=20%` ----> 20% of available space<br>- `--store=path=/mnt/ssd01,size=0.2` ----> 20% of available space<br>- `--store=path=/mnt/ssd01,size=.2` ----> 20% of available space<br> Default: 100% <br>For an in-memory store, the value is a percentage based on memory size or an exact value (in bytes), for example:<br>- `--store=type=mem,size=20GB`<br>- `--store=type=mem,size=90%`<br>**Note**: If using the percentage sign (`%`) format, ensure the system can correctly recognize the escaped percentage sign. In some configuration files, the percentage sign may be interpreted as a comment marker. Therefore, decimal values are recommended.|

#### Log Flags

By default, the system writes all information to log files and does not output anything to `stderr`.

| Flag                | Description                                                                                                                                                                                                                          |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `--log-dir`               | Enable logging and specify the log directory. Use `--log-dir=` (empty string) to disable logging.                                                                                                     |
| `--log-dir-max-size`      | When all log files reach the specified size, KWDB deletes the oldest log files. <br> Default: `100MiB`                                                                                                                                          |
| `--log-file-max-size`     | When a single log file exceeds the specified size, KWDB creates a new log file and begins writing logs to the new file. <br> Default: `10MiB`                                                                                                                                             |
| `--log-file-verbosity`    | Write only messages at or above the specified severity level to log files. For example, `--log-file-verbosity=WARNING`. <br> Default: `INFO`                                                                                                                                                                                        |
| `--logtostderr`           | Output messages at or above the specified severity level to `stderr`. For example, `--logtostderr=ERROR`. <br> - When no value is specified, KWDB outputs logs of all levels to `stderr`. <br> - When set to `--logtostderr=NONE`, logging to `stderr` is disabled.                                                                                                         |
| `--sql-audit-dir`         | Location for SQL audit logs. By default, SQL audit logs are written to the same directory as other KWDB logs. For more information, see [Audit Logs](../db-security/audit-mgmt.md#audit-logs).                                                                     |

### Startup Flag Configuration

The cluster startup flags can be modified using any of the following methods:

- The `kaiwudb_env` file for bare-metal deployments
- The `docker-compose.yml` file for container deployments
- The `kwbase start` command

This section explains how to modify the `kaiwudb_env` and `docker-compose.yml` files to change the startup flag configurations. For information on the `kwbase start` command, see [kwbase start](../tool-command-reference/client-tool/kwbase-sql-reference.md).

::: warning Note
Startup flags are node-level configurations. To modify the configuration for the entire cluster, you need to log into each node in the cluster and make the corresponding changes.
:::

To modify cluster startup flags, follow these steps:

1. Log into the cluster node to be modified and navigate to the KWDB installation directory.
2. Stop the KWDB service.

    ```shell
    systemctl stop kaiwudb
    ```

3. Navigate to the `/etc/kaiwudb/script` directory and open the configuration file.

    - For bare-metal deployment: open the `kaiwudb_env` file.
    - For container deployment: open the `docker-compose.yml` file.

4. Add or modify the startup flags in the configuration file as needed.

    - For bare-metal deployment:

        Add or modify the startup flags and their values after the startup command beginning with `KAIWUDB_START_ARG`.

        Example:

        The following example adds the `--cache` startup flag and sets the value to `25%`.

        ```yaml
        KAIWUDB_START_ARG="--cache=25%"
        ```

    - For container deployment:

        Add or modify startup flags and their values in the startup command beginning with `/kaiwudb/bin/`.

        ::: warning Note

        Do not remove the default startup command flags, as doing so may prevent the modified cluster from starting.

        :::

        Example:

        The following example adds the `--cache` startup flag and sets the value to `25%`.

        ```yaml
          command: 
            - /bin/bash
            - -c
            - |
              /kaiwudb/bin/kwbase start-single-node --certs-dir=<certs_dir> --listen-addr=0.0.0.0:26257 --advertise-addr=your-host-ip:port --store=/kaiwudb/deploy/kwdb-container --cache=25%
        ```

5. After saving the configuration, restart the KWDB service.

    ```shell
    systemctl restart kaiwudb
    ```

## Cluster Parameters

KWDB supports modifying cluster settings through the `SET CLUSTER SETTING` statement, which takes effect immediately.

::: warning Note

- Some cluster parameter settings affect the internal operations of KWDB. Before modifying parameter settings, it is strongly recommended to clearly understand the intended use of KWDB to avoid risks from setting changes.
- Only `admin` users can modify cluster parameter settings.

:::

The table below lists all cluster parameters supported by KWDB along with their default values. You can inspect current cluster configurations using the `SHOW CLUSTER SETTINGS` or `SHOW ALL CLUSTER SETTINGS` statements.

| Parameter                          | Description                                                                                                                                                                                                                                                                                                                                                                                                             | Default  | Type     |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------- |
| `audit.enabled`                     | Audit switch. | `FALSE`  | bool     |
| `audit.log.enabled`                 | Audit log switch. | `TRUE`   | bool     |
| `capacity.stats.period` | Period for KWDB to collect storage capacity statistics. The default value is 60, meaning storage capacity data is collected every 60 seconds. The supported range is [1, 1000]. Setting a higher value helps reduce system overhead, while a lower value helps obtain more real-time data. | `60` | int |
| `cloudstorage.gs.default.key`                           |  JSON key for Google Cloud Storage operations.                                                                                                                                                                                                                                                                                                                                                             | -         | string   |
| `cloudstorage.http.custom_ca`                           | Custom root CA to verify certificates when interacting with HTTPS storage, appended to the system's default CAs.                                                                                                                                                                                                                                                                                                                                                          | -         | string   |
| `cloudstorage.timeout`                                  | Timeout for import/export storage operations.                                                                                                                                                                                                                                                                                                 | `10m0s`     | duration |
| `cluster.organization`                                  | Organization name.                                                                                                                                                                                                                                                                                                                                                          | -         | string   |
| `cluster.preserve_downgrade_option`                     | Before reset, the system prohibits automatic or manual cluster upgrades from the specified version.                                                                                                                                                                                                                                                                                                                 | -         | string   |
| `default_transaction_read_only.enabled`                 | Read-only mode:<br>- `false`: Allow read and write operations, including DDL, DCL, and other cluster settings. <br>- `true`: Read-only mode; no write operations allowed, including DDL, DCL, and other cluster settings. | `FALSE`     | bool     |
| `diagnostics.forced_sql_stat_reset.interval`            | Time interval for the system to refresh SQL statement statistics, including uncollected SQL statement statistics. Maximum value is 24 hours. The value should be greater than the value of `diagnostics.sql_stat_reset.interval`. | `2h0m0s`    | duration |
| `diagnostics.reporting.enabled`                         | Whether to report diagnostic metrics to KWDB. | `TRUE`      | bool     |
| `diagnostics.reporting.interval`                        | Interval for reporting diagnostic data. | `1h0m0s`    | duration |
| `diagnostics.sql_stat_reset.interval`                   | Time interval for the system to reset SQL statement statistics. Maximum value is 24 hours. The value should be less than the value of `diagnostics.forced_sql_stat_reset.interval`. | `1h0m0s`    | duration |
| `external.graphite.endpoint`                            | When set to non-empty, push server metrics to the Graphite or Carbon server at the specified host and port. |           | string   |
| `external.graphite.interval`                            | Interval for pushing metrics to Graphite when metric pushing is enabled. | `10s`       | duration |
| `jobs.scheduler.enabled`                               | Enable or disable scheduled job functionality. Scheduled jobs are enabled by default. | `true`      | boolean  |
| `jobs.scheduler.max_jobs_per_iteration` | Maximum number of jobs to execute per scan. Default is 10. When set to 0, there is no job limit. | `10` | integer |
| `jobs.scheduler.pace`                                   | Frequency for scanning the `system.scheduled_jobs` task table. Default value is `60` seconds. The value cannot be less than `60s`. If set below `60s`, the default value of `60s` is used. | `60s`       | duration |
| `kv.allocator.load_based_lease_rebalancing.enabled`     | Rebalance range leases based on load and latency. | `TRUE`      | bool     |
| `kv.allocator.load_based_rebalancing`                   | Whether to rebalance based on QPS distribution across stores: <br>- `0`: Disable. <br>- `1`: Rebalance leases. <br>- `2`: Balance leases and replicas. | `2`         | enum     |
| `kv.allocator.qps_rebalance_threshold`                  | Minimum fraction between a store node's QPS and the average value to determine if the store node is overloaded or underloaded. | `0.25`      | float    |
| `kv.allocator.range_rebalance_threshold`                | Minimum fraction between a store's range count and the average value to determine if the store node is overloaded or underloaded. | `0.05`      | float    |
| `kv.allocator.ts_consider_rebalance.enabled`                | Controls automatic rebalancing for time-series data ranges. When enabled, the system automatically redistributes data after cluster scaling; when disabled, scaling does not trigger automatic redistribution. For scaling rebalancing, temporarily enable this parameter, wait for data rebalancing to complete, then disable it. | `true`      | bool    |
| `kv.allocator.ts_store_dead_rebalance.enabled`                | Controls automatic replica migration after node death. When enabled, the replica queue automatically performs replica migration, replacement, and replenishment based on node status; when disabled, replicas are not replenished even if a node dies. Note: In a 5-node three-replica cluster, disabling this feature will make it unable to tolerate consecutive node failures. | `true`      | bool    |
| `kv.bulk_io_write.max_rate`                             | Rate limit for bulk I/O write operations to disk. | `1.0 TiB`    | byte size |
| `kv.closed_timestamp.follower_reads_enabled`            | All replicas provide consistent historical reads based on closed timestamp information. | `TRUE`      | bool     |
| `kv.kvserver.ts_split_by_timestamp.enabled`            | Controls whether time-series data ranges are split by timestamp. When set to `false`, only hash points are used for splitting. When set to `true` and `kv.kvserver.ts_split_interval` is set to `1`, time-series data ranges are split based on both hash points and timestamps. | `FALSE`      | bool     |
| `kv.kvserver.ts_split_interval`            | Time-series data shard split interval. Default value is `10`. | `10`      | int     |
| `kv.protectedts.reconciliation.interval`                | Frequency for reconciling jobs through protected timestamp records. | `5m0s`      | duration |
| `kv.range_split.by_load_enabled`                        | Allow the system to automatically split ranges based on load concentration. | `TRUE`      | bool     |
| `kv.range_split.load_qps_threshold`                     | When QPS exceeds the specified threshold, the system automatically splits ranges based on load. | `2500`      | int      |
| `kv.rangefeed.enabled`                                  | Enable rangefeed registration. | `TRUE`      | bool     |
| `kv.replication_reports.interval`                       | Frequency for generating replication constraint statistics, replication statistics reports, and replication critical location information reports. | `1m0s`      | duration |
| `kv.snapshot_rebalance.max_rate`                        | Rate limit for rebalancing and replicating snapshots (in bytes per second). | `8.0 MiB`    | byte size |
| `kv.snapshot_recovery.max_rate`                         | Rate limit for recovering snapshots (in bytes per second). | `8.0 MiB`    | byte size |
| `kv.transaction.max_intents_bytes`                      | Maximum bytes for tracking locks in transactions. | `262144`    | int      |
| `kv.transaction.max_refresh_spans_bytes`               | Maximum bytes for tracking refresh spans in serializable transactions. | `256000`    | int      |
| `log.sync.enabled` | Controls whether log synchronization operations are performed. Default is `true`, enabling log synchronization. When disks are busy, log synchronization operations may trigger timeout thresholds, causing the database to actively shut down. Disabling synchronization operations can prevent database process crashes due to log synchronization timeouts. | `true` | bool |
| `server.auth_log.sql_connections.enabled`               | When set to `TRUE`, the system logs SQL client connection and disconnection events, which may affect performance on heavily loaded nodes. | `FALSE`     | bool     |
| `server.auth_log.sql_sessions.enabled`                  | When set to `TRUE`, the system logs SQL session login and disconnection events, which may affect performance on heavily loaded nodes. | `FALSE`     | bool     |
| `server.clock.forward_jump_check_enabled`               | When set to `TRUE`, clock jumps greater than `max_offset/2` will cause an emergency. | `FALSE`     | bool     |
| `server.clock.persist_upper_bound_interval`             | Interval for persisting the clock wall upper bound. The clock will not generate wall times greater than the persisted timestamp during this period. If the system sees a wall time greater than this value, it will trigger an emergency. KWDB waits for the wall time to catch up to the persisted timestamp on startup. This ensures monotonic wall time on server restart. Not setting this value or setting it to `0` disables this feature. | `0s`        | duration |
| `server.consistency_check.max_rate`                     | Rate limit for consistency checks (in bytes per second). Used together with `server.consistency_check.interval` to control the frequency of consistency checks. This may affect performance. | `8.0MiB`    | byte size |
| `server.eventlog.ttl`                                   | If nonzero, event log entries older than this duration are deleted every 10 minutes. The value should not be set below 24 hours. | `2160h0m0s` | duration |
| `server.host_based_authentication.configuration`        | Host-based authentication configuration. | -         | string   |
| `server.rangelog.ttl`                                   | If nonzero, range log entries older than this duration are deleted every 10 minutes. The value should not be set below 24 hours. | `720h0m0s`  | duration |
| `server.remote_debugging.mode`                          | Used to enable or disable remote debugging. <br>- `local`: Enable remote debugging locally only. <br>- `any`: Allow remote debugging from anywhere. <br>- `off`: Disable remote debugging. | `local`     | string   |
| `server.rest.timeout`                                   | RESTful API connection timeout threshold. After exceeding this threshold, the system will disconnect the session. Default is `60` minutes, with a range of `[1, 2^63-1]` minutes. | `60`        | int      |
| `server.restful_service.default_request_timezone` | Global control for RESTful API timezone information. Value range is -12 to 14. | `8` | int |
| `server.shutdown.drain_wait`                            | When shutting down the server, the time the server waits in an unready state. | `0s`        | duration |
| `server.shutdown.lease_transfer_wait`                   | When shutting down the server, the time the server waits for range lease transfer to complete. | `5s`        | duration |
| `server.shutdown.query_wait`                            | When shutting down the server, the time the server waits for active queries to complete. | `10s`       | duration |
| `server.sql_connections.max_limit`                            | Maximum number of connections per node. Default is set to `200`, with a supported range of [4, 10000]. When the planned number of client connections exceeds this value, this parameter can be adjusted appropriately to meet the connection needs of more clients. | `200`       | int |
| `server.time_until_store_dead`                          | If a node does not send updates via the Gossip protocol within the specified time, the system marks it as a dead node. | `30m0s`      | duration |
| `server.tsinsert_direct.enabled`                             | Enable time-series write short-circuiting to improve write performance. | `true`       | bool |
| `server.user_login.timeout`                             | When a system range is unavailable, client authentication will timeout after the set time. | `10s`       | duration |
| `server.web_session_timeout`                            | Duration that newly created web sessions remain valid in the system. | `168h0m0s`  | duration |
| `sql.all_push_down.enabled`                             | Push down all SQL operations. | `TRUE`      | bool     |
| `sql.auto_limit.quantity` | Configure the number of rows returned by SQL queries. Supported values: <br>- `0`: No limit on the number of rows returned by SQL queries. <br>- Any positive integer greater than 0: Limits the number of rows returned by SQL queries to the configured value. | `0` | int |
| `sql.defaults.default_int_size`                         | Size of the INT data type (in bytes). | `8`         | int     |
| `sql.defaults.idle_in_session_timeout` | Configure the timeout for idle sessions. If set to `0`, the session will not timeout. | `0s` | duration |
| `sql.defaults.results_buffer.size`                      | Server-side buffer size for accumulating statement results or batch results before sending to the client. Can be overridden by specifying the `results_buffer_size` parameter for a connection. Auto-retries only occur if results have not yet been delivered to the client. Reducing the buffer size may cause clients to receive more retriable errors. Increasing the buffer size may increase client wait time before receiving the first result row. Updates only affect new connections. Setting to `0` disables any buffering. | `16 KiB`     | byte size     |
| `sql.defaults.multimodel.enabled` | Configure multi-model query optimization. When enabled, the system recognizes multi-model queries and generates corresponding query plans. | `true` | bool |
| `sql.defaults.serial_normalization`                     | Default handling of SERIAL data types in table definitions `[rowid = 0,virtual_sequence = 1,sql_sequence = 2]`. | `rowid`     | enum      |
| `sql.distsql.max_running_flows`                         | Maximum number of concurrent flows that can run on a node. | `500`       | int     |
| `sql.distsql.temp_storage.joins`                        | When set to `TRUE`, disk will be used in distributed SQL sorts. <br> **Note** <br> Disabling this setting may affect memory usage and performance. | `TRUE`      | bool     |
| `sql.distsql.temp_storage.sorts`                        | When set to `TRUE`, disk will be used in distributed SQL sorts. <br> **Note** <br> Disabling this setting may affect memory usage and performance. | `TRUE`      | bool     |
| `sql.log.slow_query.latency_threshold`                  | If nonzero, when SQL statement latency exceeds the specified threshold, the system will log the statement in each node's secondary logger. | `0s`        | duration      |
| `sql.metrics.statement_details.dump_to_logs`            | When periodically clearing data, write collected statement statistics to node logs. | `FALSE`     | bool     |
| `sql.metrics.statement_details.enabled`                 | Collect query statistics for each statement. | `TRUE`      | bool     |
| `sql.metrics.statement_details.plan_collection.enabled` | Periodically save the logical plan for each fingerprint. | `TRUE`      | bool |
| `sql.metrics.statement_details.plan_collection.period`  | Time interval between collecting new logical execution plans. | `5m0s`      | duration |
| `sql.metrics.statement_details.threshold`               | Minimum execution time required to trigger statistics collection. | `0s`        | duration     |
| `sql.metrics.transaction_details.enabled`               | Collect transaction statistics for each application. | `TRUE`      | bool     |
| `sql.notices.enabled`                                   | Allow sending notices in the server/client protocol. | `TRUE`      | bool     |
| `sql.stats.automatic_collection.enabled`                | Automatic statistics collection mode. | `FALSE`     | bool     |
| `sql.stats.automatic_collection.fraction_stale_rows`    | Percentage of stale rows per table that triggers statistics refresh. | `0.2`       | float    |
| `sql.stats.automatic_collection.min_stale_rows`         | Minimum number of stale rows per table that triggers statistics refresh. | `500`       | int      |
| `sql.stats.histogram_collection.enabled`                | Histogram collection mode. | `TRUE`      | bool     |
| `sql.stats.post_events.enabled`                         | When enabled, an event record is generated each time a statistics job is created. | `FALSE`     | bool     |
| `sql.stats.ts_automatic_collection.enabled`             | Automatic time-series data statistics collection mode. | `false`     | bool     |
| `sql.temp_object_cleaner.cleanup_interval`              | Frequency for cleaning up orphaned temporary objects. | `30m0s`      | duration     |
| `sql.trace.log_statement_execute`                       | When set to `TRUE`, enable logging of statement execution. | `FALSE`     | bool      |
| `sql.trace.session_eventlog.enabled`                    | When set to `TRUE`, enable session tracing. This may significantly affect performance. | `FALSE`     | bool     |
| `sql.trace.txn.enable_threshold`                        | When a transaction's execution time exceeds the specified duration, the system will trace the transaction. Setting to `0` disables this feature. | `0s`        | duration     |
| `sql.ts_insert_select.block_memory`                       | Memory limit for data blocks per write in time-series `INSERT INTO SELECT` statements. | `200`       | int      |
| `sql.ts_insert_select_limit.enabled`                    | Allow time-series data to be written to relational tables. | `FALSE`     | bool     |
| `sql.txn.cluster_transaction_isolation` | Configure transaction isolation level. Supported values: <br>- `serializable`: The highest isolation level, ensuring that even when transactions are executed in parallel, the results are the same as if they were executed one at a time, without any concurrency. <br>- `read committed` (RC): At the RC isolation level, transactions read data that has been committed by other transactions, but do not fully guarantee serializability of transaction operations. <br>- `repeatable read` (RR): RR isolation guarantees that multiple reads of the same data within the same transaction return consistent results. | `serializable` | enum |
| `timeseries.storage.enabled`                            | Whether to store periodic time-series data within the cluster. Unless data is already stored elsewhere, disabling this feature is not recommended. | `TRUE`      | bool     |
| `timeseries.storage.resolution_10s.ttl`                 | Maximum retention time for time-series data stored at 10-second resolution. Data older than this will be aggregated and deleted. | `240h0m0s`  | duration |
| `timeseries.storage.resolution_30m.ttl`                 | Maximum retention time for time-series data stored at 30-minute resolution. Data older than this will be aggregated and deleted. | `2160h0m0s` | duration |
| `trace.debug.enable`                                    | When set to enabled, trace information for recent requests can be viewed on the `/debug` page. | `FALSE`     | bool     |
| `trace.lightstep.token`                                 | When set to enabled, trace data will be sent to Lightstep using the specified token. | -         | string   |
| `trace.zipkin.collector`                                | When set to enabled, trace data will be sent to the specified Zipkin instance, e.g., `127.0.0.1:9411`. This configuration is ignored if `trace.lightstep.token` is set. | -         | string   |
| `ts.auto_vacuum.enabled` | Controls whether to enable data reorganization. When set to `true`, the feature is enabled. | `TRUE` | bool |
| `ts.block.lru_cache.max_limit`                         | Sets the maximum memory size for the node's time-series block LRU (Least Recently Used) cache, in bytes. This cache optimizes time-series data query performance by caching hot data blocks to reduce disk I/O operations. When the cache reaches the maximum limit, the least recently used data blocks will be evicted according to the LRU policy. <br>Default is `1073741824` (1GB). Setting to `0` disables the block cache. <br>It is recommended to adjust based on the node's actual available memory. Increasing the value can improve query performance, but excessively large values may lead to out-of-memory (OOM) errors. | `1073741824`       | int      |
| `ts.count.use_statistics.enabled`  | Enables query optimization for `count(*)` operations on time-series data by using the count of previously written rows. Enabled by default. Disabling this option may reduce `count(*)` query performance. | `true`   | bool |
| `ts.compact.max_limit`  | Controls the maximum number of last segments processed in a single compaction operation. When a compaction operation is triggered, the system merges data from multiple last segments into entity segments. <br>This parameter controls the resource consumption of compaction operations. Reducing this value can decrease the workload of a single compaction, reducing CPU and I/O peak pressure, but requires more compaction operations to process all data. Increasing this value can improve single compaction efficiency and reduce the number of compactions, but will increase the resource consumption and execution time of a single operation. | `10`   | int |
| `ts.dedup.rule`                                         | Data deduplication strategy. Supports the following parameters: <br>- `override`: Full row deduplication; later written data overwrites existing data with the same timestamp. <br>- `discard`: Ignore newly written duplicate data and keep existing data. When duplicate data write fails, the client receives the count of successfully and unsuccessfully inserted data as a notice. <br>- `keep`: Allow duplicate data to be written without deduplication. Currently only supported in single-node deployment. | `override`  | string   |
| `ts.mem_segment_size.max_limit`  | Controls the maximum size of a mem segment within a single VGroup. The mem segment is the buffer for data written to memory. When its size reaches this limit, it triggers a data persistence operation that writes the in-memory data to the last segment on disk.<br>This parameter balances memory usage and flush frequency. Decreasing this value accelerates data persistence and reduces memory usage, but increases disk I/O operations. Increasing this value reduces persistence frequency and disk I/O overhead, but increases memory usage and potential data loss risk (more unwritten data at risk during failures).                                                                                 | `536870912`   | byte size |
| `ts.ordered_table.enabled`| Controls the default sort order for queries without an `ORDER BY` clause. When enabled, results are returned in reverse chronological order based on data ingestion timestamp. For single-device queries, results are sorted by timestamp (newest first). For multi-device queries, each device's data is sorted individually, then merged. | `false` | bool |
| `ts.parallel_degree`| Number of time-series query tasks that can execute in parallel on a single node, ranging from [0, cpu_core*2+2], where `cpu_core` is the number of logical processors actually in use. When set to `0` or `1`, the system executes queries serially; values greater than `1` indicate the number of tasks that can run in parallel. | `0` | int |
| `ts.partition.interval`                                 | Data partition interval. Must be set to a value greater than `0`.                                                                                                                                                                                                                                                                                                                                                                                           | `864000`    | int      |
| `ts.raft_log.sync_period` | Time-series data raft log flush period. The default `10s` means forced sync to disk every 10 seconds. Setting to `0s` enables real-time flushing, while non-zero values trigger forced sync at specified intervals. Longer flush periods improve write performance, but if a node stops unexpectedly, up to one period's worth of data may be lost. Suitable for high-performance scenarios with relatively lower data consistency requirements. | `10s` | duration |
| `ts.raftlog_combine_wal.enabled` | Enables merged raft log and WAL (Write-Ahead Log) for time-series data, reducing write amplification and improving write performance.| `false` | bool |
| `ts.reserved_last_segment.max_limit`                           | Controls the maximum number of last segments retained per partition. When the number of last segments exceeds this limit, the Compact thread automatically triggers a data merge operation that consolidates device data meeting row count thresholds from last segments into entity segments in columnar compressed format, optimizing storage space and improving query performance.<br>This parameter balances memory usage and data persistence efficiency, preventing excessive resource consumption from too many last segments.                                                                                                                                                                                                                        | `3`      | int      |
| `ts.rows_per_block.max_limit`                           | Controls the maximum number of rows a single block can hold in an entity segment, preventing individual blocks from becoming too large and degrading read efficiency.<br>This parameter balances storage density and query performance. Increasing this value improves compression ratios and saves storage space (suitable for storage-priority scenarios). Decreasing it reduces the amount of data scanned per query, improving query response times (suitable for query-priority scenarios).                                                                                                                                                                                                                             | `4096`      | int      |
| `ts.rows_per_block.min_limit`                           | Controls the minimum number of rows a single block can hold in an entity segment, serving as the row count threshold that triggers data merging from last segment to entity segment.<br>This parameter ensures each block contains sufficient data rows to improve compression efficiency and storage density, avoiding excessive small blocks that lead to file fragmentation and increased metadata overhead.<br>Increasing this value reduces block count and metadata overhead but prolongs data merge time. Decreasing it accelerates data persistence but may generate more small blocks, increasing file fragmentation.                                                                                                                                             | `512`      | int      |
| `ts.sql.query_opt_mode` | Controls cross-model query optimization features using a 4-digit integer bitmask, where each digit enables (1) or disables (0) a specific optimization:<br><br>- **1st digit**: Multi-predicate order optimization<br>- **2nd digit**: Scalar subquery optimization<br> - **3rd digit**: Inside-out pushdown aggregate optimization<br>- **4th digit**: Inside-out pushdown time_bucket optimization<br><br>**Default value**: `1110` (first three optimizations enabled)<br><br>**Note**: When enabled, the database automatically determines whether a query qualifies for optimization. Not all queries can be optimized; only those meeting specific criteria will benefit from these features. | `1110` | int  |
| `ts.stream.max_active_number` | Maximum number of streaming computation instances in running state.| `10` | int32 |
| `ts.table_cache.capacity` | Controls the number of cached time-series tables, supporting a range of [1,2147483647]. The default value of `1000` means 1000 time-series tables can be cached without needing reinitialization. To cache more time-series tables, increase this value to improve read/write performance. Note that larger values may consume more memory.| `1000` | int |
| `ts.wal.checkpoint_interval` | Time-series WAL checkpoint execution interval, controlling the time interval for flushing time-series data from memory to disk.  | `1m`      | duration        |
| `ts.wal.wal_level`               | Time-series WAL write level. Options:<br>- `0` (`off`): Disables WAL, recovers data state via time-series storage engine interface on restart<br>- `1` (`sync`): Logs are written to disk in real-time with forced persistence, providing highest safety but relatively lower performance<br>- `2` (`flush`): Logs are written to file system buffer, balancing performance and safety<br>- `3` (`byrl`): Uses raft log to ensure data consistency, WAL only for metadata consistency | `1` | integer        |