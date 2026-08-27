# Core Invariants — 不可改变清单

本文件是 `md-to-html-report` 的最高层不可变量。

任何重构、减肥、术语统一、外部 Skill 更新、QA 修复都不得改变以下语义。

如果其他文件与本文件冲突：

```text
本文件优先
```

---

# CORE-01 Raw Markdown 只是真值源，不是视觉输入

```text
Raw Markdown
= Source of Truth
+ Traceability Source
+ QA 回查来源
```

禁止：

```text
Raw Markdown → Huashu → HTML
Raw Markdown Long Paragraph → Direct Copy into Report
Raw Markdown Long Paragraph → Direct Copy into Slide
```

---

# CORE-02 Semantic Coverage = 100%

原始 Markdown 中每一个具有独立信息价值的语义单元都必须被识别并在最终输出中有有效承接。

---

# CORE-03 Long Content Transformation = 100%

> **保留语义，不保留原始表达形态。**

> **不是完整地搬运 Markdown，而是完整地重构 Markdown。**

---

# CORE-04 Source Table Coverage = 100%

任何 Source Table 都不能未处理就消失；允许改变表达形式，但核心信息必须可追溯。

---

# CORE-05 Content Transformation 必须在 Huashu 之前完成

```text
md-to-html-report
= WHAT TO SAY

huashu-design
= HOW TO SHOW IT
```

Huashu 不负责重新总结 Raw Markdown、重新提取业务数据或重新决定 Coverage 范围。

---

# CORE-06 Complete Design Input Package 是唯一正式业务设计输入

它必须是：

```text
Content Engineering
+
完整 Transformation
+
Cxxx / Txx Mapping
+
Immutable Facts
+
Required Relationships
+
render-ready Transformed Content
```

并且必须真实落盘。

---

# CORE-07 三方向只做 Design Direction Prototypes

```text
Prototype A / B / C
!=
三份完整 Report
```

三份 Prototype 只完整消费同一份 `Direction Comparison Package`，用于比较视觉方向。

---

# CORE-08 用户只做一次选择

用户只参与：

```text
Design Direction / 风格方向选择
```

此后自动生成：

```text
Report Mode
+
Presentation Mode
```

---

# CORE-09 选定方向必须固化为可执行 Design System

用户选择后必须形成：

```text
Selected Design Direction Contract
+
Selected Design System Snapshot
```

最终双模式允许 Mode Adaptation，禁止 Design Direction Drift。

---

# CORE-10 Report 与 Presentation 都必须完整

最终：

```text
Report Semantic Coverage = 100%
Presentation Semantic Coverage = 100%
Report Source Table Coverage = 100%
Presentation Source Table Coverage = 100%
```

---

# CORE-11 Presentation 使用 Main Deck + Appendix 保持“可讲述 + 完整”

```text
Main Deck Coverage
+
Appendix Coverage
=
Presentation Coverage = 100%
```

不能为了缩短 Main Deck 删除语义。

---

# CORE-12 Motion 不能成为唯一语义载体

无动画 / 动画失败时，核心事实仍必须可读。

---

# CORE-13 Reviewer 只发现问题，Fix Owner 永远是父 Skill

```text
Huashu Design Critique
= 设计好不好

frontend-visual-qa
= 实现有没有正确跑出来

md-to-html-report
= 最终 Fix Owner
```

Reviewer 不直接修改 HTML / CSS / JS。

---

# CORE-14 QA 不得通过降低标准来通过

禁止为了 PASS：

```text
删除内容
降低 Coverage
切换 Design Direction
跳过 Render QA
把 Raw Markdown 塞回页面
```

默认最多 3 个完整 Repair Rounds；超出预算仍失败则 `QA_BLOCKED`。

---

# CORE-15 原始输入与旧输出只读、版本化输出

```text
Original Inputs = READ ONLY
Existing Output Version = NO OVERWRITE
```

---

# 初衷示例：为什么需要 Semantic Coverage

例如 Markdown 中可能同时包含：

```text
章节 A
├─ 关键观点 1
├─ 关键观点 2
├─ 表格 1
└─ 结论

章节 B
├─ 人物画像
│  ├─ 消费观
│  ├─ 价值冲突
│  ├─ 决策路径
│  └─ 风险节点
├─ 表格 2
└─ 关键洞察
```

最终不能只保留“最重要的几项”，也不能把全部原文机械复制到 HTML。

---

# CORE-16 Presentation Artifact Build 必须类型安全、Manifest 驱动、Shared Asset 可锁定

Presentation 是多文件运行时产物，必须把“视觉设计”与“文件组装”分开管理。

必须满足：

```text
HTML / CSS / JS / Manifest / Media
分别具有明确 Artifact Type
+
分别走与类型匹配的 Writer
+
一个 Artifact 只有一个 Write Owner
```

禁止：

