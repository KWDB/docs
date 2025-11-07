---
title: Triggers
id: relational-trigger
---

# Triggers

To enable automated, reliable, and loosely-coupled service logic processing at the data layer while ensuring data integrity and consistency, KWDB supports triggers.

## CREATE TRIGGER

The `CREATE TRIGGER` statement creates a trigger for a specified table.

### Privileges

The user must be a member of the `admin` role or have been granted the `CREATE` privilege on the table associated with the specified trigger(s) and the privileges of related SQL statements in the trigger body. By default, the `root` user belongs to the `admin` role.

### Syntax

![](../../../../static/sql-reference/create_trigger.png)

### Parameters

| Parameter | Description |
| --- | --- |
| `IF NOT EXISTS` | Optional. <br>- When the `IF NOT EXISTS` keyword is used, the system creates a new trigger only if a trigger of the same name does not already exist. Otherwise, the system fails to create a new trigger without returning an error. <br>- When the `IF NOT EXISTS` keyword is not used, the system creates a new trigger only if a trigger of the same name does not already exist. Otherwise, the system fails to create a new trigger and returns an error.|
| `trigger_name` | The name of the trigger to create.    |
| `table_name` | The name of the table associated with the trigger.<br > **Note** <br >- The table associated with the trigger must be an ordinary relational table. <br >- Do not support performing any SQL operations on the associated table in the trigger body. <br >- When triggers associated with two tables have a mutual triggering relationship, the system returns an error when either trigger activates. |
| `trigger_time` | Specify the time to activate a trigger. Available options: <br >- `BEFORE`: The trigger activates before the SQL statement operation. <br >- `AFTER`: The trigger activates after the SQL statement. If there are both `BEFORE` and `AFTER` triggers on a table, an `AFTER` trigger is executed only if any `BEFORE` triggers and the row-level operations (`INSERT`、`UPDATE`、`DELETE`) execute successfully. <br > **Note** <br >- For statement-level triggers, an error during either a `BEFORE` or `AFTER` trigger results in failure of the entire statement that caused trigger activation. <br >- For row-level triggers, if the `BEFORE` triggers fails, the insert or update operation is not performed on the related rows. |
| `trigger_event` | Specify the event to activate a trigger. Available options: <br >- `INSERT`: The trigger activates when an `INSERT` statement is issued. <br >- `UPDATE`: The trigger activates when an `UPDATE` statement is issued. <br >- `DELETE`: The trigger activates when an `DELETE` statement is issued.  |
| `FOR EACH ROW` | Specify a row-level trigger, which activates once for each row that is affected by the statements.|
| `trigger_order` | Specify the order to activate a trigger. If there are multiple triggers defined on the same table, you can specify the order to activate triggers when creating them. Available options:  <br >- `FOLLOWS` <br >- `PRECEDES` <br > By default, the triggers activate in the order they were created.  |
| `other_trigger_name` | The names of other triggers. If there are multiple triggers defined on the same table, the triggers activate in the order they were created. |
| `trigger_body` | Specify the trigger body, including the SQL statements that activates the trigger. The trigger body supports performing multiple SQL statements and cross-table operations. When performing multiple SQL statements, you need to use the `BEGIN ... END` compound statement to encapsulate the SQL statements and use the `DELIMITER` statement to change the statement delimiter. You can also use the `OLD` and `NEW` aliases to reference columns in the associated table. <br >- `OLD.col_name`: Old table row affected by `UPDATE` and `DELETE` operations. The `DELETE` trigger can only use the `OLD` alias. <br >- `NEW.col_name`: New table row resulting from the `INSERT` and `UPDATE` operations. The `INSERT` trigger can only use the `NEW` alias.<br > **Note** <br >- The trigger body does not support DDL statements, transaction statements, `SELECT` statement, procedure statements, `PREPARE`, and `EXECUTE` statement.<br >- When the table that is performed by SQL statements in the trigger body is modified or removed, the trigger is not affected immediately. The system returns an error on the next time when the trigger activates. <br >- If you use KaiwuDB JDBC Driver to create a trigger, you should use the double dollars sign (`$$`) to wrap the `BEGIN ...END` statement. |

