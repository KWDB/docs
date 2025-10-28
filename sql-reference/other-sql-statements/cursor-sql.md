---
title: 游标
id: declare-sql
---

# 游标

KWDB 支持在存储过程中使用游标。

::: warning 说明
声明游标后，需要先打开游标，然后才能使用游标。有关如何声明游标的详细信息，参见[声明游标](../other-sql-statements/declare-sql.md#声明游标)。
:::

## 打开游标

`OPEN` 语句用于打开一个之前声明的游标。

### 所需权限

无

### 语法格式

![](../../static/sql-reference/open_cursor.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `cursor_name` | 待打开游标的名称。|

### 语法示例

```sql
DELIMITER \\
CREATE PROCEDURE process_cursor_example1()
BEGIN 
    declare var_done int; 
    declare var_age int; 
    DECLARE cur CURSOR FOR SELECT age FROM employees; 
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET var_done = 1; 
    OPEN cur;
    SELECT * FROM employees;
    LABEL my_loop: 
    WHILE var_done = 0 DO 
        FETCH cur INTO var_age; 
        select var_age;
        IF var_done = 1 THEN
            LEAVE my_loop; 
        ENDIF;                        
    ENDWHILE my_loop; 
    CLOSE cur;        
END \\
```

## 获取游标

`FETCH` 语句用于获取一行数据的赋值到指定的变量中。当赋值到指定的变量时，`FETCH` 语句中指定的输出变量的数量必须与声明游标时 `SELECT` 语句检索的列数保持一致。用户可以通过 `CONTINUE HANDLER` 语句结束游标获取，或通过其他方式退出 `FETCH` 循环。如未正确结束游标获取，导致无法获取数据的值，系统报错 `the fetch cursor has no more data`。

### 所需权限

无

### 语法格式

![](../../static/sql-reference/fetch_cursor.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `cursor_name` | 待获取游标的名称。|
| `cursor_list` | 待赋值的变量。支持指定一个或多个变量，变量之间用逗号（`,`）隔开。|

### 语法示例

```sql
DELIMITER \\
CREATE PROCEDURE into_pre() 
 BEGIN
    DECLARE val int; 
    DECLARE cur1 cursor for select a from t1;
    OPEN cur1;
    FETCH cur1 INTO val;
    CLOSE cur1;
    SELECT val;
 END \\ 
```

## 关闭游标

`CLOSE` 语句用于关闭游标。关闭游标后，需要重新打开才能继续使用。

### 所需权限

无

### 语法格式

![](../../static/sql-reference/close_cursor.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `cursor_name` | 待关闭游标的名称。|

### 语法示例

```sql
DELIMITER \\
CREATE PROCEDURE into_pre1() 
 BEGIN
    DECLARE val int4; 
    DECLARE cur2 cursor for select a from t2;
    OPEN cur2;
    FETCH cur2 INTO val;
    CLOSE cur2;
 END \\ 
```
