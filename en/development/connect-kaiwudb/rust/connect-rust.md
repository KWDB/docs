---
title: Rust
id: connect-rust
---

# Connect to KWDB Using Rust

Rust is a high-performance, memory-safe programming language with strong concurrency support. This section demonstrates how to connect to KWDB using Rust and Cargo (Rust's official package manager and build system) to perform database operations.

## Prerequisites

- [Rust](https://www.rust-lang.org/tools/install) installed
- KWDB installed and running with:
  - Properly configured database authentication
  - A database created for your connection
  - A user with appropriate privileges on tables or higher

## Configuration Example

1. Create a new Rust project and navigate into the project directory:

    ```bash
    cargo new kaiwudb-demo-rs
    cd kaiwudb-demo-rs
    ```

2. Open the `src/main.rs` file and add the following code:

    ```rust
    use chrono::{DateTime, Utc};
    use openssl::{
        error::ErrorStack,
        ssl::{SslConnector, SslFiletype, SslMethod},
    };
    use postgres::{Client, Error as PgError, NoTls};
    use postgres_openssl::MakeTlsConnector;
    use std::env;

    fn load_ssl() -> Result<MakeTlsConnector, ErrorStack> {
        let mut builder = SslConnector::builder(SslMethod::tls())?;
        builder.set_ca_file("./certs/ca.crt")?;
        builder.set_certificate_file("../../certs/client.root.crt", SslFiletype::PEM)?;
        builder.set_private_key_file("../../certs/client.root.key", SslFiletype::PEM)?;
        return Ok(MakeTlsConnector::new(builder.build()));
    }

    macro_rules! rs_count_print {
        ($sql:expr, $n:expr) => {
            println!("{}\n({} rows)", $sql, $n);
        };
    }

    fn main() -> Result<(), PgError> {
        let conn_str = format!(
            "host={} port={} user={}",
            env::var("DBHOST").unwrap_or(String::from("localhost")),
            env::var("DBPORT")
                .unwrap_or(String::from("26257"))
                .parse::<u16>()
                .unwrap(),
            env::var("DBUSER").unwrap_or(String::from("root"))
        );
        let databases = [["", "db_shig"], ["TS", "ts_shig"]];
        // Create client connection
        let pg_client = if "true" == (env::var("NOSSL").unwrap_or(String::from("false"))) {
            Client::connect(&conn_str, NoTls)
        } else {
            Client::connect(&conn_str, load_ssl().unwrap())
        };
        let mut client = pg_client.unwrap();
        // Clean up any existing databases with the same names
        for db in [["", "db_shig"], ["TS", "ts_shig"]] {
            client.execute(format!("DROP DATABASE IF EXISTS {}", &db[1]).as_str(), &[])?;
            println!("DROP DATABASE {} SUCCESS!", &db[1]);
        }
        // Create databases
        for db in databases {
            client.execute(
                format!("CREATE {} DATABASE {}", &db[0], &db[1]).as_str(),
                &[],
            )?;
            println!("DROP {} DATABASE {} SUCCESS!", &db[0], &db[1]);
        }
        for db in [["", "db_shig"], ["TS", "ts_shig"]] {
            client.execute(format!("DROP DATABASE IF EXISTS {}", &db[1]).as_str(), &[])?;
            println!("DROP DATABASE {} SUCCESS!", &db[1]);
        }
        // Create databases
        for db in [["", "db_shig"], ["TS", "ts_shig"]] {
            client.execute(
                format!("CREATE {} DATABASE {}", &db[0], &db[1]).as_str(),
                &[],
            )?;
            println!("DROP {} DATABASE {} SUCCESS!", &db[0], &db[1]);
        }
        // Create tables
        rs_count_print!(
            "CREATE TABLE ts_shig.t_electmeter",
            client.execute(
                "CREATE TABLE ts_shig.t_electmeter (
            k_timestamp timestamp NOT NULL,
            elect_name char(63) NOT NULL,
            vol_a double NOT NULL,
            cur_a double NOT NULL,
            powerf_a double) ATTRIBUTES (machine_code varchar(64) NOT NULL) 
                            PRIMARY TAGS(machine_code) 
                            retentions 3d activetime 1h 
                            partition interval 1d;",
                &[],
            )?
        );
        rs_count_print!(
            "CREATE TABLE db_shig.factory",
            client.execute(
                "CREATE TABLE db_shig.factory (
            id int2 PRIMARY KEY,
            name varchar(8),
            sub_comp_id int2 NOT NULL
        )",
                &[],
            )?
        );
        // Insert data
        rs_count_print!(
            "INSERT INTO ts_shig.t_electmeter",
            client.execute(
                "INSERT INTO ts_shig.t_electmeter (
            k_timestamp, elect_name, vol_a, cur_a, powerf_a, machine_code) 
            VALUES (now(), $1, $2, $3, $4, $5)",
                &[&"NULL", &299.4_f64, &0.01_f64, &0.01_f64, &"1_2"],
            )?
        );
        rs_count_print!(
            "INSERT INTO ts_shig.t_electmeter",
            client.execute(
                "INSERT INTO ts_shig.t_electmeter (
            k_timestamp, elect_name, vol_a, cur_a, powerf_a, machine_code) 
            VALUES (now(), $1, $2, $3, $4, $5)",
                &[&"a017", &199.4_f64, &0.11_f64, &0.21_f64, &"3_2"],
            )?
        );
        rs_count_print!(
            "INSERT INTO db_shig.factory",
            client.execute(
                "INSERT INTO db_shig.factory (
            id, name, sub_comp_id) VALUES ($1, $2, $3)",
                &[&1_i16, &"12,22FAC", &1_i16],
            )?
        );
        client.batch_execute(
            "INSERT INTO db_shig.factory 
            VALUES (2,'1_1FAC',2),(3,'3_3FAC',3),(99,'99_99FAC',5)",
        )?;
        // Query data
        println!("SELECT ts_shig.t_electmeter");
        client
            .query("SELECT * FROM ts_shig.t_electmeter", &[])
            .map(|rows| {
                for row in &rows {
                    let k_timestamp: DateTime<Utc> = row.get("k_timestamp");
                    let elect_name: String = row.get("elect_name");
                    let vol_a: f64 = row.get("vol_a");
                    let cur_a: f64 = row.get("cur_a");
                    let powerf_a: f64 = row.get("powerf_a");
                    let machine_code: String = row.get("machine_code");
                    println!(
                        "{},{},{},{},{},{}",
                        k_timestamp, elect_name, vol_a, cur_a, powerf_a, machine_code
                    );
                }
                println!("({} rows)", rows.len());
            })?;
        println!("SELECT db_shig.factory");
        client
            .query(
                "SELECT name, sub_comp_id FROM db_shig.factory WHERE id=$1",
                &[&1_i16],
            )
            .map(|rows| {
                for row in &rows {
                    let name: String = row.get("name");
                    let sub_comp_id: i16 = row.get("sub_comp_id");
                    println!("{},{}", name, sub_comp_id);
                }
                println!("({} rows)", rows.len());
            })?;
        // Update data
        rs_count_print!(
            "UPDATE db_shig.factory",
            client.execute(
                "UPDATE db_shig.factory SET name=$1 WHERE id=$2",
                &[&"99UPDATE", &99_i16],
            )?
        );
        // Delete data
        rs_count_print!(
            "DELETE FROM db_shig.factory",
            client.execute("DELETE FROM db_shig.factory WHERE id=$1", &[&3_i16],)?
        );
        // Drop tables
        client.batch_execute("DROP TABLE db_shig.factory")?;
        rs_count_print!(
            "DROP TABLE ts_shig.t_electmeter",
            client.execute("DROP TABLE ts_shig.t_electmeter", &[],)?
        );
        // Drop databases
        for db in &databases {
            let drop_sql = format!("DROP DATABASE {}", &db[1]);
            rs_count_print!(&drop_sql, client.execute(&drop_sql, &[])?);
        }
        Ok(())
    }
    ```

3. In the project root directory, update the `Cargo.toml` file with the following content:

    ```toml
    [package]
    name = "kaiwudb-demo-rs"
    version = "0.1.0"
    edition = "2021"

    [dependencies]
    chrono = "0.4.38"
    openssl = "0.10.66"
    postgres = { version = "0.19.8", features = ["with-chrono-0_4"] }
    postgres-openssl = "0.5.0"
    ```

4. Build and run your project:

    ```bash
    cargo build
    cargo run
    ```
