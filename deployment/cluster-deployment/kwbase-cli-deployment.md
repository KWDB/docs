---
title: kwbase CLI 部署
id: kwbase-cli-deployment
---

# kwbase CLI 部署

本节介绍如何通过 kwbase CLI 命令在单台机器上部署 KWDB 集群，包括启动多个节点并初始化集群的完整过程。注意：在实际生产环境中，建议每台机器仅部署一个节点，以提升可用性并降低数据丢失风险。

**前提条件**

- 节点的硬件配置、操作系统、软件依赖和端口满足[部署要求](../prepare/before-deploy-bare-metal.md#硬件)
- 安装用户为 `root` 用户或拥有 `sudo` 权限的普通用户
- 已完成[源码编译和安装](https://gitee.com/kwdb/kwdb#%E7%BC%96%E8%AF%91%E5%92%8C%E5%AE%89%E8%A3%85)

**步骤**

1. 进入 `kwbase` 脚本所在目录：

   ```bash
   cd /home/go/src/gitee.com/kwbasedb/install/bin
   ```

2. （可选）如需采用安全模式，执行以下步骤创建证书：

    1. 创建证书存放目录：

        ```bash
        mkdir -p <certs_dir>
        ```

    2. 生成证书和密钥：

        ```bash
        # 创建数据库证书颁发机构及密钥
        ./kwbase cert create-ca --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key
        
        # 创建安装数据库用户的客户端证书及密钥
        ./kwbase cert create-client <username> --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key
        
        # 创建节点服务器证书及密钥
        ./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key
        ```

        ::: warning 提示

        如果采用跨机器安全模式部署，需要使用 `./kwbase cert create-node <node_ip>` 命令为所有节点创建证书和密钥，并将所有证书和密钥传输至所有节点。

        :::

3. 启动集群节点。

    - 单副本集群：

        - 非安全模式：

            ```bash
            # 启动第一个节点
            ./kwbase start-single-replica --insecure \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host1>:26257 \
            --brpc-addr=:27257 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257

            # 启动第二个节点
            ./kwbase start-single-replica --insecure \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host2>:26258 \
            --brpc-addr=:27258 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257

            # 启动第三个节点
            ./kwbase start-single-replica --insecure \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host3>:26259 \
            --brpc-addr=:27259 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257
            ```

        - 安全模式：

            ```bash
            # 启动第一个节点
            ./kwbase start-single-replica \
            --certs-dir=<certs_dir> \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host1>:26257 \
            --brpc-addr=:27257 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257

            # 启动第二个节点
            ./kwbase start-single-replica \
            --certs-dir=<certs_dir> \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host2>:26258 \
            --brpc-addr=:27258 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257

            # 启动第三个节点
            ./kwbase start-single-replica \
            --certs-dir=<certs_dir> \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host3>:26259 \
            --brpc-addr=:27259 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257
            ```

    - 多副本集群：

        - 非安全模式：

            ```bash
            # 启动第一个节点
            ./kwbase start --insecure \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host1>:26257 \
            --brpc-addr=:27257 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257

            # 启动第二个节点
            ./kwbase start --insecure \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host2>:26258 \
            --brpc-addr=:27258 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257

            # 启动第三个节点
            ./kwbase start --insecure \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host3>:26259 \
            --brpc-addr=:27259 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257
            ```

        - 安全模式：

            ```bash
            # 启动第一个节点
            ./kwbase start \
            --certs-dir=<certs_dir> \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host1>:26257 \
            --brpc-addr=:27257 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257

            # 启动第二个节点
            ./kwbase start \
            --certs-dir=<certs_dir> \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host2>:26258 \
            --brpc-addr=:27258 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257

            # 启动第三个节点
            ./kwbase start \
            --certs-dir=<certs_dir> \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host3>:26259 \
            --brpc-addr=:27259 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257
            ```

4. 初始化集群。

    - 非安全模式：

        ```bash
        ./kwbase init --insecure --host=<address_of_any_node>
        ```

    - 安全模式：

        ```bash
        ./kwbase init --certs-dir=<certs_dir> --host=<address_of_any_node>
        ```

5. 查看集群状态。

    - 非安全模式：

        ```bash
        ./kwbase node status --insecure --host=<address_of_any_alive_node>
        ```

    - 安全模式：

        ```bash
        ./kwbase node status --certs-dir=<certs_dir> --host=<address_of_any_alive_node>
        ```