# 鲲鹏志 - Hugo 静态网站发布分支 (hugo branch)

> "本项目通过 Hugo 驱动，实现《鲲鹏志》全书的静态网页展示与分发。"

本分支是《鲲鹏志》项目的 **Hugo 发布端**，专门用于构建并部署静态网站（GitHub Pages / 华为云等）。它从 `main` 分支接收规格化的内容，并通过 Hugo 模板进行排版优化。

## 本地开发 (Local Development)

在本机运行前，请确保已安装 [Hugo](https://gohugo.io/installation/)（推荐 v0.159.0+）。

1.  **克隆主题** (如果 `themes/ananke` 为空):
    ```bash
    git clone --depth 1 https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke
    ```

2.  **本地预览**:
    ```bash
    hugo server -D
    ```
    访问 `http://localhost:1313` 即可预览。

3.  **手动构建**:
    ```bash
    hugo --minify
    ```

## 目录结构说明 (Structure)

本分支遵循 Hugo 标准目录结构：

*   `content/`：存放全书 Markdown 源码（由 `main` 分支同步而来）。
    *   `牧人记/`、`牧兰记/`、`牧月记/`、`双约记/`
*   `themes/ananke`：使用的前端主题。
*   `layouts/shortcodes/`：自定义的音视频嵌入组件。
*   `hugo.toml`：Hugo 核心配置文件。
*   `.github/workflows/deploy.yml`：GitHub Actions 自动部署脚本。

## 自动化部署 (CI/CD)

*   **同步流**：GitLab (origin) -> GitHub (github) & 阿里云 (aliyun)。
*   **发布流**：每次推送到本分支的 `hugo` 分支时，GitHub Actions 会自动触发构建，并将结果部署至 [kunpengzhi.fun](https://kunpengzhi.fun/)。

---

## 注意事项

1.  **元数据冲突**：本分支的文件 Frontmatter 已将 `published` 字段更名为 `is_published`，以避免 Hugo 内置日期解析器报错。
2.  **内容修改**：如需修改书稿内容，请优先在 `main` 分支进行，由同步脚本自动分发至本分支。本分支主要负责**配置、样式与发布逻辑**的迭代。

---
[返回项目全景 MANIFEST.md](./MANIFEST.md) | [查看同步状态 agents.md](./agents.md)
