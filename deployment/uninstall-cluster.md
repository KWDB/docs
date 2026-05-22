---
title: 卸载 KWDB
id: uninstall-cluster
---

# 卸载 KWDB

本节介绍了 KWDB 数据库在不同部署方式下的卸载方法，包括安装程序部署、kwbase CLI 部署及容器镜像部署。请根据实际部署方式选择合适的卸载方案。

## 安装程序部署卸载

对于通过安装程序部署的 KWDB，根据安装时选择的交互模式，选择对应的卸载方式。

### 命令行模式

**前提条件**：已停止 KWDB 服务。

```bash
systemctl stop kaiwudb
```

**步骤**：

1. 登录安装部署 KWDB 的初始节点，执行以下命令以命令行模式启动安装程序：

    ```bash
    ./KWDB-*.run -c
    # 或者
    ./KWDB-*.run --cli
    ```

2. 在主功能菜单中，输入 `2` 选择卸载 KWDB：

    ```plain
    1. 安装 KWDB
    2. 卸载 KWDB
    3. 安装 KWDB 并加入集群
    4. 升级节点
    5. 退出

    请输入操作 [1-5]:
    ```

3. 根据提示输入要删除的节点数量：

    ```plain
    请输入节点数量(1-100):
    ```

4. 安装程序自动打开配置文件，确认节点信息无误后保存退出。配置文件格式如下：

    ```ini
    [global]
    # 数据目录
    data_root=/var/lib/kaiwudb

    [node1]
    host=127.0.0.1
    port=22
    user=admin
    passwd=*******
    ```

5. 根据提示确认是否删除数据及配置文件。输入 `y` 删除，输入 `N` 保留：

    ```plain
    是否删除数据及配置文件(y/N):
    ```

    卸载完成后，控制台提示已成功卸载所有节点，并安全退出脚本。

### 终端图形交互模式

**前提条件**：已停止 KWDB 服务。

```bash
systemctl stop kaiwudb
```

**步骤**：

1. 登录安装部署 KWDB 的初始节点，执行以下命令以终端图形交互模式启动安装程序：

    ```bash
    ./KWDB-*.run -i
    # 或者
    ./KWDB-*.run --interact
    ```

2. 在主功能菜单中，使用方向键选中**卸载 KWDB**，按回车确认。

3. 进入参数设置菜单，根据需要依次选择各配置项进行设置：

    配置项说明：

    | 配置项 | 说明 |
    |--------|------|
    | 设置卸载节点 | 添加待卸载节点信息，需填写主机名、端口号、用户名和密码。 |
    | 管理卸载节点列表 | 查看已添加的节点信息。 |
    | 设置数据目录 | 输入待删除的数据目录，默认为 `/var/lib/kaiwudb`。 |

4. 所有配置完成后，选中**开始卸载**，按回车开始卸载。

5. 根据提示确认是否删除所有配置及数据。卸载完成后，界面提示卸载完成。

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
   docker stop <kwdb-container>
   ```

2. 移除容器。

   ```bash
   docker rm <kwdb-container>
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
