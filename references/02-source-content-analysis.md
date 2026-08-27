# 1、第一阶段：完整解析 Markdown

不要直接执行：

```text
Markdown
↓
HTML
```

首先建立完整：

```text
Content Model
```

至少识别：

```text
文档主题
目标读者
核心结论

H1
H2
H3

长段落
短段落
列表

关键观点
关键数字
关键数据

方法
流程
步骤
因果关系
对比关系

优点
缺点
风险
结论

图片
引用
链接

所有原始表格
```

目标是：

> **先理解信息，再设计视觉表达。**

而不是机械转换 Markdown 标签。

---


# 2、最高优先级：先建立 Source Content Inventory

在进行：

```text
长文本总结
内容压缩
内容重组
可视化设计
Content Transformation Map
HTML 编码
```

之前，必须先建立完整的：

```text
Source Content Inventory
```

Source Content Inventory 不是简单记录“有哪些标题和表格”，而是要把 Markdown 中所有具有独立信息价值的语义单元登记出来。

至少包括：

```text
Heading Inventory
Paragraph Insight Inventory
List / Bullet Inventory
Key Data Inventory
Process / Step Inventory
Comparison Inventory
Risk / Opportunity Inventory
Conclusion Inventory
Recommendation Inventory
Persona Dimension Inventory（如果存在人物画像）
Source Table Inventory
Image Inventory
Appendix / Assumption Inventory
```

对于每一个有独立信息价值的内容单元，分配唯一 Semantic Unit ID：

```text
C001
C002
C003
...
Cxxx
```

例如：

```text
C021 → 黄皓 / 消费观
C022 → 黄皓 / 价值观冲突
C023 → 黄皓 / 信息审美
C024 → 黄皓 / 决策优先级
C025 → 黄皓 / 流失风险
C026 → 黄皓 / 竞品差异
```

目标不是逐句编号，而是：

> **把所有具有独立分析意义、决策意义或事实意义的“信息主题”登记下来，避免后续在压缩和设计过程中无声消失。**

其中 Source Table Inventory 继续保留，但它只是 Source Content Inventory 的一个重要子集，而不是唯一完整性检查对象。

必须先完成 Source Content Inventory，再进入内容压缩、可视化和 HTML 设计。

禁止：

```text
边读 Markdown 边决定哪些内容值得留下

因为前面已经出现类似观点，就不登记后面的独立分析维度

因为页面太长，就在 Inventory 阶段主动舍弃内容
```

先登记，再转换。

---

# 3、V2.6：Source Inventory 必须携带 Semantic Obligations

`Source Content Inventory` 不得退化为：

```text
C036 = 黄皓 Persona
C037 = 周敏 Persona
T04 = 产品绝对优势表
```

这种“目录式 Inventory”只能证明主题存在，不能保护主题内部事实。

每个 Cxxx / Txx 必须按 `24-semantic-obligation-and-evidence-contract.md` 建立必要的：

```text
EXACT_FACT
SEMANTIC_POINT
REQUIRED_RELATIONSHIP
REQUIRED_DIMENSION
REQUIRED_ENTRY
CONCLUSION
QUALIFIER
EVIDENCE
ACTION
RISK_OPPORTUNITY
```

同时建立 `Source Structure Baseline`，核对显式 `Top N / Step N / Insight N`、所有 Source Table、Persona、行动、风险、附录、遗留问题、矛盾数据等结构。

Gate：

```text
Inventory Structural Coverage = 100%
Unregistered Declared Item = 0
Unregistered Source Table = 0
```

未通过不得进入 Transformation。

Inventory 不复制整段 Markdown；只保存 Source Anchor + 独立 Semantic Obligations。

# V2.9 Source Integrity Pre-Gate

Source Inventory 完成后、DIP Lock 前必须读取并执行：

```text
references/31-source-integrity-gate.md
```

发现正文 / 表格 / 数字 / 排名 / 版本口径冲突时，必须登记为 `SOURCE_CONFLICT`，不得静默纠错。
