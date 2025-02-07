---
title: 数据导入
id: import-data
---

# 数据导入

KWDB 支持导入以下数据：

- **表数据**：导入指定时序表或关系表的元数据、权限信息和用户数据。
- **库数据**：导入指定时序库或关系库的元数据、权限信息和用户数据。
- **用户信息**：导入和执行非系统用户的创建语句。
- **集群参数信息**：导入和执行集群参数的配置语句。

::: warning 说明

- 目前，KWDB 不支持导入数据库的系统表数据。
- 在导入表级别数据时，使用 `sort -t <separator> -k <primary_key_column> <file_name>` 命令提前对数据文件进行排序，有助于提升数据导入效率。

:::

## 表级别数据导入

KWDB 支持使用 SQL 语句将其他 KWDB 数据库导出的时序表或关系表的元数据、权限信息和用户数据导入到另一个 KWDB 数据库。其中元数据和权限信息存储在 `meta.sql` 文件。用户数据存储在 `.csv` 文件。

KWDB 支持同时导入表的用户数据和元数据，或者只导入表的用户数据或元数据。当目标表中已经存在用户数据，KWDB 支持增量导入用户数据。

如果关系数据导入失败，系统将回滚本次导入操作。如果时序数据导入失败，系统不会回滚操作，而会保留已成功导入的数据。控制台会输出写入失败的数据行数，同时将写入失败的数据和错误信息保存到 `reject.txt` 文件。`reject.txt` 文件与待导入的数据文件位于同一路径下。

### 前提条件

- 非三权分立模式下，用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。
- 三权分立模式下，用户是 `sysadmin` 角色的成员。默认情况下，`sysroot` 用户属于 `sysadmin` 角色。
- 只导入用户数据时，待导入表的列数和数据类型与数据库现有表的列数和数据类型保持一致。

### 语法格式

时序表和关系表的导入语法相同。

- 全量导入用户数据、元数据和权限信息，并根据指定的文件目录和表结构创建表

    ```sql
    IMPORT TABLE CREATE USING "<meta.sql_path>" CSV DATA ("<file_path>") WITH [delimiter = '<char>' | enclosed = '<char>' | escaped = '<char>' | nullif = '<char>' | thread_concurrency = '<int>'| batch_rows = '<int>'| auto_shrink | comment | charset = '<coding>' | privileges];
    ```

- 只导入用户数据或者增量导入用户数据

    ```sql
    IMPORT INTO <table_name> [<column_list>] CSV DATA ("<file_path>") WITH [delimiter = '<char>' | enclosed = '<char>' | escaped = '<char>' | nullif = '<char>' | thread_concurrency = '<int>'| batch_rows = '<int>'| auto_shrink | charset = '<coding>'];
    ```

- 只导入元数据和权限信息

    ```sql
    IMPORT TABLE CREATE USING "<sql_path>" [WITH privileges];
    ```

### 参数说明

