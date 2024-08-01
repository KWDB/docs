---
title: 流水线文件
id: prepare-pipeline-files
---

# 流水线文件

## 准备流水线文件

用户需要按照以下结构组织流水线文件及其依赖：
  
```python
pipeline/
├── pipeline/
    ├── train.py          # 用户定义的模型训练脚本（必选）
    ├── evaluate.py       # 用户定义的模型评估脚本（可选）
    ├── batch_predict.py  # 用户定义的批量预测脚本（可选）
├── requirements.txt  # Python 包依赖文件（可选）
└─ modules.zip                   # 用户自定义依赖文件（可选）
    ├─ custom_dependency.py     # 用户自定义依赖的 .py 文件
```

如需组织和打包流水线文件，遵循以下步骤。

1. 按照流水线文件要求保存流水线文件或目录。
2. 创建一个目录，例如 `pipeline`。
3. 复制流水线文件到指定目录。

    - 使用机器学习模型框架生成的模型流水线文件：直接将文件放置在 `pipeline` 目录。
    - 使用自定义脚本实现模型训练：
      1. 在 `pipeline` 目录中创建 `pipeline` 子目录。
      2. 将模型训练、评估及批量预测相关的脚本及其依赖放置在 `pipeline` 子目录。

      ::: warning 说明：

      - 所有脚本必须以 `.py` 结尾，并实现指定接口。具体信息，参见[训练脚本示例](#训练脚本示例)、[评估脚本示例](#评估脚本示例)、[批量预测脚本示例](#批量预测脚本示例)。
      - 训练脚本为必选脚本，命名为 `train.py`。
      - 评估脚本为可选脚本，命名为 `evaluate.py`。如未提供评估脚本或者未定义模型评估方法，预测分析引擎将根据模型框架决定加载和预测模型的方法，并根据问题类型选择常用指标进行模型评估。
      - 批量预测脚本为可选脚本，命名为 `batch_predict.py`。如未提供批量预测脚本或者未定义批量预测方法，预测分析引擎将根据模型框架决定加载和预测模型的方法。

      :::

4. （可选）如果依赖特定版本的 Python 包，并且可以通过 PyPI 服务器获取，支持在 `pipeline` 目录下新建 `requirements.txt` 文件，并在文件中列出依赖的 Python 包及版本。
5. （可选）如果需要使用自定义 Python 包，或者依赖的 Python 包无法通过 PyPI 服务器获取，可以将依赖的自定义 Python 包（`.py` 文件或 `.whl` 文件）打包成 `modules.zip`，并将 `modules.zip` 复制到 `pipeline` 目录。
6. 切换到 `pipeline` 目录，使用 `zip` 命令将文件和子目录打包成 `pipeline.zip` 压缩包（不包括最外层的 `pipeline` 目录）。

    ```shell
    cd pipeline
    zip -r pipeline.zip *
    ```

## 准备数据预处理文件

用户需要按照以下结构组织数据预处理文件及其依赖：

```python
data-preparation/
└── prediction/
    ├── data_preparation_prediction.py  # 用户定义的预测数据预处理脚本
    ├── requirements.txt  # Python 包依赖文件 （可选）
    └─ modules.zip                   # 用户自定义依赖文件 （可选）
        ├─ custom_dependency.py     # 用户自定义依赖的 .py 文件
└── training/
    ├── data_preparation_training.py  # 用户定义的训练数据预处理脚本
    ├── requirements.txt  # Python 包依赖文件 （可选）
    └─ modules.zip                   # 用户自定义依赖文件 （可选）
        ├─ custom_dependency.py     # 用户自定义依赖的 .py 文件
```

如需组织和打包数据预处理文件，遵循以下步骤。

1. 按照数据预处理文件要求保存数据预处理文件或目录。
2. 创建一个新目录 ，例如 `data-preparation`。
3. 如果需要预处理训练数据集的特征信息后才能进行模型预测，执行以下操作：

    1. 在 `data-preparation` 目录中创建 `prediction` 子目录。
    2. 将预测需要的数据预处理脚本及其依赖的其他脚本放置在 `prediction` 子目录。

        ::: warning 说明：

        数据预处理脚本必须命名为 `data_preparation_prediction.py` 并定义 `preprocess`、`postprocess`、`batch_preprocess`、`batch_postprocess` 函数。具体信息，参见[预处理脚本示例](#预处理脚本示例)。

        :::

    3. （可选）如果依赖特定版本的 Python 包，并且可以通过 PyPI 服务器获取，支持在 `prediction` 目录下新建 `requirements.txt` 文件，并在文件中列出依赖的 Python 包及版本。
    4. （可选）如果需要使用自定义 Python 包，或者依赖的 Python 包无法通过 PyPI 服务器获取，可以将依赖的自定义 Python 包（`.py` 文件或 `.whl` 文件）打包成 `modules.zip`，并将 `modules.zip` 复制到 `prediction` 目录。

4. 如果需要预处理训练数据集的特征信息后才能进行模型训练，执行以下操作：

    1. 在 `data-preparation` 目录中创建 `training` 子目录。
    2. 将训练需要的数据预处理脚本及其依赖的其他脚本放置在 `training` 子目录。其中数据预处理脚本须命名为 `data_preparation_training.py`，实现指定函数。

        ::: warning 说明：

        数据预处理脚本必须命名为 `data_preparation_training.py` 并定义 `preprocess`、`postprocess`、`batch_preprocess`、`batch_postprocess` 函数。具体信息，参见[预处理脚本示例](#预处理脚本示例)。

        :::

    3. 根据需要在数据预处理脚本中定义分割数据集的方法。默认情况下，预测分析引擎通过 `transform_training_data` 处理模型训练数据集。处理过程中如果有中间结果，比如统计信息等，则保存在 `data_path` 目录中。预测分析引擎通过 `transform_test_data` 处理测试数据集。如果处理测试数据集的方法和训练数据集相同，可以不提供。

        ```python
        from sklearn.model_selection import train_test_split


        def split(self, df: DataFrame):
            return train_test_split(df, test_size=0.2, shuffle=False)
        ```

    4. （可选）如果依赖特定版本的 Python 包，并且可以通过 PyPI 服务器获取，支持在 `training` 目录下新建 `requirements.txt` 文件，并在文件中列出依赖的 Python 包及版本。
    5. （可选）如果需要使用自定义 Python 包，或者依赖的 Python 包无法通过 PyPI 服务器获取，可以将依赖的自定义 Python 包（`.py` 文件或 `.whl` 文件）打包成 `modules.zip`，并将 `modules.zip` 复制到 `training` 目录。

5. 切换到 `data-preparation` 目录，使用 `zip` 命令将文件和目录打包成 `dataprep.zip`（不包括最外层的 `data-preparation` 目录）。

    ```shell
    cd data-preparation
    zip -r dataprep.zip *
    ```

## 脚本示例

### 训练脚本示例

```python
from pandas import DataFrame


def model_train(x_train: DataFrame, y_train: DataFrame, x_test: pd.DataFrame, y_test: pd.DataFrame
) -> tuple[any, any]:
    # user defined training function.
# Returns:
# tuple[any, any]: the first element is model, the second, if has, is metrics
    pass


def model_save(model: any, model_path: str):
    # user defined save function. (Optional)
    pass
```

::: warning 说明
`model_save` 为可选方法。用户可以通过该方法灵活地保存模型。若未定义该方法，预测分析引擎将根据模型框架的常用方法来保存模型。
:::

### 评估脚本示例

```python
from pandas import DataFrame


def model_evaluate(model_path: str, metrics: list, x_test: pd.DataFrame, y_test: pd.DataFrame) -> str:
    # user defined evaluate function.
# Returns:
# str: metrics result in format: [{'objective':  'metrics_name', 'score': 'metrics_score'},...]
    pass
```

### 批量预测脚本示例

```python
from pandas import DataFrame


def model_predict(model_path: str, x_test: pd.DataFrame
) -> DataFrame:
    # user defined local predict function.
# load  model with python module directly, nor by some serving framework, such as tensorflow-serving
    pass
```

### 预处理脚本示例

```python
from pandas import DataFrame


def preprocess(inputs: dict, data_path: str):
    # user defined data preparation function.
    pass


 def postprocess(inputs: dict, data_path: str) -> dict:
    # user defined post process function.
    pass


 def batch_preprocess(df: DataFrame, data_path: str) -> DataFrame:
    # user defined data preparation function for batch prediction.
    pass


 def batch_postprocess(df: DataFrame, data_path: str) -> DataFrame:
    # user defined post process function for batch prediction.
    pass
```
