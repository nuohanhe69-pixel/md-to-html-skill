# md-to-html-report-editorworkflow 工作交接文档

> 版本基线：V2.9（git `28ea89f`）｜梳理日期：2026-08-27
> 读者：接手本 Skill 的下一位维护者 / 使用者
> 一句话定位：把 Markdown 变成高质量 Report HTML + Presentation Deck，并派生一份可人工编辑副本，全程保证语义零丢失。

---

## 0. 先看结论（30 秒版）

1. **架构设计是对的**：WHAT/WHY/HOW 三权限平面 + Hash 锁定 + 唯一 Human Gate + 确定性 PostProcess，这套骨架不要推翻。
2. **真正的病根是两个**：
   - **声明式规则过多、机器可验证的过少**——几乎所有 Gate（Coverage=100%、Mutation=0）靠 LLM 自觉自评，长流程后段必然漂移；
   - **规则总量过大稀释注意力**——SKILL.md 1081 行 + references 34 个文件共 ~12,600 行，Phase 6 要求"完整读取"15 个文件，Phase 8 要读 17 个。到执行末段（Phase 10），关键指令早被挤出注意力中心，模型退回"继续生成 HTML"的惯性路径。
3. **已发生的漂移实锤**：Phase 10 本应运行 `finalize_delivery.py` 确定性注入 Editor，实际执行中 LLM 重新手写了一份"带编辑功能的全新 HTML"——base SHA 校验链被整体绕过，且重写过程丢内容（中间页面大面积隐藏）。
4. **解法方向**：瘦身 SKILL.md（Phase 卡片化）→ 把数值型 Gate 脚本化 → PostProcess/QA 用 fresh Subagent 隔离 → 明确四角色职责矩阵、给 Editor 上"户口"。

---

## 1. 现状架构总览

### 1.1 三层权限平面（CORE-20，全架构的灵魂）

| 平面 | 职责 | Owner | 载体 | 状态 |
|---|---|---|---|---|
| **WHAT** | 内容真值：事实/语义义务/表格/关系/优先级 | md-to-html-report | Complete DIP（含真实 Data Plane） | **LOCKED**（Hash 锁定，之后只消费） |
| **WHY** | 设计推理：takeaway/叙事角色/视觉风险/强调 | md-to-html-report | design-intent-package.md | **GUIDED**（可改强调，不可改范围） |
| **HOW** | 视觉表达：布局/构图/动效/Scrollytelling | huashu-design | Prototype + Snapshot + Grammar Map | **FREE**（受控高自由） |

硬原则：`WHAT is locked. WHY is guided. HOW is free.` Design Intent 可以改变视觉强调，永远不能改变内容范围。

### 1.2 根架构三层

```
SKILL.md            = Orchestrator（声明上只管 Phase 顺序 / Gate / 路由）
references/00-33    = 34 个规则域，每域单一 Owner（00-rule-ownership-map.md 仲裁）
postprocess/        = Generation 冻结后的确定性交付子系统（无 LLM，纯脚本）
```

外部协作者：`huashu-design`（HOW 视觉引擎）、`frontend-visual-qa`（渲染评审）、**User（唯一一次选方向）**。

### 1.3 五条数据链

