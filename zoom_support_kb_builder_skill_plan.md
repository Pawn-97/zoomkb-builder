# Zoom Support KB Builder skill 方案文档

> 目标：让设计师只需要告诉 AI 目标产品线，例如 **Zoom Phone**，系统就能从官方 Zoom Support Center 自动发现相关 support articles，抓取并转换为 raw markdown，清洗校验后进入 LLM-wiki ingest，最终生成 UX-partner 可用的产品线知识库。

---

## 1. 背景与问题

当前 UX-partner 项目的知识库使用方式更偏向于：

> 使用者已经有一个结构化好的 Markdown KB，然后 UX-partner 负责读取、索引和使用。

但真实情况是，大多数设计师并没有现成的 Karpathy LLM-wiki 形式知识库。尤其是 Zoom 不同产品线，例如 Zoom Phone、Zoom Contact Center、Zoom Clips、Zoom Meetings，各自都有大量官方 support articles，这些资料虽然权威，但并不是直接适合 LLM/agent 使用的知识库。

因此需要新增一个独立 skill：

```text
zoom-support-kb-builder
```

它的职责不是做 UX 设计，而是做 **产品线知识库生产**。

UX-partner 的职责是消费知识库，而不是生产知识库。两者应该解耦。

---

## 2. 总体判断

这个方案可行，但不应该设计成：

> AI 自动把 Zoom Support 全站全部爬下来，然后直接塞进 KB。

更靠谱的做法是：

> AI 自动发现候选文章 → 自动抓取 → 自动转 raw markdown → 自动打分分类 → 自动清洗校验 → 低置信度进入 review queue → 高置信度进入 ingest。

核心原则：

```text
不要追求“全自动无审核”。
要追求“自动化 + 置信度 + 可追溯 + 可审核 + 可维护”。
```

原因很简单：Zoom Support 里会有跨产品内容。比如某篇文章可能同时提到 Zoom Phone、Zoom Rooms、Zoom Contact Center、Meetings。如果没有分类和质量门禁，知识库会很快变脏，后续 UX-partner 可能引用错误产品线的知识。

---

## 3. 目标用户与使用场景

### 3.1 目标用户

主要用户是不同 Zoom 产品线的设计师，例如：

- Zoom Phone designer
- Zoom Contact Center designer
- Zoom Clips designer
- Zoom Meetings designer
- Platform / admin experience designer

### 3.2 核心使用场景

设计师输入：

```text
Build a UX KB for Zoom Phone from official Zoom Support articles.
```

系统自动完成：

```text
1. 识别目标产品线：Zoom Phone
2. 自动发现相关 support articles
3. 自动抓取文章正文
4. 自动转换为 raw markdown
5. 自动添加 frontmatter 和 metadata
6. 自动清洗、去重、质量检查
7. 自动判断产品相关性和置信度
8. 高置信度文章进入 raw KB
9. 中低置信度文章进入 review queue
10. 对 raw KB 执行 LLM-wiki ingest
11. 生成 concepts / task flows / user roles / constraints / UX patterns
12. 建立 index.md、log.md、manifest.json
13. 将最终 wiki 层交给 UX-partner 使用
```

---

## 4. 设计原则

### 4.1 Raw source 永远不可被 LLM 改写

Raw markdown 层只负责保存官方文章转换后的内容。它是 source of truth。

LLM 可以读取 raw source，但不能在 raw 层做总结、改写、脑补或重组。

### 4.2 Wiki 层才是 LLM 编译后的知识

真正适合 UX-partner 使用的是 wiki 层，而不是 raw 层。

```text
raw/support-articles/*.md
  ↓
LLM ingest
  ↓
wiki/concepts/*.md
wiki/task-flows/*.md
wiki/user-roles/*.md
wiki/constraints/*.md
wiki/ux-patterns/*.md
```

### 4.3 每个 claim 必须可溯源

wiki 层中的关键知识必须能追溯到具体 support article。

每个 wiki page 都应该包含：

```yaml
sources:
  - article_id: KB0060257
    title: Getting started with Zoom Phone
    source_url: https://support.zoom.com/...
```

### 4.4 自动化不等于无审核

高置信度内容可以自动 ingest。

中低置信度内容必须进入 review queue。

```text
High confidence:
  自动进入 raw KB + ingest

Medium confidence:
  进入 review queue，由设计师确认

Low confidence:
  进入 rejected 或 archive
```

### 4.5 产品线 KB 独立，但共享基础知识

建议整体 KB 结构分三层：

```text
Zoom-UX-KB/
  00-shared-zoom-platform/
  10-zoom-phone/
  20-zoom-contact-center/
  30-zoom-clips/
  90-schema/
```

产品线知识要独立，但账号、角色、权限、admin portal、billing、license、users、groups、sites 等共享概念应该放到 shared platform 层，避免每个产品线重复维护一套不同版本。

---

## 5. 推荐系统架构

