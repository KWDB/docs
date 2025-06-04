---
title: Telegraf
id: telegraf
---

# Telegraf

[Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) is an open-source, plugin-driven server agent for collecting, processing, and reporting metrics from systems, applications, and IoT devices. KWDB supports ingesting Telegraf-collected data through a dedicated RESTful API endpoint that accepts the InfluxDB Line Protocol format. For more information about the KWDB RESTful API for Telegraf, see [Telegraf Endpoint](../connect-kaiwudb/restful-api/connect-restful-api.md#telegraf-endpoint).

::: warning Note

- Users must have `INSERT` privileges on the target table to send data via the Telegraf endpoint.
- The target time-series table must be created in KWDB before sending data.
- The table structure and field order must match the incoming Telegraf data.

:::

To write Telegraf data into KWDB, configure the `[[outputs.http]]` section in your Telegraf configuration file (`telegraf.conf`) as follows:

```toml
[[outputs.http]]
  ## KWDB RESTful API endpoint URL
  ## Replace "your-host-ip:port" with your KWDB host and port
  ## Specify the target database with the "db" parameter
  url = "https://your-host-ip:port/restapi/telegraf?db=db1"

  ## Timeout for HTTP message
  timeout = "5s"

  ## HTTP method to use: "POST" or "PUT"
  method = "POST"

  ## Authentication headers
  ## Format: "Authorization = Basic <base64(username:password)>"
  headers = { "Authorization" = "Basic cm9vdDprd2RicGFzc3dvcmQ=" }

  ## Output data format (must be set to "influx")
  data_format = "influx"
```

Parameters:

| Parameter | Description |
|-----------|-------------|
| `url` | KWDB RESTful API endpoint URL with the target database specified in the `db` parameter|
| `timeout` | Maximum duration to wait for HTTP response completion|
| `method` | HTTP method (`POST` recommended) |
| `headers` | Authentication headers using Base64-encoded credentials (username:password)|
| `data_format` | Data format, must be set to `"influx"` |

For more information on the Telegraf configuration options, see the [official Telegraf documentation](https://docs.influxdata.com/telegraf/v1/configuration/).