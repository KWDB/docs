---
title: UPSERT
id: relational-upsert
---

# UPSERT

In semantic, the `UPSERT` statement is equivalent to `INSERT ON CONFLICT`. However, these two statements have some performance differences.

- The `UPSERT` statement considers UNIQUE constraints only for Primary Key columns. The `UPSERT` statement inserts rows in cases where specified values do not violate UNIQUE constraints and updates rows in cases where values do violate UNIQUE constraints. If there are UNIQUE constraints only on non Primary Key columns, the system returns an error when executing the `UPSERT` statement.
- The `INSERT ON CONFLICT` statement is more flexible. Besides for Primary Key columns, the statement also considers UNIQUE constraints on non Primary Key columns. Although this will make codes longer and complex, it can efficiently avoid execution failure of the `INSERT ON CONFLICT` statement when there are UNIQUE constraint conflicts on non Primary Key columns.

## Privileges

The user must be a member of the `admin` role or have been granted the `SELECT`, `INSERT`, and `UPDATE` privileges on the specified table(s).

## Syntax

![](../../../../static/sql-reference/AExgblNWSoRmDKxBhxNcz8V7nod.png)

- `common_table_expr`

    ![](../../../../static/sql-reference/QiRPb7cOXoZvlix9J1occRfinpb.png)

- `target_list`

    ![](../../../../static/sql-reference/CVUabRcaqojAxXxeTBDcwgRpnHK.png)

## Parameters

| Parameter | Description |
| --- | --- |
| `common_table_expr` | You can use it in combination with the `WITH` keyword as the `WITH AS` clause. It provides an alias for a frequently-performed SQL subquery before it is used in a larger query context. Therefore, the system can directly recall the SQL subquery using the alias. This improves the query performance. |
| `table_name` | The name of the table that contains the rows to update.  |
| `AS table_alias_name` | An alias for the table name. When an alias is provided, it completely hides the actual table name. |
| `column_name` | A comma-separated list of names of columns to update. If no column name is specified, update all columns of the table. |
| `select_stmt` | A selection query to generate data to be inserted into the table. Each value must match the data type of its column. If column names are specified, values must be in corresponding order. Otherwise, values must follow the declared order of the columns in the table. |
| `DEFAULT VALUES` | To fill all columns with their default values, use `DEFAULT VALUES` in place of `select_stmt`. To fill a specific column with its default value, do not specify a value for the column in the `SELECT` statement or use `DEFAULT` at the appropriate position.|
| `RETURNING target_list` | Return values based on rows upserted, where `target_list` can be specific column names from the table. `*` means returning values for all columns while you can also use computations using scalar expressions to specify columns. To return nothing in the response, not even the number of rows updated, use `RETURNING NOTHING`. |

## Examples

These examples assume that you have created a table and inserted data into the table.

```sql
-- 1. Crete a table named accounts.

CREATE TABLE accounts(id INT8 DEFAULT unique_rowid() PRIMARY KEY, balance DECIMAL);
CREATE TABLE 

-- 2. Insert data into the table.

INSERT INTO accounts (id, balance) VALUES (1, 10000.5), (2, 20000.75);
INSERT 2

-- 3. Check data of the table.

SELECT * FROM accounts;                         
id | balance 
---+---------
1  | 10000.5 
2  | 20000.75
(2 rows)
```

- Upsert a row when the specified values do not violate UNIQUE constraints.

    ```sql
    UPSERT INTO accounts (id, balance) VALUES (3, 6325.20);
    INSERT 1

    SELECT * FROM accounts;
    id|balance 
    --+--------
    1 |10000.5 
    2 |20000.75
    3 |6325.20 
    (3 rows)
    ```

- Upsert multiple rows when the specified values do not violate UNIQUE constraints.

    ```sql
    UPSERT INTO accounts (id, balance) VALUES (4, 1970.4), (5, 2532.9), (6, 4473.0);
    INSERT 3

    SELECT * FROM accounts;
    id|balance 
    --+--------
    1 |10000.5 
    2 |20000.75
    3 |6325.20 
    4 |1970.4  
    5 |2532.9  
    6 |4473.0  
    (6 rows)
    ```

- Update a row when the specified values violate UNIQUE constraints.

    ```sql
    SELECT * FROM accounts;
    id|balance 
    --+--------
    1 |10000.5 
    2 |20000.75
    3 |6325.20 
    4 |1970.4  
    5 |2532.9  
    6 |4473.0  
    (6 rows)


    UPSERT INTO accounts (id, balance) VALUES (3, 7500.83);
    INSERT 1


    SELECT * FROM accounts;
    id|balance 
    --+--------
    1 |10000.5 
    2 |20000.75
    3 |7500.83 
    4 |1970.4  
    5 |2532.9  
    6 |4473.0  
    (6 rows)
    ```

- Fail to update rows when the UNIQUE constraint conflict is on non Primary Key columns.

    ```sql
    SELECT * FROM accounts;
    id|balance 
    --+--------
    1 |10000.5 
    2 |20000.75
    3 |7500.83 
    4 |1970.4  
    5 |2532.9  
    6 |4473.0  
    (6 rows)

    -- Add the UNIQUE constraint to a non Primary Key column.
    ALTER TABLE accounts ADD CONSTRAINT unique_balance UNIQUE (balance);
    ALTER TABLE

    -- The inserted values violate UNIQUE constraints.

    UPSERT INTO accounts VALUES (7, 1970.4);
    ERROR:  duplicate key value (balance)=(1970.4) violates unique CONSTRAINT "accounts_balance_key"
    ```

    In this case, the `INSERT ON CONFLICT` statement is more flexible.

    ```sql
    INSERT INTO accounts VALUES (7, 1970.4) ON CONFLICT (balance) DO UPDATE SET id = excluded.id;
    INSERT 1


    SELECT * FROM accounts;
    id|balance 
    --+--------
    1 |10000.5 
    2 |20000.75
    3 |7500.83 
    5 |2532.9  
    6 |4473.0  
    7 |1970.4  
    (6 rows)
    ```
