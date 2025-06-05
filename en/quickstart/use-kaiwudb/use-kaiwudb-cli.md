---
title: Using the kwbase CLI Tool
id: use-kwbase-cli
---

# Manage KWDB Using the kwbase CLI Tool

This section explains how to use the kwbase CLI tool to manage your KWDB databases. You'll learn how to work with both time-series and relational data through practical examples.

## Time-Series Data

1. Create a time-series database.

   The following command creates a time-series database named `sensor_data`:

   ```sql
   CREATE TS DATABASE sensor_data;
   ```

2. Create a time-series table.

    The following command creates a time-series table named `readings` in the `sensor_data` database. This table will store timestamped temperature and humidity readings, with tags for sensor ID and location.

    ```sql
    CREATE TABLE sensor_data.readings (
        ts timestamp NOT NULL,         -- Timestamp for when the reading was taken
        temperature FLOAT,             -- Temperature reading in Celsius
        humidity FLOAT                 -- Humidity reading in percentage
    ) TAGS (
        sensor_id INT NOT NULL,        -- Unique ID for each sensor
        location CHAR(256) NOT NULL    -- Location of the sensor (e.g., "Room 101")
    ) PRIMARY TAGS(sensor_id);
    ```

3. Insert time-series data.

    ```sql
    INSERT INTO sensor_data.readings 
    VALUES 
    (NOW(), 23.0, 59.5, 101, 'Room 101'),
    (NOW(), 23.5, 58.9, 102, 'Room 102'),
    (NOW(), 19.8, 65.5, 103, 'Room 103');
    ```

4. Query time-series data.

    ```sql
    SELECT * FROM sensor_data.readings;
                ts               | temperature | humidity | sensor_id | location
    ------------------------------+-------------+----------+-----------+-----------
    2024-12-16 07:37:30.584+00:00 |          23 |     59.5 |       101 | Room 101
    2024-12-16 07:37:30.584+00:00 |        23.5 |     58.9 |       102 | Room 102
    2024-12-16 07:37:30.584+00:00 |        19.8 |     65.5 |       103 | Room 103
    (3 rows)
    ```

## Relational Data

1. Create a relational database.

    The following command creates a relational database named `rdb`.

    ```sql
    CREATE DATABASE rdb;
    ```

2. Create a relational table.

    The following command creates a relational table named `accounts` in the `rdb` database.  This table will store customer account information.

    ```sql
    CREATE TABLE rdb.accounts (
        id INT8 DEFAULT unique_rowid() PRIMARY KEY,  -- Auto-generating unique ID
        name STRING,                                 -- Customer name
        balance DECIMAL,                             -- Account balance
        enabled BOOL                                 -- Account status
    );
    ```

3. Insert relational data.

    ```sql
    INSERT INTO rdb.accounts 
    VALUES 
    (1, 'Lily', 10000.5, true), 
    (2, 'Ruarc', 20000.75, true), 
    (3, 'Tullia', 30000.0, false), 
    (4, 'Arturo', 45000.0, false);
    ```

4. Query relational data.

    ```sql
    SELECT * FROM rdb.accounts;
    id | name  | balance | enabled
    ---+-------+---------+--------
    1  | Lily  | 10000.5 | true
    2  | Ruarc | 20000.75| true
    3  | Tullia| 30000   | false
    4  | Arturo| 45000   | false
    (4 rows)
    ```