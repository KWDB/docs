---
title: Knex
id: connect-knex
---

# Connect to KWDB using Knex

Knex.js is a powerful SQL query builder that supports multiple database systems, including PostgreSQL and MySQL. This section demonstrates how to connect to KWDB using Knex.js to perform common database operations like creating tables, inserting data, and querying records.

## Prerequisites

- [Node.js v16 or higher](https://nodejs.org/en/download/) installed
- KWDB installed and running with:
  - Properly configured database authentication
  - A database created for your connection
  - A user with appropriate privileges on tables or higher

## Configuration Example

1. Use npm to install Knex.js:

    ```bash
    nvm use node
    npm install knex
    ```

2. Create a `data.js` file with your sample data:

    ```javascript
    export default {
    t_electmeter_data: () => [
        {
        k_timestamp: "now()",
        elect_name: "NULL",
        vol_a: 299.4,
        cur_a: 0.01,
        powerf_a: 0.01,
        allenergy_a: 0,
        pallenergy_a: 88915,
        rallenergy_a: 218893,
        allrenergy1_a: 105646,
        allrenergy2_a: 105646,
        powera_a: 0.31,
        powerr_a: 0.72,
        powerl_a: 0.16,
        vol_b: 299.5,
        cur_b: 0.03,
        powerf_b: 0.6,
        allenergy_b: 4436,
        pallenergy_b: 86837,
        rallenergy_b: 3,
        allrenergy1_b: 29679,
        allrenergy2_b: 29679,
        powera_b: 0.06,
        powerr_b: 0.62,
        powerl_b: 0.87,
        vol_c: 299.5,
        cur_c: 0.02,
        powerf_c: 0.58,
        allenergy_c: 99058,
        pallenergy_c: 61254,
        rallenergy_c: 14,
        allrenergy1_c: 0,
        allrenergy2_c: 0,
        powera_c: 0.97,
        powerr_c: 0.25,
        powerl_c: 0.18,
        vol_ab: 0.0,
        vol_bc: null,
        vol_ca: null,
        infre: 50.09,
        powerf: 0.41,
        allpower: 0.125,
        pallpower: 3765.66,
        rallpower: 0.59,
        powerr: 0.61,
        powerl: 0.17,
        allrenergy1: 2069.16,
        allrenergy2: 2069.16,
        machine_code: "1_2",
        op_group: "op_group_1",
        workshop_id: 22,
        cnc_number: 33,
        },
        {
        k_timestamp: "now()",
        elect_name: "a017",
        vol_a: 299.5,
        cur_a: 0.07,
        powerf_a: 0.02,
        allenergy_a: 0,
        pallenergy_a: 0,
        rallenergy_a: 2,
        allrenergy1_a: 33112,
        allrenergy2_a: 33112,
        powera_a: 0.42,
        powerr_a: 0.42,
        powerl_a: 0.9,
        vol_b: 299.4,
        cur_b: 0.05,
        powerf_b: 0.71,
        allenergy_b: 72159,
        pallenergy_b: 59126,
        rallenergy_b: 1,
        allrenergy1_b: 141800,
        allrenergy2_b: 141800,
        powera_b: 0.38,
        powerr_b: 0.41,
        powerl_b: 0.18,
        vol_c: 299.4,
        cur_c: 0.01,
        powerf_c: 0.05,
        allenergy_c: 137195,
        pallenergy_c: 164991,
        rallenergy_c: 9,
        allrenergy1_c: 250000,
        allrenergy2_c: 250000,
        powera_c: 0.01,
        powerr_c: 0.71,
        powerl_c: 0.53,
        vol_ab: 1.0,
        vol_bc: null,
        vol_ca: null,
        infre: 49.86,
        powerf: 0.93,
        allpower: 0.135,
        pallpower: 1077.7,
        rallpower: 0.49,
        powerr: 0.22,
        powerl: 0.35,
        allrenergy1: 1204.39,
        allrenergy2: 1204.39,
        machine_code: "2_3",
        op_group: "op_group_4",
        workshop_id: 33,
        cnc_number: 12,
        },
        [
        {
            k_timestamp: "now()",
            elect_name: "NULL",
            vol_a: 299.6,
            cur_a: 0.07,
            powerf_a: 0.03,
            allenergy_a: 0,
            pallenergy_a: 0,
            rallenergy_a: 5,
            allrenergy1_a: 0,
            allrenergy2_a: 0,
            powera_a: 0.5,
            powerr_a: 0.54,
            powerl_a: 0.47,
            vol_b: 299.5,
            cur_b: 0.12,
            powerf_b: 0.45,
            allenergy_b: 125554,
            pallenergy_b: 250000,
            rallenergy_b: 6,
            allrenergy1_b: 76932,
            allrenergy2_b: 76932,
            powera_b: 0.17,
            powerr_b: 0.79,
            powerl_b: 0.69,
            vol_c: 299.6,
            cur_c: 0.19,
            powerf_c: 0.12,
            allenergy_c: 71144,
            pallenergy_c: 37193,
            rallenergy_c: 4,
            allrenergy1_c: 249115,
            allrenergy2_c: 249115,
            powera_c: 0.9,
            powerr_c: 0.45,
            powerl_c: 0.17,
            vol_ab: 2.0,
            vol_bc: null,
            vol_ca: null,
            infre: 50.07,
            powerf: 0.17,
            allpower: 0.16,
            pallpower: 3784.95,
            rallpower: 0.51,
            powerr: 0.64,
            powerl: 0.65,
            allrenergy1: 597.74,
            allrenergy2: 597.74,
            machine_code: "2_1",
            op_group: "op_group_9",
            workshop_id: 55,
            cnc_number: 66,
        },
        {
            k_timestamp: "now()",
            elect_name: "a003",
            vol_a: 299.3,
            cur_a: 0.1,
            powerf_a: 0.04,
            allenergy_a: 42277,
            pallenergy_a: 0,
            rallenergy_a: 0,
            allrenergy1_a: 250000,
            allrenergy2_a: 250000,
            powera_a: 0.89,
            powerr_a: 0.23,
            powerl_a: 0.13,
            vol_b: 299.5,
            cur_b: 0.02,
            powerf_b: 0.52,
            allenergy_b: 72035,
            pallenergy_b: 0,
            rallenergy_b: 8,
            allrenergy1_b: 20474,
            allrenergy2_b: 20474,
            powera_b: 0.83,
            powerr_b: 0.89,
            powerl_b: 0.65,
            vol_c: 299.4,
            cur_c: 0,
            powerf_c: 0.2,
            allenergy_c: 143621,
            pallenergy_c: 79899,
            rallenergy_c: 7,
            allrenergy1_c: 101135,
            allrenergy2_c: 101135,
            powera_c: 0.9,
            powerr_c: 0.06,
            powerl_c: 0.35,
            vol_ab: 3.0,
            vol_bc: null,
            vol_ca: null,
            infre: 49.77,
            powerf: 0.45,
            allpower: 0.355,
            pallpower: 1647.18,
            rallpower: 0.76,
            powerr: 0.75,
            powerl: 0.12,
            allrenergy1: 0,
            allrenergy2: 0,
            machine_code: "4_6",
            op_group: "op_group_2",
            workshop_id: 22,
            cnc_number: 12,
        },
        {
            k_timestamp: "now()",
            elect_name: "a010",
            vol_a: 299.5,
            cur_a: 0.08,
            powerf_a: 0.05,
            allenergy_a: 114756,
            pallenergy_a: 56158,
            rallenergy_a: 4,
            allrenergy1_a: 29879,
            allrenergy2_a: 29879,
            powera_a: 0.15,
            powerr_a: 0.32,
            powerl_a: 0.08,
            vol_b: 299.5,
            cur_b: 0.12,
            powerf_b: 0.39,
            allenergy_b: 52160,
            pallenergy_b: 68640,
            rallenergy_b: 192271,
            allrenergy1_b: 136436,
            allrenergy2_b: 136436,
            powera_b: 0.91,
            powerr_b: 0.26,
            powerl_b: 0.66,
            vol_c: 299.5,
            cur_c: 0.04,
            powerf_c: 0.34,
            allenergy_c: 0,
            pallenergy_c: 93737,
            rallenergy_c: 2,
            allrenergy1_c: 0,
            allrenergy2_c: 0,
            powera_c: 0.74,
            powerr_c: 0,
            powerl_c: 0.41,
            vol_ab: 4.0,
            vol_bc: null,
            vol_ca: null,
            infre: 50.01,
            powerf: 0.71,
            allpower: 0.085,
            pallpower: 1132.23,
            rallpower: 0.92,
            powerr: 0.99,
            powerl: 0.37,
            allrenergy1: 0,
            allrenergy2: 0,
            machine_code: "6_7",
            op_group: "op_group_11",
            workshop_id: 19,
            cnc_number: 12,
        },
        {
            k_timestamp: "now()",
            elect_name: "NULL",
            vol_a: 299.3,
            cur_a: 0.02,
            powerf_a: 0.06,
            allenergy_a: 111164,
            pallenergy_a: 0,
            rallenergy_a: 196885,
            allrenergy1_a: 50261,
            allrenergy2_a: 50261,
            powera_a: 0.79,
            powerr_a: 0.51,
            powerl_a: 0.38,
            vol_b: 299.4,
            cur_b: 0.11,
            powerf_b: 0.5,
            allenergy_b: 133354,
            pallenergy_b: 146260,
            rallenergy_b: 7,
            allrenergy1_b: 0,
            allrenergy2_b: 0,
            powera_b: 0.54,
            powerr_b: 0.37,
            powerl_b: 0.8,
            vol_c: 299.3,
            cur_c: 0.08,
            powerf_c: 0.31,
            allenergy_c: 0,
            pallenergy_c: 0,
            rallenergy_c: 6,
            allrenergy1_c: 119107,
            allrenergy2_c: 119107,
            powera_c: 0.42,
            powerr_c: 0.9,
            powerl_c: 0.26,
            vol_ab: 5.0,
            vol_bc: null,
            vol_ca: null,
            infre: 49.89,
            powerf: 0.58,
            allpower: 0.09,
            pallpower: 4370.72,
            rallpower: 0.46,
            powerr: 0.48,
            powerl: 0.37,
            allrenergy1: 303.01,
            allrenergy2: 303.01,
            machine_code: "5_2",
            op_group: "op_group_0",
            workshop_id: 99,
            cnc_number: 12,
        },
        ],
    ],
    factory_data: () => [
        new Array(19).fill(0).map((_, idx) => {
        let num = idx + 1;
        return {
            id: num,
            name: `${num},${num}FAC`,
            sub_comp_id: Math.ceil(num / 5),
        };
        }),
        { id: 99, name: "9,9FAC", sub_comp_id: 99 },
    ],
    workshop_data: () => [
        new Array(98).fill(0).map((_, idx) => {
        let num = idx + 1;
        return {
            id: num,
            name: `${num},${num}WS`,
            factory_id: Math.ceil(num / 5),
        };
        }),
    ],
    workshop_electmeter_data: () => [
        new Array(19)
        .fill(0)
        .map((_, idx) => {
            let numx = idx + 1;
            return new Array(49).fill(0).map((_, idy) => {
            let numy = idy + 1;
            return {
                machine_code: `${numx}_${numy}`,
                workshop_id: 5 + numx + Math.floor(numy / 10),
            };
            });
        })
        .flat(),
    ],
    };
    ```

3. Create a `index.js` file with your connection and query logic:

    ```javascript
    import data from "./data.js";
    import Knex from "knex";
    import fs from "node:fs";

    const knex = Knex({
    client: "pg",
    connection: {
        host: process.env["DBHOST"] || "localhost",
        port: parseInt(process.env["DBPORT"] || "26257"),
        user: process.env["DBUSER"] || "root",
        ssl:
        "true" == process.env["NOSSL"]
            ? false
            : {
                key: fs.readFileSync("../../certs/client.root.key"),
                cert: fs.readFileSync("../../certs/client.root.crt"),
                ca: fs.readFileSync("../../certs/ca.crt"),
                rejectUnauthorized: false,
            },
    },
    search: "public",
    dialect: "postgres",
    version: "12",
    });

    /**
    * Print query results
    * @param {import('pg').QueryResult | any[]} rs ResultSet
    * @param {(message: string) => void} log Logging function
    */
    function rsPrint(rs, log = console.log) {
    function rowPrint(rows) {
        if (rows.length > 0) {
        let headers = [];
        let divs = [];
        for (let key of Object.keys(rows[0])) {
            headers.push(key);
            divs.push("-".repeat(key.length));
        }
        log(`  ${headers.join("  |  ")}  `);
        log(`--${divs.join("--+--")}--`);
        for (let item of rows) {
            log(`  ${headers.map((key) => item[key]).join("  |   ")}  `);
        }
        }
        log(`(${rows.length} rows)`);
    }
    if (rs instanceof Array) {
        rowPrint(rs);
    } else {
        if ("SELECT" == rs.command) {
        rowPrint(rs.rows);
        } else {
        log(rs.command || "");
        if (!!rs.rowCount) log(`(${rs.rowCount} rows)`);
        }
    }
    }

    // Drop databases
    rsPrint(await knex.schema.raw("DROP DATABASE IF EXISTS db_shig"));
    rsPrint(await knex.schema.raw("DROP DATABASE IF EXISTS ts_shig"));
    // Create a relational database
    rsPrint(await knex.schema.raw("CREATE DATABASE db_shig"));
    // Create a time-series database
    rsPrint(await knex.schema.raw("CREATE TS DATABASE ts_shig"));
    // Create relational tables
    rsPrint(
    await knex.schema.createTable("db_shig.factory", (table) => {
        table.integer("id", 2);
        table.string("name", 8);
        table.integer("sub_comp_id", 2);
        table.primary(["id"], {
        constraintName: "factory_pkey",
        });
    })
    );
    rsPrint(
    await knex.schema.createTable("db_shig.workshop", (table) => {
        table.integer("id", 2);
        table.string("name", 8);
        table.integer("factory_id", 2);
        table.primary(["id"], {
        constraintName: "workshop_pkey",
        });
    })
    );
    rsPrint(
    await knex.schema.createTable("db_shig.workshop_electmeter", (table) => {
        table.string("machine_code", 64);
        table.integer("workshop_id", 2);
        table.primary(["machine_code"], {
        constraintName: "workshop_electmeter_key",
        });
    })
    );
    // Create time-series tables
    rsPrint(
    await knex.schema.raw(`CREATE TABLE ts_shig.t_electmeter (
    k_timestamp timestamp NOT NULL,
    elect_name char(63) NOT NULL,
    vol_a double NOT NULL,
    cur_a double NOT NULL,
    powerf_a double,
    allenergy_a int NOT NULL,
    pallenergy_a int NOT NULL,
    rallenergy_a int NOT NULL,
    allrenergy1_a int NOT NULL,
    allrenergy2_a int NOT NULL,
    powera_a double NOT NULL,
    powerr_a double NOT NULL,
    powerl_a double NOT NULL,
    vol_b double NOT NULL,
    cur_b double NOT NULL,
    powerf_b double NOT NULL,
    allenergy_b int NOT NULL,
    pallenergy_b int NOT NULL,
    rallenergy_b int NOT NULL,
    allrenergy1_b int NOT NULL,
    allrenergy2_b int NOT NULL,
    powera_b double NOT NULL,
    powerr_b double NOT NULL,
    powerl_b double NOT NULL,
    vol_c double NOT NULL,
    cur_c double NOT NULL,
    powerf_c double NOT NULL,
    allenergy_c int NOT NULL,
    pallenergy_c int NOT NULL,
    rallenergy_c int NOT NULL,
    allrenergy1_c int NOT NULL,
    allrenergy2_c int NOT NULL,
    powera_c double NOT NULL,
    powerr_c double NOT NULL,
    powerl_c double NOT NULL,
    vol_ab double,
    vol_bc double,
    vol_ca double,
    infre double NOT NULL,
    powerf double NOT NULL,
    allpower double NOT NULL,
    pallpower double NOT NULL,
    rallpower double NOT NULL,
    powerr double NOT NULL,
    powerl double NOT NULL,
    allrenergy1 double NOT NULL,
    allrenergy2 double NOT NULL
    ) ATTRIBUTES (machine_code varchar(64) NOT NULL, op_group varchar(64) NOT NULL, workshop_id int2 NOT NULL, cnc_number int) PRIMARY TAGS(machine_code) retentions 3d activetime 1h partition interval 1d;`)
    );

    const tab_t_electmeter = () => knex.table("ts_shig.t_electmeter");
    const tab_factory = () => knex.table("db_shig.factory");
    const tab_workshop = () => knex.table("db_shig.workshop");
    const tab_workshop_electmeter = () => knex.table("db_shig.workshop_electmeter");

    // Insert time-series data
    for (const item of data.t_electmeter_data()) {
    rsPrint(await tab_t_electmeter().insert(item));
    }
    // Insert relational data
    for (const item of data.factory_data()) {
    rsPrint(await tab_factory().insert(item));
    }
    for (const item of data.workshop_data()) {
    rsPrint(await tab_workshop().insert(item));
    }
    for (const item of data.workshop_electmeter_data()) {
    rsPrint(await tab_workshop_electmeter().insert(item));
    }
    // Query time-series data
    rsPrint(await tab_t_electmeter().select());

    // Update relational data
    rsPrint(await tab_factory().where({ id: 99 }).update({ name: "99UPDATE" }));
    // Query relational data
    rsPrint(await tab_factory().select());
    // Delete relational data
    rsPrint(await tab_factory().where({ id: 99 }).delete());
    // Query relational data
    rsPrint(await tab_factory().select());

    // Aggregation query
    rsPrint(
    await knex.raw(
        `select * from 
    (select we.machine_code as machine_code from db_shig.factory f, db_shig.workshop w, db_shig.workshop_electmeter we
            where we.workshop_id = w.id and f.id = w.factory_id and f.sub_comp_id = 1) m, 
    ts_shig.t_electmeter e where e.machine_code = m.machine_code limit 10`
    )
    );
    // Drop tables
    rsPrint(await knex.schema.dropTable("db_shig.workshop_electmeter"));
    rsPrint(await knex.schema.dropTable("ts_shig.t_electmeter"));
    // Drop databases
    rsPrint(await knex.schema.raw("DROP DATABASE ts_shig CASCADE"));
    rsPrint(await knex.schema.raw("DROP DATABASE db_shig"));
    process.exit(0);
    ```

4. Create a `package.json` file.

    ```json
    {
    "name": "demo",
    "version": "1.0.0",
    "main": "index.js",
    "license": "MIT",
    "scripts": {
        "start": "node index.js"
    },
    "type": "module",
    "dependencies": {
        "knex": "^3.1.0",
        "pg": "^8.12.0"
    }
    }
    ```

5. Install dependencies and run the application:

    ```bash
    npm install
    npm start
    ```