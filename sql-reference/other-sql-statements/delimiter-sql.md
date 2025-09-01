---
title: 分隔符
id: delimiter-sql
---

# 分隔符

`DELIMITER` 语句用于修改当前会话的语句终结符。默认情况下，KWDB 使用分号（`;`）作为 SQL 语句的分隔符。但是有时候 SQL 语句本身也会包含分号，此时需要修改 SQL 语句的分隔符，避免执行包含分号的复合语句时引发解析冲突。

## 所需权限

无

## 语法格式

![](../../static/sql-reference/delimiter.png)

## 参数说明

| 参数 | 说明 |
| --- | --- |
| `new_delimiter` | 新的分隔符。目前，只支持使用双反斜杠（`\\`）和 分号（`;`）作为 SQL 语句的分隔符。|

## 语法示例

```sql
-- 使用双反斜杠作为 SQL 语句的分隔符。
DELIMITER \\
CREATE TABLE t(a init)\\

-- 使用分号作为 SQL 语句的分隔符。
DELIMITER ;
CREATE TABLE t1(a init);
```
