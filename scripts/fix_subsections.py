#!/usr/bin/env python3
"""直接修复子章节格式"""

import re
from pathlib import Path

def fix_subsections(content):
    """把 '第一节：xxx' 改成 '## 第一节：xxx'"""
    lines = content.split('\n')
    result = []
    in_frontmatter = False
    found_chapter = False
    
    for line in lines:
        stripped = line.strip()
        
        # 跳过 front matter
        if stripped == '---':
            in_frontmatter = not in_frontmatter
            result.append(line)
            continue
        
        if in_frontmatter:
            result.append(line)
            continue
        
        # 检测到章节标题后
        if found_chapter:
            # 已经是 ## 或 ### 的跳过
            if stripped.startswith('## ') or stripped.startswith('### '):
                result.append(line)
                continue
            
            # 检测子章节格式
            # "第一节 xxx" 或 "第一节：xxx" 或 "一、xxx"
            if re.match(r'^[一二三四五六七八九十百\d]+、', stripped):
                result.append(f'## {stripped}')
                continue
            if re.match(r'^第[一二三四五六七八九十百\d]+[节章段：]', stripped):
                result.append(f'## {stripped}')
                continue
        
        # 检测章节标题
        if stripped.startswith('# '):
            found_chapter = True
        
        result.append(line)
    
    return '\n'.join(result)

def main():
    base = Path('/Users/ben/code/kunpengzhi')
    
    for series in ['牧月记', '牧兰记', '牧人记', '双约记']:
        for f in (base / 'content' / series).glob('*.md'):
            if f.name in ['目录.md', '00_序言.md']:
                continue
            
            c = f.read_text(encoding='utf-8')
            nc = fix_subsections(c)
            if nc != c:
                print(f'修复: {f.name}')
                f.write_text(nc, encoding='utf-8')

if __name__ == '__main__':
    main()
