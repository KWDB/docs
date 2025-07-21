---
title: Docker Run 命令部署
id: docker-deployment
---

# Docker Run 命令部署

本节介绍如何通过 Docker Run 命令在单节点上部署 KWDB 集群。注意：在实际生产环境中，建议每台机器仅部署一个节点，以提升可用性并降低数据丢失风险。

## 前提条件

- 已获取 [KWDB 容器镜像](../prepare/before-deploy-docker.md#获取容器镜像)。
- 待部署节点的硬件、操作系统、软件依赖和端口满足[安装部署要求](../prepare/before-deploy-docker.md#硬件)。
- 安装用户为 root 用户或者拥有 `sudo` 权限的普通用户。
  - root 用户和配置 `sudo` 免密的普通用户在执行部署脚本时无需输入密码。
  - 未配置 `sudo` 免密的普通用户在执行部署脚本时，需要输入密码进行提权。
- 安装用户为非 root 用户时，需要通过 `sudo usermod -aG docker $USER` 命令将用户添加到 `docker` 组。

## 部署步骤

1. （可选）如需以安全模式部署 KWDB 集群, 使用以下命令创建数据库证书颁发机构、`root` 用户的客户端证书以及节点服务器证书。

    ::: warning 提示

    如果采用跨机器安全模式部署，需要使用 `./kwbase cert create-node <node_ip>` 命令为所有节点创建证书和密钥，并将 CA 证书和密钥、节点证书和密钥传输至所有节点；如果需要在其它节点上运行 KaiwuDB 客户端命令，还需要将 `root` 用户的证书和密钥复制到该节点。只有拥有 `root` 用户证书和密钥的节点，才能够访问集群。

    :::

      ```shell
      docker run --rm --privileged \
        -v /etc/kaiwudb/certs:<certs_dir> \
        -w /kaiwudb/bin \
        <kwdb_image> \
        bash -c './kwbase cert create-ca --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key && \
                  ./kwbase cert create-client root --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key && \
                  ./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key'
      ```

    参数说明：
    - `--rm`：容器停止后自动删除。
    - `--privileged`：给予容器扩展权限。
    - `-v`：设置容器目录映射, 将主机的 `/etc/kaiwudb/certs` 目录挂载到容器内的 `<certs_dir>` 目录，用于存放证书和密钥。
    - `-w /kaiwudb/bin`：将容器内的工作目录设置为 `/kaiwudb/bin`。
    - `kwdb_image`：容器镜像，需填入实际的镜像名以及标签, 例如 `kwdb:2.2.0`。
    - `bash -c`：在容器中执行后面的证书创建命令, 其中：
      - `./kwbase cert create-ca`: 创建证书颁发机构(CA)，生成 CA 证书和密钥。
      - `./kwbase cert create-client root`: 为 `root` 用户创建客户端证书和密钥。
      - `./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0`: 创建节点服务器证书和密钥，支持通过三种网络标识符访问：本地回环地址 (`127.0.0.1`)、本地主机名 (`localhost`) 和所有网络接口 (`0.0.0.0`)。
      - 所有命令均使用 `--certs-dir=<certs_dir>` 指定证书存储目录，使用 `--ca-key=<certs_dir>/ca.key` 指定 CA 密钥路径。

2. 启动三个及以上数据库实例。

    - 非安全模式

      ```shell
      # 启动第一个容器
      docker run -d --name kwdb1 --privileged \
        --ulimit memlock=-1 --ulimit nofile=1048576 \
        -p 26257:26257 -p 8080:8080 \
        -v /var/lib/kwdb1:/kaiwudb/deploy/kwdb-container \
        -v /dev:/dev \
        --ipc shareable -w /kaiwudb/bin \
        <kwdb_image> \
        ./kwbase start --insecure --listen-addr=0.0.0.0:26257 \
        --advertise-addr=<host1>:26257 --http-addr=0.0.0.0:8080 \
        --store=/kaiwudb/deploy/kwdb-container --join <host1>:26257

      # 启动第二个容器
      docker run -d --name kwdb2 --privileged \
        --ulimit memlock=-1 --ulimit nofile=1048576 \
        -p 26258:26257 -p 8081:8080 \
        -v /var/lib/kaiwudb2:/kaiwudb/deploy/kwdb-container \
        -v /dev:/dev \        
        --ipc shareable -w /kaiwudb/bin \
        <kwdb_image> \
        ./kwbase start --insecure --listen-addr=0.0.0.0:26257 \
        --advertise-addr=<host2>:26258 --http-addr=0.0.0.0:8080 \
        --store=/kaiwudb/deploy/kwdb-container --join <host1>:26257

      # 启动第三个容器
      docker run -d --name kwdb3 --privileged \
        --ulimit memlock=-1 --ulimit nofile=1048576 \
        -p 26259:26257 -p 8082:8080 \
        -v /var/lib/kaiwudb3:/kaiwudb/deploy/kwdb-container \
        -v /dev:/dev \        
        --ipc shareable -w /kaiwudb/bin \
        <kwdb_image> \
        ./kwbase start --insecure --listen-addr=0.0.0.0:26257 \
        --advertise-addr=<host3>:26259 --http-addr=0.0.0.0:8080 \
        --store=/kaiwudb/deploy/kwdb-container --join <host1>:26257
      ```

    - 安全模式

      ```shell
      # 启动第一个容器
      docker run -d --name kwdb1 --privileged \
        --ulimit memlock=-1 --ulimit nofile=1048576 \
        -p 26257:26257 -p 8080:8080 \
        -v /etc/kaiwudb/certs:<certs_dir> \
        -v /var/lib/kwdb1:/kaiwudb/deploy/kwdb-container \
        -v /dev:/dev \
        --ipc shareable -w /kaiwudb/bin \
        <kwdb_image> \
        ./kwbase start --certs-dir=<certs_dir> --listen-addr=0.0.0.0:26257 \
        --advertise-addr=<host1>:26257 --http-addr=0.0.0.0:8080 \
        --store=/kaiwudb/deploy/kwdb-container --join <host1>:26257

      # 启动第二个容器
      docker run -d --name kwdb2 --privileged \
        --ulimit memlock=-1 --ulimit nofile=1048576 \
        -p 26258:26257 -p 8081:8080 \
        -v /etc/kaiwudb/certs:<certs_dir> \
        -v /var/lib/kaiwudb2:/kaiwudb/deploy/kwdb-container \
        -v /dev:/dev \
        --ipc shareable -w /kaiwudb/bin \
        <kwdb_image> \
        ./kwbase start --certs-dir=<certs_dir> --listen-addr=0.0.0.0:26257 \
        --advertise-addr=<host2>:26258 --http-addr=0.0.0.0:8080 \
        --store=/kaiwudb/deploy/kwdb-container --join <host1>:26257

      # 启动第三个容器
      docker run -d --name kwdb3 --privileged \
        --ulimit memlock=-1 --ulimit nofile=1048576 \
        -p 26259:26257 -p 8082:8080 \
        -v /etc/kaiwudb/certs:<certs_dir> \
        -v /var/lib/kaiwudb3:/kaiwudb/deploy/kwdb-container \
        -v /dev:/dev \
        --ipc shareable -w /kaiwudb/bin \
        <kwdb_image> \
        ./kwbase start --certs-dir=<certs_dir> --listen-addr=0.0.0.0:26257 \
        --advertise-addr=<host3>:26259 --http-addr=0.0.0.0:8080 \
        --store=/kaiwudb/deploy/kwdb-container --join <host1>:26257
        ```

    参数说明：
    - `-d`：后台运行容器并返回容器 ID。
    - `--name`：指定容器名称，便于后续管理。
    - `--privileged`：给予容器扩展权限。
    - `--ulimit memlock=-1`：取消容器内存大小限制。
    - `--ulimit nofile=1048576`：设置容器内进程可以打开的最大文件数。
    - `-p`：端口映射，分别映射数据库服务端口（26257）和 HTTP 端口（8080）。
    - `-v`：设置容器目录映射：
      - 将主机的 `/var/lib/kaiwudb` 目录挂载到容器内的 `/kaiwudb/deploy/kwdb-container` 目录，用于持久化数据存储。
      - 安全模式下，将主机的 `/etc/kaiwudb/certs` 目录挂载到容器内的 `<certs_dir>` 目录，用于存放证书和密钥。
    - `--ipc shareable`：允许其他容器共享此容器的IPC命名空间。
    - `-w /kaiwudb/bin`：将容器内的工作目录设置为 `/kaiwudb/bin`。
    - `kwdb_image`：容器镜像变量，需替换为实际的镜像名称及标签, 例如 `kwdb:2.2.0`。
    - `./kwbase start`: 容器内运行的数据库启动命令, 根据安全模式和非安全模式有所不同:
      - `--insecure`：（仅非安全模式）以非安全模式运行。
      - `--certs-dir=<certs_dir>`：（安全模式）证书目录位置。
      - `--listen-addr=0.0.0.0:26257`：数据库监听的地址和端口。
      - `--advertise-addr=<hostx>:2625X`：数据库向集群中其他节点通信的地址和端口。
      - `--http-addr=0.0.0.0:8080`：HTTP 接口监听的地址和端口。
      - `--store=/kaiwudb/deploy/kwdb-container`：指定数据存储位置。
      - `--join <host1>:26257`：节点连接集群的地址，可指定集群中的一个或多个节点。

3. 初始化集群：

    - 非安全模式

        ```shell
        docker exec kwdb1 ./kwbase init --insecure --host=<host1>:26257
        ```

    - 安全模式

        ```shell
        docker exec kwdb1 ./kwbase init --certs-dir=<certs_dir> --host=<host1>:26257
        ```

    参数说明：
    - `docker exec kwdb1`：进入名为 `kwdb1` 的容器中执行命令。
    - `./kwbase init`：执行集群初始化命令。
      - `--insecure`：（仅非安全模式）指定以非安全模式运行。
      - `--certs-dir=<certs_dir>`：（安全模式）指定证书目录位置。
      - `--host=<host1>:26257`：指定连接的主机地址及端口。