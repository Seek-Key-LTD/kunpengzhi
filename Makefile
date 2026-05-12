.PHONY: help serve build check-links clean

help: ## 显示帮助信息
	@echo "鲲鹏志 Hugo 站点管理"
	@echo ""
	@echo "可用命令:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' \$(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", \$\$1, \$\$2}'

serve: ## 启动开发服务器（带草稿）
	hugo server --buildDrafts

serve-production: ## 启动生产环境服务器
	hugo server

build: ## 构建静态站点
	hugo --minify

check-links: ## 检查内部链接有效性
	python3 scripts/check_links.py content

fix-headings: ## 修复章节标题结构
	python3 scripts/fix_headings.py

fix-links: ## 修复相对链接（添加.md扩展名）
	python3 scripts/fix_links.py

clean: ## 清理生成的文件
	rm -rf public/ resources/

lint: check-links ## 代码检查（别名）

test: check-links ## 运行测试（别名）
