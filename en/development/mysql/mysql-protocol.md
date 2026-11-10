---
title: MySQL Native Protocol Support
id: mysql-protocol
---

# KWDB MySQL Native Protocol Support

Starting from KWDB V3.3.0, KWDB provides MySQL native wire protocol support on an independent port. This enables MySQL-ecosystem drivers, applications, and tools to connect to KWDB directly without changing drivers, execute SQL, and read data from both relational and time-series tables.

## Overview

Previously, KWDB only provided PostgreSQL wire protocol. MySQL-ecosystem applications, drivers (such as Connector/J, mysql-connector-python, go-sql-driver/mysql), and client tools (such as DBeaver, mysql CLI) could not connect directly. Users needed to switch to PostgreSQL drivers and modify their application code.

MySQL and PostgreSQL protocols have fundamental differences in connection establishment behavior (MySQL starts with a server-sent packet, while PostgreSQL starts with a client-sent packet). There is no first-byte-based multiplexing that could handle both protocols on the same port. Therefore, the MySQL protocol listener must bind to an independent port, completely separate from the existing PostgreSQL port.

::: warning Note
MySQL protocol support is disabled by default. You must explicitly configure a listen address to enable it. Deployments without this configuration behave identically to previous versions and do not affect existing PostgreSQL connections.
:::

## Enabling MySQL Protocol

Add the `--mysql-addr` parameter when starting the KWDB server process to specify the listen address and port for the MySQL protocol.

```shell
kwbase start --mysql-addr=0.0.0.0:3306
```

::: warning Note
`--mysql-addr` accepts only an independent listen address and cannot share a port with the PostgreSQL protocol. The default PostgreSQL protocol listen port is 26257. We recommend using port 3306 or another unused port for the MySQL protocol.
:::

## Supported Authentication Methods

KWDB MySQL protocol supports the following three password authentication plugins. Each plugin supports both TLS/SSL encrypted transport and RSA public key exchange for encrypting credentials:

| Authentication Plugin | Description | Support Status |
| --- | --- | --- |
| `caching_sha2_password` | Default authentication plugin since MySQL 8.0 | Supported |
| `mysql_native_password` | Default authentication plugin in MySQL 5.7 and earlier | Supported |
| `sha256_password` | SHA-256 hash authentication plugin | Supported |

The transport encryption coverage for each plugin is as follows:

| Authentication Plugin | TLS/SSL Encrypted Transport | RSA Public Key Exchange | No-Encryption Fast Path |
| --- | --- | --- | --- |
| `caching_sha2_password` | Supported | Supported | Supported (when credential cache hits) |
| `mysql_native_password` | Supported | N/A | Supported |
| `sha256_password` | Supported | Supported | Not supported |

The server also reports the `CLIENT_SSL` capability bit so that clients can choose whether to upgrade to TLS encrypted connections based on their configuration.

## Supported Protocol Features

### Connection and Handshake

- The server listens for MySQL protocol handshake requests on an independent port and replies with a handshake initialization packet.
- Supports capability flags negotiation, including protocol version, authentication plugins, and prepared statement support.
- Connection IDs come from an independent handshake counter to ensure each connection receives a unique identifier (previously the PostgreSQL protocol reported connection IDs based on the live connection count, which could produce duplicate IDs for serially established connections).
- Reports the `NO_BACKSLASH_ESCAPES` status bit to match KWDB's `standard_conforming_strings = on` behavior, preventing clients from applying MySQL default backslash escape rules that would corrupt literal strings.

### Text Protocol

KWDB MySQL protocol supports the following core commands:

| Command | Description | Support Status |
| --- | --- | --- |
| `COM_QUERY` | Execute SQL queries or statements | Supported |
| `COM_INIT_DB` | Switch current database | Supported |
| `COM_PING` | Heartbeat probe | Supported |
| `COM_RESET_CONNECTION` | Reset connection session | Supported |
| `COM_QUIT` | Disconnect | Supported |
| `COM_CHANGE_USER` | Switch user | Not supported |

### Binary Protocol and Prepared Statements

- Supports `COM_STMT_PREPARE`, `COM_STMT_EXECUTE`, `COM_STMT_CLOSE`, `COM_STMT_RESET`, `COM_STMT_SEND_LONG_DATA`, and other binary protocol commands.
- `?` placeholders in prepared statements are rewritten to `$N` form used by KWDB's internal SQL engine before execution. The result encoding layer outputs column definitions and row data according to the MySQL binary protocol.
- Text protocol and binary protocol share the same SQL execution engine and transaction/session state.

### Result Sets and Error Codes

- PostgreSQL SQLSTATE is mapped to MySQL error codes (for example, incorrect password returns SQLSTATE `28000` / MySQL error code `1045`).
- Supports multi-result-set framing (multiple statements separated by semicolons in a single submission).
- Zero-column result sets are correctly encoded per the MySQL protocol.

### MySQL Dialect Compatibility

After the handshake completes, drivers immediately send several MySQL-specific initialization statements. Failure of any one of them would prevent the connection from being established, rather than gracefully degrading functionality. KWDB includes a statement rewriting layer inside the MySQL protocol handler that transparently processes common driver initialization statements:

| MySQL Statement/Function | Rewritten to KWDB Equivalent |
| --- | --- |
| `@@x` (system variable read) | `current_setting('x', true)`, with synthetic `AS "@@x"` to preserve column labels |
| `USER()` | `current_user()` |
| `CONNECTION_ID()` | Inline this connection's handshake ID |
| `SET character_set_results = NULL` | Accepted as a no-op |
| `SET SESSION TRANSACTION ...` | Mapped to session default isolation level / read-only attribute |

