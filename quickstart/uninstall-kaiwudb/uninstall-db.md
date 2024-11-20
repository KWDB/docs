---
title: 卸载 KWDB 数据库
id: uninstall-db
---

# 卸载 KWDB 数据库

本文介绍如何卸载 KWDB 单机版本。

在待卸载数据库的节点上，执行以下操作。

1. 停止 KWDB 服务。

    ```shell
    systemctl stop kaiwudb
    ```

2. 进入 `kwdb_install` 目录。

3. 执行数据库卸载命令。

    ```shell
    ./deploy.sh uninstall 
    ```

4. 确认是否删除数据目录。输入 `y` 将删除数据目录，取消 KWDB 数据目录下的 loop 设备挂载。输入 `n` 将保留数据目录。

    ```shell
    When uninstalling KaiwuDB, you can either delete or keep all user data. Please confirm your choice: Do you want to delete the data? (y/n): 
    ``` 

    卸载完成后，控制台输出以下信息：

    ```shell
    [UNINSTALL COMPLETED]:KaiwuDB has been uninstalled successfully.
    ```