```text
.css → HTML Wrapper
.js → HTML Wrapper
Manifest → HTML Wrapper
Batch Slide Generation 覆盖 Shared Assets
靠扫描 slides/ 目录猜测应该生成哪些文件
靠写死页数 / 数组位置推导 Deck 状态
```

Presentation 的页数、Main / Appendix 分组、Overview、Jump、导航必须来自同一份 Deck Manifest SSOT。

如果 Artifact Build FAIL：

```text
不得重新做 Content Engineering
不得重新解释 Raw Markdown
不得修改已锁定 Complete Design Input Package
不得因为构建 Bug 改写 Selected Design System
```

只允许回滚到对应的 Presentation Artifact Build 阶段修复，再执行必要 Regression QA。



---

# CORE-17 Presentation Motion 是时间表达层，不是内容层

Presentation 可以使用更强的 Motion / Temporal Storytelling，但动画只能改变：

```text
什么时候出现
以什么顺序出现
如何建立关系
哪里形成强调 / 高潮 / 停顿
```

不能改变：

```text
Cxxx / Txx Content Scope
Immutable Facts
Required Relationships
Semantic Coverage
Source Table Coverage
```

必须满足：

```text
Static Semantic Base 先于 Motion 存在
Motion Traceability = 100%
Motion-only Semantic Unit = 0
Static / Reduced-motion Fallback Coverage = 100%
Motion-induced Information Loss = 0
```

任何关键事实、数字、结论或关系都不能只存在于短暂动画帧、hover、点击或播放中的瞬时状态。

# CORE-18 Semantic Obligation Evidence Lock：ID / Destination / PASS 声明不能替代内容证据

`Cxxx` / `Txx` 只是追踪容器，不是语义完整性的最小审计单位。

必须满足：

```text
Source Structure Baseline
+
Semantic Obligation Set
+
Source → DIP Fidelity Evidence
+
DIP Content Hash Lock
+
DIP → Final Output Evidence
```

硬规则：

```text
Huashu Content Mutation = FORBIDDEN
Manifest-only Complete DIP = FAIL
Destination-only Coverage = FAIL
Comment-only / ID-only Coverage Evidence = INVALID
Exact Fact Fidelity = 100%
Missing / Unproven Semantic Obligation = 0
```

允许高强度总结、合并、重组、图形化；但只能压缩表达，不得压缩独立语义义务。

完整数据模型与证据规则见：

```text
references/24-semantic-obligation-and-evidence-contract.md
```

---

# CORE-19 Content Safety 与 Design Ambition 必须解耦

内容锁定只能约束 `WHAT TO SAY`，不得被解释为视觉保守。

必须满足：

```text
Content Plane
= IMMUTABLE / TRACEABLE / EVIDENCE-BACKED

Design Plane
= CONTROLLED HIGH FREEDOM
```

大胆设计可以改变：

```text
Composition
Scale / Contrast
Asymmetry
Visual Carrier
Data Visualization
Whitespace
Narrative Rhythm
Interaction / Motion
Signature Expression
```

但不能改变：

```text
Semantic Scope
Exact Facts
Required Relationships
Required Entries / Dimensions
Coverage
Readability Bottom Line
Engineering Safety Bottom Line
```

最终表达强度必须忠实于用户选中的 Design Direction；既禁止把 BOLD 方向退化成保守模板，也禁止把克制方向强行做成炫技页面。

完整规则见：

```text
references/25-design-expressiveness-and-controlled-boldness.md
```

# CORE-20 WHAT / WHY / HOW 权限不可混淆

V2.9 采用：

```text
WHAT = Content Truth Plane = LOCKED
WHY  = Design Reasoning Plane = GUIDED
HOW  = Visual Expression Plane = FREE
```

必须满足：

```text
Design Intent may change emphasis, never scope.
Design Intent may identify relationships, never invent relationships.
Design Intent may recommend hierarchy, never change business priority.
Huashu may change expression, never Locked Content.
```

完整定义见：

```text
references/26-what-why-how-authority-model.md
references/27-design-intent-creative-brief-contract.md
```

---

# CORE-21 Source Integrity 必须在 DIP Lock 前检查

Source of Truth 可能内部存在矛盾。

禁止：

```text
静默纠错
自行选择一个“合理值”
通过 Web 自动替换内部 Source
把冲突的一边删除
```

必须登记 `SOURCE_CONFLICT` 并保留双方，规则见：

```text
references/31-source-integrity-gate.md
```

---

# CORE-22 Responsive / Interaction 不得造成语义丢失

响应式、Motion、Interaction 可以简化视觉，不得隐藏业务语义。

```text
Responsive Semantic Loss = 0
Interaction-induced Semantic Loss = 0
Reduced-motion Semantic Loss = 0
```

完整规则见：

```text
references/32-semantic-carrier-and-responsive-preservation.md
```
