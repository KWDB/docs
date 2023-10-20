# 安装部署

本手册介绍了KaiwuDB 1.0系列的产品规格、Docker部署及编译部署方式。

## 系统说明

### 1.1 软件规格

如果您使用Docker容器部署KaiwuDB数据库，则操作系统需要支持安装Docker Engine。KaiwuDB支持Ubuntu、Debian、Red Hat等Linux操作系统以及安装WSL的Windows系统。

Docker部署软件建议列表

|机器类型     | 操作系统      |  程序开发环境                        |
|:-------------|:--------------|:------------------------------------- |
|  Virtual Machine （Intel-based）| Ubuntu-18.04.6 LTS| - Docker-Compose 1.17.1 <br>- Docker 20.10.17 |
| Raspberry Pi 4 Model B 单板计算机 (ARM-based) | Ubuntu 20.04.4 LTS (GNU/Linux 5.4.0-1065-raspi aarch64) | - Docker-Compose 1.17.1 <br>- Docker 20.10.17  |

如果您使用代码编译的方式部署KaiwuDB数据库，只需在相应的Linux系统中安装相应的编译依赖即可。
编译部署软件建议列表

| 机器类型     | 操作系统      |  编译依赖                       |
|:------------|:--------------|:------------------------------------- |
|  Virtual Machine （Intel-based）| Ubuntu 20.04.4 LTS (GNU/Linux 5.4.0-1065-raspi aarch64) | - cmake <br> - gcc <br> - g++ <br>- libssl-dev|
| Raspberry Pi 4 Model B 单板计算机 (ARM-based) | Ubuntu 20.04.4 LTS (GNU/Linux 5.4.0-1065-raspi aarch64) | - cmake <br> - gcc <br> - g++ <br>- libssl-dev |


### 1.2 硬件规格

硬件规格建议不低于4核8G，磁盘SSD，以确保不影响KaiwuDB的性能。

硬件建议列表

| 机器类型      | 硬件规格                                      |
|:-------------|:---------------------------------------------- |
| Virtual Machine （Intel-based）| - CPU/微处理器：8 core <br> - RAM/内存：64 GB<br>- HDD/硬盘空间：根据数据量大小确定(建议SSD)<br>- Network/网卡速限：1 Gb/s |
| Raspberry Pi 4 Model B 单板计算机 (ARM-based) | - CPU/微处理器：Broadcom BCM2711, Quad core Cortex-A72 (ARM v8) 64-bit SoC @ 1.5GHz <br> - RAM/内存：8GB LPDDR4-2400 SDRAM <br> - HDD/硬盘空间：根据数据量大小确定(建议SSD) <br> - Network/网卡速限：100 Mb/s|


## Docker部署

您可以采用Docker方式在线或者离线部署KaiwuDB数据库。

### 在线Docker部署

若未安装Docker，需先安装Docker，然后拉取KaiwuDB镜像、启动容器。若已安装Docker，则可直接拉取镜像、启动容器。

KaiwuDB支持以下三种启动方式：

- 单节点单实例启动，即一台机器上启动一个KaiwuDB服务。KaiwuDB支持通过``docker run``命令或Docker Compose工具启动服务，推荐采用Docker Compose。
- 单节点多实例启动，即一台机器上启动多个KaiwuDB服务，通过启动多个KaiwuDB节点，构成一个集群。
- 多节点多实例启动，即在多台机器上启动多个KaiwuDB服务，通过启动多个KaiwuDB节点，构成一个集群，来提升写入性能和查询性能。

#### 安装Docker

1. 卸载旧版本的Docker（如已安装）。
   ```shell
   [root@node1] apt-get autoremove docker docker-ce docker-engine docker.io containerd runc
   apt-get autoremove docker-ce-*
   dpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P  # 删除无用的相关的配置文件
   rm -rf /etc/systemd/system/docker.service.d
   rm -rf /var/lib/docker
   ```
2. 安装GCC、G++ 编译器以及相关依赖包。
   ```shell
   apt install -y gcc g++
   ```
3. 设置仓库地址 。
   ```shell   
   echo -e "deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse \ndeb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse \ndeb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse \ndeb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse" > /etc/apt/sources.list
   ```
   >**注**：由于Docker默认采用国外仓库地址，建议配置国内仓库镜像地址，提高下载速度。

