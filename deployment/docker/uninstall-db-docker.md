---
title: 卸载 KWDB 数据库
id: uninstall-db-docker
---

# 卸载数据库

本文介绍如何卸载使用容器镜像部署的 KWDB 数据库。

在待卸载数据库的节点上，执行以下操作。

1. 停止 KWDB 服务。

    ```shell
    systemctl stop kaiwudb
    ```

2. 删除名为 `kaiwudb-container` 的 Docker 容器。

    ```shell
    docker rm kaiwudb-container
    ```

3. 删除名为 `kaiwudb-container` 的 Docker 镜像。

    1. 获取镜像名称。

        ```shell
        docker ps -a --filter name=kaiwudb-container --format {{.Image}}
        ubuntu
        ```

    2. 删除镜像：

        ```shell
        docker rmi <image_name>
        ```

4. 检查是否有 loop 设备挂载在 KWDB 数据目录下。
    
    ```shell
    df -h
    ```

5. 如果有设备挂载，取消设备挂载。

    ```shell
    umount /dev/loop<device_number>
    ```   


6. 删除 `/etc/kaiwudb` 目录及其内容。

    ```shell
    sudo rm -rf /etc/kaiwudb
    ```

7. 删除与 KWDB 服务相关的 `systemd` 配置文件。

    ```shell
    sudo rm -rf /etc/systemd/system/kaiwudb.service
    ```

8. 删除 KWDB 的数据目录及其内容。默认情况下，数据目录为 `/var/lib/kaiwudb`。

    ```shell
    sudo rm -rf <data_root>
    ```
