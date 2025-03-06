---
title: 事务
id: transactions-sql
---


# 事务

::: warning 说明
目前，时序数据不支持该语句。
:::

在执行 SQL 语句的时候，某些业务要求一系列操作必须全部执行，而不能仅执行一部分。这种以全有或全无的方式执行的一系列数据库操作的功能，被称为事务。事务可以确保该事务范围内的所有操作都可以全部成功或者全部失败。如果事务失败，那么效果就和没有执行这些 SQL 语句一样，不会对数据库数据有任何改动。

因此，事务具有 ACID 这四个特性：

- A（Atomicity，原子性）：将所有 SQL 语句作为原子工作单元执行，要么全部执行，要么全部不执行。
- C（Consistency，一致性）：事务完成后，所有数据的状态保持一致。
- I（Isolation，隔离性）：如果并发执行多个事务，每个事务作出的修改必须与其他事务隔离。
- D（Durability，持久性）：事务完成后，对数据库数据的修改被持久化存储。

事务分为隐式事务和显式事务，都可以保证数据的一致性和完整性。

- 隐式事务是指在不使用 `BEGIN`、`COMMIT` 等语句的情况下，KWDB 自动为每个操作创建一个事务，并在操作完成后自动提交或回滚事务。隐式事务可以提供更简洁的代码和更高的开发效率，适用于单个操作，如果操作成功，则自动提交事务，如果操作失败，则自动回滚事务。
- 显式事务是指在应用程序中明确指定事务的开始和结束，使用 `BEGIN`、`COMMIT` 等语句来控制事务的执行。显式事务可以提供更精细的控制，适用于需要进行一组操作，并在操作完成后手动提交或回滚事务的场景。

## 隔离级别

对于两个并发执行的事务，如果涉及到操作同一条记录的时候，可能会发生问题。因为并发操作会带来数据的不一致性，包括脏读、不可重复读、幻读等。隔离是 ACID 事务的一个要素，它决定了如何控制并发性，并最终保证一致性。KWDB 提供三种事务隔离级别：

- 串行化（Serializable）：Serializable 隔离是最高的隔离级别，保证了即使事务是并行执行的，其结果也与它们一次执行一个事务时的结果相同，没有任何并发性。这可以防止较弱隔离级别所允许的所有异常，从而确保数据的正确性。默认情况下，KWDB 提供 Serializable 隔离。
- 提交读（Read Committed，RC）：在 RC 隔离级别下，事务会读取到其他事务已提交的数据，但不完全保证事务操作的可序列化。事务并发时允许潜在的事务异象发生，包括不可重复读、幻读、丢失更新、写偏序，从而换取最小化事务中止、重试和阻塞，并且不会返回需要客户端处理的序列化错误。RC 隔离级别适用于以下场景：
  - 应用程序需要在保持高工作负载并发性的同时，尽量减少事务重试，并且可以容忍潜在的并发异常。在高并发情况下，可预测的查询性能比保证事务的可序列化性更有价值。
  - 将一个基于 RC 隔离级别构建的应用程序迁移到 KWDB，并且无法将应用程序修改为使用 Serializable 隔离级别。
- 可重复读（Repeatable Read，RR）：RR 隔离保证了在同一事务内多次读取同一数据时，结果是一致的。为了实现这一点，当事务执行查询时，会锁定查询的列或行，确保其他事务在此期间不能修改这些数据。RR 隔离解决了脏读 、不可重复读的问题。

默认情况下，KWDB 采用 Serializable 隔离级别。

### 配置隔离级别

KWDB 支持配置集群级、会话级、以及事务级的隔离级别，其中事务级的隔离级别优先级最高，集群级的隔离级别优先级最低。

#### 配置集群级隔离级别

集群级的隔离级别设置仅对后续启动的连接生效。有关详细信息，参见[集群配置](../../db-operation/cluster-settings-config.md)。设置完成后，用户可以使用 `SHOW cluster setting sql.txn.cluster_transaction_isolation` 语句查看集群的隔离级别设置。

