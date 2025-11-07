---
title: Relational Data Types
id: data-type-relational-db
---

# Relational Data Types

KWDB relational databases support the following data types:

- Numeric types
- BOOL types
- String types
- Date and time types
- JSON
- Array
- INET
- UUID

## Numeric Types

KWDB relational databases support integer, floating-point, decimal, and SERIAL numeric types.

::: tip

- To generate auto-incrementing globally unique values (such as primary keys), use the UUID or SERIAL type.
- For digits with arbitrary precision, use the DECIMAL type.

:::

### Integer Types

#### Basic Information

KWDB supports various signed integer data types.

| Name | Alias                | Storage Space | Range                                       |
|------|----------------------|---------------|---------------------------------------------|
| INT2 | SMALLINT             | 2 bytes       | -32768 ~ +32767                             |
| INT4 | - INT <br>- INTEGER  | 4 bytes       | -2147483648 ~ +2147483647                   |
| INT8 | - INT64 <br>- BIGINT | 8 bytes       | -9223372036854775808 ~ +9223372036854775807 |

::: warning Note

- A constant value of an integer type can be entered as a numeric literal. For example, `42`, `-1234` or `0xCAFE`.
- The different integer types place different constraints on the range of allowable values, but all integers are stored in the same way regardless of the type. Smaller values take up less space than larger ones. For example, `42` takes up less space than `2147483647`.

:::

#### Data Type Conversions and Casts

INTEGER-typed values can be cast to any of the following data types.

| Type | Description |
| --- | --- |
| BIT | Convert the INTEGER-typed value to the corresponding binary value, and truncate or pad it according to the length of the converted BIT type. If the INTEGER type is shorter than the BIT type, add zero padding to the front of the data.  |
| BOOL | `0` converts to `false`. All other values convert to `true`. |
| FLOAT | - |
| DECIMAL | - |
| STRING | Convert the INTEGER-typed value to the corresponding STRING-typed value and truncate it based on the converted STRING type. |
| DATE | Convert to days since Jan. 1, 1970. |
| TIMESTAMP | Convert to milliseconds since Jan. 1, 1970.|
| TIMESTAMPTZ | Convert to milliseconds since Jan. 1, 1970. |
| INTERVAL | Convert to seconds since Jan. 1, 1970. |

#### Examples

This example creates a table with INTEGER-typed columns.

```sql
-- 1. Create a table named ints.

CREATE TABLE ints(c1 INT PRIMARY KEY, c2 SMALLINT, c3 BIGINT, c4 INTEGER, c5 INT2, c6 INT4, c7 INT8, c8 INT64);
CREATE TABLE

-- 2. Check columns of the table.

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

### Floating-Point Types

#### Basic Information

KWDB supports FLOAT4 and FLOAT8 floating-point types, with the maximum precision of 17 decimal digits. A constant value of a floating-point type can be entered as a numeric literal. For example, `1.414` or `1234`.

| Name   | Alias                                        | Storage Space |
|--------|----------------------------------------------|---------------|
| FLOAT8 | - DOUBLE <br> - DOUBLE PRECISION <br>- FLOAT | 8 bytes       |
| FLOAT4 | REAL                                         | 4 bytes       |

A FLOAT-typed column supports values up to 8 bytes in width, but the total storage size is likely to be larger due to KWDB metadata.

Floating-point types are handled internally using the standard double-precision (64-bit binary-encoded) IEEE754 format. The special IEEE754 values for positive infinity, negative infinity and NaN (Not-a-Number) cannot be entered using numeric literals directly and must be converted using an interpreted literal or an explicit conversion from a string literal instead.

The following values are recognized:

| Value              | Syntax                                          |
|--------------------|-------------------------------------------------|
| Positive infinity  | - inf <br>- infinity <br>- +inf <br>- +infinity |
| Negative infinity  | - -inf <br>- -infinity                          |
| NaN (Not-a-Number) | nan                                             |

For example,

- `FLOAT '+Inf'`
- `'-Inf'::FLOAT`
- `CAST('NaN' AS FLOAT)`

#### Data Type Conversions and Casts

Floating-point-typed values can be cast to any of the following data types.

| Type | Description |
| --- | --- |
| BOOL | `0` converts to `false`. All other values convert to `true`. |
| INT | The system returns an error if the value is NaN or +/- Inf.|
| FLOAT | Lose precision when converting the floating-point-typed value to the corresponding FLOAT4-typed value.|
| DECIMAL | Convert the floating-point-typed value to the corresponding DECIMAL-typed value and truncate it based on the converted DECIMAL type. |
| STRING | Convert the floating-point-typed value to the corresponding STRING-typed value and truncate it based on the converted STRING type.|
| INTERVAL | - |

#### Examples

This example creates a table with floating-point-typed columns, inserts data into the table, and then uses the `CAST` function to limit the floating-point-typed columns.

```sql
-- 1. Create a table named floats.

CREATE TABLE floats (c1 FLOAT PRIMARY KEY, c2 REAL, c3 DOUBLE PRECISION);
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM floats;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | FLOAT8    |    false    | NULL           |                       | {primary} |   false   | false
  c2          | FLOAT4    |    true     | NULL           |                       | {}        |   false   | false
  c3          | FLOAT8    |    true     | NULL           |                       | {}        |   false   | false
(3 rows)

-- 3. Insert data into the floating-point-typed columns.

INSERT INTO floats VALUES (3.141592653834231235345, 2.718281828459, CAST('+Inf' AS FLOAT)),(FLOAT'-inf',1e1,'nan'::FLOAT);
INSERT 2

-- 4. Check data of the table. 

SELECT * FROM floats;
c1              |c2       |c3
----------------+---------+----
-Inf            |10.000000|NaN
3.14159265383423|2.718282 |+Inf
(2 rows)
```

### DECIMAL

#### Basic Information

The DECIMAL data type stores exact, fixed-point numbers. This type is used when it is important to preserve exact precision, for example, with monetary data. A constant value of the DECIMAL type can be entered as a numeric literal. For example, `1.414` or `-1234`.

| Name    | Alias               | Storage Space |
|---------|---------------------|---------------|
| DECIMAL | - DEC <br>- NUMERIC | 9 ~ 64K bytes |

The special IEEE754 values for positive infinity, negative infinity and NaN (Not-a-Number) cannot be entered using numeric literals directly and must be converted using an interpreted literal or an explicit conversion from a string literal instead.

The following values are recognized:

| Value              | Syntax                                          |
|--------------------|-------------------------------------------------|
| Positive infinity  | - inf <br>- infinity <br>- +inf <br>- +infinity |
| Negative infinity  | - -inf <br>- -infinity                          |
| NaN (Not-a-Number) | nan                                             |

To limit a DECIMAL-typed column, use `DECIMAL(precision, scale)`, where `precision` is the maximum count of digits both to the left and right of the decimal point and `scale` is the exact count of digits to the right of the decimal point. The `precision` must not be smaller than the `scale`. Using `DECIMAL(precision)` is equivalent to `DECIMAL(precision, 0)`.

::: warning Note

When inserting a DECIMAL value:

- If digits to the right of the decimal point exceed the column's `scale`, KWDB rounds to the `scale`.
- If digits to the right of the decimal point are fewer than the column's `scale`, KWDB pads to the `scale` with 0s.
- If digits to the left and right of the decimal point exceed the column's `precision`, KWDB returns an error.
- If the column's `precision` and `scale` are identical, the inserted value must round to less than 1.
:::

#### Data Type Conversions and Casts

DECIMAL-typed values can be cast to any of the following data types.

| Type | Description |
| --- | --- |
| BOOL | `0` converts to `false`. All other values convert to `true`. |
| INT | The system returns an error if the value is NaN or +/- Inf.|
| FLOAT | Lose precision when converting the DECIMAL-typed value to the corresponding FLOAT4-typed value.|
| STRING | Convert the DECIMAL-typed value to the corresponding STRING-typed value and truncate it based on the converted STRING type.|
| INTERVAL | - |

#### Examples

This example creates a table with DECIMAL-typed columns and then inserts data into the table.

```sql
-- 1. Create a table named decimals.

