---
title: Export Data
id: export-data
---

# Export Data

The `EXPORT` statement exports the following data:

- **Table data**: Exports the metadata, privilege information, and user data for the specified time-series or relational tables.
- **Database data**: Exports the metadata, privilege information, and user data for the specified time-series or relational databases.
- **User configuration**: Exports SQL statements or CSV files for creating non-system users.
- **Cluster parameters**: Exports SQL statements or CSV files for cluster parameter settings.

## Export Table Data

The `EXPORT` statement exports the following table data:

- The metadata, privilege information, and user data for both time-series and relational tables. The metadata and privilege information are exported to the `meta.sql` file, while user data can be exported in `.csv` or `.sql` format.
- The specified user data for both time-series and relational tables, exported in `.csv` format.
- Privilege information tables, exported in `.csv` format.

If an export fails due to an unreachable destination, KWDB returns an error. For export failures caused by other reasons, KWDB will keep exported files in the destination.

### Privileges

The user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

- To export data to a specified server:
  - The target server must run properly and allow the `PUT` permission.
  - You must have permission to access the target server.
  - To create a folder to store exported data, you must have permission to create directories on the server.

### Syntax

:::warning Note

- When exporting data using the `SELECT` statement, KWDB will not export the metadata.
- If the `SELECT` statement returns no results, KWDB will not export any data and will return a `succeed` response.
- When exporting a time-series table with regular tag indexes, KWDB will also export the index creation statements.
- When exporting table metadata, user data, and privilege information in SQL format, tables containing `BYTES` and `VARBYTES` data types are currently not supported.

:::

- Export the metadata, privilege information, and user data for both time-series and relational tables

  - Export user data in CSV format

    ```sql
    EXPORT INTO CSV "<expt_path>" FROM TABLE <table_name> WITH [ column_name | meta_only | data_only | delimiter = '<char>' | chunk_rows = '<number>' | enclosed = '<char>' | escaped = '<char>' | nullas = '<char>' | comment | charset = '<coding>' | privileges ];
    ```

  - Export user data in SQL format

    ```sql
    EXPORT INTO SQL "<expt_path>" FROM TABLE <table_name> WITH [ meta_only | data_only | delimiter = '<char>' | comment | charset = '<coding>' | privileges ];
    ```

- Export user data using the `SELECT` statement

    ```sql
    EXPORT INTO CSV "<expt_path>" FROM <select_clause>;
    ```

- Export privilege information tables

    ```sql
    EXPORT INTO CSV "<expt_path>" FROM SELECT * FROM system.information_schema.table_privileges;
    ```

### Parameters

