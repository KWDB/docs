---
title: kwbase CLI
id: access-cli
---

# kwbase CLI

kwbase is a built-in command-line tool provided by KaiwuDB. Users can connect to KWDB through kwbase for database operations and management, supporting both secure mode (for production environments) and non-secure mode (for testing).

If KWDB is deployed using scripts, the system will also automatically generate a convenient `kw-sql` script and create a soft link `kw-sql` in the `/usr/bin` directory. This script encapsulates the kwbase connection command, allowing root users to quickly log in to the database.

## Connecting to KWDB

### Quick Login Using Convenient Script

::: warning Note
`kw-sql` does not support specifying other users. If you need to use other users or three-role separation mode, please use the kwbase command to log in.
:::

**Prerequisites**:

KWDB has been deployed and started using the `deploy.sh` script.

**Steps**:

1. Execute the following command at any location on the node to connect to the database using the root user:

    ```shell
    kw-sql
    ```

### Connecting Using kwbase Command

::: warning Tip
If using container deployment, use the following command format to connect to the database:
```bash
docker exec -it <container-name> ./kwbase sql [security-options] --host=<your-host-ip> [-u <user-name>]
```
:::

#### Non-Secure Mode

::: warning Tip
Non-secure mode should only be used in testing environments.
:::

**Prerequisites**
- KWDB deployed and started in non-secure mode.

**Steps**

- Connect to KWDB using the user who deployed the database.

    ```shell
    ./kwbase sql --insecure --host=<your-host-ip>
    ```

- Regular user connecting to KWDB.

    1. Connect to KWDB using the user who deployed the database.

        ```shell
        ./kwbase sql --insecure --host=<your-host-ip>
        ```

    2. Create a regular user.

        ```sql
        CREATE USER user1;
        ```

    3. Exit the login.
    4. New user connects to KWDB.

        ```shell
        ./kwbase sql --insecure --host=<your-host-ip> -u user1
        ```

#### Secure Mode

KWDB supports users logging in with certificates or passwords by default. The following examples demonstrate how administrator users and regular users log in to the database securely in standard secure mode. For details on other authentication methods, see [Identity Authentication and Authorization](../../db-security/identity-authn.md).

**Prerequisites**

- KWDB deployed and started in secure mode.

**Steps**

- Connect to KWDB using the user who deployed the database.

    ```shell
    ./kwbase sql --certs-dir=<certs-dir> --host=<your-host-ip> 
    ```

- Regular user connecting to KWDB.

    1. Connect to KWDB using the user who deployed the database.

        ```shell
        ./kwbase sql --certs-dir=<certs-dir> --host=<your-host-ip> 
        ```

    2. Create a regular user.

        ```sql
        CREATE USER user1;
        ```

    3. Generate a certificate for the new user.

        ```shell
        ./kwbase cert create-client user1 --certs-dir=<certs-dir> --ca-key=<certs-dir>/ca.key
        ```

    4. Exit the login.
    5. New user connects to KWDB.

        ```shell
        ./kwbase sql --certs-dir=<certs-dir> --host=<your-host-ip> -u user1
        ```

## Managing KWDB

This section demonstrates how to use the kwbase CLI tool to manage KWDB's multi-model database through monitoring scenarios, including:

- **Relational data operations**: Managing relatively static basic data, such as device information, user profiles, etc.
- **Time-series data operations**: Processing dynamic data that changes over time series, such as sensor readings, monitoring metrics, etc.
- **Cross-modal queries**: Achieving multi-model data fusion analysis through joint queries of relational and time-series databases.

### Relational Data Operations

#### Creating Database and Tables

1. Create and use relational databases:
    ```sql
    -- Create relational database
    CREATE DATABASE device_info;
    -- Switch to specified database
    USE device_info;
    ```

2. Create device tables:
    ```sql
    CREATE TABLE devices (
        device_id INT PRIMARY KEY,        -- Device ID
        device_name VARCHAR NOT NULL,     -- Device name
        location VARCHAR,                 -- Location
        status VARCHAR DEFAULT 'active'   -- Status
    );
    ```

#### Writing Data