CREATE TABLE decimals(c1 DECIMAL PRIMARY KEY, c2 DEC, c3 NUMERIC, c4 DECIMAL(3), c5 DECIMAL(10, 2));
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM decimals;
  column_name |   data_type   | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+---------------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | DECIMAL       |    false    | NULL           |                       | {primary} |   false   | false
  c2          | DECIMAL       |    true     | NULL           |                       | {}        |   false   | false
  c3          | DECIMAL       |    true     | NULL           |                       | {}        |   false   | false
  c4          | DECIMAL(3)    |    true     | NULL           |                       | {}        |   false   | false
  c5          | DECIMAL(10,2) |    true     | NULL           |                       | {}        |   false   | false
(5 rows)

-- 3. Insert data into the table. The value in column c1 matches what is inserted exactly. The value in column c2 has been rounded to the column's scale. The value in column c3 is handled like the value in column c1 because NUMERIC is an alias for DECIMAL.

INSERT INTO decimals VALUES (1.01234567890123456789, 1.01234567890123456789, 1.01234567890123456789),(DECIMAL'+inf','-inf'::DEC,CAST('nan' AS NUMERIC));
INSERT 2

-- 4. Check data of the table.

SELECT * FROM decimals;
c1                    |c2                    |c3                    |c4|c5
----------------------+----------------------+----------------------+--+--
1.01234567890123456789|1.01234567890123456789|1.01234567890123456789|  |
Infinity              |-Infinity             |NaN                   |  |
(2 rows)
```

### SERIAL

#### Basic Information

The SERIAL data type is a keyword that can be used to replace a real data type when defining table columns. It is approximately equivalent to using an integer type with a `DEFAULT` expression that generates different values every time it is evaluated. This default expression in turn ensures that inserts that do not specify this column will receive an automatically generated value instead of NULL. The real data type of SERIAL is INT8. By default, it is the value that is automatically generated using the `unique_rowid()` function.

#### Examples

This example creates a table with a SERIAL-typed column as the primary key. Therefore, it can auto-generate unique IDs on insert.

```sql
-- 1. Create a table named serial.

CREATE TABLE serial (c1 SERIAL PRIMARY KEY, c2 STRING, c3 BOOL);
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM serial;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | INT8      |    false    | unique_rowid() |                       | {primary} |   false   | false
  c2          | STRING    |    true     | NULL           |                       | {}        |   false   | false
  c3          | BOOL      |    true     | NULL           |                       | {}        |   false   | false
(3 rows)

-- 3. Insert rows without values in column c1.

INSERT INTO serial (c2,c3) VALUES ('one', true), ('two', false), ('three', true);
INSERT 3

-- 4. Check data of the table. Each row has a default unique value in column c1.

SELECT * FROM serial;
          c1         |  c2   |  c3
---------------------+-------+--------
  960684591614623745 | one   | true
  960684591614754817 | two   | false
  960684591614787585 | three | true
(4 rows)
```

## BOOL Types

### Basic Information

The BOOL data type stores a Boolean value of `false` or `true`. A BOOL-typed column supports values up to 1 byte in width, but the total storage size is likely to be larger due to KWDB metadata.

| Name | Alias   | Storage Space |
|------|---------|---------------|
| BOOL | BOOLEAN | 1 byte        |

There are two predefined named constants for BOOL: `TRUE` and `FALSE` (the names are case-insensitive).

A boolean value can be obtained by coercing a numeric value. Zero is coerced to `FALSE`, and any non-zero value to `TRUE`.

- `CAST(0 AS BOOL) (false)`
- `CAST(119 AS BOOL) (true)`

### Data Type Conversions and Casts

BOOL-typed values can be cast to any of the following data types.

| Type | Description |
| --- | --- |
| INT | Convert `true` to `1`, `false` to `0`.|
| FLOAT | Convert `true` to `1`, `false` to `0`.|
| DECIMAL | Convert `true` to `1`, `false` to `0`. |
| STRING | - |

### Examples

This example creates a table with BOOL-typed columns and then inserts data into the table.

```sql
-- 1. Create a table named bools.

CREATE TABLE bools (c1 INT PRIMARY KEY, c2 BOOL, c3 BOOLEAN);
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM bools;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | INT4      |    false    | NULL           |                       | {primary} |   false   | false
  c2          | BOOL      |    true     | NULL           |                       | {}        |   false   | false
  c3          | BOOL      |    true     | NULL           |                       | {}        |   false   | false
(3 rows)

-- 3. Insert data into the table.

INSERT INTO bools VALUES (1, true, CAST(0 AS BOOL)),(2,false,CAST(3.14 AS BOOLEAN));
INSERT 2

-- 4. Check data of the table.

SELECT * FROM bools;
  c1 |  c2   |  c3
-----+-------+--------
   1 | true  | false
   2 | false | true
(2 rows)
```

## String Types

### BIT

#### Basic Information

The BIT data type stores fixed-length bit arrays. Bit array constants are expressed as literals. For example, `B'100101'` represents an array of 6 bits. The number of bits in a BIT value is determined as follows:

| Type   | Logical Size |
|--------|--------------|
| BIT    | 1 bit        |
| BIT(N) | N bits       |

For BIT and BIT(N) types, the value must match exactly the specified size. Otherwise, KWDB returns an error. The effective size of a BIT value is larger than its logical number of bits by a bounded constant factor. Internally, KWDB stores bit arrays in increments of 64 bits plus an extra integer value to encode the length. The total size of a BIT value can be arbitrarily large, but it is recommended to keep values under 1 MB to ensure performance. Above that threshold, write amplification and other considerations may cause significant performance degradation.

#### Data Type Conversions and Casts

BIT-typed values can be cast to any of the following data types.

| Type | Description |
| --- | --- |
| VARBIT | Convert the BIT-typed value to the corresponding VARBIT-typed value, and truncate or pad it according to the length of the converted VARBIT type. If the BIT type is shorter than the VARBIT type, add zero padding to the end of the data.  |
| INT | Convert the BIT-typed value to the corresponding INTEGER-typed value and get the value of the BIT type according to the length of the converted INTEGER type. |
| STRING | Convert the BIT-typed value to the corresponding STRING-typed value and truncate it based on the converted STRING type. |

#### Examples

This example creates a table with BIT-typed columns and then inserts data into the table.

```sql
-- 1. Create a table named bits.

