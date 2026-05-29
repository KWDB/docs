---
title: Uninstall KWDB
id: uninstall-cluster
---

# Uninstall KWDB

This section describes the uninstallation methods for KWDB under different deployment scenarios, including installer deployment, kwbase CLI deployment, and container image deployment. Choose the appropriate uninstallation method based on your actual deployment method.

## Uninstall Installer Deployment

For KWDB deployed using the installer, choose the uninstallation method corresponding to the interaction mode used during installation.

### Command-Line Mode

**Prerequisite**: The KWDB service has been stopped.

```bash
systemctl stop kaiwudb
```

**Steps**:

1. Log in to the initial node where KWDB was deployed, and start the installer in command-line mode:

    ```bash
    ./KWDB-*.run -c
    # or
    ./KWDB-*.run --cli
    ```

2. In the main menu, enter `2` to select Uninstall KWDB:

    ```plain
    1. Install KWDB
    2. Uninstall KWDB
    3. Install KWDB and Join a Cluster
    4. Upgrade Node
    5. Exit

    Please enter an option [1-5]:
    ```

3. Enter the number of nodes to remove when prompted:

    ```plain
    Please enter the number of nodes (1-100):
    ```

4. The installer automatically opens the configuration file. Verify the node information, then save and exit. The configuration file format is as follows:

    ```ini
    [global]
    # Data directory
    data_root=/var/lib/kaiwudb

    [node1]
    host=127.0.0.1
    port=22
    user=admin
    passwd=*******
    ```

5. Confirm whether to delete data and configuration files when prompted. Enter `y` to delete or `N` to keep:

    ```plain
    Delete data and configuration files? (y/N):
    ```

    After uninstallation is complete, the console displays a message confirming that all nodes have been successfully uninstalled and the script exits safely.

### Terminal Graphical Interaction Mode

**Prerequisite**: The KWDB service has been stopped.

```bash
systemctl stop kaiwudb
```

**Steps**:

1. Log in to the initial node where KWDB was deployed, and start the installer in terminal graphical interaction mode:

    ```bash
    ./KWDB-*.run -i
    # or
    ./KWDB-*.run --interact
    ```

2. In the main menu, use the arrow keys to select **Uninstall KWDB**, then press Enter to confirm.

3. Enter the parameter settings menu and configure each item as needed:

    Parameter descriptions:

    | Parameter | Description |
    |--------|------|
    | Set uninstall nodes | Add information for the nodes to be uninstalled, including host name, port, username, and password. |
    | Manage uninstall node list | View the added node information. |
    | Set data directory | Enter the data directory to be deleted; default is `/var/lib/kaiwudb`. |

4. After all settings are complete, select **Start Uninstallation** and press Enter to begin.

5. Confirm whether to delete all configurations and data when prompted. After uninstallation is complete, the interface displays a completion message.

## Uninstall kwbase CLI Deployment

For KWDB deployed through source code compilation, perform the following operations on each node:

::: warning Note

Before performing deletion operations, ensure all important data has been backed up. The following operations will permanently delete all KWDB data and configurations.

:::

1. Stop the KWDB service.

2. Remove the custom certificate directory:

   ```bash
   sudo rm -rf <cert_path>
   ```

3. Delete the data directory:

   ```bash
   sudo rm -rf <data_path>
   ```

4. Delete the compiled binary files and libraries.

## Uninstall Container Image Deployment

For KWDB deployed using a container image, perform the following operations on each node:

::: warning Note

Before performing deletion operations, ensure all important data has been backed up. The following operations will permanently delete all KWDB data and configurations.

:::

1. Stop the KWDB container.

   ::: warning Note

   The container name is the name specified in the `--name` parameter when running the container.
   :::

   ```bash
   docker stop <kwdb-container>
   ```

2. Remove the container:

   ```bash
   docker rm <kwdb-container>
   ```

3. Delete the Docker image:

   ```bash
   # Get the image name
   docker ps -a --filter name=kwdb-container --format {{.Image}}
   
   # Remove the image
   docker rmi ${image_name}
   ```

4. Remove the custom certificate directory:

   ```bash
   sudo rm -rf <cert_path>
   ```

5. Delete the data directory (default: `/var/lib/kaiwudb`):

   ```bash
   sudo rm -rf <data_path>
   ```
