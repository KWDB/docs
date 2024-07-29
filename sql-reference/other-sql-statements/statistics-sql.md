---
title: 统计信息
id: statistics-sql
---


# 统计信息

KWDB 支持用户手动创建统计信息和后台自动创建统计信息。

**手动创建统计信息**：用户可以执行 `CREATE STATISTICS` 命令，针对特定的表或列组合收集统计信息。

**自动创建统计信息**：数据库系统在指定端口启动服务器时，刷新统计信息的线程跟随系统的启动而启动。系统通过创建非阻塞的定时任务来实现针对时序表和关系表的自动刷新统计功能。

对于关系表以及时序表普通列和普通标签列，数据库能自主监控数据变化，并在满足特定条件时自主更新统计信息。触发规则包括：

- 无统计信息时，系统将自动为该表创建统计信息。
- 时间驱动：根据上次创建或更新统计信息的时间间隔，自动创建统计信息。初始刷新间隔为 `12` 小时。随后按 `2` 倍最近四次刷新间隔的平均时间加上 `1` 小时内的随机时间进行刷新。当用户创建一个时序表并插入部分数据，系统默认创建统计时间。`12` 小时后会触发第二次刷新。此后，系统会检查最近几次刷新之间的平均时间差，用来判断是否触发刷新，从而避免多节点同一时间进行刷新或频繁刷新。
- 行数变化驱动：基于对数据变化的监控，如表的行数变化达到一定的比例时，自动创建统计信息。关系表的行数更新达到 20% + 500 行时触发刷新，时序表的普通列和普通标签列行数更新达到 20% + 2000 行时触发更新，行数驱动的刷新仅支持通过 `INSERT` 操作触发统计信息的更新，执行定时器任务期间，用户 `INSERT` 操作预期插入的的行数和上一次刷新时记录的行数对比，关系表的行数更新达到 20% + 500 行阈值触发刷新，时序表的普通列和普通标签列行数更新达到 20% + 2000 行时触发更新。

对于时序表的主标签列，自主更新规则如下：

- 无统计信息时：系统将在大约 `1` 分钟内自动为该表创建统计信息。
- 时间驱动刷新：初始刷新间隔为 `6` 小时。随后按 4 倍最近四次刷新间隔的平均时间加上 `1` 小时内的随机时间进行刷新。
- 行数驱动刷新：当表的行数更新达到 10% + 100 行时触发刷新。

::: warning 注意

- 无统计信息时，每次定时任务触发器前允许并行采集统计信息最大表数量为 `256`（时序表和关系表之和），创建超过并行采集最大数量的表情况下，刷新时间会变长。
- 行数驱动刷新：行数驱动的刷新仅支持通过 `INSERT` 操作触发统计信息的更新。每次定时任务触发器前表的行数变更达到要求的数量触发刷新。例如，在未触发定时器事件之前，所有表的行数变化会通知到变更计数器。当触发了定时器事件，表行数的变更将不会通知到变更计数器。所以表变更消息存在一定的概率性。
- 时间驱动刷新：时间驱动的刷新在满足时间条件后，也需要通过 `INSERT` 操作触发刷新。
- 以上刷新策略根据系统运行情况适时调整。
- 当系统内存或者资源不足的情况下，不会收集统计信息。

:::

## 生成统计信息

`CREATE STATISTICS` 语句用于生成表统计信息，以供基于成本的优化器（Cost-Based Optimizer，CBO）基于最新的数据分布做出最优的查询计划。

一旦创建了表并使用 `INSERT`、`IMPORT` 等语句将数据写入表中，就可以生成表统计信息。下表列出 `CREATE STATISTICS` 语句主要收集的采集项。

| <div style="width:50px">表类型</div> |     <div style="width:50px">列类型</div>        | 采集项（未指定列名）                        | 采集项（指定列名）                          |
| ------ | ------------ | ------------------------------------------- | ------------------------------------------- |
| 关系表 | 普通列       | 总行数、不同值的数目、NULL 值的数目         | 总行数、不同值的数目、NULL 值的数目和直方图 |
|        | 索引列       | 总行数、不同值的数目、NULL 值的数目和直方图 | 总行数、不同值的数目、NULL 值的数目         |
| 时序表 | 普通和标签列 | 总行数、不同值的数目、NULL 值的数目         | 总行数、不同值的数目、NULL 值的数目和直方图 |
|        | 主标签列     | 总行数、不同值的数目、NULL 值的数目         | 总行数、不同值的数目、NULL 值的数目         |

### 所需权限

用户拥有数据库的 CREATE 权限。

### 语法格式

