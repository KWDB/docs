---
title: KaiwuDB JDBC Driver 错误码
id: error-code-jdbc-driver
---

# KaiwuDB JDBC Driver 错误码

本文介绍与 KaiwuDB JDBC 驱动相关的错误码。

| 错误码 | 消息 | 错误原因 |
| --- | --- | ---|
| 0100E   | TOO_MANY_RESULTS |结果太多                                      |
| 02000   | NO_DATA                              | 没有数据                                               |
| 07006   | INVALID_PARAMETER_TYPE                               | 无效参数类型                            |
| 08001   | CONNECTION_UNABLE_TO_CONNECT                              | 客户端不能建立 SQL 连接           |
| 08003   | CONNECTION_DOES_NOT_EXIST                              | 连接不存在                           |
| 08004   | CONNECTION_REJECTED                              | 服务器拒绝建立 SQL 连接                    |
| 08006   | CONNECTION_FAILURE                             | 连接失败                                    |
| 08007   | CONNECTION_FAILURE_DURING_TRANSACTION                              | 事务期间连接失败         |
| 08P01   | PROTOCOL_VIOLATION                             | 违反协议                                    |
| 08S01   | COMMUNICATION_ERROR                               | 通信错误                                   |
| 0A000   | NOT_IMPLEMENTED                               | 不支持此特性                                   |
| 22000   | DATA_ERROR                              | 数据错误                                            |
| 22001   | STRING_DATA_RIGHT_TRUNCATION                              | 字串数据右边被截断                |
| 22003   | NUMERIC_VALUE_OUT_OF_RANGE                               | 数字值超出范围                      |
| 22007   | BAD_DATETIME_FORMAT                              | 非法日期时间格式                           |
| 22008   | DATETIME_OVERFLOW                              | 日期时间字段溢出                             |
| 2200G   | MOST_SPECIFIC_TYPE_DOES_NOT_MATCH                              | 相关类型不匹配           |
| 22012   | DIVISION_BY_ZERO                              | 被零除                                        |
| 22023   | INVALID_PARAMETER_VALUE                               | 非法参数值                             |
| 24000   | INVALID_CURSOR_STATE                              | 非法游标状态                              |
| 25000   | TRANSACTION_STATE_INVALID                             | 非法事务状态                         |
| 25001   | ACTIVE_SQL_TRANSACTION                              | 活跃的 SQL 状态                         |
| 25P01   | NO_ACTIVE_SQL_TRANSACTION                              | 没有活跃的 SQL 事务                  |
| 25P02   | IN_FAILED_SQL_TRANSACTION                              | 在失败的 SQL 事务中                  |
| 26000   | INVALID_SQL_STATEMENT_NAME                              | 非法 SQL 语句名                     |
| 28000   | INVALID_AUTHORIZATION_SPECIFICATION                             | 非法授权声明               |
| 2F003   | STATEMENT_NOT_ALLOWED_IN_FUNCTION_CALL                              | 企图使用禁止的 SQL 语句 |
| 3B000   | INVALID_SAVEPOINT_SPECIFICATION                              | 无效的保存点声明               |
| 40P01   | DEADLOCK_DETECTED                              | 侦测到死锁                                   |
| 42601   | SYNTAX_ERROR                              | 语法错误                                          |
| 42602   | INVALID_NAME                              | 非法名字                                          |
| 42703   | UNDEFINED_COLUMN                              | 未定义的字段                                  |
| 42704   | UNDEFINED_OBJECT                              | 未定义的对象                                  |
| 42804   | DATATYPE_MISMATCH                             | 数据类型不匹配                               |
| 42809   | WRONG_OBJECT_TYPE                              | 错误的对象类型                               |
| 42820   | NUMERIC_CONSTANT_OUT_OF_RANGE                              | 数值常数超出范围                 |
| 42821   | DATA_TYPE_MISMATCH                              | 数据类型不匹配                              |
| 42846   | CANNOT_COERCE                              | 不能强迫                                         |
| 42883   | UNDEFINED_FUNCTION                              | 未定义的函数                                |
| 42P01   | UNDEFINED_TABLE                              | 未定义的表                                     |
| 53200   | OUT_OF_MEMORY                              | 内存耗尽                                         |
| 55000   | OBJECT_NOT_IN_STATE                              | 对象不在要求的状态                         |
| 55006   | OBJECT_IN_USE                              | 对象在使用中                                     |
| 57014   | QUERY_CANCELED                              | 查询被取消                                      |
| 58030   | IO_ERROR                              | IO 错误                                               |
| 60000   | SYSTEM_ERROR                               | 系统错误                                          |
| 99999   | UNEXPECTED_ERROR                              | 未定义错误                                    |
