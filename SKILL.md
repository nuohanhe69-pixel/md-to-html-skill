---
name: md-to-html-report
description: 将 Markdown 经过完整内容工程、Source Integrity、100% 语义 / Source Table Coverage 与 render-ready Transformation 后锁定 WHAT，再生成只描述语义关系 / Desired Takeaway / Visual Risk 的 Design Intent Creative Brief（WHY），由 Huashu 在 Selected Design Direction 下自由决定 Visual Grammar / Composition / Scrollytelling / Motion（HOW）。先生成三份同 WHAT、同 WHY、不同 HOW 的 Design Direction Prototypes 供用户完成唯一一次风格选择，再自动生成完整 Report HTML 与 Presentation HTML Deck。Raw Markdown 只作为 Source of Truth / Traceability；Content Plane 不可变，Design Reasoning Plane 不越权，Visual Expression Plane 保持 Controlled High Freedom；最终通过 Evidence-backed Content QA + Huashu Design Critique + frontend-visual-qa Render QA，并执行 Responsive Semantic Preservation。
---

# md-to-html-report — Orchestrator (V2.9 WHAT / WHY / HOW)

本文件只负责：

```text
任务入口
Phase 顺序
Gate
Reference 路由
角色分工
最终交付条件
```

详细规则的唯一正文在 `references/`。

开始前必须完整读取：

```text
references/00-core-invariants.md
references/00-rule-ownership-map.md
```

任何执行都不得背离 Core Invariants。

---

# 1、任务目标

目标：

```text
Markdown
↓
完整 Content Engineering
↓
Source Integrity Gate
↓
Complete Design Input Package（WHAT LOCKED）
↓
Design Intent Package（WHY GUIDED）
↓
Direction Comparison Package
↓
Prototype A / B / C（HOW DIFFERENT）
↓
用户唯一一次风格选择
↓
Selected Design Direction Contract
+
Selected Design System Snapshot
↓
Visual Grammar Exploration + Signature / Rhythm Planning（HOW）
↓
Report Mode
+
Presentation Mode（Main Deck + Appendix）
↓
Design Critique + Render QA
↓
Versioned Delivery
```

硬目标由 `00-core-invariants.md` 定义，其中包括：

```text
Semantic Coverage = 100%
Long Content Transformation = 100%
Source Table Coverage = 100%
Raw Markdown Direct Rendering = FORBIDDEN
```

---

# 2、角色

```text
md-to-html-report
= Orchestrator
+ Content Engineer
+ Transformation Engine
+ Design Intent / Creative Brief Owner
+ Coverage Guardian
+ QA Controller
+ Fix Owner

huashu-design
= Design Direction Consultant
+ Visual Design Engine
+ HTML Design Executor
+ Design Critique Reviewer（最终评审阶段）

frontend-visual-qa
= Frontend Render Reviewer

User
= Design Direction Approver
```

完整权限边界：

```text
references/10-huashu-design-contract.md
references/14-huashu-design-critique-routing.md
```

---

# 3、唯一一次 Human Gate

整个工作流只允许一个必须等待用户的 Gate：

```text
Human Design Direction Gate
```

用户只选择：

```text
Prototype A / B / C
或混合方向 / 微调后选择
```

用户不再选择：

```text
Report / Presentation / Both
```

默认自动生成 Both。

完整 Prototype 规则：

```text
references/15-direction-prototype-contract.md
```

---

# 4、严格执行顺序

除 Human Design Direction Gate 外，不要在其他中间阶段停下来只给方案。

## Phase 1 — Input & Dependency

完整读取：

```text
references/01-input-and-dependency.md
references/06-reference-design-analysis.md
```

执行：

```text
STEP 1  定位 Markdown
STEP 2  定位可选 Reference / Design Assets
STEP 3  定位并完整读取 huashu-design
STEP 3A 定位并完整读取 frontend-visual-qa
```

要求：

```text
No Default Reference Template
Original Input = READ ONLY
```

---

## Phase 2 — Source Understanding & Inventory

完整读取：

```text
references/02-source-content-analysis.md
references/03-semantic-coverage-and-fidelity.md
references/04-source-table-protocol.md
references/24-semantic-obligation-and-evidence-contract.md
references/31-source-integrity-gate.md
```

