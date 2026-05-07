# Agents Activity Tracker

本文档由 AI Agent 实时维护，用于记录当前项目的工程进度与状态。

## 当前状态 (Current Status)

### 1. 基础设施 (Infrastructure)
*   [x] **Ghost 同步引擎**：`ghost_sync.py` 修复了 Lexical 结构兼容性问题，支持强力注入自定义 CSS。
*   [x] **仓库重构**：实现了“代码与内容分离”。`infra` 分支作为脚本库，`wikijs` 分支作为纯净内容库，`main` 分支作为发布端。
*   [x] **S3 兼容性修复**：针对甲骨文云（OCI）对象存储，修复了批量删除（400 Error）及隐私警报（Bucket Listing）问题。

### 2. 内容发布 (Publishing)
*   [x] **双约记：第一章**：已成功推送至 Ghost 博客，并应用了文楷字体。
*   [ ] **批量搬迁**：计划将牧人三部曲及双约记剩余章节批量推送到 Ghost。

## 待办事项 (Next Steps)

*   [ ] **Wiki.js 初始化**：将 `wikijs` 分支推送到远程仓库，触发 Wiki.js 的 Git Storage 同步。
*   [ ] **英文版管线**：建立自动化翻译脚本，探索将内容发布为英文版的可能性。
*   [ ] **CI/CD 联调**：确保 GitLab CI 能在 `main` 分支更新时稳定触发 Ghost 同步。

## 备注 (Notes)
*   **字体 CDN**: 目前统一使用 `npm.elemecdn.com/lxgw-wenkai-screen-webfont`。
*   **OCI 配置**: 已设置 `S3_BATCH_DELETE=false`, `S3_ACL=none`, `S3_PERMISSION=` (空)。
