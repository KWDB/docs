---
title: 模型文件
id: prepare-model-files
---

# 模型文件

## 训练模型

KaiwuDB 预测分析引擎支持用户选择任何模型开发环境进行模型训练。完成模型训练后，需要组织模型文件及相关的依赖。此外，建议将模型特征和标签信息保存为 JSON 文件，以便导入模型时将其作为 SQL 的输入使用。

### 模型训练示例

以下是一些常见机器学习框架的模型训练示例。以下示例假设已经预处理输入的数据，可以直接进行模型训练。

- Lightgbm 模型

    ```python
    import joblib
    import lightgbm as lgb
    import os
    import pandas as pd

    # 定义标签列名
    label = "my_label"

    # 读取训练数据
    train_df = pd.read_csv("my_train.csv")

    # 划分训练集和验证集
    train_count = int(len(train_df) * 0.8) + 1
    train_data = train_df[:train_count]
    val_data = train_df[train_count:]

    # 准备训练数据和标签
    x_train = train_data.copy()
    y_train = x_train.pop(label)

    x_val = val_data.copy()
    y_val = x_val.pop(label)

    # 创建 LightGBM 数据集
    train_set = lgb.Dataset(x_train, label=y_train)
    val_set = lgb.Dataset(x_val, label=y_val)

    # 配置模型参数
    params = {
        'learning_rate': 0.01,
        'boosting_type': 'gbdt',
        'max_depth': 3,
        'num_leaves': 7,
        'objective': 'regression',
        'metric': 'l2',
        'training_metric': True
    }

    # 训练 LightGBM 模型
    num_round = 100
    gbm = lgb.train(params, train_set, valid_sets=[val_set], num_boost_round=num_round)

    # 创建保存模型的目录
    save_path = "model"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 保存模型为 model.joblib 文件
    joblib.dump(gbm, open(os.path.join(save_path, 'model.joblib'), 'wb'))

    print("模型已保存到", save_path)
    ```

- scikit-learn 模型

    ```python
    from sklearn.ensemble import GradientBoostingRegressor as GBR
    import joblib
    import os
    import pandas as pd
    from sklearn import metrics

    # 定义标签列名
    label = "my_label"

    # 读取训练数据
    train_df = pd.read_csv("my_train.csv")

    # 划分训练集和验证集
    train_count = int(len(train_df) * 0.8) + 1
    train_data = train_df[:train_count]
    val_data = train_df[train_count:]

    # 准备训练数据和标签
    x_train = train_data.copy()
    y_train = x_train.pop(label)

    x_val = val_data.copy()
    y_val = x_val.pop(label)

    # 创建并训练 GradientBoostingRegressor 模型
    gbr = GBR()
    gbr.fit(x_train.values, y_train.values)
    print('模型训练完成')

    # 进行验证并计算均方误差
    y_pred = gbr.predict(x_val.values)
    mse = metrics.mean_squared_error(y_val, y_pred)
    print('均方误差 (MSE): ', mse)

    # 创建保存模型的目录
    save_path = "model"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 保存模型为 model.joblib 文件
    joblib.dump(gbr, os.path.join(save_path, 'model.joblib'))

    print("模型已保存到", save_path)
    ```

- XGBoost 模型

    ```python
    import xgboost as xgb
    import joblib
    import os
    import pandas as pd

    # 定义标签列名
    label = "my_label"

    # 读取训练数据
    train_df = pd.read_csv("my_train.csv")

    # 划分训练集和验证集
    train_count = int(len(train_df) * 0.8) + 1
    train_data = train_df[:train_count]
    val_data = train_df[train_count:]

    # 准备训练数据和标签
    x_train = train_data.copy()
    y_train = x_train.pop(label)

    x_val = val_data.copy()
    y_val = x_val.pop(label)

    # 创建并训练 XGBoost 模型
    xgb_model = xgb.XGBRegressor(max_depth=9, learning_rate=0.01, n_estimators=100, objective='reg:squarederror')
    xgb_model.fit(x_train.values, y_train.values)

    # 评估模型
    score = xgb_model.score(x_val.values, y_val.values)
    print("模型评分:", score)

    # 创建保存模型的目录
    save_path = "model"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 保存模型为 model.joblib 文件
    joblib.dump(xgb_model, os.path.join(save_path, 'model.joblib'))

    print("模型已保存到", save_path)
    ```

