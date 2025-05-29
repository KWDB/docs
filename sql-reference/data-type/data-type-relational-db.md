---
title: 关系数据类型
id: data-type-relational-db
---

# 关系数据类型

KWDB 关系数据支持以下数据类型：

- 数值类型
- 布尔类型
- 字符类型
- 时间和日期类型
- JSON 类型
- 数组类型
- INET 类型
- UUID 类型

## 数值类型

KWDB 关系数据库支持的数值类型包括整数类型、浮点类型、定点类型和 SERIAL 类型。

::: warning 提示

- 如需生成自动增长的全局唯一值（例如主键），使用 UUID 或 SERIAL 数据类型。
- 如需任意精度数字，使用定点类型。

:::

### 整数类型

#### 类型描述

KWDB 支持有符号的整数数据类型。

| 名称 | 别名                 | 存储空间 | 取值范围                                    |
| ---- | -------------------- | --------------------------------------- | ------------------------------------------- |
| INT2 | SMALLINT             | 2 字节                                  | -32768 ~ +32767                             |
| INT4 | - INT <br>- INTEGER  | 4 字节                                  | -2147483648 ~ +2147483647                   |
| INT8 | - INT64 <br>- BIGINT | 8 字节                                  | -9223372036854775808 ~ +9223372036854775807 |

::: warning 说明

- 整数类型支持将数值作为文本输入，例如 `42`、`-1234`、`0xCAFE`。
- 虽然不同的整数类型对允许值的范围有不同的约束，但是所有整数采用相同的存储方式。数值越小，占据的存储空间越小，例如，存储值为 `42` 的整数类型占用较少的存储空间，而存储值为 `2147483647` 的整数类型占用较大的存储空间。

:::

#### 示例

以下示例创建一个名为 `ints` 的表，包括具有整数类型的列。

```sql
-- 1. 创建表 ints。

CREATE TABLE ints(c1 INT PRIMARY KEY, c2 SMALLINT, c3 BIGINT, c4 INTEGER, c5 INT2, c6 INT4, c7 INT8, c8 INT64);
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM ints;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | INT4      |    false    | NULL           |                       | {primary} |   false   | false
  c2          | INT2      |    true     | NULL           |                       | {}        |   false   | false
  c3          | INT8      |    true     | NULL           |                       | {}        |   false   | false
  c4          | INT4      |    true     | NULL           |                       | {}        |   false   | false
  c5          | INT2      |    true     | NULL           |                       | {}        |   false   | false
  c6          | INT4      |    true     | NULL           |                       | {}        |   false   | false
  c7          | INT8      |    true     | NULL           |                       | {}        |   false   | false
  c8          | INT8      |    true     | NULL           |                       | {}        |   false   | false
(8 rows)
```

### 浮点类型

#### 类型描述

KWDB 支持 FLOAT8 和 FLOAT4 不确定精度的浮点数据类型，最大精度为 17 位十进制小数。浮点类型支持将数值文本，例如：`1.414` 或 `1234`。

| 名称   | 别名           | 存储空间 |
| ------ | --------------------------------------------- | --------------------------------------- |
| FLOAT8 | - DOUBLE <br> - DOUBLE PRECISION <br>- FLOAT | 8 字节                                  |
| FLOAT4 | REAL                                        | 4 字节                                  |

FLOAT 列存储最多 8 个字节的值。但由于元数据的影响，实际存储大小可能会更大。

在内部处理时，KWDB 使用 64 位双精度 IEEE 754 格式表示浮点数。IEEE 754 的特殊值如正无穷大、负无穷大和 NaN（非数字），不能直接使用数字文字输入，而必须使用解释文字或从字符串文字的显式转换进行转换。

下表列出了可以识别的值：

| 值 | 语法             |
| --------------------------------- | ----------------------------------------------- |
| 正无穷大                          | - inf <br>- infinity <br>- +inf <br>- +infinity |
| 负无穷大                          | - -inf <br>- -infinity                          |
| NaN（非数字）                     | nan                                             |

例如：

- `FLOAT '+Inf'`
- `'-Inf'::FLOAT`
- `CAST('NaN' AS FLOAT)`

#### 示例

以下示例创建一个名为 `floats` 的表，向表中写入数据并使用 CAST 函数限制浮点类型的列的显示精度。

```sql
-- 1. 创建表 floats。

CREATE TABLE floats (c1 FLOAT PRIMARY KEY, c2 REAL, c3 DOUBLE PRECISION);
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM floats;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | FLOAT8    |    false    | NULL           |                       | {primary} |   false   | false
  c2          | FLOAT4    |    true     | NULL           |                       | {}        |   false   | false
  c3          | FLOAT8    |    true     | NULL           |                       | {}        |   false   | false
(3 rows)

-- 3. 向具有浮点类型的列中写入数值。

INSERT INTO floats VALUES (3.141592653834231235345, 2.718281828459, CAST('+Inf' AS FLOAT)),(FLOAT'-inf',1e1,'nan'::FLOAT);
INSERT 2

-- 4. 查看表中的数据。

SELECT * FROM floats;
c1              |c2       |c3
----------------+---------+----
-Inf            |10.000000|NaN
3.14159265383423|2.718282 |+Inf
(2 rows)
```

### 定点类型

#### 类型描述

定点类型（DECIMAL）用于存储精确的定点数，适用于需要保留精确精度的数据，例如货币数据。定点类型支持将数值作为文本输入，例如 `1.414` 或 `1234`。

| 名称    | 别名 | 存储空间 |
| ------- | ----------------------------------- | --------------------------------------- |
| DECIMAL | - DEC <br>- NUMERIC                 | 9 ~ 64K 字节                            |

IEEE 754 的特殊值如正无穷大、负无穷大和 NaN（非数字），不能直接使用数字文字输入，而必须使用解释文字或从字符串文字的显式转换进行转换。

下表列出了可以识别的值：

| 值 | 语法             |
| --------------------------------- | ----------------------------------------------- |
| 正无穷大                          | - inf <br>- infinity <br>- +inf <br>- +infinity |
| 负无穷大                          | - -inf <br>- -infinity                          |
| NaN（非数字）                     | nan                                             |

DECIMAL 列支持使用 `DECIMAL(precision, scale)` 对数值进行限制。其中 `precision` 是小数点左侧和右侧位数之和的最大值，`scale` 是小数点右侧的精确位数。`precision` 的值不能小于 `scale`。使用 `DECIMAL(precision)` 等效于 `DECIMAL(precision, 0)`。

