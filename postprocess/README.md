# Post-Generation Editor Extension — Delivery Gate V1.2 / Editor Runtime V1.1

本目录只在 V2.9 Report / Presentation / QA 全部完成后执行。

## Required delivery finalizer

```bash
python postprocess/scripts/finalize_delivery.py \
  --output-root /absolute/path/to/output-root \
  --dispatch-mode direct-fallback
```

`finalize_delivery.py` 是最终交付唯一入口；它负责检查 / 执行 Dispatcher、验证 Editable 指纹，并在成功后确定性更新 `run-state.json` 的 `delivery_gate_status=PASS` 与 `current_status=DELIVERED`。

平台原生 Subagent 可用时，优先让 fresh Subagent 执行同一命令，并把 `--dispatch-mode` 设为 `subagent`。

**Subagent 是隔离增强，不是交付成功的单点依赖。** 如果当前 Skill Runtime 没有真正暴露可调用的 Subagent 接口，Main Agent 必须在 Generation Boundary 后直接执行 Finalizer，不能因此省略 Editable Artifact。

Mandatory static validation 不依赖浏览器；Runtime Render QA 为 best-effort 且有超时，不会阻塞可编辑副本的生成。
