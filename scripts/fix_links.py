#!/usr/bin/env python3
"""
修复 Hugo Book 主题的 Markdown 链接
为相对链接添加 .md 扩展名
"""

import os
import re
from pathlib import Path


def fix_links_in_file(file_path):
    """修复单个文件中的链接"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # 匹配 [text](relative-link) 格式的链接，排除外部链接和图片
    # 只处理不以 http://, https://, mailto:, # 开头的链接
    def add_md_extension(match):
        full_match = match.group(0)
        text = match.group(1)
        url = match.group(2)
        
        # 跳过外部链接、锚点、已经是 .md 的链接
        if url.startswith(('http://', 'https://', 'mailto:', '#', '/')):
            return full_match
        
        if url.endswith('.md'):
            return full_match
        
        # 添加 .md 扩展名
        return f'[{text}]({url}.md)'
    
    # 匹配 [text](url) 但不匹配 ![alt](url)
    pattern = r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)'
    content = re.sub(pattern, add_md_extension, content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    content_dir = Path('content')
    
    if not content_dir.exists():
        print(f"❌ 错误: 目录 '{content_dir}' 不存在")
        return
    
    md_files = list(content_dir.rglob('*.md'))
    print(f"🔍 找到 {len(md_files)} 个 Markdown 文件\n")
    
    fixed_count = 0
    for file_path in md_files:
        if fix_links_in_file(file_path):
            print(f"✅ 修复: {file_path.relative_to(content_dir)}")
            fixed_count += 1
    
    print(f"\n{'='*60}")
    print(f"✅ 完成! 共修复 {fixed_count} 个文件")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
