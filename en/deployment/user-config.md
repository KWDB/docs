---
title: Create Users
id: user-config
---

# Create Users

After deploying and starting the cluster, you can create database users using either the `add_user.sh` script from the `kwdb_install` directory or the kwbase CLI.

If you skip the user creation step, the system will use the default user from database deployment and allow database access without authentication.

## Using the User Creation Script

KWDB provides the `add_user.sh` script in the installation package. After installing and running KWDB, you can execute this script to create database users and passwords, then use the credentials to log into the database.

::: tip

- To create multiple users, execute the `add_user.sh` script multiple times.
- If the installation user is root or a regular user configured with passwordless `sudo`, no password input is required when executing the script. Regular users without passwordless `sudo` configuration must enter a password for privilege escalation.

:::

## Prerequisites

- KWDB is installed and running.
- You have access to the `kwdb_install` directory.

## Steps

1. Navigate to the installation directory.

   ```shell
   cd kwdb_install
   ```

2. Run the user creation script.

    ```shell
    ./add_user.sh
    ```

3. Follow the system prompts to create a username and password.

    ```shell
    Please enter the username:
    Please enter the password:
    ```

    Upon successful execution, the following message will appear in the console:

    ```shell
    [ADD USER COMPLETED]:User creation completed.
    ```

## Using kwbase CLI

### Prerequisites

- KWDB is installed and running

### Steps

1. Navigate to the kwbase CLI directory and use the appropriate command based on your deployment method to create users and grant administrator privileges:

   - **Deployment using kwbase CLI:**

        - Insecure mode (without password):

            ```bash
            ./kwbase sql --host=127.0.0.1:$(local_port) --insecure \
            -e "create user $username; \
                grant admin to $username with admin option;"
            ```

        - Secure mode (with password):

            ```bash
            ./kwbase sql --certs-dir=$cert_path --host=127.0.0.1:$(local_port) \
            -e "create user $username with password \"$user_password\"; \
                grant admin to $username with admin option;"
            ```

    - **Deployment using Docker:**

        - Insecure mode (without password):

            ```bash
            docker exec kaiwudb-container bash -c "./kwbase sql --insecure --host=$host_ip -e \"create user $username;grant admin to $username with admin option;\""
            ```

        - Secure mode (with password):

            ```bash
            docker exec kaiwudb-container bash -c "./kwbase sql --host=$host_ip --certs-dir=$cert_path -e \"create user $username with password \\\"$user_password\\\";grant admin to $username with admin option;\""
            ```