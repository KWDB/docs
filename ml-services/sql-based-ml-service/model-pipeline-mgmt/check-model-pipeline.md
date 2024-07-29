---
title: 查看模型和流水线
id: check-model-pipeline
---

# 查看模型和流水线

## 查看所有模型

KWDB 支持查看所有模型的基本信息、版本号、最新的评估结果

### 前提条件

- 已经将模型导入到数据库中。
- 用户为 Admin 用户、模型的创建者、或者拥有模型的 SELECT 权限。

### 语法格式

```sql
SELECT * FROM kwdbml.show_models();
```

### 参数说明

无

### 返回字段说明

| 参数         | 类型      | 描述                                                     |
| ------------ | --------- | -------------------------------------------------------- |
| `schema`       | STRING    | 模型的模式名称。                                         |
| `name`         | STRING    | 模型的名称。                                             |
| `description`  | STRING    | 模型的描述信息。                                           |
| `creator`      | STRING    | 模型的创建者。                                         |
| `created`      | TIMESTAMP | 模型的创建时间。                                       |
| `problem_type` | STRING    | 模型的问题分类。                             |
| `features`     | JSON      | 模型的输入特征列信息，包括列名和数据类型。 |
| `target`       | JSON      | 模型的输出特征列信息，包括列名和数据类型。 |
| `framework`    | STRING    | 模型使用的机器学习框架类型及版本。           |
| `runtime`      | STRING    | 模型的运行环境及版本。                       |
| `active_version` | INT       | 模型的当前活跃版本。                         |
| `last_metrics`   | JSON      | 模型的最新评估结果。                       |
| `status`         | JSON      | 模型的状态。                                   |

### 语法示例

```sql
SELECT * FROM kwdbml.show_models();
```

执行成功后，控制台输出以下信息：

```sql
   schema  |    name               | description                                             | creator     | created                          | last_updated                     | problem_type | features                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | target                                | framework      | runtime     | active_version | last_metrics                                                                                                                  | status
 ----------+-----------------------+---------------------------------------------------------+-------------+----------------------------------+----------------------------------+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------+----------------+-------------+----------------+-------------------------------------------------------------------------------------------------------------------------------+----------------------  
    public | pipe_xgb_binary       | Model trained by pipeline public.pipe_xgb_binary.       | kwdbmlusr01 | 2024-05-20 03:11:27.156676+00:00 | 2024-05-20 03:11:27.156676+00:00 | b            | [{"name": "checking_status", "type": "string"}, {"name": "duration", "type": "float"}, {"name": "credit_history", "type": "string"}, {"name": "purpose", "type": "string"}, {"name": "credit_amount", "type": "float"}, {"name": "savings_status", "type": "string"}, {"name": "employment", "type": "string"}, {"name": "installment_commitment", "type": "float"}, {"name": "personal_status", "type": "string"}, {"name": "other_parties", "type": "string"}, {"name": "residence_since", "type": "float"}, {"name": "property_magnitude", "type": "string"}, {"name": "age", "type": "float"}, {"name": "other_payment_plans", "type": "string"}, {"name": "housing", "type": "string"}, {"name": "existing_credits", "type": "float"}, {"name": "job", "type": "string"}, {"name": "num_dependents", "type": "float"}, {"name": "own_telephone", "type": "string"}, {"name": "foreign_worker", "type": "string"}] | [{"name": "class", "type": "string"}] | xgboost_1.6    | python_3.8  |              1 | [{"objective": "precision", "score": 0.7675}, {"objective": "recall", "score": 0.775}]                                        | {"status": "Ready"}
```

## 查看指定模型

KWDB 支持查看指定模型或者指定版本的基本信息和详细信息。

### 前提条件

- 已经将模型导入到数据库中。
- 用户为 Admin 用户、模型的创建者、或者拥有模型的 SELECT 权限。

### 语法格式

```sql
SELECT * FROM kwdbml.show_model(<model_name> [, <model_version>]);
```

### 参数说明

| 参数          | 类型   | 描述                                                                                  |
| ------------- | ------ | ------------------------------------------------------------------------------------- |
| `model_name`    | STRING | 模型的名称。支持两级结构名称：模式名.对象名。如未指定前缀模式名，默认使用当前模式。 |
| `model_version` | INT    | 可选参数，模型版本。如未指定，表示查看目标模型的所有版本。                                      |

### 返回字段说明

| 参数         | 类型      | 描述                                                     |
| ------------ | --------- | -------------------------------------------------------- |
| `schema`       | STRING    | 模型的模式名称。                                         |
| `name`         | STRING    | 模型的名称。                                             |
| `description`  | STRING    | 模型的描述信息。                                           |
| `creator`      | STRING    | 模型的创建者。                                         |
| `created`      | TIMESTAMP | 模型的创建时间。                                       |
| `problem_type` | STRING    | 模型的问题分类。                             |
| `features`     | JSON      | 模型的输入特征列信息，包括列名和数据类型。 |
| `target`       | JSON      | 模型的输出特征列信息，包括列名和数据类型。 |
| `framework`    | STRING    | 模型使用的机器学习框架类型及版本。           |
| `runtime`      | STRING    | 模型的运行环境及版本。                       |
| `active_version` | INT       | 模型的当前活跃版本。                         |
| `last_metrics`   | JSON      | 模型的最新评估结果。                       |
| `status`         | JSON      | 模型的状态。                                   |

