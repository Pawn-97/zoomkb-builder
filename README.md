# Zoom Support KB Builder · 极光支持知识库构建器

> Build structured, design-facing knowledge bases from Zoom Support Center articles.
> 从 Zoom 支持中心文章构建面向设计的结构化知识库。

[English](#english) | [中文](#中文)

---

## English

### Overview

Zoom Support KB Builder crawls Zoom's official support articles and transforms them into a **design-facing knowledge base** (a "wiki layer"). It extracts concept pages, user-role descriptions, task flows, constraints, and UX patterns — all sourced from raw articles but compiled into design knowledge by an LLM.

**Pipeline:** `sitemap discovery → crawl (JSON-LD) → classify → validate → ingest (LLM) → lint`

### Installation in Claude Code

#### Prerequisites

- Python 3.9+
- [Claude Code](https://claude.ai/code) installed
- OpenAI API key (for the LLM ingest phase)

#### Step 1 — Clone and install the Python package

```bash
git clone https://github.com/Pawn-97/zoomkb-builder.git
cd zoomkb-builder
python3 -m venv .venv && source .venv/bin/activate  # Create & activate venv
pip install setuptools wheel                        # Ensure build deps available
pip install -e .          # Core (crawl, discover, validate)
pip install -e ".[llm]"   # + LLM ingest support
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

#### Step 3 — Set environment variables

```bash
export OPENAI_API_KEY="sk-..."           # Required for ingest
export ZOOMKB_LLM_MODEL="gpt-4o-mini"    # Optional model override
```

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
| `/zoomkb:init` | Initialize KB directory structure |
| `/zoomkb:discover` | Discover candidate articles from Zoom sitemaps |
| `/zoomkb:crawl` | Crawl and extract articles (JSON-LD primary, Trafilatura fallback) |
| `/zoomkb:validate` | Validate raw articles for quality |
| `/zoomkb:ingest` | Generate wiki pages via LLM extraction |
| `/zoomkb:lint` | Quality checks (traceability, coverage, consistency, freshness) |

See [SKILL.md](SKILL.md) for full CLI options and flags.

### Update & Maintenance

```bash
cd zoomkb-builder
git pull origin main                     # Get latest code
pip install -e ".[llm]"                  # Re-install to pick up dependency changes
```

After pulling, verify the skill definition is still current:

```bash
cp SKILL.md ~/.claude/skills/zoomkb/SKILL.md   # Update the skill definition
```

Check for new releases or breaking changes in the [GitHub repo](https://github.com/Pawn-97/zoomkb-builder).

### Architecture

```
raw/support-articles/*.md   ← Source of truth (never LLM-rewritten)
  ↓ LLM ingest (prepare → extract → commit)
wiki/concepts/*.md          ← Design-facing knowledge (dedup + quality filtered)
wiki/task-flows/*.md
wiki/user-roles/*.md
wiki/constraints/*.md
wiki/ux-patterns/*.md
```

Extracted entities go through three-stage dedup (exact slug → normalized slug → title Jaccard similarity) and are filtered with `--min-sources` and `--min-quality` to remove thin pages.

### Requirements

| Dependency | Purpose |
|------------|---------|
| `pip install -e .` | Core: crawl, discover, validate, lint |
| `pip install -e ".[llm]"` | LLM ingest via OpenAI |
| `pip install -e ".[dev]"` | Tests, linting, type checking |
| `OPENAI_API_KEY` | Required for ingest phase |
| `ZOOMKB_CRAWL4AI=1` | Optional headless browser extraction |

---

## 中文

### 概述

极光支持知识库构建器（Zoom Support KB Builder）爬取 Zoom 官方支持文章，并将其转化为**面向设计的知识库**（"wiki 层"）。它提取概念页面、用户角色描述、任务流程、约束条件和 UX 模式 —— 全部来源于原始支持文章，但通过 LLM 编译成设计知识。

**流水线：** `站点地图发现 → 爬取 (JSON-LD) → 分类 → 验证 → LLM 提取 → 质量检查`

### 在 Claude Code 中安装

#### 前置条件

- Python 3.9+
- 已安装 [Claude Code](https://claude.ai/code)
- OpenAI API Key（用于 LLM 提取阶段）

#### 第一步 — 克隆仓库并安装 Python 包

```bash
git clone https://github.com/Pawn-97/zoomkb-builder.git
cd zoomkb-builder
python3 -m venv .venv && source .venv/bin/activate  # 创建并激活虚拟环境
pip install setuptools wheel                        # 确保构建依赖可用
pip install -e .          # 核心功能（爬取、发现、验证、质量检查）
pip install -e ".[llm]"   # + LLM 提取支持
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

#### 第三步 — 设置环境变量

```bash
export OPENAI_API_KEY="sk-..."           # ingest 阶段必需
export ZOOMKB_LLM_MODEL="gpt-4o-mini"    # 可选：指定模型
```

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
| `/zoomkb:init` | 初始化知识库目录结构 |
| `/zoomkb:discover` | 从 Zoom 站点地图发现候选文章 |
| `/zoomkb:crawl` | 爬取并提取文章内容（优先 JSON-LD，备用 Trafilatura） |
| `/zoomkb:validate` | 验证原始文章质量 |
| `/zoomkb:ingest` | 通过 LLM 提取生成 wiki 页面 |
| `/zoomkb:lint` | 质量检查（可追溯性、覆盖度、一致性、新鲜度） |

详见 [SKILL.md](SKILL.md) 获取完整 CLI 参数和选项。

### 更新与维护

```bash
cd zoomkb-builder
git pull origin main                     # 拉取最新代码
pip install -e ".[llm]"                  # 重新安装以同步依赖变更
```

拉取后确认技能定义是最新的：

```bash
cp SKILL.md ~/.claude/skills/zoomkb/SKILL.md   # 更新技能定义
```

关注 [GitHub 仓库](https://github.com/Pawn-97/zoomkb-builder) 获取新版本和变更通知。

### 架构

```
raw/support-articles/*.md   ← 原始来源（永不被 LLM 改写）
  ↓ LLM 提取（准备 → 提取 → 提交）
wiki/concepts/*.md          ← 设计知识（经过去重和质量过滤）
wiki/task-flows/*.md
wiki/user-roles/*.md
wiki/constraints/*.md
wiki/ux-patterns/*.md
```

提取后的实体经过三阶段去重（精确 slug → 归一化 slug → 标题 Jaccard 相似度），并按照 `--min-sources`（最低来源数）和 `--min-quality`（最低质量分）过滤瘦页面。

### 依赖

| 依赖 | 用途 |
|------------|---------|
| `pip install -e .` | 核心：爬取、发现、验证、质量检查 |
| `pip install -e ".[llm]"` | LLM 提取（OpenAI） |
| `pip install -e ".[dev]"` | 测试、代码检查、类型检查 |
| `OPENAI_API_KEY` | ingest 阶段必需 |
| `ZOOMKB_CRAWL4AI=1` | 可选：无头浏览器提取 |

---

## License

MIT
