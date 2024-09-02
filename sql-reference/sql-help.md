---
title: 查看 SQL 语句
id: sql-help
---

# 查看 SQL 语句

## 查看所有 SQL 语句

用户可以在任何 KWDB 客户端使用 `\h` 命令查看 KWDB 支持的所有 SQL 语句及相关描述。

```sql
\h；
```

执行成功后，控制台输出以下信息：

```sql
Configuration:
  DISCARD               reset the session to its initial state
  RESET                 reset a session variable to its default value
  RESET CLUSTER SETTING reset a cluster setting to its default value
  SET CLUSTER SETTING   change a cluster setting
  SET SESSION           change a session variable
  SHOW CLUSTER SETTING  display cluster settings
  SHOW SAVEPOINT        display current savepoint properties
  SHOW SESSION          display session variables
  SHOW TRANSACTION      display current transaction properties
  USE                   set the current database

Data Manipulation:
  <SELECTCLAUSE> access tabular data
  <SOURCE>       define a data source for SELECT
  DELETE         delete rows from a table
  EXPORT      export data to file in a distributed manner
  IMPORT      load data from file in a distributed manner
  INSERT         create new rows in a table
  SELECT         retrieve rows from a data source and compute a result
  TABLE          select an entire table
  TRUNCATE       empty one or more tables
  UPDATE         update rows of a table
  UPSERT         create or replace rows in a table
  VALUES         select a given set of values

Experimental:
  SHOW HISTOGRAM  display histogram (experimental)
  SHOW STATISTICS display table statistics (experimental)

Miscellaneous:
  CANCEL JOBS        cancel background jobs
  CANCEL QUERIES     cancel running queries
  CANCEL SESSIONS    cancel open sessions
  CREATE STATISTICS  create a new table statistic
  DEALLOCATE         remove a prepared statement
  EXECUTE            execute a statement prepared previously
  EXPLAIN            show the logical plan of a query
  PAUSE JOBS         pause background jobs
  PAUSE SCHEDULE     pause specified scheduled job
  PREPARE            prepare a statement for later execution
  RESUME JOBS        resume background jobs
  RESUME SCHEDULE    resume background scheduled job
  SHOW APPLICATIONS  list open client applications
  SHOW JOBS          list background jobs
  SHOW QUERIES       list running queries
  SHOW RANGE         show range information for a row
  SHOW RANGES        list ranges
  SHOW SESSIONS      list open client sessions
  SHOW SYNTAX        analyze SQL syntax
  SHOW TRACE         display an execution trace

Privileges And Security:
  ALTER ROLE  alter a role
  CREATE ROLE define a new role
  DROP ROLE   remove a user
  GRANT       define access privileges and role memberships
  REVOKE      remove access privileges and role memberships
  SHOW GRANTS list grants
  SHOW ROLES  list defined roles
  SHOW USERS  list defined users

Schema Manipulation:
  ALTER AUDIT        change the definition of an audit
  ALTER DATABASE     change the definition of a database
  ALTER INDEX        change the definition of an index
  ALTER RANGE        change the parameters of a range
  ALTER SCHEDULE     change the definition of a schedule
  ALTER SEQUENCE     change the definition of a sequence
  ALTER TABLE        change the definition of a table
  ALTER VIEW         change the definition of a view
  CREATE AUDIT       create an audit
  CREATE DATABASE    create a new database
  CREATE FUNCTION    create a new function
  CREATE INDEX       create a new index
  CREATE SCHEMA      create a new schema
  CREATE SEQUENCE    create a new sequence
  CREATE TABLE       create a new table
  CREATE TS DATABASE create a new timeseries database
  CREATE VIEW        create a new view
  DROP AUDIT         remove an audit
  DROP DATABASE      remove a database
  DROP FUNCTION      remove a function
  DROP INDEX         remove an index
  DROP SCHEMA        remove a schema
  DROP SEQUENCE      remove a sequence
  DROP TABLE         remove a table
  DROP VIEW          remove a view
  SHOW ATTRIBUTES    list the attributes of the timeseries table
  SHOW AUDITS        list audit policies
  SHOW COLUMNS       list columns in relation
  SHOW CONSTRAINTS   list constraints
  SHOW CREATE        display the CREATE statement for a table, sequence or view
  SHOW DATABASES     list databases
  SHOW FUNCTION      Show the details of the function
  SHOW FUNCTIONS     list functions
  SHOW INDEXES       list indexes
  SHOW RETENTIONS    list retentions of the timeseries table
  SHOW SCHEDULE      show schedule details
  SHOW SCHEDULES     list schedules
  SHOW SCHEMAS       list schemas
  SHOW SEQUENCES     list sequences
  SHOW TABLES        list tables

Transaction Control:
  BEGIN           start a transaction
  COMMIT          commit the current transaction
  RELEASE         complete a sub-transaction
  ROLLBACK        abort the current (sub-)transaction
  SAVEPOINT       start a sub-transaction
  SET TRANSACTION configure the transaction settings
```

