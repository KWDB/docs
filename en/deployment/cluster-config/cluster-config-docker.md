---
title: Configure Container Deployment
id: cluster-config-docker
---

# Configure Container Deployment

After deploying KWDB with script in a container environment, the system generates the `docker-compose.yml` configuration file which can be used to control the startup flags and CPU resource allocation for KWDB.

:::warning Note

 Both startup flags and CPU configurations are node-specific. To ensure consistent performance across your cluster, apply the same configurations to all nodes.

:::

## Configure Startup Flags

While KWDB provides reasonable default settings, you can customize its behavior by modifying the startup flags. Your custom settings will override the default values. For a list of all supported parameters, see [Cluster Parameters](../../db-operation/cluster-settings-config.md#cluster-parameters).

To modify startup flags:

1. Navigate to the `/etc/kaiwudb/script` directory and stop the KWDB container.

    ```shell
    docker-compose down
    ```

2. Open `docker-compose.yml`, locate the `command` section, and add or modify parameters as needed.

    ::: warning
    Keep all existing startup flags in place. Removing them may prevent the database from starting.
    :::

    Example: Add the `--cache` parameter and set it to `25%`.

    ```yaml
    ...
        command: 
          - /bin/bash
          - -c
          - |
            /kaiwudb/bin/kwbase start-single-node --certs-dir=<certs_dir> --listen-addr=0.0.0.0:26257 --advertise-addr=your-host-ip:port --store=/kaiwudb/deploy/kwdb-container --cache=25%
    ```

3. Start KWDB with the new configuration.

    ```shell
    systemctl start kaiwudb
    ```

## Manage CPU Resources

You can adjust the CPU resources allocated to KWDB on each node by either using the `docker update` command or modifying the configuration file.

The CPU setting (`CPUs`) represents how many CPU cores KWDB can use and is calculated using the following formula: `CPUs = (desired usage percentage) × (number of CPU cores)`. For example, to use 30% of a 6-core system: `0.3 x 6 = 1.8`.

To adjust CPU allocation:

- Using the `docker update` command:

    ```shell
    docker update --cpus <value> kwdb-container
    ```

- Using the `docker-compose.yml` file:

    1. Navigate to the `/etc/kaiwudb/script` directory and stop the KWDB container.

        ```shell
        docker-compose down
        ```

    2. Edit `docker-compose.yml` to update the CPU resource limits.

        Example: Limit the CPU resources to `1.8` for KWDB

        ```yaml
        version: '3.3'
        services:
        ...
          deploy:
            resources: -1 
              limits:
                cpus:'1.8'     
        ...
        ```

    3. Recreate and start the KWDB container.

        ```shell
        systemctl start kaiwudb
        ```
