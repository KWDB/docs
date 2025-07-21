---
title: Start and Stop KWDB Service
id: local-start-stop
---

# Start and Stop KWDB Service

This section explains how to manage individual KWDB nodes within your cluster. All commands require `root` or `sudo` privileges.

## Start KWDB

1. To start a stopped node:

    ```shell
    systemctl start kaiwudb
    ```

2. To verify the service started successfully:

    ```shell
    systemctl status kaiwudb
    ```

## Stop KWDB

1. To gracefully stop a running node:

    ```shell
    systemctl stop kaiwudb
    ```

## Restart KWDB

1. To restart a running node:

    ```shell
    systemctl restart kaiwudb
    ```

    ::: warning Note

    The restart command only works on running nodes. If the service is stopped, you must use `systemctl start kaiwudb` first.

    :::

## Check Service Status

1. To check the current status of your KWDB service:

    ```shell
    systemctl status kaiwudb
    ```