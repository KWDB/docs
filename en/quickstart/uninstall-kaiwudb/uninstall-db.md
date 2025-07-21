---
title: Uninstall KWDB
id: uninstall-db
---

# Uninstall KWDB

This section provides comprehensive uninstallation procedures for single-node KWDB. Choose the appropriate uninstallation approach based on your original deployment method.

## Script Deployment

1. Stop KWDB.

    ```shell
    systemctl stop kaiwudb
    ```

2. Change to the `kwdb_install` directory.

3. Execute the uninstallation command.

    ```shell
    ./deploy.sh uninstall 
    ```

4. Confirm whether to delete the data directory.

    ```shell
    When uninstalling KWDB, you can either delete or keep all user data. Please confirm your choice: Do you want to delete the data? (y/n): 
    ```

    - Enter `y`: Delete the data directory and unmount the loop device.
    - Enter `n`: Keep the data directory for future use.

## kwbase CLI Deployment

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

5. Delete the complied binary and library.

## Docker Deployment

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

6. Delete data directory. Default data directory is `/var/lib/kaiwudb`.

   ```bash
   sudo rm -rf <data_path>
   ```