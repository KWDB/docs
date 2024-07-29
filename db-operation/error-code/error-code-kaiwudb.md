---
title: KWDB 专有错误码
id: error-code-kaiwudb
---

# KWDB 专有错误码

本文介绍常见的 KWDB 专有错误码和错误消息，并按照错误类型对错误码进行了分类，便于用户更好地查找错误码和定位原因。

## 连接相关错误码（KW001-KW013）

| 错误码 | 消息                                                            | 错误原因                    | 建议措施                                           |
| ------ | --------------------------------------------------------------- | --------------------------- | -------------------------------------------------- |
| KW001  | Connection (%ld) failed: %s                                     | 连接失败                    | 重试连接。如果问题依然存在，联系售后支持人员       |
| KW002  | Invalid connection id (%ld)                                     | 连接 ID 无效                | 检查连接 ID， 然后尝试重新连接                     |
| KW003  | Invalid request (unknown message type %d)                       | 消息类型不支持              | 使用合法的消息类型创建消息                         |
| KW004  | Invalid startup packet layout: expected terminator as last byte | 无效的连接终端              | 使用合法的终端连接数据库                           |
| KW005  | Protocol %u.%u is not supported                                 | 协议不支持                  | 更换协议后重试。如果问题依然存在，联系售后支持人员 |
| KW006  | Authentication failed for user %s                               | 用户名、密码或令牌不匹配 | 检查用户名、密码或者令牌信息，然后重试          |
| KW007  | Insufficient memory (request size: %lu)                         | 内存不足                    | 检查内存使用情况                                   |
| KW008  | Create inner connection error. %s                               | 数据库连接创建错误          | 检查连接信息、内存，或者联系售后支持人员           |
| KW009  | Failed to send messages (%s)                                    | 发送消息失败                | 联系售后支持人员                                   |
| KW010  | Failed to receive messages (%s)                                 | 接收消息失败                | 联系售后支持人员                                   |
| KW011  | Unknown type %c, %s                                             | 接收到的数据不匹配          | 联系售后支持人员                                   |
| KW012  | Get type [%c], %s                                               | 没有相应的模块              | 联系售后支持人员                                   |
| KW013  | Communication failure: %s                                       | 内部连接错误                | 联系售后支持人员                                   |

## 资源相关错误码（KW101）

| 错误码 | 消息                          | 错误原因 | 建议措施 |
| ------ | ----------------------------- | :-------------------------------------- | --------------------------------------- |
| KW101  | Apply timer thread failed. %s | 申请 timer 线程失败                     | 释放一些线程，然后重试                  |

## 数据类型相关错误码（KW201-KW203）

| 错误码 | 消息                             | 错误原因 | 建议措施 |
| ------ | -------------------------------- | --------------------------------------- | --------------------------------------- |
| KW201  | %s(id: %lu) already exists       | 对象已经存在                            | 检查对象名，然后重试                    |
| KW202  | Object %s(id: %u) does not exist | 对象不存在                              | 检查执行对象是否正确                    |
| KW203  | %s is not supported              | 功能不支持                              | 无                                      |

## 系统相关错误码（KW301-KW310）

| 错误码 | 消息                                                          | 错误原因                             | 建议措施                                                                             |
| ------ | ------------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------ |
| KW301  | Insufficient memory, failed to allocate %lu bytes memory      | 内存不足，分配内存失败               | 检查内存使用情况，然后重试。如果问题依然存在，联系售后支持人员                       |
| KW302  | Failed to create shared memory segment (%s), reason           | 创建共享内存失败                     | 检查要创建的共享内存是否已经存在或者设置是否正确。如果问题依然存在，联系售后支持人员 |
| KW303  | Insufficient memory (request size: %u) (maybe bigint)         | 内存不足                             | 检查内存使用情况，然后重试。如果问题依然存在，联系售后支持人员                       |
| KW304  | Failed to release memory (reason: %s, address is %p)          | 释放内存失败                         | 重新尝试释放内存。如果问题依然存在，联系售后支持人员                                 |
| KW305  | Parameter type error(SizeType is %s, SizeClass is %s)         | 参数类型错误                         | 检查参数的类型                                                                       |
| KW306  | Memory internal error (sanity check): address %s, stack %s %s | 内存越界                             | 联系售后支持人员                                                                     |
| KW307  | Memory internal error (free): address %s, stack %s %s         | 同一块内存释放两次                   | 联系售后支持人员                                                                     |
| KW308  | Lost connection to persistent storage engine: ExecuteQuery    | 容器停止或者重启导致连接存储引擎失败 | 检查存储容器状态，状态正常后尝试重连                                                 |
| KW309  | Lost connection to persistent storage engine: 3306 connect    | 连接存储引擎失败                     | 检查存储容器状态，状态正常后尝试重连                                                 |
| KW310  | Persistent storage engine return error: %s                    | 存储引擎报错                         | 检查存储容器                                                                         |

## 元数据相关错误码（KW501-KW513）

