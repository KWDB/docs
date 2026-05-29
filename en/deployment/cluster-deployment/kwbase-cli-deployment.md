---
title: Deploy Using kwbase CLI
id: kwbase-cli-deployment
---

# Deploy Using kwbase CLI

This section describes how to deploy a KWDB cluster on a single machine using the kwbase CLI, including the complete process of starting multiple nodes and initializing the cluster. Note: In production environments, deploy only one node per machine to enhance availability and reduce the risk of data loss.

## Prerequisites

- The hardware, operating system, software dependencies, and ports of the nodes to be deployed meet the [deployment requirements](../cluster-prepare.md#hardware).
- The installation user must be `root` or a regular user with `sudo` privileges.
- The source code is compiled following [KWDB Compilation and Installation Instructions](https://gitee.com/kwdb/kwdb#%E7%BC%96%E8%AF%91%E5%92%8C%E5%AE%89%E8%A3%85).

## Steps

1. Navigate to the directory where the `kwbase` binary is located:

   ```bash
   cd /home/go/src/gitee.com/kwbasedb/install/bin
   ```

2. (Optional) If you need to deploy in secure mode, follow these steps to create the certificates:

    1. Create a directory to store the certificates:

        ```bash
        mkdir -p <certs_dir>
        ```

    2. Generate certificates and keys:

        ```bash
        # Create database certificate authority and key
        ./kwbase cert create-ca --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key

        # Create client certificate and key for the database installation user
        ./kwbase cert create-client <username> --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key

        # Create node server certificate and key
        ./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key
        ```

        ::: warning Note

        When deploying in cross-machine mode, use the `./kwbase cert create-node <node_ip>` command to create certificates and keys for all nodes, and transfer all certificates and keys to every node in the cluster.

        :::

3. Start the cluster nodes.

    - Single-replica cluster:

        - Insecure mode:

            ```bash
            # Start the first node
            ./kwbase start-single-replica --insecure \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host1>:26257 \
            --brpc-addr=:27257 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257

            # Start the second node
            ./kwbase start-single-replica --insecure \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host2>:26258 \
            --brpc-addr=:27258 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257

            # Start the third node
            ./kwbase start-single-replica --insecure \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host3>:26259 \
            --brpc-addr=:27259 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257
            ```

        - Secure mode:

            ```bash
            # Start the first node
            ./kwbase start-single-replica \
            --certs-dir=<certs_dir> \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host1>:26257 \
            --brpc-addr=:27257 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257

            # Start the second node
            ./kwbase start-single-replica \
            --certs-dir=<certs_dir> \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host2>:26258 \
            --brpc-addr=:27258 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257

            # Start the third node
            ./kwbase start-single-replica \
            --certs-dir=<certs_dir> \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host3>:26259 \
            --brpc-addr=:27259 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257
            ```

    - Multi-replica cluster:

        - Insecure mode:

            ```bash
            # Start the first node
            ./kwbase start --insecure \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host1>:26257 \
            --brpc-addr=:27257 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257

            # Start the second node
            ./kwbase start --insecure \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host2>:26258 \
            --brpc-addr=:27258 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257

            # Start the third node
            ./kwbase start --insecure \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host3>:26259 \
            --brpc-addr=:27259 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257
            ```

        - Secure mode:

            ```bash
            # Start the first node
            ./kwbase start \
            --certs-dir=<certs_dir> \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host1>:26257 \
            --brpc-addr=:27257 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257

            # Start the second node
            ./kwbase start \
            --certs-dir=<certs_dir> \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host2>:26258 \
            --brpc-addr=:27258 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257

            # Start the third node
            ./kwbase start \
            --certs-dir=<certs_dir> \
            --listen-addr=0.0.0.0:26257 \
            --advertise-addr=<host3>:26259 \
            --brpc-addr=:27259 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb \
            --join=<host1>:26257
            ```

4. Initialize the cluster.

    - Insecure mode:

        ```bash
        ./kwbase init --insecure --host=<address_of_any_node>
        ```

    - Secure mode:

        ```bash
        ./kwbase init --certs-dir=<certs_dir> --host=<address_of_any_node>
        ```

5. View cluster status.

    - Insecure mode:

        ```bash
        ./kwbase node status --insecure --host=<address_of_any_alive_node>
        ```

    - Secure mode:

        ```bash
        ./kwbase node status --certs-dir=<certs_dir> --host=<address_of_any_alive_node>
        ```

6. (Optional) Create a database user and grant admin privileges. If this step is skipped, the system will default to using the user that deployed the database without requiring a password to access the database.

    - Insecure mode (without password):

        ```bash
        ./kwbase sql --host=127.0.0.1:$local_port --insecure \
        -e "create user $username; \
            grant admin to $username with admin option;"
        ```

    - Secure mode (with password):

        ```bash
        ./kwbase sql --certs-dir=/usr/local/kaiwudb/certs --host=127.0.0.1:$local_port \
        -e "create user $username with password \"$user_password\"; \
            grant admin to $username with admin option;"
        ```

7. After deployment is complete, you can connect to and manage KWDB via [kwbase CLI](../../quickstart/access/access-cli.md), [KWDB Supported Connectors](../../development/overview.md), or [KaiwuDB Developer Center](../../kaiwudb-tools/kaiwudb-developer-center/overview.md).
