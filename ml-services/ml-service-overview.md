---
title: 预测分析引擎概述
id: ml-service-overview
---

# 预测分析引擎概述

::: warning 说明
目前，预测分析引擎是企业版特性。如需了解预测分析引擎的更多详细信息，[联系](https://cs.kaiwudb.com/support/) KWDB 技术支持人员。
:::

KaiwuDB 在多模数据库基础上开发了预测分析引擎，用于提供从模型导入、模型训练、模型预测、模型评估到模型更新的全生命周期管理能力。任何具备数据库应用开发背景的应用开发人员都可以轻松地导入、训练、预测、评估、更新模型。

KaiwuDB 预测分析引擎支持社区活跃的主流机器学习框架，包括 [scikit-learn](https://scikit-learn.org/stable/index.html)、[XGBoost](https://xgboost.readthedocs.io/en/stable/#)、[LightGBM](https://lightgbm.readthedocs.io/en/latest/index.html#) 和 [TensorFlow](https://tensorflow.google.cn/?hl=zh-cn)。除了原生的框架支持，KaiwuDB 预测分析引擎也具备扩展能力。用户不仅可以部署 KWDB 自带的机器学习运行环境，还可以建立自定义的运行环境，满足不同项目的需要。

KaiwuDB 预测分析引擎支持用户通过 SQL 语句进行管理和预测分析模型，也支持用户下载、安装基于 WEB 界面的图形化管理工具管理模型和进行预测分析。基于 WEB 界面的图形化管理工具为可选安装组件，建议将基于 WEB 界面的图形化管理工具与预测分析引擎安装在同一设备。

本节包含以下内容：

- [预测分析引擎架构](./ml-service-architecture.md)
- [模型导入和预测流程](./ml-service-workflow.md)
- [安装预测分析引擎](./ml-service-install.md)
- 文件准备
  - [预测流程简介](./prepare-files/predict-workflow.md)
  - [训练数据预处理](./prepare-files/prepare-data.md)
  - [模型文件](./prepare-files/prepare-model-files.md)
  - [流水线文件](./prepare-files/prepare-pipeline-files.md)
- 基于 SQL 函数的预测分析
  - 模型和流水线管理
    - [导入模型和流水线](./sql-based-ml-service/model-pipeline-mgmt/import-model-pipeline.md)
    - [训练和评估模型](./sql-based-ml-service/model-pipeline-mgmt/train-evaluate-models.md)
    - [设置模型的活跃版本](./sql-based-ml-service/model-pipeline-mgmt/set-active-model-versions.md)
    - [预测分析模型](./sql-based-ml-service/model-pipeline-mgmt/predict-analyze-models.md)
    - [查看模型和流水线](./sql-based-ml-service/model-pipeline-mgmt/check-model-pipeline.md)
    - [删除模型和流水线](./sql-based-ml-service/model-pipeline-mgmt/delete-model-pipeline.md)
  - [作业管理](./sql-based-ml-service/job-mgmt.md)
  - 权限管理
    - [模型权限管理](./sql-based-ml-service/privilege-mgmt/model-privilege-mgmt.md)
    - [训练流水线权限管理](./sql-based-ml-service/privilege-mgmt/pipeline-privilege-mgmt.md)
- 基于 WEB 界面的预测分析
  - [工具准备](./web-based-ml-service/prepare-tools.md)
  - [模型管理](./web-based-ml-service/model-mgmt.md)
  - [训练流水线管理](./web-based-ml-service/pipeline-mgmt.md)
  - [作业管理](./web-based-ml-service/job-mgmt.md)
- [故障排查](./ml-service-troubleshooting.md)
- [参考信息](./ml-service-reference.md)