| 参数                 | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `sql_path`           | 待导入元数据文件的存放路径，支持 `nodelocal://node_id/folder_name/meta.sql` 和 `server_ip/folder_name/meta.sql` 两种格式。<br > `nodelocal://node_id/folder_name/meta.sql`：导入本地节点的元数据文件。<br > - `node_id`：节点 ID。当本地只有一个节点时，`node_id` 取值是 `1`。<br > - `folder_name`：存放导入元数据文件的文件夹名称，默认是 `/var/lib/kwdb/extern/<folder_name>`。<br > `server_ip/folder_name/meta.sql`：导入指定服务器的元数据文件。<br > - `server_ip`：指定服务器的 IP 地址和端口号，例如 `http://172.18.0.1:8090`。<br >- `folder_name`：存放导入元数据文件的文件夹名称。|
| `file_path`          | 待导入用户数据文件的存放路径，支持 `nodelocal://<node_id>/<folder_name>/<file_name>` 和 `<server_ip>/<dir>` 两种格式。<br > `nodelocal://<node_id>/<folder_name>/<file_name>`：导入本地节点的用户数据文件。<br > - `node_id`：节点 ID。当本地只有一个节点时，`node_id` 取值是 `1`。<br > - `folder_name`：存放导入用户数据文件的文件夹名称，默认是 `/var/lib/kwdb/extern/<folder_name>`。<br > - `file_name`：待导入用户数据文件的名称。只有导入关系表时，才需要指定用户数据文件的名称。<br > `<server_ip>/<dir>`：导入指定服务器的用户数据文件。<br >- `server_ip`：指定服务器的 IP 地址和端口，例如 `http://172.18.0.1:8090`。<br >- `dir`：存放导入用户数据文件的文件夹名称。<br> **说明**：如果该路径下包含 `reject.txt` 文件，请根据文件中的提示检查相关数据，避免后续导入时继续出错。                         |
| `delimiter`          | 可选参数，用于指定分隔符。系统根据指定的分隔符解析 `CSV` 文件并将解析的内容导入到 KWDB 系统。导入数据时，指定的分隔符需要与 `CSV` 文件中使用的分隔符保持一致，否则可能会出现解析后列数不匹配的情况，从而导致数据导入失败。 |
| `enclosed`           | 可选参数，用于指定包围符。默认为双引号（`"`），支持单引号（`'`）。使用单引号（`'`）作为包围符时，格式为 `"'"`。使用双引号（`"`）作为包围符时，格式为 `'"'`。包围符不能与分隔符相同。<br>**注意**：导入带有包围符的换行符时，应避免开启多线程导入操作。|
| `escaped`            | 可选参数，用于指定转义符。默认为双引号（`"`），支持反斜杠（`\`）。转义符不能与分隔符相同。|
| `nullif`             | 可选参数，用于指定空值的表示形式。默认不显示内容，支持指定为 `NULL`、`null`、`Null` 或 `\N`。|
| `thread_concurrency` | 可选参数，用于指定并发写入数据的数量。系统按照配置平均分割、并发读取和写入导入的文件。默认情况下，`thread_concurrency` 的取值是 `1`。`thread_concurrency` 的取值应该大于 `0`，小于等于系统核数的 2 倍。如果取值大于核数的 2 倍，系统按照核数的 2 倍并发读取、写入数据。`thread_concurrency` 参数支持与 `batch_rows`、`auto_shrink` 参数共同使用，中间使用逗号（`,`）隔开。<br> **注意**：开启多线程导入操作后，如果导入的 `.csv` 文件中带有换行符，会导致导入失败。此时，用户应删除导入的数据库或者表，将 `thread_concurrency` 参数取值设置为 1， 然后再重新导入文件。|
| `batch_rows`         | 并发导入数据时，每次读取的行数。默认情况下，`batch_rows` 的取值是 `500`。`batch_rows` 的取值应该大于 `0`，并且 batch_rows x 单行数据的大小 ≤ 4 GB。如果 batch_rows x 单行数据的大小 > 4 GB, 系统按照 4 GB 支持的最大行数读取数据。`batch_rows` 参数支持与 `thread_concurrency`、`auto_shrink` 共同使用，中间使用逗号（`,`）隔开。|
| `auto_shrink`        | 可选参数，用于指定是否进行集群自适应衰减。默认情况下，系统不进行自适应衰减。设置了 `auto_shrink` 参数后，集群将自动每 10 秒进行一次衰减。`auto_shrink` 参数支持与 `batch_rows`、`thread_concurrency` 参数共同使用，中间使用逗号（`,`）隔开。|
| `comment` | 可选参数，用于指定是否导入表的注释信息。默认不导入注释信息。<br > - 如果要导入的 SQL 文件带有注释信息，指定 `WITH comment` 参数后，系统导入注释信息。否则，系统不导入注释信息。<br > - 如果要导入的 SQL 文件没有注释信息，指定 `WITH comment` 参数后，系统报错，提示 `NO COMMENT statement in the SQL file`。|
| `charset` | 可选参数，用于指定待导入数据的字符集编码。默认值为 `utf8`，支持指定为 `gbk`、`gb18030`或 `utf8`。<br>**注意**：指定的字符集编码必须与实际字符集编码一致，否则可能会导致数据导入失败或数据乱码问题。|
| `privileges` | 可选参数，指定导入目标表的非系统用户权限信息。指定该参数时，系统将读取并执行元数据文件中与权限相关的 SQL 语句。**注意**：如果文件中没有权限相关的语句，系统将返回 `NO PRIVILEGES statement in the SQL file`, 此时需要用户删除该参数后重新执行导入语句。未指定该参数时，系统不会自动读取元数据文件中权限相关的 SQL 语句。|
| `table_name`         | 目标表名，数据导入的目标表。待导入文件的数据列数和数据类型与数据库中目标表的列数及数据类型保持一致。|
| `column_list`        | 可选参数，用于指定待导入的列。<br > - 指定列名时，KWDB 既可以按照源文件中列的顺序导入指定列的数据也可以与源文件中的列顺序不一致。时序表指定列必须包括第一列时间戳列和主标签列。<br > - 未指定列名时，KWDB 按照源文件中列的顺序导入所有数据。对于未指定列，如果该列支持空值，系统将自动写入默认值 `NULL`。如果该列不支持空值，系统提示 `Null value in column %s violates not-null constraints.`。 |

### 返回参数

| 参数                 | 说明                                                                  |
|----------------------|---------------------------------------------------------------------|
| `job_id`             | 导入任务的 ID。                                                        |
| `status`             | 导入任务的状态。                                                       |
| `fraction_completed` | 导入任务的完成情况，取值范围为 `[0,1]`。取值为 `1` 时，表示完成导入任务。 |
| `rows`               | 导入的行数。                                                          |
| `abandon_rows`        | 因数据去重未写入的行数。                                               |
| `reject_rows`        | 导入数据时，写入出错的行数。系统将写入出错的数据保存到 `reject.txt` 文件。   |
| `note`               | 写入出错时的系统提示。写入成功时显示 `None`。   |

### 语法示例

- 导入本地节点的用户数据和元数据。

    ```sql
    IMPORT TABLE CREATE USING "nodelocal://1/a/meta.sql" CSV DATA ("nodelocal://1/a");
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- 导入本地节点的用户数据和元数据时，指定携带注释信息。

    ```sql
    IMPORT TABLE CREATE USING "nodelocal://1/tb/meta.sql" CSV DATA ("nodelocal://1/tb") WITH COMMENT;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------------------+-----------+--------------------+------+--------------+-------------+------
                /        | succeeded |                  1 |    1 | 0            | 0           | None
    (1 row)
    ```

