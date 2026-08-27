# WHAT / WHY / HOW Authority Model

本文件定义 V2.9 的最高层职责边界：**内容真值、设计推理、视觉表达必须分层，且权限不可越界。**

核心原则：

> **WHAT is locked. WHY is guided. HOW is free.**

这不是三套互相独立的工作流，而是同一条设计链中的三个 Authority Plane。

---

# 1、三层 Authority Plane

## 1.1 WHAT — Content Truth Plane

负责：

```text
Source Scope
Semantic Obligations
Exact Facts
Source Tables / Required Entries / Required Dimensions
Required Relationships
Business Priority
Declared Conclusions
Contradictions / Unknowns
Render-ready Transformed Content
```

Owner：

```text
md-to-html-report
```

正式载体：

```text
Source Content Inventory
Semantic Transformation Map
Complete Design Input Package
Coverage Evidence Ledger
```

一旦 Complete DIP Lock：

```text
WHAT = IMMUTABLE / READ ONLY
```

任何下游设计阶段都不得：

```text
删掉独立 Semantic Obligation
重新挑选 Top Insight
重新决定 Top 3 / P0 / P1
替换 Source Table Entry
新增或删除业务维度
重写业务结论
把属性提升为新的独立结论
把原有独立项降级成别的分类
```

---

## 1.2 WHY — Design Reasoning Plane

负责解释：

```text
这一组内容的语义关系是什么？
用户看完应该理解什么？
这一段在全篇叙事中承担什么角色？
什么误读风险必须避免？
哪些信息应该形成视觉强调？
```

Owner：

```text
md-to-html-report = Creative Brief Owner
```

正式载体：

```text
workspace/design-intent-package.md
```

Design Intent 只能读取 Locked DIP；它不是新的 Content Engine。

允许：

```text
识别关系类型
定义 Desired Takeaway
定义 Narrative Role
定义 Visual Risk
定义 Visual Emphasis
指出可适合高冲击 / 克制表达的区域
```

禁止：

```text
重写事实
删除 Scope
新增事实
重新定义业务优先级
重新总结出新的 Top N
修改 Source Table 核心信息
把自己的“更好叙事”当成新的业务结论
```

关键规则：

> **Design Intent may change emphasis, never scope.**

> **Design Intent may identify a relationship, never invent a relationship.**

> **Design Intent may recommend hierarchy, never change business priority.**

---

## 1.3 HOW — Visual Expression Plane

负责：

```text
Layout
Composition
Typography
Color
Grid
Spacing
Visual Carrier
Data Visualization
Interactive Behavior
Scrollytelling
Motion / Choreography
Signature Expression
Responsive Expression
```

Owner：

```text
huashu-design
```

Huashu 必须同时读取：

```text
Locked Complete DIP
+ Design Intent Package
+ Selected Design Direction Contract
+ Selected Design System Snapshot
```

Huashu 拥有高自由度，但用户可见业务内容仍只能来自 Locked DIP。

---

# 2、与 V2.7 LOCKED / GUIDED / FREE 的关系

V2.7 的三层权限模型继续有效，但在 V2.9 中增加明确映射：

```text
LOCKED  ≈ WHAT
GUIDED  ≈ WHY
FREE    ≈ HOW
```

注意：

```text
GUIDED != 父 Skill 已经把页面画完
FREE   != 可以自由修改业务内容
```

正确理解：

```text
WHAT 规定“必须表达什么”
WHY 规定“必须被理解成什么关系”
HOW 决定“最终如何漂亮地表达”
```

---

# 3、权限冲突处理

如果 Design Intent 与 DIP 冲突：

```text
DIP 胜出
Design Intent 必须重做
```

如果 Visual Grammar Plan 与 Design Intent 冲突：

```text
Design Intent 胜出
Huashu 改 Visual Grammar，不改 WHY
```

如果 Selected Design System 与 Required Relationship 冲突：

```text
Required Relationship 胜出
允许 Mode Adaptation / Layout Adaptation
禁止修改 WHAT
```

---

# 4、运行时硬检查

在 Prototype 前、Final Generation 前都必须检查：

```text
Design Intent Target Coverage = 100%（允许 DU 继承 Parent / Group Intent）
Design Intent Obligation Refs Coverage = 100%
New Business Fact in Design Intent = 0
Removed Business Obligation by Design Intent = 0
Business Priority Mutation = 0
Required Relationship Mutation = 0
```

如果失败：

```text
DESIGN_INTENT_AUTHORITY_VIOLATION
```

不得继续进入 Huashu。

---

# 5、典型正确例子

Locked DIP：

```text
A = 灵蜥底盘代差优势
B = T1 450km 纯电增程代差
C = 潮奢品质人群心智空位
Required Relationship:
A × B × C → 2026 Q3-Q4 最佳上市时机
```

Design Intent：

```text
Semantic Structure = Multiplicative Convergence
Desired Takeaway = 三个独立条件共同成立，才构成上市窗口判断
Visual Risk = 不得被理解成三个互不相关卖点
Narrative Role = Executive Strategic Proof
Emphasis = HIGH
```

Huashu 可自由选择：

```text
巨大乘法公式
三路径汇聚
三角构图
动态收束
其他原创表达
```

Design Intent 不得写：

```text
必须用 3 张卡片
必须用 radial graph
把 C 删除以保持画面干净
将 B 改成“竞品窗口”更好看
```

---

# 6、最终目标

```text
V2.6 的内容可靠性
+
V2.7 的 Controlled Boldness
+
Design Intent 的语义推理
+
Huashu 的 HOW 自由
```

不是把设计做得更保守，而是让设计自由建立在明确的内容权限之上。
