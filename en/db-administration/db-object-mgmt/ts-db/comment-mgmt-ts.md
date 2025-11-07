---
title: Comments
id: comment-mgmt-ts
---

# Comments

## COMMENT ON

The `COMMENT ON` statement associates comments to databases, tables, or columns.

### Privileges

The user must be a member of the `admin` role or have the `CREATE` privilege on the object they are commenting on. By default, the `root` user belongs to the `admin` role.

### Syntax

```sql
COMMENT ON [DATABASE <database_name> | TABLE <table_name> | COLUMN <column_name> ] IS <comment_text>;
```

### Parameters

| Parameter       | Description                                 |
|-----------------|---------------------------------------------|
| `database_name` | The name of the database to comment on.     |
| `table_name`    | The name of the table to comment on.        |
| `column_name`   | The name of the column to comment on.       |
| `comment_text`  | The comment to be associated to the object. |

### Examples

- Add a comment to a database.

    ```sql
    -- 1. Add a comment to the ts_db database.

    COMMENT ON DATABASE ts_db IS 'database for power statistics';
    COMMENT ON DATABASE

    -- 2. Check the database's comments.

    SHOW DATABASES WITH COMMENT;
      database_name | engine_type |            comment
    ----------------+-------------+--------------------------------
      db1           | RELATIONAL  | NULL
      db2           | RELATIONAL  | NULL
      ts_db         | RELATIONAL  | database for power statistics
    ...
    (6 rows)
    ```

- Add a comment to a table.

    ```sql
    -- 1. Add a comment to the power table.

    COMMENT ON TABLE power IS 'power for all devices';
    COMMENT ON TABLE

    -- 2. Check the table's comments.

    SHOW TABLES WITH COMMENT;
      table_name  |    table_type     |      comment
    --------------+-------------------+--------------------
      power       | TIME SERIES TABLE | power for all devices
    (1 row)
    ```

- Add a comment to a column.

    ```sql
    -- 1. Add a comment to the ts column of the power table.

    COMMENT ON COLUMN power.ts IS 'auto-generated';
    COMMENT ON COLUMN

    -- 2. Check the column's comments.

    SHOW COLUMNS FROM power WITH COMMENT;
      column_name |  data_type  | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag |              comment
    --------------+-------------+-------------+----------------+-----------------------+-----------+-----------+--------+-------------------------------------
      ts          | TIMESTAMPTZ |    false    | NULL           |                       | {primary} |   false   | false  | auto-generated
      col         | INT4        |    true     | NULL           |                       | {}        |   false   | false  | NULL
      tag1        | INT4        |    false    | NULL           |                       | {}        |   false   |  true  | primary tag for comment
      tag2        | INT4        |    true     | NULL           |                       | {}        |   false   |  true  | tag for comment
    (4 rows)
    ```
