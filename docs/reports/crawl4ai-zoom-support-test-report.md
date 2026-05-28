# Crawl4AI / Zoom Support 抓取测试报告

## 测试时间
2026-05-17

## 测试目标
验证 Crawl4AI 能否有效抓取 Zoom Support 文章，并评估内容质量。

## 核心发现

### 1. Crawl4AI 在当前环境无法运行
- Python 3.9.6 + Crawl4AI 0.7.4 启动即报错：`TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'`
- Crawl4AI 需要 Python 3.10+ 的 `|` 联合类型语法
- macOS 系统 Python 3.9 + LibreSSL 2.8.3 与 urllib3 v2 存在兼容性问题
- **结论：正式部署需 Python 3.10+，当前环境无法直接测试 Crawl4AI**

### 2. Zoom Support 页面结构：AngularJS 单页应用
- 页面 HTML ~190KB，但**静态 HTML 中几乎没有可见正文**
- 正文全部嵌入在 `<script>` 标签的 JSON-LD schema 中
- 标准 CSS 选择器（`.article-content`, `[role='main']` 等）全部失效
- **关键发现：不需要 headless browser！requests 即可获取完整内容**

### 3. JSON-LD Schema 是稳定的数据源

5 篇测试文章全部成功提取 `articleBody`：

| Article ID | Title | Text Length | Headings | Links | Lists |
|---|---|---|---|---|---|
| KB0060257 | Getting started with Zoom Phone (admin) | 10,492 chars | 22 | 67 | 13 |
| KB0069655 | Changing Zoom Phone policy settings | 8,628 chars | 8 | 89 | 9 |
| KB0060324 | Teilnahme an Breakout-Räumen (德语) | 8,694 chars | 7 | 18 | 16 |
| KB0060325 | Participar en las salas (西班牙语) | 8,019 chars | 7 | 18 | 16 |
| KB0060344 | Mengaktifkan obrolan (印尼语) | 6,965 chars | 6 | 19 | 12 |

JSON-LD schema 包含：
- `@type`: TechArticle
- `headline`: 文章标题
- `articleSection`: 分类（如 "Admin guide"）
- `dateModified`: 最后修改时间
- `articleBody`: 完整正文（HTML 格式）
- `url`: 规范 URL

### 4. 内容质量评估

**优点：**
- 正文完整（6K-10K chars）
- 结构清晰：h2/h3 headings、ul/ol lists、requirements 区块
- Links 完整保留（67-89 个 per article）
- HTML 格式良好，可直接转为 Markdown

**缺点：**
- 无 tables（测试样本中 0 tables，可能 Zoom Support 不用 table）
- 部分 articles 有 geo IP redirect 问题（见下文）

### 5. Geo IP 语言重定向问题

`Accept-Language: en-US` header **无法阻止** geo redirect。
- KB0060324 (Breakout rooms) → 德语
- KB0060325 (Breakout rooms) → 西班牙语
- KB0060344 (Chat in meeting) → 印尼语

可能需要在 URL 中指定 locale 参数或使用特定 cookie。

## 技术选型影响

### Crawl4AI 不再是必须

| 维度 | Crawl4AI | requests + JSON-LD |
|---|---|---|
| 依赖复杂度 | 高（Playwright + 浏览器） | 低（requests + bs4） |
| 抓取速度 | 慢（浏览器渲染） | 快（纯 HTTP） |
| 可靠性 | 中（浏览器易出错） | 高 |
| 内容质量 | 好 | **同等质量** |
| 维护成本 | 高 | **低** |

### 建议调整

1. **Crawl4AI 降级为可选方案**，非必须
2. **主链路：requests → 提取 JSON-LD → articleBody HTML → Markdown**
3. **Fallback：如果 JSON-LD 缺失，再用 Trafilatura / Crawl4AI**
4. **Phase 1 可以更快推进** — 不需要配置浏览器环境

## 推荐 Phase 1 简化方案

```
requests.get(url) 
  → 正则提取 JSON-LD script
  → json.loads() → articleBody
  → BeautifulSoup 解析 HTML
  → 转 Markdown
  → 加 frontmatter
  → 保存 .md
```

预计 1-2 天即可完成 crawl pipeline，而非 2-3 周。

## 待验证问题

- [ ] 英文文章 URL 格式是什么？是否带 `/en/` 路径就能固定语言？
- [ ] 所有 Zoom Support 文章都有 JSON-LD schema 吗？（需扩大样本）
- [ ] 是否存在动态加载的内容不在 JSON-LD 中？
- [ ] 文章中的 internal links 需要规范化吗？
