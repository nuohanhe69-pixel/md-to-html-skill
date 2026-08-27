# QA & Repair Orchestration

本文件只负责 QA 的执行顺序、聚合和修复循环。

专项规则：

```text
Coverage / Fidelity → 03
Source Table → 04
Dual Reviewer → 14
Presentation Main / Appendix → 19
PASS Gate / Repair Budget → 20
Presentation Artifact Build / Integrity → 22
Presentation Motion Choreography / Semantic Safety → 23
```

---

# 1、QA 总架构

必须按顺序执行：

```text
A. Presentation Artifact Integrity QA
B. Content Integrity QA
C. Frontend Render QA
D. Huashu Design Critique
E. Mode-specific QA
F. Data Visualization & Motion QA
G. Presentation Motion Semantic Safety QA
H. Motion Expressiveness QA（适用时）
I. Selected Design System Consistency QA
```

任一关键 Gate 未通过，不得最终交付。


# 1.5、Presentation Artifact Integrity QA

Presentation 在进入浏览器 Render QA 前，必须先通过：

```text
references/22-presentation-artifact-integrity-contract.md
```

这一步只判断：

```text
Artifact Type
Writer Routing
Deck Manifest SSOT
Shared Asset Lock
Dependency Resolution
Runtime File Completeness
```

如果 Artifact FAIL：

```text
只回滚 Presentation Artifact Build
```

不得重做 Content Engineering 或改变 Selected Design System。

---

# 2、Content Integrity QA

分别对 Report / Presentation 建立：

```text
Source Semantic Coverage Mapping
Source Table Transformation Mapping
```

并执行：

```text
Inventory Structural Coverage QA
Semantic Obligation Coverage QA
Exact Fact Fidelity QA
Required Relationship Coverage QA
Source Table Entry / Dimension Coverage QA
Source → DIP Evidence QA
DIP Hash Integrity QA
DIP → Report Evidence QA
DIP → Presentation Evidence QA
Transformation QA
Raw Markdown Direct Rendering Check
```

详细 Coverage 规则见：

```text
references/03-semantic-coverage-and-fidelity.md
references/04-source-table-protocol.md
references/13-complete-design-input-contract.md
references/17-render-ready-transformation-boundary.md
references/24-semantic-obligation-and-evidence-contract.md
```

禁止把以下当成 PASS Evidence：

```text
Cxxx / Txx 仅出现在注释或属性中
只有 Destination 名称
只有 Manifest 路由
生成器自行写“Coverage = 100% PASS”
```

Coverage 必须由 `workspace/coverage-evidence-ledger.md` 的实际 Evidence 推出。

---

# 3、Huashu Design Critique

Report / Presentation 的评审 Profile、评分维度、Reviewer 权限统一由：

```text
references/14-huashu-design-critique-routing.md
```

定义。

---

# 4、Frontend Render QA

`frontend-visual-qa` 只做已经渲染结果的实现 / 浏览器 QA。

具体 Profile 与边界统一由：

```text
references/14-huashu-design-critique-routing.md
```

定义。

---

# 5、Mode-specific QA

Report 至少检查：

```text
长页面阅读节奏
Section 间距
Desktop / Mobile
宽表格与横向滚动
无意义大面积留白
文字堆叠
深度阅读体验
```

Presentation 在 Artifact Gate PASS 后至少检查：

```text
Main Deck Narrative
Appendix Completeness
每页容量
异常内部滚动
Deck 完整性
Design Grammar
翻页 / Overview / Gallery / Present
Main + Appendix Coverage = 100%
```

Presentation 的完整 IA 规则见：

```text
references/19-presentation-main-deck-and-appendix.md
references/22-presentation-artifact-integrity-contract.md
```

---

# 6、Data Visualization & Motion QA

必须检查：

```text
图表数据准确
Chart / Table 一致
Cxxx / Txx 可追溯
无虚构数据
Motion 服务理解
动画结束态可读
Static Fallback 完整
Motion Density 符合载体
```

通用 Visual / Motion Routing 见 `11-huashu-visualization-motion-routing.md`。

Presentation 额外必须按：

```text
references/23-presentation-motion-choreography.md
```

检查：

```text
Motion Traceability = 100%
Motion-only Semantic Unit = 0
Static / Reduced-motion Fallback Coverage = 100%
Final Hold Readability = PASS
Motion Runtime Failure Tolerance = PASS
Deck-level Motion Rhythm（适用时）
```

---

# 7、统一 Fix Owner

Reviewer Finding 的流程只能是：

```text
Finding
↓
md-to-html-report 复核
↓
Complete Design Input Package
+ Selected Design Direction Contract
+ Selected Design System Snapshot
+ Huashu Design Method
↓
形成修复方案
↓
修改
↓
完整 Regression QA
```

如果 Finding 成立但 Reviewer Suggested Fix 会背离用户选定方向：

```text
接受 Finding
拒绝 Suggested Fix
使用原设计体系解决同一个问题
```

---

# 8、PASS Gate / Repair Budget

完整阈值与最大修复轮数只由：

```text
references/20-qa-gates-and-repair-budget.md
```

定义。

默认最多 3 个完整 Repair Rounds；仍有关键 FAIL 时进入 `QA_BLOCKED`。

# V2.9 Design Reasoning QA 编排

V2.9 额外读取：

```text
references/26-what-why-how-authority-model.md
references/27-design-intent-creative-brief-contract.md
references/31-source-integrity-gate.md
references/32-semantic-carrier-and-responsive-preservation.md
references/33-lightweight-design-reflection-qa.md
```

Hard QA 增加：

```text
Design Intent Authority Regression
Responsive Semantic Preservation
```

Light Reflection：

```text
默认 NON-BLOCKING
不直接修改 HTML / CSS / JS
不因为“还能更好看”无限开启 Repair Round
```

如果 Reflection 暴露 Required Relationship / Semantic Loss，则升级到 Hard Gate。
