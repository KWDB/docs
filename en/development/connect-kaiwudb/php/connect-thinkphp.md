---
title: ThinkPHP
id: connect-thinkphp
---

# Connect to KWDB Using ThinkPHP

ThinkPHP is an open-source, fast, simple, and object-oriented lightweight PHP development framework. It is designed to support agile web application development and simplify enterprise application development.

This section demonstrates how to connect to KWDB using ThinkPHP and execute SQL statements for building PHP web applications.

## Prerequisites

- [ThinkPHP](https://doc.thinkphp.cn/v6_1/anzhuangThinkPHP.html?lang=en) installed
- KWDB installed and running with:
  - Properly configured database authentication
  - A database created for your connection
  - A user with appropriate privileges on tables or higher

## Configuration Example

### Install PHP and Required Extensions

1. Install PHP:

    ```bash
    sudo apt install php7.4
    ```

2. Install the PHP-PGSQL extension:

    ```bash
    sudo apt install php-pgsql
    ```

3. Enable the PDO extension by modifying the `/etc/php/7.4/mods-available/php.ini` file:

    ```ini
    extension=pdo.so
    ```

### Install and Configure Apache

1. Install Apache:

    ```bash
    sudo apt install apache2
    ```

2. Disable the default site configuration if it exists:

    ```bash
    sudo a2dissite 000-default
    ```

3. Create a `thinkphp6.conf` configuration file:

    ```bash
    sudo vim /etc/apache2/sites-available/thinkphp6.conf
    ```

4. Add the following configuration to `thinkphp6.conf`:

    ```apache
    <VirtualHost *:80>
        ServerAdmin webmaster@localhost
        ServerName yourdomain.com
        ServerAlias www.yourdomain.com

        DocumentRoot /root/test/thinkphp-test/tp6/public

        <Directory "/root/test/thinkphp-test/tp6/public">
            AllowOverride All
            Require all granted
        </Directory>

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>
    ```

5. Check if the Apache URL rewrite module is enabled:

    ```bash
    sudo a2query -m rewrite
    ```

6. If not enabled, enable it and reload Apache:

    ```bash
    sudo a2enmod rewrite
    sudo systemctl reload apache2
    ```

7. Start the Apache service:

    ```bash
    sudo systemctl start apache2
    ```

### Set Up a ThinkPHP Project

1. Clone a ThinkPHP 6 project:

    ```bash
    git clone https://gitee.com/ruoshuiyx/tp6.git
    ```

2. Configure database settings in the `.env` file:

    ```env
    [DATABASE]
    TYPE=kwdb
    HOSTNAME= <database_ip>
    DATABASE= defaultdb
    USERNAME= <user_name>
    PASSWORD= <password>
    HOSTPORT= 26800
    CHARSET= utf8
    DEBUG= true
    PREFIX= tp_
    ```

3. Add the status query function in the `app/admin/service/Backup.php` file:

    ```php
    private static function _show_status_stmt($table = null)
    {
        if (is_null($table)) {
            return "SELECT t.*, c.* FROM information_schema.tables AS t
                    JOIN kwdb_internal.tables AS c ON t.table_catalog = c.database_name
                    AND t.table_schema = c.schema_name
                    AND t.table_name = c.name
                    WHERE t.table_schema NOT IN ('information_schema', 'pg_catalog', 'crdb_internal')
                    ORDER BY t.table_catalog, t.table_schema, t.table_name;";
        } else {
            return "SELECT t.*, c.* FROM information_schema.tables AS t
                    JOIN kwdb_internal.tables AS c ON t.table_catalog = c.database_name
                    AND t.table_schema = c.schema_name
                    AND t.table_name = c.name
                    WHERE t.table_schema NOT IN ('information_schema', 'pg_catalog', 'crdb_internal')
                    AND t.table_name = '" . $table . "'
                    ORDER BY t.table_catalog, t.table_schema, t.table_name;";
        }
    }
    ```

4. Modify the `dataList` function in the same file:

    ```php
    public function dataList($table = null, $type = 1)
    {
        $db = self::connect();
        $stmt = self::_show_status_stmt($table);
        $list = $db->query($stmt);
        return array_map('array_change_key_case', $list);
    }
    ```

5. Modify the `app/common.php` file by changing `$tags = explode(',', $info[$v['field']]);` to `$tags = explode(',', $info[$v['field']][0]);`.

6. Modify the `app/common/model/Admin.php` file and comment out the `open_code` section:

    ```php
    public static function checkLogin()
    {
        // Retrieve system settings
        $system = \app\common\model\System::find(1);

        $username = Request::param("username");
        $password = Request::param("password");

        // $open_code = $system['code'];
        // if($open_code){
        //     $code = Request::param("vercode");
        //     if(!captcha_check($code)){
        //         $data = ['error' => '1', 'msg' => '验证码错误'];
        //         return json($data);
        //     }
        // }
        // }
        $result = self::where(['username' => $username, 'password' => md5($password)])->find();
    ...    
    ```

7. Configure database connection in `config/database.php`:

    ```php
    <?php

    return [
        // Default database connection configuration
        'default'         => env('database.driver', 'kwdb'),

        // Custom time query rules
        'time_query_rule' => [],

        // Automatically write timestamp fields
        // true = auto-detect type, false = disable
        // Use a string to explicitly specify the time field type: supports int, timestamp, datetime, date
        'auto_timestamp'  => true,

        // Default format for time fields when retrieved
        'datetime_format' => 'Y-m-d H:i:s',

        // Time field configuration, format: create_time, update_time
        'datetime_field'  => '',

        // Database connection configuration
        'connections'     => [
            'kwdb' => [
                // Database type
                'type'            => env('database.type', 'kwdb'),
                // Server address
                'hostname'        => env('database.hostname', '10.110.10.155'),
                // Database name
                'database'        => env('database.database', 'defaultdb'),
                // Username
                'username'        => env('database.username', 'u1'),
                // Password
                'password'        => env('database.password', 'Znbase@123'),
                // Port
                'hostport'        => env('database.hostport', '26800'),
                // Database connection parameters
                'params'          => [],
                // Default database encoding is utf8
                'charset'         => env('database.charset', 'utf8'),
                // Table prefix
                'prefix'          => env('database.prefix', ''),

                // Database deployment type: 0 = centralized (single server), 1 = distributed (primary-secondary)
                'deploy'          => 0,
                // Whether to separate reads and writes (effective only for primary-secondary mode)
                'rw_separate'     => false,
                // Number of primary servers after read/write separation
                'master_num'      => 1,
                // Specify the secondary server number
                'slave_no'        => '',
                // Strictly check whether fields exist
                'fields_strict'   => true,
                // Reconnect automatically on disconnection
                'break_reconnect' => false,
                // SQL query listening
                'trigger_sql'     => env('app_debug', true),
                // Enable field caching
                'fields_cache'    => false,
            ],

            // Additional database configurations
        ],
    ];
    ```

8. Update `public/index.php` to import `kwdb.php`:

    ```php
    require __DIR__ . '/builder/kwdb.php';
    require __DIR__ . '/connector/kwdb.php';
    ```

9. Create a `kwdb.php` file in `tp6/public/builder/` directory:

    ```php
    <?php
    // +----------------------------------------------------------------------
    // | ThinkPHP [ WE CAN DO IT JUST THINK ]
    // +----------------------------------------------------------------------
    // | Copyright (c) 2006~2019 http://thinkphp.cn All rights reserved.
    // +----------------------------------------------------------------------
    // | Licensed ( http://www.apache.org/licenses/LICENSE-2.0 )
    // +----------------------------------------------------------------------
    // | Author: liu21st <liu21st@gmail.com>
    // +----------------------------------------------------------------------
    declare (strict_types = 1);

    namespace think\db\builder;

    use think\db\Builder;
    use think\db\Query;
    use think\db\Raw;

    /**
    * KWDB database driver
    */
    class kwdb extends Builder
    {
        /**
        * SQL expression for single INSERT
        * @var string
        */
        protected $insertSql = 'INSERT INTO %TABLE% (%FIELD%) VALUES (%DATA%) %COMMENT%';

        /**
        * SQL expression for batch INSERT
        * @var string
        */
        protected $insertAllSql = 'INSERT INTO %TABLE% (%FIELD%) %DATA% %COMMENT%';

        /**
        * Analyze LIMIT clause
        * @access protected
        * @param  Query     $query        Query object
        * @param  mixed     $limit
        * @return string
        */
        public function parseLimit(Query $query, string $limit): string
        {
            $limitStr = '';

            if (!empty($limit)) {
                $limit = explode(',', $limit);
                if (count($limit) > 1) {
                    $limitStr .= ' LIMIT ' . $limit[1] . ' OFFSET ' . $limit[0] . ' ';
                } else {
                    $limitStr .= ' LIMIT ' . $limit[0] . ' ';
                }
            }

            return $limitStr;
        }

        /**
        * Handle fields and table names
        * @access public
        * @param  Query     $query     Query object
        * @param  mixed     $key       Field name
        * @param  bool      $strict    Strict checking
        * @return string
        */
        public function parseKey(Query $query, $key, bool $strict = false): string
        {
            if (is_int($key)) {
                return (string) $key;
            } elseif ($key instanceof Raw) {
                return $this->parseRaw($query, $key);
            }

            $key = trim($key);

            if (strpos($key, '->') && false === strpos($key, '(')) {
                // Support for JSON fields
                [$field, $name] = explode('->', $key);
                $key            = '"' . $field . '"' . '->>\'' . $name . '\'';
            } elseif (strpos($key, '.')) {
                [$table, $key] = explode('.', $key, 2);

                $alias = $query->getOptions('alias');

                if ('__TABLE__' == $table) {
                    $table = $query->getOptions('table');
                    $table = is_array($table) ? array_shift($table) : $table;
                }

                if (isset($alias[$table])) {
                    $table = $alias[$table];
                }

                if ('*' != $key && !preg_match('/[,\"\*\(\).\s]/', $key)) {
                    $key = '"' . $key . '"';
                }
            }

            if (isset($table)) {
                $key = $table . '.' . $key;
            }

            return $key;
        }

        /**
        * Random sort function
        * @access protected
        * @param  Query     $query        Query object
        * @return string
        */
        protected function parseRand(Query $query): string
        {
            return 'RANDOM()';
        }

    }
    ```

10. Create a `kwdb.php` file in the `tp6/public/connector/` directory:

    ```php
    <?php
    // +----------------------------------------------------------------------
    // | ThinkPHP [ WE CAN DO IT JUST THINK ]
    // +----------------------------------------------------------------------
    // | Copyright (c) 2006~2019 http://thinkphp.cn All rights reserved.
    // +----------------------------------------------------------------------
    // | Licensed ( http://www.apache.org/licenses/LICENSE-2.0 )
    // +----------------------------------------------------------------------
    // | Author: liu21st <liu21st@gmail.com>
    // +----------------------------------------------------------------------

    namespace think\db\connector;

    use PDO;
    use think\db\PDOConnection;

    /**
    * KWDB database driver
    */
    class kwdb extends PDOConnection
    {

        /**
        * Default PDO connection parameters
        * @var array
        */
        protected $params = [
            PDO::ATTR_CASE              => PDO::CASE_NATURAL,
            PDO::ATTR_ERRMODE           => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_ORACLE_NULLS      => PDO::NULL_NATURAL,
            PDO::ATTR_STRINGIFY_FETCHES => false,
        ];

        /**
        * Parse DSN (Data Source Name) for PDO connection
        * @access protected
        * @param  array $config Connection configuration
        * @return string
        */
        protected function parseDsn(array $config): string
        {
            $dsn = 'pgsql:dbname=' . $config['database'] . ';host=' . $config['hostname'];

            if (!empty($config['hostport'])) {
                $dsn .= ';port=' . $config['hostport'];
            }

            return $dsn;
        }

        /**
        * Get field (column) information for a table
        * @access public
        * @param  string $tableName
        * @return array
        */
        public function getFields(string $tableName): array
        {
            [$tableName] = explode(' ', $tableName);
            // $sql         = 'select fields_name as "field",fields_type as "type",fields_not_null as "null",fields_key_name as "key",fields_default as "default",fields_default as "extra" from table_msg(\'' . $tableName . '\');';
    //        $sql = "SELECT pg_catalog.pg_attribute.attname AS field, pg_catalog.pg_attribute.attnum AS fields_index, pg_catalog.pgsql_type ( pg_type.typname::VARCHAR ) AS type,CASE WHEN ( pg_catalog.pg_attribute.atttypmod - 4 > 0 ) THEN pg_catalog.pg_attribute.atttypmod - 4 ELSE NULL END AS fields_length,CASE WHEN pg_catalog.pg_attribute.attnotnull THEN 'NOT NULL' ELSE '' END AS null, pg_catalog.pg_attrdef.adsrc AS default, pg_catalog.pg_attrdef.adsrc AS extra, pg_catalog.pg_description.description AS fields_comment,COALESCE(( SELECT CONSTRAINT_NAME FROM information_schema.key_column_usage WHERE table_schema = 'public' AND TABLE_NAME = '". $tableName ."' AND COLUMN_NAME = pg_catalog.pg_attribute.attname),'') AS key FROM pg_catalog.pg_attribute INNER JOIN pg_catalog.pg_class ON pg_catalog.pg_attribute.attrelid = pg_catalog.pg_class.OID INNER JOIN pg_catalog.pg_type ON pg_catalog.pg_attribute.atttypid = pg_type.OID LEFT OUTER JOIN pg_catalog.pg_attrdef ON pg_catalog.pg_attrdef.adrelid = pg_catalog.pg_class.OID AND pg_catalog.pg_attrdef.adnum = pg_catalog.pg_attribute.attnum LEFT OUTER JOIN pg_catalog.pg_description ON pg_catalog.pg_description.objoid = pg_catalog.pg_class.OID AND pg_catalog.pg_description.objsubid = pg_catalog.pg_attribute.attnum WHERE pg_catalog.pg_attribute.attnum > 0 AND pg_catalog.pg_attribute.attisdropped <> 't' AND pg_catalog.pg_class.OID=(SELECT pg_class.OID FROM pg_class INNER JOIN pg_namespace ON ( pg_class.relnamespace = pg_namespace.OID AND LOWER (pg_namespace.nspname) = 'public') WHERE pg_class.relname = '". $tableName ."') ORDER BY pg_catalog.pg_attribute.attnum;";
            $sql = "SELECT 
        c.column_name AS field,
        c.ordinal_position AS fields_index,
        c.data_type AS type,
        CASE 
            WHEN c.character_maximum_length IS NOT NULL THEN c.character_maximum_length
            WHEN c.numeric_precision IS NOT NULL THEN c.numeric_precision
            ELSE NULL 
        END AS fields_length,
        CASE WHEN c.is_nullable = 'NO' THEN 'NOT NULL' ELSE '' END AS null,
        c.column_default AS default,
        c.column_default AS extra,
        COALESCE(
            (SELECT d.description 
            FROM pg_catalog.pg_description d
            JOIN pg_catalog.pg_class cl ON d.objoid = cl.oid
            JOIN pg_catalog.pg_namespace n ON cl.relnamespace = n.oid
            WHERE cl.relname = '$tableName' 
            AND n.nspname = 'public' 
            AND d.objsubid = c.ordinal_position), '') AS fields_comment,
        COALESCE(
            (SELECT kcu.constraint_name 
            FROM information_schema.key_column_usage kcu 
            WHERE kcu.table_schema = 'public' 
            AND kcu.table_name = '$tableName' 
            AND kcu.column_name = c.column_name), '') AS key
    FROM 
        information_schema.columns c
    JOIN 
        information_schema.tables t ON c.table_schema = t.table_schema AND c.table_name = t.table_name
    WHERE 
        c.table_schema = 'public'
        AND c.table_name = '$tableName'
    ORDER BY 
        c.ordinal_position;";

            $pdo    = $this->getPDOStatement($sql);
            $result = $pdo->fetchAll(PDO::FETCH_ASSOC);
            $info   = [];

            if (!empty($result)) {
                foreach ($result as $key => $val) {
                    $val = array_change_key_case($val);

                    $info[$val['field']] = [
                        'name'    => $val['field'],
                        'type'    => $val['type'],
                        'notnull' => (bool) ('' !== $val['null']),
                        'default' => $val['default'],
                        'primary' => !empty($val['key']),
                        'autoinc' => (0 === strpos($val['extra'], 'nextval(')),
                    ];
                }
            }

            return $this->fieldCase($info);
        }

        /**
        * Get table list from the database
        * @access public
        * @param  string $dbName
        * @return array
        */
        public function getTables(string $dbName = ''): array
        {
            $sql    = "select tablename as Tables_in_test from pg_tables where  schemaname ='public'";
            $pdo    = $this->getPDOStatement($sql);
            $result = $pdo->fetchAll(PDO::FETCH_ASSOC);
            $info   = [];

            foreach ($result as $key => $val) {
                $info[$key] = current($val);
            }

            return $info;
        }

        protected function supportSavepoint(): bool
        {
            return true;
        }
    }
    ```

11. Update the SQL schema files provided with the project to ensure compatibility with KWDB's SQL syntax.

### Verify Database Connection

1. Start Apache and access your ThinkPHP application to verify the database connection.