---
title: Sequences
id: sequence-mgmt-relational
---

# Sequences

## CREATE SEQUENCE

The `CREATE SEQUENCE` statement creates a new sequence within the database. The sequence can automatically increases the value in a table.

### Privileges

The user must be a member of the `admin` role or have been granted the `CREATE` privilege on the parent database. By default, the `root` user belongs to the `admin` role.

### Syntax

```sql
CREATE SEQUENCE [IF NOT EXISTS] <seq_name> 
[NO [CYCLE | MINVALUE | MAXVALUE] 
|OWNED BY [NONE | <column_name>] 
|INCREMENT [BY] <integer> 
|MINVALUE <integer> 
|MAXVALUE <integer> 
|START [WITH] <integer> 
|VIRTUAL];
```

### Parameters

| Parameter | Description |
| --- | --- |
| `IF NOT EXISTS` | Optional. <br>- When the `IF NOT EXISTS` keyword is used, the system creates a new sequence only if a sequence of the same name does not already exist. Otherwise, the system fails to create a new sequence without returning an error. <br>- When the `IF NOT EXISTS` keyword is not used, the system creates a new sequence only if a sequence of the same name does not already exist. Otherwise, the system fails to create a new sequence and returns an error. |
| `seq_name` | The name of the sequence to create. The sequence name must be unique within the database and must follow these [Identifier Rules](../../../../en/sql-reference/sql-identifiers.md). When the parent database is not set as the default, the name must be formatted as `database.seq_name`. |
| `NO CYCLE` | All sequences are set to `NO CYCLE` and the sequence will not wrap. |
| `OWNED BY` | Associate the sequence to a particular column. If that column or its parent table is dropped, the sequence will also be dropped. By default, it is set to `OWNED BY NONE`. Specifying an owner column with `OWNED BY` replaces any existing owner column on the sequence. To remove existing column ownership on the sequence and make the column free-standing, specify `OWNED BY NONE`. |
| `INCREMENT` | The value by which the sequence is incremented. A negative number creates a descending sequence. A positive number creates an ascending sequence. By default, it is set to `1`. |
| `MINVALUE` | The minimum value of the sequence. If no value is specified or if it is set to `NO MINVALUE`, default values will apply. By default, it is set to `MININT` for ascending sequences and `-1` for descending sequences. |
| `MAXVALUE` | The maximum value of the sequence. If no value is specified or if it is set to `NO MAXVALUE`, default values will apply. By default, it is set to `MAXINT` for ascending sequences and `-1` for descending sequences. |
| `START` | The first value of the sequence. By default, it is set to `1` for ascending sequences and `-1` for descending sequences. |

### Examples

- Create a sequence with default settings.

    ```sql
    -- 1. Create a sequence named orders_seq.

    CREATE SEQUENCE orders_seq;
    CREATE SEQUENCE

    -- 2. Check the created orders_seq sequence.

    SHOW CREATE orders_seq;
      table_name |                                    create_statement
    -------------+-----------------------------------------------------------------------------------------
      orders_seq | CREATE SEQUENCE orders_seq MINVALUE 1 MAXVALUE 9223372036854775807 INCREMENT 1 START 1
    (1 row)
    ```

- Create a sequence with user-defined settings.

    This example creates a sequence that starts at `-1` and descends in increments of `-2`.

    ```sql
    -- 1. Create a sequence named desc_orders_list.

    CREATE SEQUENCE desc_orders_list START -1 INCREMENT -2;
    CREATE SEQUENCE

    -- 2. Check the created desc_orders_list sequence.

    SHOW CREATE desc_orders_list;
        table_name    |                                         create_statement
    -------------------+---------------------------------------------------------------------------------------------------
      desc_orders_list | CREATE SEQUENCE desc_orders_list MINVALUE -9223372036854775808 MAXVALUE -1 INCREMENT -2 START -1
    (1 row)
    ```

- Create a table using a sequence.

    ```sql

    -- 1. Create a table named order_list using the orders_seq sequence.

    CREATE TABLE order_list (id int primary key default nextval ('orders_seq'), customer string, date date);
    CREATE TABLE

    -- 2. Insert data into the table.

    INSERT INTO order_list (customer, date) values ('Li Ming', '2024-01-02'), ('Li Hua', '2024-01-02');
    INSERT 2

    -- 3. Check data of the table.

    SELECT * FROM order_list;
      id | customer |           date
    -----+----------+----------------------------
      1 | Li Ming  | 2024-01-02 00:00:00+00:00
      2 | Li Hua   | 2024-01-02 00:00:00+00:00
    (2 rows)
    ```

