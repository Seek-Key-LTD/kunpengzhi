<<<<<<< HEAD
# Wiki.js 内容分支

## 分支说明

`wikijs-new` 分支用于存储 Wiki.js 知识库的内容文件,通过 GitLab CI/CD 自动同步到阿里云 Codeup。

## 目录结构

```
├── shuangyueji/          # 双约记
├── murenji/              # 牧人三部曲
│   ├── history-chapters/ # 历史篇章节
│   ├── geology-chapters/ # 地质篇章节
│   └── technology-chapters/ # 技术篇章节
└── etymology/            # 词根研究
```

## 自动化部署

本分支配置了 GitLab CI/CD 流水线,推送到此分支后会自动同步到阿里云 Codeup 仓库。

### CI/CD 配置

- **触发条件**: 仅当 `wikijs-new` 分支有提交时触发
- **目标仓库**: 阿里云 Codeup (https://codeup.aliyun.com/698053416ec1ba182dc6e452/seekkey/kunpengzhi.git)
- **认证方式**: 使用 Yunxiao Access Token

### 环境变量

需要在 GitLab 项目设置中配置以下 CI/CD 变量:
- `YUNXIAO_ACCESS_TOKEN`: 阿里云 Codeup 访问令牌

## 工作流程

1. 在本地修改文档内容
2. 提交到 `wikijs-new` 分支
3. GitLab Runner 自动执行同步任务
4. 内容推送到阿里云 Codeup
5. Wiki.js 从 Codeup 拉取最新内容

## 注意事项

- 所有 Markdown 文件都包含 Wiki.js 兼容的 frontmatter
- 避免在此分支进行大型重构操作
- 确保推送前已解决所有合并冲突
=======
# 鲲鹏志 (Kunpengzhi: The Kun-Peng Chronicles)

> "Once upon a time on a horseback."

鲲鹏志是一个宏大的跨学科叙事项目，旨在通过地缘政治、技术演进、地质变迁及词源考据，构建一套完整的文明路由逻辑。

## 项目结构 (Project Structure)

本项目由四个核心部分组成，分为前期构筑的“牧人三部曲”与今年完成的“双约记”。

### 1. 牧人三部曲 (The Shepherd Trilogy)
*创作于 2026 年之前。*

这三部曲带有浓厚的“智慧设定论”色彩。它通过对历史、地质与技术的深度审计，暗示在宏大叙事的背景下，必然存在一个引导文明进程的“牧者”。

*   **牧人记：历史篇 (Chronicles of the Shepherd: History)**
*   **牧兰记：地质篇 (Chronicles of the Shepherd: Geology)**
*   **牧月记：技术篇 (Chronicles of the Shepherd: Technology)**

### 2. 双约记 (A Tale of Two Treaties)
*创作于 2026 年。*

《双约记》聚焦于近现代及未来的地缘政治格局，通过对雅尔塔体系、冷战铁幕及全球文明解耦的分析，探讨文明在不同“条约”与“契约”下的演化路径。

---

## 发布与存储说明 (Publishing & Storage)

本项目采用多分支自动化发布工作流：

*   **`main` 分支**：Ghost 博客发布端。存放经过排版优化的 Markdown 内容，通过 `ghost_sync.py` 自动同步至 [blog.seekkey.eu.org](https://blog.seekkey.eu.org)。
*   **`wikijs` 分支**：Wiki.js 知识库后端。存放颗粒度极细的考据底稿、词源节点及知识图谱。
*   **`infra` 分支**：基础设施。存放所有同步脚本、CI/CD 配置及维护工具。

## 审美与排版 (Aesthetics)
项目在 Ghost 与 Wiki.js 端均推荐使用 **LXGW WenKai (霞鹜文楷)** 字体，以保持古典人文与现代学术的视觉平衡。
>>>>>>> main
