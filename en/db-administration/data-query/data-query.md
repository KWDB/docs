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

- JOIN query

    This example joins the time-series and relational tables together and gets related information based on the specified conditions.

    ```sql
    SELECT d.deviceID, dm.TypeName, dm.ModelName
    FROM rdb.Device AS d
    INNER JOIN rdb.DeviceModel AS dm ON d.modelID = dm.modelID
    INNER JOIN tsdb.MonitoringCenter AS mc ON d.deviceID = mc.deviceID
    WHERE mc.status = -1
    ORDER BY d.deviceID;
      deviceid | typename      |  modelname
    -----------+---------------+--------------
            7  | meter         | metermodel2
            16 | transformer   | transformermodel6
    (2 rows)
    ```

- Nested query

    This example performs Correlated Scalar Subquery on the `deviceID` column of the `rdb.Device` table and the `tsdb.MonitoringCenter` table to get the latest status of related devices.

    ```sql
    SELECT d.deviceID,
          (SELECT MAX(status) FROM tsdb.MonitoringCenter WHERE deviceID = d.deviceID) AS LatestStatus
    FROM rdb.Device AS d ORDER by d.deviceID;
      deviceid | lateststatus
    -----------+---------------
            1 | NULL
            2 |            0
            3 | NULL
            4 | NULL
            5 | NULL
            6 | NULL
            7 |           -1
            8 | NULL
            9 | NULL
            10 | NULL
            11 | NULL
            12 | NULL
            13 | NULL
            14 |            0
            15 | NULL
            16 |           -1
            17 | NULL
            18 |            0
            19 | NULL
            20 | NULL
            21 | NULL
    (21 rows)
    ```

- UNION query

    This example combines the query results of the `rdb.Device` and `tsdb.MonitoringCenter` tables and sorts the results based on `deviceID` and `status` with the `ASC` keyword.

    ```sql
    SELECT deviceID, NULL AS status
    FROM rdb.Device
    UNION
    SELECT NULL AS deviceID, status
    FROM tsdb.MonitoringCenter order by deviceID,status;
      deviceid | status
    -----------+---------
      NULL     |     -1
      NULL     |      0
            1 | NULL
            2 | NULL
            3 | NULL
            4 | NULL
            5 | NULL
            6 | NULL
            7 | NULL
            8 | NULL
            9 | NULL
            10 | NULL
            11 | NULL
            12 | NULL
            13 | NULL
            14 | NULL
            15 | NULL
            16 | NULL
            17 | NULL
            18 | NULL
            19 | NULL
            20 | NULL
            21 | NULL
    (23 rows)
    ```
