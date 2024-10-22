---
title: 卸载 KWDB 数据库
id: uninstall-db-bare-metal
---

# 卸载数据库

本文介绍如何卸载使用二进制安装包部署的 KWDB 数据库。

在待卸载数据库的节点上，执行以下操作。

1. 停止 KWDB 服务。

    ```shell
    systemctl stop kaiwudb
    ```

2. 检查是否有 loop 设备挂载在 KWDB 数据目录下。
    
    ```shell
    df -h
    ```

3. 如果有设备挂载，取消设备挂载。

    ```shell
    umount /dev/loop<device_number>
    ```    

4. 删除与 KWDB 服务相关的 `systemd` 配置文件。

    ```shell
    sudo rm /etc/systemd/system/kaiwudb.service
    ```

5. 删除 `/etc/kaiwudb` 目录及其内容。

    ```shell
    sudo rm -rf /etc/kaiwudb/
    ```

6. 删除 KWDB 的数据目录及其内容。默认情况下，数据目录为 `/var/lib/kaiwudb`。

    ```shell
    sudo rm -rf <data_root>
    ```

7. 卸载 KWDB 服务及相关的库。

    ```shell
    sudo apt-get -y remove kaiwudb-server kaiwudb-libcommon
    ```

8. 删除 KWDB 管理用户及其关联文件。默认情况下，管理用户为 `kaiwudb`。

    ```shell
    sudo userdel -r <management_user>
    ```
