# Zoom Support KB Builder · Zoom-UX知识库构建器

> Build structured, design-facing knowledge bases from Zoom Support Center articles.
> 从 Zoom 支持中心文章构建面向设计的结构化知识库。

[English](#english) | [中文](#中文)

---

## English

### Overview

Zoom Support KB Builder crawls Zoom's official support articles and transforms them into a **design-facing knowledge base** (a "wiki layer"). It extracts concept pages, user-role descriptions, task flows, constraints, and UX patterns — all sourced from raw articles but compiled into design knowledge by Claude Code.

**Pipeline:** `sitemap discovery → crawl (JSON-LD) → classify → validate → ingest (Claude Code extract) → lint`

### Installation in Claude Code

#### Prerequisites

- Python 3.9+
- [Claude Code](https://claude.ai/code) installed

#### Step 1 — Clone and install the Python package

```bash
git clone https://github.com/Pawn-97/zoomkb-builder.git
cd zoomkb-builder
python3 -m venv .venv && source .venv/bin/activate  # Create & activate venv
pip install setuptools wheel                        # Ensure build deps available
pip install -e .          # Core (crawl, discover, validate, lint, refresh)
```

> **macOS SSL fix:** If `pip install -e .` fails with `SSL: CERTIFICATE_VERIFY_FAILED`, re-run with:
> ```bash
> pip install --no-build-isolation -e .
> ```
> This skips the isolated build environment (setuptools/wheel must be pre-installed). Apple's Command Line Tools Python uses LibreSSL which lacks system root certificates — install Python via [Homebrew](https://brew.sh) (`brew install python`) for a permanent fix.

#### Step 2 — Register the skill in Claude Code

Copy the skill definition into your Claude Code skills directory so the `/zoomkb:*` slash commands are available in any project:

```bash
mkdir -p ~/.claude/skills/zoomkb
cp SKILL.md ~/.claude/skills/zoomkb/SKILL.md
```

Alternatively, register it per-project by placing `SKILL.md` in your project's `.claude/skills/zoomkb/` directory.

#### Cursor compatibility

This repository also ships project rules under `.cursor/rules/`:

- `zoomkb.mdc` gives Cursor agents the project architecture, run commands, and KB invariants.
- `neat-freak.mdc` makes the end-of-session documentation cleanup skill available from Cursor when the user asks to sync, tidy, or hand off the project.

Cursor does not consume Claude Code slash commands directly. In Cursor, run the Python CLI from the terminal (`zoomkb ...`) and let the project rules provide agent context.

#### Step 3 — Set environment variables

All environment variables are optional. The ingest phase uses Claude Code's built-in LLM — no API key required.

```bash
export ZOOMKB_CRAWL4AI=1                  # Optional: headless browser fallback for JS-heavy pages
```

**LLM-based relevance classifier** (advanced, requires openai package):

```bash
pip install openai
export OPENAI_API_KEY="sk-..."            # Required for classifier
export ZOOMKB_LLM_MODEL="gpt-4o-mini"     # Optional: model override
export ZOOMKB_LLM_CLASSIFIER=1            # Enable LLM-based classification
```

The default rule-based classifier works without any API keys and is sufficient for most use cases.

Add these to your shell profile (`.zshrc`, `.bashrc`, or `config.fish`) for persistence.

#### Step 4 — Verify

```bash
zoomkb --help
```

In Claude Code, type `/zoomkb:build --product "Zoom Phone"` to run the full pipeline.

### Usage

| Command | Purpose |
|---------|---------|
| `/zoomkb:build` | One-shot full pipeline (init → discover → crawl → validate → ingest → lint) |
| `/zoomkb:build-all` | Initialize KB directories for all 6 product lines |
| `/zoomkb:init` | Initialize KB directory structure |
| `/zoomkb:discover` | Discover candidate articles from Zoom sitemaps |
| `/zoomkb:crawl` | Crawl and extract articles (JSON-LD primary, Trafilatura fallback) |
| `/zoomkb:validate` | Validate raw articles for quality |
| `/zoomkb:ingest` | Generate wiki pages via Claude Code extraction (prepare → extract → commit) |
| `/zoomkb:refresh` | Re-crawl accepted articles, detect content changes |
| `/zoomkb:freshness` | Generate source freshness/staleness report |
| `/zoomkb:lint` | Quality checks (traceability, coverage, consistency, freshness) |

See [SKILL.md](SKILL.md) for full CLI options and flags.

### Update & Maintenance

```bash
cd zoomkb-builder
git pull origin main                     # Get latest code
pip install -e .                          # Re-install to pick up dependency changes
```

After pulling, verify the skill definition is still current:

```bash
cp SKILL.md ~/.claude/skills/zoomkb/SKILL.md   # Update the skill definition
```

Check for new releases or breaking changes in the [GitHub repo](https://github.com/Pawn-97/zoomkb-builder).

### Architecture

```
raw/support-articles/*.md   ← Source of truth (never LLM-rewritten)
  ↓ Claude Code extract (prepare → extract → commit)
wiki/concepts/*.md          ← Design-facing knowledge (dedup + quality filtered)
wiki/task-flows/*.md
wiki/user-roles/*.md
wiki/constraints/*.md
wiki/ux-patterns/*.md
```

Extracted entities go through three-stage dedup (exact slug → normalized slug → title Jaccard similarity) and are filtered with `--min-sources` and `--min-quality` to remove thin pages.
Discovery review files live under `review/`: `candidate-articles.json`, `rejected-articles.json`, `low-confidence/`, and `rejected/`.

### Repository layout

- `src/zoomkb/` — Python package and CLI implementation.
- `tests/` — pytest suite for ingest, lint, validation, and UX-partner compatibility.
- `references/` — current architecture, CLI, and integration references.
- `docs/ideas/` — historical product and implementation planning notes.
- `docs/reports/` — historical validation and test reports.
- `zoom-phone-kb/` — checked-in sample KB output.

### Requirements

| Dependency | Purpose |
|------------|---------|
| `pip install -e .` | Core: crawl, discover, validate, lint, refresh |
| `pip install openai` + `OPENAI_API_KEY` | Optional: LLM-based relevance classifier |
| `pip install -e ".[dev]"` | Tests, linting, type checking |
| `ZOOMKB_CRAWL4AI=1` | Optional: headless browser extraction |

---

## 中文

### 概述

Zoom-UX知识库构建器（Zoom Support KB Builder）爬取 Zoom 官方支持文章，并将其转化为**面向设计的知识库**（"wiki 层"）。它提取概念页面、用户角色描述、任务流程、约束条件和 UX 模式 —— 全部来源于原始支持文章，但通过 LLM 编译成设计知识。

**流水线：** `站点地图发现 → 爬取 (JSON-LD) → 分类 → 验证 → Claude Code 提取 → 质量检查`

### 在 Claude Code 中安装

#### 前置条件

- Python 3.9+
- 已安装 [Claude Code](https://claude.ai/code)

#### 第一步 — 克隆仓库并安装 Python 包

```bash
git clone https://github.com/Pawn-97/zoomkb-builder.git
cd zoomkb-builder
python3 -m venv .venv && source .venv/bin/activate  # 创建并激活虚拟环境
pip install setuptools wheel                        # 确保构建依赖可用
pip install -e .          # 核心功能（爬取、发现、验证、质量检查、刷新）
```

> **macOS SSL 修复：** 如果 `pip install -e .` 失败并提示 `SSL: CERTIFICATE_VERIFY_FAILED`，可重新运行：
> ```bash
> pip install --no-build-isolation -e .
> ```
> 这会跳过隔离的构建环境（需要预先安装 setuptools/wheel）。Apple Command Line Tools 自带的 Python 使用 LibreSSL，缺少系统根证书 —— 通过 [Homebrew](https://brew.sh) 安装 Python（`brew install python`）可获得永久修复。

#### 第二步 — 在 Claude Code 中注册技能

将技能定义文件复制到 Claude Code 的 skills 目录，使 `/zoomkb:*` 斜杠命令在任何项目中可用：

```bash
mkdir -p ~/.claude/skills/zoomkb
cp SKILL.md ~/.claude/skills/zoomkb/SKILL.md
```

也可以按项目注册：将 `SKILL.md` 放到项目根目录的 `.claude/skills/zoomkb/` 中。

#### Cursor 兼容

本仓库同时提供 `.cursor/rules/` 项目规则：

- `zoomkb.mdc` 为 Cursor agent 提供项目架构、运行命令和 KB 不变量。

Cursor 不会直接消费 Claude Code 的斜杠命令。在 Cursor 中请从终端运行 Python CLI（`zoomkb ...`），由项目规则负责提供 agent 上下文。

#### 第三步 — 设置环境变量

所有环境变量均为可选。ingest 阶段使用 Claude Code 内置的 LLM —— 无需 API Key。

```bash
export ZOOMKB_CRAWL4AI=1                  # 可选：无头浏览器回退提取（JS 重页面）
```

**LLM 分类器**（高级功能，需安装 openai 包）：

```bash
pip install openai
export OPENAI_API_KEY="sk-..."            # 必需：供分类器使用
export ZOOMKB_LLM_MODEL="gpt-4o-mini"     # 可选：指定模型
export ZOOMKB_LLM_CLASSIFIER=1            # 启用 LLM 分类
```

默认规则分类器无需任何 API Key，足以应对大多数使用场景。

为确保持久生效，建议将以上变量写入 shell 配置文件（`.zshrc`、`.bashrc` 或 `config.fish`）。

#### 第四步 — 验证安装

```bash
zoomkb --help
```

在 Claude Code 中输入 `/zoomkb:build --product "Zoom Phone"` 运行完整流水线。

### 使用说明

| 命令 | 用途 |
|---------|---------|
| `/zoomkb:build` | 一键运行完整流水线 |
| `/zoomkb:build-all` | 初始化全部 6 条产品线知识库目录 |
| `/zoomkb:init` | 初始化知识库目录结构 |
| `/zoomkb:discover` | 从 Zoom 站点地图发现候选文章 |
| `/zoomkb:crawl` | 爬取并提取文章内容（优先 JSON-LD，备用 Trafilatura） |
| `/zoomkb:validate` | 验证原始文章质量 |
| `/zoomkb:ingest` | 通过 Claude Code 提取生成 wiki 页面 (prepare → extract → commit) |
| `/zoomkb:refresh` | 重新抓取已收录文章，检测内容变更 |
| `/zoomkb:freshness` | 生成来源新鲜度/过期状态报告 |
| `/zoomkb:lint` | 质量检查（可追溯性、覆盖度、一致性、新鲜度） |

详见 [SKILL.md](SKILL.md) 获取完整 CLI 参数和选项。

### 更新与维护

```bash
cd zoomkb-builder
git pull origin main                     # 拉取最新代码
pip install -e .                          # 重新安装以同步依赖变更
```

拉取后确认技能定义是最新的：

```bash
cp SKILL.md ~/.claude/skills/zoomkb/SKILL.md   # 更新技能定义
```

关注 [GitHub 仓库](https://github.com/Pawn-97/zoomkb-builder) 获取新版本和变更通知。

### 架构

```
raw/support-articles/*.md   ← 原始来源（永不被 LLM 改写）
  ↓ Claude Code 提取（准备 → 提取 → 提交）
wiki/concepts/*.md          ← 设计知识（经过去重和质量过滤）
wiki/task-flows/*.md
wiki/user-roles/*.md
wiki/constraints/*.md
wiki/ux-patterns/*.md
```

提取后的实体经过三阶段去重（精确 slug → 归一化 slug → 标题 Jaccard 相似度），并按照 `--min-sources`（最低来源数）和 `--min-quality`（最低质量分）过滤瘦页面。
发现阶段的审核文件位于 `review/`：`candidate-articles.json`、`rejected-articles.json`、`low-confidence/` 和 `rejected/`。

### 仓库结构

- `src/zoomkb/` — Python 包和 CLI 实现。
- `tests/` — ingest、lint、validation、UX-partner 兼容性的 pytest 测试。
- `references/` — 当前架构、CLI 和集成参考文档。
- `docs/ideas/` — 历史产品方案和实现规划笔记。
- `docs/reports/` — 历史验证报告和测试报告。
- `zoom-phone-kb/` — 已纳入版本控制的示例 KB 输出。

### 依赖

| 依赖 | 用途 |
|------------|---------|
| `pip install -e .` | 核心：爬取、发现、验证、质量检查、刷新 |
| `pip install openai` + `OPENAI_API_KEY` | 可选：LLM 相关性分类器 |
| `pip install -e ".[dev]"` | 测试、代码检查、类型检查 |
| `ZOOMKB_CRAWL4AI=1` | 可选：无头浏览器提取 |

---

## License

MIT
