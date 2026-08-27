# Semantic Obligation & Evidence Contract

本文件定义：如何把 `Source Inventory → Transformation Map → Complete DIP → Coverage QA` 从“只有编号 / 去向 / PASS 声明的控制面”升级为真正携带 Content Evidence 的可审计数据链，同时避免把 Raw Markdown 在中间文件中重复复制多遍。

核心原则：

> **压缩原始表达，不压缩独立语义义务。**

> **Cxxx / Txx 的 ID 存在，不等于 Coverage 已经成立。Coverage 必须由具体 Content Evidence 证明。**

---

# 1、Semantic Obligation 是“不丢失”的最小审计单位

一个 Cxxx / Txx 往往包含多个不能无声消失的信息，因此不能只用 `C036 exists` / `T04 exists` 判断完整性。

每个 Source Unit 必须抽取必要的 `Semantic Obligation Set`。支持以下类型：

```text
EXACT_FACT              精确事实：数字、比例、年龄、日期、价格、车型、人名、职业、地点、参数、优先级、来源等
SEMANTIC_POINT          独立观点 / 特征 / 解释 / 业务意义
REQUIRED_RELATIONSHIP   因果、对比、先后、依赖、冲突、映射等关系
REQUIRED_DIMENSION      一个分析维度 / Persona 维度 / Table 列维度
REQUIRED_ENTRY          一个不可因压缩而消失的独立对象 / 行 / 行动项 / 风险项 / 结论项
CONCLUSION              独立结论
QUALIFIER               限定条件、置信度、版本 / 口径说明
EVIDENCE                证据来源 / 支撑关系
ACTION                  独立行动建议 / 执行动作
RISK_OPPORTUNITY        风险 / 机会节点
```

推荐子 ID：

```text
C036.F01   Exact Fact
C036.S01   Semantic Point
C036.R01   Required Relationship
C036.Q01   Qualifier

T04.D01    Required Dimension
T04.E01    Required Entry
T04.F01    Exact Fact
```

不要求逐句编号；只对具有独立事实、分析、决策或关系价值的内容建立 Obligation。

---

# 2、四份文件各自只保存一种信息，禁止复制链

正确关系：

```text
Raw Markdown
↓
Source Content Inventory
  只保存：Source Anchor + Semantic Obligations
↓
Semantic Transformation Map
  只保存：Obligation → Transformation Action → Transformed Result
↓
Complete Design Input Package
  只保存：最终 Render-ready Display Content + Obligation Refs
↓
Coverage Evidence Ledger
  只保存：Expected Obligation → DIP Evidence → Final Output Evidence → PASS / FAIL
```

禁止：

```text
Inventory 复制整段 Raw Markdown
Transformation Map 再复制整段 Raw Markdown
DIP 再复制整段 Raw Markdown
Coverage QA 再复制整份 DIP
```

四份文件通过 ID 引用形成证据链，而不是形成四份内容副本。

---

# 3、Source Content Inventory：从“目录”升级为 Obligation Inventory

错误：

```text
C036 = 黄皓 Persona
```

这只能证明“有一个 Persona”，不能保护 Persona 内部事实。

正确示例：

```yaml
C036:
  type: PERSONA
  source_anchor:
    heading: "画像卡1：技术鉴赏型精英 黄皓"

  obligations:
    exact_facts:
      F01: {field: age, value: 35}
      F02: {field: city, value: 上海}
      F03: {field: occupation, value: 互联网公司技术总监}
      F04: {field: previous_car, value: 宝马3系}
      F05: {field: family, value: 已婚一娃}
      F06: {field: income, value: 家庭年收入40万+}

    semantic_points:
      S01: 技术逻辑驱动选车
      S02: 驾控质感不能妥协
      S03: 不为品牌虚荣付费
      S04: 信任硬核技术拆解与真实车主深度内容

    required_relationships:
      R01: BBA换购 → 技术跃迁需求 → LS6驾控价值
      R02: 家庭责任 ↔ 驾驶乐趣
```

该结构比 Raw Markdown 短，但独立语义义务没有消失。

---

# 4、Inventory Completeness Gate：防止“一开始就漏登记”

Coverage 不能只计算：

```text
已登记 Cxxx 中有去向的数量 / 已登记 Cxxx 总数
```

因为如果 Inventory 一开始漏掉 Source 内容，仍可能出现“85 / 85 = 100%”的假 Coverage。

Inventory 必须额外建立 Source Structure Baseline，至少核对：

