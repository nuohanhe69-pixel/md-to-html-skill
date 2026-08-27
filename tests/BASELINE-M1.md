# M1-4 PostProcess 确定性交付基线

> 基线用途：为 M1 止血改动提供改动前后行为对照（HANDOVER.md §5 M1-4）。
> 运行方式：`python3 tests/postprocess_baseline.py`
> 依赖：仅 python3；playwright / node 缺失时 runtime QA 自动降级，不阻塞。

## 测试范围与诚实边界

本基线覆盖**确定性子系统**（postprocess/）的行为，不覆盖 LLM 执行漂移本身：

| 覆盖 | 方式 |
|---|---|
| 正常交付链（happy path） | 全 Gate 断言 |
| 漂移恢复（drift recovery） | 模拟手写 editable + 缺指纹 + 假 DELIVERED，重跑 Finalizer |
| Base 不变性 | 全场景 SHA 断言 + 剥离注入块后逐字节比对 |
| **长上下文 LLM 漂移**（Phase 1~9 后段是否真的去跑 Finalizer） | **不在本基线内**，见下方"全链路漂移审计协议" |

## 改动前基线（V2.9, commit 28ea89f 之后、M1 改动之前）

环境：macOS 26.5.2 / python3 / playwright 与 node 缺失（runtime QA 降级 SKIPPED）

| 断言 | happy | drift（重跑 Finalizer 后） |
|---|---|---|
| editable/report-editable.html 存在 | ✅ | ✅（确定性重建覆写手写版） |
| editor-validation-result.json 存在 | ✅ | ✅ |
| postprocess-status.json 存在 | ✅ | ✅ |
| postprocess_status | PASS | PASS |
| base_sha_before == base_sha_after | ✅ | ✅ |
| base SHA 全程不变 | ✅ | ✅ |
| strip(editable) == base bytes | ✅ | ✅ |
| delivery_gate_status | PASS | PASS |
| run_state current_status | DELIVERED | DELIVERED |
| **rebuild_reason 留痕** | — | **❌ 无（覆写静默，漂移无观测）** |

### 结论

1. **确定性子系统本身健全**：只要 Finalizer 被执行，Delivery Gate 全链路可过，手写漂移产物会被确定性重建覆盖，base 永不被触碰。
2. **P1 漂移的真正风险面**：漂移只在"LLM 不执行 Finalizer"时成立——此时不存在任何状态 JSON，`validate_existing` 无从触发。拦截依赖 Phase 11 的 Artifact Reality Check（LLM 行为）而非脚本。
3. **可观测缺口（M1-3 目标）**：现有代码在覆写可疑 editable 时不留痕，事后无法从 run-state 判断"发生过一次漂移重建"。

## 全链路漂移审计协议（人工，待执行）

确定性基线无法复现"长上下文后段注意力衰减"这一漂移条件，全链路审计需真实会话：

1. 新开 TRAE 会话，用 1 份真实长 Markdown 完整执行 SKILL.md 全流程（Phase 1~11）；
2. Human Gate 处正常选择方向；
3. 审计点（按 HANDOVER §3 P1）：
   - Phase 10 是否执行了 STEP 63 命令，而非手写 editable（对照 editable/ 三件套是否存在）；
   - workspace/run-state.json 的 `last_artifact_failure` / `rebuild_reason` 是否出现漂移记录；
   - 报告中间章节内容相对源 Markdown 是否丢失（抽样比对）；
4. 结果记录到本文件"全链路审计结果"一节（含日期与会话输入样本）。

## M1-3 改动后复跑结果

改动：`finalize_delivery.py` 在覆写可疑 editable 前写入 `editable_rebuilt_from_invalid` + `rebuild_reason`（成功重建后不清除）。

| 断言 | happy | drift（重跑 Finalizer 后） |
|---|---|---|
| 全部 Gate（同上表） | ✅ 无回归 | ✅ 无回归 |
| base SHA 全程不变 / strip==base | ✅ | ✅ |
| **rebuild_reason 留痕** | —（无覆写，无留痕，符合预期） | ✅ `editable_rebuilt_from_invalid=true` + `rebuild_reason`（含缺失指纹明细） |

前后对比：`drift_overwrite_trace_recorded` **false → true**，其余行为不变。

> 结论：漂移覆写从静默变为可观测。全链路 LLM 漂移拦截仍依赖 Phase 11 Artifact Reality Check + M1-1 三条硬规则；本留痕提供事后审计证据。

## Editor V2.0 移植后复跑结果（同分支追加）

改动：以 v3.0.1 的编译期标注注入器替换 V1.x 运行时盲发现（详见 HANDOVER §7）。
基线断言同步升级：字节级 strip 检查替换为结构级 namespace 检查。

| 断言 | happy | drift（重跑 Finalizer 后） |
|---|---|---|
| 全部 Delivery Gate（含三指纹 / SHA / delivery_gate_status） | ✅ PASS | ✅ PASS |
| base SHA 全程不变 | ✅ | ✅ |
| editable 标注（data-edit-id ≥5 / 模块 ≥3 / 运行时内嵌） | ✅ | ✅（确定性重建完整恢复） |
| base 无 editor namespace（6 类标记全零） | ✅ | ✅ |
| 结构级等价（validate_non_interference） | ✅ PASS | ✅ PASS |
| motion 可见性（base + editable 双侧） | ✅ PASS | ✅ PASS |
| motion-reveal 标注 / locked-fact / movable 模块 | ✅ | ✅ |
| meta.base_report_sha256 与计数（元素/模块/locked/motion） | ✅ | ✅ |
| rebuild_reason 漂移留痕（M1-3，移植后保持） | — | ✅ |

