---
title: 权限管理
id: privilege-mgmt
---

# 权限管理

KWDB 支持对数据库和表在内的数据库对象的访问和操作权限进行管理，从而确保数据库安全性。下表列出 KWDB 支持的权限。

| 权限   | 说明                          | 操作对象                                                            |
|--------|-----------------------------|---------------------------------------------------------------------|
| ALL    | 对指定数据库对象执行所有操作。 | - DATABASE <br >- TABLE <br >- SCHEMA（只适用于关系数据的自定义模式） |
| CREATE | 创建新对象。                   | - DATABASE <br >- TABLE <br >- SCHEMA（只适用于关系数据的自定义模式） |
| DROP   | 删除指定对象。                 | - DATABASE <br >- TABLE <br >- SCHEMA（只适用于关系数据的自定义模式） |
| GRANT  | 授予指定用户特定权限。         | - DATABASE <br >- TABLE <br >- SCHEMA（只适用于关系数据的自定义模式） |
| SELECT | 对指定数据表执行查询操作。     | TABLE                                                               |
| INSERT | 对指定数据表执行数据插入操作。 | TABLE                                                               |
| DELETE | 删除指定数据表。               | TABLE                                                               |
| UPDATE | 更新指定数据表。               | TABLE                                                               |

## 授予权限

授予权限的用户在目标数据库、表或模式（只适用于关系数据自定义模式）上具备被授予的权限。例如，向其他用户授予目标表的 `SELECT` 权限的用户必须具备目标表的 `GRANT` 和 `SELECT` 权限。

### 前提条件

用户拥有 Admin（ALL）权限。

### 语法格式

```shell
GRANT <privilege> ON [TABLE | DATABASE | SCHEMA] <target_name> To <user_name>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `privilege` | 权限名称。支持同时授予多个权限，权限名称之间使用逗号（`,`）隔开。支持使用 `ALL` 表示授予所有权限。 |
| `target_name` | 目标对象名称。支持同时向多个目标对象授予权限，目标对象名称之间使用逗号（`,`）隔开。 |
| `user_name` | 用户或角色名称，支持同时向多个用户或角色授予权限，用户或角色名称之间使用逗号（`,`）隔开。 |

### 语法示例

以下示例授予 `operatora` 用户 `db1` 和 `defaultdb` 数据库的创建权限。

```sql
GRANT CREATE ON DATABASE db1, defaultdb TO operatora;
```

## 撤销权限

权限撤销指移除用户或角色的特定权限，限制其对数据库对象的操作。撤销权限时，可以指定多个用户或角色，也可以针对多个目标对象进行配置。

### 前提条件

撤销其他用户的权限的用户具备目标数据库、表或模式（只适用于关系数据自定义模式）的 `GRANT` 权限和被撤销的权限。例如，撤销其他用户目标表的 `SELECT` 权限的用户必须具备目标表的 `GRANT` 和 `SELECT` 权限。

### 语法格式

```shell
REVOKE <privilege> ON [TABLE | DATABASE | SCHEMA] <target_name> FROM <user_name>;
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `privilege` | 权限名称。支持同时撤销多个权限，权限名称之间使用逗号（`,`）隔开。支持使用 `ALL` 表示授予所有权限。 |
| `target_name` | 目标对象名称。支持同时撤销多个目标对象的权限，目标对象名称之间使用逗号（`,`）隔开。 |
| `user_name` | 用户或角色名称，支持同时撤销多个用户或角色的权限，用户或角色名称之间使用逗号（`,`）隔开。 |

### 语法示例

- 撤销用户特定数据库的创建权限。

    以下示例撤销 `user11` 用户 `db1` 和 `defaultdb` 数据库的创建权限。

    ```sql
    REVOKE CREATE ON DATABASE db1, defaultdb FROM user11;
    ```

- 撤销用户指定表的删除权限。

    以下示例撤销 `user11` 用户 `defaultdb` 数据库中 `t1` 数据表的删除权限。

    ```sql
    REVOKE DELETE ON TABLE defaultdb.t1 FROM user11;
    ```

## 查看权限

查询权限指查看当前数据库中用户或角色的权限分配情况，帮助管理员了解和管理权限配置。

### 前提条件

无。如需使用 `SHOW GRANTS ON ROLE` SQL 命令，用户必须具备系统表的 `SELECT` 权限。

### 语法格式

```shell
SHOW GRANTS [ON [ROLE | DATABASE | SCHEMA | TABLE] <name> [For <user_name>]];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `name` | 目标对象名称。支持同时查看多个目标对象的权限，目标对象名称之间使用逗号（`,`）隔开。 |
| `user_name` | 可选参数，用户或角色名称，支持同时查看多个用户或角色的权限，用户或角色名称之间使用逗号（`,`）隔开。 |

### 语法示例

- 查看数据表与用户的权限关系。

    以下示例查看 `defaultdb` 数据库中 `t1` 表的用户权限的分配情况。

    ```sql
    SHOW GRANTS ON TABLE defaultdb.t1;
    ```

    执行成功后，命令行输出以下信息：

    ```sql
    database_name|schema_name|table_name|grantee|privilege_type
    -------------+-----------+----------+-------+--------------
    defaultdb    |public     |t1        |admin  |ALL
    defaultdb    |public     |t1        |root   |ALL
    defaultdb    |public     |t1        |user11 |DELETE
    (3 rows)
    ```

- 查看数据库与用户的权限关系。

    以下示例查看 `defaultdb` 数据库的用户权限的分配情况。

    ```sql
    SHOW GRANTS ON DATABASE defaultdb;
    ```

    执行成功后，命令行输出以下信息：

    ```sql
    database_name|schema_name         |grantee|privilege_type
    -------------+------------------+-------+--------------
    defaultdb    |information_schema|admin  |ALL
    defaultdb    |information_schema|root   |ALL
    defaultdb    |information_schema|user11 |CREATE
    (3 rows)
    ```

- 查看所有权限。

    ```sql
    SHOW GRANTS;
    ```
