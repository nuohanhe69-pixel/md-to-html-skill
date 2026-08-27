# Presentation Main Deck + Appendix Contract

本文件解决 Presentation Mode 在坚持 100% Semantic Coverage 时可能无限变长、失去真实汇报价值的问题。

核心原则：

> **100% Coverage 不等于所有内容都进入 Main Deck。**

---

# 1、Presentation 必须具有两层信息架构

逻辑结构：

```text
Presentation
├── Main Deck
│   ├── 核心问题
│   ├── 核心洞察
│   ├── 核心证据
│   ├── 核心结论
│   └── 必要行动 / 建议
│
└── Appendix / Backup Slides
    ├── 详细数据
    ├── 完整 Source Table / Supporting Table
    ├── 次级分析维度
    ├── 补充 Persona
    ├── 方法细节
    └── 完整证据 / 追溯内容
```

Main Deck 负责“可讲述”；Appendix 负责“完整支撑”。

---

# 2、Coverage 仍然是 100%

```text
Main Deck Coverage
+
Appendix Coverage
=
Presentation Semantic Coverage = 100%
```

Source Table 同理：

```text
Main Deck Txx
+
Appendix Txx
=
Presentation Source Table Coverage = 100%
```

禁止把 Appendix 当成“可选不做”。

---

# 3、内容路由规则

每个 Cxxx / Txx 在生成 Presentation 前都要标记：

```text
MAIN
APPENDIX
MAIN + APPENDIX
```

建议：

```text
核心结论 → MAIN
核心趋势 / 核心证据 → MAIN
复杂支撑表 → MAIN 概览 + APPENDIX 明细
次级画像维度 → APPENDIX 或必要时 MAIN
方法细节 → APPENDIX
关键风险 → MAIN
完整追溯表 → APPENDIX
```

例如：

```text
T04
→ Main Deck：Overview Chart + 3 Key Findings
→ Appendix：Detailed Table + Full Notes
```

---

# 4、Main Deck 不能为了“短”而扭曲语义

禁止：

```text
只保留一个结论但删除反例
只保留漂亮数据而删除风险
为了 20 页上限硬删重要维度
把所有复杂内容都丢到 Appendix 导致 Main Deck 失去证据
```

Main Deck 的目标不是固定页数，而是：

```text
可讲述
有证据
主次清晰
节奏合理
```

---

# 5、Main / Appendix 与 Deck Manifest 的逻辑关系

下面目录继续作为 Main / Appendix 结构示例保留；**Artifact Build 的最终物理目录、Writer Routing 与 Asset 分层以 `references/22-presentation-artifact-integrity-contract.md` 为 Canonical Owner。**

示例：

```text
presentation/
├── index.html
├── deck-manifest.json
└── slides/
    ├── 01-cover.html
    ├── 02-....html
    ├── ...
    ├── 18-summary.html
    ├── A01-....html
    ├── A02-....html
    └── ...
```

Runtime Deck Manifest 应标记：

```text
section: main | appendix
```

如果 Huashu 当前版本使用其他 Deck Manifest 结构，以当前上游为准，但逻辑上的 Main / Appendix 分组必须保留；同时必须满足 `22-presentation-artifact-integrity-contract.md` 的 Runtime SSOT 与 Artifact Integrity 要求。

---

# 6、导航体验

Presentation 必须支持：

```text
Main Deck 正常顺序播放
Main Deck 结束后可进入 Appendix
Overview / Gallery 能区分 Main / Appendix
Appendix 可被单独跳转
返回 Main Deck 不破坏当前设计语言
```

---

# 7、QA

Presentation QA 额外检查：

```text
Main Deck Narrative = PASS
Appendix Completeness = PASS
Main + Appendix Coverage = 100%
Core Evidence not hidden only in Appendix = PASS
Source Table Traceability = PASS
```


---

# 8、Main Deck 与 Appendix 的 Motion 职责

Presentation 的动态密度不应平均分配：

```text
Main Deck
→ 时间叙事 / 讲述优先
→ Motion Choreography 可以更积极

Appendix
→ 查询 / 查证优先
→ 默认 LOW Motion / Static
```

但 Main Deck 的动态表达不能替代 Appendix 的完整性，也不能让任何 Cxxx / Txx 只存在于瞬时动画帧。

完整规则见：

```text
references/23-presentation-motion-choreography.md
```

---

# 9、V2.6：Main / Appendix 路由按 Obligation 证明完整性

每个 `DUxxx` / `Cxxx` / `Txx` 的路由必须保留 `Semantic Obligation Refs`。

例如：

```text
T04.E01 → MAIN
T04.E02 → MAIN
T04.E03 → MAIN
T04.E04 → APPENDIX
T04.E05 → APPENDIX
```

或者：

```text
T04.E01-E05 → MAIN + APPENDIX
```

均可。

禁止仅写：

```text
T04 → A03
```

就把 T04 判为 100% Coverage；必须在 `coverage-evidence-ledger.md` 中证明 T04 的 Required Entries / Dimensions 在 Main + Appendix 中均有实际承接。
