# Examples & Anti-patterns — 保留示例库

本文件用于保存总控文件减肥时不应丢失的示例与反例。

重要：

> **V2.3 无损重构不减少既有 Reference 文件中的示例。原 Owner 文件里的例子继续原位保留；这里只承接从旧 `SKILL.md` 移出的示例。**

---

# 1、Semantic Coverage 示例

```text
章节 A
├─ 关键观点 1
├─ 关键观点 2
├─ 表格 1
└─ 结论

章节 B
├─ 人物画像
│  ├─ 消费观
│  ├─ 价值冲突
│  ├─ 决策路径
│  └─ 风险节点
├─ 表格 2
└─ 关键洞察
```

错误：只保留最显眼的结论，人物维度、风险节点和表格无声消失。

错误：为了 100% Coverage，把整份 Markdown 原样搬进 HTML。

正确：所有有价值语义都有 Transformation Destination，但表达形态可以被总结、合并、重组和可视化。

---

# 2、Prototype 选择后的正确做法

```text
三个 Prototype
!=
三个完整 Report

用户选定 Prototype B
!=
把 Prototype B 直接扩写几段就交付

正确做法：
Selected Direction B
+
Selected Design System Snapshot B
+
完整 Complete Design Input Package
↓
首次完整构建 Report Mode
+
首次完整构建 Presentation Mode
```

---

# 3、外部 Skill 手动安装示例

Huashu：

```bash
git clone --depth 1 https://github.com/alchaincyf/huashu-design.git ~/.codex/skills/huashu-design
# 或项目级
# git clone --depth 1 https://github.com/alchaincyf/huashu-design.git .codex/skills/huashu-design
```

frontend-visual-qa：

```bash
git clone --depth 1 https://github.com/daymade/claude-code-skills.git /tmp/daymade-claude-code-skills
```

然后完整复制：

```text
/tmp/daymade-claude-code-skills/frontend-visual-qa/
```

到当前运行环境支持的 Skill 目录。

---

# 4、Presentation 容量示例

错误：

```text
为了让 Main Deck 变短
→ 删除 Source Table
→ 删除次级分析维度
```

正确：

```text
T04
→ Main Deck：Overview Chart + 3 Key Findings
→ Appendix：Detailed Table + Full Notes
```

以及：

```text
Slide 12：T04 Overview Chart
Slide 13：T04 Detailed Table
Slide 14：T04 Key Findings
```

---

# 5、Reviewer 分工示例

```text
Render QA = PASS
Design Critique = FAIL
```

仍然不能交付。

反过来：

```text
Design Critique = PASS
Render QA = FAIL
```

同样不能交付。


---

# 99、V2.2 迁移时自动保留的显式示例

## Preserved Example 1 — from SKILL.md:516

Codex 环境若需要手动安装，可把完整仓库放入 Codex 可识别的 Skill 目录，例如：

```text
~/.codex/skills/huashu-design/
.codex/skills/huashu-design/
~/.agents/skills/huashu-design/
.agents/skills/huashu-design/
```

## Preserved Example 2 — from SKILL.md:559

Codex 常见目标位置例如：

```text
~/.codex/skills/frontend-visual-qa/
.codex/skills/frontend-visual-qa/
~/.agents/skills/frontend-visual-qa/
.agents/skills/frontend-visual-qa/
```

## Preserved Example 3 — from SKILL.md:1015

正确做法：
Selected Direction B
+
完整 Complete Design Input Package
↓
首次完整构建 Report Mode
+
首次完整构建 Presentation Mode
```

后续任何视觉调整都必须保持 Selected Design Direction Contract，除非用户明确要求换方向。

## Phase 5：Coverage Mapping、QA 与修复

必须完整读取并执行：

```text

## Preserved Example 4 — from 10-huashu-design-contract.md:194

Motion / Interaction 示例模块（如适用）
```

每一个 Prototype 必须基于同一份 Direction Comparison Package：

```text

## Preserved Example 5 — from 12-display-mode-and-presentation.md:323

复杂内容示例继续有效：

```text
T04
→ Main Deck：Overview Chart + Key Findings
→ Appendix：Detailed Table + Full Notes
```

---

# 6、Presentation Artifact-Type 真实故障模式示例【V2.4 新增】

错误：

