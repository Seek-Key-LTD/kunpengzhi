#!/usr/bin/env python3
"""
修复已重命名文件的内容：将空格改为冒号
"""

import re
from pathlib import Path

def chapter_number_to_chinese(n):
    if n == 1: return '一'
    if n == 2: return '二'
    if n == 3: return '三'
    if n == 4: return '四'
    if n == 5: return '五'
    if n == 6: return '六'
    if n == 7: return '七'
    if n == 8: return '八'
    if n == 9: return '九'
    if n == 10: return '十'
    if n < 20: return '十' + chapter_number_to_chinese(n - 10)
    if n < 100:
        tens = n // 10
        ones = n % 10
        if ones == 0:
            return chapter_number_to_chinese(tens) + '十'
        return chapter_number_to_chinese(tens) + '十' + chapter_number_to_chinese(ones)
    return str(n)

def fix_content(content, filename):
    """修复文件内容中的空格为冒号"""
    # 匹配第一章 到 第二十二章 格式（文件名已经是中文格式了）
    pattern = r'^(第[一二三四五六七八九十百\d]+章)\s+([^ \n].*)$'
    
    def replacer(m):
        chapter = m.group(1)
        rest = m.group(2)
        return f'{chapter}：{rest}'
    
    result = re.sub(pattern, replacer, content, flags=re.MULTILINE)
    return result

def process_directory(base_path, dirname):
    """处理一个目录下的所有章节文件"""
    dir_path = base_path / dirname
    if not dir_path.exists():
        print(f"目录不存在: {dir_path}")
        return
    
    files = list(dir_path.glob("第*.md"))
    print(f"\n处理 {dirname}/ ({len(files)} 个文件)")
    
    for filepath in sorted(files):
        content = filepath.read_text(encoding='utf-8')
        new_content = fix_content(content, filepath.name)
        
        if new_content != content:
            print(f"  修复: {filepath.name}")
            filepath.write_text(new_content, encoding='utf-8')
        else:
            print(f"  无需修改: {filepath.name}")

def fix_toc(content):
    """修复目录.md中的链接"""
    # [第一章 xxx] -> [第一章：xxx]
    pattern = r'(\[第[一二三四五六七八九十百\d]+章)\s+([^\]]+)'
    result = re.sub(pattern, r'\g<1>：\2', content)
    return result

def main():
    base_path = Path("/Users/ben/code/kunpengzhi")
    content_dir = base_path / "content"
    
    series_to_process = ['牧月记', '牧兰记', '牧人记']
    
    for series in series_to_process:
        process_directory(content_dir, series)
        
        # 处理目录.md
        toc_path = content_dir / series / "目录.md"
        if toc_path.exists():
            content = toc_path.read_text(encoding='utf-8')
            new_content = fix_toc(content)
            if new_content != content:
                print(f"  修复目录链接: {series}/目录.md")
                toc_path.write_text(new_content, encoding='utf-8')
    
    print("\n" + "="*50)
    print("内容修复完成！")

if __name__ == "__main__":
    main()
