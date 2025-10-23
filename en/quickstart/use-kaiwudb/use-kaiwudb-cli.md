---
title: Using the kwbase CLI Tool
id: use-kaiwudb-cli
---

# Manage KWDB Using the kwbase CLI Tool

This section demonstrates how to use kwbase CLI to manage KWDB multi-model database through monitoring scenarios, including:

- **Relational Data Operations**: Managing relatively static data, such as device information and user profiles
- **Time-Series Data Operations**: Processing time-varying dynamic data, such as sensor readings and monitoring metrics
- **Cross-Model Queries**: Performing queries across relational and time-series databases for comprehensive multi-model data analytics

## Relational Data Operations

1. Create a database and table.

    1. Create and use a relational database:

        ```sql
        -- Create a relational database
        CREATE DATABASE device_info;
        -- Switch to the specified database
        USE device_info;
        ```

    2. Create a base table:

        ```sql
        CREATE TABLE devices (
            device_id INT PRIMARY KEY,        -- Device ID
            device_name VARCHAR NOT NULL,     -- Device name
            location VARCHAR,                 -- Location
            status VARCHAR DEFAULT 'active'   -- Status
        );
        ```

2. Insert data in batch:

    ```sql
    -- Insert device data in batch
    INSERT INTO devices VALUES
        (101, 'Sensor A', 'Server Room 1', 'active'),
        (102, 'Sensor B', 'Server Room 2', 'active'),
        (103, 'Sensor C', 'Server Room 1', 'active');
    ```

3. Verify data with queries:

    ```sql
    -- Query all device information
    SELECT * FROM devices;
    ```

    Expected output:

    ```sql
    device_id | device_name | location      | status
    ----------+-------------+---------------+--------
        101 | Sensor A    | Server Room 1 | active
        102 | Sensor B    | Server Room 2 | active
        103 | Sensor C    | Server Room 1 | active
    ```

## Time-Series Data Operations

Time-series tables have specific structural requirements:

- **Timestamp column**: Must be the first column in the table
- **Tags**: Used to identify static device attributes
- **Primary tags**: Used to distinguish different entity objects

The following example demonstrates basic time-series operations using real-time sensor data.

1. Create a time-series database and table.

    1. Use the `TS` keyword to create a time-series database:

        ```sql
        -- Create a time-series database
        CREATE TS DATABASE monitoring;
        -- Switch to the time-series database
        USE monitoring;
        ```

    2. Create a time-series table:

        ```sql
        CREATE TABLE sensor_data (
            ts TIMESTAMP NOT NULL,            -- Timestamp (must be the first column)
            temperature FLOAT,                -- Temperature
            humidity FLOAT                    -- Humidity
        ) TAGS (
            device_id INT NOT NULL,           -- Device ID (tag)
            sensor_type VARCHAR NOT NULL      -- Sensor type (tag)
        ) PRIMARY TAGS(device_id);            -- Primary tag
        ```

2. Insert data:

    ```sql
    -- Insert sensor data with current timestamp
    INSERT INTO sensor_data VALUES
        (NOW(), 25.5, 60.2, 101, 'temperature'),
        (NOW(), 26.1, 58.7, 102, 'temperature'),
        (NOW(), 24.8, 62.1, 103, 'temperature');
    ```

3. Query data:

    ```sql
    -- Query the latest 5 sensor readings, ordered by timestamp in descending order
    SELECT * FROM sensor_data 
    ORDER BY ts DESC 
    LIMIT 5;
    ```

    Expected output:

    ```sql
            ts                    | temperature | humidity | device_id | sensor_type
    -------------------------------+-------------+----------+-----------+-------------
    2025-08-01 10:30:15.123+00:00 |        24.8 |     62.1 |       103 | temperature
    2025-08-01 10:30:15.123+00:00 |        26.1 |     58.7 |       102 | temperature
    2025-08-01 10:30:15.123+00:00 |        25.5 |     60.2 |       101 | temperature
    ```

## Cross-Model Queries

A core advantage of KWDB is its support for queries across time-series and relational databases, enabling comprehensive multi-model data analytics.

- Query device information with the latest monitoring data.

    ```sql
    -- Query combining device information with the latest monitoring data
    -- Use DISTINCT ON to retrieve the most recent record for each device
    SELECT 
        d.device_name,           -- Device name
        d.location,              -- Device location
        s.temperature,           -- Latest temperature
        s.humidity,              -- Latest humidity
        s.ts as last_update      -- Last update time
    FROM device_info.devices d
    JOIN (
        -- Subquery: Retrieve the latest monitoring data for each device
        SELECT DISTINCT ON (device_id) 
            device_id, temperature, humidity, ts
        FROM monitoring.sensor_data 
        ORDER BY device_id, ts DESC
    ) s ON d.device_id = s.device_id
    WHERE d.status = 'active'    -- Only query active devices
    ORDER BY d.device_id;
    ```

    Expected output:

    ```sql
    device_name | location      | temperature | humidity |        last_update
    ------------+---------------+-------------+----------+---------------------------
    Sensor A    | Server Room 1 |        25.5 |     60.2 | 2025-08-01 10:30:15.123+00:00
    Sensor B    | Server Room 2 |        26.1 |     58.7 | 2025-08-01 10:30:15.123+00:00
    Sensor C    | Server Room 1 |        24.8 |     62.1 | 2025-08-01 10:30:15.123+00:00
    ```

- Calculate average temperature and humidity by location.

    ```sql
    -- Calculate average temperature and humidity by device location for the last hour
    SELECT 
        d.location,                      -- Device location
        COUNT(*) as device_count,        -- Number of devices at this location
        AVG(s.temperature) as avg_temp,  -- Average temperature
        AVG(s.humidity) as avg_humidity  -- Average humidity
    FROM device_info.devices d
    JOIN monitoring.sensor_data s ON d.device_id = s.device_id
    WHERE s.ts > NOW() - INTERVAL '1 hour'  -- Filter data from the last hour
    GROUP BY d.location                     -- Group by location
    ORDER BY d.location;
    ```

    Expected output:

    ```sql
    location      | device_count | avg_temp | avg_humidity
    --------------+--------------+----------+--------------
    Server Room 1 |            2 |     25.2 |         61.2
    Server Room 2 |            1 |     26.1 |         58.7
    ```