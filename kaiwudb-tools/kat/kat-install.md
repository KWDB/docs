---
title: 安装部署
id: kat-install
---

# 安装部署

用户可以在 Windows、MacOS、Linux 平台部署 KAT。本文档介绍如何使用 `setup.sh` 脚本整体部署 KGA。

## 部署 KGA

### 前提条件

- 已[安装](https://docs.docker.com/compose/install/) Docker Compose，且处于运行状态。
- 已安装 `curl`，调用 KaiwuDB SSO 接口、获取公网 IP 。
- 已安装 `python3`，脚本内部用其解析 JSON 。
- 前往[KaiwuDB软件下载中心](https://www.kaiwudb.com/download?tab=3）获取 KGA Server 、UI、VIS 镜像，`setup.sh`脚本以及 `docker-compose.yaml` 模板文件。

::: warning 说明
- 安装用户为 `root` 用户。`root` 用户在进行部署时无需输入密码。
- `setup.sh` 脚本启动时会自动检查这三项依赖，缺少任何一项都会报错退出。
- （可选）如需以安全模式连接 KWDB 数据库，用户需要生成 CA 证书和密钥、客户端证书和密钥、节点证书和密钥。有关详细信息，参见 [`kwdb cert` 命令参考](../kwbase-cli-tool.md#kwbase-cert)。
:::

### 安装前准备

1. 可以使用 `bash setup.sh --help` 查看支持场景。
   
   | 命令 | 说明 |
   |-----------|------|
   | `bash setup.sh`                 | 首次完整部署（推荐）|
   | `bash setup.sh --register-only` | 仅注册 OAuth，不启动服务 | 
   | `bash setup.sh --up` |          |已有配置，直接启动 |  
   | `bash setup.sh --shutdown`      | 停止所有服务 | 
   | `bash setup.sh --force`         | 强制重新注册 OAuth | 
   | `bash setup.sh --copilot-url=http://IP:8123 --backend-url=http://IP:8000` |自定义前端访问地址 | 

2. 服务默认端口
   
   | 服务 | 默认端口 |
   |------|---------|
   | PostgreSQL | 5432 |
   | KGA API | 8000 |
   | KWDB CMD MCP | 8001 |
   | KGA UI | 3000 |
   | KWDB Agent | 8123 |
   | Knowledge Server | 8002 |
   | KWDB MCP | 8003 |
   | KGA Vis | 8004 |

3. 编辑docker-compose.yaml文件【可选】

   配置文件如下：

    ```yaml
    version: "3.9"
    services:
      postgres:
        image: postgres:16.13-alpine3.22
        container_name: kga-postgres
        restart: unless-stopped
        environment:
          POSTGRES_USER: kgaadmin
          POSTGRES_PASSWORD: kga_2026
          POSTGRES_DB: kgadb
        ports:
          - "${POSTGRES_PORT:-5432}:5432"
        volumes:
          - /KAT/3.3.0/data/postgres:/var/lib/postgresql/data
        healthcheck:
          test: ["CMD-SHELL", "pg_isready -U kgaadmin -d kgadb"]
          interval: 5s
          timeout: 5s
          retries: 5

      kga-server:
        image: kga-server:latest
        container_name: kga-server
        restart: unless-stopped
        depends_on:
          postgres:
            condition: service_healthy
        environment:
          #LOG_LEVEL: YOUR_LOG_LEVEL:"ERROR"/"WARNING"/"INFO"/"DEBUG", default is "WARN"
          LOG_LEVEL: WARNING
          POSTGRES_HOST: localhost  # 添加这个环境变量，因为使用 network_mode: host
          POSTGRES_PORT: ${POSTGRES_PORT:-5432}  # 添加这个环境变量，用于 entrypoint.sh 脚本
          DATABASE_URL: kgaadmin:kga_2026@localhost:${POSTGRES_PORT:-5432}/kgadb
          KWDB_CMD_MCP_SERVER_SSE_READ_TIMEOUT: 300
          # LANGCHAIN_TRACING: YOUR_LANGCHAIN_TRACING:"true" or "false", default is "false"
          LANGCHAIN_TRACING: ${LANGCHAIN_TRACING:-false}
          LANGSMITH_PROJECT: ${LANGSMITH_PROJECT:-kga}
          LANGSMITH_ENDPOINT: ${LANGSMITH_ENDPOINT:-https://api.smith.langchain.com}
          LANGSMITH_API_KEY: ${LANGSMITH_API_KEY:-}
          KNOWLEDGE_API_URL: http://117.73.9.174:8001/proxy/knowledge
          KNOWLEDGE_BASE_SERVER_HOST: localhost
          KNOWLEDGE_BASE_SERVER_PORT: ${KNOWLEDGE_BASE_SERVER_PORT:-8002}
          KWDB_MCP_SERVER_HOST: localhost
          KWDB_MCP_SERVER_PORT: ${KWDB_MCP_SERVER_PORT:-8003}
          API_PORT: ${API_PORT:-8000}
          AGENT_PORT: ${AGENT_PORT:-8123}
          # KWDB 数据库证书文件存储目录，默认值为 /app/data/certs
          CERTS_BASE_DIR: /app/data/certs
          OAUTH_CLIENT_ID: ${OAUTH_CLIENT_ID}
          OAUTH_CLIENT_SECRET: ${OAUTH_CLIENT_SECRET}
          TRUSTED_HOSTS: ${TRUSTED_HOSTS:-localhost,127.0.0.1}
          FRONTEND_ORIGIN: ${FRONTEND_ORIGIN:-http://localhost:3000}
        network_mode: host
        volumes:
          - ${KGA_DATA_DIR:-./data}:/app/data
          - ${KGA_DATA_DIR:-./data}/inspection-reports:/app/resources/tmp/kaiwudb-inspection

      kga-ui:
        image: kga-ui:latest
        container_name: kga-ui
        restart: unless-stopped
        network_mode: host
        environment:
          PORT: ${UI_PORT:-3000}
          COPILOT_URL: ${COPILOT_URL:-http://localhost:8123}
          BACKEND_URL: ${BACKEND_URL:-http://localhost:8000}
          KAIWUDB_CLIENT_ID: ${KAIWUDB_CLIENT_ID}

      # 🚀 新增的容器服务
      kga-vis:
        image: kga-vis:3.3.0
        container_name: kga-vis
        restart: unless-stopped
        ports:
        - "${KGA_VIS_PORT:-8004}:3100"
    ```

    参数说明

      - `postgres.image`：PostgreSQL 的镜像名字。
      - `kat-ui.container_name`：自定义 ：PostgreSQL 的容器名称。
      - `postgres.environment`：PostgreSQL 数据库的环境变量。
        - `POSTGRES_USER`：PostgreSQL 用户名，默认为 `katadmin`。
        - `POSTGRES_PASSWORD`：PostgreSQL 用户密码，默认为 `kat_2026`。生产环境建议修改为强密码。
        - `POSTGRES_DB`：KAT 元数据库名称，默认为 `katdb`。
      - `postgres.ports`：PostgreSQL 服务的端口映射配置。
      - `postgres.volumes`：PostgreSQL 数据目录的映射路径。
      - `postgres.healthcheck`：PostgreSQL 服务的健康检查配置。`kat-server` 在 PostgreSQL 健康检查通过后启动。
      - `kga-server.image`：KWDB Agent Server 的镜像名称。
      - `kga-server.container_name`：自定义 KWDB Agent Server 的容器名称。
      - `kat-server.restart`：KWDB Agent Server 的重启方式。
      - `kat-server.depends_on`：配置 `kat-server` 在 `postgres` 服务健康检查通过后启动。
      - `kat-server.environment`：KWDB Agent Server 支持的环境变量。用户可根据实际环境按需修改以下环境变量。
        - `LOG_LEVEL`：日志级别，支持设置为 `ERROR`、`WARNING`、`INFO`、或 `DEBUG` 选项，默认为 `WARNING` 。
        - `POSTGRES_HOST`：使用 network_mode: host。
        - `DATABASE_URL`：KAT 元数据库的连接信息，格式为 `用户名:密码@主机:端口/数据库名`。该参数取值需要与 `postgres.environment` 中 `POSTGRES_USER`、`POSTGRES_PASSWORD`、`POSTGRES_DB` 的取值保持一致。
        - `KWDB_CMD_MCP_SERVER_SSE_READ_TIMEOUT`: KWDB CMD Server连接超时时间，默认300。
        - `LANGCHAIN_TRACING`：配置是否开启 LangChain 链路追踪。支持设置为 `true` 或 `false`。
        - `LANGSMITH_PROJECT`：待追踪的项目名称。
        - `LANGSMITH_ENDPOINT`：LangSmith 收集过程数据的 API 地址。默认设置为 `https://api.smith.langchain.com`。
        - `LANGSMITH_API_KEY`：LangSmith API 密钥。
        - `KNOWLEDGE_API_URL`：KWDB 知识库的 API 地址，默认设置为 `http://117.73.9.174:8001/proxy/knowledge`。
        - `KNOWLEDGE_BASE_SERVER_HOST`：知识库 MCP Server 的主机地址，默认为 `localhost`。
        - `KNOWLEDGE_BASE_SERVER_PORT`：知识库 MCP Server 的端口，默认为 `8002`。
        - `KWDB_MCP_SERVER_HOST`：KWDB MCP Server 的主机地址，默认为 `localhost`。
        - `KWDB_MCP_SERVER_PORT`：KWDB MCP Server 的端口，默认为 `8003`。
        - `API_PORT`：KGA API 端口，默认为 `8000`。
        - `AGENT_PORT`：KWDB Agent 端口，默认为 `8123`。
        - `CERTS_BASE_DIR`：证书文件目录，默认为 `/app/data/certs`。
        - `OAUTH_CLIENT_ID`:SSO 返回的客户端 ID，由 setup.sh 自动写入。
        - `OAUTH_CLIENT_SECRET`: SSO 返回的客户端密钥，由 setup.sh 自动写入。
        - `TRUSTED_HOSTS`：可信主机列表，多个主机用英文逗号分隔。生产环境建议配置为实际域名，例如 `your-domain.com,www.your-domain.com`。如果服务器没有域名，填写 IP 地址和 localhost，例如 `localhost,127.0.0.1,<主机IP>`。
        - `FRONTEND_ORIGIN`：前端页面的访问地址。生产环境建议配置为实际域名，例如 `http://your-domain.com:3000`。如果服务器没有域名，填写实际 IP 地址，例如 `http://<主机IP>:3000`。
      - `kat-server.network_mode`: 配置 KWDB Agent Server 的网络访问模式。支持设置为 `host`，表示 KWDB Agent Server 容器直接使用宿主机的网络配置，而无需创建独立的虚拟网络环境。
      - `kat-server.volumes`：数据库的映射目录和报告存放目录。
      - `kat-ui.image`：KWDB Agent UI 的镜像名称。
      cc
      - `kat-ui.restart`：KWDB Agent UI 的重启方式。
      - `kat-ui.network_mode`: 配置 KWDB Agent UI 的网络访问模式。该参数取值需要与 `kat-server.network_mode` 参数的取值保持一致。
      - `kat-ui.environment`：KWDB Agent UI 支持的环境变量。用户可根据实际环境按需修改以下环境变量。
        - `COPILOT_URL`：KWDB Agent Server Copilot 服务的地址。
        - `BACKEND_URL`：KWDB Agent Server API 服务的地址。
        - `KAIWUDB_CLIENT_ID`：与 `OAUTH_CLIENT_ID` 相同。
      - `kat-vis.image`：KWDB Agent VIS 的镜像名称。
      - `kat-vis.container_name`：自定义 KWDB Agent VIS 的容器名称。
      - `kat-vis.restart`：KWDB Agent VIS 的重启方式。
      - `kat-vis.ports`：可选参数，KWDB Agent VIS 服务的端口映射配置，默认为 `8004`。
  
### 首次完整部署

    执行 `bash setup.sh` 命令进行首次完整部署。

   （1）端口检查：检查 KGA 使用的8个端口是否被占用，如果默认端口已被占用，会自动分配到 8005 以上的可用端口。

   ::: warning 说明
   如果某些端口被占用，脚本会给出提示（如 `端口 3000 (KGA UI) 已被占用，自动分配端口 8010`）。
   :::

   （2）获取本机IP
   脚本自动收集 localhost、内网 IP 和公网 IP，用于构建 OAuth 回调地址。用户无需手动操作。

   （3）输入 InitialAccessToken

   脚本会提示你输入 InitialAccessToken。获取方式：

   1. 登录 KaiwuDB Web 控制台（`https://www.kaiwudb.com`）
   2. 进入 **SSO 设置** 页面
   3. 创建一个 InitialAccessToken
   4. 将 Token 粘贴到终端

  ::: warning 说明
   如果某些端口被占用，脚本会给出提示（如 `端口 3000 (KGA UI) 已被占用，自动分配端口 8010`）。
   :::

   （4）自动注册 OAuth 客户端

   脚本使用上一步的 Token 调用 KaiwuDB SSO 注册接口，自动注册名为 "KGA" 的 OAuth 客户端。注册成功后返回 `client_id` 和 `client_secret`。

   （5）确认 URL 配置

   脚本会询问两个 URL，直接回车即可使用默认值：

  | 变量 | 默认值 | 何时需要修改 |
  |------|--------|-------------|
  | `COPILOT_URL` | `http://localhost:8123` | 前端与 Agent 不在同一台机器时 |
  | `BACKEND_URL` | `http://localhost:8000` | 前端与 API 不在同一台机器时 |

  ::: warning 说明
   如果通过命令行参数指定了 `--copilot-url` 或 `--backend-url`，此步会使用传入的值，不再询问。
   :::

  （6）确认数据目录

   脚本会提示确认数据存储目录，默认 `./data`（项目根目录下的 `data/` 文件夹）。
   ::: warning 说明
   该目录用于持久化 PostgreSQL 数据、SSL 证书和巡检报告，建议不要使用临时目录
   :::

  （7）确认配置并写入 .env

   脚本展示完整配置摘要（端口分配、URL、OAuth、安全配置等），用户确认后：

   1. 询问是否将配置写入 `.env` 文件（推荐写入）
   2. 写入成功后自动执行 `docker compose up -d`
   3. 所有服务启动完成


## 访问 KGA

::: warning 说明
对于 Chrome 浏览器，建议使用 Chrome 110 及以上版本的浏览器。
:::

成功启动 KGA 后，用户即可通过 `http://localhost:3000/` 访问 KAT。