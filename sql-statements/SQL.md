sh# 数据类型

## 数值类型

### 整型

整数类型一般用INT4表示，KaiwuDB支持各种有符号整数数据类型。

#### 基础信息

整数类型有各种不同的名称和取值范围。

| 名称              | 占用位数(bit) | 取值范围                                    |
| ----------------- | ------------- | ------------------------------------------- |
| SMALLINT          | 16            | -32768~+32767                               |
| INT4              | 32            | -2147483648 ~ +2147483647                   |
| BIGINT/BIGINTEGER | 64            | -9223372036854775808 ~ +9223372036854775807 |

数值文本可以作为INT类型的输入，例如：42，-1234。

不同的整数类型对允许值的范围设置了不同的约束。但是无论类型如何，所有整数都以相同的方式存储。

#### 示例

示例1：创建具有整数类型列的数据库表

```sql
> create table t_int(a int16 not null default 0,b INT4 not null default 0,c BIGINT not null default 0);

// 插入整数类型的值
> insert into t_int values (32767,2147483647,9223372036854775807);

# 查询插入整数类型的值
> select * from t_int;
+-------+------------+---------------------+
| a      | b         | c                   |
+-------+------------+---------------------+
| 32767 | 2147483647 | 9223372036854775807 |
+-------+------------+---------------------+
1 row in set (0.01 sec)

# 本次插入的数值超过了对应数值类型的取值范围，系统就会报错。
> insert into t_int values(32768,2147483648,9223372036854775808);
ERROR 46 (HY000): Out of range data: 32768
```

### 浮点型

KaiwuDB支持各种不确定精度的浮点数数据类型。FLOAT4为4字节浮点数，DOUBLE为8字节浮点数。

#### 基础信息

浮点数在KaiwuDB中的名称如下表所示：

| 名称   | 长度  |
|--------|-------|
| FLOAT4 | 4字节 |
| DOUBLE | 8字节 |

单精度浮点数FLOAT4或者FLOAT类型可以确保前6-7位有效数字是准确的；双精度浮点数DOUBLE可以确保前15位有效数字是准确的。

可通过以下语句对浮点类型数据进行查询：

- `set float_precision=xxx`; 设置单精度类型数据小数部分的显示位数；
- `set double_precision=xxx`; 设置双精度类型数据小数部分的显示位数。

超出有效数字位数的数字依然会被显示，但数字不准确。除此之外，小数部分最低位的0会被删除不显示。例如，设置单精度类型数据的精度`set float_precision=6`，数值2.111000查询结果显示为2.111。

#### 示例

示例1：创建具有浮点数列的表

```sql
> create table t_float(f1 FLOAT4 not null default 0.00, f2 FLOAT not null default 0.00, d DOUBLE not null default 0.00);
Query OK, 0 rows affected (0.02 sec)
```

示例2：向具有FLOAT4列的表中插入值

```sql
> insert into t_float values(2.111,2.1110,2.111),(1.2345678910,12345.678910,1.234567890123456789);
Query OK, 2 rows affected (0.00 sec)

> set float_precision=6;
Query OK, 0 rows affected (0.00 sec)

> set double_precision=12;
Query OK, 0 rows affected (0.00 sec)

> select * from t_float;
+----------+--------------+----------------+
| f1       | f2           | d              |
+----------+--------------+----------------+
| 2.111    | 2.111        | 2.111          |
| 1.234568 | 12345.678711 | 1.234567890123 |
+----------+--------------+----------------+
2 rows in set (0.00 sec)

> set float_precision=7;
Query OK, 0 rows affected (0.00 sec)

> set double_precision=15;
Query OK, 0 rows affected (0.00 sec)

> select * from t_float;
+-----------+---------------+-------------------+
| f1        | f2            | d                 |
+-----------+---------------+-------------------+
| 2.1110001 | 2.1110001     | 2.111             |
| 1.2345679 | 12345.6787109 | 1.234567890123457 |
+-----------+---------------+-------------------+
2 rows in set (0.00 sec)
```

## 字符类型

### STRING

#### 基础信息

浮动存取长度，适合数据重复率高，常用来group by或者where的数据。例如：性别、品牌等。

| 名称   | 默认长度 | 最大长度 |
|--------|----------|----------|
| STRING | 63       | 1023     |

#### 示例

示例1：创建带有string字段的t_str1表

```sql
> create table t_str1(a string(5) not null default 'a',b char(6) not null default 'a');
Query OK, 0 rows affected (0.00 sec)
```

示例2：往t_str1中插入数据

```sql
> insert into t_str1 values("abc","123");
Query OK, 1 row affected (0.00 sec)

> select * from t_str1;
+------+------+
| a    | b    |
+------+------+
| abc  | 123  |
+------+------+
1 row in set (0.00 sec)
```

### CHAR

#### 基础信息

固定存取长度，适合文字长度固定的列。例如：编号、ID等。如果插入值超过列的长度限制，KaiwuDB会提示错误。

| 名称 | 默认长度 | 最大长度 |
|------|----------|----------|
| CHAR | 32       | 786432   |

#### 示例

示例1：创建带有char类型的表

```sql
> create table t_str1(a string(5) not null default 'a',b char(6) not null default 'a');
Query OK, 0 rows affected (0.00 sec)
```

示例2：插入数据

```sql
# 插入长度标准的数据
> insert into t_str1 values("abc","123");
Query OK, 1 row affected (0.00 sec)

# 插入长度超过char(6)的数据
> insert into t_str1 values("abcdefgh","1234567");
ERROR 35 (HY000): Invalid value: abcdefgh

# 查询数据
> select * from t_str1;
+------+------+
| a    | b    |
+------+------+
| abc  | 123  |
+------+------+
1 row in set (0.01 sec)
```

### VARCHAR

在KaiwuDB中，VARCHAR数据类型存储一串Unicode字符。

#### 基础信息

在KaiwuDB中，使用VARCHAR(n)来限制列的长度，其中n是允许的最大Unicode编码点数量（通常被认为是"字节”）。

插入字符串时：如果值超过列的长度限制，KaiwuDB会提示错误。

| 名称    | 默认长度 | 最大长度 |
|---------|----------|----------|
| VARCHAR | 255      | 786432   |

#### 示例

以下示例介绍了VARCHAR类型在数据库中的应用：

```sql
> create table t_var(a VARCHAR not null default 'a',b VARCHAR(10) not null default 'a');
Query OK, 0 rows affected (0.00 sec)

> insert into t_var values ("abcdefghijkl","abcdefghijkliii");
ERROR 1 (HY000): Operation not permitted: abcdefghijkliii
```

## 日期和时间类型

| 名称         | 描述信息                     |
|--------------|------------------------------|
| DATE         | 年、月、日（4 字节长）       |
| DATETIME     | 日期和时间（8 字节长）       |
| TIMESTAMP(3) | 日期和时间（支持到毫秒精度） |

### DATE

DATE类型存储年月日信息。

#### 基础信息

字符串格式为YYYY-MM-DD。例如：`'2016-12-23'`。

当插入的字符串格式为YYYY-MM-DD hh-mi-ss。例如：`'2022-01-01 12:34:30'`，会自动截取为`'2022-01-01'`。

当插入的日期格式不符合时，会显示为`NULL`。

#### 示例

示例1：创建一个表t_date

```sql
> create table t_date(a date not null default '2023-01-01');
> show create table t_date;
+--------+-----------------------------------------------------------------+
| Table  | Create Table |
+--------+-----------------------------------------------------------------+
| t_date | CREATE TABLE `t_date` (
 `a` date NOT NULL
) ENGINE=TS
|
+--------+-----------------------------------------------------------------+
```

