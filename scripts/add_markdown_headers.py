#!/usr/bin/env python3
"""
为所有章节添加 Markdown 标题层级：
- 章节标题：# 
- 小节（如"第一节"）：##
- 子子节：###
"""

import re
from pathlib import Path

def add_headers(content):
    """为内容添加 Markdown 标题"""
    lines = content.split('\n')
    result = []
    in_frontmatter = False
    frontmatter_done = False
    
    for i, line in enumerate(lines):
        # 检测 front matter 结束
        if line == '---':
            if not in_frontmatter:
                in_frontmatter = True
            else:
                frontmatter_done = True
                in_frontmatter = False
        
        # front matter 后，第一行非空内容就是章节标题
        if frontmatter_done and i == lines.index(next(l for l in lines if l.strip() and not l.startswith('---') and lines.index(l) > 2)):
            # 找到第一行真正的内容
            pass
        
        result.append(line)
    
    return '\n'.join(result)

def fix_series(base_path, series_name):
    """处理一个系列的所有章节"""
    dir_path = base_path / 'content' / series_name
    if not dir_path.exists():
        return
    
    for md_file in sorted(dir_path.glob('*.md')):
        if md_file.name == '目录.md' or md_file.name.startswith('00_'):
            continue
        
        print(f"处理: {md_file.name}")
        content = md_file.read_text(encoding='utf-8')
        new_content = add_markdown_headers(content, md_file.name)
        md_file.write_text(new_content, encoding='utf-8')

def add_markdown_headers(content, filename):
    """为文件添加 Markdown 标题"""
    lines = content.split('\n')
    result = []
    in_frontmatter = False
    frontmatter_ended = False
    chapter_title_added = False
    
    for i, line in enumerate(lines):
        # 检测 front matter
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
            else:
                in_frontmatter = False
                frontmatter_ended = True
            result.append(line)
            continue
        
        if in_frontmatter:
            result.append(line)
            continue
        
        # front matter 结束后，处理正文
        if frontmatter_ended and not chapter_title_added:
            if line.strip():
                # 这行应该是章节标题
                result.append(f'# {line}')
                chapter_title_added = True
                result.append('')  # 空行
            else:
                result.append(line)
            continue
        
        # 处理章节内的子标题
        if chapter_title_added:
            stripped = line.strip()
            
            # 检测"第一节"、"第二节"等
            if re.match(r'^[一二三四五六七八九十百\d]+、', stripped):
                result.append(f'## {stripped}')
            # 检测"一、" "二、"等
            elif re.match(r'^[一二三四五六七八九十百\d]+、', stripped):
                result.append(f'## {stripped}')
            # 检测"楔子" "尾声" "序言"等
            elif re.match(r'^(楔子|尾声|序章|序言|引言|引子)[\s·]', stripped):
                result.append(f'## {stripped}')
            # 检测"### "已经在用的
            elif stripped.startswith('### '):
                result.append(line)
            # 检测"## "已经在用的
            elif stripped.startswith('## '):
                result.append(line)
            else:
                result.append(line)
        else:
            result.append(line)
    
    return '\n'.join(result)

def main():
    base_path = Path('/Users/ben/code/kunpengzhi')
    
    for series in ['牧月记', '牧兰记', '牧人记', '双约记']:
        dir_path = base_path / 'content' / series
        if not dir_path.exists():
            continue
        
        print(f"\n{'='*50}")
        print(f"处理 {series}/")
        print('='*50)
        
        for md_file in sorted(dir_path.glob('*.md')):
            if md_file.name == '目录.md' or md_file.name.startswith('00_'):
                print(f"跳过: {md_file.name}")
                continue
            
            print(f"处理: {md_file.name}")
            content = md_file.read_text(encoding='utf-8')
            new_content = add_markdown_headers(content, md_file.name)
            
            if new_content != content:
                md_file.write_text(new_content, encoding='utf-8')
                print(f"  ✓ 已添加标题")
            else:
                print(f"  - 无需修改")
    
    print("\n" + "="*50)
    print("完成！")

if __name__ == '__main__':
    main()
