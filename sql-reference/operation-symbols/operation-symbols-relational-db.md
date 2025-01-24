---
title: 关系数据操作符
id: operation-symbols-relational-db
---

# 关系数据操作符

数据库操作符用于执行特定操作的符号或关键字。


## 优先级

下表按照从最高优先级到最低优先级的顺序列出了 KWDB 支持的所有运算符。具有相同优先级的运算符是左关联的，这意味着这些运算符从左侧开始向右移动。

| 优先级 | 操作符                                              | 名称                                                                                                         | 操作符数目 |
| ------------------------------------ | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| 1                                    | .                                                   | 成员字段访问运算符                                                                                                                          | 双目                                      |
| 2                                    | ::                                                  | 类型转换                                                                                                                                    | 双目                                      |
| 3                                    | -                                                   | 取反                                                                                                                                        | 单目（前缀）                              |
| 3                                    | ~                                                   | 按位取反                                                                                                                                    | 单目（前缀）                              |
| 4                                    | ^                                                   | 求幂                                                                                                                                        | 双目                                      |
| 5                                    | \*                                                  | 乘                                                                                                                                          | 双目                                      |
| 5                                    | /                                                   | 除                                                                                                                                          | 双目                                      |
| 5                                    | //                                                  | 除（结果向下取整，3/2=1）                                                                                                                   | 双目                                      |
| 5                                    | %                                                   | 求余                                                                                                                                        | 双目                                      |
| 6                                    | +                                                   | 加                                                                                                                                          | 双目                                      |
| 6                                    | -                                                   | 减                                                                                                                                          | 双目                                      |
| 7                                    | <<                                                  | 按位左移                                                                                                                                    | 双目                                      |
| 7                                    | >>                                                  | 按位右移                                                                                                                                    | 双目                                      |
| 8                                    | &                                                   | 按位与                                                                                                                                      | 双目                                      |
| 9                                    | #                                                   | 按位异或                                                                                                                                    | 双目                                      |
| 10                                   | &#124;                                              | 按位或                                                                                                                                      | 双目                                      |
| 11                                   | &#124;&#124;                                        | 字符串拼接                                                                                                                                  | 双目                                      |
| 11                                   | < ANY，SOME，ALL                                    | 多值比较：小于                                                                                                                           | 双目                                      |
| 11                                   | > ANY，SOME，ALL                                    | 多值比较：大于                                                                                                                            | 双目                                      |
| 11                                   | = ANY，SOME，ALL                                    | 多值比较：等于                                                                                                                           | 双目                                      |
| 11                                   | <= ANY，SOME，ALL                                   | 多值比较：小于或等于                                                                                                                     | 双目                                      |
| 11                                   | >= ANY，SOME，ALL                                   | 多值比较：大于或等于                                                                                                                     | 双目                                      |
| 11                                   | <> ANY / != ANY，<> SOME / != SOME，<> ALL / != ALL | 多值比较：不等于                                                                                                                         | 双目                                      |
| 11                                   | [NOT] LIKE ANY，[NOT] LIKE SOME, [NOT] LIKE ALL     | 多值比较：LIKE                                                                                                                             | 双目                                      |
| 11                                   | [NOT] ILIKE ANY，[NOT] ILIKE SOME，[NOT] ILIKE ALL  | 多值比较：ILIKE                                                                                                                            | 双目                                      |
| 12                                   | [NOT] BETWEEN                                       | 值不在指定范围                                                                                                                              | 双目                                      |
|                                      | [NOT] BETWEEN SYMMETRIC                             | 类似于 `[NOT] BETWEEN`，但未排序。例如，`a BETWEEN b AND c` 指的是 `b <= a <= c`，`a BETWEEN SYMMETRIC b AND c` 指的是 `(b <= a <= c) OR (c <= a <= b)` | 双目                                      |
| 12                                   | [NOT] IN                                            | 值不在指定的集合中                                                                                                                          | 双目                                      |
| 12                                   | [NOT] LIKE                                          | 匹配[或不匹配] `LIKE` 表达式，区分大小写                                                                                                      | 双目                                      |
| 12                                   | [NOT] ILIKE                                         | 匹配[或不匹配] `LIKE` 表达式，不区分大小写                                                                                                    | 双目                                      |
| 12                                   | [NOT] SIMILAR                                       | 匹配[或不匹配] `SIMILAR TO` 正则表达式                                                                                                        | 双目                                      |
| 12                                   | ~                                                   | 匹配正则表达式，区分大小写                                                                                                                  | 双目                                      |
| 12                                   | !~                                                  | 与正则表达式不匹配，区分大小写                                                                                                              | 双目                                      |
| 12                                   | ~\*                                                 | 匹配正则表达式，不区分大小写                                                                                                                | 双目                                      |
| 12                                   | !~\*                                                | 与正则表达式不匹配，不区分大小写                                                                                                            | 双目                                      |
| 13                                   | =                                                   | 等于                                                                                                                                        | 双目                                      |
| 13                                   | <                                                   | 小于                                                                                                                                        | 双目                                      |
| 13                                   | >                                                   | 大于                                                                                                                                        | 双目                                      |
| 13                                   | <=                                                  | 小于或等于                                                                                                                                  | 双目                                      |
| 13                                   | >=                                                  | 大于或等于                                                                                                                                  | 双目                                      |
| 13                                   | !=，<>                                              | 不等于                                                                                                                                      | 双目                                      |
| 14                                   | IS [DISTINCT FROM]                                  | 等于，考虑 NULL 值                                                                                                                          | 双目                                      |
| 14                                   | IS NOT [DISTINCT FROM]                              | 不等于，`a IS NOT b` 相当于 `NOT(a IS b)`                                                                                                    | 双目                                      |
| 14                                   | ISNULL，IS UNKNOWN , NOTNULL, IS NOT UNKNOWN        | 等价于 `IS NULL` 或 `IS NOT NULL`                                                                                                                  | 单目（后缀）                              |
| 14                                   | IS NAN, IS NOT NAN                                  | 与浮点 NAN 值的比较                                                                                                                         | 单目（后缀）                              |
| 14                                   | IS OF(...)                                          | 类型谓词（是不是某种类型）                                                                                                                  | 单目（后缀）                              |
| 15                                   | NOT                                                 | 逻辑非                                                                                                                                      | 单目                                      |
| 16                                   | AND                                                 | 逻辑与                                                                                                                                      | 双目                                      |
| 17                                   | OR                                                  | 逻辑或                                                                                                                                      | 双目                                      |

## 支持的操作符

