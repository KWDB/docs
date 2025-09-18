---
title: Time-Series Operators
id: operation-symbols-ts-db
---

# Time-Series Operators

Operators are symbols or keywords used to perform specific operations.

## Order of Precedence

This table lists all KWDB operators from highest to lowest precedence, which determines the order in which they are evaluated within a statement. Operators with the same precedence are left associative. This means that those operators are grouped together starting from the left and moving right.

| Order of Precedence | Operator                                     | Name                                                | Operator Arity |
|---------------------|----------------------------------------------|-----------------------------------------------------|----------------|
| 1                   | .                                            | Member field access operator                        | binary         |
| 2                   | ::                                           | Type cast                                           | binary         |
| 3                   | -                                            | Unary minus                                         | unary (prefix) |
| 3                   | ~                                            | Bitwise not                                         | unary (prefix) |
| 4                   | ^                                            | Exponentiation                                      | binary         |
| 5                   | \*                                           | Multiplication                                      | binary         |
| 5                   | /                                            | Division                                            | binary         |
| 5                   | //                                           | Floor division                                      | binary         |
| 5                   | %                                            | Modulo                                              | binary         |
| 6                   | +                                            | Addition                                            | binary         |
| 6                   | -                                            | Subtraction                                         | binary         |
| 7                   | <<                                           | Bitwise left-shift                                  | binary         |
| 7                   | >>                                           | Bitwise right-shift                                 | binary         |
| 8                   | &                                            | Bitwise AND                                         | binary         |
| 9                   | #                                            | Bitwise XOR                                         | binary         |
| 10                  | &#124;                                       | Bitwise OR                                          | binary         |
| 11                  | &#124;&#124;                                 | Concatenation                                       | binary         |
| 12                  | [NOT] IN                                     | Value is [not] in the set of values specified       | binary         |
| 12                  | [NOT] LIKE                                   | Matches [or not] LIKE expression, case sensitive    | binary         |
| 12                  | ~                                            | Matches regular expression, case sensitive          | binary         |
| 12                  | !~                                           | Does not match regular expression, case sensitive   | binary         |
| 12                  | ~\*                                          | Matches regular expression, case insensitive        | binary         |
| 12                  | !~\*                                         | Does not match regular expression, case insensitive | binary         |
| 13                  | =                                            | Equal                                               | binary         |
| 13                  | <                                            | Less than                                           | binary         |
| 13                  | >                                            | Greater than                                        | binary         |
| 13                  | <=                                           | Less than or equal                                  | binary         |
| 13                  | >=                                           | Greater than or equal                               | binary         |
| 13                  | !=, <>                                       | Not equal                                           | binary         |
| 14                  | ISNULL, IS UNKNOWN, NOTNULL, IS NOT UNKNOWN  | Equivalent to `IS NULL` / `IS NOT NULL`             | unary (suffix) |
| 14                  | IS NAN, IS NOT NAN                           | Comparison with the floating-point NaN value        | unary (suffix) |

## Supported Operators

