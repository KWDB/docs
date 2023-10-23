# 导入导出

## 数据导入

### MySQL客户端导入

用户可以使用MySQL客户端通过INSERT或LOAD命令导入数据。

- 使用INSERT将新行插入现有表
  
  示例：

```sql
> show create table testa;
| Table | Create Table                                               |
|-------|------------------------------------------------------------|
| testa | CREATE TABLE `testa` (
`a` int NOT NULL,
`b` varchar(10) NOT NULL,
`c` double NOT NULL,
`d` datetime NOT NULL
) ENGINE=TS |
1 row in set (0.01 sec)


> insert into testa values(6,'fff',2.5552,'2023-01-01 00:00:00');
Query OK, 1 row affected (0.00 sec)
```

- 使用LOAD语句批量导入csv文件

前提条件：已经把对应的内部路径映射到了外部某个路径，如下所示：

```shell
docker run --log-driver "syslog" --log-opts tag={{.Name}} --log-opts syslog-facility=local0 -t -d --name test -p 9090:9090 -p 9091:9091 -p 3306:3306 -v /opt/data:/srv/kaiwudb/ds -v /opt/csvfile:/srv/kaiwudb/file kaiwudb:1.0
```

步骤：

1. 将要导入的数据文件放到外部映射路径，然后参考以下命令：

```
LOAD DATA INFILE "filename" INTO TABLE <table_name>;
```

示例：csv文件load入库。

```sql
> select count(*) from testa;
+----------+
| COUNT(*) |
+----------+
| 6        |
+----------+
1 row in set (0.01 sec)

> load data infile "output.csv" into table testa;
Query OK, 6 rows affected (0.00 sec)

> select count(*) from testa;
+----------+
| COUNT(*) |
+----------+
| 12       |
+----------+
1 row in set (0.01 sec)
```

### 文件导入（9091端口）

要导入csv类型的文件，请参考以下命令：

```shell
(echo -e "csv\x01my_data_tbl" ; cat my_data.csv) > /dev/tcp/127.0.0.1/9091
```

或者：

```shell
(echo -e "csv\x01my_data_tbl" ; cat my_data.csv) | nc 127.0.0.1 9091
```

其中 `my_data_tbl` 是 `my_data.csv` 对应的数据库表。

如果想跳过csv文件开头的几行以达到跳过标题等目的，可以使用以下命令：

```shell
(echo -e "csv\x01my_data_tbl\x0skip_lines=10" ; cat my_data.csv) | nc 127.0.0.1 9091
```

上面的命令会跳过前10行。

示例：文件高速入库

```sql
select count(*) from testa;
+----------+
| COUNT(*) |
+----------+
| 18       |
+----------+
1 row in set (0.01 sec)

(echo -e "csv\x01db_energy.testa"; cat output.csv) >/dev/tcp/127.0.0.1/49091

select count(*) from testa;
+----------+
| COUNT(*) |
+----------+
| 24       |
+----------+
1 row in set (0.01 sec)
```

## 数据导出

数据导出命令参考如下：

```sql
mysql -h 127.0.0.1 -P <port> -s -N -e "command" | sed "s/'/\'/g;s/\"/\"\"/g;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > output.csv
```

示例：命令行导出数据。

```shell
mysql -h 127.0.0.1 -P 3306 -s -N -e"select * from db_energy.testa limit 10"|sed "s/'/\'/g;s/\"/\"\"/g;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > output.csv

cat output.csv
"1","aa","1.234","2022-12-14 10:00:20"
"2","bb","2.234","2022-12-14 11:00:20"
"3","cc","3.234","2022-12-14 12:00:20"
"4","dd","4.234","2022-12-14 13:00:20"
"5","ee","2.33333","2022-12-10 03:53:30"
"6","fff","2.5552","2022-12-14 10:10:10"
```

