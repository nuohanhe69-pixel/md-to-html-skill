# Visual Grammar Exploration Library

本文件是**视觉表达词汇库**，不是模板库。

原则：

> **Visual Grammar provides options, not prescriptions.**

Huashu 可以使用、组合、变形或完全跳出这些 Grammar，只要：

```text
WHY 被正确表达
WHAT 未被修改
Selected Design Direction 未漂移
```

---

# 1、Grammar Selection Flow

```text
Locked DIP
+
Design Intent
↓
识别 Semantic Structure
↓
浏览候选 Visual Grammar
↓
Huashu 选择 / 组合 / 自创
↓
记录为什么该表达适合当前语义
```

禁止：

```text
看到 3 个项目 → 3 Cards
看到表格 → 原样 Table
看到流程 → 默认 Horizontal Timeline
```

---

# 2、核心 Grammar Families

## 2.1 Multiplicative / Joint Drivers

适合：

```text
A × B × C → Result
多因素共同成立
多条件汇聚
```

候选：

```text
Strategic Equation
Converging Paths
Triangular Composition
Radial Convergence
Layered Build → Final Result
```

避免：

```text
三个孤立 Card 看起来互不相关
```

---

## 2.2 Causal Chain / Progressive Logic

适合：

```text
A → B → C → D
因果推进
阶段变化
```

候选：

```text
Causal Flow
Step Build
Scroll-driven Progression
Storyboard Sequence
Annotated Path
```

---

## 2.3 Comparison / Gap / Advantage

适合：

```text
A vs B
领先 / 落后
代差
```

候选：

```text
Data Duel
Slope / Gap Visualization
Side-by-side Editorial Contrast
Difference Annotation
Range / Threshold Visualization
```

例如：

```text
450km vs 212km
```

优先表达“差距”和“体验含义”，不是只显示两个 Metric Card。

---

## 2.4 Competitive Landscape

适合：

```text
多竞品定位
心智占位
阵营结构
```

候选：

```text
Positioning Map
Landscape Map
Battlefield
2×2 Matrix
Cluster / Camp Map
Ranked Landscape
```

Cards 只有在“每个对象都需要独立阅读”时才优先。

---

## 2.5 Funnel / Decision Journey

适合：

```text
首阅 → 留资 → 试驾 → 锁单
阶段流失
关键 Trigger
```

候选：

```text
Funnel
Decision Journey
Stepwise Conversion Path
Scroll-linked Stage Story
Sankey-like Flow（数据支持时）
```

---

## 2.6 Persona / Human Insight

适合：

```text
人物画像
生活方式
价值冲突
场景决策
```

候选：

```text
Persona Dossier
Day-in-the-life Journey
Identity / Tension Split
Scene-based Story
Decision Lens
Quote-led Editorial Profile
```

避免所有 Persona 永远变成同尺寸 Card Grid。

---

## 2.7 Timeline / Window / Timing

适合：

```text
上市节奏
历史演进
窗口打开 / 关闭
```

候选：

```text
Editorial Timeline
Opportunity Window
Layered Calendar
Temporal Map
Scroll-driven Timeline
```

---

## 2.8 Claim / Evidence

适合：

```text
核心结论 + 多源证据
```

候选：

```text
Claim + Evidence Stack
Evidence Spine
Proof Ladder
Source Network
Annotated Conclusion
```

---

## 2.9 Conflict / Tradeoff

适合：

```text
数据矛盾
优点与短板并存
两种来源冲突
```

候选：

```text
Split Evidence
Tension Diagram
Two-sided Ledger
Conflict Pair
Tradeoff Matrix
```

必须保留双方，不自行裁决。

---

# 3、Grammar Exploration Map

用户选定设计方向后，Huashu 应生成：

```text
workspace/visual-grammar-exploration-map.md
```

建议字段：

```text
Target DU / Cluster
Design Intent Ref
Semantic Structure
Candidate Grammars
Chosen Grammar
Why Chosen
Rejected Alternatives（可选）
Content Risk Check
Selected Direction Fit
```

这个文件属于 HOW Plane。

因此：

```text
Huashu 可以在实现阶段改选 Grammar
```

但必须：

```text
WHY 不变
WHAT 不变
如改选则同步更新 Grammar Map
```

---

# 4、Card Abuse Detection

出现以下情况应主动重新思考：

```text
连续 3 个以上 Section 都主要依赖同构 Card Grid
关系型内容被拆成平级 Card
数据对比只用 Metric Card
Persona 永远使用同一种 Dossier Card
```

Card 本身不是问题，**默认 Card 化**才是问题。

---

# 5、创新边界

Huashu 可以创造本库不存在的新 Grammar。

真正约束只有：

```text
Semantic Safety
Readability
Engineering Safety
Professional Context Fit
Selected Design Direction
```

本库的目的不是“限制 Huashu”，而是防止系统因为缺少设计词汇而自动退回最安全的 Table / Grid / Card。