```text
H1 / H2 / H3 主结构
显式编号的 Top N / Step N / Insight N
所有 Source Table
所有 Persona
所有独立行动 / 风险 / 机会 / 结论列表
所有附录 / 遗留问题 / 置信度 / 矛盾数据模块
```

例如 Source 写明：

```text
Top 7 洞察
```

则 Inventory 必须出现 7 个对应子单元，或明确记录哪些洞察被合并到哪个 Cxxx；不能只登记 6 个然后按 `6 / 6` 宣布 100%。

Gate：

```text
Inventory Structural Coverage = 100%
Unregistered Declared Item = 0
Unregistered Source Table = 0
```

未通过禁止进入 Transformation。

---

# 5、Source Table：Txx 本身不是最小 Coverage 单位

例如 T04 原表有 5 个独立优势项。

错误：

```text
T04 → Product Cards
PASS
```

正确：

```yaml
T04:
  required_dimensions:
    D01: 优势项
    D02: 具体表现
    D03: 传播价值

  required_entries:
    E01: 线控转向
    E02: 后轮转向±9°
    E03: VMC整车运动控制
    E04: 电弹前备箱
    E05: 售后智能云台相机
```

允许：

```text
5 行 Source Table
→ 3 张核心技术 Card
+ 2 张体验 Feature Card
```

但必须：

```text
T04 Entry Coverage = 5 / 5
T04 Required Dimension Coverage = 3 / 3
```

仅出现 `T04` 字样、HTML 注释、`data-source-table-id="T04"` 或一个 Destination，不构成完整 Coverage Evidence。

---

# 6、Semantic Transformation Map：必须记录“转换结果”，不能只记录“视觉计划”

错误：

```text
C036 → Persona Dossier
T02 → Timeline
```

这只是 Visual Routing。

Transformation Map 必须针对 Obligation 记录：

```text
KEEP_EXACT
COMPRESS_LABEL
SUMMARIZE
MERGE
SPLIT
STRUCTURE
VISUALIZE
ROUTE
```

并记录转换后的实际输出。

例如：

```yaml
C036:
  F01:
    action: KEEP_EXACT
    output: "35岁"

  F03:
    action: COMPRESS_LABEL
    source_meaning: "互联网公司技术总监"
    output: "互联网技术总监"

  S01:
    action: SUMMARIZE
    output: "技术逻辑驱动的理性选车者"

  R02:
    action: VISUALIZE
    output: "家庭责任 ↔ 驾驶乐趣"
```

Transformation Map 的职责是证明：

```text
每一个 Source Obligation
↓
经过什么 Transformation
↓
最终具体变成什么
```

---

# 7、Transformation 删除边界

允许删除：

```text
重复措辞
同义重复
修辞
赘述
不新增语义的信息
```

禁止删除：

```text
独立事实
独立维度
独立行动
独立风险 / 机会
独立 Persona 特征
独立流程节点
独立证据
独立结论
Required Relationship
重要限定条件
```

如果某个 Source Obligation 被 MERGE，必须指出合并到哪个 Transformed Result；不能以“已总结”为由无声消失。

---

# 8、Source → DIP Fidelity Gate：DIP 锁定前必须先证明无损

正确：

```text
Source Obligations
↓
Transformation Map
↓
Render-ready DIP
↓
Source → DIP Fidelity Gate
↓
PASS
↓
LOCK
```

禁止：

```text
Transformation
↓
先写 LOCKED
↓
再假设 DIP 完整
```

锁前至少满足：

```text
Inventory Structural Coverage = 100%
Source Obligation → Transformation Result Coverage = 100%
Source Obligation → DIP Coverage = 100%
Exact Fact Fidelity = 100%
Required Relationship Coverage = 100%
Source Table Entry Coverage = 100%
Source Table Required Dimension Coverage = 100%
Unresolved Content Mutation = 0
```

未通过：

```text
DESIGN_INPUT_LOCKED = FORBIDDEN
```

---

# 9、Complete DIP：必须包含 Data Plane，Manifest-only DIP 一律 FAIL

Complete DIP 可以包含 Manifest，但不能只有 Manifest。

错误：

```text
document_title
semantic_unit_count = 50
table_count = 27
status = LOCKED
```

这只是 `DIP Manifest`，不是 Complete Design Input Package。

真正 DIP 必须包含实际 Render-ready Display Units，例如：

