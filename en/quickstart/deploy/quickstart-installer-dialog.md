---
title: Terminal Graphical Interaction Mode Deployment
id: quickstart-installer-dialog
---

# Terminal Graphical Interaction Mode Deployment

Terminal graphical interaction mode provides a graphical experience in the character interface, supports using arrow keys and Enter to operate checkboxes, input boxes, confirmation dialogs, progress bars, and other interactive components.

During installation, the program performs real-time parameter validation. If a configuration is invalid, it prompts you to re-enter the value. It supports both secure and insecure modes, and after deployment completes, you can choose to start the database immediately.

## Prerequisites

**System requirements**:

- The hardware, operating system, and software dependencies of the node to be deployed meet the requirements in [Deployment Preparation](../prepare.md).
- You have obtained the KaiwuDB installer (`.run` file).

**User permission requirements**:

- The installation user must be `root` or a regular user with passwordless `sudo` configured.
- If you are using the container installer and the installation user is not `root`, run the following command to add the user to the `docker` group:

  ```bash
  sudo usermod -aG docker $USER
  ```

## Steps

1. Log in to the node to be deployed, copy the `.run` installer to the installation directory, and grant execution permissions:

    ```bash
    chmod +x KWDB-*.run
    ```

2. Start the installer in terminal graphical interaction mode:

    ```bash
    ./KWDB-*.run -i
    # or
    ./KWDB-*.run --interact
    ```

3. After the installer starts, go to the main menu and use the arrow keys to select **Install KWDB**, then press Enter.

    ![](../../static/quickstart/gui-dialog-welcome.png)

4. Enter the installation parameter settings menu and configure each item as needed:

    ![](../../static/quickstart/gui-dialog-config.png)

    Parameter descriptions:

    | Parameter | Description |
    |-----------|-------------|
    | Set secure mode | Supported values are:<br>- **Insecure mode**: no encrypted transport.<br>- **TLS encryption**: (default) enable TLS secure mode. When secure mode is enabled, KWDB automatically generates certificates and stores them in `/etc/kaiwudb/certs`. |
    | Set database service port | KWDB service port; default is `26257`. |
    | Set Admin UI port | KWDB Web service port; default is `8080`. |
    | Set data transfer port | Data transfer port between time-series engines. For single-node deployment, the system ignores this setting automatically; default is `27257`. |
    | Select deployment mode | Single-node mode, single-replica cluster, or three-replica cluster. For single-node deployment, select **Single-node mode**. |
    | Add node | Add node information, including host name, port, username, and password. |
    | View node list | View the added node information. |
    | Set data directory | Data directory; default is `/var/lib/kaiwudb`. |

5. After all settings are complete, select **Start Installation** and press Enter to start installing KWDB.

6. Choose whether to install KWDB for all users as needed.

7. During installation, the terminal displays the progress in real time. If an error occurs, you can review the log files in the `log` directory under the installation directory for detailed information.

8. After installation succeeds, the terminal displays a success message and asks whether to start the database.
    - Select Yes: the system starts KWDB automatically.
    - Select No: start KWDB manually later.

        ```bash
        systemctl start kaiwudb
        ```

    ![](../../static/quickstart/gui-dialog-start.png)

9. View the service or node status:

    ```bash
    # View service status
    systemctl status kaiwudb

    # View node status
    kw-status
    ```

    Field descriptions for node status:

    | Field | Description |
    |-------|-------------|
    | `id` | Node ID. |
    | `address` | Node address. |
    | `sql_address` | SQL address. |
    | `build` | KWDB version running on the node. |
    | `started_at` | Node startup date and time. |
    | `updated_at` | Node status update time. When the node is healthy, a new status record is written about every 10 seconds. If the node is abnormal, the update may lag. |
    | `locality` | Node ID. |
    | `start_mode` | Node startup mode. |
    | `is_available` / `is_live` | `true` means the node is healthy; `false` means the node is abnormal. |

10. (Optional) Configure KWDB to start automatically at system startup:

    ```bash
    systemctl enable kaiwudb
    ```

11. Run `kw-sql` to log in to the database as the deployment user, or connect to and manage KWDB using any of the following methods:
    - [kwbase CLI](../access/access-cli.md)
    - [KaiwuDB JDBC](../access/access-jdbc.md)
    - [KaiwuDB Developer Center](../access/access-kdc.md)
