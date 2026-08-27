# Direction Prototype Contract

本文件专门定义三方向阶段的职责，避免把“三方向设计”错误执行成“三份完整报告”。

---

# 1、三方向阶段的唯一目的

三方向阶段只负责：

```text
Design Direction Exploration
```

也就是让用户真实比较：

```text
A / B / C
```

三种设计语言。

它不是最终内容生产阶段。

---

# 2、Direction Comparison Package

必须先从：

```text
Complete Design Input Package
```

中抽取一份：

```text
Direction Comparison Package
```

该比较包要尽可能暴露最终设计真正会遇到的难点。

推荐包含：

```text
Cover / Hero
一个高数据密度模块
一个复杂分析模块
一个 Source Table / Data Visualization 模块
一个 Motion / Interaction 示例模块（如果适合）
```

如果文档结构特殊，可以换成更有代表性的组合。

硬约束：

```text
Prototype A Input
=
Prototype B Input
=
Prototype C Input
```

---

# 3、Prototype 的产物

输出：

```text
prototype-a.html
prototype-b.html
prototype-c.html
```

它们必须是真实可运行的 HTML，而不是纯文字风格说明。

但它们只是：

```text
Design Prototypes
```

不是：

```text
完整 Report
完整 Presentation
最终交付
```

---

# 4、Prototype Coverage

三个 Prototype 必须分别满足：

```text
Direction Comparison Package Coverage = 100%
```

同时确认：

```text
Facts Same = YES
Required Relationships Same = YES
Comparison Content Scope Same = YES
```

禁止要求：

```text
Complete Design Input Package Coverage = 100%
完整 Cxxx Coverage = 100%
完整 Txx Coverage = 100%
```

否则等价于提前把完整报告做三遍。

---

# 5、Prototype 的设计自由度

允许变化：

```text
Layout
Typography
Color
Composition
Data Visualization
Information Density
Visual Rhythm
Interaction
Motion Language
Table / Card / Chart / Matrix 的视觉组织
```

禁止变化：

```text
Comparison Package 内容范围
事实
数字
结论
Required Relationships
```

---

# 6、用户选择后发生什么

用户完成唯一一次：

```text
Design Direction / 风格选择
```

后，形成：

```text
Selected Design Direction Contract
```

然后：

```text
回到完整 Complete Design Input Package
+
Selected Design Direction Contract
↓
首次生成完整 Report Mode
+
首次生成完整 Presentation Mode
```

注意：

```text
Prototype 不直接升级为完整 Report
Prototype 也不承担最终 Coverage
```

Prototype 的设计 DNA 会被继承，但最终内容范围来自完整 Complete Design Input Package。

---

# 7、为什么不能直接复用 Prototype 当完整 Report

Prototype 只覆盖 Direction Comparison Package。

因此：

```text
Prototype B 被选中
```

表示：

```text
选择 B 的 Design DNA
```

不表示：

```text
Prototype B 已经是完整报告
```

最终 Report 必须重新基于：

```text
完整 Complete Design Input Package
```

构建完整内容，但继承 B 的：

```text
Layout DNA
Typography DNA
Color / Surface DNA
Visualization DNA
Motion DNA
Information Density DNA
Visual Rhythm
```

---

# 8、QA 边界

Prototype 阶段 QA：

```text
Comparison Package Coverage
Facts Same
Relationships Same
Prototype 可真实渲染
三个方向具有可辨识设计差异
```

最终阶段 QA：

```text
Report Semantic Coverage = 100%
Presentation Semantic Coverage = 100%
Report Source Table Coverage = 100%
Presentation Source Table Coverage = 100%
Transformation QA = PASS
Information Fidelity = 高
```

两种 QA 不能混用。

# 9、V2.6：Comparison Package 只能抽取 Locked DIP

Direction Comparison Package 必须保存 / 引用：

```text
DU IDs
Semantic Obligation Refs
Locked Display Content
```

禁止 Prototype 阶段重新读取 Raw Markdown 或自行重写业务内容。

以下属于硬 FAIL：

```text
35岁 → 32岁
P0/P0/P1 → P0/P1/P2
原阶段名被改写为新的业务阶段并改变含义
新增 DIP 中不存在的事实 / 结论
```

Prototype A / B / C 只允许 Design DNA 不同；Locked Content 必须一致。

---

# 10、V2.7：Prototype 必须比较“完整 Design DNA”，不是只比较主题皮肤

三个方向除 Typography / Color / Surface 外，还必须真实暴露各自的：

```text
Composition Boldness
Data Drama
Layout Asymmetry
Visual Variety
Whitespace Strategy
Narrative Rhythm
Report Motion / Interaction（如适用）
Signature Expression
```

用户选择后，这些特征要进入 `Selected Design Expressiveness Profile`，不能只提取色板 / 字体 / 圆角。

如果一个 Prototype 声称是 BOLD / Experimental / Editorial，但代表模块仍全部采用相同 Grid / Table / Card，无法让用户真实判断设计胆量，则：

```text
Prototype Design Differentiation = FAIL
```

但不要求为了差异而强行使用不适合内容的交互或动画。

完整规则见：

```text
references/25-design-expressiveness-and-controlled-boldness.md
```

# 11、V2.9 Prototype 必须共享同一 WHY

Prototype A / B / C 除共享相同 Direction Comparison Package 外，还必须共享相同的：

```text
Design Intent Subset
```

因此：

```text
WHAT Same = YES
WHY Same = YES
HOW Different = YES
```

Prototype 之间允许在：

```text
Visual Grammar
Composition
Typography
Data Drama
Motion
Signature Expression
```

上大胆不同，但不得因为方向不同而重写 Design Intent 或业务优先级。

完整 Intent 规则见：

```text
references/27-design-intent-creative-brief-contract.md
```
