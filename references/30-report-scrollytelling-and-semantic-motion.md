# Report Scrollytelling & Semantic Motion Contract

本文件专门定义 Report Mode 中的 Scrollytelling / Semantic Motion。

它补充 `11-huashu-visualization-motion-routing.md`，不替代 Presentation 的 `23-presentation-motion-choreography.md`。

核心原则：

> **Motion should explain, not merely decorate.**

---

# 1、Scrollytelling 不是默认模板

允许使用的前提：

```text
内容存在真实 progression / comparison / build / transition
+
Design Intent 支持逐步认知
+
Selected Design Direction 适合
```

禁止：

```text
所有章节都做 sticky scrolly
为了“高级感”强行把普通列表动画化
```

---

# 2、适合的 Semantic Structure

例如：

```text
市场从增量 → 存量
竞争格局逐步形成
时间窗口逐步打开
漏斗阶段迁移
多源证据逐层构成结论
Before → After
多因素逐步汇聚
```

---

# 3、Semantic Motion 与 Decorative Motion 区分

Decorative：

```text
fade-in
slide-up
hover-lift
```

这些可以存在，但不算 Narrative Motion。

Semantic Motion：

```text
随着滚动逐步构建因果链
图表从阶段 A 切换到阶段 B
竞争阵营逐步形成
多个驱动因素最终汇聚到结论
时间窗口随时间轴打开 / 收紧
```

---

# 4、Report Motion Progressive Enhancement

必须满足：

```text
默认 DOM = 可读
JS 只增强表达
JS 失败 = 内容仍完整
prefers-reduced-motion = 内容仍完整
关键文本不得只存在于 hidden state
```

禁止：

```text
opacity:0 作为默认静态状态且 JS 失败后永远不可见
关键结论只在 hover / click 后出现
```

---

# 5、Scrollytelling Design Record

如果采用 Scrollytelling，应在：

```text
workspace/visual-grammar-exploration-map.md
```

记录：

```text
Target DU / Intent
Why Scrollytelling
Static Base
Scroll Beats
Final Hold
Reduced-motion Fallback
```

---

# 6、视觉自由

Design Intent 不得写：

```text
必须 Scrollytelling
```

Huashu 可以判断：

```text
同一 WHY 用静态关系图更合适
```

并选择静态表达。

HOW 仍属于 Huashu。

---

# 7、质量判断

好的 Scrollytelling：

```text
滚动顺序 = 认知顺序
每个 Beat 有明确意义
Final Hold 能完整读出结论
减少动画仍能理解
```

差的 Scrollytelling：

```text
只是每滚一下换一张卡
Beat 与语义无关
动画结束后关系反而不清楚
必须快速滚动才能看到完整内容
```
