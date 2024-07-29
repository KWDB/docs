---
title: PostgreSQL 错误码
id: error-code-postgresql
---

# PostgreSQL 错误码

::: warning 说明
KWDB 扩展了 PostgreSQL 错误码消息。对一些 PGcode 而言，同一错误码可能对应多条消息。这些消息内容存在部分差异，但导致错误的根本原因是一致的，因此属于同一种类型错误。目前，下表中的消息列只列出了 PGcode 原始的错误码对应的消息，并未包含 KWDB 定制的消息。建议用户根据错误码来查找和定位原因并采取相应的措施。
:::

KWDB 采用部分 PostgreSQL 错误码。此外，一些 KWDB 专有错误码也兼容 PGcode。

本文介绍 KWDB 使用的 PostgreSQL 错误码，列出产生错误的根本原因，并提出相关建议措施。

| 错误码 | 消息                                              | 错误原因 | 建议措施                                           |
| ------------------------------------ | ------------------------------------------------- | -------------------------------------- | -------------------------------------------------- |
| 08P01                                | ProtocolViolation                                 | 网络通信协议错                         | 联系售后支持人员                                   |
| 0A000                                | FeatureNotSupported                               | 功能不支持                             | 无                                                 |
| 0LP01                                | InvalidGrantOperation                             | 授权操作不正确                         | 修改 SQL 语句后重试                                |
| 1000                                 | Warning                                           | 此报错信息为告警                       | 无                                                 |
| 21000                                | CardinalityViolation                              | 基数校验出错                           | 联系售后支持人员                                   |
| 22000                                | DeleteFailure                                     | 数据删除失败或部分失败                 | 重启服务后查询表数据，或者查询日志了解数据删除情况 |
| 22001                                | StringDataRightTruncation                         | 字符串数据右侧被删减                   | 修改 SQL 语句后重试                                |
| 22003                                | NumericValueOutOfRange                            | 数值表达式超出边界                     | 修改 SQL 语句后重试                                |
| 22004                                | NullValueNotAllowed                               | 非法空值                               | 修改 SQL 语句后重试                                |
| 22005                                | InvalidEscapeSequence                             | 转义序列错误                           | 修改 SQL 语句后重试                                |
| 22007                                | InvalidDatetimeFormat                             | 时间格式不正确                         | 修改 SQL 语句后重试                                |
| 22008                                | DatetimeFieldOverflow                             | 时间类型字段溢出                       | 联系售后支持人员                                   |
| 22012                                | DivisionByZero                                    | 除数为 0                               | 修改 SQL 语句后重试                                |
| 22013                                | InvalidWindowFrameOffset                          | 窗口偏移量非法                         | 修改 SQL 语句后重试                                |
| 2201E                                | InvalidArgumentForLogarithm                       | Log 函数参数错误                       | 修改 SQL 语句后重试                                |
| 22021                                | CharacterNotInRepertoire                          | 不可编码的未知字符                     | 检查输入的字符是否符合 UTF8 规范                   |
| 22023                                | InvalidParameterValue                             | 参数值非法                             | 修改 SQL 语句后重试                                |
| 22026                                | StringDataLengthMismatch                          | 字符串数据长度不匹配                   | 修改 SQL 语句后重试                                |
| 2202E                                | ArraySubscript                                    | 数组下标错误                           | 修改数组下标值后重试                               |
| 22C01                                | ScalarOperationCannotRunWithoutFullSessionContext | 当前会话中无法处理此标量表达式         | 修改 SQL 语句后重试                                |
| 22P02                                | InvalidTextRepresentation                         | 文本表达式不正确                       | 修改 SQL 语句后重试                                |
| 22P03                                | InvalidBinaryRepresentation                       | 二进制表达式有错                       | 修改 SQL 语句后重试                                |
| 22P05                                | UntranslatableCharacter                           | 字符串无法正确编码                     | 修改 SQL 语句后重试                                |
| 23502                                | NotNullViolation                                  | 违反非空定义                           | 修改 SQL 语句后重试                                |
| 23503                                | ForeignKeyViolation                               | 外键冲突                               | 修改 SQL 语句后重试                                |
| 23505                                | UniqueViolation                                   | 违法唯一约束                           | 修改 SQL 语句后重试                                |
| 23514                                | CheckViolation                                    | 违反约束                               | 修改 SQL 语句后重试                                |
| 25000                                | InvalidTransactionState                           | 事务状态非法                           | 提交或回滚当前事务后重试                           |
| 25001                                | ActiveSQLTransaction                              | 不支持在事务中间使用 DISCARD 命令      | 不要在事务中间使用 `DISCARD` 命令                  |
| 25006                                | ReadOnlySQLTransaction                            | 当前事务为只读事务                     | 启动读写事务后重试                                 |
| 25P02                                | InFailedSQLTransaction                            | 当前事务已发生错误                     | 结束当前事务，开始新的事务并重试                   |
| 25P03                                | NullTransaction                                   | 事务标识符为空                         | 修改 SQL 语句后重试                                |
| 26000                                | InvalidSQLStatementName                           | 非法查询语句定义                       | 修改 SQL 语句后重试                                |
| 28P01                                | InvalidPassword                                   | 密码不合法                             | 修改 SQL 语句后重试                                |
| 2BP01                                | DependentObjectsStillExist                        | 依赖对象仍然存在                       | 根据提示，解决依赖问题后重试                       |
| 34000                                | InvalidCursorName                                 | 不正确的游标名                         | 修改 SQL 语句后重试                                |
| 3B001                                | InvalidSavepointSpecification                     | 检查点定义不正确                       | 修改 SQL 语句后重试                                |
| 3D000                                | InvalidCatalogName                                | 模式命名出错                           | 修改 SQL 语句后重试                                |
| 3D000                                | UndefinedDatabase                                 | 未定义数据库                           | 修改 SQL 语句后重试                                |
| 3F000                                | InvalidSchemaName                                 | 非法模式名称                           | 修改 SQL 语句后重试                                |
| 42501                                | InsufficientPrivilege                             | 权限不足                               | 向管理员申请权限后重试                             |
| 42601                                | Syntax                                            | 语法错误                               | 修改 SQL 语句后重试                                |
| 42602                                | InvalidName                                       | 引用对象名称不正确                     | 修改 SQL 语句后重试                                |
| 42611                                | InvalidColumnDefinition                           | 不正确的列定义                         | 修改 SQL 语句后重试                                |
| 42622                                | NameTooLong                                       | 名称过长                               | 修改 SQL 语句后重试                                |
| 42701                                | DuplicateColumn                                   | 存在重复列                             | 修改 SQL 语句后重试                                |
| 42702                                | AmbiguousColumn                                   | 列名指代不明确                         | 修改 SQL 语句后重试                                |
| 42703                                | UndefinedColumn                                   | 未定义列                               | 修改 SQL 语句后重试                                |
| 42704                                | UndefinedObject                                   | 未定义对象                             | 修改 SQL 语句后重试                                |
| 42710                                | DuplicateObject                                   | 存在重复对象                           | 修改 SQL 语句后重试                                |
| 42711                                | DuplicateParameter                                | 存在重复参数                           | 修改 SQL 语句后重试                                |
| 42723                                | DuplicateFunction                                 | 存在重复函数                           | 修改 SQL 语句后重试                                |
| 42725                                | AmbiguousFunction                                 | 函数名指代不明确                       | 修改 SQL 语句后重试                                |
| 42803                                | Grouping                                          | 分组操作语法错误                       | 修改 SQL 语句后重试                                |
| 42804                                | DatatypeMismatch                                  | 数据类型不匹配                         | 修改 SQL 语句后重试                                |
| 42809                                | WrongObjectType                                   | 对象类型错误                           | 修改 SQL 语句后重试                                |
| 42830                                | InvalidForeignKey                                 | 非法外键                               | 修改 SQL 语句后重试                                |
| 42846                                | CannotCoerce                                      | 强制转换出错                           | 修改 SQL 语句后重试                                |
| 42883                                | UndefinedFunction                                 | 未定义函数                             | 修改 SQL 语句后重试                                |
| 42939                                | ReservedName                                      | 非法使用保留关键字                     | 修改 SQL 语句后重试                                |
| 42C02                                | SyncObjectFailed                                  | 数据对象同步错误                       | 联系售后支持人员                                   |
| 42C03                                | WrongExpr                                         | 表达式错误                             | 修改 SQL 语句后重试                                |
| 42C04                                | NumberMismatch                                    | 属性值个数不匹配                       | 修改 SQL 语句后重试                                |
| 42P01                                | UndefinedTable                                    | 未定义表                               | 修改 SQL 语句后重试                                |
| 42P02                                | UndefinedParameter                                | 未定义参数                             | 修改 SQL 语句后重试                                |
| 42P04                                | DuplicateDatabase                                 | 存在重复数据库                         | 修改 SQL 语句后重试                                |
| 42P06                                | DuplicateSchema                                   | 存在重复模式名                         | 修改 SQL 语句后重试                                |
| 42P07                                | DuplicateRelation                                 | 存在重复表                             | 修改 SQL 语句后重试                                |
| 42P08                                | AmbiguousParameter                                | 参数指代不明确                         | 修改 SQL 语句后重试                                |
| 42P09                                | AmbiguousAlias                                    | 别名指代不明确                         | 在查询语句中使用明确的别名                         |
| 42P10                                | InvalidColumnReference                            | 不正确的列引用                         | 修改 SQL 语句后重试                                |
| 42P15                                | InvalidSchemaDefinition                           | 非法模式定义                           | 修改 SQL 语句后重试                                |
| 42P16                                | InvalidTableDefinition                            | 表定义不正确                           | 修改 SQL 语句后重试                                |
| 42P17                                | InvalidObjectDefinition                           | 对象定义不正确                         | 修改 SQL 语句后重试                                |
| 42P18                                | IndeterminateDatatype                             | 未识别的数据类型                       | 修改 SQL 语句后重试                                |
| 42P20                                | Windowing                                         | 窗口函数语法不正确                     | 修改 SQL 语句后重试                                |
| 53200                                | OutOfMemory                                       | 内存耗尽                               | 联系售后支持人员                                   |
| 54000                                | ProgramLimitExceeded                              | 用户使用的字符串超过最大值             | 修改 SQL 语句后重试                                |
| 54011                                | TooManyColumns                                    | 列数量过多                             | 修改 SQL 语句后重试                                |
| 54021                                | TooWideRowWidth                                   | 行宽过大                               | 修改 SQL 语句后重试                                |
| 54022                                | InsertColumnMismatch                              | 插入列不匹配                           | 修改 SQL 语句后重试                                |
| 54024                                | TooWideTagWidth                                   | 属性名称过长                           | 修改 SQL 语句后重试                                |
| 55000                                | ObjectNotInPrerequisiteState                      | 对象操作不满足前置条件                 | 根据提示，解决依赖问题后重试                       |
| 55006                                | ObjectInUse                                       | 对象在使用中                           | 终止占用对象操作后重试                             |
| 55P02                                | CantChangeRuntimeParam                            | 当前不可更改运行时参数                 | 在数据库离线状态下重试                             |
| 57P03                                | CannotConnectNow                                  | 数据库不可连接                         | 等待数据库进入服务状态后重试                       |
| 58C00                                | RangeUnavailable                                  | 键值分区错误                           | 联系售后支持人员                                   |
| 58C01                                | InternalConnectionFailure                         | 内部连接错误                           | 联系售后支持人员                                   |
| XX000                                | Internal                                          | 数据库内部错误                         | 联系售后支持人员                                   |
| XXC01                                | CCLRequired                                       | 任务完成需要使用 CCL                   | 联系售后支持人员                                   |
