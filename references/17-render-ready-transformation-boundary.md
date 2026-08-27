# Render-ready Transformation Boundary Contract

本文件定义 Content Engineering 与 Huashu Design 之间的硬边界。

核心原则：

> **所有“说什么”的 Transformation 必须在 Huashu 之前完成；Huashu 只决定“怎么展示”。**

---

# 1、Phase 3 不是 Transformation 规划阶段，而是 Transformation 完成阶段

进入 Huashu 前，必须已经完成：

```text
长文本总结
长段落拆点
核心结论提炼
人物维度整理
流程节点重构
关系抽取
数据提取
Source Table 长文本压缩
Source Table 核心字段确认
跨 Cxxx 合并逻辑
Required Relationships 锁定
```

不能只写：

```text
“C037 后面要总结”
“T04 后面做成 Chart”
```

而应该已经形成 render-ready 内容，例如：

```text
C037
Title:
家庭购车决策

Display Content:
- 空间需求
- 安全感知
- 品牌认同
- 长期成本

Required Relationship:
家庭结构 → 使用需求 → 产品偏好 → 最终决策

Immutable Facts:
...

Preferred Visual Form:
Decision Journey / Matrix
```

---

# 2、Complete Design Input Package 的 render-ready 要求

每个需要视觉承接的 Cxxx / Txx 至少应包含：

```text
ID
Semantic Meaning
Transformed Display Content
Immutable Facts
Required Relationships
Semantic Destination
Preferred Visual Form（可为空，但建议提供）
Traceability Source
```

Txx 还必须包含：

```text
Source Table Core Meaning
Required Data Fields
Transformed Table Content / Extracted Data
Allowed Visual Alternatives
Forbidden Omissions
```

---

# 3、Huashu 阶段禁止继续做 Content Transformation

禁止 Huashu：

```text
重新总结 1200 字原文
重新判断哪些 Persona 维度重要
重新抽取表格里的业务字段
重新决定某个结论是否保留
重新压缩用户研究结论
自行删除“看起来不重要”的 Cxxx / Txx
```

允许 Huashu：

```text
把同一份 Transformed Display Content 做成 Card
把同一份结构化关系做成 Timeline
把同一份数据做成 Chart / Table / Matrix
调整 Section Composition
调整信息层级
调整视觉叙事顺序（不破坏 Required Relationships）
```

---

# 4、Source Table 的边界特别说明

最终生成阶段可以做：

```text
Table → Chart
Table → Cards
Table → Matrix
Table → Table + Chart
```

但不能在最终生成阶段才第一次进行：

```text
原表长文本摘要
业务字段提取
关键数字筛选
表格核心信息判断
```

这些必须在 Complete Design Input Package 锁定前完成。

---

# 5、Transformation Lock Gate

只有满足：

```text
Inventory Structural Coverage = 100%
All Cxxx / Txx Semantic Obligations Inventoried = YES
All Cxxx Render-ready = YES
All Txx Render-ready = YES
Source Obligation → DIP Coverage = 100%
Exact Fact Fidelity = 100%
Required Relationship Coverage = 100%
Source Table Entry Coverage = 100%
Source Table Required Dimension Coverage = 100%
Long Content Transformation = PASS
Source Table Transformation Preparation = PASS
Raw Markdown Direct Rendering Risk = ZERO
Complete DIP Data Plane = PRESENT
DIP Content Hash = RECORDED
```

才能：

```text
DESIGN_INPUT_LOCKED
```

否则禁止进入 Prototype 阶段。

# 6、V2.6：Source → DIP Fidelity Gate 先于 LOCK

`All Cxxx Render-ready = YES` 不能只通过“每个 Cxxx 有一个标题 / Destination”判断。

在 `DESIGN_INPUT_LOCKED` 前，必须按 `24-semantic-obligation-and-evidence-contract.md` 证明：

```text
Inventory Structural Coverage = 100%
Source Obligation → Transformation Result Coverage = 100%
Source Obligation → DIP Coverage = 100%
Exact Fact Fidelity = 100%
Required Relationship Coverage = 100%
Source Table Entry Coverage = 100%
Source Table Required Dimension Coverage = 100%
Unresolved Content Mutation = 0
```

只有 PASS 后才能计算 DIP Content Hash 并锁定。

因此：

```text
LOCKED
```

表示：

```text
Content 已经被 Source Evidence 证明无损
+
DIP Data Plane 已真实落盘
+
DIP Hash 已记录
```

而不是一个单独 boolean。
