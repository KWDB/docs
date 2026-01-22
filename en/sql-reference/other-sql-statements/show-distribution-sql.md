---
title: Storage and Compression
id: show-distribution-sql
---

# Storage and Compression

## Viewing Storage and Compression Information

The `SHOW DISTRIBUTION` statement displays the storage space and compression ratio of a specified time-series database or time-series table.

::: warning Note
The compression ratio is a rough calculation and may differ from the actual compression performance. When calculating the compression ratio, the uncompressed data length is calculated based on the column width specified when creating the table. Therefore, for variable-length columns (such as `VARCHAR` type), if the defined column width is much larger than the actual written data length (for example, defining `VARCHAR(1000)` but only writing a few characters), the compression ratio will be overestimated.
:::

### Privileges

None

### Syntax

![](../../../static/sql-reference/show-distribution.png)

### Parameters

| Parameter | Description |
| --- | --- |
| `db_name` | The name of the time-series database to view. |
| `table_name` | The name of the time-series table to view. Supports specifying tables in other time-series databases using the `db_name.table_name` format. When no database is specified, it refers to tables in the current database. |

### Return Fields

**Return fields when viewing a database:**

| Field | Description |
| --- | --- |
| `node` | Node identifier. |
| `blocks_num` | Number of data blocks. |
| `blocks_size` | Disk space used. |
| `avg_size` | Average data block size. |
| `compression_ratio` | Roughly calculated compression ratio. |

**Return fields when viewing a table:**

| Field | Description |
| --- | --- |
| `node_id` | Node identifier. |
| `level` | Compression level, including `last segment` (latest segment), `entity segment` (entity segment), and `total` (total). |
| `blocks_num` | Number of data blocks. |
| `blocks_size` | Disk space used. |
| `avg_size` | Average data block size. |
| `compression_ratio` | Roughly calculated compression ratio. |

### Examples

- View storage and compression information for a specified database.

    ```sql
    SHOW DISTRIBUTION FROM DATABASE iot;
    ```

- View storage and compression information for a specified table.

    ```sql
    SHOW DISTRIBUTION FROM TABLE sensors;
    ```