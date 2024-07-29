---
title: 故障排查
id: ml-service-troubleshooting
---

# 故障排查

如果导入或者使用模型时或者使用模型出现错误，可以采用以下方法来排查问题。

## 模型导入异常

当出现以下错误提示，可能是因为上传的模型太大，超过文件大小的上限阈值，导致上传失败。

```shell
broken pipe
command is too large: xxx bytes (max: xxx)
```

默认情况下，模型文件和数据预处理文件的大小是 64 MiB，最大不得超过 128 MiB。KWDB 支持通过以下 SQL 语句修改模型文件和数据预处理文件的大小。

```sql
SET cluster setting kv.raft.command.max_size = 128 MiB
```

## 预测结果异常

如果预测结果出现异常，用户可以在本地验证使用的代码和模型是否正确。

::: warning 说明

- 对于 XGBoost、LightGBM 和 scikit-learn，本地测试使用的代码和模型与预测分析引擎使用的代码和模型完全相同。
- 对于 Tensorflow，预测分析引擎对其模型的使用方式较为特殊，需要特别关注。

:::

### 解决办法示例

以下以 TensorFlow 模型为例，说明如何在本地搭建测试环境，验证模型。部署和预测测试模型时，建议关注以下内容：

| 阶段       | 关注点                                                                                  |
| ---------- | --------------------------------------------------------------------------------------- |
| 模型加载   | - 浅层模型的加载方法能否正常执行。<br >- TensorFlow 服务框架能否正常启动。模型能否加载成功。 |
| 数据预处理 | - 逻辑是否符合要求。<br >- 结果是否符合预期。                                                |
| 模型预测   | - 预测结果是否正确。<br >- 后处理函数的逻辑是否正确。                                        |

#### 前提条件

准备好数据预处理文件和模型文件。

#### 步骤

1. 使用 Docker 安装并运行 TensorFlow Serving。根据需要修改 TensorFlow Serving 的服务端口。

    ::: warning 说明
    如果使用 sklearn、LightGBM、XGboost 等其他框架，需要获取 KWDB 构建的相应镜像文件，修改启动命令中的 `command=['--model_dir=/models/', '--model_name=' + container_model_name, '--http_port=8501']` 参数。
    :::

    配置示例：

    ```dockerfile
    # 设置本地模型路径，该路径为外层 model 目录的路径。

    contents_path = 'my_tf_model_path'

    # 部署模型的名称，用于对外提供服务。

    container_model_name = 'tf_model_01'

    # 按照 TensorFlow Serving 的要求创建模型配置文件，
    # 该配置文件由容器内 TensorFlow Serving 使用，用来加载模型。

    with open(os.path.join(contents_path, 'models.config'), 'w') as config:
        config.write('model_config_list: {\n')
        config.write('    config: {\n')
        config.write('        name: "' + container_model_name + '",\n')
        config.write('        base_path: "/models/model",\n') 
        config.write('        model_platform: "tensorflow"\n')
        config.write('    }\n')
        config.write('}')

    # 定义 Docker 镜像、端口。

    image = 'tensorflow/serving:2.9.3' 
    ports = {'8501/tcp': 8501}

    # 将本地路径 contents_path 映射为容器内路径 /models/。

    mounts = [docker.types.Mount(target='/models/', source=contents_path, type='bind', read_only=True)]

    # 启动 TensorFlow Serving 容器。

    container = self.docker_client.containers.run(
        image=image, 
        command=['--model_config_file=/models/models.config'], # 使用配置文件配置模型
        mounts=mounts, 
        ports=ports, 
        detach=True, 
        remove=True)

    # 等待一段时间，确保容器启动完成。

    time.sleep(2)
    ```

2. 向运行在指定端口上的 TensorFlow Serving 容器发起模型预测请求。

    ```python
    test_df = pd.read_csv("my_test.csv")

    # 使用 data_preparation_prediction.py 文件预处理数据

    data = preprocess(test_df)
    port = '8501'
    url = 'http://localhost:%s/v1/models/%s:predict' % (port, container_model_name)
    resp = requests.post(url, json=data)
    ```
