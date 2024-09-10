---
title: Range 管理
id: range-mgmt-ts
---

# Range管理

## 查看分区

`SHOW RANGES` 语句用于显示数据库、表的分区信息，验证 SQL 数据如何映射到基础 Range 分区以及 Range 副本的位置。

### 前提条件

用户为 Admin 用户或者 Admin 角色成员。默认情况下，root 用户具有 Admin 角色。

### 语法格式

```sql
SHOW RANGES FROM [TABLE <table_name> | DATABASE <database_name>];
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 待查看的表名。 |
| `database_name` | 待查看的数据库名。 |

### 语法示例

- 查看表的分区。

    以下示例查看 `vehicles` 表的分区。

    ```sql
    SHOW RANGES FROM TABLE vehicles;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      start_key | end_key | range_id | range_size_mb | lease_holder | lease_holder_locality | replicas | replica_localities
    ------------+---------+----------+---------------+--------------+-----------------------+----------+---------------------
      NULL      | NULL    |      180 |      0.000077 |            1 |                       | {3}      | {""}
    (1 row)
    ```
- 查看数据库的分区。

    以下示例查看 `vtx` 数据库的分区。

    ```sql
    SHOW RANGES FROM DATABASE vtx;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      table_name | start_key | end_key | range_id | range_size_mb | lease_holder | lease_holder_locality | replicas | replica_localities
    -------------+-----------+---------+----------+---------------+--------------+-----------------------+----------+---------------------  
      vehicles   | NULL      | NULL    |      180 |      0.000077 |            1 |                       | {3}      | {""}
    (1 row)
    ```
