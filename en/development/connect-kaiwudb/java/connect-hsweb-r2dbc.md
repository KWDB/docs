---
title: hsweb_r2dbc
id: connect-hsweb-r2dbc
---

# Connect to KWDB Using hsweb_r2dbc

hsweb is a comprehensive enterprise backend management system built on Spring Boot 2.x.

This section demonstrates how to establish a connection to KWDB through hsweb_r2dbc and perform essential database operations including creation, insertion, and querying of data.

## Prerequisites

- [OpenJDK 1.8 or higher](https://openjdk.org/install/) installed
- [Maven 3.6 or higher](https://maven.apache.org/install.html) installed
- KaiwuDB JDBC driver package obtained
- KWDB installed and running with:
  - Properly configured database authentication
  - A database created for your connection
  - A user with appropriate privileges on tables or higher

## Configuration Example

1. Download the code.

2. Compile the project.

    ```bash
    cd ./java/hsweb_r2dbc
    mvn clean package -Dmaven.test.skip=true
    ```

3. Create a directory and copy the files:

    ```bash
    mkdir /opt/hsweb_r2dbc
    cp target/hsweb_r2dbc-1.0.0.jar target/classes/application.yml /opt/hsweb_r2dbc/
    ```

4. Configure the data source in the `application.yml` file.

    ```yml
    spring:
    application:
        name: hsweb_r2dbc
    r2dbc:
        primary:
        url: r2dbc:postgresql://localhost:26257/defaultdb
        username: kaiwudb
        password: <password>
        secondary:
        url: r2dbc:postgresql://localhost:26257/benchmark
        username: kaiwudb
        password: <password>

    easyorm:
    dialect: postgres
    auto-ddl: false
    allow-alter: false
    default-schema: public
    dialect-type: org.hswebframework.ezorm.rdb.supports.postgres.PostgresqlDialect

    logging:
    level:
        org:
        hswebframework: debug

    server:
    port: 8090
    ```

5. Navigate to the `hsweb_r2dbc` directory and create a log directory:

    ```bash
    cd /opt/hsweb_r2dbc
    mkdir logs
    ```

6. Start the application:

    ```bash
    nohup java -jar /opt/hsweb_r2dbc/hsweb_r2dbc-1.0.0.jar --spring.config.location=/opt/hsweb_r2dbc/application.yml > /opt/hsweb_r2dbc/logs/output.log 2>&1 &
    ```

7. Perform data insertion, query, and deletion operations in the `/opt/hsweb_r2dbc/` directory to verify the configuration:

    The following example assumes you have already created a time-series database and table structure. If not, run the following SQL commands:

    ```sql
    CREATE TS DATABASE hsweb_r2dbc;
    
    CREATE TABLE hsweb_r2dbc.cpu (
        k_timestamp TIMESTAMPTZ NOT NULL,
        usage_user INT8 NOT NULL,
        usage_system INT8 NOT NULL,
        usage_idle INT8 NOT NULL,
        usage_nice INT8 NOT NULL,
        usage_iowait INT8 NOT NULL,
        usage_irq INT8 NOT NULL,
        usage_softirq INT8 NOT NULL,
        usage_steal INT8 NOT NULL,
        usage_guest INT8 NOT NULL
    ) TAGS (
        ptag INT4 NOT NULL,
        region INT4 NOT NULL,
        datacenter INT4 NOT NULL,
        rack VARCHAR(1024),
        os VARCHAR(1024),
        arch VARCHAR(1024),
        team VARCHAR(1024),
        service VARCHAR(1024)
    ) PRIMARY TAGS (ptag);
    
    INSERT INTO hsweb_r2dbc.cpu (k_timestamp, usage_user, usage_system, usage_idle, usage_nice,
        usage_iowait, usage_irq, usage_softirq, usage_steal, usage_guest, ptag, region, datacenter,
        rack, os, arch, team, service)
    VALUES
        ('2024-01-21 22:22:22.221', 1, 2, 3, 4, 5, 6, 7, 8, 1, 1, 1, 1, '2', '2', '2', '2', '2'),
        ('2024-01-22 22:22:22.221', 1, 2, 3, 4, 5, 6, 7, 8, 1, 1, 1, 1, '2', '2', '2', '2', '2'),
        ('2024-01-23 22:22:22.221', 1, 2, 3, 4, 5, 6, 7, 8, 1, 1, 1, 1, '2', '2', '2', '2', '2');
    ```

    - Query data via REST API:

        ```shell
        # Query CPU metrics for tag ID 1 between Jan 20, 2024 and Jan 24, 2024
        curl -X GET -H  "Accept:*/*" -H  "Content-Type:application/x-www-form-urlencoded" "http://localhost:8090/hsweb_r2dbc/cpus/1?end=1706106142221&start=1705760542221"
        ```

    - Insert data via REST API:

        ```shell
        # Add a new CPU metric data point:
        curl -X POST -H  "Accept:*/*" -H  "Content-Type:application/json" -d "{\"arch\":\"\",\"dataCenter\":2,\"id\":2,\"os\":\"\",\"rack\":\"\",\"region\":2,\"service\":\"\",\"team\":\"\",\"time\":1722579427867,\"usageGuest\":1,\"usageIdle\":1,\"usageIoWait\":1,\"usageIrq\":1,\"usageNice\":1,\"usageSoftIrq\":1,\"usageSteal\":1,\"usageSystem\":1,\"usageUser\":1}" "http://localhost:8090/hsweb_r2dbc/cpu"
        ```

    - Delete data via REST API:

        ```shell
        # Delete CPU metric with ID 1 at specific timestamp
        curl -X POST -H  "Accept:*/*" -H  "Content-Type:application/json" -d "{\"id\":1,\"time\":1722579427867}" "http://localhost:8090/hsweb_r2dbc/cpu/delete"
        ```