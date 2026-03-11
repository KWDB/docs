---
title: 概述
id: kaiwudb-tools-overview
---

# KWDB 工具概述

KWDB 提供一套完整的配套工具，覆盖数据库可视化管理、AI 智能交互、数据迁移、命令行运维和性能测试等使用场景。

下表列出了 KWDB 当前提供的工具。

| 工具 | 说明 |
|------|------|
| [KaiwuDB 开发者中心](#kaiwudb-开发者中心) | 图形化数据库管理平台，提供连接管理、对象管理、数据编辑、SQL 编辑等可视化操作能力 |
| [KaiwuDB 智能体工具（KAT）](#kaiwudb-智能体工具kat) | 基于 MCP 协议的数据库智能体工具，支持通过自然语言完成数据库运维、数据分析等任务 |
| [KWDB MCP Server](#kwdb-mcp-server) | 面向应用开发的 MCP 协议连接器，供 LLM Agent 直接连接 KWDB 执行数据读写和 DDL 操作 |
| [kwbase CLI 工具](#kwbase-cli-工具) | 命令行管理工具，支持节点启动、集群初始化、证书管理、SQL 操作及节点运维等操作 |
| [TSBS MCP Server](#性能测试工具) | 基于 MCP 协议的时序数据库基准测试服务端 |
| [kwdb-tsdb](#性能测试工具) | 基于 TSBS 的时序数据库标准化性能测试工具 |

## KaiwuDB 开发者中心

KaiwuDB Developer Center（KDC）是专为 KWDB 设计的图形化数据库管理平台，可将数据库的日常操作可视化，替代传统命令行操作。KDC 支持连接管理、数据库与表对象管理、数据编辑、SQL 编辑、用户与权限管理等功能，适用于开发和日常运维场景。有关详细信息，参见 [KaiwuDB 开发者中心](./kaiwudb-developer-center/overview.md)。

## KaiwuDB 智能体工具（KAT）

KaiwuDB Agent Tools（KAT）是基于 MCP（Model Context Protocol，模型上下文协议）协议构建的数据库智能体工具，包含 KWDB MCP Server 和 AI 助手两个组件。KAT 将自然语言处理能力与 KWDB 深度融合，用户通过对话即可完成数据库安装部署、数据读写、分析查询等操作，兼容 Cline 等主流 MCP 客户端。有关详细信息，参见 [KaiwuDB 智能体工具](./kat/kat-overview.md)。

## KWDB MCP Server

KWDB MCP Server 是面向应用开发场景的 MCP 协议连接器，供兼容 MCP 协议的 LLM Agent（如 Cline）通过 HTTP SSE 或 StdIO 协议连接 KWDB，直接执行数据读写、DDL 操作和只读查询。与 KAT 的区别在于，KWDB MCP Server 是标准化的数据库接口层，开发者可将其集成到自己的 AI 应用中；KAT 则是面向最终用户的智能体交互工具。有关详细信息，参见 [KWDB MCP Server](../development/kwdb-mcp-server/connect-kwdb-mcp-server.md)。

## kwbase CLI 工具

`kwbase` 是 KWDB 提供的命令行管理工具，适用于无图形界面的部署和运维场景，是管理 KWDB 集群的核心工具。`kwbase` 支持节点启动与初始化、TLS/TLCP 证书管理、SQL 交互、节点状态管理、HTTP 会话管理及辅助配置文件生成等操作。有关各命令的详细说明，参见 [kwbase CLI 工具](./kwbase-cli-tool.md)。

## 性能测试工具

KWDB 提供以下性能测试工具，适用于不同的测试场景：

- **TSBS MCP Server** 是基于 MCP 协议的时序数据库基准测试服务端，支持在兼容 MCP 协议的 AI 环境中以自然语言方式触发和管理 KWDB 性能测试任务。有关详细信息，参见 [TSBS MCP Server](./perf-benchmark/tsbs-mcp-server.md)。
- **kwdb-tsdb** 是基于 TSBS（Time Series Benchmark Suite）的 KWDB 专用性能测试工具，用于对时序数据读写性能进行标准化评估。有关详细信息，参见 [kwdb-tsdb](./perf-benchmark/kwdb-tsbs.md)。