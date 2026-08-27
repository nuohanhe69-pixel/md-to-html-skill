# Design Expressiveness & Controlled Boldness Contract

本文件定义：如何在 `Semantic Obligation / Evidence Lock` 已经保证内容安全的前提下，恢复并保护设计胆量，避免把“内容不可变”误执行成“视觉保守”。

核心原则：

> **Content Lock MUST NOT be interpreted as Visual Conservatism.**

> **大胆只能作用于 Expression，不得作用于 Semantic Scope。**

> **目标不是 Maximum Creativity，而是 Controlled Boldness。**

---

# 1、双平面解耦：Content Plane 严格，Design Plane 大胆但有边界

## 1.1 Content Plane【硬性锁定】

```text
Content Scope
Exact Facts
Required Relationships
Required Entries / Dimensions
Conclusions
Qualifiers
Evidence
Semantic Obligations
DIP Content Hash
```

必须保持：

```text
IMMUTABLE
TRACEABLE
EVIDENCE-BACKED
```

Huashu 对上述内容：

```text
Mutation Freedom = ZERO
Omission Freedom = ZERO
Fabrication Freedom = ZERO
```

## 1.2 Design Plane【受控高自由度】

在不破坏 Content Plane 的条件下，Huashu 可以大胆决定：

```text
Visual Composition
Layout Topology
Scale Contrast
Asymmetry
Whitespace Strategy
Data Drama
Typography Hierarchy
Section-to-Section Rhythm
Table / Card / Chart / Matrix / Diagram 选择
Visual Carrier Split / Merge
Image / SVG / CSS Diagram Treatment
Interaction Pattern
Report Motion / Progressive Enhancement
Presentation Motion / Temporal Storytelling
Signature Visual Moments
```

这里的“高自由度”不等于“所有东西都做复杂”，而是允许设计师根据语义主动寻找更强表达，而不是默认回退到最安全的 `Table / Grid / Card`。

---

# 2、Controlled Boldness 的四条边界

任何大胆设计都必须同时满足：

```text
Semantic Safety
+
Readability / Usability
+
Engineering Safety
+
Professional Context Fit
```

## 2.1 Semantic Safety

禁止为了视觉效果：

```text
删掉 Source Entry
改数字 / 比例 / 年龄 / 价格 / 优先级
把定性事实伪装成精确量化
改变 Required Relationship
只保留“最适合可视化”的部分
把关键事实放到 transient-only 状态
```

## 2.2 Readability / Usability

大胆构图不能导致：

```text
核心阅读路径不清
正文长期难读
视觉焦点互相争抢
关键信息需要猜交互才能找到
移动端 / 常见桌面宽度不可用
```

## 2.3 Engineering Safety

Report / Presentation 的 Motion 或 Interaction 必须是 progressive enhancement：

```text
默认 Static Semantic Base 可读
↓
Runtime Ready
↓
再启用 reveal / count-up / build / transition
```

禁止关键内容默认 `opacity: 0` 并依赖 JS 才首次出现。

## 2.4 Professional Context Fit

视觉大胆必须服务：

```text
判断
洞察
证据
关系
决策
讲述
```

禁止无业务表达价值的炫技，例如：

```text
无意义 3D
满屏粒子
游戏化 HUD
过量霓虹
仅为“酷”而存在的鼠标跟随
每个模块都采用不同交互机制
```

---

# 3、Selected Design Expressiveness Profile

用户完成唯一一次风格选择后，`Selected Design System Snapshot` 除 Design Tokens 外，必须从被选 Prototype / 混合方向中提取：

```text
Selected Design Expressiveness Profile
```

至少记录：

```text
Visual Ambition            = RESTRAINED / BALANCED / BOLD
Composition Boldness       = LOW / MEDIUM / HIGH / VERY_HIGH
Visual Contrast            = LOW / MEDIUM / HIGH
Data Drama                 = LOW / MEDIUM / HIGH
Layout Asymmetry           = LOW / MEDIUM / HIGH
Visual Variety             = LOW / MEDIUM / HIGH
Whitespace Strategy        = DENSE / BALANCED / GENEROUS / DRAMATIC
Narrative Rhythm           = CALM / MIXED / HIGH-CONTRAST
Report Interaction Density = NONE / LOW / MEDIUM / HIGH
Report Motion Density      = NONE / LOW / MEDIUM / HIGH
Presentation Motion Density= LOW / MEDIUM / MEDIUM_HIGH / HIGH
Signature Expression DNA   = 具体可执行描述
Restrained Zones           = 哪些内容应保持安静
Must-not-drift             = 不允许退化的设计特征
```

这些值不是统一模板默认值，必须从：

```text
Selected Prototype
+
Design Context
+
内容语义
```

推导。

如果选中的方向本身是静态印刷型，`Report Motion Density = NONE / LOW` 可以成立；如果选中的 Prototype 明确依赖 reveal / data build / interactive comparison 形成设计 DNA，则最终 Report 不得无理由退化为纯静态。

---

# 4、Boldness Budget：不是所有区域都一样大胆

每个最终模式应有一个轻量 `Boldness Budget`，记录不同叙事角色的表达强度。

示例，不是固定模板：

```text
Report
Cover / Strategic Judgment   HIGH
Top Insights                 MEDIUM_HIGH
Deep Analysis                MEDIUM
Persona / Key Data Story     MEDIUM_HIGH
Evidence / Appendix          LOW

Presentation
Cover                        VERY_HIGH
Core Judgment                HIGH
Key Data Story               HIGH
Narrative Bridge             MEDIUM
Appendix                     LOW
```

