---
title: Import Data
id: import-data
---

# Import Data

The `IMPORT` statement imports the following data:

- **​Table data**: import the metadata, privilege information, and user data for the specified time-series or relational tables.
- **​Database data**: import the metadata, privilege information, and user data for the specified time-series or relational databases.
- **​User configuration**: import the SQL statements used for creating non-system users.
- **​Cluster parameters**: import the SQL statements used for setting cluster parameters.

::: warning Note

- Currently, KWDB does not support importing the data for system tables.
- When importing table data, you can use the `sort -t <separator> -k <primary_key_column> <file_name>` command to sort files to be imported. This helps improve the import efficiency.

:::

## Import Table Data

The `IMPORT` statement imports data from one KWDB database into another KWDB database, including the metadata, privilege information, and user data for the time-series or relational tables. The metadata and privilege information are stored in the `meta.sql` file while the user data is stored in `.csv` file.

KWDB supports importing data in any of the following ways:

- Import both the user data and metadata at the same time.
- Import the user data only. When there is data in the target table, KWDB supports incremental import of user data.
- Import the metadata only.

For relational tables, KWDB performs operations based on whether the target table contains label columns and data columns.

- When the target table contains both label columns and data columns:
  - When KWDB enables MAC and the target table contains data for label columns, KWDB will check label values of the label columns and the subject. If the data of the label columns is set to NULL or if the label data format or level requirement is not met, KWDB fails to import the data. For details about levels, see [MAC Policies](../../../en/db-security/access-control.md#mac-policies).
  - When only importing data for data columns, KWDB fills label columns with user labels. If no user labels are available, KWDB fills label columns with empty strings (`''`).
- When the target table only contains data columns: KWDB imports the data and returns an error if the number of data columns is not matched.
- When the target table only contains label columns: KWDB fails to import the data and returns an error saying the number of data columns is not matched.

For relational data, if an import fails, KWDB will rollback the import. For time-series data, if an import fails, KWDB will not rollback the import but keep imported files in the destination. The console prints the number of rows that fail to be imported and stores the rejected data and the error messages to the `reject.txt` file. The `reject.txt` file is generated in the same directory as the files to be imported.

::: warning Note
When importing the user data only, the number and data type of columns in the specified table should be identical to that in the existing table.
:::

### Privileges

The user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

### Syntax

- Fully import of the user data, metadata, and privilege information and create tables based on the specified directories and table structure

    ```sql
    IMPORT TABLE CREATE USING "<meta.sql_path>" CSV DATA ("<file_path>") WITH [delimiter = '<char>' | enclosed = '<char>' | escaped = '<char>' | nullif = '<char>' | thread_concurrency = '<int>'| batch_rows = '<int>'| auto_shrink | comment | charset = '<coding>' | privileges];
    ```

- Import the user data only or incrementally import the user data

    ```sql
    IMPORT INTO <table_name> [<column_list>] CSV DATA ("<file_path>") WITH [delimiter = '<char>' | enclosed = '<char>' | escaped = '<char>' | nullif = '<char>' | thread_concurrency = '<int>'| batch_rows = '<int>'| auto_shrink | charset = '<coding>'];
    ```

- Import the metadata and privilege information only

    ```sql
    IMPORT TABLE CREATE USING "<sql_path>" [WITH privileges];
    ```

### Parameters

| Parameter                 | Description |
|----------------------|------------------------|
| `sql_path`           | Specify the URL of the file location which stores the metadata to be imported, supporting `nodelocal://<node_id>/<folder_name>/meta.sql` and `<server_ip>/<folder_name>/meta.sql` formats. <br> `nodelocal://<node_id>/<folder_name>/meta.sql`: import the metadata files from local nodes. <br> - `node_id`: the node ID. When there is only one node, it is set to `1`. <br> - `folder_name`: the name of the directory that stores the metadata files. By default, it is `/var/lib/kaiwudb/extern/<folder_name>`. <br> `<server_ip>/<folder_name>/meta.sql`: import the metadata files from a specified server. <br> - `server_ip`: the IP address and port ID of the server, such as `http://172.18.0.1:8090`. <br> - `folder_name`: the name of the directory that stores the metadata files. |
| `file_path`          | Specify the URL of the file location which stores the user data to be imported, supporting `nodelocal://<node_id>/<folder_name>/<file_name>` and `<server_ip>/<dir>` formats. <br> `nodelocal://<node_id>/<folder_name>/<file_name>`: import the user data files from local nodes. <br> - `node_id`: the node ID. When there is only one node, it is set to `1`. <br> - `folder_name`: the name of the directory that stores the user data files. By default, it is `/var/lib/kaiwudb/extern/<folder_name>`. <br > - `file_name`: the names of the user data files to be imported. This parameter is only available for importing relational tables. <br> `<server_ip>/<dir>`: import the user data files from a specified server. 	<br> - `server_ip`: the IP address and port ID of the server, such as `http://172.18.0.1:8090`. <br> - `folder_name`: the name of the directory that stores the user data files. <br> **Note**: If there is the `reject.txt` file under the URL, check the data based on error messages to avoid subsequent import failure.|
| `delimiter`          | Optional. The character that delimits columns within each row. KWDB analyzes `.csv` files and imports data into KWDB database based on the delimiter. When importing data, you should use the same delimiter that is used when exporting the data. If delimiters used for exporting and importing data are inconsistent, it will cause an import failure. |
| `enclosed`           | Optional. The character that encloses columns within each row. By default, it is set to the double quotation mark (`"`). KWDB also supports using the single quotation mark (`'`). <br>- When using the single quotation mark (`''`), the format is `"'"`. <br>- When using the double quotation mark (`"`), the format is `'"'`. <br> The enclosed character cannot be identical to the delimiter. <br>**Note**: If there is any line break character in the files to be imported, avoid enabling multi-thread import.|
| `escaped` | Optional. The character that causes one or more characters that follow it to be interpreted differently. By default, it is set to the double quotation mark (`"`). KWDB also supports using the backslash (`\`). <br> The escape character cannot be identical to the delimiter.|
| `nullif` | Optional. The string that is used to represent `NULL` values. By default, no content is displayed. KWDB supports setting it to `NULL`, `null`, `Null` or `\N`.|
| `thread_concurrency` | Optional. Specify the number of data to be written concurrently. KWDB splits, concurrently reads, and writes imported files based on this setting. By default, it is set to `1`. The value should be greater than `0` and smaller than or equal to 2 times of the number of the system cores. If the value is greater than 2 times of the number of the system cores, KWDB will read and write data based on 2 times of the number of the system cores. You can use this parameter in combination with the `auto_shrink` and `batch_rows` parameters, separating them using a comma (`,`). <br> **Note**: When enabling multi-thread import, if there is any line break character in the files to be imported, it will cause an import failure. In this case, you need to remove the databases or tables to be imported, set the `thread_concurrency` parameter to `1`, and then re-import the files.|
| `batch_rows`         | Specify the number of rows to read when importing data concurrently. By default, it is set to `500`. The value should be greater than `0`. Besides, the result that is obtained by multiplying `batch_rows` and the size of each row should be smaller than or equal to 4 GB. If the result is greater than 4 GB, KWDB will read data based on the maximum number of rows available for 4 GB. You can use this parameter in combination with the `auto_shrink` and `thread_concurrency` parameters, separating them using a comma (`,`). |
| `auto_shrink`        | Optional. Specify whether to automatically shrink a KWDB cluster. By default, do not automatically shrink a KWDB cluster. With this parameter, the cluster is automatically shrinked every 10 seconds. You can use this parameter in combination with the `batch_rows` and `thread_concurrency` parameters, separating them using a comma (`,`). |
| `comment` | Optional. Specify whether to import comments on tables or columns. By default, KWDB does not import comments. <br> - If the specified tables or columns have comments, you can import the files with these comments using the `WITH comment` parameter. Otherwise, KWDB does not import comments. <br> - If the specified tables or columns do not have any comments, KWDB returns an error when you import the files using the `WITH comment` parameter, saying `NO COMMENT statement in the SQL file`.|
| `charset` | Optional. Specify the character set encoding for the data to import. By default, it is set to `utf8`. Available options are `gbk`, `gb18030` or `utf8`.<br>**Note**: The specified character set encoding must be identical with the existing character set encoding. Otherwise, it may cause import failures or garbled codes. |
| `privileges` | Optional. Import the privilege information of non-system users for the specified tables. <br>- With this parameter, KWDB reads and runs the SQL statements that are related to privileges in the metadata file. **Note**: If the metadata file does not contain any SQL statements for privileges, KWDB returns an error, saying `NO PRIVILEGES statement in the SQL file`. In this case, you need to remove this parameter and re-import the data. <br>- Without this parameter, KWDB will not read the SQL statements that are related to privileges from the metadata file.|
| `table_name`         | The name of the table to import. The number and data type of columns in the specified table should be identical to that in the existing table. |
| `column_list`        | Optional. Specify the columns to import. <br > - When column names are specified, KWDB can either import data based on the order of columns in the original table or import data without following the order of columns in the original table. For time-series tables, the first column (timestamp-typed column) and primary tag columns must be specified when specifying column names. <br > - When column names are not specified, KWDB imports data based on the order of columns in the original table. For unspecified columns, if these columns support NULL values, KWDB will automatically insert NULL values for them. Otherwise, KWDB returns an error, saying `Null value in column %s violates not-null constraints.`.  <br> **Note** <br> When the target table has label columns, KWDB does not support importing specified columns. |

### Responses

| Field                | Description                                                                                                                                     |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| `job_id`             | The ID of the import job.                                                                                                                       |
| `status`             | The status of the import job.                                                                                                                   |
| `fraction_completed` | The fraction (between `0` and `1`) of the import job that has been completed. When it is set to `1`, it means that the import job is completed. |
| `rows`               | The number of imported rows.                                                                                                                    |
| `abandon_rows`       | The number of rows that are not imported because of duplicate data.                                                                             |
| `reject_rows`        | The number of rejected rows. The rejected rows are written into the `reject.txt` file.                                                          |
| `note`               | The system output for an import job error. When an import job succeeds, it shows `None`.                                                        |

### Examples

- Import both the user data and metadata from a local node.

    ```sql
    IMPORT TABLE CREATE USING "nodelocal://1/a/meta.sql" CSV DATA ("nodelocal://1/a");
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- Import both the user data and metadata from a local node using the `COMMENT` option to import data and comments.

    ```sql
    IMPORT TABLE CREATE USING "nodelocal://1/tb/meta.sql" CSV DATA ("nodelocal://1/tb") WITH COMMENT;
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------------------+-----------+--------------------+------+--------------+-------------+------
                /        | succeeded |                  1 |    1 | 0            | 0           | None
    (1 row)
    ```

- Import both the user data and metadata from a specified server.

    ```sql
    IMPORT TABLE CREATE USING "http://172.18.0.1:8090/newdb/meta.sql" CSV DATA ("http://172.18.0.1:8090/newdb");
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------------------+-----------+--------------------+------+--------------+-------------+------
                /        | succeeded |                  1 |    1 | 0            | 0           | None
    (1 row)
    ```

- Import the user data from a local node.

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a");
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------------------+-----------+--------------------+------+--------------+-------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- Import the metadata from a local node.

    ```sql
    IMPORT TABLE CREATE USING "nodelocal://1/a/meta.sql";
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
      job_id |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------+-----------+--------------------+------+--------------+-------------+------
      /      | succeeded |                  1 |    0 | 0            | 0           | None
    (1 row)
    ```

- Import the user data from a local node using the `delimiter` option to define the character that delimits columns within each row.

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a") WITH DELIMITER = '/';
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------------------+-----------+--------------------+------+--------------+-------------+------
                /        | succeeded |                  1 |    1 | 0            | 0           | None
    (1 row)
    ```

- Import the user data from a local node using the `enclosed` option to enclose columns within each row.

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a") WITH enclosed = "'";
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------------------+-----------+--------------------+------+--------------+-------------+------
                /        | succeeded |                  1 |    1 | 0            | 0           | None
    (1 row)
    ```

- Import the user data from a local node using the `escaped` option to set the escape character to the backslash (`\`).

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a") WITH escaped = '\';
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------------------+-----------+--------------------+------+--------------+-------------+------
                /        | succeeded |                  1 |    1 | 0            | 0           | None
    (1 row)
    ```

- Import the user data from a local node using the `NULLIF` option to define the string that represents NULL values.

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a") WITH NULLIF = 'NULL';
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------------------+-----------+--------------------+------+--------------+-------------+------
                /        | succeeded |                  1 |    1 | 0            | 0           | None
    (1 row)
    ```

- Import the user data from a local node using the `thred_concurrency` and `batch_rows` options to set the write rate.

    ```sql
    IMPORT INTO user_info1 CSV DATA ("nodelocal://1/a") WITH thred_concurrency = '20', batch_rows = '200';
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows | note
    ---------------------+-----------+--------------------+------+--------------+-------------+------
                /        | succeeded |                  1 |    1 | 0            | 0           | None
    (1 row)
    ```

## Import Database Data

The `IMPORT` statement imports data from one KWDB database into another KWDB database, including the metadata, privilege information, and user data for all time-series or relational tables in the database.

KWDB supports importing data in any of the following ways:

- Import the user data, metadata, and privilege information at the same time.
- Import the metadata and privilege information only.

For relational data, if an import fails, KWDB will rollback the import. For time-series data, if an import fails, KWDB will not rollback the import but keep imported files in the destination. The console prints the number of rows that fail to be imported and stores the rejected data and the error messages to the `reject.txt` file. The `reject.txt` file is generated in the same directory as the files to be imported.

::: warning Note
KWDB does not support importing the user data of all tables only.
:::

### Privileges

: the user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

- The directory to be imported must have `.csv` files and `.sql` files.

### Syntax

```sql
IMPORT DATABASE CSV DATA ("<db_path>") WITH [ delimiter = '<char>' | enclosed = '<char>' | escaped = '<char>' | nullif = '<char>' | thread_concurrency = '<int>'| batch_rows = '<int>'| auto_shrink | comment | charset = '<coding>' | privileges ];
```

### Parameters

| Parameter                 | Description |
|----------------------|------------------------|
| `db_path`          | Specify the URL of the file location which stores the database to be imported, supporting `nodelocal://<node_id>/<dir>` and `<server_ip>/<dir>` formats. <br> `nodelocal://<node_id>/<dir>`: import the database from local nodes. <br> - `node_id`: the node ID. When there is only one node, it is set to `1`. <br> - `dir`: the name of the directory that stores the files to be imported. By default, it is `/var/lib/kaiwudb/extern/<folder_name>`. <br> `<server_ip>/<dir>`: import the database from a specified server. <br> - `server_ip`: the IP address and port ID of the server, such as `http://172.18.0.1:8090`. <br> - `dir`: the name of the directory that stores the files to be imported. <br> **Note**: If there is the `reject.txt` file under the URL, check the data based on error messages to avoid subsequent import failure.|
| `delimiter`          | Optional. The character that delimits columns within each row. KWDB analyzes `.csv` files and imports data into KWDB database based on the delimiter. When importing data, you should use the same delimiter that is used when exporting the data. If delimiters used for exporting and importing data are inconsistent, it will cause an import failure. |
| `enclosed`           | Optional. The character that encloses columns within each row. By default, it is set to the double quotation mark (`"`). KWDB also supports using the single quotation mark (`'`). <br>- When using the single quotation mark (`''`), the format is `"'"`. <br>- When using the double quotation mark (`"`), the format is `'"'`. <br> The enclosed character cannot be identical to the delimiter. <br>**Note**: If there is any line break character in the files to be imported, avoid enabling multi-thread import.|
| `escaped` | Optional. The character that causes one or more characters that follow it to be interpreted differently. By default, it is set to the double quotation mark (`"`). KWDB also supports using the backslash (`\`). <br> The escape character cannot be identical to the delimiter.|
| `nullif` | Optional. The string that is used to represent `NULL` values. By default, no content is displayed. KWDB supports setting it to `NULL`, `null`, `Null` or `\N`.|
| `thread_concurrency` | Optional. Specify the number of data to be written concurrently. KWDB splits, concurrently reads, and writes imported files based on this setting. By default, it is set to `1`. The value should be greater than `0` and smaller than or equal to 2 times of the number of the system cores. If the value is greater than 2 times of the number of the system cores, KWDB will read and write data based on 2 times of the number of the system cores. You can use this parameter in combination with the `auto_shrink` and `batch_rows` parameters, separating them using a comma (`,`). <br> **Note**: When enabling multi-thread import, if there is any line break character in the files to be imported, it will cause an import failure. In this case, you need to remove the databases or tables to be imported, set the `thread_concurrency` parameter to `1`, and then re-import the files.|
| `batch_rows`         | Specify the number of rows to read when importing data concurrently. By default, it is set to `500`. The value should be greater than `0`. Besides, the result that is obtained by multiplying `batch_rows` and the size of each row  should be smaller than or equal to 4 GB. If the result is greater than 4 GB, KWDB will read data based on the maximum number of rows available for 4 GB. You can use this parameter in combination with the `auto_shrink` and `thread_concurrency` parameters, separating them using a comma (`,`). |
| `auto_shrink`        | Optional. Specify whether to automatically shrink a KWDB cluster. By default, do not automatically shrink a KWDB cluster. With this parameter, the cluster is automatically shrinked every 10 seconds. You can use this parameter in combination with the `batch_rows` and `thread_concurrency` parameters, separating them using a comma (`,`). |
| `comment` | Optional. Specify whether to import comments on databases. By default, KWDB does not import comments. <br> - If the specified databases have comments, you can import the databases with these comments using the `WITH comment` parameter. Otherwise, KWDB does not import comments. <br> - If the specified databases do not have any comments, KWDB returns an error when you import the databases using the `WITH comment` parameter, saying `NO COMMENT statement in the SQL file`.|
| `charset` | Optional. Specify the character set encoding for the data to import. By default, it is set to `utf8`. Available options are `gbk`, `gb18030` or `utf8`.<br>**Note**: The specified character set encoding must be identical with the existing character set encoding. Otherwise, it may cause import failures or garbled codes. |
| `privileges` | Optional. Import the privilege information of non-system users for the specified databases. <br>- With this parameter, KWDB reads and runs the SQL statements that are related to privileges in the metadata file. **Note**: If the metadata file does not contain any SQL statements for privileges, KWDB returns an error, saying `NO PRIVILEGES statement in the SQL file`. In this case, you need to remove this parameter and re-import the databases. <br>- Without this parameter, KWDB will not read the SQL statements that are related to privileges from the metadata file.|

### Responses

| Field                | Description                                                                                                                                     |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| `job_id`             | The ID of the import job.                                                                                                                       |
| `status`             | The status of the import job.                                                                                                                   |
| `fraction_completed` | The fraction (between `0` and `1`) of the import job that has been completed. When it is set to `1`, it means that the import job is completed. |
| `rows`               | The number of imported rows.                                                                                                                    |
| `abandon_rows`       | The number of rows that are not imported because of duplicate data.                                                                             |
| `reject_rows`        | The number of rejected rows. The rejected rows are written into the `reject.txt` file.                                                          |
| `note`               | The system output for an import job error. When an import job succeeds, it shows `None`.                                                        |

### Examples

- Import a database from a local node.

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db");
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- Import a database from a local node using the `COMMENT` option to import data and comments.

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db") WITH COMMENT;
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- Import a database from a specified server.

    ```shell
    IMPORT DATABASE CSV DATA ("http://172.18.0.1:8090/newdb");
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
              /          | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- Import a database from a local node using the `delimiter` option to define the character that delimits columns within each row.

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db") WITH DELIMITER = '/';
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- Import a database from a local node using the `enclosed` option to enclose columns within each row.

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db") WITH enclosed = "'";
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- Import a database from a local node using the `escaped` option to set the escape character to the backslash (`\`).

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db") WITH escaped ='\';
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- Import a database from a local node using the `NULLIF` option to define the string that represents NULL values.

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db") WITH NULLIF = 'NULL';
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

- Import a database from a local node using the `charset` option to set the character set encoding to `GBK`.

    ```sql
    IMPORT DATABASE CSV DATA ("nodelocal://1/db") WITH charset = 'GBK';
    ```

    If you succeed, you should see an output similar to the following:

    ```sql
            job_id       |  status   | fraction_completed | rows | abandon_rows | reject_rows  | note
    ---------------------+-----------+--------------------+------+--------------+--------------+------
                /        | succeeded |                  1 |    1 | 0            | 0            | None
    (1 row)
    ```

## Import User Information

KWDB reads the `users.sql` file and imports all non-system user information from a specified KWDB database into the current database.

If the files to be imported do not exist or any error occurs during an import, KWDB returns an error and rollbacks the import.

::: warning Note
The imported user information does not include the passwords. When an import completes, you need to reset the passwords for users.
:::

### Privileges

: the user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.


### Syntax

```sql
IMPORT USERS SQL DATA ("<file_path>");
```

### Parameters

| Parameter                 | Description |
|----------------------|---------------|
| `file_path`           | Specify the URL of the `users.sql` file, supporting `nodelocal://<node_id>/<folder_name>/users.sql` and `<server_ip>/<dir>/users.sql` formats. <br> `nodelocal://<node_id>/<folder_name>/users.sql`: import the user information from local nodes. <br> - `node_id`: the node ID. When there is only one node, it is set to `1`. <br> - `folder_name`: the name of the directory that stores the `users.sql` file. By default, it is `/var/lib/kaiwudb/extern/<folder_name>`. <br> `<server_ip>/<dir>/users.sql`: import the user information from a specified server. <br> - `server_ip`: the IP address and port ID of the server, such as `http://172.18.0.1:8090`. <br> - `dir`: the name of the directory that stores the `users.sql` file. |

### Responses

| Field    | Description                   |
|----------|-------------------------------|
| `job_id` | The ID of the import job.     |
| `status` | The status of the import job. |
| `rows`   | The number of imported rows.  |

### Examples

This example imports all non-system user information from a local node into the current database.

```sql
IMPORT USERS SQL DATA ("nodelocal://1/users.sql");
```

If you succeed, you should see an output similar to the following:

```sql
        job_id       |  status   | rows | 
---------------------+-----------+-------
            /        | succeeded |    1 |
(1 row)
```

## Import Cluster Settings

KWDB reads the `clustersetting.sql` file and imports all cluster settings from a specified KWDB database into the current database.

If the `clustersetting.sql` file does not exist or any error occurs during an import, KWDB returns an error and rollbacks the import.

### Privileges

: the user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.


### Syntax

```sql
IMPORT CLUSTER SETTING SQL DATA ("<file_path>");
```

### Parameters

| Parameter                 | Description |
|----------------------|-----|
| `file_path`           | Specify the URL of the `clustersetting.sql` file, supporting `nodelocal://<node_id>/<folder_name>/clustersetting.sql` and `<server_ip>/<dir>/clustersetting.sql` formats. <br> `nodelocal://<node_id>/<folder_name>/clustersetting.sql`: import the user information from local nodes. <br> - `node_id`: the node ID. When there is only one node, it is set to `1`. <br> - `folder_name`: the name of the directory that stores the `clustersetting.sql` file. By default, it is `/var/lib/kaiwudb/extern/<folder_name>`. <br> `<server_ip>/<dir>/clustersetting.sql`: import the user information from a specified server. <br> - `server_ip`: the IP address and port ID of the server, such as `http://172.18.0.1:8090`. <br> - `dir`: the name of the directory that stores the `clustersetting.sql` file. |

### Examples

This example imports the current cluster settings from a local node into the current database.

```sql
IMPORT CLUSTER SETTING SQL DATA ("nodelocal://1/clustersetting.sql");
```

If you succeed, you should see an output similar to the following:

```sql
        prompt_information
+---------------------------------------+
  The cluster settings have been set    |
(1 row)
```
