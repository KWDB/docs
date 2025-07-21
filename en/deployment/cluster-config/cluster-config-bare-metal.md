---
title: Configure Bare-Metal Clusters
id: cluster-config-bare-metal
---

# Configure Bare-Metal Clusters

After deploying KWDB with script in a bare-metal environment, the system generates two essential configuration files:

- `kaiwudb_env`: Manages database startup flags.
- `kaiwudb.service`: Controls CPU resource allocation for KWDB.

::: warning Note

 Both startup flags and CPU configurations are node-specific. To ensure consistent performance across your cluster, apply the same configurations to all nodes.

 :::

## Configure Startup Flags

While KWDB provides reasonable default settings, you can customize its behavior by modifying the startup flags. Your custom settings will override the default values. For a list of all supported parameters, see [Cluster Parameter Configuration](../../db-operation/cluster-settings-config.md).

To modify startup flags:

1. Stop the KWDB service.

    ```shell
    systemctl stop kaiwudb
    ```

2. Navigate to the `/etc/kaiwudb/script` directory and open the configuration file.

    ```shell
    cd /etc/kaiwudb/script
    vi kaiwudb_env
    ```

3. Add or modify parameters as needed.

    Example: Add the `--cache` parameter and set it to `10000`.

    ```plain
    KAIWUDB_START_ARG="--cache=10000"
    ```

4. Reload the systemd daemon configuration.

    ```shell
    systemctl daemon-reload
    ```

5. Restart the KWDB service.

    ```shell
    systemctl restart kaiwudb
    ```

## Manage CPU Resources

You can adjust the CPU resources allocated to KWDB on each node without needing to restart the database.

To adjust CPU allocation:

1. Navigate to the `/etc/systemd/system` directory and open the configuration file.

    ```shell
    cd /etc/systemd/system
    vi kaiwudb.service
    ```

2. Locate the `CPUQuota` setting under the `[Service]` section.
    The `CPUQuota` value is calculated using the following formula: `CPUQuota = (desired usage percentage) × (number of CPU cores) × 100%`. For example, to use 30% of a 6-core system: `0.3 x 6 x 100% = 180%`.

    Example: Set the `CPUQuota` to `180%`.

    ```plain
    ...
    [Service]
    ...
    CPUQuota=180%
    ...
    ```

3. Reload the systemd daemon configuration.
  
    ```shell
    systemctl daemon-reload
    ```

4. Verify your changes.

    ```shell
    systemctl show kaiwudb | grep CPUQuota
    ```
