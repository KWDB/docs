---
title: 数据导出
id: export-data
---

# 数据导出

KWDB 支持以下数据导出功能：

- 表级别数据导出
- 库级别数据导出

## 表级别数据导出

KWDB 支持使用 SQL 语句导出以下信息：

- 时序表或关系表的元数据及用户数据。元数据保存为 `meta.sql` 文件。用户数据保存为 `.csv` 文件。
- 系统表数据：包括用户信息表、权限信息和集群配置表的数据。

导出数据的过程中，如果目标位置不可达，系统报错。如果由于其他原因导致数据导出中断，系统保留已成功导出的文件。

### 前提条件

- 用户拥有 Admin 权限。
- 导出数据到指定服务器时：
  - 目标服务器正常运行、并且开放 `PUT` 权限。
  - 用户拥有访问目标服务器的权限。
  - 如需创建文件夹存放导出的数据，用户需要拥有在服务器上创建文件夹的权限。

### 语法格式

时序表和关系表的导出语法略有不同。时序表支持设置包围符、转义符和空值的表示形式。时序表也支持先筛选数据范围再导出数据。

:::warning 说明

- 筛选范围导出数据时，系统不会导出元数据。
- 如果符合筛选范围的数据行不存在，系统不会导出任何数据，系统将返回 `succeed`。

:::

- 导出时序表

    ```sql
    EXPORT INTO CSV "<expt_path>" FROM TABLE <table_name> WITH [ column_name | meta_only | data_only | delimiter = '<char>' | chunk_rows = '<number>' | enclosed = '<char>' | escaped = '<char>' | nullas = '<char>' ];
    ```

- 筛选数据范围后，导出时序表数据

    ```sql
    EXPORT INTO CSV "<expt_path>" FROM SELECT [ * | <column_list> ] FROM <table_name> [<where_clause>];
    ```

- 导出关系表

    ```sql
    EXPORT INTO CSV "<expt_path>"
    FROM TABLE <table_name>
    WITH [ meta_only | data_only | delimiter = '<char>' | chunk_rows = '<number>' ];
    ```

- 导出用户信息表

    ```sql
    EXPORT INTO CSV "<expt_path>" FROM TABLE system.users;
    ```

- 导出用户权限信息

    ```sql
    EXPORT INTO CSV "<expt_path>" FROM SELELCT * FROM system.information_schema.table_privileges;
    ```

- 导出集群配置表

    ```sql
    EXPORT INTO CSV "<expt_path>" FROM TABLE system.settings;
    ```

### 参数说明

