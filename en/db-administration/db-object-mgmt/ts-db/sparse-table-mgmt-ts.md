---
title: Sparse Tables
id: sparse-table-mgmt-ts
---

# Sparse Table 

Sparse tables are special time series tables that inherit the characteristics of time series tables and are characterized by ultra-wide, high sparsity, and continuous time series. This article mainly explains the new syntax and functional features of sparse tables compared to ordinary time series tables.

## CREATE TABLE

`CREATE SPARSE TABLE` statement creates a new sparse table in a database.

### Syntax

```sql
CREATE SPARSE TABLE <table_name> (
  <column_list>
) 
tags (
  <tag_list>
) 
PRIMARY tags (
  <primary_tag_list>
) 
```

:::warning Note

- Only the time series database supports the creation of sparse tables.
- The maximum data column of the sparse table is 20,000 columns, while the maximum data column of the regular time series table is 4,096 columns.

:::

### Parameter Description

| Parameter | Description |
| --- | --- |
| `table_name`|  The name of the sparse table to create, which must be unique within its database and follow these [Identifier Rules](../../../../en/sql-reference/sql-identifiers.md). The table name supports up to 128 bytes.  |
| `column_list`| The list of data columns to be created supports the addition of more than two column definitions, with a maximum of 20,000 columns that can be specified.|
| `tag_list`| Tag list, supports adding one or multiple tag definitions, with a maximum of `128` tags specified. Tag definitions include tag name, data type, and comment information.<br>The maximum length of a label name is 128 bytes. It supports specifying NOT NULL and defaults to a null value. It does not support TIMESTAMP, TIMESTAMPTZ, NVARCHAR, and GEOMETRY data types.<br>Support adding annotation information for tag columns after the nullable condition. |
| `primary_tag_list`| A comma-separated list of primary tags. You can specify one or more primary tags. Each table supports up to 4 primary tags. Primary tags must be included in the list of tags and set to NOT NULL. Currently, primary tags does not support floating-point and variable-length data types, except for the VARCHAR data type. By default, a VARCHAR-typed data length is `64` bytes. The maximum of a VARCHAR-typed data length is `128` bytes.|

### Examples

- Create a sparse table。

    The following example creates a sparse table named `device_ts`.

    ```sql
    CREATE SPARSE TABLE device_ts (
      ts TIMESTAMP(3) NOT NULL,
      TEMP_DOUBLE DOUBLE,
      PRESS_INT INT4,
      ... (A maximum of 20,000 columns)
    ) 
    tags (device_id varchar(10) not null) 
    PRIMARY tags (device_id);
    ```

## SELECT TABLE

The `select <column_name> from <table_name> where` statement is used to query the specified column in a sparse table. <br> The `select * from <table_name> where`  statement is used to query the valid column data of the specified device in a sparse table.

### Parameter Description

| Parameter | Description |
| --- | --- |
| `table_name` |  The name of the sparse table to create, which must be unique within its database and follow these [Identifier Rules](../../../../en/sql-reference/sql-identifiers.md). The table name supports up to 128 bytes. |
| `column_name` | Column name: The newly added column name must not be duplicate with the current column names and tag names of the table to be modified. The maximum length of a column name is 128 bytes. |

### Syntax

```sql
--Specified Column Query
select <column_name> from <table_name> where <device_list>；
--Effective Column Query
select * from <table_name> where <device_list>;
```

### Examples

- Create a sparse table and write data into it

    ```sql
    CREATE SPARSE TABLE device_ts (
      ts TIMESTAMP(3) NOT NULL,
      p1 int4,
      p2 INT4,
      ...
      p9999 int4,
    )
    tags (device_id varchar(10) not null)
    PRIMARY tags (device_id);

    -- It is recommended that each 'insert' statement only includes a single device, specifying the insertion columns. The following example demonstrates the use of 'insert' statements for two devices respectively.

    root@:26257/test> insert into device_ts(ts,p1,p2,p3,p4,device_id) value('2020-11-06 17:10:23',1,1,1,1,'dev1');
    INSERT 1

    TIME: 1.045654ms

    root@:26257/test> insert into device_ts(ts,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,device_id) value('2020-11-06 17:10:25',2,2,2,2,2,2,2,2,2,2,'dev2');
    INSERT 1

    TIME: 2.189641ms
    ```

- Effective column query

    ```sql
    root@:26257/test> select * from device_ts where device_id in ('dev1','dev2');
    ```
    
    After successful execution, the following information will be output.
    ```sql
   ts|p1|p2|p3|p4|p5|p6|p7|p8|p9|p10|p11|p12|p13|p14|device_id
   ---+--+--+--+--+--+--+--+---+--+--+--+--+--+--+----------
   2020-11-06 17:10:25+00:00 |NULL |NULL |NULL|NULL| 2| 2| 2| 2| 2| 2| 2| 2| 2| 2| dev2
   2020-11-06 17:10:23+00:00 | 1| 1| 1| 1|NULL |NULL |NULL |NULL |NULL |NULL |NULL |NULL |NULL |NULL | dev1
  (2 rows)

  TIME: 5.565588ms
    ```
  When a device has not yet written data, all columns will be displayed during querying.
    ```sql
    > select * from device_ts where device_id = 'dev10000';
    ```
    ```sql
    ts|p1|p2.....|p9999|p10000|device_id
    --+--+-+.....+-----+-----+----------
  (0 rows)
    ```
  
- Specified column query

    ```sql
    root@:26257/test> select ts, p15 from device_ts where device_id = 'dev1';
    ```
    ```sql
    ts                        |p15
    --------------------------+-------
    2020-11-06 17:10:25+00:00 |NULL 
  (1 rows)
  TIME: 3.565588ms
    ```

## SHOW TABLE

The `show tables` statement is used to view the types of all tables under the current database. The sparse table type is `SPARSE TIME SERIES TABLE `.

### Syntax

```sql
show tables;
```

### Examples

- View the types of all tables in the current database.

    The following example demonstrates the sparse table `t1` and the regular time-series table `t2` in the current database.

    ```sql
    show tables;
    ```
    Output information after execution.
    ```sql
    table_name|table_type
    ----------+------------------------
    t1        |SPARSE TIME SERIES TABLE
    t2        |TIME SERIES TABLE
    ```

## LIMITATIONS

- Support for subscription publishing, stream computing, and data push has been temporarily suspended.
- `Insert...Select` is temporarily not supported.