### 语法示例

- 查看指定模型，但未指定模型版本。

    ```sql
    SELECT * FROM kwdbml.show_models('pipe_xgb_binary');
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      schema  |    name               | description                                             | creator     | created                          | last_updated                     | problem_type | features                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | target                                | framework      | runtime     | active_version | last_metrics                                                                                                                  | status
    ----------+-----------------------+---------------------------------------------------------+-------------+----------------------------------+----------------------------------+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------+----------------+-------------+----------------+-------------------------------------------------------------------------------------------------------------------------------+----------------------  
        public | pipe_xgb_binary       | Model trained by pipeline public.pipe_xgb_binary.       | kwdbmlusr01 | 2024-05-20 03:11:27.156676+00:00 | 2024-05-20 03:11:27.156676+00:00 | b            | [{"name": "checking_status", "type": "string"}, {"name": "duration", "type": "float"}, {"name": "credit_history", "type": "string"}, {"name": "purpose", "type": "string"}, {"name": "credit_amount", "type": "float"}, {"name": "savings_status", "type": "string"}, {"name": "employment", "type": "string"}, {"name": "installment_commitment", "type": "float"}, {"name": "personal_status", "type": "string"}, {"name": "other_parties", "type": "string"}, {"name": "residence_since", "type": "float"}, {"name": "property_magnitude", "type": "string"}, {"name": "age", "type": "float"}, {"name": "other_payment_plans", "type": "string"}, {"name": "housing", "type": "string"}, {"name": "existing_credits", "type": "float"}, {"name": "job", "type": "string"}, {"name": "num_dependents", "type": "float"}, {"name": "own_telephone", "type": "string"}, {"name": "foreign_worker", "type": "string"}] | [{"name": "class", "type": "string"}] | xgboost_1.6    | python_3.8  |              1 | [{"objective": "precision", "score": 0.7675}, {"objective": "recall", "score": 0.775}]                                        | {"status": "Ready"}
    ```

- 查看指定模型，且指定模型版本。

    ```sql
    SELECT * FROM kwdbml.show_models('pipe_xgb_binary', 1);
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      schema  |    name               | description                                             | creator     | created                          | last_updated                     | problem_type | features                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | target                                | framework      | runtime     | active_version | last_metrics                                                                                                                  | status
    ----------+-----------------------+---------------------------------------------------------+-------------+----------------------------------+----------------------------------+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------+----------------+-------------+----------------+-------------------------------------------------------------------------------------------------------------------------------+----------------------  
        public | pipe_xgb_binary       | Model trained by pipeline public.pipe_xgb_binary.       | kwdbmlusr01 | 2024-05-20 03:11:27.156676+00:00 | 2024-05-20 03:11:27.156676+00:00 | b            | [{"name": "checking_status", "type": "string"}, {"name": "duration", "type": "float"}, {"name": "credit_history", "type": "string"}, {"name": "purpose", "type": "string"}, {"name": "credit_amount", "type": "float"}, {"name": "savings_status", "type": "string"}, {"name": "employment", "type": "string"}, {"name": "installment_commitment", "type": "float"}, {"name": "personal_status", "type": "string"}, {"name": "other_parties", "type": "string"}, {"name": "residence_since", "type": "float"}, {"name": "property_magnitude", "type": "string"}, {"name": "age", "type": "float"}, {"name": "other_payment_plans", "type": "string"}, {"name": "housing", "type": "string"}, {"name": "existing_credits", "type": "float"}, {"name": "job", "type": "string"}, {"name": "num_dependents", "type": "float"}, {"name": "own_telephone", "type": "string"}, {"name": "foreign_worker", "type": "string"}] | [{"name": "class", "type": "string"}] | xgboost_1.6    | python_3.8  |              1 | [{"objective": "precision", "score": 0.7675}, {"objective": "recall", "score": 0.775}]                                        | {"status": "Ready"}
    ```

## 查看所有训练流水线

KWDB 支持查看所有训练流水线的基本信息。

### 前提条件

- 已经将训练流水线导入到数据库中。
- 用户为 Admin 用户、训练流水线的创建者、或者拥有训练流水线的 SELECT 权限。

### 语法格式

```sql
SELECT * FROM kwdbml.show_training_pipelines();
```

### 参数说明

无

### 返回字段说明

| 参数         | 类型      | 描述                                                     |
| ------------ | --------- | -------------------------------------------------------- |
| `schema`       | STRING    | 训练流水线的模式名称。                                         |
| `name`         | STRING    | 训练流水线的名称。                                             |
| `description`  | STRING    | 训练流水线的描述信息。                                           |
| `creator`      | STRING    | 训练流水线的创建者。                                         |
| `created`      | TIMESTAMP | 训练流水线的创建时间。                                       |
| `problem_type` | STRING    | 训练流水线训练模型的问题分类。                             |
| `features`     | JSON      | 训练流水线训练模型的输入特征列信息，包括列名和数据类型。 |
| `target`       | JSON      | 训练流水线训练模型的输出特征列信息，包括列名和数据类型。 |
| `framework`    | STRING    | 训练流水线训练模型使用的机器学习框架类型及版本。           |
| `runtime`      | STRING    | 训练流水线训练模型的运行环境及版本。                       |