| 参数 | 说明 |
|---| --- |
| `expt_path` | 导出文件的存放路径，支持 `nodelocal://<node_id>/<dir>` 和 `<server_ip>/<dir>` 两种格式。<br > `nodelocal://<node_id>/<dir>`：将文件导出至本地节点。	<br > - `node_id`：节点 ID。当本地只有一个节点时，`node_id` 取值是 `1`。<br > - `dir`：存放导出数据的文件夹名称。如果目标文件夹不存在，系统会在安装 KWDB 时定义的 KWDB 数据存放路径下创建相应的文件夹。默认情况下，KWDB 数据存放路径是 `/var/lib/kwdb/extern/<folder_name>`。<br > `<server_ip>/<dir>`：将文件导出至指定服务器。	<br > - `server_ip`：服务器的 IP 地址和端口号，例如 `http://172.18.0.1:8090`。	<br > - `dir`：存放导出数据的文件夹名称。如果目标文件夹不存在，系统会创建相应的文件夹。|
| `column_list` | 用于指定待导出的数据列和标签列。各列之间使用逗号（`,`）隔开。|
| `table_name` | 待导出数据的表名。|
| `where_clause` | 可选参数，用于限制待导出表的数据范围。KWDB 支持在 `WHERE` 子句中使用以下运算符：<br > - 比较运算符：`>`、`>=`、`<`、`<=`、`=`、`!=` <br > - 逻辑运算符：AND、OR、NOT <br >- 模糊查询：`LIKE`，支持使用通配符（`%`）表示任意字符（包括空字符）出现任意次数，或者使用下划线（`_`）表示任意单个字符。时间戳、数值和布尔类型的数据不支持模糊查询。<br >- NULL 值判断：通过 `IS NULL` 或 `IS NOT NULL` 检查某列的值是否为空或不为空。<br >- IN 运算符：用于匹配一组值中的任意一个值。 <br >- BETWEEN 运算符：用于匹配某个范围内的值。|
| `column_name` | 可选参数，表示导出数据时添加列名。默认情况下，导出数据时，系统不导出列名。|
| `meta_only` | 可选参数，表示只导出元数据。该参数与 `data_only` 参数互斥。|
| `data_only` | 可选参数，表示只导出用户数据。该参数与 `meta_only` 参数互斥。|
| `delimiter` | 可选参数，导出数据时，用于指定分隔符。系统根据指定的分隔符读取表的用户数据或者将数据写入 `CSV` 文件。分隔符支持单个字符或空字符，不支持双引号（`"`）。<br > - 分隔符应尽量避免与现有数据中的字符相同。如果数据中包含指定的分隔符，系统默认添加包围符来避免导出错误。<br > - 如果导出数据时指定了分隔符，导入数据时需要使用相同的分隔符。如果导出、导入数据时指定的分隔符不一致，可能会导致数据导入失败。|
| `chunk_rows` | 可选参数，导出数据时，用于指定单个 `CSV` 文件的行数。如果待导出数据的行数大于设定值，系统根据设定的值将待导出的表拆分成多个 `CSV` 文件，生成的文件按照 `<node_id>.<file_id>.csv` 的形式进行命名。默认值和上限值均为 `100000`。当取值为 `0` 时，表示无行数限制。 |
| `enclosed` | 可选参数，导出时序数据时，用于指定包围符。默认为双引号（`"`），支持单引号（`'`）。使用单引号（`'`）作为包围符时，格式为 `"'"`。使用双引号（`"`）作为包围符时，格式为 `'"'`。包围符不能与分隔符相同。|
| `escaped` | 可选参数，导出时序数据时，用于指定转义符。默认为双引号（`"`），支持反斜杠（`\`）。转义符不能与分隔符相同。|
| `nullas` | 可选参数，导出时序数据时，用于指定空值的表示形式。默认不显示内容，支持指定为 `NULL`、`null`、`Null` 或 `\N`。|

### 语法示例

以下示例假设已经创建时序表 `ts_table` 并写入相关数据。

- 将时序表的用户数据和元数据导出到本地节点。

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序表的用户数据和元数据导出到指定服务器。

    ```sql
    EXPORT INTO CSV "http://172.18.10.1:8090/ts_table" FROM TABLE ts_table;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 根据时间戳、列名筛选时序表数据，并将筛选后的数据导出到本地节点。

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM SELECT ts, value, site_id FROM ts_table WHERE ts > '2024-02-01 09:00:00';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序表的非空值数据导出到本地节点。

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM SELECT * from ts_table WHERE value IS NOT NULL;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序表的用户数据导出到本地节点。

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH data_only;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序表的元数据导出到本地节点。

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH meta_only;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序表导出到本地节点时，指定分隔符。

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH DELIMITER = '/';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序表导出到本地节点时，限制单个文件的行数为 `1000`。

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH chunk_rows = '1000';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序表导出到本地节点时，指定包围符为单引号（`'`）。

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH enclosed = "'";
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序表导出到本地节点时，指定转义符为反斜杠（`\`）。

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH escaped = '\';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序表导出到本地节点时，指定空值表现形式为 `NULL`。

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH NULLAS = 'NULL';
    ```

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

## 库级别数据导出

KWDB 支持一次性导出数据库中所有表的元数据和用户数据。

- 时序数据库

    导出的时序表位于 `public` 模式下。每张表是一个单独的目录，用于存放该表的用户数据（`.csv` 文件）。导出的时序数据库数据组织形式如下所示：

    ```shell
    tsdb
    |-- meta.sql
    |-- public
      |-- t1
        |-- n1.0.csv
      |-- t2
        |-- n1.0.csv
    ```

- 关系数据库

    导出的关系表按其所在模式进行组织。每张表是一个单独的目录，用于存放该表的元数据信息（`meta.sql`）和用户数据（`.csv` 文件）。导出的关系库数据组织形式如下所示：

    ```shell
    rdb
    |-- meta.sql
    |-- public
      |-- table1
        |-- meta.sql
        |-- n1.0.csv
      |-- table2
        |-- meta.sql
        |-- n1.0.csv
    |-- schema1
      |-- meta.sql
      |-- table1
        |-- meta.sql
        |-- n1.0.csv
    ```

### 前提条件

用户拥有 Admin 权限。

### 语法格式

时序数据库和关系数据库的导出语法略有不同。时序数据库支持配置包围符、转义符和空值的表示形式。

- 导出时序数据库

    ```sql
    EXPORT INTO CSV "<expt_path>" FROM DATABASE <db_name> WITH [ column_name | meta_only | data_only | delimiter = '<char>' | chunk_rows = '<number>' | enclosed = '<char>' | escaped = '<char>' | nullas = '<char>'];
    ```

- 导出关系数据库

    ```sql
    EXPORT INTO CSV "<expt_path>" FROM DATABASE <db_name> WITH [ meta_only | data_only | delimiter = '<char>' | chunk_rows = '<number>'];
    ```

