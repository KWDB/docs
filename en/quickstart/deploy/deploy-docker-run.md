---
title: Docker Run Deployment
id: quickstart-docker
---

# Docker Run Deployment

## Prerequisites

- Obtained KWDB [container installation package](../prepare.md#installation-packages).
- The hardware, operating system, software dependencies, and ports of the node to be deployed meet the [installation deployment requirements](../prepare.md).
- Installation user is root or a regular user with `sudo` privileges.
  - Root users and regular users configured with `sudo` passwordless access do not need to enter a password when executing deployment scripts.
  - Regular users without `sudo` passwordless configuration need to enter a password for privilege escalation when executing deployment scripts.
- For non-root installation users, the user needs to be added to the `docker` group using `sudo usermod -aG docker $USER`.

## Steps

1. Import the `KaiwuDB.tar` file in the `kwdb_install/packages` directory to get the image name.

    ```shell
    docker load < KaiwuDB.tar
    Loaded image: "$kwdb_image"
    ```

2. (Optional) To deploy KWDB in secure mode, use the following command to create the database certificate authority, client certificate for the `root` user, and node server certificate.

    ```shell
    docker run --rm --privileged \
      -v /etc/kaiwudb/certs:/kaiwudb/certs \
      -w /kaiwudb/bin \
      $kwdb_image \
      bash -c './kwbase cert create-ca --certs-dir=/kaiwudb/certs --ca-key=/kaiwudb/certs/ca.key && \
                ./kwbase cert create-client root --certs-dir=/kaiwudb/certs --ca-key=/kaiwudb/certs/ca.key && \
                ./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=/kaiwudb/certs --ca-key=/kaiwudb/certs/ca.key'
    ```

    Parameter description:
    
    | Parameter | Description |
    |---|---|
    | `--rm` | Automatically delete the container after it stops. |
    | `--privileged` | Grant extended privileges to the container. |
    | `-v` | Set container directory mapping, mounting the host's `/etc/kaiwudb/certs` directory to the container's `/kaiwudb/certs` directory for storing certificates and keys. |
    | `-w /kaiwudb/bin` | Set the working directory in the container to `/kaiwudb/bin`. |
    | `$kwdb_image` | Container image, needs to be filled with the actual image name and tag, for example `kwdb:3.0.0`. |
    | `bash -c` | Execute the following certificate creation commands in the container, where:<br>- `./kwbase cert create-ca`: Create certificate authority (CA), generate CA certificate and key.<br>- `./kwbase cert create-client root`: Create client certificate and key for `root` user.<br>- `./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0`: Create node certificate and key, supporting access through three network identifiers: local loopback address (`127.0.0.1`), local hostname (`localhost`), and all network interfaces (`0.0.0.0`).<br>- All commands use `--certs-dir=/kaiwudb/certs` to specify certificate storage directory and `--ca-key=/kaiwudb/certs/ca.key` to specify key path. |

3. Start the KWDB database.

    - Insecure mode

      ```shell
      docker run -d --privileged --name kaiwudb \
        --ulimit memlock=-1 \
        --ulimit nofile=$max_files \
        -p $db_port:26257 \
        -p $http_port:8080 \
        -v /var/lib/kaiwudb:/kaiwudb/deploy/kaiwudb-container \
        --ipc shareable \
        -w /kaiwudb/bin \
        $kwdb_image \
        ./kwbase start-single-node \
          --insecure \
          --listen-addr=0.0.0.0:26257 \
          --http-addr=0.0.0.0:8080 \
          --store=/kaiwudb/deploy/kaiwudb-container
      ```

    - Secure mode

        ```bash
        docker run -d --privileged --name kaiwudb \
          --ulimit memlock=-1 \
          --ulimit nofile=$max_files \
          -p $db_port:26257 \
          -p $http_port:8080 \
          -v /etc/kaiwudb/certs:/kaiwudb/certs \
          -v /var/lib/kaiwudb:/kaiwudb/deploy/kaiwudb-container \
          --ipc shareable \
          -w /kaiwudb/bin \
          $kwdb_image \
          ./kwbase start-single-node \
            --certs-dir=/kaiwudb/certs \
            --listen-addr=0.0.0.0:26257 \
            --http-addr=0.0.0.0:8080 \
            --store=/kaiwudb/deploy/kaiwudb-container
        ```

    Parameter description:

    | Parameter | Description |
    |---|---|
    | `-d` | Run container in background and return container ID. |
    | `--name` | Specify container name for subsequent management. |
    | `--privileged` | Grant extended privileges to the container. |
    | `--ulimit memlock=-1` | Remove container memory size limit. |
    | `--ulimit nofile=$max_files` | Set the maximum number of files that processes in the container can open. |
    | `-p` | Port mapping, mapping database service port (26257) and HTTP port (8080) respectively.|
    | `-v` | Set container directory mapping:<br>- Mount the host's `/var/lib/kaiwudb` directory to the container's `/kaiwudb/deploy/kaiwudb-container` directory for persistent data storage.<br>- In secure mode, mount the host's `/etc/kaiwudb/certs` directory to the container's `/kaiwudb/certs` directory for storing certificates and keys. |
    | `--ipc shareable` | Allow other containers to share this container's IPC namespace. |
    | `-w /kaiwudb/bin` | Set the working directory in the container to `/kaiwudb/bin`. |
    | `$kwdb_image` | Container image variable, needs to be replaced with the actual image name and tag, for example `kwdb:3.0.0`. |
    | `./kwbase start` | Database startup command running in the container, which varies depending on secure and Insecure modes:<br>- `--insecure`: (Insecure mode only) Run in Insecure mode.<br>- `--certs-dir=/kaiwudb/certs`: (Secure mode) Certificate directory location.<br>- `--listen-addr=0.0.0.0:26257`: Database listening address and port.<br>- `--http-addr=0.0.0.0:8080`: HTTP interface listening address and port.<br>- `--store=/kaiwudb/deploy/kaiwudb-container`: Specify data storage location.|

4. (Optional) Create a database user and grant admin privileges. If this step is skipped, the system will default to using the user that deployed the database without requiring a password to access the database.

      - Insecure mode (without password):

          ```bash
          docker exec kaiwudb bash -c "./kwbase sql --insecure --host=$host_ip -e \"create user $username;grant admin to $username with admin option;\""
          ```

      - Secure mode (with password):

          ```bash
          docker exec kaiwudb bash -c "./kwbase sql --host=$host_ip --certs-dir=$cert_path -e \"create user $username with password \\\"$user_password\\\";grant admin to $username with admin option;\""
          ```

5. After deployment is complete, you can connect to and manage KWDB via [kwbase CLI](../access/access-cli.md), [KaiwuDB JDBC](../access/access-jdbc.md), or [KaiwuDB Developer Center](../access/access-kdc.md).