### 语法示例

以下示例查看所有流水线的信息。

```sql
SELECT * FROM kwdbml.show_training_pipelines();
```

执行成功后，控制台输出以下信息：

```sql
schema | name              |     description   | creator     | created                          | problem_type | features                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | target                                | framework      | runtime
-------+-------------------+-------------------+-------------+----------------------------------+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------+----------------+-----------
public | pipe_upload_test  | pipe_upload_test  | kwdbmlusr01 | 2024-05-17 07:28:20.62134+00:00  | b            | [{"name": "checking_status", "type": "string"}, {"name": "duration", "type": "float"}, {"name": "credit_history", "type": "string"}, {"name": "purpose", "type": "string"}, {"name": "credit_amount", "type": "float"}, {"name": "savings_status", "type": "string"}, {"name": "employment", "type": "string"}, {"name": "installment_commitment", "type": "float"}, {"name": "personal_status", "type": "string"}, {"name": "other_parties", "type": "string"}, {"name": "residence_since", "type": "float"}, {"name": "property_magnitude", "type": "string"}, {"name": "age", "type": "float"}, {"name": "other_payment_plans", "type": "string"}, {"name": "housing", "type": "string"}, {"name": "existing_credits", "type": "float"}, {"name": "job", "type": "string"}, {"name": "num_dependents", "type": "float"}, {"name": "own_telephone", "type": "string"}, {"name": "foreign_worker", "type": "string"}] | [{"name": "class", "type": "string"}] | xgboost_1.6    | python_3.8
```

## 查看指定训练流水线

KWDB 支持查看指定训练流水线的基本信息。

### 前提条件

- 已经将训练流水线导入到数据库中。
- 用户为 Admin 用户、训练流水线的创建者、或者拥有训练流水线的 SELECT 权限。

### 语法格式

```sql
SELECT * FROM kwdbml.show_training_pipeline(<pipeline_name>);
```

### 参数说明

| 参数          | 类型   | 描述                                                                                    |
| ------------- | ------ | --------------------------------------------------------------------------------------- |
| `pipeline_name` | STRING | 训练流水线的名称。支持两级结构名称：模式名.对象名。如未指定前缀模式名，默认使用当前模式。 |

### 返回字段说明

| 参数         | 类型      | 描述                                                     |
| ------------ | --------- | -------------------------------------------------------- |
| `schema`       | STRING    | 训练流水线的模式名称。                                         |
| `name`         | STRING    | 训练流水线的名称。                                             |
| `description`  | STRING    | 训练流水线的描述信息。                                           |
| `creator`      | STRING    | 训练流水线的创建者。                                         |
| `created`      | TIMESTAMP | 训练流水线的创建时间。                                       |
| `problem_type` | STRING    | 训练流水线训练模型的问题分类。                             |
| `features`     | JSON      | 训练流水线训练模型的输入特征列信息，包括列名和数据类型。 |
| `target`       | JSON      | 训练流水线训练模型的输出特征列信息，包括列名和数据类型。 |
| `framework`    | STRING    | 训练流水线训练模型使用的机器学习框架类型及版本。           |
| `runtime`      | STRING    | 训练流水线训练模型的运行环境及版本。                       |

### 语法示例

以下示例查看 `pipe_upload_test` 训练流水线的信息。

```sql
SELECT * FROM kwdbml.show_training_pipeline('pipe_upload_test');
```

执行成功后，控制台输出以下信息：

```sql
schema | name              |     description   | creator     | created                          | problem_type | features                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | target                                | framework      | runtime
-------+-------------------+-------------------+-------------+----------------------------------+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------+----------------+-----------
public | pipe_upload_test  | pipe_upload_test  | kwdbmlusr01 | 2024-05-17 07:28:20.62134+00:00  | b            | [{"name": "checking_status", "type": "string"}, {"name": "duration", "type": "float"}, {"name": "credit_history", "type": "string"}, {"name": "purpose", "type": "string"}, {"name": "credit_amount", "type": "float"}, {"name": "savings_status", "type": "string"}, {"name": "employment", "type": "string"}, {"name": "installment_commitment", "type": "float"}, {"name": "personal_status", "type": "string"}, {"name": "other_parties", "type": "string"}, {"name": "residence_since", "type": "float"}, {"name": "property_magnitude", "type": "string"}, {"name": "age", "type": "float"}, {"name": "other_payment_plans", "type": "string"}, {"name": "housing", "type": "string"}, {"name": "existing_credits", "type": "float"}, {"name": "job", "type": "string"}, {"name": "num_dependents", "type": "float"}, {"name": "own_telephone", "type": "string"}, {"name": "foreign_worker", "type": "string"}] | [{"name": "class", "type": "string"}] | xgboost_1.6    | python_3.8
```
