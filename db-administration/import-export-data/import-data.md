---
title: 数据导入
id: import-data
---

# 数据导入

KWDB 支持以下数据导入功能：

- 表级别数据导入
- 库级别数据导入

## 表级别数据导入

:::warning 说明

- 目前，KWDB 不支持导入数据库的系统表数据。
- 使用 `sort -t <separator> -k <primary_key_column> <file_name>` 命令提前对数据文件进行排序，有助于提升数据导入效率。

:::

KWDB 支持使用 SQL 语句将从其它 KWDB 数据库导出的时序表或关系表的元数据和用户数据导入到另一个 KWDB 数据库。元数据保存为 `meta.sql` 文件。用户数据保存为 `.csv` 文件。KWDB 支持同时导入表的用户数据和元数据，或者只导入表的用户数据或元数据。当目标表中已经存在用户数据，KWDB 支持增量导入用户数据。如果数据导入失败，系统无法回滚导入操作，但会保留已经成功导入的数据。

时序数据导入报错后，控制台输出写入失败的数据行数。同时，系统将写入失败的数据和错误信息保存到 `reject` 文件。`reject` 文件与导入的数据文件位于同一路径下。

### 前提条件

- 用户拥有 Admin 权限。
- 待导入表的列数和数据类型与数据库现有表的列数和数据类型保持一致。

### 语法格式

时序表和关系表的导入语法略有不同。导入数据时，时序表支持设置包围符、转义符和空值的表示形式。

- 导入时序表

  - 全量导入用户数据和元数据，并根据指定的文件目录或表结构创建表

    ```sql
    IMPORT TABLE CREATE USING "<sql_path>" CSV DATA ("<file_path>") WITH [delimiter = '<char>' | enclosed = '<char>' | escaped = '<char>' | nullif = '<char>' | thread_concurrency = '<int>'| batch_rows = '<int>'| auto_shrink];
    ```

  - 只导入用户数据或者增量导入用户数据

    ```sql
    IMPORT INTO <table_name> [<column_list>] CSV DATA ("<file_path>") WITH [delimiter = '<char>' | enclosed = '<char>' | escaped = '<char>' | nullif = '<char>' | thread_concurrency = '<int>'| batch_rows = '<int>'| auto_shrink];
    ```

  - 只导入元数据

    ```sql
    IMPORT TABLE CREATE USING "<sql_path>";
    ```

- 导入关系表

  - 同时导入用户数据和元数据

    ```sql
    IMPORT TABLE CREATE USING "<sql_path>" CSV DATA ("<file_path>") WITH DELIMITER = '<char>';
    ```

  - 只导入用户数据

    ```sql
    IMPORT INTO <table_name> CSV DATA ("<file_path>") WITH DELIMITER = '<char>';
    ```

  - 只导入元数据

    ```sql
    IMPORT TABLE CREATE USING "<sql_path>";
    ```

### 参数说明