1. **内容证据链（WHAT）**：Raw MD（只读）→ Source Content Inventory（C001~Cxxx / T01~TN）→ Semantic Obligation Set（F01 事实/S01 观点/R01 关系/E01 表行/D01 维度）→ Semantic Transformation Map（Obligation→Action→实际结果，禁止"后面做 Card"空壳）→ Complete DIP（DU001~Dxxx render-ready，Manifest-only=FAIL）→ Fidelity Gate PASS 后 **DIP LOCKED**（Hash 不一致即 `DIP_MUTATED_AFTER_LOCK`）。
2. **设计推理链（WHY）**：Locked DIP（唯一输入，不回读 Raw MD）→ Design Intent Package（每个 DU 的 purpose/takeaway/narrative role/visual emphasis/visual risk/forbidden reinterpretation）→ Authority Gate（Obligation 覆盖 100%、新事实 0、删义务 0、优先级突变 0、规定布局命令 0）→ Intent Hash 锁定。
3. **方向选择链（HOW 入口）**：Locked DIP + Design Intent → Direction Comparison Package（WHAT 同 + WHY 同）→ Prototype A/B/C（只有 HOW 不同，不是三份完整 Report）→ 渲染 + Prototype QA → **Human Design Direction Gate（唯一停顿点）** → Selected Design Direction Contract + Design System Snapshot + Visual Grammar Map + Signature Moment Plan + Narrative Rhythm Map。
4. **双模式产出链**：Locked DIP + Intent + Selected Design System → Report HTML（自适应动效、Scrollytelling、响应式语义零丢失）+ Presentation（Slide Semantic Contract → Motion Choreography → Deck Manifest SSOT → Shared Assets LOCK → slides/*.html 批量生成，导航全部从 Manifest 派生）→ 双 Reviewer QA（huashu 设计好不好 + frontend-visual-qa 渲染对不对）→ **md-to-html-report 是唯一 Fix Owner**。
5. **交付后处理链（确定性，无 LLM）**：report.html（冻结，SHA 永不变）→ `finalize_delivery.py`（唯一入口）→ `build_editable.py` 在 `HE_POSTPROCESS_BEGIN/END` 块内注入 editor.css + editor.js → `validate_non_interference.py`（base SHA 前后一致、剥离注入块后逐字节一致、base 无 HE namespace）→ `validate_editor.py`（Shadow DOM 隔离、JS 语法、Playwright 冒烟 best-effort）→ `editable/report-editable.html` + 两个状态 JSON → `delivery_gate_status=PASS` → `DELIVERED`。

### 1.4 11 个 Phase 与关键 Gate

| Phase | 内容 | 关键 Gate |
|---|---|---|
| 1 | 输入定位：Markdown / Reference / huashu / frontend-visual-qa | 原始输入只读 |
| 2 | Source 理解 + Inventory + Source Integrity 扫描 | Inventory 结构覆盖 100%；冲突登记不静默纠错 |
| 3 | 完整 Transformation + DIP 落盘 | Transformation Lock（Fidelity PASS + Hash） |
| 3.5 | Design Intent（WHY） | Intent Authority Gate |
| 4 | 三方向 Prototype | Prototype QA → **Human Gate（唯一停顿点）** |
| 5 | 方向确认 + Design System/Snapshot 锁定 | DIP/Intent Hash 复核 |
| 6 | Report + Presentation 完整生成 + Artifact Build | Deck Manifest SSOT、动效语义安全预 Gate |
| 7 | Presentation Artifact 完整性 | Artifact QA（失败只回滚构建，不重做内容） |
| 8 | QA + 修复（默认 3 轮预算） | Evidence-backed Coverage、双 Reviewer、回归 QA |
| 9 | 版本化冻结 | GENERATION_FREEZE，postprocess_required=true |
| 10 | 必选 Editable PostProcess | Delivery Gate（base SHA 不变 + 三指纹齐全） |
| 11 | 最终交付 | Artifact Reality Check > run-state > 摘要 |

### 1.5 目录结构与体量

```
md-to-html-report-editorworkflow/
├── SKILL.md                       1081 行（编排 + STEP 细节混居）
├── references/                    34 个文件，共 ~12,600 行
│   ├── 00-core-invariants.md      460 行（硬目标与不变式）
│   ├── 00-rule-ownership-map.md   规则域→Owner 仲裁表
│   ├── 01~33                      各规则域（最大 24 号 733 行）
│   └── （最大文件：24/21/23/22/04，均 >600 行）
└── postprocess/                   确定性交付子系统
    ├── README.md                  入口与执行说明（Main Agent 直接执行 Finalizer，单一确定路径）
    ├── references/editor-contract.md  Editor 规则（62 行）
    ├── scripts/                   finalize / dispatch / run / validate_* 脚本
    └── editor/editor.css + editor.js（注入物）
```

### 1.6 角色与产物

- **md-to-html-report**（本 Skill）＝ Orchestrator + Content Engineer + Transformation Engine + Design Intent Owner + Coverage Guardian + QA Controller + Fix Owner（**一人七役**）。
- **huashu-design** ＝ Design Direction Consultant + Visual Design Engine + HTML Design Executor + Design Critique Reviewer（最终评审阶段）。
- **frontend-visual-qa** ＝ Frontend Render Reviewer。
- **User** ＝ Design Direction Approver（只选 A/B/C 或混合微调，不再选 Report/Presentation/Both——默认 Both）。

最终交付产物：`report.html` + `editable/`（report-editable.html + 两个状态 JSON）+ `presentation/`（index + manifest + assets + slides）+ `workspace/*`（intent/grammar/signature/rhythm 等）+ `design-prototypes/*` + `analysis.md`。

---

## 2. 必须保留的设计资产（交接底线）

下述机制是这套架构真正值钱的部分，任何重构不得破坏：

1. **WHAT/WHY/HOW 三平面权限模型**——它同时回答了三个用户诉求：WHAT 保数据不丢、WHY 保逻辑关系、HOW 给 huashu 自由。
2. **Hash 锁定链**（DIP Hash → Intent Hash → base SHA）——唯一能对抗"静默漂改"的手段。
3. **唯一 Human Gate**——只在方向选择停一次，其余全自动，用户体验正确。
4. **PostProcess 确定性子系统的验证链**——base SHA 前后一致 + 剥离注入块后逐字节一致 + HE namespace 隔离 + Shadow DOM。**这是全架构里唯一被证明"不可能被 LLM 绕过语义"的环节，应该被推广而不是被孤立。**
5. **Reviewer 只提建议 + 唯一 Fix Owner**——qa 为 huashu 提意见（保底）而非直接上手改，这个治理设计是对的。
6. **Deck Manifest SSOT**——导航/计数全部派生，禁止扫描目录/写死页数。
7. **Rule Ownership Map**——每条规则只有一个全文 Owner，冲突有仲裁顺序。

---

## 3. 已知问题（按严重度排序）

### P1｜执行漂移：PostProcess 被绕过，Editable 被手写重建【最严重，已实际发生】

**现象**：Phase 10 规定唯一合法动作是运行 `finalize_delivery.py`（确定性注入 editor.css/js 派生副本），但实际执行中模型**自己重新生成了一份带编辑功能的全新 HTML**。后果：
- `report-editable.html` 不再是 base 的字节级派生 → base SHA 校验链整体失效（手写版根本不会生成 `postprocess-status.json`，校验无从谈起）；
- 重新"创作"过程天然丢内容——**中间页面大面积隐藏**正是这个原因：它不是派生，是凭上下文记忆重写。

**根因**（比现象更重要）：
- a) **模式切换失败**：Phase 1~9 全程在训练模型"生成 HTML"这一种动作模式；Phase 10 突然要求切换到"跑一条 python 命令"。在长上下文末段，指令注意力衰减，模型退回惯性路径。
- b) **关键指令离执行点太远**：Phase 10 的规则写在 SKILL.md 第 860~895 行，文档末尾又有一段"Finalizer V1.2"附录重复表述——两处规范并存本身就是维护隐患，且都远在第 1 章任务目标之后 ~900 行。
- c) **校验靠自觉**：Phase 11 的 Artifact Reality Check（editable 指纹缺失即 INVALID_DELIVERED）定义得很好，但它也是一条"声明式规则"——模型不执行它，就没有任何东西强制它执行。

### P2｜规则总量过大：SKILL.md 与 references 的维护与注意力双重负担

- SKILL.md 1081 行，**自称"只管 Phase/Gate/路由"，实际内嵌 STEP 1~66 全部执行细节**——Orchestrator 与 Executor 混居，名不副实。
- 34 个 reference 共 ~12,600 行；Phase 6 要求"完整读取"15 个文件、Phase 8 要读 17 个。累计上下文极大，直接挤占后段执行注意力（P1 的温床）。
- 每次迭代新规则，维护者要在 ownership map + 多个引用文件间保持一致，成本高且易漏。

### P3｜角色职责混杂：Orchestrator / QA / Repair / Editor 边界不清

- **md-to-html-report 一人七役**：Orchestrator、Content Engineer、Transformation Engine、Intent Owner、Coverage Guardian、QA Controller、Fix Owner 全在同一次执行里。Phase 8 中 STEP 46~52 是 QA、STEP 53 是修复、STEP 54 是回归——**自己 QA 自己修**，"Reviewer 只提建议"的约束全靠自觉。
- **QA 规则四处分居**：08（总编排）、14（Reviewer 路由）、20（Gate+预算）、33（Reflection QA），互有重叠，维护时不知道改哪份。
- **Editor 没有规则 Owner（无"户口"）**：Editor 规则实际存在于 `postprocess/references/editor-contract.md`，但主仲裁表 `00-rule-ownership-map.md` 的 35 个规则域**没有登记 Editor/PostProcess 域**。同时 PostProcess 规则还散落在 SKILL.md V1.2 附录、postprocess/README.md、SUBAGENT.md——**四处维护同一套规则**，正是职责混杂的直接证据。

### P4｜声明式 Gate 无机器验证：用户三大诉求缺保底

- Coverage=100%、Fidelity=100%、Mutation=0……全部是 LLM 自评声明。**没有脚本从产物反推验证**。用户要的"WHAT 不丢、WHY 逻辑关系不变、HOW 不受限"目前只有纸面保证。
- DIP 是 Markdown 而非机器可读结构 → 无法脚本计算覆盖率；HTML 虽要求携带"DU/Obligation Traceability Hooks"，但**没有规定具体属性格式** → 无法脚本提取比对。
- 对照：PostProcess 用 SHA + JSON 状态机做到了机器可验证，所以它是全链路最可靠的一环。**反证了其余 Gate 应走的路。**

### P5｜WHY 逻辑关系的端到端验证最弱

- Required Relationship 在 Obligation（R01）与 Design Intent 中有登记，但"最终 HTML 是否视觉上表达了这层关系"没有任何检查；Authority Gate 的"Relationship Mutation=0"同样靠 LLM 判断。

---

## 4. 解决方案

### 方案 A｜SKILL.md 瘦身 + Phase 卡片化（治 P1 根因 b、P2）

目标：SKILL.md 从 1081 行 → **~200 行**。

- SKILL.md 只保留五块：① 任务管线总图（现有第 1 章那个箭头图）② **11 Phase 总表**（Phase/输入/Gate/产物/路由五列）③ 角色职责矩阵 ④ 冲突优先级 ⑤ 最终原则。
- STEP 1~66 全部细节迁移到 `references/phase-01.md ~ phase-11.md`（每份 ≤150 行，只含该 Phase 的 STEP、Gate 数值、路由）。
- **引入"Phase 入口协议"**（本方案抗漂移的核心）：
  ```
  每进入一个 Phase：
  1. 读 run-state.json 确认 current_phase
  2. 只完整读取该 Phase 对应的一张 phase card（≤150 行）
  3. 执行该 card 的 STEP
  4. 落盘产物 + 更新 run-state.json 后才允许进入下一 Phase
  ```
  效果：把"一次性读 12,600 行"变成"每步只读当前 150 行"——**注意力永远聚焦在执行点附近**，且天然支持断点续跑（context 压缩/跨会话恢复后，从 run-state 直接定位 Phase 并重读对应卡片）。

### 方案 B｜确定性优先：数值 Gate 脚本化（治 P4、P5，直接保住用户三大诉求）

原则：**凡能用集合运算/字符串匹配判定的 Gate，一律从 LLM 自评改为脚本验证；LLM 只负责语义与审美判断。**

1. **DIP 双格式落盘**：`complete-design-input-package.md`（人读）+ `complete-design-input-package.json`（机器读：obligation_id / unit_id / relation / exact_fact / table_entry 全结构化）。
2. **HTML Traceability 属性规范**：每个语义承载组件强制携带 `data-ob="C037.F01,C037.R01"`、`data-du="DU037"`（注意：**必须避开 `HE_*`/`data-he-*` namespace**，那是 Editor 专属，两者冲突会破坏 non-interference 校验）。
3. **新增两个验证脚本**（放 postprocess/scripts/ 旁边或新建 verify/）：
   - `verify_coverage.py`：DIP JSON 的全部 obligation_id 与最终 HTML 的 data-ob 集合做差 → 输出 coverage report JSON（WHAT 不丢的机器保底）；
   - `verify_intent_authority.py`：intent package 引用的 obligation 集合 vs DIP 集合做集合运算 → New=0 / Removed=0 / 关系集 diff=0 全部机器判定（WHY 不变的机器保底）。
4. **HOW 不受限不需要也不应该脚本化**——脚本只验"内容在不在、关系变没变"，不看视觉。视觉质量继续走 huashu Critique（只提建议）。三平面各得其所。

### 方案 C｜Phase 10 硬化 + Subagent 隔离（治 P1 现象，止血优先）

1. **SKILL.md 中 Phase 10 极简化并前置强化**，表述压缩为三条硬规则：
   - 唯一合法动作 = 运行一条命令：`python postprocess/scripts/finalize_delivery.py --output-root <root>`；
   - **禁止手写 / 重新生成 / "参考实现"任何 editable HTML**；
   - 交付前 `postprocess-status.json` 必须存在且 `delivery_gate_status=PASS`，否则一律 `INVALID_DELIVERED` 返回 Phase 10。
2. **删除 SKILL.md 末尾的 Finalizer V1.2 附录**，压缩为 3 行指向 `postprocess/README.md`——消除四处维护同一规则（见方案 D）。
3. ~~Subagent 隔离为主路径~~ **【2026-08-28 已撤】**：经查证 `--dispatch-mode subagent` 从未产生任何行为分支（仅写标签），SUBAGENT.md 从未被执行路径读取——整套 subagent 层是未接线接口面板，已按"每条规则都该有真实执行路径"原则删除（见 §7.6）。当前交付架构 = Main Agent 主上下文 + 确定性脚本平面，单一执行路径。
4. **反手写检测**：`validate_existing()` 已能识别"editable 存在但 status JSON 缺失/SHA 不匹配"，当前行为是重跑 dispatcher 覆写——保持该行为，并在 run-state 写入 `last_artifact_failure='hand-written editable detected, overwritten by deterministic build'`，让漂移留痕可观测。

### 方案 D｜四角色职责矩阵 + Editor 上"户口"（治 P3）

明确职责矩阵（R=执行 A=决策 C=被咨询 I=知会）：

| 动作 | Orchestrator<br>(SKILL.md 瘦身后) | Content/QA/Fix Owner<br>(md-to-html-report) | Reviewer<br>(huashu Critique /<br>frontend-visual-qa) | Editor Owner<br>(postprocess/ 脚本) |
|---|---|---|---|---|
| Phase 顺序 / Gate / 路由 | **A+R** | I | I | I |
| 内容转换 / WHAT | I | **A+R** | – | – |
| Design Intent / WHY | I | **A+R** | C | – |
| 视觉实现 / HOW | I | C（只约束边界） | C（只提建议） | – |
| QA 发现问题 | I | **A**（汇总裁决） | **R**（输出 findings） | – |
| 修复执行 | I | **A+R**（唯一 Fix Owner） | **禁止修改产物** | – |
| Editable 派生 | I | I（只跑命令） | – | **A+R**（确定性脚本） |

配套动作：
1. **00-rule-ownership-map.md 新增一行**：
   `| PostGeneration Editor / Delivery Finalizer | postprocess/references/editor-contract.md | SKILL.md 只给入口命令与 Delivery Gate |`
   ——Editor 从此有唯一规则 Owner，与主体系接轨。
2. **QA 文件收敛**：08/14/20/33 合并为两份——`08-qa-orchestration.md`（总编排+Repair 循环+预算）与 `14-reviewer-contracts.md`（两个 Reviewer 的输入/输出/禁止项契约）。Reviewer 输出强制 findings-only 格式（issue / evidence / severity / suggestion），**禁止输出代码 patch 或直接改产物**——这是"QA 为 huashu 提意见（保底）而非直接上手修改"的落地形式。
3. **md-to-html-report 七役拆解为执行顺序上的分离**而非逻辑角色拆分：Content 阶段（Phase 2~3）不做 QA、QA 阶段（Phase 8 STEP 46~52）不直接修、Fix 阶段（STEP 53）汇总 findings 后统一执行。配合 phase card（方案 A），每张卡片开头声明"本卡片允许的动作类型"，从上下文层面抑制串戏。

### 方案 E｜漂移可观测（所有方案的验收基础设施）

- run-state.json 每 Phase 落盘时附带 `ruleset_digest`（当时读取的 phase card hash）；
- 恢复协议升级：`Artifact Reality > run-state > context summary > remembered Phase label`（已定义，保持）+ 恢复时强制重读当前 phase card；
- 建立最小 Golden Test：固定一份样例 md → 断言三件事：coverage=100%（verify_coverage.py）、base SHA 冻结、editable 剥离注入块后与 base 逐字节一致。任何重构后跑一遍，防止"修漂移引入新漂移"。

---

## 5. 后续推进路线图

### M1（1~2 天，止血，不动结构）

- [ ] SKILL.md Phase 10/11 按方案 C 极简化 + 删除 V1.2 附录重复
- [ ] 00-rule-ownership-map.md 登记 Editor/PostProcess 域（方案 D-1）
- [ ] 确认 validate_existing 对"手写 editable"的覆写路径 + failure 留痕
- [ ] 用 1~2 份真实 Markdown 端到端跑一遍，记录每个实际漂移点（作为后续验收基线）

### M2（3~5 天，结构重构）

- [ ] SKILL.md 瘦身至 ~200 行，STEP 迁移到 phase-01~11 卡片（方案 A）
- [ ] Phase 入口协议落地（run-state 驱动的逐卡读取）
- [ ] QA 四文件收敛为两份（方案 D-2），Reviewer 输出契约 findings-only 化
- [ ] 回归 M1 基线，对比漂移点是否减少

### M3（约 1 周，机器验证）

- [ ] DIP JSON schema 定义 + 双格式落盘（方案 B-1）
- [ ] HTML data-ob / data-du 属性规范（避开 HE namespace，方案 B-2）
- [ ] verify_coverage.py + verify_intent_authority.py 上线（方案 B-3）
- [ ] Phase 8 的数值型 Gate 改为脚本判定，LLM 只做语义/审美部分

### M4（持续迭代）

- [ ] Subagent 化推广：PostProcess（已有契约）→ 双 Reviewer（各自 fresh subagent，天然满足"只提意见不改产物"）→ Prototype 渲染
- [ ] Golden Test 集扩充（多份不同类型 md：长文/多表格/强关系型）
- [ ] 观察 huashu HOW 自由度与质量：若 Critique findings 中"表达保守"占比上升，检查是否 Content Lock 被错误解释为 Visual Conservatism（26 号文件的不变式）

### 明确不建议做的事

- ❌ 增加"更多规则"来治"规则执行不力"——V2.9 已经过密，再增规则只会加剧 P1/P2；
- ❌ 把 Editor 合并进 Generation 阶段（"生成时就带编辑功能"）——会破坏 Artifact Boundary 与 SHA 冻结，等于放弃全链路唯一已验证的确定性资产；
- ❌ 让 Reviewer 拥有写权限来"提高修复效率"——会摧毁 Fix Owner 单点治理，回到多头修改。

---

## 6. 新人上手地图

| 想了解 | 去读 |
|---|---|
| 全流程骨架 | 本文档 §1 + SKILL.md（注意其 Orchestrator 名不副实的现状） |
| 硬性不变式 | references/00-core-invariants.md（460 行） |
| 规则冲突仲裁 | references/00-rule-ownership-map.md |
| WHAT 语义义务体系 | references/24（733 行，最重）+ 03 + 13 + 17 |
| WHY 权限与契约 | references/26 + 27 |
| HOW 自由度边界 | references/10 + 25 + 28 |
| QA 体系 | references/08 + 14 + 20 + 33（待收敛为两份） |
| Editor/交付 | postprocess/README.md → editor-contract.md → finalize_delivery.py |
| 已知坑 | 本文档 §3（P1 漂移务必先读） |

交接时口头补充的关键背景：**当前 git 只有一个 baseline commit（`28ea89f`），任何重构请先开分支保留 V2.9 原貌，M1 止血改动独立成 commit，方便回滚对比。**

---

## 7. Editor V2.0 移植追记（2026-08-27，分支 refactor/v3-restructure）

### 为什么要换编辑器（V1.x 的天花板根因）

用户实测发现 V1.x 编辑器"只有部分字体能改"。根因不是实现疏漏，而是
**"非干扰"的证明方式锁死了能力上限**：

```text
V1.x: 字节级证明（剥离注入块后逐字节 == base）
  → 注入器一个字节都不能碰 base DOM
  → 编辑器只能"盲注入"，在浏览器里运行时自发现可编辑节点
  → 运行时发现必须保守（safeLeaf 零子元素 + 标签白名单）
  → 富文本段落（含 strong/a/span）全部不可编辑
  → motion 未触发的元素（opacity:0）看不见也改不到
```

对照版本 `md-to-html-report-v3.0.1-motion-visibility-safety` 证明了另一条
路线：**编译期结构化标注 + 结构级非干扰证明**——注入前用解析器全量分析
DOM 并加 `data-edit-*` 标注，非干扰改为"剥离注入后 DOM 树 == base 树"。
证明弱一档，换来：富段落可编辑、模块级排版/排序、motion 元素编辑态强制
可见、权限/台账/跨会话撤销。

### 实际改动（同一 Finalizer 入口不变）

| 项 | 变化 |
|---|---|
| `inject_editor.py`（新） | 编译期标注注入器；**标准库迷你 DOM `htmldom.py` 重写（v3.0.1 原版依赖 bs4，本机不可用；保持交付子系统零第三方依赖）** |
| `build_editable.py` | **删除**（旧 HE block 注入器） |
| `validate_non_interference.py` | 字节级 → 结构级等价（剥离注入属性+artifact 后 tree_equal） |
| `validate_motion_visibility_safety.py`（新） | base+editable 双侧 motion 风险校验；base FAIL = 交付 BLOCKED |
| `validate_editor.py` | 新标记/禁用模式（网络/AI/motion 耦合）；运行时冒烟适配新编辑器 |
| `editor/` | v3.0.1 运行时移植（按钮加 id；干净导出补剥 data-motion-reveal） |
| 契约 | `editor-contract.md` 重写为 V2.0（Namespace/权限/台账/8 条 Gate） |

不变的东西：`finalize_delivery.py` 唯一入口、三指纹 Delivery Gate、
base SHA 冻结、M1-3 漂移留痕、M1-1 三条硬规则。基线全绿（见
`tests/BASELINE-M1.md` 末节）。

### 已知边界（诚实记录）

- 结构级证明依赖解析器归一化：极端不良构 HTML 的隐式标签语义可能不被
  保留（htmldom 实现了常见隐式闭合 p/li/td/tr 等；要求 base 为良构 HTML）。
- v3.0.1 面板文字编辑是 textContent 整段替换（行内标记会丢）；无全局
  font-family 字段——两者是 V2.1 的小步增量候选，不再是天花板问题。
- motion 校验对 base 的 BLOCKED 语义是新增的交付拦截（v3.0.1 同款）：
  生成期 QA 应在此前拦截，这里兜底。
- Playwright 运行时冒烟在本机 SKIPPED；交互行为待全链路审计人工确认。

### §7.1 Artifact Boundary 契约（2026-08-27 追加，同分支）

用户提出"模型知道最终会有可编辑版本，可能在生成时提前写编辑字段"。
按根因分析（拒绝症状级补丁），四个表面问题塌缩为一个根因：**report.html
是两个平面的接口，但接口没有契约**——生产侧把接口属性当装饰（24 号
"推荐"），消费侧当承重墙（模块系统硬依赖），且 namespace 清单在 4 处
各自硬编码。

修复（契约 + 执法，非补丁）：

- `postprocess/scripts/artifact_namespace.py`：MUST / FREE / FORBIDDEN
  三区唯一源（机器可读）；注入器与全部校验器 import，删掉 4 处私有清单；
- `editor-contract.md` §Artifact Boundary：人读契约（Canonical Owner，
  已登记 00-rule-ownership-map）；
- SKILL.md Phase 9 三行内联语法 + references/24 §13 "推荐"→"必须"
  （`data-du-id`，唯一实质语义变更，用户已拍板）；
- 执法两道（Delivery Gate，不新增生成侧 QA）：base 污染 → 注入器拒绝
  + BLOCKED（PostProcess 从不清洗修复 base）；base 有 `data-du-id` 承载体
  而 editable 模块为 0 → `module_capability_present` FAIL（静默能力丢失
  哨兵，顺带修复了移植时的 `data-du` vs `data-du-id` 属性名漂移 bug——
  该 bug 此前对真实报告零模块能力且无任何报错）。

Huashu 影响评估：FREE 区（class/style/id/aria-*/自定义视觉语义）首次
正式成文为保护区；MUST 属性渲染惰性、不进 CSS 计算，约束的是记账不是
表达。Presentation deck 不进此契约。

