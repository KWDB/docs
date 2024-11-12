---
title: 卸载集群
id: uninstall-cluster-docker
---

# 卸载集群

本文介绍如何卸载使用容器部署的 KWDB 集群。以下是卸载的具体步骤：

1. 登录安装部署集群的初始节点，将 `kwdb_install` 目录传输到集群的所有其他节点。
    1. 登录远程节点。

        ```shell
        ssh <username>@<node2_address> "mkdir -p ~/kwdb_install"
        ssh <username>@<node3_address> "mkdir -p ~/kwdb_install"
        ...
        ```
        
    2. 传输 `kwdb_install` 目录到目标节点。

        ```shell
        scp -r kwdb_install <username>@<node2_address>:~/kwdb_install/
        scp -r kwdb_install <username>@<node3_address>:~/kwdb_install/
        ...    
        ```

2. 在集群的每个节点执行以下操作：
    1. 停止 KWDB 服务。

        ```shell
        systemctl stop kaiwudb
        ``` 

    2. 在 `kwdb_install` 目录下执行数据库卸载命令。

        ```shell
        ./deploy.sh uninstall 
        ```
    3. 确认是否删除数据目录。输入 `y` 将删除数据目录，取消 KWDB 数据目录下的 loop 设备挂载。输入 `n` 将保留数据目录。

        ```shell
        When uninstalling KaiwuDB, you can either delete or keep all user data. Please confirm your choice: Do you want to delete the data? (y/n): 
        ``` 

        卸载完成后，控制台输出以下信息：

        ```shell
        [UNINSTALL COMPLETED]:KaiwuDB has been uninstalled successfully.
        ```