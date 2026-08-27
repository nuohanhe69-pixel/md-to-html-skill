# Source Integrity Gate

本文件解决一个容易被忽略的问题：

> **Source of Truth 也可能内部自相矛盾。**

“忠实于 Source”不等于“无条件把矛盾锁成事实”。

---

# 1、Gate 时机

在 Complete DIP Lock 前必须执行：

```text
Source Inventory Complete
↓
Source Integrity Scan
↓
Conflict / Unknown Registration
↓
Transformation
↓
Source → DIP Fidelity Gate
↓
DIP Lock
```

---

# 2、必须扫描的冲突

至少包括：

```text
数字与排名冲突
同一指标多种数值
正文结论与表格数据冲突
两个 Source 对同一事实给出不同值
百分比合计异常
时间 / 版本口径冲突
单位 / 量纲冲突
“第1 / 领先”等定性描述与数值不一致
```

---

# 3、处理原则

发现冲突时禁止：

```text
模型自行选一个“看起来合理”的值
联网替换内部 Source
静默修正
为了设计简洁只保留一边
```

必须：

```text
登记 SOURCE_CONFLICT
保留冲突双方
记录 Source Refs
标记是否可由源文件上下文解释
无法解释则进入待确认 / 矛盾清单
```

---

# 4、例子：排名与数值冲突

Source Table：

```text
LS6 驾驶感受 = 4.75（第1）
极氪7X 驾驶感受 = 4.80
```

同时正文写：

```text
LS6 驾驶感受绝对领先
```

正确：

```text
SOURCE_CONFLICT:
Numeric ranking contradicts declared rank/claim.

Preserve:
- 4.75 / “第1”
- 4.80 competitor value
- “绝对领先” source claim

Do not silently resolve.
```

最终 DIP 可展示：

```text
“源资料存在排名口径冲突，需确认。”
```

而不是继续把“4.75绝对领先”锁成无争议事实。

---

# 5、Conflict 也是 Semantic Obligation

一旦冲突被识别，它本身形成不可无声删除的义务：

```text
Cxxx.CONFLICT01
```

后续 Design Intent / Huashu 必须把它视为 WHAT 的一部分。

---

# 6、Gate 状态

```text
SOURCE_INTEGRITY_PASS
SOURCE_INTEGRITY_PASS_WITH_CONFLICTS
SOURCE_INTEGRITY_BLOCKED
```

存在已登记冲突并不一定阻止任务继续。

阻止条件包括：

```text
关键事实无法确定且用户任务必须依赖唯一值
关键数据严重破损
Source 结构不足以建立稳定 DIP
```

---

# 7、禁止把 Web 当自动纠错器

除非用户明确要求外部验证：

```text
Web Search != Source Correction Layer
```

内部 / 未发布资料以用户材料为准；冲突应报告，不自动替换。
