---
title: PHP pgsql
id: connect-php-pgsql
---

# Connect to KWDB Using PHP and PDO

PHP is a widely used open-source server-side scripting language that excels in web development. The PHP Data Objects (PDO) extension provides a lightweight, consistent interface for accessing databases in PHP, offering improved security and flexibility over older methods.

This section demonstrates how to connect to KWDB using PHP with the PDO extension and execute SQL statements.

## Prerequisites

KWDB installed and running with:

- Properly configured database authentication
- A database created for your connection
- A user with appropriate privileges on tables or higher

## Configuration Example

1. Install PHP and the PostgreSQL PDO extension:

    ```bash
    sudo apt install php
    sudo apt install php-pgsql
    ```

2. Verify the PDO extension is enabled by editing the PHP configuration file.

    ```bash
    vim /etc/php/7.4/apache2/php.ini
    ```

3. Ensure `extension=pgsql` is uncommented in the file, then save your changes.

4. Create a PHP file named `main.php` with the following code:

    ```php
    <?php
    function sql_exec($stmt, $sql) {
    print("> ".strtoupper($sql)."\n");
    $rowCount = $stmt->rowCount();
    if ($rowCount > 0) {
        $colCount = $stmt->columnCount();
        if ($colCount > 0 ) {
        $out = array();
        $divs = array();
        for ($i = 0; $i < $colCount; $i++ ) {
            $cell = "  {$stmt->getColumnMeta($i)["name"]}  ";
            array_push($out, $cell);
            array_push($divs, str_repeat("-", strlen($cell)));
        }
        print(implode(" | ", $out)."\n".implode("-+-", $divs)."\n");
        }
        for ($r = 0; $r < $rowCount; $r++ ) {
        $row = $stmt->fetch();
        if (count($row) < 1) {
            continue;
        }
        $out = array();
        for ($c = 0; $c < $colCount; $c++) {
            array_push($out, "  {$row[$c]}  ");
        }
        print(implode(" | ", $out)."\n");
        }
        print("({$rowCount} rows)\n");
    }
    }

    //$conn = "pgsql:host=127.0.0.1 port=26257 user=root password=KWdb!2022";
    $conn = "pgsql:host=127.0.0.1 port=26257 user=root";

    $conn = $conn." sslmode=verify-ca sslcert=/home/inspur/src/gitee.com/kwbasedb/install/certs/client.root.crt";
    $conn = $conn." sslkey=/home/inspur/src/gitee.com/kwbasedb/install/certs/client.root.key";
    $conn = $conn." sslrootcert=/home/inspur/src/gitee.com/kwbasedb/install/certs/ca.crt";

    // Create connection
    $db = new PDO($conn) or die("Failed to create connection");
    // Read SQL file
    $fd = fopen("test.sql", "r") or die("Failed to open file");
    $sql = "";
    while(!empty($line = fgets($fd))) {
        if(substr(ltrim($line),0,2) == "--") {
        continue;
        }
        $sql = $sql.$line;
        if(substr(rtrim($sql), -1) == ";") {
        $stmt = $db->query($sql);
        if(!$stmt) {
            die($db->errorInfo());
        } else {
            sql_exec($stmt, $sql);
        }
        $sql = "";
        }
    }

    fclose($fd);
    ?>
    ```

5. Run the sample program:

    ```bash
    php main.php
    ```
