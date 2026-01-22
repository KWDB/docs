---
title: 集群参数配置
id: cluster-settings-config
---

# 集群参数配置

部署 KWDB 集群后，用户可以通过修改**启动参数**、**环境变量**或**实时集群参数**，自定义集群配置：

|<div style="width: 70px;">**参数类型**</div>     | **影响范围**                                      | **生效方式**                                | **配置方式**                                                 |
| :--------------- | :---------------------------------------------- | :------------------------------------------ | :----------------------------------------------------------- |
| **启动参数**     | 作用于集群节点，影响单个节点的数据库服务。            | 仅在节点启动时生效，修改后需重启服务。       | 修改裸机部署的 `kaiwudb_env` 文件、容器部署的 `docker-compose.yml` 文件。其中，`kaiwudb_env` 和 `docker-compose.yml` 文件均位于 `/etc/kaiwudb/script/`。 |
| **环境变量** | 操作系统级别的参数，影响用户或操作系统级别下所有数据库实例的行为。  | 仅在数据库进程启动时读取，修改后需要重启服务才能生效。 | 可以在系统或用户级的 shell 配置文件（如 .bashrc 或 .bash_profile）中配置，或在系统服务（如 systemd）中配置。 |
| **实时集群参数** | 作用于整个集群，影响集群内所有的节点。  | 实时生效，并自动同步至集群各节点，无需重启服务。 | 通过 SQL 语句修改，变更将持久化至系统表。 |

## 启动参数

### 参数说明

集群的启动参数包括通用、网络、安全、日志等参数。

::: warning 注意

- 大部分集群启动参数都设有默认值。用户可以显式指定集群参数的取值来覆盖默认值。除 `--join` 参数以外，其他参数的指定值都是非持久化的操作，每次重新启动节点时都需要重新配置指定值。`--join` 参数的指定值存储在节点的数据文件中。推荐每次启动 KWDB 时重新配置`--join` 参数，以便在数据文件丢失时节点也能够加入集群并进行恢复。
- 重启系统后，新的启动参数配置才能生效。

:::

#### 通用参数

| 参数              | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--background`      | 设置后台运行。<br > **说明** <br > `--background` 参数适用于短时间运行和测试服务的场景。目前，由于无法从当前终端完全分离，不推荐在长时间的服务运行中使用该参数。这种情况下，推荐使用服务管理器或者 daemon(8) 等工具。                                                                                                                                                                                                                                                                                                                                               |
| `--cache`           | 缓存大小，多个物理存储设备共享使用。参数值支持准确的内存值（单位：字节）、带小数点的十进制数值（转换为百分比数值）、百分比值：<br >- `--cache=.25` <br >- `--cache=25%` <br >- `--cache=1000000000`：1000000000 字节 <br >- `--cache=1GB`：1000000000 字节 <br >- `--cache=1GiB`：1073741824 字节 <br >**说明** <br > 如果使用带百分比符号（%）的格式，确保系统能够正常识别转义的百分比符号（%）。例如，在某些配置文件中，百分比符号（%）可能被识别为注解符。因此，推荐使用带小数点的十进制数值。<br >默认值为 128 MiB。默认值的设置是基于本地部署集群的场景考虑。在实际生产环境中，推荐 `25%` 甚至更高。 |
| `--external-io-dir` | 使用本地节点目录或 NFS 驱动器执行备份和恢复操作时，使用本地文件访问路径作为前缀的外部 IO 文件夹路径。设置为 `disabled` 时，表示使用本地节点目录备份和恢复数据，禁止 NFS 驱动。<br > 默认值：第一个 `--store` 参数配置的 `extern` 子目录，用户可以对 `extern` 目录进行文件符号连接，以达到不重启节点就能够变更 `--extern-io-dir` 的目的。                                                                                                                                                                                                                         |
| `--max-sql-memory`  | SQL 查询缓存的临时数据支持使用的最大内存空间，包括准备好的查询和在查询执行期间中间数据行。该值可以是带小数点的十进制数值（转换为百分比数值）、百分比值，或者准确的值（单位：字节），例如：<br >- `--max-sql-memory=.25` <br >- `--max-sql-memory=25%` <br >- `--max-sql-memory=10000000000`：1000000000 字节 <br >- `--max-sql-memory=1GB`：1000000000 字节 <br >- `--max-sql-memory=1GiB`：1073741824 字节。<br > 这些临时文件存储在 `--temp-dir` 文件夹当中。<br >**说明** <br > 如果使用带百分比符号（%）的格式，确保系统能够正常识别转义的百分比符号（%）。例如，在某些配置文件中，百分比符号（%）可能被识别为注解符。因此，推荐使用带小数点的十进制数值。                   |
| `--store` <br >`-s`         | 存储设备路径，用于存储数据库数据。支持同时指定设备属性和空间大小。若使用多个设备存储数据，则使用 `--store=/mnt/ssd01 --store=/mnt/ssd02` 方式。更多详细信息，参见[存储参数](#存储参数)。                                                                                                                                                                                                                                                                                                                                                                |

#### 网络参数

| 参数             | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--advertise-addr` | 节点使用的 IP 地址或主机名，与其他节点通过该地址进行通信。如果是主机名，则要求能正常解析地址。如果是 IP 地址，则要求能正常访问 IP 地址。对于 IPv6，使用 `[...]` 表示法，例如：`[::1]` 或 `[fe80::f6f2:::]`。<br >参数的效果取决于与 `--listen-addr` 参数的组合使用。例如，如果端口号与`--listen-addr` 参数中使用的端口号不同，则需要端口转发。<br >默认值：`--listen-addr` 参数的取值。如未指定 `--listen-addr` 参数，默认主机名和端口为：`canonical hostname`（`/etc/host` 第二列）和 `26257`。 |
| `--brpc-addr`            | 指定时序引擎间的 brpc 通信地址，格式为 `<host>:<port>` 或 `:<port>`: <br>- 必须包含端口号，否则系统会报错 `failed to start server: --brpc-addr's port not specified`。<br>- IP 地址可省略，若未指定，系统将依次使用 `--advertise-addr` 或 `--listen-addr` 的 IP。<br>**说明**<br>`--advertise-addr` 与 `--brpc-addr` 均为节点间通信地址，因此需确保各节点间网络互通。推荐使用 `--brpc-addr=:<port>` 格式，由系统自动获取 IP 地址。|
| `--listen-addr`    | 侦听来自其他节点和客户端连接的 IP 地址/主机名和端口。IPv6 地址使用 `[...]` 表示法，例如：`[::1]` 或 `[fe80::f6f2:::]`。参数的效果取决于与  `--advertise-addr` 参数的组合使用。<br > 默认值：侦听所有 IP 地址，端口为 `26257`。如未指定 `--advertise-addr` 参数，使用 `canonical hostname` 与其他节点进行通信。                                                                                                                                                      |
| `--http-addr`      | 对外开放的 Admin 界面的 IP 地址或主机名。IPv6 地址使用 `[...]` 表示法，例如：`[::1]:8080` 或 `[fe80::f6f2:::]:8080`。<br > 默认值：与 `--listen-addr` 参数一致，端口为 `8080`。                                                                                                                                                                                                                                                                                               |
| `--join` <br >`-j`         | 节点连接集群的地址。初始化时，需要指定集群 3-5 个节点的地址和端口，然后执行 `kwbase init` 命令启动集群。如未指定该参数时，则启动一个单节点集群。此时，无需执行 `kwbase init` 命令。如需向已有集群添加新节点，支持使用该参数指定集群 3-5 个节点的地址和端口。|
| `--restful-port`   | RESTful 端口，默认值为 `8080`，取值范围为 `[0, 65535]`。|

