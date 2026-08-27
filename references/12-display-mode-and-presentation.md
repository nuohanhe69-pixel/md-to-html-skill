# Dual Display Mode Contract

本文件定义：

```text
Report Mode
+
Presentation Mode
```

用户只做一次 Design Direction 选择；之后系统自动生成两种模式。

---

# 1、共同输入与共同硬约束

双模式都基于：

```text
Complete Design Input Package
+
Selected Design Direction Contract
+
Selected Design System Snapshot
```

二者都必须 individually 满足：

```text
Semantic Coverage = 100%
Source Table Coverage = 100%
Information Fidelity = 高
Long Content Transformation = PASS
Selected Design System Consistency = PASS
```

模式变化只能改变表达方式，不能改变语义范围。

---

# 2、Report Mode

推荐输出：

```text
report.html
```

适用：

```text
阅读
研究
发送
存档
深度查看
```

表达特点：

```text
长页面
连续阅读
Scroll
高信息密度
表格和说明可更完整
响应式
```

---

# 3、Presentation Mode

推荐输出：

```text
presentation/
├── index.html
├── deck-manifest.js
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── slides/
```

适用：

```text
汇报
路演
会议
大屏
讲解
```

表达特点：

```text
HTML Slide Deck
Overview / Gallery / Present
逐页讲述
更强的数据叙事
更明确的 Motion 节奏
```

Presentation 的内部信息架构必须采用：

```text
Main Deck
+
Appendix / Backup Slides
```

完整规则见：

```text
references/19-presentation-main-deck-and-appendix.md
```

Presentation 的 Motion Choreography / Temporal Storytelling 统一由：

```text
references/23-presentation-motion-choreography.md
```

定义。

Presentation 的多文件构建、Artifact Type、Writer Routing、Deck Manifest SSOT、Shared Asset Lock 与 Integrity Gate 统一由：

```text
references/22-presentation-artifact-integrity-contract.md
```

定义。

---

# 4、Presentation 容量规则

如果内容装不下：

```text
增加 Slide
或把支撑细节路由到 Appendix
```

而不是：

```text
删内容
省略结论
隐藏表格
缩字体到不可读
```

同时也不是：

```text
把 Raw Markdown 长段落原样拆成很多 Slide
```

正确做法是：

```text
先完成 Transformation
↓
再把 Complete Design Input Package 中的结构化语义拆分到更多 Slides
```

复杂内容可以拆为多页，例如：

```text
Slide 12：T04 Overview Chart
Slide 13：T04 Detailed Table
Slide 14：T04 Key Findings
```

Main + Appendix 示例：

```text
T04
→ Main Deck：Overview Chart + Key Findings
→ Appendix：Detailed Table + Full Notes
```

---

# 5、长 Deck 的 Grammar 先行规则

如果最终 Deck 明显超过 5 页：

```text
先用代表页面建立 design grammar
+
按 23 建立 deck-level motion rhythm / representative motion grammar
↓
再批量展开完整 deck
```

但：

```text
代表页只是中间设计方法
!=
最终交付范围
```

最终 Main Deck + Appendix 都必须生成完整。

---

# 6、用户只参与一次选择

用户只参与：

```text
Design Direction / 风格方向选择
```

不再参与：

```text
Report Mode / Presentation Mode / Both
```

系统默认：

```text
Both
```

---

# 7、QA 路由

双模式 QA 编排见：

```text
references/08-qa-and-repair.md
```

Reviewer Profile 见：

```text
references/14-huashu-design-critique-routing.md
```

Presentation Artifact Build / Integrity 见：

```text
references/22-presentation-artifact-integrity-contract.md
```

本文件不维护第二份 Reviewer 评分规则。

---

# 8、V2.7：双模式共享 Design DNA，但 Expressiveness 可做载体适配

双模式都必须消费 `Selected Design Expressiveness Profile`。

```text
Report
= 阅读优先 + Adaptive Expressiveness

Presentation
= 讲述优先 + Adaptive Temporal Expressiveness
```

Mode Adaptation 可以改变表达强度，但不能无理由把用户选中的设计胆量抹平。

例如：

```text
BOLD Prototype
→ Report 保留关键 Signature Composition / Data Drama
→ Presentation 进一步强化 Stage / Motion
```

而不是：

```text
BOLD Prototype
→ Final Report 退化成普通 Table / Card 模板
```

完整规则见 `25-design-expressiveness-and-controlled-boldness.md`。

