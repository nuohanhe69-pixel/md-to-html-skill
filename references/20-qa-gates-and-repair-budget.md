# QA Pass Gates & Repair Budget Contract

本文件把“PASS / FAIL”从模糊判断变成可执行 Gate，并限制无限修复循环。

---

# 1、总原则

最终交付必须同时通过：

```text
Presentation Artifact Integrity Gate（Presentation）
Content Integrity Gate
Frontend Render Gate
Design Critique Gate
Mode-specific Gate
Data / Motion Gate
Motion Semantic Safety Gate（Presentation）
Motion Expressiveness Gate（条件性）
Design Expressiveness Fidelity Gate
Selected Design System Consistency Gate
```

任一关键 Gate FAIL：

```text
Final Delivery = BLOCKED
```


---

# 1.5、Presentation Artifact Integrity Gate【硬性】

Presentation 必须先满足：

```text
Artifact Type Violations = 0
Writer Routing Violations = 0
Runtime Deck Manifest = VALID
Manifest Slide Paths = ALL EXIST
Manifest Slide Count = Runtime Slide Count
Main / Appendix Metadata = VALID
Asset Dependency Resolution = PASS
Shared Asset Integrity = PASS
CSS / JS HTML Wrapper Violations = 0
Stale Unregistered Runtime Artifacts = 0
```

任一项 FAIL：

```text
Presentation Render QA = NOT READY
Final Delivery = BLOCKED
```

完整规则见：

```text
references/22-presentation-artifact-integrity-contract.md
```

---

# 2、Content Integrity Gate【硬性】

必须：

```text
Inventory Structural Coverage = 100%
Semantic Obligation Coverage = 100%
Exact Fact Fidelity = 100%
Required Relationship Coverage = 100%
Source Table Entry Coverage = 100%
Source Table Required Dimension Coverage = 100%
Source → DIP Evidence Coverage = 100%
DIP → Report Evidence Coverage = 100%
DIP → Presentation Evidence Coverage = 100%
DIP Hash Integrity = PASS
Missing Obligation = 0
Unproven Obligation = 0
Report Semantic Coverage = 100%
Presentation Semantic Coverage = 100%
Report Source Table Coverage = 100%
Presentation Source Table Coverage = 100%
Long Content Transformation = PASS
Raw Markdown Direct Rendering = ZERO
```

`Information Fidelity = HIGH` 仍作为语义质量要求，但不能替代 `Exact Fact Fidelity = 100%`。

这里没有“差不多通过”，也不允许 ID / Destination / Manifest / HTML 注释充当完整 Content Evidence。

完整 Evidence Gate 数据模型见：

```text
references/24-semantic-obligation-and-evidence-contract.md
```

---

# 3、Huashu Design Critique Gate

如果当前 Huashu 使用 10 分制，则父 Skill 默认 Gate 为：

```text
Overall Score >= 7.5
Concept / 立意 >= 7
No Dimension < 6
No Fatal Finding unresolved
No Critical Finding unresolved
```

Report 额外要求：

```text
Functionality >= 7
Craft Quality >= 7
```

Presentation 额外要求：

```text
Visual Hierarchy >= 7
Functionality >= 7
Narrative / Presentation Suitability = PASS
```

如果 Huashu 当前版本改了评分体系：

```text
以当前 critique guide 的评分口径为准
+
转换成等价的“无 Fatal / Critical + 良好以上” Gate
```

不得因为评分格式变化就取消质量门槛。

---

# 4、Frontend Render Gate

必须：

```text
Verification Status = verified
或对无法验证部分明确 BLOCKED
```

最终可交付版本不得存在未解决的：

```text
Critical overflow / clipping
Broken image / font
Deck navigation failure
iframe load failure
关键 responsive failure
关键 console error
Manifest / Counter / Overview / Jump runtime 不一致
Stylesheet 未实际加载
动画最终状态破坏可读性
```

若环境原因导致无法完成必要 Level A / B 验证：

```text
Render QA = BLOCKED
```

不能伪装成 PASS。

---

# 4.5、Presentation Motion Semantic Safety Gate【硬性】

Presentation 必须满足：

```text
Static / Reduced-motion Fallback Coverage = 100%
Motion Traceability = 100%
Motion-only Semantic Unit = 0
Motion-induced Information Loss = 0
Final Hold Readability = PASS
Motion Runtime 未初始化时核心内容不应永久隐藏
```

Main Deck 每一张 Slide 必须存在：

```text
Choreography Decision
```

并且 Motion Storyboard 必须可追溯到对应 Cxxx / Txx。

完整规则见：

```text
references/23-presentation-motion-choreography.md
```

任一 Semantic Safety 项 FAIL：

```text
Final Delivery = BLOCKED
```

---

# 4.6、Motion Expressiveness Gate【条件性设计质量 Gate】

如果：

```text
Selected Direction 明确包含 Motion DNA
或
Design Context 是演示 / Keynote / 大屏
或
Main Deck 有多个天然适合动态建立的趋势 / 流程 / 时间轴 / 数据关系
```

