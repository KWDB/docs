---
title: 存储管理
id: storage-mgmt
---

# 存储管理

KWDB 支持在安装时通过修改 `deploy.cfg` 文件中的 `data_root` 参数自定义数据路径。部署完成后，用户也可以修改部署生成的 `kaiwudb_env` 文件或 `docker-compose.yml` 文件中的存储路径。更多配置信息，参见[集群参数配置](./cluster-settings-config.md)。

::: warning 说明
如果采用 Docker 容器部署，则使用宿主机路径，系统自动进行挂载。
:::

下表列出 KWDB 各类文件的存储路径、文件系统和配置信息。

| 文件       | 默认路径               | 大小               | 文件系统                                                   | 配置参数    |
| ---------- | ---------------------- | ------------------ | ---------------------------------------------------------- | ----------- |
| 数据文件   | `/var/lib/kaiwudb`       | 取决于存储数据的大小 | 建议使用 ext4 文件系统。如果存储大于 16 TB 的数据，建议使用 XFS 系统。 | `--store`     |
| 日志       | `/var/lib/kaiwudb/logs`  | 默认 1G，可配置    | 建议使用 ext4 文件系统。                                       | `--log-dir`   |
| 证书       | `/etc/kaiwudb/certs`     | N/A                | 建议使用 ext4 文件系统。                                       | `--certs-dir` |
| 二进制文件 | `/usr/local/kaiwudb/bin` | > 200 M              | 建议使用 ext4 文件系统。                                       | -           |
| 动态库文件 | `/usr/local/kaiwudb/lib` | > 100 M              | 建议使用 ext4 文件系统。                                       | -           |

## 数据压缩

数据压缩是用更少的空间对原有数据进行编码的过程，其核心在于去除冗余和不必要的数据，同时保持数据的核心信息和完整性。KWDB 支持在线周期数据压缩，具备 5-30 倍的数据压缩能力，有助于降低数据存储成本。同时，系统可以直接挂载压缩数据，无需解压缩即可查询数据。

### 数据压缩算法

KWDB 支持以下无损压缩算法：

- GZIP：对于要压缩的文件，GZIP 首先使用 LZ77 算法的一个变种进行压缩，对得到的结果再使用 Huffman 编码的方法进行压缩，压缩率很高，但比较耗时。
- LZ4：属于 LZ77 压缩方案家族，压缩比并不高，但是解码速度极快。
- LZMA：LZMA（Lempel-Ziv-Markov chain Algorithm）是一种 DEFLATE 和 LZ77 算法改良和优化后的压缩算法。它使用类似于 LZ77 的字典编码机制。
- LZO：LZO 是块压缩算法，属于 LZ77 压缩方案家族。该算法旨在快速压缩和解压缩。由于块中可能存放多种类型的数据，整体的压缩效果没有针对某一种数据类型进行压缩的算法好。
- XZ：采用 LZMA2 算法，具有非常高的压缩比，但压缩和解压速度相对较慢。
- ZSTD（Zstandard）：是一种提供高压缩比的快速压缩算法。ZSTD 采用有限状态熵（Finite State Entropy，FSE）编码器，提供非常强大的压缩速度、压缩率的折中方案。

默认情况下，KWDB 采用 GZIP 压缩算法。如需设置其他算法，参见[集群实时参数配置](./cluster-settings-config.md#实时参数)。

::: warning 说明
当 mksquashfs 数据压缩工具 或者 mount 挂载工具不支持某种算法时，系统默认采用 GZIP 压缩算法并且以 WARN 日志的形式输出告警信息。
:::

#### KWDB 软件依赖支持的数据压缩算法

::: warning 说明

- mksquashfs、mount 或 squashfuse 必须同时支持某种压缩算法。
- 采用 Docker 部署 KWDB 时，需要添加 `-v /boot:/boot` 目录映射，或者复制宿主机 `/boot/config-$(uname -r)` 文件到 Docker 的 `/boot` 目录下。然后重启 KWDB。否则，系统仅支持 GZIP 压缩算法。

:::

- mksquashfs 压缩工具

    mksquashfs 压缩工具支持以下算法：

    | 版本           | 压缩算法                  |
    | -------------- | ------------------------- |
    | 4.0 及以下版本 | GZIP                      |
    | 4.1            | GZIP、LZMA、LZO           |
    | 4.2            | GZIP、LZMA、LZO、XZ       |
    | 4.3            | GZIP、LZMA、LZO、XZ、LZ4  |
    | 4.4 及以上版本 | GZIP、LZMA、LZO、XZ、ZSTD |

- mount 挂载工具支持的压缩算法与内核对 squashfs 的压缩算法支持有关。例如，

  - CentOS 7：支持挂载 GZIP、LZO、XZ 压缩的 `.sqfs` 文件。
  - Ubuntu 20.04/24.04：支持挂载 GZIP、LZO、XZ、LZ4、ZSTD 压缩的 `.sqfs` 文件。

### 数据压缩级别

数据的压缩级别与压缩速度和压缩率相关。压缩级别越高，压缩速度越慢，压缩效果越好，压缩后的文件越小。反之，压缩级别越低，压缩速度越快，压缩效果越差，压缩后的文件越大。KWDB 支持以下压缩级别：

- low：低压缩级别，通常情况下，压缩率相对较低，压缩速度快。
- middle：中压缩级别，通常情况下，兼顾压缩率及压缩速度。
- high：高压缩级别，通常情况下，压缩率相对较高，压缩速度慢。

下表列出 KWDB 支持的压缩算法与压缩级别之间的关系。

<table>
  <thead>
    <tr>
      <th>压缩级别</th>
      <th colspan="6">压缩算法</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>GZIP</td>
      <td>LZO</td>
      <td>ZSTD</td>
      <td>LZ4</td>
      <td>XZ</td>
      <td>LZMA</td>
    </tr>
    <tr>
      <td>low</td>
      <td>有效</td>
      <td>有效</td>
      <td>有效</td>
      <td>有效，等同于 middle</td>
      <td>无效</td>
      <td>无效</td>
    </tr>
    <tr>
      <td>middle</td>
      <td>有效</td>
      <td>有效</td>
      <td>有效</td>
      <td>有效</td>
      <td>无效</td>
      <td>无效</td>
    </tr>
        <tr>
      <td>high</td>
      <td>有效</td>
      <td>有效</td>
      <td>有效</td>
      <td>有效</td>
      <td>无效</td>
      <td>无效</td>
    </tr>
  </tbody>
</table>
