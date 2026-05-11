#!/usr/bin/env python3
"""
修复 Book 主题的标题结构
确保每个章节有正确的 H1/H2/H3 层级
"""

import re
from pathlib import Path


def fix_headings(content, filename):
    """修复标题层级"""
    lines = content.split('\n')
    new_lines = []
    
    # 提取章节号用于生成 H1
    match = re.search(r'第(\d+)[章回]', filename)
    chapter_num = match.group(1) if match else ''
    
    in_frontmatter = False
    frontmatter_done = False
    first_heading_added = False
    
    for i, line in enumerate(lines):
        # 处理 frontmatter
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
            else:
                in_frontmatter = False
                frontmatter_done = True
            new_lines.append(line)
            continue
        
        if in_frontmatter:
            new_lines.append(line)
            continue
        
        # 在 frontmatter 之后添加 H1 标题
        if frontmatter_done and not first_heading_added and line.strip() and not line.startswith('#'):
            # 从 frontmatter 中提取 title
            title_match = re.search(r'title:\s*["\'](.+)["\']', content)
            if title_match:
                title = title_match.group(1)
                new_lines.append(f'# {title}\n')
                first_heading_added = True
        
        # 修复现有的标题层级
        # 将 "第一节"、"第二节" 等转换为 ## 
        if re.match(r'^第[一二三四五六七八九十百]+节\s+', line):
            new_lines.append(f'## {line.strip()}')
        # 将 "楔子"、"引子" 等转换为 ##
        elif re.match(r'^(楔子|引子|前言|序言)\s*[·.•]', line):
            new_lines.append(f'## {line.strip()}')
        # 保持其他 # 标题不变
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)


def process_file(file_path):
    """处理单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经有正确的标题结构
    if '# ' in content and '## ' in content:
        return False
    
    fixed_content = fix_headings(content, file_path.stem)
    
    if fixed_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        return True
    return False


def main():
    # 内容直接在项目根目录
    base_dir = Path('.')
    
    files_modified = 0
    
    # 遍历所有章节目录
    for section_dir in ['双约记', '牧人记', '牧兰记', '牧月记', '词根考据']:
        dir_path = base_dir / section_dir
        if not dir_path.exists():
            continue
        
        for md_file in dir_path.glob('*.md'):
            if md_file.name in ['目录.md', '_index.md']:
                continue
            
            if process_file(md_file):
                print(f"✅ {md_file}")
                files_modified += 1
    
    print(f"\n{'='*60}")
    print(f"✅ 完成! 共修复 {files_modified} 个文件的标题结构")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
