# 1、Semantic Coverage + Long Content Transformation 双硬约束【最高优先级】

本任务必须同时满足：

```text
Semantic Coverage Rate = 100%

Long Content Transformation Rate = 100%
```

二者不能互相替代。

## 1.1 Semantic Coverage = 100%

Markdown 中所有被登记为 Cxxx 的 Source Semantic Unit，都必须在最终 HTML 中存在明确的信息去向。

允许：

```text
一个 Cxxx → 一个组件

一个 Cxxx → 多个组件

多个高度相关 Cxxx → 一个综合可视化模块
```

但必须能够说明：

```text
这个 Semantic Unit 最终由哪个组件承接
承接了哪些核心事实 / 观点 / 数据 / 关系 / 结论
```

绝对禁止：

```text
C021 → 无去向
C022 → 因为和前文有点像所以直接删除
C023 → 因为页面较长所以省略
C024 → 在分析时读过，但最终 HTML 没有任何表达
```

## 1.2 Long Content Transformation = 100%

Semantic Coverage = 100% 绝不意味着把原文搬过去。

以下内容一旦明显过长或信息密集，就必须进行 Transformation：

```text
长段落
长表格 Cell
复杂列表
复杂流程描述
密集对比描述
人物画像长文本
多层决策逻辑
长篇结论与证据链
```

必须经过：

```text
语义理解
↓
提取事实 / 数字 / 标签 / 观点 / 关系 / 结论
↓
删除重复和低价值修饰
↓
必要时与相关 Semantic Units 合理合并
↓
重新选择视觉表达
↓
生成精炼 HTML 组件
```

禁止通过以下方式满足 Coverage：

```text
原样复制长段落
原样复制长表格
Markdown 逐段翻译成 HTML
只加 CSS 不做信息重构
保留 Markdown 原始“标题→段落→表格→段落”的机械结构
```

核心原则：

> **Coverage 约束“信息不能消失”；Transformation 约束“信息不能原样堆积”。**

---


# 2、去重不等于删除来源维度

如果多个位置表达相似主题，可以去除重复措辞，但不能因此删除不同来源维度中的独立意义。

例如：

```text
总报告：智驾是风险

Persona A：智驾不是第一优先，但车机生态是流失风险

Persona B：安全优先，对智驾的要求是“可靠而非激进”

Persona C：智驾口碑会影响技术型用户的选择
```

不能因为总报告已经写过“智驾风险”，就把三个 Persona 中的差异全部删除。

允许合并共识，但必须保留：

```text
不同角色 / 场景 / 阶段 / 人群下的作用差异
```

判断规则：

> **可以删除重复表述，不能删除独立分析维度。**

---


# 3、不要过度总结

“总结”不等于删除重要内容。

必须保证：

```text
核心观点不丢失

关键结论不丢失

关键数字不丢失

重要限定条件不丢失

专业术语不乱改

方法步骤不丢失

因果关系不改变

原文立场不改变
```

可以减少：

```text
重复表达
冗余解释
过长句子
```

但是不能降低：

```text
Information Completeness
```

---


# 4、禁止修改原文事实

以下内容必须准确：

```text
数字
百分比
时间 / 日期
价格 / 销量
模型名称
方法名称
产品 / 车型名称
专业术语
实验结果
指标
公式
单位
人名
年龄
职业
地点
优先级
来源 / 口径
```

允许：

```text
改变表达方式
压缩标签
改变视觉结构
```

禁止：

```text
改变事实值
用“大体意思一致”替代精确事实一致
```

V2.6 起，以上内容归入 `EXACT_FACT`，硬门槛为：

```text
Exact Fact Fidelity = 100%
Exact Fact Mutation = 0
```

`Information Fidelity = 高` 不能替代 Exact Fact Gate。

---

# 5、V2.6：Coverage 按 Semantic Obligation 证明

`Cxxx / Txx 有 Destination` 是必要条件，不是充分条件。

最终必须同时满足：

```text
Inventory Structural Coverage = 100%
Semantic Obligation Coverage = 100%
Exact Fact Fidelity = 100%
Required Relationship Coverage = 100%
Missing Obligation = 0
Unproven Obligation = 0
```

例如：

```text
C036 → Persona Section
```

不能直接 PASS；必须继续证明 C036 内的年龄、职业、原车、价值冲突等 Obligations 被 DIP 和最终页面承接。

完整 Obligation / Evidence 数据模型见：

```text
references/24-semantic-obligation-and-evidence-contract.md
```