| 参数                 | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `sql_path`           | 待导入元数据文件的存放路径，支持 `nodelocal://node_id/folder_name/file_name` 和 `server_ip/folder_name/file_name` 两种格式。<br > `nodelocal://node_id/folder_name/file_name`：导入本地节点的元数据文件。<br > - `node_id`：节点 ID。当本地只有一个节点时，`node_id` 取值是 `1`。<br > - `folder_name`：存放导入元数据文件的文件夹名称，默认是 `/var/lib/kwdb/extern/<folder_name>`。<br > - `file_name`：待导入元数据文件的名称。<br > `server_ip/server_ip/folder_name/file_name`：导入指定服务器的元数据文件。<br > - `server_ip`：指定服务器的 IP 地址和端口号，例如 `http://172.18.0.1:8090`。<br >- `folder_name`：存放导入元数据文件的文件夹名称。<br > - `file_name`：待导入元数据文件的名称。 |
| `column_list`        | 可选参数，用于指定待导入的列。<br > - 指定列名时，KWDB 既可以按照源文件中列的顺序导入指定列的数据也可以与源文件中的列顺序不一致。指定列必须包括第一列时间戳列和主标签列。<br > - 未指定列名时，KWDB 按照源文件中列的顺序导入所有数据。对于未指定列，如果该列支持空值，系统将自动写入默认值 `NULL`。如果该列不支持空值，系统提示 `Null value in column %s violates not-null constraints.`。                                                                                                                                                                                                                                                                                                            |
| `file_path`          | 待导入用户数据文件的存放路径，支持 `nodelocal://<node_id>/<folder_name>/<file_name>` 和 `<server_ip>/<dir>` 两种格式。<br > `nodelocal://<node_id>/<folder_name>/<file_name>`：导入本地节点的用户数据文件。<br > - `node_id`：节点 ID。当本地只有一个节点时，`node_id` 取值是 `1`。<br > - `folder_name`：存放导入用户数据文件的文件夹名称，默认是 `/var/lib/kwdb/extern/<folder_name>`。<br > - `file_name`：待导入用户数据文件的名称。只有导入关系表时，才需要指定用户数据文件的名称。<br > `<server_ip>/<dir>`：导入指定服务器的用户数据文件。<br >- `server_ip`：指定服务器的 IP 地址和端口，例如 `http://172.18.0.1:8090`。<br >- `dir`：存放导入用户数据文件的文件夹名称。                             |
| `delimiter`          | 可选参数，导入数据时，用于指定分隔符。系统根据指定的分隔符解析 `CSV` 文件并将解析的内容导入到 KWDB 系统。导入数据时，指定的分隔符需要与 `CSV` 文件中使用的分隔符保持一致，否则可能会出现解析后列数不匹配的情况，从而导致数据导入失败。                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `enclosed`           | 可选参数，导入时序数据时，用于指定包围符。默认为双引号（`"`），支持单引号（`'`）。使用单引号（`'`）作为包围符时，格式为 `"'"`。使用双引号（`"`）作为包围符时，格式为 `'"'`。包围符不能与分隔符相同。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `escaped`            | 可选参数，导入时序数据时，用于指定转义符。默认为双引号（`"`），支持反斜杠（`\`）。转义符不能与分隔符相同。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `nullif`             | 可选参数，导入时序数据时，用于指定空值的表示形式。默认不显示内容，支持指定为 `NULL`、`null`、`Null` 或 `\N`。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `thread_concurrency` | 导入时序数据时，用于指定并发读取、写入数据的数量。系统按照配置平均分割、并发读取和写入导入的文件。默认情况下，`thread_concurrency` 的取值是 `1`。`thread_concurrency` 的取值应该大于 `0`，小于等于系统核数的 2 倍。如果取值大于核数的 2 倍，系统按照核数的 2 倍并发读取、写入数据。`thread_concurrency` 参数支持与 `batch_rows`、`auto_shrink` 参数共同使用，中间使用逗号（`,`）隔开。                                                                                                                                                                                                                                                                                                                            |
| `batch_rows`         | 并发导入时序数据时，每次读取的行数。默认情况下，`batch_rows` 的取值是 `500`。`batch_rows` 的取值应该大于 `0`，并且 batch_rows x 单行数据的大小 ≤ 4 GB。如果 batch_rows x 单行数据的大小 > 4 GB, 系统按照 4 GB 支持的最大行数读取数据。`batch_rows` 参数支持与 `thread_concurrency`、`auto_shrink` 共同使用，中间使用逗号（`,`）隔开。                                                                                                                                                                                                                                                                                                                                                      |
| `auto_shrink`        | 可选参数，用于指定是否进行集群自适应衰减。默认情况下，系统不进行自适应衰减。设置了 `auto_shrink` 参数后，集群将自动每 10 秒进行一次衰减。`auto_shrink` 参数支持与 `batch_rows`、`thread_concurrency` 参数共同使用，中间使用逗号（`,`）隔开。                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `table_name`         | 目标表名，数据导入的目标表。待导入文件的数据列数和数据类型与数据库中目标表的列数及数据类型保持一致。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |

### 语法示例

- 导入本地节点的用户数据和元数据。

    ```sql
    IMPORT TABLE CREATE USING "nodelocal://1/a/meta.sql" CSV DATA ("nodelocal://1/a");
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows
    ---------------------+-----------+--------------------+------+--------------+--------------
                /        | succeeded |                  1 |    1 | /            | /
    (1 row)
    ```

    返回参数说明：

    | 参数                 | 说明                                                                  |
    |----------------------|---------------------------------------------------------------------|
    | `job_id`             | 导入任务的 ID。                                                        |
    | `status`             | 导入任务的状态。                                                       |
    | `fraction_completed` | 导入任务的完成情况，取值范围为 `[0,1]`。取值为 `1` 时，表示完成导入任务。 |
    | `rows`               | 导入的行数 。                                                          |
    | `abandon_row`        | 因数据去重未写入的行数。                                               |
    | `reject_rows`        | 导入数据时，写入出错的行数。系统将写入出错的数据保存到 `reject` 文件。   |

- 导入指定服务器的用户数据和元数据。

    ```sql
    IMPORT TABLE CREATE USING "http://172.18.0.1:8090/newdb/meta.sql" CSV DATA ("http://172.18.0.1:8090/newdb");
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows
    ---------------------+-----------+--------------------+------+--------------+--------------
                /        | succeeded |                  1 |    1 | /            | /
    (1 row)
    ```

- 导入本地节点的用户数据。

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a");
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows
    ---------------------+-----------+--------------------+------+--------------+--------------
                /        | succeeded |                  1 |    1 | /            | /
    (1 row)
    ```

