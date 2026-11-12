---
title: kwbase windows CLI Deployment
id: quickstart-windows-cli
---

# kwbase windows CLI Deployment

## Environment preparation

### msys2 dependency installation

(1)Download the dependency package and place it in the specified directory after downloading.

Download reference link: https://mirror.umd.edu/msys2/distrib/x86_64/msys2-base-x86_64-20260322.sfx.exe

(2) Double-click it. After execution completes, an msys2 directory `<msys64>` will be created in the current directory, and all binaries will be extracted into this directory.

(3) Go into the msys2 directory and run the binary program named `mingw64.exe` to enter the MSYS2 command line. Once you see `Initial setup complete. MSYS2 is now ready to use.`,enter the command 

     ```bash
     pacman -S --noconfirm mingw-w64-x86_64-libwinpthread  mingw-w64-x86_64-gcc-libs mingw-w64-x86_64-dlfcn mingw-w64-x86_64-zlib
     ``` 

### GO Environment Preparation

（1）Download the GO zip package. Download reference:https://golang.google.cn/dl/

（2）Place it in the specified directory, and the decompression directory is `<go_dir>`

## KWDB Installation

1. Obtain the KWDB Windows installation package [Download][下载](https://www.kaiwudb.com/download?tab=2)

2. Place it in the target path, and the decompression directory is `<kwdb_dir>`

3. Create the data directory `<data_dir>`

4. Open the command line and set environment variables

    ```bash
    set PATH=<msys64>\mingw64\bin;<kwdb_dir>\kaiwudb

    set GOROOT=<go_dir>\go
     ```

5. （ (Optional) For secure mode, create certificates and keys by following these steps:

    （1）Create a directory to store the certificates and keys `<certs_dir>`

    （2）Generate certificates and keys:

     ```bash
     # Create database certificate authority and key
     kwbase cert create-ca --certs-dir=<certs_dir> --ca-key=<certs_dir>\ca.key
    
     # Create client certificate and key for the root user or database installation user
     kwbase cert create-client <username> --certs-dir=<certs_dir> --ca-key=<certs_dir>\ca.key
    
     # Create client certificate and key for the root user or database installation user
     kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=<certs_dir> --ca-key=<certs_dir>\ca.key
     ```

6. Start the database

    - Insecure mode:

     ```bash
     kwbase start-single-node --insecure --listen-addr=0.0.0.0:26257 --http-addr=0.0.0.0:8080  --store=<data_dir>
     ```

    - Secure mode:

     ```bash
     ./kwbase start-single-node  --certs-dir=<certs_dir>  --listen-addr=0.0.0.0:26257 --http-addr=0.0.0.0:8080 --store=<data_dir>
     ```

     ::: Tips
     The Windows environment does not support `--background`.
     :::

7. Check database status.

    Open a new command line and set the environment variables

     ```bash
     set PATH=<msys64>\mingw64\bin;<kwdb_dir>\kaiwudb
     ```

    Check database status. 

     ```bash
     # Insecure mode
     kwbase node status --insecure --host=0.0.0.0:26257

     # Secure mode
     kwbase node status --certs-dir=<certs_dir> --host=0.0.0.0:26257
     ```

    Login database

     ```bash
     # Insecure mode
     kwbase sql --insecure --host=0.0.0.0:26257

     # Secure mode
     kwbase sql --certs-dir=<certs_dir> --host=0.0.0.0:26257
     ```
  
8. After deployment, connect to and manage KWDB using [KaiwuDB JDBC](../access/access-jdbc.md), or [KaiwuDB Developer Center](../access/access-kdc.md).
