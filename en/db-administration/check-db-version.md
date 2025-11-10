---
title: View Database Version
id: check-db-version
---


# View Database Version

After connecting to KWDB, you can view the database version using the `SELECT version()` statement.

```sql
SELECT version();
```

If you succeed, you should see an output similar to the following:

```sql
                                            version
------------------------------------------------------------------------------------------------
  KWDB 2.0.4 (x86_64-linux-gnu, built 2024/08/06 08:20:18, go1.19, gcc 11.4.0)
(1 row)
```