| 操作符 | 表达式                           | 返回值      |
| ------ | -------------------------------- | ----------- |
| #      | int2 # int2                      | int8        |
| #      | int2 # int4                      | int8        |
| #      | int2 # int8                      | int8        |
| #      | int4 # int2                      | int8        |
| #      | int4 # int4                      | int8        |
| #      | int4 # int8                      | int8        |
| #      | int8 # int2                      | int8        |
| #      | int8 # int4                      | int8        |
| #      | int8 # int8                      | int8        |
| #      | varbit # varbit                  | varbit      |
| #>     | jsonb #> STRING[]                | jsonb       |
| #>>    | jsonb #>> STRING[]               | STRING      |
| %      | decimal % decimal                | decimal     |
| %      | decimal % INT2                   | decimal     |
| %      | decimal % INT4                   | decimal     |
| %      | decimal % INT8                   | decimal     |
| %      | float4 % float4                  | float8      |
| %      | float4 % float8                  | float8      |
| %      | float8 % float4                  | float8      |
| %      | float8 % float8                  | float8      |
| %      | INT2 % decimal                   | decimal     |
| %      | INT4 % decimal                   | decimal     |
| %      | INT8 % decimal                   | decimal     |
| %      | int2 % int2                      | int8        |
| %      | int2 % int4                      | int8        |
| %      | int2 % int8                      | int8        |
| %      | int4 % int2                      | int8        |
| %      | int4 % int4                      | int8        |
| %      | int4 % int8                      | int8        |
| %      | int8 % int2                      | int8        |
| %      | int8 % int4                      | int8        |
| %      | int8 % int8                      | int8        |
| &      | INET & INET                      | INET        |
| &      | int2 & int2                      | int8        |
| &      | int2 & int4                      | int8        |
| &      | int2 & int8                      | int8        |
| &      | int4 & int2                      | int8        |
| &      | int4 & int4                      | int8        |
| &      | int4 & int8                      | int8        |
| &      | int8 & int2                      | int8        |
| &      | int8 & int4                      | int8        |
| &      | int8 & int8                      | int8        |
| &      | varbit & varbit                  | varbit      |
| &&     | anyelement && anyelement         | BOOL        |
| &&     | INET && INET                     | BOOL        |
| *      | decimal * decimal                | decimal     |
| *      | decimal * INT2                   | decimal     |
| *      | decimal * INT4                   | decimal     |
| *      | decimal * INT8                   | decimal     |
| *      | decimal * interval               | interval    |
| *      | float4 * float4                  | float8      |
| *      | float4 * float8                  | float8      |
| *      | float8 * float4                  | float8      |
| *      | float8 * float8                  | float8      |
| *      | FLOAT4 * interval                | interval    |
| *      | FLOAT8 * interval                | interval    |
| *      | INT2 * decimal                   | decimal     |
| *      | INT4 * decimal                   | decimal     |
| *      | INT8 * decimal                   | decimal     |
| *      | int2 * int2                      | int8        |
| *      | int2 * int4                      | int8        |
| *      | int2 * int8                      | int8        |
| *      | int4 * int2                      | int8        |
| *      | int4 * int4                      | int8        |
| *      | int4 * int8                      | int8        |
| *      | int8 * int2                      | int8        |
| *      | int8 * int4                      | int8        |
| *      | int8 * int8                      | int8        |
| *      | INT2 * interval                  | interval    |
| *      | INT4 * interval                  | interval    |
| *      | INT8 * interval                  | interval    |
| *      | interval * decimal               | interval    |
| *      | interval * FLOAT4                | interval    |
| *      | interval * FLOAT8                | interval    |
| *      | interval * INT2                  | interval    |
| *      | interval * INT4                  | interval    |
| *      | interval * INT8                  | interval    |
| +      | date + INT2                      | date        |
| +      | date + INT4                      | date        |
| +      | date + INT8                      | date        |
| +      | date + interval                  | timestamptz |
| +      | date + time                      | timestamp   |
| +      | decimal + decimal                | decimal     |
| +      | decimal + INT2                   | decimal     |
| +      | decimal + INT4                   | decimal     |
| +      | decimal + INT8                   | decimal     |
| +      | float4 + float4                  | float8      |
| +      | float4 + float8                  | float8      |
| +      | float8 + float4                  | float8      |
| +      | float8 + float8                  | float8      |
| +      | INET + INT2                      | INET        |
| +      | INET + INT4                      | INET        |
| +      | INET + INT8                      | INET        |
| +      | INT2 + date                      | date        |
| +      | INT4 + date                      | date        |
| +      | INT8 + date                      | date        |
| +      | INT2 + decimal                   | decimal     |
| +      | INT4 + decimal                   | decimal     |
| +      | INT8 + decimal                   | decimal     |
| +      | INT2 + INET                      | INET        |
| +      | INT4 + INET                      | INET        |
| +      | INT8 + INET                      | INET        |
| +      | int2 + int2                      | int8        |
| +      | int2 + int4                      | int8        |
| +      | int2 + int8                      | int8        |
| +      | int4 + int2                      | int8        |
| +      | int4 + int4                      | int8        |
| +      | int4 + int8                      | int8        |
| +      | int8 + int2                      | int8        |
| +      | int8 + int4                      | int8        |
| +      | int8 + int8                      | int8        |
| +      | interval + date                  | timestamptz |
| +      | interval + interval              | interval    |
| +      | interval + time                  | time        |
| +      | interval + timestamp             | timestamp   |
| +      | interval + timestamptz           | timestamptz |
| +      | time + date                      | timestamp   |
| +      | time + interval                  | time        |
| +      | timestamp + interval             | timestamp   |
| +      | timestamptz + interval           | timestamptz |
| +      | timetz + date                    | timestamptz |
| +      | timetz + interval                | timetz      |
| -      | -decimal                         | decimal     |
| -      | -float4                          | float8      |
| -      | -float8                          | float8      |
| -      | -int2                            | int8        |
| -      | -int4                            | int8        |
| -      | -int8                            | int8        |
| -      | -interval                        | interval    |
| -      | date - date                      | INT8        |
| -      | date - INT2                      | date        |
| -      | date - INT4                      | date        |
| -      | date - INT8                      | date        |
| -      | date - interval                  | timestamptz |
| -      | date - time                      | timestamp   |
| -      | decimal - decimal                | decimal     |
| -      | decimal - INT2                   | decimal     |
| -      | decimal - INT4                   | decimal     |
| -      | decimal - INT8                   | decimal     |
| -      | float4 - float4                  | float8      |
| -      | float4 - float8                  | float8      |
| -      | float8 - float4                  | float8      |
| -      | float8 - float8                  | float8      |
| -      | INET - INET                      | INT8        |
| -      | INET - INT2                      | INET        |
| -      | INET - INT4                      | INET        |
| -      | INET - INT8                      | INET        |
| -      | INT2 - decimal                   | decimal     |
| -      | INT4 - decimal                   | decimal     |
| -      | INT8 - decimal                   | decimal     |
| -      | int2 - int2                      | int8        |
| -      | int2 - int4                      | int8        |
| -      | int2 - int8                      | int8        |
| -      | int4 - int2                      | int8        |
| -      | int4 - int4                      | int8        |
| -      | int4 - int8                      | int8        |
| -      | int8 - int2                      | int8        |
| -      | int8 - int4                      | int8        |
|        | int8 - int8                      | int8        |
| -      | interval - interval              | interval    |
| -      | jsonb - INT2                     | jsonb       |
| -      | jsonb - INT4                     | jsonb       |
| -      | jsonb - INT8                     | jsonb       |
| -      | jsonb - STRING                   | jsonb       |
| -      | jsonb - STRING[]                 | jsonb       |
| -      | time - interval                  | time        |
| -      | time - time                      | interval    |
| -      | timestamp - interval             | timestamp   |
| -      | timestamp - timestamp            | interval    |
| -      | timestamp - timestamptz          | interval    |
| -      | timestamptz - interval           | timestamptz |
| -      | timestamptz - timestamp          | interval    |
| -      | timestamptz - timestamptz        | interval    |
| -      | timetz - interval                | timetz      |
| ->     | jsonb -> INT2                    | jsonb       |
| ->     | jsonb -> INT4                    | jsonb       |
| ->     | jsonb -> INT8                    | jsonb       |
| ->     | jsonb -> STRING                  | jsonb       |
| ->>    | jsonb ->> INT2                   | STRING      |
| ->>    | jsonb ->> INT4                   | STRING      |
| ->>    | jsonb ->> INT8                   | STRING      |
| ->>    | jsonb ->> STRING                 | STRING      |
| /      | decimal / decimal                | decimal     |
| /      | decimal / INT2                   | decimal     |
| /      | decimal / INT4                   | decimal     |
| /      | decimal / INT8                   | decimal     |
| /      | FLOAT4 / FLOAT4                  | FLOAT8      |
| /      | FLOAT4 / FLOAT8                  | FLOAT8      |
| /      | FLOAT8 / FLOAT4                  | FLOAT8      |
| /      | FLOAT8 / FLOAT8                  | FLOAT8      |
| /      | INT2 / decimal                   | decimal     |
| /      | INT4 / decimal                   | decimal     |
| /      | INT8 / decimal                   | decimal     |
| /      | INT2 / INT2                      | decimal     |
| /      | INT2 / INT4                      | decimal     |
| /      | INT2 / INT8                      | decimal     |
| /      | INT4 / INT2                      | decimal     |
| /      | INT4 / INT4                      | decimal     |
| /      | INT4 / INT8                      | decimal     |
| /      | INT8 / INT2                      | decimal     |
| /      | INT8 / INT4                      | decimal     |
| /      | INT8 / INT8                      | decimal     |
| /      | interval / FLOAT4                | interval    |
| /      | interval / FLOAT8                | interval    |
| /      | interval / INT2                  | interval    |
| /      | interval / INT4                  | interval    |
| /      | interval / INT8                  | interval    |
| //     | decimal // decimal               | decimal     |
| //     | decimal // INT2                  | decimal     |
| //     | decimal // INT4                  | decimal     |
| //     | decimal // INT8                  | decimal     |
| //     | FLOAT4 // FLOAT4                 | FLOAT8      |
| //     | FLOAT4 // FLOAT8                 | FLOAT8      |
| //     | FLOAT8 // FLOAT4                 | FLOAT8      |
| //     | FLOAT8 // FLOAT8                 | FLOAT8      |
| //     | INT2 // decimal                  | decimal     |
| //     | INT4 // decimal                  | decimal     |
| //     | INT8 // decimal                  | decimal     |
| //     | INT2 // INT2                     | INT8        |
| //     | INT2 // INT4                     | INT8        |
| //     | INT2 // INT8                     | INT8        |
| //     | INT4 // INT2                     | INT8        |
| //     | INT4 // INT4                     | INT8        |
| //     | INT4 // INT8                     | INT8        |
| //     | INT8 // INT2                     | INT8        |
| //     | INT8 // INT4                     | INT8        |
| //     | INT8 // INT8                     | INT8        |
| <      | BOOL < BOOL                      | BOOL        |
| <      | BOOL[] < BOOL[]                  | BOOL        |
| <      | bytes < bytes                    | BOOL        |
| <      | bytes[] < bytes[]                | BOOL        |
| <      | collatedSTRING < collatedSTRING  | BOOL        |
| <      | date < date                      | BOOL        |
| <      | date < timestamp                 | BOOL        |
| <      | date < timestamptz               | BOOL        |
| <      | decimal < decimal                | BOOL        |
| <      | decimal < FLOAT4                 | BOOL        |
| <      | decimal < FLOAT8                 | BOOL        |
| <      | decimal < INT2                   | BOOL        |
| <      | decimal < INT4                   | BOOL        |
| <      | decimal < INT8                   | BOOL        |
| <      | decimal[] < decimal[]            | BOOL        |
| <      | FLOAT4 < decimal                 | BOOL        |
| <      | FLOAT8 < decimal                 | BOOL        |
| <      | FLOAT4 < FLOAT4                  | BOOL        |
| <      | FLOAT4 < FLOAT8                  | BOOL        |
| <      | FLOAT8 < FLOAT4                  | BOOL        |
| <      | FLOAT8 < FLOAT8                  | BOOL        |
| <      | float4 < int2                    | BOOL        |
| <      | float4 < int4                    | BOOL        |
| <      | float4 < int8                    | BOOL        |
| <      | float8 < int2                    | BOOL        |
| <      | float8 < int4                    | BOOL        |
| <      | float8 < int8                    | BOOL        |
| <      | FLOAT4[] < FLOAT4[]              | BOOL        |
| <      | FLOAT4[] < FLOAT8[]              | BOOL        |
| <      | FLOAT8[] < FLOAT4[]              | BOOL        |
| <      | FLOAT8[] < FLOAT8[]              | BOOL        |
| <      | INET < INET                      | BOOL        |
| <      | INET[] < INET[]                  | BOOL        |
| <      | INT2 < decimal                   | BOOL        |
| <      | INT4 < decimal                   | BOOL        |
| <      | INT8 < decimal                   | BOOL        |
| <      | int2 < float4                    | BOOL        |
| <      | int2 < float8                    | BOOL        |
| <      | int4 < float4                    | BOOL        |
| <      | int4 < float8                    | BOOL        |
| <      | int8 < float4                    | BOOL        |
| <      | int8 < float8                    | BOOL        |
| <      | int2 < int2                      | BOOL        |
| <      | int2 < int4                      | BOOL        |
| <      | int2 < int8                      | BOOL        |
| <      | int4 < int2                      | BOOL        |
| <      | int4 < int4                      | BOOL        |
| <      | int4 < int8                      | BOOL        |
| <      | int8 < int2                      | BOOL        |
| <      | int8 < int4                      | BOOL        |
| <      | int8 < int8                      | BOOL        |
| <      | INT2[] < INT2[]                  | BOOL        |
| <      | INT2[] < INT4[]                  | BOOL        |
| <      | INT2[] < INT8[]                  | BOOL        |
| <      | INT4[] < INT2[]                  | BOOL        |
| <      | INT4[] < INT4[]                  | BOOL        |
| <      | INT4[] < INT8[]                  | BOOL        |
| <      | INT8[] < INT2[]                  | BOOL        |
| <      | INT8[] < INT4[]                  | BOOL        |
| <      | INT8[] < INT8[]                  | BOOL        |
| <      | interval < interval              | BOOL        |
| <      | interval[] < interval[]          | BOOL        |
| <      | jsonb < jsonb                    | BOOL        |
| <      | oid < oid                        | BOOL        |
| <      | STRING < STRING                  | BOOL        |
| <      | STRING[] < STRING[]              | BOOL        |
| <      | time < time                      | BOOL        |
| <      | time < timetz                    | BOOL        |
| <      | time[] < time[]                  | BOOL        |
| <      | timestamp < date                 | BOOL        |
| <      | timestamp < timestamp            | BOOL        |
| <      | timestamp < timestamptz          | BOOL        |
| <      | timestamp[] < timestamp[]        | BOOL        |
| <      | timestamptz < date               | BOOL        |
| <      | timestamptz < timestamp          | BOOL        |
| <      | timestamptz < timestamptz        | BOOL        |
| <      | timestamptz[] < timestamptz[]    | BOOL        |
| <      | timetz < time                    | BOOL        |
| <      | timetz < timetz                  | BOOL        |
| <      | tuple < tuple                    | BOOL        |
| <      | UUID < UUID                      | BOOL        |
| <      | UUID[] < UUID[]                  | BOOL        |
| <      | varbit < varbit                  | BOOL        |
| <<     | INET << INET                     | BOOL        |
| <<     | int2 <<  int2                    | int8        |
| <<     | int2 <<  int4                    | int8        |
| <<     | int2 <<  int8                    | int8        |
| <<     | int4 <<  int2                    | int8        |
| <<     | int4 <<  int4                    | int8        |
| <<     | int4 <<  int8                    | int8        |
| <<     | int8 <<  int2                    | int8        |
| <<     | int8 <<  int4                    | int8        |
| <<     | int8 <<  int8                    | int8        |
| <<     | varbit << INT2                   | varbit      |
| <<     | varbit << INT4                   | varbit      |
| <<     | varbit << INT8                   | varbit      |
| <=     | BOOL <= BOOL                     | BOOL        |
| <=     | BOOL[] <= BOOL[]                 | BOOL        |
| <=     | bytes <= bytes                   | BOOL        |
| <=     | bytes[] <= bytes[]               | BOOL        |
| <=     | collatedSTRING <= collatedSTRING | BOOL        |
| <=     | date <= date                     | BOOL        |
| <=     | date <= timestamp                | BOOL        |
| <=     | date <= timestamptz              | BOOL        |
| <=     | date[] <= date[]                 | BOOL        |
| <=     | decimal <= decimal               | BOOL        |
| <=     | decimal <= FLOAT4                | BOOL        |
| <=     | decimal <= FLOAT8                | BOOL        |
| <=     | decimal <= INT2                  | BOOL        |
| <=     | decimal <= INT4                  | BOOL        |
| <=     | decimal <= INT8                  | BOOL        |
| <=     | decimal[] <= decimal[]           | BOOL        |
| <=     | FLOAT4 <= decimal                | BOOL        |
| <=     | FLOAT8 <= decimal                | BOOL        |
| <=     | float4 <= float4                 | BOOL        |
| <=     | float4 <= float8                 | BOOL        |
| <=     | float8 <= float4                 | BOOL        |
| <=     | float8 <= float8                 | BOOL        |
| <=     | float4 <= int2                   | BOOL        |
| <=     | float4 <= int4                   | BOOL        |
| <=     | float4 <= int8                   | BOOL        |
| <=     | float8 <= int2                   | BOOL        |
| <=     | float8 <= int4                   | BOOL        |
| <=     | float8 <= int8                   | BOOL        |
| <=     | FLOAT4[] <= FLOAT4[]             | BOOL        |
| <=     | FLOAT4[] <= FLOAT8[]             | BOOL        |
| <=     | FLOAT8[] <= FLOAT4[]             | BOOL        |
| <=     | FLOAT8[] <= FLOAT8[]             | BOOL        |
| <=     | INET <= INET                     | BOOL        |
| <=     | INET[] <= INET[]                 | BOOL        |
| <=     | INT2 <= decimal                  | BOOL        |
| <=     | INT4 <= decimal                  | BOOL        |
| <=     | INT8 <= decimal                  | BOOL        |
| <=     | int2 <= float4                   | BOOL        |
| <=     | int2 <= float8                   | BOOL        |
| <=     | int4 <= float4                   | BOOL        |
| <=     | int4 <= float8                   | BOOL        |
| <=     | int8 <= float4                   | BOOL        |
| <=     | int8 <= float8                   | BOOL        |
| <=     | int2 <= int2                     | BOOL        |
| <=     | int2 <= int4                     | BOOL        |
| <=     | int2 <= int8                     | BOOL        |
| <=     | int4 <= int2                     | BOOL        |
| <=     | int4 <= int4                     | BOOL        |
| <=     | int4 <= int8                     | BOOL        |
| <=     | int8 <= int2                     | BOOL        |
| <=     | int8 <= int4                     | BOOL        |
| <=     | int8 <= int8                     | BOOL        |
| <=     | INT2[] <= INT2[]                 | BOOL        |
| <=     | INT2[] <= INT4[]                 | BOOL        |
| <=     | INT2[] <= INT8[]                 | BOOL        |
| <=     | INT4[] <= INT2[]                 | BOOL        |
| <=     | INT4[] <= INT4[]                 | BOOL        |
| <=     | INT4[] <= INT8[]                 | BOOL        |
| <=     | INT8[] <= INT2[]                 | BOOL        |
| <=     | INT8[] <= INT4[]                 | BOOL        |
| <=     | INT8[] <= INT8[]                 | BOOL        |
| <=     | interval <= interval             | BOOL        |
| <=     | interval[] <= interval[]         | BOOL        |
| <=     | jsonb <= jsonb                   | BOOL        |
| <=     | oid <= oid                       | BOOL        |
| <=     | STRING <= STRING                 | BOOL        |
| <=     | STRING[] <= STRING[]             | BOOL        |
| <=     | time <= time                     | BOOL        |
| <=     | time <= timetz                   | BOOL        |
| <=     | time[] <= time[]                 | BOOL        |
| <=     | timestamp <= date                | BOOL        |
| <=     | timestamp <= timestamp           | BOOL        |
| <=     | timestamp <= timestamptz         | BOOL        |
| <=     | timestamp[] <= timestamp[]       | BOOL        |
| <=     | timestamptz <= date              | BOOL        |
| <=     | timestamptz <= timestamp         | BOOL        |
| <=     | timestamptz <= timestamptz       | BOOL        |
| <=     | timestamptz[] <= timestamptz[]   | BOOL        |
| <=     | timetz <= time                   | BOOL        |
| <=     | timetz <= timetz                 | BOOL        |
| <=     | tuple <= tuple                   | BOOL        |
| <=     | UUID <= UUID                     | BOOL        |
| <=     | UUID[] <= UUID[]                 | BOOL        |
| <=     | varbit <= varbit                 | BOOL        |
| <@     | anyelement <@ anyelement         | BOOL        |
| <@     | jsonb <@ jsonb                   | BOOL        |
| =      | BOOL = BOOL                      | BOOL        |
| =      | BOOL[] = BOOL[]                  | BOOL        |
| =      | bytes = bytes                    | BOOL        |
| =      | bytes[] = bytes[]                | BOOL        |
| =      | collatedSTRING = collatedSTRING  | BOOL        |
| =      | date = date                      | BOOL        |
| =      | date = timestamp                 | BOOL        |
| =      | date = timestamptz               | BOOL        |
| =      | date[] = date[]                  | BOOL        |
| =      | decimal = decimal                | BOOL        |
| =      | decimal = FLOAT4                 | BOOL        |
| =      | decimal = FLOAT8                 | BOOL        |
| =      | decimal = INT2                   | BOOL        |
| =      | decimal = INT4                   | BOOL        |
| =      | decimal = INT8                   | BOOL        |
| =      | decimal[] = decimal[]            | BOOL        |
| =      | FLOAT4 = decimal                 | BOOL        |
| =      | FLOAT8 = decimal                 | BOOL        |
| =      | float4 = float4                  | BOOL        |
| =      | float4 = float8                  | BOOL        |
| =      | float8 = float4                  | BOOL        |
| =      | float8 = float8                  | BOOL        |
| =      | float4 = int2                    | BOOL        |
| =      | float4 = int4                    | BOOL        |
| =      | float4 = int8                    | BOOL        |
| =      | float8 = int2                    | BOOL        |
| =      | float8 = int4                    | BOOL        |
| =      | float8 = int8                    | BOOL        |
| =      | FLOAT4[] = FLOAT4[]              | BOOL        |
| =      | FLOAT4[] = FLOAT8[]              | BOOL        |
| =      | FLOAT8[] = FLOAT4[]              | BOOL        |
| =      | FLOAT8[] = FLOAT8[]              | BOOL        |
| =      | INET = INET                      | BOOL        |
| =      | INET[] = INET[]                  | BOOL        |
| =      | INT2 = decimal                   | BOOL        |
| =      | INT4 = decimal                   | BOOL        |
| =      | INT8 = decimal                   | BOOL        |
| =      | int2 = float4                    | BOOL        |
| =      | int2 = float8                    | BOOL        |
| =      | int4 = float4                    | BOOL        |
| =      | int4 = float8                    | BOOL        |
| =      | int8 = float4                    | BOOL        |
| =      | int8 = float8                    | BOOL        |
| =      | int2 = int2                      | BOOL        |
| =      | int2 = int4                      | BOOL        |
| =      | int2 = int8                      | BOOL        |
| =      | Int4 = int2                      | BOOL        |
| =      | int4 = int4                      | BOOL        |
| =      | int4 = int8                      | BOOL        |
| =      | int8 = int2                      | BOOL        |
| =      | int8 = int4                      | BOOL        |
| =      | int8 = int8                      | BOOL        |
| =      | INT2[] = INT2[]                  | BOOL        |
| =      | INT2[] = INT4[]                  | BOOL        |
| =      | INT2[] = INT8[]                  | BOOL        |
| =      | INT4[] = INT2[]                  | BOOL        |
| =      | INT4[] = INT4[]                  | BOOL        |
| =      | INT4[] = INT8[]                  | BOOL        |
| =      | INT8[] = INT2[]                  | BOOL        |
| =      | INT8[] = INT4[]                  | BOOL        |
| =      | INT8[] = INT8[]                  | BOOL        |
| =      | interval = interval              | BOOL        |
| =      | interval[] = interval[]          | BOOL        |
| =      | jsonb = jsonb                    | BOOL        |
| =      | oid = oid                        | BOOL        |
| =      | STRING = STRING                  | BOOL        |
| =      | STRING[] = STRING[]              | BOOL        |
| =      | time = time                      | BOOL        |
| =      | time = timetz                    | BOOL        |
| =      | time[] = time[]                  | BOOL        |
| =      | timestamp = date                 | BOOL        |
| =      | timestamp = timestamp            | BOOL        |
| =      | timestamp = timestamptz          | BOOL        |
| =      | timestamp[] = timestamp[]        | BOOL        |
| =      | timestamptz = date               | BOOL        |
| =      | timestamptz = timestamp          | BOOL        |
| =      | timestamptz = timestamptz        | BOOL        |
| =      | timestamptz[] = timestamptz[]    | BOOL        |
| =      | timetz = time                    | BOOL        |
| =      | timetz = timetz                  | BOOL        |
| =      | tuple = tuple                    | BOOL        |
| =      | UUID = UUID                      | BOOL        |
| =      | UUID[] = UUID[]                  | BOOL        |
| =      | varbit = varbit                  | BOOL        |
| >>     | INET >> INET                     | BOOL        |
| >>     | int2 >> int2                     | int8        |
| >>     | int2 >> int4                     | int8        |
| >>     | int2 >> int8                     | int8        |
| >>     | int4 >> int2                     | int8        |
| >>     | int4 >> int4                     | int8        |
| >>     | int4 >> int8                     | int8        |
| >>     | int8 >> int2                     | int8        |
| >>     | int8 >> int4                     | int8        |
| >>     | int8 >> int8                     | int8        |
| >>     | varbit >> INT2                   | varbit      |
| >>     | varbit >> INT4                   | varbit      |
| >>     | varbit >> INT8                   | varbit      |
| ?      | jsonb ? STRING                   | BOOL        |
| ?&     | jsonb ?& STRING[]                | BOOL        |
| ?&#124;      |  jsonb ?&#124; STRING[]                                | BOOL     |
| @>     | anyelement @> anyelement         | BOOL        |
| @>     | jsonb @> jsonb                   | BOOL        |
| ILIKE                | STRING ILIKE STRING                                | BOOL        |
| IN                   | BOOL IN tuple                                      | BOOL        |
| IN                   | bytes IN tuple                                     | BOOL        |
| IN                   | collatedSTRING IN tuple                            | BOOL        |
| IN                   | date IN tuple                                      | BOOL        |
| IN                   | decimal IN tuple                                   | BOOL        |
| IN                   | FLOAT4 IN tuple                                    | BOOL        |
| IN                   | FLOAT8 IN tuple                                    | BOOL        |
| IN                   | INET IN tuple                                      | BOOL        |
| IN                   | INT2 IN tuple                                      | BOOL        |
| IN                   | INT4 IN tuple                                      | BOOL        |
| IN                   | INT8 IN tuple                                      | BOOL        |
| IN                   | interval IN tuple                                  | BOOL        |
| IN                   | jsonb IN tuple                                     | BOOL        |
| IN                   | oid IN tuple                                       | BOOL        |
| IN                   | STRING IN tuple                                    | BOOL        |
| IN                   | time IN tuple                                      | BOOL        |
| IN                   | timestamp IN tuple                                 | BOOL        |
| IN                   | timestamptz IN tuple                               | BOOL        |
| IN                   | tuple IN tuple                                     | BOOL        |
| IN                   | UUID IN tuple                                      | BOOL        |
| IN                   | varbit IN tuple                                    | BOOL        |
| IS NOT DISTINCT FROM | BOOL IS NOT DISTINCT FROM BOOL                     | BOOL        |
| IS NOT DISTINCT FROM | BOOL[] IS NOT DISTINCT FROM BOOL[]                 | BOOL        |
| IS NOT DISTINCT FROM | bytes IS NOT DISTINCT FROM bytes                   | BOOL        |
| IS NOT DISTINCT FROM | bytes[] IS NOT DISTINCT FROM bytes[]               | BOOL        |
| IS NOT DISTINCT FROM | collatedSTRING IS NOT DISTINCT FROM collatedSTRING | BOOL        |
| IS NOT DISTINCT FROM | date IS NOT DISTINCT FROM date                     | BOOL        |
| IS NOT DISTINCT FROM | date IS NOT DISTINCT FROM timestamp                | BOOL        |
| IS NOT DISTINCT FROM | date IS NOT DISTINCT FROM timestamptz              | BOOL        |
| IS NOT DISTINCT FROM | date[] IS NOT DISTINCT FROM date[]                 | BOOL        |
| IS NOT DISTINCT FROM | decimal IS NOT DISTINCT FROM decimal               | BOOL        |
| IS NOT DISTINCT FROM | decimal IS NOT DISTINCT FROM FLOAT4                | BOOL        |
| IS NOT DISTINCT FROM | decimal IS NOT DISTINCT FROM FLOAT8                | BOOL        |
| IS NOT DISTINCT FROM | decimal IS NOT DISTINCT FROM INT2                  | BOOL        |
| IS NOT DISTINCT FROM | decimal IS NOT DISTINCT FROM INT4                  | BOOL        |
| IS NOT DISTINCT FROM | decimal IS NOT DISTINCT FROM INT8                  | BOOL        |
| IS NOT DISTINCT FROM | decimal[] IS NOT DISTINCT FROM decimal[]           | BOOL        |
| IS NOT DISTINCT FROM | FLOAT4 IS NOT DISTINCT FROM decimal                | BOOL        |
| IS NOT DISTINCT FROM | FLOAT8 IS NOT DISTINCT FROM decimal                | BOOL        |
| IS NOT DISTINCT FROM | FLOAT4 IS NOT DISTINCT FROM FLOAT4                 | BOOL        |
| IS NOT DISTINCT FROM | FLOAT4 IS NOT DISTINCT FROM FLOAT8                 | BOOL        |
| IS NOT DISTINCT FROM | FLOAT8 IS NOT DISTINCT FROM FLOAT4                 | BOOL        |
| IS NOT DISTINCT FROM | FLOAT8 IS NOT DISTINCT FROM FLOAT8                 | BOOL        |
| IS NOT DISTINCT FROM | FLOAT4 IS NOT DISTINCT FROM INT2                   | BOOL        |
| IS NOT DISTINCT FROM | FLOAT4 IS NOT DISTINCT FROM INT4                   | BOOL        |
| IS NOT DISTINCT FROM | FLOAT4 IS NOT DISTINCT FROM INT8                   | BOOL        |
| IS NOT DISTINCT FROM | FLOAT8 IS NOT DISTINCT FROM INT2                   | BOOL        |
| IS NOT DISTINCT FROM | FLOAT8 IS NOT DISTINCT FROM INT4                   | BOOL        |
| IS NOT DISTINCT FROM | FLOAT8 IS NOT DISTINCT FROM INT8                   | BOOL        |
| IS NOT DISTINCT FROM | FLOAT4[] IS NOT DISTINCT FROM FLOAT4[]             | BOOL        |
| IS NOT DISTINCT FROM | FLOAT4[] IS NOT DISTINCT FROM FLOAT8[]             | BOOL        |
| IS NOT DISTINCT FROM | FLOAT8[] IS NOT DISTINCT FROM FLOAT4[]             | BOOL        |
| IS NOT DISTINCT FROM | FLOAT8[] IS NOT DISTINCT FROM FLOAT8[]             | BOOL        |
| IS NOT DISTINCT FROM | INET IS NOT DISTINCT FROM INET                     | BOOL        |
| IS NOT DISTINCT FROM | INET[] IS NOT DISTINCT FROM INET[]                 | BOOL        |
| IS NOT DISTINCT FROM | INT2 IS NOT DISTINCT FROM decimal                  | BOOL        |
| IS NOT DISTINCT FROM | INT4 IS NOT DISTINCT FROM decimal                  | BOOL        |
| IS NOT DISTINCT FROM | INT8 IS NOT DISTINCT FROM decimal                  | BOOL        |
| IS NOT DISTINCT FROM | INT2 IS NOT DISTINCT FROM FLOAT4                   | BOOL        |
| IS NOT DISTINCT FROM | INT2 IS NOT DISTINCT FROM FLOAT8                   | BOOL        |
| IS NOT DISTINCT FROM | INT4 IS NOT DISTINCT FROM FLOAT4                   | BOOL        |
| IS NOT DISTINCT FROM | INT4 IS NOT DISTINCT FROM FLOAT8                   | BOOL        |
| IS NOT DISTINCT FROM | INT8 IS NOT DISTINCT FROM FLOAT4                   | BOOL        |
| IS NOT DISTINCT FROM | INT8 IS NOT DISTINCT FROM FLOAT8                   | BOOL        |
| IS NOT DISTINCT FROM | INT2 IS NOT DISTINCT FROM INT2                     | BOOL        |
| IS NOT DISTINCT FROM | INT2 IS NOT DISTINCT FROM INT4                     | BOOL        |
| IS NOT DISTINCT FROM | INT2 IS NOT DISTINCT FROM INT8                     | BOOL        |
| IS NOT DISTINCT FROM | INT4 IS NOT DISTINCT FROM INT2                     | BOOL        |
| IS NOT DISTINCT FROM | INT4 IS NOT DISTINCT FROM INT4                     | BOOL        |
| IS NOT DISTINCT FROM | INT4 IS NOT DISTINCT FROM INT8                     | BOOL        |
| IS NOT DISTINCT FROM | INT8 IS NOT DISTINCT FROM INT2                     | BOOL        |
| IS NOT DISTINCT FROM | INT8 IS NOT DISTINCT FROM INT4                     | BOOL        |
| IS NOT DISTINCT FROM | INT8 IS NOT DISTINCT FROM INT8                     | BOOL        |
| IS NOT DISTINCT FROM | INT2[] IS NOT DISTINCT FROM INT2[]                 | BOOL        |
| IS NOT DISTINCT FROM | INT2[] IS NOT DISTINCT FROM INT4[]                 | BOOL        |
| IS NOT DISTINCT FROM | INT2[] IS NOT DISTINCT FROM INT8[]                 | BOOL        |
| IS NOT DISTINCT FROM | INT4[] IS NOT DISTINCT FROM INT2[]                 | BOOL        |
| IS NOT DISTINCT FROM | INT4[] IS NOT DISTINCT FROM INT4[]                 | BOOL        |
| IS NOT DISTINCT FROM | INT4[] IS NOT DISTINCT FROM INT8[]                 | BOOL        |
| IS NOT DISTINCT FROM | INT8[] IS NOT DISTINCT FROM INT2[]                 | BOOL        |
| IS NOT DISTINCT FROM | INT8[] IS NOT DISTINCT FROM INT4[]                 | BOOL        |
| IS NOT DISTINCT FROM | INT8[] IS NOT DISTINCT FROM INT8[]                 | BOOL        |
| IS NOT DISTINCT FROM | interval IS NOT DISTINCT FROM interval             | BOOL        |
| IS NOT DISTINCT FROM | interval[] IS NOT DISTINCT FROM interval[]         | BOOL        |
| IS NOT DISTINCT FROM | jsonb IS NOT DISTINCT FROM jsonb                   | BOOL        |
| IS NOT DISTINCT FROM | oid IS NOT DISTINCT FROM oid                       | BOOL        |
| IS NOT DISTINCT FROM | STRING IS NOT DISTINCT FROM STRING                 | BOOL        |
| IS NOT DISTINCT FROM | STRING[] IS NOT DISTINCT FROM STRING[]             | BOOL        |
| IS NOT DISTINCT FROM | time IS NOT DISTINCT FROM time                     | BOOL        |
| IS NOT DISTINCT FROM | time IS NOT DISTINCT FROM timetz                   | BOOL        |
| IS NOT DISTINCT FROM | time[] IS NOT DISTINCT FROM time[]                 | BOOL        |
| IS NOT DISTINCT FROM | timestamp IS NOT DISTINCT FROM date                | BOOL        |
| IS NOT DISTINCT FROM | timestamp IS NOT DISTINCT FROM timestamp           | BOOL        |
| IS NOT DISTINCT FROM | timestamp IS NOT DISTINCT FROM timestamptz         | BOOL        |
| IS NOT DISTINCT FROM | timestamp[] IS NOT DISTINCT FROM timestamp[]       | BOOL        |
| IS NOT DISTINCT FROM | timestamptz IS NOT DISTINCT FROM date              | BOOL        |
| IS NOT DISTINCT FROM | timestamptz IS NOT DISTINCT FROM timestamp         | BOOL        |
| IS NOT DISTINCT FROM | timestamptz IS NOT DISTINCT FROM timestamptz       | BOOL        |
| IS NOT DISTINCT FROM | timetz IS NOT DISTINCT FROM time                   | BOOL        |
| IS NOT DISTINCT FROM | timetz IS NOT DISTINCT FROM timetz                 | BOOL        |
| IS NOT DISTINCT FROM | tuple IS NOT DISTINCT FROM tuple                   | BOOL        |
| IS NOT DISTINCT FROM | unknown IS NOT DISTINCT FROM unknown               | BOOL        |
| IS NOT DISTINCT FROM | UUID IS NOT DISTINCT FROM UUID                     | BOOL        |
| IS NOT DISTINCT FROM | UUID[] IS NOT DISTINCT FROM UUID[]                 | BOOL        |
| IS NOT DISTINCT FROM | varbit IS NOT DISTINCT FROM varbit                 | BOOL        |
| LIKE                 | STRING LIKE STRING                                 | BOOL        |
| SIMILAR TO           | STRING SIMILAR TO STRING                           | BOOL        |
| ^                    | decimal ^ decimal                                  | decimal     |
| ^                    | decimal ^ INT2                                     | decimal     |
| ^                    | decimal ^ INT4                                     | decimal     |
| ^                    | decimal ^ INT8                                     | decimal     |
| ^                    | FLOAT4 ^ FLOAT4                                    | FLOAT8      |
| ^                    | FLOAT4 ^ FLOAT8                                    | FLOAT8      |
| ^                    | FLOAT8 ^ FLOAT4                                    | FLOAT8      |
| ^                    | FLOAT8 ^ FLOAT8                                    | FLOAT8      |
| ^                    | INT2 ^ decimal                                     | decimal     |
| ^                    | INT4 ^ decimal                                     | decimal     |
| ^                    | INT8 ^ decimal                                     | decimal     |
| ^                    | INT2 ^ INT2                                        | INT8        |
| ^                    | INT2 ^ INT4                                        | INT8        |
| ^                    | INT2 ^ INT8                                        | INT8        |
| ^                    | INT4 ^ INT2                                        | INT8        |
| ^                    | INT4 ^ INT4                                        | INT8        |
| ^                    | INT4 ^ INT8                                        | INT8        |
| ^                    | INT8 ^ INT2                                        | INT8        |
| ^                    | INT8 ^ INT4                                        | INT8        |
| ^                    | INT8 ^ INT8                                        | INT8        |
| &#124;                    | INET &#124; INET                                        | INET        |
| &#124;                    | INT2 &#124; INT2                                        | INT8        |
| &#124;                    | INT2 &#124; INT4                                        | INT8        |
| &#124;                    | INT2 &#124; INT8                                        | INT8        |
| &#124;                    | INT4 &#124; INT2                                        | INT8        |
| &#124;                    | INT4 &#124; INT4                                        | INT8        |
| &#124;                    | INT4 &#124; INT8                                        | INT8        |
| &#124;                    | INT8 &#124; INT2                                        | INT8        |
| &#124;                    | INT8 &#124; INT4                                        | INT8        |
| &#124;                    | INT8 &#124; INT8                                        | INT8        |
| &#124;                    | varbit &#124; varbit                                    | varbit      |
| &#124;&#124;                   | BOOL &#124;&#124; BOOL[]                                     | BOOL[]      |
| &#124;&#124;                   | BOOL[] &#124;&#124; BOOL                                     | BOOL[]      |
| &#124;&#124;                   | BOOL[] &#124;&#124; BOOL[]                                   | BOOL[]      |
| &#124;&#124;                   | bytes &#124;&#124; bytes                                     | bytes       |
| &#124;&#124;                   | bytes &#124;&#124; bytes[]                                   | bytes[]     |
| &#124;&#124;                   | bytes[] &#124;&#124; bytes                                   | bytes[]     |
| &#124;&#124;                   | bytes[] &#124;&#124; bytes[]                                 | bytes[]     |
| &#124;&#124;                   | date &#124;&#124; date[]                                     | date[]      |
| &#124;&#124;                   | date[] &#124;&#124; date                                     | date[]      |
| &#124;&#124;                   | date[] &#124;&#124; date[]                                   | date[]      |
| &#124;&#124;                   | decimal &#124;&#124; decimal[]                               | decimal[]   |
| &#124;&#124;                   | decimal[] &#124;&#124; decimal                               | decimal[]   |
| &#124;&#124;                   | decimal[] &#124;&#124; decimal[]                             | decimal[]   |
| &#124;&#124;                   | FLOAT4 &#124;&#124; FLOAT4[]                                 | FLOAT8[]    |
| &#124;&#124;                   | FLOAT4 &#124;&#124; FLOAT8[]                                 | FLOAT8[]    |
| &#124;&#124;                   | FLOAT8 &#124;&#124; FLOAT4[]                                 | FLOAT8[]    |
| &#124;&#124;                   | FLOAT8 &#124;&#124; FLOAT8[]                                 | FLOAT8[]    |
| &#124;&#124;                   | FLOAT4[] &#124;&#124; FLOAT4                                 | FLOAT8[]    |
| &#124;&#124;                   | FLOAT4[] &#124;&#124; FLOAT8                                 | FLOAT8[]    |
| &#124;&#124;                   | FLOAT8[] &#124;&#124; FLOAT4                                 | FLOAT8[]    |
| &#124;&#124;                   | FLOAT8[] &#124;&#124; FLOAT8                                 | FLOAT8[]    |
| &#124;&#124;                   | FLOAT4[] &#124;&#124; FLOAT4[]                               | FLOAT8[]    |
| &#124;&#124;                   | FLOAT4[] &#124;&#124; FLOAT8[]                               | FLOAT8[]    |
| &#124;&#124;                   | FLOAT8[] &#124;&#124; FLOAT4[]                               | FLOAT8[]    |
| &#124;&#124;                   | FLOAT8[] &#124;&#124; FLOAT8[]                               | FLOAT8[]    |
| &#124;&#124;                   | INET &#124;&#124; INET[]                                     | INET[]      |
| &#124;&#124;                   | INET[] &#124;&#124; INET                                     | INET[]      |
| &#124;&#124;                   | INET[] &#124;&#124; INET[]                                   | INET[]      |
| &#124;&#124;                   | INT2 &#124;&#124; INT2[]                                     | INT8[]      |
| &#124;&#124;                   | INT2 &#124;&#124; INT4[]                                     | INT8[]      |
| &#124;&#124;                   | INT2 &#124;&#124; INT8[]                                     | INT8[]      |
| &#124;&#124;                   | INT4 &#124;&#124; INT2[]                                     | INT8[]      |
| &#124;&#124;                   | INT4 &#124;&#124; INT4[]                                     | INT8[]      |
| &#124;&#124;                   | INT4 &#124;&#124; INT8[]                                     | INT8[]      |
| &#124;&#124;                   | INT8 &#124;&#124; INT2[]                                     | INT8[]      |
| &#124;&#124;                   | INT8 &#124;&#124; INT4[]                                     | INT8[]      |
| &#124;&#124;                   | INT8 &#124;&#124; INT8[]                                     | INT8[]      |
| &#124;&#124;                   | INT2[] &#124;&#124; INT2                                     | INT8[]      |
| &#124;&#124;                   | INT2[] &#124;&#124; INT4                                     | INT8[]      |
| &#124;&#124;                   | INT2[] &#124;&#124; INT8                                     | INT8[]      |
| &#124;&#124;                   | INT4[] &#124;&#124; INT2                                     | INT8[]      |
| &#124;&#124;                   | INT4[] &#124;&#124; INT4                                     | INT8[]      |
| &#124;&#124;                   | INT4[] &#124;&#124; INT8                                     | INT8[]      |
| &#124;&#124;                   | INT8[] &#124;&#124; INT2                                     | INT8[]      |
| &#124;&#124;                   | INT8[] &#124;&#124; INT4                                     | INT8[]      |
| &#124;&#124;                   | INT8[] &#124;&#124; INT8                                     | INT8[]      |
| &#124;&#124;                   | INT2[] &#124;&#124; INT2[]                                   | INT8[]      |
| &#124;&#124;                   | INT2[] &#124;&#124; INT4[]                                   | INT8[]      |
| &#124;&#124;                   | INT2[] &#124;&#124; INT8[]                                   | INT8[]      |
| &#124;&#124;                   | INT4[] &#124;&#124; INT2[]                                   | INT8[]      |
| &#124;&#124;                   | INT4[] &#124;&#124; INT4[]                                   | INT8[]      |
| &#124;&#124;                   | INT4[] &#124;&#124; INT8[]                                   | INT8[]      |
| &#124;&#124;                   | INT8[] &#124;&#124; INT2[]                                   | INT8[]      |
| &#124;&#124;                   | INT8[] &#124;&#124; INT4[]                                   | INT8[]      |
| &#124;&#124;                   | INT8[] &#124;&#124; INT8[]                                   | INT8[]      |
| &#124;&#124;                   | interval &#124;&#124; interval[]                             | interval[]  |
| &#124;&#124;                   | interval[] &#124;&#124; interval                             | interval[]  |
| &#124;&#124;                   | interval[] &#124;&#124; interval[]                           | interval[]  |
| &#124;&#124;                   | jsonb &#124;&#124; jsonb                                     | jsonb       |
| &#124;&#124;                   | oid &#124;&#124; oid                                         | oid         |
| &#124;&#124;                   | STRING &#124;&#124; STRING                                   | STRING      |
| &#124;&#124;                   | STRING &#124;&#124; STRING[]                                 | STRING[]    |
| &#124;&#124;                   | STRING[] &#124;&#124; STRING                                 | STRING[]    |
| &#124;&#124;                   | STRING[] &#124;&#124; STRING[]                               | STRING[]    |
| &#124;&#124;                   | time &#124;&#124; time[]                                     | time[]      |
| &#124;&#124;                   | time[] &#124;&#124; time                                     | time[]      |
| &#124;&#124;                   | time[] &#124;&#124; time[]                                   | time[]      |
| &#124;&#124;                   | timestamp &#124;&#124; timestamp[]                           | timestamp[] |
| &#124;&#124;                   | timestamp[] &#124;&#124; timestamp                           | timestamp[] |
| &#124;&#124;                   | timestamp[] &#124;&#124; timestamp[]                         | timestamp[] |
| &#124;&#124;                   | timestamptz &#124;&#124; timestamptz[]                       | timestamptz |
| &#124;&#124;                   | timestamptz[] &#124;&#124; timestamptz                       | timestamptz |
| &#124;&#124;                   | timestamptz[] &#124;&#124; timestamptz[]                     | timestamptz |
| &#124;&#124;                   | timetz &#124;&#124; timetz                                   | timetz      |
| &#124;&#124;                   | UUID &#124;&#124; UUID[]                                     | UUID[]      |
| &#124;&#124;                   | UUID[] &#124;&#124; UUID                                     | UUID[]      |
| &#124;&#124;                   | UUID[] &#124;&#124; UUID[]                                   | UUID[]      |
| &#124;&#124;                   | varbit &#124;&#124; varbit                                   | varbit      |
| ~                    | ~INET                                              | INET        |
| ~                    | ~INT2                                              | INT8        |
| ~                    | ~INT4                                              | INT8        |
| ~                    | ~INT8                                              | INT8        |
| ~                    | ~varbit                                            | varbit      |
| ~                    | STRING ~ STRING                                    | BOOL        |
| ~*                   | STRING ~* STRING                                   | BOOL        |
