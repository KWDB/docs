---
title: kwbase CLI 部署
id: quickstart-cli
---

# kwbase CLI 部署

## 前提条件

- 已完成[源码编译和安装](https://gitee.com/kwdb/kwdb#%E7%BC%96%E8%AF%91%E5%92%8C%E5%AE%89%E8%A3%85)。
- 待部署节点的硬件配置、操作系统、软件依赖和端口满足[安装部署要求](../prepare.md)
- 安装用户为 `root` 用户或拥有 `sudo` 权限的普通用户

::: warning 说明

本节介绍的 kwbase CLI 部署方式**仅适用于裸机部署**。

:::

## 步骤

1. 进入 `kwbase` 脚本所在目录：

   ```bash
   cd /home/go/src/gitee.com/kwbasedb/install/bin
   ```

2. (可选）如需采用安全模式，执行以下步骤创建证书：

    1. 创建证书存放目录：

        ```bash
        mkdir -p <certs_dir>
        ```

    2. 生成证书和密钥：

        ```bash
        # 创建数据库证书颁发机构及密钥
        ./kwbase cert create-ca --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key
        
        # 创建 root 用户或安装数据库用户的客户端证书及密钥
        ./kwbase cert create-client <username> --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key
        
        # 创建节点服务器证书及密钥
        ./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key
        ```

3. 启动数据库:

    - 非安全模式：

        ```bash
        ./kwbase start-single-node --insecure \
            --listen-addr=0.0.0.0:26257 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb
        ```

    - 安全模式：

        ```bash
        ./kwbase start-single-node \
            --certs-dir=<certs_dir> \
            --listen-addr=0.0.0.0:26257 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb
        ```

4. 查看数据库状态

    - 非安全模式：

        ```bash
        ./kwbase node status --insecure --host=<address_of_any_alive_node>
        ```

    - 安全模式：

        ```bash
        ./kwbase node status --certs-dir=<certs_dir> --host=<address_of_any_alive_node>
        ```

5. （可选）创建数据库用户并授予用户管理员权限。如果跳过该步骤，系统将默认使用源码编译安装时使用的用户，且无需密码访问数据库。

    - 非安全模式（不带密码）：

        ```bash
        ./kwbase sql --host=127.0.0.1:<local_port> --insecure \
        -e "create user <username>; \
            grant admin to <username> with admin option;"
        ```

    - 安全模式（带密码）：

        ```bash
        ./kwbase sql --certs-dir=<certs_dir> --host=127.0.0.1:<local_port> \
        -e "create user <username> with password \"<user_password>\"; \
            grant admin to <username> with admin option;"
        ```

6. 部署完成后，可通过 [kwbase CLI ](../access/access-cli.md) 、[KaiwuDB JDBC](../access/access-jdbc.md)或 [KWDB 开发者中心](../access/access-kdc.md)连接并管理 KWDB。
