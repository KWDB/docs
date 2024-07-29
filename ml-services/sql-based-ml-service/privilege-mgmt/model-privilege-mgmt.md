---
title: 模型权限管理
id: model-privilege-mgmt
---

# 模型权限管理

下表列出模型支持的权限和操作。

| 权限     | 操作说明         |
| -------- | ---------------- |
| ALL      | 所有权限。         |
| SELECT   | 查看模型。         |
| UPDATE   | 设置模型的活跃版本。 |
| DELETE   | 删除模型。         |
| EVALUATE | 评估模型。         |
| PREDICT  | 在线预测。         |

默认情况下，系统管理员（Admin）拥有所有模型的 ALL 权限。模型所有者（Owner）拥有其导入模型的 ALL 权限。

系统管理员和模型所有者可以将模型权限授予某个用户或者角色，但是授权用户无法将其拥有的权限转授给其他用户。

## 为模型授权

### 前提条件

- 已经将模型导入到数据库中。
- 用户为 KWDB 数据库用户。

### 语法格式

```sql
SELECT kwdbml.grant_privilege_on_model(<model_name>, [<user_name>|<role_name>], <privilege>);
```

### 参数说明

| 参数       | 类型   | 描述                                                                                  |
| ---------- | ------ | ------------------------------------------------------------------------------------- |
| `model_name`    | STRING | 模型的名称。支持两级结构名称：模式名.对象名。如未指定前缀模式名，默认使用当前模式。 |
| `user_name`  | STRING | 待授予模型权限的用户名。取值为 `syspublic` 表示所有用户。                                         |
| `role_name`  | STRING | 待授予模型权限的角色名。                                                                  |
| `privilege`  | STRING | 权限选项，支持指定一个或多个权限。多个权限选项之间使用管道符号（&#124;）隔开。<br >- SELECT <br >- UPDATE（设置活跃版本）<br >- DELETE <br >- PREDICT <br >- EVALUATE <br >- ALL |

### 返回字段说明

| 参数                            | 类型   | 描述             |
| ------------------------------- | ------ | ---------------- |
| `kwdbml.grant_privilege_on_model` | STRING | 授予权限的用户。 |

### 语法示例

```sql
SELECT kwdbml.grant_privilege_on_model('Tom.PowerGen', 'jerry', 'delete');
```

执行成功后，控制台输出以下信息：

```sql
kwdbml.grant_privilege_on_model
+------------------------------+ 
jerry
```

## 撤销模型授权

### 前提条件

- 已经将模型导入到数据库中。
- 用户为 Admin 用户或者模型的创建者。

### 语法格式

```sql
SELECT kwdbml.revoke_privilege_on_model(<model_name>, [<user_name>|<role_name>], <privilege>);
```

### 参数说明

| 参数       | 类型   | 描述                                                                                  |
| ---------- | ------ | ------------------------------------------------------------------------------------- |
| `model_name`    | STRING | 模型的名称。支持两级结构名称：模式名.对象名。如未指定前缀模式名，默认使用当前模式。 |
| `user_name`  | STRING | 待撤销模型权限的用户名。取值为 `syspublic` 表示所有用户。                                         |
| `role_name`  | STRING | 待撤销模型权限的角色名。                                                                  |
| `privilege`  | STRING | 权限选项，支持指定一个或多个权限。多个权限选项之间使用管道符号（&#124;）隔开。<br >- SELECT <br >- UPDATE（设置活跃版本）<br >- DELETE <br >- PREDICT <br >- EVALUATE <br >- ALL |

### 返回字段说明

| 参数                             | 类型   | 描述               |
| -------------------------------- | ------ | ------------------ |
| `kwdbml.revoke_privilege_on_model` | STRING | 撤销模型权限的用户。 |

### 语法示例

```sql
SELECT kwdbml.revoke_privilege_on_model('Tom.PowerGen', 'jerry','delete');
```

执行成功后，控制台输出以下信息：

```sql
kwdbml.revoke_privilege_on_model
+-------------------------------+
jerry
```

## 查看模型权限

### 前提条件

用户为 Admin 用户、模型的创建者、或者拥有模型的任一权限。

### 语法格式

```sql
SELECT kwdbml.has_model_privilege(<model_name>, [<user_name>|<role_name>], <privilege>);
```

### 参数说明

| 参数       | 类型   | 描述                                                                                  |
| ---------- | ------ | ------------------------------------------------------------------------------------- |
| `model_name`    | STRING | 模型的名称。支持两级结构名称：模式名.对象名。如未指定前缀模式名，默认使用当前模式。 |
| `user_name`  | STRING | 待查看模型权限的用户名。取值为 `syspublic` 表示所有用户。                                         |
| `role_name`  | STRING | 待查看模型权限的角色名。                                                                  |
| `privilege`  | STRING | 权限选项，支持指定一个或多个权限。多个权限选项之间使用管道符号（&#124;）隔开。<br >- SELECT <br >- UPDATE（设置活跃版本）<br >- DELETE <br >- PREDICT <br >- EVALUATE <br >- ALL |

### 返回字段说明

| 参数                       | 类型    | 描述                               |
| -------------------------- | ------- | ---------------------------------- |
| `kwdbml.has_model_privilege` | Boolean | 对于指定模型，用户是否具有指定权限。 |

### 语法示例

```sql
SELECT kwdbml.has_model_privilege('Tom.PowerGen','user01','SELECT|UPDATE');
```

执行成功后，控制台输出以下信息：

```sql
kwdbml.has_model_privilege
+-------------------------+
true
```
