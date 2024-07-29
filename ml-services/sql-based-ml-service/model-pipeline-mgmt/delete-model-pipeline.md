---
title: 删除模型和流水线
id: delete-model-pipeline
---

# 删除模型和流水线

## 删除模型

KWDB 支持删除指定模型的所有版本或者指定版本。

### 前提条件

- 已经将模型导入到数据库中。
- 用户为 Admin 用户、模型的创建者、或者拥有模型的 DELETE 权限。
- 待删除模型不是正在使用的模型。
- 如需删除模型的指定版本，该版本不是模型的当前活跃版本。

### 语法格式

```sql
SELECT kwdbml.remove_model(<model_name>[, <model_version>]);
```

### 参数说明

| 参数          | 类型   | 描述                                                                                  |
| ------------- | ------ | ------------------------------------------------------------------------------------- |
| `model_name`    | STRING | 模型的名称。支持两级结构名称：模式名.对象名。如未指定前缀模式名，默认使用当前模式。 |
| `model_version` | INT    | 可选参数，模型版本。如未指定，表示删除目标模型的所有版本。                                      |

### 返回字段说明

| 参数                | 类型   | 描述       |
| ------------------- | ------ | ---------- |
| `kwdbml.remove_model` | STRING | 模型的名称。 |

### 语法示例

- 删除指定模型的所有版本。

    ```sql
    SELECT kwdbml.remove_model('Tom.PowerGen');
    ```

    执行成功后，控制台输出以下信息：

    ```sql
    kwdbml.remove_model
    +-------------------+
    Tom.PowerGen 
    (1 row)
    ```

- 删除模型的指定版本。

    ```sql
    SELECT kwdbml.remove_model('Tom.PowerGen', 2);
    ```

    执行成功后，控制台输出以下信息：

    ```sql
    kwdbml.remove_model
    +-------------------+
    Tom.PowerGen 
    (1 row)
    ```

## 删除训练流水线

KWDB 支持删除指定训练流水线。

### 前提条件

- 已经将训练流水线导入到数据库中。
- 用户为 Admin 用户、训练流水线的创建者、或者拥有训练流水线的 DELETE 权限。
- 待删除的训练流水线不是正在使用的训练流水线。

### 语法格式

```sql
SELECT kwdbml.remove_training_pipeline(<pipeline_name>);
```

### 参数说明

| 参数          | 类型   | 描述                                                                                    |
| ------------- | ------ | --------------------------------------------------------------------------------------- |
| `pipeline_name` | STRING | 训练流水线的名称。支持两级结构名称：模式名.对象名。如未指定前缀模式名，默认使用当前模式。 |

### 返回字段说明

| 参数                            | 类型   | 描述             |
| ------------------------------- | ------ | ---------------- |
| `kwdbml.remove_training_pipeline` | STRING | 训练流水线的名称。  |

### 语法示例

以下示例删除 `DEMP.PowerGen` 训练流水线。

```sql
SELECT kwdbml.remove_training_pipeline('DEMP.PowerGen');
```

执行成功后，控制台输出以下信息：

```sql
kwdbml.remove_training_pipeline 
+------------------------+
DEMP.PowerGen
(1 row)
```
