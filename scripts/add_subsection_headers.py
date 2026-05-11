#!/usr/bin/env python3
"""
为子章节添加 ## 标题
"""

import re
from pathlib import Path

def add_subsection_headers(content):
    """为子章节添加 ## 标题"""
    lines = content.split('\n')
    result = []
    frontmatter_ended = False
    chapter_header_added = False
    
    for line in lines:
        # 检测 front matter 结束
        if line.strip() == '---':
            if not frontmatter_ended:
                frontmatter_ended = True
            else:
                frontmatter_ended = False
            result.append(line)
            continue
        
        if frontmatter_ended:
            stripped = line.strip()
            
            # 已经是 ## 或 ### 的跳过
            if stripped.startswith('## ') or stripped.startswith('### '):
                result.append(line)
                continue
            
            # 检测章节标题（# 开头）
            if stripped.startswith('# '):
                chapter_header_added = True
                result.append(line)
                continue
            
            # 检测子章节：第一节、第二节、第三节...或 一、二、三、
            if chapter_header_added:
                # "第一节 xxx" 或 "第一节：xxx"
                if re.match(r'^[一二三四五六七八九十百\d]+、', stripped) or \
                   re.match(r'^第[一二三四五六七八九十百\d]+[节章段]', stripped):
                    result.append(f'## {stripped}')
                    continue
            
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
        
        for md_file in sorted(dir_path.glob('*.md')):
            if md_file.name == '目录.md' or md_file.name.startswith('00_'):
                continue
            
            content = md_file.read_text(encoding='utf-8')
            new_content = add_subsection_headers(content)
            
            if new_content != content:
                print(f"  修复: {md_file.name}")
                md_file.write_text(new_content, encoding='utf-8')
            else:
                print(f"  无需修改: {md_file.name}")
    
    print("\n完成！")

if __name__ == '__main__':
    main()
