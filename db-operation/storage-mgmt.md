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