```text
User input
  ↓
Product normalizer
  ↓
Discovery engine
  ↓
URL candidate pool
  ↓
Crawler
  ↓
Raw markdown generator
  ↓
Cleaner
  ↓
Validator
  ↓
Product relevance classifier
  ↓
Review queue / accepted raw KB / rejected list
  ↓
LLM-wiki ingest
  ↓
UX-partner knowledge index
```

### 5.1 模块职责

| 模块 | 职责 |
|---|---|
| Product normalizer | 将 “Zoom Phone” 转成标准产品名、别名、关键词、相关对象 |
| Discovery engine | 自动发现候选 support article URL |
| URL canonicalizer | 去掉无意义参数，保留稳定 article ID |
| Crawler | 使用 Crawl4AI 抓取文章并生成 Markdown |
| Cleaner | 清理导航、页脚、重复内容、噪音 |
| Validator | 检查文章完整性、metadata、hash、重复、正文质量 |
| Classifier | 判断文章是否属于目标产品线 |
| Review queue | 保存低置信度或冲突内容，等待人工确认 |
| Ingest engine | 将 raw article 编译成 LLM-wiki 页面 |
| Indexer | 将 wiki 层索引给 UX-partner 使用 |

---

## 6. 推荐技术栈

### 6.1 主抓取链路：requests + JSON-LD

Phase 1 主链路不依赖浏览器渲染。Zoom Support 文章页内嵌标准 Schema.org Article JSON-LD，包含干净标题、正文、作者、发布日期。requests 拉 HTML → BeautifulSoup 提取 JSON-LD → 取 `articleBody` 即可。

优势：

- 极快（单请求，无浏览器启动）
- 正文天然干净（Zoom 服务端已清洗）
- 无 cookie banner、导航、footer 等噪音
- 结构稳定（JSON-LD 是标准 SEO 格式）
- 依赖极少（requests + beautifulsoup4）

代码路径：

```python
r = requests.get(url, timeout=30, headers={"User-Agent": "ZoomKB-Builder/1.0"})
soup = BeautifulSoup(r.text, "html.parser")
ld = json.loads(soup.find("script", type="application/ld+json").string)
markdown = html2text(ld["articleBody"])   # 正文已是清洗后 HTML
```

### 6.2 Fallback 1：Trafilatura

当 JSON-LD 缺失或 `articleBody` 为空时，用 Trafilatura 从原始 HTML 抽取正文。轻量、专为文章提取设计、返回 Markdown。

触发条件：

- 页面无 JSON-LD
- JSON-LD 中无 `articleBody`
- `articleBody` 长度 < 200 字符

### 6.3 Fallback 2：Crawl4AI（可选）

Crawl4AI 降级为可选 fallback。仅当 Trafilatura 也无法抽出有效内容时启用。

不适合作为 Phase 1 主力的原因：

- 需要 Chromium/Playwright，启动慢、内存大
- Docker 依赖重，CI 和本地环境配置成本高
- 对静态文章页过度设计（Zoom Support 不是 SPA）
- 安装和首次运行常报依赖/编译错误

启用方式：安装 `crawl4ai[all]` 后环境变量 `ZOOMKB_CRAWL4AI=1` 开启。

### 6.4 文件转换工具：MarkItDown

用于处理非网页资料，例如：

- PDF
- Word
- PowerPoint
- Excel
- 本地 HTML

### 6.5 大规模调度：Scrapy 或 Firecrawl

Phase 1 不建议上 Scrapy。

当你需要大规模、长期、可调度、增量更新时，再考虑：

- Scrapy
- Firecrawl self-host
- 自己的 crawler scheduler

---

## 7. Discovery 自动化策略

手动维护 30–100 篇 CSV 的确麻烦，因此可以自动化。但 discovery 不应该依赖爬搜索结果页，而应该使用更稳的方式。

### 7.1 不推荐方式

```text
不推荐：
- 自动爬站内 search 页面
- 模拟用户在搜索框里疯狂搜索
- 绕过 robots.txt 或登录限制
- 全站无差别爬取
```

### 7.2 推荐方式

```text
推荐：
1. 读取 robots.txt
2. 从 robots.txt 中找到 sitemap
3. 解析 sitemap
4. 提取 article URL
5. 规范化 URL
6. 根据产品关键词初筛
7. 从高置信度 seed article 做 link graph expansion
8. 抓取候选文章
9. 根据正文再做产品相关性判断
```

### 7.3 URL canonicalization

Zoom Support article URL 可能带有无意义 session 参数，需要规范化。

保留：

```text
id=zm_kb
sysparm_article=KBxxxxxxx
```

移除：

```text
ampDeviceId
ampSessionId
utm_*
session 参数
tracking 参数
```

标准形式：

```text
https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060257
```

### 7.4 Product normalizer

用户输入：

```text
Zoom Phone
```

系统转换成：

