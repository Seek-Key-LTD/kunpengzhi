#!/usr/bin/env python3
"""
Hugo 站点链接检查器
自动检测 Markdown 文件中的内部链接是否有效
"""

import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote


class LinkChecker:
    def __init__(self, content_dir):
        self.content_dir = Path(content_dir)
        self.errors = []
        self.warnings = []
        self.checked_files = 0
        self.total_links = 0

    def get_all_md_files(self):
        """获取所有 Markdown 文件"""
        return list(self.content_dir.rglob("*.md"))

    def extract_links(self, content):
        """提取 Markdown 链接 [text](url)"""
        # 匹配 [text](url) 格式，排除图片 ![alt](url)
        pattern = r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)'
        return re.findall(pattern, content)

    def resolve_link(self, link_url, current_file):
        """解析链接路径，返回对应的文件路径"""
        # 跳过外部链接
        if link_url.startswith(('http://', 'https://', 'mailto:', '#')):
            return None

        # 移除锚点
        link_url = link_url.split('#')[0]

        if not link_url:
            return None

        # 处理相对路径
        if link_url.startswith('/'):
            # 绝对路径，相对于 content 目录
            relative_path = link_url.lstrip('/')
        else:
            # 相对路径，相对于当前文件
            current_dir = current_file.parent
            relative_path = (current_dir / link_url).relative_to(self.content_dir)

        # 尝试多种可能的文件扩展名
        possible_paths = [
            self.content_dir / relative_path,
            self.content_dir / f"{relative_path}.md",
            self.content_dir / f"{relative_path}/_index.md",
            self.content_dir / f"{relative_path}/index.md",
        ]

        for path in possible_paths:
            if path.exists():
                return path

        return None

    def check_file(self, file_path):
        """检查单个文件的链接"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            links = self.extract_links(content)
            self.total_links += len(links)

            for text, url in links:
                resolved = self.resolve_link(url, file_path)

                if resolved is None:
                    # 外部链接或锚点，跳过
                    continue

                if not resolved.exists():
                    error_msg = f"❌ 断链: {file_path.relative_to(self.content_dir)}\n"
                    error_msg += f"   链接文本: {text}\n"
                    error_msg += f"   链接地址: {url}\n"
                    error_msg += f"   目标不存在: {resolved}"
                    self.errors.append(error_msg)

        except Exception as e:
            warning_msg = f"⚠️  读取文件失败: {file_path}\n   错误: {str(e)}"
            self.warnings.append(warning_msg)

    def run(self):
        """运行链接检查"""
        print(f"🔍 开始检查 Hugo 站点链接...\n")
        print(f"📁 内容目录: {self.content_dir}\n")

        md_files = self.get_all_md_files()
        self.checked_files = len(md_files)

        print(f"📄 找到 {len(md_files)} 个 Markdown 文件\n")

        for file_path in md_files:
            self.check_file(file_path)

        # 输出结果
        print("=" * 60)
        print(f"✅ 检查完成!")
        print(f"   - 检查文件数: {self.checked_files}")
        print(f"   - 检查链接数: {self.total_links}")
        print(f"   - 发现错误: {len(self.errors)}")
        print(f"   - 警告信息: {len(self.warnings)}")
        print("=" * 60)

        if self.errors:
            print("\n❌ 发现的断链:\n")
            for error in self.errors:
                print(error)
                print()

        if self.warnings:
            print("\n⚠️  警告信息:\n")
            for warning in self.warnings:
                print(warning)
                print()

        # 返回退出码
        return 0 if not self.errors else 1


def main():
    # 默认检查 content 目录
    content_dir = sys.argv[1] if len(sys.argv) > 1 else "content"

    if not os.path.isdir(content_dir):
        print(f"❌ 错误: 目录 '{content_dir}' 不存在")
        sys.exit(1)

    checker = LinkChecker(content_dir)
    exit_code = checker.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
