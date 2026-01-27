---
title: Quick Deployment
id: quick-deploy
---

# Quick Deployment

KWDB provides an automated deployment tool for first-time users: the **Quick Deployment Script** (`quick_deploy.sh`). By running this script, the system completes the full deployment workflow automatically, including system checks, parameter configuration, package download, and installation.

The quick deployment script is intended for users who are evaluating KWDB for the first time, as well as for development and testing environments.

Two usage modes are supported:

- [**Interactive Mode**](#interactive-mode): Run `./quick_deploy.sh` and follow the prompts to complete the configuration step by step.
- [**Parameter Mode**](#parameter-mode): Run `./quick_deploy.sh -i <ip_address> -s <service_port> ...`. This mode is suitable for users familiar with command-line operations.

## Supported Systems

The script automatically detects the operating system and selects an appropriate deployment method:

- **Bare-metal deployment**: Ubuntu 20.04/22.04 
- **Container deployment**: Other Linux distributions

## Prerequisites

- **Hardware**: 4 CPU cores and 8 GB RAM or higher (see [Hardware Requirements](./quickstart-bare-metal.md#hardware))
- **Permissions**: Root user or a user with `sudo` privileges
- **Network**: Access to the installation package download address
- **Quick deployment script**: Downloaded from [Gitee](https://gitee.com/kwdb/kwdb/releases), [GitHub](https://github.com/KWDB/KWDB/releases), or [GitCode](https://gitcode.com/kwdb/kwdb)

## Steps

### Interactive Mode

1. Run the script:

    ```bash
    # Grant execution permission
    chmod +x quick_deploy.sh

    # Run the script
    sudo ./quick_deploy.sh
    ```

2. Follow the on-screen prompts to enter the configuration information. Press **Enter** to accept the default values:

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

3. When prompted with “Please confirm the above information (y/n):”, review the configuration and enter `y` to proceed:

    ```bash
    ========== 用户输入 ==========
    IP 地址: 127.0.0.1
    服务端口: 26257
    HTTP 端口: 8080
    安全模式: insecure
    数据路径: /var/lib/kaiwudb
    请确认以上信息是否正确? (y/n): y
    ```

4. Wait for the deployment process to complete. Upon successful deployment, the following message is displayed:

    ```shell
    [INSTALL COMPLETED]: KaiwuDB has been installed successfully! To start KaiwuDB, please execute the command 'systemctl daemon-reload'.
    ```

5. Start KWDB:

    ```shell
    systemctl start kaiwudb
    ```

6. Connect to KWDB:

    - **Bare-metal deployment**

      ```shell
      /usr/local/kaiwudb/bin/kwbase sql --insecure --host=127.0.0.1
      ```

    - **Container deployment**

      ```shell
      docker exec -it kaiwudb-container ./kwbase sql --insecure --host=127.0.0.1
      ```

    If the following prompt appears, the connection is successful:

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

### Parameter Mode

Parameter mode is designed for users who prefer or require non-interactive, command-line-based deployment:

```shell
./quick_deploy.sh -i <ip_address> -s <service_port> -h <http_port> -m <security_mode> -p <data_path>
```

Parameters:

| Parameter | Description                  | Default          |
| --------- | ---------------------------- | ---------------- |
| `-i`      | Listen address (IP)          | 127.0.0.1        |
| `-s`      | Service port                 | 26257            |
| `-h`      | HTTP port                    | 8080             |
| `-m`      | Security mode (insecure/tls) | insecure         |
| `-p`      | Data storage path            | /var/lib/kaiwudb |

Example:

```shell
./quick_deploy.sh -i 192.168.1.100 -s 26257 -h 8080 -m tls -p /data/kaiwudb
```

## FAQ

### Which operating systems are supported by the quick deployment script?

Bare-metal deployment supports Ubuntu 20.04/22.04. For other Linux distributions, the script automatically selects container deployment.

### How can I troubleshoot deployment failures?

Check the following items:

1. Error messages displayed in the terminal
2. Log files in the installation directory (typically under `/var/log/kaiwudb/` or the `log` directory within the installation path)
3. Whether hardware, operating system, network, and port requirements are satisfied

### How can I modify the configuration after deployment?

To change the configuration after a quick deployment:

1. Uninstall the current deployment (see [Uninstall KWDB](../uninstall-kaiwudb/uninstall-db.md)).
2. Redeploy using [Bare-metal Deployment](./quickstart-bare-metal.md) or [Container Deployment](./quickstart-docker.md) for more advanced configuration options.