判别式沉淀：**改动是补丁还是修复，看它让下一次变更要碰的地方变多还是
变少**——本变更净效果：新增 1 小模块 + 契约一节，删 4 处硬编码，接口
演化从"改 4 处"变"改 1 处"。

### §7.2 motion Gate 惯用语→属性重构（2026-08-28 追加，同分支）

对 V2.9 产物（GTM.html）深查发现假阳性：它实现了教科书级渐进增强
（no-js 默认 + remove 脚本 + 配对兜底规则 + reduced-motion），却被
旧 motion Gate 判 FAIL——Gate 只认 `motion-ready` 一种字符串标记。
这推翻了两个此前推断：V2.9 未出隐藏问题**不是运气**（30 号文件 §4
早有边界规则且被真实履行）；新版动效收敛的部分原因可能是假阳性逼出的
改写（无法排除）。

根因：Gate 验证惯用语而非属性，等于用代码隐性规定 Huashu 的实现
词汇——"教 Huashu 做事"不在规则文件里，而藏在 Gate 的正则里。

修复（仅 postprocess 域内，30 号 / HOW 平面零改动）：
`classify_fallback_idioms()` 改为属性认定（V1 no-js 配对 / V1b 条件化
隐藏 / V2 无条件可见覆盖 / V3 reduced-motion 四种证明任一即可）；
修复复合选择器误判 bug（`.b-in.on{opacity:1}` 不构成静态证明）。
验证矩阵：GTM.html FAIL→PASS，其余正例保持 PASS，真不安全反例保持
FAIL；基线新增 `motion_gate_idiom_neutral` 断言防回归。

