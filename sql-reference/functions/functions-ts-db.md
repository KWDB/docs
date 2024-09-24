---
title: 时序数据函数
id: functions-ts-db
---

# 时序数据函数

数据库函数是一组预定义的操作，用于对数据执行特定的计算或转换。

## 特殊语法形式

为了兼容 SQL 标准，KWDB 支持以下函数，这些函数与常规的内置函数具有等效功能。

| 特殊形式                                                 | 等价于                                   |
| ------------------------------------------------------- | ---------------------------------------- |
| `AT TIME ZONE`                                            | `timezone()`                               |
| `CURRENT_CATALOG`                                         | `current_database()`                       |
| `COLLATION FOR`                                           | `pg_collation_for()`                       |
| `CURRENT_DATE`                                            | `current_date()`                           |
| `CURRENT_ROLE`                                            | `current_user()`                           |
| `CURRENT_SCHEMA`                                          | `current_schema()`                         |
| `CURRENT_TIMESTAMP`                                       | `current_timestamp()`                      |
| `CURRENT_TIME`                                            | `current_time()`                           |
| `CURRENT_USER`                                            | `current_user()`                           |
| `EXTRACT(<part> FROM <value>)`                            | `extract("<part>", <value>)`               |
| `EXTRACT_DURATION(<part>FROM <value>)`                    | `extract_duration("<part>",<value>)`       |
| `OVERLAY(<text1> PLACING <text2> FROM <int1> FOR <int2>)` | `overlay(<text1>,<text2>, <int1>, <int2>)` |
| `OVERLAY(<text1> PLACING <text2> FROM <int>)`             | `overlay(<text1>,<text2>, <int>)`          |
| `POSITION(<text1> IN <text2>)`                            | `strpos(<text2>, <text1>)`                 |
| `SESSION_USER`                                            | `current_user()`                           |
| `SUBSTRING(<text>FOR<int1>FROM <int2>)`                   | `substring(<text>,<int2>, <int1>)`         |
| `SUBSTRING(<text> FOR <int>)`                             | `substring(<text>, 1, <int>)`              |
| `SUBSTRING(<text>FROM<int1>FOR<int2>)`                    | `substring(<text>,<int1>, <int2>)`         |
| `SUBSTRING(<text> FROM <int>)`                            | `substring(<text>, <int>)`                 |
| `TRIM(<text1> FROM <text2>)`                              | `btrim(<text2>, <text1>)`                  |
| `TRIM(<text1>, <text2>)`                                  | `btrim(<text1>, <text2>)`                  |
| `TRIM(FROM <text>)`                                       | `btrim(<text>)`                            |
| `TRIM(LEADING <text1> FROM <text2>)`                      | `ltrim(<text2>, <text1>)`                  |
| `TRIM(LEADING FROM <text>)`                               | `ltrim(<text>)`                            |
| `TRIM(TRAILING <text1> FROM <text2>)`                     | `rtrim(<text2>, <text1>)`                  |
| `TRIM(TRAILING FROM <text>)`                              | `rtrim(<text>)`                            |
| `USER`                                                    | `current_user()`                           |

## 条件和类函数运算符


具有特殊评估规则的运算符如下：

| 运算符      | 描述                                                                                                                                                    |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CAST(...)   | 类型转换 <br >**说明** <br >- 时序表建表时，如果时间戳列的数据类型设置为 TIMESTAMP，系统会自动处理为 TIMESTAMPTZ，对该列的转换将按照数据库设置的时区进行转换。<br >- 使用 `CAST` 函数将 CHAR、NCHAR 或 VARCHAR 数据类型转换为长度不同的 CHAR、NCHAR 或 VARCHAR 数据类型时，如果目标长度不匹配原始字符串的实际字节数，服务端可能会返回乱码，客户端（如 KaiwuDB JDBC 或 KaiwuDB 开发者中心）会提示报错。 |
| IFNULL(...) | COALESCE 限制为两个操作数的别名                                                                                                                         |
| NULLIF(...) | NULL 有条件地返回                                                                                                                                       |

## 内置函数

### 日期和时间函数