::: warning 说明

在写入 DECIMAL 值时：

- 如果小数点右侧的数字位数大于 scale，会四舍五入到 scale。
- 如果小数点右侧的数字位数小于 scale，会填充零，直到达到 scale。
- 如果小数点左侧和右侧位数之和大于 precision，系统报错。
- 如果 precision 和 scale 相等，写入的值必须四舍五入为小于 1 的值。

:::

#### 示例

以下示例创建一个具有 CHAR 列的表 `decimals` 并向表中写入数据。

```sql
-- 1. 创建表 decimals。

CREATE TABLE decimals(c1 DECIMAL PRIMARY KEY, c2 DEC, c3 NUMERIC, c4 DECIMAL(3), c5 DECIMAL(10, 2));
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM decimals;
  column_name |   data_type   | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+---------------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | DECIMAL       |    false    | NULL           |                       | {primary} |   false   | false
  c2          | DECIMAL       |    true     | NULL           |                       | {}        |   false   | false
  c3          | DECIMAL       |    true     | NULL           |                       | {}        |   false   | false
  c4          | DECIMAL(3)    |    true     | NULL           |                       | {}        |   false   | false
  c5          | DECIMAL(10,2) |    true     | NULL           |                       | {}        |   false   | false
(5 rows)

-- 3. 向表中写入数据。其中 c1 列的值和 DECIMAL 精度匹配，完全保持原值。c2 列的值小数部分被四舍五入到与 DECIMAL(10,5)的 scale 相同的 5 位。c3 列的 NUMERIC 是 DECIMAL 的别名，因此和 c1 具有相同的处理方式。

INSERT INTO decimals VALUES (1.01234567890123456789, 1.01234567890123456789, 1.01234567890123456789),(DECIMAL'+inf','-inf'::DEC,CAST('nan' AS NUMERIC));
INSERT 2

-- 4. 查看表的内容。

SELECT * FROM decimals;
c1                    |c2                    |c3                    |c4|c5
----------------------+----------------------+----------------------+--+--
1.01234567890123456789|1.01234567890123456789|1.01234567890123456789|  |
Infinity              |-Infinity             |NaN                   |  |
(2 rows)
```

### SERIAL 类型

#### 类型描述

SERIAL 关键字是一种伪数据类型，用于在定义列的时候代替实际的数据类型。使用 SERIAL 定义表的列相当于使用具有 DEFAULT 表达式的整数类型。在每次求值时，DEFAULT 表达式生成唯一的值。使用 SERIAL 数据类型确保未指定此列的值时，系统自动生成一个值，而不是写入 NULL 值。SERIAL 对应的实际数据类型为 INT8，默认值为 `unique_rowid()` 的生成值。

#### 示例

以下示例创建一个具有 SERIAL 主键列的表 `serial` 并向表中写入数据。

```sql
-- 1. 创建表 serial。

CREATE TABLE serial (c1 SERIAL PRIMARY KEY, c2 STRING, c3 BOOL);
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM serial;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | INT8      |    false    | unique_rowid() |                       | {primary} |   false   | false
  c2          | STRING    |    true     | NULL           |                       | {}        |   false   | false
  c3          | BOOL      |    true     | NULL           |                       | {}        |   false   | false
(3 rows)

-- 3. 向表中写入数据，把 c1 列空出。

INSERT INTO serial (c2,c3) VALUES ('one', true), ('two', false), ('three', true);
INSERT 3

INSERT INTO serial (c1,c2,c3) VALUES (110,'four', true);
INSERT 1

-- 4. 查看表中的内容。由返回结果可以看出，每一行在 c1 列中均存在一个默认的唯一值。

SELECT * FROM serial;
          c1         |  c2   |  c3
---------------------+-------+--------
                 110 | four  | true
  960684591614623745 | one   | true
  960684591614754817 | two   | false
  960684591614787585 | three | true
(4 rows)
```

## 布尔类型

### 类型描述

布尔类型（BOOL）存储布尔值 `false` 或 `true`。通常情况下，布尔值的宽度为 1 个字节。但由于元数据的影响，实际存储大小可能会更大。

| 名称 | 别名 | 存储空间 |
| ---- | ----------------------------------- | --------------------------------------- |
| BOOL | BOOLEAN                             | 1 字节                                  |

布尔值有两个预定义的命名常量：`TRUE` 和 `FALSE`（不区分大小写）。

用户可以通过数值的强制类型转换来获取布尔值。默认情况下，零会被强制转换为 `FALSE`，任何非零的值会被强制转换为 `TRUE`，如下所示：

- `CAST(0 AS BOOL) (false)`
- `CAST(119 AS BOOL) (true)`

### 示例

以下示例创建一个具有布尔类型列的表 `bools` 并向表中写入数据。

```sql
-- 1. 创建表 bools。

CREATE TABLE bools (c1 INT PRIMARY KEY, c2 BOOL, c3 BOOLEAN);
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM bools;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | INT4      |    false    | NULL           |                       | {primary} |   false   | false
  c2          | BOOL      |    true     | NULL           |                       | {}        |   false   | false
  c3          | BOOL      |    true     | NULL           |                       | {}        |   false   | false
(3 rows)

-- 3. 向表中写入数据。

INSERT INTO bools VALUES (1, true, CAST(0 AS BOOL)),(2,false,CAST(3.14 AS BOOLEAN));
INSERT 2

-- 4. 查看表中的内容。

SELECT * FROM bools;
  c1 |  c2   |  c3
-----+-------+--------
   1 | true  | false
   2 | false | true
(2 rows)
```

## 字符类型

### BIT

#### 类型描述

BIT 数据类型用于存储固定长度的二进制位数组。位数组常量用于表示字面量值。例如，`B'100101'` 表示一个 6 位的位数组。BIT 类型的数值占用的位数如下表所示：

| 类型 | 逻辑大小 |
| ----------------------------------- | --------------------------------------- |
| BIT                                 | 1 bit                                   |
| BIT(N)                              | N bit                                   |

对于 BIT 和 BIT(N) 数据类型。数值的宽度大小必须完全匹配，否则系统会报错。BIT 值的有效大小比其逻辑位数大一个有界常数。数据库内部以 64 位增量存储位数组，并使用额外的整数值来编码长度。虽然 BIT 值的总存储大小可以任意大，但建议将其保持在 1 MB 以下以确保性能。如果超过该阈值，写入放大和其他因素可能导致性能显著下降。