CREATE TABLE bits (c1 BIT, c2 BIT(3));
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM bits;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | BIT       |    true     | NULL           |                       | {}        |   false   | false
  c2          | BIT(3)    |    true     | NULL           |                       | {}        |   false   | false
  rowid       | INT8      |    false    | unique_rowid() |                       | {primary} |   true    | false
(3 rows)

-- 3. Insert data into the table.

INSERT INTO bits VALUES (B'1', B'101');
INSERT 1

-- 4. Check data of the table.

SELECT * FROM bits;
c1|c2
--+---
1 |101
(1 row)
```

### VARBIT

#### Basic Information

The VARBIT data type stores variable-length bit arrays. The number of bits in a VARBIT value is determined as follows:

| Type      | Logical Size                      |
|-----------|-----------------------------------|
| VARBIT    | Variable with no maximum          |
| VARBIT(N) | Variable with a maximum of N bits |

For the VARBIT type, the value must not be larger than the specified maximum size. Otherwise, KWDB returns an error.

#### Examples

This example creates a table with VARBIT-typed columns and then inserts data into the table.

```sql
-- 1. Create a table named varbits.

CREATE TABLE varbits (c1 VARBIT, c2 VARBIT(3));
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM varbits;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | VARBIT    |    true     | NULL           |                       | {}        |   false   | false
  c2          | VARBIT(3) |    true     | NULL           |                       | {}        |   false   | false
  rowid       | INT8      |    false    | unique_rowid() |                       | {primary} |   true    | false
(3 rows)

-- 3. Insert data into the table.

INSERT INTO varbits VALUES (B'1', B'1');
INSERT 1

-- 4. Check data of the table.

SELECT * FROM varbits;
c1|c2
--+--
1 |1
(1 row)
```

### BYTES

#### Basic Information

The BYTES data type stores fixed-length binary strings. When inserting BYTES values into a relational table, KWDB will check the length of the value based on the characters.

| Name  | Alias | Storage Space  |
|-------|-------|----------------|
| BYTES | BYTEA | 0 ~ 1023 bytes |

The byte array constant is a syntax that is used to express fixed byte arrays. The following three byte array literals are equivalent for the same byte array:

- `b'abc'`: the prefix `b` represents the byte array constant, followed by letters a, b, and c. The three letters represent three bytes of the byte array.
- `b'\141\142\143'`: the prefix `b` represents the byte array constant, followed by the backslash (`\`) escaped octal values `\141`, `\142`, and `\143`, which represent the ASCII values of the letters a, b, and c respectively.
- `b'\x61\x62\x63'`: the prefix `b` represents the byte array constant, followed by the backslash (`\`) escaped hexadecimal values `\x61`, `\x62`, and `\x63`, which represent the ASCII values of the letters a, b, and c respectively.

In addition to the above syntaxes, KWDB also supports using string literals, including the syntax `'...'`, `e'...'` and `x'....'` in contexts for a byte array.

The size of a BYTES value is variable, but it is recommended to keep values under 1 MB to ensure performance. Above that threshold, write amplification and other considerations may cause significant performance degradation.

#### Data Type Conversions and Casts

BYTES-typed values can be cast to any of the following data types.

| Type | Description |
| --- | --- |
| STRING | Convert the BYTES-typed value to the corresponding STRING-typed value and truncate it based on the converted STRING type.|
| UUID | - |

#### Examples

This example creates a table with BYTES-typed columns and then inserts data into the table.

```sql
-- 1. Create a table named bytes.

CREATE TABLE bytes (c1 INT PRIMARY KEY, c2 BYTES,c3 BYTEA);
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM bytes;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | INT4      |    false    | NULL           |                       | {primary} |   false   | false
  c2          | BYTES     |    true     | NULL           |                       | {}        |   false   | false
  c3          | BYTES     |    true     | NULL           |                       | {}        |   false   | false
(3 rows)

-- 3. Insert data into the table.
INSERT INTO bytes(c1,c2) VALUES (1, b'\141\142\143'), (2, b'\x61\x62\x63'), (3, b'\141\x62\c');
INSERT 3

-- 4. Check data of the table.

SELECT * FROM bytes;
  c1 |    c2    |  c3
-----+----------+-------
   1 | \x616263 | NULL
   2 | \x616263 | NULL
   3 | \x616263 | NULL
(3 rows)
```

### VARBYTES

#### Basic Information

VARBYTES-typed values are variable-length strings. The maximum size of VARBYTES-typed values is subject to the column's length limit.

- If the value is shorter than the column's length limit, KWDB stores the value with its actual length and does not add space padding to the end of the value.
- If the value exceeds the column's length limit, KWDB returns an error.

VARBYTES-typed values are stored and sorted based on binary values.

| Name     | Storage Space |
|----------|---------------|
| VARBYTES | 0 ~ 64K bytes |

#### Examples

This example creates a table with VARBYTES-typed columns and then inserts data into the table.

```sql
-- 1. Create a table named varbytes.

CREATE TABLE varbytes (c1 INT PRIMARY KEY, c2 VARBYTES);
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM varbytes;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | INT4      |    false    | NULL           |                       | {primary} |   false   | false
  c2          | VARBYTES  |    true     | NULL           |                       | {}        |   false   | false
(2 rows)

-- 3. Insert data into the table.

INSERT INTO varbytes(c1,c2) VALUES (1, b'\141\142\143'), (2, b'\x61\x62\x63'), (3, b'\141\x62\c');
INSERT 3

-- 4. Check data of the table.

SELECT * FROM varbytes;
c1|c2
--+--------
1 |\x616263
2 |\x616263
3 |\x616263
(3 rows)
```

### CHAR

#### Basic Information

| Name | Alias     |
|------|-----------|
| CHAR | CHARACTER |

CHAR-typed values are fixed-length strings. The length of a CHAR-typed value is fixed to the length that you declare when you create the table.

- If the value is shorter than the column's length limit, KWDB stores the value with its actual length and does not add space padding to the end of the value.
- If the value exceeds the column's length limit, KWDB returns an error.

To limit the length of a CHAR-typed value, use `CHAR(n)`, where `n` represents the maximum number of Unicode code points allowed. A CHAR-typed value is an integer but cannot exceed the maximum value of INT32 (`2147483647`). If no length is specified, it is set to 1 by default.

| Name | Alias     |
|------|-----------|
| CHAR | CHARACTER |

#### Examples

This example creates a table with CHAR-typed columns and then inserts data into the table.

```sql
-- 1. Create a table named char.

