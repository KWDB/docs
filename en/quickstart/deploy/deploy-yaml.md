---
title: YAML File Deployment
id: quickstart-yaml
---

# YAML File Deployment

## Prerequisites

- Obtained KWDB [container installation package](../prepare.md#installation-packages).
- The hardware, operating system, software dependencies, and ports of the node to be deployed meet the [installation deployment requirements](../prepare.md).
- Installation user is root or a regular user with `sudo` privileges.
  - Root users and regular users configured with `sudo` passwordless access do not need to enter a password when executing deployment scripts.
  - Regular users without `sudo` passwordless configuration need to enter a password for privilege escalation when executing deployment scripts.
- For non-root installation users, the user needs to be added to the `docker` group using `sudo usermod -aG docker $USER`.

## Steps

1. Import the `KaiwuDB.tar` file in the `kwdb_install/packages` directory to get the image name.

    ```shell
    docker load < KaiwuDB.tar
    Loaded image: "$kwdb_image"
    ```

2. Create a `docker-compose.yml` configuration file.

    ::: warning Note
    The value of the `image` parameter must be the image name obtained after importing the `KaiwuDB.tar` file.
    :::

    Configuration file example:

    ```yaml
    version: '3.3'
    services:
      kwdb-container:
        image: "$kwdb_image"
        container_name: kwdb-experience
        hostname: kwdb-experience
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

3. Quickly start KWDB.

    ```shell
    docker-compose up -d
    ```
4. After deployment is complete, you can connect to and manage KWDB via [kwbase CLI](../access/access-cli.md), [KaiwuDB JDBC](../access/access-jdbc.md), or [KaiwuDB Developer Center](../access/access-kdc.md).