#### 示例

以下示例创建一个具有 BIT 列的表 `bits` 并向表中写入数据。

```sql
-- 1. 创建表 bits。

CREATE TABLE bits (c1 BIT, c2 BIT(3));
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM bits;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | BIT       |    true     | NULL           |                       | {}        |   false   | false
  c2          | BIT(3)    |    true     | NULL           |                       | {}        |   false   | false
  rowid       | INT8      |    false    | unique_rowid() |                       | {primary} |   true    | false
(3 rows)

-- 3. 向表中写入数据。

INSERT INTO bits VALUES (B'1', B'101');
INSERT 1

-- 4. 查看表的内容。

SELECT * FROM bits;
c1|c2
--+---
1 |101
(1 row)
```

### VARBIT

#### 类型描述

VARBIT 数据类型用于存储长度可变的二进制位数组。VARBIT 类型的值占用的位数如下表所示：

| 类型 | 逻辑大小 |
| ----------------------------------- | --------------------------------------- |
| VARBIT                              | 无最大值限制的可变长度                  |
| VARBIT(N)                           | 最多 N bit 的可变长度                   |

对于 VARBIT 类型，数值的宽度不能超过指定的最大宽度，否则系统会报错。

#### 示例

以下示例创建一个具有 VARBIT 列的表 `varbits` 并向表中写入数据。

```sql
-- 1. 创建表 varbits。

CREATE TABLE varbits (c1 VARBIT, c2 VARBIT(3));
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM varbits;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | VARBIT    |    true     | NULL           |                       | {}        |   false   | false
  c2          | VARBIT(3) |    true     | NULL           |                       | {}        |   false   | false
  rowid       | INT8      |    false    | unique_rowid() |                       | {primary} |   true    | false
(3 rows)

-- 3. 向表中写入数据。

INSERT INTO varbits VALUES (B'1', B'1');
INSERT 1

-- 4. 查看表的内容。

SELECT * FROM varbits;
c1|c2
--+--
1 |1
(1 row)
```

### BYTES

#### 类型描述

BYTES 数据类型存储指定长度的二进制字符串。向关系表中写入 BYTES 数据时，KWDB 按照字符检查长度。

| 名称  | 别名 | 存储空间 |
| ----- | ----------------------------------- | --------------------------------------- |
| BYTES | BYTEA                               | 0 ~ 1023 字节                             |

字节数组常量是一种用来表示固定字节数组值的语法。以下三种方式代表相同的字节数组：

- `b'abc'`：前缀 `b` 表示字节数组常量，后跟字母 a、b 和 c 表示字节数组的三个字节。
- `b'\141\142\143'`：前缀 `b` 表示字节数组常量，后跟反斜杠（`\`）转义的八进制值 `\141`、`\142` 和 `\143`，分别表示字母 a、b 和 c 的 ASCII 值。
- `b'\x61\x62\x63'`：前缀 `b` 表示字节数组常量，后跟反斜杠（`\`）转义的十六进制值 `\x61`、`\x62` 和 `\x63`，分别表示字母 a、b 和 c 的 ASCII 值。

除上述语法以外，BYTES 类型还支持使用字符串文字，包括在上下文中使用的语法：`...`、`e'...'` 和 `x'...'`

虽然 BYTES 值的总存储大小可变，但建议将其保持在 1 MB 以下以确保性能。如果超过该阈值，写入放大和其他因素可能导致性能显著下降。

#### 示例

以下示例创建一个具有 BYTES 列的表 `bytes` 并向表中写入数据。

```sql
-- 1. 创建表 bytes。

CREATE TABLE bytes (c1 INT PRIMARY KEY, c2 BYTES,c3 BYTEA);
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM bytes;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | INT4      |    false    | NULL           |                       | {primary} |   false   | false
  c2          | BYTES     |    true     | NULL           |                       | {}        |   false   | false
  c3          | BYTES     |    true     | NULL           |                       | {}        |   false   | false
(3 rows)

-- 3. 向表中写入数据。
INSERT INTO bytes(c1,c2) VALUES (1, b'\141\142\143'), (2, b'\x61\x62\x63'), (3, b'\141\x62\c');
INSERT 3

-- 4. 查看表的内容。

SELECT * FROM bytes;
  c1 |    c2    |  c3
-----+----------+-------
   1 | \x616263 | NULL
   2 | \x616263 | NULL
   3 | \x616263 | NULL
(3 rows)
```

### VARBYTES

#### 类型描述

VARBYTES 类型是一种可变长的二进制字符类型，以实际的二进制字符串长度存储数据。如果实际数据长度小于指定的最大长度，不会补齐。如果实际数据长度超过最大长度，则会报错。

VARBYTES 类型的数据基于二进制值进行存储和排序。

| 名称 | 存储空间 |
| ----------------------------------- | --------------------------------------- |
| VARBYTES                            | 0 ~ 64K 字节                           |

#### 示例

以下示例创建一个具有 VARBYTES 列的表 `varbytes` 并向表中写入数据。

```sql
-- 1. 创建表 varbytes。

CREATE TABLE varbytes (c1 INT PRIMARY KEY, c2 VARBYTES);
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM varbytes;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | INT4      |    false    | NULL           |                       | {primary} |   false   | false
  c2          | VARBYTES  |    true     | NULL           |                       | {}        |   false   | false
(2 rows)

-- 3. 向表中写入数据。

INSERT INTO varbytes(c1,c2) VALUES (1, b'\141\142\143'), (2, b'\x61\x62\x63'), (3, b'\141\x62\c');
INSERT 3

-- 4. 查看表的内容。

SELECT * FROM varbytes;
c1|c2
--+--------
1 |\x616263
2 |\x616263
3 |\x616263
(3 rows)
```

### CHAR

#### 类型描述

CHAR 类型是一种定长字符类型，其存储长度由指定长度确定。向关系表写入 CHAR 类型数据时，KWDB 按照长度限制检查长度。如果实际数据长度小于指定长度，不会补齐。如果实际数据长度超过指定长度，则会报错。

CHAR 类型通过 `CHAR(n)` 限制列的长度，`n` 是允许存储的最大 Unicode 代码点数，取值范围是正整数，且不能超过 `int32` 的最大值，即 `2147483647`。如果未指定长度，长度默认为 1。

| 名称 | 别名        |
| ---- | -----------| 
| CHAR | CHARACTER  |

#### 示例

以下示例创建一个具有 CHAR 列的表 `char` 并向表中写入数据。

```sql
-- 1. 创建表 char。

