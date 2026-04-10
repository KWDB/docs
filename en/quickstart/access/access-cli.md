---
title: Using the kwbase CLI Tool
id: access-cli
---

# Using the kwbase CLI Tool

This section explains how to connect to and manage KWDB using kwbase, the built-in command-line interface (CLI) client. You can connect in either insecure mode for testing purposes or secure modes for production environments.

When you deploy KWDB using scripts, the system automatically generates a `kw-sql` helper script and creates a symbolic link in the `/usr/bin` directory. This script wraps the kwbase connection command, allowing the root user to quickly access the database.

## Connect to KWDB

### Quick Login Using the Helper Script

::: warning Note
The `kw-sql` script does not support other users. To connect as a different user, use the kwbase command instead.
:::

**Prerequisites**

KWDB is deployed and started using the `deploy.sh` script.

**Steps**

1. Run the following command from anywhere on the node to connect as root:

    ```shell
    kw-sql
    ```

### Connect Using the kwbase Command

You can also connect directly using the kwbase command. This method lets you specify different users and configure various connection parameters for more flexibility.

::: warning Note
For containerized deployments, use this command format:

```bash
docker exec -it <container-name> ./kwbase sql [security-options] --host=<your-host-ip> [-u <user-name>]
```
:::

#### Insecure Mode

::: warning Note
Use insecure mode only in testing environments.
:::

**Prerequisites**

- KWDB deployed and running in insecure mode

**Steps**

- Connect as the database deployment user.

    ```shell
    ./kwbase sql --insecure --host=<your-host-ip>
    ```

- Create and connect as a regular user.

    1. Connect as the database deployment user.

        ```shell
        ./kwbase sql --insecure --host=<your-host-ip>
        ```

    2. Create a user.

        ```sql
        CREATE USER user1;
        ```

    3. Log out.
    4. Connect as the new user.

        ```shell
        ./kwbase sql --insecure --host=<your-host-ip> -u user1
        ```

#### Secure Mode

The following examples show how administrators and regular users can securely log in to KWDB using a certificate. By default, KWDB supports authentication via certificate or password. For more information on other authentication methods, see [Identity Authentication](../../db-security/identity-authn.md).

**Prerequisites**

- KWDB deployed and running in secure mode

**Steps**

- Connect as the database deployment user.

    ```shell
    ./kwbase sql --certs-dir=<certs-dir> --host=<your-host-ip> 
    ```

- Create and connect as a regular user.
    1. Connect as the database deployment user.

        ```shell
        ./kwbase sql --certs-dir=<certs-dir> --host=<your-host-ip> 
        ```

    2. Create a user.

        ```sql
        CREATE USER user1;
        ```

    3. Log out.
    4. Generate a certificate for the new user.

        ```shell
        ./kwbase cert create-client user1 --certs-dir=<certs-dir> --ca-key=<certs-dir>/ca.key
        ```

    5. Connect as the new user.

        ```shell
        ./kwbase sql --certs-dir=<certs-dir> --host=<your-host-ip> -u user1
        ```

## Manage KWDB

This section demonstrates how to use kwbase CLI to manage KWDB multi-model database through monitoring scenarios, including:

- Relational Data Operations: Managing relatively static data, such as device information and user profiles
- Time-Series Data Operations: Processing time-varying dynamic data, such as sensor readings and monitoring metrics
- Cross-Model Queries: Performing queries across relational and time-series databases for comprehensive multi-model data analytics

### Relational Data Operations

#### Create Relational Database and Table

1. Create and use a relational database:

    ```sql
    -- Create a relational database
    CREATE DATABASE device_info;
    -- Switch to the specified database
    USE device_info;
    ```

2. Create a devices table:

    ```sql
    CREATE TABLE devices (
        device_id INT PRIMARY KEY,        -- Device ID
        device_name VARCHAR NOT NULL,     -- Device name
        location VARCHAR,                 -- Location
        status VARCHAR DEFAULT 'active'   -- Status
    );
    ```

#### Insert Data

```sql
-- Insert device data in batch
INSERT INTO devices VALUES
    (101, 'Sensor A', 'Server Room 1', 'active'),
    (102, 'Sensor B', 'Server Room 2', 'active'),
    (103, 'Sensor C', 'Server Room 1', 'active');
```

#### Query Data

```sql
-- Query all device information
SELECT * FROM devices;
```

Expected output:

```plain
device_id | device_name | location      | status
----------+-------------+---------------+--------
    101 | Sensor A    | Server Room 1 | active
    102 | Sensor B    | Server Room 2 | active
    103 | Sensor C    | Server Room 1 | active
```

### Time-Series Data Operations

Time-series tables require:

- **Timestamp column**: Must be the first column
- **Tags**: Identify static device attributes
- **Primary tags**: Distinguish different entities

The following example shows basic time-series operations using real-time sensor data.

#### Create Time-Series Database and Table

1. Create a time-series database:

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
        device_id INT NOT NULL,           -- Device ID (as tag)
        sensor_type VARCHAR NOT NULL      -- Sensor type (as tag)
    ) PRIMARY TAGS(device_id);            -- Primary tag
    ```

#### Insert Data

```sql
-- Insert sensor data with current timestamp
INSERT INTO sensor_data VALUES
    (NOW(), 25.5, 60.2, 101, 'temperature'),
    (NOW(), 26.1, 58.7, 102, 'temperature'),
    (NOW(), 24.8, 62.1, 103, 'temperature');
```

#### Query Data

```sql
-- Query the latest 5 sensor readings, ordered by timestamp in descending order
SELECT * FROM sensor_data 
ORDER BY ts DESC 
LIMIT 5;
```

Expected output:

```plain
        ts                    | temperature | humidity | device_id | sensor_type
-------------------------------+-------------+----------+-----------+-------------
2025-08-01 10:30:15.123+00:00 |        24.8 |     62.1 |       103 | temperature
2025-08-01 10:30:15.123+00:00 |        26.1 |     58.7 |       102 | temperature
2025-08-01 10:30:15.123+00:00 |        25.5 |     60.2 |       101 | temperature
```

### Cross-Model Queries

KWDB excels at combining time-series and relational data for comprehensive analytics.

#### Query Device Information with Latest Monitoring Data

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

```plain
device_name | location      | temperature | humidity |        last_update
------------+---------------+-------------+----------+---------------------------
Sensor A    | Server Room 1 |        25.5 |     60.2 | 2025-08-01 10:30:15.123+00:00
Sensor B    | Server Room 2 |        26.1 |     58.7 | 2025-08-01 10:30:15.123+00:00
Sensor C    | Server Room 1 |        24.8 |     62.1 | 2025-08-01 10:30:15.123+00:00
```

#### Calculate Average Temperature and Humidity by Location

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

```plain
location      | device_count | avg_temp | avg_humidity
--------------+--------------+----------+--------------
Server Room 1 |            2 |     25.2 |         61.2
Server Room 2 |            1 |     26.1 |         58.7
```