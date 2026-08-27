# Huashu Data Visualization & Motion Capability Routing

本文件定义 `md-to-html-report` 如何把已经完成内容工程的 Design Input Package 路由给 `huashu-design` 的数据可视化、交互与动画能力。

核心原则：

> **内容决定表达；动画服务信息，不服务炫技。**

> **Huashu 可以充分发挥 Visual / Data Visualization / Motion Design 能力，但任何视觉强化都不能改变或遗漏 Design Input Package 中的语义、事实、数据和关系。**

---

# 1、先建立 Visual Expression Routing Map

在 Design Input Package 完整锁定后、三方向视觉探索开始前，必须建立：

```text
Visual Expression Routing Map
```

每一个路由对象至少记录：

```text
承接的 Cxxx / Txx / Obligation Refs
Design Intent Ref
Semantic Destination
必须表达的核心信息 / Required Relationship
Eligible Visual Modes
Potential Motion / Interaction Purpose
Evidence / Data Source
Required Static Fallback
```

V2.9 中 Routing Map 只声明“能力适配 / 资格”，不替 Huashu 做最终 HOW 决策。

`Eligible Visual Modes` 可包含：

```text
STATIC
INTERACTIVE
MOTION
```

最终 Actual Visual Mode / Visual Grammar 由 Huashu 在用户选定方向后决定，并记录在 `workspace/visual-grammar-exploration-map.md`。

---

# 2、STATIC / INTERACTIVE / MOTION 三类路由

## 2.1 STATIC

适合：

```text
正文
Executive Summary
Key Takeaways
核心结论
解释性文本
稳定阅读区域
```

## 2.2 INTERACTIVE

适合：

```text
宽表格
高维对比矩阵
Persona 对比
可展开详情
Hover Highlight
Tooltip
复杂图示的分层阅读
```

## 2.3 MOTION

适合：

```text
关键指标 Count-up / Number Reveal
趋势图 Chart Reveal
流程节点 Sequential Reveal
Timeline Progressive Reveal
Priority Ranking 逐项建立
Architecture / Process 关系建立
重点结论的轻量 Motion Emphasis
章节之间的有意义 Transition
```

---

# 3、数据可视化的事实约束【硬性】

所有图表、数字动画、矩阵、Ranking、Timeline、Process 都必须可追溯到：

```text
Cxxx
Txx
Immutable Facts
Required Relationships
```

禁止 Huashu 为了让图更完整而：

```text
补造缺失数字
补造百分比
平滑出不存在的趋势
推导用户未提供的结论
补齐时间点
伪造图例
创造不存在的类别
把定性信息伪装成精确量化数据
```

---

# 4、Motion 只能强化信息，不得隐藏信息【硬性】

最终 HTML 必须满足：

```text
动画正常运行 → 信息完整
动画未播放 → 信息仍完整
动画运行失败 → 核心信息仍可读取
用户不等待动画 → 仍能找到核心事实
```

禁止：

```text
必须看完整段动画才能知道核心结论
把最终数值只放在动画中间帧
通过动画默认隐藏重要信息且无可靠 fallback
```

---

# 5、三方向 Prototype 比较时的 Motion / Visualization 规则

Prototype A / B / C 必须使用同一份：

```text
Direction Comparison Package
```

以及该比较包对应的：

```text
Visual Expression Routing 子集
```

允许三个 Prototype 在以下方面存在差异：

```text
不同但合理的图表语言
不同的信息密度
不同的 Motion Rhythm
不同的 Interactive Pattern
不同的 Section Transition
不同的 Chart / Table / Matrix 组合
```

但必须：

```text
Comparison Package Coverage = 100%
Facts 相同
Required Relationships 相同
核心数据相同
```

Prototype 阶段不要求对完整 Complete Design Input Package 执行全部 Data / Motion 实现。

用户选定方向后，最终：

```text
Report Mode
Presentation Mode
```

才使用完整：

```text
Visual Expression Routing Map
```

覆盖完整 Design Input Package。

---

# 6、双模式 Motion Density 必须分开

Report 与 Presentation 的载体不同，不能继续使用同一套“尽量少动”的默认策略。

正式规则：

```text
Report Mode
→ ADAPTIVE
→ NONE / LOW / MEDIUM / HIGH 由 Selected Design Expressiveness Profile + 内容语义推导
→ 阅读优先，但不把“阅读优先”解释为“默认静态”

Presentation Main Deck
→ ADAPTIVE MEDIUM–HIGH
→ 时间叙事 / 讲述优先

Presentation Appendix
→ LOW
→ 查询 / 查证优先
```

注意：

```text
Presentation Main Deck Motion Density 更高
!=
每个元素都动画
```

每一张 Main Deck Slide 都必须有明确的 Choreography Decision，即使最终主动选择 STATIC。

Presentation 的：

```text
Motion Intent
Slide Motion Storyboard
Deck-level Rhythm
Final Hold State
Motion Traceability
Static / Reduced-motion Fallback
Motion Semantic Safety Gate
```

统一由：

```text
references/23-presentation-motion-choreography.md
```

定义。

仍然不要：

```text
每个 Card 都飞入
每个标题都动画
每个数字都 Count-up
所有图表都同时动
所有 Section 都使用不同动画语言
```

目标是“更会讲”，不是“更多特效”。

---

# V2.6：Visual Routing 消费 DU，不重新决定 Content Scope

`Visual Expression Routing Map` 必须以 Locked DIP 的 `DUxxx` 为主输入，并保留对应 `Cxxx / Txx / Semantic Obligation Refs`。

允许多个 DU / C / T 合并到一个视觉模块，但必须显式列出完整 refs。

禁止：

```text
Routing Map 只列少数“重点模块”
↓
其余内容没有 route
↓
却因为 Complete DIP 总计数存在而宣布 Coverage = 100%
```

Visual Routing 只回答：

```text
HOW TO SHOW
```

不能在此阶段改变：

```text
WHAT TO SAY
Exact Facts
Required Entries
Required Relationships
Semantic Obligations
```

完整证据规则见 `24-semantic-obligation-and-evidence-contract.md`。

---

# 7、V2.7：Report Motion / Interaction 不再使用固定 LOW / OPTIONAL 默认

本节进一步说明上文 `Report Mode → ADAPTIVE` 的执行边界。

Report 仍然阅读优先，但实际 Motion / Interaction Density 必须从：

```text
Selected Design Expressiveness Profile
+
Content Semantics
+
Reading Context
```

推导，因此正式规则改为：

```text
Report Mode
→ ADAPTIVE
→ NONE / LOW / MEDIUM / HIGH 均可
→ 由选中方向决定，而不是统一压低
```

如果 Selected Prototype 明确把 Scroll Reveal / Count-up / Bar Build / Interactive Comparison 等作为 Design DNA，最终 Report 不得无理由全部删除。

如果 Selected Prototype 是静态 Print / Editorial DNA，则静态 Report 完全合法。

所有 Report Motion 必须 progressive enhancement，核心内容默认可读；完整表达强度边界见 `25-design-expressiveness-and-controlled-boldness.md`。

# 8、V2.9 Report Scrollytelling / Semantic Motion

Report Mode 的 Scrollytelling 详细规则统一读取：

```text
references/30-report-scrollytelling-and-semantic-motion.md
```

关键区别：

```text
Decorative Motion = fade / slide / hover
Semantic Motion = 帮助用户理解 progression / comparison / convergence / transition
```

Design Intent 只能指出 semantic structure，不得命令“必须 Scrollytelling”。

是否采用 Scrollytelling 属于 HOW，由 Huashu 根据 Selected Design Direction + 内容语义决定。
