---
title: 安装预测分析引擎
id: install
---

# 安装预测分析引擎

KaiwuDB 预测分析引擎的安装依赖于以下组件：

- [Kubernetes](https://kubernetes.io/)
- [Kubeflow](https://www.kubeflow.org/)
- [KServe](https://kserve.github.io/website/)

KaiwuDB 预测分析引擎的安装包包含 Kubernetes、Kubeflow、KServe 以及可能需要的其他依赖。KaiwuDB 预测分析引擎安装脚本按需安装前置依赖。

## 安装准备

### 环境要求

下表列出安装 KaiwuDB 预测分析引擎所需的环境和依赖：

| 环境和依赖   | 要求                                                                                                                                                                      |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 硬件环境     | - CPU：最低 16 核，推荐 64 核及以上、x86 架构 <br >- 内存：最低 32 GB，推荐 64 GB 及以上 <br >- 可用硬盘空间：最低 60 GB，推荐 200 GB 及以上                                              |
| 操作系统     | - Ubuntu 20.04 <br >- Ubuntu 22.04                                                                                                                                                    |
| 软件环境依赖 | - K3s：v1.29.2+k3s1 <br >- Kubeflow Pipelines：v2.0.5 <br >- KServe：0.12 <br >- NGINX Ingress Controller：管理 KaiwuDB 预测分析引擎的网络 |
| 网络         | NGINX Ingress Controller 端口：KWDB 服务外部访问端口，默认为 `31000`。                                                                                            |

### 离线安装包

KaiwuDB 预测分析引擎支持离线安装。

KaiwuDB 预测分析引擎安装包名称以 `kaiwudb_aiengine-2.0.x` 开头，共计 28 个组件，提供安装所需的镜像、资源清单、环境检查脚本以及安装脚本。

安装包解压并合并后的文件结构如下：

```text
kaiwudb-ml-installer-amd64.tar.gz
├── images                                # 镜像文件
│   ├── inferencing-service-amd64.tar.gz  # 预测分析引擎推理服务镜像
│   ├── ingress-nginx-amd64.tar.gz        # Ingress Nginx 镜像
│   ├── k3s-airgap-images-amd64.tar.gz    # K3s 镜像
│   ├── kserve-amd64.tar.gz               # KServe 镜像
│   ├── kubeflow-amd64.tar.gz             # Kubeflow 镜像
│   ├── training-service-amd64.tar.gz     # 训练服务镜像
│   └── README.md                         # 镜像说明文档
├── k3s                     # K3s 相关文件
│   ├── k3s                 # K3s 可执行文件
│   └── install.sh          # K3s 安装脚本
├── manifests               # Kubernetes 资源定义文件
│   ├── cert-manager.yaml   # Cert-Manager 资源定义文件
│   ├── ingress-nginx.yaml  # Ingress Nginx 资源定义文件
│   └── kserve.yaml         # KServe 资源定义文件
├── install.sh              # 安装脚本
├── manifests-generator.sh  # 资源定义文件生成脚本
├── prerequisite-ins.sh     # 前置依赖检查脚本
├── utils.sh                # 工具脚本
└── uninstall.sh            # 卸载脚本
```

### 证书

安装配置 KaiwuDB 预测分析引擎时，用户需要提供由同一个 CA 证书签名的 KWDB 节点证书。

1. 为用户创建证书。默认情况下，证书保存至 `../certs` 目录。

    ::: warning 说明

    - 为了避免冲突，预测分析引擎证书需要与 KWDB 安装证书存放在不同位置。
    - 建议将预测分析引擎和安装包放在不同的目录，以免删除安装包时误删证书。

    :::

    配置示例：

    ```shell
    ./setup_cert_file.sh root
    ./setup_cert_file.sh kwdbmlusr
    ./setup_cert_file.sh kwdbmlusr01
    ```

2. 创建数据库节点，指定数据库所在主机的 IP 地址（`host_ip`）、预测分析引擎的域名（`ml-domain-name`）、证书和 CA 私钥的路径。

    ::: warning 说明

    - 预测分析引擎不支持使用 IP 地址签发证书。因此证书中必须包含部署预测分析服务的域名。如果没有公网域名，支持使用局域网的私有域名。
    - 签发证书时，必须使用 KWDB 证书签发私钥。默认情况下，私钥的存储路径为 `/etc/kaiwudb/certs/ca.key`。

    :::

    配置示例：

    ```shell
    ./kwbase cert create-node \ 
      localhost \  
      127.0.0.1 \
      ${host_ip} \
      ${ml-domain-name} \
      mlagent-service.kwml-system \
      mlagent-service.kwml-system.svc.cluster.local \
      --certs-dir=${path-to-certs-directory} \
      --ca-key=${path-to-ca-key}
    ```

3. 启动数据库。如果执行上述步骤前已经启动数据库，则需要重启数据库。
4. 初始化相关用户、设置预测分析引擎的域名及端口、授予用户操作数据库和表所需的权限。

    ::: warning 说明
    示例中的 [www.mlagent.com](http://www.mlagent.com:31000) 是预测分析引擎的域名及默认端口。用户可以根据实际情况修改相关配置。
    :::

    配置示例：

    ```shell
    ./kwbase sql --user=root --certs-dir="../certs" --host="${ip}:${port}" -e "
    SET CLUSTER SETTING ml.agent.addr='[www.mlagent.com](http://www.mlagent.com:31000';) 
    create user kwdbmlusr with password NULL; 
    create user kwdbmlusr01 with password 'kwdbml#1234'; 
    grant select on table system.ml_jobs to kwdbmlusr; 
    grant update on table system.ml_jobs to kwdbmlusr; 
    grant select on table system.ml_models to kwdbmlusr; 
    grant update on table system.ml_models to kwdbmlusr; 
    grant select on table system.ml_model_versions to kwdbmlusr; 
    grant update on table system.ml_model_versions to kwdbmlusr; 
    "
    ```

## 安装

预测分析引擎的安装包括 Kubernetes、Kubeflow、KServe 和预测分析引擎的推理和训练服务的安装。

步骤：

1. 解压离线安装包并进入 `kaiwudb-ml-installer` 目录。

    ```shell
    cat kaiwudb_aiengine-2.0.x-x86_64.tar.gz* | tar -xzv 
    cd kaiwudb-ml-installer
    ```

2. 执行 `install.sh` 脚本。

    ```shell
    ./install.sh
    ```

    执行成功后，控制台输出以下信息：

    ```shell
    Start to install KaiwuDB ML Services v1.0.0
    ```

3. 指定预测分析引擎的主机名，默认为 `localhost`。主机名应与准备证书时指定的预测分析引擎的域名（`ml-domain-name`）保持一致。这适用于预测分析引擎与 KWDB 数据库部署在同一服务器的场景。

    配置示例：

    ```shell
    Please input the hostname to access the KaiwuDB ML Services, default is 'localhost': <www.mlagent.com>
    ```

4. 指定预测分析引擎的端口号，默认为 `31000`。端口号应与准备证书时指定的预测分析引擎的端口号保持一致。

    配置示例：

    ```shell
    Please input the port used by the KaiwuDB ML Services, default is '31000': <31000>
    ```

5. 指定证书的存放位置，默认为 `certs`。证书的存放位置应与准备证书时指定的证书的存放位置保持一致。

    配置示例：

    ```shell
    Please input the directory for the certification files, default is 'certs': </path/to/kwdbml/certs>
    ```

6. 指定临时目录位置，保存部署模型的信息。默认为 `/kaiwudb-ml`。

    配置示例：

    ::: warning 说明
    存储目录的剩余空间至少为 60 GB。
    :::

    ```shell
    Please input the metadata store path, default is '/kaiwudb-ml': </kaiwudb-ml>
    ```

    用户输入配置项后，安装脚本首先检查用户环境中是否已经安装 Kubernetes、Kubeflow、KServe。如未安装，安装脚本会依次安装 Kubernetes、Kubeflow、KServe、预测分析引擎的推理服务和训练服务并实时输出安装详情。如已安装，安装脚本直接安装预测分析引擎的推理服务和训练服务，并输出安装详情。
    安装完成后，安装脚本检查预测分析引擎的状态，确保安装成功。一旦安装成功，系统输出安装成功信息。

    配置示例：

    ```shell
    Checking the installation options ...
    [DONE] Installation options are OK.
    Generating the manifests used by KaiwuDB ML Services ...
    [DONE] All manifests are generated successfully.
    Checking the k3s environment ...
    Installing k3s ...
    ......
    [INFO]  Skipping k3s download and verify
    [INFO]  Skipping installation of SELinux RPM
    [INFO]  Creating /usr/local/bin/kubectl symlink to k3s
    [INFO]  Creating /usr/local/bin/crictl symlink to k3s
    [INFO]  Skipping /usr/local/bin/ctr symlink to k3s, command exists in PATH at /usr/bin/ctr
    [INFO]  Creating killall script /usr/local/bin/k3s-killall.sh
    [INFO]  Creating uninstall script /usr/local/bin/k3s-uninstall.sh
    [INFO]  env: Creating environment file /etc/systemd/system/k3s.service.env
    [INFO]  systemd: Creating service file /etc/systemd/system/k3s.service
    [INFO]  systemd: Enabling k3s unit
    Created symlink /etc/systemd/system/multi-user.target.wants/k3s.service → /etc/systemd/system/k3s.service.
    [INFO]  systemd: Starting k3s
    Checking the kubernetes environment ...
    [DONE] Kubernetes is ready.
    Checking the Ingress Nginx controller ...
    Installing ingress-nginx ...
    ......
    Tagging ingress-nginx images ...
    ......
    Ingress-nginx was successfully installed!
    Checking the KServe environment ...
    Installing KServe ...
    ......
    Tagging KServe images ...
    ......
    Installing Inferencing Service ...
    ......
    Installing Training Service ...
    ......
    Checking the KaiwuDB ML inferencing service status ...
    pod/grpc-kagent-9ddc64585-dw5h6 condition met
    Inferencing service was successfully installed.
    ```

## 卸载

KaiwuDB 预测分析引擎安装包提供 `uninstall.sh` 脚本，用于自动卸载预测分析引擎。

::: warning 说明
支持使用 `uninstall.sh --help` 命令查看卸载选项。默认情况下，只卸载预测分析引擎。
:::

```shell
./uninstall.sh
```