```yaml
product_id: zoom-phone
product_name: Zoom Phone
locale: en
aliases:
  - Zoom Phone
  - Phone System Management
  - phone user
  - phone users
  - call queue
  - call queues
  - auto receptionist
  - IVR
  - shared line group
  - direct phone number
  - emergency address
  - desk phone
  - phone policy
  - Zoom Phone policy
  - common area phone
  - call delegation
  - phone site
  - phone number management
```

### 7.5 Seed article strategy

自动 discovery 仍然需要 seed，但 seed 不需要用户手动维护 CSV。

seed 可以来自：

```text
1. sitemap 中标题高度匹配的文章
2. 产品名搜索引擎结果
3. 已知产品入口页
4. 官方 support article 中的内部链接
5. 上一次 crawl 的高置信度文章
```

对于 Zoom Phone，高置信度 seed 往往包括：

```text
- Getting started with Zoom Phone
- Zoom Phone admin setup
- Zoom Phone policy settings
- Zoom Phone role management
- Phone users
- Call queues
- Auto receptionists
- Number management
- Emergency services
```

---

## 8. 产品相关性评分机制

不能只看标题是否包含 “Zoom Phone”。

很多 Zoom Phone 文章标题可能不包含完整产品名，例如：

```text
Changing phone user settings
Managing phones and devices
Making and receiving calls
Using role management
Changing account-level settings
```

因此需要 relevance scoring。

### 8.1 Scoring signals

```text
Strong signal, +5:
- title contains "Zoom Phone"
- breadcrumb/category belongs to Phone
- body contains "Phone System Management"
- requirements mention Zoom Phone admin privilege
- article clearly discusses phone users, phone numbers, call queues, auto receptionists

Medium signal, +3:
- body frequently mentions phone users, call queues, direct numbers, IVR, emergency address
- article has many links to known Zoom Phone articles
- article explains admin portal paths related to Zoom Phone

Weak signal, +1:
- mentions calling, phone, device, extension, desk phone

Negative signal, -5:
- primarily about Zoom Meetings
- primarily about Zoom Rooms
- primarily about Zoom Contact Center
- primarily about Webinar, Team Chat, Whiteboard
- mentions phone only incidentally
```

### 8.2 Confidence tiers

```text
score >= 8:
  High confidence
  自动进入 raw/support-articles
  可以进入 ingest

score 4–7:
  Medium confidence
  进入 review/candidates
  等待人工确认

score < 4:
  Low confidence
  进入 rejected
```

### 8.3 Article classification output

```json
{
  "article_id": "KB0060257",
  "title": "Getting started with Zoom Phone",
  "product": "zoom-phone",
  "relevance_score": 12,
  "confidence": "high",
  "matched_signals": [
    "title contains Zoom Phone",
    "mentions Phone System Management",
    "mentions phone users",
    "mentions auto receptionists",
    "mentions call queues"
  ],
  "decision": "accepted"
}
```

---

## 9. 目标目录结构

```text
Zoom-UX-KB/
  00-shared-zoom-platform/
    raw/
    wiki/
    manifest.json
    log.md

  10-zoom-phone/
    raw/
      support-articles/
        KB0060257-getting-started-with-zoom-phone.md
        KB0069655-changing-zoom-phone-policy-settings.md

    review/
      candidate-articles.json
      low-confidence/
      rejected/
      conflicts/

    wiki/
      index.md
      overview.md
      concepts/
      user-roles/
      task-flows/
      constraints/
      ux-patterns/

    manifest.json
    crawl-report.md
    ingest-report.md
    log.md

  90-schema/
    kb-schema.md
    ingest-rules.md
    page-types.md
    source-quality-rubric.md
    lint-rules.md
```

---

## 10. Raw markdown 格式

每篇 raw article 必须有 frontmatter。

示例：

```markdown
---
source_type: zoom_support_article
product: zoom-phone
article_id: KB0060257
title: Getting started with Zoom Phone
source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060257
captured_at: 2026-05-17T00:00:00Z
retrieval_tool: crawl4ai
relevance_score: 12
confidence: high
content_hash: sha256:xxxxxxxx
status: raw
---

# Getting started with Zoom Phone

原始文章正文 Markdown...

## Source notes

- Source: official Zoom Support article
- Captured for: Zoom Phone UX KB
```

### 10.1 Raw markdown 要求

```text
必须保留：
- article title
- headings
- task steps
- requirements
- tables
- links
- warnings / notes
- limitations
- related article links

必须去除：
- cookie banner
- navigation
- footer
- unrelated sidebar
- duplicated links
- survey module
- language selector
- login/register prompts
```

---

## 11. Manifest 设计

`manifest.json` 是整个 KB 的账本。

示例：

