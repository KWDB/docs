---
title: Telegraf 读写数据
id: telegraf
---

# Telegraf 读写数据

[Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) 是一款基于插件化的开源指标收集工具。KWDB 支持通过 RESTful API 将 Telegraf 收集的数据同步写入到 KWDB 数据库。KWDB RESTful API 提供 Telegraf Insert 接口，该接口通过发送 HTTP 请求将 InfluxDB Line 格式的 Telegraf 数据以无模式方式写入 KWDB 时序库。用户无需提前建表，即可通过该接口完成建表、字段添加和数据写入等操作。有关 Telegraf Insert API 接口的请求信息，参见 [Telegraf Insert 接口](../connect-kaiwudb/connect-restful-api.md#telegraf-insert-接口)。

::: warning 说明

用户通过 Telegraf Insert 接口将 InfluxDB Line 协议格式的 Telegraf 数据以无模式方式写入 KWDB 时序库时，需要拥有相应语句的执行权限或者是 admin 角色的成员。
:::

如需将 Telegraf 的数据写入到 KWDB，用户需要在 Telegraf 配置文件（`telegraf.conf`）的 `[[outputs.http]]` 区域配置接口的节点、认证信息、数据格式，如下所示：

```toml
[[outputs.http]]
  ## URL is the address to send metrics to
  url = "https://your-host-ip:port/restapi/telegraf?db=db1"

  ## Timeout for HTTP message
  timeout = "5s"

  ## HTTP method, one of: "POST" or "PUT"
  method = "POST"

  ## Custom HTTP headers for authroization
  ## The format is "Authorization = Basic <base64(username:password)>" 
  headers = { "Authorization" = "Basic cm9vdDprd2RicGFzc3dvcmQ=" }

  ## Data format to output.
  data_format = "influx"
```

有关 Telegraf 配置文件的更多详细信息，参见 [Telegraf 官方文档](https://docs.influxdata.com/telegraf/v1/configuration/)。