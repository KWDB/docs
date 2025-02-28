---
title: 时序函数错误码
id: error-code-ts-functions
---

# 时序函数错误码

| 错误码 | 消息 | 错误原因 |
| --- | --- | ---|
| 0A000 | twa function can only be used in time series table  | `TWA` 函数应用于非时序表。|
| 0A000 | elapsed function can only be used in time series table | `ELAPSED` 函数应用于非时序表。|
| 42804 | first parameter should be primary timestamp in twa function   | `TWA` 函数的第一个参数不是时序表的第一列（时间戳列）。|
| 42804 | first parameter should be primary timestamp in elapsed function | `ELAPSED` 函数的第一个参数不是时序表的第一列（时间戳列）。|
| 22023 | duplicate timestamps not allowed in twa function | `TWA` 函数执行过程中遇到时间戳相同的数据。|
| 22023 | invalid time unit in elapsed function | `ELAPSED` 函数的 `time_unit` 参数指定未支持的时间单位。|
