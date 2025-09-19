---
title: Identifiers
id: sql-identifiers
---

# Identifiers

Identifiers are names for objects and entities in the databases. In SQL grammar, the naming rules for an identifier include:

- Begin with a Unicode letter or an underscore (`_`). Subsequent characters can be letters, underscore (`_`), or digits (0-9).
- Must be not identical to any SQL keyword unless the keyword is accepted by the element's syntax. For example, `name` accepts unreserved keywords or column name keywords.

To bypass either of these rules, simply surround the identifier with double quotes (`" "`). You can also use double quotes to preserve case-sensitivity in database, table, view, and column names.

## Use Idenfifiers as Qualifiers

KWDB supports names composed of one or more identifiers, separated by the period character (`.`). The initial part of a composite name serves as a qualifier, influencing the interpretation of subsequent identifiers within the context.

You can reference columns using any of the methods listed in the table below:

| Column Reference                       | Description                                                                                       |
|----------------------------------------|---------------------------------------------------------------------------------------------------|
| `column_name`                          | Reference the `column_name` column in any table.                                                  |
| `table_name.column_name`               | Reference the `column_name` column in the `table_name` table within the current database.         |
| `database_name.table_name.column_name` | Reference the `column_name` column in the `table_name` table within the `database_name` database. |
| `column_name`                          | Reference any keywords or fileds with special characters.                                          |

When referencing composite identifiers, each individual identifier component must be quoted separately rather than treating the entire composite identifier as a single entity. For example, `"table"."column"` is a valid reference format, whereas `"table.column"` is invalid.

In most column reference statements, you do not need to explicitly specify table names or database names unless there is ambiguity in the target field. For example, if both `t1` and `t2` tables contain a column `c`, a `SELECT` statement retrieving column `c` from both `t1` and `t2` tables requires disambiguation by explicitly specifying `t1.c` or `t2.c`. Similarly, if two databases contain tables with identical names, you must use formats like `db1.table_name.col_name` and `db2.table_name.col_name` to precisely identify the target column.
