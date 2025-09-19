---
title: Real-time Compression
id: compression-sql
---


# Real-time Compression

Real-time compression is designed for data compression that requires fast response. It is suitable for data migration or situations where you want to release space instantly. You can manually run the `COMPRESS` statement to compress all time-series data, data under a specified time-series database, or data of a specified time-series table. The system will immediately compress all eligible data segments.

::: warning Note
Currenty, the `COMPRESS` statement is not available for relational databases.
:::

## Privileges

The user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

## Syntax

![](../../../static/sql-reference/compress.png)

## Parameters

| Parameter | Description |
| --- | --- |
| `database_name` | The name of the time-series database to compress. |
| `table_name` | The name of the time-series table to compress. You can use `<database_name>.<table_name>` to specify a table in another database. If not specified, use the table in the current database.|

## Examples

These examples assume that you have created the `sensor_data` and `device_data` time-series databases as well as `temperature` and `pressure` tables under the `device_data` database, and inserted data into these tables.

- Compress a single table under a specified database.

    ```sql
    COMPRESS TABLE sensor_data.temperature;
    ```

- Compress all tables under a specified database.

    ```sql
    COMPRESS DATABASE sensor_data;
    ```

- Compress all databases.

    ```sql
    COMPRESS ALL DATABASES;
    ```