执行：

```text
STEP 4  完整读取 Markdown
STEP 5  建立 Content Model + Source Structure Baseline
STEP 6  建立 Source Content Inventory
STEP 7  为所有 Source Semantic Unit 分配 C001 ~ Cxxx
        并为每个 Cxxx 建立必要 Semantic Obligation Set
STEP 8  为所有 Source Table 分配 T01 ~ TN
        并登记 Required Dimensions / Required Entries / Exact Facts
STEP 9  执行 Inventory Completeness Gate：
        Inventory Structural Coverage = 100%
        Unregistered Declared Item = 0
        Unregistered Source Table = 0
        然后记录 SOURCE_SEMANTIC_UNIT_COUNT + SOURCE_TABLE_COUNT
        + Semantic Obligation Counts
STEP 9A 执行 Source Integrity Gate：
        扫描数字 / 排名 / 正文-表格 / 多源口径 / 百分比 / 版本冲突；
        所有冲突必须登记 SOURCE_CONFLICT，禁止静默纠错。
```

不得只读前几十行、标题或部分章节。

---

## Phase 3 — Complete Transformation & Design Input Lock

完整读取：

```text
references/05-content-transformation.md
references/06-reference-design-analysis.md
references/13-complete-design-input-contract.md
references/16-run-state-and-persistence.md
references/17-render-ready-transformation-boundary.md
references/24-semantic-obligation-and-evidence-contract.md
references/31-source-integrity-gate.md
```

执行：

```text
STEP 10 有 Reference → Reference Design Profile
        无 Reference → Design Context Profile

STEP 11 建立 Semantic Content Transformation Map：
        对每个 Semantic Obligation 记录 Transformation Action
        + 实际 Transformed Result；禁止只写“后面做 Card / Timeline”

STEP 12 完成全部 Content Transformation：
        长文本 / Persona / Process / Relationships /
        Source Table 长文本压缩 / 数据提取 / 核心结论

STEP 13 为每个 Cxxx / Txx 形成 render-ready Transformed Content
        并形成 DUxxx Render-ready Display Units

STEP 14 建立包含真实 Data Plane 的 Complete Design Input Package
        Manifest-only DIP = FAIL

STEP 15 建立 / 更新 coverage-evidence-ledger.md，
        执行 Source → DIP Fidelity Gate

STEP 16 只有 Source → DIP Fidelity PASS 后：
        计算 Inventory / Transformation Map / DIP Content Hash
        执行 Transformation Lock Gate

STEP 16A 落盘：
        source-content-inventory.md
        semantic-transformation-map.md
        complete-design-input-package.md
        coverage-evidence-ledger.md
        run-state.json
```

Gate：

```text
Inventory Structural Coverage = 100%
Source Integrity Scan = EXECUTED
Unregistered Material Conflict = 0
All Cxxx / Txx Semantic Obligations Inventoried = YES
All Cxxx Render-ready = YES
All Txx Render-ready = YES
Source Obligation → DIP Coverage = 100%
Exact Fact Fidelity = 100%
Required Relationship Coverage = 100%
Source Table Entry / Dimension Coverage = 100%
Long Content Transformation = PASS
Raw Markdown Direct Rendering Risk = ZERO
Complete DIP Data Plane = PRESENT
DIP Content Hash = RECORDED
```

未通过不得进入 Huashu。

### Render-ready 示例

完整示例见 `17-render-ready-transformation-boundary.md`。

Huashu 接到的应该像 Locked DIP 中的 Render-ready Display Unit：

```text
DU037
Source Refs: C037 / Txx（如适用）
Obligation Refs: C037.F01 / C037.S01 / C037.R01 ...
Display Content:
- 空间需求
- 安全感知
- 品牌认同
- 长期成本
Required Relationship:
家庭结构 → 使用需求 → 产品偏好 → 最终决策
Mutation Policy:
Content = IMMUTABLE
Layout = FREE
Visual Affordance Hint（ADVISORY ONLY）:
Decision Journey / Matrix / other Huashu-original expression
```

而不是 1200 字 Raw Markdown，也不是只有 `C037 → Card` 的空壳计划。

---

## Phase 3.5 — Design Reasoning / Creative Brief（WHY）

