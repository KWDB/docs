---
title: Ranges
id: range-mgmt-relational
---

# Ranges

KWDB stores all user data (tables, indexes, etc.) and almost all system data in a sorted map of key-value pairs. This keyspace is divided into contiguous chunks called ranges. Therefore, you can find every key in one range.

From a SQL perspective, a relational table and its secondary indexes initially map to a single range, where each key-value pair in the range represents a single row in the table (also called the primary index) or a single row in a secondary index. As soon as the size of a range reaches 512 MiB, it is split into two ranges. This process continues for these new ranges as the table and its indexes continue growing. When the table and its indexes decrease, the ranges will be automatically merged. Note that KWDB supports Mark-Sweep. Therefore, ranges are not merged immediately after the data is removed. Ranges are merged only when the removed data is garbage collected.

KWDB supports using the `SHOW RANGES` statement to view range information for databases, tables, and indexes, and using the `ALTER RANGE` statement to modify the replica zone configuration of ranges.

## SHOW RANGES

The `SHOW RANGES` statement shows information about the ranges that comprise the data for a table, index, or database. This information is useful for verifying how SQL data maps to underlying ranges, and where the replicas for those ranges are located.

### Privileges

The user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

### Syntax

```sql
SHOW RANGES FROM [TABLE <table_name> | INDEX <table_name> @ <index_name> | DATABASE <database_name>];
```

### Parameters

| Parameter | Description |
| --- | --- |
| `table_name` | The name of the table you want range information about. |
| `index_name` | The name of the index you want range information about. |
| `database_name` | The name of the database you want range information about. |

### Examples

- Show ranges for a table.

    ```sql
    SHOW RANGES FROM TABLE orders;
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
      start_key | end_key | range_id | range_size_mb | lease_holder | lease_holder_locality | replicas | replica_localities
    ------------+---------+----------+---------------+--------------+-----------------------+----------+---------------------
      NULL      | NULL    |      180 |      0.000077 |            1 |                       | {1}      | {""}
    (1 row)
    ```

- Show ranges for an index.

    ```sql
    SHOW RANGES FROM INDEX orders @ primary;
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
      start_key | end_key | range_id | range_size_mb | lease_holder | lease_holder_locality | replicas | replica_localities
    ------------+---------+----------+---------------+--------------+-----------------------+----------+---------------------
      NULL      | NULL    |      180 |      0.000077 |            1 |                       | {1}      | {""}
    (1 row)
    ```

- Show ranges for a database.

    ```sql
    SHOW RANGES FROM DATABASE db3;
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
      table_name | start_key | end_key | range_id | range_size_mb | lease_holder | lease_holder_locality | replicas | replica_localities
    -------------+-----------+---------+----------+---------------+--------------+-----------------------+----------+---------------------
      order_list | NULL      | NULL    |      185 |      0.000145 |            1 |                       | {1}      | {""}
      orders     | NULL      | NULL    |      180 |      0.000077 |            1 |                       | {1}      | {""}
      orders_seq | NULL      | NULL    |      183 |      0.000114 |            1 |                       | {1}      | {""}
    (3 rows)
    ```

## ALTER RANGE

The `ALTER RANGE` statement applies a zone configuration change to a range. In addition to the databases and tables that are visible via the SQL interface, KWDB stores internal data in the following system ranges and comes with pre-configured zones for some of these ranges:

- `meta`: contain the information about the location of all data in the cluster. Set the number of replicas to `5` to make these ranges more resilient to node failure and a lower-than-default `gc.ttlseconds` value to keep these ranges smaller for reliable performance.
- `liveness`: contain the information about which nodes are live at any given time. Set the number of replicas to `5` to make these ranges more resilient to node failure and a lower-than-default `gc.ttlseconds` value to keep these ranges smaller for reliable performance.
- `system`: contain information needed to allocate new table IDs and track the status of a cluster's nodes. Set the number of replicas to `5` to make these ranges more resilient to node failure.
- `timeseries`: contain monitoring data about the cluster.

::: warning Note
Use caution when editing zone configurations for system ranges, as they could cause some (or all) parts of your cluster to stop working.
:::

### Privileges

The user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

### Syntax

```sql
ALTER RANGE <range_name> CONFIGURE ZONE [USING <variable> = [COPY FROM PARENT | <value>], <variable> = [<value> | COPY FROM PARENT], ... | DISCARD];
```

### Parameters

| Parameter | Description |
| --- | --- |
| `range_name` | The name of the range to change, including: <br>- `default`: contain default replica settings. <br>- `meta`: contain the information about the location of all data in the cluster. <br>- `liveness`: contain the information about which nodes are live at any given time. <br>- `system`: contain information needed to allocate new table IDs and track the status of a cluster's nodes. <br>- `timeseries`: contain monitoring data about the cluster.|
| `variable` | The name of the variable to modify. The following variables are supported: <br>- `range_min_bytes`: the minimum size in bytes for a data range. When a range is smaller than this value, KWDB merges it with an adjacent range. Default: 256 MiB. The value must be greater than 1 MiB (1048576 bytes) and smaller than the maximum size of the range. <br>- `range_max_bytes`: the maximum size in bytes for a data range. When a range exceeds this value, KWDB splits it into two ranges. Default: 512 MiB. The value must not be smaller than 5 MiB (5242880 bytes). <br>- `gc.ttlseconds`: the number of seconds data will be retained before garbage collection. Default: `90000` (25 hours). We recommend setting a value of at least 600 seconds (10 minutes) to avoid affecting long-running queries. A smaller value saves disk space while a larger value increases the time range allowed for `AS OF SYSTEM TIME` queries. Additionally, since all versions of each row are stored in a single, unsplit range, avoid setting this value too large to prevent all changes to a single row from exceeding 64 MiB, which may cause memory issues or other problems. <br>- `num_replicas`: the number of replicas. Default: 3. For the `system` database and the `meta`, `liveness`, and `system` ranges, the default number of replicas is 5. **Note**: The number of replicas cannot be reduced when unavailable nodes exist in the cluster. <br>- `constraints`: required (+) and/or prohibited (-) constraints for where replicas can be placed. For example, `constraints = '{"+region=NODE1": 1, "+region=NODE2": 1, "+region=NODE3": 1}'` places one replica on each of nodes 1, 2, and 3. Currently only supports the `region=NODEx` format. <br>- `lease_preferences`: an ordered list of required (+) and/or prohibited (-) constraints for where the leaseholder should be placed. For example, `lease_preferences = '[[+region=NODE1]]'` prefers placing the leaseholder on node 1. If this isn't possible, KWDB tries the next preference in the list. If no preferences can be satisfied, KWDB uses the default lease distribution algorithm, which balances leases across nodes based on their current lease count. Each value in the list can contain multiple constraints.|
| `value` | The value of the variable to change. |
|`COPY FROM PARENT`| Use the settings of the parent zone. |
|`DISCARD` | Remove the zone settings and use the default values. |

### Examples

This example changes the number of replicas to `7` for the `meta` range.

```sql
ALTER RANGE meta CONFIGURE ZONE USING num_replicas=7;
ALTER RANGE 

SHOW ZONE CONFIGURATION FOR RANGE meta;
    target   |            raw_config_sql
-------------+----------------------------------------
  RANGE meta | ALTER RANGE meta CONFIGURE ZONE USING
            |     range_min_bytes = 134217728,
            |     range_max_bytes = 536870912,
            |     gc.ttlseconds = 3600,
            |     num_replicas = 7,
            |     constraints = '[]',
            |     lease_preferences = '[]'
(1 row)
```