示例2：插入标准格式的日期类型

```sql
> insert into t_date values("2022-01-01");
Query OK, 1 row affected (0.00 sec)

> select * from t_date;
+------------+
| a          |
+------------+
| 2022-01-01 |
1 row in set (0.01 sec)
```

示例3：插入带时分秒的日期类型

```sql
> insert into t_date values("2022-01-02 12:00:01");
Query OK, 1 row affected (0.00 sec)

> select * from t_date;
+------------+
| a          |
+------------+
| 2022-01-02 |
+------------+
1 row in set (0.00 sec)
```

### DATETIME

#### 基础信息

DATETIME表示8字节长的时间。字符串格式为 YYYY-MM-DD hh-mi-ss。例如：'2022-01-01 12:34:30'。

#### 示例

示例1：创建带有DATETIME的表

```sql
> create table t_dt1(a datetime64 not null default '2023-01-01 00:00:00');
Query OK, 0 rows affected (0.00 sec)
```

示例2：插入数据

```sql
> insert into t_dt1 values("2022-01-01 12:00:00");
> select * from t_dt1;
+---------------------+
| a                   |
+---------------------+
| 2022-01-01 12:00:00 |
+---------------------+
1 row in set (0.00 sec)
```

### TIMESTAMP(3)

#### 基础信息

TIMESTAMP(3)表示毫秒精度的日期时间格式，可以采用长整型的方式插入，也可以采用字符串类型的日期时间插入。

#### 示例

示例1：创建带有TIMESTAMP(3)的表

```sql
> create table t2(ts timestamp(3) not null default "0000000000000");
Query OK, 0 rows affected (0.00 sec)
```

示例2：插入长整型的时间

```sql
> insert into t2 values(1680027263345);
Query OK, 1 row affected (0.00 sec)

> select * from t2;
+--------------------------+
| ts                       |
+--------------------------+
| 2023-03-28 18:14:23.345  |
+--------------------------+
1 row in set (0.00 sec)
```

示例3：插入长整型的时间戳

```sql
> insert into t2 values('2023-03-28 10:00:00.123');
Query OK, 1 row affected (0.00 sec)

> select * from t2;
+--------------------------+
| ts                       |
+--------------------------+
| 2023-03-28 10:00:00.123  |
+--------------------------+
1 row in set (0.00 sec)
```

## INET类型

### INET

#### 基础信息

INET包含IPV4和IPV6两种类型。

- IPv4: RFC791规定的4个八位字节格式，以十进制数字表示，以英文句点分隔。
- IPv6: RFC8200规定的4个十六进制数字组，共8组，每组以冒号分隔。

#### 示例

示例1：创建含有ipv4和ipv6类型的表

```sql
> create table t_ip(a ipv4 not null default '0.0.0.0',b ipv6 not null default '0.0.0.0');
Query OK, 0 rows affected (0.00 sec)
```

示例2：插入相应类型的数据

```sql
> insert into t_ip values("190.0.0.0","2001:4f8:3:ba:2e0:81ff:fe22:d1f1");
Query OK, 1 row affected (0.01 sec)

> select * from t_ip;
+-----------+----------------------------------+
| a         | b                                |
+-----------+----------------------------------+
| 190.0.0.0 | 2001:4f8:3:ba:2e0:81ff:fe22:d1f1 |
+-----------+----------------------------------+
1 row in set (0.00 sec)
```

## 二进制对象类型

### 二进制对象

#### 基础信息

二进制对象型有BINARY和VARBINARY两种类型，可以用来存储二进制。其中，BINARY为定长二进制型，VARBINARY为变长二进制型。

#### 示例

示例1：创建带有BINARY和VARBINARY的列

```sql
> create table t_bin(a binary not null default '0x00000000', b varbinary not null default '0x00000000000000');
Query OK, 0 rows affected (0.01 sec)
```

示例2：插入数据并查看

```sql
> insert into t_bin values("0x0000007b","0x0000007b28395C");
Query OK, 1 row affected (0.00 sec)

> select * from t_bin;
+----------------------------------+---------+
a                                  | b       |
+----------------------------------+---------+
  {                                | {(9\    |
+----------------------------------+---------+
1 row in set (0.00 sec)
```

## 布尔类型

### BOOL

#### 基础信息

布尔类型主要通过BOOL实现，存储true（1）、false（0）两种类型的值。

#### 示例

示例1：创建带有BOOL类型的列

```sql
> create table b1 (a BOOL not null);
Query OK, 0 rows affected (0.01 sec)
```

示例2：插入并查看数据

```sql
> insert into b1 ("true");
Query OK, 1 row affected (0.00 sec)

> select * from b1;
+----------------------------------+
a                                  |
+----------------------------------+
1                                  |
+----------------------------------+
1 row in set (0.00 sec)
```

# SQL语法

本章主要介绍KaiwuDB支持的SQL语法。

## DDL语句

KaiwuDB的DDL语句用于创建数据库对象。

### DATABASE

#### CREATE DATABASE

CREATE DATABASE语句可以创建一个新的KaiwuDB数据库。

##### 语法格式

```sql
CREATE DATABASE <database_name>;
```

##### 参数说明

- database_name：要创建的数据库名称，长度限制54，不支持 * - \ / 四个字符。该名称必须是唯一的，并遵循本数据库标识符规则。

##### 示例

示例：创建名为db1的数据库

```sql
CREATE DATABASE db1;
```

#### SHOW DATABASES

SHOW DATABASES语句用于列出KaiwuDB中包含的所有数据库。

##### 语法格式

```sql
SHOW DATABASES;
```

##### 示例

示例：查询所有的数据库

```sql
> show databases;
+-----------+
| Database  |
+-----------+
| a         |
| b         |
| db1       |
| log1      |
| szq_test  |
+-----------+
5 rows in set (0.00 sec)
```

#### DROP DATABASE

DROP DATABASE语句用于从KaiwuDB中删除数据库及其所有对象。

##### 语法格式

```sql
DROP DATABASE <database_name>;
```

##### 参数说明

- database_name：要删除的数据库名称。

##### 示例

示例：删除数据库

```sql
> drop database abc;
Query OK, 0 rows affected (0.01 sec)

> show databases;
+-----------+
| Database  |
+-----------+
| a         |
| b         |
| log1      |
| szq_test  |
+-----------+
4 rows in set (0.00 sec)
```

### TABLE

#### CREATE TABLE

CREATE TABLE语句用于在数据库创建新表。

##### 语法格式

```sql
CREATE TABLE <table_name> (<column_list>) [TIMEBOUND (<time_window>)] [ENGINE=TS]
```

##### 参数说明

- table_name：要创建的表的名称，长度限制63，不能含有斜线”/”。
- column_list：表中的列，以逗号分隔。如果column的值不能为null, 定义时需要显式的指定为NOT NULL，默认为NULL(可接受NULL值)。
  
  column_list = <column_definition> [, <column_definition>]；
  
  column_definition = <column_name> <data_type> [not null] default <default_value_expr>
- column_name：要创建的列的名称，不超过32个字符，无字符限制。
- data_type：定义列的类型列表。
- TIMEBOUND：表的时间窗口标识。
- time_window：时间窗口说明符，具体说明符如下：

| 时间窗口说明符 | 描述   |
|----------------|--------|
| d              | day    |
| h              | hour   |
| m              | minute |
| s              | second |

- ENGINE=TS：指定引擎信息，一般可不加。

##### 示例

示例1：创建表

```sql
> create table t(id int not null default 0);
Query OK, 0 rows affected (0.00 sec)

> show create table t;
+-------+------------------------------------------------------------+
| Table | Create Table                                               |
+-------+------------------------------------------------------------+
| t     | CREATE TABLE `t\` (
 `id` int NOT NULL
) ENGINE=TS
|
+-------+------------------------------------------------------------+
1 row in set (0.00 sec)
```

