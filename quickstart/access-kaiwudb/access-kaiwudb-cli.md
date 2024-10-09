---
title: 使用 kwbase CLI 工具连接 KWDB
id: access-kaiwudb-cli
---

# 使用 kwbase CLI 工具连接 KWDB

kwbase 是 KWDB 提供的在命令行下运行的数据库连接工具。用户可以通过此工具连接 KWDB 数据库并对其进行操作和维护。

## 前提条件

- 已部署 KWDB。有关详细信息，参见[单节点裸机部署](../install-kaiwudb/quickstart-bare-metal.md)或[单节点容器部署](../install-kaiwudb/quickstart-docker.md)。
- 配置数据库认证方式（只适用于安全模式连接）。

## 非安全模式连接

以下示例说明如何以非安全模式登录 KWDB 集群。

```sql
./kwbase sql --insecure --host=<your-host-ip>
```

## 安全模式连接

以下示例说明如何以 TLS 安全模式登录 KWDB 集群。

```sql
./kwbase sql --certs-dir=etc/kwdb/certs --host=<your-host-ip>
```