CREATE TABLE char (c1 STRING PRIMARY KEY, c2 CHARACTER, c3 CHAR);
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM char;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | STRING    |    false    | NULL           |                       | {primary} |   false   | false
  c2          | CHAR      |    true     | NULL           |                       | {}        |   false   | false
  c3          | CHAR      |    true     | NULL           |                       | {}        |   false   | false
(3 rows)

-- 3. 向表中写入数据。

INSERT INTO char VALUES ('a1b2c3d4', 's', '9');
INSERT 1

-- 4. 查看表的内容。

SELECT * FROM char;
c1      |c2|c3|
--------+--+--+
a1b2c3d4|s |9 |
(1 row)
```

### NCHAR

#### 类型描述

NCHAR 类型是一种定长字符类型，其存储长度由指定长度确定。当向关系表写入 NCHAR 类型数据时，KWDB 按照长度限制检查长度。如果实际数据长度小于指定长度，不会补齐。如果实际数据长度超过指定长度，则会报错。

NCHAR 类型通过 `NCHAR(n)` 限制列的长度，`n` 是允许存储的最大 Unicode 代码点数，取值范围是正整数，且不能超过 `int32` 的最大值，即 `2147483647`。如果未指定长度，长度默认为 1。

#### 示例

以下示例创建一个具有 NCHAR 列的表 `nchar` 并向表中写入数据。

```sql
-- 1. 创建表 nchar。

CREATE TABLE nchar(c1 NCHAR PRIMARY KEY);
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM nchar;
column_name|data_type|is_nullable|column_default|generation_expression|indices  |is_hidden
-----------+---------+-----------+--------------+---------------------+---------+---------
c1         |NCHAR    |f          |              |                     |{primary}|f
(1 row)

-- 3. 向表中写入数据。

INSERT INTO nchar VALUES ('a');
INSERT 1

-- 4. 查看表的内容。

SELECT * FROM nchar;
c1
--
a
(1 row)
```

### VARCHAR

#### 类型描述

VARCHAR 类型是一种可变长字符类型，存储长度由数据的实际长度确定。存储数据时，如果实际数据长度小于指定的最大长度，根据输入数据的字节实际长度进行存储，不会进行补齐。如果实际数据长度超过指定的最大长度，则会报错。

VARCHAR 类型支持通过 `VARCHAR(n)` 限制列的最大长度，其中 `n` 是允许存储的最大 Unicode 代码点数，取值范围是正整数，且不能超过 `int32` 的最大值，即 `2147483647`。如果未指定长度，则无长度限制。

#### 示例

以下示例创建一个具有 VARCHAR 列的表 `varchar` 并向表中写入数据。

```sql
-- 1. 创建表 varchar。

CREATE TABLE varchar (c1 STRING PRIMARY KEY, c2 VARCHAR, c3 varchar(5));
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM varchar;
  column_name | data_type  | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+------------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | STRING     |    false    | NULL           |                       | {primary} |   false   | false
  c2          | VARCHAR    |    true     | NULL           |                       | {}        |   false   | false
  c3          | VARCHAR(5) |    true     | NULL           |                       | {}        |   false   | false
(3 rows)

-- 3. 向表中写入数据。

INSERT INTO varchar VALUES ('a1b2c3d4', 's', 'e5f6');
INSERT 1

-- 4. 查看表的内容。

SELECT * FROM varchar;
     c1    | c2 |  c3
-----------+----+-------
  a1b2c3d4 | s  | e5f6
(1 row)
```

### NVARCHAR

#### 类型描述

NVARCHAR 类型是一种可变长字符类型，其存储长度由实际字符的长度确定。如果实际数据的长度小于指定的最大长度，不会进行末尾补齐。如果实际数据的长度超过指定的最大长度，则会报错。NVARCHAR 类型的数据存储使用固定的 Unicode 编码。

NVARCHAR 类型支持通过 `NVARCHAR(n)` 限制列的最大长度，其中 `n` 是允许存储的最大 Unicode 代码点数，取值范围是正整数，且不能超过 `int32` 的最大值，即 `2147483647`。如果未指定长度，则无长度限制。

#### 示例

以下示例创建一个具有 NVARCHAR 列的表 `nvarchar` 并向表中写入数据。

```sql
-- 1. 创建表 nvarchar。

CREATE TABLE nvarchar(c1 NVARCHAR PRIMARY KEY, c2 NVARCHAR(63), c3 NVARCHAR(254));
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM nvarchar;
  column_name |   data_type   | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+---------------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | NVARCHAR      |    false    | NULL           |                       | {primary} |   false   | false
  c2          | NVARCHAR(63)  |    true     | NULL           |                       | {}        |   false   | false
  c3          | NVARCHAR(254) |    true     | NULL           |                       | {}        |   false   | false
(3 rows)

-- 3. 向表中写入数据。

INSERT INTO nvarchar VALUES ('a1b2c3d4', 's', 'e5f6');
INSERT 1

-- 4. 查看表的内容。

SELECT * FROM nvarchar;
     c1    | c2 |  c3
-----------+----+-------
  a1b2c3d4 | s  | e5f6
(1 row)
```

### COLLATE

#### 类型描述

归类字符串是 SQL 常规字符串的一种使用方式，通常会伴随一个 COLLATE 子句。在定义列的时候，可以使用 COLLATE 子句指定字符串的排序规则，也可以使用 STRING 的别名表示字符串类型。例如：

```sql
CREATE TABLE collates (c1 STRING COLLATE en PRIMARY KEY, c2 TEXT COLLATE en);
```

上述示例中，`c1` 和 `c2` 列被声明为 STRING 类型，并且指定了 `en` 作为排序规则。用户也可以使用 COLLATE 子句指定特定的排序规则。例如：

```sql
INSERT INTO collates VALUES ('tianjin' COLLATE en,'KWDB' COLLATE en);
```

#### 示例

以下示例创建一个名为 `collates` 的表，为表列设置排序规则，并向表中写入数据。

```sql
-- 1. 创建表 collates，并设置列的默认排序规则为中文 (zh)。

