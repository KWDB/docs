---
title: Docker Run 部署
id: quickstart-docker
---

# Docker Run 部署

## 前提条件

- 已获取 KWDB [容器安装包](../prepare.md#安装包)。
- 待部署节点的硬件、操作系统、软件依赖和端口满足[安装部署要求](../prepare.md)。
- 安装用户为 root 用户或者拥有 `sudo` 权限的普通用户。
  - root 用户和配置 `sudo` 免密的普通用户在执行部署脚本时无需输入密码。
  - 未配置 `sudo` 免密的普通用户在执行部署脚本时，需要输入密码进行提权。
- 安装用户为非 root 用户时，需要通过 `sudo usermod -aG docker $USER` 命令将用户添加到 `docker` 组。

## 步骤

1. 在 `kwdb_install/packages` 目录下导入 `KaiwuDB.tar` 文件，获取镜像名称。

    ```shell
    docker load < KaiwuDB.tar
    Loaded image: "$kwdb_image"
    ```

2. （可选）如需以安全模式部署 KWDB, 使用以下命令创建数据库证书颁发机构、`root` 用户的客户端证书以及节点服务器证书。

    ```shell
    docker run --rm --privileged \
      -v /etc/kaiwudb/certs:/kaiwudb/certs \
      -w /kaiwudb/bin \
      $kwdb_image \
      bash -c './kwbase cert create-ca --certs-dir=/kaiwudb/certs --ca-key=/kaiwudb/certs/ca.key && \
                ./kwbase cert create-client root --certs-dir=/kaiwudb/certs --ca-key=/kaiwudb/certs/ca.key && \
                ./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=/kaiwudb/certs --ca-key=/kaiwudb/certs/ca.key'
    ```

    参数说明：
    
    | 参数 | 说明 |
    |---|---|
    | `--rm` | 容器停止后自动删除。 |
    | `--privileged` | 给予容器扩展权限。 |
    | `-v` | 设置容器目录映射，将主机的 `/etc/kaiwudb/certs` 目录挂载到容器内的 `/kaiwudb/certs` 目录，用于存放证书和密钥。 |
    | `-w /kaiwudb/bin` | 将容器内的工作目录设置为 `/kaiwudb/bin`。 |
    | `$kwdb_image` | 容器镜像，需填入实际的镜像名以及标签，例如 `kwdb:3.0.0`。 |
    | `bash -c` | 在容器中执行后面的证书创建命令，其中：<br>- `./kwbase cert create-ca`：创建证书颁发机构(CA)，生成 CA 证书和密钥。<br>- `./kwbase cert create-client root`：为 `root` 用户创建客户端证书和密钥。<br>- `./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0`：创建节点证书和密钥，支持通过三种网络标识符访问：本地回环地址 (`127.0.0.1`)、本地主机名 (`localhost`) 和所有网络接口 (`0.0.0.0`)。<br>- 所有命令均使用 `--certs-dir=/kaiwudb/certs` 指定证书存储目录，使用 `--ca-key=/kaiwudb/certs/ca.key` 指定密钥路径。 |

3. 启动 KWDB 数据库。

    - 非安全模式

      ```shell
      docker run -d --privileged --name kaiwudb \
        --ulimit memlock=-1 \
        --ulimit nofile=$max_files \
        -p $db_port:26257 \
        -p $http_port:8080 \
        -v /var/lib/kaiwudb:/kaiwudb/deploy/kaiwudb-container \
        --ipc shareable \
        -w /kaiwudb/bin \
        $kwdb_image \
        ./kwbase start-single-node \
          --insecure \
          --listen-addr=0.0.0.0:26257 \
          --http-addr=0.0.0.0:8080 \
          --store=/kaiwudb/deploy/kaiwudb-container
      ```

    - 安全模式

        ```bash
        docker run -d --privileged --name kaiwudb \
          --ulimit memlock=-1 \
          --ulimit nofile=$max_files \
          -p $db_port:26257 \
          -p $http_port:8080 \
          -v /etc/kaiwudb/certs:/kaiwudb/certs \
          -v /var/lib/kaiwudb:/kaiwudb/deploy/kaiwudb-container \
          --ipc shareable \
          -w /kaiwudb/bin \
          $kwdb_image \
          ./kwbase start-single-node \
            --certs-dir=/kaiwudb/certs \
            --listen-addr=0.0.0.0:26257 \
            --http-addr=0.0.0.0:8080 \
            --store=/kaiwudb/deploy/kaiwudb-container
        ```

    参数说明：

    | 参数 | 说明 |
    |---|---|
    | `-d` | 后台运行容器并返回容器 ID。 |
    | `--name` | 指定容器名称，便于后续管理。 |
    | `--privileged` | 给予容器扩展权限。 |
    | `--ulimit memlock=-1` | 取消容器内存大小限制。 |
    | `--ulimit nofile=$max_files` | 设置容器内进程可以打开的最大文件数。 |
    | `-p` | 端口映射，分别映射数据库服务端口（26257）和 HTTP 端口（8080）。|
    | `-v` | 设置容器目录映射：<br>- 将主机的 `/var/lib/kaiwudb` 目录挂载到容器内的 `/kaiwudb/deploy/kaiwudb-container` 目录，用于持久化数据存储。<br>- 安全模式下，将主机的 `/etc/kaiwudb/certs` 目录挂载到容器内的 `/kaiwudb/certs` 目录，用于存放证书和密钥。 |
    | `--ipc shareable` | 允许其他容器共享此容器的IPC命名空间。 |
    | `-w /kaiwudb/bin` | 将容器内的工作目录设置为 `/kaiwudb/bin`。 |
    | `$kwdb_image` | 容器镜像变量，需替换为实际的镜像名称及标签，例如 `kwdb:3.0.0`。 |
    | `./kwbase start` | 容器内运行的数据库启动命令，根据安全模式和非安全模式有所不同：<br>- `--insecure`：（仅非安全模式）以非安全模式运行。<br>- `--certs-dir=/kaiwudb/certs`：（安全模式）证书目录位置。<br>- `--listen-addr=0.0.0.0:26257`：数据库监听的地址和端口。<br>- `--http-addr=0.0.0.0:8080`：HTTP 接口监听的地址和端口。<br>- `--store=/kaiwudb/deploy/kaiwudb-container`：指定数据存储位置。|

4. （可选）创建数据库用户并授予用户管理员权限。如果跳过该步骤，系统将默认使用部署数据库时的用户，且无需密码访问数据库。

      - 非安全模式（不带密码）：

          ```bash
          docker exec kaiwudb bash -c "./kwbase sql --insecure --host=$host_ip -e \"create user $username;grant admin to $username with admin option;\""
          ```

      - 安全模式（带密码）：

          ```bash
          docker exec kaiwudb bash -c "./kwbase sql --host=$host_ip --certs-dir=$cert_path -e \"create user $username with password \\\"$user_password\\\";grant admin to $username with admin option;\""
          ```

5. 部署完成后，可通过 [kwbase CLI ](../access/access-cli.md) 、[KaiwuDB JDBC](../access/access-jdbc.md)或 [KaiwuDB 开发者中心](../access/access-kdc.md)连接并管理 KWDB。
