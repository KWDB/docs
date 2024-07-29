---
title: 预测分析模型
id: predict-analyze-models
---

# 预测分析模型

## 在线预测模型

### 前提条件

- 已经将模型导入到数据库中。
- 用户为 Admin 用户、模型的创建者、或者拥有模型的 PREDICT 权限。

### 语法格式

```sql
SELECT <column_list> kwdbml.predict(<column_list>) USING <model_name> FROM <data_source>;
```

### 参数说明

| 参数        | 类型   | 描述                                                                                                                                                                                                                                                                                                              |
| ----------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `column_list` | STRING | 不定长参数。模型预测时使用的列名。支持指定一个或多个列名，列名之间用逗号（`,`）隔开。列名和数据类型必须与模型输入匹配。支持使用星号（`*`）表示使用所有列作为输入。                                                                                                                                                                                        |
| `model_name`    | STRING | 模型的名称。支持两级结构名称：模式名.对象名。如未指定前缀模式名，默认使用当前模式。 |
| `data_source` | STRING | 在线预测数据集。KWDB 支持以下两种数据集：<br >- Table/View：表名或者视图名。KWDB 支持三级结构名称：数据库名.模式名.对象名。如果只有一个前缀名称，KWDB 首先在当前数据库中查找具有前缀名称的模式。若查找失败，KWDB 在具有前缀名称的数据库里查找 public 模式中的对象名。如未指定前缀，默认使用当前数据库的搜索路径。<br >- Query：SQL 查询语句。 |

### 返回字段说明

模型的输出模式定义了模型的预测输出信息。不同的输出模式，预测输出信息不同。

### 语法示例

以下示例对数据集为表或视图的 `Tom.PowerGen` 模型进行在线预测分析。

```sql
SELECT id, weather_temperature_celsius, kwdbml.predict('current_phase_average', 'weather_temperature_celsius','weather_relative_humidity', 'global_horizontal_radiation','diffuse_horizontal_radiation', 'wind_direction', 'weather_daily_rainfall') USING 'Tom.PowerGen' from kwdb.kwdb_training;
```

执行成功后，控制台输出以下信息：

```sql
id | weather_temperature_celsius | kwdbml.predict
---+-----------------------------+-----------
1  | 32.41                       | {"prediction": [3.5]}
2  | 41.56                       | {"prediction": [7.8]}
(2 rows)
```

## 批量预测模型

### 前提条件

- 已经将模型导入到数据库中。
- 用户为 Admin 用户、模型的创建者、或者拥有模型的 PREDICT 权限。
- 如果引用的数据源为表或视图，用户拥有目标表或视图的 SELECT 权限。
- 如果引用的数据源为 SQL 查询语句，用户拥有目标对象的 QUERY 权限和 SELECT 权限。

### 语法格式

```sql
SELECT kwdbml.batch_predict([<pipeline_name>,] <model_name>, <model_version>, <batch_data>, <result_table>, <action_if_exists>);
```

### 参数说明

| 参数             | 类型   | 描述                                                                                                                                                                                                                                                                                                                      |
| ---------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pipeline_name`    | STRING | 流水线的名称，支持为空，即 `''`。支持两级结构名称：模式名.对象名。如未指定前缀模式名，默认使用当前模式。                                                                                                                                                                                             |
| `model_name`    | STRING | 模型的名称。支持两级结构名称：模式名.对象名。如未指定前缀模式名，默认使用当前模式。 |
| `model_version` | INT    | 模型版本。                                      |
| `batch_data`       | STRING | 批量预测数据集。KWDB 支持以下两种数据集：<br >- Table/View：表名或者视图名。KWDB 支持三级结构名称：数据库名.模式名.对象名。如果只有一个前缀名称，KWDB 首先在当前数据库中查找具有前缀名称的模式。若查找失败，KWDB 在具有前缀名称的数据库里查找 public 模式中的对象名。如未指定前缀，默认使用当前数据库的搜索路径。<br >- Query：SQL 查询语句。|
| `result_table`     | STRING | 预测结果输出表。KWDB 支持三级结构名称：数据库名.模式名.对象名。当预测结果输出表不存在时，KWDB 自动创建预测结果输出表。当预测结果输出表已经存在时，KWDB 采根据 `action_if_exists` 参数的取值采取相应的措施。                                                                                                                                                                                                                                |
| `action_if_exists` | STRING | 当预测结果输出表已经存在时，KWDB 处理预测结果的方式。KWDB 支持采用以下方式处理预测结果：<br >- replace：删除当前预测结果输出表的内容，然后添加预测结果。 <br >- append：追加预测结果到当前预测结果输出表。 <br >- error：返回错误。<br > 取值不区分大小写。                                                                                                                                                                                                      |

### 返回字段说明

| 参数                 | 类型   | 描述                   |
| -------------------- | ------ | ---------------------- |
| `kwdbml.batch_predict` | STRING | 批量预测任务的任务标识。 |

### 语法示例

- 引用数据为表或视图。

    以下示例对数据集为表或视图的 `Tom.PowerGen` 模型进行批量预测分析。

    ```sql
    SELECT kwdbml.batch_predict('DEMP.PowerGen', 'Tom.PowerGen', '1',  'power_oct', 'score_out', 'replace');
    ```

    执行成功后，控制台输出以下信息：

    ```sql
    kwdbml.batch_predict
    +---------------------------+
    1dc46a55-36b7-4da5-aff1-1bf6b4c9bf3b
    ```

- 引用数据为 SQL 查询语句。

    以下示例对数据集为 SQL 查询语句的 `Tom.PowerGen` 模型进行批量预测分析。

    ```sql
    SELECT kwdbml.batch_predict('DEMP.PowerGen', 'Tom.PowerGen', '1', 'select * from power_oct', 'score_out', 'replace');
    ```

    执行成功后，控制台输出以下信息：

    ```sql
    kwdbml.batch_predict
    +---------------------------+
    1dc46a55-36b7-4da5-aff1-1bf6b4c9bf3b
    ```