| Parameter | Description |
|---| --- |
| `expt_path` | Specifies the URL of the file location where exported data will be stored, supporting `nodelocal://<node_id>/<dir>` and `<server_ip>/<dir>` formats. <br><br> `nodelocal://<node_id>/<dir>`: Exports files to local nodes. <br> - `node_id`: The node ID. When there is only one node, it is set to `1`. <br> - `dir`: The name of the directory to store exported files. If the target directory does not exist, KWDB will create the directory under the path defined for saving data during KWDB installation. By default, KWDB saves data to `/var/lib/kaiwudb/extern/<folder_name>`. <br><br> `<server_ip>/<dir>`: Exports files to a specified server. <br> - `server_ip`: The IP address and port ID of the server, such as `http://172.18.0.1:8090`. <br> - `dir`: The name of the directory to store exported files. If the target directory does not exist, KWDB will create the directory. |
| `table_name` | The name of the table to export. |
| `column_name` | Optional. Adds column names when exporting data. By default, KWDB does not export column names.|
| `meta_only` | Optional. Exports only the metadata. This parameter is mutually exclusive with the `data_only` parameter. |
| `data_only` | Optional. Exports only the user data. This parameter is mutually exclusive with the `meta_only` parameter.|
| `delimiter` | Optional. The character that delimits columns within each row. The delimiter can be a single character or an empty character but not a double quotation mark (`"`). <br>- The delimiter should not be identical to any character in the user data. If the delimiter appears in the user data, KWDB will use the enclosed character to enclose the delimiter to prevent export failures. <br>- If you specify a delimiter when exporting data, you must use the same delimiter when importing the data. Inconsistent delimiters for export and import will cause an import failure. |
| `chunk_rows` | Optional. The number of rows to be converted and written to a single `.csv` file. If the number of rows in the specified table exceeds this configured limit, KWDB will produce multiple files based on the configured limit. The produced files are named in the format `<node_id>.<file_id>.csv`. Both the default value and the maximum value are set to `100000`. When set to `0`, there is no limit on the number of rows. |
| `enclosed` | Optional. The character that encloses columns within each row. By default, it is set to the double quotation mark (`"`). KWDB also supports using the single quotation mark (`'`). <br>- When using the single quotation mark (`'`), the format is `"'"`. <br>- When using the double quotation mark (`"`), the format is `'"'`. <br> The enclosed character cannot be identical to the delimiter. |
| `escaped` | Optional. The character that causes one or more following characters to be interpreted differently. By default, it is set to the double quotation mark (`"`). KWDB also supports using the backslash (`\`). <br> The escape character cannot be identical to the delimiter.|
| `nullas` | Optional. The string used to represent `NULL` values. By default, no content is displayed. KWDB supports setting it to `NULL`, `null`, `Null`, or `\N`.|
| `comment` | Optional. Specifies whether to export comments on tables or columns. By default, KWDB does not export comments. <br> - If the specified tables or columns have comments, you can export the files with these comments using the `WITH comment` parameter. Otherwise, KWDB does not export comments. <br> - If the specified tables or columns do not have any comments, KWDB returns an error when you export the files using the `WITH comment` parameter: `TABLE or COLUMN without COMMENTS cannot be used 'WITH COMMENT'`.|
| `charset` | Optional. Specifies the character set encoding for the data to export. By default, it is set to `utf8`. Available options are `gbk`, `gb18030`, or `utf8`. |
| `privileges` | Optional. Exports the privilege information of non-system users for the specified tables. With this parameter, KWDB reads the `system.information_schema.table_privileges` table and exports related privileges to the `meta.sql` file. |
| `select_clause` | A selection query to generate data to be exported. For details about the `SELECT` statement for time-series tables, see [SELECT](../../../en/sql-reference/dml/ts-db/ts-select.md). For details about the `SELECT` statement for relational tables, see [SELECT](../../../en/sql-reference/dml/relational-db/relational-select.md). |

### Examples

These examples assume that you have created a time-series table (`ts_table`) and inserted data into this table.

- Basic Export

  - Export to a local node.

    ```sql
    -- Export in CSV format
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table;

    -- Export in SQL format
    EXPORT INTO SQL "nodelocal://1/a" FROM TABLE ts_table;
    ```

  - Export to a specified server.

    ```sql
    -- Export in CSV format
    EXPORT INTO CSV "http://172.18.10.1:8090/ts_table" FROM TABLE ts_table;
    
    -- Export in SQL format
    EXPORT INTO SQL "http://172.18.10.1:8090/ts_table" FROM TABLE ts_table;
    ```

- Conditional Export

  - Filter data based on the timestamp and column name.

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM SELECT ts, value, site_id FROM ts_table WHERE ts > '2024-02-01 09:00:00';
    ```

  - Export non-NULL values.

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM SELECT * from ts_table WHERE value IS NOT NULL;
    ```

- Specify Export Content

  - Export only the user data.

    ```sql
    -- Export in CSV format
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH data_only;

    -- Export in SQL format
    EXPORT INTO SQL "nodelocal://1/a" FROM TABLE ts_table WITH data_only;
    ```

  - Export only the metadata.

    ```sql
    -- Export in CSV format
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH meta_only;

    -- Export in SQL format
    EXPORT INTO SQL "nodelocal://1/a" FROM TABLE ts_table WITH meta_only;
    ```

  - Limit the number of rows in a single file.

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH chunk_rows = '1000';
    ```

  - Export comments.

    ```sql
    -- Export in CSV format
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH COMMENT;
    
    -- Export in SQL format
    EXPORT INTO SQL "nodelocal://1/a" FROM TABLE ts_table WITH COMMENT;
    ```

- Formatting Options

  - Set the delimiter to slash (`/`).

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH DELIMITER = '/';
    ```

  - Set the enclosed character to single quotation mark (`'`).

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH enclosed = "'";
    ```

  - Set the escape character to backslash (`\`).

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH escaped = '\';
    ```

  - Set the NULL representation to `NULL`.

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH NULLAS = 'NULL';
    ```

  - Set the character set encoding to `GBK`.

    ```sql
    EXPORT INTO CSV "nodelocal://1/a" FROM TABLE ts_table WITH charset = 'GBK';
    ```

## Export Database Data

KWDB supports exporting the metadata, user data, and privilege information of all tables in a database at once.

- Time-series database

    All exported tables are in the `public` schema. Each table is a single directory that stores the user data (supports `.csv` and `.sql` formats) of the table. The structure for the exported time-series database is shown below:

    ```shell
    tsdb
    |-- meta.sql
    |-- public
      |-- t1
        |-- n1.0.csv
      |-- t2
        |-- n1.0.csv
    ```

- Relational database

    All exported tables are structured based on their schemas. Each table is a single directory that stores the metadata (`meta.sql` file) and user data (supports `.csv` and `.sql` formats) of the table. The structure for the exported relational database is shown below:

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

### Privileges

The user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.


### Syntax

:::warning Note
When exporting user data in SQL format, tables containing `BYTES` and `VARBYTES` data types are currently not supported.
:::

The export syntax is the same for time-series and relational databases:

- Export database data in CSV format

  ```sql
  EXPORT INTO CSV "<expt_path>" FROM DATABASE <db_name> WITH [ column_name | meta_only | data_only | delimiter = '<char>' | chunk_rows = '<number>' | enclosed = '<char>' | escaped = '<char>' | nullas = '<char>' | comment | charset = '<coding>' | privileges ];
  ```

- Export database data in SQL format

  ```sql
  EXPORT INTO SQL "<expt_path>" FROM DATABASE <db_name> WITH [ meta_only | data_only | delimiter = '<char>' | comment | charset = '<coding>' | privileges ];
  ```

### Parameters

| Parameter | Description |
|---------------|-----------------|
| `expt_path` | Specifies the URL of the file location where exported data will be stored, supporting `nodelocal://<node_id>/<dir>` and `<server_ip>/<dir>` formats. <br><br> `nodelocal://<node_id>/<dir>`: Exports files to local nodes. <br> - `node_id`: The node ID. When there is only one node, it is set to `1`. <br> - `dir`: The name of the directory to store exported files. If the target directory does not exist, KWDB will create the directory under the path defined for saving data during KWDB installation. By default, KWDB saves data to `/var/lib/kaiwudb/extern/<folder_name>`. <br><br> `<server_ip>/<dir>`: Exports files to a specified server. <br> - `server_ip`: The IP address and port ID of the server, such as `http://172.18.0.1:8090`. <br> - `dir`: The name of the directory to store exported files. If the target directory does not exist, KWDB will create the directory. |
| `db_name`     | The name of the database to export.  |
| `column_name` | Optional. Adds column names when exporting data. By default, KWDB does not export column names. |
| `meta_only` | Optional. Exports only the metadata. This parameter is mutually exclusive with the `data_only` parameter. |
| `data_only` | Optional. Exports only the user data. This parameter is mutually exclusive with the `meta_only` parameter.|
| `delimiter` | Optional. The character that delimits columns within each row. The delimiter can be a single character or an empty character but not a double quotation mark (`"`). <br>- The delimiter should not be identical to any character in the user data. If the delimiter appears in the user data, KWDB will use the enclosed character to enclose the delimiter to prevent export failures. <br>- If you specify a delimiter when exporting data, you must use the same delimiter when importing the data. Inconsistent delimiters for export and import will cause an import failure. |
| `chunk_rows` | Optional. The number of rows to be converted and written to a single `.csv` file. If the number of rows in the specified table exceeds this configured limit, KWDB will produce multiple files based on the configured limit. The produced files are named in the format `<node_id>.<file_id>.csv`. Both the default value and the maximum value are set to `100000`. When set to `0`, there is no limit on the number of rows. |
| `enclosed` | Optional. The character that encloses columns within each row. By default, it is set to the double quotation mark (`"`). KWDB also supports using the single quotation mark (`'`). <br>- When using the single quotation mark (`'`), the format is `"'"`. <br>- When using the double quotation mark (`"`), the format is `'"'`. <br> The enclosed character cannot be identical to the delimiter. |
| `escaped` | Optional. The character that causes one or more following characters to be interpreted differently. By default, it is set to the double quotation mark (`"`). KWDB also supports using the backslash (`\`). <br> The escape character cannot be identical to the delimiter.|
| `nullas` | Optional. The string used to represent `NULL` values. By default, no content is displayed. KWDB supports setting it to `NULL`, `null`, `Null`, or `\N`.|
| `comment` | Optional. Specifies whether to export comments on databases. By default, KWDB does not export comments. <br> - If the specified databases have comments, you can export the files with these comments using the `WITH comment` parameter. Otherwise, the exported files do not contain any comments. <br> - If the specified databases do not have any comments, KWDB returns an error when you export the files using the `WITH comment` parameter: `DATABASE or TABLE or COLUMN without COMMENTS cannot be used 'WITH COMMENT'`.|
| `charset` | Optional. Specifies the character set encoding for the database to export. By default, it is set to `utf8`. Available options are `gbk`, `gb18030`, or `utf8`. |
| `privileges` | Optional. Exports the privilege information of non-system users for the specified databases. With this parameter, KWDB reads the `system.information_schema.table_privileges` table and exports related privileges to the `meta.sql` file. |

### Examples

These examples assume that you have created a time-series database (`ts_db`) and a relational database (`rdb`).

- Basic Export

  - Export both the user data and metadata of the time-series database to a local node.

    ```sql
    -- Export in CSV format
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db;

    -- Export in SQL format
    EXPORT INTO SQL "nodelocal://1/ts_db" FROM DATABASE ts_db;
    ```

  - Export both the user data and metadata of the relational database to a local node.

    ```sql
    -- Export in CSV format
    EXPORT INTO CSV "nodelocal://1/rdb" FROM DATABASE rdb;

    -- Export in SQL format
    EXPORT INTO SQL "nodelocal://1/rdb" FROM DATABASE rdb;
    ```

  - Export both the user data and metadata of the time-series database to a specified server.

    ```sql
    -- Export in CSV format
    EXPORT INTO CSV "http://172.18.10.1:8090/ts_db" FROM DATABASE ts_db;
    
    -- Export in SQL format
    EXPORT INTO SQL "http://172.18.10.1:8090/ts_db" FROM DATABASE ts_db;
    ```

- Specify Export Content

  - Export the user data of the time-series database to a local node.

    ```sql
    -- Export in CSV format
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH data_only;

    -- Export in SQL format
    EXPORT INTO SQL "nodelocal://1/ts_db" FROM DATABASE ts_db WITH data_only;
    ```

  - Export the metadata of the time-series database to a local node.

    ```sql
    -- Export in CSV format
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH meta_only;

    -- Export in SQL format
    EXPORT INTO SQL "nodelocal://1/ts_db" FROM DATABASE ts_db WITH meta_only;
    ```

  - Export data with comments.

    ```sql
    -- Export in CSV format
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH COMMENT;

    -- Export in SQL format
    EXPORT INTO SQL "nodelocal://1/ts_db" FROM DATABASE ts_db WITH COMMENT;
    ```

  - Limit the number of rows to `1000`.

    ```sql
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH chunk_rows = '1000';
    ```

- Formatting Options

  - Set the delimiter to slash (`/`).

    ```sql
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH DELIMITER = '/';
    ```

  - Set the enclosed character to single quotation mark (`'`).

    ```sql
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH enclosed = "'";
    ```

  - Set the escape character to backslash (`\`).

    ```sql
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH escaped = '\';
    ```

  - Set the NULL representation to `NULL`.

    ```sql
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH NULLAS = 'NULL';
    ```

  - Set the character set encoding to `GBK`.

    ```sql
    EXPORT INTO CSV "nodelocal://1/ts_db" FROM DATABASE ts_db WITH charset = 'GBK';
    ```

## Export User Information

KWDB supports exporting all non-system user information in the current cluster, providing two export methods:

- **SQL statement export** (recommended): Generates a `users.sql` file that can be imported back into KWDB database.
- **CSV file export**: Generates a `.csv` file for easy data viewing and analysis.

::: warning Note
- The exported user information does not include passwords. When importing the user information, you need to reset the passwords for users.
- CSV files currently do not support re-importing into KWDB database.
:::

### Privileges

The user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

### Syntax

- Export in SQL format

  ```sql
  EXPORT USERS TO SQL "<file_path>";
  ```

- Export in CSV format

  ```sql
  EXPORT INTO CSV "<file_path>" FROM TABLE system.users;
  ```

### Parameters

| Parameter                 | Description |
|----------------------|----------------------------|
| `file_path`          | Specifies the URL of the file location where exported data will be stored, supporting `nodelocal://<node_id>/<dir>` and `<server_ip>/<dir>` formats. <br><br> `nodelocal://<node_id>/<dir>`: Exports files to local nodes. <br> - `node_id`: The node ID. When there is only one node, it is set to `1`. <br> - `dir`: The name of the directory to store exported files. If the target directory does not exist, KWDB will create the directory under the path defined for saving data during KWDB installation. By default, KWDB saves data to `/var/lib/kaiwudb/extern/<folder_name>`. <br><br> `<server_ip>/<dir>`: Exports files to a specified server. <br> - `server_ip`: The IP address and port ID of the server, such as `http://172.18.0.1:8090`. <br> - `dir`: The name of the directory to store exported files. If the target directory does not exist, KWDB will create the directory. |

### Examples

- Export in SQL format

  This example exports all non-system user information in the current cluster to a local node.

  ```sql
  EXPORT USERS TO SQL "nodelocal://1/users";
  ```

  If you succeed, you should see an output similar to the following:

  ```sql
       queryname       | rows | node_id | file_num
  ---------------------+------+---------+-----------
         USERS         |    1 |     1   |        1
  (1 row)
  ```

- Export in CSV format

  This example exports user information to a CSV file on a local node.

  ```sql
  EXPORT INTO CSV "nodelocal://1/users" FROM TABLE system.users;
  ```

  If you succeed, you should see an output similar to the following:

  ```sql
            filename          | rows | node_id | file_num
  ----------------------------+------+---------+-----------
    TABLE system.public.users |   11 |       1 |        1
    meta.sql                  |    1 |       1 |        1
  (2 rows)
  ```

## Export Cluster Settings

KWDB supports exporting the current cluster settings, providing two export methods:

- **SQL statement export** (recommended): Generates a `clustersetting.sql` file that can be imported back into KWDB database.
- **CSV file export**: Generates a `.csv` file for easy data viewing and analysis.

::: warning Note
CSV files currently do not support re-importing into KWDB database.
:::

### Privileges

The user must be a member of the `admin` role. By default, the `root` user belongs to the `admin` role.

### Syntax

- Export in SQL format

  ```sql
  EXPORT CLUSTER SETTING TO SQL "<file_path>";
  ```

- Export in CSV format

  ```sql
  EXPORT INTO CSV "<file_path>" FROM TABLE system.settings;
  ```

### Parameters

| Parameter                 | Description |
|----------------------|---------------------------|
| `file_path`          | Specifies the URL of the file location where exported data will be stored, supporting `nodelocal://<node_id>/<dir>` and `<server_ip>/<dir>` formats. <br><br> `nodelocal://<node_id>/<dir>`: Exports files to local nodes. <br> - `node_id`: The node ID. When there is only one node, it is set to `1`. <br> - `dir`: The name of the directory to store exported files. If the target directory does not exist, KWDB will create the directory under the path defined for saving data during KWDB installation. By default, KWDB saves data to `/var/lib/kaiwudb/extern/<folder_name>`. <br><br> `<server_ip>/<dir>`: Exports files to a specified server. <br> - `server_ip`: The IP address and port ID of the server, such as `http://172.18.0.1:8090`. <br> - `dir`: The name of the directory to store exported files. If the target directory does not exist, KWDB will create the directory. |

### Examples

- Export in SQL format

  This example exports the current cluster settings to a local node.

  ```sql
  EXPORT CLUSTER SETTING TO SQL "nodelocal://1/settings";
  ```

  If you succeed, you should see an output similar to the following:

  ```sql
       queryname       | rows | node_id | file_num
  ---------------------+------+---------+-----------
    CLUSTER SETTING    |  215 |     1   |        1
  (1 row)
  ```

- Export in CSV format

  This example exports cluster settings to a CSV file on a local node.

  ```sql
  EXPORT INTO CSV "nodelocal://1/settings" FROM TABLE system.settings;
  ```

  If you succeed, you should see an output similar to the following:

  ```sql
              filename           | rows | node_id | file_num
  -------------------------------+------+---------+-----------
    TABLE system.public.settings |    5 |       1 |        1
    meta.sql                     |    1 |       1 |        1
  (2 rows)
  ```