则必须由 Huashu Critique 判断：

```text
Motion Choreography Quality = PASS
Temporal Narrative = PASS
Mechanical Fade-only Pattern = NO
Deck-level Rhythm = PASS
```

如果内容天然不适合 Motion，可标记：

```text
Motion Expressiveness = N/A / intentionally restrained
```

该 Gate 不允许反向逼迫内容“为了动画而动画”。

---

# 5、Selected Design System Consistency Gate

必须：

```text
Report vs Selected Design System Snapshot = CONSISTENT
Presentation vs Selected Design System Snapshot = CONSISTENT
Report vs Presentation Design DNA = CONSISTENT
```

如果用户选了 B，但最终更像 A：

```text
Gate = FAIL
```

即使页面本身很漂亮也不能交付。

---


# 5.5、Design Expressiveness Fidelity Gate【方向一致性设计 Gate】

最终必须基于 `Selected Design Expressiveness Profile` 判断：

```text
Design Ambition Consistency = PASS
Controlled Boldness Boundary = PASS
Structural Variety = PASS / N/A
Signature Expression Preservation = PASS / N/A
Report Expressiveness = PASS / intentionally restrained
Presentation Expressiveness = PASS / intentionally restrained
Visual Monotony = NO material issue
```

该 Gate 不要求所有设计都大胆；它要求最终表达强度忠实于用户选中的方向。

以下均可 FAIL：

```text
用户选 BOLD → Final 退化为重复 Table / Grid / Card 模板
用户选包含 Report Motion 的方向 → Final 无理由完全静态
用户选克制方向 → Final 被强行加入大量炫技 Motion
为了大胆破坏 Readability / Engineering Safety
```

完整规则见：

```text
references/25-design-expressiveness-and-controlled-boldness.md
```

# 6、Repair Budget

默认最多执行：

```text
3 个完整修复轮次
```

每一轮必须：

```text
汇总所有 Findings
↓
父 Skill 复核
↓
一次性修复一组相关问题
↓
完整 Regression QA
```

禁止：

```text
Finding 1 → 修 → 跑一次
Finding 2 → 修 → 跑一次
Finding 3 → 修 → 跑一次
```

导致无限碎片化循环。

---

# 7、三轮后仍失败怎么办

如果第 3 轮后仍存在关键 FAIL：

```text
run-state = QA_BLOCKED
Final Delivery = BLOCKED
```

输出：

```text
Remaining Findings
为什么仍未通过
已尝试的修复
是否需要用户决定取舍
```

除非用户明确要求继续，不再无限自动迭代。

---

# 8、Repair Round 不是降低标准的理由

```text
Round 3
!=
放宽 Coverage
!=
允许删内容
!=
允许换 Design Direction
!=
允许跳过 Render QA
```

Repair Budget 只限制循环次数，不改变质量标准。

---

# 9、Artifact-only Repair 的边界【V2.4】

如果 Finding 只涉及：

```text
Artifact Type
Manifest
Shared Asset
Runtime Path
Writer Routing
Navigation Assembly
```

则：

```text
只修 Artifact Build Layer
```

不得重做 Content Engineering 或 Design Direction。

Artifact-only Repair 必须被记录在当前 Repair Round 中；修复后至少重新执行：

```text
Artifact Integrity QA
受影响的 Frontend Render QA
最终完整 Regression QA
```

不能因为“只是工程 Bug”就跳过最终回归。

# 10、V2.9 Authority / Source Integrity / Responsive Semantic Gates

## 10.1 Source Integrity Gate【DIP Lock 前】

读取：

```text
references/31-source-integrity-gate.md
```

必须：

```text
Source Integrity Scan = EXECUTED
Silent Source Correction = 0
Unregistered Material Conflict = 0
```

允许：

```text
SOURCE_INTEGRITY_PASS_WITH_CONFLICTS
```

前提是冲突已形成可追溯 Semantic Obligation。

## 10.2 Design Intent Authority Gate【Huashu 前】

```text
Intent Target Coverage = 100%
Intent Obligation Ref Coverage = 100%
New Business Fact = 0
Removed Business Obligation = 0
Business Priority Mutation = 0
Required Relationship Mutation = 0
Prescriptive Layout Command = 0（用户明确指定除外）
```

失败：

```text
DESIGN_INTENT_AUTHORITY_VIOLATION
```

## 10.3 Responsive Semantic Preservation Gate【Final QA】

读取：

```text
references/32-semantic-carrier-and-responsive-preservation.md
```

必须：

```text
Responsive Semantic Loss = 0
Interaction-induced Semantic Loss = 0
Reduced-motion Semantic Loss = 0
```

## 10.4 Lightweight Design Reflection【非阻塞】

读取：

```text
references/33-lightweight-design-reflection-qa.md
```

Reflection Finding 默认不占用 Hard Gate 失败计数；只有升级为真实 Semantic / Render 问题时才进入 Repair Round。