完整读取：

```text
references/26-what-why-how-authority-model.md
references/27-design-intent-creative-brief-contract.md
```

前提：

```text
Complete DIP = LOCKED
DIP Hash = RECORDED
Source → DIP Fidelity = PASS
```

执行：

```text
STEP 16B 只读取 Locked Complete DIP，建立 workspace/design-intent-package.md：
         - target DU / Obligation Refs
         - content purpose
         - semantic structure
         - desired takeaway
         - narrative role
         - visual emphasis
         - visual risk
         - forbidden reinterpretation

STEP 16C 执行 Design Intent Authority Gate：
         Intent Obligation Ref Coverage = 100%
         New Business Fact = 0
         Removed Business Obligation = 0
         Business Priority Mutation = 0
         Required Relationship Mutation = 0
         Prescriptive Layout Command = 0（用户明确指定除外）

STEP 16D 计算 design_intent_package_hash 并写入 run-state.json
         run-state = DESIGN_INTENT_READY
```

硬原则：

```text
WHAT is locked.
WHY is guided.
HOW is free.

Design Intent may change emphasis, never scope.
```

Design Intent 是 Creative Brief，不是第二次内容总结，也不是页面布局说明书。

---

## Phase 4 — Visual Expression Routing & Direction Prototypes

完整读取：

```text
references/07-visual-design-and-html.md
references/10-huashu-design-contract.md
references/11-huashu-visualization-motion-routing.md
references/15-direction-prototype-contract.md
references/24-semantic-obligation-and-evidence-contract.md
references/25-design-expressiveness-and-controlled-boldness.md
references/26-what-why-how-authority-model.md
references/27-design-intent-creative-brief-contract.md
references/28-visual-grammar-exploration-library.md
```

执行：

```text
STEP 17 基于 Locked DUxxx + Design Intent 建立 Visual Expression Capability Routing Map：
        标记 Eligible STATIC / INTERACTIVE / MOTION，而非替 Huashu 指定最终组件；
        每个 Route 必须保留 Cxxx / Txx / Obligation / Design Intent Refs；
        Group Route 必须列出全部 refs，不允许“重点模块列表”替代完整 Routing

STEP 18 只从 Locked Complete Design Input Package 抽取
        Direction Comparison Package，并附上相同范围的 Design Intent Subset：
        DU IDs + Obligation Refs + Locked Display Content + Design Intent Refs
        禁止重新读取 Raw Markdown / 重新创作业务文案
        三方向必须 WHAT Same + WHY Same，只允许 HOW Different

STEP 19 核对 DIP Hash + Design Intent Hash 未变化并锁定 Comparison Package

STEP 20 用完全相同的 Comparison Package + Design Intent Subset 生成：
        prototype-a.html
        prototype-b.html
        prototype-c.html
        Huashu 可自由选择 / 自创 Visual Grammar；
        Visual Grammar Library 只提供词汇，不是模板。

STEP 21 Prototype QA：
        Comparison Package Coverage = 100%
        Locked Content Same = YES
        Exact Facts Same = YES
        Required Relationships Same = YES
        Design Intent Same = YES
        Business Priority Same = YES
        Comparison Scope Same = YES
        New Business Content = ZERO
        Prototype Design Differentiation = PASS
        Composition / Data Drama / Rhythm / Signature Differences = REAL

STEP 22 实际渲染三个 Prototype；环境允许时生成 Preview

STEP 23 落盘 Direction Comparison Package / Prototype Paths
        run-state = WAITING_FOR_DIRECTION_APPROVAL
```

重要：

```text
三个 Prototype
!=
三个完整 Report
```

### Human Design Direction Gate

展示三份真实 Prototype 后：

```text
STOP
```

等待用户唯一一次选择。

---

## Phase 5 — Direction Approval & Selected Design System Lock

用户回复后，完整读取：

```text
references/16-run-state-and-persistence.md
references/18-selected-design-system-snapshot.md
references/21-examples-and-anti-patterns.md
references/24-semantic-obligation-and-evidence-contract.md
references/25-design-expressiveness-and-controlled-boldness.md
references/26-what-why-how-authority-model.md
references/27-design-intent-creative-brief-contract.md
references/28-visual-grammar-exploration-library.md
references/29-signature-moment-and-narrative-rhythm.md
references/30-report-scrollytelling-and-semantic-motion.md
```