4. 更新apt软件包索引。
   ```shell 
   apt-get update
   apt-get upgrade 
   ```
5. 安装Docker。
   ```shell 
   [root@node1] apt-get install docker.io containerd
   ```
6. 设置Docker自启动并启动Docker服务。
   ```shell 
   [root@node1] systemctl enable docker
   [root@node1] systemctl start docker
   ```
#### 单节点单实例启动

KaiwuDB支持通过``docker run``命令或Docker Compose启动KaiwuDB服务，推荐使用Docker Compose。

##### 使用docker run命令启动KaiwuDB

1. 获取KaiwuDB镜像。
2. 加载KaiwuDB镜像。
   ```shell 
   [root@node1] docker load –i  <kaiwudb_image >.tar
   ```
3. 查看镜像。
   
   ```shell
   [root@node1] docker images
   REPOSITORY TAG IMAGE ID CREATED SIZE
   Kaiwudb 1.0 72cce2c0c971 2 weeks ago 161MB
   ```
   参数说明：
   - REPOSITORY：镜像仓库源;
   - TAG：镜像版本;
   - IMAGE ID：镜像id;
   - CREATED：镜像创建时间;
   - SIZE：镜像大小。

4. 启动运行数据库实例。
   
   ```shell
   [root@node1] docker run -t -d –name  <container_name > -p  <host_port >: <container_port > -p  <host_port >: <container_port > -v  <host_directory >: <container_directory > -v  <host_directory >: <container_directory > kaiwudb
   ```

   参数说明:
   - \-t：分配TTY设备，可以支持终端登录，默认为false；
   - \-d：指定容器运行于前台还是后台，默认为false（后台）；
   - \-name：指定容器名称，后续可通过名称进行容器管理；
   - \-p：指定容器暴露的端口，冒号前为宿主机端口，冒号后为容器内的映射端口；
   - \-v：表示目录映射关系，冒号前为宿主机目录，冒号后为容器内目录；
   - kaiwudb：要启动的镜像名。

   示例：
   ```shell
   [root@node1] docker run -t -d --name test –p 9091:9091 -p 3306:3306 -v /opt/data:/srv/kaiwudb/ds -v /opt/csvfile:/srv/kaiwudb/file kaiwudb
   3d9fd19ebfead04e64769bdeb094aba64384e3a1666d45db19d6fa5fc8c02dae
   ```
5. 查看容器运行状态。
   ```shell
   [root@node1] docker ps
   ```

   示例：
   ```shell
   [root@node1] docker ps
   CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
   3d9fd19ebfea kaiwudb1.0 "/entrypoint.sh bosr…" 12 minutes ago Up 12 minutes 0.0.0.0:3306- >3306/tcp, :::3306- >3306/tcp, 0.0.0.0:9091- >9091/tcp, :::9091- >9091/tcp, 6060/tcp test
   ```
   参数说明:
   - CONTAINER ID：容器ID;
   - IMAGE：镜像名;
   - COMMAND：启动命令;
   - CREATED：容器创建时间;
   - STATUS：启动时间;
   - PORTS：端口映射情况;
   - NAMES：容器名称。
6. 安装MySQL客户端。
   ```shell
   [root@node1] yum install –y mariadb
   ```   
7. 连接数据库。
   ```shell
   [root@node1] mysql -P  <port > -h 127.0.0.1 -u root -p
   ```
   > 注：默认无密码。

   示例：
   ```shell
   [root@node1] mysql -P 3306 -h 127.0.0.1 -u root -p
   Enter password:
   Welcome to the MariaDB monitor. Commands end with ; or \g.
   Your MySQL connection id is 4
   Server version: 5.6.22 KaiwuDB1.0
   Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.
   Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
   ```

##### 使用Docker Compose启动KaiwuDB

1. 下载Docker Compose。
   ```shell
   [root@node2  ~] # curl -L [https://get.daocloud.io/docker/compose/releases/download/1.25.4/](https://get.daocloud.io/docker/compose/releases/download/1.25.4/) docker-compose-`uname -s`- `uname -m `> /usr/local/bin/docker-compose
   ```

   示例：
   ```shell
   [root@node2  ~] # curl -L [https://get.daocloud.io/docker/compose/releases/download/1.25.4/](https://get.daocloud.io/docker/compose/releases/download/1.25.4/) docker-compose-`uname -s `-`uname -m`> /usr/local/bin/docker-compose
   % Total % Received % Xferd Average Speed Time Time Time Current
   Dload Upload Total Spent Left Speed
   100 423 100 423 0 0 434 0 --:--:-- --:--:-- --:--:-- 434
   100 16.3M 100 16.3M 0 0 1066k 0 0:00:15 0:00:15 --:--:-- 1138k
   ```
