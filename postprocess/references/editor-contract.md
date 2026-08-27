# Human Editor V2.0 — Compile-Time Annotated Editable Delivery Contract

> Lineage: 架构移植自 `md-to-html-report-v3.0.1-motion-visibility-safety`
> （inject_editor.py 编译期标注 + motion 可见性安全 + 权限/台账治理），
> 以标准库迷你 DOM（htmldom.py）重写，保持确定性交付子系统零第三方依赖。
> Editor V1.x 的"运行时盲发现 + 字节级 strip 校验"路线已废弃，原因见 HANDOVER §7。

## Architecture

```text
V2.9 Main Agent
↓
final report.html + V2.9 QA complete
↓
Artifact Boundary
↓
fresh PostProcess Subagent（或 direct fallback）
↓
inject_editor.py —— 编译期结构化标注
  parse base DOM → 标注可编辑元素/模块/动效/权限 → 追加运行时
↓
report-editable.html（base 的结构级派生副本 + 人工编辑运行时）
```

Editor 不参与 Generation Plane。注入器不重排、不改写、不删除任何 base
节点——只做"加属性 + 末尾追加"。

## Artifact Boundary（report.html 接口契约）

report.html 是 Generation 平面与 Delivery 平面的接口。接口语法的唯一
定义源是 `postprocess/scripts/artifact_namespace.py`（机器可读）+ 本节
（人读）；注入器与全部校验器均从该模块 import，**任何一侧都不再维护
私有清单**。

```text
MUST（生成侧必须写，语义承载体上）
  data-du-id / data-obligation-refs / data-source-table-id
  （references/24 §13 定义；编辑器模块系统与 QA 锚点结构性依赖它）

FREE（Huashu 设计平面自由区）
  class / style / id / aria-* / 自定义视觉语义属性
  PostProcess 永不读取、改写或剥离此区

FORBIDDEN（交付平面私有 namespace，base 必须为零）
  data-edit-* / data-motion-reveal / data-he-* / data-human-edit-*
  id: he-editor-style / he-editor-script / human-edit-*
  class 前缀: .he-*
  它们只能由 PostProcess 注入，且干净导出时全部剥离
```

执法（全部在 Delivery Gate，不在生成侧新增 QA）：

- base 出现任何 FORBIDDEN 项 → 注入器拒绝注入 + 校验 BLOCKED
  （PostProcess 从不"清洗修复"base——发现污染即上报，修复责任在上游）；
- base 存在 `data-du-id` 承载体但 editable 模块数为 0 → FAIL
  （模块能力静默丢失哨兵，抓契约/注入器命名漂移）。

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

## Compile-Time Annotation（V2.0 核心）

| 标注 | 规则 |
|---|---|
| 文本元素 | `data-edit-id = <最近 data-du-id>.<tag>.<序号>`（如 `DU002.p.003`）。可编辑判定 = 排除**块级**子元素；V1.x 的"零子元素纯叶节点"限制废除——带行内标记（strong/a/span）的富段落照常可编辑。`span` 仅在无子元素且 ≤180 字符时可编辑 |
| 模块 | 所有 `data-du-id` 承载体 → `data-edit-module-id`；默认 `data-edit-movable="false"` |
| 权限 | `data-edit-authority`（human-editable / locked-fact / …）+ `data-edit-obligation-refs`（桥接 M3 obligation 追溯）。来源：可选 authority map，发现路径 `<output-root>/workspace/editable-authority-map.json` |
| 动效可见性 | 扫 base CSS 检测 motion-reveal 隐藏类（rv/reveal/b-in 等）→ 元素标 `data-motion-reveal="true"`；编辑模式 CSS 强制全部可见 |

## Namespace

```text
data-edit-*            （注入标注）
data-motion-reveal     （动效可见性标注）
data-he-runtime-ui     （运行时 UI 节点）
human-edit-*           （内嵌 base-state / ledger / meta script 节点）
he-editor-style / he-editor-script
.he-*                  （运行时样式类）
```

V2.9 Base Report 中上述 namespace 必须为 0；注入器在发现既有标记时拒绝
重复注入。

## Non-Interference

```text
Base report SHA before == after（字节级，硬不变量）
Base report 中 editor namespace = 0
结构级等价：parse(editable) − 注入属性 − artifact 节点 == parse(base)
PostProcess 不调用 Huashu / LLM
PostProcess 不修改 Motion / Navigation / Responsive（编辑模式 CSS 仅在
body.he-editing 状态下强制注入标注的元素可见，不触碰 base）
```

V1.x 用"剥离 HE block 后字节相同"证明非干扰；V2.0 改为结构级证明——
换来编译期全量标注与完整编辑能力，代价是证明弱一档（解析器归一化后比对
而非逐字节）。

## Runtime Isolation

- 运行时 UI（launcher/toolbar/panel/confirm/module 标签）全部带
  `data-he-runtime-ui`，导出时移除。
- 样式全部 `.he-*` / `#he-*` 作用域 + `body.he-editing` 状态；浏览态除
  launcher 悬浮按钮外零视觉差异（runtime browse equivalence 校验）。
- `contenteditable` 仅在编辑模式开启；浏览态不可编辑。
- 编辑模式强制 `[data-motion-reveal]` 元素可见（`opacity:1 !important`），
  解决"中间页面大面积隐藏"的编辑盲区。
- Editor JS 不含网络/AI/LLM 模式，不驱动报告 motion（无 IntersectionObserver
  等耦合）。

## Authority / Human Override

- locked 内容（locked-fact 等）人工仍可改，但首次修改前弹 Human Override
  确认；台账记录 `scope=HUMAN_OVERRIDE`（元素）/ `HOW_OVERRIDE`（模块样式）/
  `NARRATIVE_ORDER_OVERRIDE`（模块移动）。
- 修改只进交付产物（浏览器导出），**不回写** Markdown / Source Inventory /
  DIP / Design Intent 等上游材料。
- 台账 `human-edit-ledger` 内嵌于文档，跨会话持久；`ai_editing=DISABLED`、
  `source_backflow=FORBIDDEN`。

## Artifact Rules

```text
report.html
= V2.9 原始最终作品，永不修改（SHA 冻结）

report-editable.html
= 编译期标注派生副本 + 编辑运行时 + 内嵌 base-state/ledger/meta

浏览器导出（用户操作）：
report-edited-<stamp>.html     可继续编辑的版本（含台账）
report-published-<stamp>.html  干净发布版（剥离全部 editor namespace）
human-edit-history-<stamp>.json 人工修改台账
```

## Validation Gates

1. Base SHA before/after identical（字节级）。
2. Base contains no editor namespace。
3. **结构级等价**：剥离全部注入属性与 artifact 节点后，editable 的 DOM 树
   与 base 完全一致（含文本节点、属性、顺序）。
4. `data-edit-id` / `data-edit-module-id` 全局唯一。
5. Ledger：`ai_editing=DISABLED`、`source_backflow=FORBIDDEN`。
6. Editor JS：无网络/AI/motion 耦合模式；node --check（可用时）。
7. **Motion Visibility Safety**：base 与 editable 双侧校验——大型语义容器
   不可处于无条件 motion 隐藏、reduced-motion 回退存在、编辑模式强制可见
   覆盖存在。
8. Runtime smoke（best-effort，playwright 可用时）：launcher 开启编辑、元素
   数量与 meta 一致、面板改字生效、undo/redo 正确、退出恢复浏览态。
