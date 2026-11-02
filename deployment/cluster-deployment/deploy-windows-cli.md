---
title: kwbase windows CLI 部署
id: deploy-windows-cli
---

# kwbase windows CLI 部署

本节介绍如何在单台机器上部署 KWDB 集群，包括启动多个节点并初始化集群的完整过程。注意：在实际生产环境中，建议每台机器仅部署一个节点，以提升可用性并降低数据丢失风险。

## 环境准备

### msys2依赖安装

（1）依赖包下载，下载后放在指定目录下

下载地址可参考：https://mirror.umd.edu/msys2/distrib/x86_64/msys2-base-x86_64-20260322.sfx.exe

（2）双击，执行完毕后会在当前目录创建msys2目录<msys64>并把所有二进制解压到该目录下

（3）进入msys2目录下，执行名称为 `mingw64.exe` 的二进制程序, 进入msys2命令行，当出现 `Initial setup complete. MSYS2 is now ready to use.`后，输入命令`pacman -S --noconfirm mingw-w64-x86_64-libwinpthread  mingw-w64-x86_64-gcc-libs mingw-w64-x86_64-dlfcn mingw-w64-x86_64-zlib` 完成依赖安装。

### GO 环境准备

（1）下载 GO zip 包
下载地址可参考：https://golang.google.cn/dl/

（2）放在指定目录下，解压目录为<go_dir>

## 安装

1. 获取 KWDB windows 安装包[下载](https://www.kaiwudb.com/download?tab=2)

2. 放在目标路径下，解压目录为<kwdb_dir>

3. 创建数据目录<data_dir1>、<data_dir2>、<data_dir3>

4. 打开命令行，设置环境变量

     ```bash
     set PATH=<msys64>\mingw64\bin;<kwdb_dir>\kaiwudb

     set ZONEINFO=<go_dir>\go1.21.13.windows-amd64\go\lib\time\zoneinfo.zip
     ```

5. （可选）如需采用安全模式，执行以下步骤创建证书：

    （1）创建证书存放目录<certs_dir>

    （2）生成证书和密钥：

     ```bash
     # 创建数据库证书颁发机构及密钥
     ./kwbase cert create-ca --certs-dir=<certs_dir> --ca-key=<certs_dir>\ca.key
    
     # 创建安装数据库用户的客户端证书及密钥
     ./kwbase cert create-client <username> --certs-dir=<certs_dir> --ca-key=<certs_dir>\ca.key
    
     # 创建节点服务器证书及密钥
     ./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=<certs_dir> --ca-key=<certs_dir>\ca.key
     ```

    ::: warning 提示

    如果采用跨机器安全模式部署，需要使用 `kwbase cert create-node <node_ip>` 命令为所有节点创建证书和密钥，并将所有证书和密钥传输至所有节点。

    :::

6. 启动集群节点。

    以多副本集群、非安全模式为例：

     ```bash
     # 启动第一个节点
     kwbase start --insecure  --listen-addr=0.0.0.0:26257  --advertise-addr=0.0.0.0:26257 --http-addr=0.0.0.0:8080  --store=<data_dir1>  --join=<host1>:26257

     # 启动第二个节点
     kwbase start --insecure  --listen-addr=0.0.0.0:26257  --advertise-addr=0.0.0.0:26258 --http-addr=0.0.0.0:8080  --store=<data_dir2>  --join=<host1>:26257

     # 启动第三个节点
     kwbase start --insecure  --listen-addr=0.0.0.0:26257  --advertise-addr=0.0.0.0:26259 --http-addr=0.0.0.0:8080  --store=<data_dir3>  --join=<host1>:26257
     ```
    ::: Tips
     windows环境不支持 `----background`
    :::

4. 初始化集群。

    打开新的命令行，设置环境变量

     ```bash
     set PATH=<msys64>\mingw64\bin;<kwdb_dir>\kaiwudb
     ```

    初始化集群

    ```bash
     - 非安全模式：
     kwbase init --insecure --host=0.0.0.0:26257

     - 安全模式：
     ./kwbase init --certs-dir=<certs_dir> --host=0.0.0.0:26257
    ```

5. 查看集群状态并登录。

    状态查看：

     ```bash
     - 非安全模式：
     kwbase node status --insecure --host=0.0.0.0:26257

     - 安全模式：
     ./kwbase node status --certs-dir=<certs_dir> --host=0.0.0.0:26257
     ```
    登录数据库：

     ```bash
     - 非安全模式：
     kwbase node status --insecure --host=0.0.0.0:26257

     - 安全模式：
     ./kwbase node status --certs-dir=<certs_dir> --host=0.0.0.0:26257
     ```

6. 部署完成后，[KWDB 支持的连接器](../../development/overview.md)或 [KaiwuDB 开发者中心](../../kaiwudb-tools/kaiwudb-developer-center/overview.md)连接并管理 KWDB。