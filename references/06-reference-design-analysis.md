# 1、Reference 是可选设计输入，不是默认模板

本版本中：

```text
Reference HTML / 设计参考资产 = Optional
```

规则：

- 如果用户提供了 Reference，则学习其设计语言。
- 如果用户没有提供 Reference，则**不要加载任何默认模板**。
- 没有 Reference 时，必须建立：

```text
Design Context Profile
```

而不是去寻找“系统自带模板”。

---

# 2、如果用户提供了 Reference，如何使用

参考 HTML 不是代码模板。

不要：

```text
复制 DOM
复制 class
复制 CSS
复制 JS
复制组件
复制 SVG
复制文案
复制图片
```

正确流程：

```text
Reference HTML / 设计参考资产
↓
设计观察
↓
设计特征抽象
↓
Reference Design Profile
↓
基于 Markdown 重新设计
```

至少分析：

```text
Layout
Content Width
Grid
Typography
Color
Spacing
Cards
Border
Radius
Shadow
Images
Tables
Navigation
Information Density
Visual Rhythm
Responsive Logic
```

---

# 3、如果用户没有提供 Reference，建立 Design Context Profile

至少分析：

```text
Document Type
Audience
Usage Scenario
Content Density
Data Density
Tone / Temperament
Brand Context（若有）
User Preference（若有）
Interaction Need
Motion Opportunity
Visual Constraints
```

这份 `Design Context Profile` 将与 `Design Input Package` 一起交给 Huashu 用于三方向设计探索。

---

# 4、三方向比较时，Reference / Context 的作用

不论是使用：

```text
Reference Design Profile
```

还是：

```text
Design Context Profile
```

其作用都只是约束设计语言与风格方向。

三方向比较时，允许改变：

```text
Layout
Typography
Color
Composition
Data Visualization
Information Density
Visual Rhythm
Motion Language
```

禁止改变：

```text
内容范围
事实
数字
结论
逻辑关系
```

因此用户比较的是：

```text
哪个设计方向更喜欢
```

而不是：

```text
哪份报告内容看起来不一样
```
