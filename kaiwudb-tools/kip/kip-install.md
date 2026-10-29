---
title: 安装部署
id: kip-install
---

# 安装部署

用户可以在 Windows、MacOS、Linux 平台部署 KIP。本文档介绍如何使用 `setup.sh` 脚本整体部署 KIP。

## 部署 KIP

### 前提条件

- 已[安装](https://docs.docker.com/compose/install/) Docker Compose，且处于运行状态。
- 已安装 `python3`，脚本内部用其解析 JSON 。
- 前往[KaiwuDB软件下载中心](https://www.kaiwudb.com/download?tab=3)申请 KIP Server 、UI、VIS 镜像、InitialAccessToken、`setup.sh`脚本以及 `docker-compose.yaml` 模板文件。

::: warning 说明
- 安装用户为 `root` 用户。`root` 用户在进行部署时无需输入密码。
- `setup.sh` 脚本启动时会自动检查依赖，缺少任何一项都会报错退出。
- （可选）如需以安全模式连接 KaiwuDB 数据库，用户需要生成 CA 证书和密钥、客户端证书和密钥、节点证书和密钥。有关详细信息，参见 [`kwdb cert` 命令参考](../kwbase-cli-tool.md#kwbase-cert)。
:::

### 安装前准备

1. 可以使用 `bash setup.sh --help` 查看支持场景。
   
  | 参数选项  | 说明 |
  |-----------|------|
  | 无参数               | 注册客户端并启动 Docker Compose |
  | `--register-only`   | 仅注册 OAuth，不启动服务 | 
  | `--up`              | 已有配置，直接启动 |  
  | `--shutdown`        | 停止所有服务 | 
  | `--force`           | 强制重新注册 |
  | `--copilot-url=URL` | 设置 COPILOT_URL |
  | `--backend-url=URL` | 设置 BACKEND_URL | 
  | `--initial-access-token=TOKEN` | 设置 InitialAccessToken |

2. 服务默认端口
   
  | 服务 | 默认端口 |
  |------|---------|
  | PostgreSQL       | 5432 |
  | KIP UI           | 3000 |
  | KIP Vis          | 8004 |
  | KWDB MCP         | 8003 |
  | KWDB Agent       | 8123 |
  | Knowledge Server | 8002 |
  | KIP API          | 8000 |

3. 编辑docker-compose.yaml文件【可选】

   配置文件如下：

  ```yaml
  # ============================================================
  # KIP (KaiwuDB Insight Platform) — Docker Compose 部署
  # ============================================================
  # 快速开始：
  #   bash setup.sh              # 交互式向导：注册 OAuth 客户端、生成 .env、启动全部服务
  #   bash setup.sh --up         # 使用已有 .env 直接启动
  #   bash setup.sh --shutdown   # 停止全部服务
  #
  # 说明：
  # - 必填项（数据库口令、加密密钥等）由 setup.sh 自动生成并写入根目录 .env；
  #   手动部署时请参照本文件各环境变量的注释说明自行准备 .env。
  # - 镜像：本文件引用本地镜像 kip-server:latest / kip-ui:latest / kip-vis:latest，启动前需先从镜像分发渠道获取并加载到本机 Docker；镜像未就绪时 docker compose up -d 会因拉不到镜像而失败。
  # - 所有服务日志只进 stdout，不写文件，用 docker logs <容器名> 查看；
  #   下方 x-logging 限制宿主机日志文件体积，长期运行不会占满磁盘。
  # - 端口暴露：postgres、kip-vis，以及 kip-server 内的 API / Agent / 知识库 MCP默认只绑环回地址（127.0.0.1）；
  #   KWDB MCP（8003）未限定监听地址，会绑到宿主机全部网卡，请注意用防火墙或前置反代收敛暴露面。对外提供服务请自行叠加反向代理，不要把数据库等端口直接暴露到局域网。

  # 日志轮换：json-file 驱动默认无限增长，长期运行会把磁盘打满；所有服务共用同一份配置
  x-logging: &default-logging
    driver: json-file
    options:
      max-size: "100m"
      max-file: "5"

  services:
    postgres:
      logging: *default-logging
      image: postgres:16.13-alpine3.22
      container_name: kip-postgres
      restart: unless-stopped
      environment:
        POSTGRES_USER: ${POSTGRES_USER:-kipadmin}
        # 必填，无默认值：缺失时 compose 直接报错退出；setup.sh 会自动生成随机口令
        POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?请设置 POSTGRES_PASSWORD 环境变量}
        POSTGRES_DB: ${POSTGRES_DB:-kipdb}
      ports:
        # 仅绑环回；对外访问请经由反向代理，不要直接把 5432 暴露到局域网
        - "127.0.0.1:${POSTGRES_PORT:-5432}:5432"
      volumes:
        - ${KIP_DATA_DIR:-./data}/postgres:/var/lib/postgresql/data
      healthcheck:
        test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-kipadmin} -d ${POSTGRES_DB:-kipdb}"]
        interval: 5s
        timeout: 5s
        retries: 5

    kip-server:
      logging: *default-logging
      image: kip-server:latest
      container_name: kip-server
      restart: unless-stopped
      depends_on:
        postgres:
          condition: service_healthy
      network_mode: host
      environment:
        # ---- 日志 ----
        # LOG_LEVEL：root logger 级别（critical/error/warning/info/debug/trace，默认 INFO），
        # 同时作用于 API 进程与 Agent 进程
        LOG_LEVEL: ${LOG_LEVEL:-INFO}
        # ACCESS_LOG：uvicorn 访问日志开关，默认关；排查流量/鉴权问题时置 true
        ACCESS_LOG: ${ACCESS_LOG:-false}
        # SQL_ECHO：打印 SQL 语句开关，默认关；排查数据库问题时置 true
        SQL_ECHO: ${SQL_ECHO:-false}

        # ---- 运维与安全旋钮 ----
        # 以下各项均有代码内默认值，缺省即走默认；在 .env 中覆盖后
        # 执行 docker compose up -d 重启容器即可生效
        # 限流总开关：true 表示按会话/IP 的固定窗口限流，默认开；排障时可置 false
        RATE_LIMIT_ENABLED: ${RATE_LIMIT_ENABLED:-true}
        # 数据清理保留期（天）：大工具结果 offload 文件默认 7 天，
        # 图表推荐任务记录默认 30 天，到期自动删除
        LARGE_TOOL_RESULTS_RETENTION_DAYS: ${LARGE_TOOL_RESULTS_RETENTION_DAYS:-7}
        CHART_RECOMMEND_TASK_RETENTION_DAYS: ${CHART_RECOMMEND_TASK_RETENTION_DAYS:-30}
        # 会话空闲超时（分钟）与登录 cookie 有效期（天），默认 120 / 30
        SESSION_IDLE_TIMEOUT_MINUTES: ${SESSION_IDLE_TIMEOUT_MINUTES:-120}
        SESSION_COOKIE_MAX_AGE_DAYS: ${SESSION_COOKIE_MAX_AGE_DAYS:-30}
        # 后台巡检间隔（秒）：异常监控扫描默认 300，语义层存在性巡检默认 3600
        ANOMALY_MONITOR_INTERVAL_SECONDS: ${ANOMALY_MONITOR_INTERVAL_SECONDS:-300}
        SEMANTIC_SYNC_INTERVAL_SECONDS: ${SEMANTIC_SYNC_INTERVAL_SECONDS:-3600}
        # 根因分析超时（秒）：全流程默认 180，单次 LLM 调用默认 90
        ROOT_CAUSE_TIMEOUT_SECONDS: ${ROOT_CAUSE_TIMEOUT_SECONDS:-180}
        ROOT_CAUSE_LLM_TIMEOUT_SECONDS: ${ROOT_CAUSE_LLM_TIMEOUT_SECONDS:-90}
        # 进程内 TTL 缓存（秒）：模型 / 提示词 / MCP 工具目录 / 语义上下文，默认各 60
        # 置 0 即关闭对应缓存，是排查配置不生效类问题的逃生开关
        # 缓存在进程导入时读取，改 .env 后需重启容器才生效
        MODEL_CACHE_TTL_SECONDS: ${MODEL_CACHE_TTL_SECONDS:-60}
        PROMPT_CACHE_TTL_SECONDS: ${PROMPT_CACHE_TTL_SECONDS:-60}
        MCP_TOOLS_CACHE_TTL_SECONDS: ${MCP_TOOLS_CACHE_TTL_SECONDS:-60}
        SEMANTIC_CONTEXT_CACHE_TTL_SECONDS: ${SEMANTIC_CONTEXT_CACHE_TTL_SECONDS:-60}
        # MCP 工具发现阶段（list_tools）的连接超时（秒），默认 10，只约束发现阶段
        MCP_DISCOVERY_TIMEOUT_SECONDS: ${MCP_DISCOVERY_TIMEOUT_SECONDS:-10}
        # 用户库连接池的进程级总上限（跨数据源累计），默认 50
        # PostgreSQL 服务端 max_connections 是硬顶，数据源多时调大前请先确认服务端额度
        USER_DB_POOL_MAX_TOTAL: ${USER_DB_POOL_MAX_TOTAL:-50}

        # ---- 数据库 ----
        # network_mode: host 下容器内 localhost 即宿主机，直连同栈的 postgres 容器
        POSTGRES_HOST: localhost
        # 供 entrypoint 初始化数据库使用（创建用户/库/表），需与 postgres 容器一致
        POSTGRES_PORT: ${POSTGRES_PORT:-5432}
        # 必填：与 postgres 容器的 POSTGRES_PASSWORD 保持一致
        POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?请设置 POSTGRES_PASSWORD 环境变量}
        # 必填：完整 scheme 格式 postgresql+psycopg://<用户>:<口令>@localhost:<端口>/<库名>
        DATABASE_URL: ${DATABASE_URL:?请设置 DATABASE_URL 环境变量，如 postgresql+psycopg://kipadmin:<口令>@localhost:5432/kipdb}
        # 必填：入库凭证（数据源密码、模型 Key 等）的 AES-256 加密密钥，32 字节 base64。
        # 生成：python -c "import secrets,base64;print(base64.b64encode(secrets.token_bytes(32)).decode())"
        # 注意：更换密钥后，用旧密钥加密的存量数据将无法解密
        AES_SECRET_KEY_B64: ${AES_SECRET_KEY_B64:?请设置 AES_SECRET_KEY_B64 环境变量}

        # ---- 链路追踪（可选，不配置则不启用）----
        # auto（默认）按密钥自动判定；langfuse / langsmith 二选一；both 同时上报；none 关闭
        TRACING_PROVIDER: ${TRACING_PROVIDER:-auto}
        # Langfuse：公钥/私钥任一为空即不启用；自建实例请修改 LANGFUSE_BASE_URL
        LANGFUSE_PUBLIC_KEY: ${LANGFUSE_PUBLIC_KEY:-}
        LANGFUSE_SECRET_KEY: ${LANGFUSE_SECRET_KEY:-}
        LANGFUSE_BASE_URL: ${LANGFUSE_BASE_URL:-https://cloud.langfuse.com}
        LANGFUSE_TRACING_ENABLED: ${LANGFUSE_TRACING_ENABLED:-true}
        LANGFUSE_TRACING_ENVIRONMENT: ${LANGFUSE_TRACING_ENVIRONMENT:-production}
        LANGFUSE_TRACE_NAME: ${LANGFUSE_TRACE_NAME:-KIP Agent}
        LANGFUSE_TRACE_TAGS: ${LANGFUSE_TRACE_TAGS:-}
        # LangSmith：开关与 API Key 两项都要配
        LANGSMITH_TRACING: ${LANGSMITH_TRACING:-false}
        LANGSMITH_API_KEY: ${LANGSMITH_API_KEY:-}
        LANGSMITH_ENDPOINT: ${LANGSMITH_ENDPOINT:-https://api.smith.langchain.com}
        LANGSMITH_PROJECT: ${LANGSMITH_PROJECT:-kip}

        # ---- 内置 MCP 服务 ----
        # MCP（Model Context Protocol，模型上下文协议）：Agent 连接外部工具服务的
        # 标准协议。以下 HOST/PORT 是 agent 客户端连接用的地址，服务随本容器启动。
        # 子代理：Agent 内部按职责拆分的专用执行器（kwdb_qa 管知识库、db_sql 管 SQL）
        # 知识库 RAG（检索增强生成）MCP：供 kwdb_qa 子代理检索知识库；只监听环回
        KNOWLEDGE_BASE_SERVER_HOST: ${KNOWLEDGE_BASE_SERVER_HOST:-127.0.0.1}
        KNOWLEDGE_BASE_SERVER_PORT: ${KNOWLEDGE_BASE_SERVER_PORT:-8002}
        # 知识库 API 地址：默认指向 KIP 知识库服务的固定公网端点；
        # 自行部署知识库服务时，可覆盖为自己的地址
        KNOWLEDGE_API_URL: ${KNOWLEDGE_API_URL:-http://117.73.9.174:8001/proxy/knowledge}
        # 知识库 API 的访问令牌：kwdb_qa 子代理检索知识库时必填，未配置则拒绝知识库调用
        AUTH_TOKEN: ${AUTH_TOKEN:-}
        # KWDB 查询 MCP：供 db_sql 子代理执行数据库查询。
        # 注意：该服务未限定监听地址，会绑到宿主机全部网卡，且为无鉴权端点，
        # 请用防火墙或前置反代收敛暴露面
        KWDB_MCP_SERVER_HOST: ${KWDB_MCP_SERVER_HOST:-localhost}
        KWDB_MCP_SERVER_PORT: ${KWDB_MCP_SERVER_PORT:-8003}

        # ---- 服务端口 ----
        API_PORT: ${API_PORT:-8000}
        AGENT_PORT: ${AGENT_PORT:-8123}
        # kip-api 访问 Agent 的地址；显式覆盖时需与 AGENT_PORT 一致（缺省时自动跟随）
        COPILOT_URL: ${COPILOT_URL:-http://127.0.0.1:${AGENT_PORT:-8123}}
        # Agent 并发运行数：同时执行的对话/任务 run 上限，默认 6，可按服务器性能调整
        AGENT_CONCURRENT_RUNS: ${AGENT_CONCURRENT_RUNS:-6}

        # ---- 数据目录 ----
        # KaiwuDB 数据源 SSL 证书存放目录（容器内路径，对应宿主机 ./data/certs）
        CERTS_BASE_DIR: /app/data/certs
        # 用户上传技能的存放目录（位于数据卷内，容器重建不丢失）
        AGENT_SKILLS_DIR: /app/data/user_skills
        # Agent 用户工作区根目录（offload 产物与 conversation_history，按用户隔离）
        # 必须位于共享 resources 根目录之外，否则 filesystem 工具可跨用户读取
        AGENT_WORKSPACE_DIR: /app/data/user_workspace
        # 报告 docx 落盘目录（容器内路径，对应宿主机 ./data/reports）
        REPORT_DIR: ${REPORT_DIR:-/app/data/reports}

        # ---- 整板报告渲染（kip-ui）----
        # PNG 渲染服务地址：network_mode: host 下 127.0.0.1 即宿主机地址，端口跟随 UI_PORT
        REPORT_RENDER_URL: ${REPORT_RENDER_URL:-http://127.0.0.1:${UI_PORT:-3000}}
        # 渲染服务共享密钥：需与 kip-ui 侧同名同值
        # 置空表示渲染端点匿名可达，仅限开发/兼容场景
        # 两侧不一致时，报告中的图会降级为统计表格
        REPORT_RENDER_TOKEN: ${REPORT_RENDER_TOKEN:-}
        # 内置 prompt 与资源目录（镜像内路径）
        BUILTIN_PROMPT_DIR: ${BUILTIN_PROMPT_DIR:-/app/resources}

        # ---- 邮件告警（可选）----
        # 私有 CA 证书（容器内路径）：仅当 SMTP 服务器使用自签证书时设置；
        # 留空则使用系统信任库并强制校验证书。文件缺失/非法会直接报错，不会静默跳过校验
        SMTP_CA_BUNDLE: ${SMTP_CA_BUNDLE:-}
        # SMTP 连接池：单个 SMTP 端点最多缓存的连接数 / 连接空闲多少秒后关闭
        SMTP_POOL_MAX_SIZE: ${SMTP_POOL_MAX_SIZE:-2}
        SMTP_POOL_MAX_IDLE_SECONDS: ${SMTP_POOL_MAX_IDLE_SECONDS:-300}

        # ---- 安全与登录 ----
        # 运行环境：production 时禁用 mock 路由、Cookie 加 secure，并开启启动校验
        # （漏配 OAuth 凭据、或把 AUTH_ENABLED 置 false 都会拒绝启动）；默认 development
        APP_ENVIRONMENT: ${APP_ENVIRONMENT:-development}
        # 登录开关：false 时跳过登录（注入本地合成用户），仅限开发自测；
        # production 下置 false 会被拒绝启动。默认 true
        AUTH_ENABLED: ${AUTH_ENABLED:-true}
        # OAuth 登录客户端凭据：由 setup.sh 自动注册，或从 KaiwuDB 控制台获取；
        # APP_ENVIRONMENT=production 时必须配置，否则容器拒绝启动
        OAUTH_CLIENT_ID: ${OAUTH_CLIENT_ID}
        OAUTH_CLIENT_SECRET: ${OAUTH_CLIENT_SECRET}
        # Host 白名单（TrustedHostMiddleware）与允许的前端来源（CORS），均为逗号分隔
        TRUSTED_HOSTS: ${TRUSTED_HOSTS:-localhost,127.0.0.1}
        FRONTEND_ORIGIN: ${FRONTEND_ORIGIN:-http://localhost:3000}
        # 跳过登录时使用的合成用户 ID（AUTH_ENABLED=false 时生效，仅开发自测）
        SKIP_AUTH_USER_ID: ${SKIP_AUTH_USER_ID:-mock_user}
      volumes:
        - ${KIP_DATA_DIR:-./data}:/app/data

    kip-ui:
      logging: *default-logging
      image: kip-ui:latest
      container_name: kip-ui
      restart: unless-stopped
      network_mode: host
      environment:
        PORT: ${UI_PORT:-3000}
        # 以下两个地址只被容器内的 Next.js 服务端使用（同源代理、鉴权中间件），
        # 浏览器不直连；network_mode: host 下 127.0.0.1 即宿主机地址，
        # 端口分别跟随 AGENT_PORT / API_PORT
        COPILOT_URL: ${COPILOT_URL:-http://127.0.0.1:${AGENT_PORT:-8123}}
        BACKEND_URL: ${BACKEND_URL:-http://127.0.0.1:${API_PORT:-8000}}
        KAIWUDB_CLIENT_ID: ${KAIWUDB_CLIENT_ID}
        # 外部嵌入图表（Grafana iframe 等）的可信域名白名单，逗号分隔；
        # 运行时读取，修改后 docker compose up -d 重启 kip-ui 即生效，无需重建镜像；
        # 留空表示不允许新增外部图表（已有图表仍可显示）
        EXTERNAL_CHART_HOSTS: ${EXTERNAL_CHART_HOSTS:-}
        # 整板报告 PNG 渲染的共享密钥：需与 kip-server 侧同名同值，两侧各读各的 env
        # 置空表示渲染端点匿名可达，仅限开发/兼容场景
        REPORT_RENDER_TOKEN: ${REPORT_RENDER_TOKEN:-}

    # 图表生成 MCP（ECharts）：Agent 的 viz 子代理通过它把查询结果渲染成图表
    kip-vis:
      logging: *default-logging
      image: kip-vis:latest
      container_name: kip-vis
      restart: unless-stopped
      ports:
        # 仅绑环回
        - "127.0.0.1:${KIP_VIS_PORT:-8004}:3100"
  ```
  
### 初始化安装

  执行 `bash setup.sh` 命令进行首次完整部署。

   （1）端口检查：检查 KIP 使用的默认端口是否被占用，如果已被占用，会自动分配到 8005 以上的可用端口。

   ::: warning 说明
   如果某些端口被占用，脚本会给出提示（如 ` 端口 5432 (Postgres) 已被占用，自动分配端口 8005`）。
   :::

   （2）获取本机IP
   脚本自动收集 localhost、内网 IP 和公网 IP，用于构建 OAuth 回调地址。用户无需手动操作。

   （3）输入 InitialAccessToken

   脚本会提示你输入 InitialAccessToken。

  ::: warning 说明
   安装前，随镜像包、脚本等一起获取。
   :::

   （4）自动注册 OAuth 客户端

   脚本使用上一步的 Token，自动注册名为 "KIP" 的 OAuth 客户端。注册成功后返回 `client_id` 和 `client_secret`。

   （5）确认外部图表服务器地址

   脚本提示`请输入 EXTERNAL_CHART_HOSTS []:`，根据实际项目输入对应地址，不需要填写的话直接回车。

  （6）确认数据目录

   脚本会提示`请输入 KIP_DATA_DIR [./data]:`，默认 `./data`（项目根目录下的 `data/` 文件夹）。
   
   ::: warning 说明
   该目录用于持久化 PostgreSQL 数据、SSL 证书等，建议不要使用临时目录
   :::

  （7）确认配置并写入 .env

   脚本展示完整配置摘要（端口分配、URL、OAuth、安全配置等），用户确认后：

   1. 询问是否将配置写入 `.env` 文件（推荐写入）
   2. 写入成功后自动执行 `docker compose up -d`
   3. 所有服务启动完成

## 访问 KIP

::: warning 说明
对于 Chrome 浏览器，建议使用 Chrome 110 及以上版本的浏览器。
:::

成功启动 KIP 后，用户即可通过 `http://localhost:3000/` 访问 KIP。