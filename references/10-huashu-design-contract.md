# Huashu Design Contract

本文件只负责一个问题：

> **父 Skill 与 `huashu-design` 的权限边界是什么。**

Prototype、双模式、Motion、Design Critique 的详细规则由各自 SSOT 文件负责。

---

# 1、定位：Huashu 是 Design Engine，不是 Content Engine

`md-to-html-report`：

```text
Source Understanding
Content Engineering
Transformation
Coverage
Facts
Required Relationships
QA Control
Fix Ownership
```

`huashu-design`：

```text
Design Direction Exploration
Visual Design
HTML Design Execution
Data / Visual Expression
Motion / Interaction Expression
```

禁止 Huashu：

```text
重新读取 Raw Markdown 后自行决定哪些内容重要
重新建立 Source Inventory
删除 Cxxx / Txx
重新抽取业务数据
纠正用户数据
修改事实 / 结论
决定 Semantic Coverage 范围
替代父 Skill 的 QA / Fix Owner
```

---

# 2、Huashu 唯一业务内容输入：Locked DIP，只读消费

正式调用 Huashu 时，业务内容只能来自：

```text
Complete Design Input Package
```

而且必须是：

```text
READ ONLY
IMMUTABLE CONTENT DATA PLANE
HASH-LOCKED
```

Huashu 不拥有业务内容修改权。它可以输出 HTML / CSS / Visual Composition，但用户可见业务内容必须来自 Locked DIP，禁止自行重新概括、改写、删减或补写。

如果出现版面密度冲突：

```text
Huashu → CONTENT_DENSITY_CONFLICT
↓
父 Skill 优先拆组件 / 加 Section / 加 Slide / Main+Appendix 路由
```

不得由 Huashu 自行删除业务内容。

其完整定义见：

```text
references/13-complete-design-input-contract.md
references/17-render-ready-transformation-boundary.md
references/24-semantic-obligation-and-evidence-contract.md
```

Raw Markdown 只允许父 Skill 用于 Source of Truth / Traceability / QA 回查。

---

# 3、三层权限模型：WHAT / WHY / HOW 与 LOCKED / GUIDED / FREE

## LOCKED

```text
Cxxx / Txx Content Scope
Immutable Facts
关键数字
关键结论
专业含义
Required Relationships
Source Table 核心信息
Semantic Coverage
Source Table Coverage
Information Fidelity
```

## GUIDED（WHY）

```text
Semantic Destination
Semantic Structure
Desired Takeaway
Narrative Role
Visual Emphasis
Visual Risk
Forbidden Reinterpretation
视觉叙事必须保持的 Required Relationship
```

注意：旧字段 `Preferred Visual Form` 如仍存在，只能作为 `ADVISORY HINT`，不得成为绑定 Huashu 的 Layout Spec。

## FREE（HOW）

```text
Visual Grammar Selection / Invention
内容的视觉分组方式（不得合并掉独立 Semantic Obligation）
Section Composition
Table / Chart / Card / Matrix / Diagram 选择
Layout
Typography
Composition
Grid
Spacing
Color
Surface
Card Language
Table Styling
Visual Rhythm
Information Density
Image Treatment
Section Transition
Micro Interaction
Scrollytelling
Motion Language
Visual Signature
```

HOW 的自由以 WHAT / WHY 不被破坏为边界，而不是以“父 Skill 已经指定组件”为前提。

---

# 4、内容事实与联网边界

Huashu 不得使用外部搜索结果：

```text
补充产品参数
纠正 Source Markdown
新增未提供数据
替换内部研究
修改用户结论
给 Cxxx / Txx 注入外部事实
```

允许：

```text
Web-derived Design Inspiration
```

但：

```text
Web-derived Design Inspiration
!=
Content Source
```

---

# 5、Prototype 权限路由

三方向阶段 Huashu 必须遵守：

```text
references/15-direction-prototype-contract.md
```

本文件不维护第二份 Prototype Coverage / Human Gate 规则。

---

# 6、用户选定方向后的设计输入

最终双模式设计输入为：

```text
Complete Design Input Package
+
Selected Design Direction Contract
+
Selected Design System Snapshot
```

Snapshot 的规范正文见：