结论：注入器、结构级非干扰、motion 安全、漂移恢复四链路全绿；运行时
Playwright 冒烟在本机降级 SKIPPED（依赖缺失，不阻塞）。富文本段落
（含行内标记）、模块排版、motion 隐藏元素的编辑能力由 editor_v2 断言
间接证明（标注存在性 + 结构等价 + meta 计数），交互行为待全链路审计
（见"全链路漂移审计协议"）在真实会话中人工确认。

## Artifact Boundary 契约落地后复跑结果（同分支追加）

改动：`artifact_namespace.py` 成为接口语法唯一源；注入器/三校验器全部
改为 import；模块发现改用 `data-du-id`（修正 V2.0 移植时的属性名漂移）；
新增两道执法。新增两个场景：

| 场景 | 断言 | 结果 |
|---|---|---|
| contaminated（base 被提前写入 `data-edit-id`） | 注入器拒绝 + BLOCKED + `last_artifact_failure` 含拒绝原因 + base 逐字节不动（无静默清洗） | ✅ 全部成立 |
| sentinel（editable 模块属性丢失 + base 有 `data-du-id` 承载体） | `module_capability_present=false` → validate_non_interference FAIL | ✅ 捕获 |

原有 happy / drift 场景无回归（fixture 同步升级为契约语法
`data-du-id` / `data-obligation-refs` / `data-source-table-id`）。

> 教训记录（夹具自洽陷阱）：V2.0 移植时 fixture 用了注入器的私有字典
> `data-du`，闭环全绿但对真实报告零模块能力且无任何报错——这正是
> `data-du-id` vs `data-du` 属性名漂移静默发生的机制。哨兵 Gate
> `module_capability_present` 即为此类漂移的永久防护；今后夹具必须从
> 契约（references/24 §13）生成，不从被测代码的假设生成。

## 全链路真实运行审计（2026-08-27 追加，M1 有效性实据）

真实会话（非测试夹具）从 48 DU / 14 表源文档跑完整链，证据来自产物
目录文件 mtime 与 run-state 留痕还原：

| M1 机制 | 真实运行表现 |
|---|---|
| motion 安全 Gate | **命中**：首次 Finalizer 因 `MOTION_RUNTIME_FAILURE_CAN_HIDE_CONTENT` BLOCKED（正是"中间页面大面积隐藏"类问题的自动拦截） |
| 契约"拒绝修复 base" | **执行**：PostProcess 未清洗 base，退回生成侧 |
| 生成侧自愈 | 修 motion CSS 后重写 report.html，二跑 Finalizer |
| M1-3 漂移留痕 | **触发**：二跑检测到旧失败产物 → `rebuild_reason` 记录首次失败原因 → 确定性重建 → PASS → DELIVERED |
| Artifact Boundary | base 零污染（data-edit-* / data-he-* 全零）；29 `data-du-id` 承载体被正确消费（editable 29 模块、815 元素、38 motion 标注） |
| WHAT 完整性 | 48/48 obligation 引用全落 report.html；14/14 源表覆盖（T12+T13 视觉合并）；74.32% / 78.44% / 12.93 / 2,170 / BBA60% 等关键一方数据抽查全在 |

跨版本横向观察（GTM.html = V2.9 另一源文档产物，非控制变量 A/B）：
工艺总量同级（CSS 规则块 375 vs 346），新版响应式更好（4 vs 2
@media）但动效显著更保守（transition 11 vs 4；keyframes 1 vs 0）。
动效保守的因果：首次尝试的动效被 motion Gate 拦截，修复后收敛——
这是安全与炫技的交易，不是 Huashu 表达力受限（B 方向视觉系统完整
落地）。调节位置在 motion Gate 通过标准，不在拆 Gate。

## motion Gate 惯用语→属性重构（2026-08-28 追加）

**修正上文审计表述**：GTM.html 深查后发现它是教科书级渐进增强实现
（`<html class="no-js">` 默认携带 + head 内联 remove + `html.no-js
.b-in{opacity:1}` 兜底 + reduced-motion），却被旧 Gate 判 FAIL——
旧 Gate 只认 `motion-ready` 一种字符串标记，把 V2.9 的 no-js 惯用语
当风险信号。"首次产出动效被 Gate 拦截"那条记录**无法排除假阳性**；
"V2.9 未出隐藏问题是运气"的推测同样被此证据推翻（V2.9 的 30 号
文件 §4 早有该边界规则，且真实履行）。

根因：**Gate 验证的是惯用语（特定字符串），不是属性（JS 失败时语义
内容是否可达）**——等于用代码隐性规定 Huashu 的实现词汇，与"不教
Huashu 做事"原则直接冲突。

重构（仅 postprocess 域内，30 号零改动）：`classify_fallback_idioms()`
按属性认定安全证明——V1 `html.no-js` 配对兜底 / V1b 隐藏规则本身
条件化于 JS 状态 / V2 同类无条件可见规则 / V3 reduced-motion；新
失败码 `HIDDEN_CONTENT_WITHOUT_JS_FAILURE_FALLBACK`（真无兜底）。
反例开发中发现并修复复合选择器误判 bug（`.b-in.on{opacity:1}` 不
构成静态证明，`_selector_targets_cls()` 排除）。

验证矩阵：GTM.html（no-js 惯用语）FAIL→**PASS**；新 report.html /
fixture / editable 保持 PASS；真不安全反例保持 FAIL。基线新增
`motion_gate_idiom_neutral` 断言（两惯用语 PASS + 反例 FAIL），防
回归。净效果：安全属性不变，通过路径从 1 条惯用语变 4 种证明方式，
动效写法自由度解除限制。

