---
title: Trigger Error Codes
id: error-code-trigger
---

# Trigger Error Codes

This section lists the error codes related to triggers.

| Error Code | Message | Suggested Action |
| --- | --- | ---|
| 0A000 | Not all nodes are at the correct version to use Triggers | Not all nodes are upgraded to the version that supports the triggers. |
| 42P17 | Object %s cannot be bound to a trigger | Do not support creating triggers on replicated tables, views, sequences, temporary tables, or time-series tables.|
| 42P17 | Trigger %s already exists on table %s | A trigger of the same name has already created on the target table. |
| 42601 | empty trigger name | No trigger name is specified when renaming a trigger. |
| 42704 | trigger \"%s\" does not exist | Fail to parse the target trigger. |
| 3D000 | unsupported table type: %s in trigger | The table associated with the trigger is not an ordinary relational table. |
| 42P13 | cannot use OLD in INSERT event trigger | The `INSERT` trigger does not support the `OLD` alias. |
| 42P13 | cannot use NEW in DELETE event trigger | The `DELETE` trigger does not support the `NEW` alias. |
| 0A000 | INSERT ... ON CONFLICT is not supported in trigger definition | The trigger body does not support the `INSERT ... ON CONFLICT` statement. |
| 42P13 | Can't update table %s in trigger because it is already used by statement which invoked this trigger. | Do not support operating on tables that are associated with the trigger in the trigger body. |
| 42704 | trigger \"%s\" on table \"%s\" does not exist | The target trigger does not exist when renaming the trigger. |
| 42P17 | trigger \"%s\" already exists on table \"%s\" | A trigger of the same name has already existed when renaming the trigger. |
| 42P17 | referenced trigger "trig1" for the given action time and event type does not exist | The event and time to create a trigger do not match with those to reference (`FOLLOWS` or `PRECEDES`) the trigger. |
| 09000 | TriggeredActionException: errMsg | An error occurs when performing the trigger body. |
