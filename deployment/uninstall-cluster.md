---
title: 卸载集群
id: uninstall-cluster
---

# 卸载集群

本节介绍了 KWDB 数据库在不同部署方式下的卸载方法，包括使用部署脚本、编译版本及容器镜像部署的数据库卸载流程。请根据实际部署方式选择合适的卸载方案。

## 脚本部署

1. 登录安装部署集群的初始节点。
2. 将 `kwdb_install` 目录传输到集群的所有其他节点。
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

3. 在集群的每个节点执行以下操作：
    1. 停止 KWDB 服务。

        ```shell
        systemctl stop kaiwudb
        ```

    2. 在 `kwdb_install` 目录下执行数据库卸载命令。

        ```shell
        ./deploy.sh uninstall 
        ```

    3. 确认是否删除数据目录。输入 `y` 将删除数据目录。输入 `n` 将保留数据目录。

        ```shell
        When uninstalling KaiwuDB, you can either delete or keep all user data. Please confirm your choice: Do you want to delete the data? (y/n): 
        ```

## 源码编译部署

对于通过源码编译部署的 KWDB，在每个节点上执行以下操作：

::: warning 注意

执行删除操作前，请确保已备份所有重要数据。以下操作将永久删除 KWDB 的所有数据和配置。

:::

1. 停止 KWDB 服务。

2. 删除自定义证书目录。

   ```bash
   sudo rm -rf <cert_path>
   ```

3. 删除数据目录。

   ```bash
   sudo rm -rf <data_path>
   ```

4. 删除编译的二进制文件和库。

## 容器镜像部署

对于通过容器镜像部署的 KWDB，在每个节点上执行以下操作：

::: warning 注意

执行删除操作前，请确保已备份所有重要数据。以下操作将永久删除 KWDB 的所有数据和配置。

:::

1. 停止 KWDB 容器。

   ::: warning 提示

   容器名称为运行容器时通过 `--name` 参数指定的容器名称。
   :::

   ```bash
   docker stop kwdb-container
   ```

2. 移除容器。

   ```bash
   docker rm kwdb-container
   ```

3. 删除 Docker 镜像。

   ```bash
   # 获取镜像名称
   docker ps -a --filter name=kwdb-container --format {{.Image}}
   
   # 删除镜像
   docker rmi ${image_name}
   ```

4. 删除自定义证书目录。

   ```bash
   sudo rm -rf <cert_path>
   ```

5. 删除数据目录（默认为 `/var/lib/kaiwudb`）。

   ```bash
   sudo rm -rf <data_path>
   ```