执行：

```text
STEP 24 读取 run-state + Complete Design Input Package + Design Intent Package
        并验证 Current DIP Hash = Locked DIP Hash
        + Current Design Intent Hash = Locked Design Intent Hash
        DIP 不一致则停止：DIP_MUTATED_AFTER_LOCK
        Intent 不一致则重新执行 Design Intent Authority Gate，不得重做 Content Engineering

STEP 25 记录用户选择原话

STEP 26 形成 Selected Design Direction Contract

STEP 27 从选中 / 混合 Prototype 提取可执行：
        Selected Design System Snapshot
        + Selected Design Expressiveness Profile
        + Boldness Budget

STEP 28 校验 Snapshot：
        Typography / Color / Grid / Spacing /
        Card / Table / Chart / Motion / Density /
        Composition Boldness / Data Drama / Visual Variety /
        Report Interaction & Motion Density / Narrative Rhythm /
        Signature Expression / Restrained Zones / Must-not-drift Rules

STEP 28A Huashu 基于 Full Design Intent + Selected Direction 建立：
         workspace/visual-grammar-exploration-map.md
         记录候选 Grammar / Chosen Grammar / Why Chosen；
         允许 Huashu 自创 Grammar，不强制套模板。

STEP 28B Huashu 建立：
         workspace/signature-moment-plan.md
         workspace/narrative-rhythm-map.md
         规划 CALM / BUILD / PEAK / HOLD / RESET 与少量 Signature Moments。

STEP 28C 标记适合 Scrollytelling / Semantic Motion 的候选关系；
         是否采用仍由 Huashu 决定，不得由 Design Intent 强制。

STEP 29 落盘 selected-design-system-snapshot.md + 上述 HOW Planning Artifacts
        selected_direction_status = DIRECTION_APPROVED
        current_status = DESIGN_REASONING_READY
```

正确做法：

```text
Selected Direction B
+
Selected Design System Snapshot B
+
完整 Complete Design Input Package
↓
首次完整构建 Report Mode
+
首次完整构建 Presentation Mode
```

---

## Phase 6 — Final Report + Presentation Generation & Artifact Build

完整读取：

```text
references/07-visual-design-and-html.md
references/10-huashu-design-contract.md
references/13-complete-design-input-contract.md
references/24-semantic-obligation-and-evidence-contract.md
references/25-design-expressiveness-and-controlled-boldness.md
references/26-what-why-how-authority-model.md
references/27-design-intent-creative-brief-contract.md
references/28-visual-grammar-exploration-library.md
references/29-signature-moment-and-narrative-rhythm.md
references/30-report-scrollytelling-and-semantic-motion.md
references/32-semantic-carrier-and-responsive-preservation.md
references/11-huashu-visualization-motion-routing.md
references/12-display-mode-and-presentation.md
references/19-presentation-main-deck-and-appendix.md
references/23-presentation-motion-choreography.md
references/22-presentation-artifact-integrity-contract.md
```

共同输入：

```text
Locked Complete Design Input Package（WHAT / 业务内容 READ ONLY）
+
Design Intent Package（WHY / READ ONLY）
+
Selected Design Direction Contract
+
Selected Design System Snapshot
+
Visual Grammar Exploration Map + Signature Moment Plan（HOW Planning）
```

强制：

```text
Huashu = Pure Consumer of Locked DIP
业务内容修改权 = NONE
Design Intent = Creative Brief，禁止改变 Scope / Priority / Fact / Relationship
Content Lock MUST NOT be interpreted as Visual Conservatism
Design Plane = CONTROLLED HIGH FREEDOM
用户可见事实 / 文案只能来自 DIP
版面过密 → 拆组件 / 加 Section / 加 Slide / Appendix
不得由 Huashu 自行删改内容
```

执行：