```yaml
DU036:
  source_units: [C036]
  component_role: PERSONA_DOSSIER

  display_content:
    identity:
      name: 黄皓
      age: 35
      city: 上海
      role: 互联网技术总监
      previous_car: 宝马3系
      family: 已婚一娃

    headline: "用技术逻辑选车，被后轮转向一把掉头征服的理性驾控派"

    traits:
      - 技术鉴赏
      - 品质溢价
      - 驾控不妥协

    value_conflict:
      left: 家庭责任
      right: 驾驶乐趣

  obligation_refs:
    - C036.F01
    - C036.F02
    - C036.F03
    - C036.F04
    - C036.F05
    - C036.S01
    - C036.R02

  mutation_policy:
    content: IMMUTABLE
    layout: FREE
```

DIP 的内容层必须能够脱离 Raw Markdown直接被 Renderer 使用；如果下游仍需要重新读取 Raw Markdown 才能写页面，说明 DIP 不 Render-ready。

---

# 10、DIP Content Lock：锁内容，不锁一个 boolean

`run-state.json` 不能只有：

```json
"complete_design_input_locked": true
```

还必须记录：

```text
DIP Path
DIP Content Hash
Inventory Hash
Transformation Map Hash
Semantic Obligation Count
Exact Fact Count
Required Relationship Count
Source Table Required Entry Count
Source → DIP Fidelity Gate Status
```

示例：

```json
{
  "complete_design_input": {
    "path": "workspace/complete-design-input-package.md",
    "status": "LOCKED",
    "content_hash": "sha256:...",
    "semantic_obligation_count": 214,
    "exact_fact_count": 83,
    "required_relationship_count": 41,
    "source_table_entry_count": 96,
    "source_to_dip_fidelity": "PASS"
  }
}
```

进入 Prototype、用户选择后恢复、Final Generation 前都必须重新核对 DIP Hash。

Hash 不一致：

```text
DIP_MUTATED_AFTER_LOCK = FAIL
```

---

# 11、Huashu 是 Locked DIP 的纯消费者

正式业务内容关系：

```text
md-to-html-report
= WHAT TO SAY

Complete DIP
= IMMUTABLE CONTENT DATA PLANE

huashu-design
= HOW TO SHOW IT
```

Huashu 不拥有业务内容修改权。

禁止 Huashu：

```text
自行改写 Display Content
自行把 35 岁改成 32 岁
自行改变车型 / 价格 / 优先级
自行删掉一个行动项 / 表格 Entry / Persona 维度
因为版面放不下就自行压缩业务内容
重新总结 DIP
```

如果设计密度冲突：

```text
Huashu → CONTENT_DENSITY_CONFLICT
↓
父 Skill 优先通过拆组件 / 加 Section / 加 Slide / Main+Appendix 路由解决
```

不能由 Huashu 自行删内容。

用户可见业务文本必须来自 Locked DIP；Huashu 只能改变 Layout / Composition / Visual Form / Motion。

---

# 12、Direction Comparison Package 只能抽取 DIP，不得重新创作业务内容

Direction Comparison Package 必须保存：

```text
DU IDs
Obligation Refs
Locked Display Content Snapshot / References
```

禁止：

```text
从 Raw Markdown 重新总结 Prototype 文案
把 DIP 的 35岁重新写成32岁
把 P0/P0/P1 重新整理成 P0/P1/P2
把“技术验证”自行改成“技术爆破”并改变业务含义
```

Prototype A / B / C 可改变设计表达，不能改变 Comparison Package 的 Locked Content。

---

# 13、Final HTML / Slide 必须携带 Traceability Hook

report.html 的语义承载体（section 级组件）必须写入：

```html
<section
  data-du-id="DU036"
  data-obligation-refs="C036.F01 C036.F02 C036.S01 C036.R02">
```

合并/拆分语义单元时：DU 拆进多个视觉步骤 → hook 写在共同容器上；
多个 DU 融为一个视觉模块 → `data-obligation-refs` 多值引用。纯装饰元素
（不承载 DU 的分隔线/背景/装饰图形）豁免。

Presentation Slide 遵循 22 号完整性契约，不在此列。

Source Table 必须保留：

```html
data-source-table-id="T04"
```

命名空间纪律（Artifact Boundary）：生成侧只使用上述 MUST 属性；
class / style / id / aria-* 与自定义视觉语义属性属于设计平面自由区；
交付平面私有 namespace（`data-edit-*` / `data-motion-reveal` /
`data-he-*` / `data-human-edit-*` / `human-edit-*` / `.he-*` 前缀）禁止
出现在 report.html——它们只能由 PostProcess 注入（契约唯一源：
`postprocess/scripts/artifact_namespace.py`，人读版
`postprocess/references/editor-contract.md` §Artifact Boundary）。