```json
{
  "product": "zoom-phone",
  "source_root": "https://support.zoom.com/hc/en",
  "generated_at": "2026-05-17T00:00:00Z",
  "articles": [
    {
      "article_id": "KB0060257",
      "title": "Getting started with Zoom Phone",
      "source_url": "https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060257",
      "local_path": "raw/support-articles/KB0060257-getting-started-with-zoom-phone.md",
      "content_hash": "sha256:xxxxxxxx",
      "relevance_score": 12,
      "confidence": "high",
      "status": "accepted",
      "captured_at": "2026-05-17T00:00:00Z",
      "last_checked_at": "2026-05-17T00:00:00Z"
    }
  ]
}
```

### 11.1 manifest 的作用

```text
- 去重
- 增量更新
- 回溯来源
- 检查哪些文章已 ingest
- 检查哪些文章待 review
- 检查哪些文章被 rejected
- 对比 content_hash 判断文章是否变化
```

---

## 12. Skill 命令设计

建议提供 5 个主命令和 1 个一键命令。

### 12.1 `/zoomkb:init`

初始化产品线 KB。

```text
/zoomkb:init --product "Zoom Phone" --output "./Zoom-UX-KB/10-zoom-phone"
```

执行内容：

```text
- 创建目录结构
- 创建 manifest.json
- 创建 log.md
- 创建 crawl-report.md
- 创建 ingest-report.md
- 创建 wiki/index.md
- 复制 90-schema 模板
```

### 12.2 `/zoomkb:discover`

自动发现候选文章。

```text
/zoomkb:discover --product "Zoom Phone" --source-root "https://support.zoom.com/hc/en"
```

执行内容：

```text
- 读取 robots.txt
- 找 sitemap
- 解析 sitemap
- 提取 article URL
- 规范化 URL
- 初步筛选候选 URL
- 抓取少量 metadata
- 生成 candidate-articles.json
```

### 12.3 `/zoomkb:crawl`

抓取候选文章并转 raw markdown。

```text
/zoomkb:crawl --product "Zoom Phone" --max-articles 300
```

执行内容：

```text
- 读取 candidate-articles.json
- 用 Crawl4AI 抓取正文
- 转换为 markdown
- 生成 content_hash
- 添加 frontmatter
- 写入 raw/support-articles
```

### 12.4 `/zoomkb:validate`

校验 raw markdown。

```text
/zoomkb:validate --product "Zoom Phone"
```

执行内容：

```text
- 检查 frontmatter
- 检查正文长度
- 检查标题
- 检查 article_id
- 检查 source_url
- 检查重复 hash
- 检查正文噪音
- 检查产品相关性
- 生成 validation report
```

### 12.5 `/zoomkb:ingest`

将 raw markdown 编译成 LLM-wiki。

```text
/zoomkb:ingest --product "Zoom Phone"
```

执行内容：

```text
- 读取 high confidence raw articles
- 根据 schema 分析实体和概念
- 生成/更新 wiki pages
- 更新 wiki/index.md
- 更新 log.md
- 生成 ingest-report.md
```

### 12.6 `/zoomkb:build`

一键执行完整流程。

```text
/zoomkb:build --product "Zoom Phone" --mode safe
```

内部执行：

```text
init
  ↓
discover
  ↓
crawl
  ↓
validate
  ↓
ingest
```

建议默认使用 `safe mode`：

```text
safe mode:
  高置信度自动处理
  中低置信度进入 review queue
  不自动 ingest 有争议内容
```

---

## 13. Phase 1 抓取伪代码（requests + JSON-LD）

```python
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import html2text
import requests
from bs4 import BeautifulSoup


def get_article_id(url: str) -> str:
    query = parse_qs(urlparse(url).query)
    return query.get("sysparm_article", ["unknown"])[0]


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:80]


def extract_jsonld_article(html: str) -> dict | None:
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("script", type="application/ld+json")
    if not tag or not tag.string:
        return None
    try:
        data = json.loads(tag.string)
        if isinstance(data, list):
            data = next((x for x in data if x.get("@type") == "Article"), None)
        if data and data.get("@type") == "Article":
            return data
    except json.JSONDecodeError:
        pass
    return None


def extract_markdown(html: str, article_id: str) -> tuple[str, str, str]:
    """Return (title, markdown_body, extraction_method)."""
    ld = extract_jsonld_article(html)
    if ld and ld.get("articleBody") and len(ld["articleBody"]) > 200:
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = True
        h.body_width = 0
        title = ld.get("headline", ld.get("name", article_id))
        body = h.handle(ld["articleBody"]).strip()
        return title, body, "jsonld"

    # Fallback: trafilatura
    try:
        import trafilatura
        downloaded = trafilatura.loads(html)
        title = trafilatura.extract(downloaded, output="json", include_comments=False, include_tables=True)
        if title:
            title_data = json.loads(title)
            return (
                title_data.get("title", article_id),
                title_data.get("raw_text", ""),
                "trafilatura",
            )
    except Exception:
        pass

    return article_id, "", "failed"


def build_frontmatter(title: str, url: str, product: str, score: int,
                      confidence: str, extraction: str, body: str) -> str:
    article_id = get_article_id(url)
    content_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()

    return f"""---
source_type: zoom_support_article
product: {product}
article_id: {article_id}
title: {title}
source_url: {url}
captured_at: {datetime.now(timezone.utc).isoformat()}
retrieval_tool: {extraction}
relevance_score: {score}
confidence: {confidence}
content_hash: sha256:{content_hash}
status: raw
---

"""


def crawl_article(url: str, product: str, output_dir: str, timeout: int = 30):
    r = requests.get(url, timeout=timeout, headers={
        "User-Agent": "ZoomKB-Builder/1.0 (research project)"
    })
    r.raise_for_status()

    article_id = get_article_id(url)
    title, body, extraction = extract_markdown(r.text, article_id)

    if not body or len(body) < 200:
        raise ValueError(f"Empty/short content from {url} (method={extraction})")

    score, confidence = classify_relevance(body, title, product)

    frontmatter = build_frontmatter(
        title=title, url=url, product=product,
        score=score, confidence=confidence,
        extraction=extraction, body=body
    )

    filename = f"{article_id}-{slugify(title)}.md"
    out = Path(output_dir) / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(frontmatter + f"# {title}\n\n" + body + "\n", encoding="utf-8")

    return {
        "article_id": article_id,
        "filename": filename,
        "score": score,
        "confidence": confidence,
        "extraction": extraction,
        "word_count": len(body.split()),
    }
```

