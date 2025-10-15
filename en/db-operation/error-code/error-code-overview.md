---
title: Overview
id: error-code-overview
---

# Error Code Overview

When you connect to KWDB using the JDBC connector or execute SQL queries, KWDB returns error codes when something goes wrong. This section lists three types of error codes provided by KWDB, each consisting of five characters:

- **[KWDB Specific Error Codes](./error-code-kaiwudb.md)**: These error codes are related to issues within KWDB itself, including database handling, storage, and query operations. They start with `KW`.
- **[PostgreSQL Error Codes](./error-code-postgresql.md)**: These error codes are part of KWDB’s PostgreSQL compatibility, identifying issues related to PostgreSQL-compatible operations.
- **[KaiwuDB JDBC Driver Error Codes](./error-code-jdbc-driver.md)**: These codes are related to issues that arise while using the KaiwuDB JDBC Driver to interact with the database.
- **[KWDB Time-series Function Error Codes](./error-code-ts-functions.md)**: These error codes are related to issues with KWDB time-series functions.
- **[Trigger Error Codes](./error-code-trigger.md)**: These error codes are related to issues with triggers.

Each error code provides the following details:

- **Error Code**: A unique identifier for the error, typically following a logical pattern. Error codes within the same category are grouped within a defined range. For example, connection-related error codes fall within the range `KW001` to `KW015`.  
- **Error Message**: A description of the error, explaining its cause and offering possible solutions.
