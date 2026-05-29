---
title: Service Management
id: local-start-stop
---

# Service Management

This section explains how to start, stop, and restart individual KWDB nodes within your cluster. All commands require `root` or `sudo` privileges.

## Start KWDB Service

1. Start the KWDB service:

    ```shell
    systemctl start kaiwudb
    ```

2. Verify that the KWDB service has started:

    ```shell
    systemctl status kaiwudb
    ```

## Stop KWDB Service

1. To stop a running KWDB service:

    ```shell
    systemctl stop kaiwudb
    ```

## Restart KWDB Service

1. To restart a running KWDB service:

    :::warning Note
    If the KWDB service is stopped, you must start the service first before restarting it.
    :::

    ```shell
    systemctl restart kaiwudb
    ```

## Check KWDB Service Status

1. To check the current KWDB service status on this node:

    ```shell
    systemctl status kaiwudb
    ```
