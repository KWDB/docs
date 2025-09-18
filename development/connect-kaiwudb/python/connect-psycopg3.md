---
title: Psycopg 3
id: connect-psycopg3
---

# 使用 Psycopg 3 连接 KWDB

Psycopg 是最受欢迎的 PostgreSQL 数据库适配器，专为 Python 编程语言而设计。Psycopg 完全遵循 Python DB API 2.0 规范，支持线程安全，允许多个线程共享同一连接，特别适合高并发和多线程的应用场景。

KWDB 支持用户通过 Psycopg 3 连接数据库，并执行创建、插入和查询操作。本示例演示了如何通过 Psycopg 3 驱动连接和使用 KWDB。

本示例使用的 Python 版本为 Python 3.10。

## 前提条件

- 安装 Python 3.10。
- 安装和运行 KWDB 数据库、配置数据库认证方式、创建数据库。
- 创建具有表级别及以上操作权限的用户。

## 配置示例

以下示例假设已在 KWDB 中创建时序库 `db_TimeSeries`。

1. 安装 Psycopg 3。

    ```bash
    pip3 install "psycopg[binary]"
    ```

2. 创建名为 `example-psycopg3-app.py` 的 Python 文件，并将以下示例代码复制到文件中：

    ```python
    #!/usr/bin/env python3
    # -*- coding: UTF-8 -*-

    import psycopg


    def main():
        url = "postgresql://test:KWdb%212022@127.0.0.1:26257/defaultdb"
        # for secure connection mode
        # url = "postgresql://root@127.0.0.1:26257/defaultdb"
        # url += "?sslrootcert=D:\\Tools\\test\\example-app-c\\example-app-cpp\\ca.crt"
        # url += "&sslcert=D:\\Tools\\test\\example-app-c\\example-app-cpp\\client.root.crt"
        # url += "&sslkey=D:\\Tools\\test\\example-app-c\\example-app-cpp\\client.root.key"
        print(url)
        try:
            con = psycopg.connect(url, autocommit=True)
            print("Connected!")
            cur = con.cursor()
        except psycopg.Error as e:
            print(f"Failed to connect to Kaiwudb: {e}")

        sql = "CREATE TABLE db_TimeSeries.table1 \
            (k_timestamp timestamp NOT NULL, \
            voltage double, \
            current double, \
            temperature double \
            ) TAGS ( \
            number int NOT NULL) \
            PRIMARY TAGS(number)"
        try:
            cur.execute(sql)
        except psycopg.Error as e:
            print(f"Failed to create table: {e}")

        sql = "INSERT INTO db_TimeSeries.table1  \
            VALUES ('2024-07-01 10:00:00', 220.0, 3.0, 20.5,123)"
        try:
            cur.execute(sql)
        except psycopg.Error as e:
            print(f"Failed to insert data: {e}")

        sql = "SELECT * from db_TimeSeries.table1"
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                print(f"k_timestamp: {row[0]}, voltage: {row[1]}, current: {row[2]}, temperature: {row[3]}, number: {row[4]}")
        except psycopg.Error as e:
            print(f"Failed to insert data: {e}")


        cur.close()
        con.close()
        return


    if __name__ == "__main__":
        main()
    ```

3. 执行示例程序。

    ```bash
    python3 example-psycopg3-app.py
    ```