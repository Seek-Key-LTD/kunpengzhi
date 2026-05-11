#!/usr/bin/env python3
"""
修复 front matter 中的 title：将空格改为冒号
"""

import re
from pathlib import Path

def fix_frontmatter(content):
    """修复 front matter 中的 title"""
    # 匹配 title: "第X章 xxx" 或 title: "牧X记 - 第X章 xxx"
    pattern = r'(title:\s*["\'])([^"\']*第[一二三四五六七八九十百\d]+章)\s+([^"\']+)(["\'])'
    
    def replacer(m):
        prefix = m.group(1)
        before = m.group(2)  # 如 "牧月记 - 第一章" 或 "第一章"
        rest = m.group(3)
        suffix = m.group(4)
        return f'{prefix}{before}：{rest}{suffix}'
    
    result = re.sub(pattern, replacer, content)
    return result

def process_directory(base_path, dirname):
    """处理一个目录下的所有章节文件"""
    dir_path = base_path / dirname
    if not dir_path.exists():
        return
    
    files = list(dir_path.glob("第*.md"))
    print(f"\n处理 {dirname}/ ({len(files)} 个文件)")
    
    for filepath in sorted(files):
        content = filepath.read_text(encoding='utf-8')
        new_content = fix_frontmatter(content)
        
        if new_content != content:
            print(f"  修复: {filepath.name}")
            filepath.write_text(new_content, encoding='utf-8')
        else:
            print(f"  无需修改: {filepath.name}")

def main():
    base_path = Path("/Users/ben/code/kunpengzhi")
    content_dir = base_path / "content"
    
    for series in ['牧月记', '牧兰记', '牧人记']:
        process_directory(content_dir, series)
    
    print("\n" + "="*50)
    print("Front matter 修复完成！")

if __name__ == "__main__":
    main()
