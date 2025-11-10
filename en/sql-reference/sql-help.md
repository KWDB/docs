---
title: View SQL Statements
id: sql-help
---

# View SQL Statements

## View All SQL Statements

You can run the `\h` command through any KWDB CLI client to list all supported SQL statements and their descriptions.

```sql
\h;
```

If you succeed, you should see an output similar to the following:

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

If the system fails to find any matched string, you should see an output similar to the following:

```shell
no help available for "<sql statement>".
Try \h with no argument to see available help.
```

## View SQL Statements Using Keyword

You can run the `\h <keyword>` command to view a group of SQL statements with the same keyword.

This example lists all supported `SHOW` statements by using the `SHOW` keyword.

```sql
\h SHOW;
```

If you succeed, you should see an output similar to the following:

```sql
Command:     SHOW
Syntax:
SHOW APPLICATIONS, SHOW BACKUP, SHOW CLUSTER SETTING, SHOW COLUMNS,
SHOW CONSTRAINTS, SHOW CREATE, SHOW CREATE DATABASE, SHOW DATABASES, SHOW HISTOGRAM, SHOW INDEXES,
SHOW PARTITIONS, SHOW JOBS, SHOW QUERIES, SHOW RANGE, SHOW RANGES,
SHOW ROLES, SHOW SCHEMAS, SHOW SEQUENCES, SHOW SESSION, SHOW SESSIONS,
SHOW STATISTICS, SHOW SYNTAX, SHOW TABLES, SHOW TRACE SHOW TRANSACTION, SHOW USERS
```

## View Help Information about Specified SQL Statements

You can run the `\h <sql_statement>` command to view the help information about a specified SQL statement, including the following parts:

- `Command`: the specified SQL statement
- `Description`: the descriptions of the SQL statement
- `Category`: the category to which the SQL statement belongs
- `Syntax`: the syntax of the SQL statement
- `See Also`: other SQL statements related to the specified SQL statement

This example lists help information about the `CREATE AUDIT` statement.

```sql
\h CREATE AUDIT;
```

If you succeed, you should see an output similar to the following:

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