2. 为Docker Compose文件添加可执行权限。
   ```shell
   [root@node2 ~]# chmod +x /usr/local/bin/docker-compose
   ```
3. 查看Docker Compose版本， 验证是否安装成功。
   ```shell  
   [root@node2 ~]# docker-compose -v
   docker-compose version 1.25.4, build 8d51620a
   ```   
4. 创建KaiwuDB服务的YML文件。
   ```shell 
   [root@node2 ~]# vim <file_name>.yml
   ```
   示例：
   ```shell 
   [root@node2 ~]# vim docker-compose-kaiwudb.yml
   ```  
5. 编辑KaiwuDB服务的YML文件。

   ```shell 
   version: "3.0"
   services:
     kaiwudb:
       image: kaiwudb:1.0
       container_name: kaiwudb
       privileged: true
       ports:
          - "53306:3306"
          - "59091:9091"
       volumes:
          - /opt/szq/data:/srv/kaiwudb/ds
          - /opt/szq/config:/srv/kaiwudb/config
          - /opt/szq/csvfile:/srv/kaiwudb/file
          - /opt/szq/log:/srv/kaiwudb/log
   environment:
       TZ: Asia/Shanghai
       KW_STREAM_CONN_LIMIT: 200
       KW_IOT_MODE: 'true'
   ```
   参数说明：

   - Image：KaiwuDB镜像版本，例如kaiwudb:1.0；
   - container_name：容器名称；
   - privileged：是否给容器root权限；
   - ports: 容器映射的port号，类似于docker run的-p参数；
   - volumes: 容器挂载出来的目录，类似于docker run的 -v参数；
   - environment: 容器中的环境变量。下表列出了目前可配置的环境变量：

     | 参数名称            | 说明                      | 示例                     |
     |:--------------------|:--------------------------|:-----------------------|
     | TZ                 | 时区                        | TZ:Asia/Taipei      |
     | version            | 版本                        | 1.0                  |
     | license            | 许可                        | 2022-11-19/kaiwudb/enterprise |
     | date_format        | date格式                    | KW_DATE_FORMAT: '%Y-%m-%d'  |
     | datetime_format    | datetime格式       | KW_DATETIME_FORMAT: '%Y-%m-%d %H:%M:%S' |
     | iot_interval       | iot模式下切换 partition的区间  | KW_INTERVAL:86400      |
     | iot_mode           | 是否为iot模式                  | KW_IOT_MODE:‘true’        |
     | logging            | Log等级。等级越高log越详细     | KW_LOGGING: 4     |
     | max_connections    | 3306联机的最大数量             | KW_MAX_CONNECTION: 200  |
     | max_log_files      | log档案最多保留数量            | KW_MAX_LOG_FILES: 30 |
     | precision          | 浮点数精度                     | KW_PRECISION:2  |
     | stream_cache_size  | 9091 buffer的大小             | KW_STREAM_CACHE_SIZE:1000  |
     | stream_conn_limit  | 9091联机的最大联机数           | KW_STREAM_CONN_LIMIT:200  |
     | table_type         | table为column-based或row-based | KW_TABLE_TYPE:‘cloumm’   |
     | zero_if_null       | 当数据为NULL时改成0            | KW_ZERO_IF_NULL:‘true’    |

6. 启动KaiwuDB服务：
   ```shell 
   [root@node2 ~]# docker-compose -f <file_name>.yml up -d
   ```   

   示例：
   ```shell
   [root@node2 ~]# docker-compose -f docker-compose-kaiwudb.yml up -d
   Creating network "root_default" with the default driver
   Pulling kaiwudb (kaiwudb:1.0)...
   1.9.0-iot: Pulling from kaiwudb
   1e55473b472a: Already exists
   908ff2f8860c: Already exists
   a30eeb63f077: Already exists
   4c5d71ff6fd5: Already exists
   02121fa5de00: Already exists
   Digest: sha256:5b3bf413b63e4baf23de0c17f809508c81ca5bd63a8bb5b87f01b60248fa6647
   Status: Downloaded newer image for kaiwudb:1.0
   Creating kaiwudb ... done
   ```   