CREATE TABLE collates (c1 STRING COLLATE zh PRIMARY KEY, c2 TEXT COLLATE zh);
CREATE TABLE

-- 2. 向表中写入数据。写入数据时，每个数据必须指定排序规则。

INSERT INTO collates VALUES ('北京' COLLATE zh, 'KWDB' COLLATE zh), ('济南' COLLATE zh, 'KWDB' COLLATE zh), ('天津' COLLATE zh, 'KWDB' COLLATE zh);
INSERT 3

-- 3. 查看表的内容。表中的数据将按照排序规则进行处理。

SELECT * FROM collates ORDER BY c1;
c1    | c2
------+--------
北京  | KWDB
济南  | KWDB
天津  | KWDB
(3 rows)

-- 4. 使用特定的排序规则排序。

SELECT * FROM collates ORDER BY c1 COLLATE cmn;
c1    | c2
------+------
北京  | KWDB
济南  | KWDB
天津  | KWDB
(3 rows)

SELECT * FROM collates ORDER BY c1 COLLATE yue;
c1    | c2
------+------
北京  | KWDB
济南  | KWDB
天津  | KWDB
(3 rows)

-- 5. 比较使用相同排序规则的字符串。系统返回结果正常。

SELECT 'A' COLLATE de < 'Ä' COLLATE de;
?column?
--------
t
(1 row)

-- 6. 比较使用不同排序规则的字符串，系统报错。

SELECT 'Ä' COLLATE sv < 'Ä' COLLATE de;
ERROR: unsupported comparison operator: <collatedstring{sv}> < <collatedstring{de}>


-- 7. 通过强制转换将带有排序规则的字符串转换为普通的字符串类型。

SELECT CAST(c1 AS STRING) FROM collates ORDER BY c1;
c1
----
北京
天津
济南
(3 rows)
```

## 日期和时间类型

### 时间戳

#### 类型描述

KWDB 关系数据库支持 TIMESTAMP 和 TIMESTAMPTZ 时间类型。

### 类型描述

时间戳包括 TIMESTAMP 和 TIMESTAMPTZ 两个变体。时间戳数值允许精确到毫秒，例如：`2020-02-12 07:23:25.123`。时间戳常量表示特定日期和时间值的固定值。通常情况下，时间戳常量不可更改。时间戳常量的格式为 `timestamp 'YYYY-MM-DD HH:MM:SS.SSS'`，例如 `timestamp '2023-10-19 15:30:00'`。

| 名称        | 别名                        | 描述                                                               |
| ----------- | --------------------------- | ------------------------------------------------------------------ |
| TIMESTAMP   | TIMESTAMP WITHOUT TIME ZONE | 以协调世界时（Coodinated Universal Time，UTC）格式存储日期和时间。 |
| TIMESTAMPTZ | TIMESTAMP WITH TIME ZONE    | 将时间戳数值从 UTC 时区转换为客户端会话时区。                      |

::: warning 说明

- KWDB 在存储 TIMESTAMPTZ 类型时不包含时区数据。
- KWDB 默认时区为 UTC。因此 TIMESTAMPTZ 的默认值与 TIMESTAMP 一致。

:::

KWDB 支持在查询中对列类型为时间戳、时间戳常量以及结果类型为时间戳的函数和表达式进行时间加减运算，运算结果支持使用大于号（`>`）、小于号（`<`）、等号（`=`）、大于等于号（`>=`）、小于等于号（`<=`）进行比较。有关详细信息，参见[简单查询](../dml/relational-db/relational-select.md)。

#### 示例

以下示例创建一个名为 `timestamps` 的表，包括 TIMESTAMP 和 TIMESTAMPTZ 时间戳类型的列，并向表中写入数据。

```sql
-- 1. 创建表 timestamps。

CREATE TABLE timestamps (c1 INT PRIMARY KEY, c2 TIMESTAMP, c3 TIMESTAMPTZ);
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM timestamps;
  column_name |  data_type  | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-------------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | INT4        |    false    | NULL           |                       | {primary} |   false   | false
  c2          | TIMESTAMP   |    true     | NULL           |                       | {}        |   false   | false
  c3          | TIMESTAMPTZ |    true     | NULL           |                       | {}        |   false   | false
(3 rows)

-- 3. 向表中写入数据。

INSERT INTO timestamps VALUES(1, TIMESTAMP '2023-03-26', TIMESTAMPTZ '2023-03-26 10:10:10-05:00');
INSERT 1

-- 4. 查看表的内容。

SELECT * FROM timestamps;
c1|c2                 |c3
--+-------------------+-------------------------
1 |2023-03-26 00:00:00|2023-03-26 15:10:10+00:00
(1 row)
```

### 日期

#### 类型描述

DATE 类型用于存储年、月、日信息。DATE 类型的常量值可以使用解释文本、DATE 类型注释、或者强制转换为 DATE 类型的字符串文本来表示。KWDB 也支持使用未解释的字符串文字输入 DATE 数值。DATE 的字符串格式为 `YYYY-MM-DD`，例如：`DATE '2016-12-23'`。DATE 类型的存储最多占用 16 个字节。但是，由于元数据的影响，实际存储大小可能会更大。

#### 示例

以下示例创建一个名为 `dates` 的表，并向表中写入数据。

```sql
-- 1. 创建表 dates。

CREATE TABLE dates (a DATE PRIMARY KEY, b INT);
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM dates;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  a           | DATE      |    false    | NULL           |                       | {primary} |   false   | false
  b           | INT4      |    true     | NULL           |                       | {}        |   false   | false
(2 rows)

-- 3. 向表中写入数据。

INSERT INTO dates VALUES (DATE '2016-03-26', 12345);
INSERT 1

-- 4. 查看表的内容。

SELECT * FROM dates;
              a             |   b
----------------------------+--------
  2016-03-26 00:00:00+00:00 | 12345
(1 row)

-- 5. 使用字符串向表中隐式写入 DATE 数据。

INSERT INTO dates VALUES ('2016-03-27', 12345);
INSERT 1

SELECT * FROM dates;
              a             |   b
----------------------------+--------
  2016-03-26 00:00:00+00:00 | 12345
  2016-03-27 00:00:00+00:00 | 12345
