---
title: 声明
id: declare-sql
---

# 声明

`DECLARE` 语句用于定义程序本地的以下项目：

- 自定义变量
- 处理程序
- 游标

::: warning 说明

- `DECLARE` 语句仅允许在存储过程中的 `BEGIN ... END` 复合语句内使用，并且必须位于复合语句的开头，位于其他任何语句之前。
- 声明必须遵循一定的顺序。自定义变量声明优先级最高，其次是游标声明，最后是处理程序声明。

:::

## 声明自定义变量

KWDB 支持在存储过程中声明自定义变量。

### 所需权限

无

### 语法格式

![](../../static/sql-reference/declare_var.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `var_name` | 自定义变量的名称。|
| `typename` | 自定义变量的数据类型，支持以下数据类型：INT2、INT4、INT8、FLOAT4、FLOAT8、DECIMAL、STRING、TEXT、CHAR、VARCHAR、TIMESTAMP、TIMESTAMPTZ。 |
| `opt_default_expr` |（可选）自定义变量的默认值。如未设置，则默认值为 NULL。|

### 语法示例

```sql
delimiter \\
CREATE PROCEDURE example_while()
 BEGIN
        declare a int;
        declare d int; 
        set a =1;
        LABEL my_loop:
        WHILE a<3 DO
                select d; 
                set a=a+1;
                LEAVE my_loop;
        ENDWHILE my_loop;
 END \\
```

## 声明处理程序

存储程序执行期间可能会出现需要特殊处理的情况，例如退出当前程序块或继续执行。KWDB 支持为一般情况（例如警告或异常）定义处理程序。

`DECLARE ... HANDLER` 语句用于指定处理一个或多个条件的处理程序。

### 所需权限

无

### 语法格式

![](../../static/sql-reference/declare_continue_handler.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `handler_action` | 指定在执行完处理程序语句后采取的操作。支持以下选项：<br>- `CONTINUE`：执行完处理程序后，继续执行存储过程。<br >- `EXIT`：执行完处理程序后，退出存储过程。|
| `condition_value` | 指定激活处理程序的特定条件。支持以下选项：<br>- `NOT FOUND`：查询无数据 <br>- `SQLEXCEPTION`：执行报错。|
|`sql_stmt`| 待执行的 SQL 语句。|

### 语法示例

- 执行完处理程序后，继续执行存储过程。

    ```sql
    delimiter \\
    create procedure test2() 
    begin 
        declare b int default 0;  -- 确保 b 有初始值
        declare err int default 0;  -- 初始化 err

        -- 声明异常处理程序
        declare continue handler for not found, sqlexception
        begin
            SELECT age FROM employees;
            set err = -1;
        endhandler;

        -- 循环开始
        while b < 1 do 
            set b = b + 2;
            select * from t1;
        endwhile;
        select err, b;
    end \\
    ```

- 执行完处理程序后，退出存储过程。

    ```sql
    delimiter \\
    create procedure test3() 
    begin 
        declare b int default 0;  -- 确保 b 有初始值
        declare err int default 0;  -- 初始化 err

        -- 声明异常处理程序
        declare exit handler for not found, sqlexception
        begin
            SELECT age FROM employees;
            set err = -1;
        endhandler;

        -- 循环开始
        while b < 1 do 
            set b = b + 2;
            select * from t1;
        endwhile;
        select err, b;
    end \\
    ```

## 声明游标

`DECLARE ... CURSOR` 语句用于声明一个游标并将其与 `SELECT` 语句相关联，以便查询游标遍历的行。一个存储程序可能包含多个游标声明，但在给定块中声明的每个游标必须具有唯一的名称。

::: warning 说明
声明游标后，需要先打开游标，然后才能使用游标。有关详细信息，参见[游标](../other-sql-statements/cursor-sql.md)。
:::

### 所需权限

无

### 语法格式

![](../../static/sql-reference/declare_cursor.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `cursor_name` | 待声明游标的名称。游标名称必须唯一。|
| `select_stmt` | `SELECT` 查询子句。<br> **说明**<br> 该 `SELECT` 语句不能包含 `INTO` 子句。|

### 语法示例

```sql
DELIMITER \\
CREATE PROCEDURE process_cursor_example1()
BEGIN 
    declare var_done int; 
    declare var_age int; 
    DECLARE cur CURSOR FOR SELECT age FROM employees; 
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET var_done = 1; 
END \\
```
