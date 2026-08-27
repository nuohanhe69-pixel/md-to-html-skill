# Run State & Intermediate Artifact Persistence Contract

本文件解决 Human Design Direction Gate、上下文压缩、跨会话继续执行时的状态丢失问题。

核心原则：

> **任何需要在用户选择前后继续使用的中间状态，都不能只存在于模型上下文里，必须落盘。**

---

# 1、必须落盘的中间产物

进入 Human Design Direction Gate 前，至少必须已经生成：

```text
workspace/
├── source-content-inventory.md
├── semantic-transformation-map.md
├── complete-design-input-package.md
├── coverage-evidence-ledger.md
├── design-intent-package.md
├── direction-comparison-package.md
├── visual-expression-routing-map.md
├── presentation-motion-storyboard.md      （用户选定方向后生成）
├── deck-motion-rhythm-map.md               （用户选定方向后生成）
└── run-state.json
```

如果当前环境更适合 JSON，可以同时生成 `.json` 版本；但必须保证人类可读版本存在，方便审计。

---

# 2、Complete Design Input Package 不允许只存在于“模型脑中”

禁止：

```text
完成 Content Engineering
↓
只在当前上下文记住 Cxxx / Txx / Transformation
↓
生成 Prototype
↓
等待用户
↓
上下文压缩后重新猜一遍内容
```

正确：

```text
完成 Content Engineering
↓
落盘 Complete Design Input Package
↓
落盘 Direction Comparison Package
↓
落盘 Visual Expression Routing Map
↓
生成 Prototype
↓
写 run-state.json = WAITING_FOR_DIRECTION_APPROVAL
↓
等待用户
```

---

# 3、run-state.json 至少记录

```text
skill_version
run_id
source_markdown_path
reference_input_path（如有）
current_phase
current_status
source_semantic_unit_count
source_table_count
complete_design_input_package_path
direction_comparison_package_path
visual_expression_routing_map_path
prototype_paths
selected_direction_status
selected_direction_contract_path
selected_design_system_snapshot_path
design_intent_package_path
design_intent_package_hash
design_intent_authority_status
visual_grammar_exploration_map_path
signature_moment_plan_path
narrative_rhythm_map_path
source_integrity_status
responsive_semantic_preservation_status
design_reflection_path
presentation_motion_storyboard_path
deck_motion_rhythm_map_path
motion_choreography_status
motion_semantic_safety_status
presentation_artifact_manifest_path
deck_manifest_path
artifact_build_status
artifact_qa_status
shared_asset_integrity_status
last_artifact_failure
report_output_path
presentation_output_path
qa_round
last_updated_at
```

状态至少允许：

```text
CONTENT_ENGINEERING
CONTENT_INVENTORY_VERIFIED
SOURCE_TO_DIP_FIDELITY_VERIFIED
SOURCE_INTEGRITY_VERIFIED
DESIGN_INPUT_LOCKED
DESIGN_INTENT_READY
DESIGN_INTENT_BLOCKED
DESIGN_REASONING_READY
CONTENT_LOCK_BLOCKED
PROTOTYPES_READY
WAITING_FOR_DIRECTION_APPROVAL
DIRECTION_APPROVED
PRESENTATION_CHOREOGRAPHY_PLANNED
FINAL_GENERATION
PRESENTATION_ARTIFACT_BUILD
PRESENTATION_ARTIFACT_QA
PRESENTATION_ARTIFACT_BLOCKED
QA_IN_PROGRESS
QA_BLOCKED
DELIVERED
```

---

# 4、用户选择后的恢复规则

用户回复选择 A / B / C 或混合方向后：

```text
先读取 run-state.json
↓
读取 complete-design-input-package.md
↓
读取 direction-comparison-package.md
↓
读取三个 Prototype 的 Design DNA
↓
形成 Selected Design Direction Contract
↓
形成 Selected Design System Snapshot
↓
更新 run-state.json = DIRECTION_APPROVED
↓
再进入最终双模式生成
```

