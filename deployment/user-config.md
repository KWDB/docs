---
title: 创建用户
id: user-config-docker
---

# 创建用户

集群部署和启动后，用户可以使用安装包目录中的 `add_user.sh` 脚本或使用 kwbase CLI 为数据库创建用户，然后使用该用户名和密码连接和操作数据库。

如果跳过用户创建步骤，系统将默认使用部署数据库时的用户，且无需密码即可访问数据库。

## 使用创建用户脚本

KWDB 在安装包中提供了 `add_user.sh` 脚本。在安装并运行 KWDB 后，用户可以运行此脚本为数据库创建用户和密码，并使用创建的用户名和密码来连接、登录数据库。

:::warning 说明

- 如需创建多个用户，可以多次执行 `add_user.sh` 脚本。
- 安装用户为 root 用户或者配置了 `sudo` 免密的普通用户，在执行脚本时无需输入密码。未配置 `sudo` 免密的普通用户，在执行脚本时，需要输入密码进行提权。

:::

### 前提条件

- 已安装且成功启动 KWDB 数据库。
- 拥有 KWDB 安装包目录的访问权限。

### 配置步骤

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

## 使用 kwbase CLI 

### 前提条件

- 已安装且成功启动 KWDB 数据库。

### 配置步骤

1. 进入 kwbase CLI 所在目录，根据部署方式选择相应的命令创建用户并授予管理员权限。

    - 源码编译部署：

        - 非安全模式（不带密码）：

            ```bash
            ./kwbase sql --host=127.0.0.1:$(local_port) --insecure \
            -e "create user $user_name; \
                grant admin to $user_name with admin option;"
            ```

        - 安全模式（带密码）：

            ```bash
            ./kwbase sql --certs-dir=$cert_path --host=127.0.0.1:$(local_port) \
            -e "create user $user_name with password \"$user_password\"; \
                grant admin to $user_name with admin option;"
            ```

    - Docker Run 部署：

        - 非安全模式（不带密码）：

            ```bash
            docker exec kaiwudb-container bash -c "./kwbase sql --insecure -e \"create user $user_name;grant admin to $user_name with admin option;\""
            ```

        - 安全模式（带密码）：

            ```bash
            docker exec kaiwudb-container bash -c "./kwbase sql -e \"create user $user_name with password \\\"$user_password\\\";grant admin to $user_name with admin option;\"
            ```