| 错误码 | 消息                                             | 错误原因             | 建议措施                   |
| ------ | ------------------------------------------------ | -------------------- | -------------------------- |
| KW501  | Object %s(id: %lu) does not exist                | 查找对象不存在       | 检查查找使用的参数是否正确 |
| KW502  | Object %s(name: %s) does not exist               | 查找对象不存在       | 检查查找使用的参数是否正确 |
| KW503  | Object %s(key: %s) does not exist                | 查找对象不存在       | 检查查找使用的参数是否正确 |
| KW504  | Object %s(id: %lu) is invalid                    | 对象无效             | 检查对象的有效性           |
| KW505  | Object %s(name: %s) is invalid                   | 对象无效             | 检查对象的有效性           |
| KW506  | Object %s(id: %lu) already exist                 | 要创建的对象已经存在 | 更换对象，然后重试         |
| KW507  | Object %s(name: %s) already exist                | 要创建的对象已经存在 | 更换对象，然后重试         |
| KW508  | User(name: %s) does not have privilege on %s(%u) | 权限不足             | 检查用户权限               |
| KW509  | Failed to create message queue: %s.              | 创建消息队列失败     | 检查设置，然后重试         |
| KW510  | The size of ConsumeData: %d is incorrect         | 数据大小不正确       | 联系售后支持人员           |
| KW511  | Failed to serialize message(type: %s).           | 序列化消息失败       | 联系售后支持人员           |
| KW512  | Failed to deserialize message(type: %s).         | 反序列化消息失败     | 联系售后支持人员           |
| KW513  | Metadata %s (NULL) for object %s is invalid.     | 元数据无效           | 联系售后支持人员           |

## 对象校验相关错误码（KW601-KW602）

| 错误码 | 消息                             | 错误原因       | 建议措施                                             |
| ------ | -------------------------------- | -------------- | ---------------------------------------------------- |
| KW601  | Metadata(%s) verification failed | 元数据校验失败 | 检查元数据后重试。如果问题依然存在，联系售后支持人员 |
| KW602  | Parameter(%s) verification error | 参数校验失败   | 检查参数后重试。如果问题依然存在，联系售后支持人员   |

## 权限相关错误码（KW701-KW773）

| 错误码 | 消息                                      | 错误原因     | 建议措施                                               |
| ------ | ----------------------------------------- | ------------ | ------------------------------------------------------ |
| KW701  | User(name: %s) has no privilege on %s(%u) | 用户无权限   | 检查用户权限                                           |
| KW773  | Hardware checking failed                  | 硬件检查失败 | 查看硬件信息后重试。如果问题依然存在，联系售后支持人员 |

## KWDB 内部错误码（KW801-KW813）

| 错误码 | 消息                                                    | 错误原因             | 建议措施         |
| ------ | ------------------------------------------------------- | -------------------- | ---------------- |
| KW801  | Failed to initialize object(%s)                         | 初始化对象失败       | 联系售后支持人员 |
| KW802  | Internal execution error (%s)                           | 内部执行错误         | 联系售后支持人员 |
| KW803  | Null pointer(%s) is not allowed                         | 内部空指针错误       | 联系售后支持人员 |
| KW804  | MQ (name: %s) failed to send message (message_type: %d) | 发送消息队列失败     | 联系售后支持人员 |
| KW805  | Failed to insert %s(id: %lu) into list/vector/map/...   | 插入数据失败         | 联系售后支持人员 |
| KW806  | Failed to insert %s(name: %s) into list/vector/map/...  | 插入数据失败         | 联系售后支持人员 |
| KW807  | The arguments(%s) do not meet the requirements          | 传入的参数不符合要求 | 联系售后支持人员 |
| KW808  | Calling a function(%s) in a wrong way                   | 功能调用逻辑错误     | 联系售后支持人员 |
| KW809  | There is not enough memory space                        | 内存空间不足         | 联系售后支持人员 |
| KW810  | Null pointer(%s) is not allowed                         | 不支持空指针         | 联系售后支持人员 |
| KW811  | The parameter(%s) is out of range                       | 参数超出范围         | 联系售后支持人员 |
| KW812  | Pointer (%s) is a nullptr                               | 空指针               | 联系售后支持人员 |
| KW813  | %s is in the wrong state, its status is %s              | 状态错误             | 联系售后支持人员 |

## 未知错误（KW901-KW917）

| 错误码 | 消息                                     | 错误原因                       | 建议措施         |
| ------ | ---------------------------------------- | ------------------------------ | ---------------- |
| KW901  | Unknown type                             | 未知类型                       | 联系售后支持人员 |
| KW912  | All threads are busy!try again           | 所有线程均是忙碌状态           | 联系售后支持人员 |
| KW913  | Can not open cfg file/directory!         | 无法读取配置文件或者目录       | 联系售后支持人员 |
| KW914  | Can not find/parse config.               | 无法解析配置文件               | 联系售后支持人员 |
| KW915  | Failed to bind message callback function | 绑定消息回调函数失败           | 联系售后支持人员 |
| KW916  | Failed to init pubsub                    | 初始订阅、发布功能失败         | 联系售后支持人员 |
| KW917  | Failed to init T                         | 初始化失败，无法获取缓存管理器 | 联系售后支持人员 |