For some variables, a lookup table is used instead of copying KWDB's actual values, because KWDB values would be silently misread by the client:

- `transaction_isolation`: KWDB's spelling does not match the mapping table in MySQL Connector/J, so a MySQL-compatible isolation level name is returned.
- `autocommit`: KWDB's `on` value would be parsed as `false` by `Boolean.parseBoolean`, so `1` / `0` is returned instead.
- `transaction_read_only`: KWDB's `off` value would cause `Integer.parseInt` to throw an exception, so `0` / `1` is returned instead.

::: warning Note
Statement rewriting happens inside the MySQL protocol layer and does not modify KWDB's SQL grammar definition. Therefore:

- PostgreSQL clients are unaffected by these rewrite behaviors.
- `@@` inside string literals, comments, or backticks cannot be misidentified due to the prefix-based matching algorithm.
- If any token in a statement cannot be recognized, the entire statement is passed through to the SQL engine without modification.
:::

## Basic Operations Support

### DDL, DML, and Queries

Clients connecting through the MySQL protocol can perform the following operations normally:

- Create, delete, and modify relational and time-series databases
- Create, delete, and modify relational and time-series tables
- Insert, update, and delete data
- Query data (including aggregation, grouping, ordering, time-series windows, etc.)
- Execute transactions (BEGIN / COMMIT / ROLLBACK)
- Manage database objects using MySQL client tools (such as the mysql CLI)

::: warning Note
KWDB's DDL syntax differs from MySQL's native syntax. For example, time-series tables use `CREATE TABLE ... TAGS (...)` syntax. When connecting to KWDB with MySQL clients, SQL statements must follow KWDB's syntax, not MySQL's native syntax.
:::

### Driver Compatibility Testing

The following clients and drivers have been validated:

| Client/Driver | Version | Test Result |
| --- | --- | --- |
| mysql CLI | 8.0.46 | Passed |
| libmysqlclient | - | Passed |
| go-sql-driver/mysql | - | Passed |
| MySQL Connector/J | 8.4.0 | Passed |

Connector/J testing covers `caching_sha2_password + RSA public key exchange`, `mysql_native_password`, and `TLS encryption` authentication configurations.

## Known Limitations and Differences

### Functional Limitations

| Item | Description |
| --- | --- |
| Timestamp output precision | Outputs only to microsecond precision (some drivers cannot parse nanoseconds) |
| Time-series table INSERT path | Does not use the `insert_direct` fast path on MySQL protocol connections, resulting in slightly lower write performance |
| `COM_CHANGE_USER` | MySQL protocol's user-switching command is not supported |
| `SET SESSION TRANSACTION` semantics | Rewritten as session default values, takes effect from the next transaction and does not modify an already-started transaction |

### Differences from PostgreSQL Protocol

MySQL protocol result output format has the following inherent differences from KWDB's PostgreSQL protocol:

| Item | MySQL Protocol | PostgreSQL Protocol |
| --- | --- | --- |
| Boolean text format | `1` / `0` | `t` / `f` |
| TIMETZ output format | MySQL-compatible format | PostgreSQL native format |
| Array/tuple/interval output format | MySQL-compatible format | PostgreSQL native format |

These differences do not affect data correctness, only the textual representation of result sets.

### Connection Behavior

The `transaction_read_only` and `transaction_isolation` session variables on MySQL protocol connections are simulated through the rewriting layer. The actual isolation level and read-only attributes are applied in the KWDB kernel according to PostgreSQL semantics.

## Compatibility and Safeguards

The MySQL protocol support incorporates the following safeguards to ensure existing deployments are not affected:

- **Disabled by default**: The `mysql-addr` configuration option defaults to an empty string. The server creates a MySQL listener only when it is non-empty; when not configured, `s.mysqlServer` is `nil` and no port is bound.
- **Independent port**: The MySQL protocol uses a separate TCP listen port, completely isolated from the PostgreSQL protocol port.
- **No SQL grammar modification**: MySQL dialect compatibility is handled inside the protocol layer, without changing KWDB's SQL grammar definition (`sql.y`). PostgreSQL clients will not accidentally accept MySQL syntax.
- **Backward-compatible credentials**: The new MySQL authentication columns in the `system.users` table are completely transparent to existing PostgreSQL connections. Existing clusters automatically receive these columns via `sqlmigrations`.

## Self-Test Results

| Test Item | Result |
| --- | --- |
| `make kwbase-test` (lint + all Go unit tests) | 221 packages ok / 0 FAIL |
| `qa/run_test_local_v2.sh TEST_v2_integration_basic_v2.sh` | Single-node 375 / 375 passed; 5-node / 5cr cluster 1108 / 1110 passed (2 flaky cases passed in isolation) |
| `qa/run_mysql_protocol_test.sh` | Single-node 60 / 0; 5c and 5cr each 65 / 0 |
| `qa/run_mysql_protocol_test.sh jdbc` | Single-node 21 / 0; 5c and 5cr each 28 / 0 |
| MySQL protocol runs PG's basic_v3 (225 files) | 97.5% consistent with PG output (single-node) / 97.3% (5c/5cr) |
| MySQL protocol runs PG's logictest (207 files) | Approximately 94% consistent with PG output |

The lower-consistency portions (approximately 2.5% ~ 6%) have been verified case by case. The differences are attributable to inherent format differences between MySQL and PostgreSQL (such as boolean text format, TIMETZ format) or test tool limitations, and do not affect data correctness.
