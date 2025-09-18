---
title: 容器部署配置集群
id: cluster-config-docker
---

# 容器部署配置集群

使用脚本在容器中完成集群部署后，系统会将 KWDB 封装成系统服务，生成 Docker Compose 配置文件 `docker-compose.yml`，用于配置 KWDB 的启动参数和 CPU 资源占用率。

:::warning 说明

启动参数和 CPU 资源占用率配置为节点级配置。如需修改整个集群的配置，用户需要登录集群中的每个节点并完成相应的配置。

:::

## 配置启动参数

通常情况下，如果用户没有配置启动参数，系统会使用参数默认值启动 KWDB。当用户配置了启动参数，KWDB 启动时会优先使用配置的启动参数。部署完 KWDB 后，用户可以按需修改 `docker-compose.yml` 文件中的启动参数。有关所有支持的启动参数，参见[集群参数配置](../../db-operation/cluster-settings-config.md)。

1. 进入 `/etc/kaiwudb/script` 目录，停止并删除 KWDB 容器。

    ```shell
    docker-compose down
    ```

2. 进入 `/etc/kaiwudb/script` 目录，打开 `docker-compose.yml` 文件。

3. 根据需要，在 `docker-compose.yml` 文件的启动命令后添加启动参数或修改已有参数值。

    :::warning 说明
    请勿删除默认的启动命令参数。否则可能导致修改集群配置后，无法启动集群。
    :::

    以下示例添加 `--cache` 启动参数，并将参数值设置为 `25%`。

    ```yaml
    ...
        command: 
          - /bin/bash
          - -c
          - |
            /kaiwudb/bin/kwbase start-single-node --certs-dir=<certs_dir> --listen-addr=0.0.0.0:26257 --brpc-addr=:27257 --advertise-addr=your-host-ip:port --store=/kaiwudb/deploy/kwdb-container --cache=25%
    ```

4. 保存配置, 重新创建并启动 KWDB 容器。

    ```shell
    systemctl start kaiwudb
    ```

## 配置 CPU 资源占用率

部署完 KWDB 后，用户可以使用 `docker update` 命令或者修改 `docker-compose.yml` 文件来配置 KWDB 的 CPU 资源占用率。

- 使用 `docker update` 命令

    运行 `docker update` 命令，配置 KWDB 的 `cpus` 参数。

    ```dockerfile
    docker update --cpus <value> kwdb-container
    ```

    `cpus` 的计算公式为：CPU 占用率 x 服务器 CPU 核数。例如，假设节点所在服务器的 CPU 核数为 6，计划将 CPU 占用率调整为 0.3, 则对应的 `cpus` 的值应为 `0.3 x 6 = 1.8`。

- 修改 `docker-compose.yml` 文件

    1. 进入 `/etc/kaiwudb/script` 目录，停止并删除 KWDB 容器。

        ```shell
        docker-compose down
        ```

    2. 进入 `/etc/kaiwudb/script` 目录，打开 `docker-compose.yml` 文件。

    3. 根据需要，修改 KWDB 的 CPU 资源占用率。

        以下示例将 CPU 资源占用率（`cpus`）设置为 `1.8`。

        ```yaml
        version: '3.3'
        services:
        ...
          deploy:
            resources: -1 
              limits:
                cpus:'1.8'     
        ...
        ```

        `cpus` 的计算公式为：CPU 占用率 x 服务器 CPU 核数。例如，假设节点所在服务器的 CPU 核数为 6，计划将 CPU 占用率调整为 0.3, 则对应的 `cpus` 的值应为 `0.3 x 6 = 1.8`。

    4. 保存配置, 重新创建并启动 KWDB 容器。

        ```shell
        systemctl start kaiwudb
        ```