![](../../static/sql-reference/create-statistics.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `statistics_name` |正在创建的统计信息的名称。|
| `column_list` | 要为其收集统计信息的列名。支持指定一个或多个列名，用逗号隔开。如果省略，将为表中所有的列收集信息。<br >未指定列名收集统计信息时，默认情况下：<br >- 关系表收集所有索引列以及前 `100` 个非索引列的统计信息。<br >- 时序表收集主标签列的统计信息及前 `100` 个普通列和标签列的统计信息。<br >指定列名收集统计信息时，时序表只支持对单列或对所有主标签列收集统计信息。|
| `table_name` | 指定要为其创建统计信息的表的名称。|
| `as_of_clause` | 用于使用 `AS OF SYSTEM TIME` 子句创建历史统计信息。时序数据暂不支持该子句。|

### 语法示例

以下示例假设已经创建 `kv` 关系表和 `t3` 时序表。

- 创建 `kv` 关系表。
  
    ```sql
    CREATE TABLE kv (k INT PRIMARY KEY, v INT);
    ```

- 创建`t3` 时序表并写入数据。

    ```sql
    CREATE TABLE t3(k_timestamp timestamp not null,e1 int) tags (c1 smallint not null,c2 nchar(10) not null,c3 char not null,c4 varchar(10) not null,size int not null) primary tags (c1,c2,c3,c4) ;
    Insert into t3 values ('2024-1-1 1:00:00',1,1,'100','a','aa',2);
    Insert into t3 values ('2024-1-1 1:01:00',2,2,'200','a','aaa',2);
    Insert into t3 values ('2024-1-1 2:00:00',3,2,'200','a','aaa',6);
    Insert into t3 values ('2024-1-1 3:00:00',4,4,'500','b','bb',4);
    Insert into t3 values ('2024-1-1 4:00:00',5,5,'500','b','bb',5);
    Insert into t3 values ('2024-1-1 5:00:00',6,6,'6','b','bbb',6);
    Insert into t3 values ('2024-1-1 6:00:00',7,7,'8','c','cc',7);
    Insert into t3 values ('2024-1-1 7:00:00',8,8,'8','c','cc',8);
    Insert into t3 values ('2024-1-1 8:00:00',9,9,'9','c','cc',9);
    Insert into t3 values ('2024-1-1 9:00:00',10,10,'10','c','ccc',10);
    ```

- 在特定列上创建统计信息。

    - 关系表

        ```sql
        CREATE STATISTICS kvalues ON v FROM kv;
        ```

    - 时序表

        ```sql
        CREATE STATISTICS t3s1 ON e1 FROM t3;
        CREATE STATISTICS

        Time: 48.022209ms

        -- 查看表的统计信息
        show statistics for table t3;
          statistics_name | column_names |             created              | row_count | distinct_count | null_count |    histogram_id
        ------------------+--------------+----------------------------------+-----------+----------------+------------+---------------------
          t3s1            | {e1}         | 2024-03-20 11:06:49.235701+00:00 |        10 |             10 |          0 | 953097942596517889
        (1 row)

        Time: 4.205361ms
        ```

- 在一组默认列上创建统计信息。

    - 关系表

        ```sql
        CREATE STATISTICS kvalues FROM kv;
        ```

    - 时序表

        ```sql
        CREATE STATISTICS t3all FROM t3;
        CREATE STATISTICS

        Time: 54.317333ms

        -- 查看表的统计信息
        show statistics for table t3
          statistics_name | column_names  |             created              | row_count | distinct_count | null_count |    histogram_id
        ------------------+---------------+----------------------------------+-----------+----------------+------------+---------------------
          t3all           | {k_timestamp} | 2024-03-20 11:04:20.236362+00:00 |        10 |             10 |          0 | 953097454356234241
          t3all           | {e1}          | 2024-03-20 11:04:20.236362+00:00 |        10 |             10 |          0 |               NULL
          t3all           | {size}        | 2024-03-20 11:04:20.236362+00:00 |        10 |              8 |          0 |               NULL
          t3all           | {c1,c2,c3,c4} | 2024-03-20 11:04:20.236362+00:00 |         9 |              9 |          0 |               NULL
        (4 rows)

        Time: 3.96791ms
        ```

- 为关系表创建指定时间的统计信息。

    ::: warning 说明
    目前，时序数据不支持该语句。
    :::

    ```sql
    CREATE STATISTICS kvalues FROM kv AS OF SYSTEM TIME '-4m';
    CREATE STATISTICS
    ```

    其中，`'-4m'` 指 4 分钟以前。有关 `AS OF SYSTEM TIME` 语句的详细信息，参见[启动事务](./transactions-sql.md#启动事务)。

- 删除统计信息。

    ::: warning 说明
    删除统计信息后，需要重启节点，以清除统计信息缓存。
    :::

    - 删除所有数据库中表的统计信息。

        ```sql
        DELETE FROM system.table_statistics WHERE true;
        ```

    - 删除指定的统计信息。

        ```sql
        DELETE FROM system.table_statistics WHERE name = 'my_stats';
        ```

- 查看统计任务。

    `CREATE STATISTICS` 语句用于启动后台统计任务。应用程序或自动统计信息功能发出的查询也可以启动后台统计任务。支持使用 `SHOW JOBS` 或 `SHOW AUTOMATIC JOBS` 语句查看统计信息任务。
    `SHOW JOBS` 语句用于查看由用户或应用程序发出的查询而产生的统计任务。

    ```sql
    SELECT * FROM [SHOW JOBS] WHERE job_type LIKE '%CREATE STATS%';
    job_id            |job_type    |description                                                                             |statement|user_name|status   |running_status|created                   |started                   |finished                  |modified                  |fraction_completed|error                                                                         |coordinator_id
    ------------------+------------+----------------------------------------------------------------------------------------+---------+---------+---------+--------------+--------------------------+--------------------------+--------------------------+--------------------------+------------------+------------------------------------------------------------------------------+--------------
    858236607155634177|CREATE STATS|CREATE STATISTICS kvalues ON v FROM defaultdb.public.kv                                 |         |root     |succeeded|              |2023-04-20 09:37:07.086063|2023-04-20 09:37:07.095165|2023-04-20 09:37:07.109222|2023-04-20 09:37:07.108404|1                 |                                                                              |1             
    858236831262474241|CREATE STATS|CREATE STATISTICS kvalues FROM defaultdb.public.kv                                      |         |root     |succeeded|              |2023-04-20 09:38:15.478046|2023-04-20 09:38:15.481869|2023-04-20 09:38:15.499927|2023-04-20 09:38:15.493602|1                 |                                                                              |1             
    858236936373501953|CREATE STATS|CREATE STATISTICS kvalues FROM defaultdb.public.kv WITH OPTIONS AS OF SYSTEM TIME '-10m'|         |root     |failed   |              |2023-04-20 09:38:47.555391|2023-04-20 09:38:47.5584  |2023-04-20 09:38:47.567357|2023-04-20 09:38:47.561729|0                 |AS OF SYSTEM TIME: cannot specify timestamp older than 5m0s for this operation|1             
    858236958827315201|CREATE STATS|CREATE STATISTICS kvalues FROM defaultdb.public.kv WITH OPTIONS AS OF SYSTEM TIME '-5m' |         |root     |failed   |              |2023-04-20 09:38:54.407752|2023-04-20 09:38:54.411544|2023-04-20 09:38:54.423269|2023-04-20 09:38:54.415232|0                 |AS OF SYSTEM TIME: cannot specify timestamp older than 5m0s for this operation|1             
    858237045643739137|CREATE STATS|CREATE STATISTICS kvalues FROM defaultdb.public.kv WITH OPTIONS AS OF SYSTEM TIME '-4m' |         |root     |succeeded|              |2023-04-20 09:39:20.902014|2023-04-20 09:39:20.905123|2023-04-20 09:39:20.919033|2023-04-20 09:39:20.91831 |1                 |                                                                              |1             
    (5 rows)
    ```

    `SHOW AUTOMATIC JOBS` 语句查看由自动统计功能创建的统计任务。

    ```sql
    SELECT * FROM [SHOW AUTOMATIC JOBS] WHERE job_type LIKE '%CREATE STATS%';
    job_id|job_type|description|statement|user_name|status|running_status|created|started|finished|modified|fraction_completed|error|coordinator_id
    ------+--------+-----------+---------+---------+------+--------------+-------+-------+--------+--------+------------------+-----+--------------
    (0 rows)
    ```

## 查看统计信息

`SHOW STATISTICS` 语句用于查看基于成本的优化器使用的表统计信息。

### 所需权限

无

### 语法格式

![](../../static/sql-reference/P6JqbaefJombmHxF6ydcDVYVnLb.png)

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 查看其统计信息的表的名称。|

### 语法示例

以下示例查看 `kv` 表的统计信息。

```sql
-- 1. 生成 kv 表中 v 列的统计信息。

CREATE STATISTICS kvalues ON v FROM kv;
CREATE STATISTICS

-- 2. 查看 kv 表的统计信息。

SHOW STATISTICS FOR TABLE kv;
statistics_name|column_names|created                   |row_count|distinct_count|null_count|histogram_id      
---------------+------------+--------------------------+---------+--------------+----------+------------------
kvalues        |{v}         |2023-04-20 11:06:08.247022|6        |6             |0         |858254109079404545
(1 row)
```