| 函数 → 返回值                                                                    | 描述                                                                                                                                                                                                                                                    |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| age(end: timestamptz, begin: timestamptz) → interval                             | 计算 begin 和 end 之间的时间间隔。                                                                                                                                                                                                                      |
| age(val: timestamptz) → interval                                                 | 计算 val 与当前时间之间的间隔。                                                                                                                                                                                                                         |
| current_timestamp() → timestamp                                                  | 返回当前事务的时间。该值基于事务开始时选择的时间戳，并且在整个事务中保持不变。此时间戳与并发事务的提交顺序无关。                                                                                                                                      |
| current_timestamp() → timestamptz                                                | 返回当前事务的时间。该值基于事务开始时选择的时间戳，并且在整个事务中保持不变。此时间戳与并发事务的提交顺序无关。                                                                                                                                      |
| date_trunc(element: string, input: timestamp) → timestamp                        | 将输入截断成精度为 element，将所有无意义的字段设为 0（或对于日期和月份则设为 1）。兼容元素：millennium、century、decade、year、quarter、month、week、day、hour、minute、second、millisecond、microsecond。                                            |
| date_trunc(element: string, input: timestamptz) → timestamptz                    | 将输入截断成精度为 element，将所有无意义的字段设为 0（或对于日期和月份则设为 1）。兼容元素：millennium、century、decade、year、quarter、month、week、day、hour、minute、second、millisecond、microsecond。                                           |
| experimental_strftime(input: timestamp, extract_format: string) → string         |从输入中提取并格式化成 extract_format 标识的时间，extract_format 使用标准的 strftime 表示法（尽管不支持所有格式）。                                                                                                                                  |
| experimental_strftime(input: timestamptz, extract_format: string) → string       |从输入中提取并格式化成 extract_format 标识的时间，extract_format 使用标准的 strftime 表示法（尽管不支持所有格式）。                                                                                                                                  |
| extract(element: string, input: timestamp) → float8                              | 从输入中提取 element。兼容元素：millennium、century、decade、year、isoyear、quarter、month、week、dayofweek、isodow、dayofyear、julian、hour、minute、second、millisecond、microsecond、epoch、timezone、timezone_hour、timezone_minute。                   |
| extract(element: string, input: timestamptz) → float8                            | 从输入中提取 element。兼容元素：millennium、century、decade、year、isoyear、quarter、month、week、dayofweek、isodow、dayofyear、julian、hour、minute、second、millisecond、microsecond、epoch、timezone、timezone_hour、timezone_minute。                   |
| localtimestamp() → timestamp                                                     | 返回当前事务的时间。该值基于事务开始时选择的时间戳，并且在整个事务中保持不变。此时间戳与并发事务的提交顺序无关。                                                                                                                                      |
| localtimestamp() → timestamptz                                                   | 返回当前事务的时间。该值基于事务开始时选择的时间戳，并且在整个事务中保持不变。此时间戳与并发事务的提交顺序无关。                                                                                                                                      |
| localtimestamp(precision: int8) → timestamp                                      | 返回当前事务的时间。该值基于事务开始时选择的时间戳，并且在整个事务中保持不变。此时间戳与并发事务的提交顺序无关。                                                                                                                                      |
| localtimestamp(precision: int8) → timestamptz                                    | 返回当前事务的时间。该值基于事务开始时选择的时间戳，并且在整个事务中保持不变。此时间戳与并发事务的提交顺序无关。                                                                                                                                      |
| now() → timestamp                                                                | 返回当前事务的时间。该值基于事务开始时选择的时间戳，并且在整个事务中保持不变。此时间戳与并发事务的提交顺序无关。                                                                                                                                        |
| now() → timestamptz                                                              | 返回当前事务的时间。该值基于事务开始时选择的时间戳，并且在整个事务中保持不变。此时间戳与并发事务的提交顺序无关。                                                                                                                                      |
| statement_timestamp() → timestamp                                                | 返回当前语句的开始时间戳。                                                                                                                                                                                                                              |
| statement_timestamp() → timestamptz                                              | 返回当前语句的开始时间戳。                                                                                                                                                                                                                              |
| timeofday() → string                                                             | 返回某个集群节点的当前系统时间。                                                                                                                                                                                                                        |
| time_bucket(timestamp_column: timestamp, interval: STRING) → timestamp           | 时间桶函数，支持时间戳对齐。<br> 参数说明：<br>- timestamp_column：时间戳列。 <br>- interval：时间间隔，支持的单位包括秒（s）、分（m）、小时（h）、天（d）、周（w）、月（mon）、年（y）。目前，KWDB 不支持复合时间格式，如 `1d1h`。                                                                                                                                                |
| time_bucket(timestamp_column: timestamptz, interval: STRING) → timestamptz       | 时间桶函数，支持时间戳对齐。<br> 参数说明：<br>- timestamp_column：时间戳列。 <br>- interval：时间间隔，支持的单位包括秒（s）、分（m）、小时（h）、天（d）、周（w）、月（mon）、年（y）。目前，KWDB 不支持复合时间格式，如 `1d1h`。                                                                                                                                                |
| time_bucket_gapfill(timestamp_column: timestamp, interval: STRING) → timestamp     | 时间桶函数，支持时间戳对齐并根据时间间隔将缺失的时间戳进行写入操作。该函数需要与 `GROUP BY`、`ORDER BY` 配合使用。使用 `time_bucket_gapfill()`的同时，再进行其他查询时，需要使用聚合函数。<br> 参数说明：<br>- timestamp_column：时间戳列。 <br>- interval：时间间隔，支持的单位包括秒（s）、分（m）、小时（h）、天（d）、周（w）、月（mon）、年（y）。目前，KWDB 不支持复合时间格式，如 `1d1h`。 |
| time_bucket_gapfill(timestamp_column: timestamptz, interval: STRING) → timestamptz | 时间桶函数，支持时间戳对齐并根据时间间隔将缺失的时间戳进行写入操作。该函数需要与 `GROUP BY`、`ORDER BY` 配合使用。使用 `time_bucket_gapfill()`的同时，再进行其他查询时，需要使用聚合函数。<br> 参数说明：<br>- timestamp_column：时间戳列。 <br>- interval：时间间隔，支持的单位包括秒（s）、分（m）、小时（h）、天（d）、周（w）、月（mon）、年（y）。目前，KWDB 不支持复合时间格式，如 `1d1h`。 |
| time_bucket_gapfill(timestamp_column: timestamp, interval: int8) → timestamp     | 时间桶函数，支持时间戳对齐并根据时间间隔将缺失的时间戳进行写入操作。该函数需要与 `GROUP BY`、`ORDER BY` 配合使用。使用 `time_bucket_gapfill()`的同时，再进行其他查询时，需要使用聚合函数。<br> 参数说明：<br>- timestamp_column：时间戳列。 <br>- interval：时间间隔（单位：秒）。 |
| time_bucket_gapfill(timestamp_column: timestamptz, interval: int8) → timestamptz | 时间桶函数，支持时间戳对齐并根据时间间隔将缺失的时间戳进行写入操作。该函数需要与 `GROUP BY`、`ORDER BY` 配合使用。使用 `time_bucket_gapfill()`的同时，再进行其他查询时，需要使用聚合函数。<br> 参数说明：<br>- timestamp_column：时间戳列。 <br>- interval：时间间隔（单位：秒）。 |
| transaction_timestamp() → timestamp                                              | 返回当前事务的时间。该值基于事务开始时选择的时间戳，并且在整个事务中保持不变。此时间戳与并发事务的提交顺序无关。                                                                                                                                      |
| transaction_timestamp() → timestamptz                                            | 返回当前事务的时间。该值基于事务开始时选择的时间戳，并且在整个事务中保持不变。此时间戳与并发事务的提交顺序无关。                                                                                                                                      |

