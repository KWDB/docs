---
title: 时区管理
id: timezone-mgmt
---

# 时区管理

`SET TIME ZONE` 语句用于修改当前会话的时区。

## 语法格式

```sql
SET TIME ZONE [ <int> | '<location>'];
```

## 参数说明

| 参数 | 说明 |
| --- | --- |
| `int` | 相对于 UTC 时区的时差。取值范围为 `[-12, 14]`，表示 UTC-12 时区到 UTC+14 时区。|
| `location` | 时区对应的城市名称，例如 `Asia/Shanghai`。|

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
