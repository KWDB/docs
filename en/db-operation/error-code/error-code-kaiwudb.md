---
title: KWDB Specific Error Codes
id: error-code-KWDB
---

# KWDB Specific Error Codes

This section lists the specific error codes and corresponding messages for KWDB, categorized by error type. It helps users easily identify the cause of errors and take appropriate actions to resolve them.

## Error Code Format

Error codes are grouped into categories based on their type. The prefix indicates the category, and the numeric part differentiates individual error codes within each category. For example, `KW001-KW013` are connection-related errors, while `KW301-KW310` are system-related errors.

## Connection-related Error Codes (KW001-KW013)

| Error Code | Message                                                            | Suggested Action                                     |
|------------|--------------------------------------------------------------------|------------------------------------------------------|
| KW001      | Connection (%ld) failed: %s                                         | Retry the connection. If the issue persists, contact support. |
| KW002      | Invalid connection id (%ld)                                         | Check the connection ID, then try reconnecting.     |
| KW003      | Invalid request (unknown message type %d)                           | Use a valid message type to create the message.     |
| KW004      | Invalid startup packet layout: expected terminator as last byte    | Use a valid connection terminator to connect to the database. |
| KW005      | Protocol %u.%u is not supported                                     | Change the protocol and retry. If the issue persists, contact support. |
| KW006      | Authentication failed for user %s                                   | Check the username, password, or token information, then retry. |
| KW007      | Insufficient memory (request size: %lu)                             | Check memory usage.                                   |
| KW008      | Create inner connection error. %s                                   | Check connection details, memory, or contact support. |
| KW009      | Failed to send messages (%s)                                        | Contact support.                                     |
| KW010      | Failed to receive messages (%s)                                     | Contact support.                                     |
| KW011      | Unknown type %c, %s                                                 | Contact support.                                     |
| KW012      | Get type [%c], %s                                                   | Contact support.                                     |
| KW013      | Communication failure: %s                                           | Contact support.                                     |

## Resource-related Error Codes (KW101)

| Error Code | Message                             | Suggested Action                                      |
|------------|-------------------------------------|-------------------------------------------------------|
| KW101      | Apply timer thread failed. %s      | Release some threads and retry.                       |

## Data Type-related Error Codes (KW201-KW203)

| Error Code | Message                            | Suggested Action                                      |
|------------|------------------------------------|-------------------------------------------------------|
| KW201      | %s(id: %lu) already exists         | Check the object name and retry.                      |
| KW202      | Object %s(id: %u) does not exist   | Check if the object is correct.                       |
| KW203      | %s is not supported                | No action available.                                  |

## System-related Error Codes (KW301-KW310)

| Error Code | Message                                                             | Suggested Action                                      |
|------------|---------------------------------------------------------------------|-------------------------------------------------------|
| KW301      | Insufficient memory, failed to allocate %lu bytes memory            | Check memory usage, then retry. If the issue persists, contact support. |
| KW302      | Failed to create shared memory segment (%s), reason                 | Check if the shared memory already exists or if the settings are correct. Contact support if needed. |
| KW303      | Insufficient memory (request size: %u) (maybe bigint)               | Check memory usage, then retry. If the issue persists, contact support. |
| KW304      | Failed to release memory (reason: %s, address is %p)                | Retry releasing memory. If the issue persists, contact support. |
| KW305      | Parameter type error(SizeType is %s, SizeClass is %s)               | Check the parameter types.                             |
| KW306      | Memory internal error (sanity check): address %s, stack %s %s      | Contact support.                                       |
| KW307      | Memory internal error (free): address %s, stack %s %s              | Contact support.                                       |
| KW308      | Lost connection to persistent storage engine: ExecuteQuery         | Check the storage container's status and reconnect if needed. |
| KW309      | Lost connection to persistent storage engine: 3306 connect         | Check the storage container's status and reconnect if needed. |
| KW310      | Persistent storage engine returned error: %s                       | Check the storage container.                           |

## Metadata-related Error Codes (KW501-KW513)