允许根据用户选择和内容类型调整。

核心原则：

```text
需要高潮的地方敢于高潮
需要阅读的地方保持安静
需要查证的地方优先清晰
```

禁止：

```text
所有 Section 都 PEAK
所有 Section 都 CALM
```

---

# 5、Structural Boldness：防止“风格很凶，但构图很稳”

Visual Boldness 不仅是：

```text
颜色更亮
边框更粗
标题更大
```

还包括：

```text
大胆但清晰的 Composition
不同语义使用不同 Visual Grammar
关键数据使用更强 Scale Contrast
关系型内容真正变成 Relationship / Flow / Matrix
关键结论形成 Signature Moment
长页面形成节奏起伏
```

如果最终页面虽然 Token / 色板符合方向，但大量复杂内容连续退化为：

```text
Table
↓
Grid
↓
Card
↓
Table
```

且语义本来适合更强表达，则属于：

```text
Structural Conservatism Finding
```

这不是要求“每个模块都不同”。重复 Grammar 在同类数据、认知连续性或查证场景中完全允许。

只有当：

```text
重复导致视觉单调
+
Selected Expressiveness Profile 要求更高变化
+
内容语义确实支持替代形式
```

才应被 Design Critique 标记。

---

# 6、Signature Expression Moments

如果 Selected Expressiveness Profile 为：

```text
BOLD
```

或存在高 `Composition Boldness / Data Drama / Narrative Rhythm`，最终 Report / Presentation 应主动保留少量真正有记忆点的 Signature Expression Moments。

可以是：

```text
关键数字对撞
大尺度数据排版
关系图 / 决策流
非对称 Editorial Composition
Timeline Build
Persona Dossier
Cinematic Section Transition
可解释的数据动画
```

不设置机械固定数量；由内容规模与设计方向决定。

禁止把“Signature Moment”理解成：

```text
每页加动画
每个数字 Count-up
每个 Card 飞入
```

---

# 7、Report Visual Expressiveness：从 LOW / OPTIONAL 升级为 ADAPTIVE

Report 是阅读优先，但不等于静态优先。

Report 的实际表达强度必须由：

```text
Selected Design Expressiveness Profile
+
Content Semantics
+
Reading Context
```

共同决定。

允许：

```text
STATIC / PRINT-LIKE
SUBTLE INTERACTION
SCROLL REVEAL
COUNT-UP
BAR BUILD
RELATIONSHIP BUILD
SECTION TRANSITION
```

但都必须遵守 progressive enhancement。

如果选中方向的设计 DNA 明确包含 Report Motion / Interaction，而最终 Report 完全没有实现且没有合理说明：

```text
Report Expressiveness Drift = FAIL
```

如果选中方向本来就是静态 editorial / print：

```text
Report Motion = intentionally restrained
```

是合法结果。

---

# 8、Prototype 必须让用户真实看到“设计胆量”

A / B / C 不应只展示不同：

```text
色板
字体
圆角
阴影
```

还应在同一 Direction Comparison Package 上真实体现各方向的：

```text
Composition Boldness
Data Drama
Visual Variety
Whitespace Strategy
Narrative Rhythm
Motion / Interaction（如适用）
Signature Expression
```

这样用户选择的是完整 Design DNA，而不是“换皮主题”。

---

# 9、Huashu 的正确执行权限

Huashu 仍然是完整 Design / HTML Executor，不应被降级为只给 Layout 建议。

正确：

```text
Locked DIP
↓
Huashu 自由设计 Visual Carrier Topology
↓
HTML / CSS / JS
```

前提：

```text
用户可见 Content 只能来自 Locked DIP
所有 Obligation 仍可追溯
Content Hash 不变
```

Huashu 可以：

```text
一个 DU → 多个视觉载体
多个相关 DU → 一个综合视觉模块
Table → Chart + Detail Table
Long Analysis → Editorial Split Layout
```

只要没有丢失 / 修改 Semantic Obligations。

---

# 10、Design Expressiveness Fidelity Gate

最终 Design Critique 需要额外判断：

```text
Design Ambition Consistency = PASS
Controlled Boldness Boundary = PASS
Structural Variety = PASS / N/A
Signature Expression Preservation = PASS / N/A
Report Expressiveness = PASS / intentionally restrained
Presentation Expressiveness = PASS / intentionally restrained
Visual Monotony = NO material issue
```

其中：

```text
PASS
```

不等于“必须大胆”。

真正判断的是：

> **最终表达强度是否忠实于用户选中的方向，并在内容安全、可读性和工程安全范围内发挥到位。**

如果用户选的是克制方向，强行做高冲击设计同样属于 Drift。

---

# 11、Repair 原则

如果发现：

```text
Content = PASS
Design = 过于保守
```

修复只能发生在 Design Plane：

```text
Composition
Hierarchy
Visual Carrier
Data Visualization
Whitespace
Rhythm
Interaction / Motion
```

不得为了提升设计分数回滚或修改 Locked DIP。

反之，如果发现 Content 问题，应回到 Content / DIP 对应阶段修复，不能让 Huashu“顺手改文案”。

# 12、V2.9 与 WHAT / WHY / HOW 的关系

Controlled Boldness 属于 HOW Plane。

```text
WHAT = 不可变内容
WHY = 设计语义简报
HOW = Controlled High Freedom
```

因此 Boldness Budget 可以控制：

```text
Composition / Scale / Rhythm / Motion / Signature
```

不能控制：

```text
业务 Scope / Top N / P0-P2 / Exact Facts / Required Relationships
```

完整权限模型见：

```text
references/26-what-why-how-authority-model.md
```