- View the current value of a sequence.

    ```sql
    SELECT * FROM customer_seq;
      last_value | log_cnt | is_called
    -------------+---------+------------
              2 |       0 |   true
    (1 row)
    ```

    If a value is obtained from the sequence in the current session, you can also use the `currval('seq_name')` function to get that most recently obtained value.

    ```sql
    SELECT currval('customer_seq');
    currval
    -------
    2      
    (1 row)
    ```

- List all sequences.

    ```sql
    SELECT * FROM information_schema.sequences;
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
      sequence_catalog | sequence_schema |  sequence_name   | data_type | numeric_precision | numeric_precision_radix | numeric_scale | start_value |    minimum_value     |    maximum_value    | increment | cycle_option
    -------------------+-----------------+------------------+-----------+-------------------+-------------------------+---------------+-------------+----------------------+---------------------+-----------+---------------
      db3              | public          | orders_seq       | bigint    |                64 |                       2 |             0 | 1           | 1                    | 9223372036854775807 | 1         | NO
      db3              | public          | desc_orders_list | bigint    |                64 |                       2 |             0 | -1          | -9223372036854775808 | -1                  | -2        | NO
    (2 rows)
    ```

## SHOW SEQUENCES

The `SHOW SEQUENCES` statement lists all sequences in a database.

### Privileges

N/A

### Syntax

```sql
SHOW SEQUENCES [FROM <name>];
```

### Parameters

| Parameter | Description |
| --- | --- |
| `name` | The name of the database for which to list sequences. When no database is specified, the sequences in the current database are listed. |

### Examples

This example lists all sequences in the current database.

```sql
SHOW SEQUENCES;
```

If you succeed, you should see an output similar to the following:

```sql
   sequence_name
--------------------
  desc_orders_list
  orders_seq
(2 rows)
```

## ALTER SEQUENCE

The `ALTER SEQUENCE` statement changes the name, increment value, and other settings of a sequence.

### Privileges

The user must be a member of the `admin` role or have been granted the `CREATE` privilege on the parent database. By default, the `root` user belongs to the `admin` role.

### Syntax

```sql
ALTER SEQUENCE [IF EXISTS] <seq_name> 
[NO [CYCLE | MINVALUE | MAXVALUE] 
|OWNED BY [NONE | <column_name>] 
|INCREMENT [BY] <integer> 
|MINVALUE <integer> 
|MANVALUE <integer> 
|START [WITH] <integer> 
|VIRTUAL];
```

### Parameters

| Parameter | Description |
| --- | --- |
| `IF EXISTS` | Optional. <br>- When the `IF EXISTS` keyword is used, the system updates the sequence only if the target sequence has already existed. Otherwise, the system fails to update the sequence without returning an error. <br>- When the `IF EXISTS` keyword is not used, the system updates the sequence only if the target sequence has already existed. Otherwise, the system fails to update the sequence and returns an error.  |
| `seq_name` | The name of the sequence to change. The sequence name must be unique within the database and must follow these [Identifier Rules](../../../../en/sql-reference/sql-identifiers.md). When the parent database is not set as the default, the name must be formatted as `database.seq_name`. |
| `NO CYCLE` | All sequences are set to `NO CYCLE` and the sequence will not wrap. |
| `OWNED BY` | Associate the sequence to a particular column. If that column or its parent table is dropped, the sequence will also be dropped. By default, it is set to `OWNED BY NONE`. Specifying an owner column with `OWNED BY` replaces any existing owner column on the sequence. To remove existing column ownership on the sequence and make the column free-standing, specify `OWNED BY NONE`. |
| `INCREMENT` | The value by which the sequence is incremented. A negative number creates a descending sequence. A positive number creates an ascending sequence. By default, it is set to `1`. |
| `MINVALUE` | The minimum value of the sequence. If no value is specified or if it is set to `NO MINVALUE`, default values will apply. By default, it is set to `MININT` for ascending sequences and `-1` for descending sequences. |
| `MAXVALUE` | The maximum value of the sequence. If no value is specified or if it is set to `NO MAXVALUE`, default values will apply. By default, it is set to `MAXINT` for ascending sequences and `-1` for descending sequences. |
| `START` | The first value of the sequence. By default, it is set to `1` for ascending sequences and `-1` for descending sequences. <br >**Note** <br > The new first value will not take effect immediately after you change the first value of a sequence using the `ALTER SEQUENCE` statement. In this case, it is recommended to use the `SELECT SETval()` statement to manually set the current value of the sequence. For details, see the following examples. |

