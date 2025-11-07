KWDB---
title: Cursors
id: declare-sql
---

# Cursors

KWDB supports using cursors in stored procedures.

::: warning Note
After declaring a cursor, you cannot use it until open the cursor. For details about how to declare a cursor, see [Declare Cursors](../other-sql-statements/declare-sql.md#declare-cursors).
:::

## OPEN

The `OPEN` statement opens a previously declared cursor.

### Privileges

N/A

### Syntax

![](../../../static/sql-reference/open_cursor.png)

### Parameters

| Parameter | Description |
| --- | --- |
| `cursor_name` | The name of the cursor to open.|

### Examples

```sql
DELIMITER \\
CREATE PROCEDURE process_cursor_example1()
BEGIN 
    declare var_done int; 
    declare var_age int; 
    DECLARE cur CURSOR FOR SELECT age FROM employees; 
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET var_done = 1; 
    OPEN cur;
    SELECT * FROM employees;
    LABEL my_loop: 
    WHILE var_done = 0 DO 
        FETCH cur INTO var_age; 
        select var_age;
        IF var_done = 1 THEN
            LEAVE my_loop; 
        ENDIF;                        
    ENDWHILE my_loop; 
    CLOSE cur;        
END \\
```

## FETCH

The `FETCH` statement fetches values of data and applies them to the specified variables. When applying values to the specified variables, the number of variables specified in the `FETCH` statement must match the number of columns retrieved by the `SELECT` statement when declaring the cursor. You can use the `CONTINUE HANDLER` statement to stop fetching cursors or use other methods to exit `FETCH` loops. If you cannot stop fetching cursors properly, you cannot fetch values of the data and the system returns the `the fetch cursor has no more data` error.

### Privileges

N/A

### Syntax

![](../../../static/sql-reference/fetch_cursor.png)

### Parameters

| Parameter | Description |
| --- | --- |
| `cursor_name` | The name of the cursor to fetch. |
| `cursor_list` | A comma-separated list of variables to be applied with values. |

### Examples

```sql
DELIMITER \\
CREATE PROCEDURE into_pre() 
 BEGIN
    DECLARE val int; 
    DECLARE cur1 cursor for select a from t1;
    OPEN cur1;
    FETCH cur1 INTO val;
    CLOSE cur1;
    SELECT val;
 END \\ 
```

## CLOSE

The `CLOSE` statement closes a previously opened cursor. After being closed, a cursor cannot be used until it is re-opened.

### Privileges

N/A

### Syntax

![](../../../static/sql-reference/close_cursor.png)

### Parameters

| Parameter | Description |
| --- | --- |
| `cursor_name` | The name of the cursor to close. |

### Examples

```sql
DELIMITER \\
CREATE PROCEDURE into_pre1() 
 BEGIN
    DECLARE val int4; 
    DECLARE cur2 cursor for select a from t2;
    OPEN cur2;
    FETCH cur2 INTO val;
    CLOSE cur2;
 END \\ 
```
