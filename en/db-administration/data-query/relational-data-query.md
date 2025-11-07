---
title: Relational Data Query
id: relational-data-query
---

# Relational Data Query

The relational database supports executing simple and more complex queries using SQL statements. For details, see [SQL Reference](../../../en/sql-reference/dml/relational-db/relational-select.md).

## Simple Query

The simple `SELECT` clause is the main SQL syntax to read and process existing data. When used as a standalone statement, the simple `SELECT` clause is also called the `SELECT` statement. However, it is also a selection clause that can be combined with other constructs to form more complex queries.

KWDB supports addition and subtraction operations of time in queries for timestamp-typed columns or timestamp constants, and for functions and expressions whose result is timestamp. KWDB supports comparing the operation results using the greater than sign (`>`), the less than sign (`<`), the equals sign (`=`), the greater than or equal to sign (`>=`), and the less than or equal to sign (`<=`). The addition and subtraction operations can include the `interval` constant, other timestamp-typed columns, and the functions and expressions whose result is interval, timestamp, or timestampz. If both sides of the operator are timestamp-typed or timestamptz-typed columns, only subtraction is supported. 

In addition and subtraction operations, the supported units for the `interval` constant include microsecond (us), millisecond (ms), second (s), minute (m), hour (h), day (d), week (w), month (mon), and year (y). Currently, KWDB does ​not​ support composite time formats, such as `1d1h`.

The valid ranges for millisecond, second, minute, and hour are constrained by the maximum value of nanosecond (INT64). The table below specifies the supported value ranges:

| Unit             | Range                                     |
|------------------|-------------------------------------------|
| Microsecond (us) | [-62,167,219,200,000, 31,556,995,200,000] |
| Millisecond (ms) | [-62,167,219,200,000, 31,556,995,200,000] |
| Second (s)       | [-9,223,372,036, 9,223,372,036]           |
| Minute (m)       | [-153,722,867, 153,722,867]               |
| Hour (h)         | [-2,562,047, 2,562,047]                   |

The valid ranges for day, week, month, and year are constrained by the results of addition and subtraction operations, whose corresponding number of microseconds must not exceed the range of INT64.

::: warning Note

KWDB supports using the addition and subtraction operations of time in the following cases:

- `SELECT` list: such as `SELECT ts+1h FROM table1;`, which means to return the results based on the specified time (the column's timestamp + one hour).
- `WHERE` clause: such as `SELECT * FROM table1 WHERE ts+1h > now();`, which means to return the results whose specified time (the column's timestamp + one hour) is greater than the current time.
- `ORDER BY` clause: such as `SELECT * FROM table1 ORDER BY ts+1h;`, which means to sort columns based on the specified time (the column's timestamp + one hour).
- `HAVING` clause: such as `SELECT MAX(ts) FROM table1 GROUP BY ts HAVING ts+1h > now();`, which means to filter the qualified grouped results.
- Recall functions whose parameter type is set to timestamp: such as `SELECT CAST(ts+1h AS timestamp) FROM table1;`, which means to convert the results based on the specified time (the column's timestamp + one hour) into timestamp-typed values.
- Use comparison operations to indicate the join condition: such as `SELECT * FROM table1,table2 WHERE table1.ts+1h > table2.ts;`, which means to use the addition and subscription operations when joining two tables.

:::

### Privileges

The user must be a member of the `admin` role or have been granted the `SELECT` privilege on the specified table(s).

### Syntax

For details about the syntax used to query relational data, see [SQL Reference](../../../en/sql-reference/dml/relational-db/relational-select.md#syntax).

### Parameters

For details about the parameters used to query relational data, see [SQL Reference](../../../en/sql-reference/dml/relational-db/relational-select.md#parameters).

### Examples

These examples assume that you have created a table and inserted data into the table.

```sql
-- 1. Create a table named accounts.

CREATE TABLE accounts(id INT8 DEFAULT unique_rowid() PRIMARY KEY, name STRING, balance DECIMAL, enabled BOOL);
CREATE TABLE

-- 2. Insert data into the table.

INSERT INTO accounts VALUES (1, 'lily', 10000.5, true), (2, 'ruarc', 20000.75, true), (3, 'tullia', 30000, false), (4, 'arturo', 45000, false);
INSERT 4
```

- Retrieve specific columns.

    ```sql
    SELECT id FROM accounts WHERE balance < 21000;
    id
    --
    1 
    2 
    (2 rows)
    ```

- Retrieve all columns.

    ```sql
    SELECT * FROM accounts;
    id|name  |balance |enabled
    --+------+--------+-------
    1 |lily  |10000.5 |t      
    2 |ruarc |20000.75|t      
    3 |tullia|30000   |f      
    4 |arturo|45000   |f      
    (4 rows)
    ```

- Filter the table on a single condition.

    ```sql
    SELECT id FROM accounts WHERE balance < 21000;
    id
    --
    1 
    2 
    (2 rows)
    ```

- Filter the table on multiple conditions.

    ```sql
    SELECT * FROM accounts WHERE balance > 25000 AND enabled = false;
    id|name  |balance|enabled
    --+------+-------+-------
    3 |tullia|30000  |f      
    4 |arturo|45000  |f      
    (2 rows)
    ```

- Filter the non-duplicate rows. Columns without primary keys or UNIQUE constraints may have the same value.

    ```sql
    -- 1. Insert data into the accounts table.

    INSERT INTO accounts VALUES (5, 'lily', 50000.5, true);
    INSERT 1

    -- Query data with the enabled=true setting.

    SELECT name FROM accounts WHERE enabled=true;
    name 
    -----
    lily 
    ruarc
    lily 
    (3 rows)
    ```

- Use the `DISTINCT` keyword to remove all but one instance of duplicate values from your retrieved data.

    ```sql
    SELECT DISTINCT name FROM accounts WHERE enabled=true;
    name 
    -----
    lily 
    ruarc
    (2 rows)
    ```

- Use the `WHERE <column> IN (<a comma-separated list of values>)` clause to filter the table.

    ```sql
    SELECT name FROM accounts WHERE balance in (10000.5, 20000.75);
    name 
    -----
    lily 
    ruarc
    (2 rows)
    ```

- Use the `AS` keyword to rename a column's name in output.

    ```sql
    SELECT name AS n, balance FROM accounts WHERE enabled=true;
    n    |balance 
    -----+--------
    lily |10000.5 
    ruarc|20000.75
    lily |50000.5 
    (3 rows)
    ```

- Search for string values.

    Search for partial string that matches in columns using `LIKE`, which supports the following wildcard operators:

    - `%`: match `0` or multiple characters.
    - `_`: match exactly `1` character.
    - `[charlist]`: match any character listed in `charlist`.
    - `charlist` or `[!charlist]`: do not match any character listed in `charlist`.

    ```sql
    SELECT * FROM accounts WHERE name LIKE '%li%';
    id|name  |balance|enabled
    --+------+-------+-------
    1 |lily  |10000.5|t      
    3 |tullia|30000  |f      
    5 |lily  |50000.5|t      
    (3 rows)
    ```

- Use aggregate functions to perform computation on retrieved rows.

    ```sql
    SELECT MIN(balance) FROM accounts;
    min    
    -------
    10000.5
    (1 row)
    ```

    KWDB supports using the retrieved value as part of the `WHERE` clause expression.

    ```sql
    SELECT id, name, balance FROM accounts WHERE balance = (SELECT MIN(balance) FROM accounts);
    id|name|balance
    --+----+-------
    1 |lily|10000.5
    (1 row)
    ```

- Perform aggregate function on retrieved rows.

    ```sql
    SELECT SUM(balance) FROM accounts WHERE enabled=true;
    SUM     
    --------
    80001.75
    (1 row)
    ```

- Use `FILTER (WHERE <Boolean expression>)` to filter columns fed into aggregate functions. Data that return `FALSE` or `NULL` for the `FILTER` clause's Boolean expression are not fed into the aggregate function.

    ```sql
    SELECT count(*) AS unfiltered, count(*) FILTER (WHERE balance > 15000) AS filtered FROM accounts; 
    unfiltered|filtered
    ----------+--------
    5         |4       
    (1 row)
    ```

- Split the retrieved rows into groups and then perform the aggregate function on each of them.

    ```sql
    SELECT enabled AS state, SUM(balance) AS state_balance FROM accounts GROUP BY enabled;
    state|state_balance
    -----+-------------
    t    |80001.75     
    f    |75000        
    (2 rows)
    ```

- Use the `HAVING` clause to filter aggregate groups.

    ```sql
    SELECT enabled AS state, SUM(balance) AS state_balance FROM accounts GROUP BY enabled HAVING AVG(balance) between 100 AND 30000;
    state|state_balance
    -----+-------------
    t    |80001.75     
    (1 row)
    ```

- Use aggregate functions in the `HAVING` clause.

    ```sql
    SELECT name, enabled FROM accounts WHERE enabled = true GROUP BY name, enabled HAVING count(name) > 1;
    name|enabled
    ----+-------
    lily|t      
    (1 row)
    ```

- Query tables using the `LIMIT` + `count` form.

    ```sql
    SELECT * FROM accounts LIMIT 5;
    id|name  |balance |enabled
    --+------+--------+-------
    1 |lily  |10000.5 |t      
    2 |ruarc |20000.75|t      
    3 |tullia|30000   |f      
    4 |arturo|45000   |f      
    5 |lily  |50000.5 |t      
    (5 rows)
    ```

- Query tables using the `FETCH FIRST` + `count` form.

    ```sql
    SELECT * FROM accounts FETCH FIRST 2 ROW ONLY;
    id|name |balance |enabled
    --+-----+--------+-------
    1 |lily |10000.5 |t      
    2 |ruarc|20000.75|t      
    (2 rows)
    ```

- Query tables using the `LIMIT` and `OFFSET` clauses.

    ```sql
    SELECT id, name FROM accounts LIMIT 1 OFFSET 1;
      id | name
    -----+-----------
      2 | Zhang San 
    (1 row)
    ```

- Query tables using the `OFFSET` and `NEXT` keywords.

    ```sql
    SELECT * FROM accounts OFFSET 2 rows FETCH NEXT 2 ROW ONLY;
      id |  name   | balance | enabled
    -----+---------+---------+----------
      3 | Zhao Si |   30000 |  false
      4 | Wang Wu |   45000 |  false
    (2 rows)
    ```