```text
STEP 30 验证 DIP Hash + Design Intent Hash + Design Intent Authority PASS 后首次完整生成 Report Mode；
        先应用 Selected Design Expressiveness Profile / Boldness Budget；
        保留选中方向的 Composition Boldness / Data Drama / Signature Expression；
        Report Motion / Interaction = ADAPTIVE，而非统一 LOW；
        组件携带 DU / Obligation Traceability Hooks；
        每个核心 Obligation 建立 Primary Carrier，必要时使用 Supporting Carrier 减少重复；
        对 progression / comparison / convergence 可采用 Scrollytelling / Semantic Motion；
        响应式只能简化视觉，不得隐藏真实业务语义；
        禁止 Final Generator 重新总结业务内容

STEP 31 对 Presentation 中每个 DUxxx / Obligation Set 路由：
        MAIN / APPENDIX / MAIN + APPENDIX
        必须保持 Cxxx / Txx / Obligation Traceability

STEP 31A 为每张 Slide 建立 Slide Semantic Contract，先锁定：
         DUxxx / Cxxx / Txx / Obligation Refs /
         Persistent Exact Facts / Required Relationships / Final Semantic Destination

STEP 31B 建立 Presentation Motion Choreography：
         - 每张 Main Deck Slide 的 Choreography Decision
         - Motion Intent
         - Entry / Beats / Climax / Final Hold
         - workspace/presentation-motion-storyboard.md
         - workspace/deck-motion-rhythm-map.md
         - Motion Traceability

STEP 31C 执行 Motion Semantic Safety Pre-Gate：
         Static Semantic Base = COMPLETE
         Motion-only Semantic Unit = 0
         Static / Reduced-motion Fallback Coverage = 100%
         run-state = PRESENTATION_CHOREOGRAPHY_PLANNED

STEP 32 建立 Presentation Build Specification：
        Main Deck + Appendix 的完整 Slide Plan
        + Runtime Deck Manifest
        + Build-time Presentation Artifact Manifest

STEP 33 BUILD-A：锁定 Deck Manifest SSOT
        Slide ID / File / Title / Main|Appendix
        Counter / Overview / Jump / Navigation 全部由它派生

STEP 34 BUILD-B：生成 Shared Assets：
        assets/css/*
        assets/js/*
        media
        记录 fingerprint 后 LOCK

STEP 35 BUILD-C：只根据 Deck Manifest 批量生成 slides/*.html
        禁止扫描目录把非 Slide 文件送进 HTML Writer

STEP 36 BUILD-D：根据同一 Deck Manifest 生成 index.html / Runtime Navigation
        禁止写死总页数或用 i-常量 推导 Appendix 编号

STEP 37 BUILD-E：建立 Artifact Dependency Map
        并核对 Shared Asset Lock / Fingerprint

STEP 38 实现全部 Source Table 的视觉承接：
        Table / Chart / Cards / Matrix / Combination
        按 Txx Required Entries / Dimensions 完整注入；
        不得在此阶段重新做业务摘要 / 数据提取 / 删除 Entry

STEP 39 实现完整 Visual Expression Routing Map
        + Presentation Motion Storyboard
        Motion Runtime 只能作用于已经存在的 Static Semantic Base；
        关键内容默认不得依赖 JS 才可见

STEP 40 run-state = PRESENTATION_ARTIFACT_BUILD
```

最终内容必须：

```text
Inventory Structural Coverage = 100%
Semantic Obligation Coverage = 100%
Exact Fact Fidelity = 100%
Required Relationship Coverage = 100%
Source Table Entry / Dimension Coverage = 100%
DIP Hash Integrity = PASS
Report Semantic Coverage = 100%
Presentation Semantic Coverage = 100%
Report Source Table Coverage = 100%
Presentation Source Table Coverage = 100%
Main Deck + Appendix Coverage = 100%
Static / Reduced-motion Fallback Coverage = 100%
Motion Traceability = 100%
Motion-only Semantic Unit = 0
Design Ambition Consistency = PASS
Controlled Boldness Boundary = PASS
Responsive Semantic Loss = 0
Interaction-induced Semantic Loss = 0
Primary Carrier Coverage = 100%
```

Artifact Build 额外硬约束：

```text
HTML / CSS / JS / Manifest 分类型 Writer
Shared Assets 单一 Write Owner
Shared Assets Build 后 LOCK
Deck Manifest = Runtime Slide SSOT
slides/ = Slide HTML only
```

---

## Phase 7 — Presentation Artifact Integrity Gate