- 导入指定服务器的用户数据和元数据。

    ```sql
    IMPORT TABLE CREATE USING "http://172.18.0.1:8090/newdb/meta.sql" CSV DATA ("http://172.18.0.1:8090/newdb");
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------------------+-----------+--------------------+------+--------------+-------------+------
                /        | succeeded |                  1 |    1 | 0            | 0           | None
    (1 row)
    ```

- 导入本地节点的用户数据。

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a");
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------------------+-----------+--------------------+------+--------------+-------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- 导入本地节点的元数据。

    ```sql
    IMPORT TABLE CREATE USING "nodelocal://1/a/meta.sql";
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      job_id |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------+-----------+--------------------+------+--------------+-------------+------
      /      | succeeded |                  1 |    0 | 0            | 0           | None
    (1 row)
    ```

- 导入本地节点的用户数据时，指定分隔符。

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a") WITH DELIMITER = '/';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------------------+-----------+--------------------+------+--------------+-------------+------
                /        | succeeded |                  1 |    1 | 0            | 0           | None
    (1 row)
    ```

- 导入本地节点的用户数据时，指定包围符为单引号（`'`）。

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a") WITH enclosed = "'";
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------------------+-----------+--------------------+------+--------------+-------------+------
                /        | succeeded |                  1 |    1 | 0            | 0           | None
    (1 row)
    ```

- 导入本地节点的用户数据时，指定转义符为反斜杠（`\`）。

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a") WITH escaped = '\';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------------------+-----------+--------------------+------+--------------+-------------+------
                /        | succeeded |                  1 |    1 | 0            | 0           | None
    (1 row)
    ```

