# 1、输入原则

本 Skill 需要读取的核心输入为：

```text
1. 一份 Markdown 文件（必须）
2. 一份参考 HTML / 设计参考资产（可选）
```

说明：

- Markdown 是必须输入。
- Reference 是可选输入。
- **本版本不再内置默认 HTML 模板。**
- 如果用户没有提供 Reference，就不要强行加载任何默认模板；改为基于内容本身建立 `Design Context Profile`。

禁止：

```text
没有用户 Reference 时，偷偷使用旧模板
把仓库示例当默认模板
只看 Markdown 前几十行就开始设计
只看部分章节
只看参考的截图而不读源文件
```

---

# 2、输入文件完整读取

必须完整读取：

```text
Markdown 全文
+
用户提供的所有 Reference HTML / 图片 / 设计资产（如果存在）
```

Reference 的作用只能是：

```text
学习 Design Language
```

不能让 Reference 变成：

```text
内容事实来源
```

---

# 3、执行前检查 huashu-design

设计阶段首先搜索本机：

```text
huashu-design
```

优先检查：

```text
.agents/skills/
.codex/skills/
skills/
~/.agents/skills/
~/.codex/skills/
~/.workbuddy/skills/
项目内 .workbuddy/skills/
```

找到后必须完整阅读：

```text
SKILL.md
README.md
references/
assets/
scripts/
demos/
```

以及该 Skill 明确要求的其他相关文件。

同时必须完整读取本 Skill 自己的：

```text
references/10-huashu-design-contract.md
references/11-huashu-visualization-motion-routing.md
references/12-display-mode-and-presentation.md
references/13-complete-design-input-contract.md
references/14-huashu-design-critique-routing.md
references/15-direction-prototype-contract.md
references/16-run-state-and-persistence.md
references/17-render-ready-transformation-boundary.md
references/18-selected-design-system-snapshot.md
references/19-presentation-main-deck-and-appendix.md
references/20-qa-gates-and-repair-budget.md
```

---

# 4、如果找不到 huashu-design

如果确实无法找到：

```text
huashu-design
```

则：

1. 继续搜索当前环境所有可能的 Skill 目录。
2. 若本机确实没有，从官方仓库安装：

```text
https://github.com/alchaincyf/huashu-design
```

官方推荐：

```bash
npx skills add alchaincyf/huashu-design
```

如果 Skills CLI 版本过旧导致只安装 `SKILL.md` 而缺少子目录，优先升级后重装：

```bash
npm i -g skills@latest
# 或
npx skills@latest add alchaincyf/huashu-design
```

Codex 中的手动安装示例：

```bash
git clone --depth 1 https://github.com/alchaincyf/huashu-design.git ~/.codex/skills/huashu-design
# 或项目级
# git clone --depth 1 https://github.com/alchaincyf/huashu-design.git .codex/skills/huashu-design
```

安装后必须确认至少存在：

```text
SKILL.md
references/
assets/
scripts/
demos/
```

---

# 5、执行前检查 frontend-visual-qa

还需要在执行 QA 前定位：

```text
frontend-visual-qa
```

优先检查：

```text
.agents/skills/
.codex/skills/
skills/
~/.agents/skills/
~/.codex/skills/
~/.workbuddy/skills/
项目内 .workbuddy/skills/
```

找到后必须完整阅读其当前版本中与本次任务相关的：

```text
SKILL.md
README.md（如果存在）
references/
scripts/
tests/
evals/
```

并理解其当前 QA 边界。

---

# 6、如果找不到 frontend-visual-qa

如果本机确实没有，则只允许从其官方上游仓库获取：

```text
https://github.com/daymade/claude-code-skills
```

目标 Skill 目录：

```text
frontend-visual-qa/
```

可优先尝试：

```bash
npx skills add https://github.com/daymade/claude-code-skills --skill "frontend-visual-qa"
```

如果 CLI 不能精确安装单个子 Skill，则采用 Git 方式：

```bash
git clone --depth 1 https://github.com/daymade/claude-code-skills.git /tmp/daymade-claude-code-skills
```

然后把：

```text
/tmp/daymade-claude-code-skills/frontend-visual-qa/
```

完整复制到：

```text
~/.codex/skills/frontend-visual-qa/
# 或 .codex/skills/frontend-visual-qa/
```

并检查当前上游版本实际需要的：

```text
SKILL.md
references/
scripts/
tests/
evals/
```

---

# 7、两个外部 Skill 的通用安装原则

禁止：

```text
只复制 SKILL.md 单文件
安装不完整目录后假装已可用
因为安装失败而偷偷换成其他 Skill
```

如果最终仍无法找到或安装失败：

```text
huashu-design 未找到
或
frontend-visual-qa 未找到
```

必须在最终 `analysis.md` 中明确记录相应阻塞状态，不得伪装为已执行。


---

# 8、Huashu Expert Critique 依赖【新增】

进入最终 QA 前，必须从当前安装版本 `huashu-design` 中定位其设计评审入口。

当前上游通常为：

```text
huashu-design/references/critique-guide.md
```

但不要把该文件复制进本 Skill。

正确做法是：

```text
读取当前安装版本 huashu-design/SKILL.md
↓
找到当前 critique / expert review 路由
↓
读取它当前要求的评审 references
↓
执行 Huashu Design Critique
```

这样 Huashu 上游更新后，本 Skill 不会维护一套过期的复制版评审规则。
