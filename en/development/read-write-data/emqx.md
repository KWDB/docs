---
title: EMQX
id: emqx
---

# EMQX

[EMQX](https://www.emqx.io/) is an open-source, highly scalable, and distributed MQTT(Message Queuing Telemetry Transport) broker designed for IoT applications. This section explains how to configure EMQX to write data into KWDB using KWDB's RESTful API.

The integration enables EMQX to transform incoming MQTT messages into HTTP requests containing `INSERT` statements and forward them to KWDB's Insert API. Once configured, data from IoT devices will automatically flow from EMQX to your KWDB tables. For more information on the Insert endpoint, see [Insert Endpoint](../connect-kaiwudb/restful-api/connect-restful-api.md#insert-endpoint).

## Configure EMQX

### Prerequisites

Before configuring the integration, ensure you have:

- EMQX Setup:
  - Installed EMQX (version 5.0.19 or compatible)
  - Started the EMQX service
  For instructions, see [EMQX Documentation](https://www.emqx.io/).

- KWDB Setup:

  - Installed KWDB and created a database
  - Created a user with appropriate privileges on tables or higher
  - Created the target table where MQTT data will be inserted (the user must have `INSERT` privilege on this table)
  
- Authentication Token

    Generate an authentication token for KWDB API access using:

    ```shell
    curl -L -k -H "Authorization: Basic <base64(user:password)>" -X GET <node_ip>:8080/restapi/login
    ```

    Where:

    - `Base64(user:password)`: Base64-encoded username and password
    - `node_ip`: The IP address of your KWDB node

   ::: warning Note

   By default, the generated token is valid for 60 minutes. For data report intervals:

    - **Less than 60 minutes**: The system automatically extends the token.
    - **Greater than 60 minutes**: You must generate a new token before expiration or use `SET CLUSTER SETTING server.rest.timeout=<value>` to set a custom expiration period. The configurable range is [1, 2^63-1] minutes.

   :::

### Steps

The following steps uses EMQX version 5.0.19. UI elements and configuration steps may vary in other versions.

1. Create a webhook data bridge:
    1. Log in to the EMQX Dashboard.
        - Default URL: `http://<emqx_host>:18083`
        - Default credentials: Username `admin`, Password `public`
    2. Navigate to **Data Integration** > **Data Bridge** in the left sidebar.
    3. Click **Create** and select **Webhook** as the bridge type.
    4. Enter a name for your data bridge (e.g., "KWDB-Integration").

2. Configure the webhook settings:
    1. Set the HTTP method to `POST`.
    2. Enter the KWDB Insert API endpoint: `http://<kaiwudb_host>:8080/restapi/insert`.
    3. Configure the **Headers**:
        - Add header `Content-Type` with value `application/json`.
        - Add header `Authorization` with value of your token.
    4. In the **Body** section, enter the SQL template for inserting data:

        ```SQL
        INSERT INTO my_database.my_table VALUES (now(), ${payload.temperature}, ${payload.humidity}, ${payload.volume}, 'a'"
        ```

    5. Click **Create** to save the data bridge.

3. Create a rule for processing MQTT messages:
    1. Navigate to **Data Integration** > **Rules** in the left sidebar.
    2. Click **Create**.
    3. In the **SQL Editor**, enter a rule to select and process incoming MQTT messages.
    4. Click **Add Action**.
    5. Select **Forward using Data Bridge** as the action type.
    6. Choose the data bridge you created earlier from the dropdown.
    7. Click **Add** to add the action.

    For more information on EMQX rules and examples, see [EMQX Documentation](https://www.emqx.io/docs/en/v4.4/rule/rule-engine.html#publish-message).
