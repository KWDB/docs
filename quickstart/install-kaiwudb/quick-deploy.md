---
title: 快速部署
id: quick-deploy
---

# 快速部署

KWDB 为首次体验的用户提供了自动化部署工具——快速部署脚本 `quick_deploy.sh`。用户运行脚本后，系统会自动完成系统检测、参数配置、安装包下载和部署全流程。

快速部署脚本适用于首次体验 KWDB 和开发测试环境的用户。

支持两种使用方式：

- [**交互模式**（推荐）](#交互模式)：运行 `./quick_deploy.sh`，按照提示逐步输入配置
- [**参数模式**](#参数模式)：运行 `./quick_deploy.sh -i <ip_address> -s <service_port> ...`，适合熟悉命令行的用户

## 支持的系统

脚本会自动检测系统并选择部署方式：

- **裸机部署**：Ubuntu 20.04/22.04、Kylin V10 SP3
- **容器部署**：其他 Linux 发行版

## 前提条件

- **硬件**：4核8G及以上（详见[硬件要求](./quickstart-bare-metal.md#硬件)）
- **权限**：root 或具有 sudo 权限的用户
- **网络**：能够访问安装包下载地址
- **快速部署脚本**：通过 [Gitee](https://gitee.com/kwdb/kwdb/releases)、[Github](https://github.com/KWDB/KWDB/releases) 或 [GitCode](https://gitcode.com/kwdb/kwdb) 获取快速部署脚本

## 部署步骤

### 交互模式

1. 运行脚本：

    ```bash
    # 添加执行权限
    chmod +x quick_deploy.sh

    # 运行脚本
    sudo ./quick_deploy.sh
    ```

2. 按照提示依次输入配置信息（直接回车使用默认值）：

    ```bash
    正在收集系统信息...
    请按照提示依次输入：
    KWDB 版本（如 3.0.0）: 
    监听地址（IP，默认 127.0.0.1）: 
    服务端口（默认 26257）: 
    HTTP 端口（默认 8080）: 
    安全模式（insecure/tls，默认 insecure）: 
    数据路径（默认 /var/lib/kaiwudb）: 
    ```

3. 提示 "请确认以上信息是否正确? (y/n):" 时，检查配置无误后输入 `y`:

    ```bash
    ========== 用户输入 ==========
    IP 地址: 127.0.0.1
    服务端口: 26257
    HTTP 端口: 8080
    安全模式: insecure
    数据路径: /var/lib/kaiwudb
    请确认以上信息是否正确? (y/n): y
    ```

4. 等待部署完成。部署成功后显示：

    ```shell
    [INSTALL COMPLETED]:KaiwuDB has been installed successfully! To start KaiwuDB, please execute the command 'systemctl daemon-reload'.
    ```

5. 启动 KWDB：

    ```bash
    # 重新加载服务
    systemctl daemon-reload

    # 启动 KWDB
    systemctl start kaiwudb
    ```

6. 连接 KWDB:

    - 裸机部署

      ```bash
      /usr/local/kaiwudb/bin/kwbase sql --insecure --host=127.0.0.1
      ```

    - 容器部署

      ```bash
      docker exec -it kaiwudb-container ./kwbase sql --insecure --host=127.0.0.1
      ```

    出现以下提示表示连接成功：

    ```shell
    # Welcome to the KWDB SQL shell.
    # All statements must be terminated by a semicolon.
    # To exit, type: \q.
    #
    # Server version: KaiwuDB 3.0.0 (x86_64-linux-gnu, built 2025/11/11 02:23:47, go1.21.13, gcc 11.4.0) (same version as client)
    # Cluster ID: 4a8dfac8-83ce-4dc3-b0af-9faa7e0431ac
    #
    # Enter \? for a brief introduction.
    #
    root@127.0.0.1:26257/defaultdb>
    ```

### 参数模式

参数模式适合熟悉命令行的用户：

```shell
./quick_deploy.sh -i <ip_address> -s <service_port> -h <http_port> -m <security_mode> -p <data_path>
```

参数说明：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-i` | 监听地址（IP） | 127.0.0.1 |
| `-s` | 服务端口 | 26257 |
| `-h` | HTTP 端口 | 8080 |
| `-m` | 安全模式（insecure/tls） | insecure |
| `-p` | 数据存储路径 | /var/lib/kaiwudb |

**示例：**

```bash
./quick_deploy.sh -i 192.168.1.100 -s 26257 -h 8080 -m tls -p /data/kaiwudb
```

## 常见问题

### 快速部署脚本支持哪些操作系统？

裸机部署支持 Ubuntu 20.04/22.04 和 Kylin V10 SP3；其他 Linux 系统脚本会自动选择容器部署方式。

### 部署失败如何排查？

检查以下内容：

1. 终端输出的错误信息
2. 安装目录下的日志文件（通常在 `/var/log/kaiwudb/` 或安装目录的 `log` 目录）
3. 确认硬件、操作系统、端口等是否满足要求

### 如何修改已部署的配置？

快速部署后如需修改配置，建议：

1. 卸载当前部署（参见[卸载 KWDB](../uninstall-kaiwudb/uninstall-db.md)）
2. 使用[裸机部署](./quickstart-bare-metal.md)或[容器部署](./quickstart-docker.md)重新部署，可进行详细配置
