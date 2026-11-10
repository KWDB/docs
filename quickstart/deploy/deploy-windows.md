---
title: kwbase windows CLI 部署
id: quickstart-windows-cli
---

# kwbase windows CLI 部署

## 环境准备

### msys2依赖安装

（1）依赖包下载，下载后放在指定目录下

下载地址可参考：https://mirror.umd.edu/msys2/distrib/x86_64/msys2-base-x86_64-20260322.sfx.exe

（2）双击，执行完毕后会在当前目录创建msys2目录`<msys64>`并把所有二进制解压到该目录下

（3）进入msys2目录下，执行名称为 `mingw64.exe` 的二进制程序, 进入msys2命令行，当出现 `Initial setup complete. MSYS2 is now ready to use.`后，输入命令

     ```bash
     pacman -S --noconfirm mingw-w64-x86_64-libwinpthread  mingw-w64-x86_64-gcc-libs mingw-w64-x86_64-dlfcn mingw-w64-x86_64-zlib
     ``` 

### GO 环境准备

（1）下载 GO zip 包
下载地址可参考：https://golang.google.cn/dl/

（2）放在指定目录下，解压目录为`<go_dir>`

## KWDB 安装

1. [获取 KWDB windows 安装包](https://www.kaiwudb.com/download?tab=2)

2. 放在目标路径下，解压目录为`<kwdb_dir>`

3. 创建数据目录`<data_dir>`

4. 打开命令行，设置环境变量

    ```bash
    set PATH=<msys64>\mingw64\bin;<kwdb_dir>\kaiwudb

    set GOROOT=<go_dir>\go
     ```

5. （可选）如需采用安全模式，执行以下步骤创建证书：

    （1）创建证书存放目录`<certs_dir>`

    （2）生成证书和密钥：

     ```bash
     # 创建数据库证书颁发机构及密钥
     kwbase cert create-ca --certs-dir=<certs_dir> --ca-key=<certs_dir>\ca.key
    
     # 创建 root 用户或安装数据库用户的客户端证书及密钥
     kwbase cert create-client <username> --certs-dir=<certs_dir> --ca-key=<certs_dir>\ca.key
    
     # 创建节点服务器证书及密钥
     kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=<certs_dir> --ca-key=<certs_dir>\ca.key
     ```

6. 启动数据库

    - 非安全模式：

     ```bash
     kwbase start-single-node --insecure --listen-addr=0.0.0.0:26257 --http-addr=0.0.0.0:8080  --store=<data_dir>
     ```

    - 安全模式：

     ```bash
     ./kwbase start-single-node  --certs-dir=<certs_dir>  --listen-addr=0.0.0.0:26257 --http-addr=0.0.0.0:8080 --store=<data_dir>
     ```

     ::: Tips
     windows环境不支持 `--background`
     :::

7. 数据库状态查看

    打开新的命令行，设置环境变量

     ```bash
     set PATH=<msys64>\mingw64\bin;<kwdb_dir>\kaiwudb
     ```

    查看状态：   

     ```bash
     # 非安全模式
     kwbase node status --insecure --host=0.0.0.0:26257

     # 安全模式
     kwbase node status --certs-dir=<certs_dir> --host=0.0.0.0:26257
     ```

    登录数据库

     ```bash
     # 非安全模式
     kwbase sql --insecure --host=0.0.0.0:26257

     # 安全模式
     kwbase sql --certs-dir=<certs_dir> --host=0.0.0.0:26257
     ```
  
8. 部署完成后，[KaiwuDB JDBC](../access/access-jdbc.md)或 [KWDB 开发者中心](../access/access-kdc.md)连接并管理 KWDB。