### 数学和数值函数


| 函数 → 返回值                                                       | 描述                                                                                 |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| abs(val: float4) → float4                                           | 计算 val 的绝对值。                                                                  |
| abs(val: float8) → float8                                           | 计算 val 的绝对值。                                                                  |
| abs(val: int2) → int2                                               | 计算 val 的绝对值。                                                                  |
| abs(val: int4) → int4                                               | 计算 val 的绝对值。                                                                  |
| abs(val: int8) → int8                                               | 计算 val 的绝对值。                                                                  |
| acos(val: float4) → float8                                          | 计算 val 的反余弦值。                                                                |
| acos(val: float8) → float8                                          | 计算 val 的反余弦值。                                                                |
| asin(val: float4) → float8                                          | 计算 val 的反正弦值。                                                                |
| asin(val: float8) → float8                                          | 计算 val 的反正弦值。                                                                |
| atan(val: float4) → float8                                          | 计算 val 的反正切值。                                                                |
| atan(val: float8) → float8                                          | 计算 val 的反正切值。                                                                |
| atan2(x: float4, y: float4) → float8                                | 计算 x / y 的反正切。                                                                |
| atan2(x: float4, y: float8) → float8                                | 计算 x / y 的反正切。                                                                |
| atan2(x: float8, y: float4) → float8                                | 计算 x / y 的反正切。                                                                |
| atan2(x: float8, y: float8) → float8                                | 计算 x / y 的反正切。                                                                |
| cbrt(val: float4) → float8                                          | 计算 val 的立方根(∛)。                                                              |
| cbrt(val: float8) → float8                                          | 计算 val 的立方根(∛)。                                                              |
| ceil(val: float4) → float8                                          | 计算大于等于 val 的最小整数。                                                        |
| ceil(val: float8) → float8                                          | 计算大于等于 val 的最小整数。                                                        |
| ceil(val: int2) → float8                                            | 计算大于等于 val 的最小整数。                                                        |
| ceil(val: int4) → float8                                            | 计算大于等于 val 的最小整数。                                                        |
| ceil(val: int8) → float8                                            | 计算大于等于 val 的最小整数。                                                        |
| ceiling(val: float4) → float8                                       | 计算大于等于 val 的最小整数。                                                        |
| ceiling(val: float8) → float8                                       | 计算大于等于 val 的最小整数。                                                        |
| ceiling(val: int2) → float8                                         | 计算大于等于 val 的最小整数。                                                        |
| ceiling(val: int4) → float8                                         | 计算大于等于 val 的最小整数。                                                        |
| ceiling(val: int8) → float8                                         | 计算大于等于 val 的最小整数。                                                        |
| cos(val: float4) → float8                                           | 计算 val 的余弦值。                                                                  |
| cos(val: float8) → float8                                           | 计算 val 的余弦值。                                                                  |
| cot(val: float4) → float8                                           | 计算 val 的余切值。                                                                  |
| cot(val: float8) → float8                                           | 计算 val 的余切值。                                                                  |
| crc32c(string...) → int8                                            | 使用 Castagnoli 多项式计算 CRC-32 哈希值。                                           |
| crc32ieee(string...) → int8                                         | 使用 IEEE 多项式计算 CRC-32 哈希值。                                                 |
| degrees(val: float4) → float8                                       | 将 val 作为弧度值转换为度数值。                                                      |
| degrees(val: float8) → float8                                       | 将 val 作为弧度值转换为度数值。                                                      |
| div(x: float4, y: float4) → float8                                  | 计算 x / y 的整数商。                                                                |
| div(x: float4, y: float8) → float8                                  | 计算 x / y 的整数商。                                                                |
| div(x: float8, y: float4) → float8                                  | 计算 x / y 的整数商。                                                                |
| div(x: float8, y: float8) → float8                                  | 计算 x / y 的整数商。                                                                |
| div(x: int2, y: int2) → int8                                        | 计算 x / y 的整数商。                                                                |
| div(x: int2, y: int4) → int8                                        | 计算 x / y 的整数商。                                                                |
| div(x: int2, y: int8) → int8                                        | 计算 x / y 的整数商。                                                                |
| div(x: int4, y: int2) → int8                                        | 计算 x / y 的整数商。                                                                |
| div(x: int4, y: int4) → int8                                        | 计算 x / y 的整数商。                                                                |
| div(x: int4, y: int8) → int8                                        | 计算 x / y 的整数商。                                                                |
| div(x: int8, y: int2) → int8                                        | 计算 x / y 的整数商。                                                                |
| div(x: int8, y: int4) → int8                                        | 计算 x / y 的整数商。                                                                |
| div(x: int8, y: int8) → int8                                        | 计算 x / y 的整数商。                                                                |
| exp(val: float4) → float8                                           | 计算 e ^ val。                                                                       |
| exp(val: float8) → float8                                           | 计算 e ^ val。                                                                       |
| floor(val: float4) → float8                                         | 计算不大于 val 的最大整数。                                                          |
| floor(val: float8) → float8                                         | 计算不大于 val 的最大整数。                                                          |
| floor(val: int2) → float8                                           | 计算不大于 val 的最大整数。                                                          |
| floor(val: int4) → float8                                           | 计算不大于 val 的最大整数。                                                          |
| floor(val: int8) → float8                                           | 计算不大于 val 的最大整数。                                                          |
| fnv32(string...) → int8                                             | 计算一组值的 32 位 FNV-1 哈希值。                                                    |
| fnv32a(string...) → int8                                            | 计算一组值的 32 位 FNV-1a 哈希值。                                                   |
| fnv64(string...) → int8                                             | 计算一组值的 64 位 FNV-1 哈希值。                                                    |
| fnv64a(string...) → int8                                            | 计算一组值的 64 位 FNV-1a 哈希值。                                                   |
| isnan(val: float4) → bool                                           | 如果 val 是 NaN，则返回 `true`，否则返回 `false`。                                       |
| isnan(val: float8) → bool                                           | 如果 val 是 NaN，则返回 `true`，否则返回 `false`。                                       |
| ln(val: float4) → float8                                            | 计算 val 的自然对数。                                                                |
| ln(val: float8) → float8                                            | 计算 val 的自然对数。                                                                |
| log(b: float4, x: float4) → float8                                  | 计算 val 的指定基数的 log。                                                          |
| log(b: float4, x: float8) → float8                                  | 计算 val 的指定基数的 log。                                                          |
| log(b: float8, x: float4) → float8                                  | 计算 val 的指定基数的 log。                                                          |
| log(b: float8, x: float8) → float8                                  | 计算 val 的指定基数的 log。                                                          |
| log(val: float4) → float8                                           | 计算 val 的基数为 10 的 log。                                                        |
| log(val: float8) → float8                                           | 计算 val 的基数为 10 的 log。                                                        |
| mod(x: float4, y: float4) → float8                                  | 计算 x％y。                                                                          |
| mod(x: float4, y: float8) → float8                                  | 计算 x％y。                                                                          |
| mod(x: float8, y: float4) → float8                                  | 计算 x％y。                                                                          |
| mod(x: float8, y: float8) → float8                                  | 计算 x％y。                                                                          |
| mod(x: int2, y: int2) → int8                                        | 计算 x％y。                                                                          |
| mod(x: int2, y: int4) → int8                                        | 计算 x％y。                                                                          |
| mod(x: int2, y: int8) → int8                                        | 计算 x％y。                                                                          |
| mod(x: int4, y: int2) → int8                                        | 计算 x％y。                                                                          |
| mod(x: int4, y: int4) → int8                                        | 计算 x％y。                                                                          |
| mod(x: int4, y: int8) → int8                                        | 计算 x％y。                                                                          |
| mod(x: int8, y: int2) → int8                                        | 计算 x％y。                                                                          |
| mod(x: int8, y: int4) → int8                                        | 计算 x％y。                                                                          |
| mod(x: int8, y: int8) → int8                                        | 计算 x％y。                                                                          |
| pi() → float8                                                       | 返回 pi 的值（3.141592653589793）。                                                    |
| pow(x: float4, y: float4) → float8                                  | 计算 x^y。                                                                           |
| pow(x: float4, y: float8) → float8                                  | 计算 x^y。                                                                           |
| pow(x: float8, y: float4) → float8                                  | 计算 x^y。                                                                           |
| pow(x: float8, y: float8) → float8                                  | 计算 x^y。                                                                           |
| pow(x: int2, y: int2) → int8                                        | 计算 x^y。                                                                           |
| pow(x: int2, y: int4) → int8                                        | 计算 x^y。                                                                           |
| pow(x: int2, y: int8) → int8                                        | 计算 x^y。                                                                           |
| pow(x: int4, y: int2) → int8                                        | 计算 x^y。                                                                           |
| pow(x: int4, y: int4) → int8                                        | 计算 x^y。                                                                           |
| pow(x: int4, y: int8) → int8                                        | 计算 x^y。                                                                           |
| pow(x: int8, y: int2) → int8                                        | 计算 x^y。                                                                           |
| pow(x: int8, y: int4) → int8                                        | 计算 x^y。                                                                           |
| pow(x: int8, y: int8) → int8                                        | 计算 x^y。                                                                           |
| power(x: float4, y: float4) → float8                                | 计算 x^y。                                                                           |
| power(x: float4, y: float8) → float8                                | 计算 x^y。                                                                           |
| power(x: float8, y: float4) → float8                                | 计算 x^y。                                                                           |
| power(x: float8, y: float8) → float8                                | 计算 x^y。                                                                           |
| power(x: int2, y: int2) → int8                                      | 计算 x^y。                                                                           |
| power(x: int2, y: int4) → int8                                      | 计算 x^y。                                                                           |
| power(x: int2, y: int8) → int8                                      | 计算 x^y。                                                                           |
| power(x: int4, y: int2) → int8                                      | 计算 x^y。                                                                           |
| power(x: int4, y: int4) → int8                                      | 计算 x^y。                                                                           |
| power(x: int4, y: int8) → int8                                      | 计算 x^y。                                                                           |
| power(x: int8, y: int2) → int8                                      | 计算 x^y。                                                                           |
| power(x: int8, y: int4) → int8                                      | 计算 x^y。                                                                           |
| power(x: int8, y: int8) → int8                                      | 计算 x^y。                                                                           |
| radians(val: float4) → float8                                       | 将 val 作为度数值转换为弧度值。                                                      |
| radians(val: float8) → float8                                       | 将 val 作为度数值转换为弧度值。                                                      |
| random() → float8                                                   | 返回 0 到 1 之间的随机浮点数。                                                       |
| round(val: float4) → float8                                         | 使用四舍六入五成双（half to even）（即银行家）规则将 val 舍入到最接近的整数。     |
| round(val: float8) → float8                                         | 使用四舍六入五成双（half to even）（即银行家）规则将 val 舍入到最接近的整数。     |
| sign(val: float4) → float8                                          | 确定 val 的符号：<br>- `1` 表示正。 <br>- `0` 表示值 0。 <br>- `-1` 表示负。                                     |
| sign(val: float8) → float8                                          | 确定 val 的符号：<br>- `1` 表示正。 <br>- `0` 表示值 0。 <br>- `-1` 表示负。                                     |
| sign(val: int2) → int8                                              | 确定 val 的符号：<br>- `1` 表示正。 <br>- `0` 表示值 0。 <br>- `-1` 表示负。                                     |
| sign(val: int4) → int8                                              | 确定 val 的符号：<br>- `1` 表示正。 <br>- `0` 表示值 0。 <br>- `-1` 表示负。                                     |
| sign(val: int8) → int8                                              | 确定 val 的符号：<br>- `1` 表示正。 <br>- `0` 表示值 0。 <br>- `-1` 表示负。                                     |
| sin(val: float4) → float8                                           | 计算 val 的正弦值。                                                                  |
| sin(val: float8) → float8                                           | 计算 val 的正弦值。                                                                  |
| sqrt(val: float4) → float8                                          | 计算 val 的平方根。                                                                  |
| sqrt(val: float8) → float8                                          | 计算 val 的平方根。                                                                  |
| tan(val: float4) → float8                                           | 计算 val 的正切值。                                                                  |
| tan(val: float8) → float8                                           | 计算 val 的正切值。                                                                  |
| trunc(val: float4) → float8                                         | 截断 val 的十进制值。                                                                |
| trunc(val: float8) → float8                                         | 截断 val 的十进制值。                                                                |
| width_bucket(operand: int8, b1: int2, b2: int2, count: int8) → int8 | 返回在直方图中为其分配操作数的存储桶编号，直方图具有跨越 B1 到 B2 的等宽存储桶计数。 |
| width_bucket(operand: int8, b1: int2, b2: int4, count: int8) → int8 | 返回在直方图中为其分配操作数的存储桶编号，直方图具有跨越 B1 到 B2 的等宽存储桶计数。 |
| width_bucket(operand: int8, b1: int2, b2: int8, count: int8) → int8 | 返回在直方图中为其分配操作数的存储桶编号，直方图具有跨越 B1 到 B2 的等宽存储桶计数。 |
| width_bucket(operand: int8, b1: int4, b2: int2, count: int8) → int8 | 返回在直方图中为其分配操作数的存储桶编号，直方图具有跨越 B1 到 B2 的等宽存储桶计数。 |
| width_bucket(operand: int8, b1: int4, b2: int4, count: int8) → int8 | 返回在直方图中为其分配操作数的存储桶编号，直方图具有跨越 B1 到 B2 的等宽存储桶计数。 |
| width_bucket(operand: int8, b1: int4, b2: int8, count: int8) → int8 | 返回在直方图中为其分配操作数的存储桶编号，直方图具有跨越 B1 到 B2 的等宽存储桶计数。 |
| width_bucket(operand: int8, b1: int8, b2: int2, count: int8) → int8 | 返回在直方图中为其分配操作数的存储桶编号，直方图具有跨越 B1 到 B2 的等宽存储桶计数。 |
| width_bucket(operand: int8, b1: int8, b2: int4, count: int8) → int8 | 返回在直方图中为其分配操作数的存储桶编号，直方图具有跨越 B1 到 B2 的等宽存储桶计数。 |
| width_bucket(operand: int8, b1: int8, b2: int8, count: int8) → int8 | 返回在直方图中为其分配操作数的存储桶编号，直方图具有跨越 B1 到 B2 的等宽存储桶计数。 |