7. 连接数据库。
   ```shell
   [root@node2~]# mysql -P <port> -h 127.0.0.1 -u root -p
   ```   
   示例：
   ```shell
   [root@node2 ~]# mysql -P 53306 -h 127.0.0.1 -p
   Enter password:
   Welcome to the MariaDB monitor. Commands end with ; or \g.
   Your MySQL connection id is 22
   Server version: 5.6.22 KaiwuDB1.0
   Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.
   Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
   ``` 

#### 单节点多实例启动

KaiwuDB支持在单节点上部署多个实例。每个实例的映射port和数据文件地址必须不同。

1. 使用以下命令在同一节点上启动两个实例：
   ```shell
   [root@node1] docker run -t -d –name <container_name> -p <host_port>:<container_port> -p <host_port>:<container_port> -v <host_directory>:<container_directory> -v <host_directory>:<container_directory> kaiwudb
   ```
   参数说明：

   - \-t：分配TTY设备，可以支持终端登录，默认为false；
   - \-d：指定容器运行于前台还是后台，默认为false（后台）；
   - \-name：指定容器名称，后续可通过名称进行容器管理；
   - \-p：指定容器暴露的端口，冒号前为宿主机端口，冒号后为容器内的映射端口；
   - \-v：表示目录映射关系，冒号前为宿主机目录，冒号后为容器内目录；
   -  kaiwudb：要启动的镜像名。

   示例：
   ```shell
   [root@node1] docker run -t -d --name test1 -p 19091:9091 -p 13306:3306 -v /opt/data1:/srv/kaiwudb/ds -v /opt/csvfile1:/srv/kaiwudb/file kaiwudb
   d200fbcbe1e38d061112acfb8f57bad334f986053bc47dfbd5e2f10372a17776
   [root@node1] docker run -t -d --name test2 -p 29091:9091 -p 23306:3306 -v /opt/data2:/srv/kaiwudb/ds -v /opt/csvfile2:/srv/kaiwudb/file kaiwudb
   51c465ba1a94456b54808aa4aee6c7447c878306955e8f1be41ceb69d8430986
   ```
2. 查看容器运行状态。

   ```shell
   [root@node1] docker ps
   CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
   51c465ba1a94 kaiwudb1.0 "/entrypoint.sh bosr…" 20 seconds ago Up 19 seconds 6060/tcp, 0.0.0.0:23306->3306/tcp, :::23306->3306/tcp, 0.0.0.0:29091->9091/tcp, :::29091->9091/tcp test
   d200fbcbe1e3 kaiwudb1.0 "/entrypoint.sh bosr…" 28 seconds ago Up 26 seconds 6060/tcp, 0.0.0.0:13306->3306/tcp, :::13306->3306/tcp, 0.0.0.0:19091->9091/tcp, :::19091->9091/tcp test1
   ```  
3. 创建database和table。

   - 进入实例1，创建相应的database、table，插入数据。

      ```shell
      [root@node1] mysql -P 13306 -h 127.0.0.1 -u root -p
      Enter password:
      Welcome to the MariaDB monitor. Commands end with ; or \g.
      Your MySQL connection id is 4
      Server version: 5.6.22 KaiwuDB1.0
      Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.
      Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
      [(none)] create database test2;
      Query OK, 0 rows affected (0.00 sec)
      [(none)] use test2;
      Database changed
      [(none)] create table t(id int,name varchar(10));
      Query OK, 0 rows affected (0.00 sec)
      [(none)] insert into t values(1,'test2');
      Query OK, 0 rows affected (0.00 sec)
      [(none)] select * from t; +------+-------+
      | id  | name  |
      +------+-------+
      | 1   | test2 |
      +------+-------+
      1 row in set (0.00 sec)
      ``` 
    - 进入实例2，创建相应的database、table，插入数据。

        ```shell
       [root@node1] mysql -P 23306 -h 127.0.0.1 -u root -p
       Enter password:
       Welcome to the MariaDB monitor. Commands end with ; or \g.
       Your MySQL connection id is 4
       Server version: 5.6.22 KaiwuDB1.0
       Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.
       Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
       [(none)] create database test2;
       Query OK, 0 rows affected (0.00 sec)
       [(none)] use test2;
       Database changed
       [(none)] create table t(id int,name varchar(10));
       Query OK, 0 rows affected (0.00 sec)
       [(none)] insert into t values(2,'test1');
       Query OK, 0 rows affected (0.00 sec)
       [(none)] select * from t;
       +------+-------+
       | id  | name  |
       +------+-------+
       | 2  | test1  |
       +------+-------+
       1 row in set (0.00 sec)
        ```