### Examples

- Change the increment value of a sequence.

    ```sql
    -- 1. Change the increment value of the orders_seq sequence to 2.

    ALTER SEQUENCE orders_seq INCREMENT 2;
    ALTER SEQUENCE

    -- 2. Insert data into the order_list table.

    INSERT INTO order_list (customer, date) VALUES ('Zhou Mi', '2024-01-02');
    INSERT 1

    -- 3. Check data of the table to verify whether new records meet the new sequence setting.

    SELECT * FROM order_list;
      id | customer |           date
    -----+----------+----------------------------
      1 | Li Ming  | 2024-01-02 00:00:00+00:00
      2 | Li Hua   | 2024-01-02 00:00:00+00:00
      4 | Zhou Mi  | 2024-01-02 00:00:00+00:00
    (3 rows)
    ```

- Set the next value of a sequence.

    This example changes the next value of `orders_seq sequence` using the `setval()` function.

    ::: warning Note
    You cannot set a value outside the `MAXVALUE` or `MINVALUE` of the sequence.
    :::

    ```sql
    -- 1. Set the next value of the orders_seq sequence to 7.

    SELECT SETval('orders_seq', 7, false);
      setval
    ----------
          7
    (1 row)

    -- 2. Insert data into the order_list table.

    INSERT INTO order_list (customer, date) VALUES ('Wang Ming', '2024-01-02');
    INSERT 1

    -- 3. Check data of the table to verify whether new records meet the new sequence setting.

    SELECT * FROM order_list;
      id | customer  |           date
    -----+-----------+----------------------------
      1 | Li Ming   | 2024-01-02 00:00:00+00:00
      2 | Li Hua    | 2024-01-02 00:00:00+00:00
      4 | Zhou Mi   | 2024-01-02 00:00:00+00:00
      7 | Wang Ming | 2024-01-02 00:00:00+00:00
    (4 rows)
    ```

- Disassociate the sequence to a particular column.

    ```sql
    -- 1. Associate the orders_seq sequence to the id column of the orders_list table.

    CREATE SEQUENCE orders_seq OWNED BY order_list.id;
    CREATE SEQUENCE

    -- 2. Disassociate the sequence to the id column.

    ALTER SEQUENCE orders_seq OWNED BY NONE;
    ALTER SEQUENCE
    ```

## ALTER SEQUENCE ... RENAME TO

The `ALTER SEQUENCE ... RENAME TO` statement changes the name of a sequence or moves a sequence to another database.

::: warning Note
KWDB does not support renaming a sequence that is being used by a table. To rename a sequence used by a table, you need to remove the `DEFAULT` expression which is used to reference the sequence, rename the sequence, and then add the `DEFAULT` expression back.
:::

### Privileges

The user must be a member of the `admin` role or have been granted the `CREATE` privilege on the parent database of the newly-created sequence. By default, the `root` user belongs to the `admin` role.

### Syntax

```sql
ALTER SEQUENCE [IF EXISTS] <current_name> RENAME TO <new_name>;
```

### Parameters

| Parameter | Description |
| --- | --- |
| `IF EXISTS` | Optional. <br>- When the `IF EXISTS` keyword is used, the system renames the sequence only if the target sequence has already existed. Otherwise, the system fails to rename the sequence without returning an error. <br>- When the `IF EXISTS` keyword is not used, the system renames the sequence only if the target sequence has already existed. Otherwise, the system fails to rename the sequence and returns an error.  |
| `current_name` | The current name of the sequence to change. |
| `new_name` | The new name of the sequence. The sequence name must be unique within the database and must follow these [Identifier Rules](../../../../en/sql-reference/sql-identifiers.md). To move the sequence to another database,  the name must be formatted as `<database_name>.<current_name>`. |

