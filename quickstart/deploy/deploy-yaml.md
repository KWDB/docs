---
title: YAML 文件部署
id: quickstart-yaml
---

# YAML 文件部署

## 前提条件

- 已获取 KWDB [容器安装包](../prepare.md#安装包)。
- 待部署节点的硬件、操作系统、软件依赖和端口满足[安装部署要求](../prepare.md)。
- 安装用户为 root 用户或者拥有 `sudo` 权限的普通用户。
  - root 用户和配置 `sudo` 免密的普通用户在执行部署脚本时无需输入密码。
  - 未配置 `sudo` 免密的普通用户在执行部署脚本时，需要输入密码进行提权。
- 安装用户为非 root 用户时，需要通过 `sudo usermod -aG docker $USER` 命令将用户添加到 `docker` 组。

## 步骤

1. 在 `kwdb_install/packages` 目录下导入 `KaiwuDB.tar` 文件，获取镜像名称。

    ```shell
    docker load < KaiwuDB.tar
    Loaded image: "$kwdb_image"
    ```

2. 创建 `docker-compose.yml` 配置文件。

    ::: warning 说明
    `image` 参数的取值必须是导入 `KaiwuDB.tar` 文件后获取的镜像名称。
    :::

    配置文件示例：

    ```yaml
    version: '3.3'
    services:
      kwdb-container:
        image: "$kwdb_image"
        container_name: kwdb-experience
        hostname: kwdb-experience
        ports:
          - 8080:8080
          - 26257:26257
        ulimits:
          memlock: -1
        networks: 
          - default
        restart: on-failure
        ipc: shareable
        privileged: true
        environment:
          - LD_LIBRARY_PATH=/kaiwudb/lib
        tty: true
        working_dir: /kaiwudb/bin
        command: 
          - /bin/bash
          - -c
          - |
            /kaiwudb/bin/kwbase start-single-node --insecure --listen-addr=0.0.0.0:26257 --advertise-addr=127.0.0.1:26257 --http-addr=0.0.0.0:8080 --store=/kaiwudb/deploy/kaiwudb
    ```

3. 快速启动 KWDB。

    ```shell
    docker-compose up -d
    ```
4. 部署完成后，可通过 [kwbase CLI ](../access/access-cli.md) 、[KaiwuDB JDBC](../access/access-jdbc.md)或 [KaiwuDB 开发者中心](../access/access-kdc.md)连接并管理 KWDB。
