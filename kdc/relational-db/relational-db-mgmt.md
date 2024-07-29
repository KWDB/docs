---
title: 数据库管理
id: relational-db-mgmt
---

# 数据库管理

KaiwuDB 开发者中心支持创建、编辑、查看、重命名和删除关系数据库。

## 创建数据库

### 前提条件

用户拥有 DATABASE CREATE 或 ALL 权限。

### 步骤

如需创建关系数据库，遵循以下步骤。

1. 在数据库导航区，右键单击**关系数据库**，然后选择**新建关系数据库**。

    ![](../../static/kdc/create-relational-db.png)

2. 在**创建数据库**窗口，填写数据库名称，然后单击**确定**。

    ![](../../static/kdc/create-relational-db-02.png)

    创建成功后，新建数据库将自动显示在数据库导航区内，继承 KWDB 数据库系统的角色和用户设置。

    ![](../../static/kdc/create-relational-db-03.png)

## 编辑数据库

### 前提条件

用户拥有 DATABASE CREATE 或 ALL 权限。

### 步骤

如需编辑关系数据库，遵循以下步骤。

1. 在数据库导航区，右键单击需要修改的数据库，然后选择**编辑关系数据库**。

    ![](../../static/kdc/edit-relational-db-01.png)

2. 修改数据库名称和描述信息，然后单击**保存**。

    ![](../../static/kdc/edit-relational-db-02.png)

3. 在**执行修改**对话框，确认 SQL 语句无误，然后单击**执行**。

    ![](../../static/kdc/edit-relational-db-03.png)

## 查看数据库

在数据库导航区，双击需要查看的数据库，即可在对象窗口查看数据库的名称、描述信息、模式、角色和用户、设置以及权限信息。

![](../../static/kdc/view-relational-db.png)

## 删除数据库

### 前提条件

- 用户拥有 DATABASE DROP 权限。
- 要删除的数据库不是当前使用的数据库。

### 步骤

如需删除关系数据库，遵循以下步骤。

1. 在数据库导航区，右键单击需要删除的数据库，然后选择**删除**。

    ![](../../static/kdc/delete-relational-db-01.png)

2. 在**删除对象**窗口中，单击**是**。删除成功后，系统将自动更新导航栏菜单。

    ![](../../static/kdc/delete-relational-db-02.png)

## 重命名数据库

### 前提条件

- 用户为 Admin 用户或者 Admin 角色成员。
- 待重命名数据库不是当前使用的数据库。

### 步骤

如需重命名关系数据库，遵循以下步骤。

1. 在数据库导航区，右键单击需要重命名的数据库，然后选择**重命名**。

    ![](../../static/kdc/rename-relational-db-01.png)

2. 在**重命名**窗口，设置新的数据库名称，然后单击**确定**。

    ![](../../static/kdc/rename-relational-db-02.png)

3. 在**重命名脚本**窗口，确认新数据库名称无误，然后单击**执行**。
