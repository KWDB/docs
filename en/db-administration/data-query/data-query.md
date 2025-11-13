---
title: Cross-model Query
id: data-query
---


# Cross-model Query

Cross-model query​ is a method for retrieving related data across different types of databases, such as querying associated data between relational databases and time-series databases.

KWDB supports ​cross-model queries​ between relational tables and time-series tables, including:

- ​JOIN queries​
  - INNER JOIN
  - LEFT JOIN
  - RIGHT JOIN
  - FULL JOIN
- ​Nested queries​
  - Correlated Subquery: the inner query depends on the outer query’s result and is executed for each row processed by the outer query.
  - Non-Correlated Subquery: the inner query is independent of the outer query and is executed only once, returning a fixed result.
  - Correlated Scalar Subquery: the inner query depends on the outer query’s result and returns a single scalar value.
  - Non-Correlated Scalar Subquery: the inner query is independent and returns a single scalar value.
  - `FROM` Subquery: embed a complete SQL query within the `FROM` clause of another query, acting as a temporary table.
- UNION queries
  - UNION: combine multiple queries and remove duplicate rows.
  - UNION ALL: combine multiple queries without removing duplicate rows.
  - INTERSECT: return intersected rows of all queries, removing duplicate rows.
  - INTERSECT ALL: return intersected rows of all queries, retaining duplicate rows.
  - EXCEPT: return rows that are in the first query but not in the second query, removing duplicate rows.
  - EXCEPT ALL: return rows that are in the first query but not in the second query, retaining duplicate rows.

::: warning Note

- ​KWDB supports executing time-series data queries and insertion within explicit transactions, but it ​does not guarantee transactional integrity​ for the time-series engine or ​consistency of cross-model query results.
- When using `FULL JOIN`, ​avoid using subqueries in join conditions.

:::

## Privileges

The user must be a member of the `admin` role or have been granted the `SELECT` privilege on the specified table(s).

## Examples

These examples assume that you have created a time-series database (`tsdb`), a relational database (`rdb`), two relational tables (`DeviceModel` and `Device`), and a time-series table (`MonitoringCenter`), and inserted data into these tables.

```sql
-- Create relational database
CREATE DATABASE rdb;

-- Switch to relational database
USE rdb;

-- Create device model table
CREATE TABLE DeviceModel (
    modelID INT PRIMARY KEY,
    TypeName VARCHAR(50),
    ModelName VARCHAR(50)
);

-- Create device table
CREATE TABLE Device (
    deviceID INT PRIMARY KEY,
    modelID INT,
    deviceName VARCHAR(100),
    FOREIGN KEY (modelID) REFERENCES DeviceModel(modelID)
);

-- Insert device model data
INSERT INTO DeviceModel (modelID, TypeName, ModelName) VALUES
(101, 'Smart Meter', 'SM-E100 Single-Phase Meter'),
(102, 'Smart Meter', 'SM-E300 Three-Phase Meter'),
(201, 'Distribution Transformer', 'TR-D500 Oil-Immersed Transformer'),
(202, 'Distribution Transformer', 'TR-D800 Dry-Type Transformer'),
(301, 'Circuit Breaker', 'CB-V200 Vacuum Circuit Breaker');

-- Insert device data
INSERT INTO Device (deviceID, modelID, deviceName) VALUES
(1001, 101, 'Building 1 Single-Phase Meter'),
(1002, 101, 'Building 2 Single-Phase Meter'),
(1003, 102, 'Building 3 Three-Phase Meter'),
(2001, 201, 'Area A Main Transformer'),
(2002, 201, 'Area B Main Transformer'),
(2003, 202, 'Area C Dry-Type Transformer'),
(3001, 301, 'Main Feeder Circuit Breaker'),
(3002, 301, 'Line 1 Circuit Breaker'),
(3003, 301, 'Line 2 Circuit Breaker'),
(3004, 301, 'Line 3 Circuit Breaker');

-- Create time-series database
CREATE TS DATABASE tsdb;

-- Switch to time-series database
USE tsdb;

-- Create monitoring center time-series table
CREATE TABLE MonitoringCenter (
    ts TIMESTAMP NOT NULL,
    status INT
) TAGS (
    deviceID INT NOT NULL,
    location VARCHAR(100)
) PRIMARY TAGS (deviceID);

-- Insert monitoring center data
-- Device status description: 0-Normal, 1-Minor Alert, -1-Critical Fault
INSERT INTO MonitoringCenter (ts, status, deviceID, location) VALUES
('2024-11-13 10:00:00', 0, 1001, 'Beijing Haidian'),
('2024-11-13 10:00:00', 0, 1002, 'Beijing Chaoyang'),
('2024-11-13 10:00:00', -1, 1003, 'Beijing Fengtai'),    -- Critical Fault: Three-Phase Meter
('2024-11-13 10:00:00', 0, 2001, 'Shanghai Pudong'),
('2024-11-13 10:00:00', 1, 2002, 'Shanghai Jing\'an'),
('2024-11-13 10:00:00', 0, 2003, 'Shanghai Xuhui'),
('2024-11-13 10:00:00', 0, 3001, 'Guangzhou Tianhe'),
('2024-11-13 10:00:00', 1, 3002, 'Guangzhou Yuexiu'),
('2024-11-13 10:00:00', -1, 3003, 'Shenzhen Nanshan'),    -- Critical Fault: Line 2 Circuit Breaker
('2024-11-13 10:00:00', 0, 3004, 'Shenzhen Futian');
```