CREATE TABLE char (c1 STRING PRIMARY KEY, c2 CHARACTER, c3 CHAR);
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM char;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | STRING    |    false    | NULL           |                       | {primary} |   false   | false
  c2          | CHAR      |    true     | NULL           |                       | {}        |   false   | false
  c3          | CHAR      |    true     | NULL           |                       | {}        |   false   | false
(3 rows)

-- 3. Insert data into the table.

INSERT INTO char VALUES ('a1b2c3d4', 's', '9');
INSERT 1

-- 4. Check data of the table.

SELECT * FROM char;
c1      |c2|c3|
--------+--+--+
a1b2c3d4|s |9 |
(1 row)
```

### NCHAR

#### Basic Information

NCHAR-typed values are fixed-length strings. The length of a NCHAR-typed value is fixed to the length that you declare when you create the table.

- If the value is shorter than the column's length limit, KWDB stores the value with its actual length and does not add space padding to the end of the value.
- If the value exceeds the column's length limit, KWDB returns an error.

To limit the length of a NCHAR-typed value, use `NCHAR(n)`, where `n` represents the maximum number of Unicode code points allowed. A NCHAR-typed value is an integer but cannot exceed the maximum value of INT32 (`2147483647`). If no length is specified, it is set to 1 by default.

#### Examples

This example creates a table with NCHAR-typed columns and then inserts data into the table.

```sql
-- 1. Create a table named nchar.

CREATE TABLE nchar(c1 NCHAR PRIMARY KEY);
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM nchar;
column_name|data_type|is_nullable|column_default|generation_expression|indices  |is_hidden
-----------+---------+-----------+--------------+---------------------+---------+---------
c1         |NCHAR    |f          |              |                     |{primary}|f
(1 row)

-- 3. Insert data into the table.

INSERT INTO nchar VALUES ('a');
INSERT 1

-- 4. Check data of the table.

SELECT * FROM nchar;
c1
--
a
(1 row)
```

### VARCHAR

#### Basic Information

VARCHAR-typed values are variable-length strings. The maximum size of VARCHAR-typed values is subject to the column's length limit.

- If the value is shorter than the column's length limit, KWDB stores the value with its actual length and does not add space padding to the end of the value.
- If the value exceeds the column's length limit, KWDB returns an error.

To limit the length of a VARCHAR-typed value, use `VARCHAR(n)`, where `n` represents the maximum number of Unicode code points allowed. A VARCHAR-typed value is an integer but cannot exceed the maximum value of INT32 (`2147483647`). If no length is specified, there is no length limit.

#### Examples

This example creates a table with VARCHAR-typed columns and then inserts data into the table.

```sql
-- 1. Create a table named varchar.

CREATE TABLE varchar (c1 STRING PRIMARY KEY, c2 VARCHAR, c3 varchar(5));
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM varchar;
  column_name | data_type  | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+------------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | STRING     |    false    | NULL           |                       | {primary} |   false   | false
  c2          | VARCHAR    |    true     | NULL           |                       | {}        |   false   | false
  c3          | VARCHAR(5) |    true     | NULL           |                       | {}        |   false   | false
(3 rows)

-- 3. Insert data into the table.

INSERT INTO varchar VALUES ('a1b2c3d4', 's', 'e5f6');
INSERT 1

-- 4. Check data of the table.

SELECT * FROM varchar;
     c1    | c2 |  c3
-----------+----+-------
  a1b2c3d4 | s  | e5f6
(1 row)
```

### NVARCHAR

#### Basic Information

NVARCHAR-typed values are variable-length strings. The maximum size of NVARCHAR-typed values is subject to the column's length limit.

- If the value is shorter than the column's length limit, KWDB stores the value with its actual length and does not add space padding to the end of the value.
- If the value exceeds the column's length limit, KWDB returns an error.

NVARCHAR-typed values are stored using the Unicode coding method.

To limit the length of a NVARCHAR-typed value, use `NVARCHAR(n)`, where `n` represents the maximum number of Unicode code points allowed. A NVARCHAR-typed value is an integer but cannot exceed the maximum value of INT32 (`2147483647`). If no length is specified, there is no length limit.

#### Examples

This example creates a table with NVARCHAR-typed columns and then inserts data into the table.

```sql
-- 1. Create a table named nvarchar.

CREATE TABLE nvarchar(c1 NVARCHAR PRIMARY KEY, c2 NVARCHAR(63), c3 NVARCHAR(254));
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM nvarchar;
  column_name |   data_type   | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+---------------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | NVARCHAR      |    false    | NULL           |                       | {primary} |   false   | false
  c2          | NVARCHAR(63)  |    true     | NULL           |                       | {}        |   false   | false
  c3          | NVARCHAR(254) |    true     | NULL           |                       | {}        |   false   | false
(3 rows)

-- 3. Insert data into the table.

INSERT INTO nvarchar VALUES ('a1b2c3d4', 's', 'e5f6');
INSERT 1

-- 4. Check data of the table.

SELECT * FROM nvarchar;
     c1    | c2 |  c3
-----------+----+-------
  a1b2c3d4 | s  | e5f6
(1 row)
```

### COLLATE

#### Basic Information

Collated strings are used as normal strings in SQL, but have a `COLLATE` clause appended to them to sort STRING values. When defining a column, you can use the `COLLATE` clause to define the sorting rules of strings or use any of the aliases for STRING values.

```sql
CREATE TABLE collates (c1 STRING COLLATE en PRIMARY KEY, c2 TEXT COLLATE en);
```

The above example specifies columns `c1` and `c2` as STRING-typed columns and uses `en` to sort their values. You can also use the `COLLATE` clause to sort values, as shown below:

```sql
INSERT INTO collates VALUES ('tianjin' COLLATE en,'KWDB' COLLATE en);
```

#### Examples

This example creates a table with STRING-typed columns, inserts data into the data, and then sets a column collation to `en`.

```sql
-- 1. Create a table named collates and set the column collation to en.

CREATE TABLE collates (c1 STRING COLLATE en PRIMARY KEY, c2 TEXT COLLATE en);
CREATE TABLE

-- 2. Insert data into the table. When inserting values into this column, you must specify the collation for every value.

INSERT INTO collates VALUES ('Beijing' COLLATE en, 'KWDB' COLLATE en), ('Jinan' COLLATE en, 'KWDB' COLLATE en), ('Tianjin' COLLATE en, 'KWDB' COLLATE en);
INSERT 3

-- 3. Check data of the table. The data will be processed based on the sorting rule.

SELECT * FROM collates ORDER BY c1;
c1       | c2
---------+--------
Beijing  | KWDB
Jinan    | KWDB
Tianjin  | KWDB
(3 rows)

-- 4. Sort values based on the specified rule. 

SELECT * FROM collates ORDER BY c1 COLLATE cmn;
c1       | c2
---------+--------
Beijing  | KWDB
Jinan    | KWDB
Tianjin  | KWDB
(3 rows)

SELECT * FROM collates ORDER BY c1 COLLATE yue;
c1       | c2
---------+--------
Beijing  | KWDB
Jinan    | KWDB
Tianjin  | KWDB
(3 rows)

-- 5. Compare values with the same collations.

