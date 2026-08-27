# 1、输出文件不得覆盖

每次执行必须生成新版本。

输出文件命名基于待转换 Markdown 文件的基础名（不含 `.md` 扩展名），并追加版本号。

推荐结构：

```text
outputs/
└── {markdown-base-name}-v00X/
    ├── workspace/
    │   ├── source-content-inventory.md
    │   ├── semantic-transformation-map.md
    │   ├── complete-design-input-package.md
    │   ├── coverage-evidence-ledger.md
    │   ├── direction-comparison-package.md
    │   ├── visual-expression-routing-map.md
    │   ├── selected-design-system-snapshot.md
    │   ├── presentation-motion-storyboard.md
    │   ├── deck-motion-rhythm-map.md
    │   ├── presentation-artifact-manifest.md
    │   └── run-state.json
    ├── report.html
    ├── presentation/
    │   ├── index.html
    │   ├── deck-manifest.js（或当前环境可靠的等价 Runtime Manifest）
    │   ├── assets/
    │   │   ├── css/
    │   │   │   └── shared.css
    │   │   ├── js/
    │   │   └── images/
    │   └── slides/
    │       ├── 01-cover.html
    │       ├── 02-....html
    │       ├── ...
    │       ├── A01-....html
    │       └── ...
    ├── design-prototypes/
    │   ├── prototype-a.html
    │   ├── prototype-b.html
    │   ├── prototype-c.html
    │   ├── prototype-a-preview.png   （环境允许时）
    │   ├── prototype-b-preview.png
    │   └── prototype-c-preview.png
    ├── direction-approved.md
    └── analysis.md
```

如果对应版本已存在，则自动生成下一个版本，禁止覆盖旧结果。

---

# 2、原始输入不得修改

禁止修改：

```text
原 Markdown
用户提供的 Reference
```

只能读取。

---

# 3、三方向 Design Prototype 与唯一一次用户选择记录

必须保留：

```text
design-prototypes/
```

目录中的三个真实 HTML Prototype：

```text
prototype-a.html
prototype-b.html
prototype-c.html
```

它们：

```text
不是三份完整报告
不是最终 Report
不是最终 Presentation
```

三个 Prototype 必须使用完全相同的：

```text
Direction Comparison Package
```

并分别达到：

```text
Direction Comparison Package Coverage = 100%
Facts Same = YES
Required Relationships Same = YES
Comparison Content Scope Same = YES
```

**不得要求三个 Prototype 分别覆盖完整 Complete Design Input Package。**

`direction-approved.md` 至少记录：

```text
Direction Comparison Package 摘要
展示的三个 Prototype
每个 Prototype 的核心 Design DNA
每个 Prototype 的 Design Expressiveness DNA
用户选择原话
是否混合方向
最终 Selected Design Direction Contract
用户只参与这一次选择的说明
```

如果用户尚未选择：

```text
Design Direction Approval = PENDING
```

此时必须停在 Human Design Direction Gate，不得擅自继续生成完整 Report / Presentation。

---

# 4、双模式最终交付【自动同时生成】

在用户选定方向后，必须自动同时生成：

```text
report.html
presentation/index.html
presentation/deck-manifest.js（或可靠等价 Manifest）
presentation/assets/*
presentation/slides/*
```

不再要求用户选择：

```text
Report Mode / Presentation Mode / Both
```

因为本版本默认：

```text
Both
```

---

# 5、analysis.md

同时输出：

```text
analysis.md
```

至少包含：

```text
Skill
Markdown 输入
Reference 输入（如有）
Design Context Profile 摘要（如果无 Reference）
Reference Design Profile 摘要（如果有 Reference）
Complete Design Input Package 摘要
huashu-design Availability
frontend-visual-qa Availability
Prototype A / B / C 产物
Direction Comparison Package 摘要
Prototype Comparison Coverage QA
用户 Design Direction Approval
Selected Design Direction Contract
Selected Design System Snapshot
Selected Design Expressiveness Profile / Boldness Budget
run-state.json
QA Repair Round Count
Presentation Main Deck / Appendix Mapping
Presentation Artifact Manifest
Deck Manifest Slide Count / Main Count / Appendix Count
Artifact Integrity QA
Shared Asset Lock / Fingerprint QA
Asset Dependency QA
Report Mode 输出路径
Presentation Mode 输出路径
Report Mode Semantic Coverage Rate
Presentation Mode Semantic Coverage Rate
Report Mode Source Table Coverage Rate
Presentation Mode Source Table Coverage Rate
Transformation QA
Raw Markdown Direct Rendering Check
Complete Design Input Package Coverage QA
Information Fidelity QA
Data Visualization & Motion QA
Presentation Motion Storyboard / Deck Rhythm Map
Motion Traceability Rate
Motion-only Semantic Unit Count
Static / Reduced-motion Fallback Coverage
Final Hold Readability
Motion Expressiveness QA（适用时）
Design Ambition Consistency
Controlled Boldness Boundary
Structural Variety
Signature Expression Preservation
Report Expressiveness
Presentation Expressiveness

Report Mode Huashu Design Critique
Presentation Mode Huashu Design Critique

Report Mode Frontend Render QA
Presentation Mode Frontend Render QA

Huashu Critique Keep / Fix / Quick Wins 摘要
Frontend Render Findings 摘要

最终状态
```

