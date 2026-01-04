---
title: 使用 kwbase CLI 工具连接 KWDB
id: access-kaiwudb-cli
---

# 使用 kwbase CLI 工具连接 KWDB

kwbase 是 KWDB 提供的在命令行下运行的数据库连接工具。用户可以通过此工具连接 KWDB 数据库并对其进行操作和维护。

如果使用脚本部署 KWDB，系统还会自动生成 `kw-sql` 便捷脚本，并在 `/usr/bin` 目录下创建软链接 `kw-sql`。该脚本封装了 kwbase 连接命令，方便 root 用户快速登录数据库。

## 使用便捷脚本快速登录

::: warning 说明
`kw-sql` 不支持指定其他用户，如需使用其他用户或三权分立模式，请使用 kwbase 命令登录。
:::

### 前提条件

已使用 `deploy.sh` 脚本部署和启动 KaiwuDB。

### 步骤

1. 在节点任一位置执行以下命令，使用 root 用户连接数据库：

    ```shell
    kw-sql
    ```

## 使用 kwbase 命令连接数据库

除了使用便捷脚本外，用户也可以直接使用 kwbase 命令连接数据库。kwbase 命令支持指定不同用户、配置各类连接参数，适用于需要灵活控制的场景。

### 前提条件

已部署 KWDB。有关详细信息，参见[单节点裸机部署](../install-kaiwudb/quickstart-bare-metal.md)或[单节点容器部署](../install-kaiwudb/quickstart-docker.md)。

::: warning 提示

如采用容器部署方式，需使用以下命令格式连接数据库：

```bash
docker exec -it <container-name> ./kwbase sql [security-options] --host=<your-host-ip> [-u <username>]
```

:::

### 非安全模式连接

::: warning 提示
非安全模式应仅在测试环境中使用。
:::

以下示例说明如何以非安全模式连接 KWDB。

- 使用部署数据库时所用的用户：

    ```shell
    ./kwbase sql --insecure --host=<your-host-ip>
    ```

- 使用自定义用户：

    ```shell
    ./kwbase sql --insecure --host=<your-host-ip> -u <username>
    ```

### 安全模式连接

以下示例说明如何以安全模式连接 KWDB。

- 使用部署数据库时所用的用户：

    ```shell
    ./kwbase sql --certs-dir=/etc/kaiwudb/certs --host=<your-host-ip>
    ```

- 使用自定义用户：

    ```shell
    ./kwbase sql --certs-dir=/etc/kaiwudb/certs --host=<your-host-ip> -u <username>
    ```