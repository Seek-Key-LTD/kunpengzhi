#!/usr/bin/env python3
"""
为 Book 主题的章节文件添加 weight 参数
"""

import re
from pathlib import Path


def add_weight_to_chapter(file_path):
    """为章节文件添加 weight 参数"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经有 weight
    if 'weight:' in content:
        return False
    
    # 提取章节号
    filename = file_path.stem
    match = re.search(r'第(\d+)[章回]', filename)
    if not match:
        return False
    
    weight = int(match.group(1))
    
    # 在 frontmatter 中添加 weight
    # 找到第一个 --- 之后的位置
    lines = content.split('\n')
    new_lines = []
    inserted = False
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        # 在 title 行之后插入 weight
        if not inserted and line.startswith('title:'):
            new_lines.append(f'weight: {weight}')
            inserted = True
    
    new_content = '\n'.join(new_lines)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def main():
    content_dir = Path('content')
    
    chapters_modified = 0
    
    # 遍历所有章节目录
    for section_dir in ['牧人记', '牧兰记', '牧月记', '双约记', '词根考据']:
        dir_path = content_dir / section_dir
        if not dir_path.exists():
            continue
        
        for md_file in dir_path.glob('*.md'):
            if md_file.name == '目录.md' or md_file.name == '_index.md':
                continue
            
            if add_weight_to_chapter(md_file):
                print(f"✅ {md_file.relative_to(content_dir)}")
                chapters_modified += 1
    
    print(f"\n{'='*60}")
    print(f"✅ 完成! 共修改 {chapters_modified} 个章节文件")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