SELECT 'A' COLLATE de < 'Ä' COLLATE de;
?column?
--------
t
(1 row)

-- 5. Compare values with different collations and KWDB returns an error.

SELECT 'Ä' COLLATE sv < 'Ä' COLLATE de;
ERROR: unsupported comparison operator: <collatedstring{sv}> < <collatedstring{de}>


-- 6. Use casting to remove collations from values.

SELECT CAST(c1 AS STRING) FROM collates ORDER BY c1;
c1
----
Beijing
Tianjin
Jinan
(3 rows)
```

### BLOB

#### Basic Information

A BLOB (Binary Large Object) is a binary large object that can hold a variable amount of non-textual byte stream data (such as programs, images, audio, and video). The size of a BLOB value is variable, but it is recommended to keep values under 64 MB to ensure performance.

BLOB values can be converted to the following data types. When data conforms to the rules, the system converts the data. Otherwise, the system returns an error.

| BLOB | STRING | UUID |
| --- | --- | --- |
| BLOB | - STRING <br >- NAME <br >- CHAR <br >- NCHAR <br >- VARCHAR <br >- NVARCHAR <br >- GEOMETRY <br >- BYTES <br > - VARBYTES | UUID |

#### Examples

This example creates a table with BLOB-typed columns and then inserts data into the table.

```sql
-- 1. Create a table.
CREATE TABLE blobs (e1 INT4, e2 BLOB);
CREATE TABLE

-- 2. Insert data into the table.
INSERT INTO blobs VALUES ('1','a')；
INSERT 1

-- 3. Check data of the table.
SELECT * FROM blobs;
  e1 |  e2
-----+-------
  1  | \x61
(1 row)

-- 4. Check the SQL statement that creates the table.
SHOW CREATE blobs;
  table_name |           create_statement
-------------+---------------------------------------
  blobs      | CREATE TABLE blobs (
             |     e1 INT4 NULL,
             |     e2 BLOB NULL,
             |     FAMILY "primary" (e1, e2, rowid)
             | )
(1 row)
```

### CLOB

#### Basic Information

A CLOB (Character Large Object) is associated with character sets and used for storing text-based data (such as historical archives and large-volume publications). The size of a CLOB value is variable, but it is recommended to keep values under 64 MB to ensure performance.

CLOB values can be converted to the following data types. When data conforms to the rules, the system converts the data. Otherwise, the system returns an error.

| CLOB | Numeric | BOOL | STRING | Date and time | JSONB | INET | UUID |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CLOB | - INT2 <br >- INT4 <br >- INT8 <br >- FLOAT4 <br >- FLOAT8 <br >- DECIMAL | BOOL | - STRING <br >- NAME <br >- CHAR <br >- NCHAR <br >- VARCHAR <br >- NVARCHAR <br >- BIT <br >- VARBIT <br >- GEOMETRY <br >- BYTES <br > - VARBYTES | - TIME <br >- TIMEZ <br >- TIMESTAMP <br >- TIMESTAMPTZ <br >- INTERVAL | JSONB | INET | UUID |

#### Examples

This example creates a table with CLOB-typed columns and then inserts data into the table.

```sql
-- 1. Create a table.
CREATE TABLE clobs (c1 INT, c2 CLOB);
CREATE TABLE

-- 2. Insert data into the table.
INSERT INTO clobs VALUES ('1','adh')；
INSERT 1

-- 3. Check data of the table.
SELECT * FROM clobs;
  c1 |  c2
-----+-------
  1  | adh
(1 row)

-- 4. Check the SQL statement that creates the table.
SHOW CREATE clobs;
  table_name |           create_statement
-------------+---------------------------------------
  clobs      | CREATE TABLE clobs (
             |     c1 INT  NULL,
             |     c2 CLOB NULL,
             |     FAMILY "primary" (c1, c2, rowid)
             | )
(1 row)
```

## Date and Time Types

KWDB relational databases support TIMESTAMP and TIMESTAMPTZ time types.

### TIMESTAMP

#### Basic Information

The TIMESTAMP data type has TIMESTAMP and TIMESTAMPTZ variants.

TIMESTAMP constants represent specific date and time. In general, the TIMESTAMP constants cannot be modified. You can express TIMESTAMP constants using the `timestamp 'YYYY-MM-DD HH:MM:SS.SSS'` format, such as `timestamp '2020-02-12 07:23:25.123'`.

| Name        | Alias                       | Description                                                          |
|-------------|-----------------------------|----------------------------------------------------------------------|
| TIMESTAMP   | TIMESTAMP WITHOUT TIME ZONE | Store date and time in UTC.                                          |
| TIMESTAMPTZ | TIMESTAMP WITH TIME ZONE    | Convert TIMESTAMP values from UTC to the client's session time zone. |

::: warning note

- TIMESTAMPTZ does not store any time zone data.
- By default, KWDB adopts UTC. Therefore, the default value for TIMESTAMPTZ is identical to that of TIMESTAMP.

:::

KWDB supports addition and subtraction operations of time in queries for timestamp-typed columns or timestamp constants, and for functions and expressions whose result is timestamp. KWDB supports comparing the operation results using the greater than sign (`>`), the less than sign (`<`), the equals sign (`=`), the greater than or equal to sign (`>=`), and the less than or equal to sign (`<=`). For details, see [Simple Query](../dml/relational-db/relational-select.md).

#### Data Type Conversions and Casts

TIMESTAMP-typed values can be cast to any of the following data types.

| Type | Description |
| --- | --- |
| INT | The system returns an error if the value is NaN or +/- Inf. |
| FLOAT | Convert to milliseconds since Jan. 1, 1970. |
| DECIMAL | Convert to seconds since Jan. 1, 1970. |
| STRING | - |
| DATE | Convert to the date portion (`YYYY-MM-DD`) of the timestamp. |
| TIME | Convert to the time portion (`HH:MM:SS`) of the timestamp. |
| TIMESTAMPTZ | - |

#### Data Type Conversions and Casts

TIMESTAMPTZ-typed values can be cast to any of the following data types.

| Type | Description |
| --- | --- |
| INT | The system returns an error if the value is NaN or +/- Inf. |
| FLOAT | Convert to milliseconds since Jan. 1, 1970. |
| DECIMAL | Convert to seconds since Jan. 1, 1970. |
| STRING | - |
| DATE | Convert to the date portion (`YYYY-MM-DD`) of the timestamp. |
| TIME | Convert to the time portion (`HH:MM:SS`) of the timestamp. |
| TIMESTAMP | - |

#### Examples

This example creates a table with TIMESTAMP-typed and TIMESTAMPTZ-typed columns.

```sql
-- 1. Create a table named timestamps.

CREATE TABLE timestamps (c1 INT PRIMARY KEY, c2 TIMESTAMP, c3 TIMESTAMPTZ);
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM timestamps;
  column_name |  data_type  | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-------------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | INT4        |    false    | NULL           |                       | {primary} |   false   | false
  c2          | TIMESTAMP   |    true     | NULL           |                       | {}        |   false   | false
  c3          | TIMESTAMPTZ |    true     | NULL           |                       | {}        |   false   | false
