---
title: Deploy Using Docker
id: docker-deployment
---

# Deploy Using Docker

This section describes how to deploy a KWDB cluster on a single machine using the Docker Run commands.

**Note**: For production environments, it is recommended to deploy only one node per machine to improve availability and reduce the risk of data loss.

## Prerequisites

- The hardware, operating system, software dependencies, and ports of the nodes to be deployed meet the [deployment requirements](../prepare/before-deploy-docker.md#hardware).
- One of the following user permissions:
  - Root user access
  - Regular user with `sudo` privileges:
    - Users with passwordless `sudo` won't need to enter passwords during installation.
    - Users without passwordless `sudo` will be prompted for passwords when needed.
    - Regular users must be in the docker group (add with `sudo usermod -aG docker $USER`).
- The [KWDB image](../prepare/before-deploy-docker.md#obtaining-container-images) is obtained.

## Steps

1. (Optional) If you need to deploy the cluster in secure mode, create the necessary certificates using the following commands:

    ::: tip

    If deploying in secure mode across machines, you need to use the `./kwbase cert create-node <node_ip>` command to create certificates and keys for all nodes, and transfer all the certificates and keys to all node.

    :::

    ```shell
    docker run --rm --privileged \
      -v /etc/kaiwudb/certs:<certs_dir> \
      -w /kaiwudb/bin \
      <kwdb_image> \
      bash -c './kwbase cert create-ca --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key && \
                ./kwbase cert create-client root --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key && \
                ./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0 --certs-dir=<certs_dir> --ca-key=<certs_dir>/ca.key'
    ```

    Parameters:
  
    | Parameter | Description |
    |---|---|
    | `--rm` | Automatically removes the container after it stops. |
    | `--privileged` | Grants extended privileges to the container. |
    | `-v` | Mounts the host's `/etc/kaiwudb/certs` directory to the container's `<certs_dir>` directory for certificate and key storage. |
    | `-w /kaiwudb/bin` | Sets the working directory inside the container to `/kaiwudb/bin`. |
    | `kwdb_image` | Container image name and tag (e.g., `kwdb:3.0.0`). |
    | `bash -c` | Executes the following certificate creation commands within the container:<br>- `./kwbase cert create-ca`: Creates a certificate authority (CA), generating CA certificates and keys.<br>- `./kwbase cert create-client root`: Creates client certificates and keys for the `root` user.<br>- `./kwbase cert create-node 127.0.0.1 localhost 0.0.0.0`: Creates node server certificates and keys, supporting access through three network identifiers: local loopback address (`127.0.0.1`), local hostname (`localhost`), and all network interfaces (`0.0.0.0`).<br>- `--certs-dir=<certs_dir>`: Specifies the certificate storage directory.<br>- `--ca-key=<certs_dir>/ca.key`: Specifies the CA key path.|

2. Start three or more database instances.

    - Insecure mode

      ```shell
      docker run -d --name kwdb1 --privileged \
        --ulimit memlock=-1 --ulimit nofile=1048576 \
        -p 26257:26257 \
        -p 27257:27257 \
        -p 8080:8080 \
        -v /var/lib/kwdb1:/kaiwudb/deploy/kwdb-container \
        --ipc shareable -w /kaiwudb/bin \
        <kwdb_image> \
        ./kwbase start --insecure --listen-addr=0.0.0.0:26257 \
        --advertise-addr=<host1>:26257 --brpc-addr=:27257 --http-addr=0.0.0.0:8080 \
        --store=/kaiwudb/deploy/kwdb-container --join <host1>:26257

      docker run -d --name kwdb2 --privileged \
        --ulimit memlock=-1 --ulimit nofile=1048576 \
        -p 26258:26257 \
        -p 27258:27258 \
        -p 8081:8080 \
        -v /var/lib/kwdb2:/kaiwudb/deploy/kwdb-container \
        --ipc shareable -w /kaiwudb/bin \
        <kwdb_image> \
        ./kwbase start --insecure --listen-addr=0.0.0.0:26257 \
        --advertise-addr=<host2>:26258 --brpc-addr=:27258 --http-addr=0.0.0.0:8080 \
        --store=/kaiwudb/deploy/kwdb-container --join <host1>:26257

      docker run -d --name kwdb3 --privileged \
        --ulimit memlock=-1 --ulimit nofile=1048576 \
        -p 26259:26257 \
        -p 27259:27259 \
        -p 8082:8080 \
        -v /var/lib/kwdb3:/kaiwudb/deploy/kwdb-container \
        --ipc shareable -w /kaiwudb/bin \
        <kwdb_image> \
        ./kwbase start --insecure --listen-addr=0.0.0.0:26257 \
        --advertise-addr=<host3>:26259 --brpc-addr=:27259 --http-addr=0.0.0.0:8080 \
        --store=/kaiwudb/deploy/kwdb-container --join <host1>:26257
      ```

    - Secure mode

      ```shell
      docker run -d --name kwdb1 --privileged \
        --ulimit memlock=-1 --ulimit nofile=1048576 \
        -p 26257:26257 \
        -p 27257:27257 \
        -p 8080:8080 \
        -v /etc/kaiwudb/certs:<certs_dir> \
        -v /var/lib/kwdb1:/kaiwudb/deploy/kwdb-container \
        --ipc shareable -w /kaiwudb/bin \
        <kwdb_image> \
        ./kwbase start --certs-dir=<certs_dir> --listen-addr=0.0.0.0:26257 \
        --advertise-addr=<host1>:26257 --brpc-addr=:27257 --http-addr=0.0.0.0:8080 \
        --store=/kaiwudb/deploy/kwdb-container --join <host1>:26257

      docker run -d --name kwdb2 --privileged \
        --ulimit memlock=-1 --ulimit nofile=1048576 \
        -p 26258:26257 \
        -p 27258:27258 \
        -p 8081:8080 \
        -v /etc/kaiwudb/certs:<certs_dir> \
        -v /var/lib/kwdb2:/kaiwudb/deploy/kwdb-container \
        --ipc shareable -w /kaiwudb/bin \
        <kwdb_image> \
        ./kwbase start --certs-dir=<certs_dir> --listen-addr=0.0.0.0:26257 \
        --advertise-addr=<host2>:26258 --brpc-addr=:27258 --http-addr=0.0.0.0:8080 \
        --store=/kaiwudb/deploy/kwdb-container --join <host1>:26257

      docker run -d --name kwdb3 --privileged \
        --ulimit memlock=-1 --ulimit nofile=1048576 \
        -p 26259:26257 \
        -p 27259:27259 \
        -p 8082:8080 \
        -v /etc/kaiwudb/certs:<certs_dir> \
        -v /var/lib/kwdb3:/kaiwudb/deploy/kwdb-container \
        --ipc shareable -w /kaiwudb/bin \
        <kwdb_image> \
        ./kwbase start --certs-dir=<certs_dir> --listen-addr=0.0.0.0:26257 \
        --advertise-addr=<host3>:26259 --brpc-addr=:27259 --http-addr=0.0.0.0:8080 \
        --store=/kaiwudb/deploy/kwdb-container --join <host1>:26257
      ```

    Parameters:

    | Parameter | Description |
    |---|---|
    | `-d` | Runs the container in the background and returns the container ID. |
    | `--name` | Specifies the container name for easier management. |
    | `--privileged` | Grants extended privileges to the container. |
    | `--ulimit memlock=-1` | Removes container memory size limit. |
    | `--ulimit nofile=1048576` | Sets the maximum number of files that processes inside the container can open. |
    | `-p` | Port mapping for the database service port (26257), brpc port, and HTTP port (8080). **Note:** The brpc port must be the same on both the host and container. |
    | `-v` | Sets up volume mounts:<br>- Mounts host's `/var/lib/kaiwudb` directory to container's `/kaiwudb/deploy/kwdb-container` directory for persistent data storage.<br>- In secure mode, mounts host's `/etc/kaiwudb/certs` directory to container's `<certs_dir>` directory for certificate and key storage. |
    | `--ipc shareable` | Allows other containers to share this container's IPC namespace. |
    | `-w /kaiwudb/bin` | Sets the working directory inside the container to `/kaiwudb/bin`. |
    | `kwdb_image` | Container image variable (replace with actual image name and tag, e.g., `kwdb:3.0.0`). |
    | `./kwbase start` | Database startup command with different flags for different modes:<br>- `--insecure`: (Insecure mode only) Runs in insecure mode.<br>- `--certs-dir=<certs_dir>`: (Secure mode) Specifies certificate directory location.<br>- `--listen-addr=0.0.0.0:26257`: Address and port the database listens on.<br>- `--advertise-addr=${host}:2625X`: Address and port the database uses to communicate with other cluster nodes.<br>- `--brpc-addr=:2725X`: brpc port for inter-node communication between KaiwuDB time-series engines.<br>- `--http-addr=0.0.0.0:8080`: Address and port the HTTP interface.<br>- `--store=/kaiwudb/deploy/kwdb-container`: Specifies data storage location.<br>- `--join ${host}:26257`: Address for the node to connect to the cluster (can specify one or more cluster nodes).|

3. Initialize the cluster:

    - Insecure mode

        ```shell
        docker exec kwdb1 ./kwbase init --insecure --host=<host1>:26257
        ```

    - Secure mode

        ```shell
        docker exec kwdb1 ./kwbase init --certs-dir=<certs_dir> --host=<host1>:26257
        ```

    Parameters:

    | Parameter | Description |
    |---|---|
    | `docker exec kwdb1` | Executes commands inside the container named `kwdb1`. |
    | `./kwbase init` | Executes the cluster initialization command:<br>- `--insecure`: (Insecure mode only) Enables insecure mode.<br>- `--certs-dir=<certs_dir>`: (Secure mode) Specify certificate directory location.<br>- `--host=<host1>:26257`: Specifies the host address and port to connect to.|