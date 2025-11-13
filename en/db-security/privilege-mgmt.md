---
title: Privilege Management
id: privilege-mgmt
---

# Privilege Management

KWDB supports managing privileges on objects within a database to ensure database security. This table lists all privileges supported by KWDB.

| Privilege  |    Description  | Object                                                             |
|--------|-----------------------------|---------------------------------------------------------------------|
| ALL    | Perform all operations on the specified object(s). | - DATABASE <br >- TABLE <br >- SCHEMA (only for user-defined schema of relational databases) <br>- PROCEDURE|
| CREATE | Create one or more objects.                   | - DATABASE <br >- TABLE <br >- SCHEMA (only for user-defined schema of relational databases)<br>- PROCEDURE |
| DROP   | Remove the specified object(s).                 | - DATABASE <br >- TABLE <br >- SCHEMA (only for user-defined schema of relational databases)<br>- PROCEDURE |
| GRANT  | Grant privileges to the specific user(s).        | - DATABASE <br >- TABLE <br >- SCHEMA (only for user-defined schema of relational databases) <br>- PROCEDURE |
| SELECT | Query data from the specified table(s).     | TABLE                                                               |
| INSERT | Insert data into the specified table(s). | TABLE                                                               |
| DELETE | Remove the specified table(s).             | TABLE                                                               |
| UPDATE | Update the specified table(s).               | TABLE                                                               |

## GRANT {privilege}

The `GRANT <privilege>` statement grants privileges on the specified objects to one or more users/roles.

::: warning Note
If the privileges of a user are not updated on time, you can remove the user and then create a new user with a different name and re-grant privileges to the new user.
:::

### Privileges

The user granting the privileges must also have the `GRANT` privilege on the specified database(s), table(s), column(s) or schema(s) (only for user-defined schema of relational databases). For example, a user granting the `SELECT` privilege on a table to another user must have the `GRANT` and `SELECT` privileges on that table.

### Syntax

```shell
GRANT <privilege> ON [TABLE | DATABASE | SCHEMA] <target_name> To <user_name>;
```

### Parameters

| Parameter     | Description                                                                                             |
|---------------|---------------------------------------------------------------------------------------------------------|
| `privilege`   | A comma-separated list of privileges to grant. The privileges to grant depend on the objects. <br> If it is set to `ALL`, it means to grant all privileges. |
| `target_name` | A comma-separated list of object names to grant privileges on.                                         |
| `user_name`   | A comma-separated list of role or user names to grant privileges to.                                    |

### Examples

This example grants the C privilege to create the `db1` and `defaultdb` databases to `operatora` user.

```sql
GRANT CREATE ON DATABASE db1, defaultdb TO operatora;
```

## REVOKE {privilege}

The `REVOKE <privilege>` statement revokes privileges on the specified objects from one or more users/roles.

### Privileges

The user revoking the privileges must also have the `GRANT` privilege on the specified database(s), table(s), column(s) or schema(s) (only for user-defined schema of relational databases). For example, a user revoking the `SELECT` privilege on a table from another user must have the `GRANT` and `SELECT` privileges on that table.

### Syntax

```shell
REVOKE <privilege> ON [TABLE | DATABASE | SCHEMA] <target_name> FROM <user_name>;
```

### Parameters

| Parameter     | Description                                                                                               |
|---------------|-----------------------------------------------------------------------------------------------------------|
| `privilege`   | A comma-separated list of privileges to revoke. The privileges to revoke depend on the objects. <br>If it is set to `ALL`, it means to revoke all privileges. |
| `target_name` | A comma-separated list of object names to revoke privileges from.                                        |
| `user_name`   | A comma-separated list of role or user names to revoke privileges from.                                   |

### Examples

- Revoke the privilege to create databases from the specified user(s).

    This example revokes the `CREATE` privilege to create the `db1` and `defaultdb` databases from `user11` user.

    ```sql
    REVOKE CREATE ON DATABASE db1, defaultdb FROM user11;
    ```

- Revoke the privilege to drop tables from the specified user(s).

    This example revokes the `DELETE` privilege to drop the `t1` table of the `defaultdb` database from `user11` user.

    ```sql
    REVOKE DELETE ON TABLE defaultdb.t1 FROM user11;
    ```

## SHOW GRANTS

The `SHOW GRANTS` statement lists the privileges granted to users on databases, tables, or user-defined schemas (only for user-defined schema of relational databases).

### Privileges

N/A. To run the `SHOW GRANTS ON ROLE` command, the user must have been granted the `SELECT` privilege on the system table.

### Syntax

```shell
SHOW GRANTS [ON [ROLE | DATABASE | SCHEMA | TABLE] <name> [For <user_name>]];
```

### Parameters

| Parameter   | Description                                                                |
|-------------|----------------------------------------------------------------------------|
| `name`      | A comma-separated list of object names to show privileges.                |
| `user_name` | Optional. A comma-separated list of role or user names to show privileges. |

### Examples

- Show privileges granted to users on the specified table(s).

    This example shows grants on the `defaultdb.t1` table.

    ```sql
    SHOW GRANTS ON TABLE defaultdb.t1;
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
    database_name|schema_name|table_name|grantee|privilege_type
    -------------+-----------+----------+-------+--------------
    defaultdb    |public     |t1        |admin  |ALL
    defaultdb    |public     |t1        |root   |ALL
    defaultdb    |public     |t1        |user11 |DELETE
    (3 rows)
    ```

- Show privileges granted to users on the specified database(s).

    This example shows grants on the `defaultdb` database.

    ```sql
    SHOW GRANTS ON DATABASE defaultdb;
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
    database_name|schema_name         |grantee|privilege_type
    -------------+------------------+-------+--------------
    defaultdb    |information_schema|admin  |ALL
    defaultdb    |information_schema|root   |ALL
    defaultdb    |information_schema|user11 |CREATE
    (3 rows)
    ```

- Show all privileges.

    ```sql
    SHOW GRANTS;
    ```