禁止因为上下文不足而重新从 Raw Markdown 做第二次内容工程，除非用户明确要求重新分析输入。

---

# 5、状态文件只能保存工作流状态，不能成为新的事实来源

```text
Raw Markdown / 用户材料
= Source of Truth

Complete Design Input Package
= render-ready semantic contract

run-state.json
= execution state only
```

不能把 run-state.json 中的摘要当作事实替代源材料。

---

# 6、版本化与恢复

每一个输出版本必须使用自己的 workspace：

```text
outputs/{markdown-base-name}-v00X/workspace/
```

旧版本 workspace 不得覆盖。

如果执行中断：

```text
优先从最新未完成版本的 run-state.json 恢复
```

不得自动新建一份新的内容工程结果造成同一版本内出现两个不一致的 DIP。

---

# 7、Presentation Artifact Failure 的恢复规则【V2.4】

如果：

```text
Complete Design Input Package 已锁定
Selected Design System Snapshot 已锁定
Presentation Artifact Build / QA 失败
```

恢复时必须优先读取：

```text
run-state.json
workspace/presentation-artifact-manifest.md
presentation/deck-manifest.js
```

然后只从失败的 Artifact Build Phase 继续。

禁止因为 `_shared.css`、Manifest、Runtime Navigation、Asset Path 等构建错误而重新做：

```text
Raw Markdown 解析
Cxxx / Txx Inventory
Content Transformation
Prototype Exploration
用户 Design Direction 选择
Selected Design System Extraction
```

# 8、V2.6：Content Lock 必须持久化 Hash + Evidence

`run-state.json` 除现有路径与状态外，还必须记录：

```text
source_inventory_hash
semantic_transformation_map_hash
complete_design_input_hash
semantic_obligation_count
exact_fact_count
required_relationship_count
source_table_required_entry_count
inventory_structural_coverage_status
source_to_dip_fidelity_status
coverage_evidence_ledger_path
```

Prototype 前、用户选择后恢复、Final Generation 前都必须重新核对 `complete_design_input_hash`。

如果：

```text
Current DIP Hash != Locked DIP Hash
```

则：

```text
DIP_MUTATED_AFTER_LOCK
run-state = QA_BLOCKED / CONTENT_LOCK_BLOCKED
```

不得继续生成。

`coverage-evidence-ledger.md` 在 Human Gate 前至少完成 Source → DIP Evidence；最终生成后追加 Report / Presentation Evidence。

# 9、V2.7：Design Expressiveness 状态持久化

`Selected Design Expressiveness Profile` 与 `Boldness Budget` 存在于：

```text
workspace/selected-design-system-snapshot.md
```

`run-state.json` 额外记录：

```text
selected_design_expressiveness_profile_status
report_expressiveness_status
presentation_expressiveness_status
design_ambition_consistency_status
controlled_boldness_boundary_status
```

Human Gate 恢复后必须从已选择 Prototype + Snapshot 恢复 Expressiveness，不得只恢复 Color / Typography Tokens。

# 10、V2.9 Design Reasoning 状态持久化

Human Gate 前新增持久化：

```text
workspace/design-intent-package.md
```

用户选择后新增：

```text
workspace/visual-grammar-exploration-map.md
workspace/signature-moment-plan.md
workspace/narrative-rhythm-map.md
workspace/design-reflection.md（QA 后，可选但推荐）
```

`run-state.json` 额外记录：

```text
source_integrity_status
design_intent_package_path
design_intent_package_hash
design_intent_authority_status
visual_grammar_exploration_map_path
signature_moment_plan_path
narrative_rhythm_map_path
responsive_semantic_preservation_status
design_reflection_path
```

新增状态允许：

```text
SOURCE_INTEGRITY_VERIFIED
DESIGN_INTENT_READY
DESIGN_INTENT_BLOCKED
DESIGN_REASONING_READY
```

恢复规则：

```text
DIP Hash
+
Design Intent Hash
```

都必须验证。

如果 Design Intent Hash 变化但 DIP 未变化，应重新执行 Intent Authority Gate；不得因此重新 Content Engineering。
