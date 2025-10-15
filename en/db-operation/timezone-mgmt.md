---
title: Time Zone Management
id: timezone-mgmt
---

# Time Zone Management

You can use the `SET TIME ZONE` SQL statement to modify the time zone of the current session.

## Privileges

No privileges required.

## Synopsis

```sql
SET TIME ZONE [ <int> | '<location>'];
```

## Parameters

| Parameter | Description |
| --- | --- |
| `int` | The time difference from UTC, ranging from `[-12, 14]` (UTC-12 to UTC+14).|
| `location` | The name of the time zone, such as `Asia/Shanghai`.|

## Examples

1. Set the session's time zone to UTC+8.

    ```sql
    SET TIME ZONE 8;
    ```

2. Verify the time zone setting:

    ```sql
    SHOW TIME ZONE;
    timezone

    ---
    8
    (1 row)
    ```
