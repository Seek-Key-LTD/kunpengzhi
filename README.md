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
