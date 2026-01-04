---
title: VACUUM
id: vacuum-sql
---

# VACUUM

When you need to immediately free up storage space or optimize query performance for time-series data, you can manually trigger a reorganization operation using the `VACUUM TS DATABASES;` command.

This command is particularly useful in the following scenarios:

- Freeing Space After Deleting Data or Dropping Tables: After executing DELETE or DROP operations, immediately remove deleted data to quickly reclaim storage space
- Data Organization After Bulk Writes: After large batch data writes, organize and sort data files to improve subsequent query performance

## Privileges

N/A

## Syntax

![](../../../static/sql-reference/vacuum.png)

## Parameters

N/A

## Examples

The following examples demonstrate how to use the VACUUM command to free up storage space or optimize query performance.

- Free up storage space

    ```sql
    -- Execute delete operation
    DELETE FROM sensor_data WHERE ts < '2024-01-01';

    -- Immediately reorganize to reclaim storage space
    VACUUM TS DATABASES;
    ```

- Optimize query performance

    ```sql
    -- Bulk write data from multiple devices
    INSERT INTO sensor_data VALUES
        (NOW(), 25.5, 60.2, 101, 'temperature'),
        (NOW(), 26.1, 58.7, 102, 'temperature'),
        (NOW(), 24.8, 62.1, 103, 'temperature'),
        ...;

    -- Immediately reorganize to optimize data organization and improve query performance
    VACUUM TS DATABASES;
    ```