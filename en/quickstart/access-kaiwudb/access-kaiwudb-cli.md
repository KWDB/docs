---
title: Using the kwbase CLI Tool
id: access-kaiwudb-cli
---

# Connect to KWDB Using the kwbase CLI Tool

This section explains how to connect to KWDB using kwbase, the built-in command-line interface (CLI) client. You can connect in either non-secure mode for testing purposes or secure mode for production environments.

## Prerequisites

- KWDB is deployed and running.
  - For bare-metal deployment, see [Single-Node Bare-Metal Deployment](../install-kaiwudb/quickstart-bare-metal.md).
  - For container-based deployment, see [Single-Node Container Deployment](../install-kaiwudb/quickstart-docker.md).

::: warning Note
For containerized deployments, connect to the database using the following command format:

```bash
docker exec -it <container-name> ./kwbase sql [security-opions] --host=<your-host-ip> [-u <username>]
```

:::

## Insecure Mode

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

## Secure Mode

- Connect as the database deployment user.

    ```shell
    ./kwbase sql --certs-dir=certs --host=<your-host-ip> 
    ```

- Connect as a regular user.

    ```shell
    ./kwbase sql --certs-dir=certs --host=<your-host-ip> -u <username>
    ```