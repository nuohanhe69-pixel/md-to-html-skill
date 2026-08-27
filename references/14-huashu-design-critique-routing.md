# Huashu Design Critique Routing

本文件定义最终 HTML 生成后，如何让 `huashu-design` 自带专家评审与 `frontend-visual-qa` 分工。

核心原则：

> **Huashu Design Critique 判断“设计好不好、表达是否成立”。**

> **frontend-visual-qa 判断“实现有没有正确跑出来”。**

两者都不是 Content QA，也都没有直接修改权。

---

# 1、为什么需要双 Reviewer

最终产物可能同时存在：

```text
A. 设计问题
- Concept / 立意弱
- 视觉层级不成立
- 信息密度与载体不匹配
- Slide 叙事差
- Motion 只是炫技
- 设计哲学漂移

B. 实现 / 渲染问题
- Overflow
- Clipping
- Overlap
- Broken image / font
- Responsive 错误
- iframe / navigation 错误
- Deck 翻页失效
- 动画结束态异常
```

因此必须分开检查。

---

# 2、Huashu Design Critique 的职责

调用当前安装版本 `huashu-design` 自带 critique / expert review 路由。

父 Skill 不复制评分细则。

至少评审：

```text
Concept / 立意
Design Philosophy Alignment
Visual Hierarchy
Craft Quality
Functionality
Originality
Information Density
Visual Rhythm
Data Storytelling
Motion 是否服务表达
Selected Design Direction Consistency
```

输出至少包含：

```text
Overall Score
Dimension Scores
Keep
Fix
Quick Wins
Priority / Severity
```

---

# 3、Report Mode Critique Profile

使用：

```text
Report / Whitepaper / PDF-oriented profile
```

重点：

```text
细节执行
功能性
视觉层级
专业感
长页面阅读节奏
数据展示是否帮助理解
信息密度是否适合深度阅读
是否出现“漂亮但像模板”的页面
```

---

# 4、Presentation Mode Critique Profile【主设计评审】

使用：

```text
PPT / Keynote-oriented profile
```

重点：

```text
每页是否有清晰视觉入口
每页核心表达是否明确
Visual Hierarchy
Functionality
Slide-to-Slide Rhythm
Narrative Flow
Concept / 视觉母题
设计哲学一致性
Data Storytelling
Motion Language
Temporal Narrative / Motion Choreography
Deck-level Rhythm / Pause / Hold
Motion 是否帮助建立数据 / 流程 / 因果 / 对比关系
是否只是机械 fade / stagger
信息密度是否匹配演示载体
```

即使：

```text
Frontend Render QA = PASS
```

但：

```text
Huashu Design Critique = FAIL
```

也不能交付。

---

# 5、frontend-visual-qa 的职责

在本 Skill 中统一定义为：

```text
Frontend Render QA
```

负责检查：

```text
Typography rendering
Wrapping
Clipping
Overlap
Overflow
Responsive / Projection viewport
Image / Font loading
DOM geometry
Data visualization rendering
Browser-visible defects
Interaction / navigation 是否真的工作
Console
```

它不负责最终判断：

```text
Concept 是否高级
设计哲学是否成立
Slide 叙事是否精彩
视觉母题是否独特
Presentation 是否是一套优秀演示
```

---

# 6、Presentation Mode Render Profile

进入本 Reviewer 前，Presentation 必须先通过 `references/22-presentation-artifact-integrity-contract.md` 的 Artifact Integrity Gate。

重点检查：

```text
presentation/index.html
slides/*
1920×1080 或目标 canvas
scale-to-fit
iframe 加载
Overview
Gallery
Present Mode
← / →
Space
ESC
Page Counter / Jump / Overview 与 Deck Manifest 一致
Stylesheet 实际加载成功
Slide overflow
Slide internal scroll
Font / image loading
Animation final state
Console
```

这一步回答：

> **这套 Deck 有没有正确跑出来？**

---

# 7、Report Mode Render Profile

重点检查：

```text
Desktop / Mobile
Long-page composition
Wrapping
Overflow
Wide table scroll ownership
Images
Charts
Whitespace
Content width
Responsive reflow
Console
```

---

# 8、两个 Reviewer 都只能给建议【硬约束】

Huashu Design Critique：

```text
只输出 Score / Keep / Fix / Quick Wins / 建议
```

frontend-visual-qa：

```text
只输出 Findings / Evidence / 修改建议
```

两者都禁止：

```text
直接改 HTML
直接改 CSS
直接改 JS
重新选择 Design Direction
改变 Complete Design Input Package
```

---

# 9、真正的 Fix Owner

所有修改统一由：

```text
md-to-html-report
```

决定。

```text
Reviewer Finding
↓
本 Skill 复核
↓
Complete Design Input Package
+ Selected Design Direction Contract
+ Huashu Design Method
↓
形成修复方案
↓
修改
↓
完整 Regression QA
```

---

# 10、Regression QA

任何修复后必须重新执行：

```text
Presentation Artifact Integrity QA（如涉及 Presentation）
Content Integrity QA
Huashu Design Critique
Frontend Render QA
Mode-specific QA
Data Visualization & Motion QA
Motion Semantic Safety QA
Motion Choreography Quality QA（适用时）
Design Expressiveness / Controlled Boldness QA
```

---

# 11、V2.7 Design Expressiveness Critique

Huashu Design Critique 还必须读取 Selected Design Expressiveness Profile，并判断：

```text
Design Ambition Consistency
Controlled Boldness Boundary
Structural Variety
Signature Expression Preservation
Report Expressiveness
Presentation Expressiveness
Visual Monotony（是否存在实质问题）
```

特别区分：

```text
Visual Boldness
!=
Structural Boldness
```

例如“超大字号 + 强颜色 + 粗边框”，但所有内容仍连续使用相同 Table / Grid / Card，可以被标记为：

```text
Visual surface bold, structural expression conservative
```

反之，如果用户选的是克制、静态、印刷型方向，不得因为缺少动画而机械扣分。

完整判断边界见 `25-design-expressiveness-and-controlled-boldness.md`。

# 12、V2.9 Lightweight Design Reflection

除正式 Huashu Design Critique 外，可运行轻量设计复盘：

```text
references/33-lightweight-design-reflection-qa.md
```

它只用于识别：

```text
Missed Expression Opportunity
Card Abuse
Default Layout
Signature Weakness
Narrative Rhythm Monotony
Semantic Motion Opportunity
```

默认：

```text
NON-BLOCKING
ADVISORY ONLY
```

如果发现的其实是 Required Relationship 被错误表达，则升级到 Content Integrity Hard Gate。

Reflection Reviewer 不能直接修改 HTML / CSS / JS。