净效果：安全属性不变，实现词汇约束解除——动效表达自由度回归，
防护强度不降。

### §7.3 修复模式章程（2026-08-28 追加，同分支）

真实运行（6a903…会话）暴露的缺口：Phase 10 Gate FAIL 后，主上下文以
Huashu 身份修 report.html 时处于**无锚点状态**——不重读 huashu-design
/ 25 / 30，注意力钉在失败码上，最短路径（删动效）比正确路径（补安全
证照）便宜。修复时有职责路由（HOW 域失败必回 Huashu 域），但没有角色
重入指令、手术范围原则与表达力可观测性。

修复 = SKILL.md Phase 10 失败分支三行元规则（R1 角色重入：HOW 域失败
动手前重读 huashu-design 相关文件 + 25/30 边界节；R2 手术范围：只修
`last_artifact_failure` evidence 指向的结构，禁止顺手简化；R3 表达力
可观测：对照 motion_density 显著下降必须报告不得静默）+
`validate_motion_visibility_safety.py` 新增 `motion_density` 纯观测
指标（7 维计数落 evidence，零判定影响）。七问与判别式已过：规则只在
修复时刻生效、管"怎么修"不管"修成什么样"、下次调修复行为只碰一处。

### §7.4 依赖机制纠错与版本快照决策（2026-08-28 追加）

