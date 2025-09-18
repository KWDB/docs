---
title: User-defined Functions
id: self-defined-functions-sql
---

# User-defined Functions

KWDB supports creating, using, viewing, and deleting user-defined functions that are defined using the Lua programming language. User-defined functions work like other built-in functions.

## CREATE FUNCTION

The `CREATE FUNCTION` statement creates a user-defined function.

### Privileges

The user must have been granted the `CREATE` privilege on the current database.

### Syntax

![](../../../static/sql-reference/UR6abHXW8o6CSLxaPkkcqVM7ntd.png)

### Parameters

| Parameter | Description |
| --- | --- |
| `IF NOT EXISTS` | Optional. <br>- When the `IF NOT EXISTS` keyword is used, the system creates a new user-defined function only if a user-defined function of the same name does not already exist. Otherwise, the system fails to create a new user-defined function without returning an error. <br>- When the `IF NOT EXISTS` keyword is not used, the system creates a new user-defined function only if a user-defined function of the same name does not already existed. Otherwise, the system fails to create a new user-defined function and returns an error. |
| `function_name` | The name of the user-defined function to create. The user-defined function name must be unique within the database. |
| `arguments` | A comma-separated list of user-defined function parameters, specifying the name and type. Available types: TIMESTAMP, INT2, INT4, INT8, FLOAT4, FLOAT8, CHAR, VARCHAR, NCHAR and NVARCHAR.|
| `return_type` | The type returned by the user-defined function. Available types: TIMESTAMP, INT2, INT4, INT8, FLOAT4, FLOAT8, CHAR, VARCHAR, NCHAR and NVARCHAR. |
| `function_content` | The body of the user-defined function, enclosed in single quotes (`''`). If there are any specical characters in the function body, the system will automatically change these special characters to be interpreted differently. For example, the system will change single quotes (`''`) to (`'`). |

### Examples

This example assumes that you have created a time-series database (`power`) and a time-series table (`consumption`), and inserted data into the table.

```sql
-- 1. Create a database named power.

CREATE TS DATABASE power;
CREATE TS DATABASE

-- 2. Use the power database.

USE power;
SET

-- 3. Create a table named consumption.

CREATE TABLE consumption (k_timestamp timestamp not null,c1 int,c2 int) tags (site int not null) primary tags (site);
CREATE TABLE

-- 4. Set the timezone for the database.
SET timezone = 8;
SET

-- 5. Insert data into the consumption table.

INSERT INTO consumption VALUES('2024-1-1 1:00:00',1,2,1),('2024-1-1 1:00:00',2,4,1),('2024-1-1 2:00:00',6,3,1),('2024-1-1 5:00:00',8,12,1),('2024-1-1 5:00:00',0,3,1);
INSERT 5
```

This example creates a user-defined function and uses the function to view the growth rate of the `consumption` table.

```sql
-- 1. Create a user-defined function named calculate_growth_rate.

CREATE FUNCTION calculate_growth_rate(previous_consumption int, current_consumption int)
    RETURNS FLOAT
    LANGUAGE LUA
BEGIN
'function calculate_growth_rate(previous_consumption, current_consumption)
  if previous_consumption == 0 then
        return nil
    end
  return (current_consumption - previous_consumption) / previous_consumption
end'
END;
CREATE FUNCTION

-- 2. View the growth rate of the `consumption` table using the calculate_growth_rate user-defined function.

SELECT calculate_growth_rate(c1,c2) from consumption where k_timestamp >= '2024-1-1 1:00:00' and k_timestamp <= '2024-1-1 5:00:00';

    calculate_growth_rate
----------------------------------
                        1
                      -0.5
NULL
(3 rows)
```

## SHOW FUNCTIONS

The `SHOW FUNCTIONS` statement lists all user-defined functions or details about a specified user-defined function.

### Privileges

N/A

### Syntax

- List all user-defined functions

    ![](../../../static/sql-reference/AdVHbGmyxoXQNhxlR35c1a8in4c.png)

- List details of a specified user-defined function

    ![](../../../static/sql-reference/IG4NbcrqIoNWpAxVu1gcNzqbnVb.png)

### Parameters

| Parameter       | Description                                    |
|-----------------|------------------------------------------------|
| `function_name` | The name of the user-defined function to view. |

### Examples

- View all user-defined functions.

    ```sql
    SHOW FUNCTIONS;
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
          function_name
    ---------------------------
      calculate_growth_rate
    ```

- View details of a specified user-defined function.

    ```sql
    SHOW FUNCTION calculate_growth_rate;
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
          function_name     | argument_types | return_type | function_type | language
    ------------------------+----------------+-------------+---------------+-----------
      calculate_growth_rate | INT, INT       | DOUBLE      | function      | LUA
    (1 row)
    ```

## DROP FUNCTION

The `DROP FUNCTION` statement removes a user-defined functions from a database.

### Privileges

The user must have been granted the `CREATE` privilege on the current database.

### Syntax

![](../../../static/sql-reference/El3zb8KrUo4qQoxQPuycjOJunTc.png)

### Parameters

| Parameter | Description |
| --- | --- |
| `IF EXISTS` | Optional. <br>- When the `IF EXISTS` keyword is used, the system removes a user-defined function only if the target user-defined function has already existed. Otherwise, the system fails to remove the user-defined function without returning an error. <br>- When the `IF EXISTS` keyword is not used, the system removes a user-defined function only if the target user-defined function has already existed. Otherwise, the system fails to remove the user-defined function and returns an error. |
| `function_name` | The name of the user-defined function to remove. |

### Examples

This example removes a user-defined function named `calculate_growth_rate`.

```sql
DROP FUNCTION calculate_growth_rate;
```
