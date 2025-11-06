---
title: Time-Series Databases
id: ts-database
---

# Time-Series Databases

As a multi-model database system, KWDB supports creating one or more database objects on a KWDB instance to manage time-series and relational data. One of the database objects dedicated to storing and managing time-series data is the time-series database. The time-series database includes the `public` schema and user-defined time-series tables.

## CREATE DATABASE

The `CREATE DATABASE` statement creates a new time-series database.

### Privileges

The user must be the Admin user or a member of the `admin` role.

### Syntax

![](../../../../static/sql-reference/create-db-ts.png)

### Parameters

:::warning Note

- The optional parameters must be configured in an order of `[RETENTIONS <keep_duration>] [COMMENT [=] <'comment_text'>]`. Otherwise, the system returns an error.
- Version 3.0.0 only supports a 10-day database partition interval. Other configuration values are not valid.

:::

| Parameter | Description |
| --- | --- |
| `database_name` | The name of the database to create, which must be unique and follow these [Identifier Rules](../../sql-identifiers.md). Currently, the name does not support Chinese characters and supports up to 63 bytes.|
| `keep_duration` | Optional. Specify the retention of the database. By default, it is set to `0d`, which means not deleting the database after expiration. Support the following units: second (S or SECOND), minute (M or MINUTE), hour (H or HOUR), day (D or DAY), week (W or WEEK), month (M or MONTH), and year (Y or YEAR), such as `RETENTIONS 10 DAY`. The value must be an integer and the maximum value must not exceed `1000` years. |
| `interval` | Optional. Specify a partition interval for a database. By default, it is set to `10d`, which means making a partition every 10 days. Support the following units: day (D or DAY), week (W or WEEK), month (M or MONTH), and year (Y or YEAR). The value must be an integer and the maximum value must not exceed `1000` years.|
| `comment_text` | Optional. Specify the comment to be associated to the database.|

:::warning Note