4. 查看集群状态。

   ```shell
   [(none)] show cluster;
   Empty set (0.00 sec)
   ``` 
5. 添加集群Client，其中：
   - ip为实例所在节点的IP。
   - db为在实例中创建的database。
   - port为启动KaiwuDB服务时的port，建议取9091映射的port。

   ```shell
   [(none)] ADD CLIENT ip="192.168.26.101" db="test2" port="19091";
   Query OK, 0 rows affected (0.00 sec)
   [(none)] ADD CLIENT ip="192.168.26.101" db="test2" port="29091";
   Query OK, 0 rows affected (0.00 sec)
    ``` 
6. 再次查看集群状态。

   ```shell
   [(none)] show cluster;
   +----------------+----------------+-------+-------+------+-------+
   | host           | ip             | port  | db    | type | alias |
   +----------------+----------------+-------+-------+------+-------+
   | 192.168.26.101 | 192.168.26.101 | 19091 | test2 |      |       |
   | 192.168.26.101 | 192.168.26.101 | 29091 | test2 |      |       |
   +----------------+----------------+-------+-------+------+-------+
   2 rows in set (0.00 sec)
    ``` 
7. 使用CLUSTER SELECT语句验证集群查询是否成功，查出多个Client所有的数据即为集群部署成功。

   示例：
   ```shell
   [(none)]> cluster select * from t;
   +------+-------+
   | id   | name  |
   +------+-------+
   | 1    | test2 |
   | 2    | test1 |
   +------+-------+
   2 rows in set (0.00 sec)
   ```

### Docker离线部署

KaiwuDB离线安装主要通过以下步骤：

1. 离线安装Docker；如Docker已安装，则直接执行第3步，启动KaiwuDB服务。
2. 启动KaiwuDB服务。

