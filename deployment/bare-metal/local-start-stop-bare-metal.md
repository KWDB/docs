---
title: 启动与停止 KWDB 服务
id: local-start-stop-bare-metal
---

# 启动与停止 KWDB 服务

本文介绍如何启动、停止、重启集群中的单个 KWDB 节点。

- 启动 KWDB 服务。

    ```shell
    systemctl start kaiwudb
    ```

- 停止 KWDB 服务。

    ```shell
    systemctl stop kaiwudb
    ```

- 重启 KWDB 服务。

    :::warning 说明
    如果 KWDB 服务处于停止状态，用户需要先启动 KWDB 服务，然后再重启服务。
    :::

    ```shell
    systemctl restart kaiwudb
    ```