完整读取：

```text
references/22-presentation-artifact-integrity-contract.md
references/16-run-state-and-persistence.md
references/20-qa-gates-and-repair-budget.md
```

执行：

```text
STEP 41 run-state = PRESENTATION_ARTIFACT_QA

STEP 42 Artifact Registry / Type / Writer QA

STEP 43 Deck Manifest QA：
        可解析 / 可执行
        Slide ID 唯一
        Slide Path 全部存在
        Main / Appendix Metadata 合法
        Runtime Count = Manifest Count

STEP 44 Shared Asset QA：
        CSS / JS 类型正确
        无 HTML Wrapper
        Dependencies 全部存在
        Fingerprint 未被 Slide Batch 改写

STEP 45 如果 Artifact FAIL：
        run-state = PRESENTATION_ARTIFACT_BLOCKED
        只回滚到失败的 Artifact Build Phase
        禁止重做 Content Engineering / Cxxx / Txx / Prototype / Design System
```

Artifact Gate PASS 后，才允许进入 Frontend Render QA。

---

## Phase 8 — QA & Repair

完整读取：

```text
references/03-semantic-coverage-and-fidelity.md
references/04-source-table-protocol.md
references/08-qa-and-repair.md
references/11-huashu-visualization-motion-routing.md
references/14-huashu-design-critique-routing.md
references/18-selected-design-system-snapshot.md
references/19-presentation-main-deck-and-appendix.md
references/20-qa-gates-and-repair-budget.md
references/22-presentation-artifact-integrity-contract.md
references/23-presentation-motion-choreography.md
references/24-semantic-obligation-and-evidence-contract.md
references/25-design-expressiveness-and-controlled-boldness.md
references/26-what-why-how-authority-model.md
references/27-design-intent-creative-brief-contract.md
references/31-source-integrity-gate.md
references/32-semantic-carrier-and-responsive-preservation.md
references/33-lightweight-design-reflection-qa.md
```

执行：

```text
STEP 46 Content Integrity QA：
        更新 coverage-evidence-ledger.md
        逐 Obligation 建立 DIP → Report / Presentation Evidence
        禁止 ID / Destination / Manifest / HTML Comment-only PASS
STEP 47 frontend-visual-qa Frontend Render QA
STEP 48 Huashu Design Critique
STEP 49 Mode-specific QA
STEP 50 Data / Motion QA
STEP 50A Presentation Motion Semantic Safety QA：
         Motion Traceability / Static Fallback / Final Hold / Runtime Failure Tolerance
STEP 50B Motion Expressiveness QA（适用时）：
         Temporal Narrative / Deck Rhythm / 非机械 fade-only
STEP 50C Design Expressiveness / Controlled Boldness QA：
         Design Ambition Consistency / Structural Variety /
         Signature Expression Preservation / Report Expressiveness /
         Controlled Boldness Boundary / Visual Monotony
STEP 50D Design Intent Authority Regression：
         Final 没有因为视觉优化改变 Scope / Priority / Required Relationship
STEP 50E Responsive / Interaction Semantic Preservation QA：
         Responsive Semantic Loss = 0
         Interaction-induced Semantic Loss = 0
STEP 51 Selected Design System Consistency QA
STEP 51A Lightweight Design Reflection QA：
         输出 workspace/design-reflection.md；默认 NON-BLOCKING，
         只给表达改进建议，不直接修改 HTML / CSS / JS
STEP 52 汇总 Hard Findings + 可选 Reflection Suggestions
STEP 53 md-to-html-report 统一修复
STEP 54 完整 Regression QA：
        Artifact Integrity
        + Evidence-backed Content Integrity
        + DIP Hash Integrity
        + Frontend Render
        + Huashu Design Critique
        + Motion Semantic Safety / Choreography
        + Design Expressiveness / Controlled Boldness
        + Design Intent Authority
        + Responsive Semantic Preservation
        + Mode / Data / Design System
```

Reviewer 分工：

```text
Huashu Design Critique
= 设计好不好

frontend-visual-qa
= 实现有没有正确跑出来
```

两个 Reviewer 都只能给建议。

Fix Owner：

```text
md-to-html-report
```