Traceability Hook 是 QA 定位辅助，不等于 Coverage Evidence 本身；但
`data-du-id` 同时是下游编辑器模块系统与 Delivery Gate 哨兵的结构性依赖，
缺失会被 `module_capability_present` 检查捕获。

HTML 注释中的：

```html
<!-- T18, T19, T20 -->
```

不能作为 Coverage PASS 证据。

---

# 14、Coverage Evidence Ledger：最终只保存 Expected → Evidence

新增持久化文件：

```text
workspace/coverage-evidence-ledger.md
```

它在 DIP 锁前先记录 Source → DIP Evidence；最终生成后再补 Report / Presentation Evidence。

例如 Exact Fact：

```yaml
C036.F01:
  expected: 35
  dip_evidence: DU036.identity.age = 35
  report_evidence:
    selector: "#persona-huanghao [data-field='age']"
    actual: "35岁"
  presentation_evidence:
    slide: "11-personas"
    actual: "35岁"
  result: PASS
```

例如 Semantic Point：

```yaml
C036.S01:
  expected_meaning: 技术逻辑驱动选车
  dip_evidence: DU036.traits / headline
  report_evidence: DU036 Persona Dossier
  presentation_evidence: Persona Slide
  meaning_preserved: YES
  result: PASS
```

Ledger 不复制整段 DIP，只记录引用、实际 Evidence 和结果。

---

# 15、Evidence-backed Coverage Gate

最终 Coverage 必须按 Obligation 证明，禁止只按 Unit ID / Destination 名称证明。

必须满足：

```text
Inventory Structural Coverage = 100%
Semantic Obligation Coverage = 100%
Exact Fact Fidelity = 100%
Required Relationship Coverage = 100%
Source Table Entry Coverage = 100%
Source Table Required Dimension Coverage = 100%
Source → DIP Evidence Coverage = 100%
DIP → Report Evidence Coverage = 100%
DIP → Presentation Evidence Coverage = 100%
DIP Hash Integrity = PASS
Missing Obligation = 0
Unproven Obligation = 0
```

以下都不能单独构成 PASS：

```text
C036 有一个 Destination
T19 出现在 HTML 注释
Manifest 写 T09-T14 → A02
页面标题写“Top 7”
生成器自己写“Coverage 100% PASS”
```

> **Coverage 必须由证据推出，不能由生成者声明。**

---

# 16、回滚边界

如果 Final Evidence 发现：

```text
DIP 正确
但 HTML / Slide 丢了内容
```

只回滚 Final Rendering / Layout。

如果发现：

```text
DIP 已经漏了 Source Obligation
或 Exact Fact 在 DIP 中已变异
```

必须回滚到 Content Transformation，生成新的 DIP 版本并重新执行 Source → DIP Fidelity Gate；不得在 HTML 端偷偷补一条来伪造 Coverage。

---

# 17、最终目标

正确系统不是：

```text
50 C IDs
+ 27 T IDs
+ LOCKED = true
+ Destination Names
= 100% Coverage
```

而是：

```text
Source
↓
Semantic Obligations
↓
Transformation Evidence
↓
Render-ready DIP Data Plane
↓
Content Hash Lock
↓
Huashu Pure Consumption
↓
Final Output Evidence
↓
100% Coverage
```

这使系统同时保持：

```text
不是 Markdown 换皮
+
可以高强度总结 / 合并 / 重组 / 可视化
+
独立事实 / 维度 / 关系 / 结论一个不无声消失
```

# 18、V2.9 Design Intent 与 Semantic Carrier

Design Intent 只引用 Semantic Obligation，不拥有 Semantic Obligation。

因此：

```text
Design Intent Ref != Coverage Evidence
```

Coverage 仍然只能由：

```text
DIP → Final Rendered Evidence
```

证明。

Design Intent 必须保持：

```text
Obligation Ref Coverage = 100%
Scope Mutation = 0
```

对于 Final Output，可为 Obligation 定义：

```text
Primary Carrier
Supporting Carrier(s)
```

用于减少重复渲染，同时保持 Evidence-backed Coverage。

完整规则见：

```text
references/27-design-intent-creative-brief-contract.md
references/32-semantic-carrier-and-responsive-preservation.md
```
