---
title: 时序数据操作符
id: operation-symbols-ts-db
---

# 时序数据操作符

数据库操作符用于执行特定操作的符号或关键字。


## 优先级

下表按照从最高优先级到最低优先级的顺序列出了 KWDB 支持的所有运算符。具有相同优先级的运算符是左关联的，这意味着这些运算符从左侧开始向右移动。

| 优先级 | 操作符                                       | 名称                                   | 操作符数目 |
| ------------------------------------- | -------------------------------------------- | -------------------------------------- | ----------------------------------------- |
| 1                                     | .                                            | 成员字段访问运算符                     | 双目                                      |
| 2                                     | ::                                           | 类型转换                               | 双目                                      |
| 3                                     | -                                            | 取反                                   | 单目（前缀）                              |
| 3                                     | ~                                            | 按位取反                               | 单目（前缀）                              |
| 4                                     | ^                                            | 求幂                                   | 双目                                      |
| 5                                     | \*                                           | 乘                                     | 双目                                      |
| 5                                     | /                                            | 除                                     | 双目                                      |
| 5                                     | //                                           | 除（结果向下取整，3/2=1）              | 双目                                      |
| 5                                     | %                                            | 求余                                   | 双目                                      |
| 6                                     | +                                            | 加                                     | 双目                                      |
| 6                                     | -                                            | 减                                     | 双目                                      |
| 7                                     | <<                                           | 按位左移                               | 双目                                      |
| 7                                     | >>                                           | 按位右移                               | 双目                                      |
| 8                                     | &                                            | 按位与                                 | 双目                                      |
| 9                                     | #                                            | 按位异或                               | 双目                                      |
| 10                                    | &#124;                                       | 按位或                                 | 双目                                      |
| 11                                    | &#124;&#124;                                 | 字符串拼接                             | 双目                                      |
| 12                                    | [NOT] IN                                     | 值不在指定的集合中                     | 双目                                      |
| 12                                    | [NOT] LIKE                                   | 匹配[或不匹配] LIKE 表达式，区分大小写 | 双目                                      |
| 12                                    | ~                                            | 匹配正则表达式，区分大小写             | 双目                                      |
| 12                                    | !~                                           | 与正则表达式不匹配，区分大小写         | 双目                                      |
| 12                                    | ~\*                                          | 匹配正则表达式，不区分大小写           | 双目                                      |
| 12                                    | !~\*                                         | 与正则表达式不匹配，不区分大小写       | 双目                                      |
| 13                                    | =                                            | 等于                                   | 双目                                      |
| 13                                    | <                                            | 小于                                   | 双目                                      |
| 13                                    | >                                            | 大于                                   | 双目                                      |
| 13                                    | <=                                           | 小于或等于                             | 双目                                      |
| 13                                    | >=                                           | 大于或等于                             | 双目                                      |
| 13                                    | !=，<>                                       | 不等于                                 | 双目                                      |
| 14                                    | ISNULL，IS UNKNOWN , NOTNULL, IS NOT UNKNOWN | 等价于 IS NULL/IS NOT NULL             | 单目（后缀）                              |
| 14                                    | IS NAN, IS NOT NAN                           | 与浮点 NAN 值的比较                    | 单目（后缀）                              |

## 支持的操作符

