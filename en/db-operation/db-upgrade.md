---
title: Database Upgrade
id: db-upgrade
---

# Database Upgrade

## Overview

This section describes how to upgrade KWDB. Prepare the upgrade according to your actual deployment topology, and then follow the corresponding upgrade steps based on the deployment method you used during installation.

### Upgrade Paths

| Deployment Topology | Current Version | Target Version | Upgrade Method |
|--------------------|----------------|----------------|----------------|
| Standalone deployment | 3.0.0, 3.1.0 | 3.2.0 | Script or CLI deployment: installer<br>Container image deployment: container image upgrade |
|                      | 1.x, 2.x | 3.2.0 | Import/export |
| Multi-replica cluster | 3.0.0, 3.1.0 | 3.2.0 | Script or CLI deployment: installer<br>Container image deployment: container image upgrade |
|                      | 1.x, 2.x | 3.2.0 | Import/export |
| Single-replica cluster | 3.0.0, 3.1.0 | 3.2.0 | Script or CLI deployment: installer<br>Container image deployment: container image upgrade |
|                       | 1.x, 2.x | 3.2.0 | Import/export |

:::warning Note
- When upgrading from 3.0.0 to 3.2.0, if you want to use the time-series raft log storage engine added in 3.1.0 and later, deploy a new cluster first and then import historical data.
- In 3.2.0, the default value of `ts.raft_log.sync_period` changed from `10s` to `0s` (flush to disk immediately). Before upgrading a multi-replica cluster from 3.0.0 or 3.1.0 to 3.2.0, switch this parameter to `0s` on the old version nodes and wait for it to take effect. Otherwise, the upgrade may fail. For details, see the preparation steps in [Cluster Deployment](#cluster-deployment).
:::

**Notes**

- After upgrade, you cannot simply downgrade to the previous version. If you need to downgrade, uninstall the current version first, reinstall the old version of KWDB, and then restore data from the backup created before uninstallation. For uninstall instructions, see [Uninstall KWDB](../deployment/uninstall-cluster.md).
- KWDB supports upgrading from any prior version to the latest version using import/export. See [Data Export](../db-administration/import-export-data/export-data.md) and [Data Import](../db-administration/import-export-data/import-data.md). **Note**: When upgrading from 2.x, the exported `meta.sql` file contains `PARTITION INTERVAL` syntax for time-series tables. Since 3.1.0 and later versions have deprecated this syntax (although time-series databases still support it), remove the related syntax from the file before importing; otherwise the import will fail. After upgrading via import/export, high availability in multi-replica clusters may be affected.

## Upgrade Preparation

### Standalone Deployment

1. Confirm that the new version is higher than the installed version.
2. Stop the KWDB service:

   ```bash
   systemctl stop kaiwudb
   ```

3. Back up the user data directory.

### Cluster Deployment

1. Confirm that the new version is higher than the installed version.
2. If the cluster is multi-replica, complete the following before upgrade:
   1. Switch `ts.raft_log.sync_period` to `0s`:

      ```sql
      SET CLUSTER SETTING ts.raft_log.sync_period = '0s';
      ```

   2. Wait for at least 5 minutes for the cluster to finish the parameter change.
   3. Query the shard status and confirm that the cluster is healthy. If not, repeat the above steps.

      ```sql
      SELECT * FROM kwdb_internal.ranges;
      ```

3. Check cluster status:
   - View cluster status:

     ```bash
     kw-status
     ```

   - View replica status:

     ```sql
     SELECT sum((metrics->>'ranges.unavailable')::DECIMAL)::INT AS ranges_unavailable,
            sum((metrics->>'ranges.underreplicated')::DECIMAL)::INT AS ranges_underreplicated
     FROM kwdb_internal.kv_store_status;
     ```

4. Use `SHOW JOBS` to check whether any schema changes or bulk import jobs are running.
5. Check whether leaseholders and replicas are evenly distributed across the cluster using:

   ```sql
   SELECT * FROM kwdb_internal.ranges;
   ```

6. Back up the cluster. If the upgrade fails, restore the cluster from the backup.

## Performing the Upgrade

### Upgrade Using the Installer

During installer-based upgrades, if the node is not installed with KWDB, KWDB is still running, the version is wrong, or the deployment mode is incorrect, the upgrade is aborted and an error message is shown.

#### Prerequisites

- The new version of the installer (`.run`) has been obtained.
- The target node already has KWDB installed.
- The user data directory of the target node has been backed up.
- The execution node (any node in the cluster) can SSH into the target node and has write permission in the target node's installation directory.
- The user is `root` or a normal user with passwordless `sudo` configured.
- For container deployment, if the user is not `root`, use `sudo usermod -aG docker $USER` to add the user to the `docker` group.

#### CLI Mode

1. Copy the new installer to the cluster node that performs the upgrade and grant it execute permission:

   ```bash
   chmod +x KaiwuDB-*.run
   ```

2. On the target node, stop KWDB:

   ```bash
   sudo systemctl stop kaiwudb
   ```

3. On the execution node, start the installer in CLI mode:

   ```bash
   ./KaiwuDB-*.run -c
   # or
   ./KaiwuDB-*.run --cli
   ```

4. In the main menu, enter `4` to select **Upgrade Nodes**.

5. Set the number of nodes to upgrade to `1`.

6. The installer generates an upgrade configuration file and opens an editor. Change `host` to the IP address of the target node, verify the rest of the settings, and save to start the upgrade automatically.

   ```ini
   [node1]
   host=192.168.122.224
   port=22
   user=admin
   passwd=*******
   ```

7. On the target node, modify the relevant configuration files according to the deployment mode.

8. Reload system service settings and start KWDB:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start kaiwudb
   ```

9. Verify the node status:

   ```bash
   kw-status
   ```

10. Repeat steps 2 to 9 for the remaining nodes in the cluster.

11. After all nodes are upgraded, verify that the data is intact. For multi-replica clusters, also query the shard status to confirm normal cluster operation.

   ```sql
   SELECT * FROM kwdb_internal.ranges;
   ```

#### Terminal Graphical Interaction Mode

1. Copy the new installer to the cluster node that performs the upgrade and grant it execute permission.
2. On the target node, stop KWDB.
3. On the execution node, start the installer in terminal graphical interaction mode.
4. In the main menu, select **Upgrade Nodes** and press Enter.
5. In the upgrade settings menu, click **Set Upgrade Nodes**, enter the target node IP, port, username, and password, then click **Save**. Select **Start Upgrade** and press Enter.
6. On the target node, modify the relevant configuration files according to the deployment mode.
7. Reload system service settings and start KWDB.
8. Verify the node status.

## Upgrade from Source Code Compilation

For KWDB instances installed by compiling from source code, you can upgrade by compiling the new version. This method is suitable for users with specific customization requirements and compilation/deployment experience.

### Prerequisites

- Backup of data and configuration files
- Downloaded new version [source code](https://gitee.com/kwdb/kwdb)
- [Compilation environment and dependencies](https://gitee.com/kwdb/kwdb#%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F%E5%92%8C%E8%BD%AF%E4%BB%B6%E4%BE%9D%E8%B5%96) meet KWDB requirements

### Steps

1. Compile the new version following the [KWDB compilation documentation](https://gitee.com/kwdb/kwdb#%E7%BC%96%E8%AF%91%E5%92%8C%E5%AE%89%E8%A3%85).
2. Start the service using the same [startup command](../kaiwudb-tools/kwbase-cli-tool.md#kwbase-start) as the previous version.
3. Verify that the service is running as expected.

## Upgrade for Container Image Deployment

For KWDB instances deployed using Docker container images, you can upgrade by updating the container image. This includes both Docker Compose upgrade and Docker Run upgrade.

### Docker Compose Upgrade

#### Prerequisites

- Back up data and configuration files.
- Obtain the new container image.

#### Steps

1. Load the new container image:

   ```bash
   docker load < KaiwuDB.tar
   ```

2. Stop and remove the existing container:

   ```bash
   docker-compose down
   ```

3. Delete the old image:

   ```bash
   docker rmi ${image_name}
   ```

4. Update `docker-compose.yml` and change the image version.

5. Start the new KWDB version:

   ```bash
   docker-compose up -d
   ```

### Docker Run Upgrade

#### Prerequisites

- Back up data and configuration files.
- Obtain the new container image.

#### Steps

1. Stop the KWDB container. The container name is the one specified with the `--name` parameter when the container was started.

   ```bash
   docker stop <kwdb-container>
   ```

2. Remove the container:

   ```bash
   docker rm <kwdb-container>
   ```

3. Obtain the new image.

   - Pull from the image repository:

     ```bash
     docker pull kwdb/kwdb:<new-version>
     ```

   - Import from a local file:

     ```bash
     docker load < KaiwuDB.tar
     ```

4. Start the new container. Except for the image name, all parameters should remain the same as the original container.

   - In insecure mode:

     ```bash
     docker run -d --privileged --name kwdb \
         --ulimit memlock=-1 \
         --ulimit nofile=$max_files \
         -p $db_port:26257 \
         -p $http_port:8080 \
         -v /var/lib/kaiwudb:/kaiwudb/deploy/kwdb-container \
         --ipc shareable \
         -w /kaiwudb/bin \
         <kwdb_image> \
         ./kwbase start-single-node \
         --insecure \
         --listen-addr=0.0.0.0:26257 \
         --http-addr=0.0.0.0:8080 \
         --store=/kaiwudb/deploy/kwdb-container
     ```

   - In secure mode:

     ```bash
     docker run -d --privileged --name kwdb \
         --ulimit memlock=-1 \
         --ulimit nofile=$max_files \
         -p $db_port:26257 \
         -p $http_port:8080 \
         -v /etc/kaiwudb/certs:<certs_dir> \
         -v /var/lib/kaiwudb:/kaiwudb/deploy/kwdb-container \
         --ipc shareable \
         -w /kaiwudb/bin <kwdb_image> \
         ./kwbase start-single-node \
         --certs-dir=<certs_dir> \
         --listen-addr=0.0.0.0:26257 \
         --http-addr=0.0.0.0:8080 \
         --store=/kaiwudb/deploy/kwdb-container
     ```
