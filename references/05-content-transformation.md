# 1、长文本继续保持当前优秀处理方式

不要因为增加 Source Table 保护机制，就降低长文本处理质量。

对于明显过长内容继续执行：

```text
原始长文本
↓
语义理解
↓
核心结论提取
↓
信息点拆分
↓
结构重新组织
↓
视觉组件选择
```

长文本可转换为：

```text
Executive Summary
Key Takeaways
Step Cards
Timeline
Process
Comparison
Callout
Insight Card
Pros / Cons
FAQ
Metric Cards
Generated Table
Architecture
```

原则继续保持：

> **长内容结构化，短内容自然保留。**

---


# 2、重要内容采用双层表达

对于重要的长内容，优先：

```text
第一层：
一句话结论

第二层：
- 要点1
- 要点2
- 要点3
- 要点4
```

必要时增加：

```text
详情
表格
图示
流程
```

让页面同时支持：

```text
快速浏览
+
深入阅读
```

---


# 3、建立 Semantic Content Transformation Map

正式编码前，建立：

```text
Semantic Content Transformation Map
```

它必须以 Source Content Inventory 中的 Cxxx 为主线，而不是只按 Markdown 标签类型做粗粒度映射。

例如：

```text
H1
→ Hero

开篇长文本
→ Executive Summary

方法长文本
→ Steps

数字
→ Metric Cards

对比关系
→ Generated Comparison Table

流程
→ Process Diagram

结论
→ Highlight

Source Table T01
→ 精炼后的 Comparison Table

Source Table T02
→ 数据提取
→ Metric Cards + Supporting Chart

C071 Persona A / 消费观
→ 3 个消费决策标签 + 一句话结论

C072 Persona A / 价值冲突
→ “理性 VS 情感”对立结构图

C073 Persona A / 决策优先级
→ Priority Ranking

C074 Persona A / 优势节点
+
C075 Persona A / 风险节点
→ Advantages / Risks Matrix

C076 Persona A / 竞品差异
→ Persona Insight Callout
```

尤其注意：

> 每一个 Cxxx 都必须在 Transformation Map 中有明确 Destination；每个 Source Table Txx 也必须作为其子集被追踪。

禁止出现没有去向、没有转换结果的 Cxxx 或 Txx。

最终 HTML 中视觉模块数量可以少于 Semantic Unit 数量，因为多个相关 Semantic Unit 可以合并表达。

但：

```text
Source Unit 数量可以减少为更少的视觉模块
≠
Source Unit 可以没有信息承接
```

---

# 4、Transformation 必须在 Huashu 之前完成【V2.2 硬化】

本文件中的 Transformation 不再只是“规划”。

进入 Prototype / Huashu 阶段前：

```text
所有 Cxxx / Txx 必须已经形成 render-ready Transformed Content
```

详细边界见：

```text
references/17-render-ready-transformation-boundary.md
```

原有所有长文本、双层表达、Semantic Content Transformation Map 示例全部继续有效，不做删减。

# 5、V2.6：Transformation Map 必须保存 Transformation Result

以下只有视觉计划，不算完整 Transformation Map：

```text
C036 → Persona Dossier
T02 → Timeline
T04 → Cards
```

每个 Semantic Obligation 必须记录：

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

以及实际 `Transformed Result`。

因此 Transformation Map 回答的是：

```text
这个 Source Obligation
→ 经过什么转换
→ 最终具体变成什么
```

而 `Visual Expression Routing Map` 才回答：

```text
这个 Render-ready Content
→ 最终用什么视觉形式展示
```

两者不得混同。

允许删除重复措辞 / 修辞 / 赘述；独立事实、维度、行动、风险、流程节点、证据、结论、Required Relationship 不得无声删除。