```text
slides/
├── 01-cover.html
├── 02-overview.html
└── _shared.css

Batch Generator
↓
把目录内所有文件都送进 HTML Template
↓
_shared.css 变成：
<html>...</html>
↓
浏览器仍能加载 iframe HTML
但 Stylesheet 解析失败
↓
Slides 白屏 / 无样式
```

正确：

```text
presentation/
├── index.html
├── deck-manifest.js
├── assets/css/shared.css
└── slides/*.html
```

并且：

```text
shared.css
→ CSS_RAW_WRITER
→ LOCK

slides/*.html
→ HTML_SLIDE_WRITER
```

---

# 7、Deck Manifest SSOT 示例【V2.4 新增】

错误：

```text
HTML 初始写死：1 / 14

但 Runtime Slide List 实际：17 Slides
```

即使 JS 最终把 Counter 改对，也说明存在两个 Slide Count 真值源。

另一个错误：

```text
Appendix Display Number
= i - 11
```

它隐含假设 Main Deck 永远是 12 页。

正确：

```text
Deck Manifest.slides.length
= 唯一总页数来源

Deck Manifest.slide.id
= 唯一显示编号来源

Deck Manifest.slide.section
= Main / Appendix 唯一分组来源
```

Counter、Overview、Jump、Navigation 全部从同一个 Manifest 派生。

---

# 8、Artifact Bug 的局部回滚示例【V2.4 新增】

前提：

```text
Content Coverage = PASS
Source Table Coverage = PASS
Selected Design System = LOCKED
```

发现：

```text
shared.css Artifact Type = FAIL
```

错误修法：

```text
重新读 Markdown
→ 重新做 Cxxx / Txx
→ 重新生成 Prototype
→ 重新设计整套 Deck
```

正确修法：

```text
保留 Complete Design Input Package
保留 Selected Design System Snapshot
↓
只重建 shared.css
↓
Artifact Integrity QA
↓
Frontend Render QA
↓
最终 Regression QA
```



---

# 9、Presentation Motion 不丢 Input 示例【V2.5 新增】

假设一页承接：

```text
C021 市场增长
C022 用户需求变化
C023 竞争加剧
C024 最终判断：黄金窗口
```

错误：

```text
0.8s 只闪过 C021
1.4s 只闪过 C022
2.0s 只闪过 C023
2.6s 出现 C024
3.0s 后全部淡出
```

这虽然“很动态”，但关键语义只存在于瞬时帧：

```text
Motion-only Semantic Unit > 0
→ FAIL
```

正确：

```text
Static Semantic Base 已经包含 C021~C024
↓
Beat 1 BUILD C021
Beat 2 REVEAL C022
Beat 3 COMPARE C023
Climax FOCUS C024
↓
Final Hold：四个核心事实与关系仍然可读
```

---

# 10、Static Fallback 实现反例【V2.5 新增】

错误：

```css
[data-motion] { opacity: 0; }
```

然后完全依赖 JS 把内容改回 `opacity:1`。

如果 JS 失败：

```text
核心内容永久隐藏
→ Semantic Coverage 实际失效
```

更安全的思路：

```text
默认 DOM = 可见 / 可读
Motion Runtime Ready
→ 加 motion-ready 状态
→ 才应用 staged initial state
```

并提供 reduced-motion / disabled-motion 的完整静态状态。

---

# 11、Motion “有但很干”反例【V2.5 新增】

错误：

```text
Slide 01：fade-up
Slide 02：fade-up
Slide 03：fade-up
Slide 04：fade-up
...
所有 duration 相同
所有 stagger 相同
```

这在技术上有动画，但没有 Temporal Narrative。

正确方向：

```text
CALM
→ BUILD
→ PEAK
→ HOLD
```

根据内容设计 Deck-level Rhythm，并只在少数关键页形成 Signature Motion Moment。

## V2.6 — Semantic Obligation / Evidence-backed Coverage 示例

### 例：Manifest-only DIP 是假锁

错误：

```text
semantic_unit_count = 50
table_count = 27
status = LOCKED
```

但没有任何 C/T 的 Render-ready Display Content。

结果：

```text
LOCK FLAG = TRUE
!=
CONTENT LOCKED
```

正确：Complete DIP 必须包含真实 DU Data Plane + Obligation Refs，并记录 Content Hash。

### 例：Inventory 阶段已经发生语义替换

Source：

```text
洞察7 = 年轻潮流 → 品质家庭；探索远方 × 经营小家
```

错误 Inventory：

```text
C009 = 洞察7：窄路掉头与停车痛点
```

