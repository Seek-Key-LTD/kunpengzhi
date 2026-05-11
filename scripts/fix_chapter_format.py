#!/usr/bin/env python3
"""
修复文件名和标题格式：
1. 第01章 xxx → 第一章：xxx (去掉前导零，空格改冒号)
2. 更新 front matter 中的 title
3. 更新正文中的章节标题
4. 更新目录链接
"""

import re
import os
from pathlib import Path

def chapter_number_to_chinese(n):
    """将数字转换为中文"""
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
            return chapter_number_to_chinese(tents) + '十'
        return chapter_number_to_chinese(tens) + '十' + chapter_number_to_chinese(ones)
    return str(n)

def fix_chapter_filename(filename):
    """将 '第01章 xxx' 转换为 '第一章：xxx'"""
    pattern = r'^第(\d+)章\s+(.*)$'
    match = re.match(pattern, filename)
    if match:
        num = int(match.group(1))
        rest = match.group(2)
        chinese = chapter_number_to_chinese(num)
        return f"第{chinese}章：{rest}"
    return None

def fix_content(content, old_name, new_name):
    """修复文件内容中的标题和链接"""
    # 解析旧文件名
    old_match = re.match(r'^第(\d+)章\s+(.*)$', old_name)
    if not old_match:
        return content
    
    old_num = int(old_match.group(1))
    old_chinese = f"第{chapter_number_to_chinese(old_num)}章"
    
    # 解析新文件名
    new_match = re.match(r'^第(\d+)章：(.*)$', new_name)
    if not new_match:
        return content
    
    new_chinese = f"第{chapter_number_to_chinese(old_num)}章"  # 用旧数字转换
    
    result = content
    
    # 1. 修复 front matter 中的 title (有引号)
    # 匹配: title: "第1章 xxx" 或 title: '第1章 xxx'
    title_pattern1 = rf'(title:\s*["\'])第\d+章\s+([^"\']+)(["\'])'
    result = re.sub(title_pattern1, f'\\g<1>{new_chinese}：\\2\\3', result)
    
    # 2. 修复 front matter 中的 title (无引号)
    title_pattern2 = rf'(title:\s*)第\d+章\s+([^"\']+?)(?:\s*["\']|$)'
    def fix_title2(m):
        prefix = m.group(1)
        title = m.group(2).rstrip()
        return f'{prefix}"{new_chinese}：{title}"'
    result = re.sub(title_pattern2, fix_title2, result)
    
    # 3. 修复正文标题行 - 第一行通常是章节标题
    # 匹配独立一行的 "第一章 xxx" (不带 # 的)
    body_pattern1 = rf'^({old_chinese}\s+.+)$'
    result = re.sub(body_pattern1, lambda m: new_chinese + '：' + m.group(1).lstrip()[len(old_chinese)+1:], result, flags=re.MULTILINE)
    
    # 4. 修复带 # 的标题行
    body_pattern2 = rf'^(#{1,6}\s+){old_chinese}\s+(.+)$'
    result = re.sub(body_pattern2, f'\\g<1>{new_chinese}：\\2', result, flags=re.MULTILINE)
    
    # 5. 修复目录中的链接
    link_pattern = rf'\[({old_chinese}\s+[^\]]+)\]\((?:第\d+章\s+)?([^)]+)\)'
    def fix_link(m):
        title = m.group(1)
        # 去掉旧的中文章节号前缀
        fixed_title = new_chinese + '：' + title[len(old_chinese)+1:]
        return f'[{fixed_title}]({new_name})'
    result = re.sub(link_pattern, fix_link, result)
    
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
        old_name = filepath.stem  # 不含扩展名
        new_name = fix_chapter_filename(old_name)
        
        if new_name and new_name != old_name:
            print(f"  {old_name}")
            print(f"  → {new_name}")
            
            content = filepath.read_text(encoding='utf-8')
            new_content = fix_content(content, old_name, new_name)
            filepath.write_text(new_content, encoding='utf-8')
            
            new_path = filepath.parent / (new_name + ".md")
            filepath.rename(new_path)
        else:
            status = "(无需修改)" if new_name else "(跳过)"
            print(f"  {old_name} {status}")

def fix_toc(content):
    """修复目录.md中的链接"""
    def replacer(m):
        chinese = m.group(1)
        title = m.group(2)
        return f'[第{chinese}章：{title}](第{chinese}章：{title})'
    
    result = re.sub(
        r'\[第([一二三四五六七八九十百]+)章\s+([^\]]+)\]\(第\d+章\s+([^)]+)\)',
        replacer,
        content
    )
    return result

def main():
    base_path = Path("/Users/ben/code/kunpengzhi")
    content_dir = base_path / "content"
    
    series_to_process = ['牧月记', '牧兰记', '牧人记']
    
    for series in series_to_process:
        process_directory(content_dir, series)
        
        toc_path = content_dir / series / "目录.md"
        if toc_path.exists():
            print(f"\n处理 {series}/目录.md")
            content = toc_path.read_text(encoding='utf-8')
            new_content = fix_toc(content)
            toc_path.write_text(new_content, encoding='utf-8')
            print("  已更新目录链接格式")
    
    print("\n" + "="*50)
    print("修复完成！")

if __name__ == "__main__":
    main()
