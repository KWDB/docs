---
title: Deploy Using kwbase CLI
id: kwbase-cli-deployment
---

# Deploy Using kwbase CLI

This section describes how to deploy a KWDB cluster on a single machine using the `kwbase` CLI.

**Note:** In production environments, deploy only one node per machine to enhance availability and reduce the risk of data loss.

## Prerequisites

- The hardware, operating system, software dependencies, and ports of the nodes to be deployed meet the [deployment requirements](../prepare/before-deploy-bare-metal.md#hardware).
- One of the following user permissions:
  - Root user access
  - Regular user with `sudo` privileges:
    - Users with passwordless `sudo` won't need to enter passwords during installation.
    - Users without passwordless `sudo` will be prompted for passwords when needed.
- The source code is compiled following [KWDB Compilation and Installation Instructions](https://gitee.com/kwdb/kwdb/blob/master/README.en.md#compilation-and-installation).

## Steps

1. Navigate to the program directory:

   ```bash
   cd /home/go/src/gitee.com/kwbasedb/install/bin
   ```

2. (Optional) For secure deployment, create certificates by following these steps:

   1. Create a directory to store the certificates:

      ```bash
      mkdir -p <certs_dir>
      ```

   2. Generate certificates and keys:

        ```bash
        # Create database certificate authority and key
        ./kwbase cert create-ca --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key && \

        # Create client certificate and key for database installation user (replace username with actual username)
        ./kwbase cert create-client <username> --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key && \

        # Create node certificate and key
        ./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key
        ```

      ::: warning Note

      When deploying in cross-machine mode, use the `./kwbase cert create-node <node_ip>` command to create certificates and keys for all nodes, then transfer all certificates and keys to every node in the cluster.

      :::

3. Start the cluster by starting all the nodes in the cluster:

   - **For single-replica clusters:**

        - Insecure mode:

            ```bash
            ./kwbase start-single-replica --insecure \
                --listen-addr=0.0.0.0:26257 \
                --advertise-addr=<host1>:26257 \
                --brpc-addr=:27257 \
                --http-addr=0.0.0.0:8080 \
                --store=/var/lib/kaiwudb \
                --join=<host1>:26257

            ./kwbase start-single-replica --insecure \
                --listen-addr=0.0.0.0:26257 \
                --advertise-addr=<host2>:26258 \
                --brpc-addr=:27258 \
                --http-addr=0.0.0.0:8080 \
                --store=/var/lib/kaiwudb \
                --join=<host1>:26257

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
            ./kwbase start-single-replica \
                --certs-dir=<certs_dir> \
                --listen-addr=0.0.0.0:26257 \
                --advertise-addr=<host1>:26257 \
                --brpc-addr=:27257 \
                --http-addr=0.0.0.0:8080 \
                --store=/var/lib/kaiwudb \
                --join=<host1>:26257

            ./kwbase start-single-replica \
                --certs-dir=<certs_dir> \
                --listen-addr=0.0.0.0:26257 \
                --advertise-addr=<host2>:26258 \
                --brpc-addr=:27258 \
                --http-addr=0.0.0.0:8080 \
                --store=/var/lib/kaiwudb \
                --join=<host1>:26257

            ./kwbase start-single-replica \
                --certs-dir=<certs_dir> \
                --listen-addr=0.0.0.0:26257 \
                --advertise-addr=<host3>:26259 \
                --brpc-addr=:27259 \
                --http-addr=0.0.0.0:8080 \
                --store=/var/lib/kaiwudb \
                --join=<host1>:26257
            ```

   - **For multi-replica clusters:**

        - Insecure mode:

            ```bash
            ./kwbase start --insecure \
                --listen-addr=0.0.0.0:26257 \
                --advertise-addr=<host1>:26257 \
                --brpc-addr=:27257 \
                --http-addr=0.0.0.0:8080 \
                --store=/var/lib/kaiwudb \
                --join=<host1>:26257

            ./kwbase start --insecure \
                --listen-addr=0.0.0.0:26257 \
                --advertise-addr=<host2>:26258 \
                --brpc-addr=:27258 \
                --http-addr=0.0.0.0:8080 \
                --store=/var/lib/kaiwudb \
                --join=<host1>:26257

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
            ./kwbase start --certs-dir=<certs_dir> \
                --listen-addr=0.0.0.0:26257 \
                --advertise-addr=<host1>:26257 \
                --brpc-addr=:27257 \
                --http-addr=0.0.0.0:8080 \
                --store=/var/lib/kaiwudb \
                --join=<host1>:26257

            ./kwbase start --certs-dir=<certs_dir> \
                --listen-addr=0.0.0.0:26257 \
                --advertise-addr=<host2>:26258 \
                --brpc-addr=:27258 \
                --http-addr=0.0.0.0:8080 \
                --store=/var/lib/kaiwudb \
                --join=<host1>:26257

            ./kwbase start --certs-dir=<certs_dir> \
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

5. View database status.

    - Insecure mode:

        ```bash
        ./kwbase node status --insecure --host=<address_of_any_alive_node>
        ```

    - Secure mode:

        ```bash
        ./kwbase node status --certs-dir=<certs_dir> --host=<address_of_any_alive_node>
        ```