| Error Code | Message                                       | Suggested Action                                  |
|------------|-----------------------------------------------|---------------------------------------------------|
| KW501      | Object %s(id: %lu) does not exist              | Check if the parameters used are correct.         |
| KW502      | Object %s(name: %s) does not exist             | Check if the parameters used are correct.         |
| KW503      | Object %s(key: %s) does not exist              | Check if the parameters used are correct.         |
| KW504      | Object %s(id: %lu) is invalid                  | Check the validity of the object.                 |
| KW505      | Object %s(name: %s) is invalid                 | Check the validity of the object.                 |
| KW506      | Object %s(id: %lu) already exists             | Change the object and retry.                      |
| KW507      | Object %s(name: %s) already exists            | Change the object and retry.                      |
| KW508      | User(name: %s) does not have privilege on %s(%u) | Check user privileges.                            |
| KW509      | Failed to create message queue: %s.            | Check the settings and retry.                     |
| KW510      | The size of ConsumeData: %d is incorrect       | Contact support.                                  |
| KW511      | Failed to serialize message(type: %s).         | Contact support.                                  |
| KW512      | Failed to deserialize message(type: %s).       | Contact support.                                  |
| KW513      | Metadata %s (NULL) for object %s is invalid.   | Contact support.                                  |

## Object Validation-related Error Codes (KW601-KW602)

| Error Code | Message                             | Suggested Action                                      |
|------------|-------------------------------------|-------------------------------------------------------|
| KW601      | Metadata(%s) verification failed   | Check metadata and retry. If the issue persists, contact support. |
| KW602      | Parameter(%s) verification error   | Check parameters and retry. If the issue persists, contact support. |

## Permission-related Error Codes (KW701-KW773)

| Error Code | Message                                      | Suggested Action                                      |
|------------|---------------------------------------------|-------------------------------------------------------|
| KW701      | User(name: %s) has no privilege on %s(%u)    | Check user privileges.                                |
| KW773      | Hardware checking failed                    | Check hardware information and retry. If the issue persists, contact support. |

## KWDB Internal Error Codes (KW801-KW813)

| Error Code | Message                                                    | Suggested Action                                    |
|------------|------------------------------------------------------------|-----------------------------------------------------|
| KW801      | Failed to initialize object(%s)                           | Contact support.                                    |
| KW802      | Internal execution error (%s)                             | Contact support.                                    |
| KW803      | Null pointer(%s) is not allowed                           | Contact support.                                    |
| KW804      | MQ (name: %s) failed to send message (message_type: %d)    | Contact support.                                    |
| KW805      | Failed to insert %s(id: %lu) into list/vector/map/...      | Contact support.                                    |
| KW806      | Failed to insert %s(name: %s) into list/vector/map/...     | Contact support.                                    |
| KW807      | The arguments(%s) do not meet the requirements            | Contact support.                                    |
| KW808      | Calling a function(%s) in a wrong way                     | Contact support.                                    |
| KW809      | There is not enough memory space                          | Contact support.                                    |
| KW810      | Null pointer(%s) is not allowed                           | Contact support.                                    |
| KW811      | The parameter(%s) is out of range                         | Contact support.                                    |
| KW812      | Pointer (%s) is a nullptr                                 | Contact support.                                    |
| KW813      | %s is in the wrong state, its status is %s                | Contact support.                                    |

## Unknown Error Codes (KW901-KW917)

| Error Code | Message                                     | Suggested Action                                  |
|------------|---------------------------------------------|---------------------------------------------------|
| KW901      | Unknown type                                 | Contact support.                                  |
| KW912      | All threads are busy! Try again             | Contact support.                                  |
| KW913      | Cannot open cfg file/directory!            | Contact support.                                  |
| KW914      | Cannot find/parse config.                  | Contact support.                                  |
| KW915      | Failed to bind message callback function    | Contact support.                                  |
| KW916      | Failed to init pubsub                       | Contact support.                                  |
| KW917      | Failed to init T                            | Contact support.                                  |