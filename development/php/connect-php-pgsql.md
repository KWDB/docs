---
title: PHP pgsql
id: connect-php-pgsql
---

# 使用 PHP 和 PDO 连接 KWDB

PHP 是一种广泛使用的开源服务器端脚本语言，特别适合用于 Web 开发。PHP 数据对象（PDO）扩展提供了轻量级且统一的接口，支持用户在 PHP 中访问数据库。

本示例演示了如何通过 PHP 和 PDO 扩展连接 KWDB，执行 SQL 语句。

## 前提条件

- 安装和运行 KWDB 数据库、配置数据库认证方式、创建数据库。
- 创建具有表级别及以上操作权限的用户。

## 配置示例

1. 安装 PHP 和 PDO 扩展。

    ```bash
    sudo apt install php
    sudo apt install php-pgsql
    ```

2. 打开 PDO 扩展配置文件。

    ```bash
    vim /etc/php/7.4/apache2/php.ini
    ```

3. 在文件中添加 `extension=pgsql` 后保存配置文件。

4. 创建名为 `main.php` 的 PHP 文件，并将以下示例代码复制到文件中：

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

    // 创建连接
    $db = new PDO($conn) or die("创建连接失败");
    // 读取执行文件
    $fd = fopen("test.sql", "r") or die("打开文件失败");
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

5. 执行示例程序。

    ```bash
    php main.php
    ```
