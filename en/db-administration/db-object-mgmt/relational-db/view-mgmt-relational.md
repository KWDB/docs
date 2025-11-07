---
title: Views
id: view-mgmt-relational
---

# Views

## CREATE VIEW

The `CREATE VIEW` statement creates a new view, which is a stored query represented as a virtual table.

### Privileges

The user must be a member of the `admin` role or have been granted the `CREATE` privilege on the parent database and the `SELECT` privilege on any table(s) referenced by the view. By default, the `root` user belongs to the `admin` role.

### Syntax

```sql
CREATE VIEW [IF NOT EXISTS] <view_name> [(<name_list>)] AS <select_stmt>;
```

### Parameters

| Parameter | Description |
| --- | --- |
| `IF NOT EXISTS` | Optional. <br>- When the `IF NOT EXISTS` keyword is used, the system creates a new view only if a view of the same name does not already exist. Otherwise, the system fails to create a view table without returning an error. <br>- When the `IF NOT EXISTS` keyword is not used, the system creates a new view only if a view of the same name does not already exist. Otherwise, the system fails to create a new view and returns an error.  |
| `view_name` | The name of the view to create. The view name must be unique within the database and must follow these [Identifier Rules](../../../../en/sql-reference/sql-identifiers.md). When the parent database is not set as the default, the name must be formatted as `database.view_name`. |
| `name_list` | An optional, comma-separated list of column names for the view. If specified, these names will be used in the response instead of the columns specified in the `select_stmt` statement. |
| `select_stmt` | The selection query to execute when the view is requested. Currently, it is possible to use `*` to select all columns from a referenced table. <br >- Where there are duplicate columns in the result set, the system returns the `duplicate column name: "a"` error. <br >- When new columns are added to the original table, the view structure is not changed. <br >- When deleting a column referenced by the view from the original table, the system returns the `cannot drop column "b" because view "v" depends on it` error. |

### Examples

```sql
-- 1. Check data of the orders table.

SELECT * FROM orders;
  customer_id |   id   | total
--------------+--------+--------
       100001 | 100001 |   234
       100001 | 100002 |   120
       100002 | 100003 |    59
       100002 | 100004 |   120
(4 rows)

-- 2. Create a view named short_order for the orders table to get the order id and order amount. 

CREATE VIEW short_order (id, amount) AS SELECT id, total FROM orders;
CREATE VIEW

-- 3. Check the view. 

SELECT * FROM short_order;
    id   | amount
---------+---------
  100001 |    234
  100002 |    120
  100003 |     59
  100004 |    120
(4 rows)
```

## ALTER VIEW

The `ALTER VIEW` statement changes the name of a view.

### Privileges

The user must be a member of the `admin` role or have been granted the `DROP` privilege on the current view and the `CREATE` privilege on the parent database of the renamed view. By default, the `root` user belongs to the `admin` role.

### Syntax

```sql
ALTER VIEW [IF EXISTS] <view_name> RENAME TO <name>;
```

### Parameters

| Parameter | Description |
| --- | --- |
| `IF EXISTS` | Optional. <br>- When the `IF EXISTS` keyword is used, the system updates the view only if the target view has already existed. Otherwise, the system fails to update the view without returning an error. <br>- When the `IF EXISTS` keyword is not used, the system updates the view only if the target view has already existed. Otherwise, the system fails to update the view and returns an error. |
| `view_name` | The current name of the view to rename. You can use the `SELECT * FROM information_schema.tables WHERE table_type = 'VIEW'` statement to get existing view names. |
| `name` | The new name of the view. The view name must be unique within the database and must follow these [Identifier Rules](../../../../en/sql-reference/sql-identifiers.md). |

### Examples

This example renames the `test_view` view to `names`.

```sql
-- 1. Check all views. 

SELECT * FROM information_schema.tables WHERE table_type = 'VIEW';
  table_catalog | table_schema | table_name  | table_type | is_insertable_into | version | namespace_oid
----------------+--------------+-------------+------------+--------------------+---------+----------------
  db2           | public       | test_view   | VIEW       | NO                 |       1 |    1497612465
  db2           | public       | short_order | VIEW       | NO                 |       1 |    1497612465
(2 rows)

-- 2. Rename the test_view view to names.

ALTER VIEW test_view rename to names;
RENAME VIEW

-- 3. Check all views. 

SELECT * FROM information_schema.tables WHERE table_type = 'VIEW';
  table_catalog | table_schema | table_name  | table_type | is_insertable_into | version | namespace_oid
----------------+--------------+-------------+------------+--------------------+---------+----------------
  db2           | public       | names       | VIEW       | NO                 |       3 |    1497612465
  db2           | public       | short_order | VIEW       | NO                 |       1 |    1497612465
(2 rows)
```

## DROP VIEW

The `DROP VIEW` statement removes a view from a database.

### Privileges

- Remove a view with no dependency: the user must be a member of the `admin` role or have been granted the `DROP` privilege on the specified view(s). By default, the `root` user belongs to the `admin` role.
- Remove a view with dependencies: the user must be a member of the `admin` role or have been granted the `DROP` privilege on the specified view(s) and its dependent objects. By default, the `root` user belongs to the `admin` role.

### Syntax

```sql
DROP VIEW [IF EXISTS] <view_name_list> [CASCADE | RESTRICT];
```

### Parameters

| Parameter | Description |
| --- | --- |
| `IF EXISTS` | Optional. <br>- When the `IF EXISTS` keyword is used, the system removes the view only if the target view has already existed. Otherwise, the system fails to remove the view without returning an error. <br>- When the `IF EXISTS` keyword is not used, the system removes the view only if the target view has already existed. Otherwise, the system fails to remove the view and returns an error. |
| `view_name_list` | A comma-separated list of view names. You can use the `SELECT * FROM information_schema.tables WHERE table_type = 'VIEW'` statement to get existing view names. |
| `CASCADE` | Optional. Remove the target view and its dependent objects. The `CASCADE` keyword does not list objects it removes, so it should be used cautiously. |
| `RESTRICT` | (Default) Optional. Do not remove the view if any objects depend on it. |

### Examples

This example removes the `names` view.

```sql
-- 1. Check all views. 

SELECT * FROM information_schema.tables WHERE table_type = 'VIEW';
  table_catalog | table_schema | table_name  | table_type | is_insertable_into | version | namespace_oid
----------------+--------------+-------------+------------+--------------------+---------+----------------
  db2           | public       | names       | VIEW       | NO                 |       3 |    1497612465
  db2           | public       | short_order | VIEW       | NO                 |       1 |    1497612465
(2 rows)

-- 2. Remove the names view.

DROP VIEW names;
DROP VIEW

-- 3. Check all views. 

SELECT * FROM information_schema.tables WHERE table_type = 'VIEW';
  table_catalog | table_schema | table_name  | table_type | is_insertable_into | version | namespace_oid
----------------+--------------+-------------+------------+--------------------+---------+----------------
  db2           | public       | short_order | VIEW       | NO                 |       1 |    1497612465
(1 row)
```
