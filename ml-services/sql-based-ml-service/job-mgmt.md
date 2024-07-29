---
title: 作业管理
id: job-mgmt
---

# 作业管理

用户执行模型训练、模型评估或批量预测命令后，KaiwuDB 预测分析引擎创建相应的机器学习作业，并将作业提交到 [Kubeflow](https://www.kubeflow.org/) 集群中运行。作业运行成功后，系统会将对应的模型、模型性能指标和预测结果保存到 KWDB 数据库中。

KWDB 支持用户查看、中止、删除已生成的后台作业。

## 查看作业

KWDB 支持查看所有或指定后台作业的基本信息。

### 查看所有后台作业

#### 前提条件

用户为 Admin 用户或者作业的创建者。

#### 语法格式

```sql
SELECT * FROM kwdbml.show_jobs(<model_name>, <model_version>, <job_type>, <job_status>);
```

#### 参数说明

| 参数          | 类型        | 描述                                                                                                                       |
| ------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------- |
| `model_name`    | STRING      | 模型的名称。支持两级结构名称：模式名.对象名。如未指定前缀模式名，默认使用当前模式。星号（`*`）表示不过滤模型的名称。             |
| model_version | INT         | 可选参数，模型版本。未指定表示显示所有模型版本的作业。                                                                       |
| `model_version` | INT    | 可选参数，模型版本。如未指定，表示查看目标模型的所有版本。                                      |
| `job_type`      | STRINGARRAY | 可选参数，作业类型，支持 TRAIN（训练）、EVALUATE（评估）、BATCH_PREDICT（批量预测）。`['*']` 表示所有作业类型。                 |
| `job_status`    | STRINGARRAY | 作业状态，支持 RUNNING（正在运行）、SUCCEEDED（成功）、FAILED（失败）、CANCELED（已取消）。`['*']` 表示所有作业状态。 |

KWDB 支持同时省略 `model_name`, `model_version` 和 `job_type`，表示查看所有作业。

#### 返回字段说明

| 参数          | 类型      | 描述                                                         |
| ------------- | --------- | ------------------------------------------------------------ |
| `id`            | STRING    | 后台作业的标识。                                                 |
| `type`          | STRING    | 后台作业的类型。                                                 |
| `status`        | STRING    | 后台作业的状态。                                                 |
| `pipeline_name` | STRING    | 后台作业相关的流水线名称。                                         |
| `model_name`    | STRING    | 后台作业相关的模型名称。                                           |
| `model_version` | INT       | 后台作业相关的模型版本。当作业类型是模型训练时，此列是 NULL 值。 |
| `creator`       | STRING    | 后台作业的创建者。                                               |
| `created`       | TIMESTAMP | 后台作业的开始时间。                                             |
| `finished`      | TIMESTAMP | 后台作业的结束时间。                                             |
| `settings`      | JSON      | 后台作业的配置，例如，训练模型后是否立即部署等。               |
| `result`        | JSON      | 后台作业正常结束的返回结果。                                   |
| `error`         | JSON      | 后台作业非正常结束的错误信息。                                 |

#### 语法示例

- 查看所有作业。

    ```sql
    SELECT * FROM kwdbml.show_jobs();
    ```

- 查看指定作业。

    以下示例查看 `public.m1` 模型中所有的 TRAIN 和 EVALUATE 作业。

    ```sql
    SELECT * FROM kwdbml.show_jobs('public.m1', ['TRAIN', 'EVALUATE'], ['*']);
    ```

### 查看指定后台作业

#### 前提条件

用户为 Admin 用户或作业的创建者。

#### 语法格式

```sql
SELECT * FROM kwdbml.show_job(<job_id>);
```

#### 参数说明

| 参数   | 类型 | 描述         |
| ------ | ---- | ------------ |
| `job_id` | UUID | 后台作业的标识。 |

#### 返回字段说明

| 参数          | 类型      | 描述                                                         |
| ------------- | --------- | ------------------------------------------------------------ |
| `id`            | STRING    | 后台作业的标识。                                                 |
| `type`          | STRING    | 后台作业的类型。                                                 |
| `status`        | STRING    | 后台作业的状态。                                                 |
| `pipeline_name` | STRING    | 后台作业相关的流水线名称。                                         |
| `model_name`    | STRING    | 后台作业相关的模型名称。                                           |
| `model_version` | INT       | 后台作业相关的模型版本。当作业类型是模型训练时，此列是 NULL 值。 |
| `creator`       | STRING    | 后台作业的创建者。                                               |
| `created`       | TIMESTAMP | 后台作业的开始时间。                                             |
| `finished`      | TIMESTAMP | 后台作业的结束时间。                                             |
| `settings`      | JSON      | 后台作业的配置，例如，训练模型后是否立即部署等。               |
| `result`        | JSON      | 后台作业正常结束的返回结果。                                   |
| `error`         | JSON      | 后台作业非正常结束的错误信息。                                 |

#### 语法示例

```sql
SELECT * FROM kwdbml.show_job('00f58d83-c934-4a3f-98dc-84bf5936dfeb');
```

执行成功后，控制台输出以下信息：

```sql

                   id                  | type  |  status   |        pipeline_name        | model_name | model_version |   creator   |             created              | finished                         | settings |                                                             result                                                              | error
---------------------------------------+-------+-----------+-----------------------------+------------+---------------+-------------+----------------------------------+----------------------------------+----------+---------------------------------------------------------------------------------------------------------------------------------+--------
  00f58d83-c934-4a3f-98dc-84bf5936dfeb | TRAIN | SUCCEEDED | public.pipe_tf_binary_py310 |            |             1 | kwdbmlusr01 | 2024-05-17 06:35:02.125377+00:00 | 2024-05-17 06:36:47.574758+00:00 | {}       | [{"objective": "loss", "score": 0.4962}, {"objective": "precision", "score": 0.7879}, {"objective": "recall", "score": 0.9123}] |
(1 row)
```

## 中止作业

### 前提条件

- 用户为 Admin 用户或作业的创建者。
- 待中止的作业正在运行（RUNNING 状态）。

### 语法格式

```sql
SELECT kwdbml.cancel_job(<job_id>);
```

### 参数说明

| 参数   | 类型 | 描述         |
| ------ | ---- | ------------ |
| `job_id` | UUID | 后台作业的标识。 |

### 返回字段说明

| 参数              | 类型   | 描述                 |
| ----------------- | ------ | -------------------- |
| `kwdbml.cancel_job` | STRING | 已中止的后台作业的标识。 |

### 语法示例

```sql
SELECT kwdbml.cancel_job('1dc46a55-36b7-4da5-aff1-1bf6b4c9bf3b');
```

执行成功后，控制台输出以下信息：

```sql
kwdbml.cancel_job 
+-------------------------+
1dc46a55-36b7-4da5-aff1-1bf6b4c9bf3b
(1 row)
```

## 删除作业

### 前提条件

用户为 Admin 用户。

### 语法格式

```sql
SELECT kwdbml.remove_job(job_id);
```

### 参数说明

| 参数   | 类型 | 描述         |
| ------ | ---- | ------------ |
| `job_id` | UUID | 后台作业的标识。 |

### 返回字段说明

| 参数              | 类型   | 描述                 |
| ----------------- | ------ | -------------------- |
| `kwdbml.remove_job` | STRING | 已删除的后台作业的标识。 |

### 语法示例

```sql
SELECT kwdbml.remove_job('1dc46a55-36b7-4da5-aff1-1bf6b4c9bf3b');
```

执行成功后，控制台输出以下信息：

```sql
kwdbml.remove_job 
+------------------------+
1dc46a55-36b7-4da5-aff1-1bf6b4c9bf3b
(1 row)
```
