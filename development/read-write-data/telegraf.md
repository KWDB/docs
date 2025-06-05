---
title: Telegraf 读写数据
id: telegraf
---

# Telegraf 读写数据

[Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) 是一款基于插件化的开源指标收集工具。KWDB 提供了专用的 RESTful API 接口，支持将 Telegraf 收集的数据直接写入 KWDB 数据库。该接口接收符合 InfluxDB Line Protocol 格式的数据，并通过标准 HTTP 请求完成数据传输。更多接口相关的信息，参见 [Telegraf 接口](../connect-kaiwudb/restful-api/connect-restful-api.md#telegraf-接口)。

::: warning 说明

- 发送 `Telegraf` API 请求的用户，需要有目标表的 `INSERT` 权限。
- 使用 `Telegraf` API 向 KWDB 时序库中写入数据之前，用户需要根据 Telegraf 数据及数据顺序提前在 KWDB 数据库创建好相应的时序表。
  :::

如需将 Telegraf 的数据写入到 KWDB，用户需要在 Telegraf 配置文件（`telegraf.conf`）的 `[[outputs.http]]` 区域配置 KWDB Telegraf 接口的节点、认证信息、数据格式，如下所示：

```toml
[[outputs.http]]
  ## URL of the KWDB RESTful endpoint
  ## Replace "your-host-ip:port" with your KWDB host and port
  ## The "db" parameter specifies the target database
  url = "https://your-host-ip:port/restapi/telegraf?db=db1"

  ## Timeout for HTTP message
  timeout = "5s"

  ## HTTP method to use: "POST" or "PUT"
  method = "POST"

  ## HTTP headers for authorization
  ## Format: "Authorization = Basic <base64(username:password)>"
  headers = { "Authorization" = "Basic cm9vdDprd2RicGFzc3dvcmQ=" }

  ## Output data format (must be "influx")
  data_format = "influx"
```

有关 Telegraf 配置文件的更多详细信息，参见 [Telegraf 官方文档](https://docs.influxdata.com/telegraf/v1/configuration/)。