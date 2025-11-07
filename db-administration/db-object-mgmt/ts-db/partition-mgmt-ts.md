---
title: 分区管理
id: partition-mgmt-ts
---

# 分区管理

表分区是一种数据库优化技术，通过对数据存储位置进行行级控制，将数据分布到指定节点上，从而有效降低查询延迟并提升性能。

## 工作原理

时序数据库中，表分区功能由两个核心组件协同工作：

**分区定义**

用户可以在修改表时为表设置哈希点（HashPoint）分区，系统会根据数据的哈希值自动将数据分配到不同分区。KWDB 支持以下两种分区方式：

- **按连续范围分区**：将哈希值范围分配给分区（如将哈希值 1-100 分配给分区 A）
- **按指定值分区**：将特定哈希值分配给分区（如将特定哈希值 1 和 5 分配给分区 B）

分区配置与表的生命周期紧密绑定，删除表时分区配置会自动失效，重新设置表分区时，新配置将完全覆盖原有设置，系统会自动清理已删除分区的区域配置信息。

分区设置操作支持重复执行，便于用户根据需要调整分区策略。

建议将分区设置与数据分片（Range）分布保持对应关系，确保 Range 能够按照预期的分区规则正确分布到目标节点。注意：分区设置不会触发现有 Range 的重新切分操作，仅影响 Range 的区域配置分布策略，通过调整数据副本的存储位置来实现性能优化。

**区域配置**

分区定义仅为满足条件的表行添加标识。要使分区真正发挥作用，需要配置区域（zone）并将其应用到相应分区。

**配置优先级：** 分区 > 表 > 数据库

## 创建分区

### 所需权限

用户是 `admin` 角色成员或拥有目标表的 CREATE 权限，`root` 用户默认属于 `admin` 角色。

### 语法格式

::: warning 说明

