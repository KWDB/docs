---
title: Data Publication
id: data-pub
---

# Data Publication

KWDB provides out-of-the-box data publication capabilities. It allows publishing data of specified objects within a database instance. Subscribers can subscribe to the data via the subscription feature of KaiwuDB Enterprise Edition to realize real-time application or synchronization of data.

## Limitations

- A table that has been used as a subscription target cannot be set as a publication object, nor can it be republished. Sequential or bidirectional publication and subscription links are prohibited.
- DDL statements of source tables are not supported for publication.
- Publication is not available for relational databases, tables, and views.
- No DDL operations are permitted on a target database or time-series table with active publication tasks. When publishing an entire database or multiple time-series tables, column specification and filter conditions are not supported, nor can publication and subscription objects be modified. Filter conditions cannot include aggregate functions, type conversion, collation rules, references to system columns or non-immutable built-in functions. Built-in data deduplication rules are not supported during data replication; data deduplication needs to be implemented on the application side.
- The publisher and subscriber run asynchronously. One publication task can only have one active subscription. Ensure no running subscription exists before starting a new subscription for the corresponding publication. Data replicated during publication and subscription can be captured again after being written to the subscriber instance.
- In scenarios with parallel data synchronization across multiple nodes, concurrent transmission may cause data to arrive at the target out of the original order. It is not recommended to run order-dependent synchronization operations concurrently. If such operations are required, complete them within a single session.
- In a clustered high-availability environment, table operations related to CDC on newly expanded nodes will be blocked before the nodes establish connections with business services.

## Main Features

The table below lists the supported features for data publication and subscription in KWDB.

|Feature | Description |
| --- | --- |
|Publication Objects                | - Single time-series database: Supports publishing and subscribing all tables in a single time-series database. Column selection is not allowed. Table structures must be consistent between the publisher and subscriber. Tables cannot be added or removed from the database after the subscription is established.<br >
- Single time-series table: Supports publishing and subscribing all or partial columns (including tag columns and data columns). If partial columns are selected for publication, the subscriber table must contain all specified columns.<br >
- Multiple time-series tables: Supports publishing and subscribing all columns only. Column selection is not allowed. Table structures must be consistent between the publisher and subscriber.<br >
- Only time-series tables can be used as subscription targets. Dropping tables or altering table structures on the subscriber side is prohibited. |
| Data Sources for Publication	    | **Real-time data**: Data written, deleted or updated via `INSERT`, `DELETE` and `UPDATE` statements. No publication will be triggered if a DELETE or UPDATE operation affects zero rows.<br >**Historical data**<br >
- Out-of-order data inserted into the database.<br >- Existing data in the database, which will be published in batches after subscription is enabled.<br >- Data imported via `IMPORT` and `INSERT INTO ... SELECT` statements.<br >
**Note**<br > Database-level import is not supported for publication. | 
| Publication Modes	                | - Batch synchronization: Data is synchronized at a fixed interval (currently set to 2 seconds).<br >- Near real-time replication: Qualified data is published immediately.| 
| Filter Conditions for Publication |- Filtering based on timestamp columns of time-series tables is supported.<br >- Filtering based on Primary Tag columns, regular Tag columns and data columns is supported.<br >- Filter conditions are not allowed when publishing an entire time-series database or multiple time-series tables.|
| Supported SQL Operations	        | -  `INSERT`<br >- `DELETE`: Synchronizes delete operations on data columns and regular Tag columns. Deletions executed while the publication task is running will be synchronized to the subscriber in real time. Deletions made during task suspension will also be synchronized after resumption to ensure data consistency.<br >
-  `UPDATE `： Synchronizes update operations on data columns and regular Tag columns. If deduplication policies are configured on the subscriber side for data columns, deduplication and updates will be performed there. Updates executed while the task is running will be synchronized in real time, and updates made during suspension will be synchronized after resumption to ensure data consistency.<br >
**Note:**<br >Currently, data deletion and Tag value update are only supported based on Primary Tag.| 
| Publication Task Management	    | - Supports starting and stopping publication services.<br >
- Supports resuming transmission from the breakpoint of untransmitted data when restarting a publication task.<br >
- Allows viewing running publication tasks, including task name, creation time, creator, current status, start time, end time, failure time and failure causes.<br >
- Supports deleting specified publication tasks. | 
| Resumable Transmission		    | Resumable transmission is supported. If data replication stops manually or unexpectedly, the system will continue replicating untransmitted data after restart or recovery.<br >Note: Resumable transmission synchronizes the final state of source data rather than the complete sequence of operations. | 
| Applicable Scenarios		        | - Scale-in, scale-out, shutdown and upgrade in distributed systems.<br >- Cloud-edge deployment scenarios.| 
| High Availability	                | Node exception handling for publication clusters: If a node in the active publication cluster goes down, restarts or scales, the publication service runs normally when the subscriber connects to a healthy node in the cluster. If the subscriber is connected to a faulty node, it will automatically retry to discover and reconnect to the publisher. If the connection is restored within the retry period, the publication task will resume automatically and continue replicating data based on the recorded replication checkpoint. | 