# Selected Design System Snapshot Contract

本文件解决“用户选中了 Prototype B，但最终 Report / Presentation 重新生成后风格漂移”的问题。

核心原则：

> **Selected Design Direction Contract 负责记录用户选择；Selected Design System Snapshot 负责把该选择变成可执行设计系统。**

---

# 1、生成时机

用户完成唯一一次 Design Direction 选择后：

```text
Selected Design Direction Contract
↓
从被选 Prototype / 混合方向中提取真实 Design DNA
↓
Selected Design System Snapshot
↓
最终 Report + Presentation
```

禁止只用一句：

```text
“采用 B 的高级数据感风格”
```

去重新猜最终设计。

---

# 2、Snapshot 至少包含

```text
Design Concept / Visual Motif
Typography Scale / Hierarchy
Font Strategy
Color Tokens
Surface Tokens
Border / Radius / Shadow Language
Spacing Scale
Grid / Content Width / Gutter
Card Grammar
Table Grammar
Chart Grammar
Image Treatment
Section Transition Grammar
Information Density Rules
Motion Duration / Easing / Stagger / Reveal Grammar
Temporal Storytelling Grammar
Motion Intensity / Pause / Hold Language
Stage / Camera / Transition Grammar（如果选中方向包含）
Signature Motion Pattern（如果选中方向包含）
Responsive / Projection Behavior
Must-preserve Signature Elements
Must-not-drift Rules
```

可以记录具体数值，也可以记录设计 Token；重点是“可执行”，不能只写抽象形容词。

---

# 3、Report 与 Presentation 的关系

两种模式可以根据载体重新组织：

```text
Report：连续阅读 / 高密度 / 长页面
Presentation：逐页讲述 / 更强节奏 / Main Deck + Appendix
```

但必须共享同一个：

```text
Selected Design System Snapshot
```

允许 Mode Adaptation，禁止 Design Direction Drift。

例如：

```text
同一 Typography DNA
→ Report 使用更适合长读的字号组合
→ Presentation 使用更适合投影的字号组合
```

这属于：

```text
Mode Adaptation
```

不是换风格。

---

# 4、最终 QA 必须检查 Snapshot Consistency

至少检查：

```text
Report vs Snapshot = CONSISTENT
Presentation vs Snapshot = CONSISTENT
Report vs Presentation Design DNA = CONSISTENT
```

如果视觉好看但偏离用户选中的 Prototype：

```text
Selected Design System Consistency QA = FAIL
```

---

# 5、V2.7：Snapshot 必须包含 Selected Design Expressiveness Profile

仅保存 Token 不足以保护用户选中的“设计胆量”。

Snapshot 新增必填子区：

```text
Selected Design Expressiveness Profile
```

至少记录：

```text
Visual Ambition
Composition Boldness
Visual Contrast
Data Drama
Layout Asymmetry
Visual Variety
Whitespace Strategy
Narrative Rhythm
Report Interaction Density
Report Motion Density
Presentation Motion Density
Signature Expression DNA
Restrained Zones
Must-not-drift Expressiveness Rules
Boldness Budget
```

这些值从用户选中的 Prototype / 混合方向提取，不使用全局固定默认。

最终 Consistency QA 不再只检查“颜色 / 字体像不像”，还必须检查：

```text
Design Ambition 是否漂移
Structural Boldness 是否被无理由削弱
Signature Expression 是否被保留
Report / Presentation 是否完成合理 Mode Adaptation
```

完整数据模型见 `25-design-expressiveness-and-controlled-boldness.md`。

# 6、V2.9 Design Reasoning → HOW Planning

Selected Direction Lock 后，Huashu 需要基于同一 Design Intent Package 形成：

```text
workspace/visual-grammar-exploration-map.md
workspace/signature-moment-plan.md
workspace/narrative-rhythm-map.md
```

这些文件属于 HOW Plane：

```text
可修改视觉选择
不可修改 Locked DIP / Design Intent 的语义约束
```

Snapshot 还应声明：

```text
Signature Expression Language
Narrative Rhythm Preference
Report Scrollytelling Suitability
Semantic Motion Style
```

但不得强制每个 Section 使用某一种组件或动画。