QA Gate 与默认 3 轮 Repair Budget 以 `20-qa-gates-and-repair-budget.md` 为准。

如果预算耗尽仍有关键 FAIL：

```text
QA_BLOCKED
```

不得降低 Coverage / Design / Render / Artifact Integrity 标准。

---

## Phase 9 — Generation Artifact Freeze

完整读取：

```text
references/09-output-and-delivery.md
references/16-run-state-and-persistence.md
references/22-presentation-artifact-integrity-contract.md
references/24-semantic-obligation-and-evidence-contract.md
references/25-design-expressiveness-and-controlled-boldness.md
references/26-what-why-how-authority-model.md
references/27-design-intent-creative-brief-contract.md
references/28-visual-grammar-exploration-library.md
references/29-signature-moment-and-narrative-rhythm.md
references/32-semantic-carrier-and-responsive-preservation.md
```

执行：

```text
STEP 55 生成独立新版本输出，不覆盖旧文件
STEP 56 保存 workspace / prototypes / direction approval / design system snapshot
        并保存最终 coverage-evidence-ledger.md + Content Hash 状态
STEP 57 保存 workspace/design-intent-package.md
        + workspace/visual-grammar-exploration-map.md
        + workspace/signature-moment-plan.md
        + workspace/narrative-rhythm-map.md
        + workspace/design-reflection.md（如已生成）
        + workspace/presentation-motion-storyboard.md
        + workspace/deck-motion-rhythm-map.md
        + workspace/presentation-artifact-manifest.md
STEP 58 保存 report.html
STEP 59 保存 presentation/index.html + deck-manifest.js + assets/* + slides/*
STEP 60 生成 analysis.md
STEP 61 冻结 Generation Core：
        current_phase = GENERATION_FREEZE
        current_status = GENERATION_COMPLETE
        postprocess_required = true
        pending_tasks = [POSTPROCESS_FINALIZER, FINAL_DELIVERY]
```

到 STEP 61 为止，V2.9 Generation Core 才算完成。

在 STEP 61 之前禁止读取 `postprocess/` 的实现细节，禁止为了下游编辑器修改 Huashu / DOM / CSS / Motion / Navigation / Responsive。

STEP 58 保存 report.html 时遵守 Artifact Boundary（契约全文见 `postprocess/references/editor-contract.md` §Artifact Boundary）：

```text
必须写（语义承载体 section 级组件上）  data-du-id / data-obligation-refs / data-source-table-id
自由区（Huashu 设计平面）            class / style / id / aria-* / 自定义视觉语义属性
禁区（交付平面私有，base 必须为零）  data-edit-* / data-motion-reveal / data-he-* /
                                    data-human-edit-* / human-edit-* / .he-* 前缀
```

知道"最终会有编辑器"不构成提前写编辑字段的理由——编辑字段全部由
PostProcess 注入，模型在 Generation 阶段一个都不写。

---

## Phase 10 — Required Editable PostProcess

本 Phase 是一等 Workflow Phase，不允许藏在 Phase 9 的子步骤、上下文摘要或可选尾巴里。

执行：

```text
STEP 62 进入 POSTPROCESS_REQUIRED。
        Main Agent 在 Generation 已冻结后直接执行 Finalizer
        （主上下文 + 确定性脚本，单一执行路径，无 subagent 派发）。

STEP 63 唯一允许的最终化命令：
        python postprocess/scripts/finalize_delivery.py \
          --output-root <absolute-output-root>

STEP 64 检查 Finalizer Gate：
        - report.html exists
        - editable/report-editable.html exists
        - editable/editor-validation-result.json exists
        - editable/postprocess-status.json exists
        - base_sha_before == base_sha_after
        - postprocess_status = PASS / PASS_WITH_RUNTIME_WARNING
        - delivery_gate_status = PASS
```

三条硬规则：

```text
1. Phase 10 的唯一合法动作 = STEP 63 的 Finalizer 命令。

2. 禁止手写 / 重新生成 / “参考实现” editable HTML：
   report-editable.html 只能由 Finalizer 从 report.html 确定性派生；
   任何 LLM 直接产出的 editable 副本都是漂移产物，会被确定性重建覆盖。

3. STEP 64 缺任何指纹 = INVALID_DELIVERED，返回本 Phase 重跑 Finalizer；
   禁止以此为由重做 V2.9 / Huashu / report.html。
```