**纠错**：`huashu-design` 是真实的外部 skill（GitHub: alchaincyf/
huashu-design，本机装于 `~/.codex/skills/huashu-design`，534 行
SKILL.md + 32 份设计语汇文件），由 references/01 §3~§4 的路径搜索
协议在 STEP 3 定位、**完整读入主上下文后按文件执行**——是文件级活
依赖，不是子进程，也不经 TRAE Skill 工具调用。此前会话中"Huashu 只
是角色、没有 skill"的说法为误，以本节为准。本项目全部改动从未触碰
该 skill 一个字节（它位于仓库与 TRAE 安装目录之外）。

**版本漂移风险（供应链观察，暂不处理）**：活依赖意味着上游
huashu-design 更新（如 critique-guide.md 路径/内容变化）本 skill 无
感知。references/01 §8 已有"从当前安装版本定位评审入口"的弹性条款，
风险已缓释，重放依赖锁定需要时再立项。

**V2.9 冻结决策（用户已确认）**：V2.9 原包（纯生成器，无交付平面）
产出质量经 GTM.html 深查验证（安全属性真实履行、语义结构完整），
**一个字节不改**。其三个已知"毛病"（data-du-id 可选措辞、无机器执法、
无可编辑版）全部长在它不存在的交付平面上，归编辑器线修复（已完成）。
V2.9 的剩余价值 = A/B 对照组（动效密度对比已使用一次，M2 验收仍需）
+ 回滚保险（main 分支 28ea89f）。勿改、勿同步、勿双线维护。

