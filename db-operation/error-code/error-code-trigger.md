---
title: 触发器错误码
id: error-code-ts-functions
---

# 触发器错误码

本文介绍与触发器相关的错误码。

| 错误码 | 消息 | 错误原因 |
| --- | --- | ---|
| 0A000 | Not all nodes are at the correct version to use Triggers | 并非所有节点都升级到了支持触发器的版本。 |
| 42P17 | Object %s cannot be bound to a trigger | 不支持在复制表、视图、序列、临时表、时序表上创建触发器。 |
| 42P17 | Trigger %s already exists on table %s | 目标表上已存在同名触发器。 |
| 42601 | empty trigger name | 重命名触发器时未指定触发器名称。 |
| 42704 | trigger \"%s\" does not exist | 无法解析到目标触发器。 |
| 3D000 | unsupported table type: %s in trigger | 触发器绑定的对象不是关系引擎的普通表。 |
| 42P13 | cannot use OLD in INSERT event trigger | INSERT 事件触发器不支持使用 `OLD` 别名。 |
| 42P13 | cannot use NEW in DELETE event trigger | DELETE 事件触发器不支持使用 `NEW` 别名。 |
| 0A000 | INSERT ... ON CONFLICT is not supported in trigger definition | 触发器主体不支持 `INSERT ... ON CONFLICT` 语句。 |
| 42P13 | Can't update table %s in trigger because it is already used by statement which invoked this trigger. | 不支持在触发器主体中对触发器关联的表进行操作。 |
| 42704 | trigger \"%s\" on table \"%s\" does not exist | 重命名触发器时目标触发器不存在。 |
| 42P17 | trigger \"%s\" already exists on table \"%s\" | 重命名触发器时已存在同名触发器。 |
| 42P17 | Referenced trigger \"%s\" for the given action time does not exist | 创建的触发器的触发时机和引用的（`FOLLOWS`、`PRECEDES`）触发器的触发时机不一致。 |
| 09000 | TriggeredActionException: errMsg | 执行触发器主体时遇到错误。 |
