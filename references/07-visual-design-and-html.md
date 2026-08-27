# HTML Visual Design & Implementation

本文件只负责通用 HTML 视觉实现规则。

进入本阶段前必须已经存在：

```text
Complete Design Input Package
Selected Design Direction Contract
Selected Design System Snapshot
Semantic Content Transformation Map
```

权限边界见 `10-huashu-design-contract.md`。

---

# 1、使用 huashu-design 真正参与设计

它应该参与：

```text
信息层级
布局
Typography
Spacing
Grid
Cards
Table Design
Image Design
Information Density
Visual Rhythm
Responsive
Color System
Content Presentation
Data Visualization
Interaction
Motion
```

---

# 2、HTML 需要有丰富视觉表达

根据实际语义选择：

```text
Hero
Executive Summary
Key Takeaways
Metric Cards
Feature Cards
Source Tables
Generated Tables
Timeline
Process
Architecture
Callout
Insight Card
Quote
Warning
Pros / Cons
Checklist
Image Gallery
Conclusion
```

原则：

```text
Content Determines Component
```

---

# 3、Hero / Header 区域居中设计

报告顶部 Hero / Header 区域必须采用居中布局。

主标题、副标题、元信息、关键标签、摘要信息条优先采用居中组合呈现。

---

# 4、控制 Card 化程度

禁止：

```text
所有内容 → Card
所有列表 → Card
每一句话 → Card
```

必须形成：

```text
正文
+
表格
+
卡片
+
图片
+
图示
+
流程
```

之间的视觉节奏。

---

# 5、图片策略

优先保留 Markdown 中已有图片并优化展示；
如果内容适合视觉化，可以增加流程图、概念图、架构图、示意图、数据图、信息图、SVG、HTML/CSS Diagram。

禁止为了丰富页面虚构：

```text
事实
数字
比例
研究
案例
引用
```

---

# 6、版面与 Typography 基础要求

必须避免：

```text
右侧大面积留白
文字全部纵向堆叠
桌面端只占左侧 50% 内容
几十个 H2 + Paragraph 连续下坠
```

需要利用：

```text
max-width
grid
flex
columns
content width
spacing rhythm
typography hierarchy
```

形成专业报告的阅读节奏。

---

# 7、Report / Presentation 不在此重复定义

双模式规则统一读取：

```text
references/12-display-mode-and-presentation.md
references/19-presentation-main-deck-and-appendix.md
```

通用视觉规则在两种模式中都生效，但模式差异由上述 Owner 决定。

---

# 8、Data Visualization / Interaction / Motion

详细路由规则见：

```text
references/11-huashu-visualization-motion-routing.md
```

---

# 9、V2.7 Controlled Boldness

通用 HTML 视觉实现还必须读取：

```text
references/25-design-expressiveness-and-controlled-boldness.md
```

关键原则：

```text
Content Lock != Visual Conservatism
```

复杂内容不应因为“安全”默认退化成重复的 Table / Grid / Card。是否采用更大胆的构图、数据冲击、非对称、关系图或 Motion，应由 Selected Design Expressiveness Profile + 内容语义决定。

同时，大胆表达不能破坏可读性、响应式、可访问性或 Static Fallback。

# 10、V2.9 Design Reasoning / Carrier / Responsive Rules

进入最终 HTML 实现前必须读取：

```text
references/26-what-why-how-authority-model.md
references/27-design-intent-creative-brief-contract.md
references/28-visual-grammar-exploration-library.md
references/29-signature-moment-and-narrative-rhythm.md
references/30-report-scrollytelling-and-semantic-motion.md
references/32-semantic-carrier-and-responsive-preservation.md
```

实现原则：

```text
Content Determines Meaning
Design Intent Clarifies WHY
Huashu Chooses HOW
```

响应式只允许简化视觉载体，不得 `display:none` 隐藏真实业务语义。

对于重复出现的同一 Obligation，优先使用：

```text
Primary Carrier + Supporting Carrier
```

而不是在多个 Section 重复整段内容。
