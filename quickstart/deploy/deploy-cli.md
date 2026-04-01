---
title: kwbase CLI 部署
id: quickstart-cli
---

# kwbase CLI 部署

## 前提条件

- 已获取 KWDB [裸机安装包](../prepare.md#安装包)。
- 待部署节点的硬件配置、操作系统、软件依赖和端口满足[安装部署要求](../prepare.md)
- 安装用户为 `root` 用户或拥有 `sudo` 权限的普通用户

::: warning 说明

本节介绍的 kwbase CLI 部署方式**仅适用于裸机部署**，不适用于容器部署。如需容器部署，请参考 [Docker Run 部署](./deploy-docker-run.md)。

:::

## 步骤

1. 登录待部署节点，进入安装包目录下的 `packages` 目录。

2. 安装依赖包和服务器组件。

   - DEB 包系统（Debian/Ubuntu）：

     ```bash
     dpkg -i ./kaiwudb-libcommon-<版本号>.deb ./kaiwudb-server-<版本号>.deb
     ```

   - RPM 包系统（CentOS/RHEL）：

     ```bash
     rpm -ivh ./kaiwudb-libcommon-<版本号>.rpm ./kaiwudb-server-<版本号>.rpm
     ```

3. 切换至程序目录：

   ```bash
   cd /usr/local/kaiwudb/bin
   ```

4. (可选）如需采用安全部署模式，执行以下步骤创建证书：

    1. 创建证书存放目录：

        ```bash
        mkdir -p /usr/local/kaiwudb/certs
        ```

    2. 生成证书和密钥。

        ```bash
        # 创建数据库证书颁发机构及密钥
        ./kwbase cert create-ca --certs-dir=/usr/local/kaiwudb/certs --ca-key=/usr/local/kaiwudb/certs/ca.key && \
        
        # 创建安装数据库用户的客户端证书及密钥（USERNAME 替换为实际用户名）
        ./kwbase cert create-client $USERNAME --certs-dir=/usr/local/kaiwudb/certs --ca-key=/usr/local/kaiwudb/certs/ca.key && \
        
        # 创建节点服务器证书及密钥
        ./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=/usr/local/kaiwudb/certs --ca-key=/usr/local/kaiwudb/certs/ca.key
        ```

5. 启动数据库。

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
            --certs-dir=/usr/local/kaiwudb/certs \
            --listen-addr=0.0.0.0:26257 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb
        ```

6. 查看数据库状态。

    - 非安全模式：

        ```bash
        ./kwbase node status --insecure --host=<address_of_any_alive_node>
        ```

    - 安全模式：

        ```bash
        ./kwbase node status --certs-dir=/usr/local/kaiwudb/certs --host=<address_of_any_alive_node>
        ```

7. （可选）创建数据库用户并授予用户管理员权限。如果跳过该步骤，系统将默认使用部署数据库时的用户，且无需密码访问数据库。

    - 非安全模式（不带密码）：

        ```bash
        ./kwbase sql --host=127.0.0.1:$local_port --insecure \
        -e "create user $username; \
            grant admin to $username with admin option;"
        ```

    - 安全模式（带密码）：

        ```bash
        ./kwbase sql --certs-dir=/usr/local/kaiwudb/certs --host=127.0.0.1:$local_port \
        -e "create user $username with password \"$user_password\"; \
            grant admin to $username with admin option;"
        ```

8. 部署完成后，可通过 [kwbase CLI ](../access/access-cli.md) 、[KWDB JDBC](../access/access-jdbc.md)或 [KWDB 开发者中心](../access/access-kdc.md)连接并管理 KWDB。
