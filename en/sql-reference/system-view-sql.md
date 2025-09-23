---
title: System Views
id: system-view-sql
---

# System Views

## Privileges

The user must be a `root` user.

## kwdb_internal.audit_policies

The `kwdb_internal.audit_policies` system view describes audit policies.

| Column Name   | Data Type       | Description                                                                                                                                                                                           |
|---------------|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `audit_name`  | STRING NOT NULL | The name of the audit policy.                                                                                                                                                                         |
| `target_type` | STRING NOT NULL | The type of the audit target, such as users, roles, databases, tables, views, indexes, constraints, sequences, privileges, ranges, queries, jobs, session, statistics, audits, properties, and so on. |
| `target_name` | STRING          | The name of the audit target.                                                                                                                                                                         |
| `target_id`   | INT             | The ID of the audit target.                                                                                                                                                                           |
| `operations`  | STRING NOT NULL | The audit operation.                                                                                                                                                                                  |
| `operators`   | STRING NOT NULL | The audit user.                                                                                                                                                                                       |
| `condition`   | INT             | Reserved field. The audit condition.                                                                                                                                                                  |
| `whenever`    | STRING NOT NULL | The audit results.                                                                                                                                                                                    |
| `action`      | INT             | Reserved field. The post-audit operations.                                                                                                                                                            |
| `level`       | INT             | Reserved field. The audit level.                                                                                                                                                                      |
| `enable`      | BOOL NOT NULL   | Whether to enable database audit.                                                                                                                                                                     |
