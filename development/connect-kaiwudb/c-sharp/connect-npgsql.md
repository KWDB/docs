---
title: Npgsql
id: connect-npgsql
---

# 使用 Npgsql 驱动连接 KWDB

Npgsql 是专为 PostgreSQL 设计的开源 ADO.NET 数据提供程序，支持用户使用 C#、Visual Basic 和 F# 编写的程序访问 PostgreSQL 数据库服务器。

KWDB 支持用户通过 Npgsql 驱动连接数据库，并执行创建、插入和查询操作。本示例演示了如何在 .NET 框架中，通过 Npgsql 驱动连接和使用 KWDB。

本示例使用的操作环境为 Windows 11。

## 前提条件

- 安装 [.NET 6.0](https://dotnet.microsoft.com/zh-cn/download/dotnet/6.0) 和 [Visual Studio 2022](https://visualstudio.microsoft.com/zh-hans/vs/)。
- 安装和运行 KWDB 数据库、配置数据库认证方式、创建数据库。
- 创建具有表级别及以上操作权限的用户。

## 配置示例

以下示例假设已在 KWDB 中创建关系库 `bank`。

1. 新建一个 .NET 项目。

    ```bash
    dotnet new console -o kaiwudb-test-app
    ```

2. 进入项目目录并添加 Npgsql 包。

    ```bash
    cd kaiwudb-test-app
    dotnet add package Npgsql
    ```

3. 编辑自动生成的 `Program.cs` 文件，将内容替换为以下示例代码：

    ```csharp
    // See https://aka.ms/new-console-template for more information
    using System;
    using System.Data;
    using System.Net.Security;
    using Npgsql;

    namespace Example
    {
    class MainClass
    {
        static void Main(string[] args)
        {
        var connStringBuilder = new NpgsqlConnectionStringBuilder();
        connStringBuilder.Host = "172.18.139.126";
        connStringBuilder.Port = 26257;
        // for secure connection mode
        // connStringBuilder.SslMode = SslMode.VerifyCA;
        // connStringBuilder.RootCertificate = <file_path_of_root_ca_certificate file>;
        // connStringBuilder.SslCertificate = <file_path_of_user_certificate_file>;
        // connStringBuilder.SslKey = <file_path_of_user_certificate_key>;
        connStringBuilder.Username = "test";
        connStringBuilder.Password = "123";
        connStringBuilder.Database = "bank";
        Simple(connStringBuilder.ConnectionString);
        }

        static void Simple(string connString)
        {
        using (var conn = new NpgsqlConnection(connString))
        {
            conn.Open();

            // Create the "accounts" table.
            using (var cmd = new NpgsqlCommand("CREATE TABLE IF NOT EXISTS accounts (id INT PRIMARY KEY, balance INT)", conn))
            {
            cmd.ExecuteNonQuery();
            }
            // Insert two rows into the "accounts" table.
            using (var cmd = new NpgsqlCommand())
            {
            cmd.Connection = conn;
            cmd.CommandText = "UPSERT INTO accounts(id, balance) VALUES(@id1, @val1), (@id2, @val2)";
            cmd.Parameters.AddWithValue("id1", 1);
            cmd.Parameters.AddWithValue("val1", 1000);
            cmd.Parameters.AddWithValue("id2", 2);
            cmd.Parameters.AddWithValue("val2", 250);
            cmd.ExecuteNonQuery();
            }

            // Print out the balances.
            System.Console.WriteLine("Initial balances:");
            using (var cmd = new NpgsqlCommand("SELECT id, balance FROM accounts", conn))
            using (var reader = cmd.ExecuteReader())
            while (reader.Read())
                Console.Write("\taccount {0}: {1}\n", reader.GetValue(0), reader.GetValue(1));

            // Create time series database.
            using (var cmd = new NpgsqlCommand("CREATE TS DATABASE db_TimeSeries", conn))
            {
            cmd.ExecuteNonQuery();
            }

            // Create time series table
            using (var cmd = new NpgsqlCommand("CREATE TABLE db_TimeSeries.table1 " + 
                                            "(k_timestamp timestamp NOT NULL, " +
                                            "voltage double, " +
                                            "current double, " +
                                            "temperature double " +
                                            ") TAGS ( " +
                                            "number int NOT NULL) " +
                                            "PRIMARY TAGS(number); ", conn))
            {
            cmd.ExecuteNonQuery();
            }

            // Insert data into time series table
            using (var cmd = new NpgsqlCommand("INSERT INTO db_TimeSeries.table1 " +
                                            "VALUES ( " +
                                            "'2024-07-01 10:00:00', " +
                                            "220.0, 3.0, 20.5, " +
                                            "123); ", conn))
            {
                cmd.ExecuteNonQuery();
            }

            
            System.Console.WriteLine("Data from time series table db_TimeSeries.table1:");
            using (var cmd = new NpgsqlCommand("SELECT * from db_TimeSeries.table1", conn))
            using (var reader = cmd.ExecuteReader())
            while (reader.Read())
                Console.Write("\tTime: {0}\tvoltage: {1}\tcurrent: {2}\ttemperature: {3}\tnumber: {4}\n", 
                        reader.GetValue(0), reader.GetValue(1), reader.GetValue(2), reader.GetValue(3), reader.GetValue(4));
        }
        }
    }
    }
    ```

4. 检查项目文件 `kaiwudb-test-app.csproj`，确保项目文件包含 Npgsql 依赖项。

    ```xml
    <Project Sdk="Microsoft.NET.Sdk">
        <PropertyGroup>
            <OutputType>Exe</OutputType>
            <TargetFramework>net6.0</TargetFramework>
            <RootNamespace>kaiwudb_test_app</RootNamespace>
            <ImplicitUsings>enable</ImplicitUsings>
            <Nullable>enable</Nullable>
        </PropertyGroup>
        <ItemGroup>
            <PackageReference Include="Npgsql" Version="8.0.3" />
        </ItemGroup>
    </Project>
    ```

5. 执行示例程序。

    ```bash
    dotnet run
    ```