# Design Intent Creative Brief Contract

本文件定义 `workspace/design-intent-package.md` 的生成规范。

定位：

> **Design Intent = Creative Brief，不是 Layout Spec，不是 Content Rewrite。**

完整权限边界先读：

```text
references/26-what-why-how-authority-model.md
```

---

# 1、生成时机

必须满足：

```text
Complete DIP = LOCKED
Source → DIP Fidelity = PASS
DIP Hash = RECORDED
```

然后才允许生成 Design Intent Package。

Design Intent 只能读取 Locked DIP，不得重新读取 Raw Markdown 做第二次业务总结。

---

# 2、每个 Intent 至少包含

推荐结构：

```yaml
design_intent_id: DI-001
target_du_refs:
  - DU003
obligation_refs:
  - C003.F01
  - C003.S01
  - C003.R01
content_purpose: "证明三个条件共同构成上市窗口"
semantic_structure: "multiplicative_convergence"
desired_takeaway: "三个条件缺一不可，且共同指向同一战略判断"
narrative_role: "strategic_proof"
visual_emphasis: "high"
visual_risk:
  - "不得被看成三个孤立卖点"
  - "不得让结论与三因素视觉脱节"
forbidden_reinterpretation:
  - "不得删除任一因素"
  - "不得把业务优先级改成视觉优先级"
notes_for_huashu:
  - "允许任何能正确表达共同驱动关系的原创构图"
```

---

# 3、Design Intent 可以定义什么

## 3.1 Semantic Structure

可使用但不限于：

```text
comparison
contrast
causal_chain
multiplicative_convergence
hierarchy
sequence
progression
feedback_loop
tradeoff
funnel
matrix_relationship
network_relationship
before_after
problem_solution
claim_evidence
conflict
portfolio
journey
```

这些是语义描述，不是组件名称。

## 3.2 Desired Takeaway

只描述用户应该理解的认知结果，不新增结论。

例如：

```text
“450 vs 212 的核心不是两个数字，而是日常用车频率的代差。”
```

前提是这个语义已被 Locked DIP 支持。

## 3.3 Narrative Role

可标记：

```text
OPENING
CONTEXT
TENSION
PROOF
COMPARISON
HUMANIZATION
DECISION
SYNTHESIS
APPENDIX_SUPPORT
```

这只用于全篇叙事编排，不改变业务优先级。

## 3.4 Visual Emphasis

```text
LOW / MEDIUM / HIGH / SIGNATURE_CANDIDATE
```

这是视觉资源分配，不是 P0 / P1 / P2。

禁止：

```text
visual_emphasis=HIGH
↓
自动把业务 P1 改成 P0
```

---

# 4、Design Intent 不得定义什么

禁止字段成为硬命令：

```text
layout = three-column-cards
component = card
chart = donut
animation = fade-in
color = red
position = left
```

如果需要提供视觉启发，只允许写成：

```text
possible_expression_notes
```

并明确：

```text
ADVISORY ONLY
Huashu may ignore / replace
```

Visual Grammar 的候选规则统一见：

```text
references/28-visual-grammar-exploration-library.md
```

---

# 5、Design Intent Grouping / Inheritance

不要求每个细小 DU 都单独写一份长 Creative Brief。

Intent Coverage = 100% 可以通过：

```text
EXPLICIT_INTENT
或
INHERIT_PARENT_INTENT
```

实现。

例如 Appendix 中多个同类 Detail DU 可以继承一个 `APPENDIX_SUPPORT` Intent，只要各自 Obligation Refs 仍可追溯。

允许多个相关 DU 共享一个 Intent，前提：

```text
所有 DU / Obligation Refs 显式列出
Required Relationships 不被改变
独立 Semantic Obligation 不因 Grouping 消失
```

禁止：

```text
“这几条都差不多”
→ 合并成一个新结论
→ 原有独立含义消失
```

---

# 6、Design Intent Integrity Gate

生成完成后必须检查：

```text
Intent Target Coverage = 100%（EXPLICIT + INHERITED）
Intent Obligation Ref Coverage = 100%
New Business Facts = 0
Business Priority Mutation = 0
Scope Mutation = 0
Required Relationship Mutation = 0
Source Table Entry Mutation = 0
Prescriptive Layout Commands = 0（除非用户明确要求固定形式）
```

通过后计算：

```text
design_intent_package_hash
```

并写入 `run-state.json`。

---

# 7、Prototype 与 Final 的消费方式

Prototype：

```text
Direction Comparison Package
+
对应的 Design Intent Subset
↓
Prototype A / B / C
```

三方向必须共享同一 WHY，但可以有完全不同 HOW。

Final：

```text
Complete DIP
+
Full Design Intent Package
+
Selected Design System Snapshot
↓
Huashu
```

---

# 8、错误例子

错误：

```text
原文 Top 7
↓
Design Intent 认为 5 条更聚焦
↓
Final Top 5
```

这是 `CONTENT_SCOPE_MUTATION`。

错误：

```text
原 Top 3 行动 = A / B / C
↓
Design Intent 认为 D 更适合展示
↓
替换 C 为 D
```

这是 `BUSINESS_PRIORITY_MUTATION`。

正确：

```text
Top 7 仍是 Top 7
Top 3 仍是 Top 3

但 Huashu 可以让其中某一条成为视觉高潮，
也可以通过 Appendix / Secondary Carrier 控制阅读密度。
```
