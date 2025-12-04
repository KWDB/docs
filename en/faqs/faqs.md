---
title: Frequently Asked Questions (FAQ)
id: faqs
---

# Frequently Asked Questions (FAQ)

## Deployment FAQ

### Operating System Compatibility

- **Issue Description**

  Deploying KWDB on Loongson 3C5000L or Zhaoxin KH-30000 operating systems.

- **Solution**

  KWDB has not yet been comprehensively tested and verified on Loongson 3C5000L and Zhaoxin KH-30000 operating systems. If you need to deploy on these platforms, please [contact](https://www.kaiwudb.com/support/) KWDB technical support for assistance with compilation, adaptation, and testing.

### Missing Dependencies

- **Issue Description**

  Installation of KWDB fails with a system error message.

- **Solution**

  You may not have installed the required dependencies. Check the relevant logs in the `kwdb_install/log` directory, then install the missing dependencies using the `apt install` command based on the log information.

  Log example:

  ```shell
  root@node:/home/admin/kwdb_install/log# cat 2024-08-28
  [INFO] 2024-08-28 09:35:57 start init directory /etc/kaiwudb/data/kaiwudb
  [INFO] 2024-08-28 09:35:57 init directory success
  [INFO] 2024-08-28 09:35:57 start install binaries and libraries to /usr/local/kaiwudb
  [ERROR] 2024-08-28 09:35:57 error: Failed dependencies: squashfs-tools is needed by kaiwudb-server-2.0.3.2-kylin.kyl0.aarch64
  ```

## Storage FAQ

### Storage Space Not Released After Table Deletion

- **Issue Description**

  After deleting a table, the storage space is not immediately released.

- **Solution**

  In KWDB 2.x, when a table deletion operation is executed while other threads are still using the table, the system will not immediately delete the table. Instead, it waits for all threads to complete their operations before proceeding with deletion. The system performs a check every 5 minutes to determine whether the table can be safely deleted. In extreme cases where a thread holds the table for an extended period, storage space may not be released. If this occurs, manually delete the related data to free up storage space.

## SQL FAQ

### Data Writing

#### Insufficient Space

- **Issue Description**

  When writing data to the database, the write operation fails with an error message `could not PutData`. The log shows `resize file failed` and `No space left on device`.

- **Solution**

  This may occur because there are too many columns being written, reaching the handle limit, or the database has insufficient available disk space. This can be resolved by increasing the file descriptor limit.

  ::: warning Note

  - This setting only applies to bare metal deployment.
  - This configuration is applied at the node level. To modify the configuration for the entire cluster, log in to each node and apply the configuration accordingly.
  :::

  1. Navigate to the `/etc/systemd/system` directory and open the `kaiwudb.service` file.

  2. Add `LimitNOFILE=1048576` to the `[Service]` section to increase the maximum number of file descriptors a single process can open.

     ```yaml
     ...
     [Service]
     ...
     LimitNOFILE=1048576
     ...
     ```

  3. After saving the `kaiwudb.service` file, reload the configuration.
  
     ```shell
     systemctl daemon-reload
     ```

  4. Verify the modification is effective:

     ```shell
     systemctl show kaiwudb | grep LimitNOFILE
     ```

#### Table Creation Error

- **Issue Description**

  When running KWDB in a container on CentOS, time-series databases can be created successfully, but an error occurs when creating time-series tables: `Error: have been trying 30s, timed out of AdminReplicaVoterStatusConsistent`. The log shows: `Err :connection error: desc = "transport: Error while dialing dial tcp 100.153.0.246:26257: connect: connection refused`.

- **Solution**

  This may occur when the container cannot access the host's IP address, causing table creation to fail. Modify the firewall configuration to allow the container network segment to access the host.

  Example:

  ```shell
  firewall-cmd --zone=public --add-rich-rule='rule family="ipv4" source address="172.18.0.4/24" port protocol="tcp" port="22" accept' --permanent
  ```

#### Multi-row Insert Failure

- **Issue Description**

  When using JDBC with PREPARE INSERT statements to write data to a table containing several thousand columns, batch inserting 10 rows succeeds, but batch inserting 20 rows fails.

- **Solution**

  The length of the batch insert SQL statement exceeds the length limit specified by the PostgreSQL protocol. This can be resolved by:

  - **Reducing SQL statement length**: Decrease the number of rows or columns in a single batch insert.
  - **Avoiding PREPARE statements**: Execute INSERT statements directly without using the pre-compiled PREPARE statements.

### Data Querying

#### Lifecycle Settings

- **Issue Description**

  A time-series table was created with a lifecycle of `1` minute and data was written to it. However, after the table's lifecycle expires, the table data can still be queried.

  ```sql
  show create temp;
    table_name |              create_statement
  -------------+----------------------------------------------
    temp       | CREATE TABLE temp (
              |     ts TIMESTAMPTZ NOT NULL,
              |     c1 INT4 NULL
              | ) TAGS (
              |     tag1 INT4 NOT NULL ) PRIMARY TAGS(tag1)
              |      retentions 1m
  (1 row)

  select * from temp;
                ts               | c1 | tag1
  --------------------------------+----+-------
    2024-05-27 03:06:14.465+00:00 |  3 |    1
    2024-05-27 03:06:39.188+00:00 |  1 |    1
    2024-05-27 03:06:46.104+00:00 |  2 |    1
    2024-05-27 03:10:55.501+00:00 |  3 |    1
  (4 rows)
  ```

- **Solution**

  In KWDB 2.x, the lifecycle setting for time-series tables only applies to completed partitions, not the current active partition. By default, the system creates a new partition every 10 days. Therefore, even after the table's lifecycle period has elapsed, data in the current partition remains queryable until that partition is closed and a new one is created.

#### Insufficient Memory

- **Issue Description**

  When executing complex sorting queries on large datasets in a standalone deployment of KWDB, an insufficient memory error is reported.

- **Solution**

  The sorting operator may consume excessive memory in specific scenarios, causing errors after the memory pool is exhausted. This can be resolved by setting the startup flag `buffer-pool-size` to increase the buffer pool size.

  **Bare-Metal Deployment:**

  1. Stop the KWDB service.

     ```shell
     systemctl stop kaiwudb
     ```

  2. Navigate to the `/etc/kaiwudb/script` directory, open the `kaiwudb_env` file, and add the startup flag `buffer-pool-size`.

     ```yaml
     KAIWUDB_START_ARG="--buffer-pool-size=32657"
     ```

  3. Save the `kaiwudb_env` file and reload the configuration.

     ```shell
     systemctl daemon-reload
     ```

  4. Restart the KWDB service.

     ```shell
     systemctl restart kaiwudb
     ```

  **Container Deployment:**

  1. Navigate to the `/etc/kaiwudb/script` directory, stop and remove the KWDB container.

     ```bash
     docker-compose down
     ```

  2. Open the `docker-compose.yml` file and add the startup flag `buffer-pool-size`.

     ```yaml
     ...
         command: 
           - /bin/bash
           - -c
           - |
             /kaiwudb/bin/kwbase start-single-node --certs-dir=/kaiwudb/certs --listen-addr=0.0.0.0:26257 --advertise-addr=your-host-ip:port --store=/kaiwudb/deploy/kaiwudb-container --buffer-pool-size=32657
     ```

  3. Save the configuration, recreate and start the KWDB container.

     ```shell
     systemctl start kaiwudb
     ```

## Performance Tuning

### Write Optimization

#### Mass Data Write Optimization

- **Issue Description**

  When writing large amounts of data to KWDB using SQL statements, the write speed is slow.

- **Solution**

  You can adjust cluster settings or disable certain features that may affect performance based on your business scenarios to improve data write speed:

  1. Increase the processor's available memory limit to reduce reliance on temporary storage. The default value is 64 MiB; it is recommended to set it to 1/8 of physical memory to improve processing efficiency.

     Example:

     ```sql
     SET CLUSTER SETTING sql.distsql.temp_storage.workmem = '32768Mib';
     ```

  2. Enable SQL pushdown to reduce data processing overhead.

     ```sql
     SET CLUSTER SETTING sql.all_push_down.enabled = TRUE;
     ```

  3. Enable short-circuit optimization to reduce unnecessary operation steps.

     ```sql
     SET CLUSTER SETTING sql.pg_encode_short_circuit.enabled = TRUE;
     ```

  4. Disable automatic time-series data statistics collection. Note: After disabling this feature, monitoring data will not be available. This is suitable for scenarios requiring high performance with low reliance on monitoring data.

     ```sql
     SET CLUSTER SETTING sql.stats.ts_automatic_collection.enabled = FALSE;
     ```

  5. (KWDB 2.x) Disable data compression to reduce computational overhead during writes. This is suitable for scenarios not sensitive to space usage.

     ```sql
     ALTER SCHEDULE scheduled_table_compress F Recurring '0 0 1 1 ？2099';
     ```

  6. Disable lifecycle management to avoid periodic table cleanup operations. This is suitable for scenarios requiring long-term data retention and high write performance.

     ```sql
     ALTER SCHEDULE scheduled_table_retention Recurring '0 0 1 1 ? 2099';
     ```

  7. Disable WAL. Note: Disabling WAL will affect data recovery after a crash and is suitable only for scenarios with low data consistency requirements.

     1. Disable WAL.

        ```sql
        SET CLUSTER SETTING ts.wal.flush_interval = -1s;
        ```

     2. Restart the KWDB service.

        ```shell
        systemctl restart kaiwudb
        ```

#### Ultra-Wide Table Write Optimization

- **Issue Description**

  For ultra-wide tables (tables with more than 500 columns), when batch writing more than 500 records at a time or writing more than 4MB of data in a single write operation, write performance is poor.

- **Solution**

  You can configure the `KWBASE_RAFT_ELECTION_TIMEOUT_TICKS` environment variable on each node by following these steps:

  **Bare-Metal Deployment:**

  1. Stop the KWDB service.

     ```shell
     systemctl stop kaiwudb
     ```

  2. Navigate to the `/etc/kaiwudb/script` directory, edit the `kaiwudb_env` configuration file, and add the `KWBASE_RAFT_ELECTION_TIMEOUT_TICKS` environment variable.

     ```plain
     KAIWUDB_START_ARG=""
     KWBASE_RAFT_ELECTION_TIMEOUT_TICKS=100
     ```

  3. Save the file and reload the configuration.

     ```shell
     systemctl daemon-reload
     ```

  4. Restart the KWDB service.

     ```shell
     systemctl restart kaiwudb
     ```

  **Container Deployment:**

  1. In the `/etc/kaiwudb/script` directory, stop and remove the KWDB container.

     ```shell
     docker-compose down
     ```

  2. Open the `docker-compose.yml` file and add the `KWBASE_RAFT_ELECTION_TIMEOUT_TICKS` environment variable.

     ```plain
     ...
         environment:
           - LD_LIBRARY_PATH=/kaiwudb/lib
           - KWBASE_RAFT_ELECTION_TIMEOUT_TICKS=100
     ...
     ```

  3. Save the configuration, recreate and start the KWDB container.

     ```shell
     systemctl start kaiwudb
     ```

### Query Optimization

- **Issue Description**

  Retrieving all tag values from a time-series table using SQL statements is slow.

- **Solution**

  Query performance can be optimized by providing specific hints to the database query optimizer using the following SQL statement:

  ```sql
  SELECT /*+ STMT_HINT(ACCESS_HINT(TAG_ONLY,<table_name>)) */ <tag_name> FROM <table_name> GROUP BY <tag_name>;
  ```

  Parameter description:

  - `/*+ STMT_HINT(ACCESS_HINT(TAG_ONLY, <table_name>)) */`: Query optimization hint with the following parameters:
    - `ACCESS_HINT`: Specifies the table access method.
    - `TAG_ONLY`: Instructs the query to access only tag data.
    - `table_name`: The name of the target table.
  - `tag_name`: The name of the target tag.

  Example:

  ```sql
  > SELECT /*+ STMT_HINT(ACCESS_HINT(TAG_ONLY,t1)) */ tag1 FROM t1 GROUP BY tag1;
    tag1
  ------
     3
     1
     2
     5
     6
     4
  (6 rows)
  ```

## Ecosystem FAQ

### MyBatis and MyBatis-Plus

#### `BigInteger` Type Write Failure

- **Issue Description**

  Inserting `BigInteger` type data into an `INT8` column of a time-series table through Spring and MyBatis returns an `unsupported input type *tree.DDecimal` error.

- **Solution**

  When writing data via JDBC, Java `BigInteger` type data is automatically converted to `BigDecimal` type. In KWDB, `BigDecimal` maps to the `DECIMAL` and `NUMERIC` data types, which are not supported by time-series tables, resulting in this error. To resolve this issue, change the Java data type from `BigInteger` to `Integer`.

#### `NCHAR` Type Query Error

- **Issue Description**

  Querying an `NCHAR` column through Spring and MyBatis returns a `SQLSTATE(0A000)` error, indicating that the `getNString` method is not implemented.

- **Solution**

  JDBC version 2.0.3 does not support the `getNString` method, causing errors when querying N`CHAR` columns. To resolve this issue, either create a custom MyBatis type handler that uses `getString` to retrieve data, or upgrade to JDBC version 2.0.4 or later.

#### Pagination Query Error

- **Issue Description**

  When using MyBatis-Plus to connect to KWDB and executing pagination queries, the system reports an error: `Error querying database. com.baomidou.mybatisplus.core.exceptions.MybatisPlusException: other database not supported`.

- **Solution**

  The MyBatis-Plus pagination plugin fails during database type validation. To resolve this, explicitly declare the `InnerInterceptor` for `DbType.POSTGRE_SQL`.

  Steps:

  1. Create a MyBatis-Plus configuration class in the application code (e.g., `MybatisPlusConfig`).

  2. Add pagination configuration.

     ```java
     @Configuration
     public class MybatisPlusConfig {
       @Bean
       public MybatisPlusInterceptor mybatisPlusInterceptor() {
         MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
         interceptor.addInnerInterceptor(new PaginationInnerInterceptor(DbType.POSTGRE_SQL));
         return interceptor;
       }
     }
     ```

#### Time-Series Mode Does Not Support Transactions

- **Issue Description**

  When using MyBatis-Plus native interfaces to connect to the database and calling interface methods, the database returns an error: `ERROR: explicit transaction is not supported in TS mode`.  

- **Solution**

  Override the MyBatis-Plus interface method implementation and apply the `@Transactional(propagation = Propagation.NOT_SUPPORTED)` annotation to disable transaction management for that method.
  
  Example:

  ```java
  @Service
  public class TimeSeriesServiceImpl extends ServiceImpl<TimeSeriesMapper, TimeSeriesData> implements TimeSeriesService {
    @Override
    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public boolean saveBatch(Collection<TimeSeriesData> entityList) {
      return super.saveBatch(entityList);
    }
  }
  ```
  