```sql
-- Batch insert device basic information
INSERT INTO devices VALUES
    (101, 'Sensor A', 'Server Room 1', 'active'),
    (102, 'Sensor B', 'Server Room 2', 'active'),
    (103, 'Sensor C', 'Server Room 1', 'active');
```

#### Querying Data

```sql
-- Query all device information
SELECT * FROM devices;
```

Example query results:
```plain
device_id | device_name | location      | status
----------+-------------+---------------+--------
      101 | Sensor A    | Server Room 1 | active
      102 | Sensor B    | Server Room 2 | active
      103 | Sensor C    | Server Room 1 | active
```

### Time-Series Data Operations

Time-series tables have special structural requirements:
- **Timestamp column**: Must be the first column of the table
- **Tag columns (TAGS)**: Used to identify static device attributes
- **Primary tags (PRIMARY TAGS)**: Used to distinguish different entity objects

#### Creating Time-Series Database and Tables

1. Create time-series database:
    ```sql
    -- Create time-series database
    CREATE TS DATABASE monitoring;
    -- Switch to time-series database
    USE monitoring;
    ```

2. Create monitoring data table:
    ```sql
    CREATE TABLE sensor_data (
        ts TIMESTAMP NOT NULL,            -- Timestamp (must be first column)
        temperature FLOAT,                -- Temperature
        humidity FLOAT                  -- Humidity
    ) TAGS (
        device_id INT NOT NULL,          -- Device ID (tag)
        sensor_type VARCHAR NOT NULL     -- Sensor type (tag)
    ) PRIMARY TAGS(device_id);         -- Primary tags
    ```

#### Writing Data

```sql
-- Insert current time sensor monitoring data
INSERT INTO sensor_data VALUES
    (NOW(), 25.5, 60.2, 101, 'temperature'),
    (NOW(), 26.1, 58.7, 102, 'temperature'),
    (NOW(), 24.8, 62.1, 103, 'temperature');
```

#### Querying Data

```sql
-- Query latest 5 sensor records in descending time order
SELECT * FROM sensor_data 
ORDER BY ts DESC 
LIMIT 5;
```

Example query results:
```plain
        ts                    | temperature | humidity | device_id | sensor_type
---------------------------+-------------+----------+-----------+-------------
2025-08-01 10:30:15.123+00:00 |        24.8 |     62.1 |       103 | temperature
2025-08-01 10:30:15.123+00:00 |        26.1 |     58.7 |       102 | temperature
2025-08-01 10:30:15.123+00:00 |        25.5 |     60.2 |       101 | temperature
```

### Cross-Modal Queries

KWDB's core advantage lies in supporting joint queries across time-series and relational databases, achieving deep multi-model data fusion analysis.

#### Query Device Basic Information and Latest Monitoring Data

```sql
-- Joint query of device basic information and latest monitoring data
-- Use DISTINCT ON to get the latest data record for each device
SELECT 
    d.device_name,          -- Device name
    d.location,             -- Device location
    s.temperature,          -- Latest temperature
    s.humidity,             -- Latest humidity
    s.ts as last_update     -- Last update time
FROM device_info.devices d
JOIN (
    -- Subquery: get latest monitoring data for each device
    SELECT DISTINCT ON (device_id) 
        device_id, temperature, humidity, ts
    FROM monitoring.sensor_data 
    ORDER BY device_id, ts DESC
) s ON d.device_id = s.device_id
WHERE d.status = 'active'   -- Only query active status devices
ORDER BY d.device_id;
```

Example query results:
```plain
device_name | location      | temperature | humidity |        last_update
------------+---------------+-------------+----------+---------------------------
Sensor A    | Server Room 1 |        25.5 |     60.2 | 2025-08-01 10:30:15.123+00:00
Sensor B    | Server Room 2 |        26.1 |     58.7 | 2025-08-01 10:30:15.123+00:00
Sensor C    | Server Room 1 |        24.8 |     62.1 | 2025-08-01 10:30:15.123+00:00
```

#### Statistics Average Temperature and Humidity by Location

```sql
-- Statistics average temperature and humidity by device location in the last 1 hour
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

Example query results:
```plain
location      | device_count | avg_temp | avg_humidity
--------------+--------------+----------+--------------
Server Room 1 |            2 |     25.2 |         61.2
Server Room 2 |            1 |     26.1 |         58.7
```
