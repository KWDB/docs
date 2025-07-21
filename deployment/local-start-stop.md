---
title: 启动与停止 KWDB 服务
id: local-start-stop-docker
---

# 启动与停止 KWDB 服务

本文介绍如何启动、停止、重启集群中的单个 KWDB 节点。执行所有命令时都需要 `root` 或 `sudo` 权限。

## 启动 KWDB 服务

1. 启动 KWDB 服务。

    ```shell
    systemctl start kaiwudb
    ```

2. 确认 KWDB 服务已启动。

    ```shell
    systemctl status kaiwudb
    ```

## 停止 KWDB 服务

1. 如需停止正在运行的 KWDB 服务：

    ```shell
    systemctl stop kaiwudb
    ```

## 重启 KWDB 服务

1. 如需重启正在运行的 KWDB 服务：

    :::warning 说明
    如果 KWDB 服务处于停止状态，用户需要先启动 KWDB 服务，然后再重启服务。
    :::

    ```shell
    systemctl restart kaiwudb
    ```

## 查看 KWDB 服务状态

1. 如需查询当前节点的 KWDB 服务状态：

    ```shell
    systemctl status kaiwudb
    ```