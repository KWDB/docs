---
title: 参考信息
id: ml-service-reference
---

# 参考信息

## 构建 `.whl` 文件

1. 在用户自定义包的同级目录中，创建 `setup.py` 说明文件，用来构建 `.whl` 文件。

    ```text
    setup.py               # 创建 setup.py 进行.whl 构建
    my_package             # 用户自定义包
    ├── folder1            # 子目录
    │   ├── __init__.py
    │   └── file1.py       # 自定义文件
    ├── folder1
    │   └── file2.py
    └── __init__.py
    ```

    `setup.py` 文件内容示例：

    ```python
    import setuptools
      
    setuptools.setup(
        name="my_package",
        version="1.0.0",
        author="myname",
        author_email="myname@xxx.com",
        description="my package wheel",
        packages=setuptools.find_packages(),
        license="MIT",
        python_requires=">=3.8" # 运行环境要求。如果安装环境不符合该要求，则安装失败。
    )
    ```

2. 在 `setup.py` 所在的目录，执行以下命令：

    ```python
    python setup.py bdist_wheel
    ```

    在同级目录下会产出三个新目录：

    - `build`
    - `dist`
    - `my_package.egg-info`

    `dist` 目录下的 `my_package-1.0.0-py3-none-any.whl` 就是构建的 `.whl` 文件，可用于分发。

    ::: warning 说明

    用户也可以导出已经安装的依赖，并在新环境中使用这些依赖。具体步骤如下：

    1. 运行以下命令，将当前环境的依赖保存到 `my_file.txt` 文件。

        ```shell
        pip freeze  > my_file.txt
        ```

    2. 根据需要修改 `my_file.txt` 文件。

    3. 运行以下命令，在新环境中下载 `my_file.txt` 中所列的依赖。通常情况下，这些依赖是 `.whl` 文件。

        ```shell
        pip download -r my_file.txt
        ```

    :::
