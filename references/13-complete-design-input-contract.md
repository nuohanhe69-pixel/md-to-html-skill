# Complete Design Input Package Contract

本文件是 `Complete Design Input Package` 的唯一正式定义。

---

# 1、唯一正式业务设计输入

正确链路：

```text
Raw Markdown
↓
完整读取与语义理解
↓
Source Content Inventory
↓
C001 ~ Cxxx / T01 ~ TN
↓
完整 Content Transformation
↓
Semantic Content Transformation Map
↓
Complete Design Input Package
```

它必须是 render-ready Artifact，并真实落盘。

---

# 2、Raw Markdown 的角色

只允许：

```text
Source of Truth
Traceability
Coverage 回查
Information Fidelity 回查
QA 证据
```

不是：

```text
Huashu 的最终视觉 Brief 正文
Report Mode 的直接渲染内容
Presentation Mode 的直接渲染内容
```

---

# 3、Package 必须包含真实 Data Plane

至少：

```text
Document Identity
Design Context Profile / Reference Design Profile
Render-ready Display Units（DU001 ~ DUxxx）
Cxxx / Txx Source References
Transformed Display Content
Semantic Obligation References
Immutable / Exact Facts
Required Relationships
Semantic Destination
Preferred Visual Form
Design Constraints
Traceability Source
Mutation Policy
```

`Complete Design Input Package` 可以带 Manifest，但禁止只有：

```text
document_title
semantic_unit_count
table_count
status = LOCKED
```

这种文件只能叫 `DIP Manifest`，不能作为 Complete DIP。

硬规则：

```text
Manifest-only DIP = FAIL
DIP Data Plane Missing = FAIL
下游必须重新读 Raw Markdown 才能写业务文案 = NOT RENDER-READY
```

详细 render-ready 字段与 Obligation 数据模型见：

```text
references/17-render-ready-transformation-boundary.md
references/24-semantic-obligation-and-evidence-contract.md
```

---

# 4、“不丢失”的真实含义

当本 Skill 写：

```text
input 不丢失
内容完整
Coverage = 100%
```

统一指 Complete Design Input Package 中的：

```text
Cxxx
Txx
Immutable Facts
Required Relationships
Semantic Requirements
关键结论
关键维度
关键流程节点
关键时间 / 因果 / 对比关系
```

全部有最终承接。

不要求：

```text
原 Markdown 每一句原话都保留
原 Markdown 每个长段落都原样保留
原 Markdown 原始排版保留
```

---

# 5、禁止“假 Coverage”

以下一律 FAIL：

```text
Raw Markdown → Direct HTML Rendering
未经 Transformation 的长段落直接复制进 Report
未经 Transformation 的长段落直接复制进 Slide
为了 Cxxx Coverage = 100% 把原文全部重新塞回页面
把表格原文机械复制而不执行 Source Table Transformation
```

出现上述情况：

```text
Long Content Transformation QA = FAIL
```

---

# 6、Prototype 与最终双模式不在此重复定义

Prototype：

```text
references/15-direction-prototype-contract.md
```

Report / Presentation：

```text
references/12-display-mode-and-presentation.md
```

本文件只定义它们共同消费的业务内容契约。

---

# 7、落盘、Source → DIP Proof 与 Content Lock

必须：

```text
完成全部 Transformation
↓
写入 workspace/complete-design-input-package.md（含真实 Data Plane）
↓
写入 / 更新 workspace/coverage-evidence-ledger.md
↓
执行 Source → DIP Fidelity Gate
↓
计算 DIP Content Hash
↓
Transformation Lock Gate
↓
DESIGN_INPUT_LOCKED
```

禁止只写：

```text
complete_design_input_locked = true
```

却没有内容 Hash、Obligation Count 与 Fidelity PASS 证据。

完整状态规则见：

```text
references/16-run-state-and-persistence.md
references/24-semantic-obligation-and-evidence-contract.md
```

---

# 8、最终判断标准

正确：

```text
原始 Markdown 信息
↓
100% 理解
↓
100% 语义覆盖
↓
100% Transformation
↓
更短 / 更结构化 / 更可视化 / 更易读
↓
Complete Design Input Package
↓
Design / Presentation Pipeline
```

错误：

```text
Markdown 原文
↓
直接复制
↓
HTML 外壳
```

# 9、V2.9 DIP → Design Intent 边界

Complete DIP Lock 后：

```text
DIP = WHAT
Design Intent = WHY
```

Design Intent 不得成为第二份内容工程结果。

DIP 必须额外明确：

```text
Business Priority（如 Source 声明）
Required Relationships
Conflict / Unknown Obligations
Mutation Policy
```

以便下游区分：

```text
视觉强调级别
!=
业务优先级
```

完整规则见：

```text
references/26-what-why-how-authority-model.md
references/27-design-intent-creative-brief-contract.md
```

# 10、V2.9 Preferred Visual Form 兼容规则

旧版本 DIP 中如存在 `Preferred Visual Form`：

```text
Preferred Visual Form = ADVISORY ONLY
```

它不能：

```text
锁死组件
锁死 Chart Type
锁死 Layout
锁死 Scrollytelling
```

V2.9 推荐将其改名理解为：

```text
Visual Affordance Hint
```

真正 HOW 决策属于 Huashu，见：

```text
references/26-what-why-how-authority-model.md
references/28-visual-grammar-exploration-library.md
```