(3 rows)

-- 3. Insert data into the table.

INSERT INTO timestamps VALUES(1, TIMESTAMP '2023-03-26', TIMESTAMPTZ '2023-03-26 10:10:10-05:00');
INSERT 1

-- 4. Check data of the table.

SELECT * FROM timestamps;
c1|c2                 |c3
--+-------------------+-------------------------
1 |2023-03-26 00:00:00|2023-03-26 15:10:10+00:00
(1 row)
```

### DATE

#### Basic Information

The DATE data type stores a year, month, and day. You can express a constant value of the DATE type using an interpreted literal, or a string literal annotated with the DATE type or coerced to the DATE type. KWDB also supports using uninterpreted string literals to express a DATE value. By default, KWDB parses the `YYYY-MM-DD` string format for dates, such as `DATE '2016-12-23'`. A DATE-typed column supports values up to 16 bytes in width, but the total storage size is likely to be larger due to KWDB metadata.

#### Data Type Conversions and Casts

DATE-typed values can be cast to any of the following data types.

| Type | Description |
| --- | --- |
| INT | The system returns an error if the value is NaN or +/- Inf. |
| FLOAT | - |
| DECIMAL | - |
| STRING | - |
| TIMESTAMPTZ/TIMESTAMPTZ | - |

#### Examples

This example creates a table with DATE-typed columns and then inserts data into the table.

```sql
-- 1. Create a table named dates.

CREATE TABLE dates (a DATE PRIMARY KEY, b INT);
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM dates;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  a           | DATE      |    false    | NULL           |                       | {primary} |   false   | false
  b           | INT4      |    true     | NULL           |                       | {}        |   false   | false
(2 rows)

-- 3. Insert data into the table.

INSERT INTO dates VALUES (DATE '2016-03-26', 12345);
INSERT 1

-- 4. Check data of the table.

SELECT * FROM dates;
              a             |   b
----------------------------+--------
  2016-03-26 00:00:00+00:00 | 12345
(1 row)

-- 5. String literal implicitly typed as DATE:

INSERT INTO dates VALUES ('2016-03-27', 12345);
INSERT 1

SELECT * FROM dates;
              a             |   b
----------------------------+--------
  2016-03-26 00:00:00+00:00 | 12345
  2016-03-27 00:00:00+00:00 | 12345
(2 rows)
```

### TIME

#### Basic Information

The TIME data type stores the time of day in UTC.

| Name | Alias                  |
|------|------------------------|
| TIME | TIME WITHOUT TIME ZONE |

A constant value of the TIME type can be expressed using an interpreted literal, or a string literal annotated with the TIME type or coerced to the TIME type. KWDB also supports using uninterpreted string literals to express a TIME value. The string format for TIME is `HH:MM:SS.SSSSSS`, such as `TIME '05:40:00.000001'`. The fractional portion is optional and is rounded to microseconds (i.e., six digits after the decimal). A TIME-typed column supports values up to 8 bytes in width, but the total storage size is likely to be larger due to KWDB metadata.

#### Data Type Conversions and Casts

TIME-typed values can be cast to any of the following data types.

| Type | Description |
| --- | --- |
| STRING | - |
| INTERVAL | - |

#### Examples

This example creates a table with TIME-typed columns and then inserts data into the table.

```sql
-- 1. Create a table named time.

CREATE TABLE time (time_id INT PRIMARY KEY, time_val TIME);
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM time;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  time_id     | INT4      |    false    | NULL           |                       | {primary} |   false   | false
  time_val    | TIME      |    true     | NULL           |                       | {}        |   false   | false
(2 rows)

-- 3. Insert data into the table.

INSERT INTO time VALUES (1, TIME '05:40:00'), (2, TIME '05:41:39');
INSERT 2

-- 4. Check data of the table.

 SELECT * FROM time;
  time_id |         time_val
----------+----------------------------
        1 | 0000-01-01 05:40:00+00:00
        2 | 0000-01-01 05:41:39+00:00
(2 rows)

-- 5. Compare TIME values.

SELECT (SELECT time_val FROM time WHERE time_id = 1) < (SELECT time_val FROM time WHERE time_id = 2);
?column?
--------
  true
(1 row)
```

### INTERVAL

#### Basic Information

The INTERVAL data type stores a value that represents a span of time. A constant value of the INTERVAL type can be expressed using an interpreted literal, or a string literal annotated with the INTERVAL type or coerced to the INTERVAL type. KWDB also supports using uninterpreted string literals to express an INTERVAL value.

INTERVAL constants can be expressed using the following formats:

- SQL Standard: `INTERVAL 'Y-M D H:M:S'`
  - `Y-M D`: Use a single value to define days. Use two colon-separated values to define years and months. You can express days, years, and months as integers or floats.
  - `H:M:S`: Use a single value to define seconds. Use two colon-separated values to define hours and minutes. You can express seconds, hours, and minutes as integers or floats. Each part is optional.
- ISO 8601: `INTERVAL 'P1Y2M3DT4H5M6S'`

An INTERVAL-typed column supports values up to 24 bytes in width, but the total storage size is likely to be larger due to KWDB metadata. Intervals are stored internally as months, days, and microseconds. Therefore, a value parsed from a string value or converted from a floating-point or DECIMAL value is rounded to the nearest microsecond. Any operations (addition, subtraction, multiplication, division) performed on an INTERVAL value will also be rounded to the nearest microsecond.

#### Data Type Conversions and Casts

INTERVAL-typed values can be cast to any of the following data types.

| Type | Description |
| --- | --- |
| INT | The system returns an error if the value is NaN or +/- Inf. |
| FLOAT | Convert to seconds since Jan. 1, 1970. |
| DECIMAL | Convert to seconds since Jan. 1, 1970. |
| STRING | - |
| TIME | Convert to the time portion (`HH:MM:SS`) after the midnight. |

#### Examples

This example creates a table with INTERVAL-typed columns and then inserts data into the table.

::: warning Note

If an INTERVAL-typed column is used as a primary key, this may lead to uniqueness issues.

:::

```sql
-- 1. Create a table named intervals.

CREATE TABLE intervals (c1 INT PRIMARY KEY, c2 interval);
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM intervals;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | INT4      |    false    | NULL           |                       | {primary} |   false   | false
  c2          | INTERVAL  |    true     | NULL           |                       | {}        |   false   | false
(2 rows)

-- 3. Insert data into the table.

INSERT INTO intervals VALUES (1, interval '1 year 2 months 3 days 4 hours 5 minutes 6 seconds'),(2, interval '1-2 3 4:5:6'),(3, '1-2 3 4:5:6');
INSERT 3

-- 4. Check data of the table.

SELECT * FROM intervals;
  c1 |              c2
-----+--------------------------------
   1 | 1 year 2 mons 3 days 04:05:06
   2 | 1 year 2 mons 3 days 04:05:06
   3 | 1 year 2 mons 3 days 04:05:06
