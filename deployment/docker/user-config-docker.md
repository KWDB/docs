---
title: 创建用户
id: user-config-docker
---

# 创建用户

KWDB 在安装包中提供了 `add_user.sh` 脚本。在安装并运行 KWDB 后，用户可以运行此脚本为数据库创建用户和密码，并使用创建的用户名和密码来连接、登录数据库。

:::warning 说明

- 如需创建多个用户，可以多次执行 `add_user.sh` 脚本。
- 安装用户为 root 用户或者配置了 `sudo` 免密的普通用户，在执行脚本时无需输入密码。未配置 `sudo` 免密的普通用户，在执行脚本时，需要输入密码进行提权。

:::

## 前提条件

已安装且成功启动 KWDB 数据库。

## 配置步骤

1. 在目标机器上，进入 KWDB 安装包目录。

2. 执行 `add_user.sh` 脚本，根据系统提示创建用户名和密码。

    ```shell
    ./add_user.sh
    Please enter the username:
    Please enter the password:
    ```

    执行成功后，控制台输出以下信息：

    ```shell
    [ADD USER COMPLETED]:User creation completed.
    ```
