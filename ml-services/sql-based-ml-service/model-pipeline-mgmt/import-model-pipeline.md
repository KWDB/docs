---
title: 导入模型和流水线
id: import-model-pipeline
---

# 导入模型和流水线

## 导入模型

### 前提条件

- 所有用户均可导入新模型。
- 如需导入模型的后续版本，用户拥有目标模型的 CREATE 权限。

### 语法格式

```sql
SELECT import_model(<model_name>,<description>, <problem_type>, <framework>, <runtime>, <input_schema>, <output_schema>, <model_entity>, <transformer_entity>, <metrics>);
```

### 参数说明

| 参数               | 类型   | 描述                                                                                                                                                                                                                                                                                   |
| ------------------ | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model_name`         | STRING | 模型的名称。模型名必须唯一。支持两级结构名称：模式名.对象名。如果未指定前缀模式名，则默认使用当前模式。                                                                                                                                                           |
| `description`        | STRING | 模型的描述信息。                                                                                                                                                                                                                                                                             |
| `problem_type`       | STRING | 模型的问题分类。目前，支持的问题类型包括：<br > - R / Regression：回归问题 <br >- B / Binary_Classification：二分类问题 <br >- M / Multi_Classfication：多分类问题。<br > 取值不区分大小写。                                                                                                               |
| `framework`          | STRING | 机器学习框架的类型和版本。目前，支持的框架和版本包括：<br >- scikit-learn（sklearn）：1.3 <br >- XGBoost：1.5 和 1.6 <br >- LightGBM：3.2 和 3.3 <br >- TensorFlow：2.8 和 2.9 <br > 指定的模型机器学习框架和版本需要和本地测试环境保持一致。取值不区分大小写。                                                              |
| `runtime`            | STRING | 模型的运行环境及版本。目前，支持的环境版本包括：Python 3.8、3.9 和 3.10。指定的模型运行环境需要和本地测试环境保持一致。取值不区分大小写。                                                                                                                                                       |
| `input_schema`       | JSON   | 模型的输入特征列信息，包括列名和数据类型。特征列名和数据类型以 JSON 数组的形式定义，例如 `[{"name":"current_phase_average", "type":"float"}, {"name":" weather_temperature_celsius", "type":"float"}]`。支持的输入特征类型包括 STRING、INT、FLOAT。输入特征列信息用于预测模型和查看模型信息。 |
| `output_schema`      | JSON   | 模型的输出目标列信息，包括列名和数据类型。特征列名和数据类型以 JSON 数组的形式定义，例如 `[{"name":"prediction", "type":"float"}]`。支持的输出目标列类型包括 STRING、INT、FLOAT。输出目标列信息用于预测模型和查看模型信息。                                                                    |
| `model_entity`       | BYTES  | 模型文件，二进制 ZIP 压缩包形式，包含模型文件或目录。                                                                                                                                                                                                                                |
| `transformer_entity` | BYTES  | 数据预处理文件，二进制 ZIP 压缩包形式，包含模型预测预处理文件（`.py` 格式）等。支持为 Null。                                                                                                                                                                                                 |
| `metrics`            | JSON   | 可选参数，模型的性能数据，JSON 数组格式。如果用户已知模型的性能数据，上传模型时可以指定模型的性能数据。例如 `[{"objective ":"F1", "score":5.7}]`。                                                                                                                                                                       |

### 返回字段说明

| 参数                  | 类型   | 描述                  |
|-----------------------|--------|---------------------|
| `kwdbml.import_model` | STRING | 导入模型的名称和版本。 |

### 语法示例

- 使用 SQL 语句导入模型。

    ```sql
    > SELECT kwdbml.import_model('Tom.PowerGen', 'This is a model to predict power generation', 'regression', 'tensorflow_2.8', 'python_3.8','[{"name":"current_phase_average", "type":"float"}, {"name":"weather_temperature_celsius", "type":"float"}]', '[{"name":"prediction","type":"float"}]', model, data_preparation, '[{"objective ":"F1","score":5.7}]');
    ```

    执行成功后，控制台输出以下信息：

    ```sql
    kwdbml.import_model
    +----------------------+
    Tom.PowerGen,1 
    (1 row)
    ```

- 使用 Python 脚本导入模型。

    ```python
    import jaydebeapi
    import os

    # 读取模型和 transformer 压缩文件
    with open('model.zip', 'rb') as m, open('transformer.zip', 'rb') as t:
        model = m.read()
        transformer = t.read()

    # 连接 KWDB 数据库，将 IP 地址、端口号 修改为真实值
    url = 'jdbc:kaiwudb://127.0.0.1:26257/defaultdb'
    jdbc_driver_name = "org.kaiwudb.Driver"

    # 获取驱动包 kwjdbc-2.0.4.jar
    jdbc_driver_loc = '/path/to/kwjdbc-2.0.4.jar'
    user = 'kwdbuser'
    passwd = '123'

    # 模型元数据详情
    model_name = 'test_model'
    description = 'test case'
    problem_type = 'REGRESSION'
    framework = 'tensorflow_2.8'
    runtime = 'python_3.8'
    input_schema = '[{"name": "f1", "type": "string"}, {"name": "f2", "type": "int"}]'
    output_schema = '{"name": "label", "type": "float"}'

    # 导入模型
    sql = "SELECT kwdbml.import_model('{model_name}', '{description}', '{problem_type}', '{framework}', {runtime}, '{input_schema}', '{output_schema}', '{model.hex()}', '{transformer.hex()}')"

    conn = None
    try:
    # 连接数据库
        conn = jaydebeapi.connect(jdbc_driver_name, url, {'user': user, 'password': passwd}, jars=jdbc_driver_loc)
        cur = conn.cursor()
        
    # 执行SQL查询
        cur.execute(sql)
        
    # 关闭游标
        cur.close()
    except Exception as err:
        print(err)
    finally:
        if conn is not None:
            conn.close()
    ```

## 导入训练流水线

用户可以将其他机器学习平台开发测试好的训练流水线上传到数据库，之后就可以通过调用 `kwdbml.train_model` 内置函数进行模型训练。

由于导入训练流水线时需要提供压缩文件和数据预处理压缩文件，建议通过 WEB 界面导入训练流水线。更多详细信息，参见[创建训练流水线](../../web-based-ml-service/pipeline-mgmt.md#创建训练流水线)。

### 前提条件

任何 KWDB 用户均可导入新的训练流水线。

### 语法格式

```sql
SELECT import_training_pipeline(<pipeline_name>,<description>, <problem_type>, <framework>, <runtime>, <input_schema>, <output_schema>, <pipeline_entity>, <transformer_entity>);
```

### 参数说明

| 参数               | 类型   | 描述                                                                                                                                                                                                                                                                                   |
| ------------------ | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pipeline_name`         | STRING | 训练流水线的名称。在指定模式下，流水线的名称必须唯一。支持两级结构名称：模式名.对象名。如果未指定前缀模式名，则默认使用当前模式。                                                                                                                                                           |
| `description`        | STRING | 可选参数，训练流水线的描述信息。                                                                                                                                                                                                                                                                             |
| `problem_type`       | STRING | 问题分类。目前，支持的问题类型包括：<br > - R / Regression：回归问题 <br >- B / Binary_Classification：二分类问题 <br >- M / Multi_Classfication：多分类问题。<br > 取值不区分大小写。                                                                                                               |
| `framework`          | STRING | 机器学习框架的类型和版本。目前，支持的框架和版本包括：<br >- scikit-learn（sklearn）：1.3 <br >- XGBoost：1.5 和 1.6 <br >- LightGBM：3.2 和 3.3 <br >- TensorFlow：2.8 和 2.9 <br > 指定的训练流水线训练模型的机器学习框架和版本需要和本地测试环境保持一致。取值不区分大小写。                                                              |
| `runtime`            | STRING | 训练流水线训练模型的运行环境及版本。目前，支持的环境版本包括 Python 3.8、3.9 和 3.10。指定的训练流水线训练模型的运行环境需要和本地测试环境保持一致。取值不区分大小写。                                                                                                                                                       |
| `input_schema`       | JSON   | 训练流水线训练模型的输入特征列信息，包括列名和数据类型。特征列名和数据类型以 JSON 数组的形式定义，例如 `[{"name":"current_phase_average", "type":"float"}, {"name":" weather_temperature_celsius", "type":"float"}]`。支持的输入特征类型包括 STRING、INT、FLOAT。输入特征列信息用于训练、展示训练流水线。 |
| `output_schema`      | JSON   | 训练流水线训练模型的输出目标列信息，包括列名和数据类型。特征列名和数据类型以 JSON 数组的形式定义，例如 `[{"name":"prediction", "type":"float"}]`。支持的输出目标列类型包括 STRING、INT、FLOAT。输出目标列信息用于训练、展示训练流水线。                                                                    |
| `model_entity`       | BYTES  | 训练流水线文件，二进制 ZIP 压缩包形式。                                                                                                                                                                                                                                |
| `transformer_entity` | BYTES  | 数据预处理文件，二进制 ZIP 压缩包形式，包含模型预测预处理文件（`.py` 格式）等。支持为 Null。                                                                                                                                                                                                 |

### 返回字段说明

| 参数                            | 类型   | 描述                 |
| ------------------------------- | ------ | -------------------- |
| `kwdbml.import_training_pipeline` | STRING | 导入的训练流水线的名称。 |

### 语法示例

以下示例使用 SQL 语句导入流水线。

```sql
SELECT kwdbml.import_training_pipeline('DEMP.PowerGen', 'This is a pipeline for training a model to predict power generation', 'regression', 'tensorflow_2.8', 'python_3.8', '[{"name":"current_phase_average", "type":"float"}, {"name":" weather_temperature_celsius", "type":"float"}]', '[{"name":"prediction", "type":"float"}]', <pipeline file>, <transformer file>);
```

执行成功后，控制台输出以下信息：

```sql
kwdbml.import_training_pipeline
+-----------------------------------------+
DEMP.PowerGen
(1 row)
```
