---
title: NULL Value Handling
id: null-value-mgmt 
---

# NULL Value Handling

KWDB supports inserting `NULL` values into columns that are not defined as `NOT NULL`, and supports computing and querying the inserted `NULL` values.

## Insert NULL Values

When creating a table, if a column is not defined as `NOT NULL`, you can insert `NULL` values into that column.

::: warning Note
When inserting data into a table, the system performs a nullability check on the columns. If the target column is defined as `NOT NULL`, you cannot insert `NULL` values. Otherwise, the system returns an error.
:::

The following example creates a time-series table `nulls` and inserts `NULL` values into the table.

```sql
-- 1. Create a time-series table that allows NULL values
CREATE TABLE nulls (ts TIMESTAMP NOT NULL, power INT, speed INT) TAGS (id INT NOT NULL, site INT) PRIMARY TAGS (id);
CREATE TABLE

-- 2. Insert NULL values
INSERT INTO nulls VALUES ('2024-01-01 10:00:00', 10, 219, 1, 1), ('2024-01-01 10:10:00', 11, 220, 1, 1), ('2024-01-01 10:20:00', 14, 225, 1, 1), ('2024-01-01 10:30:00', NULL, 225, 1, 1), ('2024-01-01 10:40:00', NULL, NULL, 1, 1);
INSERT 5

-- 3. View table data
SELECT * FROM nulls;
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

When querying table data using the `SELECT` statement, if the query results contain `NULL` values, NULL will be displayed.

```sql
SELECT * FROM nulls;
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

KWDB supports NULL value calculations in scenarios involving aggregate functions, arithmetic operations, and other built-in functions. The calculation rules are as follows:

- Query scenarios

    - When querying NULL values using the `SELECT` statement, the corresponding NULL value results are displayed as NULL.

        ```sql
        SELECT * FROM nulls;
        ts             | power | speed | id | site
        ----------------------------+-------+-------+----+-------
        2024-01-01 10:00:00+00:00 |    10 |   219 |  1 |    1
        2024-01-01 10:10:00+00:00 |    11 |   220 |  1 |    1
        2024-01-01 10:20:00+00:00 |    14 |   225 |  1 |    1
        2024-01-01 10:30:00+00:00 | NULL  |   225 |  1 |    1
        2024-01-01 10:40:00+00:00 | NULL  | NULL  |  1 |    1
        (5 rows)
        ```

    - Any simple comparison operation with NULL results in NULL.

        ```sql
        SELECT 1 = NULL;
        ?column?
        --------
        NULL
        
        SELECT 4 IN (1, 2, NULL);
        ?column?
        --------
        NULL
        ```

    - When using less than (`<`), greater than (`>`), or equals (`=`) to compare with NULL in WHERE clauses, zero rows are returned because the comparison result is NULL (neither TRUE nor FALSE).

        ```sql
        SELECT power FROM nulls WHERE power > NULL;
        power
        ---
        Output has 0 rows
        ```

    - When checking for NULL values in WHERE clauses, use the `IS NULL` or `IS NOT NULL` syntax.

        ```sql
        SELECT power FROM nulls WHERE power IS NULL;
        power
        -----
        NULL
        NULL
        ```

    - Except for the `IS NULL` or `IS NOT NULL` filter statements in WHERE clauses, NULL values do not participate in calculations in all other cases, and rows with NULL values are ignored.

        ```sql
        SELECT power FROM nulls WHERE power > 1;
        power
        -----
        10
        11
        14
        ```

- Aggregate operations

    - When using `count(*)` to count the number of rows, the result includes rows with NULL values.

        ```sql
        SELECT COUNT(*) FROM nulls;
        count
        ---
        5
        (5 rows)
        ```

    - NULL values do not participate in calculations for SUM, AVG, COUNT, FIRST, LAST, and other aggregate functions when aggregating specified columns.

        ```sql
        SELECT AVG(power) FROM nulls;
                avg
        -------------------------
            11.666666666666666667
        (1 row)
        ```

- Math and numeric functions

    Arithmetic operations and mathematical operations such as `round()` and `pow()` that involve NULL values yield a NULL result.

    ```sql
    SELECT power+1 FROM nulls;
    ?column?
    ---
    11
    12
    15
    NULL
    NULL
    (5 rows)
    ```

- Date and time functions

    Functions such as `DAY()`, `DATE()`, and `ADDTIME()` that involve NULL values yield a NULL result.

- String functions

    String functions such as LOWER, RIGHT, and LOCATE that involve NULL values yield a NULL result.