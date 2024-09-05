---
title: 迁移准备
id: before-migration
---

# 迁移准备

- 部署环境
  - Linux 系统环境。
  - [安装 Java](https://docs.oracle.com/en/java/javase/22/install/overview-jdk-installation.html)（1.8 及以上版本）。
  - [安装 Python](https://www.python.org/downloads/)（2.X 或 3.X）。
  - [安装 Maven](https://maven.apache.org/install.html)（3.6 及以上版本）。
  - [安装 DataX 3.0](https://gitee.com/mirrors/DataX/blob/master/userGuid.md)。
- 工具
  - 获取 KaiwuDB 数据库迁移工具 KaiwuDB DataX Utils 的安装包（`kaiwudb-datax-utils-2.0.4.jar`）。
  - 获取 KaiwuDB DataX 插件压缩包。
- 数据库及权限设置
  - 安装并启动源数据库和目标数据库，创建需要读取和写入数据的数据库和数据表。
    ::: warning 说明
    如果目标数据库是 KWDB 数据库或者 TDengine 数据库，用户可以在配置文件中使用 `preSql[]` 参数创建待写入的数据表。
    :::
  - 用户拥有源数据库和目标数据库的操作权限，包括数据库的创建权限、表数据的读取和写入权限。
