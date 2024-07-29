---
title: MyBatis-Plus
id: connect-mybatis-plus
---

# MyBatis-Plus 连接 KWDB 数据库

[MyBatis-Plus](https://baomidou.com/getting-started/) 基于 MyBatis 进行扩展，支持更多便捷功能。例如，条件构造器、分页插件、代码生成器等，有助于提高开发效率。

本文档介绍如何基于 SpringBoot+Maven 项目使用 MyBatis-Plus 连接 KWDB。用户在完成配置后，可以基于 MyBatis-Plus 框架的应用程序开发流程，编写应用程序对 KWDB 数据库进行操作。

## 前提条件

- [安装 Java](https://docs.oracle.com/en/java/javase/22/install/overview-jdk-installation.html)（1.8 及以上版本）。
- [安装 Maven](https://maven.apache.org/install.html)（3.6 及以上版本）。
- 安装 KWDB 数据库、配置数据库认证方式、创建数据库。
- 获取 KaiwuDB JDBC 驱动包。

## 配置连接

1. 运行以下命令，将 KaiwuDB JDBC 安装到本地 Maven 仓库中。

    ```shell
    mvn install:install-file"-Dfile=../kaiwudb-jdbc.2.0.2.jar" "-DgroupId=com.kaiwudb" "-DartifactId=kaiwudb-jdbc" "-Dversion=2.0.2" "-Dpackaging=jar"
    ```

2. 在 `pom.xml` 中添加依赖，将 KaiwuDB JDBC、MyBatis-Plus、Lombok 等依赖引入到应用程序中。

    ```xml
    <dependencies>
        <dependency>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-starter</artifactId>
        </dependency>

        <!-- web -->
        <dependency>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <!-- kaiwudb-jdbc -->
        <dependency>
          <groupId>com.kaiwudb</groupId>
          <artifactId>kaiwudb-jdbc</artifactId>
          <version>2.0.2</version>
        </dependency>

        <!-- mybatis plus -->
        <dependency>
          <groupId>com.baomidou</groupId>
          <artifactId>mybatis-plus-boot-starter</artifactId>
          <version>3.5.3.1</version>
        </dependency>

        <!-- swagger -->
        <dependency>
          <groupId>com.github.xiaoymin</groupId>
          <artifactId>knife4j-spring-boot-starter</artifactId>
          <version>2.0.3</version>
        </dependency>

        <!-- lombok -->
        <dependency>
          <groupId>org.projectlombok</groupId>
          <artifactId>lombok</artifactId>
          <version>1.18.28</version>
          <scope>provided</scope>
        </dependency>
      </dependencies>
    ```

3. 配置数据源。

    在 `application.yml` 文件配置数据源信息。

    ::: warning 说明
    以下示例展示如何连接单个数据库。如需要连接多个数据库，参见 [MyBatis 配置示例](./connect-mybatis.md)。
    :::

    ```yaml
    spring: 
      # 配置数据源信息
      datasource:
        # 配置连接数据库信息
        driver-class-name: com.kaiwudb.Driver
        url: jdbc:kaiwudb://127.0.0.1:26257/lyvs
        username: <user_name>
        password: <password>

    # Swagger-UI 配置
    knife4j:
      enable: true
      basic:
        enable: false
        username: root
        password: <password>

    # 服务启动端⼝配置
    server:
      port: 8989 
    ```

## 配置举例

以下示例假设已经在数据库中创建了名为**危化品车辆**的表，批量插入了部分数据，并提供外部接口来接受外部请求。

1. 编写实体类 `whp.java`。

    ```java
    @Data
    public class Whp {
      private Timestamp gtime = new Timestamp(System.currentTimeMillis());
      private String transporttaskno = "transporttaskno";
      private String hipperId = "hipperId";
      private String hipperName = "hipperName";
      private String hipperPhone = "hipperPhone";
      private String transportId = "transportId";
      private String transportName = "transportName";
      private String transportPhone = "transportPhone";
      private String transportZi = "1";
      private String transportNo = "transportNo";
      private String jjlxdh = "jjlxdh";
      private String cmvecid = "cmvecid";
      private String branum = "branum";
      private String vectype = "1";
      private String bracolor = "2";
      private String supercargoid = "supercargoid";
      private String supercargoname = "supercargoname";
      private String supercargonum = "supercargonum";
      private String supercargophone = "supercargophone";
      private String driverid = "driverid";
      private String drivernum = "drivernum";
      private String drivername = "drivername";
      private String driverphone = "driverphone";
    }
    ```

2. 创建 Mapper 接口类映射的 `xml` 文件。

    ```xml
    <?xml
      version="1.0" encoding="UTF-8"?>

      <!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
      "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

      <mapper namespace="com.inspur.kwdb.mapper.WhpMapper">

    <insert id="insertList"
    parameterType="java.util.List">
    insert into dcjg_whp_wxhwdlysdzqd  (gtime,transporttaskno,hipper_id,hipper_name,hipper_phone,transport_id,transport_name,transport_phone,transport_zi,transport_no,jjlxdh,cmvecid,branum,vectype,bracolor,supercargoid,supercargoname,supercargonum,supercargophone,driverid,drivernum,drivername,driverphone)
    values
    <foreach
    collection="list" item="item" separator=",">
    ('${item.gtime}',
    '${item.transporttaskno}',
    '${item.hipperId}',
    '${item.hipperName}',
    '${item.hipperPhone}',
    '${item.transportId}',
    '${item.transportName}',
    '${item.transportPhone}',
    '${item.transportZi}',
    '${item.transportNo}',
    '${item.jjlxdh}',
    '${item.cmvecid}',
    '${item.branum}',
    '${item.vectype}',
    '${item.bracolor}',
    '${item.supercargoid}',
    '${item.supercargoname}',
    '${item.supercargonum}',
    '${item.supercargophone}',
    '${item.driverid}',
    '${item.drivernum}',
    '${item.drivername}',
    '${item.driverphone}')
    </foreach>
    </insert>
    </mapper>
    ```

3. 创建 Service 接口 `WhpService.java`。

    ```java
    public interface WhpService {
      void createTable();
      int insertList();
      List<Whp> findList();
    }
    ```

4. 创建 Service 接口实现类。

    ```java
    @Service
    class WhpServiceImpl implements WhpService {
    @Autowired
    private WhpMapper mapper;

    @Override
    public void createTable() {
    mapper.createTable();
    }

    @Override
    public int insertList() {
    List<Whp> list = new ArrayList<>();
    list.add(new Whp());
    list.add(new Whp());
    list.add(new Whp());
    return mapper.insertList(list);
    }

    @Override
    public List<Whp> findList() {
    Timestamp startTime = Timestamp.valueOf("2023-11-01 00:00:00");
    Timestamp endTime = Timestamp.valueOf("2023-11-30 23:59:59");
    return mapper.findList(startTime,endTime);
    }
    }
    ```

5. 创建外部接口，访问 Controller 层。

    ```java
    @RestController
    @RequestMapping("whp")
    @Api(tags = "1 危化品车辆接口")
    @ApiSort(value = 1)
    public class WhpController {
      private final static Logger LOGGER = LoggerFactory.getLogger(WhpController.class);

      @Autowired
      private WhpService service;

      @ApiOperation(value = "1.1 创建危化品车辆表")
      @ApiOperationSupport(order = 10)
      @GetMapping("create")
      public String create() {
        try {
          service.createTable();
          return "创建危化品车辆表成功";
        } catch (Exception e) {
          LOGGER.info(e.getMessage());
          return "创建危化品车辆表失败: " + e.getMessage();
        }
      }

      @ApiOperation(value = "1.2 批量插入危化品车辆数据")
      @ApiOperationSupport(order = 20)
      @GetMapping("add")
      public int add() {
        try {
          return service.insertList();
        } catch (Exception e) {
          LOGGER.info(e.getMessage());
        }
        return 0;
      }

      @ApiOperation(value = "1.3 查询危化品车辆数据列表")
      @ApiOperationSupport(order = 30)
      @GetMapping("list")
      public List<Whp> findList() {
        try {
          return service.findList();
        } catch (Exception e) {
          LOGGER.info(e.getMessage());
        }
        return null;
      }

    }
    ```