### 字符串和字节函数

| 函数 → 返回值                                                         | 描述                                                                                                           |
| ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| bit_length(val: string) → int8                                        | 计算数值的位数。                                                                                               |
| char_length(val: string) → int8                                       | 计算数值占用的字符数。                                                                                         |
| character_length(val: string) → int8                                  | 计算数值占用的字符数。                                                                                         |
| chr(val: int2) → string                                               | 返回带有 val 中给出的代码的字符。`ascii()` 的反函数。                                                          |
| chr(val: int4) → string                                               | 返回带有 val 中给出的代码的字符。`ascii()` 的反函数。                                                          |
| chr(val: int8) → string                                               | 返回带有 val 中给出的代码的字符。`ascii()` 的反函数。                                                          |
| concat(string...) → string                                            | 连接使用逗号（`,`）隔开的字符串列表。                                                                                   |
| initcap(val: string) → string                                         | 将 val 的第一个字母大写。                                                                                      |
| left(input: string, return_set: int8) → string                        | 从 input 返回前 `return_set` 个字符。                                                                            |
| length(val: string) → int8                                            | 计算 val 中的字符数。                                                                                          |
| lower(val: string) → string                                           | 将 val 中的所有字符转换为小写。                                                                                |
| lpad(string: string, length: int8) → string                           | 在字符串的左侧添加双引号（`""`），以填充字符串的长度。如果字符串的长度超过长度，则会被截断。                             |
| lpad(string: string, length: int8, fill: string) → string             | 在字符串的左侧添加 fill，以填充字符串的长度。如果字符串的长度超过长度，则会被截断。                            |
| ltrim(input: string, trim_chars: string) → string                     | 从输入的开头（左侧）删除 `trim_chars` 中包含的任何字符（递归应用）。例如，`ltrim('doggie','od')` 返回 `ggie`。   |
| ltrim(val: string) → string                                           | 删除 val 开头（左侧）的所有空格。                                                                              |
| octet_length(val: string) → int8                                      | 计算数值占用的字节数。                                                                                         |
| right(input: string, return_set: int8) → string                       | 返回 input 中最后 `return_set` 个字符。                                                                          |
| rpad(string: string, length: int8) → string                           | 在字符串的右侧添加双引号（`""`），以填充字符串的长度。如果字符串的长度超过长度，则会被截断。                             |
| rpad(string: string, length: int8, fill: string) → string             | 在字符串的右侧添加 fill，以填充字符串的长度。如果字符串的长度超过长度，则会被截断。                            |
| rtrim(input: string, trim_chars: string) → string                     | 从输入的末尾（右侧）删除 `trim_chars` 中包含的任何字符（递归应用）。例如，`rtrim('doggie'，'ei')` 返回 `dogg`。 |
| rtrim(val: string) → string                                           | 从 val 的末端（右侧）移除所有空格。                                                                            |
| substr(input: string, regex: string) → string                         | 返回与正则表达式 regex 匹配的 input 子字符串。                                                                 |
| substr(input: string, regex: string, escape_char: string) → string    | 返回与正则表达式 regex 匹配的 input 子字符串，使用 `escape_char` 作为转义字符而不是作为正则表达式的特殊符号。    |
| substr(input: string, start_pos: int8) → string                       | 返回 `start_pos` 和 `end_pos` 之间的 input 子字符串（从 1 开始计数）。                                           |
| substr(input: string, start_pos: int8, length: int8) → string         | 返回从 `substr_pos` 开始的 input 子字符串（从 1 开始计数）。                                                   |
| substring(input: string, regex: string) → string                      | 返回与正则表达式匹配 regex 的 input 子字符串。                                                                 |
| substring(input: string, regex: string, escape_char: string) → string | 返回与正则表达式匹配 regex 的 input 子字符串，使用 `escape_char` 作为转义字符而不是作为正则表达式的特殊符号。    |
| substring(input: string, start_pos: int8) → string                    | 返回 `start_pos` 和 `end_pos` 之间的 input 子字符串（从 1 开始计数）。                                           |
| substring(input: string, start_pos: int8, length: int8) → string      | 返回从 `substr_pos` 开始的 input 子字符串（从 1 开始计数）。                                                   |
| upper(val: string) → string                                           | 将 val 中的所有字符转换为大写字母。                                                                            |

