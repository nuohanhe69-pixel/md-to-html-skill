# Post-Generation Editor Extension — Delivery Gate V2.0 / Editor Runtime V2.0

本目录只在 V2.9 Report / Presentation / QA 全部完成后执行。

## Required delivery finalizer

```bash
python postprocess/scripts/finalize_delivery.py \
  --output-root /absolute/path/to/output-root
```

`finalize_delivery.py` 是最终交付唯一入口；它负责检查 / 执行 Dispatcher、验证 Editable 指纹，并在成功后确定性更新 `run-state.json` 的 `delivery_gate_status=PASS` 与 `current_status=DELIVERED`。

执行方式为单一确定路径：Main Agent 在 Generation Boundary 后直接执行 Finalizer（主上下文 + 确定性脚本平面，无 subagent 派发模式）。

Mandatory static validation 不依赖浏览器；Runtime Render QA 为 best-effort 且有超时，不会阻塞可编辑副本的生成。

## Editor V2.0：编译期结构化标注

V1.x 在浏览器里运行时"盲发现"可编辑节点（只能编辑纯文本叶节点，富段落不可
编辑，motion 未触发的元素既看不见也改不到）。V2.0 改为**注入前**由
`inject_editor.py` 完整解析 base DOM 并标注：

- 富文本段落（含 strong/a/span 行内标记）可编辑；
- 所有 `data-du-id` 模块可选中，可调排版（间距/宽度/布局/背景/边框），
  显式标记 `data-edit-movable` 的模块可调整顺序；
- motion-reveal 隐藏元素标注 `data-motion-reveal`，编辑模式强制可见；
- locked 内容经 Human Override 确认后可改，全部修改进内嵌台账
  （`human-edit-ledger`），跨会话可撤销/重做/恢复，永不回写上游。

完整契约见 `references/editor-contract.md`。

### 依赖

仅 python3 标准库（htmldom.py 为内置迷你 DOM，无 bs4/网络/LLM 依赖）。

### 可选 authority map

`<output-root>/workspace/editable-authority-map.json` 存在时自动加载：

```json
{
  "schema_version": "1.0",
  "targets": [
    {"du": "DU002", "contains_text": "关系 R01", "authority": "locked-fact",
     "obligation_refs": ["C002.R01"]}
  ],
  "modules": [
    {"selector": "section[data-du-id='DU003']", "movable": true}
  ]
}
```

`targets` 支持按 `selector` 或 `du`+`contains_text` 定位；`modules` 支持
`selector` 或 `du`。选择器子集：`tag`、`#id`、`.class`、`[attr]`、
`[attr='value']`。

### Motion Visibility Safety

`validate_motion_visibility_safety.py` 对 base 与 editable 双侧静态校验：
大型语义容器不得处于无条件 motion 隐藏、`prefers-reduced-motion` 回退必须
存在、编辑模式必须有强制可见覆盖。base 校验失败 = 交付 BLOCKED（生成期
QA 应在此前拦截该风险）。