如果 STEP 64 失败：

```text
current_status = POSTPROCESS_BLOCKED
禁止把本轮标记为 DELIVERED
保留 Base Report 并报告 PostProcess Blocker
```

修复章程（STEP 64 失败后进入修复循环时生效，三条元规则，只约束怎么修、不规定修成什么样）：

```text
R1 角色重入：失败属于 HOW 域（Motion / CSS / 视觉结构）时，动手前必须重读
   huashu-design 相关文件（按 references/01 的定位路径）与
   references/25、references/30 的边界节。修复时不是裸模型，仍戴着 Huashu 的帽子。

R2 手术范围：只修 last_artifact_failure.failures.evidence 指向的结构；
   evidence 之外的设计元素、动效、组件一律不得顺手简化或删除。
   删动效不是修复 motion 兜底的最短路径——补安全证照才是。

R3 表达力可观测：修复后重跑 Finalizer 前，对照 run-state 中
   motion_density（修复前 / 修复后）计数；显著下降时在最终交付说明中
   报告该差异，交由用户判断是否接受，不得静默吞掉。
```

完整 PostProcess 契约的唯一正文：

```text
postprocess/README.md
postprocess/references/editor-contract.md
```

---

## Phase 11 — Final Delivery

执行：

```text
STEP 65 在任何最终回复之前执行 Artifact Reality Check。
        如果 report.html 已存在但任一 Editable 指纹缺失：
        无论旧摘要 / run-state 是否写了 DELIVERED，都必须视为 INVALID_DELIVERED，返回 Phase 10。

STEP 66 只有 delivery_gate_status = PASS 才允许 current_status = DELIVERED。
        正常成功时必须同时交付 report.html 与 editable/report-editable.html。
```

上下文恢复优先级：

```text
Artifact Reality > run-state fields > context summary > remembered Phase label
```

因此上下文压缩 / 跨会话恢复后，PostProcess 不得因摘要漏项而被跳过。

最终核心产物：

```text
report.html
+
editable/
  ├── report-editable.html
  ├── editor-validation-result.json
  └── postprocess-status.json
+
presentation/
  ├── index.html
  ├── deck-manifest.js
  ├── assets/*
  └── slides/*
+
workspace/design-intent-package.md
+
workspace/visual-grammar-exploration-map.md
+
workspace/signature-moment-plan.md
+
workspace/narrative-rhythm-map.md
+
workspace/presentation-motion-storyboard.md
+
workspace/deck-motion-rhythm-map.md
+
design-prototypes/*
+
workspace/*
+
analysis.md
```

---

# 5、冲突与优先级

任何规则冲突先读取：

```text
references/00-core-invariants.md
references/00-rule-ownership-map.md
```

原有业务优先级继续保持：

```text
事实准确性
>
Semantic Coverage
>
Source Table Coverage
>
关键内容完整性
>
专业含义准确性
>
长文本结构化质量
>
可读性
>
视觉设计
>
页面简洁
```

---

# 6、最终原则

> **Cover everything, transform intelligently.**

> **保留语义，不保留原始表达形态。**

> **不是完整地搬运 Markdown，而是完整地重构 Markdown。**

> **Reviewer 负责发现问题，Design Engine 按既定方向解决问题，父 Skill 负责最终修复决策。**

> **Huashu 只消费 Locked DIP，不拥有业务内容修改权。**

> **Coverage 必须由 Semantic Obligation Evidence 推出，不能由 ID / Destination / PASS 声明推出。**

> **Content Lock 不得被解释为 Visual Conservatism；设计大胆必须受 Semantic / Readability / Engineering / Professional Boundaries 控制。**

> **WHAT is locked. WHY is guided. HOW is free.**

> **Design Intent 可以改变视觉强调，不能改变内容范围；Visual Grammar 是词汇库，不是模板；Scrollytelling 是 Huashu 的 HOW 能力，不是强制动作。**

> **Responsive / Interaction / Motion 只能改变表达，不能让业务语义在某个设备或状态下消失。**

现在直接执行完整任务；除唯一 Human Design Direction Gate 外，不要停在中间只给方案。