(3 rows)
```

## JSONB

### Basic Information

The JSONB data type stores JSON (JavaScript Object Notation) data as a binary representation of the JSONB value, which eliminates whitespace, duplicate keys, and key ordering. JSONB supports GIN indexes.

| Name  | Alias |
|-------|-------|
| JSONB | JSON  |

The syntax for the JSONB data type follows the format specified in RFC8259. You can express a constant value of the JSONB type using an interpreted literal or a string literal annotated with the JSONB type.

There are six types of JSONB values:

- Null
- Boolean
- String
- Number: a value with arbitrary precision, including integers and decimals, but not limited to INT64
- Array: an ordered sequence of JSONB values
- Object: a mapping from strings to JSONB values, such as `'{"type": "account creation", "username": "harvestboy93"}'` or `'{"first_name": "Ernie", "status": "Looking for treats", "location": "Brooklyn"}'`. If duplicate keys are included in the input, only the last value is kept.

### Data Type Conversions and Casts

JSONB-typed values can be cast to STRING-typed values.

### Examples

Example 1: This example creates a table with a JSONB-typed column and then inserts data into the table.

```sql

-- 1. Create a table named jsonb.

CREATE TABLE jsonbs (id INT8 DEFAULT unique_rowid(), name JSONB, PRIMARY KEY(id));
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM jsonbs;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  id          | INT8      |    false    | unique_rowid() |                       | {primary} |   false   | false
  name        | JSONB     |    true     | NULL           |                       | {}        |   false   | false
(2 rows)

-- 3. Insert data into the table.

INSERT INTO jsonbs (name) VALUES ('{"first_name": "Lei", "last_name": "Li", "location": "Beijing"}'), ('{"first_name": "Meimei", "last_name": "Han", "location": "Beijing"}');
INSERT 2

-- 4. Check data of the table.

SELECT * FROM jsonbs;
          id         |                                name
---------------------+----------------------------------------------------------------------
  960911294061182977 | {"first_name": "Lei", "last_name": "Li", "location": "Beijing"}
  960911294061314049 | {"first_name": "Meimei", "last_name": "Han", "location": "Beijing"}
(2 rows)

-- 5. Use the jsonb_pretty() function to retrieve JSONB data.

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

-- 6. Use the -> operator to retrieve a specific field from JSONB data.

SELECT name->'first_name', name->'location' FROM jsonbs;
  ?column? | ?column?
-----------+------------
  "Lei"    | "Beijing"
  "Meimei" | "Beijing"
(2 rows)

-- 7. Use the ->> operator to return JSONB fields as STRING values.

SELECT name->>'first_name', name->>'location' FROM jsonbs;
  ?column? | ?column?
-----------+-----------
  Lei      | Beijing
  Meimei   | Beijing
(2 rows)
```

Example 2: Create a table with a JSONB column and a stored computed column. In this example, the primary key `id` is computed as a field from the `profile` column.

```sql
-- 1. Create a table named student_profiles.

CREATE TABLE student_profiles (id STRING PRIMARY KEY AS (profile->>'id') STORED, profile JSONB);
CREATE TABLE

-- 2. Insert data into the table.

INSERT INTO student_profiles (profile) VALUES ('{"id": "d78236", "name": "Ming Wang", "age": "16", "school": "No.4 High School", "credits": 120, "sports": "none"}'), ('{"name": "Lei Zhou", "age": "15", "id": "f98112", "school": "No.4 High School", "credits": 97}'), ('{"name": "Yang Sun", "school" : "No.8 High School", "id": "t63512", "credits": 100}');
INSERT 3

-- 3. Check data of the table.

SELECT * FROM student_profiles;
    id   |                                                      profile
---------+---------------------------------------------------------------------------------------------------------------------
  d78236 | {"age": "16", "credits": 120, "id": "d78236", "name": "Ming Wang", "school": "No.4 High School", "sports": "none"}
  f98112 | {"age": "15", "credits": 97, "id": "f98112", "name": "Lei Zhou", "school": "No.4 High School"}
  t63512 | {"credits": 100, "id": "t63512", "name": "Yang Sun", "school": "No.8 High School"}
(3 rows)
```

## ARRAY

### Basic Information

The ARRAY data type stores one-dimensional, 1-indexed, homogeneous arrays of any non-array data type. KWDB does not support nested arrays. KWDB does not support indexing or sorting ARRAY-typed columns.

An ARRAY value can be expressed in the following ways:

- Append square brackets (`[]`) to any non-array data type.
- Add the term `ARRAY` to any non-array data type.

The size of an ARRAY value is variable, but it is recommended to keep values under 1 MB to ensure performance. Above that threshold, write amplification and other considerations may cause significant performance degradation.

### Examples

Example 1: This example creates a table with an ARRAY-typed column by appending square brackets (`[]`) and then inserts data into the table.

```sql
-- 1. Create a table named arrays.

CREATE TABLE arrays (b STRING[]);
CREATE TABLE

-- 2. Insert data into the table.

INSERT INTO arrays VALUES (ARRAY['sky', 'road', 'car']);
INSERT 1

-- 3. Check data of the table.

SELECT * FROM arrays;
b
--------------
{sky,road,car}
(1 row)
```

Example 2: This example creates a table with an ARRAY-typed column by adding the term `ARRAY` and then inserts data into the table.

```sql
-- 1. Create a table named c.

CREATE TABLE c (d INT ARRAY);
CREATE TABLE

-- 2. Insert data into the table.

INSERT INTO c VALUES (ARRAY[10,20,30]);
INSERT 1

-- 3. Check data of the table.

SELECT * FROM c;
d
----------
{10,20,30}
(1 row)

-- 4. Access an array element using the array index. Arrays in KWDB are 1-indexed.

SELECT d[2] FROM c;
d
--
20
(1 row)

-- 5. Append an array element to an array using the array_append function.

UPDATE c SET d = array_append(d, 40) WHERE d[3] = 30;
UPDATE 1

-- 6. Check data of the table.

SELECT * FROM c;
d
-------------
{10,20,30,40}
(1 row)

-- 7. Append an array element to an array using the append(||) operator. 

UPDATE c SET d = d || 50 WHERE d[4] = 40;
UPDATE 1

-- 8. Check data of the table.

SELECT * FROM c;
d
----------------
{10,20,30,40,50}
(1 row)
```

## INET

### Basic Information

The INET data type stores an IPv4 or IPv6 address. A constant value of the INET type can be expressed using an interpreted literal, or a string literal annotated with the INET type or coerced to the INET type.

INET constants can be expressed using the following formats:

- IPv4 addresses: Standard RFC791-specified format of 4 octets expressed individually in decimal numbers and separated by periods (`.`). Optionally, the address can be followed by a subnet mask. For example, `'190.0.0.0'`, `'190.0.0.0/24'`.
- IPv6 addresses: Standard RFC8200-specified format of 8 colon-separated groups of 4 hexadecimal digits. An IPv6 address can be mapped to an IPv4 address. Optionally, the address can be followed by a subnet mask. For example, `'2001:4f8:3:ba:2e0:81ff:fe22:d1f1'`, `'2001:4f8:3:ba:2e0:81ff:fe22:d1f1/120'`, `'::ffff:192.168.0.1/24'`.

An INET value is 32 bits for IPv4 or 128 bits for IPv6. Therefore, IPv4 addresses will sort before IPv6 addresses, including IPv4-mapped IPv6 addresses.

### Examples

This example creates a table with an INET-typed column and then inserts data into the table.

```sql
-- 1. Create a table named inets.