> **注**：单节点多实例启动的操作步骤同[单节点单实例启动](#单节点单实例启动)一致。

#### 离线安装Docker

1. 在联网机器上下载Docker。
   ```shell   
   [root@online] wget https://download.docker.com/linux/static/stable/x86_64/docker-20.10.9.tgz
   ```
2. 将包上传到离线服务器中。

   ```shell
   [root@online] scp docker-20.10.9.tgz root@192.168.26.100:/root 
   ```  
3. 解压包并复制到/usr/bin目录下。  

   ```shell
   [root@offline] tar xvf docker-20.10.9.tgz
   cp docker/* /usr/bin
   ``` 
4. 配置Docker服务。 
   ```shell
   [root@offline] touch /etc/systemd/system/docker.service
   echo -e "[Unit]\n \nescription=Docker Application Container Engine \n \nDocumentation=https://docs.docker.com\n \nAfter=network-online.target firewalld.service \n \nWants=network-online.target \n \n \n[Service]\n \nType=notify \n \nExecStart=/usr/bin/dockerd \n \nExecReload=/bin/kill -s HUP $MAINPID \n \nLimitNOFILE=infinity \n \nLimitNPROC=infinity \n \nTimeoutStartSec=0 \n \nDelegate=yes \n \nKillMode=process \n \nRestart=on-failure \n \nStartLimitBurst=3 \n \nStartLimitInterval=60s \n \n \n[Install]\n \nWantedBy=multi-user.target" > /etc/systemd/system/docker.service
   ```
5. 赋执行权限
   ```shell
   [root@offline] chmod +x /etc/systemd/system/docker.service
   systemctl daemon-reload
   ```
6. 启动Docker。
   ```shell
   [root@offline] systemctl enable docker
   [root@offline] systemctl start docker
   ```   
7. 查看Docker版本，确认Docker已安装成功。

   ```shell
   [root@offline] docker version
   Client: Docker Engine - Community
   Version: 20.10.21
   API version: 1.41
   Go version: go1.18.7
   Git commit: baeda1f
   Built: Tue Oct 25 18:04:24 2022
   OS/Arch: linux/amd64
   Context: default
   Experimental: true
   ``` 
#### 启动KaiwuDB服务

1. 获取KaiwuDB镜像。
2. 加载KaiwuDB镜像。
   ```shell 
   [root@online] docker load –i <kaiwudb_image>.tar
   ```    
3. 查看镜像。

   ```shell 
   [root@online] docker images
   REPOSITORY TAG IMAGE ID CREATED SIZE
   Kaiwudb 1.0 72cce2c0c971 3 weeks ago 161MB
   ```   
4. 保存镜像到本地。

   ```shell 
   [root@online] docker save 72cce2c0c971 > bo.tar
   ```   
5. 将镜像上传到离线服务器上 。

   ```shell   
   [root@online] scp bo.tar root@192.168.26.100:/root
   ``` 
6. 加载镜像到离线服务器的Docker中。
   ```shell  
   [root@offline] docker load < bo.tar
   ``` 
7. 验证是否加载成功。

    ```shell  
    [root@offline] docker images
    REPOSITORY TAG IMAGE ID CREATED SIZE
    <none> <none> 72cce2c0c971 3 weeks ago 161MB
    ``` 
8. 修改tag。

   ```shell  
   [root@offline] docker tag 72cce2c0c971 kaiwudb:latest
   ```
9. 启动KaiwuDB。

   ```shell  
   [root@offline] docker run -t -d --name test -p9091:9091 -p 3306:3306 -v /opt/data:/srv/kaiwudb/ds -v /opt/csvfile:/srv/kaiwudb/file kaiwudb:latest
   ```
10. 查看容器状态。

    ```shell  
    [root@offline] docker ps
    CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
    28898aa55fcc kaiwudb1.0 "/entrypoint.sh bosr…" 10 days ago Up 2 days 6060/tcp, 0.0.0.0:43306->3306/tcp, :::43306->3306/tcp, 0.0.0.0:49091->9091/tcp, :::49091->9091/tcp ok1
    ```
11. 连接数据库。
    ```shell 
    [root@offline] mysql -P 3306 -h 127.0.0.1 -u root -p
    Enter password:
    Welcome to the MariaDB monitor. Commands end with ; or \g.
    Your MySQL connection id is 4
    Server version: 5.6.22 KaiwuDB1.0
    Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.
    Type 'help;' or '\h' for help. Type '\c' to clear the current input statemen.   
    ```

## Ubuntu20.04系统环境编译部署

### 安装运行环境

1. 安装编译所需的GO、GCC、G++、cmake、openssl。

   ```shell 
   apt update
   apt install cmake gcc g++ libssl-dev wget
   cd /home && wget https://dl.google.com/go/go1.19.5.linux-amd64.tar.gz && tar -C /usr/local/ -xvf /home/go1.19.5.linux-amd64.tar.gz
   echo -e "export GOPATH=/home\nexport PATH=/usr/local/go/bin:/bin:$PATH\nexport GOPROXY=https://goproxy.cn" >> /etc/profile
   source /etc/profile
   ```
2. 配置数据库运行所需的数据目录。
   ```shell 
   mkdir -p /srv/kaiwudb/script && mkdir /etc/kw 
   # 进入下载的kaiwuDB/代码目录
   cd kaiwuDB/
   cp ./code/kwsrv/script/_init_kaiwu /srv/kaiwudb/script/_init_infoschema
   ```
### 编译数据库

1. 在下载的kaiwuDB代码目录下执行编译:
   ```shell 
   mkdir build && cd build && cmake .. && make -j4 && make install
   ```
2. 完成编译后，返回到上级kaiwuDB目录。
   
### 运行KaiwuDB

1. 在下载的kaiwuDB代码目录下执行启动:
   ```shell 
   LD_LIBRARY_PATH=./kaiwu_target/lib ./kaiwu_target/bin/kwsrvd
   ```
2. 出现类似如下结果，代表KaiwuDB已启动成功，可以通过mysql client连接使用。
   ```shell 
   -----go----- [KWINF] VEersion KaiwuDB   
   -----go----- [KWINF] number of workers: 12
   -----go----- [KWINF] number of CPU: 12    
   -----go----- [KWINF] KaiwuDB Master node
   -----go----- [KWINF] KaiwuDB Analytics is starting...
   ```    