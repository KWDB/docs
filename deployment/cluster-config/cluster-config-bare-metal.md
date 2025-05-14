---
title: 裸机部署配置集群
id: cluster-config-bare-metal
---

# 裸机部署配置集群

使用部署脚本部署完 KWDB 集群以后，用户可以按需配置 KWDB 集群。

部署完成后，系统会将 KWDB 封装成系统服务，并生成 `kaiwudb.service` 和 `kaiwudb_env` 两个文件。用户可以按需配置 KWDB 集群。

- `kaiwudb_env`：配置 KWDB 启动参数。
- `kaiwudb.service`：配置 KWDB 的 CPU 资源占用率。

## 配置启动参数

:::warning 说明
启动参数是节点级配置。如需修改整个集群的配置，用户需要登录集群中的每个节点并完成相应的配置。
:::

通常情况下，如果用户没有配置启动参数，系统会使用参数默认值启动 KWDB。当用户配置了启动参数，KWDB 启动时会优先使用配置的启动参数。部署完 KWDB 后，用户可以按需修改 `kaiwudb_env` 文件中的启动参数。有关所有支持的启动参数，参见[集群参数配置](../../db-operation/cluster-settings-config.md)。

1. 停止 KWDB 服务。

    ```sql
    systemctl stop kaiwudb
    ```

2. 进入 `/etc/kaiwudb/script` 目录，打开 `kaiwudb_env` 文件。

3. 根据需要，配置 KWDB 启动参数。

    以下示例将 `--cache` 启动参数设置为 `10000`。

    ```yaml
    KAIWUDB_START_ARG="--cache=10000"
    ```

4. 保存 `kaiwudb_env` 文件并重新加载文件。

    ```shell
    systemctl daemon-reload
    ```

5. 重新启动 KWDB 服务。

    ```sql
    systemctl restart kaiwudb
    ```

## 配置 CPU 资源占用率

:::warning 说明
CPU 资源占用率是节点级配置。如需修改整个集群的配置，用户需要登录集群中的每个节点并完成相应的配置。
:::

KWDB 支持实时修改 CPU 资源占用率。

1. 进入 `/etc/systemd/system` 目录，打开 `kaiwudb.service` 文件。
2. 根据需要，修改 KWDB 的 CPU 资源占用率。

    以下示例将 CPU 资源占用率（`CPUQuota`）设置为 `180%`。

    ```yaml
    ...
    [Service]
    ...
    CPUQuota=180%
    ...
    ```

    `CPUQuota` 的计算公式为：CPU 占用率 x 服务器CPU核数 x 100%。例如，假设节点所在服务器的 CPU 核数为 6，计划将 CPU 占用率调整为 0.3, 则对应的 `CPUQuota` 的值应为 `0.3 x 6 x 100% = 180%`。

3. 保存 `kaiwudb.service` 文件并重新加载文件。
  
    ```shell
    systemctl daemon-reload
    ```

4. 确认新的 CPU 资源占用率是否生效。

    ```shell
    systemctl show kaiwudb | grep CPUQuota
    ```