CREATE TABLE inets(c1 INET PRIMARY KEY);
CREATE TABLE

-- 2. Check columns of the table.

SHOW COLUMNS FROM inets;
  column_name | data_type | is_nullable | column_default | generation_expression |  indices  | is_hidden | is_tag
--------------+-----------+-------------+----------------+-----------------------+-----------+-----------+---------
  c1          | INET      |    false    | NULL           |                       | {primary} |   false   | false
(1 row)

-- 3. Insert data into the table.

INSERT INTO inets VALUES ('192.168.0.1'),('192.168.0.2/10'), ('2001:4f8:3:ba:2e0:81ff:fe22:d1f1/120');
INSERT 3

-- 4. Check data of the table.

SELECT * FROM inets;
c1
------------------------------------
192.168.0.2/10
192.168.0.1
2001:4f8:3:ba:2e0:81ff:fe22:d1f1/120
(3 rows)
```

## UUID

### Basic Information

The UUID (Universally Unique Identifier) data type stores a 128-bit value that is unique across both space and time. To auto-generate unique row identifiers, use UUID with the `gen_random_uuid()` function as the default value. 

You can express UUID values using the following formats:

- Standard RFC4122 format: a value specified as hyphen-separated groups of 8, 4, 4, 4, and 12 hexadecimal digits, such as `acde070d-8c4c-4f0d-9d8a-162843c10333`.
- Standard RFC4122 format: a value surrounded by braces, such as `{acde070d-8c4c-4f0d-9d8a-162843c10333}`.
- BYTES: a UUID value specified as a BYTES value.
- URN: a URN (Uniform Resource Name) specified as `"urn:uuid:"` followed by the RFC4122 format, such as `urn:uuid:63616665-6630-3064-6465-616462656564`.

A UUID value is 128 bits in width, but the total storage size is likely to be larger due to KWDB metadata.

### Data Type Conversions and Casts

UUID-typed values can be cast to any of the following data types.

| Type | Description |
| --- | --- |
| DECIMAL | - |
| STRING | Convert the UUID-typed value to the corresponding STRING-typed value and truncate it based on the converted STRING type. |
| BYTES | - |

### Examples

Example 1: This example creates a table with a UUID-typed column and then inserts data into the table.

```sql
-- 1. Create a table named uuids.

CREATE TABLE uuids (token UUID);
CREATE TABLE

-- 2. Insert a UUID value in standard RFC4122-specified format.

INSERT INTO uuids VALUES ('63616665-6630-3064-6465-616462656562');
INSERT 1

-- 3. Check data of the table.

SELECT * FROM uuids;
token
------------------------------------
63616665-6630-3064-6465-616462656562
(1 row)

-- 4. Insert a UUID value surrounded by braces.

INSERT INTO uuids VALUES ('{63616665-6630-3064-6465-616462656563}');
INSERT 1

-- 5. Check data of the table.

SELECT * FROM uuids;
token
------------------------------------
63616665-6630-3064-6465-616462656562
63616665-6630-3064-6465-616462656563
(2 rows)

-- 6. Insert a UUID value specified as a BYTES value.

INSERT INTO uuids VALUES (b'kafef00ddeadbeed');
INSERT 1

-- 7. Check data of the table.

SELECT * FROM uuids;
token
------------------------------------
63616665-6630-3064-6465-616462656562
63616665-6630-3064-6465-616462656563
6b616665-6630-3064-6465-616462656564
(3 rows)

-- 8. Insert a UUID value in URN format.

INSERT INTO uuids VALUES ('urn:uuid:63616665-6630-3064-6465-616462656564');
INSERT 1

-- 9. Check data of the table.

SELECT * FROM uuids;
token
------------------------------------
63616665-6630-3064-6465-616462656562
63616665-6630-3064-6465-616462656563
6b616665-6630-3064-6465-616462656564
63616665-6630-3064-6465-616462656564
(4 rows)
```

Example 2: This example creates a table with a UUID-typed column and uses the UUID-typed column with the `gen_random_uuid()` function as the default value.

::: warning Note
In Example 2 or Example 3, generated IDs will be 128-bit, sufficiently large to generate unique values. Once the table grows beyond a single key-value range's default size (64 MB by default), new IDs will be scattered across all of the table's ranges and, therefore, likely across different nodes. This means that multiple nodes will share in the load.
Although this approach creates a primary key, but it may not be useful in a query directly, which may require a join with another table or a secondary index. To store generated IDs in the same key-value range, you can use an integer type with the `unique_rowid()` function as the default value, either explicitly or via the SERIAL type.
:::

```sql
-- 1. Create a table named users.

CREATE TABLE users (id UUID NOT NULL DEFAULT gen_random_uuid(), name STRING, PRIMARY KEY(id, name));
CREATE TABLE

-- 2. Insert data into the table.

INSERT INTO users(name) VALUES ('Mary'), ('Tom'), ('Mark');
INSERT 3
```

Example 3: This example creates a table with a BYTES-typed column and uses the BYTES-typed column with the `uuid_v4()` function as the default value.

```sql
-- 1. Create a table named users2.

CREATE TABLE users2 (id BYTES DEFAULT uuid_v4(), name STRING, PRIMARY KEY(id, name));
CREATE TABLE

-- 2. Insert data into the table.

INSERT INTO users2(name) VALUES ('Mary'), ('Tom'), ('Mark');
INSERT 3

-- 3. Check data of the table.

SELECT * FROM users2;
id                                |name
----------------------------------+----
\x4a54c55174de428caebe9886cb663d9e|Mary
\xaa28838b33384766baa34a82ea00dd3a|Mark
\xe378c650f45c41a3b231ecf4fddad8c8|Tom
(3 rows)
```

Example 4: This example creates a table with an INT8-typed column and uses the INT8-typed column with the `unique_rowid()` function as the default value.

::: warning Note
Upon inserts, the `unique_rowid()` function generates a default value from the timestamp and ID of the node executing inserts. Such time-ordered values are likely to be globally unique except in cases where a very large number of IDs (100,000+) are generated per node per second. However, there can be gaps and the order is not completely guaranteed.
:::

```sql
-- 1. Create a table named users3.

CREATE TABLE users3 (id INT8 DEFAULT unique_rowid(), name STRING, PRIMARY KEY(id, name));
CREATE TABLE

-- 2. Insert data into the table.

INSERT INTO users3(name) VALUES ('Mary'), ('Mark'), ('Tom');
INSERT 3

-- 3. Check data of the table.

SELECT * FROM users3;
id                |name
------------------+----
858541035522097153|Mary
858541035522129921|Mark
858541035522162689|Tom
(3 rows)
```