| 操作符 | 表达式                     | 返回值      |
| ------ | -------------------------- | ----------- |
| #      | int2 # int2                | int8        |
| #      | int2 # int4                | int8        |
| #      | int2 # int8                | int8        |
| #      | int4 # int2                | int8        |
| #      | int4 # int4                | int8        |
| #      | int4 # int8                | int8        |
| #      | int8 # int2                | int8        |
| #      | int8 # int4                | int8        |
| #      | int8 # int8                | int8        |
| %      | float4 % float4            | float8      |
| %      | float4 % float8            | float8      |
| %      | float8 % float4            | float8      |
| %      | float8 % float8            | float8      |
| %      | int2 % int2                | int8        |
| %      | int2 % int4                | int8        |
| %      | int2 % int8                | int8        |
| %      | int4 % int2                | int8        |
| %      | int4 % int4                | int8        |
| %      | int4 % int8                | int8        |
| %      | int8 % int2                | int8        |
| %      | int8 % int4                | int8        |
| %      | int8 % int8                | int8        |
| &      | int2 & int2                | int8        |
| &      | int2 & int4                | int8        |
| &      | int2 & int8                | int8        |
| &      | int4 & int2                | int8        |
| &      | int4 & int4                | int8        |
| &      | int4 & int8                | int8        |
| &      | int8 & int2                | int8        |
| &      | int8 & int4                | int8        |
| &      | int8 & int8                | int8        |
| *      | float4 * float4            | float8      |
| *      | float4 * float8            | float8      |
| *      | float8 * float4            | float8      |
| *      | float8 * float8            | float8      |
| *      | int2 * int2                | int8        |
| *      | int2 * int4                | int8        |
| *      | int2 * int8                | int8        |
| *      | int4 * int2                | int8        |
| *      | int4 * int4                | int8        |
| *      | int4 * int8                | int8        |
| *      | int8 * int2                | int8        |
| *      | int8 * int4                | int8        |
| *      | int8 * int8                | int8        |
| +      | float4 + float4            | float8      |
| +      | float4 + float8            | float8      |
| +      | float8 + float4            | float8      |
| +      | float8 + float8            | float8      |
| +      | int2 + int2                | int8        |
| +      | int2 + int4                | int8        |
| +      | int2 + int8                | int8        |
| +      | int4 + int2                | int8        |
| +      | int4 + int4                | int8        |
| +      | int4 + int8                | int8        |
| +      | int8 + int2                | int8        |
| +      | int8 + int4                | int8        |
| +      | int8 + int8                | int8        |
| +      | timestamp + interval       | timestamp   |
| +      | timestamptz + interval     | timestamptz |
| -      | -float4                    | float8      |
| -      | -float8                    | float8      |
| -      | -int2                      | int8        |
| -      | -int4                      | int8        |
| -      | -int8                      | int8        |
| -      | float4 - float4            | float8      |
| -      | float4 - float8            | float8      |
| -      | float8 - float4            | float8      |
| -      | float8 - float8            | float8      |
| -      | int2 - int2                | int8        |
| -      | int2 - int4                | int8        |
| -      | int2 - int8                | int8        |
| -      | int4 - int2                | int8        |
| -      | int4 - int4                | int8        |
| -      | int4 - int8                | int8        |
| -      | int8 - int2                | int8        |
| -      | int8 - int4                | int8        |
|        | int8 - int8                | int8        |
| -      | timestamp - timestamp      | interval    |
| -      | timestamp - timestamptz    | interval    |
| -      | timestamp - interval       | timestamp   |
| -      | timestamptz - interval     | timestamptz |
| -      | timestamptz - timestamp    | interval    |
| -      | timestamptz - timestamptz  | interval    |
| /      | float4 / float4            | float8      |
| /      | float4 / float8            | float8      |
| /      | float8 / float4            | float8      |
| /      | float8 / float8            | float8      |
| /      | int2 / int2                | decimal     |
| /      | int2 / int4                | decimal     |
| /      | int2 / int8                | decimal     |
| /      | int4 / int2                | decimal     |
| /      | int4 / int4                | decimal     |
| /      | int4 / int8                | decimal     |
| /      | int8 / int2                | decimal     |
| /      | int8 / int4                | decimal     |
| /      | int8 / int8                | decimal     |
| <      | BOOL < BOOL                | BOOL        |
| <      | float4 < float4            | BOOL        |
| <      | float4 < float8            | BOOL        |
| <      | float8 < float4            | BOOL        |
| <      | float8 < float8            | BOOL        |
| <      | float4 < int2              | BOOL        |
| <      | float4 < int4              | BOOL        |
| <      | float4 < int8              | BOOL        |
| <      | float8 < int2              | BOOL        |
| <      | float8 < int4              | BOOL        |
| <      | float8 < int8              | BOOL        |
| <      | int2 < float4              | BOOL        |
| <      | int2 < float8              | BOOL        |
| <      | int4 < float4              | BOOL        |
| <      | int4 < float8              | BOOL        |
| <      | int8 < float4              | BOOL        |
| <      | int8 < float8              | BOOL        |
| <      | int2 < int2                | BOOL        |
| <      | int2 < int4                | BOOL        |
| <      | int2 < int8                | BOOL        |
| <      | int4 < int2                | BOOL        |
| <      | int4 < int4                | BOOL        |
| <      | int4 < int8                | BOOL        |
| <      | int8 < int2                | BOOL        |
| <      | int8 < int4                | BOOL        |
| <      | int8 < int8                | BOOL        |
| <      | timestamp < timestamp      | BOOL        |
| <      | timestamp < timestamptz    | BOOL        |
| <      | timestamptz < timestamp    | BOOL        |
| <      | timestamptz < timestamptz  | BOOL        |
| <<     | int2 <<  int2              | int8        |
| <<     | int2 <<  int4              | int8        |
| <<     | int2 <<  int8              | int8        |
| <<     | int4 <<  int2              | int8        |
| <<     | int4 <<  int4              | int8        |
| <<     | int4 <<  int8              | int8        |
| <<     | int8 <<  int2              | int8        |
| <<     | int8 <<  int4              | int8        |
| <<     | int8 <<  int8              | int8        |
| <=     | BOOL <= BOOL               | BOOL        |
| <=     | float4 <= float4           | BOOL        |
| <=     | float4 <= float8           | BOOL        |
| <=     | float8 <= float4           | BOOL        |
| <=     | float8 <= float8           | BOOL        |
| <=     | float4 <= int2             | BOOL        |
| <=     | float4 <= int4             | BOOL        |
| <=     | float4 <= int8             | BOOL        |
| <=     | float8 <= int2             | BOOL        |
| <=     | float8 <= int4             | BOOL        |
| <=     | float8 <= int8             | BOOL        |
| <=     | int2 <= float4             | BOOL        |
| <=     | int2 <= float8             | BOOL        |
| <=     | int4 <= float4             | BOOL        |
| <=     | int4 <= float8             | BOOL        |
| <=     | int8 <= float4             | BOOL        |
| <=     | int8 <= float8             | BOOL        |
| <=     | int2 <= int2               | BOOL        |
| <=     | int2 <= int4               | BOOL        |
| <=     | int2 <= int8               | BOOL        |
| <=     | int4 <= int2               | BOOL        |
| <=     | int4 <= int4               | BOOL        |
| <=     | int4 <= int8               | BOOL        |
| <=     | int8 <= int2               | BOOL        |
| <=     | int8 <= int4               | BOOL        |
| <=     | int8 <= int8               | BOOL        |
| <=     | timestamp <= timestamp     | BOOL        |
| <=     | timestamp <= timestamptz   | BOOL        |
| <=     | timestamptz <= timestamp   | BOOL        |
| <=     | timestamptz <= timestamptz | BOOL        |
| =      | BOOL = BOOL                | BOOL        |
| =      | float4 = float4            | BOOL        |
| =      | float4 = float8            | BOOL        |
| =      | float8 = float4            | BOOL        |
| =      | float8 = float8            | BOOL        |
| =      | float4 = int2              | BOOL        |
| =      | float4 = int4              | BOOL        |
| =      | float4 = int8              | BOOL        |
| =      | float8 = int2              | BOOL        |
| =      | float8 = int4              | BOOL        |
| =      | float8 = int8              | BOOL        |
| =      | int2 = float4              | BOOL        |
| =      | int2 = float8              | BOOL        |
| =      | int4 = float4              | BOOL        |
| =      | int4 = float8              | BOOL        |
| =      | int8 = float4              | BOOL        |
| =      | int8 = float8              | BOOL        |
| =      | int2 = int2                | BOOL        |
| =      | int2 = int4                | BOOL        |
| =      | int2 = int8                | BOOL        |
| =      | Int4 = int2                | BOOL        |
| =      | int4 = int4                | BOOL        |
| =      | int4 = int8                | BOOL        |
| =      | int8 = int2                | BOOL        |
| =      | int8 = int4                | BOOL        |
| =      | int8 = int8                | BOOL        |
| =      | timestamp = timestamp      | BOOL        |
| =      | timestamp = timestamptz    | BOOL        |
| =      | timestamptz = timestamp    | BOOL        |
| =      | timestamptz = timestamptz  | BOOL        |
| >>     | int2 >> int2               | int8        |
| >>     | int2 >> int4               | int8        |
| >>     | int2 >> int8               | int8        |
| >>     | int4 >> int2               | int8        |
| >>     | int4 >> int4               | int8        |
| >>     | int4 >> int8               | int8        |
| >>     | int8 >> int2               | int8        |
| >>     | int8 >> int4               | int8        |
| >>     | int8 >> int8               | int8        |
