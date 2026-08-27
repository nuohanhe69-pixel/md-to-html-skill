# Presentation Motion Choreography & Temporal Storytelling Contract

本文件定义 Presentation 如何在**不丢失 Complete Design Input Package** 的前提下，把 Huashu 的 Motion 能力从“可选动画效果”升级为“时间叙事设计能力”。

它不负责：

```text
重新总结内容
重新抽取数据
改变 Cxxx / Txx
重新决定 Coverage
重新选择 Design Direction
```

它只负责：

> **在已经完整、render-ready 的 Presentation Semantic Base 之上，设计信息何时出现、如何建立、怎样形成节奏、哪里强调、最后停在哪个可读状态。**

---

# 1、核心边界：Motion 是 Expression Layer，不是 Content Layer【硬性】

正确链路：

```text
Complete Design Input Package
↓
Presentation Main / Appendix Routing
↓
Slide Semantic Contracts
↓
Static Semantic Base
↓
Motion Choreography
↓
Final Hold State
↓
Static / Reduced-motion Fallback
```

禁止：

```text
Complete Design Input Package
↓
Motion Storyboard 自己重新总结 / 删除内容
↓
只把“适合动画”的部分做进 Presentation
```

必须：

```text
Static Semantic Structure
=
Motion Semantic Structure
```

允许变化的是 Temporal Order，不是 Semantic Scope。

---

# 2、进入 Motion 设计前必须读取 Huashu 当前版本的相关能力

如果 Main Deck 存在适合 Motion 的：

```text
趋势
流程
时间轴
优先级
竞争关系
多因素交汇
阶段推进
数据故事
```

父 Skill 必须让当前安装版本的 `huashu-design` 读取它**当前版本实际存在且与本任务相关**的 Motion / Animation / Slide references 和 demos。

当前上游常见内容可能包括：

```text
animation-best-practices
animation-pitfalls
animations
motion / slide demos
```

但不得为了匹配本文件伪造不存在的路径；以上游当前安装版本为准。

目标是学习：

```text
Motion Philosophy
Temporal Rhythm
Easing / Physicality
Staging
Build / Reveal / Transform
Hold / Pause
Slide / Scene Transitions
```

不是复制 Demo 的 DOM / CSS / 文案 / 品牌色。

---

# 3、Report / Main Deck / Appendix 的 Motion Density 必须分开

跨模式 Motion Density 的正式规则由 `11-huashu-visualization-motion-routing.md` 所有；Report 的 Controlled Boldness / Expressiveness 由 `25-design-expressiveness-and-controlled-boldness.md` 补充。

本文件只锁定 Presentation：

```text
Report Mode
= 由 11 / 25 的 Selected Design Expressiveness Profile 决定

Presentation Main Deck
= ADAPTIVE MEDIUM–HIGH
= 讲述优先

Presentation Appendix
= LOW
= 查询 / 查证优先
```

注意：

```text
MEDIUM–HIGH
!=
每个元素都动画
```

它表示 Main Deck 必须认真设计“时间上的讲述”，而不是默认全部 STATIC。

每一张 Main Deck Slide 都必须有：

```text
Choreography Decision
```

即使最终决定：

```text
STATIC / HOLD
```

也必须是经过判断后的主动选择，而不是遗漏 Motion 设计。

---

# 4、Slide Semantic Contract【Motion 前置硬约束】

每张 Presentation Slide 在动画设计前至少记录：

```text
Slide ID
Main / Appendix
承接的 Cxxx / Txx
Persistent Facts
Required Relationships
Narrative Focus
Persistent / Final Semantic Destination
Static Fallback Requirement
```

例如：

```text
Slide 07
Semantic IDs: C021 C022 C023 C024
Narrative Focus: 三个变量共同形成市场窗口
Persistent Facts:
- 市场增长
- 用户需求变化
- 竞争加剧
- 最终判断：黄金窗口
Required Relationship:
市场增长 + 需求变化 + 竞争加剧 → 黄金窗口
```

Motion Storyboard 无权删除这些内容。

---

# 5、Motion Intent Vocabulary

Main Deck 每张 Slide 必须选择一个或多个 Motion Intent：

```text
STATIC
REVEAL
BUILD
TRANSFORM
FOCUS
COMPARE
SEQUENCE
CAMERA_STAGE
```

含义：

