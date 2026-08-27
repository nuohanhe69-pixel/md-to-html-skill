# Presentation Artifact Build & Integrity Contract

本文件定义 Presentation 在视觉设计完成后，如何被**安全地组装成可运行的多文件 HTML Deck**。

它不负责：

```text
Content Engineering
Semantic Coverage 决策
Source Table Transformation
Design Direction 选择
Huashu Design Critique
```

它只负责：

> **把已经确定的 Presentation 设计正确写成 HTML / CSS / JS / Manifest / Media，并保证这些 Artifact 没有被错误 Writer 覆盖。**

---

# 1、为什么必须单独存在 Artifact Build Layer

Presentation 不是单文件报告，而是一个运行时文件集合：

```text
Shell
+
Slides
+
Shared Styles
+
Runtime Scripts
+
Deck Manifest
+
Media Assets
```

因此：

```text
Content Correct
+
Design Correct
```

并不自动等于：

```text
Artifact Correct
```

典型失败：

```text
shared.css 本应是纯 CSS
↓
被 Batch HTML Writer 包成 <html>...</html>
↓
iframe 能加载 Slide HTML
↓
浏览器把 shared.css 当 CSS 解析
↓
CSS 全部失效
↓
Slides 白屏 / 无样式
```

这属于：

```text
Presentation Artifact-Type Violation
```

不是 Semantic Coverage Bug，也不是 Huashu Design Direction Bug。

---

# 2、推荐的 Portable Presentation 目录

默认推荐：

```text
presentation/
├── index.html
├── deck-manifest.js
├── assets/
│   ├── css/
│   │   └── shared.css
│   ├── js/
│   │   └── deck-runtime.js      （需要时）
│   └── images/
└── slides/
    ├── 01-cover.html
    ├── 02-....html
    ├── ...
    ├── A01-....html
    └── ...
```

硬约束：

```text
slides/
= Slide HTML only

assets/css/
= Stylesheet only

assets/js/
= JavaScript only
```

禁止把 `_shared.css`、runtime JS、Manifest 等非 Slide Artifact 混放到 `slides/` 后再通过“扫描目录”批量处理。

所有运行时引用必须优先使用相对路径；最终 Presentation 不得依赖 `~/.codex/skills/...`、`.agents/skills/...` 等本机 Skill 绝对路径。

---

# 3、Build-time Presentation Artifact Manifest【必须落盘】

在真正写文件前，必须建立：

```text
workspace/presentation-artifact-manifest.md
```

它至少为每一个当前版本运行时 Artifact 记录：

```text
path
artifact_type
write_owner
writer_type
write_phase
mutable_after_phase
dependencies
```

Artifact Type 至少包括：

```text
HTML_SHELL
HTML_SLIDE
STYLESHEET
SCRIPT
RUNTIME_MANIFEST
MEDIA_ASSET
```

示例：

```text
path: presentation/assets/css/shared.css
artifact_type: STYLESHEET
write_owner: SHARED_ASSET_GENERATOR
writer_type: CSS_RAW_WRITER
write_phase: SHARED_ASSET_BUILD
mutable_after_phase: false
```

以及：

```text
path: presentation/slides/01-cover.html
artifact_type: HTML_SLIDE
write_owner: SLIDE_GENERATOR
writer_type: HTML_SLIDE_WRITER
write_phase: SLIDE_BATCH_BUILD
mutable_after_phase: false
```

---

# 4、Artifact Type → Writer Routing【硬约束】

必须：

```text
HTML_SHELL
→ HTML_DOCUMENT_WRITER

HTML_SLIDE
→ HTML_SLIDE_WRITER

STYLESHEET
→ CSS_RAW_WRITER

SCRIPT
→ JAVASCRIPT_WRITER

RUNTIME_MANIFEST
→ MANIFEST_SERIALIZER / JS_MANIFEST_WRITER

MEDIA_ASSET
→ BINARY / ASSET COPY PIPELINE
```

禁止：

```text
STYLESHEET → HTML_DOCUMENT_WRITER
SCRIPT → HTML_DOCUMENT_WRITER
RUNTIME_MANIFEST → HTML_DOCUMENT_WRITER
MEDIA_ASSET → HTML_DOCUMENT_WRITER
```

任何非 HTML Artifact 出现：

```text
<!DOCTYPE html>
<html
<head
<body
```

