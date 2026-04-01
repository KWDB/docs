---
title: kwbase CLI Deployment
id: quickstart-cli
---

# kwbase CLI Deployment

## Prerequisites

- Obtained KWDB [bare-metal installation package](../prepare.md#installation-packages).
- The hardware configuration, operating system, software dependencies, and ports of the node to be deployed meet the [installation deployment requirements](../prepare.md).
- Installation user is `root` or a regular user with `sudo` privileges.

::: warning Note

The kwbase CLI deployment method described in this section **only applies to bare-metal deployment** and is not suitable for container deployment. For container deployment, please refer to [Docker Run Deployment](./deploy-docker-run.md).

:::

## Steps

1. Log in to the node to be deployed and enter the `packages` directory under the installation package directory.

2. Install dependency packages and server components.

   - DEB package systems (Debian/Ubuntu):

     ```bash
     dpkg -i ./kaiwudb-libcommon-<version>.deb ./kaiwudb-server-<version>.deb
     ```

   - RPM package systems (CentOS/RHEL):

     ```bash
     rpm -ivh ./kaiwudb-libcommon-<version>.rpm ./kaiwudb-server-<version>.rpm
     ```

3. Switch to the program directory:

   ```bash
   cd /usr/local/kaiwudb/bin
   ```

4. (Optional) If you need to use secure deployment mode, execute the following steps to create certificates:

    1. Create certificate storage directory:

        ```bash
        mkdir -p /usr/local/kaiwudb/certs
        ```

    2. Generate certificates and keys.

        ```bash
        # Create database certificate authority and key
        ./kwbase cert create-ca --certs-dir=/usr/local/kaiwudb/certs --ca-key=/usr/local/kaiwudb/certs/ca.key && \
        
        # Create client certificate and key for database installation user (replace USERNAME with actual username)
        ./kwbase cert create-client $USERNAME --certs-dir=/usr/local/kaiwudb/certs --ca-key=/usr/local/kaiwudb/certs/ca.key && \
        
        # Create node server certificate and key
        ./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=/usr/local/kaiwudb/certs --ca-key=/usr/local/kaiwudb/certs/ca.key
        ```

5. Start the database.

    - Non-secure mode:

        ```bash
        ./kwbase start-single-node --insecure \
            --listen-addr=0.0.0.0:26257 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb
        ```

    - Secure mode:

        ```bash
        ./kwbase start-single-node \
            --certs-dir=/usr/local/kaiwudb/certs \
            --listen-addr=0.0.0.0:26257 \
            --http-addr=0.0.0.0:8080 \
            --store=/var/lib/kaiwudb
        ```

6. Check database status.

    - Non-secure mode:

        ```bash
        ./kwbase node status --insecure --host=<address_of_any_alive_node>
        ```

    - Secure mode:

        ```bash
        ./kwbase node status --certs-dir=/usr/local/kaiwudb/certs --host=<address_of_any_alive_node>
        ```

7. (Optional) Create a database user and grant admin privileges. If this step is skipped, the system will default to using the user that deployed the database without requiring a password to access the database.

    - Non-secure mode (without password):

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

8. After deployment is complete, you can connect to and manage KWDB via [kwbase CLI](../access/access-cli.md), [KaiwuDB JDBC](../access/access-jdbc.md), or [KaiwuDB Developer Center](../access/access-kdc.md).