---

## 14. Validation checklist

每次抓取后必须检查：

```text
Metadata:
- 是否有 article_id
- 是否有 title
- 是否有 source_url
- 是否有 captured_at
- 是否有 content_hash
- 是否有 product
- 是否有 confidence

Content quality:
- 正文是否为空
- 正文是否过短
- 是否包含过多导航噪音
- 是否包含主要 heading
- 表格是否保留
- task steps 是否保留
- links 是否保留

Product relevance:
- 是否真的属于目标产品线
- 是否只是偶然提到目标产品
- 是否和其他产品线冲突

Duplication:
- 是否重复 article_id
- 是否重复 content_hash
- 是否同一文章不同 URL

Freshness:
- 是否已经抓过
- content_hash 是否变化
- 是否需要重新 ingest
```

---

## 15. Ingest 设计

Ingest 阶段不是总结文章，而是把 raw support article 编译成 design-facing knowledge。

### 15.1 Ingest 输入

```text
raw/support-articles/*.md
90-schema/ingest-rules.md
90-schema/page-types.md
90-schema/source-quality-rubric.md
```

### 15.2 Ingest 输出

```text
wiki/
  index.md
  overview.md
  concepts/
    zoom-phone-policy-settings.md
    phone-user.md
    call-queue.md
    auto-receptionist.md

  user-roles/
    account-owner.md
    phone-super-admin.md
    phone-site-admin.md
    call-queue-admin.md

  task-flows/
    configure-phone-policy.md
    add-phone-users.md
    manage-call-queue.md
    set-up-auto-receptionist.md

  constraints/
    account-vs-site-vs-extension-settings.md
    role-based-access-constraints.md
    license-plan-constraints.md

  ux-patterns/
    inherited-settings.md
    locked-settings.md
    bulk-apply.md
```

### 15.3 Page types

#### concept

用于解释产品概念。

示例：

```text
Zoom Phone policy settings
Call queue
Auto receptionist
Shared line group
```

#### user-role

用于解释角色、权限、可见范围、能做什么、不能做什么。

示例：

```text
Phone Super Admin
Phone Site Admin
Call Queue Admin
Phone User
```

#### task-flow

用于解释用户完成某个任务的步骤、入口、依赖、失败点。

示例：

```text
Configure Zoom Phone policy settings
Add phone users
Assign direct phone numbers
Set up auto receptionist
```

#### constraint

用于记录设计约束。

示例：

```text
Account-level vs site-level settings
Role-based visibility
License requirements
Locked inherited settings
```

#### ux-pattern

用于沉淀可复用交互模式。

示例：

```text
Inherited setting pattern
Bulk apply pattern
Disabled state explanation
Permission-gated action
```

---

## 16. Wiki page 示例

```markdown
---
type: concept
product: zoom-phone
title: Zoom Phone policy settings
sources:
  - article_id: KB0069655
    title: Changing Zoom Phone policy settings
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0069655
confidence: high
last_reviewed: 2026-05-17
---

# Zoom Phone policy settings

## Summary

Zoom Phone policy settings allow admins to control feature availability and behavior across different hierarchy levels.

## Key UX implications

- Designers must account for inherited settings.
- Some settings may be editable only at specific hierarchy levels.
- Admin permission scope affects visibility and editability.
- Disabled controls should explain why the setting cannot be changed.

## Related concepts

- [[role-based-access-constraints]]
- [[account-vs-site-vs-extension-settings]]
- [[inherited-settings]]

## Open questions

- Which policy settings are inherited by default?
- Which settings can be overridden at lower levels?
```

---

## 17. Lint 设计