即使 C009 后续有 Destination，也不能算 Coverage；因为 Source Obligation 在 Inventory 阶段已经被替换。

### 例：Transformation Map 不能修改优先级

Source T01：

```text
P0 / P0 / P1
```

错误 Transformation：

```text
P0 / P1 / P2
```

这是 Exact Fact / Action Priority Mutation，必须在 Source → DIP Fidelity Gate 失败。

### 例：Persona 事实必须 Exact

Source：

```text
黄皓 = 35岁
```

错误 Comparison / Final：

```text
黄皓 = 32岁
```

即使 Persona 的“大体人群含义”不变，也必须：

```text
Exact Fact Fidelity = FAIL
```

### 例：Txx ID 不等于表内 Coverage

```text
<!-- T18, T19, T20 -->
```

不能证明 T19 / T20 内容存在。

必须证明：

```text
T19 Required Entries / Dimensions → DIP → Final Evidence
T20 Required Entries / Dimensions → DIP → Final Evidence
```

---

# 10、Controlled Boldness 示例【V2.7 新增】

## 10.1 正确：内容锁定，但表达大胆

```text
Locked DIP:
>90 天种草
7 天锁单
Required Relationship: 慢进 → 快出

Final Expression:
超大数字对撞 + 关系箭头 + progressive bar build
```

语义、数字、关系完全不变，但视觉表达可以很强。

## 10.2 错误：把“内容锁”理解成“设计也别动”

```text
复杂 Process → 普通 Table
Persona → 普通 2x2 Grid
Key Data → 普通 Card
Relationship → 普通 Table
```

如果用户选中的是高 Expressiveness 方向，这属于 Structural Conservatism。

## 10.3 错误：为了大胆而删内容

```text
Source Table 有 7 个 Required Entries
↓
为了做“Top 3”大卡片
只保留 3 项
```

即使视觉非常漂亮：

```text
Semantic Obligation Coverage = FAIL
```

## 10.4 正确：Boldness Budget

```text
Cover        HIGH
Core Data    HIGH
Deep Read    MEDIUM
Appendix     LOW
```

形成节奏，而不是每个 Section 都抢注意力。

## 10.5 正确：Report Motion Progressive Enhancement

```text
默认 DOM：可见
Runtime Ready：加 .motion-ready
.motion-ready 下才启用 reveal initial state
prefers-reduced-motion / JS fail：恢复完整可读
```

禁止：

```text
.reveal { opacity: 0 }
+
必须依赖 JS 才能首次看见关键内容
```

# 10、V2.9 WHAT / WHY / HOW 真实反例

## 10.1 三驱动关系被 Flex Wrap 破坏

Source / DIP：

```text
A × B × C → Result
```

错误实现：

```text
A × B
×
C
```

问题不只是 CSS：上游没有把“共同驱动”作为 WHY 传给 Huashu。

正确：

```text
Design Intent:
Semantic Structure = multiplicative_convergence
Visual Risk = 不得被理解成三个孤立卖点
```

Huashu 仍可自由决定最终构图。

## 10.2 Design Intent 越权重选 Top N

错误：

```text
Source Top 7
↓
Design Intent 为了更聚焦
↓
Final Top 5
```

这是 `CONTENT_SCOPE_MUTATION`，不是设计优化。

## 10.3 为了四卡构图改变产品分类

错误：

```text
Source Absolute Advantages = 5 项
↓
为了 4-card composition
把其中一项移到 Relative Advantage
再把一个属性提升成独立卡
```

这是 `SEMANTIC_RECLASSIFICATION_FOR_LAYOUT`。

正确：

```text
5 个 WHAT 保持不变
Huashu 自由选择 5 项构图、分组视觉、主次布局或多载体承接
```

## 10.4 Responsive 隐藏业务语义

错误：

```css
@media (max-width:960px){
  .business-direction{display:none}
}
```

如果该字段是“借势方向 / 结论 / 业务标签”，则属于 `RESPONSIVE_SEMANTIC_LOSS`。

正确：

```text
隐藏视觉 Track 可以
业务文本必须重排后继续可读
```

## 10.5 Source 自身冲突

Source：

```text
LS6 驾驶感受 4.75（第1）
竞品驾驶感受 4.80
```

错误：继续把“4.75绝对领先”当成无争议 Locked Fact。

正确：登记 `SOURCE_CONFLICT`，保留双方并进入待确认 / 矛盾清单。