---

# 6、最终汇报格式

完成之后明确输出：

```text
本轮 Design Engine：
- huashu-design

用户选择（唯一一次）：
- Design Direction / 风格方向选择

自动生成的最终产物：
- outputs/{markdown-base-name}-v00X/report.html
- outputs/{markdown-base-name}-v00X/presentation/index.html
- outputs/{markdown-base-name}-v00X/presentation/deck-manifest.js
- outputs/{markdown-base-name}-v00X/presentation/assets/*
- outputs/{markdown-base-name}-v00X/presentation/slides/*
- outputs/{markdown-base-name}-v00X/design-prototypes/*
- outputs/{markdown-base-name}-v00X/direction-approved.md
- outputs/{markdown-base-name}-v00X/analysis.md
```

---

# 7、交付验收强调

最终汇报中必须明确写出：

```text
1. 用户只参与一次风格选择
2. Report Mode 与 Presentation Mode 已自动同时生成
3. 双模式都完整覆盖 Complete Design Input Package；这里的“完整”指 Cxxx / Txx / Immutable Facts / Required Relationships / Semantic Requirements 全部有去向，不指 Raw Markdown 原文逐段复制
4. 如果 Presentation 需要更多页数，是通过增加 Slide 实现，而不是通过删内容实现
```


---

# 9、QA 汇报语义【新增】

最终汇报必须明确：

```text
Huashu Design Critique
= 设计好不好

frontend-visual-qa
= 实现有没有正确跑出来
```

Presentation Mode 中：

```text
Huashu Design Critique（PPT / Keynote Profile）
= 主设计质量评审

frontend-visual-qa（HTML Deck / Slide / Projection Profile）
= 实现与渲染评审
```

---

# 10、V2.2 新增交付状态

最终版本还必须保留：

```text
workspace/run-state.json
workspace/complete-design-input-package.md
workspace/selected-design-system-snapshot.md
```

Presentation 必须在 `analysis.md` 中说明：

```text
Main Deck Slide Count
Appendix Slide Count
Main Deck + Appendix Coverage = 100%
```

QA 必须说明：

```text
QA Repair Rounds
Final QA Gate Status
Remaining Blockers（如有）
```

---

# 11、Presentation Artifact 交付记录【V2.4】

最终 `analysis.md` 与汇报必须明确记录：

```text
Presentation Artifact Integrity = PASS / FAIL / BLOCKED
Runtime Deck Manifest Path
Runtime Deck Manifest Slide Count
Main Deck Slide Count
Appendix Slide Count
Manifest Count = Runtime Count
Shared Asset Integrity = PASS / FAIL
Asset Dependency Resolution = PASS / FAIL
Artifact Type Violations = 0
Stale Unregistered Runtime Artifacts = 0
```

不得只写：

```text
iframe 加载正常
```

就跳过 Artifact Integrity。



---

# 12、Presentation Motion 交付记录【V2.5】

最终 `analysis.md` 必须明确记录：

```text
Presentation Motion Choreography = PLANNED / N/A
Main Deck Choreography Decision Coverage = 100%
Motion Traceability = 100%
Motion-only Semantic Unit = 0
Static / Reduced-motion Fallback Coverage = 100%
Motion-induced Information Loss = 0
Final Hold Readability = PASS
Motion Expressiveness = PASS / N/A / FAIL
Signature Motion Moments（如有）
```

并保留：

```text
workspace/presentation-motion-storyboard.md
workspace/deck-motion-rhythm-map.md
```

---

# 12、V2.6 Evidence-backed Content Lock 交付记录

`workspace/` 必须额外保留：

```text
coverage-evidence-ledger.md
```

`analysis.md` 必须记录：

```text
Inventory Structural Coverage
Semantic Obligation Count
Exact Fact Count
Required Relationship Count
Source Table Required Entry Count
Source → DIP Fidelity Gate
DIP Content Hash
DIP Hash Integrity
Semantic Obligation Coverage
Exact Fact Fidelity
Required Relationship Coverage
Source Table Entry Coverage
Source Table Required Dimension Coverage
DIP → Report Evidence Coverage
DIP → Presentation Evidence Coverage
Missing Obligation Count
Unproven Obligation Count
```

最终汇报不得只写：

```text
C001-C050 = PASS
T01-T27 = PASS
```

而必须以 Evidence-backed Gate 结果说明完整性。

# V2.9 Design Reasoning Artifacts

每个版本的 workspace 还应保存：

```text
workspace/design-intent-package.md
workspace/visual-grammar-exploration-map.md
workspace/signature-moment-plan.md
workspace/narrative-rhythm-map.md
workspace/design-reflection.md（如已生成）
```

这些文件不得覆盖旧版本。

交付分析 `analysis.md` 建议记录：

```text
WHAT / WHY / HOW Authority Status
Source Integrity Status
Design Intent Authority Status
Primary Carrier Coverage
Responsive Semantic Preservation Status
Signature / Rhythm Summary
Light Design Reflection Summary
```
