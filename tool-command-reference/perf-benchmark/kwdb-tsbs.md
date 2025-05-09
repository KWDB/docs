---
title: kwdb-tsbs
id: kwdb-tsbs
---

# kwdb-tsbs 性能测试

## kwdb-tsbs 概述

kwdb-tsbs 是一款基于 [Timescale](https://www.timescale.com/) [Time Series Benchmark Suite (TSBS)](https://github.com/timescale/tsbs) 的时序数据库性能基准测试工具，用于生成数据集，然后对 KWDB 数据库的读写性能进行基准测试。kwdb-tsbs 支持时序数据生成、数据写入、查询处理、自动化结果汇总统计等功能。

### 功能特性

- **数据生成**：支持自定义设备数量、数据采样时间范围和数据采样间隔。
- **数据导入**：提供针对 KWDB 优化的批量写入工具。
- **查询场景**：提供标准的时序查询模板。
- **自动化测试**：一键执行完整的 KWDB 性能基准测试流程。

### 测试场景

::: warning 说明
目前，kwdb-tsbs 只支持 DevOps cpu-only 测试场景。
:::

DevOps cpu-only 测试场景只关注 CPU 指标。该测试场景模拟对服务器 CPU 监控生成的时序数据，针对每台设备（CPU）记录其 10 个 CPU 指标。

下表列出 kwdb-tsbs 在 cpu-only 测试场景中支持的查询类型。

| 查询类型              | 描述                                                                           |
|-----------------------|------------------------------------------------------------------------------|
| single-groupby-1-1-1  | 对单台主机的单个指标进行简单汇总（MAX）。每 5 分钟汇总一次，持续 1 小时。           |
| single-groupby-1-1-12 | 对单台主机的单个指标进行简单汇总（MAX）。每 5 分钟汇总一次，持续 12 小时。          |
| single-groupby-1-8-1  | 对八台主机的单个指标进行简单汇总（MAX）。每 5 分钟汇总一次，持续 1 小时。           |
| single-groupby-5-1-1  | 对单台主机的五个指标进行简单汇总（MAX）。每 5 分钟汇总一次，持续 1 小时。           |
| single-groupby-5-1-12 | 对单台主机的五个指标进行简单汇总（MAX）。每 5 分钟汇总一次，持续 12 小时。          |
| single-groupby-5-8-1  | 对八台主机的五个指标进行简单汇总（MAX）。每 5 分钟汇总一次，持续 1 小时。           |
| cpu-max-all-1         | 汇总 1 小时内单台主机每小时的所有 CPU 指标。                                    |
| cpu-max-all-8         | 汇总 1 小时内八台主机每小时的所有 CPU 指标。                                    |
| double-groupby-1      | 对时间和主机进行汇总，得出 24 小时内每台主机每小时单个 CPU 指标的平均值。        |
| double-groupby-5      | 对时间和主机进行汇总，得出 24 小时内每台主机每小时 5 个 CPU 指标的平均值。       |
| double-groupby-all    | 对时间和主机进行汇总，得出 24 小时内每台主机每小时所有 CPU 指标（10 个）的平均值。 |
| high-cpu-all          | 所有主机的某个指标超过阈值的所有读数。                                          |
| high-cpu-1            | 特定主机的某个指标超过阈值的所有读数。                                          |
| lastpoint             | 每台主机的最后读数。                                                            |
| groupby-orderby-limit | 在随机选定的时间终点前，按时间维度汇总的最后 5 个读数。                          |

## 源码编译

### 前提条件

- 已安装 Go 1.23 或更高版本。

### 安装部署

1. 克隆仓库。

    ```shell
    git clone https://gitee.com/kwdb/kwdb-tsbs.git
    cd kwdb-tsbs
    ```

2. 构建应用。

    ```shell
    make
    ```

编译和安装成功后的文件清单如下：

```plain text
kwdb-tsbs/
└── bin/
    ├── tsbs_generate_data      # 数据生成工具
    ├── tsbs_load_kwdb          # 数据导入工具
    ├── tsbs_generate_queries   # 查询生成工具
    └── tsbs_run_queries_kwdb   # 查询执行工具
```

## 使用举例

使用 kwdb-tsbs 进行基准测试包括 4 个阶段：数据生成、数据导入、查询生成、和查询执行。

### 生成数据

kwdb-tsbs 提供数据生成工具（`tsbs_generate_data`），为 KWDB 数据库生成一个伪 CSV 文件。其中，每行表示一条记录，首项为操作类型（1 或 3）。

- 1：表示插入数据（包括数据值和标签值），格式为 `1,ptag名,字段数量,插入的数据`。
- 3：表示写入标签值，格式为 `3,表名,ptag名,标签值`。

示例：

```sql
1,host_0,11,(1451606400000,58,2,24,61,22,63,6,44,80,38,'host_0')
3,cpu,host_0,('host_0','eu-central-1','eu-central-1a','6','Ubuntu15.10','x86','SF','19','1','test')
```

以下示例生成一个数据文件，可用于将数据批量加载到 KWDB 数据库中。

```shell
./tsbs_generate_data \
  --format="kwdb" \
  --use-case="cpu-only" \
  --seed=123 \
  --scale=100 \
  --timestamp-start="2016-01-01T00:00:00Z" \
  --timestamp-end="2016-01-02T00:00:00Z" \
  --log-interval="10s" \
  --orderquantity=12 > data.dat
```

参数说明：

| 参数          | 描述                                                                                                                              | 类型   | 可选值     | 默认值                                           |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------ | -------------- | ---------------------------------------------------- |
| `format`          | 目标数据库的格式。                                                                                                                     | STRING | `kwdb`         | N/A                                                  |
| `use-case`        | 测试场景类型。                                                                                                                         | STRING | `cpu-only`     | `cpu-only`                                           |
| `seed`            | 伪随机数生成器 PRNG 种子。                                                                                                             | INT    | 正整数         | `0`，表示使用当前时间戳。                            |
| `scale`           | 生成数据的设备数量。                                                                                                                   | INT    | 正整数         | `1`                                                  |
| `timestamp-start` | 数据生成的起始时间。遵循 RFC 3339 标准。                                                                                               | STRING | N/A            | `2016-01-01T00:00:00Z`                               |
| `timestamp-end`   | 数据生成的结束时间。遵循 RFC 3339 标准。                                                                                               | STRING | N/A            | `2016-03-02T00:00:00Z`                               |
| `log-interval`    | 数据生成的间隔时间。                                                                                                                   | STRING | 如 "10s"、"1m" | `10s`                                                |
| `orderquantity`   | 初始生成设备数量。例如，对于 100 台 设备，首先生成从 `host_0` 到 `host_11` 的数据，然后生成从 `host_12` 到 `host_23` 的数据，依此类推。 | INT    | 正整数         | 建议与导入数据时使用的 `worker` 参数的取值保持一致。 |

### 导入数据

kwdb-tsbs 提供数据导入工具（`tsbs_load_data`），将由 `tsbs_generate_data` 工具生成的数据文件导入到目标数据库。`tsbs_load_data` 工具支持 INSERT 模式和 PREPARE 模式。两种数据导入模式的参数基本相同。

- INSERT 模式

    ```shell
    ./tsbs_load_kwdb \
      --file=data.dat \
      --user=root \
      --pass=1234 \
      --host=127.0.0.1 \
      --port=26257 \
      --insert-type=insert \
      --batch-size=1000 \
      --db-name=benchmark \
      --case=cpu-only \
      --workers=12 \
      --partition=false
    ```

- PREPARE 模式

    ```shell
    ./tsbs_load_kwdb \
      --file=data.dat \
      --user=root \
      --pass=1234 \
      --host=127.0.0.1 \
      --port=26257 \
      --insert-type=prepare \
      --preparesize=1000 \
      --db-name=benchmark \
      --case=cpu-only \
      --workers=12 \
      --partition=false
    ```

参数说明：

| 参数                      | 描述                                                                                                        | 类型   | 可选值            | 默认值                                                  |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------- | ------ | --------------------- | ----------------------------------------------------------- |
| `file`                        | 数据生成文件的路径。                                                                                             | STRING | N/A                   | N/A                                                         |
| `user`                        | 连接 KWDB 数据库的用户名。                                                                                       | STRING | N/A                   | `root`                                                      |
| `pass`                        | 身份验证时使用的密码。                                                                                           | STRING | N/A                   | 默认为空。                                                  |
| `host`                      | KWDB 数据库的 IP 地址。                                                                                          | STRING | N/A                   | N/A                                                         |
| `port`                      | KWDB 数据库的连接端口。                                                                                          | INT    | N/A                   | `26257`                                                     |
| `insert-type`                 | 数据写入模式。<br >- `insert`：直接插入数据。 <br >- `prepare`：预编译数据。                                                | STRING | `insert` 或 `prepare` | `insert`                                                    |
| `batch-size` 或 `preparesize` | 每批次写入的数据量。<br > **说明** <br >- `batch-size` 参数只适用于 INSERT 模式。<br >- `preparesize` 参数只适用于 PREPARE 模式。 | INT    | 正整数                | `1000`                                                      |
| `db-name`                     | 需要访问的 KWDB 数据库名称。                                                                                     | STRING | N/A                   | `benchmark`                                                 |
| `case`                        | 测试场景类型。                                                                                                   | STRING | `cpu-only`            | `cpu-only`                                                  |
| `workers`                     | 并发写入线程数。                                                                                                 | INT    | 正整数                | 建议与生成数据时使用的 `orderquantity` 参数的取值保持一致。 |
| `partition`                   | 设置是否分区。- 单节点：`false`- 集群：`true`                                                                    | BOOL   | `true` 或 `false`     | `false`                                                     |

### 生成查询

kwdb-tsbs 提供查询生成工具（`tsbs_generate_queries`），用以生成指定查询类型的查询脚本。

```shell
./tsbs_generate_queries \
    --format=kwdb \
    --use-case="cpu-only" \
    --seed=123 \
    --scale=100 \
    --query-type=${QUERY_TYPE} \
    --queries=100 \
    --timestamp-start="2016-01-01T08:00:00Z" \
    --timestamp-end="2016-01-05T00:00:01Z" \
    --db-name=benchmark > query.dat
```

参数说明：

| 参数          | 描述                                | 类型   | 可选值                                                                                                                                 | 默认值                |
| ----------------- | ---------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------- |
| `format`          | 目标数据库的格式。                       | STRING | `kwdb`                                                                                                                                     | N/A                       |
| `use-case`        | 测试场景类型。                           | STRING | cpu-only                                                                                                                                   | cpu-only                  |
| `seed`            | 伪随机数生成器 PRNG 种子。               | INT    | 正整数                                                                                                                                     | `0`，表示使用当前时间戳。 |
| `scale`           | 生成查询的设备数量。                     | INT    | 正整数                                                                                                                                     | `1`                       |
| `query-type`      | 查询类型。                               | STRING | 有关 kwdb-tsbs 支持的查询类型，参见[测试场景](#测试场景)。 | N/A                       |
| `queries`         | 产生的查询语句数量。                     | INT    | 正整数                                                                                                                                     | N/A                       |
| `timestamp-start` | 查询生成的起始时间。遵循 RFC 3339 标准。 | STRING | N/A                                                                                                                                        | `2016-01-01T08:00:00Z`    |
| `timestamp-end`   | 查询生成的结束时间。遵循 RFC 3339 标准。 | STRING | N/A                                                                                                                                        | `2016-01-05T00:00:01Z`    |
| `db-name`         | 需要访问的 KWDB 数据库名称。             | STRING | N/A                                                                                                                                        | `benchmark`               |

### 执行查询

在完成数据生成、数据导入、查询生成后，用户可以使用 `tsbs_run_queries_kwdb` 工具测试 KWDB 数据库的查询执行性能。

```shell
./tsbs_run_queries_kwdb \
    --file=query.dat \
    --user=root \
    --pass=1234 \
    --host=127.0.0.1 \
    --port=26257 \
    --workers=1 > query.log
```

参数说明：

| 参数  | 描述                  | 类型   | 可选值 | 默认值 |
| --------- | -------------------------- | ------ | ---------- | ---------- |
| `file`    | 数据生成文件的路径。       | STRING | N/A        | N/A        |
| `user`    | 连接 KWDB 数据库的用户名。 | STRING | N/A        | `root`     |
| `pass`    | 身份验证时使用的密码。     | STRING | N/A        | 默认为空。 |
| `host`    | KWDB 数据库的 IP 地址。    | STRING | N/A        | N/A        |
| `port`    | KWDB 数据库的连接端口。    | INT    | N/A        | `26257`    |
| `workers` | 并发查询线程数。           | INT    | 正整数     | N/A        |

### 自动化测试

kwdb-tsbs 在 `kwdb-tsbs/scripts` 目录下提供自动化脚本（`tsbs_kwdb.sh`），用户可以一键执行完整的 KWDB 性能基准测试流程。

#### 前提条件

- 已安装 kwdb-tsbs 以及 Go 1.23 或更高版本。
- 具有执行自动化测试脚本的权限。

#### 推荐配置

- 硬件

    下表列出执行自动化测试推荐的硬件规格。用户可以根据实际的业务规模和性能要求规划硬件资源。

    | 组件 | 规格  |
    |------|-------|
    | CPU  | 16 核 |
    | 内存 | 32 GB |
    | 磁盘 | SSD   |

- 操作系统

    下表列出执行自动化测试推荐的操作系统。未提及的操作系统版本也许可以运行自动化测试脚本，但尚未得到 KWDB 官方支持。

    | 操作系统 | 版本 | 架构 |
    | --- | --- | --- |
    | Ubuntu | V20.04 | x86_64 |

#### 执行自动化脚本

1. 配置自动化脚本参数。

    ```shell
    workspace="$GOPATH/src/gitee.com/kwdb"
    ```

    参数说明：

    - `workspace`：KWDB 工作目录的路径。有关更多自动化测试脚本的参数配置，参见[脚本文件](https://gitee.com/kwdb/kwdb-tsbs/blob/master/scripts/tsbs_kwdb.sh)中的详细注释说明。

2. 执行自动化脚本。

    ```shell
    cd kwdb-tsbs/scripts
    ./tsbs_kwdb.sh
    ```

    运行完成后，生成以下相关文件：

    ```plain text
    kwdb-tsbs/
    ├── load_data/          # 生成的导入数据
    ├── query_data/         # 生成的查询数据
    └── reports/            # 生成的测试结果
    └── YMD_HMS_scale[scaleNum]_cluster[clusterNum]_insert[insertType]_wal[walSetting]_replica[replicaNum]_dop[degreeOfParallelism]/
    ├── load_data/  # 导入测试的结果
    └── query_data/ # 查询测试的结果
    ```
