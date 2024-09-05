---
title: 连接 KWDB 数据库
id: kdc-db-connect
---

# 连接数据库

本文档假设用户已经[安装 KaiwuDB 开发者中心](./kdc-install.md)。

首次建立连接或软件中的所有连接都被删除后，软件启动后会自动弹出**新建连接**向导，引导用户建立连接。

<img src="../static/kdc/database-connect.png" alt="数据库连接" style="zoom: 50%;" />

其他情况下，如需创建连接，可以选择以下任一操作：

- 单击工具栏或数据库导航区工具栏中的**新建连接**按钮。

    <img src="../static/kdc/new-connect-button.png" style="zoom: 67%;" />

- 在菜单栏中，单击**数据库**，然后从下拉菜单中选择**新建连接**。

    <img src="../static/kdc/new-connect.png" style="zoom:67%;" />

## 新建连接

以下步骤以首次建立连接为例，说明如何连接数据库。

1. 在**创建新连接**窗口，选择 KaiwuDB 驱动，然后单击**下一步**。

    <img src="../static/kdc/create-connect-01.png" style="zoom: 50%;" />

2. 在**常规**页签，设置主机、端口、数据库、用户和密码。

    <img src="../static/kdc/create-connect-02.png" style="zoom:67%;" />

3. （可选）勾选**显示非缺省的数据库**，显示所有数据库。默认情况下，只显示指定连接的数据库。
4. （可选）单击**测试链接**，检查连接是否成功。

5. 单击**完成**。

## SSH 登录

如需使用 SSH 连接数据库，遵循以下步骤。

1. 单击工具栏或数据库导航区工具栏中的**新建连接**按钮，或者在菜单栏中单击**数据库** > **新建连接**。
2. 在**创建新连接**窗口，选择 KaiwuDB 驱动，然后单击**下一步**。

    <img src="../static/kdc/create-connect-01.png" style="zoom:67%;" />

3. 在**常规**页签，填写要连接的数据库名称，用户名及密码。主机和端口使用系统默认值。

    <img src="../static/kdc/create-connect-02.png" style="zoom:60%;" />

4. （可选）勾选**显示非缺省的数据库**，显示所有数据库。默认情况下，只显示指定连接的数据库。
5. 在 **SSH** 页签，勾选**使用 SSH 通道**，设置主机地址、端口、用户名和密码。

    <img src="../static/kdc/ssh-login-01.png" style="zoom:67%;" />

6. （可选）单击**测试链接**，检查连接是否成功。

7. 单击**完成**。

## Proxy

如需使用 Proxy 连接数据库，遵循以下步骤。

1. 单击工具栏或数据库导航区工具栏中的**新建连接**按钮，或者在菜单栏中单击**数据库** > **新建连接**。
2. 在**创建新连接**窗口，选择 KaiwuDB 驱动，然后单击**下一步**。

    <img src="../static/kdc/create-connect-01.png" style="zoom:67%;" />

3. 在**常规**页签，填写数据库名称、用户名及密码。主机和端口使用系统默认值。

    <img src="../static/kdc/create-connect-02.png" style="zoom:67%;" />

4. （可选）勾选**显示非缺省的数据库**，显示所有数据库。默认情况下，只显示指定连接的数据库。
5. 在 **Proxy** 页签，勾选**使用 SOCKS 代理**，设置主机地址、端口、用户名和密码。

    <img src="../static/kdc/proxy-login-01.jpg" style="zoom:67%;" />

6. （可选）单击**测试链接**，检查连接是否成功。

7. 单击**完成**。

## SSL 登录

### 前提条件

- 已经获取 `ca.crt`和 `client.<user>.crt` 文件。
- 已经使用 OpenSSL 命令将 `client.<user>.key` 文件转换为 `.pk8` 格式。

::: warning 说明
如果选择启用安全模式 安装部署 KWDB，系统自动生成 `ca.crt` 和 `client.<user>.crt` 文件。文件的存储目录是 `/etc/kwdb/certs/`。
:::

### 步骤

如需使用 SSL 连接数据库，遵循以下步骤。

1. 单击工具栏或数据库导航区工具栏中的**新建连接**按钮，或者在菜单栏中单击**数据库** > **新建连接**。
2. 在**创建新连接**窗口，选择 KaiwuDB 驱动，然后单击**下一步**。

    <img src="../static/kdc/create-connect-01.png" style="zoom:67%;" />

3. 在**常规**页签，填写主机地址、端口号、数据库名称、用户名及密码。

    <img src="../static/kdc/create-connect-02.png" style="zoom:67%;" />

4. （可选）勾选**显示非缺省的数据库**，显示所有数据库。默认情况下，只显示指定连接的数据库。
5. 在 **SSL** 页签，勾选**使用 SSL**，添加根证书、SSL 证书和 SSL 证书密钥。

    <img src="../static/kdc/ssl-login-01.png" style="zoom:67%;" />

6. （可选）单击**测试链接**，检查连接是否成功。

7. 单击**完成**。