示例2：创建时间限制表

```sql
> create table t1(dt datetime32 not null default '2023-01-01 00:00:00',id int not null default 0, timebound(10m));
Query OK, 0 rows affected (0.00 sec)

> show create table t1;
+-------+------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                   |
+-------+------------------------------------------------------------------------------------------------+
| t1    | CREATE TABLE `t1` (
`dt` datetime NOT NULL,
`id` INT4 NOT NULL
) timebound(600) ENGINE=TS
|
+-------+------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

> 说明：
> 可以组合多个时间窗口说明符来表示一个时间窗口。例如“2h30m”表示时间窗口为2小时30分钟。

#### SHOW TABLES

SHOW TABLES可显示目标数据库的目标模式下的表。

##### 语法格式

```
SHOW TABLES;
```

##### 示例

示例1：显示当前数据库中的表

```sql
> show tables;
+---------------------+
| Tables_in_test      |
+---------------------+
| t                   |
| t1                  |
| time_table          |
+---------------------+
3 rows in set (0.00 sec)
```

示例2：显示不同数据库下的表

```sql
> show tables from a;
+-------------+
| Tables_in_a |
+-------------+
| t           |
+-------------+
1 row in set (0.00 sec)

> show tables from abc;
+---------------+
| Tables_in_abc |
+---------------+
| t             |
| t1            |
+---------------+
2 rows in set (0.00 sec)

> show tables from b;
+-------------+
| Tables_in_b |
+-------------+
| t           |
+-------------+
1 row in set (0.00 sec)
```

#### ALTER TABLE

ALTER TABLE语句用于在已有表中更改表名、添加列和更改列名。

##### 语法格式

```sql
ALTER TABLE <table_name> [RENAME TO <table_name> | RENAME <column_name> TO <column_name> | ADD COLUMN <column_name> <datatype_name>];
```

##### 参数说明

- table_name：表名。
- RENAME TO <table_name>：更改表名。
- RENAME <column_name> TO <column_name>：更改列名。
- ADD COLUMN <column_name> <datatype_name>：增加列。

##### 示例

示例1：更改表名

```sql
> alter table t rename to t1;
```

示例2：更改列名

```sql
> alter table t rename name to new_name;
Query OK, 0 rows affected (0.00 sec)

> show create table t;
+-------+---------------+
| Table | Create Table  |
+-------+---------------+
| t | CREATE TABLE `t` (
`id` int NOT NULL,
`new_name` varchar(10) NOT NULL
) ENGINE=TS
|
+-------+----------------+
1 row in set (0.00 sec)
```

示例3：增加列

```sql
> alter table t add column dt datetime32;
Query OK, 0 rows affected (0.00 sec)

> show create table t;
+-------+--------------+
| Table | Create Table |
+-------+--------------+
| t | CREATE TABLE `t` (
`id` int NOT NULL,
`new_name` varchar(10) NOT NULL,
`dt` datetime
) ENGINE=TS
|
+-------+---------------+
1 row in set (0.00 sec)
```

#### DROP TABLE

DROP TABLE语句用于从数据库中删除表。

##### 语法格式

```sql
DROP TABLE <table_name>;
```

##### 参数说明

- table_name：要删除的表名

##### 示例

示例：删除表

```sql
> show tables;
+---------------------+
| Tables_in_test      |
+---------------------+
| t                   |
| t1                  |
| time_table          |
+---------------------+
3 rows in set (0.00 sec)

> drop table t1;
Query OK, 0 rows affected (0.01 sec)

> show tables;
+---------------------+
| Tables_in_test      |
+---------------------+
| t                   |
| time_table          |
+---------------------+
2 rows in set (0.00 sec)
```

## DML语句

KaiwuDB支持DML语句，对数据进行操作。

### INSERT

创建表后，用户可以使用INSERT语句将每一列对应的值插入到表中。

#### 语法格式

```sql
INSERT INTO <table_name> VALUES (value1, value2, ...);
```

#### 参数说明

- table_name：要写入数据的表名。
- value1, value2, ...：写入数据到列的值。如果创建表时，某个column未被定义为 not null，写入的值可以为null，例如`INSERT INTO table1 values (2, null);`

#### 语法示例

示例：插入一个单行和多行

```sql
# 创建表product,customer和sales

> CREATE TABLE Product ('id' INT4 not null default 0, 'name' STRING(63) not null default 'a', 'brand' STRING(63) not null default 'a', 'brandOwner' STRING(63) not null default 'a', 'weightGrams' FLOAT4 not null default 0.00, 'weightOunce' FLOAT4 not null default 0.00, 'category' STRING(63) not null default 'a', 'price' FLOAT4 not null default 0.00, 'cost' FLOAT4 not null default 0.00, 'profit' FLOAT4 not null default 0.00);
Query OK, 0 rows affected (0.02 sec)

> CREATE TABLE Customer ('id' INT4 not null default 0, 'name' STRING not null default 'a', 'language' STRING not null default 'a', 'state' STRING not null default 'a', 'company' STRING not null default 'a', 'gender' STRING not null default 'a', 'age' INT4 not null default 0);
Query OK, 0 rows affected (0.00 sec)

> CREATE TABLE sales ('order_id' INT4 not null default 0, 'Customer.id' INT4 not null default 0, 'Product.id' INT4 not null default 0, 'channel_name' STRING not null default 'a', 'Date' DATETIME32 not null default '2023-01-01 00:00:00', 'qty' BIGINT not null default 0, 'total_price' DOUBLE not null default 0.00);
Query OK, 0 rows affected (0.00 sec)

# 插入数据

> INSERT INTO Product VALUES ('2','Throwback Cola', 'Pepsi', 'Pepsico','0', '0', 'soda', '12.01', '3.11', '8.9');
Query OK, 1 row affected (0.01 sec)

> INSERT INTO Customer VALUES ('4', 'Julia Kennedy', 'Italian', 'Florida', 'Fivespan', 'Female', '30');
Query OK, 1 row affected (0.00 sec)

> INSERT INTO sales VALUES('8713','366','0','CVS','2013-01-01 00:06:30','6','77.94'),('8713','3263','7','7-11','2013-01-01 00:09:52','2','19.94');
Query OK, 2 rows affected (0.00 sec)

# 查询数据

> select * from Product;
+----+---------------+---------+------------+------------+-------------+---------+-------+------+----------+
| id |     name      |  brand  | brandOwner | weightGrams | weightOunce | category | price | cost | profit |
+----+---------------+---------+------------+------------+-------------+---------+-------+------+----------+
| 2  | Throwback Cola |  Pepsi  |  Pepsico  |     0      |      0      |   soda  | 12.01 | 3.11 |  8.9     |
+----+---------------+---------+------------+------------+-------------+---------+-------+------+----------+
1 row in set (0.00 sec)

> select * from Customer;
+----+----------------+----------+----------+----------+--------+------+
| id |      name      | language |  state   | company  | gender | age  |
+----+----------------+----------+----------+----------+--------+------+
| 4  | Julia Kennedy  | Italian  | Florida  | Fivespan | Female |  30  |
+----+----------------+----------+----------+----------+--------+------+
1 row in set (0.00 sec)

