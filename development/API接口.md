# API接口

KaiwuDB RESTFUL API旨在满足大多数开发人员的最低依赖性要求。开发人员可以通过HTTP到API端点将命令提交给KaiwuDB。

## HTTP请求

命令在HTTP POST主体中描述为JSON对象。可能的值是：

-   stmt：发表声明。
-   params(optional)：用于控制响应的JSON对象的附加参数。
-   size：返回的行数（从1到1000）。默认值为1000。

请求示例：

```
{
  "stmt": "SELECT * FROM sales LIMIT 100000",
  "params": {
    "size": 25
  }
}
```

## HTTP响应

KaiwuDB将使用HTTP状态代码200进行响应。

HTTP/1.1 200 OK

Content-Type: application/json

消息正文将包含以下JSON对象：

-   retcode：如果成功则为0，否则为负数。
-   errmsg：失败的错误信息。
-   meta：返回结果的描述字典。
-   results：返回的数据。

每个命令返回的JSON如下所述。

-   HTTP POST大小限制：HTTP POST大小限制为64MB字节。HTTP错误：如果post请求超过大小限制，将返回413（请求实体太大）。

### CREATE, DROP, INSERT, UPDATE, TRIM, GC(DEL, ALL)

- Returns
  - results: null

请求示例：

```
{
    "stmt": "CREATE TABLE Pi (id BIGINT not null default 0, method STRING not null default 'a', \`estimated_pi\` DOUBLE not null default 0.00)"
}
```

响应示例：

```
{
    "retcode": 0,
    "meta": {
    },
    "results": null
}
```

### SHOW

- Returns

  - meta

    - size: 返回的数据数


  - results: 返回的数据列表


请求报文示例：

```
{
    "stmt": "SHOW TABLES"
}
```

响应报文示例：

```
{
    "retcode": 0,
    "meta": {
        "size": 20
    },
    "results": [
        ["Product"],
        ["Customer"],
        ["sales"],
        ...
        ["facebook_likes_2012"]
    ]
}
```

### SELECT

- Params

  - handle (bool): 返回句柄 ID 供以后访问

- Returns

  - meta

    - size: 返回的数据数

    - next: 下一个起始索引。-1如果没有更多数据

  - results: 返回的数据列表。如果设置了参数，则返回句柄ID

请求报文示例：

```
{
    "stmt": "SELECT \* FROM Pi"
}
```

响应报文示例：

```
{
    "retcode": 0,
    "meta": {
      "size": 1000,
      "next": 1001
    },
    "results": [
      [1, "cosine", 3.14],
      [2, "maple", 3.141],
      [3, "monte-carlo", 3.1415],
      ...
    ]
}
```

示例请求正文（使用句柄）：

```
{
    "stmt": "SELECT * FROM Pi",
    "params": {
        "handle": true
  }
}
```

响应报文示例：

```
{
    "retcode": 0,
    "meta": {},
    "results": {
        "res": "12cf0a5dee76"
    }
}
```

### SCAN

- Params
  - None
- Returns
  - meta
    - size: 返回的数据数
    - next: 下一个起始索引。-1 如果没有更多数据
  - results: 返回的数据列表

检索数据的语法按以下格式指定（不区分大小写）,在请求负载的stmt字段中提供。

```
SCAN <RESOURCE_ID> <START> <END>
```

START和END位置包括在内。

示例（不区分大小写）：

-   `SCAN 12cf0a5dee76`扫描所有数据，每个数据块将是默认的页面大小
-   `SCAN 12cf0a5dee76 145`从index 145开始扫描数据到末尾
-   `SCAN 12cf0a5dee76 100 9922`从索引100到索引9922扫描数据

空格处理

用户必须确保字符串之间没有重复的空格。

请求报文示例：

```
{
    "stmt": "SCAN 12cf0a5dee76 5001 10000"
}
```

响应报文示例：

```
{
    "retcode": 0,
    "meta": {
        "size": 1000,
        "next": 6001
    },
    "results": [
        [5001, "method5001", 3.14],
        [5002, "\`method\`5002", 3.141],
        [5003, "\`method\`5003", 3.1415],
        ...
        [6000, "\`method6000\`", 3.1415926...]
    ]
}
```

### DESC,HDESC

HDESC HDESC用于检索resource_id处理程序的架构。

- Returns
  - results: 映射上下文，在创建的资源中查询元数据。

请求报文示例：

```
{
    "stmt": "DESC Pi"
}
```

响应报文示例：

```
{
    "retcode": 0,
    "meta": {},
    "results": {
        "create_stmt": "CREATE TABLE Pi (id BIGINT not null default 0, method STRING not null default 'a', \`\`estimated_pi\`\` DOUBLE not null default 0.00)"
        "name": "Pi",
        "schema": {
            "attr": [
                { "name": "id", "type": "BIGINT" },
                { "name": "method", "type": "STRING" },
                { "name": "estimated_pi", "type": "DOUBLE" }
            ],
        },
        "size": 31415926
    }
}
```

### GC LIST

- Returns

  - meta

    - size: 返回的数据数


  - results: 返回的数据列表


请求报文示例：

```
{
    "stmt": "GC LIST"
}
```

响应报文示例：

```
{
    "retcode": 0,
    "meta": {
        "size": 4
    },
    "results": ["aabbccddeeff0011", "0011223344556677", "6677889900aabbcc", "0123456789abcdef"]
}
```

### GC

从SELECT、FIND和GET分配的资源，在参数字段中设置了句柄，在延长的空闲会话后会受到垃圾收集的影响。虽然上述命令的默认行为将在数据流结束后立即释放，无论成功与否。

### 自动GC定时器

用户可以设置`BO_GC_TIMER`环境变量允许资源空闲的最短时间（以秒为单位）。
