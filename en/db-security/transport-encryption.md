---
title: Transport Encryption
id: transport-encryption
---

# Transport Encryption

By default, KWDB deploys clusters in secure mode and uses TLS encryption to verify node and client identities, as well as to encrypt data transmitted between nodes and clients. This protects sensitive data from unauthorized access and tampering during transport and helps ensure data security and integrity throughout the cluster.

## Enable Secure Mode

By default, KWDB deploys clusters in secure mode. During deployment, you can choose whether to enable or disable secure mode.

When secure mode is enabled, KWDB generates TLS certificates for clients and applications to connect to the database. These certificates are stored in `/etc/kaiwudb/certs`. KWDB also generates `kaiwudb_certs.tar.gz` in the installation directory to simplify future cluster expansion.

For more configuration details, see [Cluster Deployment](../deployment/overview.md).

## Manage and Store Certificates

By default, the generated certificates are stored in `/etc/kaiwudb/certs`. To change the certificate directory, modify the `--certs-dir` parameter in the generated `kaiwudb_env` or `docker-compose.yml` file under `/etc/kaiwudb/script`. For more information, see [Cluster Parameter Configuration](../db-operation/cluster-settings-config.md).

- Example configuration for the bare-metal `kaiwudb_env` file:

    ```yaml
    KAIWUDB_START_ARG="--certs-dir=<certs_dir>"
    ```

- Example configuration for the container `docker-compose.yml` file:

    ```yaml
    command:
      - /bin/bash
      - -c
      - |
        /kaiwudb/bin/kwbase start-single-node --certs-dir=<certs_dir> --listen-addr=0.0.0.0:26257 --advertise-addr=your-host-ip:port --store=/kaiwudb/deploy/kwdb-container
    ```
