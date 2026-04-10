---
title: YAML File Deployment
id: quickstart-yaml
---

# YAML File Deployment

## Prerequisites

- Obtained KWDB [docker image](../prepare.md#installation-packages-container-images-and-compilation-versions).
- The hardware, operating system, software dependencies, and ports of the node to be deployed meet the [installation deployment requirements](../prepare.md).
- The user performing the installation is the `root` user or a regular user with `sudo` privileges:
  - `root` users or users with passwordless `sudo` configured will not be prompted for a password during script execution.
  - Users without passwordless `sudo` will be prompted to enter a password to escalate privileges.
- If the user is not a `root` user, add the user to the `docker` group by running `sudo usermod -aG docker $USER`.

## Steps

1. Create the `docker-compose.yml` configuration file.

    ::: warning Note
    The `image` parameter must match the image name obtained after importing the `KaiwuDB.tar` file or the pulled image name.
    :::

    Example:

    ```yaml
    version: '3.3'
    services:
      kwdb-container:
        image: "kwdb/kwdb:3.0.0"
        container_name: kaiwudb-experience
        hostname: kaiwudb-experience
        ports:
          - 8080:8080
          - 26257:26257
        ulimits:
          memlock: -1
        networks: 
          - default
        restart: on-failure
        ipc: shareable
        privileged: true
        environment:
          - LD_LIBRARY_PATH=/kaiwudb/lib
        tty: true
        working_dir: /kaiwudb/bin
        command: 
          - /bin/bash
          - -c
          - |
            /kaiwudb/bin/kwbase start-single-node --insecure --listen-addr=0.0.0.0:26257 --advertise-addr=127.0.0.1:26257 --http-addr=0.0.0.0:8080 --store=/kaiwudb/deploy/kaiwudb
    ```

2. Sart KWDB.

    ```bash
    docker-compose up -d
    ```
3. After deployment is complete, you can connect to and manage KWDB via [kwbase CLI](../access/access-cli.md), [KaiwuDB JDBC](../access/access-jdbc.md), or [KaiwuDB Developer Center](../access/access-kdc.md).