```sql
SET CLUSTER SETTING sql.txn.cluster_transaction_isolation = <level>;
```

`level` 参数取值：

- `serializable`：默认值，串行化隔离级别。
- `read committed`：提交读隔离级别
- `repeatable read`：可重复读隔离级别

#### 配置会话级隔离级别

会话级隔离级别设置只对当前连接生效。如果启动会话时未指定隔离级别，则继承集群级隔离级别。用户可以使用以下命令更改会话的隔离级别。更新完成后，用户可以使用 `SHOW default_transaction_isolation` 语句查看当前会话的隔离级别设置。

```sql
SET default_transaction_isolation = <level>;
```

`level` 参数取值：

- `serializable`：默认值，串行化隔离级别。
- `read committed`：提交读隔离级别
- `repeatable read`：可重复读隔离级别

#### 配置事务级隔离级别

如果启动事务时未指定隔离级别，则继承会话级隔离级别设置。用户可以使用以下命令更改事务的隔离级别。更新完成后，用户可以使用 SHOW transaction isolation level 语句查看显式事务内的隔离级别。

::: warning 说明
显式事务中只能在没有进行 kv 操作时（即读写操作）更改事务的隔离级别。
:::

- 使用 `BEGIN TRANSACTION ISOLATION LEVEL` 语句

  ```sql
  BEGIN TRANSACTION ISOLATION LEVEL <iso_level>;
  ```

  `iso_level` 参数取值：

  - `SERIALIZABLE`：默认值，串行化隔离级别。
  - `READ COMMITTED`：提交读隔离级别
  - `REPEATABLE READ`：可重复读隔离级别

- 使用 `SET TRANSACTION ISOLATION LEVEL` 语句

  ```sql
  BEGIN; ---开启事务
  SET TRANSACTION ISOLATION LEVEL <iso_level>; ---在显式事务内执行
  ```

  `iso_level` 参数取值：

  - `SERIALIZABLE`：默认值，串行化隔离级别。
  - `READ COMMITTED`：提交读隔离级别
  - `REPEATABLE READ`：可重复读隔离级别

- 使用 `transaction_isolation` 会话变量

  ```sql
  BEGIN; ---开启事务
  SET transaction_isolation = <level>;  ---在显式事务内执行
  ```

  `level` 参数取值：

  - `serializable`：默认值，串行化隔离级别。
  - `read committed`：提交读隔离级别
  - `repeatable read`：可重复读隔离级别

- 使用 `SET SESSION TRANSACTION ISOLATION LEVEL` 语句

  ```sql
  BEGIN; ---开启事务
  SET SESSION TRANSACTION ISOLATION LEVEL <iso_level>; ---在显式事务内执行
  ```

  `level` 参数取值：

  - `serializable`：默认值，串行化隔离级别。
  - `read committed`：提交读隔离级别
  - `repeatable read`：可重复读隔离级别

## SQL 语句

### 启动事务

`BEGIN` 语句用于启动事务，该事务将以全有或全无的方式执行包含的所有语句。在 KWDB 中，`BEGIN` 语句的别名包括：

- `BEGIN TRANSACTION`
- `START TRANSACTION`

#### 所需权限

启动事务不需要任何权限。但是，事务中的每个语句都需要相应的权限。

#### 语法格式

![](../../static/sql-reference/begintransaction.png)

#### 参数说明

