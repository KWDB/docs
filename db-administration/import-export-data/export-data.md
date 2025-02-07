---
title: 数据导出
id: export-data
---

# 数据导出

KWDB 支持导出以下数据：

- **表数据**：包括时序表和关系表的元数据、权限信息、用户数据、以及用户表、权限信息表和系统配置表的数据。
- **库数据**：导出指定时序库或关系库的元数据、权限信息和用户数据。
- **用户设置信息**：导出创建非系统用户的 SQL 语句。
- **集群参数信息**：导出集群参数配置的 SQL 语句。

## 表级别数据导出

KWDB 支持使用 SQL 语句导出以下信息：

- 时序表或关系表的元数据、权限信息和用户数据。元数据和权限信息保存为 `meta.sql` 文件。用户数据保存为 `.csv` 文件。
- 时序表或关系表指定范围的用户数据。
- 系统表数据：包括用户信息表、权限信息表和集群配置表的数据。

导出数据的过程中，如果目标位置不可达，系统报错。如果由于其他原因导致数据导出中断，系统保留已成功导出的文件。

### 前提条件

- 非三权分立模式下，用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。
- 三权分立模式下，用户是 `sysadmin` 角色的成员。默认情况下，`sysroot` 用户属于 `sysadmin` 角色。
- 导出数据到指定服务器时：
  - 目标服务器正常运行、并且开放 `PUT` 权限。
  - 用户拥有访问目标服务器的权限。
  - 如需创建文件夹存放导出的数据，用户需要拥有在服务器上创建文件夹的权限。

### 语法格式

:::warning 说明

- 筛选范围导出数据时，系统不会导出元数据。
- 如果符合筛选范围的数据行不存在，系统不会导出任何数据，系统将返回 `succeed`。

:::

- 导出时序表或关系表的元数据、用户数据和权限信息

    ```sql
    EXPORT INTO CSV "<expt_path>" FROM TABLE <table_name> WITH [ column_name | meta_only | data_only | delimiter = '<char>' | chunk_rows = '<number>' | enclosed = '<char>' | escaped = '<char>' | nullas = '<char>' | comment | charset = '<coding>' | privileges ];
    ```

