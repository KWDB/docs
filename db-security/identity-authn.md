---
title: 身份鉴别
id: identity-authn
---

# 身份鉴别

## 基于用户名和密码的身份鉴别

基于用户名和密码的身份鉴别是 KWDB 最基本的身份验证方式。使用此方法时，KWDB 在用户登录数据库时验证其提供的用户名和密码是否匹配。

### 设置用户密码

`CREATE USER` 语句用于创建用户并为用户设置密码。KWDB 支持为每个用户设置密码的有效期，以增强安全性。

#### 前提条件

用户拥有 Admin（ALL）权限或者具有创建角色（CREATEROLE）的权限。

#### 语法格式

```sql
CREATE USER <name> WITH PASSWORD '<password>' [VALID UNTIL '<time>'];
```

#### 参数说明

| 参数 | 说明 |
| --- | --- |
| `name` | 待创建的用户名。用户名不区分大小写，必须以字母或下划线（`_`）开头，只支持字母，数字或下划线（`_`），长度为 1 - 63 个字符。|
| `password` | 设置用户密码。设置该选项的用户可以使用密码安全访问节点。密码必须采用字符串的形式，并使用单引号（`'`）将密码括起来。|
|  `time` | 可选参数，设置密码有效期。支持 timestamp 格式。到达指定日期或时间后，密码失效。设置时需使用单引号（`'`）将密码有效期括起来。|

#### 语法示例

以下示例创建 `user1` 用户，并为用户设置密码和密码有效期。

```sql
CREATE USER user1 WITH PASSWORD '11aa!!AA' VALID UNTIL '2025-01-01 00:00:00+00:00';
```

### 修改用户密码

`ALTER USER` 语句用于更改一个或多个用户选项，如更改用户登录密码等。每条语句只支持更改一个用户。

#### 前提条件

用户拥有 Admin（ALL）权限或者具有创建角色（CREATEROLE）的权限。

#### 语法格式

```sql
ALTER USER [IF EXISTS] <name> WITH [ PASSWORD '<password>' | VALID UNTIL '<time>'];
```

#### 参数说明

| 参数 | 说明 |
| --- | --- |
| `IF  EXISTS` | 可选关键字。当使用 `IF EXISTS` 关键字时，如果目标用户存在，系统修改目标用户。如果目标用户不存在，系统修改用户失败，但不会报错。当未使用 `IF EXISTS` 关键字时，如果目标用户存在，系统修改用户。如果目标用户不存在，系统报错，提示目标用户不存在。 |
| `name` | 待修改的用户名。用户名不区分大小写，必须以字母或下划线（`_`）开头，只支持字母，数字或下划线（`_`），长度为 1 - 63 个字符。|
| `password` | 设置用户密码。密码必须采用字符串的形式，并使用单引号（`'`）将密码括起来。|
|  `time` | 设置密码有效期。支持 timestamp 格式。设置时需使用单引号（`'`）将密码有效期括起来。|

#### 语法示例

以下示例修改 `user1` 用户的用户密码和密码的有效期。

```sql
ALTER USER user1 WITH PASSWORD 'PassWord4Deomo' VALID UNTIL '2025-12-31';
(6 rows)
```

## 基于主机的认证

KWDB 提供基于主机的认证配置，控制客户端的访问权限。认证规则格式兼容 PostgreSQL 的 `pg_hba.conf` 配置。用户可以使用 `server.host_based_authentication.configuration` 集群参数设置认证规则。

### 前提条件

用户拥有 Admin 权限。

### 语法格式

```shell
SET CLUSTER SETTING server.host_based_authentication.configuration = 'host all <user_name> <address> <method>';
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `user_name` | 用户名称。支持设置为 `all`，表示匹配所有用户。|
| `address` | 设置允许或拒绝访问的 IP 地址范围。如果字段值包含了 IP 地址及其掩码，则无需提供掩码值。如果字段值只包含了 IP 地址，则接下来的字段必须提供有效的 IP 掩码。支持设置为 `all`，表示允许或拒绝所有 IP 地址。|
|  `method` | 认证规则，用户可以根据需求定制认证规则，具体包括：<br >- `cert`：基于证书的身份验证（需要 SSL 连接）。<br >- `cert-password`：基于证书或密码的身份验证（需要 SSL 连接）。<br >- `password`：基于密码的身份验证（需要 SSL 连接）。<br >- `trust`：无条件允许匹配的连接。<br >- `reject`：无条件拒绝匹配的连接。|

### 语法示例

- 禁用特定 IP 地址的用户连接。

    以下示例拒绝使用 `10.xxx.xxx.2` 地址的 `all` 用户连接 KWDB 集群。

    ```sql
    SET CLUSTER SETTING server.host_based_authentication.configuration = 'host all all 10.xxx.xxx.2 reject';
    ```

- 允许用户使用证书连接。

    以下示例允许 `testuser` 使用证书连接 KWDB 集群。

    ```sql
    SET CLUSTER SETTING server.host_based_authentication.configuration = 'host all testuser 0.0.0.0/0 cert';
    ```