| 参数 | 说明 |
| --- | --- |
| `ISOLATION LEVEL` | 事务的隔离级别，支持以下取值：<br >- 串行化（Serializable）：Serializable 隔离是最高的隔离级别，保证了即使事务是并行执行的，其结果也与它们一次执行一个事务时的结果相同，没有任何并发性。<br >- 提交读（Read Committed，RC）：在 RC 隔离级别下，事务会读取到其他事务已提交的数据，但不完全保证事务操作的可序列化。<br >- 可重复读（Repeatable Read，RR）：RR 隔离保证了在同一事务内多次读取同一数据时，结果是一致的。<br >默认情况下，事务的隔离级别为 Serializable。|
| `PRIORITY` | 事务的优先级。默认情况下，事务的优先级为 `NORMAL`。用户可以根据需要将事务的优先级设置为 `LOW` 或 `HIGH`。优先级越高的事务，重试的几率越低。|
| `READ` | 事务访问模式，支持 `READ ONLY` 或 `READ WRITE` 访问模式。默认模式为 `READ WRITE`。用户可以通过修改会话变量 `transaction_read_only` 设置访问模式。|
| `AS OF SYSTEM TIME` |  对截至指定时间的数据库内容执行事务。事务访问模式设置为 `READ ONLY` 时才能使用 `AS OF SYSTEM TIME` 子句。如果事务包含任何写操作，或者事务访问模式为 `READ WRITE`，系统将返回错误。|

#### 语法示例

以下示例假设已经创建 `accounts`、`orders`、`customers` 表并写入相关数据。

- 采用默认配置启动事务。

    默认情况下，事务采用 `SERIALIZABLE` 隔离级别和 `NORMAL` 优先级。

    ```sql
    -- 1. 启动事务。

    BEGIN;
    Now adding input for a multi-line SQL transaction client-side (smart_prompt enabled).
    Press Enter two times to send the SQL text collected so far to the server, or Ctrl+C to cancel.
    You can also use \show to display the statements entered so far.

    -- 2. 创建保存点 foo。

    SAVEPOINT foo;

    -- 3. 更新 accounts 表。

    UPDATE accounts SET balance = 5000.0 WHERE id = 2;

    -- 4. 向 accounts 表中写入数据。

    INSERT INTO accounts (id, balance) VALUES (9, DEFAULT);

    -- 5. 提交事务。
    COMMIT;
    COMMIT
    ```