- TensorFlow 模型

    ::: warning 说明
    以下示例保存的目录的名称是 `tf_model`。如需在 TensorFlow Serving 部署 KaiwuDB 预测分析引擎，需要将目录名改为可以表示版本号的名字，例如 `001` 或 `002`。
    :::

    ```python
    import os
    import json
    import tensorflow as tf
    import pandas as pd

    # 定义标签列名
    label = "my_label"

    # 读取训练数据
    train_df = pd.read_csv("my_train.csv")

    # 划分训练集和验证集
    train_count = int(len(train_df) * 0.8) + 1
    train_data = train_df[:train_count]
    val_data = train_df[train_count:]

    # 准备训练数据和标签
    x_train = train_data.copy()
    y_train = x_train.pop(label)

    x_val = val_data.copy()
    y_val = x_val.pop(label)

    # 创建并编译 TensorFlow 模型
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(74,)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),
        metrics=[tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
    )

    model.summary()

    # 训练模型
    model.fit(x_train.values.tolist(), y_train.values.tolist(), epochs=5)

    # 评估模型
    loss, precision, recall = model.evaluate(x_val.values.tolist(), y_val.values.tolist())
    metrics = [{'objective': 'loss', 'score': round(loss, 4)}, {'objective': 'precision', 'score': round(precision, 4)}, 
              {'objective': 'recall', 'score': round(recall, 4)}]

    # 创建保存模型的目录
    save_path = "saved_model/tf_model"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 保存模型为 TensorFlow SavedModel 格式
    model.save(save_path)

    # 创建模型信息的JSON文件
    model_info = {
        "framework": "tensorflow",
        "runtime": "python_xxx",
        "problemType": "BINARY_CLASSIFICATION",
        "target": [{"name": label, "type": "int"}],
        "features": []  # 需根据输入特征定义补充
    }

    with open(os.path.join(save_path, "model_info.json"), "w") as json_file:
        json.dump(model_info, json_file)

    print("模型已保存到", save_path)
    ```

### 模型特征示例

以下是模型特征文件（`features.json`）示例。

```json
"features": [
  {
    "name": "feature1",     // 模型特征 1 名称
    "type": "float"         // 模型特征 1 数据类型
  },
  {
    "name": "feature2",     // 模型特征 2 名称
    "type": "float"         // 模型特征 2 数据类型
  },
  ...
  {
    "name": "featureN",     // 模型特征 N 名称
    "type": "float"         // 模型特征 N 数据类型
  }
]
```

### 标签信息文件示例

以下是标签信息文件（`target.json`）示例。

```json
"target": [
  {
    "name": "my_label",     // 输入标签列名
    "type": "int"           // 标签数据类型
  }
]
```

## 准备外部依赖

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

## 组织和打包文件

模型训练完成后，用户需要按照以下结构组织模型文件及其依赖：

```text
model
  └─ model                       # 用于保存模型文件或模型目录。
    └─ model.joblib              # 训练产出的模型文件，不同框架有所不同。
  ├─ requirements.txt            # 可选，用于声明额外需要的Python依赖。
  └─ modules.zip                 # 可选，包含自定义依赖.py文件和.whl文件。
```

下表列出不同框架保存的模型文件或目录信息。

|     框架     |   模型文件   |                                                                                                         说明                                                                                                          |
|--------------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| XGBoost      | `model.joblib` | 单个文件，文件名不可更改。后缀支持使用 `.joblib`、`.pkl`、`.pickle`、`.json`，推荐使用`.joblib`。                                                                                                                                 |
| LightGBM     | `model.joblib` | 单个文件，文件名不可更改。后缀支持使用 `.joblib`、`.pkl`、`.pickle`、`.txt`。                                                                                                                                                   |
| scikit-learn | `model.joblib` | 单个文件，文件名不可更改。后缀支持使用 `.joblib`、`.pkl`、`.pickle`。                                                                                                                                                         |
| TensorFlow   | `001/`         | 单个目录，目录名支持任何可以表示版本号的数字，如 `001`。目录下的内容为 TensorFlow 模型训练完成后保存的模型：<br >- `saved_model.pb` <br > - `keras_metadata.pb` <br > - `variables/` <br >- `assets/` <br > **说明** <br > 模型必须保存为目录，不支持 `.h5` 或者 `.keras` 格式。 |

如需组织和打包模型文件及其依赖，遵循以下步骤。

1. 按照模型文件要求保存模型文件或目录。

2. 创建一个目录，例如 `model`，并在该目录中创建 `model` 子目录。

3. 复制模型文件到指定目录。

    - 将 scikit-learn、XGBoost、LightGBM 训练生成的 `joblib` 文件复制到 `model` 子目录。
    - 将 TensforFlow 训练的模型目录完整复制到 `model` 子目录。

4. （可选）如果依赖特定版本的 Python 包，并且可以通过 PyPI 服务器获取，支持在 `model` 目录下新建 `requirements.txt` 文件，并在文件中列出依赖的 Python 包及版本。
5. （可选）如果需要使用自定义 Python 包，或者依赖的 Python 包无法通过 PyPI 服务器获取，可以将依赖的自定义 Python 包（`.py` 文件或 `.whl` 文件）打包成 `modules.zip`，并将 `modules.zip` 复制到 `model` 目录。

6. 切换到 `model` 目录并打包文件。

    ```shell
    cd model
    zip -r model.zip *
    ```
