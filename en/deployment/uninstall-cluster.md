---
title: Uninstall KWDB Cluster
id: uninstall-cluster
---

# Uninstall KWDB Cluster

This section provides comprehensive uninstallation procedures for KWDB clusters across different deployment methods. Choose the appropriate uninstallation approach based on your original deployment method.

## Script Deployment

1. Log in to the initial deployment node.
2. Transfer the `kwdb_install` directory to all other cluster nodes.
    1. Create the required directory on remote nodes.

        ```shell
        ssh <username>@<node2_address> "mkdir -p ~/kwdb_install"
        ssh <username>@<node3_address> "mkdir -p ~/kwdb_install"
        # Repeat for additional nodes...
        ```

    2. Transfer the installation directory to remote nodes.

        ```shell
        scp -r kwdb_install <username>@<node2_address>:~/kwdb_install/
        scp -r kwdb_install <username>@<node3_address>:~/kwdb_install/
        # Repeat for additional nodes...  
        ```

3. Uninstall on each node.
    1. Stop KWDB.

        ```shell
        systemctl stop kaiwudb
        ```

    2. Change to the `kwdb_install` directory.

    3. Run the uninstallation command.

        ```shell
        ./deploy.sh uninstall 
        ```

    4. When prompted, decide whether to keep or remove data.

        ```shell
        When uninstalling KaiwuDB, you can either delete or keep all user data. Please confirm your choice: Do you want to delete the data? (y/n): 
        ```

        - Enter `y` to delete the data directory and unmount the loop device.
        - Enter `n` to keep the data directory for future use.


## CLI Deployment

For clusters deployed using the kwbase CLI, execute these steps on **each node**:

::: warning  

Before proceeding, ensure all important data has been backed up. These operations will permanently delete all KWDB data and configurations.

:::

1. Stop KWDB.

2. Check and unmount loop devices:

   ```bash
   # List active loop devices
   losetup -a
   
   # Unmount the appropriate device
   sudo umount /dev/loop<device_number>
   ```

3. Remove custom certificate directory:

   ```bash
   sudo rm -rf <cert_path>
   ```

4. Delete data directory:

   ```bash
   sudo rm -rf <data_path>
   ```

5. Delete the complied libraries and binaries.

## Docker Deployment

For clusters deployed using Docker images, execute these steps on **each node**:

::: warning

Before proceeding, ensure all important data has been backed up. These operations will permanently delete all KWDB data and configurations.

:::

1. Stop the KWDB container:

   ```bash
   docker stop kwdb-container
   ```

   ::: tip  

   Replace `kwdb-container` with the actual container name specified using the `--name` parameter during container creation.

   :::

2. Remove the container:

   ```bash
   docker rm kwdb-container
   ```

3. Delete the Docker image:

   ```bash
   # Retrieve the image name
   docker ps -a --filter name=kwdb-container --format "{{.Image}}"
   
   # Remove the image
   docker rmi ${image_name}
   ```

4. Check and unmount loop devices:

   ```bash
   # List active loop devices
   losetup -a
   
   # Unmount the appropriate device
   sudo umount /dev/loop<device_number>
   ```

5. Remove custom certificate directory:

   ```bash
   sudo rm -rf <cert_path>
   ```

6. Delete data directory:

   ```bash
   # Default data directory is /var/lib/kaiwudb
   sudo rm -rf <data_path>
   ```