- 导入本地节点的用户数据时，指定空值表现形式为 `NULL`。

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a") WITH NULLIF = 'NULL';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------------------+-----------+--------------------+------+--------------+-------------+------
                /        | succeeded |                  1 |    1 | 0            | 0           | None
    (1 row)
    ```

- 导入本地节点的用户数据时，设置写入速率。

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a") WITH thred_concurrency = '20', batch_rows = '200';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------------------+-----------+--------------------+------+--------------+-------------+------
                /        | succeeded |                  1 |    1 | 0            | 0           | None
    (1 row)
    ```

## 库级别数据导入

KWDB 支持使用 SQL 语句将从其他 KWDB 时序库或关系库导出的所有表的元数据、权限信息和用户数据导入到另一个 KWDB 数据库。

KWDB 支持同时导入数据库的表数据、元数据和权限信息，或者只导入数据库的元数据和权限信息，不支持只导入所有表的用户数据。

如果关系数据导入失败，系统将回滚本次导入操作。如果时序数据导入失败，系统不会回滚操作，而会保留已成功导入的数据。控制台会输出写入失败的数据行数，同时将写入失败的数据和错误信息保存到 `reject.txt` 文件。`reject.txt` 文件与待导入的数据文件位于同一路径下。

### 前提条件

- 非三权分立模式下，用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。
- 三权分立模式下，用户是 `sysadmin` 角色的成员。默认情况下，`sysroot` 用户属于 `sysadmin` 角色。
- 待导入数据的文件夹包含 `.csv` 文件 和 `.sql` 文件。

### 语法格式

时序数据库和关系数据库的导入语法相同。

```sql
IMPORT DATABASE CSV DATA ("<db_path>") WITH [ delimiter = '<char>' | enclosed = '<char>' | escaped = '<char>' | nullif = '<char>' | thread_concurrency = '<int>'| batch_rows = '<int>'| auto_shrink  | comment | charset = '<coding>' | privileges ];
```

### 参数说明