(2 rows)
```

### 时间

#### 类型描述

TIME 类型用于存储没有时区的时间信息。

| 名称 | 别名 |
| ----------------------------------- | ----------------------------------- |
| TIME                                | TIME WITHOUT TIME ZONE              |

TIME 类型的常量值可以使用解释文本、带有 TIME 类型注释的字符串文本或强制转换为 TIME 类型的字符串文本来表示。KWDB 也支持使用未解释的字符串文字输入 TIME 数值。TIME 类型的字符串格式为 `HH:MM:SS.SSSSSS`，例如：`TIME '05:40:00.000001'`。TIME 类型的小数部分可选，四舍五入到微秒级别（即小数点后的六位数）。TIME 类型支持的最大宽度为 8 个字节。但是，由于元数据的影响，实际存储大小可能会更大。

#### 示例

以下示例创建一个名为 `time` 的表，并向表中写入数据。

```sql
-- 1. 创建表 time。

CREATE TABLE time (time_id INT PRIMARY KEY, time_val TIME);
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM time;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  time_id     | INT4      |    false    | NULL           |                       | {primary} |   false   | false
  time_val    | TIME      |    true     | NULL           |                       | {}        |   false   | false
(2 rows)

-- 3. 向表中写入数据。

INSERT INTO time VALUES (1, TIME '05:40:00'), (2, TIME '05:41:39');
INSERT 2

-- 4. 查看表的内容。

 SELECT * FROM time;
  time_id |         time_val
----------+----------------------------
        1 | 0000-01-01 05:40:00+00:00
        2 | 0000-01-01 05:41:39+00:00
(2 rows)

-- 5. 比较 TIME 类型的数值。

SELECT (SELECT time_val FROM time WHERE time_id = 1) < (SELECT time_val FROM time WHERE time_id = 2);
?column?
--------
  true
(1 row)
```

### 间隔

#### 类型描述

INTERVAL 数据类型用于存储表示时间跨度的值。INTERVAL 类型的常量值可以使用解释文本、带有 INTERVAL 类型注释的字符串文本或强制转换为 INTERVAL 类型的字符串文本来表示。KWDB 也支持使用未解释的字符串文字输入 INTERVAL 数值。
INTERVAL 常量可以使用以下格式表示：

- 标准 SQL 格式：`INTERVAL 'Y-M D H:M:S'`
  - `Y-M D`：用单个数值定义天数，用两个数值定义年份和月份。数值必须为整数。
  - `H:M:S`：用单个数值定义秒，用两个数值定义小时和分钟。数值可以是整数或浮点数。每个部分都是可选的。
- ISO 8601 格式：`INTERVAL 'P1Y2M3DT4H5M6S'`

INTERVAL 列支持的最大宽度为 24 个字节。但是，由于元数据的影响，实际存储大小可能会更大。在 Kaiwu 数据库内部，INTERVAL 数据类型以月、天和微秒的形式进行存储。因此，从字符串解析或从浮点数或十进制数转换得到的数据将舍入到最接近的微秒。对 INTERVAL 进行的任何算术运算（加、减、乘、除）也将舍入到最接近的微秒。

#### 示例

以下示例创建一个名为 `intervals` 的表，并向表中写入数据。

::: warning 说明

如果将 `interval` 用作主键，则可能会导致唯一性问题。

:::

```sql
-- 1. 创建表 intervals。

CREATE TABLE intervals (c1 INT PRIMARY KEY, c2 interval);
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM intervals;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | INT4      |    false    | NULL           |                       | {primary} |   false   | false
  c2          | INTERVAL  |    true     | NULL           |                       | {}        |   false   | false
(2 rows)

-- 3. 向表中写入数据。

INSERT INTO intervals VALUES (1, interval '1 year 2 months 3 days 4 hours 5 minutes 6 seconds'),(2, interval '1-2 3 4:5:6'),(3, '1-2 3 4:5:6');
INSERT 3

-- 4. 查看表的内容。

SELECT * FROM intervals;
  c1 |              c2
-----+--------------------------------
   1 | 1 year 2 mons 3 days 04:05:06
   2 | 1 year 2 mons 3 days 04:05:06
   3 | 1 year 2 mons 3 days 04:05:06
(3 rows)
```

## JSONB 类型

### 类型描述

JSONB 数据类型用于以二进制形式存储 JSON 数据，便于消除空格、重复键和键顺序，并支持反向索引。

| 名称 | 别名 |
| ----------------------------------- | ----------------------------------- |
| JSONB                               | JSON                                |

JSONB 数据类型的语法遵循 RFC 8259 指定的格式。JSONB 值的常量可以使用解释文本或带有 JSONB 类型注释的字符串文本来表示。
JSONB 类型具有六种值类型：

- Null：空值。
- Boolean：布尔值。
- String：字符串值。
- Number：任意精度的数值，包括整数和小数，而不仅限于 INT64 范围内的整数。
- Array：有序的 JSONB 值序列。
- Object：从字符串到 JSONB 值的映射。例如，`'{"type": "account creation", "username": "harvestboy93"}'` 或 `'{"first_name": "Ernie", "status": "Looking for treats", "location": "Brooklyn"}'`。如果输入的字符串中包含重复键，JSONB 会保留最后一个出现的键值对，忽略之前的重复键值对。

### 示例

示例 1：以下示例创建一个具有 JSONB 列的表 `jsonb` 并向表中写入数据。

```sql

-- 1. 创建表 jsonb。

CREATE TABLE jsonbs (id INT8 DEFAULT unique_rowid(), name JSONB, PRIMARY KEY(id));
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM jsonbs;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  id          | INT8      |    false    | unique_rowid() |                       | {primary} |   false   | false
  name        | JSONB     |    true     | NULL           |                       | {}        |   false   | false
(2 rows)

-- 3. 向表中写入数据。

INSERT INTO jsonbs (name) VALUES ('{"first_name": "Lei", "last_name": "Li", "location": "Beijing"}'), ('{"first_name": "Meimei", "last_name": "Han", "location": "Beijing"}');
INSERT 2

-- 4. 查看表的内容。

SELECT * FROM jsonbs;
          id         |                                name
---------------------+----------------------------------------------------------------------
  960911294061182977 | {"first_name": "Lei", "last_name": "Li", "location": "Beijing"}
  960911294061314049 | {"first_name": "Meimei", "last_name": "Han", "location": "Beijing"}
(2 rows)

-- 5. 使用 jsonb_pretty() 函数检索格式化的 JSONB 数据。

 SELECT id, jsonb_pretty(name) FROM jsonbs;
          id         |        jsonb_pretty
