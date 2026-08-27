# 1、Source Table 零遗漏与高质量转换协议【硬性要求】

原 Markdown 中已经存在的所有表格定义为：

```text
Source Table
```

后续根据长文本、比较关系等新生成的表格定义为：

```text
Generated Table
```

必须明确区分二者。

Source Table 作为 Source Content Inventory 的重要子集，仍然必须 100% 进入转换流程。

本任务对 Source Table 的要求不是“原模原样保留”，而是：

```text
每一个 Source Table 都必须被识别
↓
每一个 Source Table 都必须进入 Content Transformation Map
↓
每一个 Source Table 都必须在最终 HTML 中有明确的转换结果
↓
允许转换成精炼表格 / 图表 / 卡片 / 矩阵 / 信息图 / 组合模块
↓
禁止任何 Source Table 被直接删除、跳过或没有任何最终表达
```

因此真正的硬性指标是：

```text
Source Table Coverage Rate = 100%
```

而不是：

```text
Source Table 原样保留率 = 100%
```

表格里的长文本与普通长文本一样，必须继续进行：

```text
语义理解
↓
数据提取
↓
关键结论提炼
↓
关键词 / 标签抽取
↓
冗余压缩
↓
选择更适合的图 / 表 / 卡片 / 矩阵表达
```

目标是：

> **Markdown 中每张表都被“点到并处理”，但最终 HTML 必须比原 Markdown 更精炼、更直观，而不是把原始长文本表格机械搬过去。**

同时要注意：

> **表格被覆盖 ≠ 整份 Markdown 已覆盖。**

即使：

```text
T01 ~ T15 全部 PASS
```

如果仍存在：

```text
人物画像中的决策路径消失
关键洞察的“证据→结论→决策意义”链条消失
流程中的关键阶段被压没
某个风险 / 机会维度没有最终表达
```

则整体：

```text
Semantic Coverage QA = FAIL
```

---


# 2、生成前必须完整盘点所有 Source Table

完整读取 Markdown 后，建立：

```text
Source Table Inventory
```

例如：

```text
SOURCE_TABLE_COUNT = 5
```

然后按照 Markdown 出现顺序建立：

```text
T01
T02
T03
T04
T05
```

每张表记录至少：

```text
Source ID
所属章节
表格前后的上下文
表格标题（如果存在）

Columns 数量
Rows 数量

Header
关键字段
关键数字
单位
备注
脚注
```

例如：

```text
T01

所属章节：
3.1 方法性能比较

Columns：
4

Rows：
6

Header：
方法
参数量
准确率
备注
```

必须先完成整个：

```text
Source Table Inventory
```

再进入后续阶段。

禁止：

```text
一边读取 Markdown
一边直接写 HTML
```

---


# 3、Source Table 必须具有唯一追踪 ID

按照源 Markdown 顺序编号：

```text
T01
T02
T03
...
TN
```

最终 HTML 中对应 Source Table 必须保留追踪信息。

推荐：

```html
<table data-source-table-id="T01">
```

例如：

```html
<div class="table-wrapper">
  <table
    class="data-table"
    data-source-table-id="T03"
  >
    ...
  </table>
</div>
```

后续 QA 必须通过这些 ID 进行完整性检查。

---


# 4、Source Table 必须有明确转换结果，但允许改变表达形式

下面这种情况属于错误：

```text
T01 → 已转换
T02 → 已转换
T03 → 没有任何处理，直接消失
T04 → 已转换
T05 → 没有任何处理，直接消失
```

这属于：

```text
Source Table Missing
```

但 Source Table 不要求最终仍然是 HTML `<table>`。

允许根据内容语义转换为：

```text
精炼后的 Comparison Table
Metric Cards
Bar / Line Chart
Heatmap
Radar Chart（确实适合时）
Persona Cards
2×2 Matrix
Timeline
Process Diagram
Ranking
Key Takeaways
Table + Chart
Table + Cards
其他更适合快速理解的可视化组件
```

例如：

```text
T02：包含大量用户画像长文本
→ 提取年龄 / 性别 / 首购率 / 偏好等核心数据
→ Persona Cards + 对比矩阵

T04：包含多个车型指标数字
→ 提取关键数值
→ Bar Chart + 精炼对比表
```

因此遵循：

> **Source Table 必须被覆盖和转换，但不要求原样保留。**

---


# 5、禁止“未处理就删除” Source Table

huashu-design 可以在本 Skill 的 Design Contract 约束下重新设计：

```text
表头
字体
颜色
背景
Border
圆角
阴影
Padding
Row Height
Hover
Zebra Striping
重点列
重点数据
Caption
Table Container
Responsive
Sticky Header
```

但是绝对禁止：

