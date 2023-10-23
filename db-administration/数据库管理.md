# 数据库管理

## 启动数据库

```shell
docker start [<container_id> | <container_name>]
```

## 暂停数据库

```shell
docker stop [<container_id> | <container_name>]
```

## 删除数据库

```shell
docker rm [<container_id> | <container_name>]
```

## 登录和退出数据库

KaiwuDB内置交互式SQL客户端，用于从交互式shell程序或直接从命令行执行SQL语句。

### 示例

- 启动交互式SQL Shell

```sql
mysql -h test01 -P 3306 -u root -p  
Enter password:  
Welcome to the MariaDB monitor. Commands end with; or \g.  
Your MySQL connection id is 122  
Server version: 5.6.22 KaiwuDB1.0  
Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.  
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.  
>
```

- 退出交互式SQL Shell：使用\\q，quit，exit，或者ctrl-d

## 查看数据库状态

```shell
docker ps –a
```

示例：

查看数据库实例状态，UP为启动状态。

```shell
docker ps -a
CONTAINER ID   IMAGE         COMMAND                  CREATED       STATUS       PORTS                  NAMES
95dc2ddd91d9   kaiwudb:1.0   "/entrypoint.sh bosr…"   4 weeks ago   Up 15 hours   0.0.0.0:3306->3306/tcp, :::3306->3306/tcp, 0.0.0.0:9091->9091/tcp, :::9091->9091/tcp, 6060/tcp   test1
```

## 用户管理

### 创建用户

CREATE USER语句用于创建数据库用户。

#### 语法格式

```sql
CREATE USER <user_name> IDENTIFIED BY 'password';
```

- user_name：要创建的用户名, 不超过32个字符，无字符限制。
- password：用户密码,长度不超过79字符，不可以用反斜线 "\\" 单引号’，双引号”。

#### 语法示例

```sql
> CREATE USER testu1 IDENTIFIED BY 'test123';
Query OK, 0 rows affected (0.01 sec)
```

### 删除用户

DROP USER语句用于删除用户。

#### 语法格式

```sql
DROP USER <user_name>;
```

- user_name：要删除的用户名

#### 语法示例

```sql
> DROP USER user1;
DROP USER user1
```