```text
STATIC
→ 这一页以停留 / 阅读为主，不强行动画

REVEAL
→ 逐步显露已有信息

BUILD
→ 逐步建立图表 / 关系 / 结构

TRANSFORM
→ 同一信息结构发生有意义的视觉形态转换

FOCUS
→ 通过聚焦 / 弱化帮助观众识别核心结论

COMPARE
→ 通过时间顺序建立对比关系

SEQUENCE
→ 流程 / 时间轴 / Priority 按语义顺序推进

CAMERA_STAGE
→ 舞台、镜头、场景层级的空间变化
```

不能为了“更动”随意选择 Intent；Intent 必须服务当前 Semantic Relationship。

---

# 6、每张 Main Deck Slide 必须建立 Motion Storyboard

至少记录：

```text
Entry State
Beat 1
Beat 2
Beat 3（如需要）
Climax / Focus Moment（如需要）
Final Hold State
Static Fallback State
```

每个 Beat 至少记录：

```text
Beat ID
Semantic IDs（Cxxx / Txx）
Purpose
Motion Intent
What Changes Visually
What Must Not Change Semantically
End State
```

示例：

```text
Slide 07 — 三重窗口

Entry State
→ 标题 + 三个变量的静态容器已经存在

Beat 1
C021
→ BUILD 市场趋势

Beat 2
C022
→ REVEAL 用户需求变化

Beat 3
C023
→ COMPARE / BUILD 竞争压力

Climax
C024
→ 三个关系视觉交汇，FOCUS 到“黄金窗口”

Final Hold
→ C021 / C022 / C023 / C024 的核心事实与关系全部可读
```

---

# 7、Deck-level Motion Rhythm Map

除了逐页 Storyboard，还必须建立：

```text
workspace/deck-motion-rhythm-map.md
```

它至少记录：

```text
Slide ID
Narrative Role
Motion Intensity
Transition Intent
Signature Moment? YES / NO
Hold / Pause Intent
```

推荐 Motion Intensity：

```text
CALM
BUILD
PEAK
HOLD
```

目标不是机械套用固定节奏，而是防止：

```text
每页 0.4s fade-up
每页同一 stagger
每页同一速度
```

导致技术上“有动画”，体验上仍然很干。

如果 Main Deck 超过 5 页且内容本身适合动态叙事，建议识别 1–3 个：

```text
Signature Motion Moments
```

让整套 Deck 有少量真正值得记忆的高潮，其余页面保持克制。

---

# 8、Motion Traceability【硬性】

必须生成：

```text
workspace/presentation-motion-storyboard.md
```

并保证每一个 Motion Beat 都可追溯到：

```text
Cxxx
Txx
Immutable Facts
Required Relationships
```

必须：

```text
Motion Traceability = 100%
Motion-only Semantic Unit = 0
```

错误：

```text
1.2s 出现关键数字 32%
2.0s 后永久消失
最终页面没有任何稳定承接
```

正确：

```text
32%
→ Motion Entry
→ Motion Emphasis
→ 最终稳定停留 / 或同页 persistent summary
```

或者：

```text
Main Deck 动态概览
+
Appendix 持久详细表达
```

前提是 Main Deck 本身仍保留准确的核心语义。

---

# 9、Static Semantic Base 的实现安全规则【非常重要】

对承担核心语义的 DOM，默认状态优先必须是：

```text
VISIBLE / READABLE
```

只有当 Motion Runtime 成功初始化后，才允许进入动画初始态。

推荐语义：

```text
Default DOM
→ Static Visible

Motion Runtime Ready
→ 添加 .motion-ready / data-motion-enabled
→ 再启用 opacity / transform / staged reveal 初始态
```

禁止：

```text
关键内容默认 opacity: 0
+
必须依赖 JS 才能恢复
```

因为：

```text
JS 失败
→ 内容永久隐藏
→ Semantic Coverage 实际失效
```

`prefers-reduced-motion` / Motion Disabled 时必须恢复：

```text
opacity: 1
transform: none
transition: none / minimal
核心内容全部可读
```

---

# 10、Final Hold State【硬性】

Motion 可以有：

```text
过程态
聚焦态
对比态
临时弱化态
```

但最终必须进入可读的：

```text
Final Hold State
```

其中：

```text
核心结论可读
关键数字可读
Required Relationships 可理解
不会因为动画结束而把关键信息移出画布
```