| 参数                 | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `db_path`            | 待导入数据库的存放路径。支持 `nodelocal://<node_id>/<dir>` 和 `<server_ip>/<dir>` 两种格式。<br > `nodelocal://node_id/<folder_name>`：导入本地节点的数据库数据。 <br >- `node_id`：节点 ID。当本地只有一个节点时，`node_id` 取值是 `1`。<br > - `dir`：存放导入数据的文件夹名称。默认情况下，KWDB 导入数据的存放路径是 `/var/lib/kwdb/extern/<folder_name>`。<br > `<server_ip>/<dir>`：导入指定服务器的数据库数据。	<br > - `server_ip`：指定服务器的 IP 地址和端口，例如 `http://172.18.0.1:8090`。<br > - `dir`：存放导入数据的文件夹名称。 <br> **说明**：如果该路径下包含 `reject.txt` 文件，请根据文件中的提示检查相关数据，避免后续导入时继续出错。|
| `delimiter`          | 可选参数，用于指定分隔符。系统根据指定的分隔符解析 `CSV` 文件并将解析的内容导入到 KWDB 系统。导入数据时，指定的分隔符需要与 `CSV` 文件中使用的分隔符保持一致，否则可能会出现解析后列数不匹配的情况，从而导致数据导入失败。                                                                                                                                                                                                                                                                                   |
| `enclosed`           | 可选参数，用于指定包围符。默认为双引号（`"`），支持单引号（`'`）。使用单引号（`'`）作为包围符时，格式为 `"'"`。使用双引号（`"`）作为包围符时，格式为 `'"'`。包围符不能与分隔符相同。<br> **注意**：导入带有包围符的换行符时，应避免开启多线程导入操作。                                                                                                                                                                                                                                                                                                                                  |
| `escaped`            | 可选参数，用于指定转义符。默认为双引号（`"`），支持反斜杠（`\`）。转义符不能与分隔符相同。                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `nullif`             | 可选参数，用于指定空值的表示形式。默认不显示内容，支持指定为 `NULL`、`null`、`Null` 或 `\N`。                                                                                                                                                                                                                                                                                                                                                                                                              |
| `thread_concurrency` | 可选参数，用于指定并发写入数据的数量。系统按照配置平均分割、并发读取和写入导入的文件。默认情况下，`thread_concurrency` 的取值是 `1`。`thread_concurrency` 的取值应该大于 `0`，小于等于系统核数的 2 倍。如果取值大于核数的 2 倍，系统按照核数的 2 倍并发读取、写入数据。`thread_concurrency` 参数支持与 `batch_rows`、`auto_shrink` 参数共同使用，中间使用逗号（`,`）隔开。<br> **注意**：开启多线程导入操作后，如果导入的 `.csv` 文件中带有换行符，会导致导入失败。此时，用户应删除导入的数据库或者表，将 `thread_concurrency` 参数取值设置为 1， 然后再重新导入文件。    |
| `batch_rows`         | 并发导入数据时，每次读取的行数。默认情况下，`batch_rows` 的取值是 `500`。`batch_rows` 的取值应该大于 `0`，并且 batch_rows x 单行数据的大小 ≤ 4 GB。如果 batch_rows x 单行数据的大小 > 4 GB, 系统按照 4 GB 支持的最大行数读取数据。`batch_rows` 参数支持与 `thread_concurrency`、`auto_shrink` 共同使用，中间使用逗号（`,`）隔开。                                                                                                                                                                           |
| `auto_shrink`        | 可选参数，用于指定是否进行集群自适应衰减。默认情况下，系统不进行自适应衰减。设置了 `auto_shrink` 参数后，集群将自动每 10 秒进行一次衰减。`auto_shrink` 参数支持与 `batch_rows`、`thread_concurrency` 参数共同使用，中间使用逗号（`,`）隔开。                                                                                                                                                                                                                                                                                     |
| `comment` | 可选参数，用于指定是否导入数据库的注释信息。默认不导入注释信息。<br > - 如果要导入的 SQL 文件带有注释信息，指定 `WITH comment` 参数后，系统导入注释信息。否则，系统不导入注释信息。<br > - 如果要导入的 SQL 文件没有注释信息，指定 `WITH comment` 参数后，系统报错，提示 `NO COMMENT statement in the SQL file`。|
| `charset` | 可选参数，用于指定待导入数据的字符集编码。默认值为 `utf8`，支持指定为 `gbk`、`gb18030` 或 `utf8`。<br>**注意**：指定的字符集编码必须与实际字符集编码一致，否则可能会导致数据导入失败或数据乱码问题。|
| `privileges` | 可选参数，指定导入目标数据库的非系统用户权限信息。导入语句中指定该参数时，系统将读取并执行元数据文件中权限相关的 SQL 语句。**注意**：如果文件中没有权限相关的语句，系统将返回 `NO PRIVILEGES statement in the SQL file`, 此时需要用户删除该参数后重新执行导入语句。未指定该参数时，系统不会自动读取元数据文件中权限相关的 SQL 语句。|

### 返回参数

| 参数                 | 说明                                                                  |
|----------------------|---------------------------------------------------------------------|
| `job_id`             | 导入任务的 ID。                                                        |
| `status`             | 导入任务的状态。                                                       |
| `fraction_completed` | 导入任务的完成情况，取值范围为 `[0,1]`。取值为 `1` 时，表示完成导入任务。 |
| `rows`               | 导入的行数。                                                          |
| `abandon_rows`        | 因数据去重未写入的行数。                                               |
| `reject_rows`        | 导入数据时，写入出错的行数。系统将写入出错的数据保存到 `reject.txt` 文件。   |
| `note`               | 写入出错时的系统提示。写入成功时显示 `None`。   |

### 语法示例

- 导入本地节点的数据库数据。

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db");
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- 导入本地节点的数据库数据，指定携带注释信息。

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db") WITH COMMENT;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- 导入指定服务器的数据库数据。

    ```shell
    IMPORT DATABASE CSV DATA ("http://172.18.0.1:8090/newdb");
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
              /          | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- 导入本地节点的数据库数据时，指定分隔符。

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db") WITH DELIMITER = '/';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- 导入本地节点的数据库数据时，指定包围符为单引号（`'`）。

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db") WITH enclosed = "'";
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- 导入本地节点的数据库数据时，指定转义符为反斜杠（`\`）。

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db") WITH escaped ='\';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- 导入本地节点的数据库数据时，指定空值表现形式为 `NULL`。

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db") WITH NULLIF = 'NULL';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- 导入本地节点的数据库数据时，设置导入注释信息。

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db") WITH COMMENT;
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- 导入本地节点的数据库数据时，指定导入数据库的字符集编码为 GBK。

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db") WITH charset = 'GBK';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

## 用户信息导入

KWDB 支持使用 SQL 语句将从其他 KWDB 集群导出的用户信息， 以 `users.sql` 文件的形式导入到当前数据库。

如果待导入文件不存在或导入过程中发生错误，系统将提示错误原因，并回滚本次操作。

::: warning 说明

导入的用户信息不包含密码信息，导入完成后请根据需要设置密码。

:::

### 前提条件

- 非三权分立模式下，用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。
- 三权分立模式下，用户是 `sysadmin` 角色的成员。默认情况下，`sysroot` 用户属于 `sysadmin` 角色。

### 语法格式

```sql
IMPORT USERS SQL DATA ("<file_path>");
```

### 参数说明

| 参数                 | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `file_path`          | `users.sql` 文件的路径，支持以下两种格式：<br> - `nodelocal://<node_id>/<folder_name>/users.sql`：导入本地节点的用户信息文件。`node_id` 为节点 ID。如果本地只有一个节点，`node_id` 为 `1`。`folder_name` 为文件所在的文件夹，默认路径为 `/var/lib/kwdb/extern/<folder_name>`。<br> - `<server_ip>/<dir>/users.sql`：导入指定服务器的用户信息文件。 `server_ip`为服务器的 IP 地址和端口，例如 `http://172.18.0.1:8090`。`dir` 为 `users.sql` 文件所在文件夹的路径。                       |

