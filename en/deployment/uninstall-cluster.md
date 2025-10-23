---
title: Uninstall KWDB Cluster
id: uninstall-cluster
---

# Uninstall KWDB Cluster

This section describes how to uninstall KWDB clusters for different deployment scenarios, including script deployment, kwbase CLI deployment, and container image deployment. Choose the appropriate uninstallation method based on your deployment approach.

## Uninstall Script Deployment

For KWDB deployed using the installation script, perform the following steps:

1. Log in to the initial deployment node.
2. Transfer the `kwdb_install` directory to all other cluster nodes.
    1. Log in to remote nodes and create the required directory:

        ```shell
        ssh <username>@<node2_address> "mkdir -p ~/kwdb_install"
        ssh <username>@<node3_address> "mkdir -p ~/kwdb_install"
        ...
        ```

    2. Transfer the `kwdb_install` directory to the target nodes:

        ```shell
        scp -r kwdb_install <username>@<node2_address>:~/kwdb_install/
        scp -r kwdb_install <username>@<node3_address>:~/kwdb_install/
        ...  
        ```

3. Execute the following operations on each node in the cluster:
    1. Stop the KWDB service:

        ```shell
        systemctl stop kaiwudb
        ```

    2. Run the uninstallation command in the `kwdb_install` directory:

        ```shell
        ./deploy.sh uninstall 
        ```

    3. When prompted, choose whether to delete the data directory:

         ```shell
         When uninstalling KaiwuDB, you can either delete or keep all user data. Please confirm your choice: Do you want to delete the data? (y/n): 
         ```

         - Enter `y`: Delete the data directory.
         - Enter `n`: Keep the data directory for future use.

## Uninstall kwbase CLI Deployment

For KWDB deployed using kwbase CLI, perform the following steps on each node to be uninstalled:

::: warning

Before proceeding, ensure all important data has been backed up. These operations will permanently delete all KWDB data and configurations.

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

## Uninstall Container Image Deployment

For KWDB deployed using a container image, perform the following steps on each node to be uninstalled:

::: warning

Before proceeding, ensure all important data has been backed up. These operations will permanently delete all KWDB data and configurations.

:::

1. Stop the KWDB container:

   ::: tip

   The container name is the name specified in the `--name` parameter when running the container.

   :::

   ```bash
   docker stop kwdb-container
   ```

2. Remove the container:

   ```bash
   docker rm kwdb-container
   ```

3. Delete the Docker image:

   ```bash
   # Get the image name
   docker ps -a --filter name=kwdb-container --format "{{.Image}}"
   
   # Remove the image
   docker rmi ${image_name}
   ```

4. Remove custom certificate directory:

   ```bash
   sudo rm -rf <cert_path>
   ```

5. Delete the data directory (default location: `/var/lib/kaiwudb`):

   ```bash
   sudo rm -rf <data_path>
   ```