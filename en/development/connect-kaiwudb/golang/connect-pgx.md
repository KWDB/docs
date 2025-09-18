---
title: pgx
id: connect-pgx

---

# Connect to KWDB Using the pgx Driver

pgx is a high-performance PostgreSQL driver and toolkit written in Go. It provides a direct interface for accessing PostgreSQL-specific features and includes an adapter compatible with standard database/sql interface.

Since KWDB offers PostgreSQL compatibility, you can leverage the pgx driver to perform database operations such as creating tables, inserting data, and executing queries.

This section demonstrates how to connect to KWDB using the pgx driver and perform basic time-series database operations.

## Prerequisites

- Go version 1.16 or higher installed.
- KWDB installed and running with:
  - Properly configured database authentication
  - A database created for your connection
  - A user with appropriate privileges on tables or higher

## Configuration Example

1. Create a `go.mod` file for your project.

2. Set the Go proxy (if required) and download the necessary dependencies:

   ```bash
   go env -w GOPROXY=https://goproxy.cn
   go mod tidy
   ```

3. Create a file named `main.go` with the following code:

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
       // Connect using username and password
       url := fmt.Sprintf("postgresql://%s:%s@%s/%s", "test", "KWdb!2022", "127.0.0.1:26257", "defaultdb")
   
       // Alternatively, connect using certificates
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
   
       // Create a time-series database
       _, err = conn.Exec(context.Background(), "CREATE TS DATABASE db_TimeSeries")
       if err != nil {
           log.Fatalf("error creating database: %v", err)
       }
   
       // Create a time-series table
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
   
       // Insert data
       _, err = conn.Exec(context.Background(), "INSERT INTO db_TimeSeries.table1 " +
           "VALUES (" +
           "'2024-07-01 10:00:00', " +
           "220.0, 3.0, 20.5, " +
           "123);")
       if err != nil {
           log.Fatalf("error inserting data: %v", err)
       }
   
       // Query data
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

4. Run the program:

   ```bash
   go run .
   ```