---------------------+------------------------------
  960911294061182977 | {
                     |     "first_name": "Lei",
                     |     "last_name": "Li",
                     |     "location": "Beijing"
                     | }
  960911294061314049 | {
                     |     "first_name": "Meimei",
                     |     "last_name": "Han",
                     |     "location": "Beijing"
                     | }
(2 rows)

-- 6. 使用 -> 运算符检索 JSONB 值的特定字段。

SELECT name->'first_name', name->'location' FROM jsonbs;
  ?column? | ?column?
-----------+------------
  "Lei"    | "Beijing"
  "Meimei" | "Beijing"
(2 rows)

-- 7. 使用 ->> 运算符将 JSONB 字段值作为字符串值返回。

SELECT name->>'first_name', name->>'location' FROM jsonbs;
  ?column? | ?column?
-----------+-----------
  Lei      | Beijing
  Meimei   | Beijing
(2 rows)
```

示例 2：以下示例使用 JSONB 列和计算列创建一个名为 `student_profiles` 的表。示例中，主键 `id` 作为 `profile` 列中的字段进行计算。

```sql
-- 1. 创建表 student_profiles。

CREATE TABLE student_profiles (id STRING PRIMARY KEY AS (profile->>'id') STORED, profile JSONB);
CREATE TABLE

-- 2. 向表中写入数据。

INSERT INTO student_profiles (profile) VALUES ('{"id": "d78236", "name": "Ming Wang", "age": "16", "school": "No.4 High School", "credits": 120, "sports": "none"}'), ('{"name": "Lei Zhou", "age": "15", "id": "f98112", "school": "No.4 High School", "credits": 97}'), ('{"name": "Yang Sun", "school" : "No.8 High School", "id": "t63512", "credits": 100}');
INSERT 3

-- 3. 查看表的内容。

SELECT * FROM student_profiles;
    id   |                                                      profile
---------+---------------------------------------------------------------------------------------------------------------------
  d78236 | {"age": "16", "credits": 120, "id": "d78236", "name": "Ming Wang", "school": "No.4 High School", "sports": "none"}
  f98112 | {"age": "15", "credits": 97, "id": "f98112", "name": "Lei Zhou", "school": "No.4 High School"}
  t63512 | {"credits": 100, "id": "t63512", "name": "Yang Sun", "school": "No.8 High School"}
(3 rows)
```

## 数组类型

### 类型描述

数组类型（ARRAY）是一种存储单索引、一维、相同类型元素的数组。ARRAY 不支持嵌套数组，也无法在数组上创建数据库索引或按数组进行排序。
ARRAY 类型有以下两种表达方式：

- 在任何非数组数据类型后面添加方括号（`[]`）。
- 在任何非数组数据类型前面添加关键字 ARRAY。

虽然 ARRAY 值的总存储大小可变，但建议将其保持在 1 MB 以下以确保性能。如果超过该阈值，写入放大和其他因素可能导致性能显著下降。

### 示例

示例 1：以下示例创建一个名为 `arrays` 的表，采用添加方括号的形式创建数组列，并向表中写入数据。

```sql
-- 1. 创建表 arrays。

CREATE TABLE arrays (b STRING[]);
CREATE TABLE

-- 2. 向表中写入数据。

INSERT INTO arrays VALUES (ARRAY['sky', 'road', 'car']);
INSERT 1

-- 3. 查看表的内容。

SELECT * FROM arrays;
b
--------------
{sky,road,car}
(1 row)
```

示例 2：以下示例创建一个名为 `c` 的表，采用添加关键字 `ARRAY` 的形式创建数组列，并向表中写入数据。

```sql
-- 1. 创建表 c。

CREATE TABLE c (d INT ARRAY);
CREATE TABLE

-- 2. 向表中写入数据。

INSERT INTO c VALUES (ARRAY[10,20,30]);
INSERT 1

-- 3. 查看表的内容。

SELECT * FROM c;
d
----------
{10,20,30}
(1 row)

-- 4. 使用数组索引访问数组元素。 KWDB 中的数据是单索引的。

SELECT d[2] FROM c;
d
--
20
(1 row)

-- 5. 使用 array_append 函数将元素追加到数组中。

UPDATE c SET d = array_append(d, 40) WHERE d[3] = 30;
UPDATE 1

-- 6. 查看表的内容。

SELECT * FROM c;
d
-------------
{10,20,30,40}
(1 row)

-- 7. 使用 append（||）运算符将元素追加到数组中。

UPDATE c SET d = d || 50 WHERE d[4] = 40;
UPDATE 1

-- 8. 查看表的内容。

SELECT * FROM c;
d
----------------
{10,20,30,40,50}
(1 row)
```

## INET 类型

### 类型描述

INET 数据类型用于存储 IPv4 或 IPv6 地址。INET 的常量值可以使用解释文本、类型 INET 注释的字符串文本，或者强制类型转换为类型 INET 来表示。
INET 常量可以使用以下格式表示：

- IPv4 地址：RFC 791 标准指定的 4 个八位字节格式，以十进制数字表示，并以句点（`.`）分隔。IPv4 地址选择是否带有子网掩码。例如，`'190.0.0.0'`、`'190.0.0.0 / 24'`。
- IPv6 地址：RFC8 200 标准指定的 8 个冒号（`:`）分隔的 4 个十六进制数字组。IPv6 地址可以映射为 IPv4 地址。IPv6 地址可选择是否带有子网掩码。例如 `'2001:4f8:3:ba:2e0:81ff:fe22:d1f1'`、`'::ffff:192.168.0.1/24'`、`'2001:4f8:3:ba:2e0:81ff:fe22:d1f1/120'`。

IPv4 格式的 INET 数据类型占用 32 位。IPv6 格式的 INET 数据类型，占用 128 位。因此，IPv4 地址将在 IPv6 地址之前排序，包括 IPv4 地址映射的 IPv6 地址。

### 示例

以下示例创建一个名为 `inets` 的表，并向表中写入数据。

```sql
-- 1. 创建表 inets。

CREATE TABLE inets(c1 INET PRIMARY KEY);
CREATE TABLE

-- 2. 查看表的列。

SHOW COLUMNS FROM inets;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | INET      |    false    | NULL           |                       | {primary} |   false   | false
(1 row)