### 返回参数

| 参数                 | 说明                                                                  |
|----------------------|---------------------------------------------------------------------|
| `job_id`             | 导入任务的 ID。                                                        |
| `status`             | 导入任务的状态。                                                       |
| `rows`               | 导入的行数。                                                          |

### 语法示例

```sql
IMPORT USERS SQL DATA ("nodelocal://1/users.sql");
```

执行成功后，控制台输出以下信息：

```sql
        job_id       |  status   | rows | 
---------------------+-----------+-------
            /        | succeeded |    1 |
(1 row)
```

## 集群参数信息导入

KWDB 支持使用 SQL 语句将从其他 KWDB 数据库导出的集群参数信息，以 `clustersetting.sql` 文件的形式导入到当前数据库。

如果待导入文件不存在或导入过程中发生错误，系统将提示错误原因，并回滚本次操作。

### 前提条件

- 非三权分立模式下，用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。
- 三权分立模式下，用户是 `sysadmin` 角色的成员。默认情况下，`sysroot` 用户属于 `sysadmin` 角色。

### 语法格式

```sql
IMPORT CLUSTER SETTING SQL DATA ("<file_path>");
```

### 参数说明

| 参数                 | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `file_path`          | `clustersetting.sql` 文件的路径，支持以下两种格式：<br> - `nodelocal://<node_id>/<folder_name>/clustersetting.sql`：导入本地节点的集群参数文件。`node_id` 为节点 ID。如果本地只有一个节点，`node_id` 为 `1`。`folder_name` 为文件所在的文件夹，默认路径为 `/var/lib/kwdb/extern/<folder_name>`。<br> - `<server_ip>/<dir>/clustersetting.sql`：导入指定服务器的集群参数文件。`server_ip`为服务器的 IP 地址和端口，例如 `http://172.18.0.1:8090`。`dir` 为文件所在文件夹的路径。                       |

### 语法示例

```sql
IMPORT CLUSTER SETTING SQL DATA ("nodelocal://1/clustersetting.sql");
```

执行成功后，控制台输出以下信息：

```sql
        prompt_information
+---------------------------------------+
  The cluster settings have been set    |
(1 row)
```