- 导出指定范围的用户数据

    ```sql
    EXPORT INTO CSV "<expt_path>" FROM <select_clause>;
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
| `expt_path` | 导出文件的存放路径，支持 `nodelocal://<node_id>/<dir>` 和 `<server_ip>/<dir>` 两种格式。<br> `nodelocal://<node_id>/<dir>`：将文件导出至本地节点。	<br> - `node_id`：节点 ID。当本地只有一个节点时，`node_id` 取值是 `1`。<br> - `dir`：存放导出数据的文件夹名称。如果目标文件夹不存在，系统会在安装 KWDB 时定义的 KWDB 数据存放路径下创建相应的文件夹。默认情况下，KWDB 数据存放路径是 `/var/lib/kwdb/extern/<folder_name>`。<br> `<server_ip>/<dir>`：将文件导出至指定服务器。	<br> - `server_ip`：服务器的 IP 地址和端口号，例如 `http://172.18.0.1:8090`。	<br> - `dir`：存放导出数据的文件夹名称。如果目标文件夹不存在，系统会创建相应的文件夹。|
| `table_name` | 待导出数据的表名。|
| `column_name` | 可选参数，表示导出数据时添加列名。默认情况下，导出数据时，系统不导出列名。|
| `meta_only` | 可选参数，表示只导出元数据。该参数与 `data_only` 参数互斥。|
| `data_only` | 可选参数，表示只导出用户数据。该参数与 `meta_only` 参数互斥。|
| `delimiter` | 可选参数，用于指定分隔符。系统根据指定的分隔符读取表的用户数据或者将数据写入 `CSV` 文件。分隔符支持单个字符或空字符，不支持双引号（`"`）。<br> - 分隔符应尽量避免与现有数据中的字符相同。如果数据中包含指定的分隔符，系统默认添加包围符来避免导出错误。<br> - 如果导出数据时指定了分隔符，导入数据时需要使用相同的分隔符。如果导出、导入数据时指定的分隔符不一致，可能会导致数据导入失败。|
| `chunk_rows` | 可选参数，用于指定单个 `CSV` 文件的行数。如果待导出数据的行数大于设定值，系统根据设定的值将待导出的表拆分成多个 `CSV` 文件，生成的文件按照 `<node_id>.<file_id>.csv` 的形式进行命名。默认值和上限值均为 `100000`。当取值为 `0` 时，表示无行数限制。 |
| `enclosed` | 可选参数，用于指定包围符。默认为双引号（`"`），支持单引号（`'`）。使用单引号（`'`）作为包围符时，格式为 `"'"`。使用双引号（`"`）作为包围符时，格式为 `'"'`。包围符不能与分隔符相同。|
| `escaped` | 可选参数，用于指定转义符。默认为双引号（`"`），支持反斜杠（`\`）。转义符不能与分隔符相同。|
| `nullas` | 可选参数，用于指定空值的表示形式。默认不显示内容，支持指定为 `NULL`、`null`、`Null` 或 `\N`。|
| `comment` | 可选参数，用于指定是否导出注释信息。默认不导出注释信息。<br> - 如果要导出的表或表中的列带有注释信息，指定 `WITH comment` 参数后，系统导出带有注释信息的 SQL 文件。否则，系统导出的 SQL 文件不会带有注释信息。<br> - 如果要导出的表或表中的列没有注释信息，指定 `WITH comment` 参数后，系统报错，提示 `TABLE or COLUMN without COMMENTS cannot be used 'WITH COMMENT'`。|
| `charset` | 可选参数，用于指定待导出数据的字符集编码。默认值为 `utf8`，支持指定为 `gbk`、`gb18030` 或 `utf8`。|
| `privileges` | 可选参数，导出目标表的非系统用户权限信息。导出语句中指定该参数时，系统将读取系统表中的权限表，并将对应的权限 SQL 语句写入 `meta.sql` 文件中。|
| `select_clause` | 指定待导出的数据范围。时序表支持的 SELECT 语句见 [SELECT](../../sql-reference/dml/ts-db/ts-select.md)。关系表支持的 SELECT 语句见 [SELECT](../../sql-reference/dml/relational-db/relational-select.md)。 |

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

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序表导出到本地节点时，指定携带注释信息。

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH COMMENT;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

- 将时序表导出到本地节点时，指定字符集编码为 GBK。

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH charset = 'GBK';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

## 库级别数据导出

KWDB 支持一次性导出指定数据库中所有表的元数据、用户数据和权限信息。

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

- 非三权分立模式下，用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。
- 三权分立模式下，用户是 `sysadmin` 角色的成员。默认情况下，`sysroot` 用户属于 `sysadmin` 角色。

### 语法格式

时序数据库和关系数据库的导出语法相同：

  ```sql
  EXPORT INTO CSV "<expt_path>" FROM DATABASE <db_name> WITH [ column_name | meta_only | data_only | delimiter = '<char>' | chunk_rows = '<number>' | enclosed = '<char>' | escaped = '<char>' | nullas = '<char>' | comment | charset = '<coding>' | privileges ];
  ```

### 参数说明

| 参数          | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `expt_path`   | 导出文件的存放路径，支持 `nodelocal://<node_id>/<dir>` 和 `<server_ip>/<dir>` 两种格式。<br> `nodelocal://<node_id>/<dir>`：将文件导出至本地节点。	<br> - `node_id`：节点 ID。当本地只有一个节点时，`node_id` 取值是 `1`。<br> - `dir`：存放导出数据的文件夹名称。如果目标文件夹不存在，系统会在安装 KWDB 时定义的 KWDB 数据存放路径下创建相应的文件夹。默认情况下，KWDB 数据存放路径是 `/var/lib/kwdb/extern/<folder_name>`。<br> `<server_ip>/<dir>`：将文件导出至指定服务器。	<br> - `server_ip`：服务器的 IP 地址和端口号，例如 `http://172.18.0.1:8090`。	<br> - `dir`：存放导出数据的文件夹名称。如果目标文件夹不存在，系统会创建相应的文件夹。 |
| `db_name`     | 待导出数据的数据库名。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `column_name` | 可选参数，表示导出数据时添加列名。默认情况下，导出数据时，系统不导出列名。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `meta_only`   | 可选参数，表示只导出元数据。该参数与 `data_only` 参数互斥。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `data_only`   | 可选参数，表示只导出用户数据。该参数与 `meta_only` 参数互斥。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `delimiter`   | 可选参数，用于指定分隔符。系统根据指定的分隔符读取表的用户数据或者将数据写入 `CSV` 文件。分隔符支持单个字符或空字符，不支持双引号（`"`）。<br> - 分隔符应尽量避免与现有数据中的字符相同。如果数据中包含指定的分隔符，系统默认添加包围符来避免导出错误。<br> - 如果导出数据时指定了分隔符，导入数据时需要使用相同的分隔符。如果导出、导入数据时指定的分隔符不一致，可能会导致数据导入失败。                                                                                                                                                                                                                                                      |
| `chunk_rows`  | 可选参数，用于指定单个 `CSV` 文件的行数。如果待导出数据的行数大于设定值，系统根据设定的值将待导出的表拆分成多个 `CSV` 文件，生成的文件按照 `<node_id>.<file_id>.csv` 的形式进行命名。默认值和上限值均为 `100000`。当取值为 `0` 时，表示无行数限制。                                                                                                                                                                                                                                                                                                                                                                                          |
| `enclosed`    | 可选参数，用于指定包围符。默认为双引号（`"`），支持单引号（`'`）。使用单引号（`'`）作为包围符时，格式为 `"'"`。使用双引号（`"`）作为包围符时，格式为 `'"'`。包围符不能与分隔符相同。                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `escaped`     | 可选参数，用于指定转义符。默认为双引号（`"`），支持反斜杠（`\`）。转义符不能与分隔符相同。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `nullas`      | 可选参数，用于指定空值的表示形式。默认不显示内容，支持指定为 `NULL`、`null`、`Null` 或 `\N`。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `comment` | 可选参数，指定是否导出数据库的注释信息。默认不导出注释信息。<br> - 如果要导出的数据库带有注释信息，指定 `WITH comment` 参数后，系统导出带有注释信息的 SQL 文件。否则，系统导出的 SQL 文件不会带有注释信息。<br> - 如果要导出的数据库没有注释信息，指定 `WITH comment` 参数后，系统报错，提示 `DATABASE or TABLE or COLUMN without COMMENTS cannot be used 'WITH COMMENT'`。|
| `charset` | 可选参数，指定待导出数据库的字符集编码。默认值为 `utf8`，支持指定为 `gbk`、`gb18030` 或 `utf8`。|
| `privileges` | 可选参数，导出目标数据库的非系统用户权限信息。导出语句中指定该参数时，系统将读取系统表中的权限表，并将对应的权限 SQL 语句写入 `meta.sql` 文件中。|

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

- 将时序数据库数据导出到本地节点时，指定携带注释信息。

    ```sql
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH COMMENT;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```
  
- 将时序数据库数据导出到本地节点时，指定字符集编码为 GBK。

    ```sql
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH charset = 'GBK';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      result
    -----------
      succeed
    (1 row)
    ```

## 用户信息导出

KWDB 支持使用 SQL 语句导出当前 KWDB 集群的所有非系统用户信息，并将其存储为 `users.sql` 文件。

::: warning 说明

导出的用户信息不包含密码信息，后续导入时需要根据需要重新设置密码。

:::

### 前提条件

- 非三权分立模式下，用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。
- 三权分立模式下，用户是 `sysadmin` 角色的成员。默认情况下，`sysroot` 用户属于 `sysadmin` 角色。

### 语法格式

```sql
EXPORT USERS TO SQL "<file_path>";
```

### 参数说明

| 参数                 | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `file_path`          | 导出文件的存放路径，支持以下两种格式：<br> - `nodelocal://<node_id>/<dir>`：将文件导出至本地节点。`node_id` 为节点 ID。如果本地只有一个节点，`node_id` 为 `1`。`dir` 为文件所在的文件夹。如果目标文件夹不存在，系统会在 KWDB 安装时定义的数据存放路径下创建该文件夹。默认路径为 `/var/lib/kwdb/extern/<dir>`。<br> - `<server_ip>/<dir>`：将文件导出至指定服务器。 `server_ip`为服务器的 IP 地址和端口，例如 `http://172.18.0.1:8090`。`dir` 为存放文件的文件夹路径，如果目标文件夹不存在，系统会创建该文件夹。                       |

