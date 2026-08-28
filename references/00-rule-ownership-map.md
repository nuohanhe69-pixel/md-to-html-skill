# Rule Ownership Map — Single Source of Truth

规则：

> **每一类规则只有一个全文 Owner。其他文件只允许做上下文摘要、调用说明或示例，不得维护第二份独立规范。**

| 规则域 | Canonical Owner | 其他文件职责 |
|---|---|---|
| Core Invariants | `00-core-invariants.md` | 只引用 |
| 输入 / 外部 Skill 依赖 | `01-input-and-dependency.md` | SKILL 只路由 |
| Source Inventory | `02-source-content-analysis.md` | 其他文件消费其结果 |
| Semantic Coverage / Fidelity | `03-semantic-coverage-and-fidelity.md` | QA 引用 |
| Source Table | `04-source-table-protocol.md` | 视觉阶段只实现已转换结果 |
| Content Transformation 方法 | `05-content-transformation.md` | 17 定义边界，不重复方法 |
| Reference / Design Context | `06-reference-design-analysis.md` | 只作为设计上下文 |
| HTML 视觉实现 | `07-visual-design-and-html.md` | 12 管模式，不重复通用视觉规则 |
| QA 总编排 | `08-qa-and-repair.md` | 14/20 提供专项规则 |
| 输出 / 版本 / 交付 | `09-output-and-delivery.md` | SKILL 只给最终路由 |
| 父 Skill ↔ Huashu 权限 | `10-huashu-design-contract.md` | Prototype/Mode/QA 规则分别引用专项 Owner |
| Visualization / Motion Routing | `11-huashu-visualization-motion-routing.md` | 其他文件不复制 Motion 规范 |
| Report / Presentation Mode | `12-display-mode-and-presentation.md` | 19 管 Presentation 内部 IA |
| Complete Design Input Package | `13-complete-design-input-contract.md` | 16 管落盘，17 管 render-ready Gate |
| 双 Reviewer 职责 | `14-huashu-design-critique-routing.md` | 08 只编排 |
| Direction Prototype | `15-direction-prototype-contract.md` | 10 只声明 Huashu 必须遵守 |
| Run State / Persistence | `16-run-state-and-persistence.md` | 09 记录交付 |
| Transformation Boundary | `17-render-ready-transformation-boundary.md` | 05 提供方法 |
| Selected Design System | `18-selected-design-system-snapshot.md` | 最终生成消费 |
| Presentation Main + Appendix | `19-presentation-main-deck-and-appendix.md` | 12 声明必须采用 |
| QA Gate / Repair Budget | `20-qa-gates-and-repair-budget.md` | 08 编排执行 |
| Examples / Anti-patterns | `21-examples-and-anti-patterns.md` | 其他 Owner 文件原有例子继续保留 |
| Presentation Artifact Build / Integrity | `22-presentation-artifact-integrity-contract.md` | 12/19 只声明 Presentation 必须遵守；08/20 只编排 / Gate |
| Presentation Motion Choreography / Temporal Storytelling | `23-presentation-motion-choreography.md` | 11 只负责 STATIC / INTERACTIVE / MOTION 路由；12/14/19/20 只引用专项规则 |
| Semantic Obligation / Evidence-backed Coverage / Content Lock Proof | `24-semantic-obligation-and-evidence-contract.md` | 02 负责 Inventory 建立；03 定义 Coverage/Fidelity 语义；13 定义 DIP；08/20 只编排与设 Gate |
| Design Expressiveness / Controlled Boldness | `25-design-expressiveness-and-controlled-boldness.md` | 10 管 Huashu 权限；15 管 Prototype；18 管 Snapshot；14/20 只评审 / Gate |
| WHAT / WHY / HOW 权限模型 | `26-what-why-how-authority-model.md` | 10/27/28/29/30/33 只按其权限消费 |
| Design Intent / Creative Brief | `27-design-intent-creative-brief-contract.md` | Prototype / Final Generation 只消费，不重写 |
| Visual Grammar Exploration | `28-visual-grammar-exploration-library.md` | 07/10/15/18 只引用 |
| Signature Moment / Narrative Rhythm | `29-signature-moment-and-narrative-rhythm.md` | 18/25/33 只引用 |
| Report Scrollytelling / Semantic Motion | `30-report-scrollytelling-and-semantic-motion.md` | 11 负责总路由，30 负责 Report 专项 |
| Source Integrity Gate | `31-source-integrity-gate.md` | 02/03/13/20 只编排 / Gate |
| Semantic Carrier / Responsive Preservation | `32-semantic-carrier-and-responsive-preservation.md` | 07/24/20 只引用 |
| Lightweight Design Reflection QA | `33-lightweight-design-reflection-qa.md` | 08/14 只编排；Reviewer 不直接修改 |
| PostGeneration Editor / Delivery Finalizer | `postprocess/references/editor-contract.md` | SKILL.md 只给入口命令与 Delivery Gate；postprocess/README.md 只给执行说明 |
| Artifact Boundary（report.html 接口 MUST/FREE/FORBIDDEN 语法） | `postprocess/references/editor-contract.md` §Artifact Boundary + `postprocess/scripts/artifact_namespace.py`（机器可读唯一源） | SKILL.md Phase 9 只内联三行语法；references/24 §13 只定义义务侧（MUST 属性）并指回本契约 |

## 冲突处理

如果同一规则在两个文件出现：

```text
先查本表 Owner
↓
Owner 为规范正文
↓
非 Owner 只作为上下文说明
```

不得通过“就近读取”覆盖 Canonical Owner。