**2026-08-28 补注**：huashu-design 当日上午被 TRAE 会话按 references/01
依赖协议全新安装到 `~/.agents/skills/`（符号链接进 TRAE 技能注册表），
从此存在两条加载路径（Skill 工具调用 + 文件级 Read）。新旧两版仅
SKILL.md 有 59 行差异（32 份 references 逐字节一致）：新版定位升为
"设计师工作室"六角色协作 + "one thousand no's"探索预算 + 30 天静默
版本自检；核心哲学从"合格执行者"升到"对标顶级工作室"。references/01
搜索顺序 `~/.agents` 优先于 `~/.codex`，后续运行自动用新版；旧版保留
作 A/B 对照引擎。此前"不经 TRAE Skill 工具调用"的表述按此更新。

### §7.5 M1 全链路审计实据（2026-08-28 追加）

当晚真实运行（用户产出目录 6a903c62…）提供了 M1 有效性最硬证据：
首次 Finalizer 被 motion Gate 拦截（MOTION_RUNTIME_FAILURE_CAN_HIDE_
CONTENT，即"中间页面大面积隐藏"类问题被 Gate 抓获）→ PostProcess
拒修 base（契约行为）→ 主上下文以 Huashu 身份重写 motion CSS → 重跑
Finalizer 检测旧失败产物 → rebuild_reason 留痕 → 确定性重建 →
PASS → DELIVERED。M1-1 硬规则 / M1-3 留痕 / motion Gate 三者在
生产环境各司其职。注：首次命中是否为假阳性已无法考证（首版被覆盖），
Gate 惯用语偏见已于 §7.2 修复，此处仅记录审计链完整性。

