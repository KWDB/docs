---
title: kwbase windows CLI 部署
id: deploy-windows-cli
---

# kwbase windows CLI 部署

This section describes how to deploy a KWDB cluster on a single machine, including the complete process of starting multiple nodes and initializing the cluster. Note: In a real production environment, it is recommended to deploy only one node per machine to improve availability and reduce the risk of data loss.

## Environment preparation

### msys2 dependency installation

(1)Download the dependency package and place it in the specified directory after downloading.

Download reference link: https://mirror.umd.edu/msys2/distrib/x86_64/msys2-base-x86_64-20250830.sfx.exe

(2) Double-click it. After execution completes, an msys2 directory `<msys64>` will be created in the current directory, and all binaries will be extracted into this directory.

(3) Go into the msys2 directory and run the binary program named `mingw64.exe` to enter the MSYS2 command line. Once you see `Initial setup complete. MSYS2 is now ready to use.`, enter the command 

     ```bash
     pacman -S --noconfirm mingw-w64-x86_64-libwinpthread  mingw-w64-x86_64-gcc-libs mingw-w64-x86_64-dlfcn mingw-w64-x86_64-zlib
     ``` 

### GO Environment Preparation

（1）Download the GO zip package. Download reference:https://golang.google.cn/dl/

（2）Place it in the specified directory, and the decompression directory is `<go_dir>`

## 安装

1. [Obtain the KWDB Windows installation package ](https://www.kaiwudb.com/download?tab=2)

2. Place it in the target path, and the decompression directory is `<kwdb_dir>`

3. Create the data directory`<data_dir1>、<data_dir2>、<data_dir3>`

4. Open the command line and set environment variables

     ```bash
     set PATH=<msys64>\mingw64\bin;<kwdb_dir>\kaiwudb

     set GOROOT=<go_dir>\go
     ```

5. （ (Optional) For secure mode, create certificates and keys by following these steps:

    （1）Create a directory to store the certificates and keys`<certs_dir>`

    （2）Generate certificates and keys:

     ```bash
     # Create database certificate authority and key
     kwbase cert create-ca --certs-dir=<certs_dir> --ca-key=<certs_dir>\ca.key
    
     # Create client certificate and key for the root user or database installation user
     kwbase cert create-client <username> --certs-dir=<certs_dir> --ca-key=<certs_dir>\ca.key
    
     # Create client certificate and key for the root user or database installation user
     kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=<certs_dir> --ca-key=<certs_dir>\ca.key
     ```

    ::: warning 

    When deploying in cross-machine mode, use the `./kwbase cert create-node <node_ip>` command to create certificates and keys for all nodes, and transfer all certificates and keys to every node in the cluster.

    :::

6. Start the cluster and complete cluster initialization.
    
    Taking a multi-replica cluster in non-secure mode as an example: open a CMD command prompt window, or double-click to run the cluster-start.bat script

     The reference for the cluster-start.bat script is as follows:

     ```bash
     :: =====================Modify the path configuration as needed=====================
     set "msys64_dir=D:\msys64"
     set "kwdb_dir=D:\KaiwuDB\windows\KaiwuDB-Windows"
     set "go_dir=D:\KaiwuDB\windows\go1.21.13.windows-amd64"
     set "msys64_dir=D:\KaiwuDB\windows\msys64"

     set "data_dir1=D:\KaiwuDB\windows\cluster-data\data1"
     set "data_dir2=D:\KaiwuDB\windows\cluster-data\data2"
     set "data_dir3=D:\KaiwuDB\windows\cluster-data\data3"

     :: =============Start the cluster and complete cluster initialization.===============
     set PATH=%msys64_dir%\mingw64\bin;%kwdb_dir%\kaiwudb
     set GOROOT=%go_dir%\go

     :: Start node 1
     start kwbase start --insecure --listen-addr=0.0.0.0:26257 --advertise-addr=0.0.0.0:26257 --http-addr=0.0.0.0:8080 --store=%data_dir1% --join=0.0.0.0:26257

     :: Start node 2
     start kwbase start --insecure --listen-addr=0.0.0.0:26258 --advertise-addr=0.0.0.0:26258 --http-addr=0.0.0.0:8081 --store=%data_dir2% --join=0.0.0.0:26257

     :: Start node 3
     start kwbase start --insecure --listen-addr=0.0.0.0:26259 --advertise-addr=0.0.0.0:26259 --http-addr=0.0.0.0:8082 --store=%data_dir3% --join=0.0.0.0:26257

     :: Init
     start  kwbase init --insecure --host=0.0.0.0:26257 
     ```
     
    ::: Tips
     - The Windows environment does not support `--background`.
     - Cluster initialization in secure mode:
        ```bash
        kwbase init --certs-dir=<certs_dir> --host=0.0.0.0:26257
        ```
    :::

7. Check database status and login.

    在脚本执行窗口操作：
    
    - Check status

     ```bash
     - Insecure mode
     kwbase node status --insecure --host=0.0.0.0:26257

     - Secure mode
     ./kwbase node status --certs-dir=<certs_dir> --host=0.0.0.0:26257
     ```
    - Login database

     ```bash
     - Secure mode
     kwbase node status --insecure --host=0.0.0.0:26257

     - Secure mode
     ./kwbase node status --certs-dir=<certs_dir> --host=0.0.0.0:26257
     ```

8. After deployment, connect to and manage KWDB using [KaiwuDB JDBC](../access/access-jdbc.md), or [KaiwuDB Developer Center](../access/access-kdc.md).