### Examples

- Rename a sequence.

    ```sql
    -- 1. Rename the desc_orders_list sequence to orders_list_seq.

    ALTER SEQUENCE desc_orders_list RENAME TO orders_list_seq;
    RENAME SEQUENCE

    -- 2. Check all sequences.

    SELECT * FROM information_schema.sequences;
      sequence_catalog | sequence_schema |  sequence_name  | data_type | numeric_precision | numeric_precision_radix | numeric_scale | start_value |    minimum_value     |    maximum_value    | increment | cycle_option
    -------------------+-----------------+-----------------+-----------+-------------------+-------------------------+---------------+-------------+----------------------+---------------------+-----------+---------------
      db3              | public          | orders_seq      | bigint    |                64 |                       2 |             0 | 1           | 1                    | 9223372036854775807 | 2         | NO
      db3              | public          | orders_list_seq | bigint    |                64 |                       2 |             0 | -1          | -9223372036854775808 | -1                  | -2        | NO
    (2 rows)
    ```

- Move a sequence.

    ```sql
    -- 1. Move the orders_list_seq sequence from the current database to db1 database.

    ALTER SEQUENCE orders_list_seq RENAME TO db1.orders_list_seq;
    RENAME SEQUENCE

    -- 2. Check all sequences in db1 database.

    SELECT * FROM db1.information_schema.sequences;
      sequence_catalog | sequence_schema |  sequence_name  | data_type | numeric_precision | numeric_precision_radix | numeric_scale | start_value |    minimum_value     | maximum_value | increment | cycle_option
    -------------------+-----------------+-----------------+-----------+-------------------+-------------------------+---------------+-------------+----------------------+---------------+-----------+---------------
      db1              | public          | orders_list_seq | bigint    |                64 |                       2 |             0 | -1          | -9223372036854775808 | -1            | -2        | NO
    (1 row)
    ```

## DROP SEQUENCE

The `DROP SEQUENCE` statement removes a sequence from a database. KWDB supports removing multiple sequences at once.

### Privileges

The user must be a member of the `admin` role or have been granted the `DROP` privilege on the specified sequence(s). By default, the `root` user belongs to the `admin` role.

### Syntax

```sql
DROP SEQUENCE [IF EXISTS] <sequence_name_list> [RESTRICT];
```

### Parameters

| Parameter | Description |
| --- | --- |
| `IF EXISTS` | Optional. <br>- When the `IF EXISTS` keyword is used, the system removes the sequence only if the target sequence has already existed. Otherwise, the system fails to remove the sequence without returning an error. <br>- When the `IF EXISTS` keyword is not used, the system removes the sequence only if the target sequence has already existed. Otherwise, the system fails to remove the sequence and returns an error. |
| `seq_name_list` | A comma-separated list of sequence names. You can use the `SHOW CREATE TABLE <table_name>` statement to get existing sequence names. |
| `RESTRICT` | (Default) Optional. Do not remove the sequence if any objects depend on it. |

### Examples

This example removes the `orders_list_seq` from the `sequences` table under the `information_ schema` schema in `db1` database.

```sql
-- 1. Check all sequences in db1 database.

SELECT * FROM db1.information_schema.sequences;
  sequence_catalog | sequence_schema |  sequence_name  | data_type | numeric_precision | numeric_precision_radix | numeric_scale | start_value |    minimum_value     | maximum_value | increment | cycle_option
-------------------+-----------------+-----------------+-----------+-------------------+-------------------------+---------------+-------------+----------------------+---------------+-----------+---------------
  db1              | public          | orders_list_seq | bigint    |                64 |                       2 |             0 | -1          | -9223372036854775808 | -1            | -2        | NO
(1 row)

-- 2. Remove the orders_list_seq sequence.

DROP SEQUENCE orders_list_seq;
DROP SEQUENCE

-- 3. Check all sequences in db1 database.

SELECT * FROM information_schema.sequences;
  sequence_catalog | sequence_schema | sequence_name | data_type | numeric_precision | numeric_precision_radix | numeric_scale | start_value | minimum_value | maximum_value | increment | cycle_option
-------------------+-----------------+---------------+-----------+-------------------+-------------------------+---------------+-------------+---------------+---------------+-----------+---------------
(0 rows)
```