- 导入本地节点的元数据。

    ```sql
    IMPORT TABLE CREATE USING "nodelocal://1/a/meta.sql";
    ```

    执行成功后，控制台输出以下信息：

    ```sql
      job_id |  status   | fraction_completed | rows | abandon_rows | reject_rows
    ---------+-----------+--------------------+------+--------------+--------------
      /      | succeeded |                  1 |    0 | 0            | 0
    (1 row)
    ```

- 导入本地节点的用户数据时，指定分隔符。

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a") WITH DELIMITER = '/';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows
    ---------------------+-----------+--------------------+------+--------------+--------------
                /        | succeeded |                  1 |    1 | /            | /
    (1 row)
    ```

- 导入本地节点的用户数据时，指定包围符为单引号（`'`）。

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a") WITH enclosed = "'";
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows
    ---------------------+-----------+--------------------+------+--------------+--------------
                /        | succeeded |                  1 |    1 | /            | /
    (1 row)
    ```

- 导入本地节点的用户数据时，指定转义符为反斜杠（`\`）。

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a") WITH escaped = '\';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows
    ---------------------+-----------+--------------------+------+--------------+--------------
                /        | succeeded |                  1 |    1 | /            | /
    (1 row)
    ```

- 导入本地节点的用户数据时，指定空值表现形式为 `NULL`。

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a") WITH NULLIF = 'NULL';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows
    ---------------------+-----------+--------------------+------+--------------+--------------
                /        | succeeded |                  1 |    1 | /            | /
    (1 row)
    ```

- 导入本地节点的用户数据时，设置写入速率。

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a") WITH thred_concurrency = '20', batch_rows = '200';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows
    ---------------------+-----------+--------------------+------+--------------+--------------
                /        | succeeded |                  1 |    1 | /            | /
    (1 row)
    ```

## 库级别数据导入

KWDB 支持一次性导入数据库中所有表的元数据和用户数据。KWDB 支持使用 SQL 语句将从其它 KWDB 数据库导出的所有表的元数据和用户数据导入到另一个 KWDB 数据库。KWDB 支持同时导入数据库的表数据和元数据，或者只导入数据库的元数据，不支持只导入所有表的用户数据。如果数据导入失败，系统无法回滚导入操作，但会保留已经成功导入的数据。

时序数据导入报错后，控制台输出写入失败的数据行数。同时，系统将写入失败的数据和错误信息保存到 `reject` 文件。`reject` 文件与导入的数据文件位于同一路径下。

### 前提条件

- 用户拥有 Admin 权限。
- 待导入数据的文件夹包含 `.csv` 文件 和 `.sql` 文件。

### 语法格式

时序数据库和关系数据库的导入语法略有不同。导入数据时，时序数据库支持设置包围符、转义符和空值的表示形式。

- 导入时序数据库

    ```sql
    IMPORT DATABASE CSV DATA ("<db_path>") WITH [ delimiter = '<char>' | enclosed = '<char>' | escaped = '<char>' | nullif = '<char>' | thread_concurrency = '<int>'| batch_rows = '<int>'| auto_shrink];
    ```

- 导入关系数据库

    ```sql
    IMPORT DATABASE CSV DATA ("<db_path>") [WITH DELIMITER = '<char>'];
    ```

### 参数说明