以下语法仅列出创建分区的必需参数。关于修改表支持的完整参数，参见[修改表](../../../sql-reference/ddl/ts-db/ts-table.md#修改表)。

:::

- 按指定哈希值分区：

    ```SQL
    ALTER TABLE <table_name> 
    PARTITION BY HASHPOINT (
        PARTITION <partition_name> VALUES IN [<hashpoint_list>], 
        PARTITION <partition_name> VALUES IN [<hashpoint_list>],
        ... 
    );
    ```

- 按指定哈希值范围分区：

    ```SQL
    ALTER TABLE <table_name>  
    PARTITION BY HASHPOINT (
        PARTITION <partition_name> VALUES FROM (<hashpoint_1>) TO (<hashpoint_2>),
        PARTITION <partition_name> VALUES FROM (<hashpoint_1>) TO (<hashpoint_2>),
        ... 
    );
    ```

### 参数说明

| 参数             | 说明                                       |
| :--------------- | :----------------------------------------- |
| `table_name`     | 分区所在的表名                             |
| `partition_name` | 分区名称                                   |
| `hashpoint_list` | 哈希值列表，用逗号分隔，如：`1,3,5,7`      |
| `hashpoint_1`    | 范围分区的起始哈希值（包含），必须是整数   |
| `hashpoint_2`    | 范围分区的结束哈希值（不包含），必须是整数 |

### 语法示例

- 按指定哈希值分区

    ```SQL
    -- 为订单表创建按指定哈希值的分区 
    ALTER TABLE orders  
    PARTITION BY HASHPOINT (
        PARTITION p_region_1 VALUES IN [1, 3, 5, 7],
        PARTITION p_region_2 VALUES IN [2, 4, 6, 8],
        PARTITION p_region_3 VALUES IN [9, 10] 
    );
    ```

- 按指定哈希值范围分区

    ```SQL
    -- 为用户表创建按哈希值范围的分区 
    ALTER TABLE users
    PARTITION BY HASHPOINT (
        PARTITION p_low VALUES FROM (0) TO (100),
        PARTITION p_medium VALUES FROM (100) TO (200),
        PARTITION p_high VALUES FROM (200) TO (300) 
    );
    ```

## 设置分区

`ALTER PARTITION` 语句用于修改表分区的副本区域配置。

::: warning 注意

- **异常和缩容对规则执行的影响**：当规则指定的目标节点包含异常节点或正在进行缩容操作时，设置的 `lease_preferences` 和 `constraints` 可能无法按照指定规则成功分布。
- **规则对分布式高可用和缩容的影响**：
  - 如果集群中某个节点异常，指向该节点的 `lease_preferences` 可能会失效，但系统会保持高可用性，`constraints` 设置的约束可能会限制后续的高可用副本补充操作。
  - 执行缩容操作时，设置的 `lease_preferences` 可能会失效，但系统仍会保持高可用性，`constraints` 约束设置可能导致缩容操作无法正常完成。

:::

### 所需权限

用户是 `admin` 角色成员或拥有目标表的 CREATE 权限，`root` 用户默认属于 `admin` 角色。

### 语法格式

```SQL
ALTER PARTITION <partition_name> OF TABLE <table_name> 
CONFIGURE ZONE [USING <variable> = <value>, <variable> = <value>, ... | DISCARD];
```

### 参数说明

| 参数             | 说明                                                         |
| :--------------- | :----------------------------------------------------------- |
| `partition_name` | 待修改的分区名称                                             |
| `table_name`     | 分区所在的表名                                               |
| `variable`       | 支持修改以下变量：<br>- `num_replicas`：副本数量。默认值为 3<br>- `constraints`：副本位置的必需（+）和/或禁止（-）约束。例如 `constraints = '{"+region=NODE1": 1, "+region=NODE2": 1, "+region=NODE3": 1}'` 表示在节点 1、节点 2、节点 3 上必须各放置 1 个副本。目前只支持 `region=NODEx` 格式<br>- `lease_preferences`：主副本位置的必需（+）和/或禁止（-）约束的有序列表。例如 `lease_preferences = '[[+region=NODE1]]'` 表示倾向将主副本放置在节点 1。如果不能满足首选项，KWDB 将尝试下一个优先级。如果所有首选项都无法满足，KWDB 将使用默认的租约分布算法，基于每个节点已持有的租约数量来决定租约位置，尝试平衡租约分布。列表中的每个值可以包含多个约束<br><br>**注意**：<br>- 租约偏好不必与 `constraints` 字段共享，用户可以单独定义 `lease_preferences`<br>- 设置 `constraints` 时需要同步设置 `num_replicas`，且 `constraints` 数量需要小于等于 `num_replicas` 数量。`constraints` 中的顺序无影响 |
| `value`          | 变量值，可以是具体的配置值，也可以是 `COPY FROM PARENT`，即使用父区域的设置值 |
| `DISCARD`        | 移除区域配置，采用默认值                                     |

### 语法示例

```SQL
-- 低哈希值分区：数据存储在所有节点，lease 偏向节点 1
ALTER PARTITION p_low OF TABLE users 
CONFIGURE ZONE USING 
    num_replicas = 3, 
    constraints = '{"+region=NODE1": 1, "+region=NODE2": 1, "+region=NODE3": 1}',
    lease_preferences = '[[+region=NODE1]]';

-- 中哈希值分区：数据存储在所有节点，lease 偏向节点 2
ALTER PARTITION p_medium OF TABLE users  
CONFIGURE ZONE USING 
    num_replicas = 3, 
    constraints = '{"+region=NODE1": 1, "+region=NODE2": 1, "+region=NODE3": 1}',
    lease_preferences = '[[+region=NODE2]]';

-- 高哈希值分区：数据存储在所有节点，lease 偏向节点 3
ALTER PARTITION p_high OF TABLE users 
CONFIGURE ZONE USING 
    num_replicas = 3, 
    constraints = '{"+region=NODE1": 1, "+region=NODE2": 1, "+region=NODE3": 1}',
    lease_preferences = '[[+region=NODE3]]';

-- 插入测试数据
INSERT INTO users (created_at, id, name, email, region) VALUES 
('2024-01-15 09:30:00', 1, 'Zhang Wei', 'zhangwei@example.com', 'North'),
('2024-01-15 10:15:30', 2, 'Li Ming', 'liming@example.com', 'East'),
('2024-01-15 11:20:45', 3, 'Wang Lei', 'wanglei@example.com', 'South'),
('2024-02-10 14:25:12', 101, 'Liu Fang', 'liufang@example.com', 'West'),
('2024-02-10 15:40:28', 102, 'Chen Xin', 'chenxin@example.com', 'North'),
('2024-03-05 08:55:33', 201, 'Yang Hao', 'yanghao@example.com', 'East'),
('2024-03-05 16:10:18', 202, 'Zhou Mei', 'zhoumei@example.com', 'South');

-- 查看数据分布
SELECT database_name, table_name, range_id, start_pretty, end_pretty, lease_holder, replicas, range_size 
FROM kwdb_internal.ranges 
WHERE database_name = 'ecommerce_orders' AND table_name = 'users';
```