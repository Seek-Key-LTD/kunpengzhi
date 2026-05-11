#!/usr/bin/env python3
"""修复 description"""

import re
from pathlib import Path

def fix_description(content):
    """修复 description"""
    pattern = r'(description:\s*["\'][^"\']* - )([^"\']*第[一二三四五六七八九十百\d]+章)\s+([^\'"]+)(["\'])'
    def replacer(m):
        prefix = m.group(1)
        before = m.group(2)
        rest = m.group(3)
        suffix = m.group(4)
        return f'{prefix}{before}：{rest}{suffix}'
    return re.sub(pattern, replacer, content)

content_dir = Path('content')
for series in ['牧月记', '牧兰记', '牧人记']:
    for f in (content_dir / series).glob('第*.md'):
        c = f.read_text(encoding='utf-8')
        new_c = fix_description(c)
        if new_c != c:
            print(f'修复 description: {f.name}')
            f.write_text(new_c, encoding='utf-8')
print('完成')
