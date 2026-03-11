---
title: TSBS MCP Server
id: tsbs-mcp-server
---

# TSBS MCP Server

TSBS MCP Server 是基于 [MCP](https://modelcontextprotocol.io/introduction)（Model Context Protocol，模型上下文协议）Go SDK 开发的性能测试服务。它通过 HTTP 接口对外提供标准化的 MCP 协议，将 kwdb-tsbs 测试工具封装为 MCP 工具，使 AI 助手及其他 MCP 客户端能够便捷地与 kwdb-tsbs 测试工具进行交互。

TSBS MCP Server 主要提供以下功能：

- 支持异步任务执行与状态跟踪。
- 基于数据库实现任务状态管理。
- 提供基于 Streamable HTTP 传输的 MCP 协议支持。
- 兼容 kwdb-tsbs 测试工具的全功能操作，包括时序数据生成、数据写入、查询处理、自动化结果汇总统计等。

## 支持的 MCP 工具

- 执行工具
  - `tsbs_generate_data`：数据生成工具，用于生成测试数据。
  - `tsbs_load_kwdb`：数据导入工具，用于将测试数据加载到 KWDB 数据库。
  - `tsbs_generate_queries`：查询生成工具，用于生成测试查询。
  - `tsbs_run_queries_kwdb`：查询执行工具，用于执行测试查询。
- 状态查询工具
  - `get_tsbs_generate_data_status`：数据生成状态查询工具，用于查询数据的生成状态。
  - `get_tsbs_load_status`：数据导入状态查询工具，用于查询数据的加载状态。
  - `get_tsbs_generate_queries_status`：查询生成状态查询工具，用于查询测试查询的生成状态。
  - `get_tsbs_run_queries_status`：查询执行状态查询工具，用于查询测试查询的执行状态。

## 配置 TSBS MCP Server

用户可以通过 TSBS MCP Server 的配置文件（`configs/config.yaml`）或环境变量来配置 TSBS MCP Server。

::: warning 说明
环境变量的优先级高于配置文件。
:::

### 配置文件

通过配置文件 `configs/config.yaml` 配置 TSBS MCP Server 服务。

配置文件示例：

```yaml
server:
  port: 8081          # HTTP 服务端口
  host: "0.0.0.0"     # 监听地址（0.0.0.0 表示所有网络接口）

# 任务状态数据库配置（用于存储任务状态和结果）
database:
  host: "localhost"   # 数据库主机地址
  port: 26257         # 数据库端口（KWDB 默认 26257，PostgreSQL 默认 5432）
  user: "root"        # 数据库用户名
  password: ""         # 数据库密码（建议使用环境变量 TSBS_DB_PASSWORD）
  dbname: "defaultdb"  # 数据库名称
  sslmode: "disable"  # SSL 模式（disable/require/verify-ca/verify-full）
  # SSL 证书配置（当 sslmode 为 verify-ca 或 verify-full 时需要）
  # sslcert: "/path/to/client.crt"      # 客户端证书文件路径（可选）
  # sslkey: "/path/to/client.key"       # 客户端密钥文件路径（可选）
  # sslrootcert: "/path/to/ca.crt"      # 根证书文件路径（verify-ca 和 verify-full 模式必需）

tsbs:
  bin_path: "./bin"                    # TSBS 二进制文件路径
  work_dir: "./tsbs_work"              # 工作目录
  data_dir: "./tsbs_work/load_data"    # 数据文件存储目录
  query_dir: "./tsbs_work/query_data"  # 查询文件存储目录
  reports_dir: "./tsbs_work/reports"    # 报告文件存储目录
  test_dbname: "tsbs"  # TSBS 测试数据库名称，与元数据数据库分离，避免冲突
  # 可选：TSBS 配置文件路径，用于读取测试目标数据库的默认配置
  # tsbs_config_path: "./config.yaml"
```

下表列出 TSBS MCP Server 的配置参数。

| 类别 | 参数 | 说明 |
| --- | --- | --- |
| TSBS MCP Server 配置 | `server.port` | TSBS MCP Server 的 HTTP 服务监听端口，默认为 `8081` |
| | `server.host` | TSBS MCP Server 的监听地址 <br>- `0.0.0.0`：表示监听所有网络接口 <br>-`127.0.0.1`：表示仅本地访问 |
| 数据库配置 | - | 元数据数据库，用于存储任务状态、进度和结果。支持 PostgreSQL 和 KWDB。|
| | `database.host` | 数据库的主机地址 |
| | `database.port` | 数据库的端口号 <br>- KWDB：默认为 `26257` <br>- PostgreSQL：默认为 `5432` |
| | `database.user` | 数据库的用户名 |
| | `database.password` | 数据库的用户密码 |
| | `database.dbname` | 数据库的名称 |
| | `database.sslmode` | SSL 连接模式。当 `database.sslmode` 设置为 `verify-ca` 或 `verify-full` 时，用户需要在配置文件中指定证书的存放路径。 <br>- `disable`：不使用加密连接（适用于开发环境）。 <br>- `require`：确保已加密连接（不验证证书）。<br>- `verify-ca`：确保已加密连接，并且客户端信任服务器证书。该参数必须与 `sslrootcert` 参数配合使用。<br>- `verify-full`：确保已加密连接，客户端信任服务器证书，并且服务器主机名与服务器证书列出的主机名匹配。该参数必须与 `sslrootcert` 参数配合使用。该参数也可以与 `sslcert` 和 `sslkey` 参数配合使用。|
| | `database.sslcert` | 可选参数，SSL 客户端证书的存放路径（用于客户端证书认证） |
| | `database.sslkey` | 可选参数，SSL 客户端密钥的存放路径（用于客户端证书认证） |
| | `database.sslrootcert` | SSL 根证书（CA）的存放路径。当 `database.sslmode` 设置为 `verify-ca` 或 `verify-full` 时，用户必须设置该参数。 |
| kwdb-tsbs 配置 | `tsbs.bin_path` | kwdb-tsbs 二进制文件的存放路径，需要包含以下文件：<br>- `tsbs_generate_data` <br>- `tsbs_load_kwdb` <br>- `tsbs_generate_queries` <br>- `tsbs_run_queries_kwdb`  |
| | `tsbs.work_dir` | 工作目录的根路径 |
| | `tsbs.data_dir` | 生成的数据文件的存放目录 |
| | `tsbs.query_dir` | 生成的查询文件的存放目录 |
| | `tsbs.reports_dir` | 测试报告的存放目录 |
| | `test_dbname` | TSBS 测试数据库的名称，与元数据数据库进行区分。 |
| | `tsbs.config_path` | 可选参数，TSBS MCP Server 配置文件的路径，用于读取测试目标数据库的默认配置。 |

### 环境变量

- `TSBS_SERVER_PORT`：TSBS MCP Server 的 HTTP 服务监听端口（覆盖 `server.port`）
- `TSBS_SERVER_HOST`：TSBS MCP Server 的监听地址（覆盖 `server.host`）
- `TSBS_DB_HOST`：数据库的主机地址（覆盖 `database.host`）
- `TSBS_DB_PORT`：数据库的端口号（覆盖 `database.port`）
- `TSBS_DB_USER`：数据库的用户名（覆盖 `database.user`）
- `TSBS_DB_PASSWORD`：数据库的用户密码（覆盖 `database.password`）
- `TSBS_DB_NAME`：数据库的名称（覆盖 `database.dbname`）
- `TSBS_DB_SSLMODE`：SSL 连接模式（覆盖 `database.sslmode`）
- `TSBS_DB_SSLCERT`：SSL 客户端证书的存放路径（覆盖 `database.sslcert`）
- `TSBS_DB_SSLKEY`：SSL 客户端密钥的存放路径（覆盖 `database.sslkey`）
- `TSBS_DB_SSLROOTCERT`：SSL 根证书的存放路径（覆盖 `database.sslrootcert`）
- `TSBS_BIN_PATH`：kwdb-tsbs 二进制文件的存放路径（覆盖 `tsbs.bin_path`）
- `TSBS_WORK_DIR`：工作目录的根路径（覆盖 `tsbs.work_dir`）
- `TSBS_DATA_DIR`：生成的数据文件的存放目录（覆盖 `tsbs.data_dir`）
- `TSBS_QUERY_DIR`：生成的查询文件的存放目录（覆盖 `tsbs.query_dir`）
- `TSBS_REPORTS_DIR`：测试报告的存放目录（覆盖 `tsbs.reports_dir`）

### MCP 客户端配置

TSBS MCP Server 可与任何支持 MCP 协议的 MCP 客户端配合使用。MCP 客户端通过 Streamable HTTP 传输协议连接 TSBS MCP Server，然后连接 KaiwuDB 数据库，执行时序数据生成、数据写入、查询处理、自动化结果汇总统计等操作。

::: warning 说明
本节示例使用 [Cursor](https://cursor.com/cn/download) 客户端。
:::

编辑 Cursor 的配置文件（`~/.cursor/mcp.json`）。

配置示例：

```json
{
  "mcpServers": {
    "tsbs-mcp-server": {
      "url": "http://localhost:8081"
    }
  }
}
```

## 安装并运行 TSBS MCP Server

### 前提条件

- 已下载并安装 Go（1.21+）。
- 已安装和运行 PostgreSQL 或 KWDB 数据库、配置数据库认证方式、创建数据库。
- 已获取 kwdb-tsbs 二进制文件（`tsbs_generate_data`, `tsbs_load_kwdb`, `tsbs_generate_queries`, `tsbs_run_queries_kwdb`）。

### 步骤

1. 构建 TSBS MCP Server。

    ```bash
    make mcp-server-build
    ```

    或者

    ```bash
    go build -o bin/tsbs-mcp-server ./cmd/tsbs-mcp-server
    ```

2. 启动 TSBS MCP Server 服务。

    ```bash
    ./bin/tsbs-mcp-server
    ```

    默认情况下，系统将在配置的端口（默认 `8081`）上启动 TSBS MCP Server 服务。启动后，TSBS MCP Server 服务自动创建以下表：

    - `tsbs_test_tasks`：主任务表
    - `tsbs_test_subtasks`：子任务表
    - `tsbs_test_results`：结果表

## 使用举例

TSBS MCP Server 通过 HTTP 对外提供基于 JSON-RPC 2.0 协议的 MCP 接口。MCP 客户端调用时，需发送符合 JSON-RPC 2.0 规范格式的请求。

- 生成数据示例

    ```json
    {
      "jsonrpc": "2.0",
      "id": 1,
      "method": "tools/call",
      "params": {
        "name": "tsbs_generate_data",
        "arguments": {
          "use_case": "cpu-only",
          "scale": 1000,
          "timestamp_start": "2016-01-01T00:00:00Z",
          "timestamp_end": "2016-02-01T00:00:00Z",
          "log_interval": "10s"
        }
      }
    }
    ```

- 查询状态示例

    ```json
    {
      "jsonrpc": "2.0",
      "id": 2,
      "method": "tools/call",
      "params": {
        "name": "get_tsbs_generate_data_status",
        "arguments": {
          "test_task_id": "task_ID"
        }
      }
    }
    ```