```text
references/18-selected-design-system-snapshot.md
```

---

# 7、Visualization / Motion 权限路由

通用 Visual Mode 路由见：

```text
references/11-huashu-visualization-motion-routing.md
```

Presentation 的 Temporal Storytelling / Motion Choreography 见：

```text
references/23-presentation-motion-choreography.md
```

当 Presentation 存在适合动态叙事的内容时，Huashu 必须读取其当前安装版本实际存在且与本任务相关的 animation / motion / slide references 与 demos，学习当前 Motion Grammar；不得只凭父 Skill 的摘要自行发明一套简化动画。

Huashu 可以充分发挥表达形式，但 Motion 不能隐藏核心信息或改变事实。

---

# 8、双模式路由

Report / Presentation 的完整规则见：

```text
references/12-display-mode-and-presentation.md
references/19-presentation-main-deck-and-appendix.md
```

本文件不维护第二份双模式 Coverage 规则。

---

# 9、Huashu 的第二角色：Design Critique Reviewer

最终生成后，Huashu 可以切换到 Critique / Expert Review 角色。

此时：

```text
Design Engine
!=
Design Critique Reviewer
```

详细评分与权限见：

```text
references/14-huashu-design-critique-routing.md
```

Critique Reviewer 不能自动应用自己的修复建议。

---

# 10、不复制外部 Skill 内部实现

父 Skill 只维护：

```text
路由
权限
输入输出契约
QA / Fix 编排
```

不复制 Huashu 或 frontend-visual-qa 的内部 scripts / references 形成长期分叉。

# 11、Locked Content Injection

最终组件推荐携带：

```html
data-du-id="DU036"
data-obligation-refs="C036.F01 C036.S01 C036.R02"
```

这些 Traceability Hook 用于父 Skill 回查。

Huashu 可以决定：

```text
DU036 → Persona Card / Split Layout / Tabs / Slide
```

但不能把：

```text
DU036.display_content
```

重新生成成另一份业务文案。

如果确需改变业务表达，必须由父 Skill 回滚 Content Transformation，生成新的 DIP 版本并重新通过 Source → DIP Fidelity Gate；不能在 Huashu 阶段偷偷修改。

---

# 12、V2.7：Content Mutation = ZERO，不等于 Design Freedom = LOW

Huashu 必须同时理解两条规则：

```text
业务内容修改权 = ZERO
设计重构自由度 = CONTROLLED HIGH
```

`Locked DIP` 只锁定业务内容，不锁定 Visual Composition。

Huashu 仍然可以完整执行：

```text
大胆构图
非对称布局
大尺度 Typography
高对比 Data Storytelling
Visual Carrier Split / Merge
Chart / Matrix / Diagram / Timeline 重构
Interaction
Motion
Signature Visual Moment
```

前提是：

```text
Semantic Obligations 不变
Exact Facts 不变
Required Relationships 不变
Traceability 保持
DIP Hash 不变
```

禁止把“只读消费 Locked DIP”误执行成：

```text
只会套 Card / Grid / Table
只给 Layout 建议而不真正做 HTML Design
为了避免风险自动降低用户已选择方向的设计胆量
```

完整边界见：

```text
references/25-design-expressiveness-and-controlled-boldness.md
```

# 11、V2.9 WHAT / WHY / HOW【硬边界】

完整权限模型见：

```text
references/26-what-why-how-authority-model.md
```

映射：

```text
WHAT = LOCKED
WHY  = GUIDED
HOW  = FREE
```

Final Generation 时 Huashu 的正式输入扩展为：

```text
Locked Complete Design Input Package
+
Design Intent Package（WHY，只读）
+
Selected Design Direction Contract
+
Selected Design System Snapshot
```

Huashu 负责 HOW，可以自由选择 / 自创 Visual Grammar，并可采用 Scrollytelling / Semantic Motion。

Huashu 不得把 Creative Brief 解释成新的 Content Scope，也不得把 Visual Emphasis 解释成业务 P0 / P1 / P2。

Visual Grammar / Signature / Report Scrollytelling 分别见：

```text
references/28-visual-grammar-exploration-library.md
references/29-signature-moment-and-narrative-rhythm.md
references/30-report-scrollytelling-and-semantic-motion.md
```
