---
title: Time Zone Management
id: timezone-mgmt
---

# Time Zone Management

You can use the `SET TIME ZONE` SQL statement to modify the time zone of the current session.

You can use the `SET CLUSTER SETTING cluster.connection.timezone` SQL statement to configure the cluster's time zone

## Privileges

No privileges required.

## Syntax

```sql
SET TIME ZONE [ '<int>' | '<location>'];
```

```sql
SET CLUSTER SETTING cluster.connection.timezone =  [ '<int>' | '<location>'| '<ISO 8601>'| '<''>or<default>']
```

## Parameters

| Parameter | Description |
| --- | --- |
| `int` | The time difference from UTC, ranging from `[-12, 14]` (UTC-12 to UTC+14).|
| `location` | The name of the time zone, such as `Asia/Shanghai`.|
| `ISO 8601` | The ISO 8601 format representation corresponding to the cluster's time zone, for example `+8:00`。|
| `null or default` | The default time zone for clusters is UTC.|

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
 The following example sets the time zone of the current cluster to the default value.

1. Set the time zone of the current cluster to the default value:

    ```sql
    SET CLUSTER SETTING cluster.connection.timezone = default;
    ```
2. Check whether the cluster time zone has been set successfully:

    ```sql
    SHOW CLUSTER SETTING cluster.connection.timezone;
      cluster.connection.timezone
    ------------------
    UTC
    (1 row)
    ```