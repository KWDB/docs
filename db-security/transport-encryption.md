---
title: 加密传输
id: transport-encryption
---

# 加密传输

默认情况下，KWDB 采用安全模式部署 KWDB 集群，使用 TLS 加密技术来验证节点和客户端的身份，对节点与客户端、以及节点之间的传输数据进行加密。这一机制有效地防范了未经授权的用户访问和篡改数据，保障了数据的安全性和完整性。

## 启用安全模式

默认情况下，KWDB 采用安全模式部署 KWDB 集群。用户可以在安装部署时选择启用或禁用安全模式。

启用安全模式后，部署 KWDB 时，将生成 TLS 安全证书，作为客户端或应用程序连接数据库的凭证，并将生成的相关证书存放在 `/etc/kaiwudb/certs` 目录。KWDB 还会在安装包目录生成 `kaiwudb_certs.tar.gz`，便于后续扩容集群时使用。

更多配置相关信息，参见[集群部署](../deployment/overview.md)。

## 管理和存放证书

默认情况下，部署完 KWDB 后，生成的相关证书存放在 `/etc/kaiwudb/certs` 目录。如需修改证书的存放目录，用户可以修改 `kaiwudb_env` 文件或者 `docker-compose.yml` 文件中的 `--certs-dir` 参数，指定证书的存放目录。其中，`kaiwudb_env` 文件为裸机部署后生成的文件，`docker-compose.yml` 文件为容器部署后生成的文件，文件路径均为 `/etc/kaiwudb/script`。具体配置信息，参见[集群参数配置](../db-operation/cluster-settings-config.md)。

- 裸机部署 `kaiwudb_env` 文件配置示例：

    ```yaml
    KAIWUDB_START_ARG="--certs-dir=<certs_dir>"
    ```

- 容器部署 `docker-compose.yml` 文件配置示例：

    ```yaml
    command: 
          - /bin/bash
          - -c
          - |
            /kaiwudb/bin/kwbase  start-single-node --certs-dir=<certs_dir> --listen-addr=0.0.0.0:26257 --advertise-addr=your-host-ip:port --store=/kaiwudb/deploy/kwdb-container
    ```