> select * from sales;
+----------+-------------+------------+--------------+---------------------+------+-------------+
| order_id | Customer.id | Product.id | channel_name | Date                | qty  | total_price |
+----------+-------------+------------+--------------+---------------------+------+-------------+
|     8713 |         366 |          0 | CVS          | 2013-01-01 00:06:30 |    6 |       77.94 |
|     8713 |        3263 |          7 | 7-11         | 2013-01-01 00:09:52 |    2 |       19.94 |
+----------+-------------+------------+--------------+---------------------+------+-------------+
2 rows in set (0.00 sec)
```

### UPDATE

更新表中某行数据。

#### 语法格式

```sql
UPDATE <table_name> SET <column_name> = <literal_value>, [ <column_name> = <literal_value> ] WHERE <filter_condition>;
```

#### 参数说明

- table_name：要更新的表名。
- column_name：要更新的列名。
- literal_value：更新的字段值。
- filter_condition：更新时的过滤条件。

#### 语法示例

示例1：更新一行中的某一列

```sql
> select * from Customer;
+----+----------------+----------+----------+----------+--------+------+
| id |      name      | language |  state   | company  | gender | age  |
+----+----------------+----------+----------+----------+--------+------+
| 4  | Julia Kennedy  | Italian  | Florida  | Fivespan | Female |  30  |
+----+----------------+----------+----------+----------+--------+------+
1 row in set (0.00 sec)

> UPDATE Customer SET state='Ohio' WHERE name='Julia Kennedy' ;
Query OK, 1 row affected (0.00 sec)

> select * from Customer;
+----+----------------+----------+-------+----------+--------+------+
| id |      name      | language | state | company  | gender | age  |
+----+----------------+----------+-------+----------+--------+------+
| 4  | Julia Kennedy  | Italian  |  Ohio | Fivespan | Female |  30  |
+----+----------------+----------+-------+----------+--------+------+
1 row in set (0.00 sec)
```

示例2：更新一行中的多个列的值

```sql
> select * from Product;
+----+---------------+---------+------------+------------+-------------+---------+-------+------+--------+
| id |     name      |  brand  | brandOwner | weightGrams| weightOunce | category| price | cost | profit |
+----+---------------+---------+------------+------------+-------------+---------+-------+------+--------+
| 2  |Throwback Cola |  Pepsi  |  Pepsico   |     0      |      0      |   soda  | 12.01 | 3.11 |  8.9   |
+----+---------------+---------+------------+------------+-------------+---------+-------+------+--------+
1 row in set (0.00 sec)

> update Product set weightGrams=1,weightOunce=1 where id=2 and name='Throwback Cola';
Query OK, 1 row affected (0.00 sec)

> select * from Product;
+----+---------------+---------+------------+------------+-------------+---------+-------+------+--------+
| id |     name      |  brand  | brandOwner | weightGrams| weightOunce | category| price | cost | profit |
+----+---------------+---------+------------+------------+-------------+---------+-------+------+--------+
| 2  | Throwback Cola|  Pepsi  |  Pepsico   |     1      |      1      |   soda  | 12.01 | 3.11 |  8.9   |
+----+---------------+---------+------------+------------+-------------+---------+-------+------+--------+
1 row in set (0.00 sec)
```

示例3：更新所有列

```sql
> select * from sales;
+----------+-------------+------------+--------------+---------------------+------+-------------+
| order_id | Customer.id | Product.id | channel_name | Date                | qty  | total_price |
+----------+-------------+------------+--------------+---------------------+------+-------------+
|     8713 |         366 |          0 | CVS          | 2013-01-01 00:06:30 |    6 |       77.94 |
|     8713 |        3263 |          7 | 7-11         | 2013-01-01 00:09:52 |    2 |       19.94 |
+----------+-------------+------------+--------------+---------------------+------+-------------+
2 rows in set (0.00 sec)

> update sales set total_price=0;
Query OK, 2 rows affected (0.00 sec)

> select * from sales;
+----------+-------------+------------+--------------+---------------------+------+-------------+
| order_id | Customer.id | Product.id | channel_name | Date                | qty  | total_price |
+----------+-------------+------------+--------------+---------------------+------+-------------+
|     8713 |         366 |          0 | CVS          | 2013-01-01 00:06:30 |    6 |           0 |
|     8713 |        3263 |          7 | 7-11         | 2013-01-01 00:09:52 |    2 |           0 |
+----------+-------------+------------+--------------+---------------------+------+-------------+
2 rows in set (0.00 sec)
```

### DELETE

DELETE语句用于删除一个表中的行数据。

#### 语法格式

```sql
DELETE FROM <table_name> WHERE <filter_condition>;
```

> 注：必须带删除条件。

#### 参数说明

- table_name：要删除的行所在表的表名。
- filter_condition：要删除行的过滤条件。

#### 语法示例

示例：删除数据

```sql
# 创建表
> create default table t1(id int not null default 0);
Query OK, 0 rows affected (0.01 sec)

# 插入数据
> insert into t1 values(1),(2),(3);
Query OK, 3 row affected (0.00 sec)

# 查询数据
> select * from t1;
+----+
| id |
+----+
|  1 |
|  2 |
|  3 |
+----+
3 rows in set (0.00 sec)

# 删除数据
> delete from t1 where id=1;
Query OK, 1 row affected (0.01 sec)

