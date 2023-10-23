# 错误码

下表列举了KaiwuDB返回错误时的几种错误信息。

> 注：错误代码在HTTP接口中以负数形式返回。

| 编号 | 信息                                             | 描述                   |
| ---- | ------------------------------------------------ | ---------------------- |
| 1    | Operation not permitted                          | 不允许操作             |
| 2    | Object corrupted                                 | 对象损坏               |
| 4    | Out of memory                                    | 内存超限               |
| 5    | Unknown function                                 | 未知功能               |
| 6    | Object exits                                     | 对象退出               |
| 7    | No space left on device                          | 设备上没有剩余空间     |
| 8    | Too many open files                              | 打开的文件太多         |
| 9    | Invalid path                                     | 无效路径               |
| 10   | Operation not permitted on read-only file system | 只读文件系统不允许操作 |
| 11   | No such object                                   | 没有该对象             |
| 12   | Unknown data type                                | 未知数据类型           |
| 14   | Unknown column name                              | 未知列名               |
| 16   | Column name too long                             | 列名太长               |
| 18   | Column name exists                               | 列名存在               |
| 19   | Duplicate column name                            | 重复列名               |
| 22   | Cannot join                                      | 无法加入               |
| 24   | Invalid date time                                | 日期时间无效           |
| 25   | Cannot lock (read) object                        | 无法锁定（读取）对象   |
| 26   | Cannot lock (write) object                       | 无法锁定（写入）对象   |
| 29   | Other errors                                     | 其他错误               |
| 31   | VARCHAR is not allowed                           | 不允许使用VARCHAR      |
| 33   | Invalid argument                                 | 无效参数               |
| 303  | Integer is expected                              | 应为整数               |
| 304  | Data type mismatch                               | 数据类型不匹配         |
| 305  | Syntax error                                     | 语法错误               |
| 310  | Invalid filter                                   | 过滤器无效             |
| 533  | Cannot suspend                                   | 不能暂停               |
| 534  | Cannot resume                                    | 无法恢复               |

