---
title: Using the kwbase CLI Tool
id: access-kaiwudb-cli
---

# Connect to KWDB Using the kwbase CLI Tool

This section explains how to connect to KWDB using kwbase, the built-in command-line interface (CLI) client. You can connect in either insecure mode for testing purposes or secure modes for production environments.

When you deploy KWDB using scripts, the system automatically generates a `kw-sql` helper script and creates a symbolic link in the `/usr/bin` directory. This script wraps the kwbase connection command, allowing the root user to quickly access the database.

## Quick Login Using the Helper Script

::: warning Note
The `kw-sql` script does not support other users. To connect as a different user or use Separation of Duties mode, use the kwbase command instead.
:::

**Prerequisites**

KWDB is deployed and started using the `deploy.sh` script.

**Steps**

1. Run the following command from anywhere on the node to connect as root:

    ```shell
    kw-sql
    ```

## Connect Using the kwbase Command

You can also connect directly using the kwbase command. This method lets you specify different users and configure various connection parameters for more flexibility.

::: warning Note
For containerized deployments, use this command format:

```bash
docker exec -it <container-name> ./kwbase sql [security-options] --host=<your-host-ip> [-u <user-name>]
```
:::

### Insecure Mode

::: warning Note
Insecure mode should only be used for testing purposes.
:::

- Connect as the database deployment user.

    ```shell
    ./kwbase sql --insecure --host=<your-host-ip>
    ```

- Connect as a regular user.

    ```shell
    ./kwbase sql --insecure --host=<your-host-ip> -u <username>
    ```

### Secure Mode

- Connect as the database deployment user.

    ```shell
    ./kwbase sql --certs-dir=/etc/kaiwudb/certs --host=<your-host-ip> 
    ```

- Connect as a regular user.

    ```shell
    ./kwbase sql --certs-dir=/etc/kaiwudb/certs --host=<your-host-ip> -u <username>
    ```