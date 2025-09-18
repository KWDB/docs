---
title: 卸载 KWDB 数据库
id: uninstall-db
---

# 卸载 KWDB 数据库

本节介绍了 KWDB 数据库在不同部署方式下的卸载方法，包括使用部署脚本、编译版本及容器镜像部署的数据库卸载流程。请根据实际部署方式选择合适的卸载方案。

## 脚本部署卸载

对于通过安装包脚本部署的 KWDB，在待卸载节点上执行以下操作：

1. 停止 KWDB 服务。

    ```shell
    systemctl stop kaiwudb
    ```

2. 进入 `kwdb_install` 目录。

3. 执行数据库卸载命令。

    ```shell
    ./deploy.sh uninstall 
    ```

4. 确认是否删除数据目录。输入 `y` 将删除数据目录。输入 `n` 将保留数据目录。

    ```shell
    When uninstalling KaiwuDB, you can either delete or keep all user data. Please confirm your choice: Do you want to delete the data? (y/n): 
    ```

    卸载完成后，控制台输出以下信息：

    ```shell
    [UNINSTALL COMPLETED]:KaiwuDB has been uninstalled successfully.
    ```

## 源码编译部署卸载

对于通过源码编译部署的 KWDB，在待卸载节点上执行以下操作：

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

## 容器镜像部署卸载

对于通过容器镜像部署的 KWDB，在待卸载节点上执行以下操作：

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