KB 会腐坏，所以必须定期 lint。

### 17.1 Lint 检查项

```text
Source traceability:
- wiki claim 是否有 source
- wiki page 是否缺 sources
- source_url 是否存在

Coverage:
- raw article 是否尚未 ingest
- high confidence article 是否遗漏
- important concept 是否没有 page

Consistency:
- 同一概念是否有多个重复 page
- 权限描述是否冲突
- 产品名是否不一致

Freshness:
- source article hash 是否变化
- wiki page 是否基于旧版本 raw source
- last_reviewed 是否过旧

Navigation:
- index.md 是否更新
- wikilink 是否断裂
- 是否有 orphan page

Quality:
- 是否有过多总结话术
- 是否缺少 UX implications
- 是否缺少 constraints
- 是否有 hallucinated claim
```

### 17.2 Lint 输出

```text
lint-report.md
review/conflicts/
review/stale-pages/
review/orphan-pages/
```

---

## 18. 与 UX-partner 的集成方式

### 18.1 KB builder 和 UX-partner 解耦

```text
zoom-support-kb-builder:
  负责生产 KB

UX-partner:
  负责消费 KB
```

### 18.2 集成流程

```text
zoom-support-kb-builder
  ↓
生成 wiki/
  ↓
UX-partner setup-kb
  ↓
索引 wiki markdown
  ↓
UX-partner 在 discovery 中调用 KB
```

### 18.3 UX-partner 使用策略

UX-partner 在回答或分析设计需求时，应该优先读取：

```text
1. wiki/index.md
2. 相关 concept page
3. 相关 task-flow page
4. 相关 constraint page
5. 必要时再回看 raw source
```

不要每次都直接搜索 raw support articles。raw 层是 source of truth，但不是最佳 reasoning surface。

---

## 19. MVP 路线图

### Phase 1：本地 MVP

目标：验证 Zoom Phone KB 自动生成是否可行。

范围：

```text
- 只支持 Zoom Phone
- 只支持英文 Zoom Support
- 只处理公开 support articles
- 只输出 raw markdown + manifest + review queue
- requests + JSON-LD 作为主抓取链路（无浏览器依赖）
- Trafilatura 作为 fallback
- Crawl4AI 作为可选 fallback（默认不启用）
- 规则 + 可选 LLM 分类器
```

交付：

```text
/zoomkb:init
/zoomkb:discover
/zoomkb:crawl
/zoomkb:validate
```

### Phase 2：LLM-wiki ingest

目标：从 raw markdown 生成 design-facing wiki。

范围：

```text
- concept pages
- user-role pages
- task-flow pages
- constraints pages
- ux-pattern pages
- index.md
- log.md
```

交付：

```text
/zoomkb:ingest
/zoomkb:lint
```

### Phase 3：UX-partner 集成

目标：让 UX-partner 能直接使用生成的 KB。

范围：

```text
- setup-kb 读取 wiki 层
- context-mode / local search indexing
- query routing
- source citation policy
```

交付：

```text
UX-partner 可直接基于 Zoom Phone KB 做需求理解、约束识别、场景扩展、UX risk analysis。
```

### Phase 4：多产品线支持

目标：支持多个 Zoom 产品线。

范围：

```text
- Zoom Contact Center
- Zoom Clips
- Zoom Meetings
- Zoom Rooms
- Shared platform KB
```

交付：

```text
每个产品线都有独立 KB，同时共享平台层知识。
```

### Phase 5：增量更新与治理

目标：长期维护 KB。

范围：

```text
- 定期 refresh
- content_hash diff
- stale source detection
- review queue
- conflict detection
- source freshness report
```

---

## 20. 风险与应对

### 20.1 风险：抓到不相关内容

应对：

```text
- relevance scoring
- confidence tiers
- review queue
- rejected manifest
```

### 20.2 风险：页面结构变化

应对：

```text
- Crawl4AI 主链路
- Scrapling fallback
- Trafilatura 清洗兜底
- selector 配置化
```

### 20.3 风险：KB 被错误内容污染

应对：

```text
- high confidence 才自动 ingest
- medium confidence 人工确认
- 每个 wiki claim 必须有 source
- 定期 lint
```

### 20.4 风险：违反站点抓取规则

应对：

```text
- 读取 robots.txt
- 不爬 disallowed path
- 不绕过登录或权限
- 控制请求频率
- 优先使用 sitemap 和公开 article URL
```

### 20.5 风险：LLM hallucination

应对：

```text
- raw 层不可改写
- wiki 层必须引用 source
- no-source claim 不允许进入 accepted wiki
- 低置信度进入 review
```

---

## 21. 推荐的最终体验

用户只需要输入：

```text
Build a UX KB for Zoom Phone from official Zoom Support articles.
```

系统返回：

