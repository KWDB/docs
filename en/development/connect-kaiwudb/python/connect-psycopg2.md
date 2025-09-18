---
title: Psycopg2
id: connect-psycopg2
---

# Connect to KWDB Using Psycopg2

Psycopg2 is the most popular PostgreSQL database adapter for Python. It fully complies with the Python DB API 2.0 specification and provides thread safety, allowing multiple threads to share the same connection. This makes it particularly suitable for high-concurrency and multithreaded application scenarios.

KWDB supports connections via Psycopg2, enabling users to perform create, insert, and query operations efficiently. This section demonstrates how to connect to and use KWDB with the Psycopg2 driver.

This example uses Python 3.10.

## Prerequisites

- Python 3.10 installed.
- KWDB installed and running with:
  - Properly configured database authentication
  - A database created for your connection
  - A user with appropriate privileges on tables or higher

## Configuration Example

The following example assumes you have already created a time-series database named `db_TimeSeries` in KWDB.

1. Install Psycopg2 using pip:

    ```bash
    pip3 install psycopg2-binary
    ```

2. Create a Python file named `example-psycopg2-app.py` with the following code:

    ```python
    #!/usr/bin/env python3
    # -*- coding: UTF-8 -*-
    
    import psycopg2


    def main():
        try:
            con = psycopg2.connect(database="defaultdb", user="test", password="KWdb!2022", host="127.0.0.1",port="26257")
            # for secure connection mode
            # con = psycopg2.connect(database="defaultdb", user="root", password="", host="127.0.0.1",
            #                        port="26257", sslmode="verify-ca",
            #                        sslrootcert=<file_path_of_root_ca_certificate file>,
            #                        sslcert=<file_path_of_user_certificate_file>,
            #                        sslkey=<file_path_of_user_certificate_key>)
            print("Connected!")
            con.set_session(autocommit=True)
            cur = con.cursor()
        except psycopg2.Error as e:
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
        except psycopg2.Error as e:
            print(f"Failed to create table: {e}")
    
        sql = "INSERT INTO db_TimeSeries.table1  \
            VALUES ('2024-07-01 10:00:00', 220.0, 3.0, 20.5,123)"
        try:
            cur.execute(sql)
        except psycopg2.Error as e:
            print(f"Failed to insert data: {e}")
    
        sql = "SELECT * from db_TimeSeries.table1"
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                print(f"k_timestamp: {row[0]}, voltage: {row[1]}, current: {row[2]}, temperature: {row[3]}, number: {row[4]}")
        except psycopg2.Error as e:
            print(f"Failed to insert data: {e}")


        cur.close()
        con.close()
        return


    if __name__ == "__main__":
        main()
    ```

3. Run the sample program:

    ```bash
    python3 example-psycopg2-app.py
    ```