| Operator | Expression                 | Return      |
|----------|----------------------------|-------------|
| #        | int2 # int2                | int8        |
| #        | int2 # int4                | int8        |
| #        | int2 # int8                | int8        |
| #        | int4 # int2                | int8        |
| #        | int4 # int4                | int8        |
| #        | int4 # int8                | int8        |
| #        | int8 # int2                | int8        |
| #        | int8 # int4                | int8        |
| #        | int8 # int8                | int8        |
| %        | float4 % float4            | float8      |
| %        | float4 % float8            | float8      |
| %        | float8 % float4            | float8      |
| %        | float8 % float8            | float8      |
| %        | int2 % int2                | int8        |
| %        | int2 % int4                | int8        |
| %        | int2 % int8                | int8        |
| %        | int4 % int2                | int8        |
| %        | int4 % int4                | int8        |
| %        | int4 % int8                | int8        |
| %        | int8 % int2                | int8        |
| %        | int8 % int4                | int8        |
| %        | int8 % int8                | int8        |
| &        | int2 & int2                | int8        |
| &        | int2 & int4                | int8        |
| &        | int2 & int8                | int8        |
| &        | int4 & int2                | int8        |
| &        | int4 & int4                | int8        |
| &        | int4 & int8                | int8        |
| &        | int8 & int2                | int8        |
| &        | int8 & int4                | int8        |
| &        | int8 & int8                | int8        |
| *        | float4 * float4            | float8      |
| *        | float4 * float8            | float8      |
| *        | float8 * float4            | float8      |
| *        | float8 * float8            | float8      |
| *        | int2 * int2                | int8        |
| *        | int2 * int4                | int8        |
| *        | int2 * int8                | int8        |
| *        | int4 * int2                | int8        |
| *        | int4 * int4                | int8        |
| *        | int4 * int8                | int8        |
| *        | int8 * int2                | int8        |
| *        | int8 * int4                | int8        |
| *        | int8 * int8                | int8        |
| +        | float4 + float4            | float8      |
| +        | float4 + float8            | float8      |
| +        | float8 + float4            | float8      |
| +        | float8 + float8            | float8      |
| +        | int2 + int2                | int8        |
| +        | int2 + int4                | int8        |
| +        | int2 + int8                | int8        |
| +        | int4 + int2                | int8        |
| +        | int4 + int4                | int8        |
| +        | int4 + int8                | int8        |
| +        | int8 + int2                | int8        |
| +        | int8 + int4                | int8        |
| +        | int8 + int8                | int8        |
| +        | timestamp + interval       | timestamp   |
| +        | timestamptz + interval     | timestamptz |
| -        | -float4                    | float8      |
| -        | -float8                    | float8      |
| -        | -int2                      | int8        |
| -        | -int4                      | int8        |
| -        | -int8                      | int8        |
| -        | float4 - float4            | float8      |
| -        | float4 - float8            | float8      |
| -        | float8 - float4            | float8      |
| -        | float8 - float8            | float8      |
| -        | int2 - int2                | int8        |
| -        | int2 - int4                | int8        |
| -        | int2 - int8                | int8        |
| -        | int4 - int2                | int8        |
| -        | int4 - int4                | int8        |
| -        | int4 - int8                | int8        |
| -        | int8 - int2                | int8        |
| -        | int8 - int4                | int8        |
|          | int8 - int8                | int8        |
| -        | timestamp - timestamp      | interval    |
| -        | timestamp - timestamptz    | interval    |
| -        | timestamp - interval       | timestamp   |
| -        | timestamptz - interval     | timestamptz |
| -        | timestamptz - timestamp    | interval    |
| -        | timestamptz - timestamptz  | interval    |
| /        | float4 / float4            | float8      |
| /        | float4 / float8            | float8      |
| /        | float8 / float4            | float8      |
| /        | float8 / float8            | float8      |
| /        | int2 / int2                | decimal     |
| /        | int2 / int4                | decimal     |
| /        | int2 / int8                | decimal     |
| /        | int4 / int2                | decimal     |
| /        | int4 / int4                | decimal     |
| /        | int4 / int8                | decimal     |
| /        | int8 / int2                | decimal     |
| /        | int8 / int4                | decimal     |
| /        | int8 / int8                | decimal     |
| <        | BOOL < BOOL                | BOOL        |
| <        | float4 < float4            | BOOL        |
| <        | float4 < float8            | BOOL        |
| <        | float8 < float4            | BOOL        |
| <        | float8 < float8            | BOOL        |
| <        | float4 < int2              | BOOL        |
| <        | float4 < int4              | BOOL        |
| <        | float4 < int8              | BOOL        |
| <        | float8 < int2              | BOOL        |
| <        | float8 < int4              | BOOL        |
| <        | float8 < int8              | BOOL        |
| <        | int2 < float4              | BOOL        |
| <        | int2 < float8              | BOOL        |
| <        | int4 < float4              | BOOL        |
| <        | int4 < float8              | BOOL        |
| <        | int8 < float4              | BOOL        |
| <        | int8 < float8              | BOOL        |
| <        | int2 < int2                | BOOL        |
| <        | int2 < int4                | BOOL        |
| <        | int2 < int8                | BOOL        |
| <        | int4 < int2                | BOOL        |
| <        | int4 < int4                | BOOL        |
| <        | int4 < int8                | BOOL        |
| <        | int8 < int2                | BOOL        |
| <        | int8 < int4                | BOOL        |
| <        | int8 < int8                | BOOL        |
| <        | timestamp < timestamp      | BOOL        |
| <        | timestamp < timestamptz    | BOOL        |
| <        | timestamptz < timestamp    | BOOL        |
| <        | timestamptz < timestamptz  | BOOL        |
| <<       | int2 <<  int2              | int8        |
| <<       | int2 <<  int4              | int8        |
| <<       | int2 <<  int8              | int8        |
| <<       | int4 <<  int2              | int8        |
| <<       | int4 <<  int4              | int8        |
| <<       | int4 <<  int8              | int8        |
| <<       | int8 <<  int2              | int8        |
| <<       | int8 <<  int4              | int8        |
| <<       | int8 <<  int8              | int8        |
| <=       | BOOL <= BOOL               | BOOL        |
| <=       | float4 <= float4           | BOOL        |
| <=       | float4 <= float8           | BOOL        |
| <=       | float8 <= float4           | BOOL        |
| <=       | float8 <= float8           | BOOL        |
| <=       | float4 <= int2             | BOOL        |
| <=       | float4 <= int4             | BOOL        |
| <=       | float4 <= int8             | BOOL        |
| <=       | float8 <= int2             | BOOL        |
| <=       | float8 <= int4             | BOOL        |
| <=       | float8 <= int8             | BOOL        |
| <=       | int2 <= float4             | BOOL        |
| <=       | int2 <= float8             | BOOL        |
| <=       | int4 <= float4             | BOOL        |
| <=       | int4 <= float8             | BOOL        |
| <=       | int8 <= float4             | BOOL        |
| <=       | int8 <= float8             | BOOL        |
| <=       | int2 <= int2               | BOOL        |
| <=       | int2 <= int4               | BOOL        |
| <=       | int2 <= int8               | BOOL        |
| <=       | int4 <= int2               | BOOL        |
| <=       | int4 <= int4               | BOOL        |
| <=       | int4 <= int8               | BOOL        |
| <=       | int8 <= int2               | BOOL        |
| <=       | int8 <= int4               | BOOL        |
| <=       | int8 <= int8               | BOOL        |
| <=       | timestamp <= timestamp     | BOOL        |
| <=       | timestamp <= timestamptz   | BOOL        |
| <=       | timestamptz <= timestamp   | BOOL        |
| <=       | timestamptz <= timestamptz | BOOL        |
| =        | BOOL = BOOL                | BOOL        |
| =        | float4 = float4            | BOOL        |
| =        | float4 = float8            | BOOL        |
| =        | float8 = float4            | BOOL        |
| =        | float8 = float8            | BOOL        |
| =        | float4 = int2              | BOOL        |
| =        | float4 = int4              | BOOL        |
| =        | float4 = int8              | BOOL        |
| =        | float8 = int2              | BOOL        |
| =        | float8 = int4              | BOOL        |
| =        | float8 = int8              | BOOL        |
| =        | int2 = float4              | BOOL        |
| =        | int2 = float8              | BOOL        |
| =        | int4 = float4              | BOOL        |
| =        | int4 = float8              | BOOL        |
| =        | int8 = float4              | BOOL        |
| =        | int8 = float8              | BOOL        |
| =        | int2 = int2                | BOOL        |
| =        | int2 = int4                | BOOL        |
| =        | int2 = int8                | BOOL        |
| =        | Int4 = int2                | BOOL        |
| =        | int4 = int4                | BOOL        |
| =        | int4 = int8                | BOOL        |
| =        | int8 = int2                | BOOL        |
| =        | int8 = int4                | BOOL        |
| =        | int8 = int8                | BOOL        |
| =        | timestamp = timestamp      | BOOL        |
| =        | timestamp = timestamptz    | BOOL        |
| =        | timestamptz = timestamp    | BOOL        |
| =        | timestamptz = timestamptz  | BOOL        |
| >>       | int2 >> int2               | int8        |
| >>       | int2 >> int4               | int8        |
| >>       | int2 >> int8               | int8        |
| >>       | int4 >> int2               | int8        |
| >>       | int4 >> int4               | int8        |
| >>       | int4 >> int8               | int8        |
| >>       | int8 >> int2               | int8        |
| >>       | int8 >> int4               | int8        |
| >>       | int8 >> int8               | int8        |
