---
title: 时区管理
id: timezone-mgmt
---

# 时区管理

`SET TIME ZONE` 语句用于修改当前会话的时区。
`SET CLUSTER SETTING cluster.connection.timezone` 语句用于集群时区配置
## 语法格式

```sql
SET TIME ZONE [ '<int>' | '<location>'];
```

```sql
SET CLUSTER SETTING cluster.connection.timezone =  [ '<int>' | '<location>'| '<ISO 8601>'| '<''>或<default>']
```

## 参数说明

| 参数 | 说明 |
| --- | --- |
| `int` | 相对于 UTC 时区的时差。取值范围为 `[-12, 14]`，表示 UTC-12 时区到 UTC+14 时区。|
| `location` | 时区对应的城市名称，例如 `Asia/Shanghai`。|
| `ISO 8601` | 集群时区对应的ISO 8601格式表述，例如，`+8:00`。|
| `空值或default` | 集群时区默认值为UTC时区。|

## 语法示例

以下示例将当前会话的时区设置为 UTC+8。

1. 将当前会话的时区设置为 UTC+8。

    ```sql
    SET TIME ZONE 8;
    ```

2. 查看时区是否设置成功：

    ```sql
    SHOW TIME ZONE;
    timezone

    ---
    8
    (1 row)
    ```
以下示例将当前集群的时区设置为默认值。

1. 将当前集群的时区设置为默认值。

    ```sql
    SET CLUSTER SETTING cluster.connection.timezone = default;
    ```
2. 查看集群时区是否设置成功：

    ```sql
    SHOW CLUSTER SETTING cluster.connection.timezone;
      cluster.connection.timezone
    ------------------
    UTC
    (1 row)
    ```