### 返回参数

| 参数                 | 说明                                                                  |
|----------------------|---------------------------------------------------------------------|
| `queryname`          | 查询名称。                                                        |
| `rows`               | 导出的行数。                                                          |
| `node_id`            | 节点 ID。                                                       |
| `file_num`           | 导出的文件数量。                                                       |

### 语法示例

```sql
EXPORT USERS TO SQL "nodelocal://1/users";
```

执行成功后，控制台输出以下信息：

```sql
     queryname       | rows | node_id | file_num
---------------------+------+---------+-----------
       USERS         |    1 |     1   |        1
(1 row)
```

## 集群参数信息导出

KWDB 支持使用 SQL 语句导出当前 KWDB 集群的参数设置信息，并将其存储为 `clustersetting.sql` 文件。

### 前提条件

- 非三权分立模式下，用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。
- 三权分立模式下，用户是 `sysadmin` 角色的成员。默认情况下，`sysroot` 用户属于 `sysadmin` 角色。

### 语法格式

```sql
EXPORT CLUSTER SETTING TO SQL "<file_path>";
```

### 参数说明

| 参数                 | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `file_path`          | 导出文件的存放路径，支持以下两种格式：<br> - `nodelocal://<node_id>/<dir>`：将文件导出至本地节点。`node_id` 为节点 ID。如果本地只有一个节点，`node_id` 为 `1`。`dir` 为文件所在的文件夹。如果目标文件夹不存在，系统会在 KaiwuDB 安装时定义的数据存放路径下创建该文件夹。默认路径为 `/var/lib/kwdb/extern/<dir>`。<br> - `<server_ip>/<dir>`：将文件导出至指定服务器。`server_ip`为服务器的 IP 地址和端口，例如 `http://172.18.0.1:8090`。`dir` 为文件的文件夹路径，如果目标文件夹不存在，系统会创建该文件夹。                         |

### 返回参数

| 参数                 | 说明                                                                  |
|----------------------|---------------------------------------------------------------------|
| `queryname`          | 查询名称。                                                        |
| `rows`               | 导出的行数。                                                          |
| `node_id`            | 节点 ID。                                                       |
| `file_num`           | 导出的文件数量。                                                       |

### 语法示例

```sql
IMPORT CLUSTER SETTING TO SQL "nodelocal://1/settings";
```

执行成功后，控制台输出以下信息：

```sql
     queryname       | rows | node_id | file_num
---------------------+------+---------+-----------
  CLUSTER SETTING    |  215 |     1   |        1
(1 row)
```