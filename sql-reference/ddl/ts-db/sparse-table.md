---
title: 稀疏表
id: sparse-table
---

# 稀疏表管理

稀疏表（SPARSE TABLE）是在继承了时序表特性基础上，具有超宽、高稀疏、时序连续的特殊时序表。本文主要说明稀疏表与普通时序表相比，新增的语法及功能特性。

## 创建表

`CREATE SPARSE TABLE` 语句用于创建稀疏表。

### 语法格式

![](../../../static/sql-reference/createtable-sparse.png)

:::warning 说明

- 只有时序库支持创建稀疏表。
- 稀疏表最大数据列为20000列，普通时序表最大数据列为4096列。

:::

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name`| 待创建的稀疏表的名称，表名的最大长度为 128 字节。在指定数据库中，稀疏表名称必须唯一，并且遵循[数据库标识符规则](../../../sql-reference/sql-identifiers.md)。 |
| `column_list`| 待创建的数据列列表，支持添加两个以上的列定义，最多可指定 20000 列。|
| `tag_list`| 标签列表，支持添加一个或多个标签定义，最多可指定 `128` 个标签。标签定义包含标签名、数据类型和注释信息。<br>- 标签名的最大长度为 128 字节，支持指定 NOT NULL，默认为空值。不支持 TIMESTAMP、TIMESTAMPTZ、NVARCHAR 和 GEOMETRY 数据类型。<br>- 支持在 nullable 条件之后添加标签列的注释信息。 |
| `primary_tag_list`| 主标签列表，支持添加一个或多个主标签名称，最多可指定 `4` 个。主标签必须包含在标签列表内且指定为 NOT NULL，不支持浮点类型和除 VARCHAR 之外的变长数据类型。VARCHAR 类型长度默认 `64` 字节，最大长度为 `128` 字节。|

### 语法示例

- 创建稀疏表。

    以下示例创建一个名为 `device_ts` 的稀疏表。

    ```sql
    CREATE SPARSE TABLE device_ts (
      ts TIMESTAMP(3) NOT NULL,
      TEMP_DOUBLE DOUBLE,
      PRESS_INT INT4,
      ... (最多20000列)
    ) 
    tags (device_id varchar(10) not null) 
    PRIMARY tags (device_id);
    ```

## 查询表

`select <column_name> from <table_name> where`语句用于查询稀疏表中指定列<br>`select * from <table_name> where` 语句用于查询稀疏表中指定设备的有效列数据。

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `table_name` | 待创建的稀疏表的名称，表名的最大长度为 128 字节。在指定数据库中，稀疏表名称必须唯一，并且遵循[数据库标识符规则](../../../sql-reference/sql-identifiers.md)。 |
| `column_name` | 列名，新增列名不得与待修改表的当前列名和标签名重复。列名的最大长度为 128 字节。 |

### 语法格式

- 指定列查询

![](../../../static/sql-reference/select-sparse-table.png)

- 有效列查询

![](../../../static/sql-reference/select-sparse-table-01.png)

### 语法示例

- 创建稀疏表并写入数据

    ```sql
    CREATE SPARSE TABLE device_ts (
      ts TIMESTAMP(3) NOT NULL,
      p1 int4,
      p2 INT4,
      ...
      p9999 int4,
    )
    tags (device_id varchar(10) not null)
    PRIMARY tags (device_id);

    -- 推荐每个'insert'语句只包含单个设备，指定插入列，如下示例为2个设备分别使用'insert'语句：

    root@:26257/test> insert into device_ts(ts,p1,p2,p3,p4,device_id) value('2020-11-06 17:10:23',1,1,1,1,'dev1');
    INSERT 1

    TIME: 1.045654ms

    root@:26257/test> insert into device_ts(ts,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,device_id) value('2020-11-06 17:10:25',2,2,2,2,2,2,2,2,2,2,'dev2');
    INSERT 1

    TIME: 2.189641ms
    ```

- 有效列查询

    ```sql
    root@:26257/test> select * from device_ts where device_id in ('dev1','dev2');
    ```
    
    执行成功后，输出以下信息：
    ```sql
   ts|p1|p2|p3|p4|p5|p6|p7|p8|p9|p10|p11|p12|p13|p14|device_id
   ---+--+--+--+--+--+--+--+---+--+--+--+--+--+--+----------
   2020-11-06 17:10:25+00:00 |NULL |NULL |NULL|NULL| 2| 2| 2| 2| 2| 2| 2| 2| 2| 2| dev2
   2020-11-06 17:10:23+00:00 | 1| 1| 1| 1|NULL |NULL |NULL |NULL |NULL |NULL |NULL |NULL |NULL |NULL | dev1
  (2 rows)

  TIME: 5.565588ms
    ```
  当某个设备还未写入数据时，则查询时显示所有列：
    ```sql
    > select * from device_ts where device_id = 'dev10000';
    ```
    ```sql
    ts|p1|p2.....|p9999|p10000|device_id
    --+--+-+.....+-----+-----+----------
  (0 rows)
    ```
  
- 指定列查询

    ```sql
    root@:26257/test> select ts, p15 from device_ts where device_id = 'dev1';
    ```
    ```sql
    ts                        |p15
    --------------------------+-------
    2020-11-06 17:10:25+00:00 |NULL 
  (1 rows)
  TIME: 3.565588ms
    ```

## 查看表类型

`show tables` 语句用于查看当前数据库下的所有表的类型，稀疏表类型为`SPARSE TIME SERIES TABLE `。

### 语法格式

![](../../../static/sql-reference/show-tables-sparse.png)

### 语法示例

- 查看当前数据库中所有表的类型。

    以下示例查看当前数据库中稀疏表 `t1` 和普通时序表 `t2`。

    ```sql
    show tables;
    ```
    执行后输出信息：
    ```sql
    table_name|table_type
    ----------+------------------------
    t1        |SPARSE TIME SERIES TABLE
    t2        |TIME SERIES TABLE
    ```

## 功能限制说明

- 订阅发布、流计算、数据推送暂缓支持
- Insert...Select暂缓支持