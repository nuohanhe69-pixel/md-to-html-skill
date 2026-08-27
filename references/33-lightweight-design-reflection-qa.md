# Lightweight Design Reflection QA

本文件定义一个**轻量、非阻塞、只给建议**的设计复盘层。

定位：

```text
Reviewer / Advisor
NOT Modifier
```

它不能替代：

```text
Content Integrity QA
Huashu Design Critique
frontend-visual-qa
```

也不能形成一个新的重型 Review Board。

---

# 1、为什么需要 Reflection QA

Hard QA 主要回答：

```text
内容有没有丢？
实现有没有坏？
设计有没有达到最低标准？
```

Reflection QA 只回答：

> **在不改变 WHAT 的前提下，这个页面是否错过了更好的表达机会？**

---

# 2、输入

必须读取：

```text
Locked DIP
Design Intent Package
Selected Design System Snapshot
Visual Grammar Exploration Map
Signature Moment Plan
Rendered HTML
```

禁止重新读取 Raw Markdown 做新的业务解释。

---

# 3、重点观察

## 3.1 Intent-to-Expression Fit

例如：

```text
WHY = 三因素共同驱动
HOW = 三个孤立 Card
```

建议：

```text
当前视觉没有充分表达共同驱动关系；
可在下一轮尝试汇聚 / 方程 / 关系型构图。
```

如果已经造成 Required Relationship 被误表达，则转交 Hard Content QA，不再视为轻量建议。

## 3.2 Visual Grammar Quality

观察：

```text
Card Abuse
Default Layout
Missed Visualization Opportunity
Table Overuse
Unjustified Decoration
```

## 3.3 Signature Moment

观察：

```text
计划的 PEAK 是否真的形成记忆点
是否高潮过多
是否高潮出现在错误的重要性层级
```

## 3.4 Narrative Rhythm

观察：

```text
连续同构 Section
缺少 CALM / BUILD / PEAK / HOLD 变化
长篇阅读是否疲劳
```

## 3.5 Semantic Motion Opportunity

观察：

```text
是否存在非常适合 Scrollytelling 的 progression，最终却只是静态堆叠
是否 Motion 只是 fade，而没有帮助理解
```

---

# 4、输出格式

生成：

```text
workspace/design-reflection.md
```

建议结构：

```yaml
reflection_id: DR-001
target: DU016
type: MISSED_EXPRESSION_OPPORTUNITY
observation: "三因素关系被表现为平级卡片，关系弱化"
why_it_matters: "用户难以感知三个条件共同构成结论"
possible_directions:
  - "relation-driven composition"
  - "progressive convergence"
preserve:
  - "Locked DIP"
  - "Required Relationship"
  - "Selected Design DNA"
blocking: false
```

---

# 5、默认不阻塞交付

Reflection Finding 默认：

```text
blocking = false
```

只有当它暴露的是：

```text
Semantic Misrepresentation
Required Relationship Loss
Responsive Semantic Loss
```

才升级到对应 Hard Gate。

---

# 6、Reviewer 不直接修改

禁止：

```text
Reflection Reviewer 自己改 HTML / CSS / JS
Reflection Reviewer 自己改 Design Intent
Reflection Reviewer 自己改 DIP
```

Fix Owner 仍然是：

```text
md-to-html-report
```

但父 Skill 可以选择：

```text
接受建议
忽略建议
记录到下一版本
```

避免为了“优化到完美”形成无限修复循环。
