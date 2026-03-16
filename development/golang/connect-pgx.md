---
title: pgx
id: connect-pgx
---

# 使用 pgx 驱动连接 KWDB

pgx 是用 Go 语言编写的 PostgreSQL 驱动和工具包，提供了高性能的低级接口，支持用户直接利用 PostgreSQL 的特性。pgx 还包含一个适配器，与标准的数据库或 SQL 接口兼容，方便开发者进行数据库操作。

KWDB 支持用户通过 pgx 驱动连接数据库，并执行创建、插入和查询操作。本示例演示了如何使用 Go 语言通过 pgx 驱动连接 KWDB。


## 前提条件

- 安装和运行 KWDB 数据库、配置数据库认证方式、创建数据库。
- 创建具有表级别及以上操作权限的用户。
- 已安装 Go 1.16 及以上版本。

## 配置示例

1. 创建 `go.mod` 文件。

2. 设置 Go 代理并下载依赖。

    ```bash
    go env -w GOPROXY=https://goproxy.cn
    go mod tidy
    ```

3. 创建名为 `main.go` 的文件。

    ```go
    package main

    import (
        "context"
        "fmt"
        "log"
        "time"

        "github.com/jackc/pgx/v5"
    )

    func main() {
        // 使用账号密码连接
        url := fmt.Sprintf("postgresql://%s:%s@%s/%s", "test", "KWdb!2022", "127.0.0.1:26257", "defaultdb")

        // 或者使用证书连接
        // url := fmt.Sprintf("postgresql://%s@%s/%s?sslmode=verify-full&sslrootcert=%s&sslcert=%s&sslkey=%s",
        //     "root", "127.0.0.1:26257", "defaultdb",
        //     "/home/inspur/src/gitee.com/kwbasedb/install/certs/ca.crt",
        //     "/home/inspur/src/gitee.com/kwbasedb/install/certs/client.root.crt",
        //     "/home/inspur/src/gitee.com/kwbasedb/install/certs/client.root.key")

        config, err := pgx.ParseConfig(url)
        if err != nil {
            log.Fatalf("error parsing connection configuration: %v", err)
        }

        config.RuntimeParams["application_name"] = "sample_application_gopgx"
        conn, err := pgx.ConnectConfig(context.Background(), config)
        if err != nil {
            log.Fatalf("error connecting to database: %v", err)
        }
        defer conn.Close(context.Background())

        // 创建时间序列数据库
        _, err = conn.Exec(context.Background(), "CREATE TS DATABASE db_TimeSeries")
        if err != nil {
            log.Fatalf("error creating database: %v", err)
        }

        // 创建表
        _, err = conn.Exec(context.Background(), "CREATE TABLE db_TimeSeries.table1 (" +
            "k_timestamp timestamp NOT NULL, " +
            "voltage double, " +
            "current double, " +
            "temperature double " +
            ") TAGS ( " +
            "number int NOT NULL) " +
            "PRIMARY TAGS(number);")
        if err != nil {
            log.Fatalf("error creating table: %v", err)
        }

        // 插入数据
        _, err = conn.Exec(context.Background(), "INSERT INTO db_TimeSeries.table1 " +
            "VALUES (" +
            "'2024-07-01 10:00:00', " +
            "220.0, 3.0, 20.5, " +
            "123);")
        if err != nil {
            log.Fatalf("error inserting data: %v", err)
        }

        // 查询数据
        rows, err := conn.Query(context.Background(), "SELECT * from db_TimeSeries.table1")
        if err != nil {
            log.Fatalf("error querying data: %v", err)
        } else {
            for rows.Next() {
                values, err := rows.Values()
                if err != nil {
                    log.Fatal("error while iterating dataset")
                }
                timestamp := values[0].(time.Time)
                voltage := values[1].(float64)
                current := values[2].(float64)
                temperature := values[3].(float64)
                number := values[4].(int32)
                log.Println("[k_timestamp:", timestamp, ", voltage:", voltage, ", current:", current, ", temperature:", temperature, ", number:", number, "]")
            }
        }
    }
    ```

4. 执行程序。

    ```bash
    go run .
    ```