### §7.6 Subagent 层删除决策（2026-08-28 追加，用户确认）

**查证结论**：`--dispatch-mode subagent` 在 finalize_delivery.py 与
dispatch_postprocess.py 中从未产生任何行为分支（仅作为标签写入
run-state/analysis）；`postprocess/SUBAGENT.md` 从未被任何执行路径
读取（其契约内容已被 editor-contract.md 全文覆盖）。整套 subagent 层
是 M1 时代规划的隔离方案在 TRAE runtime 无此接口下的未完成迁移残留
——违反"每条规则都该有真实执行路径"的治理原则，保留会误导接手人。

**已删除**：SUBAGENT.md 文件、两个脚本的 --dispatch-mode 参数及
run-state 的 postprocess_dispatch_mode 字段、README/ownership-map/
HANDOVER 三处引用。基线同步重跑全绿。

**保留记录**：若 M3 决定将 Huashu 抽为真子代理，届时按新契约新建
（参考 §7.7 教训），不是恢复本次删除物。

### §7.7 IM 版"工作记录与最终设计颠倒"的教训（2026-08-28 分析，未动我们代码）

用户测试 im-report-only 时发现：其 Phase 4 ONE BEST 原型即完成设计
→ Phase 5 锁定的 Hash 锚定完整原型 → Phase 5b 才写 HOW planning
→ Phase 6 消费 locked design system 而非 planning。planning 从
"设计输入"退化为"事后记录"。我们版本的三重结构性保护（Human Gate
插在原型与锁定之间、快照与 planning 同 STEP 落盘、Phase 6 共同输入
清单明文含 HOW Planning）使该颠倒结构性不可能。**教训：若未来把
Huashu 抽成独立子代理，brief 必须携带 HOW planning 文件作为设计输入，
否则会复刻 IM 版颠倒；fresh re-entry 的锚定物选择是关键设计变量。**
im-report-only 的同步议题因此升级为强烈建议（仍待其 Owner 决策）。

