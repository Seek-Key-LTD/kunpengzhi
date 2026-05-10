# 鲲鹏志 (Kunpengzhi: The Kun-Peng Chronicles)

> "Once upon a time on a horseback."

鲲鹏志是一个宏大的跨学科叙事项目，旨在通过地缘政治、技术演进、地质变迁及词源考据，构建一套完整的文明路由逻辑。

## 项目结构 (Project Structure)

本项目由四个核心部分组成，分为前期构筑的“牧人三部曲”与今年完成的“双约记”。

### 1. 牧人三部曲 (The Shepherd Trilogy)
*创作于 2026 年之前。*

*   **牧人记：历史篇 (Chronicles of the Shepherd: History)**
*   **牧兰记：地质篇 (Chronicles of the Shepherd: Geology)**
*   **牧月记：技术篇 (Chronicles of the Shepherd: Technology)**

### 2. 双约记 (A Tale of Two Treaties)
*创作于 2026 年。*

《双约记》聚焦于近现代及未来的地缘政治格局，通过对雅尔塔体系、冷战铁幕及全球文明解耦的分析。

---

## 分支策略 (Branching Strategy)

本项目采用多分支工作流，确保内容生产与多端发布的解耦：

*   **`main` 分支 (Source)**：**内容源头与分发中心**。
    - 存储原始稿件 (`murenji/*.md`, `shuangyueji.md`)。
    - 存储词源考据底稿 (`etymology/`)。
    - 负责执行章节拆分、元数据注入等预处理任务。
    - 保持结构稳健，不承担具体的 APP 发布配置。
*   **`wikijs` 分支**：Wiki.js 知识库专用。包含针对 Wiki.js 优化的路径结构、中文文件名及特定 frontmatter。
*   **`ghost` 分支**：Ghost 博客发布专用。包含经过排版优化的内容及同步脚本。
*   **`develop` 分支**：开发与实验性功能。

## 目录结构 (Directory Structure)

```
├── murenji/              # 牧人三部曲原始稿件
│   ├── history-chapters/ # 历史篇章节 (自动生成)
│   ├── geology-chapters/ # 地质篇章节 (自动生成)
│   └── technology-chapters/ # 技术篇章节 (自动生成)
├── shuangyueji/          # 双约记章节 (自动生成)
├── etymology/            # 词根研究
├── MANIFEST.md           # 内容清单与拆分进度
└── README.md             # 项目说明
```

---

## 自动化说明

推送至 `main` 分支后，相关脚本会自动化执行内容校验与初步处理，并作为上游源同步至各发布分支。