### 参数说明

| 参数          | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `expt_path`   | 导出文件的存放路径，支持 `nodelocal://<node_id>/<dir>` 和 `<server_ip>/<dir>` 两种格式。<br > `nodelocal://<node_id>/<dir>`：将文件导出至本地节点。	<br > - `node_id`：节点 ID。当本地只有一个节点时，`node_id` 取值是 `1`。<br > - `dir`：存放导出数据的文件夹名称。如果目标文件夹不存在，系统会在安装 KWDB 时定义的 KWDB 数据存放路径下创建相应的文件夹。默认情况下，KWDB 数据存放路径是 `/var/lib/kwdb/extern/<folder_name>`。<br > `<server_ip>/<dir>`：将文件导出至指定服务器。	<br > - `server_ip`：服务器的 IP 地址和端口号，例如 `http://172.18.0.1:8090`。	<br > - `dir`：存放导出数据的文件夹名称。如果目标文件夹不存在，系统会创建相应的文件夹。 |
| `db_name`     | 待导出数据的数据库名。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `column_name` | 可选参数，表示导出数据时添加列名。默认情况下，导出数据时，系统不导出列名。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `meta_only`   | 可选参数，表示只导出元数据。该参数与 `data_only` 参数互斥。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `data_only`   | 可选参数，表示只导出用户数据。该参数与 `meta_only` 参数互斥。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `delimiter`   | 可选参数，导出数据时，用于指定分隔符。系统根据指定的分隔符读取表的用户数据或者将数据写入 `CSV` 文件。分隔符支持单个字符或空字符，不支持双引号（`"`）。<br > - 分隔符应尽量避免与现有数据中的字符相同。如果数据中包含指定的分隔符，系统默认添加包围符来避免导出错误。<br > - 如果导出数据时指定了分隔符，导入数据时需要使用相同的分隔符。如果导出、导入数据时指定的分隔符不一致，可能会导致数据导入失败。                                                                                                                                                                                                                                                      |
| `chunk_rows`  | 可选参数，导出数据时，用于指定单个 `CSV` 文件的行数。如果待导出数据的行数大于设定值，系统根据设定的值将待导出的表拆分成多个 `CSV` 文件，生成的文件按照 `<node_id>.<file_id>.csv` 的形式进行命名。默认值和上限值均为 `100000`。当取值为 `0` 时，表示无行数限制。                                                                                                                                                                                                                                                                                                                                                                                          |
| `enclosed`    | 可选参数，导出时序数据时，用于指定包围符。默认为双引号（`"`），支持单引号（`'`）。使用单引号（`'`）作为包围符时，格式为 `"'"`。使用双引号（`"`）作为包围符时，格式为 `'"'`。包围符不能与分隔符相同。                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `escaped`     | 可选参数，导出时序数据时，用于指定转义符。默认为双引号（`"`），支持反斜杠（`\`）。转义符不能与分隔符相同。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `nullas`      | 可选参数，导出时序数据时，用于指定空值的表示形式。默认不显示内容，支持指定为 `NULL`、`null`、`Null` 或 `\N`。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

### 语法示例

以下示例假设已经创建时序数据库 `ts_db` 和关系数据库 `rdb`。

- 将时序数据库的用户数据和元数据导出到本地节点。

    ```sql
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将关系数据库的用户数据和元数据导出到本地节点。

    ```sql
    EXPORT INTO CSV "nodelocal://1/rdb" FROM DATABASE rdb;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
    filename           |rows|node_id|file_num
    -------------------+----+-------+--------
    TABLE rdb.public.t1|2   |1      |1
    meta.sql           |1   |1      |1
    TABLE rdb.public.t2|2   |1      |1
    meta.sql           |1   |1      |1
    (4 rows)
    ```

- 将时序数据库的用户数据和元数据导出到指定服务器。

    ```sql
    EXPORT INTO CSV "http://172.18.10.1:8090/ts_db" FROM DATABASE ts_db;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序数据库的用户数据导出到本地节点。

    ```sql
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH data_only;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序数据库的元数据导出到本地节点。

    ```sql
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH meta_only;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序数据库数据导出到本地节点时，指定分隔符。

    ```sql
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH DELIMITER = '/';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序数据库数据导出到本地节点时，限制单个文件的行数为 `1000`。

    ```sql
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH chunk_rows = '1000';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序数据库数据导出到本地节点时，指定包围符为单引号（`'`）。

    ```sql
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH enclosed = "'";
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序数据库数据导出到本地节点时，指定转义符为反斜杠（`\`）。

    ```sql
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH escaped = '\';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序数据库数据导出到本地节点时，指定空值表现形式为 `NULL`。

    ```sql
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH NULLAS = 'NULL';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```