-- 3. 向表中写入数据。

INSERT INTO inets VALUES ('192.168.0.1'),('192.168.0.2/10'), ('2001:4f8:3:ba:2e0:81ff:fe22:d1f1/120');
INSERT 3

-- 4. 查看表的内容。

SELECT * FROM inets;
c1
------------------------------------
192.168.0.2/10
192.168.0.1
2001:4f8:3:ba:2e0:81ff:fe22:d1f1/120
(3 rows)
```

## UUID 类型

### 类型描述

UUID（Universally Unique Identifier，通用唯一标识符）数据类型用于存储 128 位的数值，该值在空间和时间上都是唯一的。为了自动生成唯一的行标识符，建议使用带有 `gen_random_uuid()` 函数的 UUID 作为默认值。
UUID 值支持使用以下格式表示：

- RFC 4122 标准指定的格式，由连字符（`-`）隔开的 `8-4-4-4-12` 个十六进制数字组成。例如：`acde070d-8c4c-4f0d-9d8a-162843c10333`。
- RFC 4122 标准指定的格式，并带有大括号（`}`）。例如：`{acde070d-8c4c-4f0d-9d8a-162843c10333}`。
- 字节格式，例如，`b'kafef00ddeadbeed'`。
- 用作 URN（Uniform Resource Name，统一资源名称），格式为 `"urn:uuid:"` + RFC 4122 标准指定的格式。例如：`urn:uuid:63616665-6630-3064-6465-616462656564`。

UUID 值的宽度为 128 位。但是，由于元数据的影响，实际存储大小可能会更大。

### 示例

示例 1：以下示例创建一个名为 `uuids` 的表，并向表中写入数据。

```sql
-- 1. 创建表 uuids。

CREATE TABLE uuids (token UUID);
CREATE TABLE

-- 2. 向表中写入符合 RFC 4122 标准指定格式的 UUID 数值。

INSERT INTO uuids VALUES ('63616665-6630-3064-6465-616462656562');
INSERT 1

-- 3. 查看表的内容。

SELECT * FROM uuids;
token
------------------------------------
63616665-6630-3064-6465-616462656562
(1 row)

-- 4. 向表中写入带大括号的格式的 UUID 数值。

INSERT INTO uuids VALUES ('{63616665-6630-3064-6465-616462656563}');
INSERT 1

-- 5. 查看表的内容。

SELECT * FROM uuids;
token
------------------------------------
63616665-6630-3064-6465-616462656562
63616665-6630-3064-6465-616462656563
(2 rows)

-- 6. 向表中写入字节格式的 UUID 数值。

INSERT INTO uuids VALUES (b'kafef00ddeadbeed');
INSERT 1

-- 7. 查看表的内容。

SELECT * FROM uuids;
token
------------------------------------
63616665-6630-3064-6465-616462656562
63616665-6630-3064-6465-616462656563
6b616665-6630-3064-6465-616462656564
(3 rows)

-- 8. 向表中写入 URN 格式的 UUID 数值。

INSERT INTO uuids VALUES ('urn:uuid:63616665-6630-3064-6465-616462656564');
INSERT 1

-- 9. 查看表的内容。

SELECT * FROM uuids;
token
------------------------------------
63616665-6630-3064-6465-616462656562
63616665-6630-3064-6465-616462656563
6b616665-6630-3064-6465-616462656564
63616665-6630-3064-6465-616462656564
(4 rows)
```

示例 2：使用带有 `gen_random_uuid()` 函数的 UUID 列作为默认值，创建一个包含自动生成的唯一行 ID 的表 `user`。

::: warning 说明
示例 2 和示例 3 中生成的 ID 都是 128 位，几乎不太可能生成重复的值。一旦表超出了单个键值范围（默认情况下，超过 64 MB），新的 ID 将分布在表的所有范围内，因此可能分布在不同的节点上。这意味着多个节点将共享负载。
这种方法虽然创建了一个主键，但是该主键可能在直接查询中没有直接用途，可能需要与另一个表或辅助索引连接。如果要将生成的 ID 存储在相同的键值范围内，可以显式地或通过 SERIAL 伪类型将整数类型与 `unique_rowid()` 函数用作默认值。
:::

```sql
-- 1. 创建表 user。

CREATE TABLE users (id UUID NOT NULL DEFAULT gen_random_uuid(), name STRING, PRIMARY KEY(id, name));
CREATE TABLE

-- 2. 向表中写入数据。

INSERT INTO users(name) VALUES ('小蓝'), ('小红'), ('小白');
INSERT 3
```

示例 3：使用带有 `uuid_v4()` 函数的 BYTES 列作为默认值，来创建一个包含自动生成的唯一行 ID 的表 `user2`。

```sql
-- 1. 创建表 user2。

CREATE TABLE users2 (id BYTES DEFAULT uuid_v4(), name STRING, PRIMARY KEY(id, name));
CREATE TABLE

-- 2. 向表中写入数据。

INSERT INTO users2(name) VALUES ('小蓝'), ('小红'), ('小白');
INSERT 3

-- 3. 查看表的内容。

SELECT * FROM users2;
id                                |name
----------------------------------+----
\x4a54c55174de428caebe9886cb663d9e|小蓝
\xaa28838b33384766baa34a82ea00dd3a|小白
\xe378c650f45c41a3b231ecf4fddad8c8|小红
(3 rows)
```

示例 4：使用带有 `unique_rowid()` 函数的 INT8 列作为默认值，来创建一个包含自动生成的唯一行 ID 的表 `user3`。

::: warning 说明
在执行写入操作时，`unique_rowid()` 函数会根据执行写入的节点的时间戳和 ID 生成默认值。只有在每个节点每秒生成大量 ID（超过 100,000 个）时，这些基于时间排序的值才有可能重复。然而，由于时间戳的差异，不能完全保证写入顺序绝对一致。
:::

```sql
-- 1. 创建表 user2。

CREATE TABLE users3 (id INT8 DEFAULT unique_rowid(), name STRING, PRIMARY KEY(id, name));
CREATE TABLE

-- 2. 向表中写入数据。

INSERT INTO users3(name) VALUES ('小蓝'), ('小红'), ('小白');
INSERT 3

-- 3. 查看表的内容。

SELECT * FROM users3;
id                |name
------------------+----
858541035522097153|小蓝
858541035522129921|小红
858541035522162689|小白
(3 rows)
```