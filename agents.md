# Agents Activity Tracker

本文档由 AI Agent 实时维护，用于记录当前项目的工程进度与状态。

## 当前状态 (Current Status)

### 1. 基础设施 (Infrastructure)
*   [x] **Ghost 同步引擎**：`ghost_sync.py` 修复了 Lexical 结构兼容性问题，支持强力注入自定义 CSS。
*   [x] **仓库重构**：实现了“代码与内容分离”。`infra` 分支作为脚本库，`wikijs` 分支作为纯净内容库，`main` 分支作为发布端。
*   [x] **S3 兼容性修复**：针对甲骨文云（OCI）对象存储，修复了批量删除（400 Error）及隐私警报（Bucket Listing）问题。

### 2. 内容发布 (Publishing)
*   [x] **双约记：完整章节**：已从原始文本恢复并重新拆分为 9 个章节及序言。
*   [x] **牧人三部曲：全量拆分**：已利用 `fix_content.py` 将历史、地质、技术三部大部头文件按章拆分，保留了完整的子章节结构。
*   [x] **多端同步**：`main` 与 `wikijs` 分支已完成结构对齐并推送到远程。

## 待办事项 (Next Steps)

*   [x] **Wiki.js 初始化**：将 `wikijs` 分支推送到远程仓库，触发 Wiki.js 的 Git Storage 同步。
*   [ ] **英文版管线**：建立自动化翻译脚本，探索将内容发布为英文版的可能性。
*   [x] **CI/CD 联调**：GitLab CI 已加入完整内容分发管线（main→ghost/bookstack 同步 + Ghost CMS 发布）。

## 2026-06-14 更新：内容分发管线 Phase 2

*   [x] **`content_sync.py` 脚本**：从 `main` 自动提取四书内容分发到 `ghost`/`bookstack` 分支，处理分支特有的 frontmatter 格式
*   [x] **ghost 分支内容同步**：四书64个 md 文件从 `main` 同步到 `ghost` 分支并推送远程
*   [x] **Ghost CMS 发布（全量）**：
    *   牧月记：9篇（7章+序+目录）
    *   牧兰记：24篇（22章+序+目录）
    *   牧人记：20篇（19章+目录）
    *   双约记：11篇（9章+序+目录）
    *   合计：**64篇文章已发布到 blog.seekkey.eu.org**，含霞鹜文楷字体注入 + Wiki.js 跳转链接
*   [x] **bookstack 分支同步**：四书内容同步并推送远程
*   [x] **GitLab CI 更新**：main 推送时自动触发内容分发，ghost 推送时自动触发 Ghost CMS 发布
*   [x] **MANIFEST.md 更新**：标记已完成项，新增 Phase 2 追踪

## 备注 (Notes)
*   **字体 CDN**: 目前统一使用 `npm.elemecdn.com/lxgw-wenkai-screen-webfont`。
*   **OCI 配置**: 已设置 `S3_BATCH_DELETE=false`, `S3_ACL=none`, `S3_PERMISSION=` (空)。
*   **内容分发脚本**: `content_sync.py` 支持 `--target ghost|bookstack`、`--all`、`--status` 参数。