如果系统无法找到匹配的字符串，控制台输出以下信息：

```shell
no help available for "<sql statement>".
Try \h with no argument to see available help.
```

## 使用关键字查看 SQL 语句

用户也可以使用关键字查看某一类的 SQL 语句。

以下示例使用 `SHOW` 关键字查看 KWDB 支持的所有 `SHOW` 语句。

```sql
\h SHOW;
```

执行成功后，控制台输出以下信息：

```sql
Command:     SHOW
Syntax:
SHOW APPLICATIONS, SHOW BACKUP, SHOW CLUSTER SETTING, SHOW COLUMNS,
SHOW CONSTRAINTS, SHOW CREATE, SHOW DATABASES, SHOW HISTOGRAM, SHOW INDEXES,
SHOW PARTITIONS, SHOW JOBS, SHOW QUERIES, SHOW RANGE, SHOW RANGES,
SHOW ROLES, SHOW SCHEMAS, SHOW SEQUENCES, SHOW SESSION, SHOW SESSIONS,
SHOW STATISTICS, SHOW SYNTAX, SHOW TABLES, SHOW TRACE SHOW TRANSACTION, SHOW USERS
```

## 查看特定 SQL 语句的帮助信息

用户可以在指定 SQL 语句前使用 `\h` 命令，查看对应 SQL 语句的帮助信息。系统返回特定 SQL 语句的具体帮助信息，包括：`Command`、`Description`、`Category`、`Syntax`、`See also` 等。

- `Command`：SQL 语句
- `Description`：SQL 语句的描述信息
- `Category`：SQL 语句所属类别
- `Syntax`：SQL 语句的句法结构
- `See Also`：与指定 SQL 语句相关的其他 SQL 语句

以下示例查看 `CREATE AUDIT` 语句的帮助信息。

```sql
\h CREATE AUDIT;
```

执行成功后，控制台输出以下信息：

```sql
Description: create a AUDIT
Category:    schema manipulation
Syntax:
--Object Audit
 CREATE AUDIT <audit_name> ON <TargetType> target_name
              FOR [ Oprations, ...] TO [username]
                         [ WITH <option> [= <value>] [, ...] ]
              [ ACTION ...]
              [ LEVEL ]
 --Stmt Audit
 CREATE AUDIT <audit_name> ON <TargetType>
              FOR [ Oprations, ...] TO [username]
                         [ WITH <option> [= <value>] [, ...] ]
              [ ACTION ...]
              [ LEVEL ]
 --Stmt TargetType:
     DATABASE, SCHEMA, TABLE, INDEX, VIEW, SEQUENCE,
     PROCEDURE, FUNCTION, TRIGGER, CDC, JOB, USER,
     ROLE, PRIVILEGE, QUERY, TRANSACTION, SAVEPOINT,
     RANGE, STATISTICS, SESSION, SCHEDULE, AUDIT
 --Object TargetType:
     TABLE, VIEW, COLUMN, FUNCTION

See also:
  ALTER AUDIT
  DROP AUDIT
  SHOW AUDITS
```