如果某些详细信息为了叙事在 Main Deck 中被压缩，则必须由 Main / Appendix Routing 保证其 Persistent Destination 已存在；不能让它只存在于瞬时帧。

---

# 11、交互同样不能成为唯一语义入口

禁止关键事实只存在于：

```text
Hover
Tooltip
Click-to-reveal
Auto-play transient frame
```

允许这些机制提供：

```text
补充解释
细节探索
视觉强调
```

但核心语义必须有 persistent / fallback 表达。

---

# 12、Shell / Slide Transition Strategy

Presentation 不应只有：

```text
iframe src 瞬间切换
```

如果 Selected Design System / Huashu Motion Grammar 支持，可设计一致的：

```text
Crossfade
Stage Shift
Scale / Depth
Directional Transition
Focus Transition
```

但整套 Deck 应优先使用 1–2 种稳定的 Transition Primitives，而不是每页一种花活。

如果 Runtime Deck Manifest 记录 motion / transition metadata：

```text
Slide Identity / Count / Main|Appendix
仍然只能以 Deck Manifest 为唯一 SSOT
```

Motion metadata 只能附着在 Slide Entry 上，不能另建一份相互竞争的 Slide List。

---

# 13、Motion Quality：不是“有没有 CSS animation”

以下不应被视为高质量 Motion：

```text
所有 Slide 都只是 opacity 0 → 1
所有 Card 都 translateY(20px)
所有数字都 Count-up
所有页面同一 duration / stagger
为了“动态”让每个元素都飞入
```

Huashu Design Critique 应判断：

```text
是否存在 Temporal Narrative
是否有节奏变化
是否有主次
是否存在合理的 pause / hold
是否至少存在少量 Signature Motion Moment（内容适合时）
Motion 是否建立数据 / 流程 / 因果 / 对比关系
是否体现 Selected Design System Snapshot 的 Motion DNA
```

---

# 14、Motion Semantic Safety Gate【硬性】

必须：

```text
Presentation Semantic Coverage = 100%
Presentation Source Table Coverage = 100%
Static / Reduced-motion Fallback Coverage = 100%
Motion Traceability = 100%
Motion-only Semantic Unit = 0
Motion-induced Information Loss = 0
Final Hold Readability = PASS
```

验证至少包含：

```text
A. Motion Enabled
→ 正常播放并检查最终状态

B. Motion Disabled / Reduced Motion
→ 关闭或最小化动画
→ 核心语义仍可完整读取

C. Runtime Failure Tolerance
→ 动画 Runtime 未初始化时
→ Static Semantic Base 不应永久隐藏
```

任一硬性项 FAIL：

```text
Final Delivery = BLOCKED
```

---

# 15、Motion Expressiveness Gate【条件性质量 Gate】

这是设计质量 Gate，不改变 Content Coverage 标准。

当满足任一条件时：

```text
Selected Design Direction 明确具有 Motion DNA
Design Context 明确是演示 / 大屏 / Keynote
Main Deck 存在多个趋势 / 流程 / 时间轴 / 数据关系，天然适合动态建立
```

则 Huashu Critique 必须判断：

```text
Motion Choreography Quality = PASS / FAIL
```

如果最后只是机械 fade / stagger，虽然 Render 正常，也可以被判为设计质量 FAIL。

如果当前内容天然不适合 Motion，允许：

```text
Motion Expressiveness = N/A / intentionally restrained
```

不能为了通过这一 Gate 强行动画化静态内容。

---

# 16、与 Artifact Build Layer 的边界

Motion Storyboard / Rhythm Map 属于设计规范；真正的：

```text
CSS
JS
Runtime Manifest
Slide HTML
```

仍必须遵守：

```text
references/22-presentation-artifact-integrity-contract.md
```

Motion Runtime 不能绕过：

```text
Artifact Type
Writer Routing
Single Writer Ownership
Shared Asset Lock
Dependency Resolution
```

---

# 17、最终目标

正确目标不是：

```text
动画更多
```

而是：

```text
Complete Design Input Package 一个不漏
+
Main Deck 更会讲
+
Appendix 更适合查
+
Motion 有时间叙事
+
Static / Reduced-motion 状态仍然完整
```

即：

> **完整内容之上增加 Temporal Storytelling Layer，而不是用 Temporal Storytelling 替代完整内容。**