#### 安全参数

| 参数        | 描述                                                                                                                                                                                                                                                                                                                                     |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--certs-dir` | 安全证书目录的路径，用于访问、验证以安全模式部署的集群。<br >默认值：`${HOME}/.kaiwudb-certs/`                                                                                                                                                                                                                                                 |
| `--insecure`  | 以非安全模式启动集群。如未指定，以安全模式启动集群。有关以非安全模式启动集群的风险，参见[安全性](./cluster-planning.md#安全性)。<br >默认值：`false` |

#### 存储参数

`--store` 参数支持以下配置项，配置项之间使用逗号（`,`）隔开。用户需要在配置项的值当中避免使用逗号（`,`）。

::: warning 注意

- 内存存储不适合在生产部署环境中使用。
- 在没有特殊复制约束的情况下，KWDB 会重新平衡副本以利用可用的存储空间。但是，在 3 节点集群中，如果每个节点具有多个存储，KWDB 不能将副本从一个存储重新平衡到同一节点上的另一存储中。因为这会导致该节点暂时具有相同 Range 的多个副本。重新平衡机制不允许发生这种情况。在该机制下，集群会先删除目标副本，然后再在目标位置创建副本的副本。也就是说，要允许跨存储区的重新平衡，集群必须具有 4 个及以上节点。这样，集群在删除源副本之前，在尚未具有该 Range 副本的节点上创建副本的副本，然后将新副本迁移到原始节点中空间更大的存储中。

:::

| 配置项 | 简介 |
| --- | --- |
| `type`   | 如果是内存存储，则应设置为 `mem`。`path` 配置项取值为空。其他情况下，该值应为空。 |
| `path`   | 存储设备路径，例如：`--store=path=/mnt/ssd01,size=20GB`。<br > 默认值：`kaiwudb-data`|
| `size`   | 存储设备允许节点使用的最大空间。达到此阈值时，KWDB 尝试将数据重新散布到具有可用容量的其他节点。当其他节点没有可用容量时，该节点将无视该限制，继续使用更多空间。一旦集群有其他新的可用空间，则该节点超出阈值的数据将转移到新的可用空间上。该参数值可以是基于硬盘大小的百分数或者准确的值（单位：字节），例如：<br >- `--store=path=/mnt/ssd01,size=10000000000`：10000000000 字节 <br >- `--store=path=/mnt/ssd01,size=20GB`：20000000000 字节 <br >- `--store=path=/mnt/ssd01,size=20GiB`：21474836480 字节 <br >- `--store=path=/mnt/ssd01,size=0.02TiB`：21474836480 字节 <br >- `--store=path=/mnt/ssd01,size=20%`：20% 的可用存储空间 <br >- `--store=path=/mnt/ssd01,size=0.2`：20% 的可用存储空间 <br >- `--store=path=/mnt/ssd01,size=.2`：20% 的可用存储空间 <br > 默认值：100% <br >若是内存存储，则该值是基于内存大小的百分数或是准确的值（单位：字节），例如：<br >- `--store=type=mem,size=20GB` <br >- `--store=type=mem,size=90%`  <br >**说明** <br > 如果使用带百分比符号（%）的格式，确保系统能够正常识别转义的百分比符号（%）。例如，在某些配置文件中，百分比符号（%）可能被识别为注解符。因此，推荐使用带小数点的十进制数值。 |

#### 日志参数

默认情况下，系统将所有信息打印到日志文件中，不向 stderr 输出任何内容。

| 参数                 | 描述                                                                                                                                                                                               |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--log-dir`            | 启动日志功能并在指定的目录下记录日志。`--log-dir` 配置为空字符串（`--log-dir=`）时，表示关闭日志功能。                                                                                                 |
| `--log-dir-max-size`   | 所有日志文件大小达到阈值以后，KWDB 将删除最老的日志。<br >默认值：`100MiB`                                                                                                                        |
| `--log-file-max-size`  | 单个日志文件大小达到阈值以后，KWDB 创建新的日志文件并输出日志到新文件。<br >默认值：`10MiB`                                                                                                 |
| `--log-file-verbosity` | 讲指定日志级别及以上的日志输出到日志文件，例如：`--log-file-verbosity=WARNING`。 <br > 默认值：`INFO`                                                                                                  |
| `--logtostderr`        | 将指定日志级别及以上的日志输出到 stderr，例如 `--logtostderr=ERROR`。  <br > - 当未指定参数取值时，KWDB 将所有级别的日志输出到 stderr。<br > - 当配置为 `--logtostderr=NONE` 时，表示禁止输出日志到 stderr。 |
| `--sql-audit-dir`     | 安全审计日志的位置。默认情况下，SQL 审核日志与 KWDB 生成的其他日志写入同一目录。有关更多信息，参见[审计日志](../db-security/audit-mgmt.md#审计日志)。                                                                     |

### 启动参数配置

启动参数支持以下配置方式：

- 修改裸机部署的 `kaiwudb_env` 文件
- 修改容器部署的 `docker-compose.yml` 文件
- 使用 `kwbase start` 命令

本节介绍如何通过`kaiwudb_env` 或`docker-compose.yml` 文件修改启动参数配置，`kwbase start` 命令相关信息，参见[kwbase start](../tool-command-reference/client-tool/kwbase-sql-reference.md)。

::: warning 提示
启动参数是节点级别的配置。如需修改整个集群的配置，需要登录到集群中的每个节点并完成相应的参数配置。
:::

如需修改集群启动参数配置，遵循以下步骤。

1. 登录集群中待修改的节点，进入 KWDB 安装包目录。
2. 停止 KWDB 服务。

    ```shell
    systemctl stop kaiwudb
    ```

3. 打开配置文件。

    - 裸机部署：进入 `/etc/kaiwudb/script` 目录，打开 `kaiwudb_env` 文件。
    - 容器部署：进入 `/etc/kaiwudb/script` 目录，打开 `docker-compose.yml` 文件。

4. 根据需要添加或者修改配置文件中的启动命令参数。

    - 裸机部署：在 `KAIWUDB_START_ARG` 开头的启动命令后添加或者修改启动参数和参数值。

        配置示例：

        以下示例添加 `--cache` 启动参数，并肩参数值设置为 `25%`。

        ```yaml
        KAIWUDB_START_ARG="--cache=25%"
        ```

    - 容器部署：在 `/kaiwudb/bin/` 开头的启动命令后添加或者修改启动参数和参数值。

        ::: warning 注意

        请勿删除默认启动命令参数，否则可能导致无法启动修改后的集群。

        :::

        配置示例：

        以下示例添加 `--cache` 启动参数，并肩参数值设置为 `25%`。

        ```yaml
          command: 
            - /bin/bash
            - -c
            - |
              /kaiwudb/bin/kwbase  start-single-node --certs-dir=<certs_dir> --listen-addr=0.0.0.0:26257 --advertise-addr=your-host-ip:port --store=/kaiwudb/deploy/kwdb-container --cache=25%
        ```

5. 保存配置后，重新启动 KWDB 服务。

    ```shell
    systemctl restart kaiwudb
    ```

## 环境变量

### 参数说明

环境变量是操作系统级别的参数，影响用户或操作系统级别下所有数据库实例的行为。

要查看当前的 KWDB 配置和其他环境变量，请运行 `env` 命令。节点启动时使用的环境变量会被打印到节点日志中。

KWDB 配置的优先级顺序(从高到低)为：

- 启动参数
- 环境变量
- 默认值

下表列出了目前支持配置的环境变量：

| 参数名称 | 说明 | 默认值 |
|---------|------|--------|
| `KWBASE_ENABLE_FOLLOWER_READ` | 控制是否允许从多副本集群数据分片(range)的 follower 副本中读取数据。<br><br>集群发生严重故障，存活节点数少于副本总数的一半且无法恢复故障节点时，可通过启用该参数连接存活节点，从 follower 副本中查询时序和关系数据。<br><br>**注意**:<br>- 启用后会影响写入功能，**正常运行的集群不应启用此参数**<br>- 由于副本间数据同步可能存在延迟，从 follower 副本读取的数据可能慢于 leaseholder 副本，不适用于强一致性要求的场景<br>- 仅能查询存活节点上的数据，未在存活节点分布的数据无法访问<br>- 对于超过 5 节点的集群，由于元数据默认副本数为 5，存活节点重启后可能无法正常查询 | `false` |

### 环境变量配置

::: warning 提示
环境变量是节点级别的配置。如需修改整个集群的配置，需要在集群的每个节点上分别完成配置。
:::

步骤：

1. 登录待修改环境变量的集群节点，停止 KWDB 服务。

    ```shell
    systemctl stop kaiwudb
    ```

2. 设置环境变量：

    ```bash
    export KWBASE_ENABLE_FOLLOWER_READ=true
    ```

3. 重新启动 KWDB 服务。

    ```shell
    systemctl start kaiwudb
    ```

## 实时参数

KWDB 支持通过 `SET CLUSTER SETTING` 语句修改集群设置，设置后立即生效。

::: warning 注意

- 一些集群参数的设置会影响 KWDB 的内部运行机制。修改参数设置前，强烈建议明确使用 KWDB 的目的，以免因修改设置带来风险。
- 只有 `admin` 角色成员可以更改集群参数设置。

:::

下表列出 KWDB 支持设置的所有集群参数及默认值。用户可以使用 `SHOW CLUSTER SETTINGS` 或 `SHOW ALL CLUSTER SETTINGS` 语句查看当前集群的所有参数及配置值。

| 参数                                                  | 描述                                                                                                                                                                                                                                                                                                                                                                                                                       | 默认值    | 类型     |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | -------- |
| `audit.enabled`                                         | 审计开关。                                                                                                                                                                                                                                                                                                                                                                                                                   | `FALSE`     | bool     |
| `audit.log.enabled`                                     | 审计日志文件记录开关。                                                                                                                                                                                                                                                                                                                                                                                                       | `TRUE`      | bool     |
| `capacity.stats.period`                                 | KWDB 统计存储容量数据的周期。默认值为 `12`，表示每 120 秒统计一次存储容量数据。支持设置的范围为 [1, 1000]。设置较高的值有助于减少系统开销，较低的值有助于获取更实时的数据。 | `12` | int |
| `cloudstorage.gs.default.key`                           | Google Cloud Storage 操作的 JSON 密钥。                                                                                                                                                                                                                                                                                                                                                                                      | -         | string   |
| `cloudstorage.http.custom_ca`                           | 与 HTTPS 存储交互时，验证证书的自定义根 CA，附加到系统的默认 CA。                                                                                                                                                                                                                                                                                                                                                              | -         | string   |
| `cloudstorage.timeout`                                  | 导入导出存储操作的超时时间。                                                                                                                                                                                                                                                                                                                                                                                                 | `10m0s`     | duration |
| `cluster.organization`                                  | 组织名称。                                                                                                                                                                                                                                                                                                                                                                                                                   | -         | string   |
| `cluster.preserve_downgrade_option`                     | 重置前，系统禁止从指定版本自动或手动升级集群版本。                                                                                                                                                                                                                                                                                                                                                                           | -         | string   |
| `default_transaction_read_only.enabled`                 | 只读模式<br >- `false`：可以读写，包括 DDL、DCL 和其他集群设置。 <br >- `true`：表示只能读不能写，包括 DDL、DCL 和其他集群设置。                                                                                                                                                                                                                                                                                                                                        | `FALSE`     | bool     |
| `diagnostics.forced_sql_stat_reset.interval`            | 系统刷新 SQL 语句统计信息的时间间隔，包括未收集的 SQL 语句统计信息。最大值为 24 小时。设置值应大于 `diagnostics.sql_stat_reset.interval` 参数的取值。                                                                                                                                                                                                                                                                                   | `2h0m0s`    | duration |
| `diagnostics.reporting.enabled`                         | 向 KWDB 报告诊断指标。                                                                                                                                                                                                                                                                                                                                                                                               | `TRUE`      | bool     |
| `diagnostics.reporting.interval`                        | 报告诊断数据的间隔。                                                                                                                                                                                                                                                                                                                                                                                                         | `1h0m0s`    | duration |
| `diagnostics.sql_stat_reset.interval`                   | 系统重置 SQL 语句统计信息的时间间隔。最大值为 24 小时。设置值应小于 `diagnostics.forced_sql_stat_reset.interval` 参数的取值。                                                                                                                                                                                                                                                                             | `1h0m0s`    | duration |
| `external.graphite.endpoint`                            | 设置为非空时，系统将服务器指标推送到指定主机、端口的 Graphite 或 Carbon 服务器。                                                                                                                                                                                                                                                                                                                                          |           | string   |
| `external.graphite.interval`                            | 启用指标推送时，将指标推送到 Graphite 的时间间隔。                                                                                                                                                                                                                                                                                                                                                                           | `10s`       | duration |
| `jobs.scheduler.enabled`                                | 开启或关闭定时任务功能。默认开启定时任务。                                                                                                                                                                                                                                                                                                                                                                                         | `true`      | boolean  |
| `jobs.scheduler.max_jobs_per_iteration`                 | 每次扫描执行的最大任务数。默认值为 `10`。设置为 `0` 时，表示无任务数限制。                                                                                                                                                                                                                                                                                                                                                       | `10`        | integer  |
| `jobs.scheduler.pace`                                   | 扫描 `system.scheduled_jobs` 任务表的频率。默认值为 `60` 秒。设置值不能小于 `60s`，如果设置值小于 `60s`，采用默认值 `60s`。                                                                                                                                                                                                                                                                                                 | `60s`       | duration |
| `kv.allocator.load_based_lease_rebalancing.enabled`     | 基于负载和延迟重新平衡 Range 租约。                                                                                                                                                                                                                                                                                                                                                                                          | `TRUE`      | bool     |
| `kv.allocator.load_based_rebalancing`                   | 是否基于存储之间的 QPS 分布重新平衡。<br >- `0`：表示不启动。 <br >- `1`：表示重新平衡租约。 <br >- `2`：表示平衡租约和副本。                                                                                                                                                                                                                                                                                                                                | `2`         | enum     |
| `kv.allocator.qps_rebalance_threshold`                  | 存储节点的 QPS 与平均值之间的最小分数，用于判断存储节点负载是否过高或过低。                                                                                                                                                                                                                                                                                                                                                  | `0.25`      | float    |
| `kv.allocator.range_rebalance_threshold`                | 存储的 Range 数与平均值的最小分数，用于判断存储节点负载是否过高或过低。                                                                                                                                                                                                                                                                                                                                                      | `0.05`      | float    |
| `kv.allocator.ts_consider_rebalance.enabled`                | 控制后台时序数据分片的自动均衡行为。启用时，集群扩缩容后系统会自动进行数据重分布；禁用时，扩缩容后不会自动触发数据重分布。如需进行扩缩容均衡，可临时启用该参数等待数据均衡完成后再关闭。                                                                                                                                                                                                                                                                                                                                               | `true`      | bool    |
| `kv.allocator.ts_store_dead_rebalance.enabled`                | 控制节点死亡后的副本自动迁移行为。启用时，副本队列会根据节点状态自动进行副本迁移、替换和补足；禁用时，即使节点死亡也不会进行副本补足。注意：在 5 节点三副本集群中禁用该功能后，将无法承受连续节点故障。                                                                                                                                                                                                                                                                                                                                    | `true`      | bool    |
| `kv.bulk_io_write.max_rate`                             | 批量输入/输出（IO）操作向磁盘写入数据时的速率限制。                                                                                                                                                                                                                                                                                                                                                                          | `1.0 TiB`    | byte size      |
| `kv.closed_timestamp.follower_reads_enabled`            | 所有副本基于封闭时间戳的信息提供一致的历史读取。                                                                                                                                                                                                                                                                                                                                                                           | `TRUE`      | bool     |
| `kv.kvserver.qps_ts_follower_read_threshold` | 设置热点时序数据分片（range）的 QPS（每秒查询次数）阈值，以控制是否允许从 follower 副本中读取数据。当某个时序数据分片的 QPS 超过该阈值时，系统将允许从该数据分片的 follower 副本中读取数据，以分担 leaseholder 副本的查询压力，降低高负载节点的资源使用，提升整体查询效率。<br>该参数适用于集群内存在热点数据分片或某些数据分片负载较高的场景。<br>默认值为 `0`，表示不启用该功能。<br>**注意**：由于副本间数据同步可能存在延迟，从 follower 副本读取的数据可能慢于 leaseholder 副本，无法完全保证数据的强一致性。建议根据集群的实际 QPS 负载情况合理设置阈值，在查询性能和数据一致性之间取得平衡。<br>**提示**：可通过 `SELECT range_id, lease_holder, lease_holder_qps FROM kwdb_internal.ranges` SQL 命令查看各个时序数据分片的 QPS 情况，根据实际负载设置合适的阈值。 | `0` | float |
| `kv.kvserver.ts_split_by_timestamp.enabled`            | 控制时序数据分片是否按照时间戳进行拆分，设置为 `false` 时只根据哈希点进行拆分。设置为 `true` 且 `kv.kvserver.ts_split_interval` 设置为 `1` 时，时序数据分片将根据哈希点和时间戳进行拆分。                                                                                                                                                                                                                                                                              | `FALSE`      | bool     |
| `kv.kvserver.ts_split_interval`            | 时序数据分片拆分间隔，默认值为 `10`。                                                                                                                                                                                                                                                                                                                                                                           | `10`      | int     |
| `kv.protectedts.reconciliation.interval`                | 通过受保护的时间戳记录协调作业的频率。                                                                                                                                                                                                                                                                                                                                                                                       | `5m0s`      | duration |
| `kv.range_split.by_load_enabled`                        | 允许系统根据负载集中的位置自动拆分 Range。                                                                                                                                                                                                                                                                                                                                                                                 | `TRUE`      | bool     |
| `kv.range_split.load_qps_threshold`                     | 当 QPS 超过指定阈值时，系统将根据负载情况自动拆分 Range。                                                                                                                                                                                                                                                                                                                                                             | `2500`      | int      |
| `kv.rangefeed.enabled`                                  | 启用 rangefeed 注册。                                                                                                                                                                                                                                                                                                                                                                                                      | `TRUE`      | bool     |
| `kv.replication_reports.interval`                       | 生成复制约束统计、复制统计报告以及复制关键位置信息报告的频率。                                                                                                                                                                                                                                                                                                                                                             | `1m0s`      | duration |
| `kv.snapshot_rebalance.max_rate`                        | 重新平衡和复制快照的速率限制（单位：字节/秒）。                                                                                                                                                                                                                                                                                                                                                                                | `8.0 MiB`    | byte size      |
| `kv.snapshot_recovery.max_rate`                         | 恢复快照的速率限制（单位：字节/秒）。                                                                                                                                                                                                                                                                                                                                                                                            | `8.0 MiB`    | byte size      |
| `kv.transaction.max_intents_bytes`                      | 事务中用于跟踪锁的最大字节数。                                                                                                                                                                                                                                                                                                                                                                                             | `262144`    | int      |
| `kv.transaction.max_refresh_spans_bytes`               | 序列化事务中用于跟踪刷新跨度的最大字节数。                                                                                                                                                                                                                                                                                                                                                                                 | `256000`    | int      |
| `log.sync.enabled` | 用于控制是否执行日志同步操作。默认值为 `true`, 表示启用日志同步。在磁盘繁忙时，日志同步操作可能会触发超时阈值，导致数据库主动宕机。通过禁用同步操作，可以避免因日志同步超时导致数据库进程宕机。 | `true` | bool |
| `server.auth_log.sql_connections.enabled`               | 设置为 `TRUE` 时，系统记录 SQL 客户端连接和断开事件，可能会影响负载较重节点的性能。                                                                                                                                                                                                                                                                                                                                        | `FALSE`     | bool     |
| `server.auth_log.sql_sessions.enabled`                  | 设置为 `TRUE` 时，系统记录 SQL 会话登录和断开事件，可能会影响负载较重节点的性能。                                                                                                                                                                                                                                                                                                                                          | `FALSE`     | bool     |
| `server.clock.forward_jump_check_enabled`               | 设置为 `TRUE` 时，当时钟跳变大于 `max_offset/2` 时，会导致紧急情况。                                                                                                                                                                                                                                                                                                                                                                 | `FALSE`     | bool     |
| `server.clock.persist_upper_bound_interval`             | 持久化时钟墙上限的时间间隔。时钟在此期间不会生成大于已持久化时间戳的墙上时间。系统如果看到大于此值的墙上时间，将引发紧急情况。KWDB 启动时会等待墙上时间追赶至已持久化时间戳。这确保了在服务器重启时墙上时间的单调递增。不设置此值或将其设置为 `0`，表示禁用此功能。                                                                                                                                                          | `0s`        | duration |
| `server.consistency_check.max_rate`                     | 一致性检查的速率限制（单位：字节/秒）。与 `server.consistency_check.interval` 参数一起使用，用以控制一致性检查的频率。这可能会影响性能。                                                                                                                                                                                                                                                                                                   | `8.0MiB`    | byte size      |
| `server.eventlog.ttl`                                   | 如果取值非零，系统每 10 分钟删除一次超出该时长的事件日志条目。设置值不应低于 `24` 小时。                                                                                                                                                                                                                                                                                                                                                     | `2160h0m0s` | duration |
| `server.host_based_authentication.configuration`        | 连接验证期间，使用基于主机的验证配置。                                                                                                                                                                                                                                                                                                                                                                                       | -         | string   |
| `server.rangelog.ttl`                                   | 如果取值非零，系统每 10 分钟删除一次超出该时长的 Range 日志条目。设置值不应低于 `24` 小时。                                                                                                                                                                                                                                                                                                                                                  | `720h0m0s`  | duration |
| `server.remote_debugging.mode`                          | 用于启用或禁用远程调试。<br >- `local`：仅在本地启用远程调试。<br >- `any`：允许从任何地方启用远程调试。<br >- `off`：禁用远程调试。                                                                                                                                                                                                                                                                              | `local`     | string   |
| `server.rest.timeout`                                   | RESTful API 连接超时阈值。超过该阈值后，系统将断开该会话连接。默认值为 `60` 分钟，取值范围为 `[1, 2^63-1]` 分钟。                                                                                                                                                                                                                                                                                                              | `60`        | int      |
| `server.restful_service.default_request_timezone` | 用于全局控制 RESTful API 的时区信息。取值范围为 -12 到 14。| `8` | int |
| `server.shutdown.drain_wait`                            | 关闭服务器时，服务器在未准备好状态下等待的时间。                                                                                                                                                                                                                                                                                                                                                                           | `0s`        | duration |
| `server.shutdown.lease_transfer_wait`                   | 关闭服务器时，服务器等待 Range 租约传输完成的时间。                                                                                                                                                                                                                                                                                                                                                                        | `5s`        | duration |
| `server.shutdown.query_wait`                            | 关闭服务器时，服务器等待活动查询完成的时间。                                                                                                                                                                                                                                                                                                                                                                                             | `10s`       | duration |
| `server.sql_connections.max_limit`                            | 单个节点的最大连接数，默认设置为 `200`，支持设置范围为 [4, 50000]。当计划连接的客户端数量超过该值时，可适当调高该参数，以满足更多客户端的连接需求。      | `200`       | int |
| `server.time_until_store_dead`                          | 如果节点在指定时间内没有通过 Gossip 协议发送更新，系统将其标记为死亡节点。                                                                                                                                                                                                                                                                                                                                                 | `30m0s`      | duration |
| `server.tsinsert_direct.enabled`                             | 启用时序写入短接功能，以提升写入性能。                                                                                                                                                                                                                                                                                                                                                          | `true`       | bool |
| `server.user_login.timeout`                             | 当某个系统 Range 不可用时，超过设置时间，客户端身份验证将超时。                                                                                                                                                                                                                                                                                                                                                            | `10s`       | duration |
| `server.web_session_timeout`                            | 新创建 Web 会话在系统中保持有效的时间。                                                                                                                                                                                                                                                                                                                                                                                    | `168h0m0s`  | duration |
| `sql.all_push_down.enabled`                             | 下推所有 SQL 操作。                                                                                                                                                                                                                                                                                                                                                                                                    | `TRUE`      | bool     |
| `sql.auto_limit.quantity` | 配置 SQL 查询结果的返回行数。支持以下取值： <br>- `0`：不限制 SQL 查询结果的返回行数。<br>- 任意大于 0 的正整数：按照配置的值限制 SQL 查询结果的返回行数。 | `0` | int |
| `sql.defaults.default_int_size`                         | INT 数据类型的大小（单位：字节）。                                                                                                                                                                                                                                                                                                                                                                                           | `8`         | int     |
| `sql.defaults.idle_in_session_timeout` | 配置空闲会话的超时时间。如果取值为 `0`，表示会话不会超时。| `0s` |  duration |
| `sql.defaults.results_buffer.size`                      | 将查询结果发送到客户端之前，服务器端累积语句结果或语句批处理结果的缓冲区大小。支持通过指定连接的 `results_buffer_size` 参数覆盖本设置值。自动重试只有在结果尚未传递到客户端时才会发生。因此，如果减小缓冲区大小，客户端可能会接收更多可重试错误。增加缓冲区大小则可能会增加客户端在收到第一个结果行之前的等待时间。更新设置仅影响新连接。设置为 `0` 时，表示禁用任何缓冲。                                                       | `16 KiB`     | byte size     |
| `sql.defaults.multimodel.enabled` | 配置多模查询优化。开启后，系统识别多模查询并生成相应的查询计划。| `true` | bool |
| `sql.defaults.serial_normalization`                     | 表定义中 SERIAL 数据类型的默认处理方式 `[rowid = 0,virtual_sequence = 1,sql_sequence = 2]`。                                                                                                                                                                                                                                                                                                                                     | `rowid`     | enum       |
| `sql.distsql.max_running_flows`                         | 在节点上可以运行的最大并发流数量。                                                                                                                                                                                                                                                                                                                                                                                         | `500`       | bool     |
| `sql.distsql.temp_storage.joins`                        | 设置为 `TRUE` 时，将在分布式 SQL 连接中使用磁盘。<br > **说明** <br > 禁用该设置可能会影响内存使用和性能。                                                                                                                                                                                                                                                                                                                                      | `TRUE`      | bool     |
| `sql.distsql.temp_storage.sorts`                        | 设置为 `TRUE` 时，将在分布式 SQL 排序中使用磁盘。<br > **说明** <br > 禁用该设置可能会影响内存使用和性能。                                                                                                                                                                                                                                                                                                                                      | `TRUE`      | bool     |
| `sql.log.slow_query.latency_threshold`                  | 如果取值非零，当 SQL 语句服务延迟超过指定阈值时，系统将在每个节点的辅助日志记录器记录该语句。                                                                                                                                                                                                                                                                                                                              | `0s`        | duration      |
| `sql.metrics.statement_details.dump_to_logs`            | 定期清除数据时，将收集的语句统计信息写入到节点日志中。                                                                                                                                                                                                                                                                                                                                                                           | `FALSE`     | bool     |
| `sql.metrics.statement_details.enabled`                 | 收集每个语句的查询统计信息。                                                                                                                                                                                                                                                                                                                                                                                               | `TRUE`      | bool     |
| `sql.metrics.statement_details.plan_collection.enabled` | 定期保存每个指纹的逻辑计划。                                                                                                                                                                                                                                                                                                                                                                                               | `TRUE`      | bool |
| `sql.metrics.statement_details.plan_collection.period`  | 收集新的逻辑执行计划之间的时间间隔。                                                                                                                                                                                                                                                                                                                                                                                       | `5m0s`      | duration |
| `sql.metrics.statement_details.threshold`               | 触发统计信息收集所需的最小执行时间。                                                                                                                                                                                                                                                                                                                                                                                         | `0s`        | bool     |
| `sql.metrics.transaction_details.enabled`               | 收集每个应用的事务统计信息。                                                                                                                                                                                                                                                                                                                                                                                                 | `TRUE`      | bool     |
| `sql.notices.enabled`                                   | 在服务器/客户端协议中发送通知。                                                                                                                                                                                                                                                                                                                                                                                              | `TRUE`      | bool     |
| `sql.stats.automatic_collection.enabled`                | 自动统计信息收集模式。                                                                                                                                                                                                                                                                                                                                                                                                     | `FALSE`     | bool     |
| `sql.stats.automatic_collection.fraction_stale_rows`    | 每张表触发统计信息刷新的过期行百分比。                                                                                                                                                                                                                                                                                                                                                                                     | `0.2`       | float    |
| `sql.stats.automatic_collection.min_stale_rows`         | 每张表触发统计信息刷新的最小过期行行数。                                                                                                                                                                                                                                                                                                                                                                                   | `500`       | int      |
| `sql.stats.histogram_collection.enabled`                | 直方图收集模式。                                                                                                                                                                                                                                                                                                                                                                                                           | `TRUE`      | bool     |
| `sql.stats.post_events.enabled`                         | 启用设置后，每次创建统计信息作业时都会生成一个事件记录。                                                                                                                                                                                                                                                                                                                                                                   | `FALSE`     | bool     |
| `sql.stats.ts_automatic_collection.enabled`             | 自动统计时序数据信息收集模式。                                                                                                                                                                                                                                                                                                                                                                                             | `TRUE`      | bool     |
| `sql.temp_object_cleaner.cleanup_interval`              | 清理孤立临时对象的频率。                                                                                                                                                                                                                                                                                                                                                                                                   | `30m0s`     | bool     |
| `sql.trace.log_statement_execute`                       | 设置为 `TRUE` 时，启用执行语句的日志记录。                                                                                                                                                                                                                                                                                                                                                                                     | `FALSE`     | bool      |
| `sql.trace.session_eventlog.enabled`                    | 设置为 `TRUE` 时，启用会话跟踪。这可能会明显影响性能。                                                                                                                                                                                                                                                                                                                                                                           | `FALSE`     | bool     |
| `sql.trace.txn.enable_threshold`                        | 事务的执行时间超过指定的持续时间时，系统将对该事务进行追踪。设置为 `0` 时，表示禁用该功能。                                                                                                                                                                                                                                                                                                                                        | `0s`        | duration    |
| `sql.ts_insert_select.block_memory`                       | 时序数据 `INSERT INTO SELECT` 语句单次写入的数据块内存限制。                                                                                                                                                                                                                                                                                                                                                                       | `200`       | int      |
| `sql.ts_insert_select_limit.enabled`                    | 允许时序数据写入关系表。                                                                                                                                                                                                                                                                                                                                                                                                     | `FALSE`     | bool     |
| `sql.txn.cluster_transaction_isolation` | 配置事务隔离级别，支持以下取值：<br >- 串行化（`serializable`）：Serializable 隔离是最高的隔离级别，保证了即使事务是并行执行的，其结果也与它们一次执行一个事务时的结果相同，没有任何并发性。<br >- 提交读（`read committed`，RC）：在 RC 隔离级别下，事务会读取到其他事务已提交的数据，但不完全保证事务操作的可序列化。<br >- 可重复读（`repeatable read`，RR）：RR 隔离保证了在同一事务内多次读取同一数据时，结果是一致的。| `serializable` | enum |
| `timeseries.storage.enabled`                            | 是否在集群内存储周期性的时序数据。除非数据已经在其他地方存储，否则不建议禁用此功能。                                                                                                                                                                                                                                                                                                                                               | `TRUE`      | bool     |
| `timeseries.storage.resolution_10s.ttl`                 | 以 `10` 秒分辨率存储的时序数据的最大保存时长。超过该时长的数据将被汇总和删除。                                                                                                                                                                                                                                                                                                                                             | `240h0m0s`  | duration |
| `timeseries.storage.resolution_30m.ttl`                 | 以 `30` 分钟分辨率存储的时序数据的最大保存时长。超过该时长的数据将被汇总和删除。                                                                                                                                                                                                                                                                                                                                           | `2160h0m0s` | duration |
| `trace.debug.enable`                                    | 设置为启用后，可以在 `/debug` 页面中查看最近请求的跟踪信息。                                                                                                                                                                                                                                                                                                                                                               | `FALSE`     | bool     |
| `trace.lightstep.token`                                 | 设置为启用后，跟踪数据将使用指定的令牌发送到 Lightstep。                                                                                                                                                                                                                                                                                                                                                                   | -         | string   |
| `trace.zipkin.collector`                                | 设置为启用后，跟踪数据将发送到指定的 Zipkin 实例，例如：`127.0.0.1:9411`。如果设置了 `trace.lightstep.token` 参数，将忽略该配置。                                                                                                                                                                                                                                                                                               | -         | string   |
| `ts.auto_vacuum.enabled` | 用于控制是否启用数据重组功能，设置为 `true` 时，表示启用该功能。 | `TRUE` | bool |
| `ts.block.lru_cache.max_limit`                         | 用于设置节点时序块 LRU（Least Recently Used，最近最少使用）缓存的最大内存大小，单位为字节。该缓存用于优化时序数据查询性能，通过缓存热点数据块来减少磁盘 I/O 操作。当缓存达到最大限制时，将按照 LRU 策略淘汰最近最少使用的数据块。<br>默认值为 `1073741824`（1GB），设置为 `0` 时，表示关闭块缓存功能。<br>建议根据节点实际可用内存进行调整，适当调大可以提升查询性能，但过大可能导致内存溢出（OOM）                                                                                                                                                                                 | `1073741824`       | int      |
| `ts.count.use_statistics.enabled`  | 指定 `count(*)` 函数查询时序数据时是否使用已写入的行数，以优化查询时间。默认开启，支持关闭；关闭后可能会影响 `count(*)` 的查询性能。                                                                                                 | `true`   | bool |
| `ts.compact.max_limit`  | 控制单次合并操作中处理的 Last Segment 最大数量。触发合并操作时，系统会将多个 Last Segment 的数据合并到 Entity Segment。<br>该参数用于控制合并操作的资源消耗。减小此值可以减少单次合并的工作量，降低 CPU 和 I/O 峰值压力，但需要更多次合并操作才能处理完所有数据。增大此值可以提高单次合并效率，减少合并次数，但会增加单次操作的资源消耗和执行时间。                                                                                              | `10`   | int |
| `ts.compression.last_segment.enabled` | 控制是否对 last segment 启用压缩。支持以下设置值：<br>- `true`：启用压缩。last segment 数据写入时进行压缩，可减少内存和磁盘占用，但会增加写入时的 CPU 消耗。<br>- `false`：禁用压缩。last segment 数据以原始格式存储，写入性能更高，但占用更多内存和磁盘空间。<br>该参数用于在写入性能和存储效率之间进行权衡。写入密集型场景建议设置为 `false` 以提高写入吞吐量；存储敏感型场景建议设置为 `true` 以减少资源占用。 | `true` | boolean |
| `ts.compress.stage` | 控制时序数据的压缩层级。支持以下设置值：<br>- `0`：不压缩，数据以原始格式存储。<br>- `1`：一级压缩，根据列类型对列进行编码。<br>- `2`：二级压缩，使用通用压缩算法，可进一步减少存储空间，但会增加 CPU 消耗。<br>该参数用于在存储空间和计算资源之间进行权衡。较高的压缩层级可显著减少磁盘占用，但会增加数据写入和读取时的 CPU 开销。 | `2` | int |
| `ts.dedup.rule`                                         | 数据去重策略。支持设置为以下参数：<br>- `override`：整行去重，后写入的数据覆盖已写入的具有相同时间戳的数据。<br>- `merge`：对相同时间戳的数据进行去重和整合。同一时间戳的数据多次写入时，后写入的非 NULL 列值会覆盖先前写入的对应列值，最终整合为一行记录。该模式适用于相同时间戳不同字段数据分批写入的场景。<br>- `discard`：忽略新写入的重复数据，保留已写入的数据。当重复数据写入失败后，客户端会收到成功插入数据的条数，并以 Notice 的形式展示未成功插入数据的条数。<br>- `keep`：允许重复数据写入且不去重。目前只支持单节点部署时设置。| `override`  | string   |
| `ts.force_sync_file.enabled` | 控制时序数据写入磁盘时是否强制刷盘（fsync）：<br>- 启用(`true`)：数据物理落盘后返回成功，保证任何异常停机（断电、宕机等）后均可正常重启，但会降低写入性能，HDD 影响较大，SSD 影响相对较小<br>- 禁用(`false`)：数据写入系统缓存后返回成功，写入性能大幅提升，宕机等场景可正常重启，但断电时缓存数据可能丢失，导致无法自动重启，需要人工介入恢复 | `false` | bool |
| `ts.last_cache_size.max_limit`  | 设置时序数据 `last_row` 读缓存功能的内存限制，即每个 vgroup 为每个设备的最新数据分配的缓存内存大小。<br>取值范围为 [0, 1,073,741,824] 字节，默认值为 1 GB （1,073,741,824 字节）。<br>设置为 `0` 时关闭读缓存功能；缓存占用内存超过设置值时，系统将自动淘汰部分缓存数据。开启再关闭读缓存功能后，系统会在第一次写入数据时淘汰所有已缓存数据，后续写入也不再缓存。<br>该参数适用于写入设备数量适中且需要频繁查询最新数据的场景。开启读缓存功能后，`last` 和 `last_row` 查询可直接从内存读取数据，显著提升查询响应速度。<br>**注意**：在设备数量巨大的场景下使用该功能可能影响数据写入性能，适当增大参数值可降低缓存淘汰频率，减少对写入性能的影响。建议根据实际业务需求动态调整该参数，在查询性能和写入性能之间取得平衡。                                                                                 | `1073741824`   | byte size |
| `ts.mem_segment_size.max_limit`  | 控制单个 VGroup 中 Mem Segment 的最大大小。Mem Segment 是数据写入内存的缓冲区，当其大小达到此限制时，会触发数据持久化操作，将内存数据写入磁盘的 Last Segment。<br>该参数用于平衡内存占用和刷盘频率，减小此值可以加快数据持久化频率，降低内存占用，但会增加磁盘 I/O 次数；增大此值可以减少持久化频率，降低磁盘 I/O 开销，但会增加内存占用和潜在的数据丢失风险（故障时未持久化的数据量更大）。                                                                                 | `536870912`   | byte size |
| `ts.ordered_table.enabled`| 当用户未使用 `ORDER BY` 子句指定排序时，配置是否按照数据写入的时间戳逆序返回查询结果。当设置为 `true` 时，对于单设备查询，按照数据写入的时间戳逆序返回查询结果。对于多设备查询，先转换成单设备查询，然后再合并所有的数据。 | `false` | bool |
| `ts.parallel_degree`| 单节点可并行执行的时序数据查询任务数量，范围为 [0, cpu_core*2+2]，其中 `cpu_core` 是实际使用的逻辑处理器数量。设置为 `0` 或 `1` 时，系统将串行执行查询；设置大于 `1` 时，表示可并行执行的任务数量。 | `0` | int |
| `ts.partition.interval`                                 | 数据分区间隔，设置值必须大于 `0`。                                                                                                                                                                                                                                                                                                                                                                                           | `864000`    | int      |
| `ts.raft_log.sync_period` | 时序数据 raft log 落盘周期。默认 `10s` 表示每 10 秒强制同步落盘。设置为 `0s` 时表示实时落盘，设置为非零值时，系统将按指定时间间隔强制同步落盘。延长落盘时间有助于提升写入性能，但如果节点意外停机，可能丢失最多一个周期内的数据。适用于高性能要求、对数据一致性要求相对较低的场景。 | `10s` | duration |
| `ts.raftlog_combine_wal.enabled` | 启用时序数据 raft log 和 WAL 合并功能，开启后可减少写放大效应，提升时序数据写入性能。| `false` | bool |
| `ts.reserved_last_segment.max_limit`                           | 控制单个分区下保留的最大 Last Segment 个数。当 Last Segment 数量超出此限制时，Compact 线程会自动触发数据合并操作，将 Last Segment 中满足行数阈值的设备数据合并并以列存压缩格式写入 Entity Segment，以优化存储空间并提升查询性能。<br>此参数用于平衡内存占用与数据持久化效率，避免 Last Segment 过多导致的资源消耗。                                                                                                                                                                                                                        | `3`      | int      |
| `ts.rows_per_block.max_limit`                           | 控制 Entity Segment 中单个 Block 可保存的最大行数，避免单个 Block 过大导致读取效率下降。<br>该参数用于调节存储密度和查询性能之间的平衡。增大此值可提高压缩率，节省存储空间（适合存储优先场景），减小此值可减少单次查询扫描的数据量，提升查询响应速度（适合查询优先场景）。                                                                                                                                                                                                                             | `4096`      | int      |
| `ts.rows_per_block.min_limit`                           | 控制 Entity Segment 中单个 Block 可保存的最小行数，即触发数据从 Last Segment 合并到 Entity Segment 的行数阈值。<br>该参数确保每个 Block 包含足够的数据行以提高压缩效率和存储密度，避免生成过多小 Block 导致文件碎片化和元数据开销增加。<br>增大此值可减少 Block 数量，降低元数据开销，但会延长数据合并时间；减小此值可加快数据持久化，但可能产生更多小 Block，增加文件碎片。                                                                                                                                             | `512`      | int      |
| `ts.sql.query_opt_mode` | 配置跨模查询优化。取值为一个四位数的 INT 值，每一位表示对应优化功能的开关，其中 1 表示开启，0 表示关闭。四个跨模查询优化功能从左到右依次为多谓词顺序优化、标量子查询优化、Inside-out 下推聚合优化、Inside-out 下推 time_bucket 优化。默认情况下，开启多谓词顺序优化、标量子查询优化、Inside-out 下推聚合优化。<br>**说明** <br>用户使用数据库时，仅需考虑是否开启对应的跨模查询优化功能。若打开相应的优化功能，数据库系统会自行判断输入的查询是否可以被优化。只有满足特定的条件才能被优化。 | `1110` | int  |
| `ts.stream.max_active_number` | 运行状态的流计算实例的最大数量。| `10` | int32 |
| `ts.table_cache.capacity` | 控制已缓存的时序表数量，支持范围为[1,2147483647]。默认值为 `1000`，表示可以缓存 1000 个时序表，缓存中的时序表无需重新初始化。如果需要缓存更多的时序表，可增大该值以提升读写性能。注意，较大的设置值可能会占用更多内存。| `1000` | int |
| `ts.wal.checkpoint_interval` | 时序 WAL 检查点执行间隔，用于控制时序数据从内存刷新到磁盘的时间间隔。  | `1m`      | duration        |
| `ts.wal.wal_level`               | 时序 WAL 写入级别。可选值：<br>- `0` (`off`)：关闭 WAL，重启时通过时序存储引擎接口恢复数据状态<br>- `1` (`sync`)：日志实时写入磁盘并强制持久化，提供最高安全性，性能相对较低<br>- `2` (`flush`)：日志写入文件系统缓冲区，在性能和安全性间取得平衡<br>- `3` (`byrl`)：基于 Raft Log 保证数据一致性，WAL 仅负责元数据一致性 | `2` | integer        |