都必须视为高优先级 Artifact Type Violation，除非该 Artifact Type 本来就是 HTML。

---

# 5、Single Writer Ownership【硬约束】

一个运行时 Artifact 只能有一个 Write Owner。

例如：

```text
shared.css
owner = SHARED_ASSET_GENERATOR
```

允许：

```text
Slide Generator READ shared.css
Shell READ shared.css / manifest
QA READ all artifacts
```

禁止：

```text
Slide Generator WRITE shared.css
Shell Generator 覆盖 shared.css
QA Rewrite shared.css
```

---

# 6、Shared Assets 必须先生成、后锁定

正确顺序：

```text
Shared Asset Build
↓
shared.css / runtime.js / media
↓
记录 hash / integrity fingerprint
↓
LOCK
↓
Slide Batch Build
↓
再次核对 fingerprint
```

必须满足：

```text
Shared Asset Hash Before Slide Batch
=
Shared Asset Hash After Slide Batch
```

如果不同：

```text
Shared Asset Mutation = FAIL
```

如果环境不适合计算 cryptographic hash，也至少要进行等价的内容 fingerprint / size + checksum 检查；不能什么都不检查。

---

# 7、Deck Manifest 是 Runtime SSOT【硬约束】

推荐直接打开的 HTML Deck 使用：

```text
presentation/deck-manifest.js
```

例如：

```javascript
window.DECK_MANIFEST = {
  title: "Example",
  canvas: { width: 1920, height: 1080 },
  slides: [
    { id: "01", file: "slides/01-cover.html", title: "封面", section: "main" },
    { id: "02", file: "slides/02-overview.html", title: "总览", section: "main" },
    { id: "A01", file: "slides/A01-detail.html", title: "附录", section: "appendix" }
  ]
};
```

如果使用 JSON Manifest，必须确保目标运行环境能够可靠加载；对于需要直接 `file://` 打开的独立 Deck，优先使用无需 fetch 的 JS Manifest 或 Huashu 当前等价机制。

以下全部必须从同一份 Manifest 派生：

```text
Slide Count
Current / Total Counter
Overview Cards
Jump Select
Main / Appendix 分组
Previous / Next Boundary
Appendix 编号
Slide Title
```

禁止：

```text
HTML 写死 “1 / 14”
但 Manifest 实际有 17 Slides

靠 i - 11 推导 Appendix 序号

Overview 用一套 Slide List
Jump Select 再维护一套 Slide List
```

正确：

```text
Manifest slides.length
= 唯一 Total Slide Count

Manifest slide.id
= 唯一显示编号来源
```

---

# 8、Manifest-driven Build，禁止目录扫描驱动生成

正确：

```text
for slide in Deck Manifest.slides
→ render_slide(slide)
```

禁止：

```text
for file in presentation/slides/
→ 把目录里的每个文件都当 Slide 重新生成
```

原因：目录扫描会把非 Slide Artifact、残留文件或错误文件卷入 Batch Writer。

当前版本目录必须从空的新版本目录开始构建，不得把旧版本残留 Artifact 作为当前 Manifest 的隐式输入。

---

# 9、Presentation Build 必须拆成明确阶段

推荐顺序：

```text
BUILD-A
建立 Build-time Presentation Artifact Manifest
+
建立 Runtime Deck Manifest

BUILD-B
生成 Shared Assets
→ LOCK

BUILD-C
仅根据 Deck Manifest 批量生成 slides/*.html

BUILD-D
根据同一 Deck Manifest 生成 index.html / runtime navigation

BUILD-E
建立 Dependency Map
+
执行 Artifact Integrity Gate
```

不得使用一个“通用 HTML 模板循环”一次性写所有扩展名文件。

---

# 10、Artifact Dependency Map

必须验证：

```text
每个 Slide 引用的 CSS 存在
每个 Slide 引用的 JS 存在
每个 Slide 引用的 Image / Media 存在
index.html 引用的 Manifest 存在
Manifest 中列出的每个 Slide 文件存在
```

并确认：

```text
所有路径在最终交付目录中可解析
```

不能依赖生成机器之外的临时目录。

---

# 11、Artifact Integrity Gate【Frontend Render QA 之前】

Presentation 进入浏览器 Render QA 前必须通过：