```text
Zoom Phone KB build completed.

Summary:
- 412 candidate articles discovered
- 186 articles accepted
- 47 articles require review
- 179 articles rejected
- 186 raw markdown files generated
- 72 wiki pages created
- 15 concept pages
- 12 task-flow pages
- 8 user-role pages
- 21 constraint pages
- 16 UX-pattern pages

Next:
- Review medium confidence candidates
- Run /zoomkb:lint
- Run UX-partner setup-kb on wiki/
```

---

## 22. 最终结论

这个方案值得做，而且应该做成独立 skill。

但正确的目标不是：

```text
自动把 Zoom Support 全站扒下来。
```

而是：

```text
自动构建一个有置信度、有审核、有溯源、有治理能力的 Zoom 产品线 LLM-wiki 知识库。
```

对 UX-partner 来说，这个能力非常关键。因为 UX-partner 真正的产品价值不是“会搜索文档”，而是：

```text
基于可信产品知识，帮助设计师更快理解需求、识别约束、扩展场景、发现 UX 风险，并产出更可靠的设计分析。
```

---

## 23. 推荐下一步

建议下一步直接写 `zoom-support-kb-builder` skill 的正式创建文档，包含：

```text
1. SKILL.md
2. Commands
3. Scripts
4. Schema templates
5. Output examples
6. Acceptance criteria
7. Scoring rubric
8. MVP engineering task breakdown
```

优先实现：

```text
/zoomkb:init
/zoomkb:discover
/zoomkb:crawl
/zoomkb:validate
```

等 raw KB pipeline 跑通后，再做：

```text
/zoomkb:ingest
/zoomkb:lint
UX-partner setup-kb integration
```

---

## 24. Claude Code Plugin 路线

### 24.1 目标

将 `zoomkb-builder` 打包为 **Claude Code Plugin**，设计师在 Claude Code 中直接通过 slash command 触发 KB 构建流程，无需离开设计环境。

### 24.2 插件形态

```text
zoomkb-builder/
├── .claude-plugin/
│   └── manifest.json          # 插件元信息
├── skills/
│   └── zoomkb.md              # Claude Code skill 定义
├── src/
│   └── zoomkb/                # 现有 Python 包
├── pyproject.toml
└── README.md
```

### 24.3 Skill 命令映射

| Slash Command | Python CLI | 说明 |
|---|---|---|
| `/zoomkb:init` | `zoomkb init` | 初始化产品线 KB 目录 |
| `/zoomkb:discover` | `zoomkb discover` | 从 sitemap 发现候选文章 |
| `/zoomkb:crawl` | `zoomkb crawl` | 抓取文章生成 raw markdown |
| `/zoomkb:validate` | `zoomkb validate` | 校验 raw markdown 质量 |
| `/zoomkb:ingest` | `zoomkb ingest` | LLM 生成 wiki 页面 |
| `/zoomkb:lint` | `zoomkb lint` | 检查 KB 完整性/一致性 |
| `/zoomkb:build` | `zoomkb build` | 一键执行全流程 |

### 24.4 Skill 集成要点

- Skill 定义通过 SKILL.md 注册到 Claude Code，调用 Python CLI 作为后端
- 需要处理的权限：网络请求（爬取）、文件写入（生成 KB）、Shell 命令执行（Python 子进程）
- `discover` 阶段需并行网络 IO，ThreadPoolExecutor 已验证可行
- `ingest` 阶段调用 LLM（通过 Claude API），需配置 API key
- 大输出（crawl/validate report）通过 context-mode 工具拿到 indexed 结果，不直接进 context

### 24.5 插件 MVP 路线

```text
Phase P1: 命令行可用
  - zoomkb CLI 全部 7 个命令可独立运行
  - pyproject.toml 配置 entry_points
  - pip install 即可用

Phase P2: Skill 包装
  - 编写 SKILL.md，将每个命令映射为 slash command
  - 配置 settings.json 权限
  - 在 Claude Code 中可交互式使用

Phase P3: 一键体验
  - /zoomkb:build 一键执行 init → discover → crawl → validate → ingest → lint
  - 进度反馈、错误恢复
  - 与 UX-partner skill 的 setup-kb 自动衔接
```

### 24.6 当前进度

| Phase | 状态 |
|---|---|
| Phase 1 (本地 MVP) | ✅ 完成 — init/discover/crawl/validate |
| Phase 2 (LLM-wiki ingest) | ✅ 完成 — ingest/lint 均已实现 |
| Phase P1 (CLI 完整) | ✅ 完成 — 8 个命令全部可用 (init/discover/crawl/validate/ingest/extract/lint/build) |
| Phase P2 (Skill 包装) | ✅ 完成 — SKILL.md 已编写，git 已推送 |
| Phase P3 (一键体验) | ✅ 完成 — build 全流程验证通过，2 bug 已修复 |
| Phase 3 (UX-partner 集成) | ✅ 完成 — 5 changes (manifest kb_type, wiki subdirs, index placeholder, integration test, SKILL.md docs) |
| Phase 4 (多产品线) | ✅ 完成 — 5 product configs, hardcoded fix, dynamic output, build-all, SKILL.md |
| Phase 5 (增量更新) | ✅ 完成 — refresh, freshness, conflict detection, review queue, manifest query helpers |

