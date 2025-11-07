---
title: Delimiters
id: delimiter-sql
---

# Delimiters

The `DELIMITER` statement redefines the statement delimiter of the current session. By default, KWDB recognizes the semicolon (`;`) as a statement delimiter. However, sometimes the compound SQL statements may containing semicolon characters. In these cases, you need to redefine the delimiter to avoid interpretation conflicts when executing the statements.

## Privileges

N/A

## Syntax

![](../../../static/sql-reference/delimiter.png)

## Parameters

| Parameter | Description |
| --- | --- |
| `new_delimiter` | The new delimiter. Currently, KWDB only supports using the double backslash (`\\`) and semicolon (`;`) as the statement delimiter. |

## Examples

```sql
-- Use the double backslash as the statement delimiter.
DELIMITER \\
CREATE TABLE t(a init)\\

-- Use the semicolon as the statement delimiter.
DELIMITER ;
CREATE TABLE t1(a init);
```
