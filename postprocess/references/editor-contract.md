# Human Editor V1.0 — Deterministic Post-Generation Contract

## Architecture

```text
V2.9 Main Agent
↓
final report.html + V2.9 QA complete
↓
Artifact Boundary
↓
fresh PostProcess Subagent
↓
fixed run_postprocess.py
↓
report-editable.html
```

Editor 不参与 Generation Plane。

## Delivery Lifecycle

```text
GENERATION_COMPLETE
↓
POSTPROCESS_REQUIRED
↓
Required Delivery Finalizer（finalize_delivery.py，唯一入口）
↓
DELIVERY_READY
↓
DELIVERED（delivery_gate_status = PASS）
```

## Non-Interference

```text
Base report SHA before == after
Base report 中 HE namespace = 0
PostProcess 不调用 Huashu / LLM
PostProcess 不修改 Motion / Navigation / Responsive
```

## Namespace

仅使用：

```text
HE_POSTPROCESS_*
he-editor-*
data-he-*
.he-*
```

V2.9 Base Report 中上述 Editor namespace 必须为 0。

## Runtime Isolation

- Toolbar / Inspector 位于 Shadow DOM。
- Editor CSS 只进入 Shadow DOM，不作为全局 stylesheet 生效。
- Browse Mode 不发现/标记正文编辑节点；只有用户点击“编辑”后才执行 runtime discovery。
- 不允许 Editor 控制 Report Motion / Scroll / Navigation。
- 复杂父容器不整体 `contenteditable`；仅安全文本叶节点直接编辑。

## Artifact Rules

```text
report.html
= V2.9 原始最终作品，永不修改

report-editable.html
= report.html 的确定性派生副本 + 固定 Editor Runtime

report-published.html
= 用户人工修改后的干净导出版（由浏览器 Editor 导出）
```

## Validation Gates

1. Base SHA before/after identical.
2. Base contains no HE namespace.
3. Initial editable artifact, after stripping the injected HE block, is byte-identical to Base.
4. Editor JS syntax passes when Node is available.
5. Editor source contains no known Report Motion coupling selectors/APIs.
6. Runtime smoke test passes when Playwright/Chromium are available.
