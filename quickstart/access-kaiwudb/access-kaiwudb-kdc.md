---
title: 使用 KaiwuDB 开发者中心连接 KWDB
id: access-kaiwudb-kdc
---

# 使用 KaiwuDB 开发者中心连接 KWDB

安装部署完 KWDB 以后，用户可以使用 [KaiwuDB Developer Center（KaiwuDB 开发者中心）](../../kaiwudb-developer-center/overview.md)连接和管理 KWDB。本文介绍如何使用 KaiwuDB 开发者中心可视化工具连接 KWDB 数据库。

## 安装 KaiwuDB 开发者中心

本节介绍 KaiwuDB 开发者中心支持的操作系统、环境要求，以及如何安装 KaiwuDB 开发者中心。

### 支持的操作系统

::: warning 说明
不同操作系统版本的界面略有差异，但功能完全相同。
:::

KaiwuDB 开发者中心支持以下操作系统：

- Windows 7 及以上 64 位系统
- Linux 内核 2.6 及以上系统
- Mac 操作系统（macOS）

### 环境要求

KaiwuDB 开发者中心的安装需满足以下环境要求：

| 环境 | 要求            |
| ----------------------------------- | ---------------------------------------------- |
| 硬件环境                            | - 内存：1G 及以上 <br> - 硬盘: 10G 及以上                |
| 软件环境                            | - KWDB 2.0 及以上版本 <br> - OpenJRE 8 及以上版本 |

### 安装步骤

如需安装 KaiwuDB 开发者中心，遵循以下步骤。

1. 根据操作系统[下载](https://gitee.com/kwdb/kwdb/releases) KaiwuDB 开发者中心对应的安装包。

   ::: warning 提示：

   因文件大小限制，可能需要下载多个安装包。

   :::

2. 合并解压缩安装包，文件目录如下：

   ![安装包](../../static/quickstart/JD1MbIGlXoE7qzxwqOjcc8Wtn4e.png)

3. 双击运行 `KaiwuDB Developer Center.exe` 应用程序。

## 连接 KWDB 数据库

首次建立连接或软件中的所有连接都被删除后，软件启动后会自动弹出**新建连接**向导，引导用户建立连接。

![数据库连接](../../static/quickstart/VfcqbD99roY3zbxdCQdcCRFenBc.png)

其他情况下，如需创建连接，可以选择以下任一操作：

- 单击工具栏或数据库导航区工具栏中的**新建连接**按钮。

  ![](../../static/quickstart/RSxWbFLxYoqf5dxHTHkcpyN3nle.png)

- 在菜单栏中，单击**数据库**，然后从下拉菜单中选择**新建连接**。

  ![](../../static/quickstart/WcrObb1VhorfioxESFJcxGtgnAd.png)

以下步骤以首次建立连接为例，说明如何连接数据库。

1. 在**创建新连接**窗口，选择 KaiwuDB 驱动，然后单击**下一步**。

   ![](../../static/quickstart/FU8sbwC1yoqPchxh3ttcptgan4d.png)

2. 在**常规**页签，设置主机、端口、数据库、用户和密码。

   ![](../../static/quickstart/EQ1UbjSRroq00Ix5LdzcapFcnaf.png)

3. （可选）勾选**显示非缺省的数据库**，显示所有数据库。默认情况下，只显示指定连接的数据库。
4. （可选）单击**测试链接**，检查连接是否成功。连接成功后，将显示以下信息：

   ![](../../static/quickstart/TU6nb8Vf1o2gWCxdq1ocIELtnng.png)

5. 单击**确定**。

   数据库导航区将自动更新，显示已连接的数据库。

   ![](../../static/quickstart/TLQcbBq6eoTndRxSYQucuY7bn9e.png)