| 参数                 | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `db_path`            | 待导入数据库的存放路径。支持 `nodelocal://<node_id>/<dir>` 和 `<server_ip>/<dir>` 两种格式。<br > `nodelocal://node_id/<folder_name>`：导入本地节点的数据库数据。 <br >- `node_id`：节点 ID。当本地只有一个节点时，`node_id` 取值是 `1`。<br > - `dir`：存放导入数据的文件夹名称。默认情况下，KWDB 导入数据的存放路径是 `/var/lib/kwdb/extern/<folder_name>`。<br > `<server_ip>/<dir>`：导入指定服务器的数据库数据。	<br > - `server_ip`：指定服务器的 IP 地址和端口，例如 `http://172.18.0.1:8090`。<br > - `dir`：存放导入数据的文件夹名称。 |
| `delimiter`          | 可选参数，导入数据时，用于指定分隔符。系统根据指定的分隔符解析 `CSV` 文件并将解析的内容导入到 KWDB 系统。导入数据时，指定的分隔符需要与 `CSV` 文件中使用的分隔符保持一致，否则可能会出现解析后列数不匹配的情况，从而导致数据导入失败。                                                                                                                                                                                                                                                                                   |
| `enclosed`           | 可选参数，导入时序数据时，用于指定包围符。默认为双引号（`"`），支持单引号（`'`）。使用单引号（`'`）作为包围符时，格式为 `"'"`。使用双引号（`"`）作为包围符时，格式为 `'"'`。包围符不能与分隔符相同。                                                                                                                                                                                                                                                                                                                                  |
| `escaped`            | 可选参数，导入时序数据时，用于指定转义符。默认为双引号（`"`），支持反斜杠（`\`）。转义符不能与分隔符相同。                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `nullif`             | 可选参数，导入时序数据时，用于指定空值的表示形式。默认不显示内容，支持指定为 `NULL`、`null`、`Null` 或 `\N`。                                                                                                                                                                                                                                                                                                                                                                                                              |
| `thread_concurrency` | 导入时序数据时，用于指定并发读取、写入数据的数量。系统按照配置平均分割、并发读取和写入导入的文件。默认情况下，`thread_concurrency` 的取值是 `1`。`thread_concurrency` 的取值应该大于 `0`，小于等于系统核数的 2 倍。如果取值大于核数的 2 倍，系统按照核数的 2 倍并发读取、写入数据。`thread_concurrency` 参数支持与 `batch_rows`、`auto_shrink` 参数共同使用，中间使用逗号（`,`）隔开。                                                                                                                                                 |
| `batch_rows`         | 并发导入时序数据时，每次读取的行数。默认情况下，`batch_rows` 的取值是 `500`。`batch_rows` 的取值应该大于 `0`，并且 batch_rows x 单行数据的大小 ≤ 4 GB。如果 batch_rows x 单行数据的大小 > 4 GB, 系统按照 4 GB 支持的最大行数读取数据。`batch_rows` 参数支持与 `thread_concurrency`、`auto_shrink` 共同使用，中间使用逗号（`,`）隔开。                                                                                                                                                                           |
| `auto_shrink`        | 可选参数，用于指定是否进行集群自适应衰减。默认情况下，系统不进行自适应衰减。设置了 `auto_shrink` 参数后，集群将自动每 10 秒进行一次衰减。`auto_shrink` 参数支持与 `batch_rows`、`thread_concurrency` 参数共同使用，中间使用逗号（`,`）隔开。                                                                                                                                                                                                                                                                                     |

### 语法示例

- 导入本地节点的数据库数据。

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db");
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows
    ---------------------+-----------+--------------------+------+--------------+--------------
                /        | succeeded |                  1 |    1 | /            | /
    (1 row)
    ```

- 导入指定服务器的数据库数据。

    ```shell
    IMPORT DATABASE CSV DATA ("http://172.18.0.1:8090/newdb");
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows
    ---------------------+-----------+--------------------+------+--------------+--------------
              /         | succeeded |                  1 |    1 | /            | /
    (1 row)
    ```

- 导入本地节点的数据库数据时，指定分隔符。

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db") WITH DELIMITER = '/';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows
    ---------------------+-----------+--------------------+------+--------------+--------------
                /        | succeeded |                  1 |    1 | /            | /
    (1 row)
    ```

- 导入本地节点的数据库数据时，指定包围符为单引号（`'`）。

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db") WITH enclosed = "'";
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows
    ---------------------+-----------+--------------------+------+--------------+--------------
                /        | succeeded |                  1 |    1 | /            | /
    (1 row)
    ```

- 导入本地节点的数据库数据时，指定转义符为反斜杠（`\`）。

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db") WITH escaped ='\';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows
    ---------------------+-----------+--------------------+------+--------------+--------------
                /        | succeeded |                  1 |    1 | /            | /
    (1 row)
    ```

- 导入本地节点的数据库数据时，指定空值表现形式为 `NULL`。

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db") WITH NULLIF = 'NULL';
    ```

    执行成功后，控制台输出以下信息：

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows
    ---------------------+-----------+--------------------+------+--------------+--------------
                /        | succeeded |                  1 |    1 | /            | /
    (1 row)
    ```
