---
title: 训练数据
id: prepare-data
---

# 训练数据

在预测分析模型之前，用户需要提前处理训练数据。本文介绍如何预处理训练数据。

## 准备数据

用户需要准备以下数据：

- 数据预处理需要实现的函数
- 需要用到的外部依赖
- 用于处理模型预测的其他数据

### 需要实现的函数

通常情况下，原始数据需要根据预测目标以及所选的模型框架和算法进行预处理后，才能用来训练模型。

KaiwuDB 预测分析引擎使用以下接口封装用户的数据预处理过程。该接口的实现脚本需要保存为名为 `data_preparation_prediction.py` 的文件。

```python
import pandas as pd

def preprocess(inputs: pd.DataFrame, data_path: str):
    # 数据预处理函数
    return inputs

def postprocess(inputs: Dict, data_path: str):
    # 预测结果后处理函数
    return inputs
```

- 预处理函数

    输入参数说明：

    | 字段    | 类型             | 说明                                                                                                                                                                                |
    | --------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `inputs`    | pandas.DataFrame | 数据按行组织，每行是一个样本，每列是一个特征。DataFrame 的列名、类型和顺序必须与导入模型时的特征定义一致。                                                                          |
    | `data_path` | STRING           | 存储用户自定义数据的目录。确保用户自定义数据放置在 `data/` 目录下。有关用户自定义数据的详细信息，参见[其他数据](#其他数据)。 |

    预处理函数的返回值为 DICT 类型，不同框架返回值有所不同：

    - scikit-learn、XGBoost、LightGBM 架构

    <table>
      <thead>
        <tr>
          <th>框架</th>
          <th>返回值</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>
            <p> scikit-learn </p>
            <p> XGBoost </p>
            <p> LightGBM </p>
          </td>
          <td>
            <pre><code>
              {
                  "instances":"(nested)list"
              }
            </code></pre>
            <p><code>instances</code>：必填字段，值是数组。数组的每个元素表示一个最终样本。</p>
          </td>
        </tr>
        <tr>
          <td>TensorFlow</td>
          <td>
            <pre><code>
              {
                // Input Tensors in row   ("instances") or columnar ("inputs") format.
                // A request can have either of them but NOT both.
                "instances":"value"|"(nested)list"|"list-of-objects"
                "inputs":"value"|"(nested)list"|"object"
              }
            </code></pre>
            <p> 数据结构符合 TensorFlow Serving RESTful API 的定义，可以采用以下任一方式：</p>
            <ul>
            <li> 使用 <code>instances</code> 字段，取值支持单个值、嵌套列表或对象列表。</li>
            <li> 使用 <code>inputs</code> 字段，取值支持单个值、嵌套列表或对象列表。</li>
            </ul>
            <p> 预测阶段，TensorFlow Serving 负责维护模型。数据结构应该符合 TensorFlow Serving RESTful API 的定义。更多信息，参见 <a href="https://tensorflow.google.cn/tfx/serving/api_rest#predict_api">TensorFlow Serving Predict API</a>。</p>
          </td>
        </tr>
      </tbody>
    </table>

- 后处理函数

    输入参数说明：

    <table>
    <thead>
      <tr>
        <th>字段</th>
        <th>类型</th>
        <th>说明</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>inputs</code></td>
        <td>DICT</td>
        <td>
          <p>推荐的数据结构：</p>
          <pre><code>
            {
              "predictions":"(nested)list"|"list-of-objects"
            }
          </code></pre>
          <p><code>predictions</code>：值为数组，数组的每个元素表示一个样本的预测结果。</p>
        </td>
      </tr>
      <tr>
        <td><code>data_path</code></td>
        <td>STRING</td>
        <td>存储用户自定义数据的目录。确保数据放置在 <code>data/</code> 目录下。</td>
      </tr>
    </tbody>
    </table>

    返回值说明：

    <table>
    <thead>
      <tr>
        <th>类型</th>
        <th>说明</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>DICT</td>
        <td>
          <pre><code>
            {
                "predictions":"(nested)list"|"list-of-objects"
            }
          </code></pre>
          <p>对预测结果进行处理，不建议改变数据组织方式。</p>
        </td>
      </tr>
    </tbody>
    </table>

### 外部依赖

::: warning 说明

- 预测分析引擎使用的 PIP 源是[清华源](https://pypi.tuna.tsinghua.edu.cn/simple/)，在使用较为特殊的依赖时需要额外注意。
- 预测分析引擎已经附带以下常用的 Python 模块，请优先选择。如非特殊需要，不建议安装新版本。
  - numpy~=1.21.5
  - pandas==1.3.5
  - scikit-learn==1.1.2 或 scikit-learn==1.0.2，预测分析引擎根据用户模型框架选择合适的版本。
  - xgboost~=1.7.3
  - lightgbm==3.3.2
  - tensorflow==2.9.3
- 如果预测分析引擎的运行环境无法访问外网，将无法自动安装 `requirements.txt` 中声明的依赖。这种情况下只能通过 `modules.zip` 提供所需的依赖。

:::

预测分析引擎支持通过以下两种方式提供预处理逻辑的其他外部依赖：

- `requirements.txt`：声明公共组件依赖，KaiwuDB 预测分析引擎负责安装相关依赖，内容示例如下：
  
    ```text
    numpy~=1.19.5
    pandas~=1.1.5
    ```

- `modules.zip`：提供自定义依赖或其他需要本地安装的依赖。这类依赖采用 `.py` 或 `.whl` 格式的文件。其中，`.py` 格式的依赖可以通过 `from modules import file_name` 的方式使用。

    ::: warning 说明

    `.py` 文件的使用依赖文件路径，而且使用要求较多。`.whl` 文件使用时没有太多限制，便于分发和维护，而且不易产生冲突。推荐构建自定义 `.whl` 文件，构建完成后将 `.whl` 文件复制到相关目录下进行打包即可。有关如何构建 `.whl` 文件，参见[构建 `.whl` 文件](../ml-service-reference.md#构建-whl-文件)。有关如何打包 `.whl` 文件，参见[组织和打包文件](#组织和打包文件)。

    :::

    `modules.zip` 文件结构如下：

    ```text
    modules.zip
      ├─ dependency1.py      # 用户自定义 .py 文件，文件名无特殊限制
      └─ dependency2.whl     # 用户自定义 .whl 文件，文件名无特殊限制
    ```

### 其他数据

在预处理阶段，模型训练数据集可能会生成额外的数据，用于处理模型预测的输入数据。例如，类别特征取值统计，数值特征统计量等。

特征统计数据示例：

```text
job category    {"values": ["UNK", "skilled", "unskilled resident", "high qualif/self emp/mgmt", "unemp/unskilled non res"]}
own_telephone   category    {"values": ["UNK", "none", "yes"]}
foreign_worker  category    {"values": ["UNK", "yes", "no"]}
duration    numeric {"min": 4.0, "max": 72.0, "mean": 20.6512, "std": 12.1563}
credit_amount   numeric {"min": 250.0, "max": 15945.0, "mean": 3190.9762, "std": 2732.6718}
```

用户自定义这类数据的文件名和数据格式，并将其放置在 `data` 目录下。用户可以在预测结果后处理函数中通过 `data_path` 参数访问这些数据。更多详细信息，参见[需要实现的函数](#需要实现的函数)。

## 组织和打包文件

用户需要按照以下结构组织数据预处理的相关文件：

```text
data_preparation
   ├─ data
   │   ├─ c1.data                   # 用户自定义数据文件，文件名和格式可自行决定。
   │   └─ c2.data                   # 用户自定义数据文件，文件名和格式可自行决定。
   ├─ prediction
   │   └─ data_preparation_prediction.py   # 数据预处理和后处理 Python 文件
   ├─ requirements.txt              # 依赖的 Python 包列表
   └─ modules.zip                   # 用户自定义依赖文件
        ├─ custom_dependency.py     # 用户自定义依赖的 .py 文件
        └─ custom_dependency.whl    # 用户自定义依赖的 .whl 文件
```

如需组织和打包数据预处理的相关文件，遵循以下步骤。

1. 按照规定的目录结构创建目录和文件，其中必须包含 `data_preparation_prediction.py` 文件。
2. 在 `data_preparation_prediction.py` 中定义 `preprocess` 和 `postprocess` 函数。

    ::: warning 说明
    数据预处理脚本必须命名为 `data_preparation_prediction.py` 并定义 `preprocess` 和 `postprocess` 函数。
    :::

3. （可选）如需使用训练时生成的数据统计信息等文件，在 `data_preparation` 目录下创建 `data` 目录，并将数据文件复制到 `data` 目录。
4. （可选）如果预处理脚本依赖特定版本的 Python 包，并且可以通过 PyPI 服务器获取，支持在 `data_preparation` 目录下新建 `requirements.txt` 文件，并在文件中列出依赖的 Python 包及版本。
5. （可选）如果需要使用自定义 Python 包，或者依赖的 Python 包无法通过 PyPI 服务器获取，可以将依赖的自定义 Python 包（`.py` 文件或 `.whl` 文件）打包成 `modules.zip`，并将 `modules.zip` 复制到 `data_preparation` 目录。
6. 切换到 `data_preparation` 目录并打包文件。

    ```shell
    cd data_preparation
    zip -r data_preparation.zip *
    ```

## 数据预处理示例

以下示例定义了一个 Python 接口，输出 `feature_type.txt` 和 `feature_value.txt` 两个文件来保存训练数据集的特征信息。

```python
import os
import sys
from typing import List, Dict
import logging
import numpy as np
import pandas as pd

def preprocess(inputs: pd.DataFrame, data_path: str):
    # 加载特征数据，典型数据是训练阶段产出的特征统计数据
    # load_feature_type(os.path.join(data_path, 'feature_type.txt'))
    # load_feature_value(os.path.join(data_path, 'feature_value.txt'))
    
    # 筛选特征，构建特征，进行特征处理
    # inputs['col1'] = xxx
    # inputs['col2'] = xxx
    # inputs = inputs[['new_col1', 'new_col2,',...]]
    
    # 遵循KServe协议，输出数据作为instances的值
    res = {'instances': inputs.values.tolist()}
    return res

def postprocess(inputs: Dict, data_path: str):
    # 加载特征数据
    # load_feature_type(os.path.join(data_path, 'feature_type.txt'))
    # load_feature_value(os.path.join(data_path, 'feature_value.txt'))
    
    # 假设分类模型标签取值如下
    label_values = ['cls1', 'cls2', 'cls3']
    
    # inputs包含字段predictions，对应的值为预测结果
    res = inputs['predictions']
    new_res = []
    
    # 将预测概率值转换为相应的标签
    for data in res:
        if data < 0.3:
            new_res.append(label_values[0])
        elif data < 0.7:
            new_res.append(label_values[1])
        else:
            new_res.append(label_values[2])
    
    inputs['predictions'] = new_res
    return inputs
```
