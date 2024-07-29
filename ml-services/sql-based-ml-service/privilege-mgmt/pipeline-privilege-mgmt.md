---
title: 训练流水线权限管理
id: pipeline-privilege-mgmt
---

# 训练流水线权限管理

下表列出训练流水线支持的权限和操作。

| 权限   | 操作说明       |
| ------ | -------------- |
| ALL    | 所有权限。       |
| DELETE | 删除训练流水线。 |
| SELECT | 查看训练流水线。 |
| TRAIN  | 训练模型。       |

默认情况下，系统管理员（Admin）拥有所有训练流水线的 ALL 权限。训练流水线所有者（Owner）拥有其导入流水线的 ALL 权限。

系统管理员和训练流水线所有者可以将训练流水线权限授予某个用户或者角色，但是授权用户无法将其拥有的权限转授给其他用户。

## 为训练流水线授权

### 前提条件

- 已经将训练流水线导入到数据库中。
- 用户为 Admin 用户或者训练流水线的创建者。

### 语法格式

```sql
SELECT kwdbml.grant_privilege_on_training_pipeline(<pipeline_name>, [<user_name> | <role_name>], <privilege>);
```

### 参数说明

| 参数          | 类型   | 描述                                                                                    |
| ------------- | ------ | --------------------------------------------------------------------------------------- |
| `pipeline_name` | STRING | 训练流水线的名称。支持两级结构名称：模式名.对象名。如未指定前缀模式名，默认使用当前模式。 |
| `user_name`  | STRING | 待授予训练流水线权限的用户名。取值为 `syspublic` 表示所有用户。                                         |
| `role_name`  | STRING | 待授予训练流水线权限的角色名。                                                                  |
| `privilege`  | STRING | 权限选项，支持指定一个或多个权限。多个权限选项之间使用管道符号（&#124;）隔开。<br >- SELECT <br >- DELETE <br >- TRAIN <br >- ALL |

### 返回字段说明

| 参数                            | 类型   | 描述             |
| ------------------------------- | ------ | ---------------- |
| `kwdbml.grant_privilege_on_pipeline` | STRING | 待授予训练流水线权限的用户。 |

### 语法示例

```sql
SELECT kwdbml.grant_privilege_on_training_pipeline('DEMP.PowerGen', 'jerry', 'train');
```

执行成功后，控制台输出以下信息：

```sql
kwdbml.grant_privilege_on_pipeline
+--------------------------------------------+
jerry
```

## 撤销训练流水线的授权

### 前提条件

用户为 Admin 用户或者训练流水线的创建者。

### 语法格式

```sql
SELECT kwdbml.revoke_privilege_on_training_pipeline (<pipeline_name>, [<user_name> | <role_name>], <privilege>);
```

### 参数说明

| 参数          | 类型   | 描述                                                                                    |
| ------------- | ------ | --------------------------------------------------------------------------------------- |
| `pipeline_name` | STRING | 训练流水线的名称。支持两级结构名称：模式名.对象名。如未指定前缀模式名，默认使用当前模式。 |
| `user_name`  | STRING | 待撤销训练流水线权限的用户名。取值为 `syspublic` 表示所有用户。                                         |
| `role_name`  | STRING | 待撤销训练流水线权限的角色名。                                                                  |
| `privilege`  | STRING | 权限选项，支持指定一个或多个权限。多个权限选项之间使用管道符号（&#124;）隔开。<br >- SELECT <br >- DELETE <br >- TRAIN <br >- ALL |

### 返回字段说明

| 参数                                | 类型   | 描述                     |
| ----------------------------------- | ------ | ------------------------ |
| `kwdbml.revoke_privilege_on_pipeline` | STRING | 撤销训练流水线权限的用户。 |

### 语法示例

```sql
SELECT kwdbml.remvoke_privilege_on_training_pipeline('DEMP.PowerGen', 'jerry', 'train');
```

执行成功后，控制台输出以下信息：

```sql
kwdbml.revoke_privilege_on_pipeline
+--------------------------------------------+
jerry
```

## 查看训练流水线的权限

### 前提条件

用户为 Admin 用户、训练流水线的创建者、或者拥有训练流水线的任一权限。

### 语法格式

```sql
SELECT kwdbml.has_training_pipeline_privilege(<pipeline_name>, [<user_name> | <role_name>], <privilege>);
```

### 参数说明

| 参数          | 类型   | 描述                                                                                    |
| ------------- | ------ | --------------------------------------------------------------------------------------- |
| `pipeline_name` | STRING | 训练流水线的名称。支持两级结构名称：模式名.对象名。如未指定前缀模式名，默认使用当前模式。 |
| `user_name`  | STRING | 待查看训练流水线权限的用户名。取值为 `syspublic` 表示所有用户。                                         |
| `role_name`  | STRING | 待查看训练流水线权限的角色名。                                                                  |
| `privilege`  | STRING | 权限选项，支持指定一个或多个权限。多个权限选项之间使用管道符号（&#124;）隔开。<br >- SELECT <br >- DELETE <br >- TRAIN <br >- ALL |

### 返回字段说明

| 参数                                   | 类型    | 描述                                   |
| -------------------------------------- | ------- | -------------------------------------- |
| `kwdbml.has_training_pipeline_privilege` | Boolean | 对于指定流水线，用户是否具有指定权限。 |

### 语法示例

```sql
SELECT kwdbml.has_training_pipeline_privilege('PowerGen_pipeline','user01','ALL');
```

执行成功后，控制台输出以下信息：

```sql
kwdbml.has_training_pipeline_privilege
+-------------------------------------------+
false
```
