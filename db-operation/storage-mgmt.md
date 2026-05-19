---
title: 存储管理
id: storage-mgmt
---

# 存储管理

## 存储路径设置

### 默认存储路径和系统要求

下表列出了 KWDB 各类文件的默认存储路径、文件系统和配置信息。

| <div style="width:80px">文件</div>       | 默认路径               | 大小               | 文件系统                                                   | 配置参数    |
| ---------- | ---------------------- | ------------------ | ---------------------------------------------------------- | ----------- |
| 数据文件   | `/var/lib/kaiwudb`       | 取决于存储数据的大小 | - 建议使用 ext4 文件系统。<br>- 如果存储大于 16 TB 的数据，建议使用 XFS 系统。 | - 部署配置文件中的 `data_root` 参数<br>- `--store` 启动参数     |
| 日志       | `/var/lib/kaiwudb/logs`  | 默认 1G，可配置    | 建议使用 ext4 文件系统。                                       | `--log-dir` 启动参数  |
| 证书       | `/etc/kaiwudb/certs`     | N/A                | 建议使用 ext4 文件系统。                                       | `--certs-dir` 启动参数 |
| 二进制文件 | `/usr/local/kaiwudb/bin` | > 200 M              | 建议使用 ext4 文件系统。                                       | N/A            |
| 动态库文件 | `/usr/local/kaiwudb/lib` | > 100 M              | 建议使用 ext4 文件系统。                                       | N/A            |

::: warning 说明
如果采用 Docker 容器部署，则使用宿主机路径，系统自动进行挂载。
:::

### 存储路径设置

KWDB 支持以下存储路径设置方式：

- 安装时通过修改 `deploy.cfg` 文件中的 `data_root` 参数自定义数据路径。
- 部署完成后，用户也可以通过修改部署生成的 `kaiwudb_env` 文件、 `docker-compose.yml` 文件或 `kwbase start` 命令修改存储路径。

## 数据压缩

KWDB 支持在创建或修改时序表时，为每个数据列单独指定编码算法、压缩算法及压缩级别，针对不同数据特征选择最优压缩策略，在存储空间和系统资源之间灵活权衡。配置修改后仅对新写入数据生效，已有数据不受影响。

### 编码算法、压缩算法及压缩级别

#### 编码算法

不同数据类型支持的编码算法及默认值如下：

| 数据类型 | 可选编码算法 | 默认值 |
| --- | --- | --- |
| INT2 / INT4 / INT8 | `simple8b` / `disabled` | `simple8b` |
| TIMESTAMP / TIMESTAMPTZ | `simple8b` / `disabled` | `simple8b` |
| FLOAT / DOUBLE | `chimp` / `disabled` | `chimp` |
| BOOL | `bitpacking` / `disabled` | `bitpacking` |
| 字符类型 | `disabled` | `disabled` |
#### 压缩算法

所有数据类型均支持以下压缩算法，默认使用 `lz4`：

| 算法 | 压缩率 | 压缩速度 | 解压速度 | CPU 占用 | 内存占用 | 适用场景 |
| --- | --- | --- | --- | --- | --- | --- |
| `lz4` | 低到中（2x-3x） | 极快 | 最快 | 很低 | 很低 | 高频写入、对延迟敏感的场景（默认） |
| `zstd` | 中到高（2.5x-5x+） | 很快 | 极快（与 lz4 同级） | 低到中（取决于等级） | 中等（可调） | 存储空间敏感、兼顾读写性能的场景 |
| `zlib` | 中（2.5x-4x） | 中等 | 快 | 中等 | 中等 | 存储空间敏感、对写入性能要求较低的场景 |
| `snappy` | 低（1.5x-2x） | 极快 | 极快 | 很低 | 很低 | 速度优先、不需要调节压缩级别的场景 |
| `disabled` | — | — | — | — | — | 关闭压缩 |

::: warning 说明
- `zstd` 压缩速度接近 `lz4`，但压缩率更高，解压速度同样极快，是需要兼顾空间与性能时的优先选择。
- `zlib` 压缩率与 `zstd` 相近，但压缩和解压速度均较慢，CPU 和内存消耗更高，在高频大批量写入场景下影响尤为明显，请谨慎评估后使用。
:::

#### 压缩级别

支持 `low`、`medium`（默认）、`high`，可简写为 `l`、`m`、`h`。压缩级别越高，压缩率越高，CPU 和内存占用也越多，请根据业务负载合理配置。

::: warning 说明
`snappy` 和 `lz4` 不支持压缩级别设置，对其指定压缩级别不会有实际效果。
:::

### 压缩配置

各级压缩配置的优先级规则如下：

- **不修改 cluster setting 时**：列级自定义配置 > 数据类型默认值 > cluster setting 全局配置
- **已设置 cluster setting 时**：列级自定义配置 > 数据类型默认值 = cluster setting 全局配置

建议优先通过 cluster setting 设置全局基准，仅对有特殊需求的列单独指定配置。

#### 全局压缩配置

通过 cluster setting 统一配置全局默认压缩行为，无需逐列指定：

```sql
-- 设置压缩模式（0-3）
SET CLUSTER SETTING ts.compress.stage = 3;

-- 设置全局默认压缩算法
SET CLUSTER SETTING ts.compress.algorithm = 'lz4';

-- 设置全局默认压缩级别
SET CLUSTER SETTING ts.compress.level = 'medium';
```

参数说明：