- JOIN query

    This example joins the `Device`, `DeviceModel`, and `MonitoringCenter` tables using INNER JOIN to query detailed information about faulty devices.

    ```sql
    SELECT d.deviceID, dm.TypeName, dm.ModelName
    FROM rdb.Device AS d
    INNER JOIN rdb.DeviceModel AS dm ON d.modelID = dm.modelID
    INNER JOIN tsdb.MonitoringCenter AS mc ON d.deviceID = mc.deviceID
    WHERE mc.status = -1
    ORDER BY d.deviceID;
    ```

    Expected result:

    ```sql
      deviceid |     typename      |            modelname
    -----------+-------------------+----------------------------------
          1003 | Smart Meter       | SM-E300 Three-Phase Meter
          3003 | Circuit Breaker   | CB-V200 Vacuum Circuit Breaker
    (2 rows)
    ```

- Nested query

    This example uses Correlated Scalar Subquery to associate the device ID with the `tsdb.MonitoringCenter` table to get the latest status of each device.

    ```sql
    SELECT d.deviceID,
          (SELECT MAX(status) FROM tsdb.MonitoringCenter WHERE deviceID = d.deviceID) AS LatestStatus
    FROM rdb.Device AS d ORDER by d.deviceID;
    ```

    Expected result:

    ```sql
      deviceid | lateststatus
    -----------+---------------
          1001 |            0
          1002 |            0
          1003 |           -1
          2001 |            0
          2002 |            1
          2003 |            0
          3001 |            0
          3002 |            1
          3003 |           -1
          3004 |            0
    (10 rows)
    ```

- UNION query

    This example uses the `UNION` operator to combine query results from the `rdb.Device` and `tsdb.MonitoringCenter` tables, generating a list of devices requiring special attention (meter devices and faulty devices).

    ```sql
    SELECT deviceID, deviceName, 'Meter Device' AS category
    FROM rdb.Device
    WHERE modelID IN (101, 102)
    UNION ALL
    SELECT d.deviceID, d.deviceName, 'Faulty Device' AS category
    FROM rdb.Device AS d
    INNER JOIN tsdb.MonitoringCenter AS mc ON d.deviceID = mc.deviceID
    WHERE mc.status = -1
    ORDER BY deviceID;
    ```

    Expected result:

    ```sql
      deviceid |          devicename           |    category
    -----------+-------------------------------+----------------
          1001 | Building 1 Single-Phase Meter | Meter Device
          1002 | Building 2 Single-Phase Meter | Meter Device
          1003 | Building 3 Three-Phase Meter  | Meter Device
          1003 | Building 3 Three-Phase Meter  | Faulty Device
          3003 | Line 2 Circuit Breaker        | Faulty Device
    (5 rows)
    ```