```text
Artifact Registry Complete = PASS
Artifact Type / Writer Routing = PASS
Runtime Deck Manifest Parse / Execute = PASS
Manifest Slide Paths Exist = PASS
Manifest Slide Count = Runtime Slide Count = PASS
Main / Appendix Metadata = PASS
Asset Dependency Resolution = PASS
Shared Asset Lock / Fingerprint = PASS
No HTML Wrapper in CSS / JS = PASS
No Stale Unregistered Runtime Artifact = PASS
```

CSS 至少检查：

```text
存在
非空
不是 HTML Document
能作为 Stylesheet 被浏览器加载
```

JS 至少检查：

```text
存在
不是 HTML Document
关键语法 / runtime load 正常
```

Manifest 至少检查：

```text
可解析 / 可执行
Slide entries 唯一
id 唯一
file path 唯一且存在
section 合法：main | appendix
```

---

# 12、Browser Render QA 负责验证“真的加载成功”

Artifact Gate PASS 后，`frontend-visual-qa` 再负责实际浏览器验证。

至少覆盖代表性页面：

```text
Cover
Main 中间页
Main 最后一页
Appendix 第一页
Appendix 最后一页
```

检查：

```text
iframe Loaded
Stylesheet Loaded
Fonts / Images Loaded
Slide Overflow = ZERO（关键页面）
Navigation = PASS
Overview = PASS
Main → Appendix = PASS
Counter / Jump / Overview 与 Manifest 一致
Console Critical Error = ZERO
```

注意：

```text
Artifact Gate
= 文件结构 / 类型 / 依赖是否正确

Frontend Render QA
= 浏览器里是否真的正确跑出来
```

二者不能互相替代。

---

# 13、Artifact Failure 的局部回滚规则

如果：

```text
Content Integrity = PASS
Selected Design System = LOCKED
Presentation Artifact = FAIL
```

禁止：

```text
重新读 Raw Markdown
重新做 Content Engineering
重新建立 Cxxx / Txx
重新选择 Prototype
重新总结业务内容
```

正确：

```text
保留 Complete Design Input Package
保留 Selected Design Direction Contract
保留 Selected Design System Snapshot
保留 Main / Appendix Routing
↓
回滚到失败的 Artifact Build Phase
↓
修复 Artifact
↓
Artifact Integrity QA
↓
受影响的 Frontend Render QA
↓
最终完整 Regression QA
```

例如：

```text
shared.css Artifact Type FAIL
↓
只重建 shared.css
↓
重新验证 Asset Lock / Dependencies
↓
重新验证代表性 Slides
```

---

# 14、Run State

Artifact Build 期间必须允许：

```text
PRESENTATION_ARTIFACT_BUILD
PRESENTATION_ARTIFACT_QA
PRESENTATION_ARTIFACT_BLOCKED
```

`run-state.json` 必须记录：

```text
presentation_artifact_manifest_path
deck_manifest_path
artifact_build_status
artifact_qa_status
shared_asset_integrity_status
last_artifact_failure
```

这样跨会话恢复时可以从 Artifact Build 继续，而不是重做内容工程。

---

# 15、与现有规则的边界

```text
Main Deck / Appendix 内容路由
→ references/19-presentation-main-deck-and-appendix.md

Presentation 的模式定义
→ references/12-display-mode-and-presentation.md

QA 总编排
→ references/08-qa-and-repair.md

PASS / FAIL Gate 与 Repair Budget
→ references/20-qa-gates-and-repair-budget.md

实际浏览器 Reviewer
→ references/14-huashu-design-critique-routing.md
```

本文件是 Presentation Artifact Build / Integrity 的唯一 Canonical Owner。


---

# 15、Motion Runtime Artifact 仍受本 Contract 约束【V2.5】

如果 `references/23-presentation-motion-choreography.md` 产生：

```text
motion runtime JS
transition CSS
per-slide motion metadata
shared animation utilities
```

它们仍然必须进入正常 Artifact Registry，并遵守：

```text
Artifact Type
Writer Routing
Single Writer Ownership
Shared Asset Lock
Dependency Resolution
Deck Manifest SSOT
```

禁止为了 Motion 方便而：

```text
临时把 JS 写进 .css
把 Motion Manifest 变成第二份 Slide List
绕过 Shared Asset Fingerprint
在 Slide Batch 里重写 shared motion runtime
```