- The retention configuration does not apply to the current partition. The data is stored in the current partition. When the value of the retention is less than the partition interval, you can still query the data even if the retention of the database has expired.
- When all data in a partition exceeds the retention (`now() - retention time`), the system attempts to delete the data in that partition. If you are reading or writing the data in the partition at this time, or the system is compressing or making statistcs on the partition, the system cannot delete the data in the partition immediately. The system tries to delete the data again at the next retention. (By default, the system schedules data every hour.)
- The retention and partition interval settings are closely related to the storage space of the system. The longer the retention and the larger the partition interval, the more storage space the system requires. For the formula for calculating the storage space, see [Estimate Disk Usage](../../../db-operation/cluster-planning.md#estimate-disk-usage).
- When you individually specify or modify the retention or partition interval of a time-series table within the database, the configuration applies only to that time-series table.

:::

### Examples

- Create a database.

    This example creates a database named `ts_db`.

    ```sql
    CREATE TS DATABASE ts_db;
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
    CREATE TS DATABASE
    ```

- Create a database and set the retention of the database.

    This example creates a database named `ts_db_temp` and sets the database retention to `50d`.

    ```sql
    CREATE TS DATABASE ts_db_temp RETENTIONS 50d;
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
    CREATE TS DATABASE
    ```

- Create a database and set the retention and the partition interval of the database.

    This example creates a database named `iot` and sets the database retention and the partition interval to `50d` and `2d` respectively.

    ```sql
    CREATE TS DATABASE iot RETENTIONS 50d PARTITION INTERVAL 2d;
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
    CREATE TS DATABASE
    ```

- Create a database and specify comments for the database.

    This example creates a database named `ts_db_power` and associates the comment text `database for power statistics` to the database.

    ```sql
    CREATE TS DATABASE ts_db_power COMMENT = 'database for power statistics';
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
    CREATE TS DATABASE
    ```

## SHOW DATABASES

The `SHOW DATABASES` statement lists all databases in the KWDB cluster, including relational databases and time-series databases.

### Privileges

N/A

### Syntax

![](../../../../static/sql-reference/show_databases_ts.png)

### Parameters

| Parameter      | Description                                                                                                |
|----------------|------------------------------------------------------------------------------------------------------------|
| `WITH COMMENT` | Optional. Show a database's comments. By default, the database's comment is set to `NULL`. |

### Examples

:::warning Note
The `engine_type` for time-series databases and relational databases is `TIME SERIES` and `RELATIONAL` respectively.
:::

- Show all created databases.

    ```sql
    SHOW DATABASES;
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
      database_name  |   engine_type 
    -----------------+-------------------        
      defaultdb      | RELATIONAL
      postgres       | RELATIONAL
      system         | RELATIONAL
      ts_db          | TIME SERIES
    (4 rows)
    ```

- Show all created databases' comments.

    ```sql
    SHOW DATABASES WITH COMMENT;
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
      database_name       | engine_type |            comment
    ----------------------+-------------+--------------------------------
      defaultdb           | RELATIONAL  | NULL
      postgres            | RELATIONAL  | NULL
      ts_db               | TIME SERIES | database for power statistics
      system              | RELATIONAL  | NULL
    (4 rows)
    ```

## SHOW CREATE DATABASE

The `SHOW CREATE DATABASE` statement shows the `CREATE DATABASE` statement for an existing database and the parameters specified when creating the database. You can check the name and values of the `retentions` and `partition interval` parameters. If no value is specified for the `retentions` and `partition interval` parameters, the default values will be displayed. By default, the `retentions` parameter is set to `0s` and the `partition interval` parameter is set to `10d`.

### Privileges

N/A

### Syntax

![](../../../../static/sql-reference/showcreatedb.png)

### Parameters

| Parameter       | Description                       |
|-----------------|-----------------------------------|
| `database_name` | The name of the database to view. |

### Examples

This example shows the statement that is used to create the `tsdb1` database, and the values of related parameters.

```sql
-- 1. Create a database named tsdb1, and set retentions and partition interval to `10d`.

CREATE TS DATABASE tsdb1 RETENTIONS 10d PARTITION INTERVAL 10d;

--2. Show the created tsdb1 database.

SHOW CREATE DATABASE tsdb1;
  database_name |          create_statement
----------------+-------------------------------------
  tsdb1         | CREATE TS DATABASE tsdb1
                |      retentions 864000s
                |      partition interval 10d
(1 row)
```

## USE

The `USE` statement sets a target database to the current database.

### Privileges

N/A

### Syntax

![](../../../../static/sql-reference/EVTHbwr1VokEQCxFcDjcbzYOn3b.png)

### Parameters

| Parameter | Description                      |
|-----------|----------------------------------|
| `db_name` | The name of the database to use. |

### Examples

This example sets the `ts_db` database to the current database.

```sql
USE ts_db;
```

## ALTER DATABASE

The `ALTER DATABASE` statement applies a name, retention, or partition interval to a database.

:::warning Note

- The retention configuration does not apply to the current partition. The data is stored in the current partition. When the value of the retention is less than the partition interval, you can still query the data even if the retention of the database has expired.
- When all data in a partition exceeds the retention (`now() - retention time`), the system attempts to delete the data in that partition. If you are reading or writing the data in the partition at this time, or the system is compressing or making statistcs on the partition, the system cannot delete the data in the partition immediately. The system tries to delete the data again at the next retention. (By default, the system schedules data every hour.)
- The retention and partition interval settings are closely related to the storage space of the system. The longer the retention and the larger the partition interval, the more storage space the system requires. For the formula for calculating the storage space, see [Estimate Disk Usage](../../../db-operation/cluster-planning.md#estimate-disk-usage).
- When you individually specify or modify the retention or partition interval of a time-series table within the database, the configuration applies only to that time-series table.

:::

### Privileges

The user must be the Admin user or a member of the `admin` role.

### Syntax

- Change the name of the database

    ![](../../../../static/sql-reference/HLAybCbuLoVFWExpDzxc3l0ynnc.png)

- Change the retention or partition interval of the database

    ![](../../../../static/sql-reference/Ab69bP86UozqWDxtCLMc3vxznwh.png)

### Parameters

| Parameter | Description |
| --- | --- |
| `old_name` | The name of the database to change. |
| `new_name` | The new name of the database, which must be unique and follow these [Identifier Rules](../../sql-identifiers.md). Currently, the name does not support Chinese characters and supports up to 63 bytes.|
| `database_name` | The name of the database to change. |
| `keep_duration` | Optional. Specify the retention of the database. By default, it is set to `0d`, which means not deleting the database after expiration. Support the following units: second (S or SECOND), minute (M or MINUTE), hour (H or HOUR), day (D or DAY), week (W or WEEK), month (M or MONTH), and year (Y or YEAR), such as `RETENTIONS 10 DAY`. The value must be an integer and the maximum value must not exceed `1000` years. |
| `interval` | Optional. Specify a partition interval for a database. By default, it is set to `10d`, which means making a partition every 10 days. Support the following units: day (D or DAY), week (W or WEEK), month (M or MONTH), and year (Y or YEAR). The value must be an integer and the maximum value must not exceed `1000` years.|

### Examples

- Change the name of a database.

    This example renames the `ts_db` database to `tsdb`.

    ```sql
    ALTER DATABASE ts_db RENAME TO tsdb;
    ```

- Change the retention of a database.

    This example sets the retention of the `tsdb` database to `10 day`.

    ```sql
    ALTER TS DATABASE tsdb SET RETENTIONS = 10 day;
    ```

- Change the partition interval of a database.

    This example sets the partition interval of the `tsdb` database to `2 day`.

    ```sql
    ALTER TS DATABASE tsdb SET PARTITION INTERVAL = 2 day;
    ```

## DROP DATABASE

The `DROP DATABASE` statement removes a database and all its objects from a KWDB cluster. To remove the current database, use the `USE <database_name>` statement to set another database as the current database. After deletion, all privileges on the database and its tables are also removed.

::: warning Note
When removing a database, KWDB will check whether the current database is referenced by the real-time data feed service. If yes, the system ruturns an error and lists all pipes that reference the specified database. In this case, you can use the `CASCADE` keyword to remove the specified database and its dependent objects.
:::

### Privileges

The user must have the `DROP` privilege on the specified database and tables in the database.

### Syntax

![](../../../../static/sql-reference/AN7KbiqPPoaiCdxDfgSchsWLnFc.png)

### Parameters

| Parameter | Description |
| --- | --- |
| `IF EXISTS` | Optional. <br>- When the `IF EXISTS` keyword is used, the system removes the database only if the database has already existed. Otherwise, the system fails to remove the database without returning an error. <br>- When the `IF EXISTS` keyword is not used, the system removes the database only if the database has already existed. Otherwise, the system fails to remove the database and returns an error. |
| `database_name` | The name of the database to remove. |
| `CASCADE` | Optional. Remove all tables in the database. The `CASCADE` keyword does not list objects it removes, so it should be used cautiously.|

### Examples

This example removes the `tsdb` database and its dependent objects using the `CASCADE` keyword.

```sql
-- 1. Show tables in the tsdb database.

SHOW TABLES FROM tsdb;
  table_name  |    table_type
--------------+--------------------
  sensor_data | TIME SERIES TABLE
  temp        | TIME SERIES TABLE
  water       | TIME SERIES TABLE
(3 rows)

-- 2. Remove the tsdb database and its dependent objects.

DROP DATABASE tsdb CASCADE;
DROP DATABASE

-- 3. Show tables in the tsdb database.

SHOW TABLES FROM tsdb;
ERROR: target database or schema does not exist
```
