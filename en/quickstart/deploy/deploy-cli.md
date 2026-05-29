---
title: kwbase CLI Deployment
id: quickstart-cli
---

# kwbase CLI Deployment

## Prerequisites

- KaiwuDB source code is compiled and installed according to the [KaiwuDB Compilation and Installation Instructions](https://gitee.com/kwdb/kwdb#%E7%BC%96%E8%AF%91%E5%92%8C%E5%AE%89%E8%A3%85).
- The hardware configuration, operating system, software dependencies, and ports of the node to be deployed meet the [installation deployment requirements](../prepare.md).
- Installation user is `root` or a regular user with `sudo` privileges.

::: warning Note

The kwbase CLI deployment method described in this section **only applies to bare-metal deployment**.

:::

## Steps

1. Navigate to the directory where the `kwbase` script is located:

   ```bash
   cd /home/go/src/gitee.com/kwbasedb/install/bin
   ```

2. (Optional) For secure mode, create certificates and keys by following these steps:

   1. Create a directory to store the certificates and keys:

        ```bash
        mkdir -p <certs_dir>
        ```

   2. Generate certificates and keys:

        ```bash
        # Create database certificate authority and key
        ./kwbase cert create-ca --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key

        # Create client certificate and key for the root user or database installation user
        ./kwbase cert create-client <username> --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key

        # Create node server certificate and key
        ./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key
        ```

3. Start the database.

    - Insecure mode:

        ```bash
        ./kwbase start-single-node --insecure \
            --listen-addr=0.0.0.0:26257 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb
        ```

    - Secure mode:

        ```bash
        ./kwbase start-single-node \
            --certs-dir=<certs_dir> \
            --listen-addr=0.0.0.0:26257 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb
        ```

4. Check database status.

    - Insecure mode:

        ```bash
        ./kwbase node status --insecure --host=<address_of_any_alive_node>
        ```

    - Secure mode:

        ```bash
        ./kwbase node status --certs-dir=<certs_dir> --host=<address_of_any_alive_node>
        ```

5. (Optional) Create a database user and grant administrator privileges to the user. If this step is skipped, the system will default to using the user from the source code compilation installation, and no password is required to access the database.

    - Insecure mode (without password):

        ```bash
        ./kwbase sql --host=127.0.0.1:<local_port> --insecure \
        -e "create user <username>; \
            grant admin to <username> with admin option;"
        ```

    - Secure mode (with password):

        ```bash
        ./kwbase sql --certs-dir=<certs_dir> --host=127.0.0.1:<local_port> \
        -e "create user <username> with password \"<user_password>\"; \
            grant admin to <username> with admin option;"
        ```

6. After deployment, connect to and manage KWDB using [kwbase CLI](../access/access-cli.md), [KaiwuDB JDBC](../access/access-jdbc.md), or [KaiwuDB Developer Center](../access/access-kdc.md).
