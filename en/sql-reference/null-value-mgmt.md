---
title: NULL Value Handling
id: null-value-mgmt 
---

# NULL Value Handling

KWDB supports inserting `NULL` values into columns without defining `NOT NULL`, as well as computing and querying inserted `NULL` values.

## Insert NULL Values

When creating a table, if a column is not defined as `NOT NULL`, you can insert the `NULL` value into the column.

::: warning Note
When inserting data into a table, the system will check the nullability on the specified columns. If the specified columns are defined as `NOT NULL`, you cannot insert `NULL` values into the column. Otherwise, the system returns an error.
:::

This example creates a table and inserts `NULL` values into the table.

```sql
-- 1. Create a table and allow inserting Null values into the table.
create table nulls (ts timestamp not null, power int, speed int) tags (id int not null, site int) primary tags (id);
CREATE TABLE

-- 2. Insert NULL values.
insert into nulls values ('2024-01-01 10:00:00', 10, 219, 1, 1), ('2024-01-01 10:10:00', 11, 220, 1,1), ('2024-01-01 10:20:00', 14, 225, 1,1), ('2024-01-01 10:30:00',
null,225,1,1), ('2024-01-01 10:40:00', null, null, 1,1);
INSERT 5

-- 3. Check data of the table.
select * from nulls;
             ts             | power | speed | id | site
----------------------------+-------+-------+----+-------
  2024-01-01 10:00:00+00:00 |    10 |   219 |  1 |    1
  2024-01-01 10:10:00+00:00 |    11 |   220 |  1 |    1
  2024-01-01 10:20:00+00:00 |    14 |   225 |  1 |    1
  2024-01-01 10:30:00+00:00 | NULL  |   225 |  1 |    1
  2024-01-01 10:40:00+00:00 | NULL  | NULL  |  1 |    1
(5 rows)
```

## Query NULL Values

When querying data using the `SELECT` statement, `NULL` will be printed to the output if there are any `NULL` values in the query results.

```sql
select * from nulls;
             ts             | power | speed | id | site
----------------------------+-------+-------+----+-------
  2024-01-01 10:00:00+00:00 |    10 |   219 |  1 |    1
  2024-01-01 10:10:00+00:00 |    11 |   220 |  1 |    1
  2024-01-01 10:20:00+00:00 |    14 |   225 |  1 |    1
  2024-01-01 10:30:00+00:00 | NULL  |   225 |  1 |    1
  2024-01-01 10:40:00+00:00 | NULL  | NULL  |  1 |    1
(5 rows)
```

## Rules for Calculating NULL Values

KWDB supports comparing NULL values with aggregate functions and arithmetic operations.

- Query scenarios

    - When querying data using the `SELECT` statement, `NULL` will be printed to the output if there are any `NULL` values in the query results.

        ```sql
        select * from nulls;
        ts             | power | speed | id | site
        ----------------------------+-------+-------+----+-------
        2024-01-01 10:00:00+00:00 |    10 |   219 |  1 |    1
        2024-01-01 10:10:00+00:00 |    11 |   220 |  1 |    1
        2024-01-01 10:20:00+00:00 |    14 |   225 |  1 |    1
        2024-01-01 10:30:00+00:00 | NULL  |   225 |  1 |    1
        2024-01-01 10:40:00+00:00 | NULL  | NULL  |  1 |    1
        (5 rows)
        ```

    - Use the `IS NULL` or `IS NOT NULL` in the `WHERE` clauses when checking for `NULL` values.

        ```sql
        SELECT power FROM nulls WHERE power is NULL;
        power
        -----
        NULL
        NULL
        ```

    - Any comparison between arithmetic operations (`<`, `>`, `=`) and `NULL` values results in zero rows.

        ```sql
        SELECT power FROM nulls WHERE power > NULL;
        power
        ---
        Output has 0 rows
        ```

    - Except for the `IS NULL` or `IS NOT NULL` in the `WHERE` clauses, `NULL` values are not calculated in other cases.

        ```sql
        SELECT power FROM nulls WHERE power > 1;
        power
        -----
        10
        11
        14
        ```

- Aggregate calculation

    - When using the `count(*)` aggregate function to count the number of rows, the result includes the number of rows whose values are `NULL` values.

        ```sql
        select count(*) from nulls;
        count
        ---
        5
        (5 rows)
        ```

    - `NULL` values are not considered in the calculation of the `SUM`, `AVG`, `COUNT`, `FIRST`, `LAST` aggregate functions.

        ```sql
        select avg(power) from nulls;
                  avg
        -------------------------
          11.666666666666666667
        (1 row)
        ```

- FLOAT and INT functions

    Arithmetic operations, as well as the `round()` and `pow()` functions that involve a `NULL` value will yield a `NULL` result.

    ```sql
    select power+1 from nulls;
    ?column?
    ---
    11
    12
    15
    NULL
    NULL
    (5 rows)
    ```

- Date and Time functions

    `DAY()`, `DATE()`, and `ADDTIME()` date and time functions that involve a `NULL` value will yield a `NULL` result.

- String functions

    `LOWER`, `RIGHT`, and `LOCATE` functions that involve a `NULL` value will yield a `NULL` result.
