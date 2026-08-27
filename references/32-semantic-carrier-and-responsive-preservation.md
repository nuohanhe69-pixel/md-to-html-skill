# Semantic Carrier & Responsive Preservation Contract

本文件解决两个实际问题：

1. 为了 100% Coverage 导致同一内容反复完整渲染。
2. 为了响应式适配，CSS / JS 把真实业务语义隐藏掉。

---

# 1、Coverage 不等于重复渲染

目标：

```text
Semantic Coverage = 100%
```

不要求：

```text
每个 Obligation 在 3 个地方都完整重复
```

每个重要 Obligation 应定义：

```text
Primary Carrier
Supporting Carrier(s)（可选）
```

Primary Carrier 负责完整承担语义。

Supporting Carrier 可以：

```text
引用
摘要
跳转
视觉提示
```

但不得制造新的含义。

---

# 2、Carrier 例子

```text
X3 = “慢进快出”
```

可以：

```text
Primary Carrier:
完整 90天 vs 7天 视觉模块

Supporting Carrier:
Cross Matrix 仅保留 X3 名称 + Evidence Refs

Supporting Carrier:
Action Table 引用“洞察3”
```

无需在三个地方都重复整段解释。

---

# 3、Source Table 的 Carrier

Source Table 可以：

```text
Primary = Visualization / Matrix / Cards
Supporting = Appendix Detailed Table
```

但 Required Entries / Dimensions 必须有 Evidence。

如果主视觉为了可读性压缩 Detail：

```text
Main Visual = Summary Carrier
Appendix = Complete Carrier
```

而不是删 Detail。

---

# 4、Responsive Semantic Preservation【硬性】

响应式允许简化：

```text
装饰
辅助坐标
视觉轨道
非必要连线
动画
```

响应式禁止隐藏：

```text
事实
关键数字
业务标签
借势方向
结论
Required Relationship
Source Table Required Entry
```

典型错误：

```css
@media (max-width:960px){
  .rank .rk-dir{display:none}
}
```

如果 `.rk-dir` 是“借势方向”等业务内容，则这是：

```text
RESPONSIVE_SEMANTIC_LOSS
```

正确做法：

```text
桌面：Event + Bar + Direction + Score
移动：Event + Score + Direction（Bar 可隐藏）
```

---

# 5、Interactive / Motion 同样适用

禁止：

```text
只有 hover 才出现核心含义
只有 active tab 才存在唯一 DOM 内容且不可访问
关键内容被 JS 删除而不是重新排布
```

可以：

```text
默认 DOM 保留语义
交互只改变展示层级 / 聚焦状态
```

---

# 6、QA

最终 QA 需要检查：

```text
Primary Carrier Coverage = 100%
Unnecessary Full-content Duplication = NO material issue
Responsive Semantic Loss = 0
Interaction-induced Semantic Loss = 0
Reduced-motion Semantic Loss = 0
```