### 24.7 Phase 3 交付明细

| 文件 | 变更 |
|---|---|
| `src/zoomkb/manifest.py` | 新 manifest 写入 `kb_type: "zoomkb"` + `kb_version: "1.0"`；已有 manifest 回填 |
| `src/zoomkb/cli.py` | `cmd_init()` 预创建全部 5 个 wiki 子目录，确保 UX-partner 检测不因空目录失败 |
| `src/zoomkb/ingest.py` | `_generate_index()` 空分类输出 `_No entries yet._` |
| `SKILL.md` | 新增 "UX-partner Integration" 章节（用法、检测、分类标签、引用策略） |
| `tests/test_ux_partner_integration.py` | 12 个集成测试：manifest 标记、wiki 结构、frontmatter、type/子目录一致性、wikilink 孤儿检测、分类兼容性 |

验证结果：
- 54/54 测试通过 (12 集成 + 42 已有)
- UX-partner `index-to-context-mode.js` 对 test-kb-e2e 全部 402 文件分类正确 (0 条 UNCATEGORIZED)
- 端到端流程：`/zoomkb:build` → `/ux-project:setup-kb` 可衔接

### 24.8 Phase 4 交付明细

| 文件 | 变更 |
|---|---|
| `src/zoomkb/constants.py` | 新增 5 个产品配置: `zoom-contact-center`, `zoom-clips`, `zoom-meetings`, `zoom-rooms`, `shared-zoom-platform` |
| `src/zoomkb/ingest.py` | `prepare_extraction_queue()` 接受 `product` 参数；`_write_wiki_page()` 接受 `product` 参数；`commit_extraction()` 传递 product 到 wiki page |
| `src/zoomkb/cli.py` | 新增 `_default_output()` 动态目录名；新增 `ALL_PRODUCTS` 常量；新增 `cmd_build_all` 命令；`cmd_init`/`cmd_discover`/`cmd_build` 使用动态 output |
| `SKILL.md` | 新增 `build-all` 命令文档、支持产品线表、Shared Platform KB 说明 |

验证结果：
- 54/54 测试通过
- `init --product "Zoom Meetings"` → `./zoom-meetings-kb/`
- `build-all` → 6/6 产品线全部初始化成功

### 24.10 Phase 5 交付明细

| 文件 | 变更 |
|---|---|
| `src/zoomkb/refresh.py` | **新文件**: `refresh_articles()` 重新抓取已接受文章并对比 content_hash；`generate_freshness_report()` 生成完整 freshness 报告 |
| `src/zoomkb/manifest.py` | 新增 3 个查询辅助函数: `get_review_queue()`, `get_stale_sources()`, `get_changed_since()` |
| `src/zoomkb/cli.py` | 新增 `cmd_refresh` + `cmd_freshness` 命令和对应 arg parser；`cmd_ingest` 输出增加 conflict-flagged 统计 |
| `src/zoomkb/ingest.py` | `_write_wiki_page()` 返回 `tuple[Path, bool, bool]`（增加 conflict_flagged）；≥3 个来源的实体添加 `conflict_flag: multiple-sources` frontmatter；commit stats 新增 `entities_conflict_flagged`；ingest 报告新增冲突统计 |
| `SKILL.md` | 新增 `/zoomkb:refresh` 和 `/zoomkb:freshness` 命令文档；输出结构增加 `refresh-report.md` 和 `freshness-report.md` |

新增命令：
- `zoomkb refresh` — 重新抓取已接受文章，hash 对比，变化文章标记 `status: review`，不可达标记 `stale`
- `zoomkb freshness` — 生成 `freshness-report.md`，包含逐篇文章表、stale 列表、review queue

验证结果：
- 54/54 测试通过
- `zoomkb freshness --output ./test-kb` 正常运行（3 篇文章，1 review queue）
- `zoomkb refresh --help` 和 `zoomkb freshness --help` 均可正常输出

### 24.9 即时下一步

1. ~~用真实 Zoom Support 数据端到端验证 `build` 全流程~~ ✅ 已完成
2. ~~编写 ingest 中间步的批处理脚本~~ ✅ 已完成 — `zoomkb extract` + `--auto-extract`
3. ~~Phase 3: UX-partner 集成~~ ✅ 已完成
4. ~~Phase 4: 多产品线支持~~ ✅ 已完成
5. ~~Phase 5: 增量更新与治理~~ ✅ 已完成 — refresh, freshness, conflict detection, review queue
6. UX-partner 侧交叉建议：setup-kb 优先读 `kb_type` 字段；indexer 加入 `review/` skip；输出路径改为 KB root
7. **Phase 6: 真实数据验证** — 用真实 Zoom Support 数据跑通完整流程，验证 refresh/conflict detection 在实际场景下行为正确