- 启动事务，并将事务的隔离级别设置为 `read committed`。

    ::: warning 说明
    用户也可以使用 `SET TRANSACTION` 语句设置事务的隔离级别。有关详细信息，参见 [设置事务](#设置事务)。
    :::

    ```sql
    -- 1. 启动事务。
    BEGIN TRANSACTION ISOLATION LEVEL read committed;

    -- 2. 提交事务。
    COMMIT;
    COMMIT
    ```

- 启动事务，并将事务优先级设置为 `HIGH`。

    ::: warning 说明
    用户也可以使用 `SET TRANSACTION` 语句设置事务的优先级。有关详细信息，参见 [设置事务](#设置事务)。
    :::

    ```sql
    -- 1. 启动事务。
    BEGIN PRIORITY HIGH;
    Now adding input for a multi-line SQL transaction client-side (smart_prompt enabled).
    Press Enter two times to send the SQL text collected so far to the server, or Ctrl+C to cancel.
    You can also use \show to display the statements entered so far.

    -- 2. 提交事务。
    COMMIT;
    COMMIT
    ```

- 启动事务，并使用 `AS OF SYSTEM TIME` 选项设置使用截止到指定时间的数据库内容执行事务。

    ::: warning 说明
    用户也可以使用 `SET TRANSACTION` 语句设置事务的优先级。有关详细信息，参见 [设置事务](#设置事务)。
    :::

    ```sql
    -- 1. 启动事务。

    BEGIN AS OF SYSTEM TIME '2023-04-18 10:00:00.0+00:00';
    Now adding input for a multi-line SQL transaction client-side (smart_prompt enabled).
    Press Enter two times to send the SQL text collected so far to the server, or Ctrl+C to cancel.
    You can also use \show to display the statements entered so far.

    -- 2. 提交事务。
    COMMIT;
    COMMIT
    ```

- 使用自动重试开始事务。

    如果事务中包括 `BEGIN` 和 `COMMIT` 操作，KWDB 支持自动重试批处理所有事务操作。批处理由驱动程序或客户端的行为控制。这意味着 KWDB 一次接收所有语句，而不是分次接收。如果任一语句没有执行成功，用户无需更改任何语句的值。KWDB 会自动重试事务，直到所有语句都执行成功。
    从 KWDB 的角度来看，批量发送的事务执行过程如下：

    ```sql
    -- 1. 启动事务。

    BEGIN;
    Now adding input for a multi-line SQL transaction client-side (smart_prompt enabled).
    Press Enter two times to send the SQL text collected so far to the server, or Ctrl+C to cancel.
    You can also use \show to display the statements entered so far.

    -- 2. 删除 customers 表中 id 取值为 1 的数据。
    DELETE FROM customers WHERE id = 1;
    DELETE 

    -- 3. 删除 orders 表中 customer 取值为 1 的数据。

    DELETE orders WHERE customer = 1;
    DELETE 1

    -- 4. 提交事务。

    COMMIT;
    ```

    在应用程序的代码中，批处理事务通常一次发送多个语句。如下示例将批量发送多个语句，并自动重试。

    ```go
    db.Exec(
      "BEGIN;

      DELETE FROM customers WHERE id = 1;

      DELETE orders WHERE customer = 1;

      COMMIT;"
    )
    ```

### 设置事务

用户执行 `BEGIN` 语句后，但未执行其他数据库语句之前，可以使用 `SET TRANSACTION` 语句设置事务优先级、访问模式以及截止时间戳。

#### 所需权限

设置事务不需要任何权限。但是事务中的每个语句都需要相应的权限。

#### 语法格式

![](../../static/sql-reference/settransaction.png)

#### 参数说明

| 参数 | 说明 |
| --- | --- |
| `ISOLATION LEVEL` | 配置事务隔离级别，支持以下取值：<br >- 串行化（Serializable）：Serializable 隔离是最高的隔离级别，保证了即使事务是并行执行的，其结果也与它们一次执行一个事务时的结果相同，没有任何并发性。<br >- 提交读（Read Committed，RC）：在 RC 隔离级别下，事务会读取到其他事务已提交的数据，但不完全保证事务操作的可序列化。<br >- 可重复读（Repeatable Read，RR）：RR 隔离保证了在同一事务内多次读取同一数据时，结果是一致的。<br >默认情况下，事务的隔离级别为 Serializable。|
| `PRIORITY` | 事务的优先级。默认情况下，事务的优先级为 `NORMAL`。用户可以根据需要将事务的优先级设置为 `LOW` 或 `HIGH`。优先级越高的事务，重试的几率越低。|
| `READ` | 事务访问模式，支持 `READ ONLY` 或 `READ WRITE` 访问模式。默认模式为 `READ WRITE`。用户可以通过修改会话变量 `transaction_read_only` 设置访问模式。|
| `AS OF SYSTEM TIME` |  对截至指定时间的数据库内容执行事务。事务访问模式设置为 `READ ONLY` 时才能使用 `AS OF SYSTEM TIME` 子句。如果事务包含任何写操作，或者事务访问模式为 `READ WRITE`，系统将返回错误。|

#### 语法示例

- 设置事务隔离级别。

    ```sql
    -- 1. 启动事务。

    BEGIN;
    Now adding input for a multi-line SQL transaction client-side (smart_prompt enabled).
    Press Enter two times to send the SQL text collected so far to the server, or Ctrl+C to cancel.
    You can also use \show to display the statements entered so far.

    -- 2. 设置事务隔离级别为 READ COMMITTED。

    SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

    -- 3. 提交事务。

    COMMIT;
    COMMIT
    ```

- 设置事务优先级。

    ```sql
    -- 1. 启动事务。

    BEGIN;
    Now adding input for a multi-line SQL transaction client-side (smart_prompt enabled).
    Press Enter two times to send the SQL text collected so far to the server, or Ctrl+C to cancel.
    You can also use \show to display the statements entered so far.

    -- 2. 设置事务优先级为 HIGH。

    SET TRANSACTION PRIORITY HIGH;

    -- 3. 提交事务。

    COMMIT;
    COMMIT
    ```

- 设置 `AS OF SYSTEM TIME` 选项。

    ```sql
    -- 1. 启动事务。

    BEGIN;
    Now adding input for a multi-line SQL transaction client-side (smart_prompt enabled).
    Press Enter two times to send the SQL text collected so far to the server, or Ctrl+C to cancel.
    You can also use \show to display the statements entered so far.

    -- 2. 设置事务的 AS OF SYSTEM TIME 选项。

    SET TRANSACTION AS OF SYSTEM TIME '2023-04-18 10:00:00+00:00'; 

    -- 3. 提交事务。

    COMMIT;
    COMMIT
    ```

### 回滚事务

`ROLLBACK` 语句用于中止当前事务及其嵌套事务，丢弃事务语句产生的所有更新。

#### 所需权限

回滚事务不需要任何权限。但是事务中的每个语句都需要权限。

#### 语法格式

![](../../static/sql-reference/IqaRbHTgro1RLtxcZOzcRauPn4d.png)

#### 参数说明

| 参数 | 说明 |
| --- | --- |
| `savepoint_name` | 保存点的名称，KWDB 支持以下两类事务的保存点：<br >- 嵌套事务：保存点名称可以是任意名称。<br >- 自动重试事务：默认情况下，自动重试事务的保存点名称是 `kwbase_restart`，用户可以根据需要自定义保存点的名称。要使自定义保存点的名称生效，用户需要将 `force_savepoint_restart` 会话变量设置为 `true`。设置生效后，自动重试事务的保存点名称可以是任意名称。|

#### 语法示例

- 回滚事务。

    以下示例假设已经创建 `accounts` 表。

    ```sql
    -- 1. 查看 accounts 表的数据。

    SELECT * FROM accounts;
      id | balance
    -----+----------
      1 |    1000
      2 |    2000
      3 |    3000
    (3 rows)

    -- 2. 启动事务。

    BEGIN;
    Now adding input for a multi-line SQL transaction client-side (smart_prompt enabled).
    Press Enter two times to send the SQL text collected so far to the server, or Ctrl+C to cancel.
    You can also use \show to display the statements entered so far.

    -- 3. 更新 accounts 表。

    UPDATE accounts SET balance = 2500 WHERE id = 1;

    -- 4. 回滚事务。
    ROLLBACK;
    ROLLBACK

    -- 5. 查看 accounts 表的数据。

    SELECT * FROM accounts;
      id | balance
    -----+----------
      1 |    1000
      2 |    2000
      3 |    3000
    (3 rows)
    ```

- 重试事务。

    如果 KWDB 开启事务自动重试机制，当事务返回 `40001 / retry transaction` 错误时，用户可以使用该语句重试整个事务。

    ```sql
    ROLLBACK TO SAVEPOINT kwbase_restart;
    ```

- 使用 `ROLLBACK TO SAVEPOINT` 语句实现多级回滚。

    当事务中存在多个保存点时，用户可以使用 `ROLLBACK TO SAVEPOINT` 语句归滚到外层保存点。

    以下示例假设已创建 `kv` 关系表并写入数据。

    以下示例中，事务回滚值 `(6,6)` 和 `(7,7)`，仅将值 `(5,5)` 插入 `kv` 表。

    ```sql
    -- 1. 启动事务。

    BEGIN;

    -- 2. 向 kv 表中写入值 (5,5)。

    INSERT INTO kv VALUES (5,5);

    -- 3. 创建保存点 foo。

    SAVEPOINT foo;

    -- 4. 向 kv 表中写入值 (6,6)。

    INSERT INTO kv VALUES (6,6);

    -- 5. 创建保存点 bar。

    SAVEPOINT bar;

    -- 6. 向 kv 表中写入值 (7,7)。

    INSERT INTO kv VALUES (7,7);

    -- 7. 释放保存点 bar。

    RELEASE SAVEPOINT bar;

    -- 8. 回滚到保存点 foo。

    ROLLBACK TO SAVEPOINT foo;

    -- 9. 提交事务。

    COMMIT;
    COMMIT

    -- 10. 查看 kv 表的数据。

    SELECT * FROM kv;
    k|v
    -+-
    1|1
    2|2
    3|3
    4|4
    5|5
    (5 rows)
    ```

- 使用 `ROLLBACK TO SAVEPOINT` 语句恢复嵌套事务中的错误。

    `ROLLBACK TO SAVEPOINT` 语句支持恢复事务的错误。出现数据库错误后，嵌套事务进入已终止状态。 在这种状态下，事务将不再执行任何其他 SQL 语句。用户可以使用 `ROLLBACK TO SAVEPOINT` 语句恢复嵌套事务中的逻辑错误。 逻辑错误包括：

    - 唯一索引错误（重复行）
    - 外键约束检查失败（引用表中不存在行）
    - 查询中的错误（引用不存在的列）

    ```sql
    -- 1. 启动事务。

    BEGIN;

    -- 2. 创建保存点 error1。

    SAVEPOINT error1;

    -- 3. 向 kv 表中写入值 (5,5)。

    INSERT INTO kv VALUES (5,5);
    ERROR:  duplicate key value (k)=(5) violates unique CONSTRAINT "primary"

    -- 4. 创建保存点 foo。

    SAVEPOINT foo;

    -- 6. 查看事务状态。

    SHOW TRANSACTION STATUS;
    TRANSACTION STATUS
    ------------------
    Aborted           
    (1 row)

    -- 7. 回滚到保存点 error1。

    ROLLBACK TO SAVEPOINT error1;

    -- 8. 向 kv 表中写入值 (6,6)。

    INSERT INTO kv VALUES (6,6);
    INSERT 1

    -- 9. 提交事务。

    COMMIT;

    -- 10. 查看 kv 表的数据。

    SELECT * FROM kv;
    k|v
    -+-
    1|1
    2|2
    3|3
    4|4
    5|5
    6|6
    (6 rows)
    ```

### 提交事务

`COMMIT` 语句用于提交当前事务，或者在 KWDB 开启事务自动重试机制时，清除连接并开始新事务。

- 开启事务自动重试机制后，如果执行 `RELEASE SAVEPOINT` 语句，系统会提交保存点之后执行的语句。此时，需要执行 `COMMIT` 语句，清除连接并开始新事务。
- 未开启事务自动重试机制时，如果事务中的语句运行出现任何错误，`COMMIT` 语句用于中止事务并丢弃其语句产生的所有更新。此时，`COMMIT` 语句等效于 `ROLLBACK` 语句。

在 KWDB 中，`COMMIT` 语句的别名是 `END`。

#### 所需权限

提交事务不需要任何权限。但是，事务中的每个语句都需要权限。

#### 语法格式

![](../../static/sql-reference/HQdubWwXqoqy6ixxEJucNaPynSd.png)

#### 参数说明

无

#### 语法示例

```sql
-- 1. 启动事务。

BEGIN;

-- 2. 提交事务。

COMMIT;
```

### 创建保存点

SavePoint（保存点）是定义嵌套事务开始的标记。用户可以使用此标记来提交或回滚嵌套事务，而不会影响整个事务的进度。

#### 所需权限

创建保存点不需要任何权限。但是，事务中的每个语句都需要相应的权限。

#### 语法格式

![](../../static/sql-reference/BwsBbkFAkodWOVxVKRVcjYPgnje.png)

#### 参数说明

| 参数 | 说明 |
| --- | --- |
| `savepoint_name` | 保存点的名称，KWDB 支持以下两类事务的保存点：<br >- 嵌套事务：保存点名称可以是任意名称。<br >- 自动重试事务：默认情况下，自动重试事务的保存点名称是 `kwbase_restart`，用户可以根据需要自定义保存点的名称。要使自定义保存点的名称生效，用户需要将 `force_savepoint_restart` 会话变量设置为 `true`。设置生效后，自动重试事务的保存点名称可以是任意名称。|

#### 语法示例

以下示例假设已经创建 `kv` 关系表。

```sql
CREATE TABLE kv (k INT PRIMARY KEY, v INT);
CREATE TABLE
```

- 在事务内建立保存点。

    ```sql
    SAVEPOINT foo;
    ```

    ::: warning 说明
    `SAVEPOINT foo` 和 `SAVEPOINT Foo` 语句都表示创建一个名为 `foo` 的保存点。而 `SAVEPOINT "Foo"` 语句创建一个名为 `Foo` 的保存点。
    :::

- 嵌套事务的保存点。

    事务之间可以使用保存点名称相互嵌套。在嵌套结构中，`RELEASE SAVEPOINT` 和 `ROLLBACK TO SAVEPOINT` 语句都可以指向更高层级的保存点。在这种情况下，系统会自动释放、回滚嵌套结构内的所有保存点。

    - 当回滚先前的保存点后，系统也会将该保存点之后输入的语句进行回滚。有关详细信息，参见[回滚事务](#回滚事务)。
    - 当释放先前的保存点后，系统会将在保存点之后输入的语句进行提交。有关详细信息，参见[释放保存点](#释放保存点)。

- 自动重试事务的保存点。

    `kwbase_restart` 保存点是重试保存点，用于实现自动事务重试，如下所示。

    默认情况下，自动重试事务的保存点名称是 `kwbase_restart`。支持用户自定义保存点的名称。如需使用自定义的保存点，用户需要将 `force_savepoint_restart` 会话变量设置为 `true`。

    ```sql
    -- 1. 启动事务。

    BEGIN;

    -- 2. 创建 kwbase_restart 重试保存点。

    SAVEPOINT kwbase_restart;

    -- 3. 更新 products 表。

    UPDATE products SET inventory = 0 WHERE sku = '8675309';

    -- 4. 向 orders 表写入数据。

    INSERT INTO orders (customer, sku, status) VALUES (1001, '8675309', 'new');

    -- 5. 释放 kwbase_restart 重试保存点。

    RELEASE SAVEPOINT kwbase_restart;

    -- 6. 提交事务。

    COMMIT;
    ```

- 保存点和 `prepared` 语句。

    `PREPARE` / `EXECUTE` 语句不是事务性的语句。因此，回滚保存点时，`PREPARE` 语句仍在事务内保存并执行，不会失效。

    ```sql
    -- 1. 启动事务。
    BEGIN;

    -- 2. 创建保存点 foo。

    SAVEPOINT foo;

    -- 3. 预定义 bar。

    PREPARE bar AS SELECT 1;

    -- 4. 回退到保存点 foo。

    ROLLBACK TO SAVEPOINT foo;

    -- 5. 执行预定义的 bar。

    EXECUTE bar;

    ?column?
    --------
    1       
    (1 row)

    -- 6. 提交事务。

    COMMIT;
    ```

### 释放保存点

`RELEASE SAVEPOINT` 语句使用相同的保存点名称从相应的 `SAVEPOINT` 语句开始提交嵌套事务（包括其嵌套子事务）。`RELEASE SAVEPOINT` 语句进一步支持重试保存点。

#### 所需权限

释放保存点不需要任何权限。但是，事务中的每个语句都需要相应的权限。

#### 语法格式

![](../../static/sql-reference/XgghbhVzEoSNhxx39gzcXJHMnod.png)

#### 参数说明

| 参数 | 说明 |
| --- | --- |
| `savepoint_name` | 保存点的名称，KWDB 支持以下两类事务的保存点：<br >- 嵌套事务：保存点名称可以是任意名称。<br >- 自动重试事务：默认情况下，自动重试事务的保存点名称是 `kwbase_restart`，用户可以根据需要自定义保存点的名称。要使自定义保存点的名称生效，用户需要将 `force_savepoint_restart` 会话变量设置为 `true`。设置生效后，自动重试事务的保存点名称可以是任意名称。|

#### 处理错误

嵌套事务出现错误后，用户无法使用 `RELEASE SAVEPOINT` 语句消除错误。在这种情况下，用户可以采取以下操作：

- `ROLLBACK TO SAVEPOINT`：回滚到上一个保存点。
- `ROLLBACK` 或 `ABORT`：回滚相关事务。
- `COMMIT`：提交所有相关事务。如果发生错误，`COMMIT` 也用于回滚事务。

当事务（或子事务）出现重试错误时，客户端应重复 `ROLLBACK TO SAVEPOINT` 和事务中的语句，直到语句完整无误，然后再释放保存点。

当嵌套事务出现错误后，如需完全删除其标记并在外部事务中开始其他操作，请立即使用 `ROLLBACK TO SAVEPOINT` 语句，然后再释放保存点。

#### 语法示例

- 确认保存点名称是否存在。

    用户无法查看已回滚的保存点名称。以下示例中，事务回滚后，用户无法查看 `bar` 保存点。

    ```sql
    -- 1. 启动事务。

    BEGIN;

    -- 2. 创建 foo 保存点。

    SAVEPOINT foo;

    -- 3. 创建 bar 保存点。

    SAVEPOINT bar;

    -- 4. 回滚到 foo 保存点。

    ROLLBACK TO SAVEPOINT foo;

    -- 5. 释放 bar 保存点。
    RELEASE SAVEPOINT bar;
    ERROR:  savepoint "bar" does not exist

    -- 6. 提交事务。
    COMMIT;
    ```

- 释放保存点，提交事务。

    以下示例中，事务会将事务会将值 `(2,2)` 和 `(4,4)` 写入 `kv` 表中。

    ```sql
    -- 1. 启动事务。

    BEGIN;

    -- 2. 创建 foo 保存点。

    SAVEPOINT foo;

    -- 3. 向 kv 表中写入数据 (2,2)。
    INSERT INTO kv VALUES (2,2);

    -- 4. 向 kv 表中写入数据 (4,4)。
    INSERT INTO kv VALUES (4,4);

    -- 5. 释放 foo 保存点。

    RELEASE SAVEPOINT foo;

    -- 6. 提交事务。

    COMMIT;

    -- 7. 查看 kv 表的数据。

    SELECT * FROM kv;
    k|v
    -+-
    2|2
    4|4
    (2 rows)
    ```

- 释放保存点，提交嵌套事务。

    以下示例回滚内层嵌套事务（由保存点 `lower` 标记），提交外层保存点 `higher`。

    ```sql
    -- 1. 启动事务。

    BEGIN;

    -- 2. 创建 higher 保存点。

    SAVEPOINT higher;

    -- 3. 更新 promo_codes 表。

    UPDATE promo_codes SET rules = jsonb_set(rules, '{value}', '"15%"') WHERE rules @> '{"type": "percent_discount"}';

    -- 4. 创建 lower 保存点。

    SAVEPOINT lower;

    -- 5. 更新 promo_codes 表。

    UPDATE promo_codes SET rules = jsonb_set(rules, '{value}', '"7.5%"') WHERE rules @> '{"type": "percent_discount"}';

    -- 6. 回滚到 lower 保存点。

    ROLLBACK TO SAVEPOINT lower;

    -- 7. 释放 higher 保存点。

    RELEASE SAVEPOINT higher;

    -- 8. 提交事务。
    COMMIT;
    ```

- 释放重试保存点，提交事务。

    指定重试保存点后，用户可以使用 `RELEASE SAVEPOINT` 语句释放保存点，然后使用 `COMMIT` 语句提交事务，为下个事务准备连接。

    ```sql
    -- 1. 启动事务。

    BEGIN;

    -- 2. 创建 kwbase_restart 重试保存点。

    SAVEPOINT kwbase_restart;

    -- 3. 更新 products 表。

    UPDATE products SET inventory = 0 WHERE sku = '8675309';

    -- 4. 向orders 表中写入数据。

    INSERT INTO orders (customer, sku, status) VALUES (1001, '8675309', 'new');

    -- 5. 释放 kwbase_restart 重试保存点。
    RELEASE SAVEPOINT kwbase_restart;

    -- 6. 提交事务。
    COMMIT;
    ```
