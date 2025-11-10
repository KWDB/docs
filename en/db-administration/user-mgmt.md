---
title: User Management
id: user-mgmt
---

# User Management

KWDB supports user permission management to ensure the security of critical and important functions and data. In addition, KWDB also supports customized management permissions for users.

## Create Users

The `CREATE USER` statement creates a user and sets one or more options for the user, such as creating a role and setting a login password. By default, the new user has the login option. Each statement creates only one user.

### Prerequisites

The user must have the `CREATEROLE` option or be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

### Syntax

```sql
CREATE USER [IF NOT EXISTS] <name> [WITH] [CREATEROLE | NOCREATEROLE | LOGIN | NOLOGIN | <password_clause> | <valid_until_clause>];
```

### Parameters

| Parameter | Description |
| --- | --- |
| `IF NOT EXISTS` | Optional keyword. When the `IF NOT EXISTS` keyword is used, if the target user does not exist, the system creates the target user. If the target user exists, the system fails to create the user but does not return an error. When the `IF NOT EXISTS` keyword is not used, if the target user does not exist, the system creates the user. If the target user exists, the system returns an error indicating that the target user already exists. |
| `name` | The name of the user to create. The username is case-insensitive, must start with a letter or an underscore (`_`), can only contain letters, numbers, or underscores (`_`), and must be 1 - 63 characters in length.|
| `CREATEROLE` | Create role. Users with this option can create, modify, and delete other users or roles. By default, this option is not set when creating a user. |
| `NOCREATEROLE` | The default option when creating a user, indicating that creating roles is prohibited.|
| `LOGIN` | The default option when creating a user, indicating that the user can log in to the KWDB server.|
| `NOLOGIN` | Prohibit login to the KWDB server. By default, this option is not set when creating a user.|
| `password_clause` | Set the user password. The format is `PASSWORD <string_or_placeholder>`, and it also supports using `NULL` values. Users with this option can securely access nodes using a password. The password must be in string form and enclosed in single quotes (`'`). By default, this option is not set when creating a user.|
| `valid_until_clause` | Set the password expiration date. The format is `VALID UNTIL <string_or_placeholder>`, and it also supports using `NULL` values. It supports timestamp format. After reaching the specified date or time, the password becomes invalid. When setting this, you need to enclose the password expiration date in single quotes (`'`). By default, this option is not set when creating a user.|

### Examples

- Create a user.

    The following example creates user `user1`. By default, this user cannot create roles but can log in to the KWDB server.

    ```sql
    CREATE USER user1;
    CREATE USER
    ```

- Create a user and grant the user permission to create roles.

    The following example creates user `user2` and grants the user permission to create roles.

    ```sql
    CREATE USER user2 WITH CREATEROLE;
    CREATE USER
    ```

- Create a user and prohibit the user from logging in to the KWDB server.

    The following example creates user `user3` and prohibits the user from logging in to the KWDB server.

    ```sql
    CREATE USER user3 WITH NOLOGIN;
    CREATE USER
    ```

- Create a user and set the password and password expiration date for the user.

    The following example creates user `user4` and sets the login password and password expiration date for the KWDB server.

    ```sql
    CREATE USER user4 WITH PASSWORD '11aa!!AA' VALID UNTIL '2023-01-01 00:00:00+00:00';
    CREATE USER
    ```

## Show Users

The `SHOW USERS` or `SHOW ROLES` statement queries user information in the database.

### Prerequisites

The user must have the `SELECT` privilege on the `system.users` and `system.role_members` tables.

### Syntax

```sql
SHOW USERS;
```

or

```sql
SHOW ROLES;
```

### Parameters

N/A

### Examples

```sql
SHOW USERS;
```

If you succeed, the console outputs the following information:

```sql
username|options                              |member_of
--------+-------------------------------------+---------
admin   |CREATEROLE                           |{}
root    |CREATEROLE                           |{admin}
user1   |CREATEROLE                           |{}
user2   |CREATEROLE                           |{}
user3   |VALID UNTIL=2023-01-01 00:00:00+00:00|{}
```

## Alter Users

The `ALTER USER` statement modifies a user.

### Prerequisites

- The user must have the `CREATEROLE` option or be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.
- Log in to the KWDB database in secure mode.

### Syntax

```sql
ALTER USER [IF EXISTS] <name> [WITH] [CREATEROLE | NOCREATEROLE | LOGIN | NOLOGIN | <password_clause> | <valid_until_clause>];
```

### Parameters

| Parameter | Description |
| --- | --- |
| `IF EXISTS` | Optional keyword. When the `IF EXISTS` keyword is used, if the target user exists, the system modifies the target user. If the target user does not exist, the system fails to modify the user but does not return an error. When the `IF EXISTS` keyword is not used, if the target user exists, the system modifies the user. If the target user does not exist, the system returns an error indicating that the target user does not exist. |
| `name` | The name of the user to modify. The username is case-insensitive, must start with a letter or an underscore (`_`), can only contain letters, numbers, or underscores (`_`), and must be 1 - 63 characters in length.|
| `CREATEROLE` | Create role. Users with this option can create, modify, and delete other users or roles. By default, this option is not set when creating a user. |
| `NOCREATEROLE` | The default option when creating a user, indicating that creating roles is prohibited.|
| `LOGIN` | The default option when creating a user, indicating that the user can log in to the KWDB server.|
| `NOLOGIN` | Prohibit login to the KWDB server. By default, this option is not set when creating a user.|
| `password_clause` | Set the user password. The format is `PASSWORD <string_or_placeholder>`, and it also supports using `NULL` values. Users with this option can securely access nodes using a password. The password must be in string form and enclosed in single quotes (`'`). By default, this option is not set when creating a user.|
| `valid_until_clause` | Set the password expiration date. The format is `VALID UNTIL <string_or_placeholder>`, and it also supports using `NULL` values. It supports timestamp format. After reaching the specified date or time, the password becomes invalid. When setting this, you need to enclose the password expiration date in single quotes (`'`). By default, this option is not set when creating a user.|

### Examples

The following example modifies the password and password expiration date for user `user4`.

```sql
-- 1. Modify the password and password expiration date for user4.

ALTER USER user4 WITH PASSWORD '11aa!!AA' VALID UNTIL '2023-01-01 00:00:00+00:00';
ALTER USER

-- 2. View user information.

SHOW USERS;
  username |                    options                     | member_of
-----------+------------------------------------------------+------------
  admin    | CREATEROLE                                     | {}
  root     | CREATEROLE                                     | {admin}
  user1    |                                                | {}
  user2    |                                                | {}
  user3    | NOLOGIN, VALID UNTIL=2023-12-31 00:00:00+00:00 | {}
  user4    | VALID UNTIL=2023-01-01 00:00:00+00:00          | {}
(6 rows)
```

## Drop Users

The `DROP USER` statement deletes a user.

### Prerequisites

The user must have the `CREATEROLE` option or be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

### Syntax

```sql
DROP USER [IF EXISTS] <name>;
```

### Parameters

| Parameter | Description |
| --- | --- |
| `name` | The name of the user to delete. Supports deleting multiple users at once.|

### Examples

The following example deletes user `user1`.

```sql
DROP USER user1;
```