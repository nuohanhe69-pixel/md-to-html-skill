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
