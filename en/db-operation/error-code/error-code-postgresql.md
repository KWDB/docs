---
title: PostgreSQL Error Codes
id: error-code-postgresql
---

# PostgreSQL Error Codes

KWDB uses several PostgreSQL error codes (PGcodes), along with some KWDB-specific error codes that are compatible with PGcode.

This section provides a list of PGcodes used in KWDB, along with recommended actions.

::: warning Note

Some PGcodes may correspond to multiple messages. While these messages may vary slightly, the underlying cause of the error remains consistent. The table below includes only the messages associated with the original PGcode error and does not cover KWDB’s custom messages. Use the error code to identify the cause and take the appropriate action.

:::


| Error Code | Message                                           | Suggested Action                                      |
| ---------- | ------------------------------------------------- | ----------------------------------------------------- |
| 08P01      | ProtocolViolation                                  | Contact support                                      |
| 0A000      | FeatureNotSupported                                | No action available                                  |
| 0LP01      | InvalidGrantOperation                              | Retry after modifying the SQL statement              |
| 1000       | Warning                                            | No action available                                   |
| 21000      | CardinalityViolation                               | Contact support                          |
| 22000      | DeleteFailure                                      | Restart the service and check table data, or review logs |
| 22001      | StringDataRightTruncation                          | Retry after modifying the SQL statement               |
| 22003      | NumericValueOutOfRange                             | Retry after modifying the SQL statement               |
| 22004      | NullValueNotAllowed                                | Retry after modifying the SQL statement               |
| 22005      | InvalidEscapeSequence                              | Retry after modifying the SQL statement               |
| 22007      | InvalidDatetimeFormat                              | Retry after modifying the SQL statement               |
| 22008      | DatetimeFieldOverflow                              | Contact support                          |
| 22012      | DivisionByZero                                     | Retry after modifying the SQL statement               |
| 22013      | InvalidWindowFrameOffset                           | Retry after modifying the SQL statement               |
| 2201E      | InvalidArgumentForLogarithm                        | Retry after modifying the SQL statement               |
| 22021      | CharacterNotInRepertoire                           | Check if the input characters comply with UTF8 standards |
| 22023      | InvalidParameterValue                              | Retry after modifying the SQL statement               |
| 22026      | StringDataLengthMismatch                           | Retry after modifying the SQL statement               |
| 2202E      | ArraySubscript                                     | Retry after modifying the array subscript           |
| 22C01      | ScalarOperationCannotRunWithoutFullSessionContext  | Retry after modifying the SQL statement               |
| 22P02      | InvalidTextRepresentation                          | Retry after modifying the SQL statement               |
| 22P03      | InvalidBinaryRepresentation                        | Retry after modifying the SQL statement               |
| 22P05      | UntranslatableCharacter                            | Retry after modifying the SQL statement               |
| 23502      | NotNullViolation                                   | Retry after modifying the SQL statement               |
| 23503      | ForeignKeyViolation                                | Retry after modifying the SQL statement               |
| 23505      | UniqueViolation                                    | Retry after modifying the SQL statement               |
| 23514      | CheckViolation                                     | Retry after modifying the SQL statement               |
| 25000      | InvalidTransactionState                            | Retry after committing or rolling back the current transaction |
| 25001      | ActiveSQLTransaction                               | Do not use the `DISCARD` command in the middle of a transaction |
| 25006      | ReadOnlySQLTransaction                             | Retry after starting a read-write transaction         |
| 25P02      | InFailedSQLTransaction                             | End the current transaction and retry with a new one   |
| 25P03      | NullTransaction                                    | Retry after modifying the SQL statement               |
| 26000      | InvalidSQLStatementName                            | Retry after modifying the SQL statement               |
| 28P01      | InvalidPassword                                    | Retry after modifying the SQL statement               |
| 2BP01      | DependentObjectsStillExist                         | Resolve dependency issues before retrying             |
| 34000      | InvalidCursorName                                  | Retry after modifying the SQL statement               |
| 3B001      | InvalidSavepointSpecification                      | Retry after modifying the SQL statement               |
| 3D000      | InvalidCatalogName                                 | Retry after modifying the SQL statement               |
| 3D000      | UndefinedDatabase                                  | Retry after modifying the SQL statement               |
| 3F000      | InvalidSchemaName                                  | Retry after modifying the SQL statement               |
| 42501      | InsufficientPrivilege                              | Retry after requesting privileges from the administrator |
| 42601      | Syntax                                             | Retry after modifying the SQL statement               |
| 42602      | InvalidName                                        | Retry after modifying the SQL statement               |
| 42611      | InvalidColumnDefinition                            | Retry after modifying the SQL statement               |
| 42622      | NameTooLong                                        | Retry after modifying the SQL statement               |
| 42701      | DuplicateColumn                                    | Retry after modifying the SQL statement               |
| 42702      | AmbiguousColumn                                    | Retry after modifying the SQL statement               |
| 42703      | UndefinedColumn                                    | Retry after modifying the SQL statement               |
| 42704      | UndefinedObject                                    | Retry after modifying the SQL statement               |
| 42710      | DuplicateObject                                    | Retry after modifying the SQL statement               |
| 42711      | DuplicateParameter                                 | Retry after modifying the SQL statement               |
| 42723      | DuplicateFunction                                  | Retry after modifying the SQL statement               |
| 42725      | AmbiguousFunction                                  | Retry after modifying the SQL statement               |
| 42803      | Grouping                                           | Retry after modifying the SQL statement               |
| 42804      | DatatypeMismatch                                   | Retry after modifying the SQL statement               |
| 42809      | WrongObjectType                                    | Retry after modifying the SQL statement               |
| 42830      | InvalidForeignKey                                  | Retry after modifying the SQL statement               |
| 42846      | CannotCoerce                                       | Retry after modifying the SQL statement               |
| 42883      | UndefinedFunction                                  | Retry after modifying the SQL statement               |
| 42939      | ReservedName                                       | Retry after modifying the SQL statement               |
| 42C02      | SyncObjectFailed                                   | Contact support                          |
| 42C03      | WrongExpr                                          | Retry after modifying the SQL statement               |
| 42C04      | NumberMismatch                                     | Retry after modifying the SQL statement               |
| 42P01      | UndefinedTable                                     | Retry after modifying the SQL statement               |
| 42P02      | UndefinedParameter                                 | Retry after modifying the SQL statement               |
| 42P04      | DuplicateDatabase                                  | Retry after modifying the SQL statement               |
| 42P06      | DuplicateSchema                                    | Retry after modifying the SQL statement               |
| 42P07      | DuplicateRelation                                  | Retry after modifying the SQL statement               |
| 42P08      | AmbiguousParameter                                 | Retry after modifying the SQL statement               |
| 42P09      | AmbiguousAlias                                     | Use a clear alias in the query                         |
| 42P10      | InvalidColumnReference                             | Retry after modifying the SQL statement               |
| 42P15      | InvalidSchemaDefinition                            | Retry after modifying the SQL statement               |
| 42P16      | InvalidTableDefinition                             | Retry after modifying the SQL statement               |
| 42P17      | InvalidObjectDefinition                            | Retry after modifying the SQL statement               |
| 42P18      | IndeterminateDatatype                              | Retry after modifying the SQL statement               |
| 42P20      | Windowing                                          | Retry after modifying the SQL statement               |
| 53200      | OutOfMemory                                        | Contact support                          |
| 54000      | ProgramLimitExceeded                               | Retry after modifying the SQL statement               |
| 54011      | TooManyColumns                                     | Retry after modifying the SQL statement               |
| 54021      | TooWideRowWidth                                    | Retry after modifying the SQL statement               |
| 54022      | InsertColumnMismatch                               | Retry after modifying the SQL statement               |
| 54024      | TooWideTagWidth                                    | Retry after modifying the SQL statement               |
| 55000      | ObjectNotInPrerequisiteState                       | Resolve dependency issues before retrying             |
| 55006      | ObjectInUse                                        | Retry after terminating the operation that is occupying the object |
| 55P02      | CantChangeRuntimeParam                             | Retry after taking the database offline             |
| 57P03      | CannotConnectNow                                   | Retry after the database is available for connection  |
| 58C00      | RangeUnavailable                                   | Contact support                          |
| 58C01      | InternalConnectionFailure                          | Contact support                          |
| 59000      | replication_error                                  | Check primary-secondary replication status |
| 59001      | replication_primary_error                          | Check primary node status and logs |
| 59002      | replication_secondary_error                        | Check secondary node status and logs |
| XX000      | Internal                                           | Contact support                          |
| XXC01      | CCLRequired                                        | Contact support                          |