# 再次查询数据
> select * from t1;
+------+
| id   |
+------+
|  2   |
|  3   |
+------+
2 rows in set (0.00 sec)
```

### SELECT

数据库创建后，用户可以使用SELECT语句进行读取和处理KaiwuDB中的数据。

#### 语法格式

```sql
SELECT [table_name.]<column_name>
| [function_name]
| [number_constant]
| [string_constant]
| [time_constant]
| [CASE WHEN <bool_expression> THEN <simple_expression> [WHEN <bool_expression> THEN <simple_expression> … ] ELSE <simple_expression> END]
[ AS <string_identifier> ]
FROM <table_name>
[ WHERE <column_name> LIKE [%] <string_constant> [%]
| <column_name> <comparison_operator> <expression>
|<column_name> BETWEEN <constant_expression> AND <constant_expression> [ AND | OR <select_expression>
[group_by_clause [ having_clause ] ]
[order_by_clause]
[limit_clause];
```

当数据列是顺序的且没有空值的情况下时，可采用如下语法进行更快速的范围查询。

```sql
SELECT [table_name.]<column_name>
| [function_name]
| [number_constant]
| [string_constant]
| [time_constant]
| [CASE WHEN <bool_expression> THEN <simple_expression> [ WHEN <bool_expression> THEN <simple_expression> … ] ELSE <simple_expression> END]
[ AS <string_identifier> ]
FROM <table_name>
[ WHERE <column_name> LIKE [%] <string_constant> [%]
| <column_name> <comparison_operator> <expression>
|<column_name>
BETWEEN <constant_expression> AND <constant_expression> of <column_name> [ AND | OR <select_expression> of <column_name>
[group_by_clause [ having_clause ] ]
[order_by_clause]
[limit_clause];
```

> 注：where 条件句使用NULL值比较，语法是is null 或is not null; 例如，select a from t1 where a is NULL；where 条件句中使用<、>、= 与NULL比较时，均返回0行结果；where 除上面is null或is not null过滤语句外，其余情况NULL值均不参与计算， NULL值的行会被忽略掉。例如select a from t4 where a>1，查询a列大于1的行，NULL值的行会被忽略，不进行显示。

#### 参数说明

- table_name：查询的表名。
- column_name：列名称。
- function_name：函数名称。
- simple_expression：函数表达式。
- number_constant：数值常量。
- string_constant：字符串常量。
- time_constant：时间常量。
- bool_expression：布尔表达式。
- string_identifier：字符串标识符。
- select_expression：选择表达式。
- comparison_operator：比较符如：= > | < | >= | <= | =。
- expression：表达式。
- group_by_clause：分组子句：GROUP BY < select_expression >。
- having_clause：having子句：HAVING < select_expression> <comparison> <constant_expression >。
- order_by_clause：排序子句：ORDER BY < select_expression> [ ASC | DESC]。
- limit_clause：limit子句：LIMIT <constant_int>。

#### 语法示例

示例1：一般查询

```sql
> select * from sales;
+----------+-------------+------------+--------------+---------------------+------+-------------+
| order_id | Customer.id | Product.id | channel_name | Date                | qty  | total_price |
+----------+-------------+------------+--------------+---------------------+------+-------------+
|     8713 |         366 |          0 | CVS          | 2013-01-01 00:06:30 |    6 |       77.94 |
|     8713 |        3263 |          7 | 7-11         | 2013-01-01 00:09:52 |    2 |       19.94 |
+----------+-------------+------------+--------------+---------------------+------+-------------+
2 rows in set (0.00 sec)
```

示例2：WHERE子句指定带有条件过滤器的查询

```sql
> select * from t;
+------+---------------------+
| id   |         dt          |
+------+---------------------+
|  1   | 2022-12-22 08:48:46 |
|  2   | 2022-12-22 08:48:56 |
|  3   | 2022-12-22 08:49:05 |
|  4   | 2022-12-22 08:49:14 |
|  5   | 2022-12-22 08:49:22 |
|  1   | 2022-12-22 08:52:14 |
|  2   | 2022-12-22 08:52:20 |
|  3   | 2022-12-22 08:52:26 |
|  4   | 2022-12-22 08:52:33 |
|  5   | 2022-12-22 08:52:39 |
+------+---------------------+
10 rows in set (0.00 sec)

> select * from t where id=3;
+------+---------------------+
| id   |         dt          |
+------+---------------------+
|  3   | 2022-12-22 08:49:05 |
|  3   | 2022-12-22 08:52:26 |
+------+---------------------+
2 rows in set (0.00 sec)
```

示例3：WHERE子句中使用字符串模式匹配查询

```sql
> create table t1(id int not null default 0,name varchar(50) not null default 'a',dt datetime32 not null default '2023-01-01 00:00:00');  
Query OK, 0 rows affected (0.00 sec)  

> insert into t1 select 1,"shanghai1",now();  
Query OK, 1 row affected (0.00 sec)  

> insert into t1 select 2,"beijing1",now();  
Query OK, 1 row affected (0.00 sec)  

> insert into t1 select 3,"tianjing1",now();  
Query OK, 1 row affected (0.00 sec)  

> insert into t1 select 4,"shandong1",now();  
Query OK, 1 row affected (0.00 sec)  

> select * from t1;  
+------+-----------+---------------------+  
| id   | name      | dt                  |  
+------+-----------+---------------------+  
|    1 | shanghai1 | 2022-12-22 09:17:29 |  
|    2 | beijing1  | 2022-12-22 09:17:41 |  
|    3 | tianjing1 | 2022-12-22 09:17:51 |  
|    4 | shandong1 | 2022-12-22 09:18:03 |  
+------+-----------+---------------------+  
4 rows in set (0.00 sec)  

> select * from t1 where name like '%1';  
+------+-----------+---------------------+  
| id   | name      | dt                  |  
+------+-----------+---------------------+  
|    1 | shanghai1 | 2022-12-22 09:17:29 |  
|    2 | beijing1  | 2022-12-22 09:17:41 |  
|    3 | tianjing1 | 2022-12-22 09:17:51 |  
|    4 | shandong1 | 2022-12-22 09:18:03 |  
+------+-----------+---------------------+  
4 rows in set (0.00 sec)  

> select * from t1 where name like 'shanghai%';  
+------+-----------+---------------------+  
|   id | name      | dt                  |  
+------+-----------+---------------------+  
|    1 | shanghai1 | 2022-12-22 09:17:29 |  
+------+-----------+---------------------+  
1 row in set (0.00 sec)  

> select * from t1 where name regexp 'shanghai';  
+------+-----------+---------------------+  
|   id | name      | dt                  |  
+------+-----------+---------------------+  
|    1 | shanghai1 | 2022-12-22 09:17:29 |  
+------+-----------+---------------------+  
1 row in set (0.00 sec)
```

示例4：GROUP BY 分组查询

```sql
> select * from t;
+------+---------------------+
|  id  |         dt          |
+------+---------------------+
|  1   | 2022-12-22 08:48:46 |
|  2   | 2022-12-22 08:48:56 |
|  3   | 2022-12-22 08:49:05 |
|  4   | 2022-12-22 08:49:14 |
|  5   | 2022-12-22 08:49:22 |
|  1   | 2022-12-22 08:52:14 |
|  2   | 2022-12-22 08:52:20 |
|  3   | 2022-12-22 08:52:26 |
|  4   | 2022-12-22 08:52:33 |
|  5   | 2022-12-22 08:52:39 |
+------+---------------------+
10 rows in set (0.00 sec)

> select id,count(id) as ct from t group by id;
+------+------+
|  id  |  ct  |
+------+------+
|  1   |  2   |
|  2   |  2   |
|  3   |  2   |
|  4   |  2   |
|  5   |  2   |
+------+------+
5 rows in set (0.00 sec)
```

示例5：使用 HAVING 子句来指定聚合函数的过滤条件

```sql
> select * from t;
+------+----------+-----------+-----------+
|  id  |   city   |   price   |   cost    |
+------+----------+-----------+-----------+
|  1   | beijing  |   18.09   |   21.23   |
|  2   | tianjin  |  19.209999|   20.33   |
|  3   | shandong | 22.450001 | 28.389999 |
|  4   | shanghai |   33      |   34      |
|  5   | nanjing  |   33      |   34      |
|  5   | nanjing  |   34      |   35      |
|  5   | nanjing  |   36      |   36      |
|  4   | shanghai |   34      |   34      |
|  4   | shanghai |   34      |   35      |
|  4   | shanghai |   36      |   37      |
|  3   | shandong | 22.450001 | 28.389999 |
|  2   | tianjin  |   19.41   | 21.360001 |
+------+----------+-----------+-----------+
12 rows in set (0.00 sec)

> select city,sum(price) from t group by city;
+----------+-------------+
|   city   | SUM(price)  |
+----------+-------------+
|  beijing  |   18.09    |
|  tianjin  |  38.619999 |
| shandong  | 44.900002  |
| shanghai  |    137     |
|  nanjing  |    103     |
+----------+-------------+
5 rows in set (0.00 sec)

> select city,sum(price) from t group by city having sum(price)>100;
+----------+------------+
|   city   | SUM(price) |
+----------+------------+
| shanghai |    137     |
|  nanjing |    103     |
+----------+------------+
2 rows in set (0.00 sec)
```

示例6：带有ORDER BY子句的

```sql
> select id,count(id) as ct from t group by id order by id desc;
+------+------+
|  id  |  ct  |
+------+------+
|  5   |  2   |
|  4   |  2   |
|  3   |  2   |
|  2   |  2   |
|  1   |  2   |
+------+------+
5 rows in set (0.00 sec)
```

示例7：使用LIMIT子句指定显示的记录数

```sql
> select * from t limit 8;
+------+----------+-----------+-----------+
|  id  |   city   |   price   |   cost    |
+------+----------+-----------+-----------+
|   1  |  beijing |   18.09   |   21.23   |
|   2  |  tianjin | 19.209999 |   20.33   |
|   3  | shandong | 22.450001 | 28.389999 |
|   4  | shanghai |    33     |    34     |
|   5  | nanjing  |    33     |    34     |
|   5  | nanjing  |    34     |    35     |
|   5  | nanjing  |    36     |    36     |
|   4  | shanghai |    34     |    34     |
+------+----------+-----------+-----------+
8 rows in set (0.00 sec)
```

### JOIN

KaiwuDB目前只支持INNER JOIN即内连接，内连接运算是组合两个表中的记录，只要在公共字段之中有相符的值。内连接使用INNER JOIN关键字连接两张表，并使用ON子句来设置连接条件。

#### 语法格式

```sql
SELECT [<table_name>.]<column_name> FROM <table_name> INNER JOIN <table_name> <ON_clause>;
```

#### 参数说明

- column_name：需要查询的字段名称。
- table_name：需要内连接的表名。
- ON_clause：ON子句用来设置内连接的连接条件。

#### 语法示例

示例：

在tb_students_info表和tb_course表之间，使用内连接查询学生姓名和相对应的课程名称

```sql
> SELECT s.name,c.course_name FROM tb_students_info s INNER JOIN tb_course c ON s.course_id = c.id;
+--------+-------------+
|  name  | course_name |
+--------+-------------+
|  Dany  |     Java    |
|  Green |     MySQL   |
|  Henry |     Java    |
|  Jane  |    Python   |
|   Jim  |     MySQL   |
|  John  |      Go     |
|  Lily  |      Go     |
| Susan  |     C++     |
| Thomas |     C++     |
|  Tom   |     C++     |
+--------+-------------+
10 rows in set (0.00 sec)
```

### UNION ALL

UNION ALL称为并运算，用于合并来自两个或多个 SELECT 语句的结果集，不做去除重复结果集处理。

#### 语法格式

```sql
[<select_clause>] UNION ALL [<select_clause>]
```

#### 参数说明

- select_clause：SELECT子句,其返回值为一个结果集。

#### 语法示例

示例：返回两个查询结果集。

```sql
> select * from t limit 8 union all select * from t limit 8 offset 2;
+----+----------+-------+-------+
| id |   city   | price | cost  |
+----+----------+-------+-------+
| 1  | beijing  | 18.09 | 21.23 |
| 2  | tianjin  | 19.21 | 20.33 |
| 3  | shandong | 22.45 | 28.39 |
| 4  | shanghai | 33.00 | 34.00 |
| 5  | nanjing  | 33.00 | 34.00 |
| 5  | nanjing  | 34.00 | 35.00 |
| 5  | nanjing  | 36.00 | 36.00 |
| 4  | shanghai | 34.00 | 34.00 |
| 3  | shandong | 22.45 | 28.39 |
| 4  | shanghai | 33.00 | 34.00 |
| 5  | nanjing  | 33.00 | 34.00 |
| 5  | nanjing  | 34.00 | 35.00 |
| 5  | nanjing  | 36.00 | 36.00 |
| 4  | shanghai | 34.00 | 34.00 |
| 4  | shanghai | 34.00 | 35.00 |
| 4  | shanghai | 36.00 | 37.00 |
+----+----------+-------+-------+
16 rows in set (0.00 sec)
```

## 其他语句

### USE

#### 语法格式

```sql
USE <database_name>;
```

#### 参数说明

- database_name：数据库名称。

#### 语法示例

示例：选择数据库

```sql
> use test_database;
Database changed
```

### SHOW

- SHOW CREATE 语句用于显示现有表的创建语句。
- SHOW DATABASES 语句用于显示现有数据库。
- SHOW TABLES 语句用于显示当前库下的所有表。
- SHOW PROCESSLIST语句用于显示当前正在执行的所有语句。

#### 语法格式

SHOW管理语句语法格式如下：

```sql
SHOW CREATE TABLE <table_name>;
SHOW DATABASES;
SHOW TABLES;
SHOW PROCESSLIST;
```

#### 参数说明

- table_name：表名称。

#### 语法示例

示例1：查看表的创建语句

```sql
> show create table t;
+-------+------------------------------------------------------------+
| Table | Create Table                                               |
+-------+------------------------------------------------------------+
| t | CREATE TABLE `t` (
`id` int NOT NULL
) ENGINE=TS
|
+-------+------------------------------------------------------------+
1 row in set (0.00 sec)
```

示例2：查看所有数据库名

```sql
> show databases;
+-----------+
| Database  |
+-----------+
| a         |
| abc       |
| b         |
| log1      |
| szq_test  |
+-----------+
5 rows in set (0.00 sec)
```

示例3：查看当前库下的所有表名

```sql
> show tables;
+---------------------+
| Tables_in_test      |
+---------------------+
| Customer            |
| Product             |
| s_t1                |
| sales               |
| t                   |
| t1                  |
| time_table          |
+---------------------+
7 rows in set (0.00 sec)
```

示例4：查看当前正在执行的SQL语句

```sql
> show processlist;
+-----+------+------------+------+---------+------+-----------+------------------+
| ID  | USER | HOST       | DB   | COMMAND | TIME | STATE     | INFO             |
+-----+------+------------+------+---------+------+-----------+------------------+
| 109 | root | localhost  | test | Query   | 0    | executing | show processlist |
+-----+------+------------+------+---------+------+-----------+------------------+
1 row in set (0.00 sec)
```

# 内置函数

## 聚合函数

| 函数             | 描述                                                                                                                                                                                                                   |
|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AVG              | 数字列的平均值。 支持int4、smallint、bigint、biginteger、float4、double、bool数据类型。                                                                                                                                |
| CORR(col1,col2)  | 两个数字列之间的相关性：包括数据的变化趋势的方向以及程度。值范围-1到+1，0表示两个变量不相关，正值表示正相关，负值表示负相关，值越大相关性越强。 支持int4、smallint、bigint、biginteger、float4、double、bool数据类型。 |
| COUNT            | 总行数，支持所有数据类型。                                                                                                                                                                                             |
| FIRST            | 所选列的第一个值。 支持int4、smallint、bigint、biginteger、float4、double、date、datetime、timestamp、timestamp(3)、bool数据类型。                                                                                     |
| LAST             | 所选列的最后一个值。支持int4、smallint、bigint、biginteger、float4、double、date、datetime、timestamp、timestamp(3)、bool数据类型。                                                                                    |
| MAX              | 数字列的最大值。支持int4、smallint、bigint、biginteger、float4、double、string、char、varchar、date、datetime、timestamp、timestamp(3)、bool数据类型。                                                                 |
| MIN              | 数字列的最小值。支持int4、smallint、bigint、biginteger、float4、double、string、char、varchar、date、datetime、timestamp、timestamp(3)、bool数据类型。                                                                 |
| STDDEV           | (Population)数字列的标准偏差。支持int4、smallint、bigint、biginteger、float4、double、bool数据类型。                                                                                                                   |
| STDDEV_SAMP      | 数字列的样本标准偏差。支持int4、smallint、bigint、biginteger、float4、double、bool数据类型。                                                                                                                           |
| SUM              | 数字列的总和。支持int4、smallint、bigint、biginteger、float4、double、bool数据类型。                                                                                                                                   |
| VARIANCE         | (Population)数字列的方差。支持int4、smallint、bigint、biginteger、float4、double、bool数据类型。                                                                                                                       |

> 注：使用count(*)统计行数时，行数结果包含NULL值的行数；sum、avg、count、first、last及其它聚合函数指定列聚合运算，NULL不参与运算。

### 用法示例

部分函数使用参考示例如下：

示例：CORR(col1,col2)函数用法

```sql
> select corr(col1,col2) from test_int;
+------------------+
| corr(col1, col2) |
+------------------+
| -0.5             |
+------------------+
1 row in set (0.00 sec)
```

## 日期和时间函数

| 函数                                | 描述                                                         |
| ----------------------------------- | ------------------------------------------------------------ |
| ADDDATE(datetime,time-interval)     | 将时间间隔添加到日期时间。 时间间隔可以是表示天数的整数、时间值、时间窗口说明符或INTERVAL值。 INTERVAL指定为：INTERVAL expr unit expr确定间隔值，单位可以是SECOND、MINUTE、HOUR、DAY、WEEK、MONTH、QUARTER或YEAR，表示时间单位。 支持string、char、varchar、date、datetime、timestamp、timestamp(3)数据类型。 |
| ADDTIME(datetime,time)              | 将时间值添加到日期时间（用法类似ADDDATE）。 时间参数可以是表示秒的整数、时间窗口说明符、时间表达式或INTERVAL值。 支持string、char、varchar、date、datetime、timestamp、timestamp(3)数据类型。 |
| CURDATE()                           | 返回当前日期，支持所有数据类型。                             |
| DATEDIFF(date1,date2)               | 两个日期时间之间的差异。 函数返回(date1 - date2)之间的天数差异。支持int4、smallint、bigint、biginteger、string、char、varchar、date、datetime、timestamp、timestamp(3)、bool数据类型。 |
| DATE_FORMAT(date-time,format)       | 将指定格式的日期时间转换为CHAR字符串。支持int4、smallint、bigint、biginteger、float4、double、string、char、varchar、date、datetime、timestamp、timestamp(3)、bool数据类型。 格式字符串中可以使用以下格式说明符： %a	缩写的工作日名称（Sun..Sat）%A	完整的工作日名称（星期日..星期六）%b	缩写月份名称（Jan..Dec）%B	全月名称（January..December）%C	年份除以100(00-99)%d	一个月中的第几天(00-31)%D	MM/DD/YY 日期(08/23/01)%e	一个月中的第几天(0-31)%F	YYYY-MM-DD日期(2016-08-23)%H	24小时格式的小时(00-23)%i	分钟(00-59)%I	12小时格式的小时(01-12)%k	24小时格式的小时(00-23)%l	12小时格式的小时(01-12)%m	月(00-12)%M	分钟(00-59)%p	AM（上午）或PM（下午）%s	秒(00-59)%S	秒(00-59)%T	HH:MM:SS(14:55:02)%Y	年(2017)%%	A % character |
| DATE_TRUNC(date-time,datepart)      | 将日期时间截断为指定的日期部分。  date部分可用的日期部分类型：  year,quarter,month,week,day,hour,minute。  支持int4、smallint、bigint、biginteger、string、char、varchar、date、datetime、timestamp、timestamp(3)、bool数据类型。 |
| DATE()                              | 返回日期时间的日期部分。支持string、char、varchar、date、datetime、timestamp、timestamp(3)数据类型。 |
| DAY()                               | DAYOFMONTH()的同义词。支持int4、date、datetime、timestamp、timestamp(3)数据类型。 |
| DAYOFMONTH()                        | 返回日期时间的月份中的第几天。支持int4、date、datetime、timestamp、timestamp(3)数据类型。 |
| DAYOFWEEK()                         | 返回日期时间的工作日索引（1 = 星期日，2 = 星期一，...，7 = 星期六）。支持int4、date、datetime、timestamp、timestamp(3)数据类型。 |
| HOUR()                              | 返回日期时间的小时部分。支持int4、date、datetime、timestamp、timestamp(3)数据类型。 |
| MINUTE()                            | 返回日期时间的分钟部分。支持int4、date、datetime、timestamp、timestamp(3)数据类型。 |
| MONTH()                             | 返回日期时间的月份。支持int4、date、datetime、timestamp、timestamp(3)数据类型。 |
| NOW()                               | 当前日期时间，无须传入参数。                                 |
| SECOND()                            | 返回日期时间的秒。支持int4、date、datetime、timestamp、timestamp(3)数据类型。 |
| SUBTIME(date-time, time-interval)   | 从日期时间减去时间间隔后返回一个新的日期时间。  时间间隔可以是代表秒数的整数或时间窗口说明符。  支持string、char、varchar、date、datetime、timestamp、timestamp(3)数据类型。 |
| TIME_BUCKET(date-time, time_window) | 将同一时间窗口内的所有时间日期转换为时间窗口的起始时间日期，返回的时间日期的数据类型与写入函数的时间日期数据类型一致。时间窗的长度由时间窗说明符指示。  支持int4、smallint、bigint、biginteger、float4、double、string、char、varchar、date、datetime、timestamp、timestamp(3)、bool数据类型。 |
| TIMESTAMP()                         | 日期时间的TIMESTAMP。支持int4、date、datetime、timestamp、timestamp(3)数据类型。 |
| WEEK()                              | 日期时间的周数。支持int4、date、datetime、timestamp、timestamp(3)数据类型。 |
| WEEKDAY()                           | 0（星期日）- 6（星期六），一天中的工作日。支持int4、date、datetime、timestamp、timestamp(3)数据类型。 |
| YEAR()                              | 日期时间的年份。支持int4、date、datetime、timestamp、timestamp(3)数据类型。 |

> 注：DAY()、DATE()、ADDTIME()等函数对NULL值进行计算时，结果仍为NULL。

### 用法示例

示例1：ADDDATE函数用法

```sql
> select d,adddate(d,interval 1 day) from testa;  
+---------------------+---------------------------+
|        d            | adddate(d,INTERVAL 1 day) |
+---------------------+---------------------------+
| 2022-12-14 10:00:20 | 2022-12-15 10:00:20       |
| 2022-12-14 11:00:20 | 2022-12-15 11:00:20       |
| 2022-12-14 12:00:20 | 2022-12-15 12:00:20       |
| 2022-12-14 13:00:20 | 2022-12-15 13:00:20       |
+---------------------+---------------------------+
4 rows in set (0.00 sec)
```

示例2：CURDATE函数用法

```sql
> select CURDATE();  
+------------+  
| CURDATE()  |  
+------------+  
| 2022-12-20 |  
+------------+  
1 row in set (0.00 sec)
```

示例3：DATEDIFF函数用法

```sql
> select datediff('2022-12-22','2022-12-21');  
+-------------------------------------+  
| datediff('2022-12-22','2022-12-21') |  
+-------------------------------------+  
|                                   1 |  
+-------------------------------------+  
1 row in set (0.00 sec)
```

示例4：DATE_FORMAT函数用法

```sql
> select DATE_FORMAT(NOW(),'%m-%d-%Y');  
+-------------------------------+  
| DATE_FORMAT(NOW(),'%m-%d-%Y') |  
+-------------------------------+  
| 12-20-2022                    |  
+-------------------------------+  
1 row in set (0.00 sec)
```

示例5：DATE_TRUNC函数用法

```sql
> select now(),DATE_TRUNC(now(),'year');  
+---------------------+--------------------------+  
| now()               | DATE_TRUNC(now(),'year') |  
+---------------------+--------------------------+  
| 2022-12-20 03:02:09 | 2022-01-01 00:00:00      |  
+---------------------+--------------------------+  
1 row in set (0.00 sec)
```

示例6：DATE函数用法

```sql
> select now(),date(now());  
+---------------------+-------------+  
| now()               | date(now()) |  
+---------------------+-------------+  
| 2022-12-20 03:18:49 | 2022-12-20  |  
+---------------------+-------------+  
1 row in set (0.01 sec)
```

示例7：DAYOFMONTH函数用法

```sql
> select now(),dayofmonth(now());  
+---------------------+-------------------+  
| now()               | dayofmonth(now()) |  
+---------------------+-------------------+  
| 2022-12-20 03:19:26 |                20 |  
+---------------------+-------------------+  
1 row in set (0.00 sec)
```

示例8：DAYOFWEEK函数用法

```sql
> select now(),dayofweek(now());  
+---------------------+------------------+  
| now()               | dayofweek(now()) |  
+---------------------+------------------+  
| 2022-12-20 03:20:18 |                3 |  
+---------------------+------------------+  
1 row in set (0.00 sec)
```

示例9：SUBTIME函数用法

```sql
> select now(),SUBTIME(now(),'1d');  
+---------------------+---------------------+  
| now()               | SUBTIME(now(),'1d') |  
+---------------------+---------------------+  
| 2022-12-20 09:48:11 | 2022-12-19 09:48:11 |  
+---------------------+---------------------+  
1 row in set (0.00 sec)
```

示例10：TIME_BUCKET函数用法

```sql
> select d,TIME_BUCKET(d,'1d') from testa; 
+---------------------+---------------------------+
|         d           |  TIME_BUCKET(d,'1d')      |
+---------------------+---------------------------+
| 2022-12-14 10:00:20 | 2022-12-14 00:00:00       |
| 2022-12-14 11:00:20 | 2022-12-14 00:00:00       |
| 2022-12-14 12:00:20 | 2022-12-14 00:00:00       |
| 2022-12-14 13:00:20 | 2022-12-14 00:00:00       |
+---------------------+---------------------------+
4 rows in set (0.00 sec)
```

示例11：TIMESTAMP函数用法

```sql
> select timestamp(now());  
+------------------+  
| timestamp(now()) |  
+------------------+  
|       1671587789 |  
+------------------+  
1 row in set (0.00 sec)
```

示例12：WEEKDAY函数用法

```sql
> select now(),weekday(now());  
+---------------------+----------------+  
| now()               | weekday(now()) |  
+---------------------+----------------+  
| 2022-12-21 02:22:18 |              3 |  
+---------------------+----------------+  
1 row in set (0.00 sec)
```

## 数学和数值函数

| 函数                | 描述                                                                                                 |
|---------------------|------------------------------------------------------------------------------------------------------|
| CEIL()              | 返回大于或等于数字的最小整数。支持int4、smallint、bigint、biginteger、float4、double、bool数据类型。 |
| CEILING()           | 与CEIL()相同。支持int4、smallint、bigint、biginteger、float4、double、bool数据类型。                 |
| COS()               | 返回弧度数的余弦。支持int4、smallint、bigint、biginteger、float4、double、bool数据类型。             |
| FLOOR()             | 返回小于或等于数字的最大整数。支持int4、smallint、bigint、biginteger、float4、double、bool数据类型。 |
| PI()                | 返回PI的常量值。支持所有数据类型。                                                                   |
| POW(base, exponent) | 计算基数的幂指数。支持int4、smallint、bigint、biginteger、float4、double、bool数据类型。             |
| POWER()             | 与POW()相同。支持int4、smallint、bigint、biginteger、float4、double、bool数据类型。                  |
| ROUND()             | 返回数字的整数。支持int4、smallint、bigint、biginteger、float4、double、bool数据类型。               |
| SIN()               | 返回弧度数的正弦。支持int4、smallint、bigint、biginteger、float4、double、bool数据类型。             |
| SQRT()              | 计算平方根。支持int4、smallint、bigint、biginteger、float4、double、bool数据类型。                   |

> 注：NULL值的四则运算、round()、pow()等数学和数值函数，运算结果为NULL

### 用法示例

示例：POW函数用法。

```sql
> select pow(2,3);
+----------+
| pow(2,3) |
+----------+
| 8        |
+----------+
1 row in set (0.00 sec)
```

## 字符串函数

| 函数                          | 描述                                                                                                                                                                                                                                 |
|-------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CONCAT(string1, string2, ...) | 将多个字符串参数连接成一个CHAR字符串。支持int4、smallint、bigint、biginteger、float4、double、string、char、varchar、date、datetime、timestamp、timestamp(3)、bool数据类型。                                                         |
| FORMAT(number, precision)     | 将FLOAT4或DOUBLE转换为具有指定精度的CHAR字符串。支持int4、smallint、bigint、biginteger、float4、double、string、char、varchar、binary、timestamp、bool数据类型。                                                                     |
| LEFT(string, n)               | 返回字符串中指定的最左边字符。支持int4、smallint、bigint、biginteger、float4、double、string、char、varchar、date、datetime、ipv4、ipv6、binary、varbinary、timestamp、timestamp(3)、bool数据类型。                                  |
| LENGTH()                      | 返回字符串长度。支持string、char、varchar、binary、varbinary数据类型。                                                                                                                                                               |
| STRPOS(string1,string2)       | 返回子字符串在另一个字符串中的位置。 返回string2在string1中第一次出现的位置。如果string2不在string1中，返回0。 支持string、char、varchar数据类型。                                                                                   |
| LOWER()                       | 将指定字符串中的所有字母转换为小写。支持所有数据类型。                                                                                                                                                                               |
| LPAD(string, n, padstring)    | 返回用指定字符串左填充的 CHAR字符串 string字符或者参数 n 字符的长度，是返回的字符串的数量，如果这个数量比原字符串的长度要短，lpad函数将会把字符串截取成从左到右的n个字符 padstring要粘贴到string的左边的字符串。支持所有数据类型。   |
| LTRIM()                       | 删除前导空格。支持所有数据类型。                                                                                                                                                                                                     |
| RIGHT(string, n)              | 返回字符串中指定的最右边字符数。支持所有数据类型。                                                                                                                                                                                   |
| RPAD(string, n, padstring)    | 返回用指定字符串右填充的 CHAR 字符串。 string字符或者参数 n字符的长度，是返回的字符串的数量，如果这个数量比原字符串的长度要短，lpad函数将会把字符串截取成从左到右的n个字符 padstring要粘贴到string的左边的字符串。支持所有数据类型。 |
| RTRIM()                       | 从字符串中删除尾随空格。支持所有数据类型。                                                                                                                                                                                           |
| SUBSTR(string, pos, len)      | 返回指定的CHAR子字符串 String：原字符串 Pos：起始位置 Len：截取长度。 支持所有数据类型。                                                                                                                                             |
| SUBSTRING()                   | 和SUBSTR()相同。支持所有数据类型。                                                                                                                                                                                                   |
| UPPER()                       | 将指定字符串中的所有字母转换为大写。支持所有数据类型。                                                                                                                                                                               |
| CAST(expr AS new_type)        | 将数据转换为其他类型。支持支持int4、smallint、bigint、biginteger、float4、double、char、varchar、date、datetime、ipv4、ipv6、binary、varbinary、timestamp、timestamp(3)、bool数据类型。                                              |

> 注：LOWER、RIGHT等字符串函数对NULL值进行计算时，结果仍为NULL。

### 用法示例

示例1：CONCAT函数用法

```sql
> select concat('a','b','c','d');  
+-------------------------+  
| concat('a','b','c','d') |  
+-------------------------+  
| abcd                    |  
+-------------------------+  
1 row in set (0.00 sec)
```

示例2：FORMAT函数用法

```sql
> select FORMAT(1.1234,2);  
+------------------+  
| FORMAT(1.1234,2) |  
+------------------+  
| 1.12             |  
+------------------+  
1 row in set (0.00 sec)
```

示例3：LPAD函数用法

```sql
> select LPAD('a123',8,'b');  
+--------------------+  
| LPAD('a123',8,'b') |  
+--------------------+  
| bbbba123           |  
+--------------------+  
1 row in set (0.00 sec)
```

示例4：SUBSTR函数用法

```sql
> select SUBSTR('abcdefg',2,3);  
+-----------------------+  
| SUBSTR('abcdefg',2,3) |  
+-----------------------+  
| bcd                   |  
+-----------------------+  
1 row in set (0.00 sec)
```

