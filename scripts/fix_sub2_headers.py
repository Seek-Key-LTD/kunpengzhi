#!/usr/bin/env python3
"""添加 ### 第三层级标题"""

import re
from pathlib import Path

def add_third_level(content):
    """把 '## 一、xxx' 改成 '### 一、xxx'"""
    pattern = r'^## ([一二三四五六七八九十百\d]+、) '
    return re.sub(pattern, r'### \1', content, flags=re.MULTILINE)

def main():
    base = Path('/Users/ben/code/kunpengzhi')
    
    for series in ['牧月记', '牧兰记', '牧人记', '双约记']:
        for f in (base / 'content' / series).glob('*.md'):
            if f.name in ['目录.md', '00_序言.md']:
                continue
            
            c = f.read_text(encoding='utf-8')
            nc = add_third_level(c)
            if nc != c:
                print(f'修复: {f.name}')
                f.write_text(nc, encoding='utf-8')

if __name__ == '__main__':
    main()
