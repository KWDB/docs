---
title: Transport Encryption
id: transport-encryption
---

# Transport Encryption

By default, KWDB deploys clusters in secure mode, leveraging TLS encryption protocols to authenticate identities of nodes and clients, and encrypt data transmitted between nodes and clients as well as between nodes within clusters. This mechanism prevents unauthorized access to sensitive data, protects data against data tampering during transport, and guarantees data security and integrity throughout the cluster.

## Enable Secure Mode

By default, KWDB deploys clusters in secure mode. You can modify the `deploy.cfg` configuration file in the installation directory to enable or disable the secure mode.

When the secure mode is enabled, KWDB ​automatically generates TLS certificates based on the `secure_mode` parameter. These certificates serve as ​credentials for clients/applications to connect to KWDB clusters. These certificates are stored in the `/etc/kaiwudb/certs` directory. In addition, a bundled `kaiwudb_certs.tar.gz` archive is created in the installation directory for ​cluster expansion.

Here is an example of the `deploy.cfg` configuration file:

```yaml
[global]
# Enable TLS secure
secure_mode=tls
# KWDB management user 
management_user=kaiwudb
# KWDB Web service port
rest_port=8080
# KWDB service port
kaiwudb_port=26257
# KWDB data directory
data_root=/var/lib/kaiwudb
# CPU usage, range of [0,1]
# cpu=1

[local]
# Local node address
node_addr=your-host-ip
```

For more information about configuration parameters, see [Cluster Deployment](../deployment/cluster-deployment/script-deployment.md).

## Manage and Store Certificates

By default, TLS certificates generated during KWDB deployment are stored in the `/etc/kaiwudb/certs` directory. You can modify the `--certs-dir` parameter in `kaiwudb_env` or `docker-compose.yml` file to specify another directory. The `kaiwudb_env` file is generated for bare-metal deployment while the `docker-compose.yml` is generated for Docker deployment. Both files are located in `/etc/kaiwudb/script`. For detailed information, see [Cluster Setting Configurations](../db-operation/cluster-settings-config.md).

- Configuration examples for the `kaiwudb_env` file:

    ```yaml
    KAIWUDB_START_ARG="--certs-dir=<certs_dir>"
    ```

- Configuration examples for the `docker-compose.yml` file:

    ```yaml
    command: 
          - /bin/bash
          - -c
          - |
            /kaiwudb/bin/kwbase  start-single-node --certs-dir=<certs_dir> --listen-addr=0.0.0.0:26257 --advertise-addr=your-host-ip:port --store=/kaiwudb/deploy/kwdb-container
    ```
