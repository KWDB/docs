---
title: Npgsql
id: connect-npgsql

---

# Connect to KWDB Using the Npgsql Driver

Npgsql is an open-source ADO.NET data provider specifically designed for PostgreSQL, enabling developers to access PostgreSQL database servers from applications written in C#, Visual Basic, F#, and other .NET languages.

KWDB is a PostgreSQL-compatible database system that fully supports connections via the Npgsql driver. This compatibility allows developers to seamlessly perform database operations including creating tables, inserting data, and executing queries.

This section demonstrates how to connect to and interact with KWDB using the Npgsql driver in a .NET environment on Windows 11.

## Prerequisites

- [.NET 6.0](https://dotnet.microsoft.com/en-us/download/dotnet/6.0) and [Visual Studio 2022](https://visualstudio.microsoft.com/vs/) installed.
- KWDB installed and running with:
  - Properly configured database authentication
  - A database created for your connection
  - A user with appropriate privileges on tables or higher

## Configuration Example

This example assumes that a relational database `bank` has been created in KWDB.

1. Create a new .NET project:

   ```bash
   dotnet new console -o kaiwudb-test-app
   ```

2. Navigate to the project directory and install the required package:

   ```bash
   cd kaiwudb-test-app
   dotnet add package Npgsql
   ```

3. Edit the auto-generated `Program.cs` file and replace its content with the following example code:

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
   
           // Create a standard relational table "accounts"
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
   
           // Create a time-series database.
           using (var cmd = new NpgsqlCommand("CREATE TS DATABASE db_TimeSeries", conn))
           {
           cmd.ExecuteNonQuery();
           }
   
           // Create a time-series table
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
   
           // Insert data into the time-series table
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

4. Ensure your project file `kaiwudb-test-app.csproj` includes the Npgsql dependency:

   ```XML
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

5. Execute the program:

   ```bash
   dotnet run
   ```