| 参数 | 说明 | 默认值 | 类型 |
| --- | --- | --- | --- |
| `ts.compress.stage` | 控制时序数据的压缩模式：<br>- `0`：关闭编码，关闭压缩<br>- `1`：开启编码，关闭压缩<br>- `2`：关闭编码，开启压缩<br>- `3`：开启编码，开启压缩 | `3` | int |
| `ts.compress.algorithm` | 全局默认压缩算法，支持 `lz4`、`zstd`、`zlib`、`snappy`、`disabled`。优先级低于列级配置。 | `lz4` | string |
| `ts.compress.level` | 全局默认压缩级别，支持 `low`、`medium`、`high`。优先级低于列级配置。 | `medium` | string |

#### 列级压缩配置

- 建表时为各列指定编码和压缩配置：

  ```sql
  CREATE TABLE test_compress.t1 (
      k_timestamp TIMESTAMPTZ ENCODE 'Simple8B' COMPRESS 'lz4' LEVEL 'high' NOT NULL,
      c1 INT ENCODE 'Simple8B' COMPRESS 'zlib' LEVEL 'high',
      c2 FLOAT COMPRESS 'zlib' LEVEL 'medium',
      c3 INT ENCODE 'Simple8B',           -- 仅指定编码，压缩使用默认值
      c4 BLOB COMPRESS 'disabled',
      c5 BOOL ENCODE 'disabled',
      c7 VARCHAR ENCODE 'disabled' COMPRESS 'disabled'
  ) TAGS (
      code1 INT2 NOT NULL
  ) PRIMARY TAGS (code1);
  ```

- 修改已有列的压缩配置：

  ```sql
  -- 修改压缩算法和压缩级别
  ALTER TABLE t1 ALTER COLUMN c2 COMPRESS 'zstd' LEVEL 'high';

  -- 同时修改编码和压缩算法（ENCODE 必须在 COMPRESS 之前）
  ALTER TABLE t1 ALTER COLUMN c1 ENCODE 'Simple8B' COMPRESS 'zstd' LEVEL 'medium';

  -- 关闭列的压缩
  ALTER TABLE t1 ALTER COLUMN c4 COMPRESS 'disabled';
  ```

## 数据重组

数据重组是指按照特定规则对原始时序数据进行清理和整理的过程，主要应用于以下场景:

- **删除数据清理**：执行 DELETE 或 DROP 操作后，清理被标记删除的数据以释放存储空间
- **过期数据清理**：清理通过生命周期管理功能识别出的过期数据
- **数据整理优化**：对不连续的 entity 数据进行重组排序，提高查询效率

数据重组可以优化存储空间利用率，提升数据库查询性能和响应速度，改善整体系统效率。

### 重组方式

KWDB 提供自动重组和手动重组两种数据重组方式：

#### 自动重组

系统定期自动触发重组任务，以分区(Partition)为基本单位，采用单线程串行方式处理，确保操作的稳定性和数据一致性。具体流程如下：

1. 任务触发：系统定期自动触发重组任务
2. 分区遍历：依次扫描各个分区，对每个分区执行重组操作
3. 数据清理：
    - 清理过期数据
    - 清理被标记删除的数据
4. 文件重建：生成优化后的新数据文件，替换原有文件
5. 标记清理：清理相关的删除标记记录，完成重组流程

重组操作与合并操作互斥，同一 entity segment 不会同时执行这两种操作。

#### 手动重组

需要立即释放存储空间或优化查询性能时，可以通过立即重组命令 `VACUUM TS DATABASES;` 手动触发重组操作。

手动重组特别适用于以下场景：

- **删除数据或删除库表后释放空间**：执行 DELETE 或 DROP 操作后，立即清理已删除数据，快速释放存储空间
- **批量写入后数据整理**：大批量数据写入后，对数据文件进行整理排序，加速后续查询性能

手动重组功能与自动重组功能兼容，互不影响，同时具有以下特点：

- 对当前分区数据执行重组操作
- 对不连续的 entity 数据进行重组排序，整理分散的 block 以提高查询效率（无论是否有删除操作）
- 及时检查并清理已删除表的相关数据
- 将内存数据持久化到磁盘，并合并 last 文件

### 重组配置

- **自动重组**：自动数据重组功能默认启用，用户可以通过 `ts.auto_vacuum.enabled` 实时参数选择是否启用或禁用该功能。有关详细信息，参见[集群实时参数](./cluster-settings-config.md#实时参数)。
- **手动重组**：用户需要通过执行立即重组命令 [`VACUUM TS DATABASES;`](../sql-reference/other-sql-statements/vacuum.md) 命令手动触发重组操作。

## 时序分布式日志存储引擎

时序分布式日志存储引擎（RaftLog Store）是专门针对分布式集群时序数据场景的存储优化，通过减少磁盘 IO 压力和优化写入路径，在机械硬盘环境下显著提升数据写入性能。

该功能适用于分布式集群、大量时序数据写入、机械硬盘存储环境且对写入性能要求较高的应用场景。

启用后，系统会在数据目录的时序引擎目录下自动创建 `raftlog` 子目录，当前文件达到 512 MB 时自动转换为历史文件，每 30 分钟检查一次合并需求。

### 功能配置

启用时序分布式日志存储引擎需要在节点启动命令中添加 `--use-raft-store` 参数。

::: warning 注意

- 该参数必须在数据库**首次安装启动时**指定，默认为关闭状态。
- 数据库初始化完成后，**无法**通过修改启动参数切换存储引擎。

:::

启动命令的更多信息和示例，参见[kwbase start](../kaiwudb-tools/kwbase-cli-tool.md#kwbase-start)。