```text
Source Table 没有任何转换结果就直接删除

为了页面简洁直接跳过某张表

只处理“看起来重要”的几张表，其余表格完全不处理

把 Source Table 从最终 HTML 中省略，同时没有任何图 / 表 / 卡片 / 矩阵承接其核心信息

为了缩短页面而删除关键数字、关键对象、关键关系或核心结论

隐藏会影响判断的重要数据
```

允许对原表结构进行重组、压缩、合并和视觉转换，但必须保证其核心信息在最终 HTML 中有明确承接。

---


# 6、表格内部长文本必须进行总结、数据提取与可视化

长文本总结不仅作用于普通段落，也必须作用于表格中的长文本单元格。

```text
长段落
重复文字
冗余解释
复杂叙述
```

对于 Source Table 内部内容，必须优先识别：

```text
关键数字

百分比

单位

对象名称

模型 / 方法 / 产品名称

时间

指标

比较关系

核心结论

重要限定条件
```

如果单元格中存在大段文字，禁止原样搬运到 HTML 表格里。

正确流程：

```text
表格长文本
↓
语义理解
↓
数据 / 标签 / 结论抽取
↓
删除重复和修饰性表达
↓
压缩为高信息密度短文本
↓
根据语义转换为精炼表格 / 图表 / 卡片 / 矩阵
```

原则：

> **保留信息，不保留冗余文字；保留事实，不保留原始啰嗦表达。**

---


# 7、宽表格处理原则

如果 Source Table 很宽：

禁止：

```text
删除列
隐藏列
丢弃数据
```

优先采用：

```css
overflow-x: auto;
```

并结合：

```text
合理 column width
word-break
white-space
responsive wrapper
sticky first column（必要时）
sticky header（必要时）
```

解决显示问题。

---


# 8、允许合理整合 Source Table，但必须保证覆盖关系可追踪

例如 Markdown 中：

```text
T01：模型性能

T02：模型计算量
```

如果字段接近、主题高度相关，可以：

```text
T01 + T02
↓
一个综合表 / 综合图表 / 组合模块
```

但必须明确记录：

```text
该综合模块覆盖：T01 + T02
```

并确保 T01、T02 的核心信息都已经被承接。

因此最终 HTML 中视觉模块数量可以少于 Source Table 数量，但：

```text
Source Table Coverage Rate 必须仍然 = 100%
```

---


# 9、表格设计继续保持高质量

保留 Source Table 不等于机械复制 Markdown 表。

必须对表格做专业视觉设计。

至少考虑：

```text
清晰 Header

合理 Padding

Row Separation

Hover

Zebra Striping（适用时）

重点数据突出

合理 Column Width

长文本换行

Responsive Wrapper

Mobile Horizontal Scroll

Caption

Table Description
```

但是：

> **不要机械复制原表。表格中的长文本必须继续总结、提炼和数据抽取；允许改变表格结构甚至转换为其他可视化形式，但关键事实、关键数字、关键关系和核心结论必须准确保留。**

---


# 10、Generated Table 策略

对于原 Markdown 长文本中存在明显：

```text
A vs B

优点 / 缺点

方法 / 特点 / 效果

阶段 / 工作 / 输出

类型 / 作用 / 场景
```

可以额外创建：

```text
Generated Table
```

建议 HTML 标记：

```html
<table data-generated-table="true">
```

而 Source Table 标记：

```html
<table data-source-table-id="T01">
```

两类必须可以区分。

---


# 11、不要使用 HTML `<table>` 数量判断 Source Table 是否完成覆盖

例如：

```text
Markdown Source Tables = 5
```

最终 HTML 完全可能是：

```text
2 个精炼 Table
1 个 Bar Chart
1 组 Persona Cards
1 个 2×2 Matrix
```

只要它们分别覆盖：

```text
T01
T02
T03
T04
T05
```

则：

```text
Source Table Coverage = 5 / 5 = 100%
PASS
```

因此检查对象应该是：

```text
每一个 Txx 是否存在明确的 Transformation Destination
```

而不是最终 HTML 有多少个 `<table>`。

---

# 9、V2.6：Source Table 内部 Entry / Dimension Coverage

`Txx` 本身不是 Source Table 完整性的最小单位。

每张 Source Table 在 Inventory 阶段必须登记：

```text
Required Dimensions
Required Entries
Exact Facts / Key Values
Required Relationships（如适用）
```

例如原表 5 个独立对象，最终允许：

```text
5 行 Table
→ 3 Cards + 2 Feature Blocks
```

但必须：

```text
Source Table Entry Coverage = 5 / 5
Source Table Required Dimension Coverage = 100%
```

以下不能作为完整 Coverage：

```text
T04 出现在注释中
T04 出现在 data-source-table-id 中
T04 有一个 Destination 名称
Manifest 写 T04 → 某页
```

必须有实际 Content Evidence。

完整规则见 `24-semantic-obligation-and-evidence-contract.md`。