### Examples

This example creates a `BEFORE` trigger which activates and inserts data to the `audit_log` table when inserting data into the `orders` table.

```sql
-- Create the orders and audit_log tables.
create table orders (id int, name string, price float, time timestamp);
create table audit_log(id int, name string, price float, time timestamp, currentuser string);

-- Create a BEFORE trigger that activates before an INSERT is issued on the orders table.
delimiter \\
create trigger my_trigger
before insert
on orders for each row
begin
    insert into audit_log values (NEW.id, NEW.name, NEW.price, NEW.time, current_user());
end \\
delimiter ;

-- Insert data into the orders table.
insert into orders values (1, 'kwdb', 99.99, now());

-- Query data from the audit_log table.
select * from audit_log;
 id | name | price |               time                 |     current_user
-----+------+-------+-----------------------------------+-------------------
  1 | kwdb | 99.99 | 2025-04-28 09:26:45.028688+00:00.  |         kkk
```

## SHOW TRIGGERS

The `SHOW TRIGGERS` or `SHOW CREATE TRIGGER` statement to list all or specified triggers.

### Privileges

N/A

### Syntax

![](../../../../static/sql-reference/show_trigger.png)

### Parameters

| Parameter      | Description                                        |
|----------------|----------------------------------------------------|
| `trigger_name` | The name of the trigger to show.                   |
| `table_name`   | The name of the table associated with the trigger. |

### Examples

This example lists all triggers associated with the `orders` table.

```sql
SHOW TRIGGERS FROM orders;
```

If you succeed, you should see an output similar to the following:

```sql
  trigger_name | trigger_action_time | trigger_event | trigger_order | on_table | enabled
---------------+---------------------+---------------+---------------+----------+----------
  my_trigger   | BEFORE              | INSERT        |             1 | orders   |  true
(1 row)
```

## ALTER TRIGGER

The `ALTER TRIGGER...RENAME TO` statement renames a trigger.

### Privileges

The user must be a member of the `admin` role or have been granted the `DROP` privilege on the specified trigger(s). By default, the `root` user belongs to the `admin` role.

### Syntax

![](../../../../static/sql-reference/alter_trigger.png)

### Parameters

| Parameter          | Description                                        |
|--------------------|----------------------------------------------------|
| `trigger_name`     | The name of the trigger to modify.                 |
| `table_name`       | The name of the table associated with the trigger. |
| `new_trigger_name` | The new name of the trigger.                       |

### Examples

This example renames the `my_trigger` trigger that is associated with the `orders` table to `trigger_test`.

```sql
ALTER TRIGGER my_trigger ON orders RENAME TO trigger_test;
```

## DROP TRIGGER

The `DROP TRIGGER` statement removes a trigger.

### Privileges

The user must be a member of the `admin` role or have been granted the `DROP` privilege on the specified trigger(s). By default, the `root` user belongs to the `admin` role.

### Syntax

![](../../../../static/sql-reference/drop_trigger.png)

### Parameters

| Parameter | Description |
| --- | --- |
| `IF EXISTS` | Optional. <br>- When the `IF EXISTS` keyword is used, the system removes the trigger only if the trigger has already existed. Otherwise, the system fails to remove the trigger without returning an error. <br>- When the `IF EXISTS` keyword is not used, the system removes the trigger only if the trigger has already existed. Otherwise, the system fails to remove the trigger and returns an error.|
| `trigger_name` | The name of the trigger to remove. |
| `table_name` | The name of the table associated with the trigger. |

### Examples

This example removes the `trigger_test` trigger that is associated with the `orders` table.

```sql
DROP TRIGGER trigger_test ON orders;
```
