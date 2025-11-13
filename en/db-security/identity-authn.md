---
title: Authentication
id: identity-authn
---

# Authentication

## Password-based Authentication

The password-based authentication is the most common authentication method. With this authentication method, each user is provided with a unique password to ensure only authorized users can access the KWDB database.

### Set Passwords for Users

The `CREATE USER` statement creates a user and sets a password for the user. KWDB supports setting the expiration time for the password to enhance database security.

#### Privileges

The user must have the `CREATEROLE` option or be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

#### Syntax

```sql
CREATE USER <name> WITH PASSWORD '<password>' [VALID UNTIL '<time>'];
```

#### Parameters

| Parameter | Description |
| --- | --- |
| `name` | The name of the user to create. The username is case-insensitive and follows these rules: <br> - Start with a letter or an underscore (`_`). <br >- Contain letters, numbers, or underscore (`_`). <br>- Must be 1 - 63 characters in length.|
| `password` | Set the password for the user. The user with this option can access to a secure cluster with the password. The password should be entered as a string literal, enclosed in single quotes (`' '`).|
| `time` | Set the expiration time (in the `timestamp` format) after which the password is not valid. It is enclosed in single quotes (`' '`). |

#### Examples

This example creates a user and sets the password and expiration time for the user.

```sql
CREATE USER user1 WITH PASSWORD '11aa!!AA' VALID UNTIL '2025-01-01 00:00:00+00:00';
```

### Modify Passwords for Users

The `ALTER USER` statement changes the password for a user. Each statement changes only one user.

#### Privileges

The user must have the `CREATEROLE` option or be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

#### Syntax

```sql
ALTER USER [IF EXISTS] <name> WITH [ PASSWORD '<password>' | VALID UNTIL '<time>'];
```

#### Parameters

| Parameter | Description |
| --- | --- |
| `IF EXISTS` | Optional. <br>- When the `IF EXISTS` keyword is used, the system changes a user only if the target user has already existed. Otherwise, the system fails to change the user without returning an error. <br>- When the `IF EXISTS` keyword is not used, the system changes a user only if the target user has already existed. Otherwise, the system fails to change the user and returns an error. |
| `name` | The name of the user to change. The username is case-insensitive and follows these rules: <br> - Start with a letter or an underscore (`_`). <br >- Contain letters, numbers, or underscore (`_`). <br>- Must be 1 - 63 characters in length.|
| `password` | Set the password for the user. The user with this option can access to a secure cluster with the password. The password should be entered as a string literal, enclosed in single quotes (`' '`).|
| `time` | Set the expiration time (in the `timestamp` format) after which the password is not valid. It is enclosed in single quotes (`' '`). |

#### Examples

This example changes the password and expiration time for a user.

```sql
ALTER USER user1 WITH PASSWORD 'PassWord4Deomo' VALID UNTIL '2025-12-31';
```

## Host-based Authentication

KWDB provides host-based authentication to control user access. The authentication rule format is compatible with PostgreSQL's `pg_hba.conf` configuration. You can set authentication rules using the `server.host_based_authentication.configuration` cluster parameter.

### Privileges

The user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

### Syntax

```shell
SET CLUSTER SETTING server.host_based_authentication.configuration = 'host all <user_name> <address> <method>';
```

### Parameters

| Parameter | Description |
| --- | --- |
| `user_name` | Specify the username to connect to the KWDB. When it is set to `all`, it means allowing all users to connect. |
| `address` | Specify the allowed or rejected IP address range. Available options: <br>- `all`: all IP addresses. <br>- A signle IP address: such as `192.168.1.100`<br>- An IP address with a CIDR mask length, such as `192.168.1.0/24`<br>- An IP address with a subnet mask, such as `192.168.1.0 255.255.255.0`|
| `method` | Authentication methods to specify how to authenticate the clients. Available options: <br >- `cert`: Certificate-based authentication (SSL connection required)<br >- `cert-password`: Certificate-based and password-based authentication (SSL connection required) <br >- `password`: Password-based authentication (SSL connection required) <br >- `trust`: Allow all matched connections. <br >- `reject`: Reject all matched connections.|

### Examples

- Reject the user with the specific IP address to connect to the KWDB database.

    This example rejects any user from the host `10.xxx.xxx.2` to connect to any database.

    ```sql
    SET CLUSTER SETTING server.host_based_authentication.configuration = 'host all all 10.xxx.xxx.2 reject';
    ```

- Allow the user to connect to the KWDB database using a certificate.
  
    This example allows the `testuser` user from host `0.0.0.0/0` to connect to any database if the user's certificate is correctly supplied.

    ```sql
    SET CLUSTER SETTING server.host_based_authentication.configuration = 'host all testuser 0.0.0.0/0 cert';
    ```