## 聚合函数

::: warning 说明

- 避免 `AVG`、`SUM` 函数的计算结果超过函数支持的最大范围。
- 聚合查询与 `GROUP BY` 连用时，避免 `GROUP BY` 后的结果集行数过大。

:::

| 函数 → 返回值                             | 描述                                                      |
| ------------------------------------------ | --------------------------------------------------------- |
| avg(arg1: float4) → float8                | 计算选定值的平均值。                                      |
| avg(arg1:  float8) → float8               | 计算选定值的平均值。                                      |
| avg(arg1: INT2) → DECIMAL                 | 计算选定值的平均值。                                      |
| avg(arg1: INT4) → DECIMAL                 | 计算选定值的平均值。                                      |
| avg(arg1: INT8) → DECIMAL                 | 计算选定值的平均值。                                      |
| count(arg1: anyelement) → INT8            | 计算选定元素的数目。                                      |
| first(val: float4) → float4               | 获取条件范围内时间戳最小的一条数据（不包含空值 NULL）。   |
| first(val:  float8) →  float8             | 获取条件范围内时间戳最小的一条数据（不包含空值 NULL）。   |
| first(val: INT2) → INT2                   | 获取条件范围内时间戳最小的一条数据（不包含空值 NULL）。   |
| first(val: INT4) → INT4                   | 获取条件范围内时间戳最小的一条数据（不包含空值 NULL）。   |
| first(val: INT8) → INT8                   | 获取条件范围内时间戳最小的一条数据（不包含空值 NULL）。   |
| first(val: STRING) → STRING               | 获取条件范围内的时间戳最小的一条数据（不包含空值 NULL）。 |
| first(val: timestamp) → timestamp         | 获取条件范围内时间戳最小的一条数据（不包含空值 NULL）。   |
| first(val: timestamptz) → timestamptz     | 获取条件范围内时间戳最小的一条数据（不包含空值 NULL）。   |
| first(val: varbytes) →varbytes            | 获取条件范围内时间戳最小的一条数据（不包含空值 NULL）。   |
| first(val: varchar) →varchar              | 获取条件范围内时间戳最小的一条数据（不包含空值 NULL）。   |
| first(*)→any element                      | 获取条件范围内时间戳最小的一条数据（不包含空值 NULL）。   |
| first_row(val: float4) → float4           | 获取条件范围内时间戳最小的一条数据（可以是空值 NULL）。   |
| first_row(val:  float8) →  float8         | 获取条件范围内时间戳最小的一条数据（可以是空值 NULL）。   |
| first_row(val: INT2) → INT2               | 获取条件范围内时间戳最小的一条数据（可以是空值 NULL）。   |
| first_row(val: INT4) → INT4               | 获取条件范围内时间戳最小的一条数据（可以是空值 NULL）。   |
| first_row(val: INT8) → INT8               | 获取条件范围内时间戳最小的一条数据（可以是空值 NULL）。   |
| first_row(val: STRING) → STRING           | 获取条件范围内时间戳最小的一条数据（可以是空值 NULL）。   |
| first_row(val: timestamp) → timestamp     | 获取条件范围内时间戳最小的一条数据（可以是空值 NULL）。   |
| first_row(val: timestamptz) → timestamptz | 获取条件范围内时间戳最小的一条数据（可以是空值 NULL）。   |
| first_row(val: varbytes) →varbytes        | 获取条件范围内时间戳最小的一条数据（可以是空值 NULL）。   |
| first_row(val: varchar) →varchar          | 获取条件范围内时间戳最小的一条数据（可以是空值 NULL）。   |
| first_row(*) →any element                 | 获取条件范围内时间戳最小的一条数据（可以是空值 NULL）。   |
| last(val: float4) → float4                | 获取条件范围内时间戳最大的一条数据（不包含空值 NULL）。   |
| last(val:  float8) →  float8              | 获取条件范围内时间戳最大的一条数据（不包含空值 NULL）。   |
| last(val: INT2) → INT2                    | 获取条件范围内时间戳最大的一条数据（不包含空值 NULL）。   |
| last(val: INT4) → INT4                    | 获取条件范围内时间戳最大的一条数据（不包含空值 NULL）。   |
| last(val: INT8) → INT8                    | 获取条件范围内时间戳最大的一条数据（不包含空值 NULL）。   |
| last(val: STRING) → STRING                | 获取条件范围内时间戳最大的一条数据（不包含空值 NULL）。   |
| last(val: timestamp) → timestamp          | 获取条件范围内时间戳最大的一条数据（不包含空值 NULL）。   |
| last(val: timestamptz) → timestamptz      | 获取条件范围内时间戳最大的一条数据（不包含空值 NULL）。   |
| last(val: varbytes) →varbytes             | 获取条件范围内时间戳最大的一条数据（不包含空值 NULL）。   |
| last(val: varchar) →varchar               | 获取条件范围内时间戳最大的一条数据（不包含空值 NULL）。   |
| last(*)→any element                       | 获取条件范围内时间戳最大的一条数据（不包含空值 NULL）。   |
| last_row (val: varchar) →varchar          | 获取条件范围内时间戳最大的一条数据（可以是空值 NULL）。   |
| last_row(val: float4) → float4            | 获取条件范围内时间戳最大的一条数据（可以是空值 NULL）。   |
| last_row(val:  float8) →  float8          | 获取条件范围内时间戳最大的一条数据（可以是空值 NULL）。   |
| last_row(val: INT2) → INT2                | 获取条件范围内时间戳最大的一条数据（可以是空值 NULL）。   |
| last_row(val: INT4) → INT4                | 获取条件范围内时间戳最大的一条数据（可以是空值 NULL）。   |
| last_row(val: INT8) → INT8                | 获取条件范围内时间戳最大的一条数据（可以是空值 NULL）。   |
| last_row(val: STRING) → STRING            | 获取条件范围内时间戳最大的一条数据（可以是空值 NULL）。   |
| last_row(val: timestamp) → timestamp      | 获取条件范围内时间戳最大的一条数据（可以是空值 NULL）。   |
| last_row(val: timestamptz) → timestamptz  | 获取条件范围内时间戳最大的一条数据（可以是空值 NULL）。   |
| last_row(val: varbytes) →varbytes         | 获取条件范围内时间戳最大的一条数据（可以是空值 NULL）。   |
| last_row(*) →any element                  | 获取条件范围内时间戳最大的一条数据（可以是空值 NULL）。   |
| max(arg1: float4) → float4                | 标识选定的最大值。                                        |
| max(arg1:  float8) →  float8              | 标识选定的最大值。                                        |
| max(arg1: INT2) → INT2                    | 标识选定的最大值。                                        |
| max(arg1: INT4) → INT4                    | 标识选定的最大值。                                        |
| max(arg1: INT8) → INT8                    | 标识选定的最大值。                                        |
| max(arg1: STRING) → STRING                | 标识选定的最大值。                                        |
| max(arg1: timestamp) → timestamp          | 标识选定的最大值。                                        |
| max(arg1: timestamptz) → timestamptz      | 标识选定的最大值。                                        |
| min(arg1: float4) → float4                | 标识选定的最小值。                                        |
| min(arg1:  float8) →  float8              | 标识选定的最小值。                                        |
| min(arg1: INT2) → INT2                    | 标识选定的最小值。                                        |
| min(arg1: INT4) → INT4                    | 标识选定的最小值。                                        |
| min(arg1: INT8) → INT8                    | 标识选定的最小值。                                        |
| min(arg1: STRING) → STRING                | 标识选定的最小值。                                        |
| min(arg1: timestamp) → timestamp          | 标识选定的最小值。                                        |
| min(arg1: timestamptz) → timestamptz      | 标识选定的最小值。                                        |
| sum(arg1: float4) → float8                | 计算选定值的总和。                                        |
| sum(arg1:  float8) → float8               | 计算选定值的总和。                                        |
| sum(arg1: INT2) → DECIMAL                 | 计算选定值的总和。                                        |
| sum(arg1: INT4) → DECIMAL                 | 计算选定值的总和。                                        |
| sum(arg1: INT8) → DECIMAL                 | 计算选定值的总和。                                        |

## 地理函数

| 函数 → 返回值                                            | 描述                                        |
| --------------------------------------------------------- | ------------------------------------------- |
| ST_Distance (a: geometry, b: geometry) → float8          | 计算 a、b 两个⼏何对象之间的欧⽒距离。      |
| ST_DWithin (a: geometry, b: geometry, d: float8)  → bool | 检查 a、b 两个⼏何对象是否在给定距离（d）内。|
| ST_Contains (a: geometry, b: geometry) → bool            | 检查⼏何对象 a 是否完全包含⼏何对象 b。     |
| ST_Intersects (a: geometry, b: geometry) → bool          | 检查 a、b 两个⼏何对象是否相交或重叠。      |
| ST_Equals (a: geometry, b: geometry) → bool              | 比较 a、b 两个⼏何对象是否完全相同。        |
| ST_Touches (a: geometry, b: geometry) →  bool            | 检查 a、b 两个⼏何对象是否相邻。            |
| ST_Covers (a: geometry, b: geometry) → bool              | 检查⼏何对象 a 是否完全覆盖⼏何对象 b。     |
| ST_Area (a：geometry) → float8                           | 计算⼀个多边形的面积                        |
