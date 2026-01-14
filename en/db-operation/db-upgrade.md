---
title: Database Upgrade
id: db-upgrade
---

# Database Upgrade

This section covers upgrade procedures for KWDB database across different deployment scenarios, including upgrades using deployment scripts and container images.

Before upgrading, carefully review all precautions and select the appropriate upgrade method based on your deployment approach.

## Upgrade Using Deployment Scripts

## Upgrading with Deployment Scripts

Script-based upgrades are the most common method for KWDB instances installed through deployment scripts. Upgrade procedures vary based on your deployment topology: standalone instances, multi-replica clusters, and single-replica clusters each require different approaches. The available upgrade methods depend on your specific deployment type:

- **Standalone Instances**：[3.0.0 to 3.1.0 offline upgrade](#upgrading-standalone-instances).
- **Multi-Replica Clusters**：[3.0.0 to 3.1.0 node-by-node online upgrade](#upgrading-multi-replica-clusters). **Note**: To use the new time-series raft log storage engine, deploy a fresh 3.1.0 cluster and import historical data.
- **Single-Replica Clusters**：[3.0.0 to 3.1.0 offline upgrade](#upgrading-single-replica-clusters).

::: warning Note

- Direct downgrades to the previous version are not supported after an upgrade. To perform a downgrade, you must first uninstall the current version, then install the original version of KWDB. Afterward, restore the data from the backup created before uninstallation. For instructions, see [Uninstall Standalone Databases](../quickstart/uninstall-kaiwudb/uninstall-db.md) or [Uninstall Clusters](../deployment/uninstall-cluster.md).
- KWDB supports upgrading from any previous version to the latest version through import-export method. For specific operations, see [Data Export](../db-administration/import-export-data/export-data.md) and [Data Import](../db-administration/import-export-data/import-data.md). Note: After upgrading using the import-export method, high availability of multi-replica clusters may be affected.
:::

### Upgrading Standalone Instances

If any upgrade errors occur—such as KWDB not being installed, KWDB still running, incorrect version, or incorrect deployment method—the system aborts the upgrade and displays the relevant error messages.

If the upgrade fails during new version installation, the system retains the data directory, certificates, and configuration files while removing the new version files from the node. You can then choose to manually install either the new or the old version.

#### Prerequisites

- KWDB is installed on the target node.
- The data directory is backed up.
- You have obtained the new version package.
- You have one of the following user permissions:
  - Root user access
  - Regular user with `sudo` privileges (users with passwordless `sudo` won't need to enter passwords during upgrade; others will be prompted when needed)
  - For container deployment: Regular user in the `docker` group (add with `sudo usermod -aG docker $USER`)

#### Steps

1. Copy the new version package to the target node and extract the contents.

2. Check if KWDB is stopped. If the service is still running, stop it using `systemctl stop kaiwudb`.

   ```shell
   systemctl status kaiwudb
   ```

3. Navigate to the directory of the new version package.

4. Run the local upgrade command:

   ```shell
   ./deploy.sh upgrade -l
   ```

   or

   ```shell
   ./deploy.sh upgrade --local
   ```

   If the upgrade succeeds, the console displays:

   ```shell
   UPGRADE COMPLETED: KaiwuDB has been upgraded successfully! 
   ```

5. Start KWDB:

   ```shell
   systemctl start kaiwudb
   ```

6. Verify that the service is running:

   ```shell
   systemctl status kaiwudb
   ```

### Upgrading Multi-Replica Clusters

During the upgrade process, compression and lifecycle operations on the upgraded nodes may fail temporarily but resume once the upgrade completes. If upgrade errors occur—such as KWDB not being installed, unhealthy or unavailable nodes, incorrect version, or incorrect deployment method—the system aborts the upgrade and displays the relevant error messages.

#### Preparing for Upgrade

**Steps**

1. Ensure that the client communicates with multiple nodes to avoid communication interruption when upgrading a single node.

2. Check the cluster status:

   1. Check node status:

      - Deployment script:

         ```shell
         kw-status
         ```

      - kwbase command:

         ```shell
         <kwbase_path>/kwbase node status [--host=<ip:port>] [--insecure | --certs-dir=<path>]
         ```

   2. Check replica status:

         ```sql
      SELECT sum((metrics->>'ranges.unavailable')::DECIMAL)::INT AS ranges_unavailable,
         sum((metrics->>'ranges.underreplicated')::DECIMAL)::INT As ranges_underreplicated
      FROM kwdb_internal.kv_store_status;
         ```

3. Check for ongoing schema changes or bulk import jobs using the `SHOW JOBS` SQL command.

4. Use the `SELECT * FROM kwdb_internal.ranges` SQL command to check if leaseholders and replicas are evenly distributed across the nodes in the cluster.

5. Back up the cluster. If the upgrade fails, you can restore the cluster from the backup.

#### Executing Upgrade

Perform the upgrade on each node in the cluster, one at a time. After each node rejoins the cluster and its version and status are verified, proceed to upgrade the next node.

**Prerequisites**

- KWDB is installed on the target node.
- The node is available (both `is_available` and `is_live` are `true`).
- The user data directory is backed up.
- You have obtained the new version package.
- You have one of the following user permissions:
  - Root user access
  - Regular user with `sudo` privileges (users with passwordless `sudo` won't need to enter passwords during upgrade; others will be prompted when needed)
  - For container deployment: Regular user in the `docker` group (add with `sudo usermod -aG docker $USER`)

**Steps**

1. Copy the new version installation package to the target node and extract the contents.

2. Check if KWDB is stopped. If the service is still running, stop it using `systemctl stop kaiwudb`.

   ```shell
   systemctl status kaiwudb
   ```

3. Navigate to the directory of the new version installation package.

4. Run the local upgrade command:

   ```shell
   ./deploy.sh upgrade -l
   ```

   or

   ```shell
   ./deploy.sh upgrade --local
   ```

   If the upgrade succeeds, the console displays:

   ```shell
   UPGRADE COMPLETED: KaiwuDB has been upgraded successfully!
   ```

5. Start KWDB:

   ```shell
   systemctl start kaiwudb
   ```

6. Verify that the service is running:

   ```shell
   systemctl status kaiwudb
   ```

### Upgrading Single-Replica Clusters

If upgrade errors occur—such as KWDB not being installed, KWDB still running, incorrect version, or incorrect deployment method—the system aborts the upgrade and displays the relevant error messages.

If the upgrade fails during new version installation, the system retains the data directory, certificates, and configuration files while removing the new version installation files from the node. You can then choose to manually install either the new or the old version.

#### Prerequisites

- KWDB is installed on all target nodes.
- The data directory is backed up on all nodes.
- You have obtained the new version package.
- You have one of the following user permissions:
  - Root user access
  - Regular user with `sudo` privileges (users with passwordless `sudo` won't need to enter passwords during upgrade; others will be prompted when needed)
  - For container deployment: Regular user in the `docker` group (add with `sudo usermod -aG docker $USER`)

#### Steps

1. Stop KWDB on all nodes in the cluster:

   ```shell
   systemctl stop kaiwudb
   ```

2. Perform the following upgrade operations on each node:
   1. Copy the new version package to the node and extract the contents.
   2. Navigate to the directory of the new version package.
   3. Run the local upgrade command:

      ```shell
      ./deploy.sh upgrade -l
      ```

      or

      ```shell
      ./deploy.sh upgrade --local
      ```

      If the upgrade succeeds, the console displays:

      ```shell
      UPGRADE COMPLETED: KaiwuDB has been upgraded successfully! 
      ```

3. After all nodes are upgraded, execute the following commands on each node to start the database:
   1. Start KWDB:

      ```shell
      systemctl start kaiwudb
      ```

   2. Verify that the service is running:

      ```shell
      systemctl status kaiwudb
      ```

## Upgrade for Source Code Compilation

For KWDB instances installed by compiling from source code, you can upgrade by compiling the new version. This upgrade method is suitable for users with specific customization requirements who have compilation and deployment experience.

### Prerequisites

- Completed data and configuration backup
- Downloaded new version [source code](https://gitee.com/kwdb/kwdb)
- [Compilation environment and dependencies](https://gitee.com/kwdb/kwdb#%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F%E5%92%8C%E8%BD%AF%E4%BB%B6%E4%BE%9D%E8%B5%96) meet KWDB requirements

### Steps

1. Compile the new version following the [KWDB compilation documentation](https://gitee.com/kwdb/kwdb#%E7%BC%96%E8%AF%91%E5%92%8C%E5%AE%89%E8%A3%85).
2. Start the service using the same [startup command](../tool-command-reference/client-tool/kwbase-sql-reference.md#kwbase-start) as the previous version.
3. Verify that the service is running as expected.

## Upgrade for Container Image Deployment

For KWDB deployed using Docker container images, upgrades are performed by updating the container image.

This section covers two upgrade methods:

- Upgrade using Docker Compose
- Upgrade using Docker commands

### Upgrade Using Docker Compose

#### Prerequisites

- Data and configuration files have been backed up.
- The new version container image has been obtained.

#### Steps

1. Load the new container image:

   ```bash
   docker load < KaiwuDB.tar
   ```

2. Stop and remove existing containers:

   ```bash
   docker-compose down
   ```

3. Remove the old version image:

   ```bash
   docker rmi ${image_name}
   ```

4. Update the image version in `docker-compose.yml`.

5. Start KWDB with the new version:

   ```bash
   docker-compose up -d
   ```

### Upgrade Using Docker Commands

#### Prerequisites

- Data and configuration files have been backed up.

#### Steps

1. Stop the KWDB container. The container name is the one specified by the `--name` parameter when running the container.

   ```bash
      docker stop <kwdb-container>
   ```

2. Remove the container:

   ```bash
      docker rm <kwdb-container>
   ```

3. Obtain the new version image:

   - Pull from image repository:

      ```bash
         docker pull kwdb/kwdb:<new_version_number>
      ```

   - Import from local file:

      ```bash
         docker load < KaiwuDB.tar
      ```

4. Start the new version container. All parameters should remain consistent with the original container except for the image name.
   - Insecure mode:

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

   - Secure mode:

     ```bash
     docker run -d --privileged --name kwdb \
         --ulimit memlock=-1 \
         --ulimit nofile=$max_files \
         -p $db_port:26257 \
         -p $http_port:8080 \
         -v /etc/kaiwudb/certs:<certs_dir> \
         -v /var/lib/kaiwudb:/kaiwudb/deploy/kwdb-container \
         --ipc shareable \
         -w /kaiwudb/bin \
         <kwdb_image> \
         ./kwbase start-single-node \
         --certs-dir=<certs_dir> \
         --listen-addr=0.0.0.0:26257 \
         --http-addr=0.0.0.0:8080 \
         --store=/kaiwudb/deploy/kwdb-container
     ```
