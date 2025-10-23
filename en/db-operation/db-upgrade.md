---
title: Database Upgrade
id: db-upgrade
---

# Database Upgrade

This section covers upgrade procedures for KWDB database across different deployment scenarios, including upgrades using deployment scripts and container images.

Before upgrading, carefully review all precautions and select the appropriate upgrade method based on your deployment approach.

## Upgrade Using Deployment Scripts

Due to major architectural refactoring in v3.0.0, v1.x and v2.x **cannot be directly upgraded** to v3.0.0.

**Recommended upgrade approach:**

1. Deploy a new v3.0.0 version.
2. Migrate data using the export and import functionality.

For instructions, see [Data Export](../db-administration/import-export-data/export-data.md) and [Data Import](../db-administration/import-export-data/import-data.md).

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
      docker stop kwdb-container
   ```

2. Remove the container:

   ```bash
      docker rm kwdb-container
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
