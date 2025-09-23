---
title: 系统视图
id: system-view-sql
---

# 系统视图

## 所需权限

用户是 `admin` 角色的成员。默认情况下，`root` 用户属于 `admin` 角色。

## kwdb_internal.audit_policies

`kwdb_internal.audit_policies` 系统视图描述审计策略。

| 列名        | 数据类型        | 描述                                                                                                                    |
| ----------- | --------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `audit_name`  | STRING NOT NULL | 审计策略名称                                                                                                            |
| `target_type` | STRING NOT NULL | 审计目标类型，例如用户、角色、数据库、表、视图、索引、约束、序列、权限、Range、查询、任务、会话、统计信息、审计、属性等 |
| `target_name` | STRING          | 审计目标名称                                                                                                            |
| `target_id`   | INT             | 审计目标对象 ID                                                                                                         |
| `operations`  | STRING NOT NULL | 审计操作                                                                                                                |
| `operators`   | STRING NOT NULL | 审计的用户                                                                                                              |
| `condition`   | INT             | 审计条件，预留字段                                                                                                      |
| `whenever`    | STRING NOT NULL | 审计结果                                                                                                                |
| `action`      | INT             | 审计后操作，预留字段                                                                                                    |
| `level`       | INT             | 审计等级，预留字段                                                                                                      |
| `enable`      | bool NOT NULL   | 审计策略开关                                                                                                            |