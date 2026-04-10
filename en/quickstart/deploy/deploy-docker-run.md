---
title: Docker Run Deployment
id: quickstart-docker
---

# Docker Run Deployment

## Prerequisites

- Obtained KWDB [docker image](../prepare.md#installation-packages-container-images-and-compilation-versions).
- The hardware, operating system, software dependencies, and ports of the node to be deployed meet the [installation deployment requirements](../prepare.md).
- Installation user is root or a regular user with `sudo` privileges.
  - Root users and regular users configured with `sudo` passwordless access do not need to enter a password when executing deployment scripts.
  - Regular users without `sudo` passwordless configuration need to enter a password for privilege escalation when executing deployment scripts.
- For non-root installation users, the user needs to be added to the `docker` group using `sudo usermod -aG docker $USER`.

## Steps

1. (Optional) To deploy KWDB in secure mode, use the following command to create the database certificate authority, client certificate for the `root` user, and node server certificate.

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
    | `--rm` | Automatically removes the container after it stops. |
    | `--privileged` | Grants extended privileges to the container. |
    | `-v` | Mounts the host's `/etc/kaiwudb/certs` directory to the container's `<certs_dir>` directory for certificate and key storage. |
    | `-w /kaiwudb/bin` | Sets the working directory inside the container to `/kaiwudb/bin`. |
    | `kwdb_image` | Container image name and tag (e.g., `kwdb:3.0.0`). |
    | `bash -c` | Executes the following certificate creation commands within the container:<br>- `./kwbase cert create-ca`: Creates a certificate authority (CA), generating CA certificates and keys.<br>- `./kwbase cert create-client root`: Creates client certificates and keys for the `root` user.<br>- `./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0`: Creates node server certificates and keys, supporting access through three network identifiers: local loopback address (`127.0.0.1`), local hostname (`localhost`), and all network interfaces (`0.0.0.0`).<br>- `--certs-dir=<certs_dir>`: Specifies the certificate storage directory.<br>- `--ca-key=<certs_dir>/ca.key`: Specifies the CA key path.|

2. Start the KWDB database.

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
    | `-d` | Runs the container in the background and returns the container ID. |
    | `--name` | Specifies the container name for easier management. |
    | `--privileged` | Grants extended privileges to the container. |
    | `--ulimit memlock=-1` | Removes container memory size limit. |
    | `--ulimit nofile=$max_files` | Sets the maximum number of file descriptors that can be opened concurrently by processes within the container. |
    | `-p` | Maps ports between host and container (database service port 26257 and HTTP port 8080). |
    | `-v` | Sets up volume mounts:<br>- Mounts host's `/var/lib/kaiwudb` directory to container's `/kaiwudb/deploy/kwdb-container` directory for persistent data storage.<br>- In secure mode, mounts host's `/etc/kaiwudb/certs` directory to container's `<certs_dir>` directory for certificate and key storage. |
    | `--ipc shareable` | Allows other containers to share this container's IPC namespace. |
    | `-w /kaiwudb/bin` | Sets the working directory inside the container to `/kaiwudb/bin`. |
    | `kwdb_image` | Container image variable (replace with actual image name and tag, e.g., `kwdb:3.0.0`). |
    | `./kwbase start` | Database startup command with different flags for different mode:<br>- `--insecure`: (Insecure mode only) Runs in insecure mode.<br>- `--certs-dir=<certs_dir>`: (Secure mode) Specifies certificate directory location.<br>- `--listen-addr=0.0.0.0:26257`: Address and port for database client connections.<br>- `--http-addr=0.0.0.0:8080`: Address and port for the web-based admin UI and API endpoints.<br>- `--store=/kaiwudb/deploy/kwdb-container`: Specifies data storage location.|

3. (Optional) Create a database user and grant administrator privileges to the user. If skipped, the system will use database deployment user by default, and no password is required to access the database.

      - Insecure mode (without password):

          ```bash
          docker exec kwdb bash -c "./kwbase sql --insecure --host=<host_ip> -e \"create user <username>;grant admin to <username> with admin option;\""
          ```

      - Secure mode (with password):

          ```bash
          docker exec kwdb bash -c "./kwbase sql --host=<host_ip> --certs-dir=<cert_dir> -e \"create user <username> with password \\\"<user_password>\\\";grant admin to <username> with admin option;\""
          ```

4. After deployment is complete, you can connect to and manage KWDB via [kwbase CLI](../access/access-cli.md), [KaiwuDB JDBC](../access/access-jdbc.md), or [KaiwuDB Developer Center](../access/access-kdc.md).
